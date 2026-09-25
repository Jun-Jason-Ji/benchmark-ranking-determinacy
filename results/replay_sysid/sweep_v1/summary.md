# Replay fit error by controller condition

Exploratory ManiSkill3/Windows platform (torch-Jacobian IK adapter); SIMPLER sysid protocol; not original SIMPLER main.

| condition | n | transl err mm (±sem) | rot err deg | total err | init err mm |
|---|---:|---:|---:|---:|---:|
| nominal | 40 | 17.4 ±1.0 | 1.52 | 0.0439 | 0.1 |
| stiff_x0.5 | 40 | 21.4 ±1.0 | 1.86 | 0.0538 | 0.1 |
| stiff_x2.0 | 40 | 20.6 ±1.2 | 1.68 | 0.0499 | 0.1 |
| damp_x0.5 | 40 | 20.6 ±1.2 | 1.68 | 0.0499 | 0.1 |
| damp_x2.0 | 40 | 21.4 ±1.0 | 1.86 | 0.0538 | 0.1 |
| force_x0.5 | 40 | 17.4 ±1.0 | 1.52 | 0.0439 | 0.1 |
| delay_1 | 40 | 20.4 ±0.9 | 1.75 | 0.0508 | 0.1 |

## Paired difference of per-episode total error vs nominal

| condition | n | Δ total err | bootstrap 95% |
|---|---:|---:|---|
| stiff_x0.5 | 40 | +0.0099 | [+0.0075, +0.0123] |
| stiff_x2.0 | 40 | +0.0060 | [+0.0046, +0.0073] |
| damp_x0.5 | 40 | +0.0060 | [+0.0045, +0.0074] |
| damp_x2.0 | 40 | +0.0099 | [+0.0076, +0.0123] |
| force_x0.5 | 40 | -0.0000 | [-0.0000, +0.0000] |
| delay_1 | 40 | +0.0069 | [+0.0045, +0.0093] |