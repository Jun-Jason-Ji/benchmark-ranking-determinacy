# Multiplicity across the 17 bridge policy pairs

Per-pair intervals are what the core table reports, and the ledger's $E_{MC}$ is a joint event over pairs, so the counts have to be corrected before they can be read as "each of these orderings holds". This file performs the correction that Appendix A.2 previously only flagged as missing. Correction is needed across **pairs** and not across **conditions**: a false envelope declaration requires one particular condition's own lower bound to exceed its own truth, and that condition is fixed by the surface rather than selected from the data (Sect. 3.3).

Estimator: Eq. (eq:var), run observation unit, $\alpha = 0.05$. The $z$ for a pair is $\hat\Delta/\mathrm{se}$ at nominal. The envelope declares only when every condition agrees, so it is an intersection-union test and its $p$ is the LARGEST of the per-condition $p$ values. Holm then controls the family-wise error rate over pairs without an independence assumption, which matters because these pairs share policy data. Benjamini-Hochberg is printed beside it because the choice between a family-wise and a false-discovery reading is a choice about what the table claims, not a technicality.

| task | pair | $n$ | point $\Delta$ [95%] | $p$ | Holm | BH | envelope | IUT $p$ | Holm | BH |
|---|---|---:|---|---:|---|---|---|---:|---|---|
| eggplant (ms3) | `octo-small` vs `octo-base` | 64 | +0.055 [-0.008, +0.117] | 8.68e-02 | no | no | [-0.008, +0.244] | 8.68e-02 | no | no |
| eggplant (ms3) | `octo-small` vs `octo-small@hist1` | 64 | +0.072 [+0.009, +0.135] | 2.49e-02 | no | yes | [+0.009, +0.237] | 2.49e-02 | no | yes |
| eggplant (ms3) | `octo-small` vs `octo-base@hist1` | 64 | +0.128 [+0.066, +0.190] | 4.75e-05 | **yes** | yes | [+0.012, +0.245] | 2.06e-02 | no | yes |
| eggplant (ms3) | `octo-small` vs `openvla-7b-4bit` | 64 | +0.328 [+0.264, +0.393] | 2.25e-23 | **yes** | yes | [+0.173, +0.504] | 1.13e-15 | **yes** | yes |
| eggplant (ms3) | `octo-base` vs `octo-small@hist1` | 64 | +0.017 [-0.048, +0.082] | 6.04e-01 | no | no | [-0.145, +0.156] | 6.04e-01 | no | no |
| eggplant (ms3) | `octo-base` vs `octo-base@hist1` | 64 | +0.073 [+0.010, +0.137] | 2.43e-02 | no | yes | [-0.064, +0.137] | 9.87e-01 | no | no |
| eggplant (ms3) | `octo-base` vs `openvla-7b-4bit` | 64 | +0.273 [+0.207, +0.340] | 8.65e-16 | **yes** | yes | [+0.066, +0.422] | 2.69e-05 | **yes** | yes |
| eggplant (ms3) | `octo-small@hist1` vs `octo-base@hist1` | 64 | +0.056 [-0.008, +0.120] | 8.54e-02 | no | no | [-0.159, +0.146] | 1.17e-01 | no | no |
| eggplant (ms3) | `octo-small@hist1` vs `openvla-7b-4bit` | 64 | +0.256 [+0.189, +0.323] | 5.61e-14 | **yes** | yes | [+0.090, +0.406] | 6.77e-07 | **yes** | yes |
| eggplant (ms3) | `octo-base@hist1` vs `openvla-7b-4bit` | 64 | +0.200 [+0.134, +0.266] | 2.60e-09 | **yes** | yes | [+0.017, +0.426] | 1.01e-02 | no | yes |
| spoon (ms3) | `octo-small` vs `octo-base` | 24 | +0.396 [+0.227, +0.564] | 4.06e-06 | **yes** | yes | [+0.035, +0.564] | 1.84e-02 | no | yes |
| carrot (ms3) | `octo-small` vs `octo-base` | 24 | -0.042 [-0.123, +0.040] | 3.17e-01 | no | no | [-0.199, +0.074] | 4.80e-01 | no | no |
| eggplant (ms2, original stack) | `octo-small` vs `octo-base` | 24 | +0.062 [-0.096, +0.221] | 4.39e-01 | no | no | [-0.106, +0.288] | 4.67e-01 | no | no |
| eggplant (ms2, original stack) | `octo-small` vs `openvla-7b-4bit` | 24 | +0.438 [+0.315, +0.560] | 2.56e-12 | **yes** | yes | [+0.315, +0.560] | 2.56e-12 | **yes** | yes |
| eggplant (ms2, original stack) | `octo-base` vs `openvla-7b-4bit` | 24 | +0.375 [+0.275, +0.475] | 2.00e-13 | **yes** | yes | [+0.190, +0.475] | 5.73e-07 | **yes** | yes |
| spoon (ms2, original stack) | `octo-small` vs `octo-base` | 24 | +0.208 [+0.079, +0.337] | 1.57e-03 | **yes** | yes | [+0.038, +0.475] | 1.14e-02 | no | yes |
| carrot (ms2, original stack) | `octo-small` vs `octo-base` | 24 | +0.000 [-0.100, +0.100] | 1.00e+00 | no | no | [-0.142, +0.100] | 1.00e+00 | no | no |

## Counts

| criterion | declares uncorrected | survives Holm | survives BH |
|---|---:|---:|---:|
| point calibration | 11 | 9 | 11 |
| union bound over the fibre | 10 | 5 | 10 |

Point declarations that do not survive Holm: `octo-small` vs `octo-small@hist1` (eggplant (ms3), lower bound +0.0091); `octo-base` vs `octo-base@hist1` (eggplant (ms3), lower bound +0.0095).

Envelope declarations that do not survive Holm: `octo-small` vs `octo-small@hist1` (eggplant (ms3), envelope bound +0.0091); `octo-small` vs `octo-base@hist1` (eggplant (ms3), envelope bound +0.0117); `octo-base@hist1` vs `openvla-7b-4bit` (eggplant (ms3), envelope bound +0.0174); `octo-small` vs `octo-base` (spoon (ms3), envelope bound +0.0351); `octo-small` vs `octo-base` (spoon (ms2, original stack), envelope bound +0.0375).

The knife-edge declarations of Sect. 7.2 are the ones to watch here: a bound of $+0.0091$ or $+0.0095$ carries a $p$ far too large to survive a step-down procedure over 17 hypotheses, which is the concrete form of the caveat in Appendix A.2. Whether the corrected or the uncorrected count is the right one to quote depends on what is being claimed -- a reader interested in one named pair wants the uncorrected interval, a reader who scans the table for whichever orderings it declares wants the corrected one -- and we report both rather than choosing for them.
