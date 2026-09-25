# Statistical strengthening: assumption audit and finite-sample sensitivities

24 September 2026. Frozen SIMPLER records were reanalysed; no original scripts, manuscript files, or raw outcomes were overwritten and no robot/GPU evaluations were performed for this audit. This analysis does not assign or guarantee a manuscript acceptance probability.

## Recommendation for the primary paper

Remove **nine point / five set declarations** from the abstract-level evidence of robustness. Keep it as an explicitly conditional, retrospective normal-model sensitivity in the supplement. Its calculation is reproducible, but the records do not establish the observation-independence or execution-noise assumptions needed to promote the count into assumption-robust evidence. Lead instead with the measured sensitivity magnitudes and the separate prospectively frozen new-scene validation.

Do **not** simply replace 9/5 with 9/4 or 5/1 as the new definitive answer. Those numbers answer different probability-model questions. In particular, the zero sampling variance of a known greedy decoder is legitimate when conditioning on deterministic execution; it does not establish zero execution variability. This audit makes that distinction explicit.

## Two rejection-relevant statistical weaknesses

### P1: within-configuration replication does not capture shared run effects

The main census estimator is an equal-configuration average. Its diagonal variance sum drops cross-configuration and cross-policy covariances. The historical `--unit directory` variant first averages repeated episodes within each directory at each configuration, but then still sums separate configuration variances. It is **not** a whole-run cluster analysis and does not protect against directory-level common shocks. Different policy seed numbers are consistent with the intended per-episode reset design; they are not an empirical test that execution has no shared run effects.

`controller_sweep.py`, `controller_sweep_ms2.py`, and `octo_policy_server.py` document the deliberate per-episode resets for the principal sweeps. The reference-protocol advancing-stream reproduction is a different dataset and is not silently substituted into the 17-pair table. The analyses here distinguish individual episode observations, shared numerical-seed clusters, and complete directory-level censuses.

The complete-block sensitivity computes each block's equal-configuration policy difference **before** estimating variability across blocks. It therefore retains cross-configuration and within-block cross-policy covariances. The same complete block labels are retained across all evaluated settings, based on inventory alone. For the six Octo–Octo eggplant comparisons this leaves four complete blocks, A, C, D and E; B is incomplete in at least one non-nominal setting. The OpenVLA eggplant comparisons have only one complete common block. Original-stack comparisons also have one directory-level block. Some two-block spoon/carrot setting contrasts have zero observed variance; we do not convert that into infinite certainty.

### P1: decoder randomness, execution randomness, and outcome-based de-duplication are different

`openvla_policy_server.py` invokes `predict_action(..., do_sample=False)` and ignores the nominal policy seed in reset. Thus the **decoder** supplies no stochastic action-sampling term. Whether the whole quantised inference/simulation execution is deterministic is a separate question. The frozen records include differing execution outcomes on shared configurations. At four eggplant perturbations only one OpenVLA execution per configuration is available, so execution variance is unmeasured there.

The historical raw-data functions also merge directories when their per-configuration outcome sequences or means happen to agree. This uses the response variable as a de-duplication criterion; equal success outcomes alone do not establish that two executions are the same observation. Actual duplicate records should be identified by run identity and provenance, while absence of policy sampling should be identified from the implementation. These questions should not be decided by observed equality.

Importantly, isolating these two operations shows that **removing only outcome-based directory de-duplication does not change 9/5**. The change to **9/4** occurs when the single-run OpenVLA zero term is replaced with a pooled Bernoulli execution-noise working model. That replacement is an additional unverified model, not a newly discovered empirical variance and not an unconditional correction.

## Full frozen-family comparison

The family is the same 17 bridge policy pairs. Fifteen pairs have six evaluated settings. The two original-stack Octo–OpenVLA pairs have only nominal and half torque; their narrower setting scope is retained explicitly. All conditions require their complete task configuration inventory, with no silent intersection. Each method applies directional IUT before Holm across the entire 17-pair family; unsupported pairs receive p=1 rather than being removed from the family.

