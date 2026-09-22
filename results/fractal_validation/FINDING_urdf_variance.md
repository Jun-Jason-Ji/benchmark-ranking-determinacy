# 原版栈 fractal 流水线验证通过，并暴露一个比我们此前量化的所有隐藏变量都大的方差来源（2026-09-21）

数据：`results/fractal_validation/octo-base/GraspSingleOpenedCokeCanInScene-v0/nominal.jsonl`，
octo-base × pick coke can，官方 visual matching 协议的**全部 300 个构型**
（4 个 URDF 变体 × 3 种罐姿 × 5×5 物体 xy 网格），原版 SIMPLER 栈（ManiSkill2_real2sim + SAPIEN 2.2.2，
WSL、CPU 物理、lavapipe 渲染经 vk_fakesemfd 层），策略由本项目的 HTTP Octo 服务器提供（`policy_setup=google_robot`，
黏滞夹爪 `sticky_gripper_num_repeat=15`）。

## 1. 验证门：通过

| | 成功率 |
|---|---:|
| 本项目复现（300 构型全普查） | **0.173** [0.130, 0.216] |
| `metrics.py` 公布值 | 0.170 |
| 差 | **+0.003** |

这是第二个本体（google robot / fractal）上的端到端验证，与 §8 的 bridge 套件复现（8 格平均绝对差 0.026）
相互独立。至此原版栈流水线在**两个本体、两套协议**上都对上了公布值，fractal 上的后续扫描可以进入正式阶段。

## 2. 意外发现：公布数字在一个**纯视觉**冗余变量上求平均，而该变量的跨度是 0.40

| URDF 变体 | lr_switch | upright | laid_vertically | 变体均值 |
|---|---:|---:|---:|---:|
| （默认，不重上色） | 0.000 | 0.000 | 0.000 | **0.000** |
| recolor_tabletop_visual_matching_1 | 0.440 | 0.160 | 0.240 | **0.280** |
| recolor_tabletop_visual_matching_2 | 0.000 | 0.000 | 0.040 | **0.013** |
| recolor_cabinet_visual_matching_1 | 0.520 | 0.240 | 0.440 | **0.400** |

- 变体间极差 **0.400**，标准差 0.199；相比之下罐姿的极差只有 0.140。
- `urdf_version` 只改机器人模型的**贴图颜色**，不改物理。它对策略的影响却是 0.000 → 0.400。
- 官方协议正是要在这 4 个变体上取平均（`scripts/octo_pick_coke_can_visual_matching.sh` 的
  `urdf_version_arr` 含 `None`），所以这**不是实现错误**，是协议设计；而 (0.000+0.280+0.013+0.400)/4 = 0.173
  与公布值吻合，本身就是"我们的 URDF 处理是对的"的证据。

## 3. 量级对照：这是目前最大的隐藏变量

| 来源 | 对成功率 / Δ 的影响 | 能否靠加评测消掉 |
|---|---:|---|
| 策略种子噪声（同代 A′/B/C） | sd 0.055 | 能，∝1/√S |
| 实现版本漂移（换推理栈代次） | ≤0.078 | 否，但可固定版本 |
| 校准不可见物理参数（力矩上限 ×0.5） | 0.141 | **否** |
| **URDF 视觉变体（本节）** | **极差 0.400** | 否，只能按协议全跑 |

若只评测单一变体（文献中常见的省事做法），相对 4 变体均值的偏差是 −0.173 ~ +0.227——
**比我们整篇论文讨论的参数位移还大**。

## 4. 这对论文意味着什么，以及还不能说什么

**能说的。** §5"基准数字到底对什么求平均"又多了一个实例，而且是最尖锐的一个：被平均掉的不是物理参数，
而是渲染外观的选择；它对校准协议（回放轨迹）是**完全不可见**的——回放损失根本不含图像项。
这把"校准不可见"从物理参数推广到了渲染配置。

**还不能说的。** 本节只有**一个策略**。方差大不等于**排序**会变；要证明后者，需要在同一 300 构型网格上
跑第二个策略，看各变体上的排序是否一致。这正是 RT-1（rt-1-x / rt-1-converged / rt-1-15pct）要做的事：
若两个策略对 URDF 变体的响应不同，则逐变体的排序可能互相矛盾，那将是本文现象在**第二个本体**上的独立实例，
而且该套件带公布的真机成绩可作对照。在拿到第二个策略之前，本节只作为方差来源报告，不作排序结论。

## 5. 复现

```
# Windows 侧：起带 google_robot 设置的 Octo 服务器（会话级设置，见 scripts/octo_policy_server.py）
wsl.exe -e bash scripts/run_wsl_server.sh octo-base 8772
# WSL 侧：跑 300 构型全普查
bash scripts/run_fractal_validation.sh octo-base 8772
```
