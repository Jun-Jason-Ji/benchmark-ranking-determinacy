"""Dump one ms2 eggplant observation frame, exactly as controller_sweep_ms2 builds the env."""
import sys
from pathlib import Path
import numpy as np
ROOT = Path("/mnt/e/research/the_world")
SIMPLER = ROOT / "third_party/SimplerEnv"
sys.path.insert(0, str(SIMPLER / "ManiSkill2_real2sim"))
sys.path.insert(0, str(SIMPLER))
import mani_skill2_real2sim.envs  # noqa
import gymnasium as gym
from PIL import Image

env = gym.make("PutEggplantInBasketScene-v0", obs_mode="rgbd", robot="widowx_sink_camera_setup",
               sim_freq=500, control_mode="arm_pd_ee_target_delta_pose_align2_gripper_pd_joint_pos",
               control_freq=5, max_episode_steps=120, scene_name="bridge_table_1_v2",
               camera_cfgs={"add_segmentation": True},
               rgb_overlay_path=str(SIMPLER / "ManiSkill2_real2sim/data/real_inpainting/bridge_sink.png"),
               rgb_overlay_cameras=["3rd_view_camera"])
opts = {"robot_init_options": {"init_xy": np.array([0.127, 0.06]), "init_rot_quat": np.array([0, 0, 0, 1.0])}}
obs, _ = env.reset(seed=0, options=dict(opts, obj_init_options={"episode_id": 0}, reconfigure=True))
img = obs["image"]["3rd_view_camera"]["rgb"]
print("dtype", img.dtype, "shape", img.shape, "min", img.min(), "max", img.max(), "mean", float(np.mean(img)))
Image.fromarray(np.asarray(img, dtype=np.uint8)).save("/mnt/e/research/the_world/results/ms2_frame_ep0.png")
print("saved")
