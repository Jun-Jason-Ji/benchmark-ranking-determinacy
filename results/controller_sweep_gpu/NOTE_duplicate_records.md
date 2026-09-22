# 记录：茄子 hist1 标称文件的重复记录与调度器崩溃（2026-09-19 00:35）

## 现象
`octo-small@hist1/…/nominal.jsonl` 120 行 / 96 个 episode_id（24 个重复），`octo-base@hist1/…/nominal.jsonl` 131 行 / 96 个（35 个重复）。
重复记录的 policy_seed 相同；成功与否一致的比例 15/24 与 27/35，与已记录的跨进程数值不确定性（`FINDING_eggplant_friction.md`）一致。

## 原因
近平局 96 集队列在暂停/恢复时，同一条件的两个 controller_sweep 进程并发追加同一文件（逐集 resume 检查只在进程启动时做一次）。
另一次事故：`queue_v2.busy_ports` 逐 token 解析所有 controller_sweep 进程命令行中的 `http://127.0.0.1:` 端口，一条含该字串的诊断 PowerShell 命令行使 `int()` 失败，调度器进程退出（在跑的 4 个作业不受影响）。

## 处理
- 分析统一采用"同一 episode_id 保留首条完成记录"（`analyze_variant_pairs.py --dedupe first`，默认）；并输出 `--dedupe last` 版本作稳健性对照（`analysis_variant_pairs_eggplant96_dedupe_last.md`）。
- `queue_v2`：端口用正则解析并容错；启动前跳过已完整的作业（`job_complete`）；同一 (策略, 任务, 条件) 已有进程在写时不再启动第二个（`running_jobs`）。
- 三个调度器（eggplant 96、spoon 96、OpenVLA）于 00:37 在新代码上重启（`scripts/restart_queues_after_crash.cmd`）。
