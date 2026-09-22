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
| octo-base | force_x0.5 vs nominal (force limit inactive) | 47 | 0.128 | 0.149 | -0.021 | [-0.06, +0.00] |

### Between-policy Δ = small − base under each member of the pair

| pair | n | Δ under A | 95% | Δ under B | 95% | Δ(A) − Δ(B) | 95% | sign pattern |
|---|---:|---:|---|---:|---|---:|---|---|
| stiff_x2.0 vs damp_x0.5 (k/d ratio 2) | 48 | -0.042 | [-0.15, +0.06] | -0.042 | [-0.15, +0.06] | +0.000 | [-0.12, +0.12] | 0/0 |
| stiff_x0.5 vs damp_x2.0 (k/d ratio 0.5) | 48 | -0.062 | [-0.19, +0.06] | -0.083 | [-0.23, +0.06] | +0.021 | [-0.12, +0.15] | 0/0 |
| force_x0.5 vs nominal (force limit inactive) | 47 | +0.000 | [-0.13, +0.11] | -0.021 | [-0.15, +0.10] | +0.021 | [+0.00, +0.06] | 0/0 |

## CI-supported ranking flips across calibration-equivalent pairs

None so far.