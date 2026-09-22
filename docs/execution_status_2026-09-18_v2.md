# Sim2Real 研究执行记录 v2（2026-09-18 晚）

承接 `execution_status_2026-09-18.md`。本文件记录当日下午至晚间完成的机器人侧实验、发现、撤回与在跑任务。所有结果均来自 ManiSkill 3.0.1 + SAPIEN 3（Windows，CPU 物理 + GPU 渲染，torch 雅可比 IK 适配器）与 WSL2 GPU 上的 Octo 1.0 推理，**是探索平台，不是原始 SIMPLER main 复现**。

## 1. 基础设施（当日打通）

| 项 | 状态 |
|---|---|
| Octo 1.0 GPU 推理 | WSL2，jax 0.5.3 + CUDA 12 插件（Blackwell 需 ≥ 0.5.x；0.4.20/0.4.30 因 XLA 把目标降为 sm_90a 而失败）。Octo 源码两处补丁（KeyArray、distrax 延迟导入）。每步推理 0.06–0.25 s（视并发） |
| 策略服务器 | `scripts/octo_policy_server.py`，本地 HTTP，每策略两台（8767/8769 small，8768/8770 base），支持部署变体配置（集成开关、动作块、历史窗口） |
| 扫描客户端 | `scripts/controller_sweep.py`：控制器参数、时延、物体摩擦/密度的进程内改写；共同随机数；断点续跑；连接重试 |
| 调度 | `scripts/queue_v2.py` 系列：按服务器端口分配作业，检测外部占用；`queue_variants.py` 可重启服务器 |
| 校准回放 | `scripts/read_bridge_batch.py`（40 条 BridgeData V2 示范，分片 0 全部 30 条 + 分片 1 前 10 条）、`scripts/replay_bridge_sysid.py`（SIMPLER sysid 协议移植，IK 从固定姿态起、2π 回绕） |
| 分析 | `analyze_controller_sweep.py`、`analyze_equiv_pairs.py`、`analyze_compatible_set.py`、`analyze_variant_pairs.py`、`check_iso_invariance.py`、`make_figures.py` |

## 2. 发现（按价值排序）

1. **校准协议的精确结构不可辨识性**（`results/replay_sysid/*/iso_invariance.md`，`results/replay_sysid_smoke/FINDING_iso_ratio.md`）：自由空间回放只能辨识刚度/阻尼比值与时延；共同尺度与力矩上限逐点差 < 0.14 mm。比值方向误差曲线为碗形，0.7–1.4 倍即可分辨。
2. **相容集合校准 vs 点校准**（`FINDING_compatible_set.md`，`analysis_compatible_set.md`）：相容集合 = 比值≈1 × 尺度全轴 × 力矩全轴（× 接触参数）。点校准在勺子、茄子上判 small 优，集合校准在三个任务上均拒判。方法（C2）的首次真实数据实例。
3. **茄子任务物体摩擦的可判定性翻转**（`FINDING_eggplant_friction.md`，96 集）：Δ 从 +0.21 [+0.08, +0.32] 降到 +0.05 [−0.07, +0.18]，变化 −0.156 [−0.29, −0.03] 区间支持；弱策略上升、强策略下降。密度 ×0.5：−0.135 [−0.27, 0.00]，机制为强策略变差。
4. **无排序符号翻转**（`SUMMARY_48.md`）：Octo-small vs Octo-base，四任务，20 个条件（含 wide、接触），48–96 集，没有区间支持的反向。撤回了两次中期候选（胡萝卜等比轴、勺子力矩上限）。
5. **翻转稀少的结构原因**：几乎所有条件只压低强策略，弱策略无上升空间；例外仅茄子低摩擦。
6. **跨后端**（`analysis_cross_backend.md`）：CPU 与 GPU 后端逐集一致率 0.83–0.96，条件级成功率一致；比较只能在同一后端内做。
7. **功效**：成功率 ≤ 0.15 时 96 集半宽仍约 0.08；低成功率任务不适合排序敏感性研究。

## 3. 图件（`results/figures/`）

- `fig_replay_identifiability.png`：比值可辨识、尺度不可见、时延可辨识。
- `fig_delta_by_condition.png`：三任务逐条件 Δ 与区间，按可辨识/不可见分色，标出集合上下界与点/集合判定。
- `fig_eggplant_contact.png`：茄子接触参数 96 集成功率。

## 4. 在跑与排队（GPU）

1. 部署变体策略（noens / chunk4 / hist1 × 两模型）× 茄子、勺子 × 6 条件 × 24 集；结束后 `analysis_variants.md` 与近平局对分析 `analysis_variant_pairs.md`。中期：noens 与 chunk4 把两模型压回低成功率区间；hist1 待出。
2. 种子复现：茄子标称与摩擦 0.2，两策略，新种子 96 集，`results/controller_sweep_gpu_rep/analysis_replication.md`。

## 5. 论文主线（当前判断）

- 核心表：任务 × {点校准判定, 集合校准判定}，配合回放可辨识性图和茄子摩擦案例。
- 强形式（排序反转）在本策略对上未观察到；作为带功效分析的负结果与"翻转集中在近平局中段成功率对"的命题一并报告。
- 必须补的：Linux + SIMPLER main 复核不可辨识性；更多策略对（不同模型家族）；把逐条件极值换成响应面 + 同时置信带。

## 6. 已撤回的中期陈述

胡萝卜等比轴单调反转（24/48 集）、勺子力矩 ×0.5 与刚度 ×2/阻尼 ×0.5 的可判定性翻转（24 集）。

## 7. 更新（20:35）：部署变体与近平局对

- 茄子标称（24 集）：octo-small 0.54、octo-small@hist1 0.46、octo-base@hist1 0.375、octo-base 0.25；关闭集成与 4 步动作块把两模型压到 0.08–0.17。单帧历史（hist1）保持中段成功率，并让 octo-base 从 0.25 升到 0.375。
- 近平局对（|Δ| ≤ 0.10，双方在 0.2–0.8）：base@hist1 vs small@hist1（Δ −0.08）、small vs small@hist1（+0.08）。24 集下所有不可见条件均拒判，无区间支持的翻转。文件：`analysis_variant_pairs_eggplant_interim.md`。
- 已排队：种子复现（茄子标称与摩擦 0.2）→ 近平局策略集在茄子 6 个不可见条件补到 96 集（`scripts/queue_hist1_96.py`）→ `analysis_variant_pairs_eggplant96.md`。
- 回放扩展到 98 条示范：可辨识性结构不变，区间收窄约 40%；网格回放进行中。

## 8. 更新（21:55）：变体扫描完成，勺子上的候选反向对

- 勺子标称（24 集）：octo-small 0.375、octo-small@hist1 0.25、octo-base@hist1 0.167、其余 ≤ 0.125；阈值内无近平局对。
- 候选反向对（同一权重，仅历史窗口不同）：octo-small vs octo-small@hist1，标称 +0.125（9 vs 6）、摩擦 0.2 −0.21（4 vs 9）、等比 ×0.25 −0.08；24 集下区间均跨零。已排队 `scripts/queue_spoon_hist1_96.py`（在茄子 96 集补充之后）补到 96 集并分析。
- 队列顺序：种子复现（进行中）→ 茄子近平局集 96 集 → 勺子候选对 96 集。全 8 策略成对表：`analysis_variants.md`；近平局分析：`analysis_variant_pairs.md`。
