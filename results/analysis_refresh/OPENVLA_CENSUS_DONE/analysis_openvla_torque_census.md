# Torque x0.5 × OpenVLA: 4 runs / stacks, episodes < 64

Sets: A = `results/controller_sweep_gpu`; B = `results/controller_sweep_gpu_rep`; C = `results/controller_sweep_gpu_rep3`; A-ms2 = `results/controller_sweep_ms2`. Paired bootstrap (20000) on common episode_ids; first record wins. Decision = 95% CI of Δ excludes 0. 'n' = paired episodes actually available (a cell is skipped if any side is missing).

**Config census.** `PutEggplantInBasketScene-v1` has 64 distinct initial configurations (`PutEggplantInBasketScene-v0`: 24); episode_id beyond that repeats a configuration exactly. OpenVLA is deterministic (`do_sample=False`, the per-episode seed is ignored), so for it the labelled sets are **re-runs of one configuration, not independent seed sets**, and repeated configs are dropped here; Octo samples its diffusion head from the per-episode seed, so its sets are genuine replicates. See `FINDING_seed_set_bug.md`.

## 0. Coverage

| set | policy | condition | episodes kept | distinct configs | census |
|---|---|---|---:|---:|---|
| A | openvla-7b-4bit | nominal | 64 | 64 | 64/64 **complete** |
| A | openvla-7b-4bit | force_x0.5 | 64 | 64 | 64/64 **complete** |
| A | octo-small | nominal | 64 | 64 | 64/64 **complete** |
| A | octo-small | force_x0.5 | 64 | 64 | 64/64 **complete** |
| A | octo-base | nominal | 64 | 64 | 64/64 **complete** |
| A | octo-base | force_x0.5 | 64 | 64 | 64/64 **complete** |
| A | octo-small@hist1 | nominal | 64 | 64 | 64/64 **complete** |
| A | octo-small@hist1 | force_x0.5 | 64 | 64 | 64/64 **complete** |
| A | octo-base@hist1 | nominal | 64 | 64 | 64/64 **complete** |
| A | octo-base@hist1 | force_x0.5 | 64 | 64 | 64/64 **complete** |
| B | openvla-7b-4bit | nominal | 48 | 48 | 48/64 |
| B | openvla-7b-4bit | force_x0.5 | 48 | 48 | 48/64 |
| B | octo-small | nominal | 64 | 64 | 64/64 **complete** |
| B | octo-small | force_x0.5 | 64 | 64 | 64/64 **complete** |
| B | octo-base | nominal | 64 | 64 | 64/64 **complete** |
| B | octo-base | force_x0.5 | 64 | 64 | 64/64 **complete** |
| B | octo-small@hist1 | nominal | 64 | 64 | 64/64 **complete** |
| B | octo-small@hist1 | force_x0.5 | 64 | 64 | 64/64 **complete** |
| B | octo-base@hist1 | nominal | 64 | 64 | 64/64 **complete** |
| B | octo-base@hist1 | force_x0.5 | 64 | 64 | 64/64 **complete** |
| C | openvla-7b-4bit | nominal | 48 | 48 | 48/64 |
| C | openvla-7b-4bit | force_x0.5 | 48 | 48 | 48/64 |
| C | octo-small | nominal | 64 | 64 | 64/64 **complete** |
| C | octo-small | force_x0.5 | 64 | 64 | 64/64 **complete** |
| C | octo-base | nominal | 64 | 64 | 64/64 **complete** |
| C | octo-base | force_x0.5 | 64 | 64 | 64/64 **complete** |
| C | octo-small@hist1 | nominal | 64 | 64 | 64/64 **complete** |
| C | octo-small@hist1 | force_x0.5 | 64 | 64 | 64/64 **complete** |
| C | octo-base@hist1 | nominal | 64 | 64 | 64/64 **complete** |
| C | octo-base@hist1 | force_x0.5 | 64 | 64 | 64/64 **complete** |
| A-ms2 | openvla-7b-4bit | nominal | 24 | 24 | 24/24 **complete** |
| A-ms2 | openvla-7b-4bit | force_x0.5 | 24 | 24 | 24/24 **complete** |
| A-ms2 | octo-small | nominal | 48 | 24 | 24/24 **complete** |
| A-ms2 | octo-small | force_x0.5 | 48 | 24 | 24/24 **complete** |
| A-ms2 | octo-base | nominal | 48 | 24 | 24/24 **complete** |
| A-ms2 | octo-base | force_x0.5 | 48 | 24 | 24/24 **complete** |

