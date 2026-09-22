"""Local HTTP policy server for Octo 1.0 (rail-berkeley/octo-small, octo-base) on CPU JAX.

Runs inside the isolated `.venv-policy` environment (Python 3.11, jax 0.4.20 CPU,
tensorflow 2.15 CPU, octo @ 653c54a). It ports the pre/post-processing of
SimplerEnv's `simpler_env/policies/octo/octo_model.py` (widowx_bridge setup):
  * lanczos3 antialiased resize to 256x256, uint8
  * image history of 2 frames with pad_mask, Octo 1.0 `observations["pad_mask"]` convention
  * per-step PRNG split, 5 warm-up splits after seeding (matches SIMPLER)
  * un-normalisation with the statistics of the setup's dataset (bridge_dataset for widowx_bridge,
    fractal20220817_data for google_robot)
  * action ensembling over the 4-step prediction horizon (temperature 0)
  * roll/pitch/yaw -> axis-angle with transforms3d euler2axangle (static xyz), the
    convention used by the original SIMPLER `main` branch
  * gripper: widowx_bridge binarises to +1 (open) / -1 (close); google_robot emits the relative
    action with the sticky-gripper latch (sticky_gripper_num_repeat=15), which that embodiment
    requires -- without it its success rate is ~0

Both SIMPLER embodiments are served by one process: `policy_setup` is per session (a /reset field), so a
single pair of servers covers the Bridge and fractal suites rather than four servers on an 8 GB card.

The server keeps one episode state per session id (JSON field 'session' on /reset, header X-Session on /step;
default 'default'). Two concurrent clients must use different session ids.
It is a research tool, not a benchmark reproduction: the simulator side decides
what the actions mean.
"""
import argparse
import json
import os
import sys
import threading
import time
import types
from collections import deque
from functools import partial
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

os.environ.setdefault("JAX_PLATFORMS", "cpu")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

import numpy as np


