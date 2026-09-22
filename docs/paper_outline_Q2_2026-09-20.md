# Q2 口径论文结构与贡献清单（2026-09-20 草案）

定位：**评测方法学论文**，不是又一篇 sim2real 系统论文。第一贡献放方法学（最扎实、最难驳），
"校准不可见参数改变排序可判定性"作为该方法学的主证据链，真机验证作为公开的 limitation。

---

## 0. 目标期刊（按契合度排序）

| 期刊 | 分区 | 契合点 | 风险 |
|---|---|---|---|
| **Autonomous Robots**（Springer） | JCR Q2 / 中科院 3 区 | 评测方法学 + 机器人实证，接受负面结果与协议类工作 | 偏好有真机；需强调仿真基准本身就是研究对象 |
| **Robotics and Autonomous Systems**（Elsevier） | Q2 | 系统与评测协议类常见 | 审稿周期长 |
| **Journal of Intelligent & Robotic Systems** | Q2 | 方法 + 实验均可 | 对理论深度要求中等 |
| **IEEE Access** | Q2 | 快、接受可复现性/基准审计类 | 声望较低 |
| 备选升级：**IEEE RA-L** | Q1 | 若补上真机一环 | 篇幅 8 页，需大幅压缩 |

建议首投 Autonomous Robots，备选 RAS。

---

## 1. 标题与一句话

候选标题：

1. *What a Calibrated Simulator Cannot Tell You: Decision-Relevant Non-Identifiability in Simulation-Based Policy Ranking*
2. *Ranking Robot Policies in Simulation: Finite Benchmarks, Invisible Parameters, and the Limits of Point Calibration*

一句话：**用真实示范校准的仿真器，其校准数据对一部分动力学参数零信息；在这些参数构成的相容集合内，
策略排序的结论可以被改变——而且在把基准自身的抽样误差压到零之后，这种改变依然存在。**

---

## 2. 贡献清单（按强度排序，投稿时按此顺序写）

| # | 贡献 | 证据 | 强度 |
|---|---|---|---|
| **C1** | **精确的结构不可辨识性**：SIMPLER 式自由空间回放只定出关节 PD 的 k/d 比值与执行时延；共同尺度与力矩上限的回放误差差为浮点零（不是"弱可辨识"）。两个独立仿真栈复核到亚毫米一致。 | `replay_sysid/{sweep_v1,grid}/iso_invariance.md`、`replay_sysid_ms2/FINDING_original_stack.md`、图 1 | **强**（解析 + 双栈实证） |
| **C2** | **评测基准是有限构型总体**：`episode_id mod (n_xy·n_quat)`；ms2 茄子 24、ms3 茄子 64、其余 24。超出即精确重复；**两个广泛使用的移植版评测的不是同一个基准**（茄子朝向 3 vs 8，四元数取值不同）。官方协议本就是"全普查 × 3 固定种子 = 72 集"。 | `docs/methods_census_2026-09-19.md §1`、`FINDING_seed_set_bug.md`、`FINDING_cross_stack_eggplant.md` | **强**（读码可验证） |
| **C3** | **被估量与不确定性分解**：基准值 vs 泛化值两种合法被估量；确定性策略无种子轴、全普查即精确；随机策略的残余误差是策略噪声（sd=0.055），另有实现版本漂移（0.078，逐集一致率 0.73）。单种子集 + 逐集自助会给出站不住的判定——**我们自己撤回了一条**。 | `FINDING_platform_drift.md`、`FINDING_estimand_matters.md`、`analysis_seed_noise.md` | **强**（含自我证伪实例） |
| **C4** | **决策相关的不可辨识性实例**：力矩上限 ×0.5 使 OpenVLA 茄子成功率 7/48 → 15–18/48（三次运行同号），Δ 位移 ≈0.23；余量 ≲0.2 的策略对由"可判定"退为"拒判"，余量 0.35 的扛得住。机制：全部 8 个朝向同向、增益与标称成功率负相关 r=−0.36、抓起率 +0.12~0.18。 | `FINDING_openvla_torque_replicated.md`（含更正头）、`FINDING_estimand_matters.md §2d`、`CORE_TABLE.md` | **中强**（单任务，待普查定稿） |
| **C5** | **判定阶梯与其覆盖率**：点校准 / 并集界 / GP 同时带。合成真值下点校准误判率随集数**上升**（最高 0.88），并集界=采样极值保证，GP 同时带有效但功效低（0.47→0.77 不外推配置）。真实数据上判定稳定性：point 0.50、union_ctrl 0.88、union_all 1.00。 | `benchmark/track_s/FINDING_track_s.md`、`benchmark/track_r/track_r_summary.md`、图 5 | **中强**（合成真值 + 真实稳定性） |
| **C6** | **可复现性资产**：原版 SIMPLER 在无 GPU 的 WSL 上跑通（自写 Vulkan 显式层伪装 `VK_KHR_external_semaphore_fd`）、构型普查协议、只增不改的 `runs.jsonl` 来源日志、六条可断点续跑的队列。 | `third_party/vk_fakesemfd/`、`scripts/task_configs.py`、`PROVENANCE_AUDIT_2026-09-19.md` | 中（附录/开源价值） |

