# Review evidence index

This index is a navigation aid for the frozen manuscript and its companion data/code snapshot.
It does not add a claim, validate a real-world ordering, or replace the limitations in the paper.
Use the companion snapshot's inventory and checksums to identify the inputs; a public concept DOI
or an earlier archived version does not establish that it contains the same records.

## What the paper establishes

| Claim | Measurement and scope | Analysis entry point | Boundary |
|---|---|---|---|
| Calibration and policy-comparison sensitivity differ | Octo-small versus Octo-base; MS3 eggplant, all 64 configurations, five seed sets. Estimated gaps range 0.0546875–0.17421875, a span of 0.11953125. The table's replay bounds are from MS2, explicitly identified separately. | `scripts/make_evidence_chain.py`; `results/EVIDENCE_CHAIN.md`; manuscript label `tab6a` | Both nominal and set-valued rules abstain on this pair. A span of point estimates is not a paired-effect confidence interval or a real-world ranking reversal. |
| The finite evaluation population matters | Task grids contain 24–300 configurations; two ports can enumerate different populations. Repeated policy evaluations are distinguished from configuration sampling. | `scripts/task_configs.py`; Section 5; configuration/provenance records | A census removes configuration sampling error only for the stated finite population, not policy randomness or deployment uncertainty. |
| Declaration counts depend on inference scope | Across 17 bridge pairs, unadjusted point/set counts are 11/10; Holm-adjusted counts are 9/5, with four additional set abstentions. | `scripts/analyze_multiplicity.py`; `results/MULTIPLICITY.md` | Input p values rely on the stated normal approximation and variance treatment. Four abstentions are not four confirmed error corrections. |
| Operating-point sensitivity differs between the two tasks measured | Both operating points have all six conditions on both tasks. Eggplant: gap shift +0.0313; both envelopes abstain. Spoon: gap 0.3958→0.1250, paired shift −0.2708 with primary 95% interval [−0.4580, −0.0837]; both point and set verdicts change from declaration to abstention. | `scripts/analyze_fitted_point.py`; `results/FITTED_POINT.md`; manuscript label `tab10` | Eggplant's paired-shift interval includes zero. Spoon has only two seed blocks; its block sensitivity interval has one degree of freedom. No exact small-sample coverage is claimed. The 98 demonstrations are not certified as the original fitting sample. |
| The published budget need not resolve each reported ordering | Correct reference RNG lifecycle; 72 episodes per cell; one or two of four orderings resolved depending on the variance model. | `scripts/analyze_official_protocol.py`; `results/controller_sweep_ms2_official_stream/` | A protocol reproduction and budget diagnosis, not a verified real-robot reversal. |

The separate torque comparison across four Octo/OpenVLA pairs has shifts 0.104–0.146
(mean 0.121). It must not be substituted for the effect on the first row's Octo/Octo pair.
The completed eggplant and spoon comparisons are both included in the frozen companion snapshot.
Their matched comparison design contains 120 condition/policy/seed files with 5,760 episode records:
64 configurations at three seed sets for eggplant and 24 configurations at two for spoon.

## Reproduce the main decision tables

From the root of the companion data/code snapshot, with the recorded Python analysis dependencies:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
python scripts/reproduce_review_evidence.py --out ../review-reproduction
```

On POSIX shells, prefix the Python command with `PYTHONDONTWRITEBYTECODE=1` instead. This environment
setting is inherited by the analysis subprocesses and prevents cache files from changing the
verified snapshot. Alternatively, run in a working copy. The output path must be new.
The command runs five existing CPU analyses, records their source and
output hashes, writes separate logs and stops on failure. It does not run policies, launch services,
download checkpoints or write to `results/`. The regenerated `FITTED_POINT.md` contains both
completed operating-point comparisons.
See `REPRODUCIBILITY.md` for further analyses and the original evaluation instructions.

## Interpret the statistical statements

For a fixed finite parameter set and valid equal-tailed 95% component intervals, a false declaration
in a pre-specified direction has probability at most 0.025. A rule that may declare either direction
has any-false-declaration probability at most 0.05. The outer interval covers the true range over
that finite set with probability at least 0.95. These statements do not cover unsampled parameter
values, invalidate the paper's variance caveats, or confer a sim-to-real guarantee.

The proposed physical validation is an unexecuted plan. Its sample-size illustration gives power
approximately 0.565/0.852/0.989 at 200/400/800 trials **per policy**, under the explicitly stated
independent-Bernoulli and normal-approximation assumptions. It is not evidence that a future result
will reverse a simulated ranking.

## Release boundary

The manuscript snapshot contains the PDF, editable sources, bibliography, figures, cover letter,
interface declarations and this index. The companion snapshot separately contains the selected
records, replay trajectories, scripts and dependencies documented by its manifest. Its inclusion of
historical or quarantined records is for traceability, not permission to treat every record as an
analysis observation. The existing scripts define filtering and completeness rules.

The final companion snapshot contains 16,848 selected source files (16,853 files including package
metadata), and was verified again after the five analyses were reproduced. Its identifiers are:

- `DATA_SHA256SUMS.txt`: `c3235d8d566ecf2c48b8a3db2b177053e53dba8116ff0ba896e7fd470699bfc0`
- `REVIEW_PACKAGE_SHA256SUMS.txt`: `378865873233e665bc5c14d5eb7217e7f11aa396f4b26e23949cd6cdb64d0c27`

Current public deposition of this exact snapshot has not been verified. Authors can provide both
review packages as submission materials or deposit them separately and record the resulting
version-specific identifier. The official annual journal classification required by the institution
is also an author-side eligibility check; this package does not assert that it has been verified.
