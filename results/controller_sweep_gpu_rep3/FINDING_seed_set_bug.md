# 方法学错误与更正：确定性策略没有"种子集"，SIMPLER 任务的初始构型是有限且会循环的（2026-09-19 20:30）

## 1. 事实

**(a) 环境初始状态完全由 `episode_id` 对构型数取模决定。** 两个栈的实现相同：

```
pos  = (episode_id % (n_xy * n_quat)) // n_quat
quat =  episode_id %  n_quat
```
（ms3: `mani_skill/envs/tasks/digital_twins/bridge_dataset_eval/base_env.py:357`；
ms2: `ManiSkill2_real2sim/.../custom_scenes/put_on_in_scene.py:188`）

| 任务 | 栈 | n_xy | n_quat | **不同构型数** |
|---|---|---:|---:|---:|
| 茄子 PutEggplantInBasketScene-v1 | ms3 | 8 | 8 | **64** |
| 茄子 PutEggplantInBasketScene-v0 | ms2（原版） | 8 | 3 | **24** |
| 勺子 / 胡萝卜 | 两栈 | 12 | 2 | **24** |
| 堆叠 | 两栈 | 24 | 1 | **24** |

物体缩放 `model_scales` 虽由 `np_random` 抽取，但资产表里每个物体只有 `[1.0]` 一个取值，不引入额外变化。因此 **episode_id ≥ 构型数就是在精确重复此前的初始状态**：ms3 茄子的 ep 64–95 与 ep 0–31 完全相同；ms2 茄子 / 勺子 / 胡萝卜的 48 集跑法等于 24 个构型各跑两遍。

**(b) OpenVLA 推理是确定性的。** `openvla_policy_server.py` 用 `predict_action(..., do_sample=False)`，`reset()` 接收 seed 但从不使用。Octo 则相反：`octo_policy_server.py:78` 用 `jax.random.PRNGKey(seed)` 播种扩散头采样。

**(c) 直接证据。** OpenVLA 茄子标称条件下，"种子集 B"（20270101）与"种子集 C"（20280101）的 48 条记录**逐条完全相同**（48/48，成功/步数/夹爪事件/抓取标志全等）。

## 2. 由此产生的错误

`FINDING_openvla_torque_replicated.md`（2026-09-19 15:50）把 A/B 两组 OpenVLA 数据当作"两个独立种子集"，据此宣布力矩效应"已按预注册规则复现"。**该复现论证不成立**：对确定性策略，改变 policy seed 不产生任何新样本，A/B/C 是同一配置的重复运行。唯一的抽样轴是环境构型，而两组用的是同一批 ep 0–47（同样 48 个构型）。

其次，"96 集"的计划对 OpenVLA 也是无效的：ep 64–95 精确重复 ep 0–31，若计入自助抽样会凭空把区间收窄约 √2 倍。

Octo 侧不受影响：其 seed 真实参与采样，A/B/C 是合法的独立复制。

## 3. 更正后的口径：构型普查

对确定性策略，把基准当作**有限总体**处理：跑完全部构型即得到**精确**的成功率，不存在需要靠加集数收窄的抽样误差。剩下的不确定性只有两项：

1. **仿真器参数**（本研究的对象）——相容集合内的力矩上限等不可见方向；
2. **运行间数值不确定性**——同一构型重复运行的 GPU 非确定性（bitsandbytes 4-bit 核选择）。实测同意率：标称 A vs B 42/48、B vs C 48/48；力矩 ×0.5 A vs B 45/48、B vs C 46/48，即每集约 0–12% 的翻转率。

这反而强化了论文主张：**把抽样误差压到恰好为零（全构型普查）之后，校准不可见的参数依然改变判定能否下。**

## 4. 已做的修正

- 停掉 `queue_openvla_strengthen`（A/B 扩到 96 集）与 `queue_openvla_more`（勺子 24→48 等纯重复作业）。
- 新增 `scripts/task_configs.py`：各任务构型数、`config_id()`、确定性策略判定、普查去重。
- `scripts/analyze_openvla_torque_sets.py` 改为普查口径：对确定性策略按构型去重（首条为准），输出覆盖率表与运行间同意率表。
- 新队列 `scripts/queue_openvla_census.py`：茄子 ms3 补到 64 构型全普查（标称 + 力矩，以及 iso_x0.25 / iso_x4.0 / fric_x0.4 / dens_x0.5）；胡萝卜 24 构型全普查；ms2 茄子 24 构型全普查（跨栈）。勺子 ms3 六个条件各 24 集，已是全普查，无需再跑。
- `scripts/queue_octo_strengthen.py` 改为对齐同一普查：第三种子集 0–63、第二种子集补到 0–63（原计划 48–95 中的 64–95 属于构型重复）。

## 5. 现有结论的去留

| 结论 | 状态 |
|---|---|
| 力矩 ×0.5 使 OpenVLA 茄子成功率上升（7/48 → 15–18/48，三次运行同号） | **保留**，但措辞改为"48/64 构型上的测量，三次重复运行一致"，不再称"两个独立种子集复现" |
| octo-small / small@hist1 对 OpenVLA 由"可判定"退为"拒判" | **保留**，三次运行均如此（见 `analysis_openvla_torque_census.md` §3） |
| "按预注册两种子集规则已复现" | **撤回措辞**，改为普查 + 运行间稳定性两条证据 |
| Octo 家族内部全部结论（含四个撤回的候选） | **不受影响**，Octo 的种子集有效 |
