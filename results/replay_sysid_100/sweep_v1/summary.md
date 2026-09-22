# Replay fit error by controller condition

Exploratory ManiSkill3/Windows platform (torch-Jacobian IK adapter); SIMPLER sysid protocol; not original SIMPLER main.

| condition | n | transl err mm (±sem) | rot err deg | total err | init err mm |
|---|---:|---:|---:|---:|---:|
| nominal | 98 | 20.2 ±1.3 | 1.62 | 0.0485 | 0.1 |
| stiff_x0.5 | 98 | 23.5 ±1.2 | 1.94 | 0.0574 | 0.1 |
| stiff_x2.0 | 98 | 23.5 ±1.4 | 1.80 | 0.0549 | 0.1 |
| damp_x0.5 | 98 | 23.5 ±1.4 | 1.80 | 0.0549 | 0.1 |
| damp_x2.0 | 98 | 23.5 ±1.2 | 1.94 | 0.0574 | 0.1 |
| force_x0.5 | 98 | 20.2 ±1.3 | 1.62 | 0.0485 | 0.1 |
| delay_1 | 98 | 22.6 ±1.2 | 1.83 | 0.0545 | 0.1 |

## Paired difference of per-episode total error vs nominal

| condition | n | Δ total err | bootstrap 95% |
|---|---:|---:|---|
| stiff_x0.5 | 98 | +0.0089 | [+0.0073, +0.0105] |
| stiff_x2.0 | 98 | +0.0064 | [+0.0055, +0.0072] |
| damp_x0.5 | 98 | +0.0064 | [+0.0055, +0.0072] |
| damp_x2.0 | 98 | +0.0089 | [+0.0073, +0.0105] |
| force_x0.5 | 98 | -0.0000 | [-0.0000, +0.0000] |
| delay_1 | 98 | +0.0060 | [+0.0046, +0.0075] |