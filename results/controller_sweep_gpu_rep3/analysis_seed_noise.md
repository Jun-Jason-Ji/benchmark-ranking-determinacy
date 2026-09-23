# Policy noise across seed sets on a fixed configuration census: PutEggplantInBasketScene-v1

All seed sets are restricted to the same 64 configurations, so the spread of Δ across them is policy noise alone. `sd_seed` is that spread (sample sd over seed sets); `half-width at S seeds` is 1.96·sd_seed/√S; `S*` is the smallest number of seeds whose half-width falls below |Δ|. The last column is the ordinary i.i.d. episode bootstrap on the first listed seed set, which also carries the configuration variance and answers a different question.

| pair | condition | seeds | Δ per seed | mean Δ | sd_seed | half-width @1 / @3 / @10 | S* | i.i.d. bootstrap 95% (one set) |
|---|---|---:|---|---:|---:|---|---:|---|
| octo-small vs octo-base | nominal | 5 (A',B,C,D,E) | +0.141, -0.031, -0.047, +0.125, +0.094 | +0.056 | 0.089 | 0.174 / 0.100 / 0.055 | 10 | [+0.00, +0.30] |
| octo-small vs octo-base | force_x0.5 | 5 (A',B,C,D,E) | +0.125, +0.109, -0.047, +0.156, +0.188 | +0.106 | 0.091 | 0.178 / 0.103 / 0.056 | 3 | [-0.05, +0.30] |
| octo-small vs octo-small@hist1 | nominal | 5 (A',B,C,D,E) | +0.172, +0.000, +0.062, +0.047, +0.125 | +0.081 | 0.068 | 0.132 / 0.076 / 0.042 | 3 | [+0.00, +0.33] |
| octo-small vs octo-small@hist1 | force_x0.5 | 5 (A',B,C,D,E) | +0.062, +0.125, +0.031, +0.156, +0.031 | +0.081 | 0.057 | 0.111 / 0.064 / 0.035 | 2 | [-0.09, +0.22] |
| octo-small vs octo-base@hist1 | nominal | 5 (A',B,C,D,E) | +0.172, +0.141, +0.062, +0.141, +0.172 | +0.138 | 0.045 | 0.088 / 0.051 / 0.028 | 1 | [+0.02, +0.33] |
| octo-small vs octo-base@hist1 | force_x0.5 | 5 (A',B,C,D,E) | +0.125, +0.203, +0.031, +0.203, +0.219 | +0.156 | 0.079 | 0.155 / 0.089 / 0.049 | 1 | [-0.03, +0.28] |
| octo-base vs octo-small@hist1 | nominal | 5 (A',B,C,D,E) | +0.031, +0.031, +0.109, -0.078, +0.031 | +0.025 | 0.067 | 0.131 / 0.076 / 0.041 | 28 | [-0.11, +0.16] |
| octo-base vs octo-small@hist1 | force_x0.5 | 5 (A',B,C,D,E) | -0.062, +0.016, +0.078, +0.000, -0.156 | -0.025 | 0.089 | 0.174 / 0.100 / 0.055 | 49 | [-0.22, +0.09] |
| octo-base vs octo-base@hist1 | nominal | 5 (A',B,C,D,E) | +0.031, +0.172, +0.109, +0.016, +0.078 | +0.081 | 0.063 | 0.123 / 0.071 / 0.039 | 3 | [-0.12, +0.19] |
| octo-base vs octo-base@hist1 | force_x0.5 | 5 (A',B,C,D,E) | +0.000, +0.094, +0.078, +0.047, +0.031 | +0.050 | 0.037 | 0.073 / 0.042 / 0.023 | 3 | [-0.14, +0.14] |
| octo-small@hist1 vs octo-base@hist1 | nominal | 5 (A',B,C,D,E) | +0.000, +0.141, +0.000, +0.094, +0.047 | +0.056 | 0.061 | 0.120 / 0.069 / 0.038 | 5 | [-0.12, +0.12] |
| octo-small@hist1 vs octo-base@hist1 | force_x0.5 | 5 (A',B,C,D,E) | +0.062, +0.078, +0.000, +0.047, +0.188 | +0.075 | 0.069 | 0.136 / 0.078 / 0.043 | 4 | [-0.09, +0.22] |

## Practical reading

- Policy noise at one seed on this task: sd_seed = 0.068 (median over pairs and conditions), so a single-seed Δ carries a ±0.132 uncertainty from the policy alone, before any configuration sampling.
- Averaging 3 seeds (the official SIMPLER protocol) cuts that to ±0.076; 10 seeds to ±0.042.
- Compare with the parameter-induced shift measured on this task. The torque x0.5 shift is **0.121** on the complete 64-configuration census at S=5 (`analyze_torque_shift_s5.py`); an earlier reading of ~0.23 came from 48 of the 64 configurations and is superseded. At three seeds the policy half-width and the parameter shift are the same order, so a practitioner there cannot tell an identifiability problem from a power problem; at S=5 the half-width drops below the shift and the two separate.
- These half-widths use the sd across whole seed sets as the noise model, which is NOT the estimator the paper's tables use. Those use Eq. (eq:var), pooling per-configuration run variances, and give per-pair three-seed half-widths of 0.075-0.088 on the same census. Both appear in the paper and neither substitutes for the other: this one asks how much a whole-census result moves between seed sets; Eq. (eq:var) asks how precisely one census estimates the benchmark value.
