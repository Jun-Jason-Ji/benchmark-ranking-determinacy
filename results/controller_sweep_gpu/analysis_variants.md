# Controller sweep: descriptive analysis

Exploratory ManiSkill3/Windows platform (torch-Jacobian IK adapter), not original SIMPLER. Paired by episode_id; Wilson 95% for rates; paired bootstrap 95% for differences.

## Success rates

| policy | env | condition | n | success | rate | Wilson 95% | mean steps | mean inference s/step |
|---|---|---|---:|---:|---:|---|---:|---:|
| octo-base | PutCarrotOnPlateInScene-v1 | damp_x0.25 | 24 | 3 | 0.125 | [0.04, 0.31] | 60.0 | 0.19 |
| octo-base | PutCarrotOnPlateInScene-v1 | damp_x0.5 | 48 | 6 | 0.125 | [0.06, 0.25] | 60.0 | 0.22 |
| octo-base | PutCarrotOnPlateInScene-v1 | damp_x2.0 | 48 | 8 | 0.167 | [0.09, 0.30] | 60.0 | 0.23 |
| octo-base | PutCarrotOnPlateInScene-v1 | damp_x4.0 | 24 | 4 | 0.167 | [0.07, 0.36] | 60.0 | 0.19 |
| octo-base | PutCarrotOnPlateInScene-v1 | delay_1 | 48 | 4 | 0.083 | [0.03, 0.20] | 60.0 | 0.20 |
| octo-base | PutCarrotOnPlateInScene-v1 | delay_2 | 24 | 0 | 0.000 | [0.00, 0.14] | 60.0 | 0.19 |
| octo-base | PutCarrotOnPlateInScene-v1 | dens_x0.5 | 24 | 2 | 0.083 | [0.02, 0.26] | 60.0 | 0.19 |
| octo-base | PutCarrotOnPlateInScene-v1 | dens_x2.0 | 24 | 4 | 0.167 | [0.07, 0.36] | 60.0 | 0.12 |
| octo-base | PutCarrotOnPlateInScene-v1 | force_x0.5 | 48 | 6 | 0.125 | [0.06, 0.25] | 60.0 | 0.23 |
| octo-base | PutCarrotOnPlateInScene-v1 | fric_x0.4 | 24 | 4 | 0.167 | [0.07, 0.36] | 60.0 | 0.22 |
| octo-base | PutCarrotOnPlateInScene-v1 | fric_x2.5 | 24 | 4 | 0.167 | [0.07, 0.36] | 60.0 | 0.21 |
| octo-base | PutCarrotOnPlateInScene-v1 | iso_x0.25 | 96 | 10 | 0.104 | [0.06, 0.18] | 60.0 | 0.22 |
| octo-base | PutCarrotOnPlateInScene-v1 | iso_x0.5 | 96 | 12 | 0.125 | [0.07, 0.21] | 60.0 | 0.21 |
| octo-base | PutCarrotOnPlateInScene-v1 | iso_x2.0 | 48 | 10 | 0.208 | [0.12, 0.34] | 60.0 | 0.22 |
| octo-base | PutCarrotOnPlateInScene-v1 | iso_x4.0 | 96 | 13 | 0.135 | [0.08, 0.22] | 60.0 | 0.21 |
| octo-base | PutCarrotOnPlateInScene-v1 | nominal | 48 | 7 | 0.146 | [0.07, 0.27] | 60.0 | 0.17 |
| octo-base | PutCarrotOnPlateInScene-v1 | stiff_x0.25 | 24 | 0 | 0.000 | [0.00, 0.14] | 60.0 | 0.19 |
| octo-base | PutCarrotOnPlateInScene-v1 | stiff_x0.5 | 48 | 7 | 0.146 | [0.07, 0.27] | 60.0 | 0.17 |
| octo-base | PutCarrotOnPlateInScene-v1 | stiff_x2.0 | 48 | 8 | 0.167 | [0.09, 0.30] | 60.0 | 0.18 |
| octo-base | PutCarrotOnPlateInScene-v1 | stiff_x4.0 | 24 | 3 | 0.125 | [0.04, 0.31] | 60.0 | 0.19 |
| octo-base | PutEggplantInBasketScene-v1 | damp_x0.25 | 24 | 10 | 0.417 | [0.24, 0.61] | 120.0 | 0.16 |
| octo-base | PutEggplantInBasketScene-v1 | damp_x0.5 | 48 | 18 | 0.375 | [0.25, 0.52] | 120.0 | 0.22 |
| octo-base | PutEggplantInBasketScene-v1 | damp_x2.0 | 48 | 14 | 0.292 | [0.18, 0.43] | 120.0 | 0.22 |
| octo-base | PutEggplantInBasketScene-v1 | damp_x4.0 | 24 | 3 | 0.125 | [0.04, 0.31] | 120.0 | 0.10 |
| octo-base | PutEggplantInBasketScene-v1 | delay_1 | 48 | 9 | 0.188 | [0.10, 0.32] | 120.0 | 0.16 |
| octo-base | PutEggplantInBasketScene-v1 | delay_2 | 24 | 0 | 0.000 | [0.00, 0.14] | 120.0 | 0.07 |
| octo-base | PutEggplantInBasketScene-v1 | dens_x0.5 | 96 | 38 | 0.396 | [0.30, 0.50] | 120.0 | 0.15 |
| octo-base | PutEggplantInBasketScene-v1 | dens_x2.0 | 24 | 6 | 0.250 | [0.12, 0.45] | 120.0 | 0.16 |
| octo-base | PutEggplantInBasketScene-v1 | force_x0.5 | 48 | 15 | 0.312 | [0.20, 0.45] | 120.0 | 0.20 |
| octo-base | PutEggplantInBasketScene-v1 | fric_x0.4 | 96 | 42 | 0.438 | [0.34, 0.54] | 120.0 | 0.18 |
| octo-base | PutEggplantInBasketScene-v1 | fric_x2.5 | 24 | 6 | 0.250 | [0.12, 0.45] | 120.0 | 0.19 |
| octo-base | PutEggplantInBasketScene-v1 | iso_x0.25 | 48 | 17 | 0.354 | [0.23, 0.50] | 120.0 | 0.21 |
| octo-base | PutEggplantInBasketScene-v1 | iso_x0.5 | 48 | 16 | 0.333 | [0.22, 0.47] | 120.0 | 0.21 |
| octo-base | PutEggplantInBasketScene-v1 | iso_x2.0 | 48 | 18 | 0.375 | [0.25, 0.52] | 120.0 | 0.20 |
| octo-base | PutEggplantInBasketScene-v1 | iso_x4.0 | 48 | 17 | 0.354 | [0.23, 0.50] | 120.0 | 0.17 |
| octo-base | PutEggplantInBasketScene-v1 | nominal | 96 | 36 | 0.375 | [0.28, 0.47] | 120.0 | 0.21 |
| octo-base | PutEggplantInBasketScene-v1 | stiff_x0.25 | 24 | 2 | 0.083 | [0.02, 0.26] | 120.0 | 0.19 |
| octo-base | PutEggplantInBasketScene-v1 | stiff_x0.5 | 48 | 12 | 0.250 | [0.15, 0.39] | 120.0 | 0.21 |
| octo-base | PutEggplantInBasketScene-v1 | stiff_x2.0 | 48 | 18 | 0.375 | [0.25, 0.52] | 120.0 | 0.22 |
| octo-base | PutEggplantInBasketScene-v1 | stiff_x4.0 | 24 | 8 | 0.333 | [0.18, 0.53] | 120.0 | 0.19 |
| octo-base | PutSpoonOnTableClothInScene-v1 | damp_x0.25 | 24 | 2 | 0.083 | [0.02, 0.26] | 60.0 | 0.21 |
| octo-base | PutSpoonOnTableClothInScene-v1 | damp_x0.5 | 48 | 3 | 0.062 | [0.02, 0.17] | 60.0 | 0.20 |
| octo-base | PutSpoonOnTableClothInScene-v1 | damp_x2.0 | 48 | 4 | 0.083 | [0.03, 0.20] | 60.0 | 0.17 |
| octo-base | PutSpoonOnTableClothInScene-v1 | damp_x4.0 | 24 | 0 | 0.000 | [0.00, 0.14] | 60.0 | 0.21 |
| octo-base | PutSpoonOnTableClothInScene-v1 | delay_1 | 48 | 8 | 0.167 | [0.09, 0.30] | 60.0 | 0.16 |
| octo-base | PutSpoonOnTableClothInScene-v1 | delay_2 | 24 | 4 | 0.167 | [0.07, 0.36] | 60.0 | 0.20 |
| octo-base | PutSpoonOnTableClothInScene-v1 | dens_x0.5 | 24 | 1 | 0.042 | [0.01, 0.20] | 60.0 | 0.21 |
| octo-base | PutSpoonOnTableClothInScene-v1 | dens_x2.0 | 24 | 0 | 0.000 | [0.00, 0.14] | 60.0 | 0.21 |
| octo-base | PutSpoonOnTableClothInScene-v1 | force_x0.5 | 48 | 5 | 0.104 | [0.05, 0.22] | 60.0 | 0.16 |
| octo-base | PutSpoonOnTableClothInScene-v1 | fric_x0.4 | 24 | 2 | 0.083 | [0.02, 0.26] | 60.0 | 0.21 |
| octo-base | PutSpoonOnTableClothInScene-v1 | fric_x2.5 | 24 | 3 | 0.125 | [0.04, 0.31] | 60.0 | 0.21 |
| octo-base | PutSpoonOnTableClothInScene-v1 | iso_x0.25 | 48 | 1 | 0.021 | [0.00, 0.11] | 60.0 | 0.23 |
| octo-base | PutSpoonOnTableClothInScene-v1 | iso_x0.5 | 48 | 1 | 0.021 | [0.00, 0.11] | 60.0 | 0.23 |
| octo-base | PutSpoonOnTableClothInScene-v1 | iso_x2.0 | 48 | 5 | 0.104 | [0.05, 0.22] | 60.0 | 0.23 |
| octo-base | PutSpoonOnTableClothInScene-v1 | iso_x4.0 | 48 | 3 | 0.062 | [0.02, 0.17] | 60.0 | 0.22 |
| octo-base | PutSpoonOnTableClothInScene-v1 | nominal | 48 | 4 | 0.083 | [0.03, 0.20] | 60.0 | 0.20 |
| octo-base | PutSpoonOnTableClothInScene-v1 | stiff_x0.25 | 24 | 0 | 0.000 | [0.00, 0.14] | 60.0 | 0.21 |
| octo-base | PutSpoonOnTableClothInScene-v1 | stiff_x0.5 | 48 | 4 | 0.083 | [0.03, 0.20] | 60.0 | 0.21 |
| octo-base | PutSpoonOnTableClothInScene-v1 | stiff_x2.0 | 48 | 4 | 0.083 | [0.03, 0.20] | 60.0 | 0.21 |
| octo-base | PutSpoonOnTableClothInScene-v1 | stiff_x4.0 | 24 | 1 | 0.042 | [0.01, 0.20] | 60.0 | 0.21 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x0.25 | 24 | 0 | 0.000 | [0.00, 0.14] | 60.0 | 0.22 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x0.5 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.18 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x2.0 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.17 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x4.0 | 24 | 0 | 0.000 | [0.00, 0.14] | 60.0 | 0.22 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | delay_1 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.15 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | delay_2 | 24 | 0 | 0.000 | [0.00, 0.14] | 60.0 | 0.17 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | force_x0.5 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.16 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x0.25 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.13 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x0.5 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.13 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x2.0 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.12 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x4.0 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.08 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | nominal | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.19 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x0.25 | 24 | 0 | 0.000 | [0.00, 0.14] | 60.0 | 0.21 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x0.5 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.19 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x2.0 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.19 |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x4.0 | 24 | 0 | 0.000 | [0.00, 0.14] | 60.0 | 0.22 |
| octo-base@chunk4 | PutEggplantInBasketScene-v1 | dens_x0.5 | 24 | 5 | 0.208 | [0.09, 0.40] | 120.0 | 0.06 |
| octo-base@chunk4 | PutEggplantInBasketScene-v1 | force_x0.5 | 24 | 3 | 0.125 | [0.04, 0.31] | 120.0 | 0.05 |
| octo-base@chunk4 | PutEggplantInBasketScene-v1 | fric_x0.4 | 24 | 3 | 0.125 | [0.04, 0.31] | 120.0 | 0.04 |
| octo-base@chunk4 | PutEggplantInBasketScene-v1 | iso_x0.25 | 24 | 4 | 0.167 | [0.07, 0.36] | 120.0 | 0.05 |
| octo-base@chunk4 | PutEggplantInBasketScene-v1 | iso_x4.0 | 24 | 4 | 0.167 | [0.07, 0.36] | 120.0 | 0.05 |
| octo-base@chunk4 | PutEggplantInBasketScene-v1 | nominal | 24 | 2 | 0.083 | [0.02, 0.26] | 120.0 | 0.17 |
| octo-base@chunk4 | PutSpoonOnTableClothInScene-v1 | dens_x0.5 | 24 | 2 | 0.083 | [0.02, 0.26] | 60.0 | 0.11 |
| octo-base@chunk4 | PutSpoonOnTableClothInScene-v1 | force_x0.5 | 24 | 1 | 0.042 | [0.01, 0.20] | 60.0 | 0.20 |
| octo-base@chunk4 | PutSpoonOnTableClothInScene-v1 | fric_x0.4 | 24 | 0 | 0.000 | [0.00, 0.14] | 60.0 | 0.19 |
| octo-base@chunk4 | PutSpoonOnTableClothInScene-v1 | iso_x0.25 | 24 | 0 | 0.000 | [0.00, 0.14] | 60.0 | 0.20 |
| octo-base@chunk4 | PutSpoonOnTableClothInScene-v1 | iso_x4.0 | 24 | 1 | 0.042 | [0.01, 0.20] | 60.0 | 0.16 |
| octo-base@chunk4 | PutSpoonOnTableClothInScene-v1 | nominal | 24 | 0 | 0.000 | [0.00, 0.14] | 60.0 | 0.27 |
| octo-base@hist1 | PutEggplantInBasketScene-v1 | dens_x0.5 | 24 | 7 | 0.292 | [0.15, 0.49] | 120.0 | 0.20 |
| octo-base@hist1 | PutEggplantInBasketScene-v1 | force_x0.5 | 24 | 11 | 0.458 | [0.28, 0.65] | 120.0 | 0.22 |
| octo-base@hist1 | PutEggplantInBasketScene-v1 | fric_x0.4 | 24 | 9 | 0.375 | [0.21, 0.57] | 120.0 | 0.21 |
| octo-base@hist1 | PutEggplantInBasketScene-v1 | iso_x0.25 | 24 | 6 | 0.250 | [0.12, 0.45] | 120.0 | 0.22 |
| octo-base@hist1 | PutEggplantInBasketScene-v1 | iso_x4.0 | 24 | 11 | 0.458 | [0.28, 0.65] | 120.0 | 0.21 |
| octo-base@hist1 | PutEggplantInBasketScene-v1 | nominal | 24 | 9 | 0.375 | [0.21, 0.57] | 120.0 | 0.22 |
| octo-base@hist1 | PutSpoonOnTableClothInScene-v1 | dens_x0.5 | 24 | 5 | 0.208 | [0.09, 0.40] | 60.0 | 0.09 |
| octo-base@hist1 | PutSpoonOnTableClothInScene-v1 | force_x0.5 | 24 | 3 | 0.125 | [0.04, 0.31] | 60.0 | 0.10 |
| octo-base@hist1 | PutSpoonOnTableClothInScene-v1 | fric_x0.4 | 24 | 5 | 0.208 | [0.09, 0.40] | 60.0 | 0.09 |
| octo-base@hist1 | PutSpoonOnTableClothInScene-v1 | iso_x0.25 | 24 | 4 | 0.167 | [0.07, 0.36] | 60.0 | 0.49 |
| octo-base@hist1 | PutSpoonOnTableClothInScene-v1 | iso_x4.0 | 24 | 7 | 0.292 | [0.15, 0.49] | 60.0 | 0.20 |
| octo-base@hist1 | PutSpoonOnTableClothInScene-v1 | nominal | 24 | 4 | 0.167 | [0.07, 0.36] | 60.0 | 0.47 |
| octo-base@noens | PutEggplantInBasketScene-v1 | dens_x0.5 | 24 | 3 | 0.125 | [0.04, 0.31] | 120.0 | 0.22 |
| octo-base@noens | PutEggplantInBasketScene-v1 | force_x0.5 | 24 | 8 | 0.333 | [0.18, 0.53] | 120.0 | 0.22 |
| octo-base@noens | PutEggplantInBasketScene-v1 | fric_x0.4 | 24 | 9 | 0.375 | [0.21, 0.57] | 120.0 | 0.23 |
| octo-base@noens | PutEggplantInBasketScene-v1 | iso_x0.25 | 24 | 4 | 0.167 | [0.07, 0.36] | 120.0 | 0.17 |
| octo-base@noens | PutEggplantInBasketScene-v1 | iso_x4.0 | 24 | 5 | 0.208 | [0.09, 0.40] | 120.0 | 0.18 |
| octo-base@noens | PutEggplantInBasketScene-v1 | nominal | 24 | 4 | 0.167 | [0.07, 0.36] | 120.0 | 0.34 |
| octo-base@noens | PutSpoonOnTableClothInScene-v1 | dens_x0.5 | 24 | 2 | 0.083 | [0.02, 0.26] | 60.0 | 0.40 |
| octo-base@noens | PutSpoonOnTableClothInScene-v1 | force_x0.5 | 24 | 2 | 0.083 | [0.02, 0.26] | 60.0 | 0.21 |
| octo-base@noens | PutSpoonOnTableClothInScene-v1 | fric_x0.4 | 24 | 2 | 0.083 | [0.02, 0.26] | 60.0 | 0.22 |
| octo-base@noens | PutSpoonOnTableClothInScene-v1 | iso_x0.25 | 24 | 0 | 0.000 | [0.00, 0.14] | 60.0 | 0.23 |
| octo-base@noens | PutSpoonOnTableClothInScene-v1 | iso_x4.0 | 24 | 1 | 0.042 | [0.01, 0.20] | 60.0 | 0.22 |
| octo-base@noens | PutSpoonOnTableClothInScene-v1 | nominal | 24 | 3 | 0.125 | [0.04, 0.31] | 60.0 | 0.23 |
| octo-small | PutCarrotOnPlateInScene-v1 | damp_x0.25 | 24 | 2 | 0.083 | [0.02, 0.26] | 60.0 | 0.15 |
| octo-small | PutCarrotOnPlateInScene-v1 | damp_x0.5 | 48 | 4 | 0.083 | [0.03, 0.20] | 60.0 | 0.17 |
| octo-small | PutCarrotOnPlateInScene-v1 | damp_x2.0 | 48 | 4 | 0.083 | [0.03, 0.20] | 60.0 | 0.21 |
| octo-small | PutCarrotOnPlateInScene-v1 | damp_x4.0 | 24 | 2 | 0.083 | [0.02, 0.26] | 60.0 | 0.15 |
| octo-small | PutCarrotOnPlateInScene-v1 | delay_1 | 48 | 5 | 0.104 | [0.05, 0.22] | 60.0 | 0.21 |
| octo-small | PutCarrotOnPlateInScene-v1 | delay_2 | 24 | 0 | 0.000 | [0.00, 0.14] | 60.0 | 0.15 |
| octo-small | PutCarrotOnPlateInScene-v1 | dens_x0.5 | 24 | 3 | 0.125 | [0.04, 0.31] | 60.0 | 0.19 |
| octo-small | PutCarrotOnPlateInScene-v1 | dens_x2.0 | 24 | 2 | 0.083 | [0.02, 0.26] | 60.0 | 0.15 |
| octo-small | PutCarrotOnPlateInScene-v1 | force_x0.5 | 48 | 6 | 0.125 | [0.06, 0.25] | 60.0 | 0.21 |
| octo-small | PutCarrotOnPlateInScene-v1 | fric_x0.4 | 24 | 3 | 0.125 | [0.04, 0.31] | 60.0 | 0.19 |
| octo-small | PutCarrotOnPlateInScene-v1 | fric_x2.5 | 24 | 3 | 0.125 | [0.04, 0.31] | 60.0 | 0.18 |
| octo-small | PutCarrotOnPlateInScene-v1 | iso_x0.25 | 96 | 8 | 0.083 | [0.04, 0.16] | 60.0 | 0.19 |
| octo-small | PutCarrotOnPlateInScene-v1 | iso_x0.5 | 96 | 6 | 0.062 | [0.03, 0.13] | 60.0 | 0.16 |
| octo-small | PutCarrotOnPlateInScene-v1 | iso_x2.0 | 48 | 7 | 0.146 | [0.07, 0.27] | 60.0 | 0.19 |
| octo-small | PutCarrotOnPlateInScene-v1 | iso_x4.0 | 96 | 13 | 0.135 | [0.08, 0.22] | 60.0 | 0.13 |
| octo-small | PutCarrotOnPlateInScene-v1 | nominal | 48 | 6 | 0.125 | [0.06, 0.25] | 60.0 | 0.15 |
| octo-small | PutCarrotOnPlateInScene-v1 | stiff_x0.25 | 24 | 2 | 0.083 | [0.02, 0.26] | 60.0 | 0.15 |
| octo-small | PutCarrotOnPlateInScene-v1 | stiff_x0.5 | 48 | 4 | 0.083 | [0.03, 0.20] | 60.0 | 0.16 |
| octo-small | PutCarrotOnPlateInScene-v1 | stiff_x2.0 | 48 | 6 | 0.125 | [0.06, 0.25] | 60.0 | 0.17 |
| octo-small | PutCarrotOnPlateInScene-v1 | stiff_x4.0 | 24 | 2 | 0.083 | [0.02, 0.26] | 60.0 | 0.15 |
| octo-small | PutEggplantInBasketScene-v1 | damp_x0.25 | 24 | 13 | 0.542 | [0.35, 0.72] | 120.0 | 0.15 |
| octo-small | PutEggplantInBasketScene-v1 | damp_x0.5 | 48 | 22 | 0.458 | [0.33, 0.60] | 120.0 | 0.19 |
| octo-small | PutEggplantInBasketScene-v1 | damp_x2.0 | 48 | 26 | 0.542 | [0.40, 0.67] | 120.0 | 0.19 |
| octo-small | PutEggplantInBasketScene-v1 | damp_x4.0 | 24 | 12 | 0.500 | [0.31, 0.69] | 120.0 | 0.13 |
| octo-small | PutEggplantInBasketScene-v1 | delay_1 | 48 | 24 | 0.500 | [0.36, 0.64] | 120.0 | 0.16 |
| octo-small | PutEggplantInBasketScene-v1 | delay_2 | 24 | 9 | 0.375 | [0.21, 0.57] | 120.0 | 0.09 |
| octo-small | PutEggplantInBasketScene-v1 | dens_x0.5 | 96 | 45 | 0.469 | [0.37, 0.57] | 120.0 | 0.14 |
| octo-small | PutEggplantInBasketScene-v1 | dens_x2.0 | 24 | 13 | 0.542 | [0.35, 0.72] | 120.0 | 0.15 |
| octo-small | PutEggplantInBasketScene-v1 | force_x0.5 | 48 | 22 | 0.458 | [0.33, 0.60] | 120.0 | 0.19 |
| octo-small | PutEggplantInBasketScene-v1 | fric_x0.4 | 96 | 47 | 0.490 | [0.39, 0.59] | 120.0 | 0.15 |
| octo-small | PutEggplantInBasketScene-v1 | fric_x2.5 | 24 | 10 | 0.417 | [0.24, 0.61] | 120.0 | 0.15 |
| octo-small | PutEggplantInBasketScene-v1 | iso_x0.25 | 48 | 20 | 0.417 | [0.29, 0.56] | 120.0 | 0.19 |
| octo-small | PutEggplantInBasketScene-v1 | iso_x0.5 | 48 | 26 | 0.542 | [0.40, 0.67] | 120.0 | 0.18 |
| octo-small | PutEggplantInBasketScene-v1 | iso_x2.0 | 48 | 24 | 0.500 | [0.36, 0.64] | 120.0 | 0.18 |
| octo-small | PutEggplantInBasketScene-v1 | iso_x4.0 | 48 | 27 | 0.562 | [0.42, 0.69] | 120.0 | 0.18 |
| octo-small | PutEggplantInBasketScene-v1 | nominal | 96 | 56 | 0.583 | [0.48, 0.68] | 120.0 | 0.18 |
| octo-small | PutEggplantInBasketScene-v1 | stiff_x0.25 | 24 | 4 | 0.167 | [0.07, 0.36] | 120.0 | 0.15 |
| octo-small | PutEggplantInBasketScene-v1 | stiff_x0.5 | 48 | 29 | 0.604 | [0.46, 0.73] | 120.0 | 0.19 |
| octo-small | PutEggplantInBasketScene-v1 | stiff_x2.0 | 48 | 24 | 0.500 | [0.36, 0.64] | 120.0 | 0.19 |
| octo-small | PutEggplantInBasketScene-v1 | stiff_x4.0 | 24 | 13 | 0.542 | [0.35, 0.72] | 120.0 | 0.16 |
| octo-small | PutSpoonOnTableClothInScene-v1 | damp_x0.25 | 24 | 3 | 0.125 | [0.04, 0.31] | 60.0 | 0.19 |
| octo-small | PutSpoonOnTableClothInScene-v1 | damp_x0.5 | 48 | 10 | 0.208 | [0.12, 0.34] | 60.0 | 0.18 |
| octo-small | PutSpoonOnTableClothInScene-v1 | damp_x2.0 | 48 | 14 | 0.292 | [0.18, 0.43] | 60.0 | 0.18 |
| octo-small | PutSpoonOnTableClothInScene-v1 | damp_x4.0 | 24 | 5 | 0.208 | [0.09, 0.40] | 60.0 | 0.19 |
| octo-small | PutSpoonOnTableClothInScene-v1 | delay_1 | 48 | 8 | 0.167 | [0.09, 0.30] | 60.0 | 0.15 |
| octo-small | PutSpoonOnTableClothInScene-v1 | delay_2 | 24 | 4 | 0.167 | [0.07, 0.36] | 60.0 | 0.19 |
| octo-small | PutSpoonOnTableClothInScene-v1 | dens_x0.5 | 24 | 6 | 0.250 | [0.12, 0.45] | 60.0 | 0.19 |
| octo-small | PutSpoonOnTableClothInScene-v1 | dens_x2.0 | 24 | 4 | 0.167 | [0.07, 0.36] | 60.0 | 0.19 |
| octo-small | PutSpoonOnTableClothInScene-v1 | force_x0.5 | 48 | 16 | 0.333 | [0.22, 0.47] | 60.0 | 0.16 |
| octo-small | PutSpoonOnTableClothInScene-v1 | fric_x0.4 | 24 | 4 | 0.167 | [0.07, 0.36] | 60.0 | 0.18 |
| octo-small | PutSpoonOnTableClothInScene-v1 | fric_x2.5 | 24 | 7 | 0.292 | [0.15, 0.49] | 60.0 | 0.19 |
| octo-small | PutSpoonOnTableClothInScene-v1 | iso_x0.25 | 48 | 12 | 0.250 | [0.15, 0.39] | 60.0 | 0.21 |
| octo-small | PutSpoonOnTableClothInScene-v1 | iso_x0.5 | 48 | 17 | 0.354 | [0.23, 0.50] | 60.0 | 0.21 |
| octo-small | PutSpoonOnTableClothInScene-v1 | iso_x2.0 | 48 | 12 | 0.250 | [0.15, 0.39] | 60.0 | 0.21 |
| octo-small | PutSpoonOnTableClothInScene-v1 | iso_x4.0 | 48 | 18 | 0.375 | [0.25, 0.52] | 60.0 | 0.21 |
| octo-small | PutSpoonOnTableClothInScene-v1 | nominal | 48 | 18 | 0.375 | [0.25, 0.52] | 60.0 | 0.17 |
| octo-small | PutSpoonOnTableClothInScene-v1 | stiff_x0.25 | 24 | 4 | 0.167 | [0.07, 0.36] | 60.0 | 0.19 |
| octo-small | PutSpoonOnTableClothInScene-v1 | stiff_x0.5 | 48 | 16 | 0.333 | [0.22, 0.47] | 60.0 | 0.18 |
| octo-small | PutSpoonOnTableClothInScene-v1 | stiff_x2.0 | 48 | 14 | 0.292 | [0.18, 0.43] | 60.0 | 0.18 |
| octo-small | PutSpoonOnTableClothInScene-v1 | stiff_x4.0 | 24 | 3 | 0.125 | [0.04, 0.31] | 60.0 | 0.19 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x0.25 | 24 | 0 | 0.000 | [0.00, 0.14] | 60.0 | 0.19 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x0.5 | 48 | 2 | 0.042 | [0.01, 0.14] | 60.0 | 0.16 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x2.0 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.16 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x4.0 | 24 | 0 | 0.000 | [0.00, 0.14] | 60.0 | 0.19 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | delay_1 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.16 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | delay_2 | 24 | 0 | 0.000 | [0.00, 0.14] | 60.0 | 0.19 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | force_x0.5 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.16 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x0.25 | 48 | 1 | 0.021 | [0.00, 0.11] | 60.0 | 0.19 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x0.5 | 48 | 1 | 0.021 | [0.00, 0.11] | 60.0 | 0.18 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x2.0 | 48 | 1 | 0.021 | [0.00, 0.11] | 60.0 | 0.18 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x4.0 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.18 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | nominal | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.16 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x0.25 | 24 | 0 | 0.000 | [0.00, 0.14] | 60.0 | 0.18 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x0.5 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.16 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x2.0 | 48 | 0 | 0.000 | [0.00, 0.07] | 60.0 | 0.16 |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x4.0 | 24 | 1 | 0.042 | [0.01, 0.20] | 60.0 | 0.19 |
| octo-small@chunk4 | PutEggplantInBasketScene-v1 | dens_x0.5 | 24 | 5 | 0.208 | [0.09, 0.40] | 120.0 | 0.04 |
| octo-small@chunk4 | PutEggplantInBasketScene-v1 | force_x0.5 | 24 | 5 | 0.208 | [0.09, 0.40] | 120.0 | 0.04 |
| octo-small@chunk4 | PutEggplantInBasketScene-v1 | fric_x0.4 | 24 | 7 | 0.292 | [0.15, 0.49] | 120.0 | 0.04 |
| octo-small@chunk4 | PutEggplantInBasketScene-v1 | iso_x0.25 | 24 | 3 | 0.125 | [0.04, 0.31] | 120.0 | 0.06 |
| octo-small@chunk4 | PutEggplantInBasketScene-v1 | iso_x4.0 | 24 | 5 | 0.208 | [0.09, 0.40] | 120.0 | 0.04 |
| octo-small@chunk4 | PutEggplantInBasketScene-v1 | nominal | 24 | 4 | 0.167 | [0.07, 0.36] | 120.0 | 0.11 |
| octo-small@chunk4 | PutSpoonOnTableClothInScene-v1 | dens_x0.5 | 24 | 2 | 0.083 | [0.02, 0.26] | 60.0 | 0.04 |
| octo-small@chunk4 | PutSpoonOnTableClothInScene-v1 | force_x0.5 | 24 | 2 | 0.083 | [0.02, 0.26] | 60.0 | 0.04 |
| octo-small@chunk4 | PutSpoonOnTableClothInScene-v1 | fric_x0.4 | 24 | 1 | 0.042 | [0.01, 0.20] | 60.0 | 0.04 |
| octo-small@chunk4 | PutSpoonOnTableClothInScene-v1 | iso_x0.25 | 24 | 2 | 0.083 | [0.02, 0.26] | 60.0 | 0.04 |
| octo-small@chunk4 | PutSpoonOnTableClothInScene-v1 | iso_x4.0 | 24 | 2 | 0.083 | [0.02, 0.26] | 60.0 | 0.04 |
| octo-small@chunk4 | PutSpoonOnTableClothInScene-v1 | nominal | 24 | 2 | 0.083 | [0.02, 0.26] | 60.0 | 0.04 |
| octo-small@hist1 | PutEggplantInBasketScene-v1 | dens_x0.5 | 24 | 11 | 0.458 | [0.28, 0.65] | 120.0 | 0.18 |
| octo-small@hist1 | PutEggplantInBasketScene-v1 | force_x0.5 | 24 | 11 | 0.458 | [0.28, 0.65] | 120.0 | 0.18 |
| octo-small@hist1 | PutEggplantInBasketScene-v1 | fric_x0.4 | 24 | 9 | 0.375 | [0.21, 0.57] | 120.0 | 0.19 |
| octo-small@hist1 | PutEggplantInBasketScene-v1 | iso_x0.25 | 24 | 9 | 0.375 | [0.21, 0.57] | 120.0 | 0.18 |
| octo-small@hist1 | PutEggplantInBasketScene-v1 | iso_x4.0 | 24 | 14 | 0.583 | [0.39, 0.76] | 120.0 | 0.19 |
| octo-small@hist1 | PutEggplantInBasketScene-v1 | nominal | 24 | 11 | 0.458 | [0.28, 0.65] | 120.0 | 0.18 |
| octo-small@hist1 | PutSpoonOnTableClothInScene-v1 | dens_x0.5 | 24 | 5 | 0.208 | [0.09, 0.40] | 60.0 | 0.28 |
| octo-small@hist1 | PutSpoonOnTableClothInScene-v1 | force_x0.5 | 24 | 6 | 0.250 | [0.12, 0.45] | 60.0 | 0.29 |
| octo-small@hist1 | PutSpoonOnTableClothInScene-v1 | fric_x0.4 | 24 | 9 | 0.375 | [0.21, 0.57] | 60.0 | 0.34 |
| octo-small@hist1 | PutSpoonOnTableClothInScene-v1 | iso_x0.25 | 24 | 8 | 0.333 | [0.18, 0.53] | 60.0 | 0.17 |
| octo-small@hist1 | PutSpoonOnTableClothInScene-v1 | iso_x4.0 | 24 | 6 | 0.250 | [0.12, 0.45] | 60.0 | 0.37 |
| octo-small@hist1 | PutSpoonOnTableClothInScene-v1 | nominal | 24 | 6 | 0.250 | [0.12, 0.45] | 60.0 | 0.18 |
| octo-small@noens | PutEggplantInBasketScene-v1 | dens_x0.5 | 24 | 6 | 0.250 | [0.12, 0.45] | 120.0 | 0.17 |
| octo-small@noens | PutEggplantInBasketScene-v1 | force_x0.5 | 24 | 5 | 0.208 | [0.09, 0.40] | 120.0 | 0.16 |
| octo-small@noens | PutEggplantInBasketScene-v1 | fric_x0.4 | 24 | 5 | 0.208 | [0.09, 0.40] | 120.0 | 0.16 |
| octo-small@noens | PutEggplantInBasketScene-v1 | iso_x0.25 | 24 | 4 | 0.167 | [0.07, 0.36] | 120.0 | 0.14 |
| octo-small@noens | PutEggplantInBasketScene-v1 | iso_x4.0 | 24 | 3 | 0.125 | [0.04, 0.31] | 120.0 | 0.13 |
| octo-small@noens | PutEggplantInBasketScene-v1 | nominal | 24 | 4 | 0.167 | [0.07, 0.36] | 120.0 | 0.28 |
| octo-small@noens | PutSpoonOnTableClothInScene-v1 | dens_x0.5 | 24 | 6 | 0.250 | [0.12, 0.45] | 60.0 | 0.16 |
| octo-small@noens | PutSpoonOnTableClothInScene-v1 | force_x0.5 | 24 | 5 | 0.208 | [0.09, 0.40] | 60.0 | 0.16 |
| octo-small@noens | PutSpoonOnTableClothInScene-v1 | fric_x0.4 | 24 | 4 | 0.167 | [0.07, 0.36] | 60.0 | 0.16 |
| octo-small@noens | PutSpoonOnTableClothInScene-v1 | iso_x0.25 | 24 | 3 | 0.125 | [0.04, 0.31] | 60.0 | 0.16 |
| octo-small@noens | PutSpoonOnTableClothInScene-v1 | iso_x4.0 | 24 | 4 | 0.167 | [0.07, 0.36] | 60.0 | 0.16 |
| octo-small@noens | PutSpoonOnTableClothInScene-v1 | nominal | 24 | 3 | 0.125 | [0.04, 0.31] | 60.0 | 0.16 |

