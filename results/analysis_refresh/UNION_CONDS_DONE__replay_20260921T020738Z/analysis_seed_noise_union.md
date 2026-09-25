# Policy noise across seed sets on a fixed configuration census: PutEggplantInBasketScene-v1

All seed sets are restricted to the same 64 configurations, so the spread of Δ across them is policy noise alone. `sd_seed` is that spread (sample sd over seed sets); `half-width at S seeds` is 1.96·sd_seed/√S; `S*` is the smallest number of seeds whose half-width falls below |Δ|. The last column is the ordinary i.i.d. episode bootstrap on the first listed seed set, which also carries the configuration variance and answers a different question.

| pair | condition | seeds | Δ per seed | mean Δ | sd_seed | half-width @1 / @3 / @10 | S* | i.i.d. bootstrap 95% (one set) |
|---|---|---:|---|---:|---:|---|---:|---|
| octo-small vs octo-base | nominal | 3 (A',B,C) | +0.141, -0.031, -0.047 | +0.021 | 0.104 | 0.204 / 0.118 / 0.064 | 96 | [+0.00, +0.30] |
| octo-small vs octo-base | force_x0.5 | 3 (A',B,C) | +0.125, +0.109, -0.047 | +0.062 | 0.095 | 0.186 / 0.108 / 0.059 | 9 | [-0.05, +0.30] |
| octo-small vs octo-base | iso_x0.25 | 2 (A',C) | +0.156, +0.000 | +0.078 | 0.110 | 0.217 / 0.125 / 0.068 | 8 | [-0.02, +0.33] |
| octo-small vs octo-base | iso_x4.0 | 2 (A',C) | +0.297, +0.203 | +0.250 | 0.066 | 0.130 / 0.075 / 0.041 | 1 | [+0.16, +0.44] |
| octo-small vs octo-base | fric_x0.4 | 3 (A',B,C) | +0.031, +0.125, +0.016 | +0.057 | 0.059 | 0.116 / 0.067 / 0.037 | 5 | [-0.12, +0.19] |
| octo-small vs octo-base | dens_x0.5 | 2 (A',C) | +0.188, +0.016 | +0.102 | 0.122 | 0.238 / 0.138 / 0.075 | 6 | [+0.03, +0.34] |
| octo-small vs octo-small@hist1 | nominal | 3 (A',B,C) | +0.172, +0.000, +0.062 | +0.078 | 0.087 | 0.171 / 0.098 / 0.054 | 5 | [+0.00, +0.33] |
| octo-small vs octo-small@hist1 | force_x0.5 | 3 (A',B,C) | +0.062, +0.125, +0.031 | +0.073 | 0.048 | 0.094 / 0.054 / 0.030 | 2 | [-0.09, +0.22] |
| octo-small vs octo-small@hist1 | iso_x0.25 | 2 (A',C) | +0.250, +0.109 | +0.180 | 0.099 | 0.195 / 0.113 / 0.062 | 2 | [+0.12, +0.38] |
| octo-small vs octo-small@hist1 | iso_x4.0 | 2 (A',C) | +0.172, +0.094 | +0.133 | 0.055 | 0.108 / 0.063 / 0.034 | 1 | [-0.02, +0.36] |
| octo-small vs octo-small@hist1 | fric_x0.4 | 2 (A',C) | +0.062, +0.188 | +0.125 | 0.088 | 0.173 / 0.100 / 0.055 | 2 | [-0.08, +0.20] |
| octo-small vs octo-small@hist1 | dens_x0.5 | 2 (A',C) | +0.141, +0.062 | +0.102 | 0.055 | 0.108 / 0.063 / 0.034 | 2 | [-0.02, +0.30] |
| octo-small vs octo-base@hist1 | nominal | 3 (A',B,C) | +0.172, +0.141, +0.062 | +0.125 | 0.056 | 0.110 / 0.064 / 0.035 | 1 | [+0.02, +0.33] |
| octo-small vs octo-base@hist1 | force_x0.5 | 3 (A',B,C) | +0.125, +0.203, +0.031 | +0.120 | 0.086 | 0.169 / 0.097 / 0.053 | 2 | [-0.03, +0.28] |
| octo-small vs octo-base@hist1 | iso_x0.25 | 2 (A',C) | +0.234, -0.016 | +0.109 | 0.177 | 0.346 / 0.200 / 0.110 | 11 | [+0.09, +0.38] |
| octo-small vs octo-base@hist1 | iso_x4.0 | 2 (A',C) | +0.297, +0.094 | +0.195 | 0.144 | 0.282 / 0.163 / 0.089 | 3 | [+0.14, +0.45] |
| octo-small vs octo-base@hist1 | fric_x0.4 | 2 (A',C) | +0.031, +0.000 | +0.016 | 0.022 | 0.043 / 0.025 / 0.014 | 8 | [-0.12, +0.19] |
| octo-small vs octo-base@hist1 | dens_x0.5 | 2 (A',C) | +0.219, +0.031 | +0.125 | 0.133 | 0.260 / 0.150 / 0.082 | 5 | [+0.06, +0.38] |
| octo-base vs octo-small@hist1 | nominal | 3 (A',B,C) | +0.031, +0.031, +0.109 | +0.057 | 0.045 | 0.088 / 0.051 / 0.028 | 3 | [-0.11, +0.17] |
| octo-base vs octo-small@hist1 | force_x0.5 | 3 (A',B,C) | -0.062, +0.016, +0.078 | +0.010 | 0.070 | 0.138 / 0.080 / 0.044 | 176 | [-0.22, +0.09] |
| octo-base vs octo-small@hist1 | iso_x0.25 | 2 (A',C) | +0.094, +0.109 | +0.102 | 0.011 | 0.022 / 0.013 / 0.007 | 1 | [-0.06, +0.23] |
| octo-base vs octo-small@hist1 | iso_x4.0 | 2 (A',C) | -0.125, -0.109 | -0.117 | 0.011 | 0.022 / 0.013 / 0.007 | 1 | [-0.30, +0.05] |
| octo-base vs octo-small@hist1 | fric_x0.4 | 2 (A',C) | +0.031, +0.172 | +0.102 | 0.099 | 0.195 / 0.113 / 0.062 | 4 | [-0.11, +0.17] |
| octo-base vs octo-small@hist1 | dens_x0.5 | 2 (A',C) | -0.047, +0.047 | +0.000 | 0.066 | 0.130 / 0.075 / 0.041 | ∞ | [-0.19, +0.09] |
| octo-base vs octo-base@hist1 | nominal | 3 (A',B,C) | +0.031, +0.172, +0.109 | +0.104 | 0.070 | 0.138 / 0.080 / 0.044 | 2 | [-0.12, +0.19] |
| octo-base vs octo-base@hist1 | force_x0.5 | 3 (A',B,C) | +0.000, +0.094, +0.078 | +0.057 | 0.050 | 0.098 / 0.057 / 0.031 | 3 | [-0.14, +0.14] |
| octo-base vs octo-base@hist1 | iso_x0.25 | 2 (A',C) | +0.078, -0.016 | +0.031 | 0.066 | 0.130 / 0.075 / 0.041 | 18 | [-0.09, +0.23] |
| octo-base vs octo-base@hist1 | iso_x4.0 | 2 (A',C) | +0.000, -0.109 | -0.055 | 0.077 | 0.152 / 0.088 / 0.048 | 8 | [-0.16, +0.16] |
| octo-base vs octo-base@hist1 | fric_x0.4 | 2 (A',C) | +0.000, -0.016 | -0.008 | 0.011 | 0.022 / 0.013 / 0.007 | 8 | [-0.14, +0.14] |
| octo-base vs octo-base@hist1 | dens_x0.5 | 2 (A',C) | +0.031, +0.016 | +0.023 | 0.011 | 0.022 / 0.013 / 0.007 | 1 | [-0.12, +0.17] |
| octo-small@hist1 vs octo-base@hist1 | nominal | 3 (A',B,C) | +0.000, +0.141, +0.000 | +0.047 | 0.081 | 0.159 / 0.092 / 0.050 | 12 | [-0.12, +0.12] |
| octo-small@hist1 vs octo-base@hist1 | force_x0.5 | 3 (A',B,C) | +0.062, +0.078, +0.000 | +0.047 | 0.041 | 0.081 / 0.047 / 0.026 | 3 | [-0.09, +0.22] |
| octo-small@hist1 vs octo-base@hist1 | iso_x0.25 | 2 (A',C) | -0.016, -0.125 | -0.070 | 0.077 | 0.152 / 0.088 / 0.048 | 5 | [-0.14, +0.11] |
| octo-small@hist1 vs octo-base@hist1 | iso_x4.0 | 2 (A',C) | +0.125, +0.000 | +0.062 | 0.088 | 0.173 / 0.100 / 0.055 | 8 | [-0.03, +0.28] |
| octo-small@hist1 vs octo-base@hist1 | fric_x0.4 | 2 (A',C) | -0.031, -0.188 | -0.109 | 0.110 | 0.217 / 0.125 / 0.068 | 4 | [-0.17, +0.11] |
| octo-small@hist1 vs octo-base@hist1 | dens_x0.5 | 2 (A',C) | +0.078, -0.031 | +0.023 | 0.077 | 0.152 / 0.088 / 0.048 | 42 | [-0.05, +0.20] |

## Practical reading

- Policy noise at one seed on this task: sd_seed = 0.074 (median over pairs and conditions), so a single-seed Δ carries a ±0.144 uncertainty from the policy alone, before any configuration sampling.
- Averaging 3 seeds (the official SIMPLER protocol) cuts that to ±0.083; 10 seeds to ±0.046.
- Compare with the parameter-induced shift measured on this task (torque ×0.5: ≈0.23): the ambiguity is larger than the policy noise at any realistic seed budget, which is why more evaluation cannot settle it.
