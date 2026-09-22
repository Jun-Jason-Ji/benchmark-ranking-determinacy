# Cluster bootstrap by configuration: `results/controller_sweep_gpu`, PutCarrotOnPlateInScene-v1, episodes < 96

The task has **24** distinct initial configurations; episodes beyond that repeat one (same scene, new policy noise). i.i.d. = the paired bootstrap used so far; cluster = configurations resampled with replacement. A verdict that holds i.i.d. but not under clustering was resting on repeated scenes.

| pair | condition | eps | configs | reps/config | Δ | i.i.d. 95% | verdict | cluster 95% | verdict | width ratio |
|---|---|---:|---:|---:|---:|---|---|---|---|---:|
| octo-small vs octo-base | nominal | 48 | 24 | 2.0 | -0.021 | [-0.15, +0.10] | abstain | [-0.19, +0.12] | abstain | 1.25 |
| octo-small vs octo-base | iso_x0.25 | 96 | 24 | 4.0 | -0.021 | [-0.08, +0.04] | abstain | [-0.10, +0.06] | abstain | 1.33 |
| octo-small vs octo-base | iso_x0.5 | 96 | 24 | 4.0 | -0.062 | [-0.14, +0.01] | abstain | [-0.15, +0.01] | abstain | 1.07 |
| octo-small vs octo-base | iso_x2.0 | 48 | 24 | 2.0 | -0.062 | [-0.17, +0.04] | abstain | [-0.17, +0.04] | abstain | 1.00 |
| octo-small vs octo-base | iso_x4.0 | 96 | 24 | 4.0 | +0.000 | [-0.08, +0.08] | abstain | [-0.10, +0.10] | abstain | 1.25 |

## Verdicts that do not survive clustering

- none
