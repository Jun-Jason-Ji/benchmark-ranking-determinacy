"""Controller / contact sensitivity sweep on the ORIGINAL SIMPLER main stack (ManiSkill2_real2sim + SAPIEN 2.2.2),
run inside WSL with CPU physics and CPU (lavapipe) rendering through the fake-semaphore Vulkan layer
(third_party/vk_fakesemfd). Policies are the same local HTTP Octo servers used by the ManiSkill3 sweep.

Protocol mirrors simpler_env/evaluation/maniskill2_evaluator.py and scripts/octo_bridge.sh: obs_mode rgbd,
robot widowx, control 5 Hz / sim 500 Hz, scene + rgb overlay + robot init per task, obj_variation_mode
'episode' (episode_id -> fixed xy/quat config), run to max_episode_steps, success = final-step info['success'].
Octo never predicts termination in SIMPLER, so early stopping does not apply.

Conditions are the same names as scripts/controller_sweep.py (PRESETS) and are applied as:
  stiffness/damping/force_scale -> arm joint drive properties (set after every reset, verified by read-back)
  delay_steps                   -> execute the action issued N control steps earlier
  fric_scale                    -> object static/dynamic friction (env attribute, then reconfigure; verified from the collision material)
  dens_scale                    -> model_db density (then reconfigure; verified from actor mass)

Usage (WSL, with the render env vars exported):
  python scripts/controller_sweep_ms2.py --policy-name octo-small --policy-url http://127.0.0.1:8767 \
      --task widowx_carrot_on_plate --preset variants_v1 --episodes 24 --output-dir results/controller_sweep_ms2
"""
import argparse
import http.client
import json
import sys
import time
from collections import OrderedDict, deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from task_configs import is_deterministic as _is_det, n_configs as _n_configs  # noqa: E402
SIMPLER = ROOT / "third_party/SimplerEnv"
# Per robot, as simpler_env/utils/env/env_builder.py:get_robot_control_mode selects. The google robot
# uses a different controller family (planner-interpolated delta pose, and a target-delta-pos gripper),
# so the control mode is a task property rather than a constant.
CONTROL_MODE = "arm_pd_ee_target_delta_pose_align2_gripper_pd_joint_pos"
CONTROL_MODE_GOOGLE = ("arm_pd_ee_delta_pose_align_interpolate_by_planner_gripper_pd_joint"
                       "_target_delta_pos_interpolate_by_planner")

TASKS = {
    "widowx_carrot_on_plate": dict(env_id="PutCarrotOnPlateInScene-v0", robot="widowx", scene="bridge_table_1_v1", overlay="ManiSkill2_real2sim/data/real_inpainting/bridge_real_eval_1.png", init_xy=(0.147, 0.028), max_steps=60),
    "widowx_spoon_on_towel": dict(env_id="PutSpoonOnTableClothInScene-v0", robot="widowx", scene="bridge_table_1_v1", overlay="ManiSkill2_real2sim/data/real_inpainting/bridge_real_eval_1.png", init_xy=(0.147, 0.028), max_steps=60),
    "widowx_stack_cube": dict(env_id="StackGreenCubeOnYellowCubeBakedTexInScene-v0", robot="widowx", scene="bridge_table_1_v1", overlay="ManiSkill2_real2sim/data/real_inpainting/bridge_real_eval_1.png", init_xy=(0.147, 0.028), max_steps=60),
    "widowx_put_eggplant_in_basket": dict(env_id="PutEggplantInBasketScene-v0", robot="widowx_sink_camera_setup", scene="bridge_table_1_v2", overlay="ManiSkill2_real2sim/data/real_inpainting/bridge_sink.png", init_xy=(0.127, 0.06), max_steps=120),
    # fractal / google robot. Mirrors scripts/octo_pick_coke_can_visual_matching.sh exactly: control 3 Hz /
    # sim 501 Hz, 80 steps, one robot pose, and the configuration set is the outer product of 4 urdf variants,
    # 3 can orientations and a 5x5 object xy grid = 300. Two traps that silently zero the success rate:
    # the overlay camera is `overhead_camera` here (not `3rd_view_camera`), and the object is placed by
    # `init_xy` (obj_variation_mode='xy'), not by `episode_id` as in the bridge tasks.
    "google_pick_coke_can": dict(
        env_id="GraspSingleOpenedCokeCanInScene-v0", robot="google_robot_static", scene="google_pick_coke_can_1_v4",
        overlay="ManiSkill2_real2sim/data/real_inpainting/google_coke_can_real_eval_1.png",
        init_xy=(0.35, 0.20), max_steps=80, control_freq=3, sim_freq=501,
        camera="overhead_camera", policy_setup="google_robot", obj_mode="xy", control_mode=CONTROL_MODE_GOOGLE,
        obj_grid=dict(x=(-0.35, -0.12, 5), y=(-0.02, 0.42, 5)),
        can_options=["lr_switch", "upright", "laid_vertically"],
        urdf_versions=[None, "recolor_tabletop_visual_matching_1", "recolor_tabletop_visual_matching_2", "recolor_cabinet_visual_matching_1"]),
}


