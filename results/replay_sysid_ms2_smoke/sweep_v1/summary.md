# Replay sysid on original SIMPLER main (ms2 + SAPIEN 2, headless WSL): sweep_v1

3 demos; PutCarrotOnPlateInScene-v0; control arm_pd_ee_target_delta_pose_align2_gripper_pd_joint_pos; error = transl L2 + rot arcsin; gripper action 0.

| condition | n | mean total err | transl | rot | init ok |
|---|---:|---:|---:|---:|---:|
| nominal | 3 | 0.06935 | 0.01485 | 0.05450 | 1.00 |
| stiff_x0.5 | 3 | 0.07734 | 0.02366 | 0.05368 | 1.00 |
| stiff_x2.0 | 3 | 0.07955 | 0.02038 | 0.05917 | 1.00 |
| damp_x0.5 | 3 | 0.07956 | 0.02039 | 0.05918 | 1.00 |
| damp_x2.0 | 3 | 0.07735 | 0.02366 | 0.05368 | 1.00 |
| force_x0.5 | 3 | 0.06935 | 0.01485 | 0.05450 | 1.00 |
| delay_1 | 3 | 0.07296 | 0.01780 | 0.05516 | 1.00 |