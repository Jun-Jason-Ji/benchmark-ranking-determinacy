"""Local HTTP policy server for the RT-1 family (TF SavedModel) on CPU TensorFlow.

Runs in `.venv-rt1-win` on the **Windows** side (python 3.11, tensorflow 2.15.0, tf_agents 0.19.0). It is not
in WSL because WSL here ships only python 3.12, which tensorflow 2.15 does not support, and because WSL's
outbound network cannot reach PyPI (the same problem that forces HF_HUB_OFFLINE on the Octo servers). The
ManiSkill2 sweep runs in WSL and reaches this server over 127.0.0.1, as the OpenVLA server is already used.

Ports the pre/post-processing of simpler_env/policies/rt1/rt1_model.py for the `google_robot` setup:
  * tf.image.resize_with_pad to 320x256, uint8
  * Universal Sentence Encoder embedding of the instruction (512,), cached under TFHUB_CACHE_DIR
  * tf_agents SavedModelPyTFEagerPolicy with the policy's recurrent state carried across steps
  * small-action filter on the gripper only (|g| < 1e-2 -> 0), arm movement unfiltered
  * no un-normalisation (that is the widowx_bridge path), rotation read as axis-angle, gripper NOT inverted
  * terminate_episode passed through to the client -- RT-1 predicts episode termination and Octo does not,
    so the caller must honour it (simpler_env's evaluator loops `while not (terminated or truncated)`)

Same wire protocol as scripts/octo_policy_server.py, including per-session state, so the sweep client needs
no special case: POST /reset {instruction, seed, config, session}; POST /step with X-Shape and X-Session
headers and the raw uint8 image as the body; GET /health.

Usage: .venv-rt1-win/Scripts/python.exe scripts/rt1_policy_server.py --checkpoint rt-1-x --port 8773
"""
import argparse
import json
import os
import threading
import time
import types
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")  # CPU only: the 8 GB card is held by the Octo servers
ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("TFHUB_CACHE_DIR", str(ROOT / ".runtime" / "tfhub"))

import numpy as np

CHECKPOINTS = {
    "rt-1-x": "rt_1_x_tf_trained_for_002272480_step",
    "rt-1-converged": "rt_1_tf_trained_for_000400120",
    "rt-1-15pct": "rt_1_tf_trained_for_000058240",
    "rt-1-begin": "rt_1_tf_trained_for_000001120",
}
USE_URL = "https://tfhub.dev/google/universal-sentence-encoder-large/5"


