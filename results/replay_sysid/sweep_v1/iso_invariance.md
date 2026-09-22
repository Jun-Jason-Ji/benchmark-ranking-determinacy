# Iso-ratio invariance check: results\replay_sysid\sweep_v1

| group (k/d ratio, delay) | conditions | episodes | max |Δp| (mm) | p95 |Δp| (mm) | max |Δ mean err| |
|---|---|---:|---:|---:|---:|
| ('force', 0) | force_x0.5, nominal | 40 | 0.000 | 0.000 | 1.06e-08 |
| (0.5, 0) | stiff_x0.5, damp_x2.0 | 40 | 0.030 | 0.020 | 5.04e-06 |
| (2.0, 0) | stiff_x2.0, damp_x0.5 | 40 | 0.076 | 0.056 | 2.02e-05 |

Between-group reference (nominal vs ratio-changing or delayed conditions): median / max |Δp| over episodes

- stiff_x2.0: median 17.80 mm, max 484.77 mm
- damp_x0.5: median 17.80 mm, max 484.75 mm
- stiff_x0.5: median 27.44 mm, max 106.19 mm
- damp_x2.0: median 27.44 mm, max 106.18 mm
- delay_1: median 29.20 mm, max 125.17 mm

**Verdict:** within-group max |Δp| = 0.076 mm vs tolerance 1.0 mm → invariance HOLDS.