**负面结果要显式写**：强形式（排序符号在相容集合内翻转）**在本研究的全部条件下均不成立**；四个 24/48 集的候选在加集数后全部撤回。这是诚实性资产，不是缺点。

---

## 3. 章节结构（目标 ~14–18 页双栏或 ~30 页单栏）

### 1 Introduction
- 现象引入：仿真基准被用来给基础策略排序（SIMPLER、AutoEval、RoboArena 的兴起）。
- 问题：校准把仿真器"调准"到示范数据上，但**校准数据对一部分参数零信息**，而这些参数可能改变排序。
- 贡献列表（C1–C6），并明确 scope：仿真内部的可判定性，不含真机验证。

### 2 Related Work
sim2real 评测（SIMPLER/AutoEval/RoboArena）、系统辨识与可辨识性、评测可复现性与统计实践（bootstrap 误用、种子敏感性）、集合型推断/部分识别（partial identification）。
> 重点差异化：既有工作问"仿真和真机相关性多高"，本文问"**给定校准数据，哪些结论原则上无法下**"。

### 3 Problem Setup
- 记号：\(\Delta^{sim}_{ij}(z;\pi)\)，有限构型集合 \(\mathcal{C}\)，策略随机源 \(\sigma\)，实现版本 \(\pi\)（`theory_protocol.md §6.1`）。
- 相容集合 \(C_\alpha\) 的定义与检验反演构造。
- **判定问题**的形式化：给定 \(C_\alpha\)，何时可以宣布 \(i \succ j\)。

### 4 The Calibration Protocol Is Structurally Blind（C1）
- 自由空间回放的解析论证：一阶响应只依赖时间常数 d/k；力矩在示范速度范围内不饱和。
- 双栈实证（98 条 Bridge 示范）：等比不变 ≤0.21 mm、力矩误差差为浮点零、比值/时延可辨识（碗形曲线）。
- **图 1**：`fig_replay_identifiability.png`

### 5 What a Finite Benchmark Measures（C2+C3）
- 构型映射与各任务构型数表；两个移植版的网格差异。
- 官方协议 = 普查 × 3 种子；文献普遍只跑一次。
- 两种被估量与方差分解；确定性策略的特殊性。
- **隐藏变量量级对照表**：种子 0.055 / 版本 0.078（逐集一致 0.73）/ 参数 0.23。
- **自我证伪实例**：Δ(small−base)=+0.250 [+0.08,+0.32] 被三个同代种子集推翻（+0.141/−0.031/−0.047）。
- **图 2（新）**：三种不确定性来源的量级条形图（需作图）。

### 6 Decision-Relevant Non-Identifiability（C4）
- 核心表：点校准 vs 并集界（`CORE_TABLE.md`）。
- 力矩 × OpenVLA 的完整证据：三次运行、构型层面分解、机制检查。
- 任务相关性：勺子上同一参数几乎不改变 Δ（−0.01~−0.07），茄子上 −0.23。
- **图 3**：`fig_delta_by_condition.png`；**图 4（新）**：按朝向的效应分解。

### 7 A Verdict Ladder and Its Coverage（C5）
- 三级判据；合成赛道 S 的覆盖率与功效；真实赛道 R 的稳定性。
- **图 5**：`fig_track_s.png`；**图 6**：`fig_response_surface.png`（GP 同时带）。

