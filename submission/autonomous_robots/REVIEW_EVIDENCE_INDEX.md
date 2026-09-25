# Review evidence index

This index is a navigation aid for the frozen manuscript and its companion data/code snapshot.
It does not add a claim, validate a real-world ordering, or replace the limitations in the paper.
Use the companion snapshot's inventory and checksums to identify the inputs; a public concept DOI
or an earlier archived version does not establish that it contains the same records.

## What the paper establishes

| Claim | Measurement and scope | Analysis entry point | Boundary |
|---|---|---|---|
| Calibration and policy-comparison sensitivity differ | Octo-Small versus Octo-Base; MS3 eggplant, all 64 configurations, five seed sets. Estimated gaps range 0.0546875–0.17421875, a span of 0.11953125. The table's replay bounds are from MS2, explicitly identified separately. | `scripts/make_evidence_chain.py`; `results/EVIDENCE_CHAIN.md`; manuscript label `tab6a` | Both nominal and set-valued rules abstain on this pair. A span of point estimates is not a paired-effect confidence interval or a real-world ranking reversal. |
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
The command runs six existing CPU analyses, records their source and
output hashes, writes separate logs and stops on failure. It does not run policies, launch services,
download checkpoints or write to `results/`. The regenerated `FITTED_POINT.md` contains both
completed operating-point comparisons.
See `REPRODUCIBILITY.md` for further analyses and the original evaluation instructions.

## Reproduction map: analysis entry points moved out of the typeset manuscript

This map preserves the executable entry points formerly printed in prose and captions. The
locations below are stable LaTeX labels in `main.tex`, rather than printed section or table numbers.
Paths and command-line options were checked against the frozen companion source on 23 September
2026; **the commands in this expanded map were not executed as part of the typesetting revision**.
The six-analysis runner above has its separately recorded reproduction checks. A command's presence
here is not a claim that it was re-tested in this revision.

Run commands from the companion root using the recorded analysis dependencies. Preserve the frozen
snapshot: set `PYTHONDONTWRITEBYTECODE=1`, and use a separate writable working copy for the individual
commands below. Several original entry points write to `results/` or to the manuscript figure
directory by default. Where `--out` is supported, the examples redirect reports to a pre-created
sibling `../analysis-output/` directory; this does not change the scientific inputs. Avoid importing
scripts merely to inspect them: some perform analysis at module scope. Rebuilding analysis outputs
requires no policy server, GPU inference or new robot trials.

### Recorded-data analyses and statistical diagnostics