## Pairwise differences Δ = rate(policy_i) − rate(policy_j), paired by episode

### PutCarrotOnPlateInScene-v1: octo-base vs octo-small

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| damp_x0.25 | 24 | +0.042 | [-0.08, +0.17] | 0 |
| damp_x0.5 | 48 | +0.042 | [-0.06, +0.15] | 0 |
| damp_x2.0 | 48 | +0.083 | [-0.06, +0.23] | 0 |
| damp_x4.0 | 24 | +0.083 | [-0.12, +0.29] | 0 |
| delay_1 | 48 | -0.021 | [-0.12, +0.08] | 0 |
| delay_2 | 24 | +0.000 | [+0.00, +0.00] | 0 |
| dens_x0.5 | 24 | -0.042 | [-0.21, +0.08] | 0 |
| dens_x2.0 | 24 | +0.083 | [+0.00, +0.21] | 0 |
| force_x0.5 | 48 | +0.000 | [-0.12, +0.12] | 0 |
| fric_x0.4 | 24 | +0.042 | [-0.12, +0.21] | 0 |
| fric_x2.5 | 24 | +0.042 | [-0.12, +0.25] | 0 |
| iso_x0.25 | 96 | +0.021 | [-0.04, +0.08] | 0 |
| iso_x0.5 | 96 | +0.062 | [+0.00, +0.14] | 0 |
| iso_x2.0 | 48 | +0.062 | [-0.04, +0.17] | 0 |
| iso_x4.0 | 96 | +0.000 | [-0.08, +0.08] | 0 |
| nominal | 48 | +0.021 | [-0.10, +0.15] | 0 |
| stiff_x0.25 | 24 | -0.083 | [-0.21, +0.00] | 0 |
| stiff_x0.5 | 48 | +0.062 | [-0.06, +0.19] | 0 |
| stiff_x2.0 | 48 | +0.042 | [-0.06, +0.15] | 0 |
| stiff_x4.0 | 24 | +0.042 | [+0.00, +0.12] | 0 |

