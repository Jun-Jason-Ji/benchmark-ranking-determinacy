# Public real-evaluation and correlation audit

Date: 2026-09-24. This is a retrospective analysis of public summaries, not a new robot experiment, held-out validation, or cross-benchmark replication. The Chinese manuscript was not modified.

## Decision for the manuscript

Add a short counts-only sensitivity analysis to the English real-evaluation section, and retain the full source inventory, per-task correlation table and model assumptions in the supplement. Correct the claim that trial budgets are unavailable. Do not claim that this audit refutes SIMPLER's correlation result or confirms a reversal of the underlying real/simulated ordering.

The useful conclusion is that strong across-policy correlation and an unresolved particular policy comparison can coexist. This limitation is already discussed qualitatively by SIMPLER; our increment is the numerical audit at the policy pair used by this manuscript, with transparent count and design assumptions.

## Sources and provenance

All three official source files are frozen at commit `06accaca93535902d408da4855f21cece12bceb7`, dated 2025-12-20. They were downloaded from GitHub at that commit, rather than copied from an untracked local edit. SHA-256 values are in `analysis.json`.

- Aggregate real and simulated rates, and metric definitions: [metrics.py](https://github.com/simpler-env/SimplerEnv/blob/06accaca93535902d408da4855f21cece12bceb7/simpler_env/utils/metrics.py).
- Real task budgets and coke orientation rates: [evaluation source](https://github.com/simpler-env/SimplerEnv/blob/06accaca93535902d408da4855f21cece12bceb7/tools/calc_metrics_evaluation_videos.py).
- Per-task metric driver: [calc_metrics.py](https://github.com/simpler-env/SimplerEnv/blob/06accaca93535902d408da4855f21cece12bceb7/tools/calc_metrics.py).
- Protocol: [formal CoRL paper, Appendix A, printed pages 15–16](https://jiajunwu.com/papers/simpler_corl.pdf). The PDF is downloaded locally for verification. The appendix specifies coke 75, move-near 60, opening/closing 27 each, apple 27, and each WidowX task 24 real trials. These are real-evaluation budgets, not the larger seed/texture-aggregated simulation budgets.

The existing `li2024simpler` reference is sufficient for these data, with the fixed source URL retained in the evidence index. Verified optional methodological references are supplied in `verified_methods.bib`.

## Count reconstruction is conditional, not recovery of raw trials

The public table has 42 task/policy cells over nine task rows (opening and closing are separate rows). At the stated task budgets, 41 rates have exactly one integer count within half a unit of their three-decimal rounding. A matching count is compatible with the publication, not proof that a particular cohort or exclusion rule generated the table.

The exception is eggplant / Octo-Small: 0.400 cannot equal a rounded integer fraction with denominator 24. The script flags it and does not manufacture a count by rounding 9.6 to 10. Inferences involving this cell are excluded. The other eggplant cells remain explicitly conditional on the stated budget/cohort mapping.

No synthetic binary arrays are treated as raw logs. In particular, the upstream `construct_unordered_trial_results` creates an unordered list from rounded totals. It does not preserve paired configurations, sessions, exclusions, or trial chronology.

## Five opposite published mean directions

Excluding RT-2-X only for the public-checkpoint analysis reproduces the manuscript's 62 within-task pairs: five opposite mean directions and three ties in at least one domain. For descriptive correlations, RT-2-X is retained because its public labels are usable even though its weights cannot be rerun.

The following are *nominal 95% Newcombe intervals under two independent, identically distributed binomial samples and the assumed budget-to-cohort mapping*. They are approximate model-conditional intervals, not a familywise assertion and not source-published intervals.

| Task; first policy minus second | Compatible counts | Real difference | Conditional 95% interval |
|---|---:|---:|---:|
| Coke; RT-1 Converged minus RT-1 15% | 64/75 minus 69/75 | −0.0667 | [−0.1729, +0.0380] |
| Move-near; RT-1 Begin minus Octo-Base | 1/60 minus 21/60 | −0.3333 | [−0.4604, −0.2033] |
| Close drawer; RT-1 Converged minus RT-1-X | 25/27 minus 20/27 | +0.1852 | [−0.0191, +0.3802] |
| Close drawer; RT-1 15% minus RT-1-X | 24/27 minus 20/27 | +0.1481 | [−0.0640, +0.3492] |
| Carrot; Octo-Base minus Octo-Small | 6/24 minus 2/24 | +0.1667 | [−0.0515, +0.3746] |

Thus four of the five real-side comparisons remain unresolved under this simple model. This is not evidence that four true reversals are absent. The move-near real-side interval excludes zero, including under the script's per-task Bonferroni/Clopper–Pearson sensitivity, but the public simulated difference is only +0.008 and its sampling uncertainty is not reconstructed here. It would be incorrect to label it a confirmed real/sim ordering reversal.

The full CSV additionally gives per-task simultaneous bounds formed from Clopper–Pearson marginal intervals at error probability 0.05/m, where m is the number of count-compatible policies in that task. Pair bounds subtract marginal endpoints. The union-bound guarantee does not require independence between policies, but the individual binomial models still require justification. These families are defined per task; no claim of simultaneous coverage across all nine tasks is made.

## Coke: account for what the public design actually reveals

The three orientation strata supply stronger provenance than rounded overall rates:

| Orientation | Converged successes / trials | 15% successes / trials |
|---|---:|---:|
| Horizontal | 24/25 | 25/25 |
| Vertical | 22/25 | 24/25 |
| Standing | 18/25 | 20/25 |

The equal-weight average difference is −5/75 = −0.0667. We report several *alternative sensitivity models*, not multiple opportunities to select the most significant result:

1. **Pooled independent binomial working model:** Newcombe interval [−0.1729, +0.0380]. This ignores the fixed orientation/position design, so it must not be presented as the definitive design-based interval.
2. **Orientation-stratified binomial sensitivity:** construct six Clopper–Pearson intervals with error 0.05/6, then average the three policy-difference lower/upper bounds with weights 1/3. The resulting conservative interval is [−0.3887, +0.2806]. It allows dependence across policy cells for the union bound, but still assumes a binomial model within each orientation/policy cell. Fixed position heterogeneity is not eliminated merely by stratifying on orientation.
3. **Independent but non-identically distributed trials:** a union of Hoeffding bounds for the two 75-trial means gives [−0.4085, +0.2752] for the difference in expected averages over those planned evaluation slots. This permits different success probabilities across positions. It still requires trial independence within each policy; unknown session dependence can invalidate that assumption. It gives no coverage for a different deployment distribution.
4. **Hypothetical matched evaluation:** if each policy were evaluated once on the same 25 scenes per orientation, all 2×2 tables consistent with the observed margins have 0–6 Converged-only successes and 5–11 15%-only successes. The seven possible pooled discordant tables produce exact two-sided McNemar p values between 0.0625 and 0.3323. None rejects at 0.05 under the conditional discordant-sign binomial model. Actual pairing has not been verified; heterogeneous or dependent pair outcomes require additional assumptions. This is a bound over possible pairings under a stated test model, not a substitute for actual pairing metadata.

All four treatments leave the coke real ordering unresolved at this level. They cannot establish equality, determine the magnitude of a structural sim-to-real bias, or certify the original trial design.

## Correlation audit: result is not a collapse of the headline

We recompute the upstream metrics task by task, with matched policy identifiers. No mixture of tasks or embodiments is treated as one independent correlation sample; pairwise comparisons are not bootstrapped as independent observations.

| Task row | Policies | Pearson r | MMRV | Opposite means / pairs | Deletion range of r |
|---|---:|---:|---:|---:|---:|
| Coke | 6 | 0.975 | 0.0313 | 3/15 | 0.951–0.994 |
| Move-near | 6 | 0.856 | 0.1110 | 1/15 | 0.854–0.942 |
| Open drawer | 6 | 0.983 | 0.0000 | 0/15 | 0.980–0.996 |
| Close drawer | 6 | 0.771 | 0.1233 | 3/15 | 0.706–0.868 |
| Apple into drawer | 6 | 0.969 | 0.0000 | 0/15 | 0.905–0.988 |
| Spoon | 3 | 0.827 | 0.0000 | 0/3 | Two points: uninformative |
| Carrot | 3 | 0.571 | 0.1113 | 1/3 | Two points: uninformative |
| Cube stacking | 3 | 1.000 | 0.0000 | 0/3 | Two points or constant |
| Eggplant | 3 | 0.989 | 0.0000 | 0/3 | Two points: uninformative |

All published policies give 87 within-task pairs, eight opposite directions and three ties. The main text should keep the existing five-of-62 count for the checkpoint-accessible subset, and explain the different denominator if the full-label analysis is mentioned.

Coke is the clearest concise illustration: r=0.975 remains between 0.951 and 0.994 after deletion of any one policy, yet three of its 15 published policy pairs have opposite directions. Restricting to accessible checkpoints gives r=0.971, MMRV=0.0268 and one opposite pair among ten. Strong correlation is not contradicted; it answers a different question from certifying a particular comparison. MMRV already exposes a nonzero penalty. The manuscript should acknowledge that SIMPLER itself motivates MMRV by discussing limitations of Pearson correlation.

Deletion ranges are deterministic sensitivity summaries over this fixed policy set, not confidence intervals. Three-policy tasks leave only two policies after deletion, making Pearson r exactly ±1 unless one vector is constant; reporting such ranges as evidence of robustness would be misleading.

## Verification and reproduction

Run `analyze_public_evidence.py` using Python 3, with no external numerical package required. Frozen inputs are in `sources/`; outputs are `analysis.json` and four CSV files. No simulator or policy code executes.

The script passes 11 checks, including recovery of the manuscript's 62/5/3 inventory, exclusion of the incompatible eggplant cell, count/rate agreement, interval antisymmetry, boundary cases and the complete pairing range. An independent run with SciPy 1.12.0 checks 432 Clopper–Pearson intervals (maximum absolute difference 4.98×10⁻¹³), all seven McNemar values, and 18 correlation/MMRV rows against SciPy and the frozen upstream functions. See `INDEPENDENT_NUMERICAL_VERIFICATION.json`.

No existing experiment log, manuscript, historical script, or Chinese file was modified by this analysis. `manuscript_insert.tex` is a proposed concise English integration; `supplement_insert.tex` records the extra statistical detail. The parent editor should place the counts/cohort caveat next to the results, not only in a distant limitations paragraph.