| Manuscript location (LaTeX label) | Inputs and purpose | Entry point / explicit options |
|---|---|---|
| `subsec3_2`: reference-selection bias | Synthetic equal-risk candidates; diagnostic of selecting and testing the reference on the same demonstrations, not new policy evaluation. Prints to stdout. | `python scripts/check_selection_bias.py --candidates 50 --demos 98 --boot 1000 --reps 1000 --alpha 0.05` |
| `subsec4_3`, `tab1`: measured replay invariance | Saved replay arrays from the two stacks; reports exact equality and nonzero residuals separately. Prints to stdout. | `python scripts/audit_exact_invariance.py --a nominal --b force_x0.5` |
| `subsec4_4`, `secA1`: replay-compatible set and loss structure | The 98-demonstration replay grids; composite loss, not a length. | `python scripts/analyze_compatible_set_v2.py --out ../analysis-output/COMPATIBLE_SET.md` |
| `subsec4_4`, `secA1`: explicit candidate test | `results/replay_sysid_100/grid` for `ms3`, `results/replay_sysid_ms2/grid` for `ms2`; printed candidate table. | `python scripts/rebuild_compatible_set.py --stack ms3 --loss mean_total_err --ref best --alpha 0.05 --tol 0 --boot 10000 --seed 0 --top 50`; replace `--stack ms3` with `--stack ms2` for the original stack. |
| `subsec3_2`, `subsec4_4`, `secA1`: held-out reference selection and tolerance sensitivity | Same replay grids. Selection and testing use disjoint demonstration halves under `--split`. An externally justified margin can be passed as `--tol`; it is not an automatic engineering tolerance. | Add `--split --split-seed 0` to the preceding command for one recorded split convention; use `--split-seed` to specify further splits explicitly. `--tol 0` is the stated zero-margin rule. `--ref nominal` reproduces the historical reference choice, not the current primary rule. |
| `subsec5_5`, `tab3`, `subsec6_2`: policy-seed variability | Eggplant records; default current-build seed sets, per-pair shared episode IDs. The script's 0.068 statistic has its own ID intersection, distinct from the common-to-all-five-sets scope in `tab3`. | `python scripts/analyze_seed_noise.py --env PutEggplantInBasketScene-v1 --conditions nominal,force_x0.5 --out ../analysis-output/SEED_NOISE.md` |
| `subsec5_5`, `tab3`: implementation-build drift | Pre-fix and current-build records, paired on shared episode IDs. Reports the unpaired diagnostic too; use the paired calculation for the manuscript. | `python scripts/analyze_platform_drift_paired.py --out ../analysis-output/BUILD_DRIFT_PAIRED.md` |
| `sec6`, `tab4`: reference-protocol reproduction | Original-stack reference-stream records and published benchmark rates; optional comparison with per-episode re-seeding. `--compare` requires a directory argument. | `python scripts/analyze_official_protocol.py --root results/controller_sweep_ms2_official_stream --compare results/controller_sweep_ms2_official --out ../analysis-output/OFFICIAL_PROTOCOL_COMPARE.md` |
| `subsec6_3`, `tab5`: uncertainty at the reference budget | The same two original-stack record roots; prints the estimates under both RNG lifecycles and variance models. | `python scripts/make_table5.py --root results/controller_sweep_ms2_official_stream --compare results/controller_sweep_ms2_official` |
| `subsec7_1b`, `tab6a`: calibration-to-policy evidence chain | Saved replay summaries and current-build policy census. The replay and policy columns retain their distinct simulator provenance. | `python scripts/make_evidence_chain.py --out ../analysis-output/EVIDENCE_CHAIN.md` |
| `subsec7_2`, `tab6`: per-pair decision table | Episode records selected by policy family and stack; current nominal/set rules, configuration counts and variance model. | `python scripts/make_core_table.py --unit run --out ../analysis-output/CORE_TABLE.md` |
| `subsec7_2`: observation-unit sensitivity | Same selected records; aggregate within directory before the alternative variance calculation. | `python scripts/make_core_table.py --unit directory --out ../analysis-output/CORE_TABLE_DIRECTORY.md` |
| `subsec7_2`, `tab6`: three-versus-five seed-set budgets | Same code and run observation unit; `--max-sets 3` limits the seed-set selection. The default `--max-sets 0` means no limit, not zero evaluated sets. | `python scripts/make_core_table.py --unit run --max-sets 3 --out ../analysis-output/CORE_TABLE_THREE_SETS.md`; compare with the unrestricted run-unit command above. |
| `subsec7_2`, `tab6b`: multiplicity across policy pairs | The 17 Bridge pair statistics, with the stated variance assumptions. | `python scripts/analyze_multiplicity.py --alpha 0.05 --out ../analysis-output/MULTIPLICITY.md` |
| `subsec7_3`: cross-family torque shifts | Eggplant census, five Octo seed sets; record-identical deterministic repeats are deduplicated. | `python scripts/analyze_torque_shift_s5.py --out ../analysis-output/TORQUE_SHIFT_S5.md` |
| `subsec7_4`, `fig3`: current configuration-level torque decomposition | The same run-deduplication rule and current inputs as the figure; JSON records input hashes. Do not substitute older three-seed mechanism summaries. | `python scripts/analyze_torque_scope_current.py --out ../analysis-output/TORQUE_SCOPE_CURRENT.json` |
| `subsec7_7`, `tab10`: matched operating-point censuses | Complete eggplant and spoon data, all six conditions at each operating point; same-policy seed matching. The code checks each condition, excludes incomplete conditions and explicitly marks any resulting reduced-condition envelope as partial; it does not universally refuse the entire comparison. | `python scripts/analyze_fitted_point.py --out ../analysis-output/FITTED_POINT.md`; `python scripts/analyze_fitted_point.py --selftest` separately exercises the per-condition completeness check with temporary fixtures. |
| `subsec8_2`, `tab7`: synthetic coverage, error and power | Cached `results/benchmark/track_s/track_s_results.json` and `results/benchmark/track_s_smax2/track_s_results.json`; prints both strip extents. This does not rerun the synthetic experiment. | `python scripts/make_table7.py --cache track_s --compare track_s_smax2` |
| `subsec8_2`, `fig6`: exploratory response-surface band | Older pre-fix sweep with 24–96 paired episodes per design point, not a uniformly weighted census; see Supplementary Material S1. This script writes its report and figure under their original locations in a working copy. | `python scripts/analyze_response_surface_v2.py` |
| `subsec8_3`, `tab8`: replicated declarations versus agreed abstentions | `results/benchmark/track_r/track_r_summary.md`; prints the decomposition of stability. | `python scripts/analyze_declaration_replication.py` |
| `subsec8_4`, `tab9`: selected opposite published mean orderings | `results/fractal_reversal/` records; comparison with the cited published real means does not supply their missing intervals. | `python scripts/analyze_fractal_reversal.py --n-boot 20000 --out ../analysis-output/FRACTAL_REVERSAL.md` |
| `sec9`, `tab:power`: indicative real-trial budget | Assumed rates 0.853 and 0.920, independent Bernoulli trials, equal allocation, normal approximation; no real trials are executed. Counts are per policy. Prints to stdout. | `python scripts/plan_real_robot_trial.py --p1 0.853 --p2 0.920 --n 200 400 800` |
| `secC`, `tabC1`: complete per-cell counts | The core table's record reduction and configuration mapping; prints LaTeX and also writes `results/appendix_c_table.tex` in the working copy. | `python scripts/make_appendix_c.py` |