### PutEggplantInBasketScene-v1: octo-base vs octo-base@chunk4

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | +0.208 | [-0.04, +0.46] | 0 |
| force_x0.5 | 24 | +0.250 | [+0.00, +0.46] | 0 |
| fric_x0.4 | 24 | +0.333 | [+0.12, +0.54] | + |
| iso_x0.25 | 24 | +0.208 | [+0.00, +0.42] | 0 |
| iso_x4.0 | 24 | +0.208 | [+0.04, +0.42] | + |
| nominal | 24 | +0.167 | [+0.00, +0.33] | 0 |

### PutEggplantInBasketScene-v1: octo-base vs octo-base@hist1

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | +0.125 | [-0.12, +0.38] | 0 |
| force_x0.5 | 24 | -0.083 | [-0.38, +0.21] | 0 |
| fric_x0.4 | 24 | +0.083 | [-0.17, +0.29] | 0 |
| iso_x0.25 | 24 | +0.125 | [-0.12, +0.38] | 0 |
| iso_x4.0 | 24 | -0.083 | [-0.29, +0.12] | 0 |
| nominal | 24 | -0.125 | [-0.38, +0.12] | 0 |

### PutEggplantInBasketScene-v1: octo-base vs octo-base@noens

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | +0.292 | [+0.08, +0.50] | + |
| force_x0.5 | 24 | +0.042 | [-0.17, +0.25] | 0 |
| fric_x0.4 | 24 | +0.083 | [-0.21, +0.38] | 0 |
| iso_x0.25 | 24 | +0.208 | [+0.00, +0.42] | 0 |
| iso_x4.0 | 24 | +0.167 | [-0.08, +0.42] | 0 |
| nominal | 24 | +0.083 | [-0.12, +0.29] | 0 |