### 8 Reproducing the Published Protocol（外部效度）✅ 初稿 `docs/paper_draft_s8.md`
- 我们的 72 集复现 vs `metrics.py` 公布值逐格对比（`FINDING_official_protocol.md`，2026-09-20 完成）。
- 8 个格子平均绝对差 **0.026**、最大 **0.042**，全部落在我们测得的种子噪声（3 种子 ±0.062）内 ⇒ 流水线可信。
- 额外收获（计划外）：在公布协议自己的 72 集预算下，octo-small vs octo-base 的**四个任务排序只有一个可判定**，
  且胡萝卜在忠实复现中**反号**（我们 −0.056，公布 +0.014，双方都在噪声内）。这是"评测表上的排序重跑不复现"的
  一个具体实例，直接支撑中心论点。

### 9 Limitations
1. 无真机验证；AutoEval 公共端点离线、RoboArena 额度未确认（有截图与日期记录）。
2. 2 个模型家族、1 种本体、3–4 个任务；OpenVLA 为 4-bit 量化。
3. 强形式命题不成立。
4. 成功率 0.1–0.5 导致大量"拒判"；功效分析见 §7。
5. 实现版本漂移只在 2 个策略上做了分离实验。

### 10 Conclusion
把"更多评测无法解决该问题"的定量依据收尾：3 种子 ±0.062、10 种子 ±0.034，而参数位移 0.23。

### Appendix
A 相容集合的检验反演细节；B 原版栈无 GPU 渲染方案；C 完整条件表与每格 n；D 复现步骤（对应路线页 §7）。

---

## 4. 图表清单

| 编号 | 内容 | 状态 |
|---|---|---|
| 表 1 | 核心表：点校准 vs 并集界（每格含构型覆盖、运行数、方差模型） | ✅ `results/CORE_TABLE.md`，不一致对 **3** 个；T1-B/T2-A 完成后自动刷新 |
| 表 2 | 各任务构型数 × 两个移植版 | 已有（方法节） |
| 表 3 | 隐藏变量量级对照 | 已有 |
| 表 4 | 官方协议复现对表 | ✅ `FINDING_official_protocol.md`，正文见 `paper_draft_s8.md` §8.2 |
| 表 5 | 公布预算下四个排序的可判定性（含胡萝卜反号） | ✅ `paper_draft_s8.md` §8.3（计划外新增） |
| 图 1 | 回放可辨识性（碗形 vs 平坦） | ✅ |
| 图 2 | 三种不确定性来源量级 | ✅ `fig_uncertainty_budget.png`（`scripts/make_figures_v2.py`，数据驱动，数据齐后重跑即可） |
| 图 3 | Δ 按条件 | ✅ |
| 图 4 | 力矩效应按朝向分解 | ✅ `fig_torque_by_orientation.png`（同上） |
| 图 5 | 赛道 S 覆盖率 | ✅ |
| 图 6 | GP 响应面与同时带 | ✅ |

---

## 5. 投稿前检查清单

- [x] 今晚队列跑完：茄子/胡萝卜全普查、并集界当代重采、官方协议复现（2026-09-20）
- [x] ms3 勺子/胡萝卜在当代平台补齐（T1-A，2026-09-20 15:45；审计更新见 `PROVENANCE_AUDIT` §5.1）
- [x] OpenVLA bf16 对照一组，或在 setup 中明确把 4-bit 写成研究设定 → **取后者**（8 GB 卡放不下 bf16，见第 2 档 T2-C）
- [x] 图 2、图 4 作图（数据齐后重跑 `scripts/make_figures_v2.py` 刷新数值）
- [ ] 每个数字标注五项来源信息（构型覆盖、运行数、方差模型、被估量、移植版与版本）
- [ ] 所有撤回条目在正文或附录显式列出（诚实性资产）
- [ ] 代码与数据打包：脚本 + `runs.jsonl` + 队列 + 路线页
- [ ] 与 SIMPLER 作者沟通：网格差异与公布值不确定性，避免被读成指责

---

## 6. 若要升级到 RA-L / T-RO

1. 真机或第三方真机代评闭环（哪怕 1 任务 × 1 对策略）；
2. ≥4 个策略家族 × 2 种本体 × 6–8 任务；
3. 正面方法结果：并集界/GP 同时带在有真值场景下"既保守又有用"的定量证明。
