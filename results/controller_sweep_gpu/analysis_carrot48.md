# Controller sweep: descriptive analysis

Exploratory ManiSkill3/Windows platform (torch-Jacobian IK adapter), not original SIMPLER. Paired by episode_id; Wilson 95% for rates; paired bootstrap 95% for differences.

## Success rates

| policy | env | condition | n | success | rate | Wilson 95% | mean steps | mean inference s/step |
|---|---|---|---:|---:|---:|---|---:|---:|
| octo-base | PutCarrotOnPlateInScene-v1 | damp_x0.5 | 48 | 6 | 0.125 | [0.06, 0.25] | 60.0 | 0.22 |
| octo-base | PutCarrotOnPlateInScene-v1 | damp_x2.0 | 48 | 8 | 0.167 | [0.09, 0.30] | 60.0 | 0.23 |
| octo-base | PutCarrotOnPlateInScene-v1 | delay_1 | 48 | 4 | 0.083 | [0.03, 0.20] | 60.0 | 0.20 |
| octo-base | PutCarrotOnPlateInScene-v1 | force_x0.5 | 48 | 6 | 0.125 | [0.06, 0.25] | 60.0 | 0.23 |
| octo-base | PutCarrotOnPlateInScene-v1 | nominal | 48 | 7 | 0.146 | [0.07, 0.27] | 60.0 | 0.17 |
| octo-base | PutCarrotOnPlateInScene-v1 | stiff_x0.5 | 48 | 7 | 0.146 | [0.07, 0.27] | 60.0 | 0.17 |
| octo-base | PutCarrotOnPlateInScene-v1 | stiff_x2.0 | 48 | 8 | 0.167 | [0.09, 0.30] | 60.0 | 0.18 |
| octo-base | PutSpoonOnTableClothInScene-v1 | damp_x0.5 | 24 | 2 | 0.083 | [0.02, 0.26] | 60.0 | 0.22 |
| octo-base | PutSpoonOnTableClothInScene-v1 | damp_x2.0 | 7 | 1 | 0.143 | [0.03, 0.51] | 60.0 | 0.18 |
| octo-base | PutSpoonOnTableClothInScene-v1 | nominal | 24 | 2 | 0.083 | [0.02, 0.26] | 60.0 | 0.22 |
| octo-base | PutSpoonOnTableClothInScene-v1 | stiff_x0.5 | 24 | 3 | 0.125 | [0.04, 0.31] | 60.0 | 0.23 |
| octo-base | PutSpoonOnTableClothInScene-v1 | stiff_x2.0 | 24 | 1 | 0.042 | [0.01, 0.20] | 60.0 | 0.23 |
| octo-small | PutCarrotOnPlateInScene-v1 | damp_x0.5 | 48 | 4 | 0.083 | [0.03, 0.20] | 60.0 | 0.17 |
| octo-small | PutCarrotOnPlateInScene-v1 | damp_x2.0 | 48 | 4 | 0.083 | [0.03, 0.20] | 60.0 | 0.21 |
| octo-small | PutCarrotOnPlateInScene-v1 | delay_1 | 48 | 5 | 0.104 | [0.05, 0.22] | 60.0 | 0.21 |
| octo-small | PutCarrotOnPlateInScene-v1 | force_x0.5 | 48 | 6 | 0.125 | [0.06, 0.25] | 60.0 | 0.21 |
| octo-small | PutCarrotOnPlateInScene-v1 | nominal | 48 | 6 | 0.125 | [0.06, 0.25] | 60.0 | 0.15 |
| octo-small | PutCarrotOnPlateInScene-v1 | stiff_x0.5 | 48 | 4 | 0.083 | [0.03, 0.20] | 60.0 | 0.16 |
| octo-small | PutCarrotOnPlateInScene-v1 | stiff_x2.0 | 48 | 6 | 0.125 | [0.06, 0.25] | 60.0 | 0.17 |
| octo-small | PutSpoonOnTableClothInScene-v1 | damp_x0.5 | 24 | 6 | 0.250 | [0.12, 0.45] | 60.0 | 0.21 |
| octo-small | PutSpoonOnTableClothInScene-v1 | damp_x2.0 | 24 | 5 | 0.208 | [0.09, 0.40] | 60.0 | 0.20 |
| octo-small | PutSpoonOnTableClothInScene-v1 | force_x0.5 | 11 | 3 | 0.273 | [0.10, 0.57] | 60.0 | 0.18 |
| octo-small | PutSpoonOnTableClothInScene-v1 | nominal | 24 | 9 | 0.375 | [0.21, 0.57] | 60.0 | 0.18 |
| octo-small | PutSpoonOnTableClothInScene-v1 | stiff_x0.5 | 24 | 5 | 0.208 | [0.09, 0.40] | 60.0 | 0.19 |
| octo-small | PutSpoonOnTableClothInScene-v1 | stiff_x2.0 | 24 | 8 | 0.333 | [0.18, 0.53] | 60.0 | 0.21 |

