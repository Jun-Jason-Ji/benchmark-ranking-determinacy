"""Experiment B-1: open-loop replay of real BridgeData V2 demonstrations under different
controller conditions, measuring end-effector trajectory fit error (SIMPLER tools/sysid protocol,
ported to ManiSkill 3.0.1 on the Windows CPU-physics route with the torch-Jacobian IK adapter).

Protocol (per condition, per episode):
  1. Empty scene with the Real2Sim-tuned WidowX (robot lifted 1 m, free space, sim 500 Hz / control 5 Hz,
     controller arm_pd_ee_target_delta_pose_align2 + gripper_pd_joint_pos) and patched arm gains.
  2. Align the simulated end-effector to the first recorded pose by iterating the controller's own
     Levenberg-Marquardt IK step until convergence; reset joint velocities and the controller target.
  3. Replay the recorded actions (world_vector, euler rpy -> axis-angle via transforms3d 'sxyz',
     gripper +1 open / -1 close), optionally with an execution delay of k control steps.
  4. Before each action, record the simulated EE pose at base and compare with the recorded pose:
     translation L2 error and the rotation error arcsin(||R_sim - R_gt||_F / (2*sqrt(2))) as in SIMPLER.

Recorded pose convention (SIMPLER prepare_sysid_dataset): p = state[:3],
R = euler2mat(*state[3:6]) @ [[0,0,1],[0,1,0],[-1,0,0]].

Usage:
  python scripts/replay_bridge_sysid.py --preset sweep_v1 --episodes 40
  python scripts/replay_bridge_sysid.py --grid --episodes 40      # stiffness x damping x delay grid
Outputs results/replay_sysid/<preset|grid>/<condition>.jsonl (+ npz trajectories) and summary.md.
"""
import argparse
import json
import math
import os
import sys
import time
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MS_ASSET_DIR", str(ROOT / "data/maniskill-assets"))
sys.path.insert(0, str(ROOT / "scripts"))

import sys as _sys
try:
    _sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
import numpy as np  # noqa: E402

MAT_TRANSFORM = np.array([[0.0, 0.0, 1.0], [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0]], dtype=np.float64)
ROBOT_UID = "widowx250s_bridgedataset_flat_table"
CONTROL_MODE = "arm_pd_ee_target_delta_pose_align2_gripper_pd_joint_pos"


def grid_conditions():
    conds = {}
    for ss in [0.5, 0.7, 1.0, 1.4, 2.0]:
        for ds in [0.5, 0.7, 1.0, 1.4, 2.0]:
            for delay in [0, 1]:
                name = f"s{ss:g}_d{ds:g}_delay{delay}"
                conds[name] = dict(stiffness_scale=ss, damping_scale=ds, delay_steps=delay)
    return conds


