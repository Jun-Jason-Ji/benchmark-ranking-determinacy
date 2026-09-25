# V3 prospective spoon repeatability with controlled initialization

All 768 planned rollouts completed. Negative block shifts: 7/8; zeros: 0/8.
Prespecified one-sided exact binomial p = 0.03515625; one-sided 95% lower bound on P(D_block < 0) = 0.529321.
This tests directional repeatability across the specified seed-block sampling model, not a population mean shift.

| Block | Small nominal | Base nominal | Small fitted | Base fitted | Nominal gap | Fitted gap | Change |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 8/24 | 2/24 | 5/24 | 5/24 | +0.2500 | +0.0000 | -0.2500 |
| 2 | 11/24 | 2/24 | 4/24 | 4/24 | +0.3750 | +0.0000 | -0.3750 |
| 3 | 5/24 | 0/24 | 6/24 | 4/24 | +0.2083 | +0.0833 | -0.1250 |
| 4 | 14/24 | 3/24 | 11/24 | 3/24 | +0.4583 | +0.3333 | -0.1250 |
| 5 | 10/24 | 1/24 | 9/24 | 2/24 | +0.3750 | +0.2917 | -0.0833 |
| 6 | 7/24 | 0/24 | 7/24 | 4/24 | +0.2917 | +0.1250 | -0.1667 |
| 7 | 7/24 | 2/24 | 10/24 | 2/24 | +0.2083 | +0.3333 | +0.1250 |
| 8 | 9/24 | 1/24 | 6/24 | 3/24 | +0.3333 | +0.1250 | -0.2083 |

Secondary mean change: -0.151042.
Secondary t working-model 95% interval (7 df): [-0.271621, -0.030462].
Secondary distribution-free bounded-mean interval: [-2.000000, +1.769604], using D in [-2,2].

All initial states/images, parameter assignments, reseeding responses and source hashes passed the fixed integrity checks. Statistical independence of blocks remains an assumption; unique seed numbers do not prove it.

Not a test of E[D]=0; not a six-setting envelope confirmation, real-world or cross-engine validation. This tests the direction under a repaired initialization protocol, not causal isolation of the historical protocol contrast.
