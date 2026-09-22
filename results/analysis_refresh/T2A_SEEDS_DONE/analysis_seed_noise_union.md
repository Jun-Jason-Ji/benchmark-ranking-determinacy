# Policy noise across seed sets on a fixed configuration census: PutEggplantInBasketScene-v1

All seed sets are restricted to the same 64 configurations, so the spread of Δ across them is policy noise alone. `sd_seed` is that spread (sample sd over seed sets); `half-width at S seeds` is 1.96·sd_seed/√S; `S*` is the smallest number of seeds whose half-width falls below |Δ|. The last column is the ordinary i.i.d. episode bootstrap on the first listed seed set, which also carries the configuration variance and answers a different question.

| pair | condition | seeds | Δ per seed | mean Δ | sd_seed | half-width @1 / @3 / @10 | S* | i.i.d. bootstrap 95% (one set) |
|---|---|---:|---|---:|---:|---|---:|---|
| octo-small vs octo-base | nominal | 5 (A',B,C,D,E) | +0.141, -0.031, -0.047, +0.125, +0.094 | +0.056 | 0.089 | 0.174 / 0.100 / 0.055 | 10 | [+0.00, +0.30] |
| octo-small vs octo-base | force_x0.5 | 5 (A',B,C,D,E) | +0.125, +0.109, -0.047, +0.156, +0.188 | +0.106 | 0.091 | 0.178 / 0.103 / 0.056 | 3 | [-0.05, +0.30] |
| octo-small vs octo-base | iso_x0.25 | 4 (A',C,D,E) | +0.156, +0.000, +0.203, +0.031 | +0.098 | 0.097 | 0.191 / 0.110 / 0.060 | 4 | [-0.02, +0.33] |
| octo-small vs octo-base | iso_x4.0 | 4 (A',C,D,E) | +0.297, +0.203, +0.141, +0.172 | +0.203 | 0.068 | 0.132 / 0.076 / 0.042 | 1 | [+0.16, +0.44] |
| octo-small vs octo-base | fric_x0.4 | 5 (A',B,C,D,E) | +0.031, +0.125, +0.016, +0.094, +0.172 | +0.087 | 0.065 | 0.127 / 0.074 / 0.040 | 3 | [-0.12, +0.19] |
| octo-small vs octo-base | dens_x0.5 | 4 (A',C,D,E) | +0.188, +0.016, +0.203, +0.172 | +0.145 | 0.087 | 0.170 / 0.098 / 0.054 | 2 | [+0.03, +0.34] |
| octo-small vs octo-small@hist1 | nominal | 5 (A',B,C,D,E) | +0.172, +0.000, +0.062, +0.047, +0.125 | +0.081 | 0.068 | 0.132 / 0.076 / 0.042 | 3 | [+0.00, +0.33] |
| octo-small vs octo-small@hist1 | force_x0.5 | 5 (A',B,C,D,E) | +0.062, +0.125, +0.031, +0.156, +0.031 | +0.081 | 0.057 | 0.111 / 0.064 / 0.035 | 2 | [-0.09, +0.22] |
| octo-small vs octo-small@hist1 | iso_x0.25 | 4 (A',C,D,E) | +0.250, +0.109, +0.203, +0.094 | +0.164 | 0.075 | 0.147 / 0.085 / 0.046 | 1 | [+0.12, +0.38] |
| octo-small vs octo-small@hist1 | iso_x4.0 | 4 (A',C,D,E) | +0.172, +0.094, +0.047, +0.156 | +0.117 | 0.058 | 0.113 / 0.065 / 0.036 | 1 | [-0.02, +0.36] |
| octo-small vs octo-small@hist1 | fric_x0.4 | 4 (A',C,D,E) | +0.062, +0.188, +0.312, +0.156 | +0.180 | 0.103 | 0.202 / 0.117 / 0.064 | 2 | [-0.08, +0.20] |
| octo-small vs octo-small@hist1 | dens_x0.5 | 4 (A',C,D,E) | +0.141, +0.062, +0.234, +0.016 | +0.113 | 0.096 | 0.188 / 0.108 / 0.059 | 3 | [-0.02, +0.30] |
| octo-small vs octo-base@hist1 | nominal | 5 (A',B,C,D,E) | +0.172, +0.141, +0.062, +0.141, +0.172 | +0.138 | 0.045 | 0.088 / 0.051 / 0.028 | 1 | [+0.02, +0.33] |
| octo-small vs octo-base@hist1 | force_x0.5 | 5 (A',B,C,D,E) | +0.125, +0.203, +0.031, +0.203, +0.219 | +0.156 | 0.079 | 0.155 / 0.089 / 0.049 | 1 | [-0.03, +0.28] |
| octo-small vs octo-base@hist1 | iso_x0.25 | 4 (A',C,D,E) | +0.234, -0.016, +0.141, +0.031 | +0.098 | 0.112 | 0.220 / 0.127 / 0.070 | 6 | [+0.09, +0.38] |
| octo-small vs octo-base@hist1 | iso_x4.0 | 4 (A',C,D,E) | +0.297, +0.094, +0.172, +0.172 | +0.184 | 0.084 | 0.165 / 0.095 / 0.052 | 1 | [+0.14, +0.45] |
| octo-small vs octo-base@hist1 | fric_x0.4 | 4 (A',C,D,E) | +0.031, +0.000, +0.062, +0.141 | +0.059 | 0.060 | 0.118 / 0.068 / 0.037 | 5 | [-0.12, +0.19] |
| octo-small vs octo-base@hist1 | dens_x0.5 | 4 (A',C,D,E) | +0.219, +0.031, +0.234, +0.234 | +0.180 | 0.099 | 0.194 / 0.112 / 0.062 | 2 | [+0.06, +0.38] |
| octo-base vs octo-small@hist1 | nominal | 5 (A',B,C,D,E) | +0.031, +0.031, +0.109, -0.078, +0.031 | +0.025 | 0.067 | 0.131 / 0.076 / 0.041 | 28 | [-0.11, +0.17] |
| octo-base vs octo-small@hist1 | force_x0.5 | 5 (A',B,C,D,E) | -0.062, +0.016, +0.078, +0.000, -0.156 | -0.025 | 0.089 | 0.174 / 0.100 / 0.055 | 49 | [-0.22, +0.09] |
| octo-base vs octo-small@hist1 | iso_x0.25 | 4 (A',C,D,E) | +0.094, +0.109, +0.000, +0.062 | +0.066 | 0.048 | 0.095 / 0.055 / 0.030 | 3 | [-0.06, +0.23] |
| octo-base vs octo-small@hist1 | iso_x4.0 | 4 (A',C,D,E) | -0.125, -0.109, -0.094, -0.016 | -0.086 | 0.049 | 0.095 / 0.055 / 0.030 | 2 | [-0.30, +0.05] |
| octo-base vs octo-small@hist1 | fric_x0.4 | 4 (A',C,D,E) | +0.031, +0.172, +0.219, -0.016 | +0.102 | 0.112 | 0.219 / 0.126 / 0.069 | 5 | [-0.11, +0.17] |
| octo-base vs octo-small@hist1 | dens_x0.5 | 4 (A',C,D,E) | -0.047, +0.047, +0.031, -0.156 | -0.031 | 0.093 | 0.182 / 0.105 / 0.058 | 34 | [-0.19, +0.09] |
| octo-base vs octo-base@hist1 | nominal | 5 (A',B,C,D,E) | +0.031, +0.172, +0.109, +0.016, +0.078 | +0.081 | 0.063 | 0.123 / 0.071 / 0.039 | 3 | [-0.12, +0.19] |
| octo-base vs octo-base@hist1 | force_x0.5 | 5 (A',B,C,D,E) | +0.000, +0.094, +0.078, +0.047, +0.031 | +0.050 | 0.037 | 0.073 / 0.042 / 0.023 | 3 | [-0.14, +0.14] |
| octo-base vs octo-base@hist1 | iso_x0.25 | 4 (A',C,D,E) | +0.078, -0.016, -0.062, +0.000 | +0.000 | 0.058 | 0.115 / 0.066 / 0.036 | ∞ | [-0.09, +0.23] |
| octo-base vs octo-base@hist1 | iso_x4.0 | 4 (A',C,D,E) | +0.000, -0.109, +0.031, +0.000 | -0.020 | 0.062 | 0.121 / 0.070 / 0.038 | 39 | [-0.16, +0.16] |
| octo-base vs octo-base@hist1 | fric_x0.4 | 4 (A',C,D,E) | +0.000, -0.016, -0.031, -0.031 | -0.020 | 0.015 | 0.029 / 0.017 / 0.009 | 3 | [-0.14, +0.14] |
| octo-base vs octo-base@hist1 | dens_x0.5 | 4 (A',C,D,E) | +0.031, +0.016, +0.031, +0.062 | +0.035 | 0.020 | 0.039 / 0.022 / 0.012 | 2 | [-0.12, +0.17] |
| octo-small@hist1 vs octo-base@hist1 | nominal | 5 (A',B,C,D,E) | +0.000, +0.141, +0.000, +0.094, +0.047 | +0.056 | 0.061 | 0.120 / 0.069 / 0.038 | 5 | [-0.12, +0.12] |
| octo-small@hist1 vs octo-base@hist1 | force_x0.5 | 5 (A',B,C,D,E) | +0.062, +0.078, +0.000, +0.047, +0.188 | +0.075 | 0.069 | 0.136 / 0.078 / 0.043 | 4 | [-0.09, +0.22] |
| octo-small@hist1 vs octo-base@hist1 | iso_x0.25 | 4 (A',C,D,E) | -0.016, -0.125, -0.062, -0.062 | -0.066 | 0.045 | 0.088 / 0.051 / 0.028 | 2 | [-0.14, +0.11] |
| octo-small@hist1 vs octo-base@hist1 | iso_x4.0 | 4 (A',C,D,E) | +0.125, +0.000, +0.125, +0.016 | +0.066 | 0.068 | 0.133 / 0.077 / 0.042 | 5 | [-0.03, +0.28] |
| octo-small@hist1 vs octo-base@hist1 | fric_x0.4 | 4 (A',C,D,E) | -0.031, -0.188, -0.250, -0.016 | -0.121 | 0.116 | 0.227 / 0.131 / 0.072 | 4 | [-0.17, +0.11] |
| octo-small@hist1 vs octo-base@hist1 | dens_x0.5 | 4 (A',C,D,E) | +0.078, -0.031, +0.000, +0.219 | +0.066 | 0.111 | 0.219 / 0.126 / 0.069 | 11 | [-0.05, +0.20] |

## Practical reading

- Policy noise at one seed on this task: sd_seed = 0.068 (median over pairs and conditions), so a single-seed Δ carries a ±0.133 uncertainty from the policy alone, before any configuration sampling.
- Averaging 3 seeds (the official SIMPLER protocol) cuts that to ±0.077; 10 seeds to ±0.042.
- Compare with the parameter-induced shift measured on this task (torque ×0.5: ≈0.23): the ambiguity is larger than the policy noise at any realistic seed budget, which is why more evaluation cannot settle it.