class OctoPolicy:
    def __init__(self, model_type: str, horizon: int = 2, pred_action_horizon: int = 4,
                 image_size: int = 256, action_scale: float = 1.0):
        import jax
        import jax.numpy as jnp
        from octo.model.octo_model import OctoModel

        self.jax, self.jnp = jax, jnp
        self.model_type = model_type
        self.hf_id = f"hf://rail-berkeley/{model_type}"
        t0 = time.perf_counter()
        self.model = OctoModel.load_pretrained(self.hf_id)
        self.load_seconds = time.perf_counter() - t0
        # One entry per SIMPLER policy setup: (action mean, action std, sticky_gripper_num_repeat).
        # Values follow simpler_env/policies/octo/octo_model.py.
        self.setups = {}
        for setup, dataset_id, sticky in (("widowx_bridge", "bridge_dataset", 1),
                                          ("google_robot", "fractal20220817_data", 15)):
            if dataset_id not in self.model.dataset_statistics:
                raise KeyError(f"{self.hf_id} has no dataset_statistics[{dataset_id!r}] "
                               f"(needed for policy_setup={setup!r})")
            st_ = self.model.dataset_statistics[dataset_id]["action"]
            self.setups[setup] = (np.asarray(st_["mean"], dtype=np.float32),
                                  np.asarray(st_["std"], dtype=np.float32), sticky)
        self.action_mean, self.action_std, _ = self.setups["widowx_bridge"]
        self.horizon = horizon
        self.pred_action_horizon = pred_action_horizon
        self.image_size = image_size
        self.action_scale = action_scale
        self.lock = threading.Lock()
        self._resize = jax.jit(jax.vmap(partial(jax.image.resize, shape=(image_size, image_size, 3),
                                                method="lanczos3", antialias=True)))
        self.reset("warmup", seed=0)
        self.jit_warmup_seconds = None

    # ---- episode state (per session; clients pass a session id so that two concurrent clients never
    # share history / ensemble / instruction state -- incident 2026-09-19, results/contaminated_2026-09-19) --
    def reset(self, instruction: str, seed: int, config: dict = None, session: str = "default"):
        """config: deployment variant (same weights) -- ensemble (bool), exec_horizon (int, open-loop
        chunk length; >1 implies no ensembling), history (int, image window 1..2) -- plus
        policy_setup ('widowx_bridge' | 'google_robot'), which selects the un-normalisation statistics
        and the gripper convention of the embodiment being evaluated."""
        jax = self.jax
        config = config or {}
        st = types.SimpleNamespace()
        st.policy_setup = str(config.get("policy_setup", "widowx_bridge"))
        if st.policy_setup not in self.setups:
            raise ValueError(f"unknown policy_setup {st.policy_setup!r}; have {sorted(self.setups)}")
        st.action_mean, st.action_std, st.sticky_gripper_num_repeat = self.setups[st.policy_setup]
        # Sticky-gripper latch, per session. google_robot holds a commanded gripper change for
        # sticky_gripper_num_repeat steps; widowx_bridge (repeat 1) never engages it.
        st.sticky_action_is_on = False
        st.gripper_action_repeat = 0
        st.sticky_gripper_action = 0.0
        st.previous_gripper_action = None
        st.action_ensemble = bool(config.get("ensemble", True))
        st.exec_horizon = int(config.get("exec_horizon", 1))
        st.horizon = int(config.get("history", 2))
        st.chunk = deque()
        st.instruction = instruction
        st.task = self.model.create_tasks(texts=[instruction])
        st.rng = jax.random.PRNGKey(int(seed))
        for _ in range(5):  # match SIMPLER's octo server seeding
            st.rng, _ = jax.random.split(st.rng)
        st.image_history = deque(maxlen=st.horizon)
        st.num_image_history = 0
        st.action_history = deque(maxlen=self.pred_action_horizon)
        st.step_count = 0
        st.last_used = time.time()
        if not hasattr(self, "sessions"):
            self.sessions = {}
        self.sessions[session] = st
        for k in [k for k, v in self.sessions.items() if k != session and time.time() - v.last_used > 3600]:
            del self.sessions[k]  # drop sessions idle for more than an hour
        self.step_count = sum(v.step_count for v in self.sessions.values())

    def _resize_image(self, image_u8: np.ndarray):
        jnp = self.jnp
        img = self._resize(jnp.asarray(image_u8, dtype=jnp.float32))
        return jnp.clip(jnp.round(img), 0, 255).astype(jnp.uint8)

    def _ensemble(self, st, cur_action):
        # cur_action: (1, pred_horizon, 7). Equal-weight average (temperature 0) of all
        # earlier predictions that targeted the current timestep, as in SIMPLER.
        st.action_history.append(np.asarray(cur_action))
        n = len(st.action_history)
        preds = np.stack([pred[:, i] for i, pred in zip(range(n - 1, -1, -1), st.action_history)])
        return preds.mean(axis=0)  # (1, 7)

    @staticmethod
    def _gripper_action(st, current: float) -> float:
        """Env gripper command for one step, advancing the session's sticky latch.

        widowx_bridge binarises to +1 open / -1 close. google_robot instead sends the *relative*
        action (1 = close, -1 = open) and latches it for sticky_gripper_num_repeat steps, matching the
        real robot; this is the 'alternative implementation' in simpler_env's octo_model.py. Called once
        per environment step, including for each action of an open-loop chunk, so the latch advances in
        step with the simulator.
        """
        if st.policy_setup != "google_robot":
            return 2.0 * float(current > 0.5) - 1.0
        if st.previous_gripper_action is None:
            relative = 0.0
        else:
            relative = float(st.previous_gripper_action - current)
        st.previous_gripper_action = current
        if abs(relative) > 0.5 and st.sticky_action_is_on is False:
            st.sticky_action_is_on = True
            st.sticky_gripper_action = relative
        if st.sticky_action_is_on:
            st.gripper_action_repeat += 1
            relative = st.sticky_gripper_action
        if st.gripper_action_repeat == st.sticky_gripper_num_repeat:
            st.sticky_action_is_on = False
            st.gripper_action_repeat = 0
            st.sticky_gripper_action = 0.0
        return relative

    def step(self, image_u8: np.ndarray, session: str = "default"):
        """image_u8: (H, W, 3) uint8. Returns dict with 7-dim env action and raw action."""
        jax, jnp = self.jax, self.jnp
        from transforms3d.euler import euler2axangle

        t0 = time.perf_counter()
        st = self.sessions.get(session)
        if st is None:
            raise KeyError("unknown session %r: call /reset with this session id first" % session)
        st.last_used = time.time()
        if st.chunk:  # open-loop action chunk: execute stored actions without re-querying the model
            a = st.chunk.popleft()
            st.step_count += 1
            return {"action": a.tolist(), "raw_action": None, "inference_seconds": 0.0, "history_len": 0, "from_chunk": True, "session": session}
        img = self._resize_image(image_u8[None])  # (1, 256, 256, 3)
        st.image_history.append(img)
        st.num_image_history = min(st.num_image_history + 1, st.horizon)
        images = jnp.stack(list(st.image_history), axis=1)  # (1, h, 256, 256, 3)
        h = images.shape[1]
        pad_mask = jnp.ones((1, h), dtype=jnp.float32)
        pad_mask = pad_mask.at[:, : h - min(h, st.num_image_history)].set(0)
        st.rng, key = jax.random.split(st.rng)
        obs = {"image_primary": images, "pad_mask": pad_mask}
        norm = self.model.sample_actions(obs, st.task, rng=key)
        raw = np.asarray(norm) * st.action_std[None] + st.action_mean[None]  # (1, 4, 7)
        assert raw.shape == (1, self.pred_action_horizon, 7), raw.shape

        def to_env_action(r7):
            world = r7[:3] * self.action_scale
            roll, pitch, yaw = [float(v) for v in r7[3:6]]
            ax, ang = euler2axangle(roll, pitch, yaw)  # static xyz, original SIMPLER convention
            rot = np.asarray(ax, dtype=np.float64) * float(ang) * self.action_scale
            gripper = self._gripper_action(st, float(r7[6]))
            return np.concatenate([world.astype(np.float64), rot, [gripper]])

        if st.exec_horizon > 1:  # open-loop chunk: execute the first exec_horizon predicted actions
            k = min(st.exec_horizon, raw.shape[1])
            acts = [to_env_action(raw[0, j]) for j in range(k)]
            st.chunk.extend(acts[1:])
            raw7 = raw[0, 0]
            action = acts[0]
        elif st.action_ensemble:
            raw7 = self._ensemble(st, raw)[0]  # (7,)
            action = to_env_action(raw7)
        else:  # no ensembling: first predicted action only
            raw7 = raw[0, 0]
            action = to_env_action(raw7)
        st.step_count += 1
        self.step_count += 1
        return {"action": action.tolist(), "raw_action": np.asarray(raw7, dtype=float).tolist(),
                "inference_seconds": time.perf_counter() - t0, "history_len": int(h), "from_chunk": False, "session": session}