| Analysis | Point, before Holm | Set, before Holm | Point, after Holm | Set, after Holm | Interpretation |
|---|---:|---:|---:|---:|---|
| Historical normal model | 11 | 10 | 9 | 5 | Reproduces the submitted calculation |
| Raw executions; historical variance rules retained | 11 | 10 | 9 | 5 | Isolates removal of outcome-based de-duplication |
| Raw executions; pooled execution-noise fallback for single observations | 11 | 10 | 9 | 4 | Additional variance-homogeneity and independent-execution assumptions |
| Weighted episode Hoeffding | 8 | 2 | 5 | 1 | No variance imputation; every included episode assumed independent |
| Shared-seed Hoeffding, stochastic Octo pairs only | 1 | 0 | 0 | 0 | Allows arbitrary dependence across policies sharing a seed; 6 greedy-policy pairs unsupported |
| Whole-directory Hoeffding | 0 | 0 | 0 | 0 | Allows arbitrary dependence within a labelled directory/block; independent blocks still assumed |
| Complete-census block t sensitivity | 3 | 0 | 0 | 0 | Few-block distributional sensitivity, not an exact distribution-free test |

The last three rows are **not evidence that the true policy differences are zero** and are not additional successful demonstrations of the method. They show that this budget cannot simultaneously deliver weaker dependence assumptions and informative family-level declarations. Conversely, the first four rows do not establish that their independence assumptions hold. Complete-block analysis also restricts the data to blocks with every configuration under every evaluated condition and uses an equal-block estimator; its differences from the primary result cannot be attributed solely to a changed standard error.

The episode Hoeffding analysis retains one sampled-set declaration, Octo-Small versus OpenVLA on ManiSkill3 eggplant. It relies on treating the retained execution records as independent; a greedy seed that is ignored cannot by itself justify that assumption. This result should be supplementary sensitivity, not a replacement headline.

## Exact mechanism of 9/5 versus 9/4

The affected pair is **ManiSkill3 eggplant, Octo-Small with one-frame history versus OpenVLA**.

- At gain scale 0.25 the difference is +0.1359375 in both calculations. There are 304 Octo episodes and 64 OpenVLA episodes, exactly one OpenVLA observation at each of the 64 configurations.
- The historical standard error is 0.0224170200, including a zero OpenVLA policy-sampling term.
- Introducing a pooled Bernoulli **execution-noise** fallback raises the standard error to 0.0522158146. The bidirectional IUT p-value becomes 0.009231013 and does not survive Holm.
- The historical worst setting was half torque, with IUT p=0.0000006766400. The extra execution-noise model changes which setting limits the envelope.
- At nominal, retaining all 160 OpenVLA executions instead of the 112 left by outcome-based de-duplication leaves the point estimate unchanged and narrows its standard error. This nominal change is **not** what removes the set declaration.

Relevant scope metadata is `results/controller_sweep_gpu/openvla-7b-4bit/PutEggplantInBasketScene-v1/run_meta.json`: one 64-episode collection on the four perturbations, seed base 20260918, 4-bit OpenVLA, Torch 2.7.1+cu128. It is supporting provenance, not a proof of execution determinism. Every consumed metadata/log file and implementation is pinned in `INPUT_MANIFEST.json`.

## Finite-sample method, without a new theorem claim

Let the equal-configuration contrast be a weighted sum of bounded success indicators, with signed episode weights +1/(N n_A(c)) and -1/(N n_B(c)). Group observations into blocks within which arbitrary dependence is permitted. For each independent block g, its contribution has range width r_g equal to the sum of absolute episode weights in that block. Write R² = sum_g r_g². The classical bounded-sum inequality gives the one-sided null p bound exp(-2 max(d,0)²/R²), with the corresponding negative-direction bound. The two-sided 95% half-width is sqrt(R² log(2/0.05)/2).

For independent episodes each observation is a block. For shared-seed sensitivity, all policy observations bearing the same seed are one block and greedy-policy comparisons are marked unsupported. For directory sensitivity, the whole corresponding seed-set directory across both policies is one block. Cross-setting independence is never required for the directional IUT. Holm additionally does not require pair independence.

These mathematical guarantees require the designated independent blocks, the stated expectation target, and a fixed sampling/analysis design. They are not unconditional coverage claims for retrospectively chosen budgets, pairs, or settings. The existing experiment was developed adaptively, so these results remain model sensitivities. The separate frozen holdout protocol supplies a cleaner confirmatory design.

