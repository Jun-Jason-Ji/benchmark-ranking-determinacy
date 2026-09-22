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
| `results/**/*.jsonl` | 832 files, 22.7 MB: one line per episode, with the outcome and the `info` counters |
| `results/**/runs.jsonl` | append-only provenance: port branch, inference-stack version, seeds, per run |
| `results/replay_sysid*/**/*.npz` | 14,064 files, 59.7 MB: per-episode replay trajectories, the evidence for the exact-invariance claim |
| `results/**/analysis_*.md` | script-generated tables |
| `results/**/FINDING_*.md` | hand-written conclusions, including the retractions |
| `results/CORE_TABLE.md` | the point-versus-set verdict table, regenerable |
| `docs/` | manuscript drafts and the formal error ledger |
| `submission/autonomous_robots/` | the manuscript as submitted, with its figures |
| `SHA256SUMS.txt` | checksums for the 1,069 record files, so a reader can confirm nothing drifted |

Captured stderr (`results/**/*.err`, 57.8 MB) is excluded. It is build noise; the provenance claim
rests on `runs.jsonl`.

## Regenerating the tables and figures

Every number in the manuscript is computed from the episode records rather than typed in, so the
tables and figures can be rebuilt without re-running any evaluation:

```bash
python scripts/make_core_table.py                  # results/CORE_TABLE.md (the 18-row per-pair table)
python scripts/analyze_compatible_set_v2.py        # the compatible set (results/COMPATIBLE_SET.md)
python scripts/rebuild_compatible_set.py --stack ms3   # full candidate table, switchable rule
python scripts/make_table5.py --root results/controller_sweep_ms2_official_stream \
       --compare results/controller_sweep_ms2_official     # Tables 4-5, both RNG lifecycles
python scripts/analyze_fractal_reversal.py         # the real-vs-sim reversal pair (Sect. 8.4)
python scripts/analyze_torque_shift_s5.py          # the per-pair torque shift at S = 5 (Sect. 7.3)
python scripts/analyze_benchmark_value.py          # benchmark-value estimator and intervals
python scripts/analyze_platform_drift.py           # implementation-build drift
python scripts/audit_exact_invariance.py           # torque-limit invariance, bitwise per episode (Table 1)
python scripts/analyze_declaration_replication.py  # affirmative vs abstain replication (Table 8)
python scripts/make_table7.py --cache track_s --compare track_s_smax2   # Table 7, both strip extents
python scripts/make_figures.py                     # Figures 1 and 4
python scripts/make_figures_v2.py                  # Figures 2 and 3
python scripts/analyze_response_surface_v2.py      # Figure 6 and the restricted simultaneous band
python benchmark/decidability_bench/run_track_s.py --redraw   # Figure 5, from cached cells
python scripts/export_submission_figures.py        # all six as journal-geometry EPS
```

Several of these exist because a claim needed to be stated at the resolution the data support rather
than one step beyond it. `audit_exact_invariance.py` counts bitwise-identical replays per episode,
which `check_iso_invariance.py` cannot do because it reports millimetres and a difference of
1e-12 m prints as 0.000 mm. `analyze_declaration_replication.py` separates replicated declarations
from agreed abstentions, which the stability column of Table 8 conflates. `make_table7.py` prints the
coverage table for both strip extents, because narrowing the strip changes the ground truth and
therefore every method's coverage, not only the band's. `make_table5.py` generates Tables 4 and 5,
which had been computed by hand and so could not be re-derived when the RNG lifecycle changed.

**`analyze_compatible_set.py` is superseded and should not be used for the set.** It read the
40-demonstration directory, fixed `nominal` as the test reference -- which makes nominal's own loss
increase zero by construction, so the procedure could never reject it -- and took a 2.5% quantile
where the text says one-sided 5%. `analyze_compatible_set_v2.py` replaces it; see the next section
for why the answer changes.

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

## The compatible set: state the reference point, or the test cannot reject anything

The inverted test needs four things named -- a search domain, a loss, a reference and a threshold --
and the answer moves with all four. Getting the reference wrong is the failure that hides itself,
because testing every candidate against `nominal` makes nominal's own loss increase identically zero
and no threshold can then exclude it. Tested against the grid's loss minimiser instead, on the
98 common demonstrations:

