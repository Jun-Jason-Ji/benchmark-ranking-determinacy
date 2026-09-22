# Calibration-equivalent condition pairs vs policy outcomes

Pairs are indistinguishable by free-space demo replay (max trajectory difference < 0.1 mm over 40 demos). Paired by episode_id; bootstrap 95% intervals. Exploratory ManiSkill3/Windows platform.

## PutCarrotOnPlateInScene-v1

### Within-policy: success(A) − success(B) for calibration-equivalent A, B

| policy | pair | n | rate A | rate B | diff | 95% |
|---|---|---:|---:|---:|---:|---|
| octo-small | stiff_x2.0 vs damp_x0.5 (k/d ratio 2) | 48 | 0.125 | 0.083 | +0.042 | [-0.04, +0.12] |
| octo-small | stiff_x0.5 vs damp_x2.0 (k/d ratio 0.5) | 48 | 0.083 | 0.083 | +0.000 | [-0.08, +0.08] |
| octo-small | force_x0.5 vs nominal (force limit inactive) | 48 | 0.125 | 0.125 | +0.000 | [+0.00, +0.00] |
| octo-base | stiff_x2.0 vs damp_x0.5 (k/d ratio 2) | 48 | 0.167 | 0.125 | +0.042 | [-0.04, +0.12] |
| octo-base | stiff_x0.5 vs damp_x2.0 (k/d ratio 0.5) | 48 | 0.146 | 0.167 | -0.021 | [-0.10, +0.06] |
| octo-base | force_x0.5 vs nominal (force limit inactive) | 48 | 0.125 | 0.146 | -0.021 | [-0.06, +0.00] |

### Between-policy Δ = small − base under each member of the pair

| pair | n | Δ under A | 95% | Δ under B | 95% | Δ(A) − Δ(B) | 95% | sign pattern |
|---|---:|---:|---|---:|---|---:|---|---|
| stiff_x2.0 vs damp_x0.5 (k/d ratio 2) | 48 | -0.042 | [-0.15, +0.06] | -0.042 | [-0.15, +0.06] | +0.000 | [-0.12, +0.12] | 0/0 |
| stiff_x0.5 vs damp_x2.0 (k/d ratio 0.5) | 48 | -0.062 | [-0.19, +0.06] | -0.083 | [-0.23, +0.06] | +0.021 | [-0.12, +0.15] | 0/0 |
| force_x0.5 vs nominal (force limit inactive) | 48 | +0.000 | [-0.12, +0.12] | -0.021 | [-0.15, +0.10] | +0.021 | [+0.00, +0.06] | 0/0 |

## PutSpoonOnTableClothInScene-v1

### Within-policy: success(A) − success(B) for calibration-equivalent A, B

| policy | pair | n | rate A | rate B | diff | 95% |
|---|---|---:|---:|---:|---:|---|
| octo-small | stiff_x2.0 vs damp_x0.5 (k/d ratio 2) | 24 | 0.333 | 0.250 | +0.083 | [-0.12, +0.29] |
| octo-small | stiff_x0.5 vs damp_x2.0 (k/d ratio 0.5) | 24 | 0.208 | 0.208 | +0.000 | [-0.21, +0.21] |
| octo-small | force_x0.5 vs nominal (force limit inactive) | 24 | 0.250 | 0.375 | -0.125 | [-0.25, +0.00] |
| octo-base | stiff_x2.0 vs damp_x0.5 (k/d ratio 2) | 24 | 0.042 | 0.083 | -0.042 | [-0.12, +0.00] |
| octo-base | stiff_x0.5 vs damp_x2.0 (k/d ratio 0.5) | 24 | 0.125 | 0.042 | +0.083 | [+0.00, +0.21] |
| octo-base | force_x0.5 vs nominal (force limit inactive) | 24 | 0.083 | 0.083 | +0.000 | [+0.00, +0.00] |

### Between-policy Δ = small − base under each member of the pair

| pair | n | Δ under A | 95% | Δ under B | 95% | Δ(A) − Δ(B) | 95% | sign pattern |
|---|---:|---:|---|---:|---|---:|---|---|
| stiff_x2.0 vs damp_x0.5 (k/d ratio 2) | 24 | +0.292 | [+0.12, +0.50] | +0.167 | [+0.00, +0.33] | +0.125 | [-0.08, +0.33] | +/0 |
| stiff_x0.5 vs damp_x2.0 (k/d ratio 0.5) | 24 | +0.083 | [-0.12, +0.29] | +0.167 | [+0.00, +0.38] | -0.083 | [-0.29, +0.12] | 0/0 |
| force_x0.5 vs nominal (force limit inactive) | 24 | +0.167 | [+0.00, +0.38] | +0.292 | [+0.12, +0.46] | -0.125 | [-0.25, +0.00] | 0/+ |

## CI-supported ranking flips across calibration-equivalent pairs

None so far.