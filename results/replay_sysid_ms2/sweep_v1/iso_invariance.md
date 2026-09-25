# Iso-ratio invariance check: results\replay_sysid_ms2\sweep_v1

| group (k/d ratio, delay) | conditions | episodes | max |Δp| (mm) | p95 |Δp| (mm) | max |Δ mean err| |
|---|---|---:|---:|---:|---:|
| ('force', 0) | force_x0.5, nominal | 98 | 0.050 | 0.000 | 1.71e-06 |
| (0.5, 0) | stiff_x0.5, damp_x2.0 | 98 | 0.039 | 0.019 | 7.93e-06 |
| (2.0, 0) | stiff_x2.0, damp_x0.5 | 98 | 0.141 | 0.052 | 2.28e-05 |

Between-group reference (nominal vs ratio-changing or delayed conditions): median / max |Δp| over episodes

- stiff_x2.0: median 17.01 mm, max 64.75 mm
- damp_x0.5: median 17.02 mm, max 64.78 mm
- damp_x2.0: median 27.61 mm, max 96.77 mm
- stiff_x0.5: median 27.61 mm, max 96.77 mm
- delay_1: median 29.27 mm, max 129.77 mm

**Verdict:** within-group max |Δp| = 0.141 mm vs tolerance 1.0 mm → invariance HOLDS.