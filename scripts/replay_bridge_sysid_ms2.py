"""B-1 calibration replay on the ORIGINAL SIMPLER main stack (ManiSkill2_real2sim + SAPIEN 2.2.2), run in WSL
with CPU physics and no renderer (SAPIEN's Vulkan renderer is unavailable in WSL; renderer/camera/lighting
setup is stubbed, physics, controllers and Pinocchio IK are untouched).

Protocol mirrors third_party/SimplerEnv/tools/sysid/sysid.py: env.reset(); robot lifted to (0,0,1); at step 0 the
arm is set by the controller's own compute_ik to the first demo TCP pose; demo actions replayed open-loop
(world_vector, euler2axangle(rpy), gripper 0); error = translation L2 + arcsin(||R_pred-R_gt||_F / (2*sqrt(2))).
Controller conditions scale the arm controller config (stiffness, damping, force_limit) before reset; delay
executes the action issued `delay_steps` control steps earlier.

Outputs the same files as scripts/replay_bridge_sysid.py (<cond>.jsonl, <cond>_epNNN.npz, run_meta.json,
summary.md) so scripts/check_iso_invariance.py works unchanged.

Usage (WSL):  source .venv-linux/bin/activate && python scripts/replay_bridge_sysid_ms2.py --episodes 100 --preset sweep_v1 --output-dir results/replay_sysid_ms2
"""
import argparse
import inspect
import json
import math
import sys
import time
from collections import OrderedDict, deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
MAT_TRANSFORM = np.array([[0.0, 0.0, 1.0], [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0]], dtype=np.float64)
ENV_ID = "PutCarrotOnPlateInScene-v0"
CONTROL_MODE = "arm_pd_ee_target_delta_pose_align2_gripper_pd_joint_pos"
PRESETS = {
    "sweep_v1": OrderedDict([
        ("nominal", dict()),
        ("stiff_x0.5", dict(stiffness_scale=0.5)), ("stiff_x2.0", dict(stiffness_scale=2.0)),
        ("damp_x0.5", dict(damping_scale=0.5)), ("damp_x2.0", dict(damping_scale=2.0)),
        ("force_x0.5", dict(force_scale=0.5)), ("delay_1", dict(delay_steps=1)),
    ]),
    "iso_ratio_v1": OrderedDict([
        ("iso_x0.25", dict(stiffness_scale=0.25, damping_scale=0.25)), ("iso_x0.5", dict(stiffness_scale=0.5, damping_scale=0.5)),
        ("nominal", dict()), ("iso_x2.0", dict(stiffness_scale=2.0, damping_scale=2.0)), ("iso_x4.0", dict(stiffness_scale=4.0, damping_scale=4.0)),
    ]),
    # The common scale swept at the CALIBRATION-PREFERRED ratio (d/k = 0.25), which the 50-point
    # grid samples only once. iso_ratio_v1 does the same at ratio 1. Sixteenfold span, matching the
    # range the policy sweeps use. Grid naming (sN_dM_delayK) so the group analyses parse them.
    "iso_at_fitted": OrderedDict([
        ("s0.5_d0.125_delay1", dict(stiffness_scale=0.5, damping_scale=0.125, delay_steps=1)),
        ("s1_d0.25_delay1", dict(stiffness_scale=1.0, damping_scale=0.25, delay_steps=1)),
        ("s2_d0.5_delay1", dict(stiffness_scale=2.0, damping_scale=0.5, delay_steps=1)),
        ("s4_d1_delay1", dict(stiffness_scale=4.0, damping_scale=1.0, delay_steps=1)),
        ("s8_d2_delay1", dict(stiffness_scale=8.0, damping_scale=2.0, delay_steps=1)),
    ]),
}


def full_condition(c):
    return dict(stiffness_scale=c.get("stiffness_scale", 1.0), damping_scale=c.get("damping_scale", 1.0),
                force_scale=c.get("force_scale", 1.0), delay_steps=int(c.get("delay_steps", 0)))


