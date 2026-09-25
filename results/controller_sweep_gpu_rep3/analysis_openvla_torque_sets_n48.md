# Torque x0.5 × OpenVLA: 4 seed sets / stacks, episodes < 48

Sets: A = `results/controller_sweep_gpu`; B = `results/controller_sweep_gpu_rep`; C = `results/controller_sweep_gpu_rep3`; A-ms2 = `results/controller_sweep_ms2`. Paired bootstrap (20000) on common episode_ids; first record wins. Decision = 95% CI of Δ excludes 0. 'n' = paired episodes actually available (a cell is skipped if any side is missing).

## 1. Single-policy paired change, force_x0.5 − nominal

| policy | A nominal | A force | A change [95%] | B nominal | B force | B change [95%] | C nominal | C force | C change [95%] | A-ms2 nominal | A-ms2 force | A-ms2 change [95%] |
|---|---:|---:|---|---:|---:|---|---:|---:|---|---:|---:|---|
| openvla-7b-4bit | 0.146 (7/48) | 0.312 (15/48) | +0.167 [+0.02, +0.31] | 0.146 (7/48) | 0.333 (16/48) | +0.188 [+0.04, +0.33] | 0.146 (7/48) | 0.375 (18/48) | +0.229 [+0.08, +0.38] | – | – | – |
| octo-small | 0.521 (25/48) | 0.458 (22/48) | -0.062 [-0.17, +0.04] | 0.500 (24/48) | 0.521 (25/48) | +0.021 [-0.08, +0.12] | 0.200 (1/5) | 0.200 (1/5) | +0.000 [+0.00, +0.00] | 0.438 (21/48) | 0.479 (23/48) | +0.042 [-0.04, +0.12] |
| octo-base | 0.292 (14/48) | 0.312 (15/48) | +0.021 [-0.10, +0.17] | 0.500 (24/48) | 0.417 (20/48) | -0.083 [-0.25, +0.08] | – | – | – | 0.375 (18/48) | 0.354 (17/48) | -0.021 [-0.10, +0.06] |
| octo-small@hist1 | 0.375 (18/48) | 0.375 (18/48) | +0.000 [-0.08, +0.08] | 0.521 (25/48) | 0.396 (19/48) | -0.125 [-0.23, -0.02] | – | – | – | – | – | – |
| octo-base@hist1 | 0.375 (18/48) | 0.354 (17/48) | -0.021 [-0.19, +0.15] | 0.292 (14/48) | 0.250 (12/48) | -0.042 [-0.21, +0.12] | – | – | – | – | – | – |

## 2. Pairs Δ = Octo − OpenVLA

| pair | set | n | Δ nominal [95%] | decision | Δ force_x0.5 [95%] | decision | Δ change [95%] | change supported |
|---|---|---:|---|---|---|---|---|---|
| octo-small vs OpenVLA | A | 48 | +0.375 [+0.19, +0.54] | Octo> | +0.146 [-0.04, +0.33] | abstain | -0.229 [-0.42, -0.04] | yes |
| octo-small vs OpenVLA | B | 48 | +0.354 [+0.17, +0.54] | Octo> | +0.188 [-0.02, +0.40] | abstain | -0.167 [-0.33, +0.00] | no |
| octo-small vs OpenVLA | C | 5 | +0.000 [-0.60, +0.60] | abstain | -0.600 [-1.00, +0.20] | abstain | -0.600 [-1.00, -0.20] | yes |
| octo-small vs OpenVLA | A-ms2 | 0 | – | – | – | – | – | – |
| octo-small vs OpenVLA | pooled | 101 | | | | | -0.218 [-0.35, -0.09] | yes |
| octo-base vs OpenVLA | A | 48 | +0.146 [-0.02, +0.31] | abstain | +0.000 [-0.19, +0.19] | abstain | -0.146 [-0.33, +0.06] | no |
| octo-base vs OpenVLA | B | 48 | +0.354 [+0.17, +0.54] | Octo> | +0.083 [-0.10, +0.29] | abstain | -0.271 [-0.50, -0.04] | yes |
| octo-base vs OpenVLA | C | 0 | – | – | – | – | – | – |
| octo-base vs OpenVLA | A-ms2 | 0 | – | – | – | – | – | – |
| octo-base vs OpenVLA | pooled | 96 | | | | | -0.208 [-0.36, -0.05] | yes |
| octo-small@hist1 vs OpenVLA | A | 48 | +0.229 [+0.06, +0.40] | Octo> | +0.062 [-0.12, +0.25] | abstain | -0.167 [-0.33, +0.00] | no |
| octo-small@hist1 vs OpenVLA | B | 48 | +0.375 [+0.19, +0.54] | Octo> | +0.062 [-0.15, +0.27] | abstain | -0.312 [-0.48, -0.15] | yes |
| octo-small@hist1 vs OpenVLA | C | 0 | – | – | – | – | – | – |
| octo-small@hist1 vs OpenVLA | A-ms2 | 0 | – | – | – | – | – | – |
| octo-small@hist1 vs OpenVLA | pooled | 96 | | | | | -0.240 [-0.36, -0.11] | yes |
| octo-base@hist1 vs OpenVLA | A | 48 | +0.229 [+0.08, +0.38] | Octo> | +0.042 [-0.15, +0.23] | abstain | -0.188 [-0.44, +0.06] | no |
| octo-base@hist1 vs OpenVLA | B | 48 | +0.146 [-0.02, +0.31] | abstain | -0.083 [-0.27, +0.10] | abstain | -0.229 [-0.46, +0.00] | no |
| octo-base@hist1 vs OpenVLA | C | 0 | – | – | – | – | – | – |
| octo-base@hist1 vs OpenVLA | A-ms2 | 0 | – | – | – | – | – | – |
| octo-base@hist1 vs OpenVLA | pooled | 96 | | | | | -0.208 [-0.38, -0.04] | yes |

## 3. Across-set verdicts

- **octo-small vs OpenVLA** (3 sets): decidable→abstain in 2/3 [A: Octo>→abstain, B: Octo>→abstain, C: abstain→abstain]; sign flip in 0/3; Δ-change CI-supported in 2/3; pooled Δ change -0.218 [-0.35, -0.09].
- **octo-base vs OpenVLA** (2 sets): decidable→abstain in 1/2 [A: abstain→abstain, B: Octo>→abstain]; sign flip in 0/2; Δ-change CI-supported in 1/2; pooled Δ change -0.208 [-0.36, -0.05].
- **octo-small@hist1 vs OpenVLA** (2 sets): decidable→abstain in 2/2 [A: Octo>→abstain, B: Octo>→abstain]; sign flip in 0/2; Δ-change CI-supported in 1/2; pooled Δ change -0.240 [-0.36, -0.11].
- **octo-base@hist1 vs OpenVLA** (2 sets): decidable→abstain in 1/2 [A: Octo>→abstain, B: abstain→abstain]; sign flip in 0/2; Δ-change CI-supported in 0/2; pooled Δ change -0.208 [-0.38, -0.04].
- **OpenVLA single-policy torque effect**: CI-supported positive in 3/3 sets (A, B, C); Octo policies CI-supported in 1/11 cells.
