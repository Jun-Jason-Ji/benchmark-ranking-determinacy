# Calibration-equivalent condition pairs vs policy outcomes

Pairs are indistinguishable by free-space demo replay (max trajectory difference < 0.1 mm over 40 demos). Paired by episode_id; bootstrap 95% intervals. Exploratory ManiSkill3/Windows platform.

## PutEggplantInBasketScene-v1

### Within-policy: success(A) − success(B) for calibration-equivalent A, B

| policy | pair | n | rate A | rate B | diff | 95% |
|---|---|---:|---:|---:|---:|---|
| octo-small | stiff_x2.0 vs damp_x0.5 (k/d ratio 2) | 48 | 0.500 | 0.458 | +0.042 | [-0.06, +0.15] |
| octo-small | stiff_x0.5 vs damp_x2.0 (k/d ratio 0.5) | 48 | 0.604 | 0.542 | +0.062 | [-0.06, +0.19] |
| octo-small | force_x0.5 vs nominal (force limit inactive) | 48 | 0.458 | 0.521 | -0.062 | [-0.17, +0.04] |
| octo-small | iso_x0.25 vs nominal (iso scale 0.25) | 48 | 0.417 | 0.521 | -0.104 | [-0.25, +0.04] |
| octo-small | iso_x0.5 vs nominal (iso scale 0.5) | 48 | 0.542 | 0.521 | +0.021 | [-0.08, +0.12] |
| octo-small | iso_x2.0 vs nominal (iso scale 2) | 48 | 0.500 | 0.521 | -0.021 | [-0.15, +0.10] |
| octo-small | iso_x4.0 vs nominal (iso scale 4) | 48 | 0.562 | 0.521 | +0.042 | [-0.10, +0.19] |
| octo-small | fric_x0.4 vs nominal (object friction 0.2) | 96 | 0.490 | 0.583 | -0.094 | [-0.19, +0.00] |
| octo-small | fric_x2.5 vs nominal (object friction 1.25) | 24 | 0.417 | 0.542 | -0.125 | [-0.38, +0.12] |
| octo-small | dens_x0.5 vs nominal (object density x0.5) | 96 | 0.469 | 0.583 | -0.115 | [-0.21, -0.02] |
| octo-small | dens_x2.0 vs nominal (object density x2) | 24 | 0.542 | 0.542 | +0.000 | [-0.21, +0.21] |
| octo-base | stiff_x2.0 vs damp_x0.5 (k/d ratio 2) | 48 | 0.375 | 0.375 | +0.000 | [-0.12, +0.10] |
| octo-base | stiff_x0.5 vs damp_x2.0 (k/d ratio 0.5) | 48 | 0.250 | 0.292 | -0.042 | [-0.17, +0.06] |
| octo-base | force_x0.5 vs nominal (force limit inactive) | 48 | 0.312 | 0.292 | +0.021 | [-0.10, +0.15] |
| octo-base | iso_x0.25 vs nominal (iso scale 0.25) | 48 | 0.354 | 0.292 | +0.062 | [-0.08, +0.23] |
| octo-base | iso_x0.5 vs nominal (iso scale 0.5) | 48 | 0.333 | 0.292 | +0.042 | [-0.08, +0.17] |
| octo-base | iso_x2.0 vs nominal (iso scale 2) | 48 | 0.375 | 0.292 | +0.083 | [+0.00, +0.19] |
| octo-base | iso_x4.0 vs nominal (iso scale 4) | 48 | 0.354 | 0.292 | +0.062 | [-0.06, +0.19] |
| octo-base | fric_x0.4 vs nominal (object friction 0.2) | 96 | 0.438 | 0.375 | +0.062 | [-0.03, +0.16] |
| octo-base | fric_x2.5 vs nominal (object friction 1.25) | 24 | 0.250 | 0.250 | +0.000 | [-0.21, +0.21] |
| octo-base | dens_x0.5 vs nominal (object density x0.5) | 78 | 0.385 | 0.321 | +0.064 | [-0.06, +0.19] |
| octo-base | dens_x2.0 vs nominal (object density x2) | 24 | 0.250 | 0.250 | +0.000 | [-0.29, +0.29] |

### Between-policy Δ = small − base under each member of the pair

| pair | n | Δ under A | 95% | Δ under B | 95% | Δ(A) − Δ(B) | 95% | sign pattern |
|---|---:|---:|---|---:|---|---:|---|---|
| stiff_x2.0 vs damp_x0.5 (k/d ratio 2) | 48 | +0.125 | [-0.02, +0.27] | +0.083 | [-0.10, +0.27] | +0.042 | [-0.10, +0.19] | 0/0 |
| stiff_x0.5 vs damp_x2.0 (k/d ratio 0.5) | 48 | +0.354 | [+0.17, +0.52] | +0.250 | [+0.06, +0.44] | +0.104 | [-0.08, +0.29] | +/+ |
| force_x0.5 vs nominal (force limit inactive) | 48 | +0.146 | [-0.02, +0.31] | +0.208 | [+0.09, +0.32] | -0.083 | [-0.27, +0.10] | 0/+ |
| iso_x0.25 vs nominal (iso scale 0.25) | 48 | +0.062 | [-0.10, +0.23] | +0.208 | [+0.09, +0.32] | -0.167 | [-0.40, +0.04] | 0/+ |
| iso_x0.5 vs nominal (iso scale 0.5) | 48 | +0.208 | [+0.04, +0.38] | +0.208 | [+0.09, +0.32] | -0.021 | [-0.19, +0.15] | +/+ |
| iso_x2.0 vs nominal (iso scale 2) | 48 | +0.125 | [-0.02, +0.27] | +0.208 | [+0.09, +0.32] | -0.104 | [-0.25, +0.04] | 0/+ |
| iso_x4.0 vs nominal (iso scale 4) | 48 | +0.208 | [+0.02, +0.40] | +0.208 | [+0.09, +0.32] | -0.021 | [-0.23, +0.21] | +/+ |
| fric_x0.4 vs nominal (object friction 0.2) | 96 | +0.052 | [-0.07, +0.18] | +0.208 | [+0.09, +0.32] | -0.156 | [-0.29, -0.03] | 0/+ |
| fric_x2.5 vs nominal (object friction 1.25) | 24 | +0.167 | [-0.04, +0.38] | +0.208 | [+0.09, +0.32] | -0.125 | [-0.42, +0.17] | 0/+ |
| dens_x0.5 vs nominal (object density x0.5) | 78 | +0.064 | [-0.06, +0.19] | +0.208 | [+0.09, +0.32] | -0.179 | [-0.32, -0.04] | 0/+ |
| dens_x2.0 vs nominal (object density x2) | 24 | +0.292 | [+0.00, +0.54] | +0.208 | [+0.09, +0.32] | +0.000 | [-0.38, +0.38] | 0/+ |

## CI-supported ranking flips across calibration-equivalent pairs

None so far.