# Deployment-variant policy pairs (same 24 episode_ids per condition)

Policies: octo-base, octo-base@chunk4, octo-base@hist1, octo-base@noens, octo-small, octo-small@chunk4, octo-small@hist1, octo-small@noens. Near-tied = |Δ| ≤ 0.1 at nominal with both rates in [0.2, 0.8].

## PutEggplantInBasketScene-v1

### Nominal success rates

| policy | n | rate |
|---|---:|---:|
| octo-base | 24 | 0.250 |
| octo-base@chunk4 | 24 | 0.083 |
| octo-base@hist1 | 24 | 0.375 |
| octo-base@noens | 24 | 0.167 |
| octo-small | 24 | 0.542 |
| octo-small@chunk4 | 24 | 0.167 |
| octo-small@hist1 | 24 | 0.458 |
| octo-small@noens | 24 | 0.167 |

### All pairs at nominal (Δ = rate(A) − rate(B), paired)

| A | B | n | Δ | 95% | near-tied |
|---|---|---:|---:|---|---|
| octo-base | octo-base@chunk4 | 24 | +0.167 | [+0.00, +0.38] |  |
| octo-base | octo-base@hist1 | 24 | -0.125 | [-0.38, +0.12] |  |
| octo-base | octo-base@noens | 24 | +0.083 | [-0.12, +0.29] |  |
| octo-base | octo-small | 24 | -0.292 | [-0.50, -0.08] |  |
| octo-base | octo-small@chunk4 | 24 | +0.083 | [-0.17, +0.33] |  |
| octo-base | octo-small@hist1 | 24 | -0.208 | [-0.46, +0.00] |  |
| octo-base | octo-small@noens | 24 | +0.083 | [-0.08, +0.25] |  |
| octo-base@chunk4 | octo-base@hist1 | 24 | -0.292 | [-0.50, -0.08] |  |
| octo-base@chunk4 | octo-base@noens | 24 | -0.083 | [-0.25, +0.08] |  |
| octo-base@chunk4 | octo-small | 24 | -0.458 | [-0.67, -0.21] |  |
| octo-base@chunk4 | octo-small@chunk4 | 24 | -0.083 | [-0.29, +0.12] |  |
| octo-base@chunk4 | octo-small@hist1 | 24 | -0.375 | [-0.58, -0.17] |  |
| octo-base@chunk4 | octo-small@noens | 24 | -0.083 | [-0.21, +0.00] |  |
| octo-base@hist1 | octo-base@noens | 24 | +0.208 | [+0.00, +0.46] |  |
| octo-base@hist1 | octo-small | 24 | -0.167 | [-0.46, +0.12] |  |
| octo-base@hist1 | octo-small@chunk4 | 24 | +0.208 | [-0.04, +0.46] |  |
| octo-base@hist1 | octo-small@hist1 | 24 | -0.083 | [-0.33, +0.17] | yes |
| octo-base@hist1 | octo-small@noens | 24 | +0.208 | [-0.04, +0.46] |  |
| octo-base@noens | octo-small | 24 | -0.375 | [-0.58, -0.17] |  |
| octo-base@noens | octo-small@chunk4 | 24 | +0.000 | [-0.25, +0.21] |  |
| octo-base@noens | octo-small@hist1 | 24 | -0.292 | [-0.50, -0.12] |  |
| octo-base@noens | octo-small@noens | 24 | +0.000 | [-0.21, +0.21] |  |
| octo-small | octo-small@chunk4 | 24 | +0.375 | [+0.08, +0.62] |  |
| octo-small | octo-small@hist1 | 24 | +0.083 | [-0.17, +0.33] | yes |
| octo-small | octo-small@noens | 24 | +0.375 | [+0.17, +0.58] |  |
| octo-small@chunk4 | octo-small@hist1 | 24 | -0.292 | [-0.54, -0.04] |  |
| octo-small@chunk4 | octo-small@noens | 24 | +0.000 | [-0.21, +0.25] |  |
| octo-small@hist1 | octo-small@noens | 24 | +0.292 | [+0.04, +0.54] |  |

