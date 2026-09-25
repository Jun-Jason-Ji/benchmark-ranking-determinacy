# Multiplicity across the 17 bridge policy pairs

Per-pair intervals are what the core table reports, and the ledger's $E_{MC}$ is a joint event over pairs, so the counts have to be corrected before they can be read as "each of these orderings holds". This file performs the correction that Appendix A.2 previously only flagged as missing. Correction is needed across **pairs** and not across **conditions**: in a pre-specified direction a false envelope declaration requires one particular condition's one-sided bound to fail; accounting for both directions gives total level alpha, conditional on valid component bounds (Sect. 3.3).

Estimator: Eq. (eq:var), run observation unit, $\alpha = 0.05$. The $z$ for a pair is $\hat\Delta/\mathrm{se}$ at nominal. The envelope declares only when every condition agrees. Its bidirectional IUT $p$ is $\min(1,2\min\{\max_z p_z^+,\max_z p_z^-\})$: the maximum one-sided $p$ within each direction, followed by a two-direction correction. For same-sign estimates this equals the largest two-sided component $p$; mixed-sign estimates give $p=1$ before Holm. With valid input $p$ values, Holm controls the family-wise error rate over pairs without an independence assumption, which matters because these pairs share policy data. Benjamini-Hochberg is printed beside it because the choice between a family-wise and a false-discovery reading is a choice about what the table claims, not a technicality.

| task | pair | $n$ | point $\Delta$ [95%] | $p$ | Holm | BH | envelope | IUT $p$ | Holm | BH |
|---|---|---:|---|---:|---|---|---|---:|---|---|
| eggplant (ms3) | `octo-small` vs `octo-base` | 64 | +0.055 [-0.008, +0.117] | 8.68e-02 | no | no | [-0.008, +0.244] | 8.68e-02 | no | no |
| eggplant (ms3) | `octo-small` vs `octo-small@hist1` | 64 | +0.072 [+0.009, +0.135] | 2.49e-02 | no | yes | [+0.009, +0.237] | 2.49e-02 | no | yes |
| eggplant (ms3) | `octo-small` vs `octo-base@hist1` | 64 | +0.128 [+0.066, +0.190] | 4.75e-05 | **yes** | yes | [+0.012, +0.245] | 2.06e-02 | no | yes |
| eggplant (ms3) | `octo-small` vs `openvla-7b-4bit` | 64 | +0.328 [+0.264, +0.393] | 2.25e-23 | **yes** | yes | [+0.173, +0.504] | 1.13e-15 | **yes** | yes |
| eggplant (ms3) | `octo-base` vs `octo-small@hist1` | 64 | +0.017 [-0.048, +0.082] | 6.04e-01 | no | no | [-0.145, +0.156] | 1.00e+00 | no | no |
| eggplant (ms3) | `octo-base` vs `octo-base@hist1` | 64 | +0.073 [+0.010, +0.137] | 2.43e-02 | no | yes | [-0.064, +0.137] | 1.00e+00 | no | no |
| eggplant (ms3) | `octo-base` vs `openvla-7b-4bit` | 64 | +0.273 [+0.207, +0.340] | 8.65e-16 | **yes** | yes | [+0.066, +0.422] | 2.69e-05 | **yes** | yes |
| eggplant (ms3) | `octo-small@hist1` vs `octo-base@hist1` | 64 | +0.056 [-0.008, +0.120] | 8.54e-02 | no | no | [-0.159, +0.146] | 1.00e+00 | no | no |
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

| standard applied over the 17 pairs | point declares | envelope declares | point declares, envelope abstains |
|---|---:|---:|---:|
| no correction across pairs | 11 | 10 | **1** |
| Holm at $\alpha$ = 0.05 | 9 | 5 | **4** |
| Benjamini-Hochberg at 0.05 | 11 | 10 | **1** |

The last column is the quantity the manuscript reports, and it is the one to read. Under a common error-control standard across pairs the two rules disagree on **4 of 17** pairs, not 1: the correction removes more of the envelope's declarations than of point calibration's, so it turns agreements into disagreements. Quoting only the envelope's own fall from 10 to 5 drops that comparison.

What this does **not** show is that the extra abstentions are corrections. They are abstentions. Without the true ordering for these pairs we cannot say whether each one avoided a false declaration or gave up a correct one, and the two rules are answering different questions in any case -- one about a single setting, one about agreement across a set of settings. What is established is that a declaration is sensitive to the parameter set and to the error-control standard; that a set-valued rule improves real-world decision accuracy is not established here and we do not claim it.

Pairs on which the two rules disagree after Holm: `octo-small` vs `octo-base@hist1` (eggplant (ms3)); `octo-base@hist1` vs `openvla-7b-4bit` (eggplant (ms3)); `octo-small` vs `octo-base` (spoon (ms3)); `octo-small` vs `octo-base` (spoon (ms2, original stack)).

Point declarations that do not survive Holm: `octo-small` vs `octo-small@hist1` (eggplant (ms3), lower bound +0.0091); `octo-base` vs `octo-base@hist1` (eggplant (ms3), lower bound +0.0095).

Envelope declarations that do not survive Holm: `octo-small` vs `octo-small@hist1` (eggplant (ms3), envelope bound +0.0091); `octo-small` vs `octo-base@hist1` (eggplant (ms3), envelope bound +0.0117); `octo-base@hist1` vs `openvla-7b-4bit` (eggplant (ms3), envelope bound +0.0174); `octo-small` vs `octo-base` (spoon (ms3), envelope bound +0.0351); `octo-small` vs `octo-base` (spoon (ms2, original stack), envelope bound +0.0375).

The knife-edge declarations of Sect. 7.2 are the ones to watch here: a bound of $+0.0091$ or $+0.0095$ carries a $p$ far too large to survive a step-down procedure over 17 hypotheses, which is the concrete form of the caveat in Appendix A.2. Whether the corrected or the uncorrected count is the right one to quote depends on what is being claimed -- a reader interested in one named pair wants the uncorrected interval, a reader who scans the table for whichever orderings it declares wants the corrected one -- and we report both rather than choosing for them.