def coke_config(task, ep):
    """episode_id -> (urdf_version, can orientation, object xy) for the fractal visual-matching grid.

    Ordered so that consecutive episode_ids mostly share a build (25 in a row share the can orientation,
    75 share the urdf variant): those two are *build* kwargs, so changing them forces a new env.
    """
    xs = np.linspace(*task["obj_grid"]["x"])
    ys = np.linspace(*task["obj_grid"]["y"])
    n_xy, ncan = len(xs) * len(ys), len(task["can_options"])
    i = ep % (n_xy * ncan * len(task["urdf_versions"]))
    urdf = task["urdf_versions"][i // (n_xy * ncan)]
    can = task["can_options"][(i // n_xy) % ncan]
    k = i % n_xy
    return urdf, can, (float(xs[k // len(ys)]), float(ys[k % len(ys)]))


def build_groups(task, eps):
    """[(build_kwargs, obj_init_options_by_ep, [eps])] -- one group per env rebuild."""
    if task.get("obj_mode", "episode") != "xy":
        return [({}, {ep: {"episode_id": ep} for ep in eps}, list(eps))]
    groups = OrderedDict()
    for ep in eps:
        urdf, can, xy = coke_config(task, ep)
        key = (urdf, can)
        groups.setdefault(key, ([], {}))
        groups[key][0].append(ep)
        groups[key][1][ep] = {"init_xy": np.array(xy)}
    out = []
    for (urdf, can), (group_eps, opts) in groups.items():
        kw = {can: True}
        if urdf is not None:
            kw["urdf_version"] = urdf
        out.append((kw, opts, group_eps))
    return out
PRESETS = {
    "sweep_v1": OrderedDict([("nominal", {}), ("stiff_x0.5", dict(stiffness_scale=0.5)), ("stiff_x2.0", dict(stiffness_scale=2.0)),
                             ("damp_x0.5", dict(damping_scale=0.5)), ("damp_x2.0", dict(damping_scale=2.0)), ("force_x0.5", dict(force_scale=0.5)), ("delay_1", dict(delay_steps=1))]),
    "iso_ratio_v1": OrderedDict([("iso_x0.25", dict(stiffness_scale=0.25, damping_scale=0.25)), ("iso_x0.5", dict(stiffness_scale=0.5, damping_scale=0.5)), ("nominal", {}),
                                 ("iso_x2.0", dict(stiffness_scale=2.0, damping_scale=2.0)), ("iso_x4.0", dict(stiffness_scale=4.0, damping_scale=4.0))]),
    "contact_v1": OrderedDict([("fric_x0.4", dict(fric_scale=0.4)), ("fric_x2.5", dict(fric_scale=2.5)), ("dens_x0.5", dict(dens_scale=0.5)), ("dens_x2.0", dict(dens_scale=2.0))]),
    "variants_v1": OrderedDict([("nominal", {}), ("iso_x0.25", dict(stiffness_scale=0.25, damping_scale=0.25)), ("iso_x4.0", dict(stiffness_scale=4.0, damping_scale=4.0)),
                                ("force_x0.5", dict(force_scale=0.5)), ("fric_x0.4", dict(fric_scale=0.4)), ("dens_x0.5", dict(dens_scale=0.5))]),
    "quick2": OrderedDict([("nominal", {}), ("fric_x0.4", dict(fric_scale=0.4))]),
}
VARIANTS = {"default": dict(ensemble=True, exec_horizon=1, history=2), "noens": dict(ensemble=False, exec_horizon=1, history=2),
            "chunk4": dict(ensemble=False, exec_horizon=4, history=2), "hist1": dict(ensemble=True, exec_horizon=1, history=1)}


def full_condition(c):
    return dict(stiffness_scale=c.get("stiffness_scale", 1.0), damping_scale=c.get("damping_scale", 1.0), force_scale=c.get("force_scale", 1.0),
                delay_steps=int(c.get("delay_steps", 0)), fric_scale=c.get("fric_scale", 1.0), dens_scale=c.get("dens_scale", 1.0))


def parse_policy_name(name):
    base, _, var = name.partition("@")
    return base, (VARIANTS[var] if var else None)


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
                time.sleep(3 * (attempt + 1))
        raise RuntimeError(f"policy server {path} unreachable after {retries} attempts: {last}")

    def health(self):
        return self._req("GET", "/health")

    def reset(self, instruction, seed, config=None):
        return self._req("POST", "/reset", json.dumps({"instruction": instruction, "seed": seed, "config": config, "session": self.session}), {"Content-Type": "application/json"})

    def step(self, img_u8):
        img = np.ascontiguousarray(img_u8, dtype=np.uint8)
        return self._req("POST", "/step", img.tobytes(), {"Content-Type": "application/octet-stream", "X-Shape": ",".join(str(s) for s in img.shape), "X-Session": self.session})


def apply_headless_if_needed():
    """Rendering is required here (rgbd obs); we only make sure the layer env vars are present."""
    import os
    missing = [k for k in ("VK_LAYER_PATH", "VK_INSTANCE_LAYERS") if not os.environ.get(k)]
    return dict(render="sapien2_lavapipe_via_vk_fakesemfd_layer", missing_env=missing)


def set_arm_drives(u, cond, nominal):
    arm = u.agent.controller.controllers["arm"]
    joints = u.agent.robot.get_active_joints()
    st = np.array(nominal["stiffness"]) * cond["stiffness_scale"]
    dp = np.array(nominal["damping"]) * cond["damping_scale"]
    fl = np.array(nominal["force_limit"]) * cond["force_scale"]
    for k, j in enumerate(arm.joint_indices):
        joints[j].set_drive_property(float(st[k]), float(dp[k]), float(fl[k]))
    return dict(stiffness=[float(joints[j].stiffness) for j in arm.joint_indices], damping=[float(joints[j].damping) for j in arm.joint_indices],
                force_limit=[float(joints[j].force_limit) for j in arm.joint_indices])


def policy_seed(args, ep):
    """One seed for the whole run (official SIMPLER protocol) or a per-episode seed (our default)."""
    return args.policy_seed_fixed if args.policy_seed_fixed is not None else args.policy_seed_base + ep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy-name", required=True)
    ap.add_argument("--policy-url", default="http://127.0.0.1:8767")
    ap.add_argument("--task", default="widowx_carrot_on_plate", choices=sorted(TASKS))
    ap.add_argument("--preset", default="variants_v1", choices=sorted(PRESETS))
    ap.add_argument("--conditions", default=None)
    ap.add_argument("--episodes", type=int, default=24)
    ap.add_argument("--episode-offset", type=int, default=0)
    ap.add_argument("--policy-seed-base", type=int, default=20260918)
    ap.add_argument("--policy-seed-fixed", type=int, default=None,
                    help="Use this one policy seed for every episode, as the official SIMPLER protocol does "
                         "(scripts/octo_bridge.sh: one --octo-init-rng per run over the whole config range), "
                         "instead of policy_seed_base + episode_id.")
    ap.add_argument("--output-dir", default="results/controller_sweep_ms2")
    ap.add_argument("--max-steps", type=int, default=None)
    args = ap.parse_args()

    compat = apply_headless_if_needed()
    sys.path.insert(0, str(SIMPLER))
    import gymnasium as gym
    import mani_skill2_real2sim.envs  # noqa: F401
    from sapien.core import Pose  # noqa: F401

    task = TASKS[args.task]
    T = task["max_steps"] if args.max_steps is None else args.max_steps
    base_model, variant_cfg = parse_policy_name(args.policy_name)
    client = PolicyClient(args.policy_url)
    h = client.health()
    assert h.get("model") == base_model, f"server on {args.policy_url} serves {h.get('model')}, wanted {base_model}"
    conds = OrderedDict(PRESETS[args.preset])
    if args.conditions:
        conds = OrderedDict((k, conds[k]) for k in [c.strip() for c in args.conditions.split(",")])
    conds = OrderedDict((k, full_condition(v)) for k, v in conds.items())

    # Config-grid guard (2026-09-19): episode_id maps onto a finite grid of initial configurations, so a range
    # beyond it repeats earlier scenes exactly -- for a deterministic policy those episodes carry no information.
    _env_id = task["env_id"]
    _n_cfg = _n_configs(_env_id)
    if _n_cfg and args.episode_offset + args.episodes > _n_cfg:
        _msg = (f"[config-grid] {_env_id} has {_n_cfg} distinct configurations; requested episodes "
                f"{args.episode_offset}..{args.episode_offset + args.episodes - 1} wrap around and repeat earlier scenes")
        if _is_det(args.policy_name):
            print(_msg + " -- a deterministic policy reproduces them bit-for-bit; run the census instead", flush=True)
        else:
            print(_msg + " (valid extra policy-noise samples, but not new scenes)", flush=True)

    out = ROOT / args.output_dir / args.policy_name / task["env_id"]
    out.mkdir(parents=True, exist_ok=True)
    meta = dict(started_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), args=vars(args), compat=compat, task=task, control_mode=task.get("control_mode", CONTROL_MODE),
                evidence="original_simpler_main_ms2_sapien2_cpu_render_wsl", server_health=h, variant=variant_cfg,
                episode_protocol="run to max_episode_steps unless the policy predicts terminate_episode (RT-1 does, Octo does not), success from final info; common episode_ids and policy seeds")
    (out / f"run_meta_{args.preset}.json").write_text(json.dumps(meta, indent=2, default=str), encoding="utf-8")
    # append-only provenance: the per-preset meta above is overwritten by the next run of the same preset
    with (out / "runs.jsonl").open("a", encoding="utf-8") as _rf:
        print(json.dumps(meta, ensure_ascii=False, default=str), file=_rf)

    for cname, cond in conds.items():
        jsonl = out / f"{cname}.jsonl"
        done = set()
        if jsonl.exists():
            for line in jsonl.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    done.add(json.loads(line)["episode_id"])
        todo = [ep for ep in range(args.episode_offset, args.episode_offset + args.episodes) if ep not in done]
        if not todo:
            print(f"[{cname}] complete", flush=True)
            continue
        cam = task.get("camera", "3rd_view_camera")
        first_ep, effective = todo[0], None
        # The fractal grid varies the urdf version and the can orientation, which are *build* kwargs: each
        # distinct combination needs its own env. Bridge tasks yield a single group, so the loop is a no-op
        # for them and the episode body below is shared.
        for build_kw, obj_opts, group_eps in build_groups(task, sorted(todo)):
            env = gym.make(task["env_id"], obs_mode="rgbd", robot=task["robot"], sim_freq=task.get("sim_freq", 500),
                           control_mode=task.get("control_mode", CONTROL_MODE), control_freq=task.get("control_freq", 5),
                           max_episode_steps=T, scene_name=task["scene"], camera_cfgs={"add_segmentation": True},
                           rgb_overlay_path=str(SIMPLER / task["overlay"]),
                           # env_builder.py picks this per robot; a direct gym.make skips that helper and
                           # then silently drops the real-image overlay
                           rgb_overlay_cameras=[cam], **build_kw)
            u = env.unwrapped
            arm_cfg = u.agent.controller.controllers["arm"].config
            nominal = dict(stiffness=list(map(float, arm_cfg.stiffness)), damping=list(map(float, arm_cfg.damping)),
                           force_limit=list(map(float, arm_cfg.force_limit)))
            # contact conditions need a reconfigure (models are loaded with friction/density at load time)
            u.obj_static_friction = 0.5 * cond["fric_scale"]
            u.obj_dynamic_friction = 0.5 * cond["fric_scale"]
            if cond["dens_scale"] != 1.0:
                for mid, rec in u.model_db.items():
                    rec["density"] = rec.get("density", 1000.0) * cond["dens_scale"]
            robot_init = {"init_xy": np.array(task["init_xy"]), "init_rot_quat": np.array([0, 0, 0, 1.0])}
            env.reset(seed=0, options={"robot_init_options": robot_init, "reconfigure": True,
                                       "obj_init_options": obj_opts[group_eps[0]]})
            delay = cond["delay_steps"]
            if build_kw:
                print(f"[{cname}] build {build_kw} -> {len(group_eps)} episodes", flush=True)
            for ep in group_eps:
                t0 = time.perf_counter()
                obs, info0 = env.reset(seed=ep, options={"robot_init_options": robot_init,
                                                         "obj_init_options": obj_opts[ep]})
                drives = set_arm_drives(u, cond, nominal)
                if effective is None:
                    # bridge put-on-in-scene envs name it episode_source_obj/source_obj; the fractal
                    # grasp_single envs call it obj. Without this the friction/density read-back is
                    # silently None and the condition goes unverified.
                    src = (getattr(u, "episode_source_obj", None) or getattr(u, "source_obj", None)
                           or getattr(u, "obj", None))
                    mat = None
                    try:
                        mat = src.get_collision_shapes()[0].get_physical_material()
                    except Exception:
                        pass
                    effective = dict(cond, drives=drives, obj_static_friction=(float(mat.get_static_friction()) if mat else None),
                                     obj_dynamic_friction=(float(mat.get_dynamic_friction()) if mat else None),
                                     obj_mass=(float(src.mass) if src is not None else None))
                    print(f"[{cname}] effective: {json.dumps(effective)}", flush=True)
                instruction = u.get_language_instruction()
                client.reset(instruction, policy_seed(args, ep), dict(variant_cfg or {}, policy_setup=task.get("policy_setup", "widowx_bridge")))
                queue = deque([np.array([0, 0, 0, 0, 0, 0, 1.0])] * delay) if delay else None
                gripper_closes, prev_grip, inf_s, steps, success, done_flag = 0, 1.0, 0.0, 0, False, False
                terminated_by_policy = False
                for t in range(T):
                    img = obs["image"][cam]["rgb"]
                    r = client.step(img)
                    inf_s += float(r.get("inference_seconds", 0.0))
                    a = np.asarray(r["action"], dtype=np.float64)
                    if delay:
                        queue.append(a)
                        a = queue.popleft()
                    if prev_grip > 0 and a[6] <= 0:
                        gripper_closes += 1
                    prev_grip = a[6]
                    obs, reward, done_flag, truncated, info = env.step(a)
                    steps = t + 1
                    success = bool(info.get("success", False))
                    # RT-1 predicts episode termination; Octo never does. simpler_env's evaluator loops
                    # `while not (predicted_terminated or truncated)` and, when the policy terminates on a
                    # non-final subtask, suppresses the termination and advances the subtask instead. Without
                    # this an RT-1 run is not the protocol being reproduced.
                    if bool(r.get("terminate_episode", False)):
                        if hasattr(u, "is_final_subtask") and not u.is_final_subtask():
                            u.advance_to_next_subtask()
                        else:
                            terminated_by_policy = True
                            break
                    if truncated:
                        break
                flat = {k: (float(v) if isinstance(v, (int, float, np.floating, np.integer, bool)) else str(v)) for k, v in info.items()}
                rec = dict(policy=args.policy_name, env_id=task["env_id"], task=args.task, condition=cname, episode_id=ep,
                           policy_seed=policy_seed(args, ep), instruction=instruction, steps=steps, success=success, info=flat,
                           gripper_close_events=gripper_closes, inference_seconds=inf_s,
                           terminated_by_policy=terminated_by_policy,
                           episode_seconds=time.perf_counter() - t0, effective=effective if ep == first_ep else None,
                           build=(build_kw or None))
                with jsonl.open("a", encoding="utf-8") as f:
                    print(json.dumps(rec, default=str), file=f)
                print(f"[{cname}] ep {ep} success={int(success)} steps={steps} grip_closes={gripper_closes} "
                      f"{rec['episode_seconds']:.1f}s (inf {inf_s:.1f}s)", flush=True)
            env.close()
        rows = [json.loads(l) for l in jsonl.read_text(encoding="utf-8").splitlines() if l.strip()]
        print(f"[{cname}] n={len(rows)} success_rate={np.mean([r['success'] for r in rows]):.3f}", flush=True)
    print("SWEEP_MS2_DONE", out, flush=True)


if __name__ == "__main__":
    main()
