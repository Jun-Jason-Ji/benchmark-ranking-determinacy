# 核心表：点校准 vs 相容集合判定（构型普查口径）

每格的 Δ 为基准值估计量（全构型枚举后构型抽样误差为零，区间只含策略噪声与确定性策略的运行间噪声）。**点校准** = 仅标称条件；**并集界** = 结论须在全部校准不可见条件上同号，区间取 [min 下界, max 上界]。两者不一致的行，就是点校准宣布了校准数据无法支撑的排序。仅用当代服务器采集的数据（Octo 用种子集 A', B, C, D, E；OpenVLA 的服务器自始至终是同一套 Windows 进程，故其数据不受该问题影响，沿用 A, B, C, D, E）。

| 任务 | 策略对 | 构型 | 运行数 | 点校准 Δ [95%] | 判定 | 并集界 | 判定 | 不一致 | 方差模型 |
|---|---|---|---|---|---|---|---|---|---|
| eggplant (ms3) | octo-small vs octo-base | 64/64 | 5/5 | +0.055 [-0.01, +0.12] | abstain | [-0.01, +0.24] | abstain | 否 | empirical / empirical |
| eggplant (ms3) | octo-small vs octo-small@hist1 | 64/64 | 5/5 | +0.072 [+0.01, +0.13] | octo-small>† | [+0.01, +0.24] | octo-small>† | 否 | empirical / empirical |
| eggplant (ms3) | octo-small vs octo-base@hist1 | 64/64 | 5/5 | +0.128 [+0.07, +0.19] | octo-small> | [+0.01, +0.24] | octo-small> | 否 | empirical / empirical |
| eggplant (ms3) | octo-small vs openvla-7b-4bit | 64/64 | 5/1 | +0.328 [+0.26, +0.39] | octo-small> | [+0.17, +0.50] | octo-small> | 否 | empirical / empirical |
| eggplant (ms3) | octo-base vs octo-small@hist1 | 64/64 | 5/5 | +0.017 [-0.05, +0.08] | abstain | [-0.14, +0.16] | abstain | 否 | empirical / empirical |
| eggplant (ms3) | octo-base vs octo-base@hist1 | 64/64 | 5/5 | +0.073 [+0.01, +0.14] | octo-base>† | [-0.06, +0.14] | abstain | **是** | empirical / empirical |
| eggplant (ms3) | octo-base vs openvla-7b-4bit | 64/64 | 5/1 | +0.273 [+0.21, +0.34] | octo-base> | [+0.07, +0.42] | octo-base> | 否 | empirical / empirical |
| eggplant (ms3) | octo-small@hist1 vs octo-base@hist1 | 64/64 | 5/5 | +0.056 [-0.01, +0.12] | abstain | [-0.16, +0.15] | abstain | 否 | empirical / empirical |
| eggplant (ms3) | octo-small@hist1 vs openvla-7b-4bit | 64/64 | 5/1 | +0.256 [+0.19, +0.32] | octo-small@hist1> | [+0.09, +0.41] | octo-small@hist1> | 否 | empirical / empirical |
| eggplant (ms3) | octo-base@hist1 vs openvla-7b-4bit | 64/64 | 5/1 | +0.200 [+0.13, +0.27] | octo-base@hist1> | [+0.02, +0.43] | octo-base@hist1> | 否 | empirical / empirical |
| spoon (ms3) | octo-small vs octo-base | 24/24 | 2/2 | +0.396 [+0.23, +0.56] | octo-small> | [+0.04, +0.56] | octo-small> | 否 | empirical / empirical |
| carrot (ms3) | octo-small vs octo-base | 24/24 | 2/2 | -0.042 [-0.12, +0.04] | abstain | [-0.20, +0.07] | abstain | 否 | empirical / empirical |
| eggplant (ms2, original stack) | octo-small vs octo-base | 24/24 | 2/2 | +0.062 [-0.10, +0.22] | abstain | [-0.11, +0.29] | abstain | 否 | empirical / empirical |
| eggplant (ms2, original stack) | octo-small vs openvla-7b-4bit | 24/24 | 2/1 | +0.438 [+0.32, +0.56] | octo-small> | [+0.32, +0.56] | octo-small> | 否 | empirical / 1 run (drift unmeasured) |
| eggplant (ms2, original stack) | octo-base vs openvla-7b-4bit | 24/24 | 2/1 | +0.375 [+0.27, +0.48] | octo-base> | [+0.19, +0.48] | octo-base> | 否 | empirical / 1 run (drift unmeasured) |
| spoon (ms2, original stack) | octo-small vs octo-base | 24/24 | 2/2 | +0.208 [+0.08, +0.34] | octo-small> | [+0.04, +0.47] | octo-small> | 否 | empirical / empirical |
| carrot (ms2, original stack) | octo-small vs octo-base | 24/24 | 2/2 | +0.000 [-0.10, +0.10] | abstain | [-0.14, +0.10] | abstain | 否 | empirical / empirical |
| pick-coke-can (ms2, fractal) | rt-1-converged vs rt-1-15pct | 300/300 | 1/1 | +0.147 [+0.08, +0.21] | rt-1-converged> | [+0.07, +0.24] | rt-1-converged> | 否 | binomial (1 run/config) / binomial (1 run/config) |