**Superseded entry point.** `scripts/analyze_compatible_set.py` is present for historical
traceability, not for rebuilding the current compatible set. Its own docstring records the
40-demonstration input, fixed-nominal reference and incorrect tail-quantile handling. Use
`scripts/analyze_compatible_set_v2.py` and `scripts/rebuild_compatible_set.py` above. Likewise,
`--legacy-a` on the core-table or seed-noise script deliberately admits older Octo build data and
is not part of the current primary analysis.

### Additional audit record outside the companion snapshot

For `subsec8_4`, the project-local supporting census of published real/simulated policy pairs is
`research_audit/published_pairwise_audit.md`. This file exists in the project source but is **not
included in the frozen companion snapshot** identified below. It is an auxiliary audit locator,
not a new dataset in that snapshot; the manuscript cites the benchmark source of the published
rates. Removing this long path from the typeset prose does not change the audit count or identify
this unbundled file as a submitted companion input. No archive was changed to add it.

### Figure reconstruction

These entry points regenerate plots from saved records or cached synthetic cells and write files
in a **working copy**. They do not collect new robot or simulator episodes.

| Manuscript figure label | Entry point | Output role |
|---|---|---|
| `fig1`, `fig4` | `python scripts/make_figures.py` | Replay identifiability and policy-gap-by-condition plots. |
| `fig2`, `fig3` | `python scripts/make_figures_v2.py` | Uncertainty budget and torque effect by orientation; paired/shared-ID and deterministic-run reductions are defined in this source. |
| `fig5` | `python benchmark/decidability_bench/run_track_s.py --redraw --out results/benchmark/track_s` | Redraw from the existing cache; omitting `--redraw` runs the synthetic experiment instead. |
| `fig6` | `python scripts/analyze_response_surface_v2.py` | Exploratory simultaneous-band plot from the older sweep, with its stated scope. |
| `fig1` through `fig6` | `python scripts/export_submission_figures.py` | Re-renders all six at the manuscript geometry, exports EPS to `submission/autonomous_robots/` and writes proof images; checks lettering and geometry. It invokes the underlying figure routines and can also write their original plots. |

### Re-collecting evaluations and the optional original-stack rendering layer

This is a different operation from regenerating the tables. It requires policy checkpoints,
simulator assets, the relevant simulator environment and the policy inference endpoint. The
companion does not bundle those third-party environments. Original-stack and ManiSkill3 grids are
not interchangeable. The reference original-stack evaluations can use CPU physics and software
rendering; policy inference has its own resource requirements. None of these services or
rendering settings is required by the recorded-data commands above.