def make_handler(policy: OctoPolicy, meta: dict):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):  # quiet
            pass

        def _json(self, code, payload):
            body = json.dumps(payload).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path == "/health":
                self._json(200, dict(meta, step_count=policy.step_count, sessions=len(getattr(policy, "sessions", {})), session_isolation=True))
            else:
                self._json(404, {"error": "unknown path"})

        def do_POST(self):
            n = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(n)
            try:
                if self.path == "/reset":
                    req = json.loads(body)
                    session = str(req.get("session", "default"))
                    with policy.lock:
                        policy.reset(req["instruction"], int(req.get("seed", 0)), req.get("config"), session=session)
                    self._json(200, {"ok": True, "instruction": req["instruction"], "session": session})
                elif self.path == "/step":
                    shape = tuple(int(v) for v in self.headers["X-Shape"].split(","))
                    img = np.frombuffer(body, dtype=np.uint8).reshape(shape)
                    session = str(self.headers.get("X-Session", "default"))
                    with policy.lock:
                        out = policy.step(img, session=session)
                    self._json(200, out)
                else:
                    self._json(404, {"error": "unknown path"})
            except Exception as e:  # report to client instead of dying
                self._json(500, {"error": f"{type(e).__name__}: {e}"})

    return Handler


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="octo-small", choices=["octo-small", "octo-base"])
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--host", default="127.0.0.1")
    args = p.parse_args()

    import jax
    t0 = time.perf_counter()
    policy = OctoPolicy(args.model)
    # JIT warm-up with a blank frame so the first real step is not timed as compilation.
    tw = time.perf_counter()
    policy.reset("warmup", seed=0)
    policy.step(np.zeros((480, 640, 3), dtype=np.uint8))
    policy.step(np.zeros((480, 640, 3), dtype=np.uint8))
    policy.jit_warmup_seconds = time.perf_counter() - tw
    policy.reset("idle", seed=0)
    import flax, tensorflow as tf
    meta = dict(model=args.model, hf_id=policy.hf_id, jax=jax.__version__, flax=flax.__version__,
                tensorflow=tf.__version__, numpy=np.__version__, python=sys.version.split()[0],
                jax_backend=jax.default_backend(), load_seconds=policy.load_seconds,
                jit_warmup_seconds=policy.jit_warmup_seconds,
                rotation_convention="transforms3d.euler2axangle(roll,pitch,yaw) static xyz",
                variants="reset config: ensemble(bool), exec_horizon(int), history(int), policy_setup(str)",
                policy_setups={k: {"sticky_gripper_num_repeat": v[2]} for k, v in policy.setups.items()},
                action_mean=policy.action_mean.tolist(), action_std=policy.action_std.tolist(),
                startup_seconds=time.perf_counter() - t0)
    print(json.dumps(meta), flush=True)
    server = ThreadingHTTPServer((args.host, args.port), make_handler(policy, meta))
    print(f"READY {args.host}:{args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