### PutEggplantInBasketScene-v1: octo-base vs octo-small

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| damp_x0.25 | 24 | -0.125 | [-0.38, +0.12] | 0 |
| damp_x0.5 | 48 | -0.083 | [-0.27, +0.10] | 0 |
| damp_x2.0 | 48 | -0.250 | [-0.44, -0.06] | − |
| damp_x4.0 | 24 | -0.375 | [-0.58, -0.17] | − |
| delay_1 | 48 | -0.312 | [-0.50, -0.12] | − |
| delay_2 | 24 | -0.375 | [-0.58, -0.21] | − |
| dens_x0.5 | 96 | -0.073 | [-0.19, +0.04] | 0 |
| dens_x2.0 | 24 | -0.292 | [-0.54, +0.00] | 0 |
| force_x0.5 | 48 | -0.146 | [-0.31, +0.02] | 0 |
| fric_x0.4 | 96 | -0.052 | [-0.18, +0.07] | 0 |
| fric_x2.5 | 24 | -0.167 | [-0.38, +0.04] | 0 |
| iso_x0.25 | 48 | -0.062 | [-0.23, +0.10] | 0 |
| iso_x0.5 | 48 | -0.208 | [-0.38, -0.04] | − |
| iso_x2.0 | 48 | -0.125 | [-0.27, +0.02] | 0 |
| iso_x4.0 | 48 | -0.208 | [-0.40, -0.02] | − |
| nominal | 96 | -0.208 | [-0.32, -0.09] | − |
| stiff_x0.25 | 24 | -0.083 | [-0.25, +0.08] | 0 |
| stiff_x0.5 | 48 | -0.354 | [-0.52, -0.17] | − |
| stiff_x2.0 | 48 | -0.125 | [-0.27, +0.02] | 0 |
| stiff_x4.0 | 24 | -0.208 | [-0.46, +0.04] | 0 |

### PutEggplantInBasketScene-v1: octo-base vs octo-small@chunk4

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | +0.208 | [-0.04, +0.46] | 0 |
| force_x0.5 | 24 | +0.167 | [-0.08, +0.42] | 0 |
| fric_x0.4 | 24 | +0.167 | [-0.08, +0.42] | 0 |
| iso_x0.25 | 24 | +0.250 | [+0.04, +0.46] | + |
| iso_x4.0 | 24 | +0.167 | [-0.08, +0.42] | 0 |
| nominal | 24 | +0.083 | [-0.17, +0.33] | 0 |

### PutEggplantInBasketScene-v1: octo-base vs octo-small@hist1

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.042 | [-0.25, +0.17] | 0 |
| force_x0.5 | 24 | -0.083 | [-0.29, +0.12] | 0 |
| fric_x0.4 | 24 | +0.083 | [-0.12, +0.29] | 0 |
| iso_x0.25 | 24 | +0.000 | [-0.21, +0.21] | 0 |
| iso_x4.0 | 24 | -0.208 | [-0.46, +0.04] | 0 |
| nominal | 24 | -0.208 | [-0.46, +0.04] | 0 |

### PutEggplantInBasketScene-v1: octo-base vs octo-small@noens

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | +0.167 | [-0.12, +0.42] | 0 |
| force_x0.5 | 24 | +0.167 | [-0.08, +0.42] | 0 |
| fric_x0.4 | 24 | +0.250 | [+0.00, +0.50] | 0 |
| iso_x0.25 | 24 | +0.208 | [+0.00, +0.46] | 0 |
| iso_x4.0 | 24 | +0.250 | [+0.00, +0.50] | 0 |
| nominal | 24 | +0.083 | [-0.08, +0.25] | 0 |

### PutEggplantInBasketScene-v1: octo-base@chunk4 vs octo-base@hist1

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.083 | [-0.33, +0.17] | 0 |
| force_x0.5 | 24 | -0.333 | [-0.54, -0.12] | − |
| fric_x0.4 | 24 | -0.250 | [-0.50, +0.00] | 0 |
| iso_x0.25 | 24 | -0.083 | [-0.33, +0.12] | 0 |
| iso_x4.0 | 24 | -0.292 | [-0.46, -0.12] | − |
| nominal | 24 | -0.292 | [-0.50, -0.08] | − |

### PutEggplantInBasketScene-v1: octo-base@chunk4 vs octo-base@noens

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | +0.083 | [-0.12, +0.29] | 0 |
| force_x0.5 | 24 | -0.208 | [-0.42, +0.04] | 0 |
| fric_x0.4 | 24 | -0.250 | [-0.42, -0.08] | − |
| iso_x0.25 | 24 | +0.000 | [-0.21, +0.21] | 0 |
| iso_x4.0 | 24 | -0.042 | [-0.17, +0.08] | 0 |
| nominal | 24 | -0.083 | [-0.25, +0.08] | 0 |

### PutEggplantInBasketScene-v1: octo-base@chunk4 vs octo-small

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.375 | [-0.62, -0.12] | − |
| force_x0.5 | 24 | -0.375 | [-0.62, -0.08] | − |
| fric_x0.4 | 24 | -0.375 | [-0.58, -0.17] | − |
| iso_x0.25 | 24 | -0.292 | [-0.50, -0.08] | − |
| iso_x4.0 | 24 | -0.375 | [-0.62, -0.12] | − |
| nominal | 24 | -0.458 | [-0.67, -0.21] | − |

### PutEggplantInBasketScene-v1: octo-base@chunk4 vs octo-small@chunk4

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | +0.000 | [-0.25, +0.21] | 0 |
| force_x0.5 | 24 | -0.083 | [-0.29, +0.12] | 0 |
| fric_x0.4 | 24 | -0.167 | [-0.33, +0.00] | 0 |
| iso_x0.25 | 24 | +0.042 | [-0.12, +0.21] | 0 |
| iso_x4.0 | 24 | -0.042 | [-0.25, +0.17] | 0 |
| nominal | 24 | -0.083 | [-0.29, +0.12] | 0 |

### PutEggplantInBasketScene-v1: octo-base@chunk4 vs octo-small@hist1

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.250 | [-0.50, +0.00] | 0 |
| force_x0.5 | 24 | -0.333 | [-0.58, -0.08] | − |
| fric_x0.4 | 24 | -0.250 | [-0.46, -0.04] | − |
| iso_x0.25 | 24 | -0.208 | [-0.42, +0.00] | 0 |
| iso_x4.0 | 24 | -0.417 | [-0.62, -0.21] | − |
| nominal | 24 | -0.375 | [-0.58, -0.17] | − |

### PutEggplantInBasketScene-v1: octo-base@chunk4 vs octo-small@noens

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.042 | [-0.29, +0.21] | 0 |
| force_x0.5 | 24 | -0.083 | [-0.25, +0.08] | 0 |
| fric_x0.4 | 24 | -0.083 | [-0.29, +0.12] | 0 |
| iso_x0.25 | 24 | +0.000 | [-0.21, +0.25] | 0 |
| iso_x4.0 | 24 | +0.042 | [-0.17, +0.25] | 0 |
| nominal | 24 | -0.083 | [-0.21, +0.00] | 0 |

### PutEggplantInBasketScene-v1: octo-base@hist1 vs octo-base@noens

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | +0.167 | [+0.00, +0.33] | 0 |
| force_x0.5 | 24 | +0.125 | [-0.12, +0.38] | 0 |
| fric_x0.4 | 24 | +0.000 | [-0.29, +0.29] | 0 |
| iso_x0.25 | 24 | +0.083 | [-0.17, +0.33] | 0 |
| iso_x4.0 | 24 | +0.250 | [+0.08, +0.42] | + |
| nominal | 24 | +0.208 | [+0.00, +0.46] | 0 |

### PutEggplantInBasketScene-v1: octo-base@hist1 vs octo-small

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.292 | [-0.50, -0.08] | − |
| force_x0.5 | 24 | -0.042 | [-0.25, +0.17] | 0 |
| fric_x0.4 | 24 | -0.125 | [-0.33, +0.08] | 0 |
| iso_x0.25 | 24 | -0.208 | [-0.42, +0.00] | 0 |
| iso_x4.0 | 24 | -0.083 | [-0.38, +0.21] | 0 |
| nominal | 24 | -0.167 | [-0.42, +0.12] | 0 |

### PutEggplantInBasketScene-v1: octo-base@hist1 vs octo-small@chunk4

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | +0.083 | [-0.12, +0.29] | 0 |
| force_x0.5 | 24 | +0.250 | [+0.00, +0.50] | 0 |
| fric_x0.4 | 24 | +0.083 | [-0.12, +0.29] | 0 |
| iso_x0.25 | 24 | +0.125 | [+0.00, +0.25] | 0 |
| iso_x4.0 | 24 | +0.250 | [+0.00, +0.50] | 0 |
| nominal | 24 | +0.208 | [-0.04, +0.46] | 0 |

### PutEggplantInBasketScene-v1: octo-base@hist1 vs octo-small@hist1

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.167 | [-0.46, +0.08] | 0 |
| force_x0.5 | 24 | +0.000 | [-0.21, +0.21] | 0 |
| fric_x0.4 | 24 | +0.000 | [-0.29, +0.29] | 0 |
| iso_x0.25 | 24 | -0.125 | [-0.38, +0.12] | 0 |
| iso_x4.0 | 24 | -0.125 | [-0.38, +0.12] | 0 |
| nominal | 24 | -0.083 | [-0.33, +0.17] | 0 |

### PutEggplantInBasketScene-v1: octo-base@hist1 vs octo-small@noens

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | +0.042 | [-0.08, +0.17] | 0 |
| force_x0.5 | 24 | +0.250 | [+0.08, +0.42] | + |
| fric_x0.4 | 24 | +0.167 | [-0.04, +0.38] | 0 |
| iso_x0.25 | 24 | +0.083 | [-0.17, +0.33] | 0 |
| iso_x4.0 | 24 | +0.333 | [+0.04, +0.58] | + |
| nominal | 24 | +0.208 | [-0.04, +0.46] | 0 |

### PutEggplantInBasketScene-v1: octo-base@noens vs octo-small

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.458 | [-0.67, -0.25] | − |
| force_x0.5 | 24 | -0.167 | [-0.38, +0.04] | 0 |
| fric_x0.4 | 24 | -0.125 | [-0.38, +0.12] | 0 |
| iso_x0.25 | 24 | -0.292 | [-0.54, +0.00] | 0 |
| iso_x4.0 | 24 | -0.333 | [-0.58, -0.08] | − |
| nominal | 24 | -0.375 | [-0.58, -0.17] | − |

### PutEggplantInBasketScene-v1: octo-base@noens vs octo-small@chunk4

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.083 | [-0.25, +0.08] | 0 |
| force_x0.5 | 24 | +0.125 | [+0.00, +0.25] | 0 |
| fric_x0.4 | 24 | +0.083 | [-0.17, +0.33] | 0 |
| iso_x0.25 | 24 | +0.042 | [-0.17, +0.25] | 0 |
| iso_x4.0 | 24 | +0.000 | [-0.21, +0.25] | 0 |
| nominal | 24 | +0.000 | [-0.25, +0.21] | 0 |

### PutEggplantInBasketScene-v1: octo-base@noens vs octo-small@hist1

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.333 | [-0.54, -0.12] | − |
| force_x0.5 | 24 | -0.125 | [-0.33, +0.08] | 0 |
| fric_x0.4 | 24 | +0.000 | [-0.29, +0.29] | 0 |
| iso_x0.25 | 24 | -0.208 | [-0.42, +0.00] | 0 |
| iso_x4.0 | 24 | -0.375 | [-0.58, -0.21] | − |
| nominal | 24 | -0.292 | [-0.50, -0.12] | − |

### PutEggplantInBasketScene-v1: octo-base@noens vs octo-small@noens

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.125 | [-0.33, +0.08] | 0 |
| force_x0.5 | 24 | +0.125 | [-0.12, +0.38] | 0 |
| fric_x0.4 | 24 | +0.167 | [-0.08, +0.42] | 0 |
| iso_x0.25 | 24 | +0.000 | [-0.21, +0.25] | 0 |
| iso_x4.0 | 24 | +0.083 | [-0.12, +0.29] | 0 |
| nominal | 24 | +0.000 | [-0.21, +0.21] | 0 |

### PutEggplantInBasketScene-v1: octo-small vs octo-small@chunk4

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | +0.375 | [+0.12, +0.62] | + |
| force_x0.5 | 24 | +0.292 | [+0.08, +0.50] | + |
| fric_x0.4 | 24 | +0.208 | [+0.00, +0.42] | 0 |
| iso_x0.25 | 24 | +0.333 | [+0.17, +0.50] | + |
| iso_x4.0 | 24 | +0.333 | [+0.08, +0.58] | + |
| nominal | 24 | +0.375 | [+0.08, +0.62] | + |

### PutEggplantInBasketScene-v1: octo-small vs octo-small@hist1

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | +0.125 | [-0.12, +0.38] | 0 |
| force_x0.5 | 24 | +0.042 | [-0.21, +0.29] | 0 |
| fric_x0.4 | 24 | +0.125 | [-0.12, +0.38] | 0 |
| iso_x0.25 | 24 | +0.083 | [-0.17, +0.33] | 0 |
| iso_x4.0 | 24 | -0.042 | [-0.29, +0.21] | 0 |
| nominal | 24 | +0.083 | [-0.17, +0.33] | 0 |

