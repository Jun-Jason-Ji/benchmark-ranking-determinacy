# Controller sweep: descriptive analysis

Exploratory ManiSkill3/Windows platform (torch-Jacobian IK adapter), not original SIMPLER. Paired by episode_id; Wilson 95% for rates; paired bootstrap 95% for differences.

## Success rates

| policy | env | condition | n | success | rate | Wilson 95% | mean steps | mean inference s/step |
|---|---|---|---:|---:|---:|---|---:|---:|
| octo-base | PutCarrotOnPlateInScene-v1 | damp_x0.5 | 48 | 6 | 0.125 | [0.06, 0.25] | 60.0 | 0.22 |
| octo-base | PutCarrotOnPlateInScene-v1 | damp_x2.0 | 48 | 8 | 0.167 | [0.09, 0.30] | 60.0 | 0.23 |
| octo-base | PutCarrotOnPlateInScene-v1 | delay_1 | 48 | 4 | 0.083 | [0.03, 0.20] | 60.0 | 0.20 |
| octo-base | PutCarrotOnPlateInScene-v1 | force_x0.5 | 48 | 6 | 0.125 | [0.06, 0.25] | 60.0 | 0.23 |
| octo-base | PutCarrotOnPlateInScene-v1 | iso_x0.25 | 96 | 10 | 0.104 | [0.06, 0.18] | 60.0 | 0.22 |
| octo-base | PutCarrotOnPlateInScene-v1 | iso_x0.5 | 96 | 12 | 0.125 | [0.07, 0.21] | 60.0 | 0.21 |
| octo-base | PutCarrotOnPlateInScene-v1 | iso_x2.0 | 48 | 10 | 0.208 | [0.12, 0.34] | 60.0 | 0.22 |
| octo-base | PutCarrotOnPlateInScene-v1 | iso_x4.0 | 96 | 13 | 0.135 | [0.08, 0.22] | 60.0 | 0.21 |
| octo-base | PutCarrotOnPlateInScene-v1 | nominal | 48 | 7 | 0.146 | [0.07, 0.27] | 60.0 | 0.17 |
| octo-base | PutCarrotOnPlateInScene-v1 | stiff_x0.25 | 15 | 0 | 0.000 | [-0.00, 0.20] | 60.0 | 0.18 |
| octo-base | PutCarrotOnPlateInScene-v1 | stiff_x0.5 | 48 | 7 | 0.146 | [0.07, 0.27] | 60.0 | 0.17 |
| octo-base | PutCarrotOnPlateInScene-v1 | stiff_x2.0 | 48 | 8 | 0.167 | [0.09, 0.30] | 60.0 | 0.18 |
| octo-base | PutEggplantInBasketScene-v1 | damp_x0.5 | 48 | 18 | 0.375 | [0.25, 0.52] | 120.0 | 0.22 |
| octo-base | PutEggplantInBasketScene-v1 | damp_x2.0 | 48 | 14 | 0.292 | [0.18, 0.43] | 120.0 | 0.22 |
| octo-base | PutEggplantInBasketScene-v1 | delay_1 | 48 | 9 | 0.188 | [0.10, 0.32] | 120.0 | 0.16 |
| octo-base | PutEggplantInBasketScene-v1 | force_x0.5 | 48 | 15 | 0.312 | [0.20, 0.45] | 120.0 | 0.20 |
| octo-base | PutEggplantInBasketScene-v1 | iso_x0.25 | 48 | 17 | 0.354 | [0.23, 0.50] | 120.0 | 0.21 |
| octo-base | PutEggplantInBasketScene-v1 | iso_x0.5 | 48 | 16 | 0.333 | [0.22, 0.47] | 120.0 | 0.21 |
| octo-base | PutEggplantInBasketScene-v1 | iso_x2.0 | 48 | 18 | 0.375 | [0.25, 0.52] | 120.0 | 0.20 |
| octo-base | PutEggplantInBasketScene-v1 | iso_x4.0 | 48 | 17 | 0.354 | [0.23, 0.50] | 120.0 | 0.17 |
| octo-base | PutEggplantInBasketScene-v1 | nominal | 48 | 14 | 0.292 | [0.18, 0.43] | 120.0 | 0.20 |
| octo-base | PutEggplantInBasketScene-v1 | stiff_x0.5 | 48 | 12 | 0.250 | [0.15, 0.39] | 120.0 | 0.21 |
| octo-base | PutEggplantInBasketScene-v1 | stiff_x2.0 | 48 | 18 | 0.375 | [0.25, 0.52] | 120.0 | 0.22 |
| octo-base | PutSpoonOnTableClothInScene-v1 | damp_x0.5 | 48 | 3 | 0.062 | [0.02, 0.17] | 60.0 | 0.20 |
| octo-base | PutSpoonOnTableClothInScene-v1 | damp_x2.0 | 48 | 4 | 0.083 | [0.03, 0.20] | 60.0 | 0.17 |
| octo-base | PutSpoonOnTableClothInScene-v1 | delay_1 | 48 | 8 | 0.167 | [0.09, 0.30] | 60.0 | 0.16 |
| octo-base | PutSpoonOnTableClothInScene-v1 | force_x0.5 | 48 | 5 | 0.104 | [0.05, 0.22] | 60.0 | 0.16 |
| octo-base | PutSpoonOnTableClothInScene-v1 | iso_x0.25 | 48 | 1 | 0.021 | [0.00, 0.11] | 60.0 | 0.23 |
| octo-base | PutSpoonOnTableClothInScene-v1 | iso_x0.5 | 48 | 1 | 0.021 | [0.00, 0.11] | 60.0 | 0.23 |
| octo-base | PutSpoonOnTableClothInScene-v1 | iso_x2.0 | 48 | 5 | 0.104 | [0.05, 0.22] | 60.0 | 0.23 |
| octo-base | PutSpoonOnTableClothInScene-v1 | iso_x4.0 | 48 | 3 | 0.062 | [0.02, 0.17] | 60.0 | 0.22 |
| octo-base | PutSpoonOnTableClothInScene-v1 | nominal | 48 | 4 | 0.083 | [0.03, 0.20] | 60.0 | 0.20 |
| octo-base | PutSpoonOnTableClothInScene-v1 | stiff_x0.25 | 14 | 0 | 0.000 | [0.00, 0.22] | 60.0 | 0.21 |
| octo-base | PutSpoonOnTableClothInScene-v1 | stiff_x0.5 | 48 | 4 | 0.083 | [0.03, 0.20] | 60.0 | 0.21 |
| octo-base | PutSpoonOnTableClothInScene-v1 | stiff_x2.0 | 48 | 4 | 0.083 | [0.03, 0.20] | 60.0 | 0.21 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x0.5 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.18 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x2.0 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.17 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | delay_1 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.15 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | force_x0.5 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.16 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x0.25 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.13 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x0.5 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.13 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x2.0 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.12 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x4.0 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.08 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | nominal | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.19 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x0.5 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.19 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x2.0 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.19 |
| octo-small | PutCarrotOnPlateInScene-v1 | damp_x0.5 | 48 | 4 | 0.083 | [0.03, 0.20] | 60.0 | 0.17 |
| octo-small | PutCarrotOnPlateInScene-v1 | damp_x2.0 | 48 | 4 | 0.083 | [0.03, 0.20] | 60.0 | 0.21 |
| octo-small | PutCarrotOnPlateInScene-v1 | delay_1 | 48 | 5 | 0.104 | [0.05, 0.22] | 60.0 | 0.21 |
| octo-small | PutCarrotOnPlateInScene-v1 | force_x0.5 | 48 | 6 | 0.125 | [0.06, 0.25] | 60.0 | 0.21 |
| octo-small | PutCarrotOnPlateInScene-v1 | iso_x0.25 | 96 | 8 | 0.083 | [0.04, 0.16] | 60.0 | 0.19 |
| octo-small | PutCarrotOnPlateInScene-v1 | iso_x0.5 | 96 | 6 | 0.062 | [0.03, 0.13] | 60.0 | 0.16 |
| octo-small | PutCarrotOnPlateInScene-v1 | iso_x2.0 | 48 | 7 | 0.146 | [0.07, 0.27] | 60.0 | 0.19 |
| octo-small | PutCarrotOnPlateInScene-v1 | iso_x4.0 | 96 | 13 | 0.135 | [0.08, 0.22] | 60.0 | 0.13 |
| octo-small | PutCarrotOnPlateInScene-v1 | nominal | 48 | 6 | 0.125 | [0.06, 0.25] | 60.0 | 0.15 |
| octo-small | PutCarrotOnPlateInScene-v1 | stiff_x0.25 | 18 | 0 | 0.000 | [0.00, 0.18] | 60.0 | 0.15 |
| octo-small | PutCarrotOnPlateInScene-v1 | stiff_x0.5 | 48 | 4 | 0.083 | [0.03, 0.20] | 60.0 | 0.16 |
| octo-small | PutCarrotOnPlateInScene-v1 | stiff_x2.0 | 48 | 6 | 0.125 | [0.06, 0.25] | 60.0 | 0.17 |
| octo-small | PutEggplantInBasketScene-v1 | damp_x0.5 | 48 | 22 | 0.458 | [0.33, 0.60] | 120.0 | 0.19 |
| octo-small | PutEggplantInBasketScene-v1 | damp_x2.0 | 48 | 26 | 0.542 | [0.40, 0.67] | 120.0 | 0.19 |
| octo-small | PutEggplantInBasketScene-v1 | delay_1 | 48 | 24 | 0.500 | [0.36, 0.64] | 120.0 | 0.16 |
| octo-small | PutEggplantInBasketScene-v1 | force_x0.5 | 48 | 22 | 0.458 | [0.33, 0.60] | 120.0 | 0.19 |
| octo-small | PutEggplantInBasketScene-v1 | iso_x0.25 | 48 | 20 | 0.417 | [0.29, 0.56] | 120.0 | 0.19 |
| octo-small | PutEggplantInBasketScene-v1 | iso_x0.5 | 48 | 26 | 0.542 | [0.40, 0.67] | 120.0 | 0.18 |
| octo-small | PutEggplantInBasketScene-v1 | iso_x2.0 | 48 | 24 | 0.500 | [0.36, 0.64] | 120.0 | 0.18 |
| octo-small | PutEggplantInBasketScene-v1 | iso_x4.0 | 48 | 27 | 0.562 | [0.42, 0.69] | 120.0 | 0.18 |
| octo-small | PutEggplantInBasketScene-v1 | nominal | 48 | 25 | 0.521 | [0.38, 0.66] | 120.0 | 0.17 |
| octo-small | PutEggplantInBasketScene-v1 | stiff_x0.5 | 48 | 29 | 0.604 | [0.46, 0.73] | 120.0 | 0.19 |
| octo-small | PutEggplantInBasketScene-v1 | stiff_x2.0 | 48 | 24 | 0.500 | [0.36, 0.64] | 120.0 | 0.19 |
| octo-small | PutSpoonOnTableClothInScene-v1 | damp_x0.5 | 48 | 10 | 0.208 | [0.12, 0.34] | 60.0 | 0.18 |
| octo-small | PutSpoonOnTableClothInScene-v1 | damp_x2.0 | 48 | 14 | 0.292 | [0.18, 0.43] | 60.0 | 0.18 |
| octo-small | PutSpoonOnTableClothInScene-v1 | delay_1 | 48 | 8 | 0.167 | [0.09, 0.30] | 60.0 | 0.15 |
| octo-small | PutSpoonOnTableClothInScene-v1 | force_x0.5 | 48 | 16 | 0.333 | [0.22, 0.47] | 60.0 | 0.16 |
| octo-small | PutSpoonOnTableClothInScene-v1 | iso_x0.25 | 48 | 12 | 0.250 | [0.15, 0.39] | 60.0 | 0.21 |
| octo-small | PutSpoonOnTableClothInScene-v1 | iso_x0.5 | 48 | 17 | 0.354 | [0.23, 0.50] | 60.0 | 0.21 |
| octo-small | PutSpoonOnTableClothInScene-v1 | iso_x2.0 | 48 | 12 | 0.250 | [0.15, 0.39] | 60.0 | 0.21 |
| octo-small | PutSpoonOnTableClothInScene-v1 | iso_x4.0 | 48 | 18 | 0.375 | [0.25, 0.52] | 60.0 | 0.21 |
| octo-small | PutSpoonOnTableClothInScene-v1 | nominal | 48 | 18 | 0.375 | [0.25, 0.52] | 60.0 | 0.17 |
| octo-small | PutSpoonOnTableClothInScene-v1 | stiff_x0.25 | 15 | 4 | 0.267 | [0.11, 0.52] | 60.0 | 0.19 |
| octo-small | PutSpoonOnTableClothInScene-v1 | stiff_x0.5 | 48 | 16 | 0.333 | [0.22, 0.47] | 60.0 | 0.18 |
| octo-small | PutSpoonOnTableClothInScene-v1 | stiff_x2.0 | 48 | 14 | 0.292 | [0.18, 0.43] | 60.0 | 0.18 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x0.5 | 48 | 2 | 0.042 | [0.01, 0.14] | 60.0 | 0.16 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x2.0 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.16 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | delay_1 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.16 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | force_x0.5 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.16 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x0.25 | 48 | 1 | 0.021 | [0.00, 0.11] | 60.0 | 0.19 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x0.5 | 48 | 1 | 0.021 | [0.00, 0.11] | 60.0 | 0.18 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x2.0 | 48 | 1 | 0.021 | [0.00, 0.11] | 60.0 | 0.18 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x4.0 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.18 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | nominal | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.16 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x0.5 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.16 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x2.0 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.16 |

