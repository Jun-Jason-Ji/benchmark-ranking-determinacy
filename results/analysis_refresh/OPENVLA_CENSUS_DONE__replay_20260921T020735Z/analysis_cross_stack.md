# Cross-stack comparison: original SIMPLER main (ms2/SAPIEN2, WSL CPU render) vs ManiSkill3/Windows, episodes 0-23

Same policies (Octo-small / Octo-base via the same HTTP servers), same episode_ids and policy seeds, variants_v1 conditions. Δ = small − base, paired bootstrap 95%. Union bound = min/max of per-condition CI over the 5 calibration-invisible conditions.

**Config grids.** An episode_id means the same initial state on both stacks only when the two envs share the configuration grid. Spoon and carrot do (12 positions x 2 orientations); **eggplant does not** (ManiSkill3 8 x 8 vs original 8 x 3, different quaternions), so per-episode agreement is not computed there and the rates compare different initial-pose distributions. See results/controller_sweep_gpu_rep3/FINDING_seed_set_bug.md.

## eggplant

| condition | n (ms2/ms3) | small ms2 / ms3 | base ms2 / ms3 | Δ ms2 [95%] | Δ ms3 [95%] | verdict ms2 / ms3 | per-episode agreement small / base |
|---|---:|---|---|---|---|---|---|
| nominal | 24/24 | 0.458 / 0.542 | 0.375 / 0.250 | +0.083 [-0.12, +0.29] | +0.292 [+0.08, +0.50] | abstain / small | n/a (grids differ) |
| iso_x0.25 | 24/24 | 0.375 / 0.458 | 0.333 / 0.375 | +0.042 [-0.17, +0.25] | +0.083 [-0.17, +0.33] | abstain / abstain | n/a (grids differ) |
| iso_x4.0 | 24/24 | 0.500 / 0.542 | 0.375 / 0.375 | +0.125 [-0.04, +0.29] | +0.167 [-0.12, +0.46] | abstain / abstain | n/a (grids differ) |
| force_x0.5 | 24/24 | 0.583 / 0.500 | 0.292 / 0.375 | +0.292 [+0.12, +0.46] | +0.125 [-0.12, +0.38] | small / abstain | n/a (grids differ) |
| fric_x0.4 | 24/24 | 0.500 / 0.500 | 0.375 / 0.458 | +0.125 [-0.12, +0.38] | +0.042 [-0.21, +0.29] | abstain / abstain | n/a (grids differ) |
| dens_x0.5 | 24/24 | 0.417 / 0.583 | 0.292 / 0.417 | +0.125 [-0.12, +0.38] | +0.167 [-0.08, +0.42] | abstain / abstain | n/a (grids differ) |

Point calibration (nominal): ms2 **abstain**, ms3 **small**. Union bound over the invisible conditions: ms2 [-0.17, +0.46] → **abstain**; ms3 [-0.21, +0.46] → **abstain**.

## spoon

| condition | n (ms2/ms3) | small ms2 / ms3 | base ms2 / ms3 | Δ ms2 [95%] | Δ ms3 [95%] | verdict ms2 / ms3 | per-episode agreement small / base |
|---|---:|---|---|---|---|---|---|
| nominal | 24/24 | 0.375 / 0.375 | 0.167 / 0.083 | +0.208 [+0.00, +0.42] | +0.292 [+0.12, +0.50] | abstain / small | 0.75 / 0.75 |
| iso_x0.25 | 24/24 | 0.375 / 0.250 | 0.125 / 0.000 | +0.250 [+0.04, +0.46] | +0.250 [+0.08, +0.42] | small / small | 0.88 / 0.88 |
| iso_x4.0 | 24/24 | 0.458 / 0.292 | 0.083 / 0.125 | +0.375 [+0.17, +0.58] | +0.167 [-0.04, +0.38] | small / abstain | 0.75 / 0.88 |
| force_x0.5 | 24/24 | 0.375 / 0.250 | 0.125 / 0.083 | +0.250 [+0.04, +0.46] | +0.167 [+0.00, +0.38] | small / abstain | 0.79 / 0.79 |
| fric_x0.4 | 24/24 | 0.417 / 0.167 | 0.042 / 0.083 | +0.375 [+0.21, +0.58] | +0.083 [-0.12, +0.29] | small / abstain | 0.75 / 0.88 |
| dens_x0.5 | 24/24 | 0.375 / 0.250 | 0.000 / 0.042 | +0.375 [+0.21, +0.58] | +0.208 [+0.00, +0.42] | small / abstain | 0.79 / 0.96 |

Point calibration (nominal): ms2 **abstain**, ms3 **small**. Union bound over the invisible conditions: ms2 [+0.04, +0.58] → **small**; ms3 [-0.12, +0.42] → **abstain**.

## carrot

| condition | n (ms2/ms3) | small ms2 / ms3 | base ms2 / ms3 | Δ ms2 [95%] | Δ ms3 [95%] | verdict ms2 / ms3 | per-episode agreement small / base |
|---|---:|---|---|---|---|---|---|
| nominal | 24/24 | 0.083 / 0.125 | 0.042 / 0.083 | +0.042 [+0.00, +0.12] | +0.042 [-0.12, +0.21] | abstain / abstain | 0.88 / 0.96 |
| iso_x0.25 | 24/24 | 0.083 / 0.042 | 0.042 / 0.125 | +0.042 [-0.08, +0.17] | -0.083 [-0.21, +0.00] | abstain / abstain | 0.96 / 0.83 |
| iso_x4.0 | 24/24 | 0.083 / 0.208 | 0.083 / 0.083 | +0.000 [-0.17, +0.17] | +0.125 [+0.00, +0.25] | abstain / abstain | 0.88 / 1.00 |
| force_x0.5 | 24/24 | 0.083 / 0.125 | 0.083 / 0.083 | +0.000 [-0.12, +0.12] | +0.042 [-0.12, +0.21] | abstain / abstain | 0.88 / 1.00 |
| fric_x0.4 | 24/24 | 0.083 / 0.125 | 0.042 / 0.167 | +0.042 [-0.08, +0.21] | -0.042 [-0.21, +0.12] | abstain / abstain | 0.88 / 0.79 |
| dens_x0.5 | 24/24 | 0.083 / 0.125 | 0.042 / 0.083 | +0.042 [-0.08, +0.17] | +0.042 [-0.08, +0.21] | abstain / abstain | 0.79 / 0.96 |

Point calibration (nominal): ms2 **abstain**, ms3 **abstain**. Union bound over the invisible conditions: ms2 [-0.17, +0.21] → **abstain**; ms3 [-0.21, +0.25] → **abstain**.
