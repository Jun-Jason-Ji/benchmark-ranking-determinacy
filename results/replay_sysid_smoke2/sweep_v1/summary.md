# Replay fit error by controller condition

Exploratory ManiSkill3/Windows platform (torch-Jacobian IK adapter); SIMPLER sysid protocol; not original SIMPLER main.

| condition | n | transl err mm (±sem) | rot err deg | total err | init err mm |
|---|---:|---:|---:|---:|---:|
| stiff_x0.5 | 40 | 21.4 ±1.0 | 1.86 | 0.0538 | 0.1 |
| nominal | 40 | 17.4 ±1.0 | 1.52 | 0.0439 | 0.1 |

## Paired difference of per-episode total error vs nominal

| condition | n | Δ total err | bootstrap 95% |
|---|---:|---:|---|
| stiff_x0.5 | 40 | +0.0099 | [+0.0075, +0.0123] |