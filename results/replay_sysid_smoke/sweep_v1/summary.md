# Replay fit error by controller condition

Exploratory ManiSkill3/Windows platform (torch-Jacobian IK adapter); SIMPLER sysid protocol; not original SIMPLER main.

| condition | n | transl err mm (±sem) | rot err deg | total err | init err mm |
|---|---:|---:|---:|---:|---:|
| nominal | 3 | 17.1 ±1.1 | 3.13 | 0.0718 | 0.1 |
| stiff_x0.5 | 3 | 19.5 ±0.5 | 3.10 | 0.0737 | 0.1 |
| stiff_x2.0 | 3 | 21.5 ±1.5 | 3.39 | 0.0807 | 0.1 |
| damp_x0.5 | 3 | 21.5 ±1.5 | 3.39 | 0.0807 | 0.1 |
| damp_x2.0 | 3 | 19.5 ±0.5 | 3.10 | 0.0737 | 0.1 |
| force_x0.5 | 3 | 17.1 ±1.1 | 3.13 | 0.0718 | 0.1 |
| delay_1 | 3 | 18.7 ±0.6 | 3.18 | 0.0743 | 0.1 |

## Paired difference of per-episode total error vs nominal

| condition | n | Δ total err | bootstrap 95% |
|---|---:|---:|---|
| stiff_x0.5 | 3 | +0.0019 | [-0.0036, +0.0068] |
| stiff_x2.0 | 3 | +0.0089 | [+0.0053, +0.0118] |
| damp_x0.5 | 3 | +0.0089 | [+0.0054, +0.0118] |
| damp_x2.0 | 3 | +0.0019 | [-0.0036, +0.0068] |
| force_x0.5 | 3 | +0.0000 | [+0.0000, +0.0000] |
| delay_1 | 3 | +0.0025 | [-0.0003, +0.0042] |