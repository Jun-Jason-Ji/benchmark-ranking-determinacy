"""Controller-parameter sensitivity sweep for Bridge/WidowX digital-twin tasks (ManiSkill 3.0.1).

Question: do pairwise policy rankings flip when the arm PD controller parameters
(stiffness, damping, force limit) or the execution latency change within a
plausible range, with everything else fixed?

Design:
  * Process-local monkey-patching of the Real2Sim-tuned robot class attributes
    (WidowX250SBridgeDatasetFlatTable.arm_stiffness / arm_damping / arm_force_limit)
    before the env is built. No installed file is modified.
  * Execution latency is a wrapper that executes the action issued k control
    steps earlier (initial queue: zero motion, gripper open).
  * Common random numbers: identical episode_ids (initial object configs) and
    policy seeds across all conditions and policies.
  * Episodes run to the registered max_episode_steps (as SIMPLER's ms3 eval
    script does) and success is read from the final info.
  * Windows CPU-physics + GPU-render route via scripts/ms3_windows_compat.py,
    which replaces the Pinocchio IK by ManiSkill's torch Jacobian solver. This
    is an exploratory platform, NOT a reproduction of the original SIMPLER main
    branch used for the published real-vs-sim numbers.

Output: one JSONL line per episode + condition summary JSON under --output-dir.
"""
import argparse
import http.client
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
import time
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MS_ASSET_DIR", str(ROOT / "data/maniskill-assets"))
sys.path.insert(0, str(ROOT / "scripts"))
from task_configs import is_deterministic as _is_det, n_configs as _n_configs  # noqa: E402

NOMINAL = dict(
    arm_stiffness=[1169.7891719504198, 730.0, 808.4601346394447, 1229.1299089624076,
                   1272.2760456418862, 1056.3326605132252],
    arm_damping=[330.0, 180.0, 152.12036565582588, 309.6215302722146, 201.04998711007383,
                 269.51458932695414],
    arm_force_limit=[200, 200, 100, 100, 100, 100],
    gripper_stiffness=1000, gripper_damping=200, gripper_force_limit=60,
)

# name -> dict(stiffness_scale, damping_scale, force_scale, gripper_force_scale, delay_steps)
PRESETS = {
    "sweep_v1": {
        "nominal": dict(),
        "stiff_x0.5": dict(stiffness_scale=0.5),
        "stiff_x2.0": dict(stiffness_scale=2.0),
        "damp_x0.5": dict(damping_scale=0.5),
        "damp_x2.0": dict(damping_scale=2.0),
        "force_x0.5": dict(force_scale=0.5),
        "delay_1": dict(delay_steps=1),
    },
    # same stiffness/damping ratio, different absolute scale: free-space replay cannot distinguish
    # these (see results/replay_sysid_smoke/FINDING_iso_ratio.md); contact outcomes might.
    "iso_ratio_v1": {
        "iso_x0.25": dict(stiffness_scale=0.25, damping_scale=0.25),
        "iso_x0.5": dict(stiffness_scale=0.5, damping_scale=0.5),
        "nominal": dict(),
        "iso_x2.0": dict(stiffness_scale=2.0, damping_scale=2.0),
        "iso_x4.0": dict(stiffness_scale=4.0, damping_scale=4.0),
    },
    # wider ratio-changing perturbations and a 2-step latency (identifiable directions, larger amplitude)
    "wide_v1": {
        "stiff_x0.25": dict(stiffness_scale=0.25),
        "stiff_x4.0": dict(stiffness_scale=4.0),
        "damp_x0.25": dict(damping_scale=0.25),
        "damp_x4.0": dict(damping_scale=4.0),
        "delay_2": dict(delay_steps=2),
    },
    # object contact parameters (calibration-invisible by construction for free-space demo replay)
    "contact_v1": {
        "fric_x0.4": dict(friction_scale=0.4),
        "fric_x2.5": dict(friction_scale=2.5),
        "dens_x0.5": dict(density_scale=0.5),
        "dens_x2.0": dict(density_scale=2.0),
    },
    # deployment-variant study: nominal + calibration-invisible perturbations
    "variants_v1": {
        "nominal": dict(),
        "iso_x0.25": dict(stiffness_scale=0.25, damping_scale=0.25),
        "iso_x4.0": dict(stiffness_scale=4.0, damping_scale=4.0),
        "force_x0.5": dict(force_scale=0.5),
        "fric_x0.4": dict(friction_scale=0.4),
        "dens_x0.5": dict(density_scale=0.5),
    },
    "quick3": {
        "nominal": dict(),
        "stiff_x0.5": dict(stiffness_scale=0.5),
        "delay_1": dict(delay_steps=1),
    },
}