不一致的策略对共 **1** 个。

† 打了此标记的判定落在刀口上：把它排除出 0 的那一端界限绝对值小于 0.01，四舍五入到两位小数即为 0。**这种“宣布”与拒判之间只差数值噪声，不应与稳健的宣布同等看待。**

- eggplant (ms3)，octo-small vs octo-small@hist1：点校准 [+0.009079, +0.134671]（刀口）；并集界 [+0.009079, +0.237057]（刀口）
- eggplant (ms3)，octo-base vs octo-base@hist1：点校准 [+0.009548, +0.137327]（刀口）；并集界 [-0.064198, +0.137327]

**并集所覆盖的条件数按任务不同，不可横向当作同等强度**（条件越少，并集界越接近点校准）：

- eggplant (ms3)：5 个条件 — `iso_x0.25`, `iso_x4.0`, `force_x0.5`, `fric_x0.4`, `dens_x0.5`
- spoon (ms3)：5 个条件 — `iso_x0.25`, `iso_x4.0`, `force_x0.5`, `fric_x0.4`, `dens_x0.5`
- carrot (ms3)：5 个条件 — `iso_x0.25`, `iso_x4.0`, `force_x0.5`, `fric_x0.4`, `dens_x0.5`
- eggplant (ms2, original stack)：5 个条件 — `iso_x0.25`, `iso_x4.0`, `force_x0.5`, `fric_x0.4`, `dens_x0.5`
- spoon (ms2, original stack)：5 个条件 — `iso_x0.25`, `iso_x4.0`, `force_x0.5`, `fric_x0.4`, `dens_x0.5`
- carrot (ms2, original stack)：5 个条件 — `iso_x0.25`, `iso_x4.0`, `force_x0.5`, `fric_x0.4`, `dens_x0.5`
- pick-coke-can (ms2, fractal)：2 个条件 — `force_x0.5`, `fric_x0.4`

`pick-coke-can (ms2, fractal)` 一行是真机-仿真反转对：该对的公布真机排序与仿真相反（真机 0.853 vs 0.920，仿真 0.857 vs 0.710），因此它检验的是**判据会不会在仿真出错的对上拒判**。结论见 `results/fractal_reversal/analysis_fractal_reversal.md`与论文 §8.4：不会——并集界在该对上宣布了真机反对的排序。

**观察单位：`run`。** Eq. (eq:var) 的 S_c 写的是「构型 c 上的运行次数」，即 `run` 口径；早期实现先在目录内对同构型的多集取平均，再把目录均值作为观察值（`directory` 口径）。两者在 18 对中有 2 对判决不同：MS3 eggplant small−base（`directory` 下界 +0.000042 宣布，`run` 下为 [−0.0079, +0.1173] 拒判）与 MS2 spoon small−base（`directory` 拒判，`run` 宣布）。**point/set 不一致的总数在两种口径下都是 1。** 主分析用 `run`，因为公式如此定义、且同一目录内不同 episode 用的是不同策略种子；`directory` 更保守（防目录级共同效应），以 `--unit directory` 复现，作为敏感性报告。口径不是按哪种更容易得到宣布来选的。

口径与限制见 `docs/methods_census_2026-09-19.md`；形式化账本见 `docs/theory_protocol.md §6.1`；数据来源与风险分级见 `results/PROVENANCE_AUDIT_2026-09-19.md`。