### PutEggplantInBasketScene-v1: octo-small vs octo-small@noens

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | +0.333 | [+0.12, +0.54] | + |
| force_x0.5 | 24 | +0.292 | [+0.04, +0.54] | + |
| fric_x0.4 | 24 | +0.292 | [+0.12, +0.46] | + |
| iso_x0.25 | 24 | +0.292 | [+0.08, +0.50] | + |
| iso_x4.0 | 24 | +0.417 | [+0.21, +0.62] | + |
| nominal | 24 | +0.375 | [+0.17, +0.58] | + |

### PutEggplantInBasketScene-v1: octo-small@chunk4 vs octo-small@hist1

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.250 | [-0.50, +0.00] | 0 |
| force_x0.5 | 24 | -0.250 | [-0.50, +0.00] | 0 |
| fric_x0.4 | 24 | -0.083 | [-0.29, +0.12] | 0 |
| iso_x0.25 | 24 | -0.250 | [-0.46, -0.04] | − |
| iso_x4.0 | 24 | -0.375 | [-0.62, -0.08] | − |
| nominal | 24 | -0.292 | [-0.54, -0.04] | − |

### PutEggplantInBasketScene-v1: octo-small@chunk4 vs octo-small@noens

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.042 | [-0.25, +0.17] | 0 |
| force_x0.5 | 24 | +0.000 | [-0.21, +0.25] | 0 |
| fric_x0.4 | 24 | +0.083 | [-0.21, +0.38] | 0 |
| iso_x0.25 | 24 | -0.042 | [-0.25, +0.17] | 0 |
| iso_x4.0 | 24 | +0.083 | [-0.12, +0.29] | 0 |
| nominal | 24 | +0.000 | [-0.21, +0.25] | 0 |

### PutEggplantInBasketScene-v1: octo-small@hist1 vs octo-small@noens

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | +0.208 | [-0.04, +0.46] | 0 |
| force_x0.5 | 24 | +0.250 | [+0.00, +0.50] | 0 |
| fric_x0.4 | 24 | +0.167 | [-0.08, +0.42] | 0 |
| iso_x0.25 | 24 | +0.208 | [+0.00, +0.42] | 0 |
| iso_x4.0 | 24 | +0.458 | [+0.21, +0.67] | + |
| nominal | 24 | +0.292 | [+0.04, +0.54] | + |

### PutSpoonOnTableClothInScene-v1: octo-base vs octo-base@chunk4

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.042 | [-0.17, +0.08] | 0 |
| force_x0.5 | 24 | +0.042 | [-0.08, +0.17] | 0 |
| fric_x0.4 | 24 | +0.083 | [+0.00, +0.21] | 0 |
| iso_x0.25 | 24 | +0.000 | [+0.00, +0.00] | 0 |
| iso_x4.0 | 24 | +0.083 | [-0.08, +0.25] | 0 |
| nominal | 24 | +0.083 | [+0.00, +0.21] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-base vs octo-base@hist1

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.167 | [-0.33, +0.00] | 0 |
| force_x0.5 | 24 | -0.042 | [-0.21, +0.12] | 0 |
| fric_x0.4 | 24 | -0.125 | [-0.33, +0.08] | 0 |
| iso_x0.25 | 24 | -0.167 | [-0.33, -0.04] | − |
| iso_x4.0 | 24 | -0.167 | [-0.38, +0.04] | 0 |
| nominal | 24 | -0.083 | [-0.29, +0.12] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-base vs octo-base@noens

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.042 | [-0.17, +0.08] | 0 |
| force_x0.5 | 24 | +0.000 | [-0.12, +0.12] | 0 |
| fric_x0.4 | 24 | +0.000 | [-0.17, +0.17] | 0 |
| iso_x0.25 | 24 | +0.000 | [+0.00, +0.00] | 0 |
| iso_x4.0 | 24 | +0.083 | [-0.08, +0.25] | 0 |
| nominal | 24 | -0.042 | [-0.21, +0.08] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-base vs octo-small

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| damp_x0.25 | 24 | -0.042 | [-0.12, +0.00] | 0 |
| damp_x0.5 | 48 | -0.146 | [-0.27, -0.04] | − |
| damp_x2.0 | 48 | -0.208 | [-0.35, -0.06] | − |
| damp_x4.0 | 24 | -0.208 | [-0.38, -0.04] | − |
| delay_1 | 48 | +0.000 | [-0.12, +0.12] | 0 |
| delay_2 | 24 | +0.000 | [-0.17, +0.17] | 0 |
| dens_x0.5 | 24 | -0.208 | [-0.42, +0.00] | 0 |
| dens_x2.0 | 24 | -0.167 | [-0.33, -0.04] | − |
| force_x0.5 | 48 | -0.229 | [-0.35, -0.10] | − |
| fric_x0.4 | 24 | -0.083 | [-0.29, +0.12] | 0 |
| fric_x2.5 | 24 | -0.167 | [-0.38, +0.04] | 0 |
| iso_x0.25 | 48 | -0.229 | [-0.35, -0.10] | − |
| iso_x0.5 | 48 | -0.333 | [-0.48, -0.19] | − |
| iso_x2.0 | 48 | -0.146 | [-0.29, +0.00] | 0 |
| iso_x4.0 | 48 | -0.312 | [-0.46, -0.17] | − |
| nominal | 48 | -0.292 | [-0.44, -0.15] | − |
| stiff_x0.25 | 24 | -0.167 | [-0.33, -0.04] | − |
| stiff_x0.5 | 48 | -0.250 | [-0.40, -0.10] | − |
| stiff_x2.0 | 48 | -0.208 | [-0.35, -0.06] | − |
| stiff_x4.0 | 24 | -0.083 | [-0.21, +0.00] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-base vs octo-small@chunk4

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.042 | [-0.17, +0.08] | 0 |
| force_x0.5 | 24 | +0.000 | [-0.17, +0.17] | 0 |
| fric_x0.4 | 24 | +0.042 | [-0.08, +0.17] | 0 |
| iso_x0.25 | 24 | -0.083 | [-0.21, +0.00] | 0 |
| iso_x4.0 | 24 | +0.042 | [+0.00, +0.12] | 0 |
| nominal | 24 | +0.000 | [-0.17, +0.17] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-base vs octo-small@hist1

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.167 | [-0.33, -0.04] | − |
| force_x0.5 | 24 | -0.167 | [-0.38, +0.00] | 0 |
| fric_x0.4 | 24 | -0.292 | [-0.50, -0.12] | − |
| iso_x0.25 | 24 | -0.333 | [-0.54, -0.17] | − |
| iso_x4.0 | 24 | -0.125 | [-0.29, +0.04] | 0 |
| nominal | 24 | -0.167 | [-0.33, +0.00] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-base vs octo-small@noens

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.208 | [-0.42, +0.00] | 0 |
| force_x0.5 | 24 | -0.125 | [-0.33, +0.08] | 0 |
| fric_x0.4 | 24 | -0.083 | [-0.29, +0.12] | 0 |
| iso_x0.25 | 24 | -0.125 | [-0.25, +0.00] | 0 |
| iso_x4.0 | 24 | -0.042 | [-0.25, +0.17] | 0 |
| nominal | 24 | -0.042 | [-0.21, +0.12] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-base@chunk4 vs octo-base@hist1

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.125 | [-0.33, +0.08] | 0 |
| force_x0.5 | 24 | -0.083 | [-0.25, +0.08] | 0 |
| fric_x0.4 | 24 | -0.208 | [-0.38, -0.04] | − |
| iso_x0.25 | 24 | -0.167 | [-0.33, -0.04] | − |
| iso_x4.0 | 24 | -0.250 | [-0.42, -0.08] | − |
| nominal | 24 | -0.167 | [-0.33, -0.04] | − |

### PutSpoonOnTableClothInScene-v1: octo-base@chunk4 vs octo-base@noens

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | +0.000 | [-0.17, +0.17] | 0 |
| force_x0.5 | 24 | -0.042 | [-0.12, +0.00] | 0 |
| fric_x0.4 | 24 | -0.083 | [-0.21, +0.00] | 0 |
| iso_x0.25 | 24 | +0.000 | [+0.00, +0.00] | 0 |
| iso_x4.0 | 24 | +0.000 | [-0.12, +0.12] | 0 |
| nominal | 24 | -0.125 | [-0.25, +0.00] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-base@chunk4 vs octo-small

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.167 | [-0.38, +0.04] | 0 |
| force_x0.5 | 24 | -0.208 | [-0.38, -0.04] | − |
| fric_x0.4 | 24 | -0.167 | [-0.33, -0.04] | − |
| iso_x0.25 | 24 | -0.250 | [-0.42, -0.08] | − |
| iso_x4.0 | 24 | -0.250 | [-0.42, -0.08] | − |
| nominal | 24 | -0.375 | [-0.58, -0.17] | − |

### PutSpoonOnTableClothInScene-v1: octo-base@chunk4 vs octo-small@chunk4

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | +0.000 | [-0.12, +0.12] | 0 |
| force_x0.5 | 24 | -0.042 | [-0.17, +0.08] | 0 |
| fric_x0.4 | 24 | -0.042 | [-0.12, +0.00] | 0 |
| iso_x0.25 | 24 | -0.083 | [-0.21, +0.00] | 0 |
| iso_x4.0 | 24 | -0.042 | [-0.17, +0.08] | 0 |
| nominal | 24 | -0.083 | [-0.21, +0.00] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-base@chunk4 vs octo-small@hist1

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.125 | [-0.33, +0.08] | 0 |
| force_x0.5 | 24 | -0.208 | [-0.42, +0.00] | 0 |
| fric_x0.4 | 24 | -0.375 | [-0.58, -0.21] | − |
| iso_x0.25 | 24 | -0.333 | [-0.54, -0.17] | − |
| iso_x4.0 | 24 | -0.208 | [-0.42, +0.00] | 0 |
| nominal | 24 | -0.250 | [-0.42, -0.08] | − |

### PutSpoonOnTableClothInScene-v1: octo-base@chunk4 vs octo-small@noens

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.167 | [-0.38, +0.00] | 0 |
| force_x0.5 | 24 | -0.167 | [-0.33, -0.04] | − |
| fric_x0.4 | 24 | -0.167 | [-0.33, -0.04] | − |
| iso_x0.25 | 24 | -0.125 | [-0.25, +0.00] | 0 |
| iso_x4.0 | 24 | -0.125 | [-0.29, +0.04] | 0 |
| nominal | 24 | -0.125 | [-0.25, +0.00] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-base@hist1 vs octo-base@noens

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | +0.125 | [+0.00, +0.25] | 0 |
| force_x0.5 | 24 | +0.042 | [-0.12, +0.21] | 0 |
| fric_x0.4 | 24 | +0.125 | [-0.04, +0.29] | 0 |
| iso_x0.25 | 24 | +0.167 | [+0.04, +0.33] | + |
| iso_x4.0 | 24 | +0.250 | [+0.08, +0.42] | + |
| nominal | 24 | +0.042 | [-0.17, +0.25] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-base@hist1 vs octo-small

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.042 | [-0.21, +0.12] | 0 |
| force_x0.5 | 24 | -0.125 | [-0.33, +0.08] | 0 |
| fric_x0.4 | 24 | +0.042 | [-0.17, +0.25] | 0 |
| iso_x0.25 | 24 | -0.083 | [-0.25, +0.08] | 0 |
| iso_x4.0 | 24 | +0.000 | [-0.17, +0.17] | 0 |
| nominal | 24 | -0.208 | [-0.46, +0.04] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-base@hist1 vs octo-small@chunk4

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | +0.125 | [-0.08, +0.33] | 0 |
| force_x0.5 | 24 | +0.042 | [-0.08, +0.17] | 0 |
| fric_x0.4 | 24 | +0.167 | [+0.00, +0.33] | 0 |
| iso_x0.25 | 24 | +0.083 | [-0.12, +0.29] | 0 |
| iso_x4.0 | 24 | +0.208 | [+0.00, +0.42] | 0 |
| nominal | 24 | +0.083 | [-0.08, +0.25] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-base@hist1 vs octo-small@hist1

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | +0.000 | [-0.17, +0.17] | 0 |
| force_x0.5 | 24 | -0.125 | [-0.29, +0.04] | 0 |
| fric_x0.4 | 24 | -0.167 | [-0.38, +0.04] | 0 |
| iso_x0.25 | 24 | -0.167 | [-0.38, +0.04] | 0 |
| iso_x4.0 | 24 | +0.042 | [-0.12, +0.21] | 0 |
| nominal | 24 | -0.083 | [-0.29, +0.12] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-base@hist1 vs octo-small@noens

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.042 | [-0.29, +0.21] | 0 |
| force_x0.5 | 24 | -0.083 | [-0.29, +0.12] | 0 |
| fric_x0.4 | 24 | +0.042 | [-0.12, +0.21] | 0 |
| iso_x0.25 | 24 | +0.042 | [-0.17, +0.25] | 0 |
| iso_x4.0 | 24 | +0.125 | [-0.08, +0.33] | 0 |
| nominal | 24 | +0.042 | [-0.17, +0.25] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-base@noens vs octo-small

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.167 | [-0.38, +0.00] | 0 |
| force_x0.5 | 24 | -0.167 | [-0.33, -0.04] | − |
| fric_x0.4 | 24 | -0.083 | [-0.29, +0.12] | 0 |
| iso_x0.25 | 24 | -0.250 | [-0.42, -0.08] | − |
| iso_x4.0 | 24 | -0.250 | [-0.42, -0.08] | − |
| nominal | 24 | -0.250 | [-0.42, -0.08] | − |

