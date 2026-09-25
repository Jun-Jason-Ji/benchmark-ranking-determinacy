# Eggplant near-tied set: two seed sets (episodes 0-47)

Original seeds 20260918+ep (`results/controller_sweep_gpu`), replication seeds 20270101+ep (`results/controller_sweep_gpu_rep`). Δ = rate(A) − rate(B), paired by episode_id, 95% paired bootstrap. Sign column: CI-supported sign. 'replicated' = both sets CI-supported with the same sign. Duplicate records: first wins.

## Single-policy rates

| policy | condition | n_orig | orig | n_rep | rep |
|---|---|---:|---:|---:|---:|
| octo-small | nominal | 48 | 0.521 | 48 | 0.500 |
| octo-small | iso_x0.25 | 48 | 0.417 | 0 | nan |
| octo-small | iso_x4.0 | 48 | 0.562 | 0 | nan |
| octo-small | force_x0.5 | 48 | 0.458 | 0 | nan |
| octo-small | fric_x0.4 | 48 | 0.438 | 48 | 0.500 |
| octo-small | dens_x0.5 | 48 | 0.500 | 0 | nan |
| octo-base | nominal | 48 | 0.292 | 48 | 0.500 |
| octo-base | iso_x0.25 | 48 | 0.354 | 48 | 0.438 |
| octo-base | iso_x4.0 | 48 | 0.354 | 48 | 0.500 |
| octo-base | force_x0.5 | 48 | 0.312 | 48 | 0.417 |
| octo-base | fric_x0.4 | 48 | 0.458 | 48 | 0.417 |
| octo-base | dens_x0.5 | 48 | 0.396 | 48 | 0.417 |
| octo-small@hist1 | nominal | 48 | 0.375 | 0 | nan |
| octo-small@hist1 | iso_x0.25 | 48 | 0.312 | 0 | nan |
| octo-small@hist1 | iso_x4.0 | 48 | 0.438 | 0 | nan |
| octo-small@hist1 | force_x0.5 | 48 | 0.375 | 0 | nan |
| octo-small@hist1 | fric_x0.4 | 48 | 0.333 | 0 | nan |
| octo-small@hist1 | dens_x0.5 | 48 | 0.396 | 0 | nan |
| octo-base@hist1 | nominal | 48 | 0.375 | 48 | 0.292 |
| octo-base@hist1 | iso_x0.25 | 48 | 0.250 | 48 | 0.292 |
| octo-base@hist1 | iso_x4.0 | 48 | 0.396 | 48 | 0.396 |
| octo-base@hist1 | force_x0.5 | 48 | 0.354 | 48 | 0.250 |
| octo-base@hist1 | fric_x0.4 | 48 | 0.333 | 48 | 0.354 |
| octo-base@hist1 | dens_x0.5 | 48 | 0.229 | 48 | 0.396 |

## Pairs

### octo-small vs octo-base

| condition | n | Δ orig | 95% | sign | Δ rep | 95% | sign | Δ pooled | 95% | verdict |
|---|---:|---:|---|---|---:|---|---|---:|---|---|
| nominal | 48+48 | +0.229 | [+0.06, +0.40] | + | +0.000 | [-0.19, +0.19] | 0 | +0.115 | [-0.01, +0.24] | one set only |
| iso_x0.25 | 0 | | | | | | | | | incomplete |
| iso_x4.0 | 0 | | | | | | | | | incomplete |
| force_x0.5 | 0 | | | | | | | | | incomplete |
| fric_x0.4 | 48+48 | -0.021 | [-0.21, +0.17] | 0 | +0.083 | [-0.12, +0.29] | 0 | +0.031 | [-0.10, +0.17] | undecided in both |
| dens_x0.5 | 0 | | | | | | | | | incomplete |

### octo-small vs octo-small@hist1

| condition | n | Δ orig | 95% | sign | Δ rep | 95% | sign | Δ pooled | 95% | verdict |
|---|---:|---:|---|---|---:|---|---|---:|---|---|
| nominal | 0 | | | | | | | | | incomplete |
| iso_x0.25 | 0 | | | | | | | | | incomplete |
| iso_x4.0 | 0 | | | | | | | | | incomplete |
| force_x0.5 | 0 | | | | | | | | | incomplete |
| fric_x0.4 | 0 | | | | | | | | | incomplete |
| dens_x0.5 | 0 | | | | | | | | | incomplete |

