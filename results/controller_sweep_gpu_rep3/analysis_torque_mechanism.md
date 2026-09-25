# Configuration-level mechanism of `force_x0.5`: PutEggplantInBasketScene-v1

The grid has **64** configurations. Per-configuration success is pooled over every run that covers it (sources chosen per policy family, as in `make_core_table.py`). A configuration counts as improved/degraded when the pooled rate moves by more than 0.01.

## openvla-7b-4bit

- configurations compared: 64/64 (**complete**); runs per configuration: 1–3 nominal, 1–3 force_x0.5
- benchmark value: 0.156 → 0.271 (**+0.115**)
- per configuration: **16 improve / 42 unchanged / 6 degrade**
- correlation of gain with nominal success: **r = -0.44**
- configurations failing outright at nominal: 51; of these **13 rescued**

| orientation | -45° | 0° | 45° | 90° | 135° | 180° | 225° | 270° |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| nominal | 0.00 | 0.21 | 0.29 | 0.12 | 0.25 | 0.04 | 0.25 | 0.08 |
| force_x0.5 | 0.25 | 0.25 | 0.25 | 0.21 | 0.29 | 0.08 | 0.54 | 0.29 |
| change | +0.25 | +0.04 | -0.04 | +0.08 | +0.04 | +0.04 | +0.29 | +0.21 |

Orientations with a positive mean change: **7/8** (range -0.04 to +0.29).

## octo-small

- configurations compared: 64/64 (**complete**); runs per configuration: 3–3 nominal, 3–3 force_x0.5
- benchmark value: 0.477 → 0.458 (**-0.018**)
- per configuration: **15 improve / 34 unchanged / 15 degrade**
- correlation of gain with nominal success: **r = -0.26**
- configurations failing outright at nominal: 16; of these **4 rescued**

| orientation | -45° | 0° | 45° | 90° | 135° | 180° | 225° | 270° |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| nominal | 0.67 | 0.79 | 0.62 | 0.23 | 0.35 | 0.67 | 0.27 | 0.21 |
| force_x0.5 | 0.67 | 0.83 | 0.54 | 0.21 | 0.33 | 0.58 | 0.29 | 0.21 |
| change | +0.00 | +0.04 | -0.08 | -0.02 | -0.02 | -0.08 | +0.02 | +0.00 |

Orientations with a positive mean change: **2/8** (range -0.08 to +0.04).