| | ManiSkill3 | original stack |
|---|---|---|
| loss minimiser over the 50-point grid | `s2_d0.5_delay1` | `s2_d0.5_delay1` |
| nominal − minimiser, paired mean | +2.90 mm | +2.26 mm |
| one-sided 5% lower bound | **+2.25 mm** | **+1.49 mm** |
| nominal retained at threshold 0? | no | no |

Both stacks independently prefer the same setting, and it is not the one the simulator ships with.

Two further points that took us longer than they should have:

**The loss factorises.** Grouping the 50 grid points by (d/k ratio, execution delay) gives 26
groups. Within a group, varying the common gain scale fourfold moves the mean loss by at most
7.2 µm; between groups the range is 60 mm. The calibration objective is flat along the common scale
and steep along ratio and delay -- which is the paper's structural-blindness result, measured on the
objective rather than on a trajectory.

**The zero threshold degenerates on a deterministic simulator.** Replay is deterministic, so the only
randomness is which demonstrations were drawn, and with 98 paired demonstrations the bootstrap
resolves mean differences of order 1e-7 m. At threshold 0 the rule rejects iso ×2 and ×4, whose mean
loss differs from nominal by 0.5 and 0.7 **nanometres**, and as the demonstration count grows the set
shrinks to the single argmin whatever the physics. Significance is the wrong question for a
difference that carries no noise. A tolerance with an external basis is the fix, and the protocol
supplies one: the two stacks, implementing the *same* nominal dynamics, disagree by **1.356 mm**
(95% CI [0.614, 2.103]). Below that, a parameter effect cannot be told apart from a change of port.
Against that tolerance the invariant directions are retained by factors of 440 and 75 000, while
nominal remains excluded -- so the invariance results are threshold-independent and nominal's status
is genuinely borderline. `rebuild_compatible_set.py --tol` takes the tolerance as an argument and
prints the one that would be needed to retain any candidate, so it has to be named and defended
rather than inherited.

## The RNG lifecycle is part of the protocol, not an implementation detail

Matching a reference protocol's outer loop is not the same as matching the protocol. The SIMPLER
bridge script runs `--obj-episode-range 0 24` for `init_rng` in {0, 2, 4}, and it is natural to read
`init_rng` as a per-episode seed. It is not. `simpler_env/policies/octo/octo_model.py` seeds
`jax.random.PRNGKey(init_rng)` in `__init__`, advances it at every step, and its `reset()` restores
the task, image history, ensembler and sticky-gripper state while never touching the key. One stream
therefore runs through every step of every episode of a run, and a run's 72 episodes carry 72
distinct noise realisations.

Our first reproduction sent the seed on every reset and `octo_policy_server.py` re-seeded on receipt,
so all 24 configurations in a run replayed **one identical noise realisation**. Three modes now
exist, and the flag names say which is which:

```bash
--policy-seed-stream S    # seed once, one stream advances: the reference lifecycle
--policy-seed-fixed S     # seed every reset, re-seeding each episode: NOT the reference
                          # (kept only to regenerate results/controller_sweep_ms2_official)
# default                 # policy_seed_base + episode_id: independent per episode, our own sweeps
```

The server echoes what it actually did (`rng_mode`: `reseed` or `continue`) and the sweep asserts it
on every episode, because the failure was silent: an un-patched server coerces a null seed to 0 and
produces plausible numbers under the wrong protocol.

What it changed, on the same 576 episodes:

| | re-seeding | reference lifecycle |
|---|---:|---:|
| mean abs difference from published | 0.026 | 0.038 |
| mean signed difference (95% CI) | −0.005 [−0.033, +0.022] | **−0.038 [−0.074, −0.002]** |
| across-run range of a cell's rate | 0.109 | 0.052 |
| cells below the published value | 5/8 | 7/8 |
| carrot Δ (published +0.014) | **−0.056** | **+0.028** |

The worse-agreeing number is the trustworthy one. Re-seeding made each run a single noise draw
replicated across the grid, which inflated the across-run variance; a noisier estimator landing
closer to a target is not evidence of fidelity, and the systematic platform offset was there all
along where the first run could not resolve it. The carrot row is why this matters beyond
bookkeeping: we had published a sign reversal that the corrected lifecycle does not reproduce.

`scripts/analyze_official_protocol.py --compare` and `scripts/make_table5.py --compare` print both
directories side by side.

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
