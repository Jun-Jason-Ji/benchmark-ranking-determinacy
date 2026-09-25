# 官方协议复现：24 构型全普查 × 3 个种子（72 集）对表 SIMPLER 公布值（逐集重播种，已被取代）

外层循环与 `scripts/octo_bridge.sh` 一致：`--obj-episode-range 0 24`，`init_rng ∈ {0, 2, 4}`。RNG 生命周期：每次 reset 都发送种子，服务器收到即重新播种（`--policy-seed-fixed`），因此一轮内 24 个构型共用同一份噪声实现——**这不是参考实现的行为**，见 `--policy-seed-stream`。平台为原版栈（ManiSkill2_real2sim + SAPIEN 2.2.2，WSL、CPU 物理、lavapipe 渲染经 vk_fakesemfd 层），策略由本项目的 HTTP Octo 服务器提供。公布值取自固定版本的 `simpler_env/utils/metrics.py`。

| 任务 | 策略 | 种子 0 | 种子 2 | 种子 4 | 合并 (n/72) | 公布值 | 差 |
|---|---|---:|---:|---:|---:|---:|---:|
| widowx_put_eggplant_in_basket | octo-small | 0.583 (24) | 0.458 (24) | 0.625 (24) | 0.556 (72) | 0.569 | -0.013 |
| widowx_put_eggplant_in_basket | octo-base | 0.375 (24) | 0.458 (24) | 0.583 (24) | 0.472 (72) | 0.431 | +0.041 |
| widowx_spoon_on_towel | octo-small | 0.375 (24) | 0.333 (24) | 0.583 (24) | 0.431 (72) | 0.472 | -0.041 |
| widowx_spoon_on_towel | octo-base | 0.042 (24) | 0.083 (24) | 0.125 (24) | 0.083 (72) | 0.125 | -0.042 |
| widowx_carrot_on_plate | octo-small | 0.042 (24) | 0.042 (24) | 0.125 (24) | 0.069 (72) | 0.097 | -0.028 |
| widowx_carrot_on_plate | octo-base | 0.125 (24) | 0.125 (24) | 0.125 (24) | 0.125 (72) | 0.083 | +0.042 |
| widowx_stack_cube | octo-small | 0.083 (24) | 0.042 (24) | 0.000 (24) | 0.042 (72) | 0.042 | -0.000 |
| widowx_stack_cube | octo-base | 0.000 (24) | 0.000 (24) | 0.000 (24) | 0.000 (72) | 0.0 | +0.000 |

## 读法

- 8 个（任务 × 策略）单元中，我们与公布值的平均差 -0.005，平均绝对差 0.026，最大 0.042。
- 对照本项目测得的种子噪声（茄子 64 构型：单种子 95% 半宽 ±0.108，3 个种子 ±0.062）。
- 两种生命周期的对比用 `--compare` 打印；逐集重播种会放大轮间方差，从而把一个系统性的平台差异掩盖成看起来更好的一致性。