For `subsec6_1` and `sec6`, `scripts/queue_ms2_official_stream.py` is the resumable original-stack
collection entry point; its source configures the policy endpoints and output roots and must be
adapted to the re-runner's environment before execution. It invokes
`scripts/controller_sweep_ms2.py` using `--policy-seed-stream S`: seed once, then continue the
stream across episodes. `--policy-seed-fixed S` instead re-seeds on every episode and corresponds
to the historical comparison, not the reference protocol. The no-fixed/stream mode uses
`--policy-seed-base` with episode IDs for the project's independent-per-episode sweeps.
`scripts/octo_policy_server.py` echoes the applied lifecycle and the sweep checks it. These
collection entry points write episode/provenance records and may perform substantial inference;
they were not run during this typesetting revision.

For `secB`, the implementation details removed from the paper are supplied in
`docs/software_rendering_compatibility.md`. The current companion also contains the actual
source, original build script and explicit-layer manifest under `third_party/vk_fakesemfd/`.
The note gives the API-to-implementation mapping, creation-chain restrictions, error-returning
descriptor functions and a relocatable build/activation template. The archived build script
contains author-specific paths; use a prepared working copy and adapt the paths.

The layer is restricted to the tested software-rendering path, which transfers host-memory
images to a separate policy server. It does not implement external synchronization; no complete
call trace establishes that the descriptor functions were never reached. Its validity remains
conditional on the workload not requiring that capability. It is enabled through the evaluation
process environment, inherited by child processes, without system-wide installation. No build,
service or environment change was performed during this document revision.

The frozen `REPRODUCIBILITY.md` remains a useful source of environment and historical-protocol
instructions, but some narrative examples describe earlier partial designs. For current result
scope and inclusion rules, use the current manuscript, this index and the current analysis outputs;
do not substitute a historical example for the completed two-task censuses.

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

The current companion snapshot contains 16,858 selected source files
(16,863 files including metadata). Relative to the department-affiliation snapshot,
the changed files are the directional-IUT analysis and the submission packaging script.
The corrected cached multiplicity report is supplied in the separate S1 provenance-source archive.
All experimental records are byte-identical. The corrected analysis changes three
input envelope p values but preserves all reported 17-pair declaration counts. The current S1 provenance
archive is supplied separately with the manuscript, including the source records for the four early
candidates and the 39 Figure 6 design cells. The package builder verified both source captures,
the complete copied inventory and checksums.

- `DATA_SHA256SUMS.txt`: `4df336b3f35a9a32dcd7fc16f8002fbb150a910a049306759e4071a3424618e0`
- `REVIEW_PACKAGE_SHA256SUMS.txt`: `6e3537608702bedb48f0efaa85eda747dc9ed2c28c6e08bc4bbd966bae61d68c`

The latest public version verified on 23 September 2026 is v1.1.3, DOI 10.5281/zenodo.22896508. This exact snapshot has not been newly published. Authors can provide both
review packages as submission materials or deposit them separately and record the resulting
version-specific identifier. The official annual journal classification required by the institution
is also an author-side eligibility check; this package does not assert that it has been verified.

## Final citation and mechanism checks

`REFERENCE_VERIFICATION.md` lists the 24 verified works and the 16 DOI identities. The Figure 3
configuration decomposition is included in the six-analysis reproduction entry point as
`TORQUE_SCOPE_CURRENT.json`. It uses the same run deduplication as the figure, with five Octo seed
sets: Octo-small has 20 improved, 28 unchanged and 16 degraded configurations, with three positive
orientation means. OpenVLA's orientation range is −0.0625 to +0.2917 and its change/nominal-rate
correlation is −0.4504. Historical three-seed summaries must not replace this current calculation.

## Final editorial consistency corrections

The present snapshot incorporates an existing-data consistency audit. These are substantive
attribution corrections as well as prose edits; no new policy evaluation or calibration run was made.

- Figure 1(a) now plots the labelled damping/stiffness ratio as `d/k = 1/s`, where `s` is the
  stiffness multiplier and damping is fixed. The input values and confidence intervals are unchanged.
  Table 1 and Section 4.3 agree: ratio ×0.5 has a replay-loss increase of about 0.0064;
  ratio ×2 has an increase of about 0.0089. `scripts/make_figures.py` contains the correction.
- Section 7.5 uses the current run observation unit, including nominal +0.073, density's interval
  [−0.024, +0.108], and friction's small negative estimate −0.00052. There is no resolved
  between-condition sign reversal. Current point/set verdicts are unchanged.
