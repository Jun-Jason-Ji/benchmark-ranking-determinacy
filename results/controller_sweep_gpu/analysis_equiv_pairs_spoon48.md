# Calibration-equivalent condition pairs vs policy outcomes

Pairs are indistinguishable by free-space demo replay (max trajectory difference < 0.1 mm over 40 demos). Paired by episode_id; bootstrap 95% intervals. Exploratory ManiSkill3/Windows platform.

## PutSpoonOnTableClothInScene-v1

### Within-policy: success(A) − success(B) for calibration-equivalent A, B

| policy | pair | n | rate A | rate B | diff | 95% |
|---|---|---:|---:|---:|---:|---|
| octo-small | stiff_x2.0 vs damp_x0.5 (k/d ratio 2) | 48 | 0.292 | 0.208 | +0.083 | [-0.04, +0.21] |
| octo-small | stiff_x0.5 vs damp_x2.0 (k/d ratio 0.5) | 48 | 0.333 | 0.292 | +0.042 | [-0.10, +0.19] |
| octo-small | force_x0.5 vs nominal (force limit inactive) | 48 | 0.333 | 0.375 | -0.042 | [-0.12, +0.04] |
| octo-small | iso_x0.25 vs nominal (iso scale 0.25) | 24 | 0.250 | 0.375 | -0.125 | [-0.25, +0.00] |
| octo-small | iso_x0.5 vs nominal (iso scale 0.5) | 24 | 0.208 | 0.375 | -0.167 | [-0.33, +0.00] |
| octo-small | iso_x2.0 vs nominal (iso scale 2) | 24 | 0.250 | 0.375 | -0.125 | [-0.33, +0.08] |
| octo-small | iso_x4.0 vs nominal (iso scale 4) | 24 | 0.292 | 0.375 | -0.083 | [-0.25, +0.08] |
| octo-base | stiff_x2.0 vs damp_x0.5 (k/d ratio 2) | 48 | 0.083 | 0.062 | +0.021 | [-0.04, +0.08] |
| octo-base | stiff_x0.5 vs damp_x2.0 (k/d ratio 0.5) | 48 | 0.083 | 0.083 | +0.000 | [-0.08, +0.08] |
| octo-base | force_x0.5 vs nominal (force limit inactive) | 48 | 0.104 | 0.083 | +0.021 | [+0.00, +0.06] |
| octo-base | iso_x0.25 vs nominal (iso scale 0.25) | 24 | 0.000 | 0.083 | -0.083 | [-0.21, +0.00] |
| octo-base | iso_x0.5 vs nominal (iso scale 0.5) | 24 | 0.000 | 0.083 | -0.083 | [-0.21, +0.00] |
| octo-base | iso_x2.0 vs nominal (iso scale 2) | 24 | 0.083 | 0.083 | +0.000 | [-0.12, +0.12] |
| octo-base | iso_x4.0 vs nominal (iso scale 4) | 24 | 0.125 | 0.083 | +0.042 | [-0.12, +0.21] |

### Between-policy Δ = small − base under each member of the pair

| pair | n | Δ under A | 95% | Δ under B | 95% | Δ(A) − Δ(B) | 95% | sign pattern |
|---|---:|---:|---|---:|---|---:|---|---|
| stiff_x2.0 vs damp_x0.5 (k/d ratio 2) | 48 | +0.208 | [+0.06, +0.35] | +0.146 | [+0.04, +0.27] | +0.062 | [-0.08, +0.21] | +/+ |
| stiff_x0.5 vs damp_x2.0 (k/d ratio 0.5) | 48 | +0.250 | [+0.10, +0.40] | +0.208 | [+0.06, +0.35] | +0.042 | [-0.12, +0.21] | +/+ |
| force_x0.5 vs nominal (force limit inactive) | 48 | +0.229 | [+0.10, +0.35] | +0.292 | [+0.15, +0.44] | -0.062 | [-0.17, +0.02] | +/+ |
| iso_x0.25 vs nominal (iso scale 0.25) | 24 | +0.250 | [+0.08, +0.42] | +0.292 | [+0.15, +0.44] | -0.042 | [-0.17, +0.08] | +/+ |
| iso_x0.5 vs nominal (iso scale 0.5) | 24 | +0.208 | [+0.04, +0.38] | +0.292 | [+0.15, +0.44] | -0.083 | [-0.25, +0.08] | +/+ |
| iso_x2.0 vs nominal (iso scale 2) | 24 | +0.167 | [+0.00, +0.33] | +0.292 | [+0.15, +0.44] | -0.125 | [-0.33, +0.08] | 0/+ |
| iso_x4.0 vs nominal (iso scale 4) | 24 | +0.167 | [-0.04, +0.38] | +0.292 | [+0.15, +0.44] | -0.125 | [-0.33, +0.08] | 0/+ |

## CI-supported ranking flips across calibration-equivalent pairs

None so far.