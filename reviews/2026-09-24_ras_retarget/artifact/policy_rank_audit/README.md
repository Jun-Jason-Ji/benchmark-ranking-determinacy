# policy-rank-audit

A small local Python package for a **declared finite configuration census** evaluated repeatedly under a **single implementation build**. It is a reusable reporting and decision component, not an automatic adapter for arbitrary robot benchmarks. The synthetic examples are not experimental evidence.

## Install and run

Python 3.10 or newer; no runtime dependencies. From this directory:

```sh
python -m pip install .
policy-rank-audit audit examples/complete.csv --manifest examples/manifest.json --out complete_audit.json
policy-rank-audit allocate examples/allocation.json --out allocation.json
python -m unittest discover -s tests -v
```

A locally built wheel is supplied under `dist/` when present. This package is not published on PyPI. For an offline environment with setuptools already installed, use `python -m pip install --no-build-isolation --no-deps .`.

## Required data and declarations

CSV columns must be exactly:

```text
task,policy,condition,configuration,replicate,success
```

`success` is binary. Each observation key must be unique. A `replicate` identifies **one complete independent run over every expected configuration for that policy and condition**, not a single episode, reset seed, or a different initial configuration.

The required JSON manifest records:

- `metadata.build`: the single implementation build used throughout this input.
- `metadata.estimand`: `equal_configuration_mean_success_difference`.
- `metadata.replicate_unit`: `complete_independent_census_run`.
- Explicit Boolean assertions `independent_runs` and `independent_policy_evaluations`.
- For each task: the complete predeclared policy, condition, configuration and replicate inventories. This first version uses one common configuration and run inventory per task.

The manifest is a declaration, not automatic proof that raw records share a build or that seeds create independent runs. False independence declarations cannot be detected from success indicators alone. Do not relabel correlated episodes as independent complete runs. Shared replicate IDs between policies are labels only and do not cause paired inference.

## Statistical scope

1. **Completeness first.** Every policy × condition × configuration × replicate cell in the manifest must exist. Unknown IDs and duplicate keys are rejected. Missing cells cause all pairs in the affected task to return `abstain_unsupported`, with no complete envelope and no intervals. A partial grid cannot silently count as a complete census.
2. **Equal configuration weights.** A run score is the arithmetic mean of the binary outcomes over the manifest's configurations. The policy estimate is the mean of its complete run scores. The gap subtracts the two policy estimates.
3. **Variance at the run level.** For R independent complete census runs, the variance contribution is the sample variance of run scores divided by R. The two policies' contributions are added under the explicitly declared independence assumption. Dependence within a run is allowed; treating all its configurations as independent repeat runs is not.
4. **Minimum replication is not a guarantee.** Fewer than two declared runs, missing independence support, or zero empirical variance yields unsupported abstention. Positive variance with at least two runs permits a **normal working-model** interval. Small R may give poor approximation: the package does not promise finite-sample coverage or silently turn zero variance into certainty.
5. **One common direction.** For each condition, the signed gap and standard error give one-sided normal p values. A directional intersection–union test takes the maximum p value across conditions separately for each direction, then applies a factor of two for choosing either direction. Strong positive and negative effects in different conditions must abstain.
6. **Full family correction.** Holm adjustment covers every manifest policy pair across every task; unsupported pairs remain in the family with p=1. No independence between conditions or policy pairs is assumed by the IUT/Holm combination. Its validity is still conditional on valid component p values.

The reported envelope is the smallest lower and largest upper condition interval. It addresses all **enumerated** conditions, not an unobserved continuous parameter domain. These intervals are simulation-side or data-model intervals; they do not bound sim-to-real bias or certify a real-robot ranking.

Exit code 2 indicates malformed input or incomplete inventory; the latter still writes a diagnostic JSON. A complete input that lacks statistical support produces a successful diagnostic report with `abstain_unsupported`, not a manufactured confidence interval. Input hashes are recorded in every report.

## Allocation subcommand

The input supplies a total budget B and strata with IDs, target weights w, pilot standard deviations sigma, and per-run costs c. Nonnegative weights must sum to one; costs must be positive. Under independent stratum sampling and fixed pilot variances, the package solves the continuous problem

```text
minimise sum_i (w_i sigma_i)^2 / n_i
subject to sum_i c_i n_i = B

n_i = B w_i sigma_i / [sqrt(c_i) sum_j w_j sigma_j sqrt(c_j)]
```

This is cost-weighted Neyman allocation for a specified weighted mean. Fractional n values are deliberate. Integer rounding, minimum repeats, fixed setup costs, uncertain pilot variance, task/configuration selection, ranking errors and simulator-bias reduction are outside the optimisation. It is **not** a universal optimal robot experiment, sample-size calculator or power guarantee. All-zero pilot variation is rejected; a zero pilot estimate is not proof of deterministic performance.

## Verification

The small test suite targets failure modes that change conclusions: missing inventory, duplicate observations, disguised configuration pseudo-replication, one-run and zero-variance inputs, unsupported independence, mixed-sign IUT evidence, preservation of the Holm family, and the allocation cost/optimality constraints. See `checks/verification.json` for the local installation, CLI and test results.

This artifact adds a reusable, explicit analysis interface. It does not establish cross-benchmark generality. The manuscript's historical primary analyses retain their documented estimands and uncertainty units; this new tool must not be described as having rerun or replaced those analyses without an explicit export and validation step.