- Appendix D assigns the lifecycle summaries consistently with Section 6: re-seeding/reference
  mean across-run ranges are 0.109/0.052, and differences from published rates are −0.005/−0.038.
- Scope statements now distinguish three policy families, seven principal configurations and five
  tasks from restricted subsets. Current shared three-task cross-stack comparisons agree in both
  point and set verdicts. Table/column references, exploratory-study boundaries and causal wording
  were corrected without adding evidence.

The earlier editorial correction left all experimental records unchanged. The preceding
figure/appendix revision also leaves those records unchanged, redraws Figure 1 from the same
paired losses, and adds the small compatibility-layer source/build/manifest and its implementation
note to the companion. The packaging and Figure 1 scripts are the only changed existing source
files relative to the preceding editorial snapshot. The supplied audit records the complete diff
and verification results. Historical summaries remain provenance records rather than substitutes
for the current analysis scope; the reference-verification archive retains its citation identities.

All four current affiliations use institution, city/region and country, without postal codes.
Yizhou Zhao’s affiliation is Sino-French Institute, Renmin University of China, Suzhou, China;
Shengjie Guo’s is College of Computer and Information Engineering, Inner Mongolia Agricultural
University, Hohhot, China. The Chinese reading version names 中法学院 and 计算机与信息工程学院, respectively. The English title is typeset once as a full-width first page, followed
by the journal's two-column body. Author order, institutional identities, email, ORCID and the
latest seven-author contribution assignments are unchanged.

The current caption revision gives all six figures and fourteen tables concise topic titles.
Essential reading instructions and validity boundaries remain next to the relevant figure or
table; longer result interpretations appear in the surrounding body. Figure 6 still identifies
its older inference stack, 24–96 paired episodes per design point and episode-level standard errors, while
its posterior-draw details and bounds appear in Section 8.2. The synthetic-results note
distinguishes extrema over all cells from declaration-rate averages over decidable-truth cells.
Appendix C distinguishes nonuniform replication from the uniformly five-run torque condition.
Figure 4's colour wording and incomplete ranking labels in Tables 5 and 6 are corrected.
All numerical table entries, displayed equations, figure assets, citation calls, author fields
and the abstract are preserved. English and Chinese PDFs have been rebuilt and visually checked.

## Current format review

The generative-AI disclosure is now an independent unnumbered section after the
conclusion in both languages. A duplicate competing-interest sentence was removed from the
otherwise empty acknowledgements; the formal declaration remains after the references.
The interface instructions distinguish the two mandatory contribution/interest fields from
manuscript declarations and do not imply that the system has been filled or author approval obtained.
The current class is byte-identical to the officially linked template; figure width settings are
retained because they fit the 160 mm text area. Figure 6's low-resolution raster components were
re-exported from the same numeric arrays, with all points, axes, colormap, interpolation and bounds
preserved. Figures 1–5, table values, formulas, bibliography, author roles and affiliations are unchanged.
The separate format-review audit records source comparisons, effective image resolution and visual QA.

## Previous typography checks

The abstract's inherited bold mathematics is corrected locally in both preambles, with the
official class unchanged. The preceding prose cleanup removed 137 English and 134 Chinese
rhetorical emphasis wrappers, retaining exact wording, notation and inference qualifications.
The current table review also removes 14 selectively bold wrappers from eight tables in each
language. Their captions and notes did not define a shared meaning for bold data. Counts,
differences, intervals, selected verdicts and the selected union-row label now use regular weight.
Table captions, column headings, task group labels and rules retain their structural formatting.

At the preceding table-weight stage, only those eight table pages changed their character/font/position signature in each PDF;
all other pages match the preceding version exactly. All table values, text, equations,
references, figure assets and author information are preserved. The eight modified pages
in each language have been visually checked after rebuilding. Previous audits document
their respective historical stages; this section records the preceding typography stage.

That typography stage reused the format-reviewed companion byte-for-byte. The preceding terminology revision rebuilt the companion; the source keys and statistical estimators remain unchanged.

AI statement revision (23 September 2026): the first sentence now reads exactly: "Large language models (OpenAI ChatGPT/Codex) assisted with manuscript revision, analysis scripts." The quantitative-results and author-responsibility sentences are preserved. The interface declaration and Chinese reading version are synchronized.

## Manuscript terminology and implementation mapping (24 September 2026)