def to_json(v):
    if isinstance(v, dict):
        return {k: to_json(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [to_json(x) for x in v]
    if hasattr(v, "detach"):
        v = v.detach().cpu()
    if hasattr(v, "tolist"):
        return v.tolist()
    return v


class PolicyClient:
    def __init__(self, url, session=None):
        host, port = url.replace("http://", "").split(":")
        self.host, self.port = host, int(port)
        import os
        self.session = session or "%d-%d" % (os.getpid(), int(time.time()))  # unique per client process

    def _req(self, method, path, body=None, headers=None, retries=5):
        last = None
        for attempt in range(retries):
            try:
                conn = http.client.HTTPConnection(self.host, self.port, timeout=600)
                conn.request(method, path, body=body, headers=headers or {})
                resp = conn.getresponse()
                data = json.loads(resp.read())
                conn.close()
                if resp.status != 200:
                    raise RuntimeError(f"policy server {path} -> {resp.status}: {data}")
                return data
            except (OSError, ConnectionError, TimeoutError, http.client.HTTPException) as e:
                last = e
                time.sleep(3 * (attempt + 1))  # transient localhost/WSL relay hiccups
        raise RuntimeError(f"policy server {path} unreachable after {retries} attempts: {last}")

    def health(self):
        return self._req("GET", "/health")

    def reset(self, instruction, seed, config=None):
        return self._req("POST", "/reset", json.dumps({"instruction": instruction, "seed": seed, "config": config, "session": self.session}),
                         {"Content-Type": "application/json"})

    def step(self, img_u8):
        import numpy as np
        img = np.ascontiguousarray(img_u8, dtype=np.uint8)
        return self._req("POST", "/step", img.tobytes(),
                         {"Content-Type": "application/octet-stream",
                          "X-Shape": ",".join(str(s) for s in img.shape), "X-Session": self.session})


VARIANTS = {
    "default": dict(ensemble=True, exec_horizon=1, history=2),
    "noens": dict(ensemble=False, exec_horizon=1, history=2),
    "chunk4": dict(ensemble=False, exec_horizon=4, history=2),
    "hist1": dict(ensemble=True, exec_horizon=1, history=1),
}


def parse_policy_name(name):
    """'octo-small' -> ('octo-small', 'default'); 'octo-small@chunk4' -> ('octo-small', 'chunk4')."""
    base, _, var = name.partition("@")
    var = var or "default"
    if var not in VARIANTS:
        raise SystemExit(f"unknown variant {var}; known: {sorted(VARIANTS)}")
    return base, var


def apply_condition(robot_cls, cond):
    """Patch class attributes; return the effective controller parameters."""
    ss = cond.get("stiffness_scale", 1.0)
    ds = cond.get("damping_scale", 1.0)
    fs = cond.get("force_scale", 1.0)
    gs = cond.get("gripper_force_scale", 1.0)
    robot_cls.arm_stiffness = [v * ss for v in NOMINAL["arm_stiffness"]]
    robot_cls.arm_damping = [v * ds for v in NOMINAL["arm_damping"]]
    robot_cls.arm_force_limit = [v * fs for v in NOMINAL["arm_force_limit"]]
    robot_cls.gripper_force_limit = NOMINAL["gripper_force_limit"] * gs
    # object contact parameters: friction is a class attribute of BaseBridgeEnv (nominal 0.5/0.5);
    # density lives in the model json loaded in __init__, scaled by patching io_utils.load_json.
    fr = cond.get("friction_scale", 1.0)
    dn = cond.get("density_scale", 1.0)
    from mani_skill.envs.tasks.digital_twins.bridge_dataset_eval import base_env as _bb
    _bb.BaseBridgeEnv.obj_static_friction = 0.5 * fr
    _bb.BaseBridgeEnv.obj_dynamic_friction = 0.5 * fr
    if not hasattr(_bb.io_utils, "_orig_load_json"):
        _bb.io_utils._orig_load_json = _bb.io_utils.load_json
    scale = dn
    def _load_json(path, *a, **k):
        d = _bb.io_utils._orig_load_json(path, *a, **k)
        if str(path).endswith(_bb.BaseBridgeEnv.MODEL_JSON) and scale != 1.0:
            for v in d.values():
                if isinstance(v, dict):
                    v["density"] = v.get("density", 1000) * scale
        return d
    _bb.io_utils.load_json = _load_json
    return dict(arm_stiffness=robot_cls.arm_stiffness, arm_damping=robot_cls.arm_damping,
                arm_force_limit=robot_cls.arm_force_limit,
                gripper_force_limit=robot_cls.gripper_force_limit,
                delay_steps=int(cond.get("delay_steps", 0)),
                obj_friction=0.5 * fr, density_scale=dn)


def git_hash(path):
    try:
        return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()
    except Exception as e:
        return f"unavailable: {e}"


def policy_seed(args, ep):
    """One seed for the whole run (official SIMPLER protocol) or a per-episode seed (our default)."""
    return args.policy_seed_fixed if args.policy_seed_fixed is not None else args.policy_seed_base + ep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env-id", default="PutCarrotOnPlateInScene-v1")
    ap.add_argument("--policy-url", default="http://127.0.0.1:8765")
    ap.add_argument("--policy-name", required=True, help="label, e.g. octo-small")
    ap.add_argument("--preset", default="sweep_v1", choices=sorted(PRESETS))
    ap.add_argument("--conditions", default=None, help="comma list to restrict conditions of the preset")
    ap.add_argument("--episodes", type=int, default=24, help="episode_ids 0..N-1")
    ap.add_argument("--episode-offset", type=int, default=0)
    ap.add_argument("--policy-seed-base", type=int, default=20260918)
    ap.add_argument("--policy-seed-fixed", type=int, default=None,
                    help="Use this one policy seed for every episode, as the official SIMPLER protocol does "
                         "(scripts/octo_bridge.sh: one --octo-init-rng per run over the whole config range), "
                         "instead of policy_seed_base + episode_id.")
    ap.add_argument("--output-dir", default="results/controller_sweep")
    ap.add_argument("--save-frames", action="store_true", help="save first/last frame PNG per episode")
    ap.add_argument("--max-steps", type=int, default=None, help="override horizon (debug only)")
    args = ap.parse_args()

    import numpy as np
    import torch
    import gymnasium as gym
    import sapien
    import mani_skill.envs  # noqa: F401  (registers envs)
    from mani_skill.envs.tasks.digital_twins.bridge_dataset_eval import base_env as bridge_base
    from mani_skill.envs.tasks.digital_twins.bridge_dataset_eval import put_on_in_scene  # noqa: F401
    from ms3_windows_compat import apply_compatibility

    compat = apply_compatibility()
    device = sapien.Device("cuda")
    render_backend = "pci:" + device.pci_string

    conds = dict(PRESETS[args.preset])
    if args.conditions:
        keep = [c.strip() for c in args.conditions.split(",")]
        conds = {k: conds[k] for k in keep}

    # Config-grid guard (2026-09-19): episode_id maps onto a finite grid of initial configurations, so a range
    # beyond it repeats earlier scenes exactly -- for a deterministic policy those episodes carry no information.
    _n_cfg = _n_configs(args.env_id)
    if _n_cfg and args.episode_offset + args.episodes > _n_cfg:
        _msg = (f"[config-grid] args.env_id has {_n_cfg} distinct configurations; requested episodes "
                f"{args.episode_offset}..{args.episode_offset + args.episodes - 1} wrap around and repeat earlier scenes")
        if _is_det(args.policy_name):
            print(_msg + " -- a deterministic policy reproduces them bit-for-bit; run the census instead", flush=True)
        else:
            print(_msg + " (valid extra policy-noise samples, but not new scenes)", flush=True)

    out = Path(args.output_dir) / args.policy_name / args.env_id
    out.mkdir(parents=True, exist_ok=True)
    client = PolicyClient(args.policy_url)
    health = client.health()
    base_model, variant = parse_policy_name(args.policy_name)
    variant_cfg = VARIANTS[variant]
    if health.get("model") != base_model:
        raise SystemExit(f"policy server serves {health.get('model')} but --policy-name is {args.policy_name}")
    if variant != "default" and "variants" not in health:
        raise SystemExit("policy server too old for deployment variants; restart it with the current octo_policy_server.py")

    run_meta = dict(
        started_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), args=vars(args),
        platform=platform.platform(), python=sys.version.split()[0],
        versions={p: importlib.metadata.version(p) for p in ["sapien", "mani_skill", "torch", "gymnasium", "numpy"]},
        compatibility_adapter=compat, sim_backend="cpu", render_backend=render_backend,
        render_device=device.name, policy_server=health, nominal=NOMINAL, preset=args.preset,
        policy_variant=variant, variant_config=variant_cfg,
        conditions=conds, evidence="exploratory_ms3_windows_platform_not_original_simpler",
        simpler_ms3_commit=git_hash(ROOT / "third_party/SimplerEnv-ms3"),
        octo_commit=git_hash(ROOT / "third_party/octo"),
        episode_protocol="run to max_episode_steps, success from final info; common episode_ids and policy seeds",
    )
    (out / "run_meta.json").write_text(json.dumps(to_json(run_meta), indent=2), encoding="utf-8")
    # run_meta.json is overwritten by the next run in the same directory, which makes the provenance of
    # already-collected episodes unrecoverable (this bit us on 2026-09-19: seed set A turned out to come
    # from an older inference-server build, and nothing on disk said so). runs.jsonl is append-only.
    with (out / "runs.jsonl").open("a", encoding="utf-8") as _rf:
        print(json.dumps(to_json(run_meta), ensure_ascii=False), file=_rf)

    robot_cls = bridge_base.WidowX250SBridgeDatasetFlatTable
    summaries = {}
    for cname, cond in conds.items():
        effective = apply_condition(robot_cls, cond)
        delay = effective["delay_steps"]
        env = gym.make(args.env_id, obs_mode="rgb+segmentation", num_envs=1, sim_backend="cpu",
                       render_backend=render_backend)
        # read back what the built controller actually uses
        arm_ctrl = env.unwrapped.agent.controller.controllers["arm"].config
        effective["built_stiffness"] = list(map(float, np.broadcast_to(arm_ctrl.stiffness, 6)))
        effective["built_damping"] = list(map(float, np.broadcast_to(arm_ctrl.damping, 6)))
        effective["built_force_limit"] = list(map(float, np.broadcast_to(arm_ctrl.force_limit, 6)))
        effective["control_freq"] = int(env.unwrapped.control_freq)
        effective["sim_freq"] = int(env.unwrapped.sim_freq)
        from mani_skill.utils.registration import REGISTERED_ENVS
        horizon = args.max_steps or REGISTERED_ENVS[args.env_id].max_episode_steps
        effective["horizon"] = int(horizon)
        jsonl = out / f"{cname}.jsonl"
        done_ids = set()
        if jsonl.exists():
            for line in jsonl.read_text(encoding="utf-8").splitlines():
                try:
                    done_ids.add(json.loads(line)["episode_id"])
                except Exception:
                    pass
        successes, n = 0, 0
        for ep in range(args.episode_offset, args.episode_offset + args.episodes):
            if ep in done_ids:
                continue
            t_ep = time.perf_counter()
            obs, _ = env.reset(seed=ep, options={"episode_id": torch.tensor([ep])})
            instruction = env.unwrapped.get_language_instruction()[0]
            client.reset(instruction, policy_seed(args, ep), variant_cfg)
            # latency queue: pre-filled with `delay` idle actions (no motion, gripper open);
            # each step appends the new action and executes the oldest one.
            queue = deque([np.array([0, 0, 0, 0, 0, 0, 1.0], dtype=np.float32)] * delay) if delay else None
            t_inf = t_sim = 0.0
            first_rgb = obs["sensor_data"]["3rd_view_camera"]["rgb"][0].cpu().numpy().astype(np.uint8)
            info = {}
            gripper_closes = 0
            prev_g = 1.0
            for t in range(horizon):
                rgb = obs["sensor_data"]["3rd_view_camera"]["rgb"][0].cpu().numpy().astype(np.uint8)
                r = client.step(rgb)
                t_inf += r["inference_seconds"]
                a = np.asarray(r["action"], dtype=np.float32)
                if delay:
                    queue.append(a)
                    a = np.asarray(queue.popleft(), dtype=np.float32)  # action issued `delay` steps ago
                if a[6] < 0 and prev_g > 0:
                    gripper_closes += 1
                prev_g = float(a[6])
                ts = time.perf_counter()
                obs, reward, terminated, truncated, info = env.step(torch.as_tensor(a)[None])
                t_sim += time.perf_counter() - ts
                if bool(truncated.any()):
                    break
            info = to_json(info)
            flat = {k: (v[0] if isinstance(v, list) and len(v) == 1 else v) for k, v in info.items()}
            success = bool(flat.get("success", False))
            rec = dict(policy=args.policy_name, env_id=args.env_id, condition=cname, episode_id=ep,
                       policy_seed=policy_seed(args, ep), instruction=instruction, steps=t + 1,
                       success=success, info=flat, gripper_close_events=gripper_closes,
                       inference_seconds=t_inf, sim_seconds=t_sim, episode_seconds=time.perf_counter() - t_ep)
            with jsonl.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec) + "\n")
            if args.save_frames:
                import imageio.v2 as imageio
                last_rgb = obs["sensor_data"]["3rd_view_camera"]["rgb"][0].cpu().numpy().astype(np.uint8)
                imageio.imwrite(out / f"{cname}_ep{ep:03d}_first.png", first_rgb)
                imageio.imwrite(out / f"{cname}_ep{ep:03d}_last.png", last_rgb)
            successes += success
            n += 1
            print(f"[{args.policy_name}|{args.env_id}|{cname}] ep {ep} success={success} "
                  f"steps={t + 1} inf={t_inf:.1f}s sim={t_sim:.1f}s total={rec['episode_seconds']:.1f}s", flush=True)
        env.close()
        # summary over everything in the jsonl (including earlier resumed episodes)
        rows = [json.loads(l) for l in jsonl.read_text(encoding="utf-8").splitlines() if l.strip()]
        k = sum(r["success"] for r in rows)
        summaries[cname] = dict(effective=to_json(effective), episodes=len(rows), successes=k,
                                success_rate=(k / len(rows) if rows else None),
                                episode_ids=sorted(r["episode_id"] for r in rows))
        (out / "summary.json").write_text(json.dumps(dict(run_meta=to_json(run_meta), conditions=summaries),
                                                     indent=2), encoding="utf-8")
        print(f"== {cname}: {k}/{len(rows)} success", flush=True)


if __name__ == "__main__":
    main()