## 1. Single-policy paired change, force_x0.5 − nominal

| policy | A nominal | A force | A change [95%] | B nominal | B force | B change [95%] | C nominal | C force | C change [95%] | A-ms2 nominal | A-ms2 force | A-ms2 change [95%] |
|---|---:|---:|---|---:|---:|---|---:|---:|---|---:|---:|---|
| openvla-7b-4bit | 0.156 (10/64) | 0.250 (16/64) | +0.094 [-0.03, +0.22] | 0.146 (7/48) | 0.333 (16/48) | +0.188 [+0.04, +0.33] | 0.146 (7/48) | 0.375 (18/48) | +0.229 [+0.08, +0.38] | 0.000 (0/24) | 0.042 (1/24) | +0.042 [+0.00, +0.12] |
| octo-small | 0.547 (35/64) | 0.484 (31/64) | -0.062 [-0.16, +0.02] | 0.484 (31/64) | 0.500 (32/64) | +0.016 [-0.09, +0.11] | 0.453 (29/64) | 0.406 (26/64) | -0.047 [-0.16, +0.06] | 0.438 (21/48) | 0.479 (23/48) | +0.042 [-0.04, +0.12] |
| octo-base | 0.297 (19/64) | 0.297 (19/64) | +0.000 [-0.12, +0.12] | 0.516 (33/64) | 0.391 (25/64) | -0.125 [-0.27, +0.03] | 0.500 (32/64) | 0.453 (29/64) | -0.047 [-0.16, +0.06] | 0.375 (18/48) | 0.354 (17/48) | -0.021 [-0.10, +0.06] |
| octo-small@hist1 | 0.406 (26/64) | 0.375 (24/64) | -0.031 [-0.11, +0.05] | 0.484 (31/64) | 0.375 (24/64) | -0.109 [-0.22, +0.00] | 0.391 (25/64) | 0.375 (24/64) | -0.016 [-0.12, +0.08] | – | – | – |
| octo-base@hist1 | 0.359 (23/64) | 0.312 (20/64) | -0.047 [-0.19, +0.09] | 0.344 (22/64) | 0.297 (19/64) | -0.047 [-0.19, +0.09] | 0.391 (25/64) | 0.375 (24/64) | -0.016 [-0.14, +0.11] | – | – | – |

## 2. Pairs Δ = Octo − OpenVLA

| pair | set | n | Δ nominal [95%] | decision | Δ force_x0.5 [95%] | decision | Δ change [95%] | change supported |
|---|---|---:|---|---|---|---|---|---|
| octo-small vs OpenVLA | A | 64 | +0.391 [+0.23, +0.55] | Octo> | +0.234 [+0.06, +0.41] | Octo> | -0.156 [-0.31, +0.00] | no |
| octo-small vs OpenVLA | B | 48 | +0.354 [+0.17, +0.54] | Octo> | +0.188 [-0.02, +0.40] | abstain | -0.167 [-0.35, +0.00] | no |
| octo-small vs OpenVLA | C | 48 | +0.312 [+0.12, +0.50] | Octo> | -0.021 [-0.23, +0.21] | abstain | -0.333 [-0.52, -0.15] | yes |
| octo-small vs OpenVLA | A-ms2 | 24 | +0.458 [+0.25, +0.67] | Octo> | +0.542 [+0.33, +0.75] | Octo> | +0.083 [-0.08, +0.25] | no |
| octo-small vs OpenVLA | pooled | 184 | | | | | -0.174 [-0.27, -0.08] | yes |
| octo-base vs OpenVLA | A | 64 | +0.141 [+0.00, +0.30] | abstain | +0.047 [-0.09, +0.19] | abstain | -0.094 [-0.27, +0.08] | no |
| octo-base vs OpenVLA | B | 48 | +0.354 [+0.17, +0.54] | Octo> | +0.083 [-0.12, +0.29] | abstain | -0.271 [-0.50, -0.04] | yes |
| octo-base vs OpenVLA | C | 48 | +0.417 [+0.25, +0.58] | Octo> | +0.125 [-0.06, +0.31] | abstain | -0.292 [-0.50, -0.08] | yes |
| octo-base vs OpenVLA | A-ms2 | 24 | +0.375 [+0.21, +0.58] | Octo> | +0.250 [+0.08, +0.42] | Octo> | -0.125 [-0.25, +0.00] | no |
| octo-base vs OpenVLA | pooled | 184 | | | | | -0.196 [-0.30, -0.09] | yes |
| octo-small@hist1 vs OpenVLA | A | 64 | +0.250 [+0.09, +0.41] | Octo> | +0.125 [-0.03, +0.28] | abstain | -0.125 [-0.27, +0.02] | no |
| octo-small@hist1 vs OpenVLA | B | 48 | +0.375 [+0.19, +0.54] | Octo> | +0.062 [-0.15, +0.27] | abstain | -0.312 [-0.50, -0.15] | yes |
| octo-small@hist1 vs OpenVLA | C | 48 | +0.229 [+0.04, +0.42] | Octo> | +0.021 [-0.19, +0.25] | abstain | -0.208 [-0.40, -0.02] | yes |
| octo-small@hist1 vs OpenVLA | A-ms2 | 0 | – | – | – | – | – | – |
| octo-small@hist1 vs OpenVLA | pooled | 160 | | | | | -0.206 [-0.30, -0.11] | yes |
| octo-base@hist1 vs OpenVLA | A | 64 | +0.203 [+0.06, +0.34] | Octo> | +0.062 [-0.09, +0.22] | abstain | -0.141 [-0.34, +0.06] | no |
| octo-base@hist1 vs OpenVLA | B | 48 | +0.146 [-0.02, +0.31] | abstain | -0.083 [-0.27, +0.10] | abstain | -0.229 [-0.46, +0.00] | no |
| octo-base@hist1 vs OpenVLA | C | 48 | +0.292 [+0.10, +0.48] | Octo> | +0.042 [-0.15, +0.23] | abstain | -0.250 [-0.42, -0.06] | yes |
| octo-base@hist1 vs OpenVLA | A-ms2 | 0 | – | – | – | – | – | – |
| octo-base@hist1 vs OpenVLA | pooled | 160 | | | | | -0.200 [-0.32, -0.08] | yes |