## Pairwise differences Δ = rate(policy_i) − rate(policy_j), paired by episode

### PutCarrotOnPlateInScene-v1: octo-base vs octo-small

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| damp_x0.5 | 48 | +0.042 | [-0.06, +0.15] | 0 |
| damp_x2.0 | 48 | +0.083 | [-0.06, +0.23] | 0 |
| delay_1 | 48 | -0.021 | [-0.12, +0.08] | 0 |
| force_x0.5 | 48 | +0.000 | [-0.12, +0.12] | 0 |
| nominal | 48 | +0.021 | [-0.10, +0.15] | 0 |
| stiff_x0.5 | 48 | +0.062 | [-0.06, +0.19] | 0 |
| stiff_x2.0 | 48 | +0.042 | [-0.06, +0.15] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-base vs octo-small

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| damp_x0.5 | 24 | -0.167 | [-0.33, +0.00] | 0 |
| damp_x2.0 | 7 | -0.143 | [-0.57, +0.29] | 0 |
| nominal | 24 | -0.292 | [-0.46, -0.12] | − |
| stiff_x0.5 | 24 | -0.083 | [-0.29, +0.12] | 0 |
| stiff_x2.0 | 24 | -0.292 | [-0.50, -0.12] | − |

## Point-estimate sign changes across conditions

- **PutCarrotOnPlateInScene-v1** octo-base vs octo-small: Δ by condition {'damp_x0.5': 0.042, 'damp_x2.0': 0.083, 'delay_1': -0.021, 'force_x0.5': 0.0, 'nominal': 0.021, 'stiff_x0.5': 0.062, 'stiff_x2.0': 0.042}

A point-estimate sign change is *not* a confirmed ranking flip: check the bootstrap intervals above; with 24 paired episodes most differences will be inconclusive.

## Within-policy sensitivity vs nominal (paired)

| policy | env | condition | paired n | rate − nominal | bootstrap 95% |
|---|---|---|---:|---:|---|
| octo-base | PutCarrotOnPlateInScene-v1 | damp_x0.5 | 48 | -0.021 | [-0.10, +0.06] |
| octo-base | PutCarrotOnPlateInScene-v1 | damp_x2.0 | 48 | +0.021 | [-0.10, +0.15] |
| octo-base | PutCarrotOnPlateInScene-v1 | delay_1 | 48 | -0.062 | [-0.17, +0.04] |
| octo-base | PutCarrotOnPlateInScene-v1 | force_x0.5 | 48 | -0.021 | [-0.06, +0.00] |
| octo-base | PutCarrotOnPlateInScene-v1 | stiff_x0.5 | 48 | +0.000 | [-0.10, +0.12] |
| octo-base | PutCarrotOnPlateInScene-v1 | stiff_x2.0 | 48 | +0.021 | [-0.04, +0.08] |
| octo-base | PutSpoonOnTableClothInScene-v1 | damp_x0.5 | 24 | +0.000 | [-0.12, +0.12] |
| octo-base | PutSpoonOnTableClothInScene-v1 | damp_x2.0 | 7 | -0.143 | [-0.57, +0.29] |
| octo-base | PutSpoonOnTableClothInScene-v1 | stiff_x0.5 | 24 | +0.042 | [-0.12, +0.21] |
| octo-base | PutSpoonOnTableClothInScene-v1 | stiff_x2.0 | 24 | -0.042 | [-0.17, +0.08] |
| octo-small | PutCarrotOnPlateInScene-v1 | damp_x0.5 | 48 | -0.042 | [-0.15, +0.06] |
| octo-small | PutCarrotOnPlateInScene-v1 | damp_x2.0 | 48 | -0.042 | [-0.17, +0.06] |
| octo-small | PutCarrotOnPlateInScene-v1 | delay_1 | 48 | -0.021 | [-0.10, +0.06] |
| octo-small | PutCarrotOnPlateInScene-v1 | force_x0.5 | 48 | +0.000 | [+0.00, +0.00] |
| octo-small | PutCarrotOnPlateInScene-v1 | stiff_x0.5 | 48 | -0.042 | [-0.17, +0.08] |
| octo-small | PutCarrotOnPlateInScene-v1 | stiff_x2.0 | 48 | +0.000 | [-0.10, +0.10] |
| octo-small | PutSpoonOnTableClothInScene-v1 | damp_x0.5 | 24 | -0.125 | [-0.33, +0.08] |
| octo-small | PutSpoonOnTableClothInScene-v1 | damp_x2.0 | 24 | -0.167 | [-0.38, +0.04] |
| octo-small | PutSpoonOnTableClothInScene-v1 | force_x0.5 | 11 | -0.182 | [-0.45, +0.00] |
| octo-small | PutSpoonOnTableClothInScene-v1 | stiff_x0.5 | 24 | -0.167 | [-0.38, +0.00] |
| octo-small | PutSpoonOnTableClothInScene-v1 | stiff_x2.0 | 24 | -0.042 | [-0.29, +0.21] |
