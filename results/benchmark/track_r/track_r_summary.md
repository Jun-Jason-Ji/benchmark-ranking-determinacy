> **更正（2026-09-19 20:30）**：`eggplant_stacks` 那一组"复制"两侧评测的不是同一批初始构型——ms3 茄子网格为 8 位置 × 8 朝向，
> ms2 原版为 8 × 3 且四元数不同，故它比较的是两个不同的基准。脚本已加 `grid_match` 标记，主汇总改为只统计同网格复制。
> 结论不变：同网格口径下 point 稳定 0.50 / 宣布 0.38，union_ctrl 0.88 / 0.06，union_all 1.00 / 0（旧口径 0.44 / 0.39、0.89 / 0.06、1.00 / 0）。
> 勺子与胡萝卜两栈网格逐值相同，不受影响。详见 `../../controller_sweep_gpu_rep3/FINDING_seed_set_bug.md`。

# Track R: verdict stability on real sweep data (episodes 0-47)

No ground truth: a method is scored by whether its verdict on one replicate is reproduced on an independent replicate. stable = same verdict; contradict = both declared with opposite signs; unsupported = declared on one replicate, abstain on the other; declare = fraction declared.

## Per dataset and method

| dataset | replicates | same config grid | method | pairs | stable | contradict | unsupported | declare |
|---|---|---|---|---:|---:|---:|---:|---:|
| eggplant_seedsets | seed sets 20260918 vs 20270101 (ManiSkill3) | yes | point | 6 | 0.33 | 0.00 | 0.67 | 0.33 |
| eggplant_seedsets | seed sets 20260918 vs 20270101 (ManiSkill3) | yes | union_ctrl | 6 | 1.00 | 0.00 | 0.00 | 0.00 |
| eggplant_seedsets | seed sets 20260918 vs 20270101 (ManiSkill3) | yes | union_all | 6 | 1.00 | 0.00 | 0.00 | 0.00 |
| eggplant_stacks | ManiSkill3 vs original SIMPLER main (same seeds) | **no** | point | 1 | 0.00 | 0.00 | 1.00 | 0.50 |
| eggplant_stacks | ManiSkill3 vs original SIMPLER main (same seeds) | **no** | union_ctrl | 1 | 1.00 | 0.00 | 0.00 | 0.00 |
| eggplant_stacks | ManiSkill3 vs original SIMPLER main (same seeds) | **no** | union_all | 1 | 1.00 | 0.00 | 0.00 | 0.00 |
| spoon_stacks | ManiSkill3 vs original SIMPLER main (same seeds) | yes | point | 1 | 1.00 | 0.00 | 0.00 | 1.00 |
| spoon_stacks | ManiSkill3 vs original SIMPLER main (same seeds) | yes | union_ctrl | 1 | 0.00 | 0.00 | 1.00 | 0.50 |
| spoon_stacks | ManiSkill3 vs original SIMPLER main (same seeds) | yes | union_all | 1 | 1.00 | 0.00 | 0.00 | 0.00 |
| carrot_stacks | ManiSkill3 vs original SIMPLER main (same seeds) | yes | point | 1 | 1.00 | 0.00 | 0.00 | 0.00 |
| carrot_stacks | ManiSkill3 vs original SIMPLER main (same seeds) | yes | union_ctrl | 1 | 1.00 | 0.00 | 0.00 | 0.00 |
| carrot_stacks | ManiSkill3 vs original SIMPLER main (same seeds) | yes | union_all | 1 | 1.00 | 0.00 | 0.00 | 0.00 |

## Aggregate over datasets

Headline = replications whose two sides evaluate the same configuration grid. The eggplant stack pair is listed separately because ManiSkill3 and the original stack use different eggplant orientation grids (8x8 vs 8x3).

| scope | method | pairs | stable | contradict | unsupported | declare |
|---|---|---:|---:|---:|---:|---:|
| same-grid replications | point | 8 | 0.50 | 0.00 | 0.50 | 0.38 |
| same-grid replications | union_ctrl | 8 | 0.88 | 0.00 | 0.12 | 0.06 |
| same-grid replications | union_all | 8 | 1.00 | 0.00 | 0.00 | 0.00 |
| all replications (legacy) | point | 9 | 0.44 | 0.00 | 0.56 | 0.39 |
| all replications (legacy) | union_ctrl | 9 | 0.89 | 0.00 | 0.11 | 0.06 |
| all replications (legacy) | union_all | 9 | 1.00 | 0.00 | 0.00 | 0.00 |

## Verdicts per pair

| dataset | pair | point A/B | union_ctrl A/B | union_all A/B |
|---|---|---|---|---|
| eggplant_seedsets | octo-small vs octo-base | +/0 | 0/0 | 0/0 |
| eggplant_seedsets | octo-small vs octo-small@hist1 | 0/0 | 0/0 | 0/0 |
| eggplant_seedsets | octo-small vs octo-base@hist1 | 0/+ | 0/0 | 0/0 |
| eggplant_seedsets | octo-base vs octo-small@hist1 | 0/0 | 0/0 | 0/0 |
| eggplant_seedsets | octo-base vs octo-base@hist1 | 0/+ | 0/0 | 0/0 |
| eggplant_seedsets | octo-small@hist1 vs octo-base@hist1 | 0/+ | 0/0 | 0/0 |
| eggplant_stacks | octo-small vs octo-base | +/0 | 0/0 | 0/0 |
| spoon_stacks | octo-small vs octo-base | +/+ | +/0 | 0/0 |
| carrot_stacks | octo-small vs octo-base | 0/0 | 0/0 | 0/0 |

Manifest: 120 input files with md5 in `track_r_manifest.json`.