The manuscript describes sampling and physical settings in scientific terms. Internal keys and
record organization are preserved. The following mapping makes the prose, records and commands traceable:

| Manuscript term | Implementation identifier | Meaning and scope |
| --- | --- | --- |
| Policy seed initializing one complete reference run | `init_rng`, CLI `--octo-init-rng` | Reference Bridge runs use 0, 2 and 4. The Octo constructor initializes the PRNG key once (including its warm-up splits); episode reset does not reset it. Source: `third_party/SimplerEnv/simpler_env/policies/octo/octo_model.py` and `third_party/SimplerEnv/scripts/octo_bridge.sh`. Stream advancement alone does not establish episode independence. |
| Episode index, e | `episode_id` | Integer index mapped onto the position/orientation grid by the unchanged modulo arithmetic. The reference range `0 24` is upper-exclusive: indices 0–23. |
| Offset for consecutive episode indices | evaluation `seed` plus loop index | The port's default 100-episode schedule need not align with a complete number of grid enumerations. The offset is `args.seed` (default 0); see `third_party/SimplerEnv-ms3/simpler_env/real2sim_eval_maniskill3.py` (default `num_envs=1`, `num_episodes=100`). |
| Episode policy seed in the census records | `policy_seed = base + episode_id` | Applies to these census records. It is distinct from the reference run-level advancing-stream lifecycle. |
| Robot texture variant | `urdf_version` | Four robot recolourings; visual/material differences without changes to the tested physical parameters. |
| Nominal | `nominal` | Baseline setting. |
| Gain scale ×0.25 / ×4 | `iso_x0.25`, `iso_x4.0` | Arm-joint stiffness and damping multiplied by the same factor. |
| Torque limit ×0.5 | `force_x0.5` | Arm-joint drive torque limits halved; not an applied external force or a change to the gripper limit. |
| Friction ×0.4 | `fric_x0.4` | Object static and dynamic friction coefficients scaled together. |
| Density ×0.5 | `dens_x0.5` | Object density halved at fixed geometry. |
| Seed sets (Sets) | seed-set directories in `make_core_table.py` | One group corresponds to one directory. The count is the number of groups with records for the policy/task/condition, not the per-configuration episode count. |
| Seed-set mean | `--unit directory` | Mean of episodes at one fixed configuration within one seed set; the resulting mean is one sensitivity-analysis observation. The primary `--unit run` uses individual episodes. Deterministic duplicate-run rules are unchanged. |
| GP simultaneous band | `gp_sim` in Track S | The same simultaneous GP band and numerical results, with a reader-facing legend. |
| Per-release corrections | `CHANGELOG.md` | Historical changes to claims, units, estimator implementation and supporting documentation. |
| Third-party terms | `NOTICE.md` | Component sources, licences and upstream terms; the notice is not itself a new licence. |

The server reports `rng_mode` in `scripts/octo_policy_server.py`; `scripts/controller_sweep_ms2.py`
asserts the expected mode in reference-stream evaluation. `scripts/queue_ms2_official_stream.py`
schedules that mode. The historical failure treated an absent seed as zero,
unintentionally restarting the random stream. The reference-stream evaluation checks the applied lifecycle on reset; the per-episode-reseeding comparison is not claimed to use the same assertion.
Appendix D retains the sampling consequence; this index retains the implementation detail.
`scripts/analyze_fitted_point.py --selftest` checks completeness handling and partial envelopes.
The torque-decomposition output records input hashes. Resumable evaluation queues skip episode IDs
already present in their output records. These implementation details do not change any estimator.

Display labels are centralized in `scripts/paper_labels.py`; `scripts/make_appendix_c.py` and the
Figure 4 generator use the same mapping. The Figure 5 generator changes method labels only.
The raw condition keys, episode records, statistical calculations and interval endpoints are unchanged.

## Journal-style revision (24 September 2026)

Eight legally available Autonomous Robots articles informed an editorial comparison. The manuscript
now uses concise topic headings, reduced metacommentary and an explicit distinction between the
union envelope (the interval across evaluated settings) and the probability union bound. Legacy
analysis keys and historical output names remain unchanged. Neither name denotes a new estimator.
The maximum-absolute build shift in Figure 2 is distinguished from its signed shift in Table 3.
Mechanistic explanations of torque effects are described as consistent with the observations;
the wording does not infer an unmeasured saturation boundary. All 14 table numeric sequences,
displayed equations, citation identities, abstract, authorship and declarations are unchanged.
The comparison literature is a local writing resource, not part of the submitted research evidence.