## 3. Across-set verdicts

- **octo-small vs OpenVLA** (4 sets): decidable→abstain in 2/4 [A: Octo>→Octo>, B: Octo>→abstain, C: Octo>→abstain, A-ms2: Octo>→Octo>]; sign flip in 0/4; Δ-change CI-supported in 1/4; pooled Δ change -0.174 [-0.27, -0.08].
- **octo-base vs OpenVLA** (4 sets): decidable→abstain in 2/4 [A: abstain→abstain, B: Octo>→abstain, C: Octo>→abstain, A-ms2: Octo>→Octo>]; sign flip in 0/4; Δ-change CI-supported in 2/4; pooled Δ change -0.196 [-0.30, -0.09].
- **octo-small@hist1 vs OpenVLA** (3 sets): decidable→abstain in 3/3 [A: Octo>→abstain, B: Octo>→abstain, C: Octo>→abstain]; sign flip in 0/3; Δ-change CI-supported in 2/3; pooled Δ change -0.206 [-0.30, -0.11].
- **octo-base@hist1 vs OpenVLA** (3 sets): decidable→abstain in 2/3 [A: Octo>→abstain, B: abstain→abstain, C: Octo>→abstain]; sign flip in 0/3; Δ-change CI-supported in 1/3; pooled Δ change -0.200 [-0.32, -0.08].
- **OpenVLA single-policy torque effect**: CI-supported positive in 2/4 sets (B, C); Octo policies CI-supported in 0/14 cells.

## 4. Run-to-run nondeterminism (OpenVLA, identical configuration)

Same env configs, same deterministic policy: any disagreement is GPU/run nondeterminism, not sampling.

| condition | run pair | common eps | success agreement | rate difference |
|---|---|---:|---:|---:|
| nominal | A vs B | 48 | 42/48 (0.875) | +0.000 |
| nominal | A vs C | 48 | 42/48 (0.875) | +0.000 |
| nominal | A vs A-ms2 | 24 | 21/24 (0.875) | +0.125 |
| nominal | B vs C | 48 | 48/48 (1.000) | +0.000 |
| nominal | B vs A-ms2 | 24 | 21/24 (0.875) | +0.125 |
| nominal | C vs A-ms2 | 24 | 21/24 (0.875) | +0.125 |
| force_x0.5 | A vs B | 48 | 45/48 (0.938) | -0.021 |
| force_x0.5 | A vs C | 48 | 43/48 (0.896) | -0.062 |
| force_x0.5 | A vs A-ms2 | 24 | 11/24 (0.458) | +0.458 |
| force_x0.5 | B vs C | 48 | 46/48 (0.958) | -0.042 |
| force_x0.5 | B vs A-ms2 | 24 | 11/24 (0.458) | +0.458 |
| force_x0.5 | C vs A-ms2 | 24 | 11/24 (0.458) | +0.458 |
