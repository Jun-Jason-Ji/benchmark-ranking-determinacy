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
| `results/**/*.jsonl` | 871 files, 24.1 MB: one line per episode, with the outcome and the `info` counters |
| `results/**/runs.jsonl` | append-only provenance: port branch, inference-stack version, seeds, per run |
| `results/replay_sysid*/**/*.npz` | 15436 files, 65.6 MB: per-episode replay trajectories, the evidence for the exact-invariance claim |
| `results/**/analysis_*.md` | script-generated tables |
| `results/**/FINDING_*.md` | hand-written conclusions, including the retractions |
| `results/CORE_TABLE.md` | the point-versus-set verdict table, regenerable |
| `results/MULTIPLICITY.md` | the same 17 pairs with a family-wise correction, regenerable |
| `docs/` | manuscript drafts and the formal error ledger |
| `submission/autonomous_robots/` | the manuscript as submitted, with its figures |
| `SHA256SUMS.txt` | checksums for the record files of this version (count in its header), so a reader can confirm nothing drifted |

Captured stderr (`results/**/*.err`, 57.8 MB) is excluded. It is build noise; the provenance claim
rests on `runs.jsonl`.

**File counts refer to the tagged version, not to the working tree.** From v1.2.0 onward each
release has added evaluation data, so the counts above and the header of `SHA256SUMS.txt` are
properties of a specific tag and the versions are no longer interchangeable. If a sweep is still
running when you read this, the working tree will hold more records than the manifest lists and
`sha256sum -c` will report those as missing from the manifest rather than as corrupt. Regenerate the
manifest only at a freeze point, and cite the version DOI for the numbers in a paper rather than the
concept DOI.

## Regenerating the tables and figures

Every number in the manuscript is computed from the episode records rather than typed in, so the
tables and figures can be rebuilt without re-running any evaluation:

```bash
python scripts/make_core_table.py                  # results/CORE_TABLE.md (the 18-row per-pair table)
python scripts/analyze_compatible_set_v2.py        # the compatible set (results/COMPATIBLE_SET.md)
python scripts/rebuild_compatible_set.py --stack ms3   # full candidate table, switchable rule
python scripts/make_table5.py --root results/controller_sweep_ms2_official_stream \
       --compare results/controller_sweep_ms2_official     # Tables 4-5, both RNG lifecycles
python scripts/analyze_fitted_point.py             # nominal vs the calibration-preferred setting
python scripts/analyze_multiplicity.py             # Holm/BH over the 17 bridge pairs (Sect. 7.2)
python scripts/plan_real_robot_trial.py            # power table for the Sect. 9 validation plan
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

## The replay loss is composite, and is not a length

Every replay-loss number in this file and in the paper is the mean over timesteps of
`||p_t - p_hat_t||_2` in metres **plus** `arcsin(||R_t - R_hat_t||_F / (2*sqrt(2)))` in radians. It
adds a translation to a rotation, weighting one radian as one metre, so it has no unit and it is not
a distance. Earlier versions of this file, of the paper and of `analyze_compatible_set_v2.py`
multiplied it by 1000 and printed "mm" (and by 1e6 and printed "um"), which is not a meaningful
operation; those renderings have been replaced by plain scientific notation. Where a genuine length
is meant -- a maximum end-effector position difference, or the translation part of a composite value
quoted on its own -- the unit is stated explicitly. Composite values do not compare with lengths.

## The compatible set: state the reference point, or the test cannot reject anything

The inverted test needs four things named -- a search domain, a loss, a reference and a threshold --
and the answer moves with all four. Getting the reference wrong is the failure that hides itself,
because testing every candidate against `nominal` makes nominal's own loss increase identically zero
and no threshold can then exclude it. Tested against the grid's loss minimiser instead, on the
98 common demonstrations:

| | ManiSkill3 | original stack |
|---|---|---|
| loss minimiser over the 50-point grid | `s2_d0.5_delay1` | `s2_d0.5_delay1` |
| nominal − minimiser, paired mean | +2.90e−3 | +2.26e−3 |
| one-sided 5% lower bound | **+2.25e−3** | **+1.49e−3** |
| nominal retained at threshold 0? | no | no |

Both stacks independently prefer the same setting, and it is not the one the simulator ships with.

Two further points that took us longer than they should have:

**The loss factorises.** Grouping the 50 grid points by (d/k ratio, execution delay) gives 26
groups. Within a group, varying the common gain scale fourfold moves the mean loss by at most
7.2e−6; between groups the range is 6.0e−2. The calibration objective is flat along the common scale
and steep along ratio and delay -- which is the paper's structural-blindness result, measured on the
objective rather than on a trajectory.

**The zero threshold degenerates on a deterministic simulator.** Replay is deterministic, so the only
randomness is which demonstrations were drawn, and with 98 paired demonstrations the bootstrap
resolves mean differences of order 1e−7. At threshold 0 the rule rejects iso ×2 and ×4, whose mean
loss differs from nominal by 4.9e−7 and 7.4e−7, and as the demonstration count grows the set
shrinks to the single argmin whatever the physics. Significance is the wrong question for a
difference that carries no noise. A tolerance with an external basis is the fix, and the protocol
supplies one: the two stacks, implementing the *same* nominal dynamics, disagree by **1.356e−3**
(95% CI [0.614, 2.103]e−3; 0.47 mm of translation plus 0.88 mrad of rotation). Below that, a parameter effect cannot be told apart from a change of port.
Against that tolerance the invariant directions are retained by factors of 440 and 75 000, while
nominal remains excluded -- so the invariance results are threshold-independent and nominal's status
is genuinely borderline. `rebuild_compatible_set.py --tol` takes the tolerance as an argument and
prints the one that would be needed to retain any candidate, so it has to be named and defended
rather than inherited.

## The operating point is a free parameter, and it decides verdicts

The set above rejects the simulator's shipped controller setting, which is also the setting at which
every published rate and every number in this project is computed. `queue_fitted_point.py` measures
what that costs: the complete 64-configuration eggplant census at `(k x2, d x0.5, delay 1)`, three
seed sets with bases matching census sets A'/C/D, so the comparison is paired on configuration and
on policy seed (identical episode ids 0-63, identical seeds on all 64 -- checked, not assumed).

| operating point | Δ | point 95% | matched set |
|---|---:|---|---|
| nominal (shipped) | +0.073 | [−0.016, +0.161] abstain | [−0.016, +0.167] abstain |
| fitted (minimiser) | +0.104 | [+0.016, +0.192] **declare** | [+0.009, +0.192] **declare** |

Both flip, on a Δ shift of only 0.031 -- under half the ±0.088 half-width at this budget. Nominal's
lower bound sat at −0.016; a 0.032 move carries it over zero.

Two things worth carrying forward if you extend this:

**The union bound cannot help here, by construction.** It ranges over the calibration-*invisible*
directions. These two settings differ in the ratio and the delay, which the calibration data
*identify*. A union over the invisible fibre is silent about a move along an identified axis.

**Match the fibres before comparing them.** The common-scale invariance is verified in 14 of the
grid's 26 (ratio, delay) groups across seven ratios, to 7.2e−6 -- but ratio 0.25 has one grid point
per delay, so at the fitted ratio it is unverified and the fitted fibre admits only the torque limit.
`analyze_fitted_point.py` therefore reports the nominal side over both its full six-condition fibre
and the matching two, and refuses any condition that is not a complete census: an envelope is a
min/max, so one partial condition moves the bound with nothing to show it did. That guard exists
because a partial run briefly produced [+0.0000, +0.1920] and the opposite conclusion.

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

`scripts/analyze_official_protocol.py` now defaults to the reference-lifecycle directory
(`results/controller_sweep_ms2_official_stream`), so running it with no arguments reproduces the
paper's Table 4 -- mean difference -0.038, mean absolute 0.038, largest 0.111. It previously
defaulted to the re-seeding directory, which meant the no-argument invocation printed the numbers
the paper reports as an artefact of our own error. Pass
`--root results/controller_sweep_ms2_official` for that run, or `--compare <the other root>` to get
both side by side; `scripts/make_table5.py --compare` does the same for Table 5.

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
