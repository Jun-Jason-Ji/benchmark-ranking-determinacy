# What Determines a Simulation Benchmark Ranking?

Reproducibility release for the manuscript *What Determines a Simulation Benchmark Ranking?
Structural Blindness, Finite Configuration Grids, and Evaluation Budget in Simulation-Based Policy
Comparison*, submitted to *Autonomous Robots*.

<!-- TODO-AUTHOR: add the Zenodo DOI badge here once the first release is tagged. -->

**Start here:** [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) - what is in this release, and the exact
commands that regenerate every table and figure from the per-episode records.

This is a **code-and-aggregate release**: it contains the harness, every per-episode record behind
every number in the paper, the append-only provenance logs, and the analysis scripts. It does not
redistribute simulator assets, policy checkpoints or the source datasets; see
[`NOTICE.md`](NOTICE.md).

| | |
|---|---|
| How to cite | [`CITATION.cff`](CITATION.cff) |
| What changed between releases | [`CHANGELOG.md`](CHANGELOG.md) |
| Integrity of the record files | [`SHA256SUMS.txt`](SHA256SUMS.txt) - 997 files, `sha256sum -c` |
| Third-party components | [`NOTICE.md`](NOTICE.md) |
| Licence | [`LICENSE`](LICENSE) - MIT for original code; records and derived outputs per `NOTICE.md` |
| The manuscript as submitted | `submission/autonomous_robots/` |

One number is carried in deliberately unreconciled - the implementation-build drift in Table 3. See
the "Known open item" section of `REPRODUCIBILITY.md`.

---

The remainder of this file is the project's working log, in Chinese. It records how the results
accumulated, including the conclusions that were withdrawn along the way.

# 决策相关可辨识性与 Sim2Real 策略比较

**2026-09-19 方法学更正（重要）**：SIMPLER 式基准的初始构型是有限且循环的（`episode_id mod 构型数`；ms3 茄子 64 个，ms2 茄子与勺子/胡萝卜各 24 个），且 OpenVLA 推理确定性、忽略策略种子。因此「多种子集复现」对确定性策略无效，`episode_id` 超出构型数是精确重复，两个移植版的茄子网格也不相同。现行口径为**构型全普查**，与 SIMPLER 官方协议（24 构型 × 3 个固定种子 = 72 集）一致。方法节见 [docs/methods_census_2026-09-19.md](docs/methods_census_2026-09-19.md)，证据见 `results/controller_sweep_gpu_rep3/FINDING_seed_set_bug.md` 与 `FINDING_estimand_matters.md`。

研究已进入执行阶段。当前主要审阅入口为 [执行记录](docs/execution_status_2026-09-18.md)、[研究方案 v3](sim2real_research_proposal_v3_2026-09-18.md) 和 [数学协议](docs/theory_protocol.md)。旧方案与审计报告保留。研究路线与复现指南（中英文可切换、离线单文件）：[docs/research_route.html](docs/research_route.html)，由 `scripts/build_research_site.py` 从 `docs/site/research_route.template.html` 生成。

## 已可复现的内容

1. [合成机制实验](pilot/README.md)：二维线性高斯模型、连续集合极值、D-optimal / c-optimal / 随机证据选择、单对 Wald 强基线。300 次重复，8 项测试通过。**不是机器人或 VLA 实验。**
2. [SIMPLER 成绩核查](research_audit/published_pairwise_audit.md)：从固定官方版本提取 42 个公开成绩单元，排除 RT-2-X 后有 37 个可考虑公开权重的单元。62 个任务内策略对中有 5 对均值差符号相反，只作描述性分析。
3. [RoboArena 提交核验](research_audit/roboarena_submission_audit_2026-09-18.md)：公开入口与技术条件可读，排队和额度尚未确认。
4. 四个 WidowX 场景的 10 步图像/动作测试通过，结果在 `results/ms3_motion_probes/`。使用明确标记的 Windows IK 适配层，不能冒充原始基准。
5. [真实轨迹读取记录](research_audit/bridge_sample_ingestion.json)：38 步公开 Bridge 示范，CRC32C 通过，按 HTTP Range 只读取约 15.2 MiB。

## 目录

| 路径 | 用途 |
|---|---|
| `pilot/` | 冻结配置、原型、单元测试、逐次数据和图表 |
| `scripts/` | 源表审计、统计绘图、SAPIEN 和场景连通测试 |
| `research_audit/` | 公开数据来源、成绩表、网页核验快照 |
| `results/` | 本机渲染与仿真检查结果，明确标记证据类型 |
| `logs/` | 安装、失败与运行日志 |
| `third_party/SimplerEnv/` | 固定主分支，原始 ManiSkill2 / SAPIEN2 |
| `third_party/SimplerEnv-ms3/` | 固定官方迁移分支，仅作兼容路径 |
| `.venv-linux/` | WSL Python3.11 原始仿真栈，当前渲染失败 |
| `.venv-windows-ms3/` | Windows Python3.11 / SAPIEN3 兼容栈 |
| `.runtime/`、`data/` | 项目内运行时缓存和公开场景资产 |

## 在当前主机复现

PowerShell，工作目录 `E:\research\the_world`。

```powershell
# 公开成绩表：解析 Python 字面量，不执行第三方指标代码
python scripts\audit_simpler.py
python scripts\analyze_published_ranking.py

# 合成实验：也可用其他带 NumPy 的 Python
& 'C:\Users\Jason\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s pilot -v
& 'C:\Users\Jason\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' pilot\run_pilot.py

# 从已保存结果生成 Matplotlib 科学图，不重新抽样
& .\.venv-windows-ms3\Scripts\python.exe scripts\plot_pilot.py

# 原生图像渲染检查
& .\.venv-windows-ms3\Scripts\python.exe scripts\probe_sapien.py --output results\environment\sapien_windows3.json

# 官方迁移后的 WidowX 场景，CPU 物理 + GPU 渲染，零动作调试
& .\.venv-windows-ms3\Scripts\python.exe scripts\smoke_simpler_ms3.py

# 有动作的探索性连通检查
& .\.venv-windows-ms3\Scripts\python.exe scripts\smoke_simpler_ms3.py --action-mode lift_probe --output-dir results\motion_probe

# 网络读取：仅一条公开真实示范，上限 64 MiB；不是校准或真实评测
& .\.venv-windows-ms3\Scripts\python.exe scripts\read_bridge_sample.py
```

脚本会覆盖对应输出目录中的同名调试结果。正式实验需使用独立输出目录并冻结配置、代码和资源校验值。Windows 兼容分支不能被称为原始 SIMPLER 主分支成绩复现。

## 研究结论的当前边界

线性原型已证实预设模型中的激励失配机制；尚未实现新决策效用，尚未证明优于经典 c-optimal，也尚未形成真实轨迹校准和冻结 VLA 评测闭环。Windows 进程内适配用上游 PyTorch IK 替代 Pinocchio IK，会改变控制行为。历史公开成绩已被查看，不能再称完全盲测标签。真实成功率不能从合成数据或动作调试产生。