def grid_conditions():
    conds = OrderedDict()
    for ss in [0.5, 0.7, 1.0, 1.4, 2.0]:
        for ds in [0.5, 0.7, 1.0, 1.4, 2.0]:
            for delay in [0, 1]:
                conds[f"s{ss:g}_d{ds:g}_delay{delay}"] = dict(stiffness_scale=ss, damping_scale=ds, delay_steps=delay)
    return conds


def apply_headless_patches():
    """Stub SAPIEN 2 renderer, cameras and lighting so the original env runs physics-only in WSL."""
    import sapien.core as sapien
    import mani_skill2_real2sim.envs.sapien_env as se

    class _NoRenderer:
        def set_log_level(self, *a):
            pass

        def create_material(self):
            return None

    se.sapien.SapienRenderer = lambda **kw: _NoRenderer()
    sapien.Engine.set_renderer = lambda self, r: None
    import mani_skill2_real2sim.envs  # noqa: F401  (registers envs)

    def _cams(self):
        self._cameras = OrderedDict()
        self._render_cameras = OrderedDict()

    n = 0
    for mod in list(sys.modules.values()):
        if mod is None or not getattr(mod, "__name__", "").startswith("mani_skill2_real2sim"):
            continue
        for _, cls in inspect.getmembers(mod, inspect.isclass):
            if issubclass(cls, se.BaseEnv):
                if "_setup_lighting" in cls.__dict__:
                    cls._setup_lighting = lambda self: None
                    n += 1
                if "_setup_cameras" in cls.__dict__:
                    cls._setup_cameras = _cams
    se.BaseEnv._setup_cameras = _cams
    se.BaseEnv._setup_lighting = lambda self: None
    return dict(renderer="stubbed_no_render", lighting_patched_classes=n, physics="sapien2_cpu_original", ik="original_controller_compute_ik")


def rot_err(R_pred, R_gt):
    d = R_pred - R_gt
    return float(np.arcsin(np.clip(np.sqrt(np.trace(d.T @ d)) / (2 * np.sqrt(2)), 0.0, 1.0)))