def rot_err(R_pred, R_gt):
    d = R_pred - R_gt
    return float(np.arcsin(np.clip(np.sqrt(np.trace(d.T @ d)) / (2 * np.sqrt(2)), 0.0, 1.0)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episodes-dir", default="data/bridge_sysid")
    ap.add_argument("--episodes", type=int, default=40, help="use ep_000..ep_{N-1}")
    ap.add_argument("--preset", default="sweep_v1")
    ap.add_argument("--conditions", default=None, help="comma list to restrict")
    ap.add_argument("--grid", action="store_true", help="stiffness x damping x delay grid instead of preset")
    ap.add_argument("--output-dir", default="results/replay_sysid")
    ap.add_argument("--max-steps", type=int, default=None, help="truncate demos (debug)")
    ap.add_argument("--ik-iters", type=int, default=400)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    import torch
    import gymnasium as gym
    import sapien
    import mani_skill.envs  # noqa: F401
    from mani_skill.envs.tasks.digital_twins.bridge_dataset_eval import base_env as bridge_base  # registers agent
    from mani_skill.utils.structs.pose import Pose
    from mani_skill.utils.geometry import rotation_conversions as rc
    from transforms3d.euler import euler2axangle, euler2mat
    from transforms3d.quaternions import mat2quat, quat2mat
    from ms3_windows_compat import apply_compatibility
    from controller_sweep import apply_condition, NOMINAL, PRESETS, git_hash

    compat = apply_compatibility()
    device = sapien.Device("cuda")
    render_backend = "pci:" + device.pci_string

    conds = grid_conditions() if args.grid else dict(PRESETS[args.preset])
    if args.conditions:
        conds = {k: conds[k] for k in [c.strip() for c in args.conditions.split(",")]}
    tag = "grid" if args.grid else args.preset
    out = ROOT / args.output_dir / tag
    out.mkdir(parents=True, exist_ok=True)

    # load demos
    demos = []
    for k in range(args.episodes):
        f = ROOT / args.episodes_dir / f"ep_{k:03d}.npz"
        if not f.exists():
            continue  # numbering may have gaps (shards have different record counts)
        d = np.load(f)
        demos.append(dict(id=k, state=d["state"].astype(np.float64), world=d["world_vector"].astype(np.float64),
                          rot=d["rotation_delta"].astype(np.float64), grip=d["open_gripper"].astype(np.int64),
                          instruction=str(d["instruction"])))
    if not demos:
        raise SystemExit("no demos found; run scripts/read_bridge_batch.py first")

    meta = dict(started_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), args=vars(args), compat=compat,
                robot_uid=ROBOT_UID, control_mode=CONTROL_MODE, sim_freq=500, control_freq=5, nominal=NOMINAL,
                conditions=conds, n_demos=len(demos), demo_ids=[d["id"] for d in demos],
                pose_convention="p=state[:3]; R=euler2mat(rpy,'sxyz') @ [[0,0,1],[0,1,0],[-1,0,0]]",
                action_convention="world_vector; euler2axangle(rpy,'sxyz'); gripper 2*open-1",
                evidence="exploratory_ms3_windows_platform_not_original_simpler",
                simpler_main_commit=git_hash(ROOT / "third_party/SimplerEnv"))
    (out / "run_meta.json").write_text(json.dumps(meta, indent=2, default=str), encoding="utf-8")

    robot_cls = bridge_base.WidowX250SBridgeDatasetFlatTable
    summary = {}
    for cname, cond in conds.items():
        effective = apply_condition(robot_cls, cond)
        delay = effective["delay_steps"]
        env = gym.make("Empty-v1", robot_uids=ROBOT_UID, obs_mode="state", sim_backend="cpu",
                       render_backend=render_backend, control_mode=CONTROL_MODE,
                       sim_config=dict(sim_freq=500, control_freq=5))
        uenv = env.unwrapped
        env.reset(seed=0)
        agent = uenv.agent
        robot = agent.robot
        arm = agent.controller.controllers["arm"]
        kin = arm.kinematics
        arm_idx = arm.active_joint_indices
        q_canon = robot.get_qpos().clone()  # rest pose of the freshly built env
        effective["built_stiffness"] = [float(v) for v in np.broadcast_to(arm.config.stiffness, 6)]
        effective["built_damping"] = [float(v) for v in np.broadcast_to(arm.config.damping, 6)]
        jsonl = out / f"{cname}.jsonl"
        done = set()
        if jsonl.exists():
            for line in jsonl.read_text(encoding="utf-8").splitlines():
                try:
                    done.add(json.loads(line)["episode_id"])
                except Exception:
                    pass
        rows = []
        for demo in demos:
            if demo["id"] in done:
                continue
            t0 = time.perf_counter()
            T = len(demo["state"]) if args.max_steps is None else min(args.max_steps, len(demo["state"]))
            gt_p = demo["state"][:T, :3]
            gt_R = np.stack([euler2mat(*demo["state"][t, 3:6]) @ MAT_TRANSFORM for t in range(T)])
            gt_q = np.stack([mat2quat(R) for R in gt_R])  # wxyz

            # fresh robot state: lift to free space; IK always starts from the canonical rest qpos
            # (Empty-v1 reset does not restore joint state, so inheriting the previous episode's
            # final qpos let IK converge to out-of-limit equivalent solutions; fixed 2026-09-18)
            env.reset(seed=0)
            robot.set_pose(sapien.Pose([0.0, 0.0, 1.0]))
            lim = robot.get_qlimits()[0]
            rng_ik = np.random.default_rng(1000 + demo["id"])
            target = Pose.create_from_pq(torch.as_tensor(gt_p[0], dtype=torch.float32)[None],
                                         torch.as_tensor(gt_q[0], dtype=torch.float32)[None])
            # iterate the controller's own LM step to convergence (absolute IK); retry from perturbed
            # starts if the solution leaves the joint limits
            ik_err, q_full, init_ok = None, None, False
            for attempt in range(6):
                q_try = q_canon.clone()
                if attempt > 0:
                    q_try[:, arm_idx] += torch.as_tensor(rng_ik.uniform(-0.6, 0.6, size=len(arm_idx)), dtype=torch.float32)
                for it in range(args.ik_iters):
                    q_arm = kin.compute_ik(target, q_try, solver_config=dict(type="levenberg_marquardt", solver_iterations=1, alpha=0.5))
                    if q_arm is None:
                        break
                    q_try[:, arm_idx] = q_arm
                    fk = kin.pk_chain.forward_kinematics(q_try[:, kin.active_ancestor_joint_idxs]).get_matrix()[0].cpu().numpy().astype(np.float64)
                    te = float(np.linalg.norm(fk[:3, 3] - gt_p[0]))
                    re = rot_err(fk[:3, :3], gt_R[0])
                    if te < 1e-4 and re < 1e-3:
                        break
                # wrap joints whose limit range is a full turn (waist, forearm_roll, wrist_rotate) into range
                for j in arm_idx.tolist():
                    lo, hi = float(lim[j, 0]), float(lim[j, 1])
                    if hi - lo >= 2 * math.pi - 1e-3:
                        q_try[0, j] = lo + torch.remainder(q_try[0, j] - lo, hi - lo)
                within = bool(torch.all(q_try[0, arm_idx] >= lim[arm_idx, 0]) and torch.all(q_try[0, arm_idx] <= lim[arm_idx, 1]))
                if q_full is None or (within and te < 1e-3):
                    q_full, ik_err = q_try, (te, re, it + 1, attempt, within)
                if within and te < 1e-3 and re < 1e-2:
                    init_ok = True
                    break
            q_full = torch.maximum(torch.minimum(q_full, lim[:, 1][None]), lim[:, 0][None])
            agent.reset(q_full)
            agent.controller.reset()
            ee0 = arm.ee_pose_at_base
            init_p = ee0.p[0].cpu().numpy().astype(np.float64)
            init_R = quat2mat(ee0.q[0].cpu().numpy().astype(np.float64))
            init_err = (float(np.linalg.norm(init_p - gt_p[0])), rot_err(init_R, gt_R[0]))

            grip0 = 2.0 * float(demo["grip"][0]) - 1.0
            queue = deque([np.array([0, 0, 0, 0, 0, 0, grip0], dtype=np.float32)] * delay) if delay else None
            sim_p, sim_q = [], []
            for t in range(T):
                ee = arm.ee_pose_at_base
                sim_p.append(ee.p[0].cpu().numpy().astype(np.float64))
                sim_q.append(ee.q[0].cpu().numpy().astype(np.float64))
                ax, ang = euler2axangle(*demo["rot"][t])
                a = np.concatenate([demo["world"][t], np.asarray(ax) * ang, [2.0 * float(demo["grip"][t]) - 1.0]]).astype(np.float32)
                if delay:
                    queue.append(a)
                    a = queue.popleft()
                uenv.step(torch.as_tensor(a)[None])
            sim_p, sim_q = np.stack(sim_p), np.stack(sim_q)
            te = np.linalg.norm(sim_p - gt_p, axis=1)
            re = np.array([rot_err(quat2mat(sim_q[t]), gt_R[t]) for t in range(T)])
            rec = dict(condition=cname, episode_id=demo["id"], steps=int(T), instruction=demo["instruction"],
                       init_transl_err=init_err[0], init_rot_err=init_err[1],
                       ik_fk_transl_err=ik_err[0] if ik_err else None, ik_iters=ik_err[2] if ik_err else None,
                       ik_attempts=(ik_err[3] + 1) if ik_err else None, ik_within_limits=ik_err[4] if ik_err else None, init_ok=bool(init_ok and init_err[0] < 2e-3),
                       mean_transl_err=float(te.mean()), mean_rot_err=float(re.mean()),
                       mean_total_err=float((te + re).mean()), max_transl_err=float(te.max()),
                       final_transl_err=float(te[-1]), gt_path_length=float(np.linalg.norm(np.diff(gt_p, axis=0), axis=1).sum()),
                       seconds=time.perf_counter() - t0)
            np.savez_compressed(out / f"{cname}_ep{demo['id']:03d}.npz", sim_p=sim_p, sim_q=sim_q, gt_p=gt_p, gt_q=gt_q,
                                transl_err=te, rot_err=re)
            with jsonl.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec) + "\n")
            rows.append(rec)
            if args.verbose or init_err[0] > 2e-3:
                print(f"[{cname}] ep {demo['id']} T={T} init_err={init_err[0]*1000:.1f}mm/{math.degrees(init_err[1]):.2f}deg "
                      f"(ik {ik_err}) mean_transl={te.mean()*1000:.1f}mm mean_rot={math.degrees(re.mean()):.2f}deg "
                      f"final={te[-1]*1000:.1f}mm {rec['seconds']:.1f}s", flush=True)
        env.close()
        allrows = [json.loads(l) for l in jsonl.read_text(encoding="utf-8").splitlines() if l.strip()]
        tr = np.array([r["mean_transl_err"] for r in allrows]); ro = np.array([r["mean_rot_err"] for r in allrows])
        summary[cname] = dict(effective=effective, episodes=len(allrows),
                              mean_transl_err_mm=float(tr.mean() * 1000), sem_transl_err_mm=float(tr.std(ddof=1) / np.sqrt(len(tr)) * 1000) if len(tr) > 1 else None,
                              mean_rot_err_deg=float(np.degrees(ro.mean())), mean_total_err=float(np.mean([r["mean_total_err"] for r in allrows])),
                              mean_init_err_mm=float(np.mean([r["init_transl_err"] for r in allrows]) * 1000))
        print(f"== {cname}: n={len(allrows)} transl {summary[cname]['mean_transl_err_mm']:.1f} mm, rot {summary[cname]['mean_rot_err_deg']:.2f} deg, "
              f"init {summary[cname]['mean_init_err_mm']:.1f} mm", flush=True)
        (out / "summary.json").write_text(json.dumps(dict(meta=meta, conditions=summary), indent=2, default=str), encoding="utf-8")

    # markdown summary with paired differences vs nominal-equivalent
    lines = ["# Replay fit error by controller condition", "",
             "Exploratory ManiSkill3/Windows platform (torch-Jacobian IK adapter); SIMPLER sysid protocol; not original SIMPLER main.", "",
             "| condition | n | transl err mm (±sem) | rot err deg | total err | init err mm |", "|---|---:|---:|---:|---:|---:|"]
    for c, s in summary.items():
        sem = f" ±{s['sem_transl_err_mm']:.1f}" if s["sem_transl_err_mm"] is not None else ""
        lines.append(f"| {c} | {s['episodes']} | {s['mean_transl_err_mm']:.1f}{sem} | {s['mean_rot_err_deg']:.2f} | {s['mean_total_err']:.4f} | {s['mean_init_err_mm']:.1f} |")
    ref = "nominal" if "nominal" in summary else ("s1_d1_delay0" if "s1_d1_delay0" in summary else None)
    if ref:
        lines += ["", f"## Paired difference of per-episode total error vs {ref}", "", "| condition | n | Δ total err | bootstrap 95% |", "|---|---:|---:|---|"]
        ref_rows = {json.loads(l)["episode_id"]: json.loads(l) for l in (out / f"{ref}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
        rng = np.random.default_rng(0)
        for c in summary:
            if c == ref:
                continue
            rows_c = {json.loads(l)["episode_id"]: json.loads(l) for l in (out / f"{c}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
            common = sorted(set(rows_c) & set(ref_rows))
            d = np.array([rows_c[e]["mean_total_err"] - ref_rows[e]["mean_total_err"] for e in common])
            if len(d) == 0:
                continue
            bs = d[rng.integers(0, len(d), size=(5000, len(d)))].mean(axis=1)
            lines.append(f"| {c} | {len(d)} | {d.mean():+.4f} | [{np.percentile(bs, 2.5):+.4f}, {np.percentile(bs, 97.5):+.4f}] |")
    (out / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
