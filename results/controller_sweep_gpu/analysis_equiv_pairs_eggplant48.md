# Calibration-equivalent condition pairs vs policy outcomes

Pairs are indistinguishable by free-space demo replay (max trajectory difference < 0.1 mm over 40 demos). Paired by episode_id; bootstrap 95% intervals. Exploratory ManiSkill3/Windows platform.

## PutEggplantInBasketScene-v1

### Within-policy: success(A) − success(B) for calibration-equivalent A, B

| policy | pair | n | rate A | rate B | diff | 95% |
|---|---|---:|---:|---:|---:|---|
| octo-small | stiff_x2.0 vs damp_x0.5 (k/d ratio 2) | 48 | 0.500 | 0.458 | +0.042 | [-0.06, +0.15] |
| octo-small | stiff_x0.5 vs damp_x2.0 (k/d ratio 0.5) | 48 | 0.604 | 0.542 | +0.062 | [-0.06, +0.19] |
| octo-small | force_x0.5 vs nominal (force limit inactive) | 48 | 0.458 | 0.521 | -0.062 | [-0.17, +0.04] |
| octo-small | iso_x0.25 vs nominal (iso scale 0.25) | 24 | 0.458 | 0.542 | -0.083 | [-0.29, +0.17] |
| octo-small | iso_x0.5 vs nominal (iso scale 0.5) | 24 | 0.583 | 0.542 | +0.042 | [-0.12, +0.21] |
| octo-small | iso_x2.0 vs nominal (iso scale 2) | 24 | 0.500 | 0.542 | -0.042 | [-0.21, +0.12] |
| octo-small | iso_x4.0 vs nominal (iso scale 4) | 24 | 0.542 | 0.542 | +0.000 | [-0.17, +0.17] |
| octo-base | stiff_x2.0 vs damp_x0.5 (k/d ratio 2) | 48 | 0.375 | 0.375 | +0.000 | [-0.12, +0.10] |
| octo-base | stiff_x0.5 vs damp_x2.0 (k/d ratio 0.5) | 48 | 0.250 | 0.292 | -0.042 | [-0.17, +0.06] |
| octo-base | force_x0.5 vs nominal (force limit inactive) | 48 | 0.312 | 0.292 | +0.021 | [-0.10, +0.15] |
| octo-base | iso_x0.25 vs nominal (iso scale 0.25) | 24 | 0.375 | 0.250 | +0.125 | [-0.12, +0.38] |
| octo-base | iso_x0.5 vs nominal (iso scale 0.5) | 24 | 0.333 | 0.250 | +0.083 | [-0.08, +0.25] |
| octo-base | iso_x2.0 vs nominal (iso scale 2) | 24 | 0.375 | 0.250 | +0.125 | [+0.00, +0.25] |
| octo-base | iso_x4.0 vs nominal (iso scale 4) | 24 | 0.375 | 0.250 | +0.125 | [-0.04, +0.29] |

### Between-policy Δ = small − base under each member of the pair

| pair | n | Δ under A | 95% | Δ under B | 95% | Δ(A) − Δ(B) | 95% | sign pattern |
|---|---:|---:|---|---:|---|---:|---|---|
| stiff_x2.0 vs damp_x0.5 (k/d ratio 2) | 48 | +0.125 | [-0.02, +0.27] | +0.083 | [-0.10, +0.27] | +0.042 | [-0.10, +0.19] | 0/0 |
| stiff_x0.5 vs damp_x2.0 (k/d ratio 0.5) | 48 | +0.354 | [+0.17, +0.52] | +0.250 | [+0.06, +0.44] | +0.104 | [-0.08, +0.29] | +/+ |
| force_x0.5 vs nominal (force limit inactive) | 48 | +0.146 | [-0.02, +0.31] | +0.229 | [+0.06, +0.40] | -0.083 | [-0.27, +0.10] | 0/+ |
| iso_x0.25 vs nominal (iso scale 0.25) | 24 | +0.083 | [-0.17, +0.33] | +0.229 | [+0.06, +0.40] | -0.208 | [-0.50, +0.08] | 0/+ |
| iso_x0.5 vs nominal (iso scale 0.5) | 24 | +0.250 | [+0.00, +0.50] | +0.229 | [+0.06, +0.40] | -0.042 | [-0.29, +0.21] | 0/+ |
| iso_x2.0 vs nominal (iso scale 2) | 24 | +0.125 | [-0.08, +0.33] | +0.229 | [+0.06, +0.40] | -0.167 | [-0.38, +0.04] | 0/+ |
| iso_x4.0 vs nominal (iso scale 4) | 24 | +0.167 | [-0.12, +0.42] | +0.229 | [+0.06, +0.40] | -0.125 | [-0.38, +0.12] | 0/+ |

## CI-supported ranking flips across calibration-equivalent pairs

None so far.