### PutSpoonOnTableClothInScene-v1: octo-base@noens vs octo-small@chunk4

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | +0.000 | [-0.17, +0.17] | 0 |
| force_x0.5 | 24 | +0.000 | [-0.17, +0.17] | 0 |
| fric_x0.4 | 24 | +0.042 | [-0.08, +0.17] | 0 |
| iso_x0.25 | 24 | -0.083 | [-0.21, +0.00] | 0 |
| iso_x4.0 | 24 | -0.042 | [-0.17, +0.08] | 0 |
| nominal | 24 | +0.042 | [-0.12, +0.21] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-base@noens vs octo-small@hist1

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.125 | [-0.25, +0.00] | 0 |
| force_x0.5 | 24 | -0.167 | [-0.38, +0.00] | 0 |
| fric_x0.4 | 24 | -0.292 | [-0.50, -0.08] | − |
| iso_x0.25 | 24 | -0.333 | [-0.54, -0.17] | − |
| iso_x4.0 | 24 | -0.208 | [-0.38, -0.04] | − |
| nominal | 24 | -0.125 | [-0.33, +0.08] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-base@noens vs octo-small@noens

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.167 | [-0.38, +0.04] | 0 |
| force_x0.5 | 24 | -0.125 | [-0.29, +0.04] | 0 |
| fric_x0.4 | 24 | -0.083 | [-0.25, +0.08] | 0 |
| iso_x0.25 | 24 | -0.125 | [-0.25, +0.00] | 0 |
| iso_x4.0 | 24 | -0.125 | [-0.29, +0.04] | 0 |
| nominal | 24 | +0.000 | [-0.17, +0.17] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-small vs octo-small@chunk4

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | +0.167 | [-0.04, +0.38] | 0 |
| force_x0.5 | 24 | +0.167 | [-0.04, +0.38] | 0 |
| fric_x0.4 | 24 | +0.125 | [-0.04, +0.29] | 0 |
| iso_x0.25 | 24 | +0.167 | [+0.00, +0.33] | 0 |
| iso_x4.0 | 24 | +0.208 | [+0.00, +0.42] | 0 |
| nominal | 24 | +0.292 | [+0.04, +0.54] | + |

### PutSpoonOnTableClothInScene-v1: octo-small vs octo-small@hist1

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | +0.042 | [-0.12, +0.21] | 0 |
| force_x0.5 | 24 | +0.000 | [-0.21, +0.21] | 0 |
| fric_x0.4 | 24 | -0.208 | [-0.46, +0.04] | 0 |
| iso_x0.25 | 24 | -0.083 | [-0.29, +0.12] | 0 |
| iso_x4.0 | 24 | +0.042 | [-0.17, +0.25] | 0 |
| nominal | 24 | +0.125 | [-0.04, +0.29] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-small vs octo-small@noens

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | +0.000 | [-0.25, +0.21] | 0 |
| force_x0.5 | 24 | +0.042 | [-0.21, +0.29] | 0 |
| fric_x0.4 | 24 | +0.000 | [-0.25, +0.21] | 0 |
| iso_x0.25 | 24 | +0.125 | [-0.08, +0.33] | 0 |
| iso_x4.0 | 24 | +0.125 | [-0.12, +0.38] | 0 |
| nominal | 24 | +0.250 | [+0.00, +0.50] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-small@chunk4 vs octo-small@hist1

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.125 | [-0.33, +0.08] | 0 |
| force_x0.5 | 24 | -0.167 | [-0.33, -0.04] | − |
| fric_x0.4 | 24 | -0.333 | [-0.54, -0.12] | − |
| iso_x0.25 | 24 | -0.250 | [-0.42, -0.08] | − |
| iso_x4.0 | 24 | -0.167 | [-0.33, -0.04] | − |
| nominal | 24 | -0.167 | [-0.33, +0.00] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-small@chunk4 vs octo-small@noens

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.167 | [-0.33, -0.04] | − |
| force_x0.5 | 24 | -0.125 | [-0.29, +0.04] | 0 |
| fric_x0.4 | 24 | -0.125 | [-0.29, +0.04] | 0 |
| iso_x0.25 | 24 | -0.042 | [-0.21, +0.12] | 0 |
| iso_x4.0 | 24 | -0.083 | [-0.29, +0.12] | 0 |
| nominal | 24 | -0.042 | [-0.21, +0.12] | 0 |

### PutSpoonOnTableClothInScene-v1: octo-small@hist1 vs octo-small@noens

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| dens_x0.5 | 24 | -0.042 | [-0.29, +0.21] | 0 |
| force_x0.5 | 24 | +0.042 | [-0.21, +0.29] | 0 |
| fric_x0.4 | 24 | +0.208 | [+0.00, +0.46] | 0 |
| iso_x0.25 | 24 | +0.208 | [+0.00, +0.42] | 0 |
| iso_x4.0 | 24 | +0.083 | [-0.12, +0.33] | 0 |
| nominal | 24 | +0.125 | [-0.12, +0.38] | 0 |

### StackGreenCubeOnYellowCubeBakedTexInScene-v1: octo-base vs octo-small

| condition | paired n | Δ | bootstrap 95% | sign |
|---|---:|---:|---|---|
| damp_x0.25 | 24 | +0.000 | [+0.00, +0.00] | 0 |
| damp_x0.5 | 48 | -0.042 | [-0.10, +0.00] | 0 |
| damp_x2.0 | 48 | +0.000 | [+0.00, +0.00] | 0 |
| damp_x4.0 | 24 | +0.000 | [+0.00, +0.00] | 0 |
| delay_1 | 48 | +0.000 | [+0.00, +0.00] | 0 |
| delay_2 | 24 | +0.000 | [+0.00, +0.00] | 0 |
| force_x0.5 | 48 | +0.000 | [+0.00, +0.00] | 0 |
| iso_x0.25 | 48 | -0.021 | [-0.06, +0.00] | 0 |
| iso_x0.5 | 48 | -0.021 | [-0.06, +0.00] | 0 |
| iso_x2.0 | 48 | -0.021 | [-0.06, +0.00] | 0 |
| iso_x4.0 | 48 | +0.000 | [+0.00, +0.00] | 0 |
| nominal | 48 | +0.000 | [+0.00, +0.00] | 0 |
| stiff_x0.25 | 24 | +0.000 | [+0.00, +0.00] | 0 |
| stiff_x0.5 | 48 | +0.000 | [+0.00, +0.00] | 0 |
| stiff_x2.0 | 48 | +0.000 | [+0.00, +0.00] | 0 |
| stiff_x4.0 | 24 | -0.042 | [-0.12, +0.00] | 0 |

## Point-estimate sign changes across conditions

- **PutCarrotOnPlateInScene-v1** octo-base vs octo-small: Δ by condition {'damp_x0.25': 0.042, 'damp_x0.5': 0.042, 'damp_x2.0': 0.083, 'damp_x4.0': 0.083, 'delay_1': -0.021, 'delay_2': 0.0, 'dens_x0.5': -0.042, 'dens_x2.0': 0.083, 'force_x0.5': 0.0, 'fric_x0.4': 0.042, 'fric_x2.5': 0.042, 'iso_x0.25': 0.021, 'iso_x0.5': 0.062, 'iso_x2.0': 0.062, 'iso_x4.0': 0.0, 'nominal': 0.021, 'stiff_x0.25': -0.083, 'stiff_x0.5': 0.062, 'stiff_x2.0': 0.042, 'stiff_x4.0': 0.042}
- **PutEggplantInBasketScene-v1** octo-base vs octo-base@hist1: Δ by condition {'dens_x0.5': 0.125, 'force_x0.5': -0.083, 'fric_x0.4': 0.083, 'iso_x0.25': 0.125, 'iso_x4.0': -0.083, 'nominal': -0.125}
- **PutEggplantInBasketScene-v1** octo-base vs octo-small@hist1: Δ by condition {'dens_x0.5': -0.042, 'force_x0.5': -0.083, 'fric_x0.4': 0.083, 'iso_x0.25': 0.0, 'iso_x4.0': -0.208, 'nominal': -0.208}
- **PutEggplantInBasketScene-v1** octo-base@chunk4 vs octo-base@noens: Δ by condition {'dens_x0.5': 0.083, 'force_x0.5': -0.208, 'fric_x0.4': -0.25, 'iso_x0.25': 0.0, 'iso_x4.0': -0.042, 'nominal': -0.083}
- **PutEggplantInBasketScene-v1** octo-base@chunk4 vs octo-small@chunk4: Δ by condition {'dens_x0.5': 0.0, 'force_x0.5': -0.083, 'fric_x0.4': -0.167, 'iso_x0.25': 0.042, 'iso_x4.0': -0.042, 'nominal': -0.083}
- **PutEggplantInBasketScene-v1** octo-base@chunk4 vs octo-small@noens: Δ by condition {'dens_x0.5': -0.042, 'force_x0.5': -0.083, 'fric_x0.4': -0.083, 'iso_x0.25': 0.0, 'iso_x4.0': 0.042, 'nominal': -0.083}
- **PutEggplantInBasketScene-v1** octo-base@noens vs octo-small@chunk4: Δ by condition {'dens_x0.5': -0.083, 'force_x0.5': 0.125, 'fric_x0.4': 0.083, 'iso_x0.25': 0.042, 'iso_x4.0': 0.0, 'nominal': 0.0}
- **PutEggplantInBasketScene-v1** octo-base@noens vs octo-small@noens: Δ by condition {'dens_x0.5': -0.125, 'force_x0.5': 0.125, 'fric_x0.4': 0.167, 'iso_x0.25': 0.0, 'iso_x4.0': 0.083, 'nominal': 0.0}
- **PutEggplantInBasketScene-v1** octo-small vs octo-small@hist1: Δ by condition {'dens_x0.5': 0.125, 'force_x0.5': 0.042, 'fric_x0.4': 0.125, 'iso_x0.25': 0.083, 'iso_x4.0': -0.042, 'nominal': 0.083}
- **PutEggplantInBasketScene-v1** octo-small@chunk4 vs octo-small@noens: Δ by condition {'dens_x0.5': -0.042, 'force_x0.5': 0.0, 'fric_x0.4': 0.083, 'iso_x0.25': -0.042, 'iso_x4.0': 0.083, 'nominal': 0.0}
- **PutSpoonOnTableClothInScene-v1** octo-base vs octo-base@chunk4: Δ by condition {'dens_x0.5': -0.042, 'force_x0.5': 0.042, 'fric_x0.4': 0.083, 'iso_x0.25': 0.0, 'iso_x4.0': 0.083, 'nominal': 0.083}
- **PutSpoonOnTableClothInScene-v1** octo-base vs octo-base@noens: Δ by condition {'dens_x0.5': -0.042, 'force_x0.5': 0.0, 'fric_x0.4': 0.0, 'iso_x0.25': 0.0, 'iso_x4.0': 0.083, 'nominal': -0.042}
- **PutSpoonOnTableClothInScene-v1** octo-base vs octo-small@chunk4: Δ by condition {'dens_x0.5': -0.042, 'force_x0.5': 0.0, 'fric_x0.4': 0.042, 'iso_x0.25': -0.083, 'iso_x4.0': 0.042, 'nominal': 0.0}
- **PutSpoonOnTableClothInScene-v1** octo-base@hist1 vs octo-small: Δ by condition {'dens_x0.5': -0.042, 'force_x0.5': -0.125, 'fric_x0.4': 0.042, 'iso_x0.25': -0.083, 'iso_x4.0': 0.0, 'nominal': -0.208}
- **PutSpoonOnTableClothInScene-v1** octo-base@hist1 vs octo-small@hist1: Δ by condition {'dens_x0.5': 0.0, 'force_x0.5': -0.125, 'fric_x0.4': -0.167, 'iso_x0.25': -0.167, 'iso_x4.0': 0.042, 'nominal': -0.083}
- **PutSpoonOnTableClothInScene-v1** octo-base@hist1 vs octo-small@noens: Δ by condition {'dens_x0.5': -0.042, 'force_x0.5': -0.083, 'fric_x0.4': 0.042, 'iso_x0.25': 0.042, 'iso_x4.0': 0.125, 'nominal': 0.042}
- **PutSpoonOnTableClothInScene-v1** octo-base@noens vs octo-small@chunk4: Δ by condition {'dens_x0.5': 0.0, 'force_x0.5': 0.0, 'fric_x0.4': 0.042, 'iso_x0.25': -0.083, 'iso_x4.0': -0.042, 'nominal': 0.042}
- **PutSpoonOnTableClothInScene-v1** octo-small vs octo-small@hist1: Δ by condition {'dens_x0.5': 0.042, 'force_x0.5': 0.0, 'fric_x0.4': -0.208, 'iso_x0.25': -0.083, 'iso_x4.0': 0.042, 'nominal': 0.125}
- **PutSpoonOnTableClothInScene-v1** octo-small@hist1 vs octo-small@noens: Δ by condition {'dens_x0.5': -0.042, 'force_x0.5': 0.042, 'fric_x0.4': 0.208, 'iso_x0.25': 0.208, 'iso_x4.0': 0.083, 'nominal': 0.125}

A point-estimate sign change is *not* a confirmed ranking flip: check the bootstrap intervals above; with 24 paired episodes most differences will be inconclusive.

## Within-policy sensitivity vs nominal (paired)

