"""One-off patch (2026-09-19): per-session episode state in octo_policy_server.py and session ids in the sweep
clients. Idempotent. See results/contaminated_2026-09-19/README.md for the incident."""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

p = ROOT / "scripts/octo_policy_server.py"
s = p.read_text(encoding="utf-8")
if "session_isolation" not in s:
    old_reset = s[s.index("    # ---- episode state"):s.index("    def _resize_image")]
    new_reset = '''    # ---- episode state (per session; clients pass a session id so that two concurrent clients never
    # share history / ensemble / instruction state -- incident 2026-09-19, results/contaminated_2026-09-19) --
    def reset(self, instruction: str, seed: int, config: dict = None, session: str = "default"):
        """config (deployment variant, same weights): ensemble (bool), exec_horizon (int, open-loop
        chunk length; >1 implies no ensembling), history (int, image window 1..2)."""
        jax = self.jax
        config = config or {}
        st = types.SimpleNamespace()
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

'''
    s = s.replace(old_reset, new_reset)
    old_ens = s[s.index("    def _ensemble(self, cur_action):"):s.index("    def step(self, image_u8: np.ndarray):")]
    new_ens = '''    def _ensemble(self, st, cur_action):
        # cur_action: (1, pred_horizon, 7). Equal-weight average (temperature 0) of all
        # earlier predictions that targeted the current timestep, as in SIMPLER.
        st.action_history.append(np.asarray(cur_action))
        n = len(st.action_history)
        preds = np.stack([pred[:, i] for i, pred in zip(range(n - 1, -1, -1), st.action_history)])
        return preds.mean(axis=0)  # (1, 7)

'''
    s = s.replace(old_ens, new_ens)
    old_step = s[s.index("    def step(self, image_u8: np.ndarray):"):s.index("def make_handler")]
    new_step = '''    def step(self, image_u8: np.ndarray, session: str = "default"):
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
        raw = np.asarray(norm) * self.action_std[None] + self.action_mean[None]  # (1, 4, 7)
        assert raw.shape == (1, self.pred_action_horizon, 7), raw.shape

        def to_env_action(r7):
            world = r7[:3] * self.action_scale
            roll, pitch, yaw = [float(v) for v in r7[3:6]]
            ax, ang = euler2axangle(roll, pitch, yaw)  # static xyz, original SIMPLER convention
            rot = np.asarray(ax, dtype=np.float64) * float(ang) * self.action_scale
            gripper = 2.0 * float(r7[6] > 0.5) - 1.0
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


'''
    s = s.replace(old_step, new_step)
    s = s.replace('''                    with policy.lock:
                        policy.reset(req["instruction"], int(req.get("seed", 0)), req.get("config"))
                    self._json(200, {"ok": True, "instruction": req["instruction"]})''', '''                    session = str(req.get("session", "default"))
                    with policy.lock:
                        policy.reset(req["instruction"], int(req.get("seed", 0)), req.get("config"), session=session)
                    self._json(200, {"ok": True, "instruction": req["instruction"], "session": session})''')
    s = s.replace('''                    with policy.lock:
                        out = policy.step(img)''', '''                    session = str(self.headers.get("X-Session", "default"))
                    with policy.lock:
                        out = policy.step(img, session=session)''')
    s = s.replace('self._json(200, dict(meta, step_count=policy.step_count))',
                  'self._json(200, dict(meta, step_count=policy.step_count, sessions=len(getattr(policy, "sessions", {})), session_isolation=True))')
    if "import types" not in s:
        s = s.replace("from collections import deque", "import types\nfrom collections import deque", 1)
    s = s.replace("The server is stateful for one episode at a time: POST /reset then POST /step.",
                  "The server keeps one episode state per session id (JSON field 'session' on /reset, header X-Session on /step;\n"
                  "default 'default'). Two concurrent clients must use different session ids.")
    assert "session_isolation" in s and "self.sessions[session] = st" in s
    p.write_text(s, encoding="utf-8")
    print("server patched")
else:
    print("server already patched")

for path in ("scripts/controller_sweep.py", "scripts/controller_sweep_ms2.py"):
    q = ROOT / path
    c = q.read_text(encoding="utf-8")
    if "X-Session" in c:
        print("client already patched", path)
        continue
    c = c.replace('''    def __init__(self, url):
        host, port = url.replace("http://", "").split(":")
        self.host, self.port = host, int(port)''', '''    def __init__(self, url, session=None):
        host, port = url.replace("http://", "").split(":")
        self.host, self.port = host, int(port)
        import os
        self.session = session or "%d-%d" % (os.getpid(), int(time.time()))  # unique per client process''')
    c = c.replace('''json.dumps({"instruction": instruction, "seed": seed, "config": config})''',
                  '''json.dumps({"instruction": instruction, "seed": seed, "config": config, "session": self.session})''')
    c = c.replace('''"X-Shape": ",".join(str(s) for s in img.shape)})''', '''"X-Shape": ",".join(str(s) for s in img.shape), "X-Session": self.session})''')
    assert "X-Session" in c and '"session": self.session' in c and "self.session = session" in c, path
    q.write_text(c, encoding="utf-8")
    print("client patched", path)

for f in ("scripts/octo_policy_server.py", "scripts/controller_sweep.py", "scripts/controller_sweep_ms2.py"):
    ast.parse((ROOT / f).read_text(encoding="utf-8"))
print("all compile")
