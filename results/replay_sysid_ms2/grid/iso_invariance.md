# Iso-ratio invariance check: results\replay_sysid_ms2\grid

| group (k/d ratio, delay) | conditions | episodes | max |Δp| (mm) | p95 |Δp| (mm) | max |Δ mean err| |
|---|---|---:|---:|---:|---:|
| (0.5, 0) | s0.5_d1_delay0, s0.7_d1.4_delay0, s1_d2_delay0 | 98 | 0.039 | 0.017 | 7.93e-06 |
| (0.5, 1) | s0.5_d1_delay1, s0.7_d1.4_delay1, s1_d2_delay1 | 98 | 0.039 | 0.017 | 1.00e-05 |
| (0.7, 0) | s0.7_d1_delay0, s1.4_d2_delay0 | 98 | 0.053 | 0.019 | 6.55e-06 |
| (0.7, 1) | s0.7_d1_delay1, s1.4_d2_delay1 | 98 | 0.053 | 0.019 | 6.00e-06 |
| (0.714286, 0) | s0.5_d0.7_delay0, s1_d1.4_delay0 | 98 | 0.076 | 0.028 | 1.17e-05 |
| (0.714286, 1) | s0.5_d0.7_delay1, s1_d1.4_delay1 | 98 | 0.076 | 0.027 | 9.56e-06 |
| (1.0, 0) | s0.5_d0.5_delay0, s0.7_d0.7_delay0, s1_d1_delay0, s1.4_d1.4_delay0, s2_d2_delay0 | 98 | 0.207 | 0.040 | 2.43e-05 |
| (1.0, 1) | s0.5_d0.5_delay1, s0.7_d0.7_delay1, s1_d1_delay1, s1.4_d1.4_delay1, s2_d2_delay1 | 98 | 0.207 | 0.039 | 2.14e-05 |
| (1.4, 0) | s0.7_d0.5_delay0, s1.4_d1_delay0 | 98 | 0.152 | 0.040 | 1.82e-05 |
| (1.4, 1) | s0.7_d0.5_delay1, s1.4_d1_delay1 | 98 | 0.152 | 0.040 | 1.87e-05 |
| (1.428571, 0) | s1_d0.7_delay0, s2_d1.4_delay0 | 98 | 0.101 | 0.029 | 1.20e-05 |
| (1.428571, 1) | s1_d0.7_delay1, s2_d1.4_delay1 | 98 | 0.101 | 0.029 | 1.15e-05 |
| (2.0, 0) | s1_d0.5_delay0, s1.4_d0.7_delay0, s2_d1_delay0 | 98 | 0.141 | 0.043 | 2.28e-05 |
| (2.0, 1) | s1_d0.5_delay1, s1.4_d0.7_delay1, s2_d1_delay1 | 98 | 0.141 | 0.044 | 2.10e-05 |

Between-group reference (nominal vs ratio-changing or delayed conditions): median / max |Δp| over episodes


**Verdict:** within-group max |Δp| = 0.207 mm vs tolerance 1.0 mm → invariance HOLDS.