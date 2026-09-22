# Replay sysid on original SIMPLER main (ms2 + SAPIEN 2, headless WSL): sweep_v1

98 demos; PutCarrotOnPlateInScene-v0; control arm_pd_ee_target_delta_pose_align2_gripper_pd_joint_pos; error = transl L2 + rot arcsin; gripper action 0.

| condition | n | mean total err | transl | rot | init ok |
|---|---:|---:|---:|---:|---:|
| nominal | 98 | 0.04714 | 0.01973 | 0.02741 | 1.00 |
| stiff_x0.5 | 98 | 0.05823 | 0.02499 | 0.03324 | 1.00 |
| stiff_x2.0 | 98 | 0.05353 | 0.02293 | 0.03060 | 1.00 |
| damp_x0.5 | 98 | 0.05354 | 0.02294 | 0.03060 | 1.00 |
| damp_x2.0 | 98 | 0.05823 | 0.02499 | 0.03324 | 1.00 |
| force_x0.5 | 98 | 0.04714 | 0.01973 | 0.02741 | 1.00 |
| delay_1 | 98 | 0.05342 | 0.02212 | 0.03131 | 1.00 |