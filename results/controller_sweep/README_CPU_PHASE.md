# CPU 阶段（已中止）

本目录下 `octo-small/` 与 `octo-base/` 的 JSONL 来自 Windows CPU JAX 推理阶段（jax 0.4.20），于 2026-09-18 约 07:25 本地时间中止，原因是 WSL2 GPU 推理通道打通后速度提升 5–10 倍，正式扫描改在 `results/controller_sweep_gpu/` 全量重跑。

CPU 阶段完成的条件（胡萝卜任务，每条件 24 集）：

| 策略 | 条件 | 成功 |
|---|---|---:|
| octo-small | nominal | 4/24 |
| octo-small | stiff_x0.5 | 3/24 |
| octo-small | stiff_x2.0 | 2/24 |
| octo-small | damp_x0.5 | 2/24 |
| octo-base | nominal | 3/24 |
| octo-base | stiff_x0.5 | 3/24 |

未完成的条件文件可能只含部分 episode。这些数据只用于与 GPU 结果做跨后端对照，不并入主分析。协议见 `PROTOCOL.md`，计时见 `gpu_timing_2026-09-18.md`，服务器与扫描日志在 `logs/`。
