# Sim2Real 研究执行记录

日期：2026-09-18。当前阶段：首轮数学原型、公开资源审计与本机仿真连通验证。论文主实验尚未完成。

## 1. 已完成的研究工作

| 项目 | 实际产物与结果 |
|---|---|
| 执行方案 | 新建 v3 与数学协议，保留原 v1/v2 和审计报告 |
| 合成原型 | 运行前冻结种子 20260918 与配置；300 次重复；54,000 条证据实验记录和 5,400 条机制记录 |
| 实现验证 | 8 项单元测试通过；两次运行逐试验 CSV SHA-256 相同 |
| 科学图 | 从保存的 CSV 用 Matplotlib 生成 PNG/PDF；已查看 PNG，文字和图例无裁切 |
| SIMPLER 成绩表 | AST 解析固定源码，42 个任务×策略单元；37 个具有公开权重候选的单元，不代表已重跑 |
| 排序描述性核查 | 62 个可考虑重跑的任务内策略对；5 对仿真/真实均值差符号相反，3 对至少一域均值相等；不作统计确认 |
| RoboArena | 当前官网与官方提交表单可读取，技术接口可查；排队、额度和指定实验能力仍未确认 |
| 机器人场景连通 | 四个 WidowX 场景均完成 640×480 图像读取和 10 步确定性抬升动作，关节位置有限且发生变化；不是学习策略评测 |
| 真实数据读取 | 读取 Bridge 第 0 个训练分片的第 1 条记录，38 步，15,903,486 字节；记录 CRC32C 及 SHA-256，提取状态/动作数值 |

合成原型的重要结果：预算 8 时，D-optimal 和 c-optimal 选择相同证据；预算 16 的可判定率分别为随机 50.3%、D-optimal 59.0%、c-optimal 60.7%。这不证明新效用或显著优越性。单个预设策略对的 Wald 区间更有效率，应保留为强基线。

完全未激励的差值方向，在 8,192 条同类证据下仍不收缩；弱但非零激励会随数据增加改善。后者不能被写成“再多数据也无效”。以上只验证已知线性模型内的机制。

## 2. 本机环境和真实执行结果

- GPU：NVIDIA GeForce RTX 5060 Laptop，8151 MiB；Windows 驱动 616.92。
- 已有 WSL：Ubuntu 24.04 / WSL2，本次按需启动现有发行版。
- 项目中建立两个互相独立的 Python 3.11.16 环境。
- WSL 原始栈：SAPIEN 2.2.2、NumPy 1.24.4、原始 SIMPLER 与固定 ManiSkill2 子模块已安装。
- 原始栈的 CPU engine 可创建，Vulkan 图像渲染失败，报 `ErrorExtensionNotPresent`。使用既有 Lavapipe ICD 的一次替代尝试同样失败，保留两份日志。
- Windows 栈：SAPIEN 3.0.3 的 64×64 离屏图像读取已通过。完整场景使用 ManiSkill 3.0.1、官方 SIMPLER `maniskill3` 分支和 CPU 物理。
- PyTorch 2.7.1+cu128 已安装，实际 CUDA 内核检查通过。Windows 环境依赖检查通过（88 个包）。
- 完整场景通过显式 `scripts/ms3_windows_compat.py` 适配：使用上游已有的 PyTorch Jacobian IK 在 CPU 上求解，并修正 PCI 地址解析，让渲染图像复制回 CPU 张量。适配只在当前 Python 进程生效，没有改安装包源码。
- 该适配改变了默认 Pinocchio IK 行为，是探索用途的控制器变体，必须与原始 SIMPLER 基线分开。Pinocchio 2.7 源码构建失败；3.8 在当前 Windows/Python 组合无可用预编译包，因此没有安装系统编译器。

| 场景 | 动作步数 | 步进耗时/秒 | 关节变化范数 |
|---|---:|---:|---:|
| Eggplant in basket | 10 | 0.148 | 0.306 |
| Carrot on plate | 10 | 0.164 | 0.245 |
| Spoon on tablecloth | 10 | 0.145 | 0.245 |
| Stack cubes | 10 | 0.151 | 0.245 |