def git_hash(path):
    try:
        import subprocess
        return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episodes-dir", default="data/bridge_sysid")
    ap.add_argument("--episodes", type=int, default=100)
    ap.add_argument("--preset", default="sweep_v1", choices=sorted(PRESETS))
    ap.add_argument("--conditions", default=None)
    ap.add_argument("--grid", action="store_true")
    ap.add_argument("--output-dir", default="results/replay_sysid_ms2")
    ap.add_argument("--max-steps", type=int, default=None)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    compat = apply_headless_patches()
    import gymnasium as gym
    import sapien.core as sapien
    from transforms3d.euler import euler2axangle, euler2mat
    from transforms3d.quaternions import mat2quat, quat2mat

    conds = grid_conditions() if args.grid else OrderedDict(PRESETS[args.preset])
    if args.conditions:
        conds = OrderedDict((k, conds[k]) for k in [c.strip() for c in args.conditions.split(",")])
    conds = OrderedDict((k, full_condition(v)) for k, v in conds.items())
    tag = "grid" if args.grid else args.preset
    out = ROOT / args.output_dir / tag
    out.mkdir(parents=True, exist_ok=True)

    demos = []
    for k in range(args.episodes):
        f = ROOT / args.episodes_dir / f"ep_{k:03d}.npz"
        if not f.exists():
            continue
        d = np.load(f)
        demos.append(dict(id=k, state=d["state"].astype(np.float64), world=d["world_vector"].astype(np.float64),
                          rot=d["rotation_delta"].astype(np.float64), grip=d["open_gripper"].astype(np.int64), instruction=str(d["instruction"])))
    if not demos:
        raise SystemExit("no demos found")

    # nominal controller config (read once from a fresh env)
    env = gym.make(ENV_ID, obs_mode="none", robot="widowx", control_mode=CONTROL_MODE, sim_freq=500, control_freq=5)
    env.reset(seed=0)
    arm_cfg = env.unwrapped.agent.controller.controllers["arm"].config
    nominal = dict(stiffness=np.array(arm_cfg.stiffness, float).tolist(), damping=np.array(arm_cfg.damping, float).tolist(),
                   force_limit=np.array(arm_cfg.force_limit, float).tolist())
    env.close()

    meta = dict(started_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), args=vars(args), compat=compat,
                env_id=ENV_ID, robot="widowx", control_mode=CONTROL_MODE, sim_freq=500, control_freq=5, nominal=nominal,
                conditions=conds, n_demos=len(demos), demo_ids=[d["id"] for d in demos],
                pose_convention="p=state[:3]; R=euler2mat(rpy,'sxyz') @ [[0,0,1],[0,1,0],[-1,0,0]]",
                action_convention="world_vector; euler2axangle(rpy,'sxyz'); gripper 0 (as in SIMPLER tools/sysid/sysid.py)",
                evidence="original_simpler_main_ms2_sapien2_cpu_headless_wsl",
                simpler_main_commit=git_hash(ROOT / "third_party/SimplerEnv"), sapien=getattr(sapien, "__version__", None))
    (out / "run_meta.json").write_text(json.dumps(meta, indent=2, default=str), encoding="utf-8")

    summary = {}
    for cname, cond in conds.items():
        jsonl = out / f"{cname}.jsonl"
        done = set()
        if jsonl.exists():
            for line in jsonl.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    done.add(json.loads(line)["episode_id"])
        todo = [d for d in demos if d["id"] not in done]
        if not todo:
            print(f"[{cname}] complete ({len(done)} demos)", flush=True)
            continue
        env = gym.make(ENV_ID, obs_mode="none", robot="widowx", control_mode=CONTROL_MODE, sim_freq=500, control_freq=5)
        u = env.unwrapped
        # condition: scale the arm controller config; the agent/controllers are rebuilt from it at reset (reconfigure)
        cfg = u.agent.controller.controllers["arm"].config
        cfg.stiffness = (np.array(nominal["stiffness"]) * cond["stiffness_scale"]).tolist()
        cfg.damping = (np.array(nominal["damping"]) * cond["damping_scale"]).tolist()
        cfg.force_limit = (np.array(nominal["force_limit"]) * cond["force_scale"]).tolist()
        env.reset(seed=0)
        robot = u.agent.robot
        arm = u.agent.controller.controllers["arm"]
        joints = robot.get_active_joints()
        effective = dict(cond, drive_stiffness=[float(joints[i].stiffness) for i in arm.joint_indices],
                         drive_damping=[float(joints[i].damping) for i in arm.joint_indices],
                         drive_force_limit=[float(joints[i].force_limit) for i in arm.joint_indices])
        delay = cond["delay_steps"]
        rows = []
        for demo in todo:
            t0 = time.perf_counter()
            T = len(demo["state"]) if args.max_steps is None else min(args.max_steps, len(demo["state"]))
            gt_p = demo["state"][:T, :3]
            gt_R = np.stack([euler2mat(*demo["state"][t, 3:6]) @ MAT_TRANSFORM for t in range(T)])
            gt_q = np.stack([mat2quat(R) for R in gt_R])  # wxyz

            env.reset(seed=0)
            robot.set_pose(sapien.Pose([0.0, 0.0, 1.0]))
            # step-0 alignment exactly as in SIMPLER sysid.py: controller IK from the current qpos
            target = sapien.Pose(p=gt_p[0], q=gt_q[0])
            cur_qpos = robot.get_qpos()
            init_q = arm.compute_ik(target)
            init_ok = init_q is not None
            if init_ok:
                cur_qpos[arm.joint_indices] = init_q
                u.agent.reset(cur_qpos)
            tcp = robot.pose.inv() * u.tcp.pose
            init_err = (float(np.linalg.norm(tcp.p - gt_p[0])), rot_err(quat2mat(tcp.q), gt_R[0]))

            queue = deque([np.zeros(7, dtype=np.float64)] * delay) if delay else None
            sim_p, sim_q = [], []
            for t in range(T):
                tcp = robot.pose.inv() * u.tcp.pose
                sim_p.append(np.array(tcp.p, dtype=np.float64))
                sim_q.append(np.array(tcp.q, dtype=np.float64))
                ax, ang = euler2axangle(*demo["rot"][t])
                a = np.concatenate([demo["world"][t], np.asarray(ax) * ang, [0.0]]).astype(np.float64)
                if delay:
                    queue.append(a)
                    a = queue.popleft()
                env.step(a)
            sim_p, sim_q = np.stack(sim_p), np.stack(sim_q)
            te = np.linalg.norm(sim_p - gt_p, axis=1)
            re = np.array([rot_err(quat2mat(sim_q[t]), gt_R[t]) for t in range(T)])
            rec = dict(condition=cname, episode_id=demo["id"], steps=int(T), instruction=demo["instruction"],
                       init_transl_err=init_err[0], init_rot_err=init_err[1], init_ok=bool(init_ok and init_err[0] < 2e-3),
                       mean_transl_err=float(te.mean()), mean_rot_err=float(re.mean()), mean_total_err=float((te + re).mean()),
                       max_transl_err=float(te.max()), final_transl_err=float(te[-1]),
                       gt_path_length=float(np.linalg.norm(np.diff(gt_p, axis=0), axis=1).sum()), seconds=time.perf_counter() - t0)
            np.savez_compressed(out / f"{cname}_ep{demo['id']:03d}.npz", sim_p=sim_p, sim_q=sim_q, gt_p=gt_p, gt_q=gt_q, transl_err=te, rot_err=re)
            with jsonl.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec) + "\n")
            rows.append(rec)
            if args.verbose or init_err[0] > 2e-3:
                print(f"[{cname}] ep {demo['id']} T={T} init_err={init_err[0]*1000:.1f}mm/{math.degrees(init_err[1]):.2f}deg mean_err={rec['mean_total_err']:.4f} {rec['seconds']:.1f}s", flush=True)
        env.close()
        allrows = [json.loads(l) for l in jsonl.read_text(encoding="utf-8").splitlines() if l.strip()]
        summary[cname] = dict(effective=effective, n=len(allrows),
                              mean_total_err=float(np.mean([r["mean_total_err"] for r in allrows])),
                              mean_transl_err=float(np.mean([r["mean_transl_err"] for r in allrows])),
                              mean_rot_err=float(np.mean([r["mean_rot_err"] for r in allrows])),
                              init_ok_frac=float(np.mean([r["init_ok"] for r in allrows])))
        print(f"[{cname}] n={len(allrows)} mean_total_err={summary[cname]['mean_total_err']:.5f} transl={summary[cname]['mean_transl_err']:.5f} rot={summary[cname]['mean_rot_err']:.5f} init_ok={summary[cname]['init_ok_frac']:.2f}", flush=True)
        (out / "summary.json").write_text(json.dumps(dict(meta=meta, conditions=summary), indent=2, default=str), encoding="utf-8")

    lines = [f"# Replay sysid on original SIMPLER main (ms2 + SAPIEN 2, headless WSL): {tag}", "",
             f"{len(demos)} demos; {ENV_ID}; control {CONTROL_MODE}; error = transl L2 + rot arcsin; gripper action 0.", "",
             "| condition | n | mean total err | transl | rot | init ok |", "|---|---:|---:|---:|---:|---:|"]
    for c, s in summary.items():
        lines.append(f"| {c} | {s['n']} | {s['mean_total_err']:.5f} | {s['mean_transl_err']:.5f} | {s['mean_rot_err']:.5f} | {s['init_ok_frac']:.2f} |")
    (out / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    print("REPLAY_MS2_DONE", out, flush=True)


if __name__ == "__main__":
    main()
