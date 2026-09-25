# Confirmatory native-task results

All 80 prespecified cells completed: 20480 rollouts, 1024 new paired initial scenes per task/setting. The 20-difference primary family uses exact paired-discordance intervals with Bonferroni/union-bound simultaneous coverage at least 95% under the independent-scene binomial sampling assumptions.

| Task | Primary endpoint | Nominal difference | Simultaneous nominal interval | Five-setting envelope | Decision |
|---|---|---:|---:|---:|---|
| PickCube-v1 | ever50 | +0.327 | [+0.262, +0.387] | [+0.241, +0.439] | joint |
| PickCube-v1 | at50 | +0.329 | [+0.263, +0.390] | [+0.247, +0.441] | joint |
| PushCube-v1 | ever50 | +0.195 | [+0.150, +0.238] | [+0.123, +0.369] | joint |
| PushCube-v1 | at50 | -0.298 | [-0.354, -0.237] | [-0.440, -0.154] | cartesian |

Prespecified PushCube reversal conjunction: **True**.
Prespecified PickCube positive-ordering contrast: **True**.

These results are conditional on the fixed checkpoints, build, endpoints, five settings and sampling assumptions. They are not cross-engine or real-world confirmation. Distinct PRNG stream seeds and unique states do not empirically prove stochastic independence.

## Complete family

| Task | Endpoint | Setting | Joint / 1024 | Cartesian / 1024 | Difference | Simultaneous interval |
|---|---|---|---:|---:|---:|---:|
| PickCube-v1 | ever50 | nominal | 994 | 659 | +0.327 | [+0.262, +0.387] |
| PickCube-v1 | ever50 | gain_half | 983 | 667 | +0.309 | [+0.241, +0.371] |
| PickCube-v1 | ever50 | gain_double | 992 | 615 | +0.368 | [+0.302, +0.429] |
| PickCube-v1 | ever50 | force_half | 995 | 680 | +0.308 | [+0.243, +0.367] |
| PickCube-v1 | ever50 | force_double | 996 | 608 | +0.379 | [+0.313, +0.439] |
| PickCube-v1 | at50 | nominal | 985 | 648 | +0.329 | [+0.263, +0.390] |
| PickCube-v1 | at50 | gain_half | 976 | 654 | +0.314 | [+0.247, +0.377] |
| PickCube-v1 | at50 | gain_double | 983 | 604 | +0.370 | [+0.303, +0.432] |
| PickCube-v1 | at50 | force_half | 993 | 673 | +0.312 | [+0.248, +0.373] |
| PickCube-v1 | at50 | force_double | 987 | 597 | +0.381 | [+0.315, +0.441] |
| PushCube-v1 | ever50 | nominal | 1024 | 824 | +0.195 | [+0.150, +0.238] |
| PushCube-v1 | ever50 | gain_half | 1022 | 695 | +0.319 | [+0.265, +0.369] |
| PushCube-v1 | ever50 | gain_double | 1018 | 844 | +0.170 | [+0.123, +0.214] |
| PushCube-v1 | ever50 | force_half | 1024 | 831 | +0.188 | [+0.144, +0.231] |
| PushCube-v1 | ever50 | force_double | 1024 | 731 | +0.286 | [+0.235, +0.334] |
| PushCube-v1 | at50 | nominal | 18 | 323 | -0.298 | [-0.354, -0.237] |
| PushCube-v1 | at50 | gain_half | 57 | 279 | -0.217 | [-0.277, -0.154] |
| PushCube-v1 | at50 | gain_double | 26 | 289 | -0.257 | [-0.315, -0.194] |
| PushCube-v1 | at50 | force_half | 15 | 284 | -0.263 | [-0.316, -0.205] |
| PushCube-v1 | at50 | force_double | 17 | 409 | -0.383 | [-0.440, -0.320] |

## Predetermined concentration-bound sensitivity

For independent bounded paired outcomes in [-1,1], a simultaneous Hoeffding family uses radius sqrt(2 log(40/0.05)/1024). It does not require normally distributed paired outcomes; independence remains an assumption.

| Task | Endpoint | Hoeffding envelope | Decision |
|---|---|---:|---|
| PickCube-v1 | ever50 | [+0.193, +0.493] | joint |
| PickCube-v1 | at50 | [+0.198, +0.495] | joint |
| PushCube-v1 | ever50 | [+0.056, +0.434] | joint |
| PushCube-v1 | at50 | [-0.497, -0.103] | cartesian |

## Predetermined diagnostics

Dwell, step-100 outcomes and first-hit times are descriptive diagnostics only. They are not additional confirmatory claims. Full batch counts, success sequences and initial/final states are preserved.

| Task | Setting | Pipeline | Ever50 | At50 | Ever100 | At100 | Dwell10 by50 | Dwell10 by100 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| PickCube-v1 | nominal | pd_joint_delta_pos | 994 | 985 | 1015 | 1006 | 975 | 1012 |
| PickCube-v1 | nominal | pd_ee_delta_pos | 659 | 648 | 677 | 656 | 626 | 669 |
| PickCube-v1 | gain_half | pd_joint_delta_pos | 983 | 976 | 1008 | 1002 | 959 | 1007 |
| PickCube-v1 | gain_half | pd_ee_delta_pos | 667 | 654 | 684 | 660 | 630 | 674 |
| PickCube-v1 | gain_double | pd_joint_delta_pos | 992 | 983 | 1008 | 1001 | 981 | 1006 |
| PickCube-v1 | gain_double | pd_ee_delta_pos | 615 | 604 | 628 | 613 | 585 | 615 |
| PickCube-v1 | force_half | pd_joint_delta_pos | 995 | 993 | 1017 | 1013 | 980 | 1017 |
| PickCube-v1 | force_half | pd_ee_delta_pos | 680 | 673 | 696 | 684 | 658 | 693 |
| PickCube-v1 | force_double | pd_joint_delta_pos | 996 | 987 | 1017 | 1013 | 971 | 1015 |
| PickCube-v1 | force_double | pd_ee_delta_pos | 608 | 597 | 621 | 605 | 574 | 613 |
| PushCube-v1 | nominal | pd_joint_delta_pos | 1024 | 18 | 1024 | 11 | 673 | 674 |
| PushCube-v1 | nominal | pd_ee_delta_pos | 824 | 323 | 826 | 313 | 366 | 367 |
| PushCube-v1 | gain_half | pd_joint_delta_pos | 1022 | 57 | 1022 | 50 | 780 | 783 |
| PushCube-v1 | gain_half | pd_ee_delta_pos | 695 | 279 | 701 | 262 | 327 | 333 |
| PushCube-v1 | gain_double | pd_joint_delta_pos | 1018 | 26 | 1018 | 25 | 582 | 583 |
| PushCube-v1 | gain_double | pd_ee_delta_pos | 844 | 289 | 844 | 283 | 326 | 326 |
| PushCube-v1 | force_half | pd_joint_delta_pos | 1024 | 15 | 1024 | 15 | 688 | 690 |
| PushCube-v1 | force_half | pd_ee_delta_pos | 831 | 284 | 835 | 271 | 354 | 361 |
| PushCube-v1 | force_double | pd_joint_delta_pos | 1024 | 17 | 1024 | 17 | 727 | 727 |
| PushCube-v1 | force_double | pd_ee_delta_pos | 731 | 409 | 737 | 367 | 437 | 453 |
