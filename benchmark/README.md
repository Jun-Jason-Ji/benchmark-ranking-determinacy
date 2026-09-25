# 可判定性基准（Decidability Benchmark）v0.1

目的：把"校准后的仿真能否可靠比较策略"从一次性实验升级为可重复评测的基准。被评测对象是**判定方法**（给定各条件下的配对成功数据，输出策略差值在相容参数集合上的上下界与判定），而不是策略本身。

## 赛道

| 赛道 | 数据 | 真值 | 状态 |
|---|---|---|---|
| **S：合成响应面** | 与真实扫描相同的 13 个设计点、相容带、配对伯努利结果（高斯 copula 共同随机数） | 已知的 Δ(z) 曲面；带内极值 [L*, U*] | v0.1 已实现（`decidability_bench/run_track_s.py`） |
| R：真实扫描数据 | 冻结的 jsonl（清单 `results/benchmark/track_r/track_r_manifest.json`）：茄子近平局集两个种子集；茄子/勺子/胡萝卜两个仿真栈 | 无真值；以独立复制（种子集、仿真栈）间的判定稳定性评分 | v0.1 已实现（`decidability_bench/run_track_r.py`） |
| C：校准审计 | Bridge 示范回放（98 条）+ 5×5×2 网格 | 等比不变性证书（组内最大偏差） | 脚本已有（`scripts/check_iso_invariance.py`），待封装为赛道 |

## 赛道 S 的评测协议

- 设计点：`nominal, stiff_x{0.5,2,0.25,4}, damp_x{0.5,2,0.25,4}, iso_x{0.25,0.5,2,4}`，坐标 (log₂ k, log₂ d)。相容带 |log₂ k − log₂ d| ≤ 0.25，带内采样点为 nominal 与 4 个 iso 点。
- 数据生成：每个设计点 n 集，两策略成功率 p_B(z) = 0.35、p_A(z) = p_B + Δ(z)。同一 episode_id 在所有条件、两策略间共享潜变量（copula 相关 ρ = 0.3），模拟共同随机数。
- 曲面族（Δ(u, v) = f(s) + g(r)，s = (u+v)/2 为不可见尺度方向，r = u − v 为可见比值方向，g(r) = −0.05·r²）：
  - `flat`：f = Δ₀
  - `linear`：f = Δ₀ + 0.04·s
  - `dip_sampled`：f = Δ₀ − 0.25·exp(−(s+2)²/(2·0.5²))（凹陷位于采样点 iso ×0.25）
  - `dip_unsampled`：f = Δ₀ − 0.25·exp(−(s−1.5)²/(2·0.3²))（凹陷位于 iso ×2 与 ×4 之间，未采样）
  - Δ₀ ∈ {0, 0.10, 0.20, 0.30}，n ∈ {24, 48, 96}
- 方法（与真实分析管线同一代码路径）：
  - `point`：仅标称条件的配对自助 95% 区间
  - `union`：带内采样条件区间的并集界（min 下界，max 上界）
  - `gp_sim`：GP 响应面同时 95% 带（超参数边际化，后验函数抽样极值）
  - `gated`：平坦性门控（任一 iso 条件的 Δ(c) − Δ(nominal) 区间不含零 → 用 union，否则用 gp_sim）
- 指标（每单元 R 次重复）：
  - `cover`：[L̂, Û] ⊇ [L*, U*] 的频率（目标 ≥ 0.95）
  - `false_declare`：宣布 "+" 而 L* ≤ 0，或宣布 "−" 而 U* ≥ 0 的频率（目标 ≤ 0.05）
  - `declare`：宣布某一符号的频率（真值可判定时即功效）
  - `width`：Û − L̂ 的均值
- 说明：`dip_unsampled` 对只在采样点取证的方法（点校准、并集界）不可见，用来区分"采样极值"型保证与"带内"型保证（GP 同时带靠采样点之间的后验方差覆盖它）。

## 复现

```
.venv-windows-ms3\Scripts\python.exe benchmark\decidability_bench\run_track_s.py --reps 300 --out results\benchmark\track_s
```
输出：`track_s_results.json`（逐单元指标）、`track_s_summary.md`（表）、`fig_track_s.png`。

## 赛道 S 首轮结果（2026-09-19）

见 `results/benchmark/track_s/FINDING_track_s.md`。要点：点校准误判率随 n 上升（最高 0.88）；并集界仅对采样极值有效（未采样凹陷覆盖 0.22）；GP 同时带在全部曲面有效但功效低；门控无收益，已从推荐阶梯中撤下。不外推配置（`DB_SMAX=2.0`）把 GP 功效提高约 1.6 倍，覆盖率下限 0.85。第三配置（`DB_ELL_MIN=1.0`，长度尺度下限 = 采样间距）功效再翻倍但对凹陷曲面失效（覆盖 0.45–0.83），不采用。

## 赛道 R 协议与首轮结果（2026-09-19）

- 复制对：(a) 同平台两个策略种子集（20260918 vs 20270101，茄子近平局集 4 策略）；(b) 同种子两个仿真栈（ManiSkill3 vs 原版 SIMPLER main，茄子/勺子/胡萝卜，Octo-small vs Octo-base）。每对 48 集。
- 方法：`point`（标称区间）、`union_ctrl`（等比 ×0.25、×4、力矩 ×0.5 的并集界）、`union_all`（加摩擦 0.2、密度 ×0.5）。
- 指标：stable（两复制同判）、contradict（两复制反号宣布）、unsupported（一复制宣布另一拒判）、declare（宣布率）。稳定性必须与宣布率一起读：从不宣布的方法稳定性恒为 1。

| 方法 | 对数 | stable | contradict | unsupported | declare |
|---|---:|---:|---:|---:|---:|
| point | 9 | 0.44 | 0.00 | 0.56 | 0.39 |
| union_ctrl | 9 | 0.89 | 0.00 | 0.11 | 0.06 |
| union_all | 9 | 1.00 | 0.00 | 0.00 | 0.00 |

点校准的宣布中超过一半在独立复制上不被支持；并集界几乎不宣布。赛道 R 的下一版需要更大的 Δ 余量对（如 Octo 对 OpenVLA）来分开"稳健地宣布"与"从不宣布"。
