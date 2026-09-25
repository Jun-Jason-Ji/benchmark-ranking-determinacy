# Iso-ratio invariance check: results\replay_sysid\grid

| group (k/d ratio, delay) | conditions | episodes | max |Δp| (mm) | p95 |Δp| (mm) | max |Δ mean err| |
|---|---|---:|---:|---:|---:|
| (0.5, 0) | s0.5_d1_delay0, s0.7_d1.4_delay0, s1_d2_delay0 | 40 | 0.030 | 0.017 | 5.04e-06 |
| (0.5, 1) | s0.5_d1_delay1, s0.7_d1.4_delay1, s1_d2_delay1 | 40 | 0.028 | 0.017 | 4.74e-06 |
| (0.7, 0) | s0.7_d1_delay0, s1.4_d2_delay0 | 40 | 0.051 | 0.017 | 6.97e-06 |
| (0.7, 1) | s0.7_d1_delay1, s1.4_d2_delay1 | 40 | 0.022 | 0.017 | 5.25e-06 |
| (0.714286, 0) | s0.5_d0.7_delay0, s1_d1.4_delay0 | 40 | 0.073 | 0.024 | 1.01e-05 |
| (0.714286, 1) | s0.5_d0.7_delay1, s1_d1.4_delay1 | 40 | 0.031 | 0.024 | 7.40e-06 |
| (1.0, 0) | s0.5_d0.5_delay0, s0.7_d0.7_delay0, s1_d1_delay0, s1.4_d1.4_delay0, s2_d2_delay0 | 40 | 0.138 | 0.042 | 2.54e-05 |
| (1.0, 1) | s0.5_d0.5_delay1, s0.7_d0.7_delay1, s1_d1_delay1, s1.4_d1.4_delay1, s2_d2_delay1 | 40 | 0.137 | 0.042 | 1.78e-05 |
| (1.4, 0) | s0.7_d0.5_delay0, s1.4_d1_delay0 | 40 | 0.104 | 0.040 | 1.71e-05 |
| (1.4, 1) | s0.7_d0.5_delay1, s1.4_d1_delay1 | 40 | 0.082 | 0.040 | 1.37e-05 |
| (1.428571, 0) | s1_d0.7_delay0, s2_d1.4_delay0 | 40 | 0.056 | 0.029 | 1.24e-05 |
| (1.428571, 1) | s1_d0.7_delay1, s2_d1.4_delay1 | 40 | 0.056 | 0.029 | 9.99e-06 |
| (2.0, 0) | s1_d0.5_delay0, s1.4_d0.7_delay0, s2_d1_delay0 | 40 | 0.076 | 0.047 | 2.02e-05 |
| (2.0, 1) | s1_d0.5_delay1, s1.4_d0.7_delay1, s2_d1_delay1 | 40 | 0.075 | 0.047 | 1.70e-05 |

Between-group reference (nominal vs ratio-changing or delayed conditions): median / max |Δp| over episodes


**Verdict:** within-group max |Δp| = 0.138 mm vs tolerance 1.0 mm → invariance HOLDS.