## Pairwise differences Δ = rate(policy_i) − rate(policy_j), paired by episode

### PutCarrotOnPlateInScene-v1: octo-base vs octo-small

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| damp_x0.5 | 48 | +0.042 | [-0.06, +0.15] | 0 |
| damp_x2.0 | 48 | +0.083 | [-0.06, +0.23] | 0 |
| delay_1 | 48 | -0.021 | [-0.12, +0.08] | 0 |
| force_x0.5 | 48 | +0.000 | [-0.12, +0.12] | 0 |
| iso_x0.25 | 96 | +0.021 | [-0.04, +0.08] | 0 |
| iso_x0.5 | 96 | +0.062 | [+0.00, +0.14] | 0 |
| iso_x2.0 | 48 | +0.062 | [-0.04, +0.17] | 0 |
| iso_x4.0 | 96 | +0.000 | [-0.08, +0.08] | 0 |
| nominal | 48 | +0.021 | [-0.10, +0.15] | 0 |
| stiff_x0.25 | 15 | +0.000 | [+0.00, +0.00] | 0 |
| stiff_x0.5 | 48 | +0.062 | [-0.06, +0.19] | 0 |
| stiff_x2.0 | 48 | +0.042 | [-0.06, +0.15] | 0 |

### PutEggplantInBasketScene-v1: octo-base vs octo-small

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| damp_x0.5 | 48 | -0.083 | [-0.27, +0.10] | 0 |
| damp_x2.0 | 48 | -0.250 | [-0.44, -0.06] | − |
| delay_1 | 48 | -0.312 | [-0.50, -0.12] | − |
| force_x0.5 | 48 | -0.146 | [-0.31, +0.02] | 0 |
| iso_x0.25 | 48 | -0.062 | [-0.23, +0.10] | 0 |
| iso_x0.5 | 48 | -0.208 | [-0.38, -0.04] | − |
| iso_x2.0 | 48 | -0.125 | [-0.27, +0.02] | 0 |
| iso_x4.0 | 48 | -0.208 | [-0.40, -0.02] | − |
| nominal | 48 | -0.229 | [-0.40, -0.06] | − |
| stiff_x0.5 | 48 | -0.354 | [-0.52, -0.17] | − |
| stiff_x2.0 | 48 | -0.125 | [-0.27, +0.02] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-base vs octo-small

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| damp_x0.5 | 48 | -0.146 | [-0.27, -0.04] | − |
| damp_x2.0 | 48 | -0.208 | [-0.35, -0.06] | − |
| delay_1 | 48 | +0.000 | [-0.12, +0.12] | 0 |
| force_x0.5 | 48 | -0.229 | [-0.35, -0.10] | − |
| iso_x0.25 | 48 | -0.229 | [-0.35, -0.10] | − |
| iso_x0.5 | 48 | -0.333 | [-0.48, -0.19] | − |
| iso_x2.0 | 48 | -0.146 | [-0.29, +0.00] | 0 |
| iso_x4.0 | 48 | -0.312 | [-0.46, -0.17] | − |
| nominal | 48 | -0.292 | [-0.44, -0.15] | − |
| stiff_x0.25 | 14 | -0.214 | [-0.43, +0.00] | 0 |
| stiff_x0.5 | 48 | -0.250 | [-0.40, -0.10] | − |
| stiff_x2.0 | 48 | -0.208 | [-0.35, -0.06] | − |