### octo-small vs octo-base@hist1

| condition | n | Δ orig | 95% | sign | Δ rep | 95% | sign | Δ pooled | 95% | verdict |
|---|---:|---:|---|---|---:|---|---|---:|---|---|
| nominal | 48+48 | +0.146 | [-0.04, +0.33] | 0 | +0.208 | [+0.06, +0.35] | + | +0.177 | [+0.06, +0.29] | one set only |
| iso_x0.25 | 0 | | | | | | | | | incomplete |
| iso_x4.0 | 0 | | | | | | | | | incomplete |
| force_x0.5 | 0 | | | | | | | | | incomplete |
| fric_x0.4 | 48+48 | +0.104 | [-0.06, +0.27] | 0 | +0.146 | [-0.02, +0.31] | 0 | +0.125 | [+0.00, +0.24] | undecided in both |
| dens_x0.5 | 0 | | | | | | | | | incomplete |

### octo-base vs octo-small@hist1

| condition | n | Δ orig | 95% | sign | Δ rep | 95% | sign | Δ pooled | 95% | verdict |
|---|---:|---:|---|---|---:|---|---|---:|---|---|
| nominal | 0 | | | | | | | | | incomplete |
| iso_x0.25 | 0 | | | | | | | | | incomplete |
| iso_x4.0 | 0 | | | | | | | | | incomplete |
| force_x0.5 | 0 | | | | | | | | | incomplete |
| fric_x0.4 | 0 | | | | | | | | | incomplete |
| dens_x0.5 | 0 | | | | | | | | | incomplete |

### octo-base vs octo-base@hist1

| condition | n | Δ orig | 95% | sign | Δ rep | 95% | sign | Δ pooled | 95% | verdict |
|---|---:|---:|---|---|---:|---|---|---:|---|---|
| nominal | 48+48 | -0.083 | [-0.27, +0.10] | 0 | +0.208 | [+0.06, +0.35] | + | +0.062 | [-0.06, +0.19] | one set only |
| iso_x0.25 | 48+48 | +0.104 | [-0.04, +0.25] | 0 | +0.146 | [+0.00, +0.29] | 0 | +0.125 | [+0.01, +0.23] | undecided in both |
| iso_x4.0 | 48+48 | -0.042 | [-0.21, +0.12] | 0 | +0.104 | [-0.06, +0.27] | 0 | +0.031 | [-0.09, +0.16] | undecided in both |
| force_x0.5 | 48+48 | -0.042 | [-0.21, +0.12] | 0 | +0.167 | [+0.00, +0.33] | 0 | +0.062 | [-0.06, +0.18] | undecided in both |
| fric_x0.4 | 48+48 | +0.125 | [-0.02, +0.29] | 0 | +0.062 | [-0.12, +0.25] | 0 | +0.094 | [-0.03, +0.22] | undecided in both |
| dens_x0.5 | 48+48 | +0.167 | [+0.00, +0.33] | 0 | +0.021 | [-0.15, +0.17] | 0 | +0.094 | [-0.02, +0.21] | undecided in both |

### octo-small@hist1 vs octo-base@hist1

| condition | n | Δ orig | 95% | sign | Δ rep | 95% | sign | Δ pooled | 95% | verdict |
|---|---:|---:|---|---|---:|---|---|---:|---|---|
| nominal | 0 | | | | | | | | | incomplete |
| iso_x0.25 | 0 | | | | | | | | | incomplete |
| iso_x4.0 | 0 | | | | | | | | | incomplete |
| force_x0.5 | 0 | | | | | | | | | incomplete |
| fric_x0.4 | 0 | | | | | | | | | incomplete |
| dens_x0.5 | 0 | | | | | | | | | incomplete |

## Summary

- CI-supported and replicated (same sign in both seed sets): 0
- CI-supported in both sets with opposite signs: 0