这是各一次初始化后的短运行时间，不含模型推理、初始化和重复方差，不能外推为正式评测吞吐。动作是 0.005 的 z 方向命令和开夹爪命令，仅验证接口。没有声称完成任务；成功标志保留在 JSON 中。

[ManiSkill 官方支持表](https://maniskill.readthedocs.io/en/latest/user_guide/getting_started/installation.html)明确列出 WSL 不支持渲染，而 Windows 支持 CPU 物理与 GPU 渲染。[PyTorch 2.7 发布说明](https://pytorch.org/blog/pytorch-2-7/)说明其 CUDA 12.8 构建支持 Blackwell。主机 `nvidia-smi` 显示的 CUDA 最大兼容版本，不能代替所安装框架的运行时版本。

**复现边界：** 官方 SIMPLER 迁移分支本身声明，复现原论文应使用 `main`。在新版模拟器上完成场景测试、甚至得到策略成功率，都不能自动与旧版真实标签组成已经校准的验证闭环。正式评测前需审计迁移后的控制器、求解器、相机、动作频率和成功定义，或使用支持原始栈的原生 Linux 机器。

## 3. 源码与依赖记录

| 资源 | 固定版本 |
|---|---|
| SIMPLER main | `06accaca93535902d408da4855f21cece12bceb7` |
| ManiSkill2_real2sim 子模块 | `ef7a4d4fdf4b69f2c2154db5b15b9ac8dfe10682` |
| SIMPLER maniskill3 | `52a5088ca4bfc3a7159828af08874a198d6f95c3` |
| 原始 metrics.py SHA-256 | `ee8596be6997d41295bf5b25f90c9b5b3ba47ef2bd92296b8c45e7ffc5606dc6` |

Linux 环境包清单在 `requirements-sim-lock.txt`，必要兼容约束在 `requirements-sim-minimal.txt`。Windows 清单为 `requirements-windows-ms3-lock.txt`；重建时 `torch==2.7.1+cu128` 需使用官方 CUDA 12.8 wheel 索引。硬件、包版本及源码在 `results/environment/hardware_and_versions.json`，350 个资产文件的 SHA-256 在 `results/environment/asset_manifest.json`。

场景资产通过 ManiSkill 官方资源表下载到 `data/maniskill-assets/data`。WidowX 资产解压器在 Windows 中遇到已创建的空目标目录；仅删除经检查为空的目标目录，并将同一项目内的官方解压目录移到该位置。未改第三方物理实现。

## 4. 目前尚未完成

1. 匹配历史真实标签的冻结 RT-1-X / Octo 1.0 推理；没有把 Octo 1.5 接到旧标签。
2. 真实轨迹批量选取、轨迹独立性与控制协议匹配。单条读取已通过，但不等于完成校准。
3. 机器人参数相容集合、真实结构偏差校准、连续参数极值误差和多策略决策效用。
4. 真实成功率逐次记录、样本量和场景分层审计；目前不从取整均值反推试验数。
5. 新增真实机器人评测，以及投稿年度/单位口径的中科院 TOP 字段确认。

AutoEval 延续此前离线结论，作为条件项。本轮没有重新声称队列在线。RoboArena 的公开表单可读也不等于获得机器人名额。

## 5. 紧接着的执行顺序

1. 决定正式复现使用原生 Linux 原始栈，或将迁移栈作为独立平台并完成控制差异审计；当前 Windows 适配结果不能填入旧版基准成绩表。
2. 建立冻结策略推理环境，下载一个与历史标签匹配的检查点，先做单图推理和调试回合，记录延迟和显存。
3. 在已通过的真实数据读取入口上，按固定分片/记录 ID 扩展小样本，核验状态坐标、动作时间对齐和终止信息。
4. 冻结开发/校准/评测划分，构造低维控制响应相容集合；随后进行策略敏感方向分析。

本轮执行的是本地可逆研究工作。未创建定时任务、开机/登录自动启动项或长期服务；未提交任何真实机器人动作、策略申请或邮件。