### StackGreenCubeOnYellowCubeBakedTexInScene-v1: octo-base vs octo-small

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| damp_x0.5 | 48 | -0.042 | [-0.10, +0.00] | 0 |
| damp_x2.0 | 48 | +0.000 | [+0.00, +0.00] | 0 |
| delay_1 | 48 | +0.000 | [+0.00, +0.00] | 0 |
| force_x0.5 | 48 | +0.000 | [+0.00, +0.00] | 0 |
| iso_x0.25 | 48 | -0.021 | [-0.06, +0.00] | 0 |
| iso_x0.5 | 48 | -0.021 | [-0.06, +0.00] | 0 |
| iso_x2.0 | 48 | -0.021 | [-0.06, +0.00] | 0 |
| iso_x4.0 | 48 | +0.000 | [+0.00, +0.00] | 0 |
| nominal | 48 | +0.000 | [+0.00, +0.00] | 0 |
| stiff_x0.5 | 48 | +0.000 | [+0.00, +0.00] | 0 |
| stiff_x2.0 | 48 | +0.000 | [+0.00, +0.00] | 0 |

## Point-estimate sign changes across conditions

- **PutCarrotOnPlateInScene-v1** octo-base vs octo-small: Δ by condition {'damp_x0.5': 0.042, 'damp_x2.0': 0.083, 'delay_1': -0.021, 'force_x0.5': 0.0, 'iso_x0.25': 0.021, 'iso_x0.5': 0.062, 'iso_x2.0': 0.062, 'iso_x4.0': 0.0, 'nominal': 0.021, 'stiff_x0.25': 0.0, 'stiff_x0.5': 0.062, 'stiff_x2.0': 0.042}