| policy | env | condition | paired n | rate − nominal | bootstrap 95% |
|---|---|---|---:|---:|---|
| octo-base | PutCarrotOnPlateInScene-v1 | damp_x0.25 | 24 | +0.042 | [+0.00, +0.12] |
| octo-base | PutCarrotOnPlateInScene-v1 | damp_x0.5 | 48 | -0.021 | [-0.10, +0.06] |
| octo-base | PutCarrotOnPlateInScene-v1 | damp_x2.0 | 48 | +0.021 | [-0.10, +0.15] |
| octo-base | PutCarrotOnPlateInScene-v1 | damp_x4.0 | 24 | +0.083 | [-0.08, +0.25] |
| octo-base | PutCarrotOnPlateInScene-v1 | delay_1 | 48 | -0.062 | [-0.17, +0.04] |
| octo-base | PutCarrotOnPlateInScene-v1 | delay_2 | 24 | -0.083 | [-0.21, +0.00] |
| octo-base | PutCarrotOnPlateInScene-v1 | dens_x0.5 | 24 | +0.000 | [+0.00, +0.00] |
| octo-base | PutCarrotOnPlateInScene-v1 | dens_x2.0 | 24 | +0.083 | [+0.00, +0.21] |
| octo-base | PutCarrotOnPlateInScene-v1 | force_x0.5 | 48 | -0.021 | [-0.06, +0.00] |
| octo-base | PutCarrotOnPlateInScene-v1 | fric_x0.4 | 24 | +0.083 | [-0.08, +0.25] |
| octo-base | PutCarrotOnPlateInScene-v1 | fric_x2.5 | 24 | +0.083 | [+0.00, +0.21] |
| octo-base | PutCarrotOnPlateInScene-v1 | iso_x0.25 | 48 | +0.000 | [-0.10, +0.10] |
| octo-base | PutCarrotOnPlateInScene-v1 | iso_x0.5 | 48 | +0.042 | [-0.06, +0.15] |
| octo-base | PutCarrotOnPlateInScene-v1 | iso_x2.0 | 48 | +0.062 | [+0.00, +0.15] |
| octo-base | PutCarrotOnPlateInScene-v1 | iso_x4.0 | 48 | -0.021 | [-0.12, +0.06] |
| octo-base | PutCarrotOnPlateInScene-v1 | stiff_x0.25 | 24 | -0.083 | [-0.21, +0.00] |
| octo-base | PutCarrotOnPlateInScene-v1 | stiff_x0.5 | 48 | +0.000 | [-0.10, +0.12] |
| octo-base | PutCarrotOnPlateInScene-v1 | stiff_x2.0 | 48 | +0.021 | [-0.04, +0.08] |
| octo-base | PutCarrotOnPlateInScene-v1 | stiff_x4.0 | 24 | +0.042 | [+0.00, +0.12] |
| octo-base | PutEggplantInBasketScene-v1 | damp_x0.25 | 24 | +0.167 | [+0.00, +0.38] |
| octo-base | PutEggplantInBasketScene-v1 | damp_x0.5 | 48 | +0.083 | [-0.04, +0.23] |
| octo-base | PutEggplantInBasketScene-v1 | damp_x2.0 | 48 | +0.000 | [-0.15, +0.15] |
| octo-base | PutEggplantInBasketScene-v1 | damp_x4.0 | 24 | -0.125 | [-0.29, +0.04] |
| octo-base | PutEggplantInBasketScene-v1 | delay_1 | 48 | -0.104 | [-0.25, +0.04] |
| octo-base | PutEggplantInBasketScene-v1 | delay_2 | 24 | -0.250 | [-0.42, -0.08] |
| octo-base | PutEggplantInBasketScene-v1 | dens_x0.5 | 96 | +0.021 | [-0.09, +0.14] |
| octo-base | PutEggplantInBasketScene-v1 | dens_x2.0 | 24 | +0.000 | [-0.29, +0.29] |
| octo-base | PutEggplantInBasketScene-v1 | force_x0.5 | 48 | +0.021 | [-0.10, +0.15] |
| octo-base | PutEggplantInBasketScene-v1 | fric_x0.4 | 96 | +0.062 | [-0.03, +0.16] |
| octo-base | PutEggplantInBasketScene-v1 | fric_x2.5 | 24 | +0.000 | [-0.21, +0.21] |
| octo-base | PutEggplantInBasketScene-v1 | iso_x0.25 | 48 | +0.062 | [-0.08, +0.23] |
| octo-base | PutEggplantInBasketScene-v1 | iso_x0.5 | 48 | +0.042 | [-0.08, +0.17] |
| octo-base | PutEggplantInBasketScene-v1 | iso_x2.0 | 48 | +0.083 | [+0.00, +0.19] |
| octo-base | PutEggplantInBasketScene-v1 | iso_x4.0 | 48 | +0.062 | [-0.06, +0.19] |
| octo-base | PutEggplantInBasketScene-v1 | stiff_x0.25 | 24 | -0.167 | [-0.38, +0.00] |
| octo-base | PutEggplantInBasketScene-v1 | stiff_x0.5 | 48 | -0.042 | [-0.19, +0.10] |
| octo-base | PutEggplantInBasketScene-v1 | stiff_x2.0 | 48 | +0.083 | [-0.04, +0.21] |
| octo-base | PutEggplantInBasketScene-v1 | stiff_x4.0 | 24 | +0.083 | [-0.17, +0.33] |
| octo-base | PutSpoonOnTableClothInScene-v1 | damp_x0.25 | 24 | +0.000 | [-0.17, +0.17] |
| octo-base | PutSpoonOnTableClothInScene-v1 | damp_x0.5 | 48 | -0.021 | [-0.10, +0.06] |
| octo-base | PutSpoonOnTableClothInScene-v1 | damp_x2.0 | 48 | +0.000 | [-0.10, +0.10] |
| octo-base | PutSpoonOnTableClothInScene-v1 | damp_x4.0 | 24 | -0.083 | [-0.21, +0.00] |
| octo-base | PutSpoonOnTableClothInScene-v1 | delay_1 | 48 | +0.083 | [-0.04, +0.21] |
| octo-base | PutSpoonOnTableClothInScene-v1 | delay_2 | 24 | +0.083 | [-0.12, +0.29] |
| octo-base | PutSpoonOnTableClothInScene-v1 | dens_x0.5 | 24 | -0.042 | [-0.12, +0.00] |
| octo-base | PutSpoonOnTableClothInScene-v1 | dens_x2.0 | 24 | -0.083 | [-0.21, +0.00] |
| octo-base | PutSpoonOnTableClothInScene-v1 | force_x0.5 | 48 | +0.021 | [+0.00, +0.06] |
| octo-base | PutSpoonOnTableClothInScene-v1 | fric_x0.4 | 24 | +0.000 | [-0.12, +0.12] |
| octo-base | PutSpoonOnTableClothInScene-v1 | fric_x2.5 | 24 | +0.042 | [-0.08, +0.17] |
| octo-base | PutSpoonOnTableClothInScene-v1 | iso_x0.25 | 48 | -0.062 | [-0.17, +0.02] |
| octo-base | PutSpoonOnTableClothInScene-v1 | iso_x0.5 | 48 | -0.062 | [-0.17, +0.02] |
| octo-base | PutSpoonOnTableClothInScene-v1 | iso_x2.0 | 48 | +0.021 | [-0.04, +0.08] |
| octo-base | PutSpoonOnTableClothInScene-v1 | iso_x4.0 | 48 | -0.021 | [-0.12, +0.08] |
| octo-base | PutSpoonOnTableClothInScene-v1 | stiff_x0.25 | 24 | -0.083 | [-0.21, +0.00] |
| octo-base | PutSpoonOnTableClothInScene-v1 | stiff_x0.5 | 48 | +0.000 | [-0.10, +0.12] |
| octo-base | PutSpoonOnTableClothInScene-v1 | stiff_x2.0 | 48 | +0.000 | [-0.12, +0.10] |
| octo-base | PutSpoonOnTableClothInScene-v1 | stiff_x4.0 | 24 | -0.042 | [-0.17, +0.08] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x0.25 | 24 | +0.000 | [+0.00, +0.00] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x0.5 | 48 | +0.000 | [+0.00, +0.00] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x2.0 | 48 | +0.000 | [+0.00, +0.00] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x4.0 | 24 | +0.000 | [+0.00, +0.00] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | delay_1 | 48 | +0.000 | [+0.00, +0.00] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | delay_2 | 24 | +0.000 | [+0.00, +0.00] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | force_x0.5 | 48 | +0.000 | [+0.00, +0.00] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x0.25 | 48 | +0.000 | [+0.00, +0.00] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x0.5 | 48 | +0.000 | [+0.00, +0.00] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x2.0 | 48 | +0.000 | [+0.00, +0.00] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x4.0 | 48 | +0.000 | [+0.00, +0.00] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x0.25 | 24 | +0.000 | [+0.00, +0.00] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x0.5 | 48 | +0.000 | [+0.00, +0.00] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x2.0 | 48 | +0.000 | [+0.00, +0.00] |
| octo-base | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x4.0 | 24 | +0.000 | [+0.00, +0.00] |
| octo-base@chunk4 | PutEggplantInBasketScene-v1 | dens_x0.5 | 24 | +0.125 | [-0.04, +0.29] |
| octo-base@chunk4 | PutEggplantInBasketScene-v1 | force_x0.5 | 24 | +0.042 | [-0.12, +0.21] |
| octo-base@chunk4 | PutEggplantInBasketScene-v1 | fric_x0.4 | 24 | +0.042 | [-0.12, +0.21] |
| octo-base@chunk4 | PutEggplantInBasketScene-v1 | iso_x0.25 | 24 | +0.083 | [-0.12, +0.29] |
| octo-base@chunk4 | PutEggplantInBasketScene-v1 | iso_x4.0 | 24 | +0.083 | [-0.12, +0.29] |
| octo-base@chunk4 | PutSpoonOnTableClothInScene-v1 | dens_x0.5 | 24 | +0.083 | [+0.00, +0.21] |
| octo-base@chunk4 | PutSpoonOnTableClothInScene-v1 | force_x0.5 | 24 | +0.042 | [+0.00, +0.12] |
| octo-base@chunk4 | PutSpoonOnTableClothInScene-v1 | fric_x0.4 | 24 | +0.000 | [+0.00, +0.00] |
| octo-base@chunk4 | PutSpoonOnTableClothInScene-v1 | iso_x0.25 | 24 | +0.000 | [+0.00, +0.00] |
| octo-base@chunk4 | PutSpoonOnTableClothInScene-v1 | iso_x4.0 | 24 | +0.042 | [+0.00, +0.12] |
| octo-base@hist1 | PutEggplantInBasketScene-v1 | dens_x0.5 | 24 | -0.083 | [-0.33, +0.17] |
| octo-base@hist1 | PutEggplantInBasketScene-v1 | force_x0.5 | 24 | +0.083 | [-0.17, +0.29] |
| octo-base@hist1 | PutEggplantInBasketScene-v1 | fric_x0.4 | 24 | +0.000 | [-0.25, +0.25] |
| octo-base@hist1 | PutEggplantInBasketScene-v1 | iso_x0.25 | 24 | -0.125 | [-0.33, +0.08] |
| octo-base@hist1 | PutEggplantInBasketScene-v1 | iso_x4.0 | 24 | +0.083 | [-0.12, +0.33] |
| octo-base@hist1 | PutSpoonOnTableClothInScene-v1 | dens_x0.5 | 24 | +0.042 | [-0.12, +0.21] |
| octo-base@hist1 | PutSpoonOnTableClothInScene-v1 | force_x0.5 | 24 | -0.042 | [-0.12, +0.00] |
| octo-base@hist1 | PutSpoonOnTableClothInScene-v1 | fric_x0.4 | 24 | +0.042 | [-0.08, +0.21] |
| octo-base@hist1 | PutSpoonOnTableClothInScene-v1 | iso_x0.25 | 24 | +0.000 | [-0.21, +0.21] |
| octo-base@hist1 | PutSpoonOnTableClothInScene-v1 | iso_x4.0 | 24 | +0.125 | [-0.04, +0.29] |
| octo-base@noens | PutEggplantInBasketScene-v1 | dens_x0.5 | 24 | -0.042 | [-0.21, +0.12] |
| octo-base@noens | PutEggplantInBasketScene-v1 | force_x0.5 | 24 | +0.167 | [+0.04, +0.33] |
| octo-base@noens | PutEggplantInBasketScene-v1 | fric_x0.4 | 24 | +0.208 | [+0.00, +0.46] |
| octo-base@noens | PutEggplantInBasketScene-v1 | iso_x0.25 | 24 | +0.000 | [-0.21, +0.21] |
| octo-base@noens | PutEggplantInBasketScene-v1 | iso_x4.0 | 24 | +0.042 | [-0.17, +0.25] |
| octo-base@noens | PutSpoonOnTableClothInScene-v1 | dens_x0.5 | 24 | -0.042 | [-0.21, +0.08] |
| octo-base@noens | PutSpoonOnTableClothInScene-v1 | force_x0.5 | 24 | -0.042 | [-0.12, +0.00] |
| octo-base@noens | PutSpoonOnTableClothInScene-v1 | fric_x0.4 | 24 | -0.042 | [-0.21, +0.08] |
| octo-base@noens | PutSpoonOnTableClothInScene-v1 | iso_x0.25 | 24 | -0.125 | [-0.25, +0.00] |
| octo-base@noens | PutSpoonOnTableClothInScene-v1 | iso_x4.0 | 24 | -0.083 | [-0.25, +0.08] |
| octo-small | PutCarrotOnPlateInScene-v1 | damp_x0.25 | 24 | -0.042 | [-0.17, +0.08] |
| octo-small | PutCarrotOnPlateInScene-v1 | damp_x0.5 | 48 | -0.042 | [-0.15, +0.06] |
| octo-small | PutCarrotOnPlateInScene-v1 | damp_x2.0 | 48 | -0.042 | [-0.17, +0.06] |
| octo-small | PutCarrotOnPlateInScene-v1 | damp_x4.0 | 24 | -0.042 | [-0.12, +0.00] |
| octo-small | PutCarrotOnPlateInScene-v1 | delay_1 | 48 | -0.021 | [-0.10, +0.06] |
| octo-small | PutCarrotOnPlateInScene-v1 | delay_2 | 24 | -0.125 | [-0.25, +0.00] |
| octo-small | PutCarrotOnPlateInScene-v1 | dens_x0.5 | 24 | +0.000 | [-0.12, +0.12] |
| octo-small | PutCarrotOnPlateInScene-v1 | dens_x2.0 | 24 | -0.042 | [-0.21, +0.08] |
| octo-small | PutCarrotOnPlateInScene-v1 | force_x0.5 | 48 | +0.000 | [+0.00, +0.00] |
| octo-small | PutCarrotOnPlateInScene-v1 | fric_x0.4 | 24 | +0.000 | [-0.12, +0.12] |
| octo-small | PutCarrotOnPlateInScene-v1 | fric_x2.5 | 24 | +0.000 | [-0.12, +0.12] |
| octo-small | PutCarrotOnPlateInScene-v1 | iso_x0.25 | 48 | -0.042 | [-0.12, +0.04] |
| octo-small | PutCarrotOnPlateInScene-v1 | iso_x0.5 | 48 | -0.062 | [-0.15, +0.02] |
| octo-small | PutCarrotOnPlateInScene-v1 | iso_x2.0 | 48 | +0.021 | [-0.06, +0.10] |
| octo-small | PutCarrotOnPlateInScene-v1 | iso_x4.0 | 48 | +0.062 | [-0.02, +0.17] |
| octo-small | PutCarrotOnPlateInScene-v1 | stiff_x0.25 | 24 | -0.042 | [-0.12, +0.00] |
| octo-small | PutCarrotOnPlateInScene-v1 | stiff_x0.5 | 48 | -0.042 | [-0.17, +0.08] |
| octo-small | PutCarrotOnPlateInScene-v1 | stiff_x2.0 | 48 | +0.000 | [-0.10, +0.10] |
| octo-small | PutCarrotOnPlateInScene-v1 | stiff_x4.0 | 24 | -0.042 | [-0.21, +0.08] |
| octo-small | PutEggplantInBasketScene-v1 | damp_x0.25 | 24 | +0.000 | [-0.25, +0.25] |
| octo-small | PutEggplantInBasketScene-v1 | damp_x0.5 | 48 | -0.062 | [-0.17, +0.02] |
| octo-small | PutEggplantInBasketScene-v1 | damp_x2.0 | 48 | +0.021 | [-0.12, +0.17] |
| octo-small | PutEggplantInBasketScene-v1 | damp_x4.0 | 24 | -0.042 | [-0.29, +0.21] |
| octo-small | PutEggplantInBasketScene-v1 | delay_1 | 48 | -0.021 | [-0.19, +0.15] |
| octo-small | PutEggplantInBasketScene-v1 | delay_2 | 24 | -0.167 | [-0.38, +0.04] |
| octo-small | PutEggplantInBasketScene-v1 | dens_x0.5 | 96 | -0.115 | [-0.21, -0.02] |
| octo-small | PutEggplantInBasketScene-v1 | dens_x2.0 | 24 | +0.000 | [-0.21, +0.21] |
| octo-small | PutEggplantInBasketScene-v1 | force_x0.5 | 48 | -0.062 | [-0.17, +0.04] |
| octo-small | PutEggplantInBasketScene-v1 | fric_x0.4 | 96 | -0.094 | [-0.19, +0.00] |
| octo-small | PutEggplantInBasketScene-v1 | fric_x2.5 | 24 | -0.125 | [-0.38, +0.12] |
| octo-small | PutEggplantInBasketScene-v1 | iso_x0.25 | 48 | -0.104 | [-0.25, +0.04] |
| octo-small | PutEggplantInBasketScene-v1 | iso_x0.5 | 48 | +0.021 | [-0.08, +0.12] |
| octo-small | PutEggplantInBasketScene-v1 | iso_x2.0 | 48 | -0.021 | [-0.15, +0.10] |
| octo-small | PutEggplantInBasketScene-v1 | iso_x4.0 | 48 | +0.042 | [-0.10, +0.19] |
| octo-small | PutEggplantInBasketScene-v1 | stiff_x0.25 | 24 | -0.375 | [-0.58, -0.21] |
| octo-small | PutEggplantInBasketScene-v1 | stiff_x0.5 | 48 | +0.083 | [-0.08, +0.25] |
| octo-small | PutEggplantInBasketScene-v1 | stiff_x2.0 | 48 | -0.021 | [-0.15, +0.10] |
| octo-small | PutEggplantInBasketScene-v1 | stiff_x4.0 | 24 | +0.000 | [-0.21, +0.25] |
| octo-small | PutSpoonOnTableClothInScene-v1 | damp_x0.25 | 24 | -0.250 | [-0.50, +0.00] |
| octo-small | PutSpoonOnTableClothInScene-v1 | damp_x0.5 | 48 | -0.167 | [-0.31, -0.02] |
| octo-small | PutSpoonOnTableClothInScene-v1 | damp_x2.0 | 48 | -0.083 | [-0.25, +0.08] |
| octo-small | PutSpoonOnTableClothInScene-v1 | damp_x4.0 | 24 | -0.167 | [-0.38, +0.04] |
| octo-small | PutSpoonOnTableClothInScene-v1 | delay_1 | 48 | -0.208 | [-0.35, -0.06] |
| octo-small | PutSpoonOnTableClothInScene-v1 | delay_2 | 24 | -0.208 | [-0.46, +0.04] |
| octo-small | PutSpoonOnTableClothInScene-v1 | dens_x0.5 | 24 | -0.125 | [-0.29, +0.00] |
| octo-small | PutSpoonOnTableClothInScene-v1 | dens_x2.0 | 24 | -0.208 | [-0.38, -0.04] |
| octo-small | PutSpoonOnTableClothInScene-v1 | force_x0.5 | 48 | -0.042 | [-0.12, +0.04] |
| octo-small | PutSpoonOnTableClothInScene-v1 | fric_x0.4 | 24 | -0.208 | [-0.42, +0.00] |
| octo-small | PutSpoonOnTableClothInScene-v1 | fric_x2.5 | 24 | -0.083 | [-0.29, +0.12] |
| octo-small | PutSpoonOnTableClothInScene-v1 | iso_x0.25 | 48 | -0.125 | [-0.25, +0.00] |
| octo-small | PutSpoonOnTableClothInScene-v1 | iso_x0.5 | 48 | -0.021 | [-0.15, +0.10] |
| octo-small | PutSpoonOnTableClothInScene-v1 | iso_x2.0 | 48 | -0.125 | [-0.27, +0.00] |
| octo-small | PutSpoonOnTableClothInScene-v1 | iso_x4.0 | 48 | +0.000 | [-0.12, +0.10] |
| octo-small | PutSpoonOnTableClothInScene-v1 | stiff_x0.25 | 24 | -0.208 | [-0.42, +0.04] |
| octo-small | PutSpoonOnTableClothInScene-v1 | stiff_x0.5 | 48 | -0.042 | [-0.21, +0.12] |
| octo-small | PutSpoonOnTableClothInScene-v1 | stiff_x2.0 | 48 | -0.083 | [-0.27, +0.10] |
| octo-small | PutSpoonOnTableClothInScene-v1 | stiff_x4.0 | 24 | -0.250 | [-0.46, -0.04] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x0.25 | 24 | +0.000 | [+0.00, +0.00] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x0.5 | 48 | +0.042 | [+0.00, +0.10] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x2.0 | 48 | +0.000 | [+0.00, +0.00] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | damp_x4.0 | 24 | +0.000 | [+0.00, +0.00] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | delay_1 | 48 | +0.000 | [+0.00, +0.00] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | delay_2 | 24 | +0.000 | [+0.00, +0.00] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | force_x0.5 | 48 | +0.000 | [+0.00, +0.00] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x0.25 | 48 | +0.021 | [+0.00, +0.06] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x0.5 | 48 | +0.021 | [+0.00, +0.06] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x2.0 | 48 | +0.021 | [+0.00, +0.06] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | iso_x4.0 | 48 | +0.000 | [+0.00, +0.00] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x0.25 | 24 | +0.000 | [+0.00, +0.00] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x0.5 | 48 | +0.000 | [+0.00, +0.00] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x2.0 | 48 | +0.000 | [+0.00, +0.00] |
| octo-small | StackGreenCubeOnYellowCubeBakedTexInScene-v1 | stiff_x4.0 | 24 | +0.042 | [+0.00, +0.12] |
| octo-small@chunk4 | PutEggplantInBasketScene-v1 | dens_x0.5 | 24 | +0.042 | [-0.17, +0.25] |
| octo-small@chunk4 | PutEggplantInBasketScene-v1 | force_x0.5 | 24 | +0.042 | [-0.21, +0.29] |
| octo-small@chunk4 | PutEggplantInBasketScene-v1 | fric_x0.4 | 24 | +0.125 | [-0.08, +0.33] |
| octo-small@chunk4 | PutEggplantInBasketScene-v1 | iso_x0.25 | 24 | -0.042 | [-0.21, +0.12] |
| octo-small@chunk4 | PutEggplantInBasketScene-v1 | iso_x4.0 | 24 | +0.042 | [-0.21, +0.29] |
| octo-small@chunk4 | PutSpoonOnTableClothInScene-v1 | dens_x0.5 | 24 | +0.000 | [-0.12, +0.12] |
| octo-small@chunk4 | PutSpoonOnTableClothInScene-v1 | force_x0.5 | 24 | +0.000 | [+0.00, +0.00] |
| octo-small@chunk4 | PutSpoonOnTableClothInScene-v1 | fric_x0.4 | 24 | -0.042 | [-0.17, +0.08] |
| octo-small@chunk4 | PutSpoonOnTableClothInScene-v1 | iso_x0.25 | 24 | +0.000 | [-0.12, +0.12] |
| octo-small@chunk4 | PutSpoonOnTableClothInScene-v1 | iso_x4.0 | 24 | +0.000 | [-0.12, +0.12] |
| octo-small@hist1 | PutEggplantInBasketScene-v1 | dens_x0.5 | 24 | +0.000 | [-0.12, +0.12] |
| octo-small@hist1 | PutEggplantInBasketScene-v1 | force_x0.5 | 24 | +0.000 | [-0.12, +0.12] |
| octo-small@hist1 | PutEggplantInBasketScene-v1 | fric_x0.4 | 24 | -0.083 | [-0.29, +0.12] |
| octo-small@hist1 | PutEggplantInBasketScene-v1 | iso_x0.25 | 24 | -0.083 | [-0.25, +0.08] |
| octo-small@hist1 | PutEggplantInBasketScene-v1 | iso_x4.0 | 24 | +0.125 | [-0.04, +0.29] |
| octo-small@hist1 | PutSpoonOnTableClothInScene-v1 | dens_x0.5 | 24 | -0.042 | [-0.21, +0.12] |
| octo-small@hist1 | PutSpoonOnTableClothInScene-v1 | force_x0.5 | 24 | +0.000 | [-0.17, +0.17] |
| octo-small@hist1 | PutSpoonOnTableClothInScene-v1 | fric_x0.4 | 24 | +0.125 | [-0.12, +0.38] |
| octo-small@hist1 | PutSpoonOnTableClothInScene-v1 | iso_x0.25 | 24 | +0.083 | [-0.12, +0.29] |
| octo-small@hist1 | PutSpoonOnTableClothInScene-v1 | iso_x4.0 | 24 | +0.000 | [-0.21, +0.21] |
| octo-small@noens | PutEggplantInBasketScene-v1 | dens_x0.5 | 24 | +0.083 | [+0.00, +0.21] |
| octo-small@noens | PutEggplantInBasketScene-v1 | force_x0.5 | 24 | +0.042 | [-0.12, +0.21] |
| octo-small@noens | PutEggplantInBasketScene-v1 | fric_x0.4 | 24 | +0.042 | [-0.12, +0.21] |
| octo-small@noens | PutEggplantInBasketScene-v1 | iso_x0.25 | 24 | +0.000 | [-0.17, +0.17] |
| octo-small@noens | PutEggplantInBasketScene-v1 | iso_x4.0 | 24 | -0.042 | [-0.17, +0.08] |
| octo-small@noens | PutSpoonOnTableClothInScene-v1 | dens_x0.5 | 24 | +0.125 | [+0.00, +0.25] |
| octo-small@noens | PutSpoonOnTableClothInScene-v1 | force_x0.5 | 24 | +0.083 | [+0.00, +0.21] |
| octo-small@noens | PutSpoonOnTableClothInScene-v1 | fric_x0.4 | 24 | +0.042 | [-0.08, +0.17] |
| octo-small@noens | PutSpoonOnTableClothInScene-v1 | iso_x0.25 | 24 | +0.000 | [-0.12, +0.12] |
| octo-small@noens | PutSpoonOnTableClothInScene-v1 | iso_x4.0 | 24 | +0.042 | [-0.12, +0.21] |