The bound is classical, not a new contribution: [Hoeffding, 1963](https://www.tandfonline.com/doi/abs/10.1080/01621459.1963.10500830). Few-cluster limitations of variance-based inference are also established; see [Cameron and Miller's author-hosted paper](https://faculty.econ.ucdavis.edu/faculty/cameron/research/Cameron_Miller_JHR_2014_July_09.pdf).

## Known-null stress test

`stress_test_null.py` uses the actual nominal observation inventories of eggplant (64 configurations, 352 episodes per policy, five directories) and spoon (24 configurations, 48 episodes per policy, two directories). It generates new synthetic Bernoulli(0.5) outcomes for both policies, so the true policy gap is exactly zero. These are **not new robot evaluations** or estimates of actual study error rates.

The generator adds independent policy-specific Gaussian shocks per directory before thresholding, with latent correlations 0, 0.05 and 0.20. The resulting within-directory binary correlations are respectively 0, 0.031844 and 0.128188. Each scenario uses 20,000 Monte Carlo draws, RNG seed 20260924. The contrast probability remains 0.5 marginally; only dependence changes.

For eggplant:

| Method | No shared dependence | Binary correlation 0.031844 | Binary correlation 0.128188 |
|---|---:|---:|---:|
| Episode normal | 0.05280 | 0.27785 | 0.53530 |
| Within-configuration directory normal | 0.05280 | 0.26530 | 0.52160 |
| Complete-census block t | 0.05035 | 0.04960 | 0.05275 |
| Independent-episode Hoeffding | 0.00635 | 0.13235 | 0.39335 |
| Whole-directory Hoeffding | 0 | 0 | 0 |

At the intermediate dependence scenario, the Monte Carlo 95% interval for the episode-normal false-declaration rate is [0.27165, 0.28411], and for the complete-block t rate it is [0.04663, 0.05270]. This illustrates why normal calibration or a finite-sample bound does not survive a wrong observation unit. The benign block-t performance here is a property of these synthetic scenarios, not a proof that t inference is exact for arbitrary few-block robot data. In the two-block spoon design it is strongly conservative, especially with the explicit zero-variance abstention rule.

The directory Hoeffding method's zero false declarations is accompanied by zero observed-data declarations. It cannot be described as improving decision utility or confirming real-world rankings. `NULL_STRESS.json` provides all scenarios and exact binomial Monte Carlo intervals. The test concerns single-pair, single-setting error; it is not claimed to estimate the actual 17-pair family-wise error.

## Minimal manuscript edits proposed

1. Remove 9/5 from abstract and contribution bullets. Keep measured effects, scope changes, and the new separately frozen holdout result central.
2. Describe the historical counts in S2 as “conditional normal-model sensitivities”; retain the 9/5 result but add the 9/4 execution-noise sensitivity and its different target. Do not call either definitive error-controlled performance.
3. Replace any assertion that within-configuration directory averaging is conservative against all directory effects with the precise statement that only whole-census blocks retain cross-configuration covariance. The existing reference-budget whole-census analysis remains a separate dataset.
4. Replace “record-identical reruns must be merged” with a provenance-based rule: absence of decoder sampling is determined from the implementation, duplicate records from execution identity, and unexplained execution variation requires replication. Equal successes alone are insufficient.
5. Add the compact method-comparison table and synthetic stress result to S2. Label the all-abstain rows as insufficient informative replication, not avoided real-world errors.

## Reproduce and verify

```powershell
python reviews/2026-09-24_ras_strengthening/statistics/reanalyze_statistics.py
python reviews/2026-09-24_ras_strengthening/statistics/stress_test_null.py
python reviews/2026-09-24_ras_strengthening/statistics/test_statistics.py
```

Python, NumPy and SciPy are required. `ANALYSIS.json` contains every condition, pair, observation count, complete block label, interval and p-value. `PAIR_RESULTS.csv` and `METHOD_COMPARISON.csv` are compact extracts. `INPUT_MANIFEST.json` pins all consumed source files. Eight meaningful checks cover inventory failure, direction selection, bound inversion, shared-seed range accounting, zero-variance abstention, covariance omission, published-family reproduction, and input hashes.
