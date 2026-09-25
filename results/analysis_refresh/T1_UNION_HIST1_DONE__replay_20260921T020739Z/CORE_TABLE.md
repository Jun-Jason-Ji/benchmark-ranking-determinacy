# 核心表：点校准 vs 相容集合判定（构型普查口径）

每格的 Δ 为基准值估计量（全构型枚举后构型抽样误差为零，区间只含策略噪声与确定性策略的运行间噪声）。**点校准** = 仅标称条件；**并集界** = 结论须在全部校准不可见条件上同号，区间取 [min 下界, max 上界]。两者不一致的行，就是点校准宣布了校准数据无法支撑的排序。仅用当代服务器采集的数据（Octo 用种子集 A', B, C, D, E；OpenVLA 的服务器自始至终是同一套 Windows 进程，故其数据不受该问题影响，沿用 A, B, C, D, E）。

| 任务 | 策略对 | 构型 | 运行数 | 点校准 Δ [95%] | 判定 | 并集界 | 判定 | 不一致 | 方差模型 |
|---|---|---|---|---|---|---|---|---|---|
| eggplant (ms3) | octo-small vs octo-base | 64/64 | 3/3 | +0.034 [-0.05, +0.12] | abstain | [-0.04, +0.29] | abstain | 否 | empirical / empirical |
| eggplant (ms3) | octo-small vs octo-small@hist1 | 64/64 | 3/3 | +0.070 [-0.01, +0.15] | abstain | [-0.01, +0.27] | abstain | 否 | empirical / empirical |
| eggplant (ms3) | octo-small vs octo-base@hist1 | 64/64 | 3/3 | +0.117 [+0.04, +0.20] | octo-small> | [-0.03, +0.28] | abstain | **是** | empirical / empirical |
| eggplant (ms3) | octo-small vs openvla-7b-4bit | 64/64 | 3/2 | +0.320 [+0.24, +0.40] | octo-small> | [+0.12, +0.52] | octo-small> | 否 | empirical / empirical |
| eggplant (ms3) | octo-base vs octo-small@hist1 | 64/64 | 3/3 | +0.036 [-0.05, +0.12] | abstain | [-0.19, +0.20] | abstain | 否 | empirical / empirical |
| eggplant (ms3) | octo-base vs octo-base@hist1 | 64/64 | 3/3 | +0.083 [+0.00, +0.17] | octo-base> | [-0.10, +0.17] | abstain | **是** | empirical / empirical |
| eggplant (ms3) | octo-base vs openvla-7b-4bit | 64/64 | 3/2 | +0.286 [+0.21, +0.36] | octo-base> | [+0.05, +0.43] | octo-base> | 否 | empirical / empirical |
| eggplant (ms3) | octo-small@hist1 vs octo-base@hist1 | 64/64 | 3/3 | +0.047 [-0.03, +0.13] | abstain | [-0.15, +0.18] | abstain | 否 | empirical / empirical |
| eggplant (ms3) | octo-small@hist1 vs openvla-7b-4bit | 64/64 | 3/2 | +0.250 [+0.17, +0.33] | octo-small@hist1> | [+0.04, +0.43] | octo-small@hist1> | 否 | empirical / empirical |
| eggplant (ms3) | octo-base@hist1 vs openvla-7b-4bit | 64/64 | 3/2 | +0.203 [+0.13, +0.28] | octo-base@hist1> | [-0.00, +0.42] | abstain | **是** | empirical / empirical |
| spoon (ms3) | octo-small vs octo-base | 24/24 | 2/2 | +0.396 [+0.23, +0.56] | octo-small> | [+0.04, +0.54] | octo-small> | 否 | empirical / empirical |
| carrot (ms3) | octo-small vs octo-base | 24/24 | 2/2 | -0.042 [-0.12, +0.04] | abstain | [-0.20, +0.07] | abstain | 否 | empirical / empirical |
| eggplant (ms2, original stack) | octo-small vs octo-base | 24/24 | 1/1 | +0.062 [-0.21, +0.34] | abstain | [-0.22, +0.40] | abstain | 否 | binomial (1 run/config) / binomial (1 run/config) |
| eggplant (ms2, original stack) | octo-small vs openvla-7b-4bit | 24/24 | 1/1 | +0.438 [+0.24, +0.64] | octo-small> | [+0.24, +0.64] | octo-small> | 否 | binomial (1 run/config) / 1 run (drift unmeasured) |
| eggplant (ms2, original stack) | octo-base vs openvla-7b-4bit | 24/24 | 1/1 | +0.375 [+0.18, +0.57] | octo-base> | [+0.12, +0.50] | octo-base> | 否 | binomial (1 run/config) / 1 run (drift unmeasured) |
| spoon (ms2, original stack) | octo-small vs octo-base | 24/24 | 1/1 | +0.208 [-0.04, +0.46] | abstain | [-0.07, +0.56] | abstain | 否 | binomial (1 run/config) / binomial (1 run/config) |
| carrot (ms2, original stack) | octo-small vs octo-base | 24/24 | 1/1 | +0.000 [-0.16, +0.16] | abstain | [-0.20, +0.14] | abstain | 否 | binomial (1 run/config) / binomial (1 run/config) |

不一致的策略对共 **3** 个。

口径与限制见 `docs/methods_census_2026-09-19.md`；形式化账本见 `docs/theory_protocol.md §6.1`；数据来源与风险分级见 `results/PROVENANCE_AUDIT_2026-09-19.md`。