class RT1Policy:
    def __init__(self, checkpoint: str, ckpt_root: Path, image_width: int = 320, image_height: int = 256,
                 action_scale: float = 1.0, policy_setup: str = "google_robot"):
        import tensorflow as tf
        import tensorflow_hub as hub
        import tf_agents
        from tf_agents.policies import py_tf_eager_policy

        self.tf, self.tf_agents = tf, tf_agents
        self.checkpoint = checkpoint
        self.model_path = ckpt_root / CHECKPOINTS[checkpoint]
        if not (self.model_path / "saved_model.pb").exists():
            raise FileNotFoundError(f"no saved_model.pb under {self.model_path}")
        self.policy_setup = policy_setup
        if policy_setup != "google_robot":
            raise NotImplementedError("this server serves the google_robot setup only")
        t0 = time.perf_counter()
        self.lang_embed_model = hub.load(USE_URL)
        self.tfa_policy = py_tf_eager_policy.SavedModelPyTFEagerPolicy(
            model_path=str(self.model_path), load_specs_from_pbtxt=True, use_tf_function=True)
        self.load_seconds = time.perf_counter() - t0
        self.image_width, self.image_height, self.action_scale = image_width, image_height, action_scale
        self.lock = threading.Lock()
        self.step_count = 0
        self.sessions = {}
        tw = time.perf_counter()
        self.reset("pick coke can", 0, session="warmup")
        self.step(np.zeros((512, 640, 3), dtype=np.uint8), session="warmup")
        self.jit_warmup_seconds = time.perf_counter() - tw
        self.sessions.pop("warmup", None)

    def _zero_observation(self):
        specs = self.tf_agents.specs
        return specs.zero_spec_nest(specs.from_spec(self.tfa_policy.time_step_spec.observation))

    def reset(self, instruction: str, seed: int, config: dict = None, session: str = "default"):
        """`seed` is accepted for interface parity and recorded, but RT-1's eager policy takes no seed:
        treat this family as deterministic (verify by re-running one configuration)."""
        st = types.SimpleNamespace()
        st.observation = self._zero_observation()
        st.policy_state = self.tfa_policy.get_initial_state(batch_size=1)
        st.instruction = instruction
        st.embedding = self.lang_embed_model([instruction])[0] if instruction else \
            self.tf.zeros((512,), dtype=self.tf.float32)
        st.seed = int(seed)
        st.step_count = 0
        st.last_used = time.time()
        self.sessions[session] = st
        for k in [k for k, v in list(self.sessions.items()) if k != session and time.time() - v.last_used > 3600]:
            del self.sessions[k]

    def _resize(self, image_u8: np.ndarray):
        tf = self.tf
        img = tf.image.resize_with_pad(image_u8, target_width=self.image_width, target_height=self.image_height)
        return tf.cast(img, tf.uint8)

    def step(self, image_u8: np.ndarray, session: str = "default"):
        tf = self.tf
        from tf_agents.trajectories import time_step as ts

        t0 = time.perf_counter()
        st = self.sessions.get(session)
        if st is None:
            raise KeyError(f"unknown session {session!r}: call /reset with this session id first")
        st.last_used = time.time()
        assert image_u8.dtype == np.uint8, image_u8.dtype
        st.observation["image"] = self._resize(image_u8)
        st.observation["natural_language_embedding"] = st.embedding
        tfa_time_step = ts.transition(st.observation, reward=np.zeros((), dtype=np.float32))
        policy_step = self.tfa_policy.action(tfa_time_step, st.policy_state)
        raw = policy_step.action
        # Small-action filter, gripper only -- matches rt1_model.py's call with arm_movement=False.
        raw["gripper_closedness_action"] = tf.where(
            tf.abs(raw["gripper_closedness_action"]) < 1e-2,
            tf.zeros_like(raw["gripper_closedness_action"]), raw["gripper_closedness_action"])
        raw = {k: np.asarray(v) for k, v in raw.items()}
        st.policy_state = policy_step.state

        world = np.asarray(raw["world_vector"], dtype=np.float64) * self.action_scale
        delta = np.asarray(raw["rotation_delta"], dtype=np.float64)
        angle = float(np.linalg.norm(delta))
        axis = delta / angle if angle > 1e-6 else np.array([0.0, 1.0, 0.0])
        rot = axis * angle * self.action_scale
        gripper = float(np.asarray(raw["gripper_closedness_action"]).reshape(-1)[0])
        terminate = bool(np.asarray(raw["terminate_episode"]).reshape(-1)[0] > 0)
        action = np.concatenate([world.reshape(-1)[:3], rot.reshape(-1)[:3], [gripper]])
        st.step_count += 1
        self.step_count += 1
        return {"action": action.tolist(), "raw_action": {k: np.asarray(v).reshape(-1).tolist() for k, v in raw.items()},
                "terminate_episode": terminate, "inference_seconds": time.perf_counter() - t0,
                "from_chunk": False, "session": session}


def make_handler(policy: RT1Policy, meta: dict):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
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
                self._json(200, dict(meta, step_count=policy.step_count, sessions=len(policy.sessions),
                                     session_isolation=True))
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
            except Exception as e:
                self._json(500, {"error": f"{type(e).__name__}: {e}"})

    return Handler


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--checkpoint", default="rt-1-x", choices=sorted(CHECKPOINTS))
    p.add_argument("--ckpt-root", default="third_party/SimplerEnv/checkpoints")
    p.add_argument("--port", type=int, default=8773)
    p.add_argument("--host", default="0.0.0.0")
    args = p.parse_args()

    t0 = time.perf_counter()
    policy = RT1Policy(args.checkpoint, ROOT / args.ckpt_root)
    import tensorflow as tf
    import tf_agents
    meta = dict(model=args.checkpoint, saved_model=str(policy.model_path),
                tensorflow=tf.__version__, tf_agents=tf_agents.__version__, numpy=np.__version__,
                policy_setup="google_robot", deterministic="no seed input; verify by re-running a config",
                image_size=[policy.image_height, policy.image_width],
                load_seconds=policy.load_seconds, jit_warmup_seconds=policy.jit_warmup_seconds,
                startup_seconds=time.perf_counter() - t0,
                terminate_episode="predicted by RT-1; the caller must honour it")
    print(json.dumps(meta), flush=True)
    srv = ThreadingHTTPServer((args.host, args.port), make_handler(policy, meta))
    print(f"READY {args.host}:{args.port}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