A point-estimate sign change is *not* a confirmed ranking flip: check the bootstrap intervals above; with 24 paired episodes most differences will be inconclusive.

## Within-policy sensitivity vs nominal (paired)

| policy | env | condition | paired n | rate − nominal | bootstrap 95% |
|---|---|---|---:|---:|---|
| octo-base | PutCarrotOnPlateInScene-v1 | damp_x0.5 | 48 | -0.021 | [-0.10, +0.06] |
| octo-base | PutCarrotOnPlateInScene-v1 | damp_x2.0 | 48 | +0.021 | [-0.10, +0.15] |
| octo-base | PutCarrotOnPlateInScene-v1 | delay_1 | 48 | -0.062 | [-0.17, +0.04] |
| octo-base | PutCarrotOnPlateInScene-v1 | force_x0.5 | 48 | -0.021 | [-0.06, +0.00] |
| octo-base | PutCarrotOnPlateInScene-v1 | iso_x0.25 | 48 | +0.000 | [-0.10, +0.10] |
| octo-base | PutCarrotOnPlateInScene-v1 | iso_x0.5 | 48 | +0.042 | [-0.06, +0.15] |
| octo-base | PutCarrotOnPlateInScene-v1 | iso_x2.0 | 48 | +0.062 | [+0.00, +0.15] |
| octo-base | PutCarrotOnPlateInScene-v1 | iso_x4.0 | 48 | -0.021 | [-0.12, +0.06] |
| octo-base | PutCarrotOnPlateInScene-v1 | stiff_x0.25 | 15 | -0.067 | [-0.20, +0.00] |
| octo-base | PutCarrotOnPlateInScene-v1 | stiff_x0.5 | 48 | +0.000 | [-0.10, +0.12] |
| octo-base | PutCarrotOnPlateInScene-v1 | stiff_x2.0 | 48 | +0.021 | [-0.04, +0.08] |
| octo-base | PutEggplantInBasketScene-v1 | damp_x0.5 | 48 | +0.083 | [-0.04, +0.23] |
| octo-base | PutEggplantInBasketScene-v1 | damp_x2.0 | 48 | +0.000 | [-0.15, +0.15] |
| octo-base | PutEggplantInBasketScene-v1 | delay_1 | 48 | -0.104 | [-0.25, +0.04] |
| octo-base | PutEggplantInBasketScene-v1 | force_x0.5 | 48 | +0.021 | [-0.10, +0.15] |
| octo-base | PutEggplantInBasketScene-v1 | iso_x0.25 | 48 | +0.062 | [-0.08, +0.23] |
| octo-base | PutEggplantInBasketScene-v1 | iso_x0.5 | 48 | +0.042 | [-0.08, +0.17] |
| octo-base | PutEggplantInBasketScene-v1 | iso_x2.0 | 48 | +0.083 | [+0.00, +0.19] |
| octo-base | PutEggplantInBasketScene-v1 | iso_x4.0 | 48 | +0.062 | [-0.06, +0.19] |
| octo-base | PutEggplantInBasketScene-v1 | stiff_x0.5 | 48 | -0.042 | [-0.19, +0.10] |
| octo-base | PutEggplantInBasketScene-v1 | stiff_x2.0 | 48 | +0.083 | [-0.04, +0.21] |
| octo-base | PutSpoonOnTableClothInScene-v1 | damp_x0.5 | 48 | -0.021 | [-0.10, +0.06] |
| octo-base | PutSpoonOnTableClothInScene-v1 | damp_x2.0 | 48 | +0.000 | [-0.10, +0.10] |
| octo-base | PutSpoonOnTableClothInScene-v1 | delay_1 | 48 | +0.083 | [-0.04, +0.21] |
| octo-base | PutSpoonOnTableClothInScene-v1 | force_x0.5 | 48 | +0.021 | [+0.00, +0.06] |
| octo-base | PutSpoonOnTableClothInScene-v1 | iso_x0.25 | 48 | -0.062 | [-0.17, +0.02] |
| octo-base | PutSpoonOnTableClothInScene-v1 | iso_x0.5 | 48 | -0.062 | [-0.17, +0.02] |
| octo-base | PutSpoonOnTableClothInScene-v1 | iso_x2.0 | 48 | +0.021 | [-0.04, +0.08] |
| octo-base | PutSpoonOnTableClothInScene-v1 | iso_x4.0 | 48 | -0.021 | [-0.12, +0.08] |
| octo-base | PutSpoonOnTableClothInScene-v1 | stiff_x0.25 | 14 | -0.143 | [-0.36, +0.00] |
| octo-base | PutSpoonOnTableClothInScene-v1 | stiff_x0.5 | 48 | +0.000 | [-0.10, +0.12] |
| octo-base | PutSpoonOnTableClothInScene-v1 | stiff_x2.0 | 48 | +0.000 | [-0.12, +0.10] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x0.5 | 48 | +0.000 | [+0.00, +0.00] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x2.0 | 48 | +0.000 | [+0.00, +0.00] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | delay_1 | 48 | +0.000 | [+0.00, +0.00] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | force_x0.5 | 48 | +0.000 | [+0.00, +0.00] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x0.25 | 48 | +0.000 | [+0.00, +0.00] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x0.5 | 48 | +0.000 | [+0.00, +0.00] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x2.0 | 48 | +0.000 | [+0.00, +0.00] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x4.0 | 48 | +0.000 | [+0.00, +0.00] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x0.5 | 48 | +0.000 | [+0.00, +0.00] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x2.0 | 48 | +0.000 | [+0.00, +0.00] |
| octo-small | PutCarrotOnPlateInScene-v1 | damp_x0.5 | 48 | -0.042 | [-0.15, +0.06] |
| octo-small | PutCarrotOnPlateInScene-v1 | damp_x2.0 | 48 | -0.042 | [-0.17, +0.06] |
| octo-small | PutCarrotOnPlateInScene-v1 | delay_1 | 48 | -0.021 | [-0.10, +0.06] |
| octo-small | PutCarrotOnPlateInScene-v1 | force_x0.5 | 48 | +0.000 | [+0.00, +0.00] |
| octo-small | PutCarrotOnPlateInScene-v1 | iso_x0.25 | 48 | -0.042 | [-0.12, +0.04] |
| octo-small | PutCarrotOnPlateInScene-v1 | iso_x0.5 | 48 | -0.062 | [-0.15, +0.02] |
| octo-small | PutCarrotOnPlateInScene-v1 | iso_x2.0 | 48 | +0.021 | [-0.06, +0.10] |
| octo-small | PutCarrotOnPlateInScene-v1 | iso_x4.0 | 48 | +0.062 | [-0.02, +0.17] |
| octo-small | PutCarrotOnPlateInScene-v1 | stiff_x0.25 | 18 | -0.056 | [-0.17, +0.00] |
| octo-small | PutCarrotOnPlateInScene-v1 | stiff_x0.5 | 48 | -0.042 | [-0.17, +0.08] |
| octo-small | PutCarrotOnPlateInScene-v1 | stiff_x2.0 | 48 | +0.000 | [-0.10, +0.10] |
| octo-small | PutEggplantInBasketScene-v1 | damp_x0.5 | 48 | -0.062 | [-0.17, +0.02] |
| octo-small | PutEggplantInBasketScene-v1 | damp_x2.0 | 48 | +0.021 | [-0.12, +0.17] |
| octo-small | PutEggplantInBasketScene-v1 | delay_1 | 48 | -0.021 | [-0.19, +0.15] |
| octo-small | PutEggplantInBasketScene-v1 | force_x0.5 | 48 | -0.062 | [-0.17, +0.04] |
| octo-small | PutEggplantInBasketScene-v1 | iso_x0.25 | 48 | -0.104 | [-0.25, +0.04] |
| octo-small | PutEggplantInBasketScene-v1 | iso_x0.5 | 48 | +0.021 | [-0.08, +0.12] |
| octo-small | PutEggplantInBasketScene-v1 | iso_x2.0 | 48 | -0.021 | [-0.15, +0.10] |
| octo-small | PutEggplantInBasketScene-v1 | iso_x4.0 | 48 | +0.042 | [-0.10, +0.19] |
| octo-small | PutEggplantInBasketScene-v1 | stiff_x0.5 | 48 | +0.083 | [-0.08, +0.25] |
| octo-small | PutEggplantInBasketScene-v1 | stiff_x2.0 | 48 | -0.021 | [-0.15, +0.10] |
| octo-small | PutSpoonOnTableClothInScene-v1 | damp_x0.5 | 48 | -0.167 | [-0.31, -0.02] |
| octo-small | PutSpoonOnTableClothInScene-v1 | damp_x2.0 | 48 | -0.083 | [-0.25, +0.08] |
| octo-small | PutSpoonOnTableClothInScene-v1 | delay_1 | 48 | -0.208 | [-0.35, -0.06] |
| octo-small | PutSpoonOnTableClothInScene-v1 | force_x0.5 | 48 | -0.042 | [-0.12, +0.04] |
| octo-small | PutSpoonOnTableClothInScene-v1 | iso_x0.25 | 48 | -0.125 | [-0.25, +0.00] |
| octo-small | PutSpoonOnTableClothInScene-v1 | iso_x0.5 | 48 | -0.021 | [-0.15, +0.10] |
| octo-small | PutSpoonOnTableClothInScene-v1 | iso_x2.0 | 48 | -0.125 | [-0.27, +0.00] |
| octo-small | PutSpoonOnTableClothInScene-v1 | iso_x4.0 | 48 | +0.000 | [-0.12, +0.10] |
| octo-small | PutSpoonOnTableClothInScene-v1 | stiff_x0.25 | 15 | -0.133 | [-0.47, +0.20] |
| octo-small | PutSpoonOnTableClothInScene-v1 | stiff_x0.5 | 48 | -0.042 | [-0.21, +0.12] |
| octo-small | PutSpoonOnTableClothInScene-v1 | stiff_x2.0 | 48 | -0.083 | [-0.27, +0.10] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x0.5 | 48 | +0.042 | [+0.00, +0.10] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x2.0 | 48 | +0.000 | [+0.00, +0.00] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | delay_1 | 48 | +0.000 | [+0.00, +0.00] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | force_x0.5 | 48 | +0.000 | [+0.00, +0.00] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x0.25 | 48 | +0.021 | [+0.00, +0.06] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x0.5 | 48 | +0.021 | [+0.00, +0.06] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x2.0 | 48 | +0.021 | [+0.00, +0.06] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x4.0 | 48 | +0.000 | [+0.00, +0.00] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x0.5 | 48 | +0.000 | [+0.00, +0.00] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x2.0 | 48 | +0.000 | [+0.00, +0.00] |
