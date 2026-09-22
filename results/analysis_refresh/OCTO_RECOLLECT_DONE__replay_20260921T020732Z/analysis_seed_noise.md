# Policy noise across seed sets on a fixed configuration census: PutEggplantInBasketScene-v1

All seed sets are restricted to the same 64 configurations, so the spread of Δ across them is policy noise alone. `sd_seed` is that spread (sample sd over seed sets); `half-width at S seeds` is 1.96·sd_seed/√S; `S*` is the smallest number of seeds whose half-width falls below |Δ|. The last column is the ordinary i.i.d. episode bootstrap on the first listed seed set, which also carries the configuration variance and answers a different question.

| pair | condition | seeds | Δ per seed | mean Δ | sd_seed | half-width @1 / @3 / @10 | S* | i.i.d. bootstrap 95% (one set) |
|---|---|---:|---|---:|---:|---|---:|---|
| octo-small vs octo-base | nominal | 3 (A',B,C) | +0.141, -0.031, -0.047 | +0.021 | 0.104 | 0.204 / 0.118 / 0.064 | 96 | [+0.00, +0.30] |
| octo-small vs octo-base | force_x0.5 | 3 (A',B,C) | +0.125, +0.109, -0.047 | +0.062 | 0.095 | 0.186 / 0.108 / 0.059 | 9 | [-0.05, +0.30] |
| octo-small vs octo-small@hist1 | nominal | 3 (A',B,C) | +0.172, +0.000, +0.062 | +0.078 | 0.087 | 0.171 / 0.098 / 0.054 | 5 | [+0.00, +0.33] |
| octo-small vs octo-small@hist1 | force_x0.5 | 3 (A',B,C) | +0.062, +0.125, +0.031 | +0.073 | 0.048 | 0.094 / 0.054 / 0.030 | 2 | [-0.09, +0.22] |
| octo-small vs octo-base@hist1 | nominal | 3 (A',B,C) | +0.172, +0.141, +0.062 | +0.125 | 0.056 | 0.110 / 0.064 / 0.035 | 1 | [+0.02, +0.33] |
| octo-small vs octo-base@hist1 | force_x0.5 | 3 (A',B,C) | +0.125, +0.203, +0.031 | +0.120 | 0.086 | 0.169 / 0.097 / 0.053 | 2 | [-0.03, +0.28] |
| octo-base vs octo-small@hist1 | nominal | 3 (A',B,C) | +0.031, +0.031, +0.109 | +0.057 | 0.045 | 0.088 / 0.051 / 0.028 | 3 | [-0.11, +0.16] |
| octo-base vs octo-small@hist1 | force_x0.5 | 3 (A',B,C) | -0.062, +0.016, +0.078 | +0.010 | 0.070 | 0.138 / 0.080 / 0.044 | 176 | [-0.22, +0.09] |
| octo-base vs octo-base@hist1 | nominal | 3 (A',B,C) | +0.031, +0.172, +0.109 | +0.104 | 0.070 | 0.138 / 0.080 / 0.044 | 2 | [-0.12, +0.19] |
| octo-base vs octo-base@hist1 | force_x0.5 | 3 (A',B,C) | +0.000, +0.094, +0.078 | +0.057 | 0.050 | 0.098 / 0.057 / 0.031 | 3 | [-0.14, +0.14] |
| octo-small@hist1 vs octo-base@hist1 | nominal | 3 (A',B,C) | +0.000, +0.141, +0.000 | +0.047 | 0.081 | 0.159 / 0.092 / 0.050 | 12 | [-0.12, +0.12] |
| octo-small@hist1 vs octo-base@hist1 | force_x0.5 | 3 (A',B,C) | +0.062, +0.078, +0.000 | +0.047 | 0.041 | 0.081 / 0.047 / 0.026 | 3 | [-0.09, +0.22] |

## Practical reading

- Policy noise at one seed on this task: sd_seed = 0.070 (median over pairs and conditions), so a single-seed Δ carries a ±0.137 uncertainty from the policy alone, before any configuration sampling.
- Averaging 3 seeds (the official SIMPLER protocol) cuts that to ±0.079; 10 seeds to ±0.043.
- Compare with the parameter-induced shift measured on this task (torque ×0.5: ≈0.23): the ambiguity is larger than the policy noise at any realistic seed budget, which is why more evaluation cannot settle it.
