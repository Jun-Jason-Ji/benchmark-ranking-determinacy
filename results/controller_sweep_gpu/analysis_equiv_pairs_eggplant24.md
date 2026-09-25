# Calibration-equivalent condition pairs vs policy outcomes

Pairs are indistinguishable by free-space demo replay (max trajectory difference < 0.1 mm over 40 demos). Paired by episode_id; bootstrap 95% intervals. Exploratory ManiSkill3/Windows platform.

## PutEggplantInBasketScene-v1

### Within-policy: success(A) − success(B) for calibration-equivalent A, B

| policy | pair | n | rate A | rate B | diff | 95% |
|---|---|---:|---:|---:|---:|---|
| octo-small | stiff_x2.0 vs damp_x0.5 (k/d ratio 2) | 24 | 0.542 | 0.500 | +0.042 | [-0.08, +0.21] |
| octo-small | stiff_x0.5 vs damp_x2.0 (k/d ratio 0.5) | 24 | 0.583 | 0.625 | -0.042 | [-0.21, +0.12] |
| octo-small | force_x0.5 vs nominal (force limit inactive) | 24 | 0.500 | 0.542 | -0.042 | [-0.17, +0.08] |
| octo-small | iso_x0.25 vs nominal (iso scale 0.25) | 24 | 0.458 | 0.542 | -0.083 | [-0.29, +0.17] |
| octo-small | iso_x0.5 vs nominal (iso scale 0.5) | 24 | 0.583 | 0.542 | +0.042 | [-0.12, +0.21] |
| octo-small | iso_x2.0 vs nominal (iso scale 2) | 20 | 0.500 | 0.600 | -0.100 | [-0.25, +0.00] |
| octo-base | stiff_x2.0 vs damp_x0.5 (k/d ratio 2) | 24 | 0.458 | 0.375 | +0.083 | [-0.08, +0.25] |
| octo-base | stiff_x0.5 vs damp_x2.0 (k/d ratio 0.5) | 24 | 0.333 | 0.292 | +0.042 | [-0.12, +0.21] |
| octo-base | force_x0.5 vs nominal (force limit inactive) | 24 | 0.375 | 0.250 | +0.125 | [-0.04, +0.29] |
| octo-base | iso_x0.25 vs nominal (iso scale 0.25) | 24 | 0.375 | 0.250 | +0.125 | [-0.12, +0.38] |
| octo-base | iso_x0.5 vs nominal (iso scale 0.5) | 24 | 0.333 | 0.250 | +0.083 | [-0.08, +0.25] |
| octo-base | iso_x2.0 vs nominal (iso scale 2) | 10 | 0.400 | 0.300 | +0.100 | [+0.00, +0.30] |

### Between-policy Δ = small − base under each member of the pair

| pair | n | Δ under A | 95% | Δ under B | 95% | Δ(A) − Δ(B) | 95% | sign pattern |
|---|---:|---:|---|---:|---|---:|---|---|
| stiff_x2.0 vs damp_x0.5 (k/d ratio 2) | 24 | +0.083 | [-0.12, +0.25] | +0.125 | [-0.08, +0.38] | -0.042 | [-0.25, +0.17] | 0/0 |
| stiff_x0.5 vs damp_x2.0 (k/d ratio 0.5) | 24 | +0.250 | [+0.00, +0.50] | +0.333 | [+0.04, +0.62] | -0.083 | [-0.33, +0.17] | 0/+ |
| force_x0.5 vs nominal (force limit inactive) | 24 | +0.125 | [-0.12, +0.38] | +0.292 | [+0.08, +0.50] | -0.167 | [-0.42, +0.08] | 0/+ |
| iso_x0.25 vs nominal (iso scale 0.25) | 24 | +0.083 | [-0.17, +0.33] | +0.292 | [+0.08, +0.50] | -0.208 | [-0.50, +0.08] | 0/+ |
| iso_x0.5 vs nominal (iso scale 0.5) | 24 | +0.250 | [+0.00, +0.50] | +0.292 | [+0.08, +0.50] | -0.042 | [-0.29, +0.21] | 0/+ |
| iso_x2.0 vs nominal (iso scale 2) | 10 | +0.300 | [+0.10, +0.60] | +0.292 | [+0.08, +0.50] | -0.100 | [-0.30, +0.00] | +/+ |

## CI-supported ranking flips across calibration-equivalent pairs

None so far.