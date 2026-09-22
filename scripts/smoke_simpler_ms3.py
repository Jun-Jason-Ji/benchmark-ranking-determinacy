"""Windows-compatible ManiSkill3 Bridge scene smoke test, not a policy benchmark.

Use CPU physics and GPU Vulkan rendering, with the explicit process-local
ms3_windows_compat adapter. This changes IK; no historical scores are claimed.
"""
import argparse
import importlib.metadata
import json
import os
import platform
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MS_ASSET_DIR", str(ROOT / "data/maniskill-assets"))


def to_json(value):
    if isinstance(value, dict):
        return {k: to_json(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [to_json(v) for v in value]
    if hasattr(value, "detach"):
        return value.detach().cpu().tolist()
    if hasattr(value, "tolist"):
        return value.tolist()
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-id", default="PutEggplantInBasketScene-v1")
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--action-mode", choices=["zero", "lift_probe"], default="zero")
    parser.add_argument("--seed", type=int, default=20260918)
    parser.add_argument("--output-dir", default="results/simpler_ms3_smoke")
    args = parser.parse_args()
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    record = dict(vars(args), status="started", evidence="simulator_smoke_only",
                  policy=args.action_mode + "_debug_only", platform=platform.platform(),
                  original_simpler_reproduction=False, sim_backend="cpu")
    started = time.perf_counter()
    env = None

    def save():
        record["elapsed_seconds"] = time.perf_counter() - started
        (out / "result.json").write_text(json.dumps(to_json(record), indent=2), encoding="utf-8")

    save()
    try:
        import gymnasium as gym
        import imageio.v2 as imageio
        import numpy as np
        import sapien
        import torch
        import mani_skill.envs
        from mani_skill.envs.tasks.digital_twins.bridge_dataset_eval import put_on_in_scene
        from ms3_windows_compat import apply_compatibility
        record["compatibility_adapter"] = apply_compatibility()

        record["versions"] = {p: importlib.metadata.version(p)
                              for p in ["sapien", "mani_skill", "torch", "gymnasium", "numpy"]}
        device = sapien.Device("cuda")
        backend = "pci:" + device.pci_string
        record.update(render_backend=backend, render_device=device.name,
                      torch_cuda_available=torch.cuda.is_available())
        save()
        env = gym.make(args.env_id, obs_mode="rgb+segmentation", num_envs=1,
                       sim_backend="cpu", render_backend=backend)
        obs, info = env.reset(seed=args.seed)
        record["instruction"] = env.unwrapped.get_language_instruction()
        record["action_shape"] = list(env.action_space.shape)
        initial_qpos = env.unwrapped.agent.robot.get_qpos().clone()
        rgb = obs["sensor_data"]["3rd_view_camera"]["rgb"][0].detach().cpu().numpy()
        imageio.imwrite(out / "initial_frame.png", rgb.astype(np.uint8))
        record["image_shape"] = list(rgb.shape)
        if rgb.shape != (480, 640, 3) or not np.isfinite(rgb).all() or rgb.std() < 1:
            raise ValueError("Invalid or blank RGB observation")
        step_start = time.perf_counter()
        record["completed_steps"] = 0
        for i in range(args.steps):
            action = np.zeros(env.action_space.shape, dtype=np.float32)
            if args.action_mode == "lift_probe":
                action[..., 2] = 0.005
                action[..., 6] = 1.0
            obs, reward, terminated, truncated, info = env.step(action)
            record["completed_steps"] = i + 1
            if bool(terminated.any()) or bool(truncated.any()):
                break
        record["step_wall_seconds"] = time.perf_counter() - step_start
        record["final_info"] = info
        final_qpos = env.unwrapped.agent.robot.get_qpos()
        if not torch.isfinite(final_qpos).all():
            raise ValueError("Non-finite joint positions")
        record["joint_displacement_norm"] = float(torch.linalg.vector_norm(final_qpos - initial_qpos))
        if args.action_mode == "lift_probe" and record["joint_displacement_norm"] <= 1e-5:
            raise ValueError("Motion probe produced no measurable joint change")
        final_rgb = obs["sensor_data"]["3rd_view_camera"]["rgb"][0].detach().cpu().numpy()
        imageio.imwrite(out / "final_frame.png", final_rgb.astype(np.uint8))
        record["status"] = "passed"
    except Exception as error:
        record.update(status="failed", error_type=type(error).__name__, error=str(error))
        raise
    finally:
        save()
        print(json.dumps(to_json(record), indent=2), flush=True)
        if env is not None:
            env.close()


if __name__ == "__main__":
    main()
