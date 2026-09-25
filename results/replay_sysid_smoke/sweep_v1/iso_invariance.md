# Iso-ratio invariance check: results\replay_sysid_smoke\sweep_v1

| group (k/d ratio, delay) | conditions | episodes | max |Δp| (mm) | p95 |Δp| (mm) | max |Δ mean err| |
|---|---|---:|---:|---:|---:|
| ('force', 0) | force_x0.5, nominal | 3 | 0.000 | 0.000 | 0.00e+00 |
| (0.5, 0) | stiff_x0.5, damp_x2.0 | 3 | 0.012 | 0.011 | 2.93e-06 |
| (2.0, 0) | stiff_x2.0, damp_x0.5 | 3 | 0.036 | 0.035 | 1.85e-05 |

Between-group reference (nominal vs ratio-changing or delayed conditions): median / max |Δp| over episodes

- stiff_x2.0: median 12.37 mm, max 16.43 mm
- damp_x0.5: median 12.39 mm, max 16.44 mm
- stiff_x0.5: median 21.24 mm, max 27.92 mm
- damp_x2.0: median 21.24 mm, max 27.92 mm
- delay_1: median 27.50 mm, max 27.56 mm

**Verdict:** within-group max |Δp| = 0.036 mm vs tolerance 1.0 mm → invariance HOLDS.