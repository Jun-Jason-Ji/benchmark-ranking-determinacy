# Cluster bootstrap by configuration: `results/controller_sweep_gpu`, PutEggplantInBasketScene-v1, episodes < 64

The task has **64** distinct initial configurations; episodes beyond that repeat one (same scene, new policy noise). i.i.d. = the paired bootstrap used so far; cluster = configurations resampled with replacement. A verdict that holds i.i.d. but not under clustering was resting on repeated scenes.

| pair | condition | eps | configs | reps/config | Δ | i.i.d. 95% | verdict | cluster 95% | verdict | width ratio |
|---|---|---:|---:|---:|---:|---|---|---|---|---:|
| octo-small vs octo-base | nominal | 64 | 64 | 1.0 | +0.250 | [+0.11, +0.39] | + | [+0.11, +0.39] | + | 1.00 |
| octo-small vs octo-base | iso_x0.25 | 64 | 64 | 1.0 | +0.047 | [-0.11, +0.20] | abstain | [-0.11, +0.20] | abstain | 1.00 |
| octo-small vs octo-base | iso_x4.0 | 64 | 64 | 1.0 | +0.234 | [+0.06, +0.39] | + | [+0.06, +0.41] | + | 1.05 |
| octo-small vs octo-base | force_x0.5 | 64 | 64 | 1.0 | +0.188 | [+0.03, +0.34] | + | [+0.03, +0.34] | + | 1.00 |
| octo-small vs octo-base | fric_x0.4 | 64 | 64 | 1.0 | +0.016 | [-0.14, +0.17] | abstain | [-0.14, +0.17] | abstain | 1.00 |
| octo-small vs octo-base | dens_x0.5 | 64 | 64 | 1.0 | +0.109 | [-0.03, +0.25] | abstain | [-0.03, +0.25] | abstain | 1.00 |
| octo-small vs octo-small@hist1 | nominal | 64 | 64 | 1.0 | +0.141 | [-0.02, +0.30] | abstain | [-0.02, +0.30] | abstain | 1.00 |
| octo-small vs octo-small@hist1 | iso_x0.25 | 64 | 64 | 1.0 | +0.141 | [-0.02, +0.30] | abstain | [-0.02, +0.30] | abstain | 1.00 |
| octo-small vs octo-small@hist1 | iso_x4.0 | 64 | 64 | 1.0 | +0.203 | [+0.05, +0.36] | + | [+0.05, +0.36] | + | 1.00 |
| octo-small vs octo-small@hist1 | force_x0.5 | 64 | 64 | 1.0 | +0.109 | [-0.05, +0.27] | abstain | [-0.05, +0.27] | abstain | 1.00 |
| octo-small vs octo-small@hist1 | fric_x0.4 | 64 | 64 | 1.0 | +0.156 | [+0.00, +0.31] | abstain | [+0.00, +0.31] | abstain | 1.00 |
| octo-small vs octo-small@hist1 | dens_x0.5 | 64 | 64 | 1.0 | +0.062 | [-0.08, +0.20] | abstain | [-0.08, +0.20] | abstain | 1.00 |
| octo-small vs octo-base@hist1 | nominal | 64 | 64 | 1.0 | +0.188 | [+0.03, +0.34] | + | [+0.03, +0.34] | + | 1.00 |
| octo-small vs octo-base@hist1 | iso_x0.25 | 64 | 64 | 1.0 | +0.172 | [+0.03, +0.31] | + | [+0.03, +0.31] | + | 1.00 |
| octo-small vs octo-base@hist1 | iso_x4.0 | 64 | 64 | 1.0 | +0.250 | [+0.09, +0.41] | + | [+0.09, +0.41] | + | 1.00 |
| octo-small vs octo-base@hist1 | force_x0.5 | 64 | 64 | 1.0 | +0.172 | [+0.02, +0.33] | + | [+0.02, +0.33] | + | 1.00 |
| octo-small vs octo-base@hist1 | fric_x0.4 | 64 | 64 | 1.0 | +0.094 | [-0.05, +0.25] | abstain | [-0.06, +0.23] | abstain | 1.00 |
| octo-small vs octo-base@hist1 | dens_x0.5 | 64 | 64 | 1.0 | +0.219 | [+0.09, +0.36] | + | [+0.09, +0.36] | + | 1.00 |
| octo-base vs octo-small@hist1 | nominal | 64 | 64 | 1.0 | -0.109 | [-0.25, +0.03] | abstain | [-0.25, +0.03] | abstain | 1.00 |
| octo-base vs octo-small@hist1 | iso_x0.25 | 64 | 64 | 1.0 | +0.094 | [-0.06, +0.25] | abstain | [-0.06, +0.23] | abstain | 0.95 |
| octo-base vs octo-small@hist1 | iso_x4.0 | 64 | 64 | 1.0 | -0.031 | [-0.20, +0.14] | abstain | [-0.20, +0.16] | abstain | 1.05 |
| octo-base vs octo-small@hist1 | force_x0.5 | 64 | 64 | 1.0 | -0.078 | [-0.22, +0.06] | abstain | [-0.22, +0.06] | abstain | 1.00 |
| octo-base vs octo-small@hist1 | fric_x0.4 | 64 | 64 | 1.0 | +0.141 | [-0.02, +0.30] | abstain | [-0.02, +0.28] | abstain | 0.95 |
| octo-base vs octo-small@hist1 | dens_x0.5 | 64 | 64 | 1.0 | -0.047 | [-0.19, +0.08] | abstain | [-0.19, +0.09] | abstain | 1.06 |
| octo-base vs octo-base@hist1 | nominal | 64 | 64 | 1.0 | -0.062 | [-0.22, +0.09] | abstain | [-0.22, +0.09] | abstain | 1.00 |
| octo-base vs octo-base@hist1 | iso_x0.25 | 64 | 64 | 1.0 | +0.125 | [+0.00, +0.27] | abstain | [-0.02, +0.27] | abstain | 1.06 |
| octo-base vs octo-base@hist1 | iso_x4.0 | 64 | 64 | 1.0 | +0.016 | [-0.14, +0.17] | abstain | [-0.14, +0.17] | abstain | 1.00 |
| octo-base vs octo-base@hist1 | force_x0.5 | 64 | 64 | 1.0 | -0.016 | [-0.16, +0.12] | abstain | [-0.16, +0.12] | abstain | 1.00 |
| octo-base vs octo-base@hist1 | fric_x0.4 | 64 | 64 | 1.0 | +0.078 | [-0.08, +0.23] | abstain | [-0.08, +0.23] | abstain | 1.00 |
| octo-base vs octo-base@hist1 | dens_x0.5 | 64 | 64 | 1.0 | +0.109 | [-0.05, +0.27] | abstain | [-0.05, +0.27] | abstain | 1.00 |
| octo-small@hist1 vs octo-base@hist1 | nominal | 64 | 64 | 1.0 | +0.047 | [-0.09, +0.19] | abstain | [-0.09, +0.19] | abstain | 1.00 |
| octo-small@hist1 vs octo-base@hist1 | iso_x0.25 | 64 | 64 | 1.0 | +0.031 | [-0.12, +0.19] | abstain | [-0.12, +0.19] | abstain | 1.00 |
| octo-small@hist1 vs octo-base@hist1 | iso_x4.0 | 64 | 64 | 1.0 | +0.047 | [-0.09, +0.19] | abstain | [-0.09, +0.19] | abstain | 1.00 |
| octo-small@hist1 vs octo-base@hist1 | force_x0.5 | 64 | 64 | 1.0 | +0.062 | [-0.09, +0.22] | abstain | [-0.08, +0.20] | abstain | 0.90 |
| octo-small@hist1 vs octo-base@hist1 | fric_x0.4 | 64 | 64 | 1.0 | -0.062 | [-0.22, +0.09] | abstain | [-0.22, +0.09] | abstain | 1.00 |
| octo-small@hist1 vs octo-base@hist1 | dens_x0.5 | 64 | 64 | 1.0 | +0.156 | [+0.02, +0.30] | + | [+0.02, +0.30] | + | 1.00 |

## Verdicts that do not survive clustering

- none
