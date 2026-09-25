# Supplement S3: research data and code

This archive accompanies "Auditing robot policy rankings in simulation:
Calibration, initialization, and success criteria" (RAS review manuscript,
25 September 2026). It is the current unpublished reviewer snapshot, not a new
public DOI deposit. Main text and Supplements S1 and S2 are supplied separately.

## Contents

This single archive combines the frozen baseline research inputs, current RAS
study records, analysis code, and relevant scientific provenance. No overlay of
other archives is required. Original relative paths are retained because frozen
analyses reference them; the `reviews/` directory name is a development-era path,
not a collection of referee reports.

| Location | Research material |
|---|---|
| `results/`, `data/`, `scripts/`, `benchmark/` | Replay arrays, historical evaluation records and analysis code |
| `reviews/2026-09-24_ras_retarget/real_counts/` | Public SIMPLER count reconstruction and replay-distance reanalysis |
| `reviews/2026-09-24_ras_retarget/cross_benchmark/` | Native-task discovery data, sources and pinned checkpoint metadata |
| `reviews/2026-09-24_ras_retarget/artifact/` | Reusable ranking-audit component and examples |
| `reviews/2026-09-24_ras_strengthening/confirmatory/` | Independent 20,480-rollout native-task confirmation and frozen plans |
| `reviews/2026-09-24_ras_strengthening/calibration_confirmation_v3/` | Valid 768-rollout spoon operating-point comparison |
| `reviews/2026-09-24_ras_strengthening/calibration_torque_control/` | Additional 384 half-torque rollouts and shared-baseline analyses |
| `reviews/2026-09-24_ras_strengthening/calibration_reset_validation/` | Initial-state validation and recorded states/images |
| `reviews/2026-09-24_ras_strengthening/statistics/` | Historical statistical sensitivity analysis |
| `reviews/2026-09-25_ras_final_review/` | Final descriptive Figure 4 generator, provenance and numerical check |

Frozen plans, amendments, failed or excluded experiment records, technical
protocols and scientific corrections are preserved. The failed sequential-reset
attempt in `calibration_confirmation/` is excluded from confirmatory inference;
historical/discovery data are not pooled with the valid confirmations. Original
stored reports remain dated research records; final interpretation is in the
current main manuscript and supplements. Do not run old queues as reproduction.

Internal editorial/referee simulations, article drafts, cover letters, submission
checklists, email drafts and typography/build review records are omitted. There
are no model weights, simulator asset bundles, downloaded reading-reference
papers, or unpublished real-robot trial logs. Public marginal rates/counts do not
recover real-trial pairing or session structure.

## Verify and reproduce

Extract into a new empty working directory. Run `python verify_manifest.py` to
check every included file against `SHA256SUMS.txt`. The manifest covers all files
except itself. Work on a copy when running analyses; several original analyzers
write derived outputs beside their inputs.

For CPU stored-data analyses, use an isolated environment. The reference versions
are Python 3.11.16, NumPy 1.26.4 and SciPy 1.12.0, recorded in
`reviews/2026-09-24_ras_strengthening/requirements-cpu.txt`. Later SciPy versions
can differ in final quantile digits and consequently in derived-output hashes.
No GPU, policy server, new trial collection or network is needed for these
commands from the extracted root:

```text
python reviews/2026-09-24_ras_strengthening/confirmatory/analyze_portable.py
python reviews/2026-09-24_ras_strengthening/materialize_audit_sources.py
python reviews/2026-09-24_ras_strengthening/calibration_confirmation_v3/analyze_confirmation.py
python reviews/2026-09-24_ras_strengthening/calibration_torque_control/analyze_torque.py
python reviews/2026-09-24_ras_strengthening/calibration_torque_control/episode_level_comparison.py
python reviews/2026-09-24_ras_strengthening/statistics/reanalyze_statistics.py
python reviews/2026-09-24_ras_strengthening/editorial/audit_replay_initialization.py
```

The source-materialization helper supplies only unchanged hashed source files for
the strict analyzer; it does not install a simulator. See the individual study
records for collection/runtime requirements. The earlier discovery analyzer
additionally verifies four public checkpoints, excluded here; its README gives
the pinned download URLs and hashes. The portable confirmation command above
does not require those weights. Plot reproduction additionally requires Matplotlib.

Packaging checks verify archive integrity, byte-preserved scientific inputs and
dependency coverage. Packaging does not constitute new experiments or a fresh
rerun of every statistical analysis. The original analysis verification dates
and their scopes remain in the corresponding records.

## Licenses and provenance

Original code uses the MIT license in `LICENSE`. Third-party terms retain
precedence; see the current `NOTICE.md` and included upstream license/notices
beside source snapshots. The baseline notice in `licenses/` is retained as a
historical record; its old inventory exclusions are superseded by the current
notice and this README. `PACKAGE_PROVENANCE.json` records input archive hashes,
selection scope and dependency checks. No conflicting scientific member was
silently replaced. The project public-release family is distinct from this
unpublished current snapshot.