### Near-tied pairs under calibration-invisible conditions (2 pairs)

#### octo-base@hist1 vs octo-small@hist1

| condition | n | Δ | 95% | sign |
|---|---:|---:|---|---|
| nominal | 24 | -0.083 | [-0.33, +0.17] | 0 |
| iso_x0.25 | 24 | -0.125 | [-0.38, +0.12] | 0 |
| iso_x4.0 | 24 | -0.125 | [-0.38, +0.12] | 0 |
| force_x0.5 | 24 | +0.000 | [-0.21, +0.21] | 0 |
| fric_x0.4 | 24 | +0.000 | [-0.29, +0.29] | 0 |
| dens_x0.5 | 24 | -0.167 | [-0.42, +0.08] | 0 |

#### octo-small vs octo-small@hist1

| condition | n | Δ | 95% | sign |
|---|---:|---:|---|---|
| nominal | 24 | +0.083 | [-0.17, +0.33] | 0 |
| iso_x0.25 | 24 | +0.083 | [-0.17, +0.33] | 0 |
| iso_x4.0 | 24 | -0.042 | [-0.29, +0.21] | 0 |
| force_x0.5 | 24 | +0.042 | [-0.21, +0.29] | 0 |
| fric_x0.4 | 24 | +0.125 | [-0.12, +0.38] | 0 |
| dens_x0.5 | 24 | +0.125 | [-0.12, +0.38] | 0 |

point-estimate sign change across conditions for octo-small vs octo-small@hist1: { nominal: +0.08, iso_x0.25: +0.08, iso_x4.0: -0.04, force_x0.5: +0.04, fric_x0.4: +0.12, dens_x0.5: +0.12 }

### CI-supported sign flips among near-tied pairs

None.

## PutSpoonOnTableClothInScene-v1

### Nominal success rates

| policy | n | rate |
|---|---:|---:|
| octo-base | 24 | 0.083 |
| octo-base@noens | 24 | 0.125 |
| octo-small | 24 | 0.375 |
| octo-small@chunk4 | 24 | 0.083 |
| octo-small@hist1 | 24 | 0.250 |
| octo-small@noens | 24 | 0.125 |

### All pairs at nominal (Δ = rate(A) − rate(B), paired)

| A | B | n | Δ | 95% | near-tied |
|---|---|---:|---:|---|---|
| octo-base | octo-base@noens | 24 | -0.042 | [-0.21, +0.08] |  |
| octo-base | octo-small | 24 | -0.292 | [-0.50, -0.12] |  |
| octo-base | octo-small@chunk4 | 24 | +0.000 | [-0.17, +0.17] |  |
| octo-base | octo-small@hist1 | 24 | -0.167 | [-0.38, +0.00] |  |
| octo-base | octo-small@noens | 24 | -0.042 | [-0.21, +0.12] |  |
| octo-base@noens | octo-small | 24 | -0.250 | [-0.42, -0.08] |  |
| octo-base@noens | octo-small@chunk4 | 24 | +0.042 | [-0.12, +0.21] |  |
| octo-base@noens | octo-small@hist1 | 24 | -0.125 | [-0.33, +0.08] |  |
| octo-base@noens | octo-small@noens | 24 | +0.000 | [-0.17, +0.17] |  |
| octo-small | octo-small@chunk4 | 24 | +0.292 | [+0.04, +0.54] |  |
| octo-small | octo-small@hist1 | 24 | +0.125 | [-0.04, +0.29] |  |
| octo-small | octo-small@noens | 24 | +0.250 | [+0.00, +0.50] |  |
| octo-small@chunk4 | octo-small@hist1 | 24 | -0.167 | [-0.38, +0.00] |  |
| octo-small@chunk4 | octo-small@noens | 24 | -0.042 | [-0.21, +0.12] |  |
| octo-small@hist1 | octo-small@noens | 24 | +0.125 | [-0.12, +0.38] |  |

### Near-tied pairs under calibration-invisible conditions (0 pairs)

### CI-supported sign flips among near-tied pairs

None.