## Reader-facing model and task names (24 September 2026)

The manuscript uses ordinary prose names. Record keys and executable arguments retain their
original spelling. These mappings preserve exact reproducibility without printing implementation
identifiers repeatedly in the paper.

| Manuscript name | Record/configuration key | Meaning |
|---|---|---|
| RT-1 (Converged) | `rt-1-converged` | RT-1 checkpoint trained to convergence |
| RT-1 (15%) | `rt-1-15pct` | RT-1 checkpoint at approximately 15% of the training steps |
| RT-1-X | `rt-1-x` | RT-1-X policy |
| Octo-Small | `octo-small` | Small model, default observation history |
| Octo-Base | `octo-base` | Base model, default observation history |
| Octo-Small (single-frame history) | `octo-small@hist1` | Same model with a single observation frame |
| Octo-Base (single-frame history) | `octo-base@hist1` | Same model with a single observation frame |
| OpenVLA | `openvla` (analysis alias), `openvla-7b-4bit` (implementation) | The evaluated 7B model, using 4-bit quantisation as disclosed in the manuscript |
| Coke-can grasping | `pick-coke-can` | Google Robot can-grasping task |
| Cube stacking | `stack cube` / `stack` | Stack green on yellow cube |

Compact tables define S as Octo-Small and B as Octo-Base. The history-comparison table also defines
B1 as Octo-Base with single-frame history and V as OpenVLA. Those upright model abbreviations are
distinct from the mathematical seed count S. The names follow the SIMPLER paper's checkpoint
definitions: https://jiajunwu.com/papers/simpler_corl.pdf, Section 5.1. The local checkpoint mapping
is preserved in `scripts/fetch_rt1_checkpoints.py` and the upstream README. A 15% training-stage
checkpoint does not mean training on 15% of the dataset. No new literature reference or DOI was added.

## Manuscript-only layout and punctuation update (24 September 2026)

Table 2 now uses one natural-width centred block for its title, body and note. Its task-name mapping appears in the main text.
Prose dash insertions were rewritten without changing scientific values, mathematical expressions, references or evidence scope.
That earlier layout-only update reused its then-current companion archive and introduced no experimental-record, analysis-script or figure-asset change. The subsequent S1/statistical revision below uses a new companion snapshot.

## Supplementary Material S1: analysis provenance and revision history

The former Appendix E is now `supplementary_provenance.pdf`, accompanied by its editable source
and `supplementary_provenance_sources.zip`. It remains part of the submission evidence.
The source archive includes the exact historical reports, execution logs and episode records;
the two inventories resolve IDs S01–S18/R01–R19 and G01–G06/GR01–GR78 with SHA-256 hashes.
Historical report wording is retained as provenance and is not a substitute for the revised paper.

- C1 and C4 are opposite-point-estimate candidates; C2 and C3 are declaration/abstention differences.
  Their 24→48/96 extensions add policy observations on the same 24 configurations.
- The C4 quarantine/clean-rerun chronology and the limits of pre-selection provenance are explicit.
- The carrot interval [-0.039,+0.094] belongs to reproduced +0.028, not published +0.014.
- The empirical compatible set, nominal-ratio evaluation strip and GP posterior grid are distinguished.
  Figure 6 uses 24–96 paired episodes per design point; some eggplant cells have partial coverage,
  and 96-episode cells have unequal configuration weights.
- Directional intersection–union p values are formed before across-pair adjustment. Seven targeted
  regressions pass. Three input p values change; counts remain 11/10/1, 9/5/4 and 11/10/1.
  The corrected code travels in the current companion snapshot. Its cached report is supplied as
  `reviews/2026-09-24_appendix_provenance/MULTIPLICITY_CORRECTED.md` in the S1 source archive,
  and the reproduction command above regenerates it from the companion inputs.

This revision does not retarget the journal template, submit a manuscript, or publish a new release.
Autonomous Robots is not eligible for a CAS major-category Q2-or-above requirement under the
publicly cross-checked 2025 table. RAS is a proposed major-category Q2, non-TOP alternative;
institutional eligibility and journal-specific preparation remain separate decisions.
