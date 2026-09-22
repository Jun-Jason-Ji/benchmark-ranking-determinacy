# Reproducibility

Companion to *What Determines a Simulation Benchmark Ranking?* This file is the source for
Appendix D of the manuscript; the two should be kept in step.

This is a **code-and-aggregate release**. It contains every per-episode record behind every table and
figure, the analysis scripts that turn those records into the tables and figures, and the platform
compatibility work. It does **not** contain policy checkpoints, simulator assets, or the vendored
third-party simulator trees — those come from their own upstreams, listed in `NOTICE.md`.

## What is here

| Path | Contents |
|---|---|
| `scripts/` | evaluation harness, the six resumable queues, every analysis script |
| `benchmark/` | the synthetic decidability track (Track S) and the real-replicate track (Track R) |
| `results/**/*.jsonl` | 784 files, 22.3 MB: one line per episode, with the outcome and the `info` counters |
| `results/**/runs.jsonl` | append-only provenance: port branch, inference-stack version, seeds, per run |
| `results/replay_sysid*/**/*.npz` | 14,064 files, 59.7 MB: per-episode replay trajectories, the evidence for the exact-invariance claim |
| `results/**/analysis_*.md` | script-generated tables |
| `results/**/FINDING_*.md` | hand-written conclusions, including the retractions |
| `results/CORE_TABLE.md` | the point-versus-set verdict table, regenerable |
| `docs/` | manuscript drafts and the formal error ledger |
| `submission/autonomous_robots/` | the manuscript as submitted, with its figures |
| `SHA256SUMS.txt` | checksums for the record files, so a reader can confirm nothing drifted |

Captured stderr (`results/**/*.err`, 57.8 MB) is excluded. It is build noise; the provenance claim
rests on `runs.jsonl`.

## Regenerating the tables and figures

Every number in the manuscript is computed from the episode records rather than typed in, so the
tables and figures can be rebuilt without re-running any evaluation:

```bash
python scripts/make_core_table.py                  # results/CORE_TABLE.md (Table 6)
python scripts/analyze_compatible_set.py           # the compatible-set verdicts
python scripts/analyze_fractal_reversal.py         # the real-vs-sim reversal pair (Sect. 8.4)
python scripts/analyze_torque_shift_s5.py          # the per-pair torque shift at S = 5 (Sect. 7.3)
python scripts/analyze_benchmark_value.py          # benchmark-value estimator and intervals
python scripts/analyze_platform_drift.py           # implementation-build drift
python scripts/make_figures.py                     # Figures 1 and 4
python scripts/make_figures_v2.py                  # Figures 2 and 3
python scripts/analyze_response_surface.py         # Figure 6
python benchmark/decidability_bench/run_track_s.py --redraw   # Figure 5, from cached cells
python scripts/export_submission_figures.py        # all six as journal-geometry EPS
```

`export_submission_figures.py` also audits each figure against the journal's requirements (174 mm
full-column width, lettering at 8 pt or more) and reports any violation rather than emitting a
figure that breaches them silently.

## Re-running the evaluations

Only needed to reproduce the records themselves, not the analysis. Two simulator stacks are involved
and they are **not** interchangeable — their configuration grids differ, so per-episode comparison
between them is undefined for the eggplant task (Sect. 5.1):

- **Original reference stack** (ManiSkill2 + SAPIEN 2.2.2), used for the published-protocol
  reproduction of Sect. 6 and the fractal work of Sect. 8.4. Runs headless on a host without a GPU
  through the Vulkan compatibility layer in `third_party/vk_fakesemfd/` (Appendix B).
- **ManiSkill3 port**, used for the controller sweeps.

Requirements are pinned in `requirements-*-lock.txt`. The queues are resumable: each skips episode
ids already present in the target `.jsonl`, so an interrupted run costs only the episode in flight.

## Two things a re-runner should expect

**Enumerate the configuration grid, do not sample it.** `episode_id` determines the initial state
modulo the grid size — 24, 64 or 300 depending on task and port — so episodes past that count are
exact repeats. `scripts/task_configs.py` exposes the mapping.

**Policy seeds are a replication axis only for policies that consume them.** Octo's diffusion head
does; OpenVLA decodes greedily and ignores the seed, so its "seed sets" are record-identical repeat
runs and must be merged into one observation, not averaged as independent draws.

## Comparing across directories: pair on shared episode ids

This one cost us a day, so it is worth stating plainly. The record directories hold different
numbers of episodes -- the pre-fix build and seed set B hold 96 where the others hold 64 -- and
because `episode_id` wraps onto the configuration grid, ids 64-95 land back on configs 0-31. A
per-configuration mean taken over each directory's own full contents therefore averages two
observations for half the grid on one side and one apiece on the other. That is not a paired
comparison, and both across-build and across-seed quantities are paired by definition.

Computed the wrong way, the implementation-build drift reads 0.055 and sits *below* policy-seed
noise; paired on shared ids it is 0.078 and sits above it, which is the ordering the manuscript
asserts. `scripts/analyze_platform_drift_paired.py` prints both columns side by side, and both
estimators in `scripts/make_figures_v2.py` now restrict to shared ids.

Any new cross-directory comparison should do the same.
