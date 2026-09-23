# Changelog

Versions are tagged in git and archived on Zenodo. **A tag is a promise**: once Zenodo mints a DOI
for it, that snapshot is permanent.

The manuscript cites the **concept DOI** [`10.5281/zenodo.22893458`](https://doi.org/10.5281/zenodo.22893458), which always resolves to the
newest version, so it does not go stale when a new one is released. Every version keeps its own DOI:

| Version | DOI |
|---|---|
| v1.1.2 | [`10.5281/zenodo.22896200`](https://doi.org/10.5281/zenodo.22896200) |
| v1.1.1 | [`10.5281/zenodo.22896075`](https://doi.org/10.5281/zenodo.22896075) |
| v1.1.0 | [`10.5281/zenodo.22895382`](https://doi.org/10.5281/zenodo.22895382) |
| v1.0.0 | [`10.5281/zenodo.22893459`](https://doi.org/10.5281/zenodo.22893459) |

There are four versions for one result, and the reason is worth stating plainly: v1.0.0 and v1.1.0
chased byte-exactness between the archive and the manuscript by re-tagging, which cannot converge —
a version DOI is minted by the snapshot that contains the manuscript, so the DOI always lands one
commit after the archive it names. v1.1.2 switched the citation to the concept DOI, which ends it.
Nothing about the data changed across any of the four: `SHA256SUMS.txt` is byte-identical
throughout. **v1.2.0 was the first release to add evaluation data**, so its `SHA256SUMS.txt` differs
from the earlier ones by 72 new record files.

## v1.4.0 -- 2026-09-22

Closes the limitation v1.3.0 opened. v1.3.0 established that the benchmark's nominal controller
setting is rejected by its own replay data, and had to leave the consequence unmeasured: every
ranking in the paper is computed at that rejected point. This release measures it.

### The census at the calibration-preferred operating point

`queue_fitted_point.py` runs the complete 64-configuration eggplant census for octo-small and
octo-base at `(k x2, d x0.5, delay 1)` -- the replay loss minimiser on both stacks -- plus the halved
torque limit there. 1,536 episodes, three seed sets whose bases match census sets A'/C/D, so the
comparison is paired on configuration **and** on policy seed: verified identical episode ids 0-63 and
identical seeds on all 64.

| operating point | Δ | point 95% | matched set |
|---|---:|---|---|
| nominal (shipped) | +0.073 | [−0.016, +0.161] abstain | [−0.016, +0.167] abstain |
| fitted (minimiser) | +0.104 | [+0.016, +0.192] **declare** | [+0.009, +0.192] **declare** |

**Both verdicts flip**, and the reason is not a large effect. Δ moves by only 0.031 -- under half the
±0.088 half-width at this budget, a quarter of the 0.121 torque shift. Nominal's lower bound was
already at −0.016, so a 0.032 move in the bound carries it across zero. The fitted declaration rests
on +0.009, inside the knife-edge band the paper marks with a dagger.

The structural point, now §7.7: the union bound **cannot** protect against this. It ranges over the
directions the calibration data leave unconstrained, while nominal and the minimiser differ in the
ratio and the delay -- the directions the data *do* constrain. This is a third kind of ambiguity,
distinct from both events the error ledger tracks: not whether the true parameter is in the set, not
evaluation noise, but that the benchmark is *operated* at a point its own evidence rejects. The
recommendation that follows costs nothing: report the operating point and how it stands against the
calibration objective.

### Two corrections caught by running it

- **A provisional set bound nearly became a published claim.** The first analysis run reported the
  fitted fibre as 2 conditions with bound [+0.0000, +0.1920] while `fitted_force_x0.5` had 14 and 2
  episodes of 64. The completeness guard covered the point estimate but not the fibre, and an
  envelope is a min/max, so one partial condition moves the bound invisibly. `envelope()` now admits
  only complete conditions and names any it excludes. On the complete data the bound is
  [+0.009, +0.192] and **declares**, the opposite of what the partial data suggested -- the draft
  had said "the set-valued verdict does not flip", which was wrong and is now corrected in four
  places.
- **The invariance was understated, not overstated.** §4.4 implied the common-scale result was
  unverified away from nominal. It is verified in 14 of the grid's 26 (ratio, delay) groups across
  seven ratios from 0.5 to 2.0, to within 7.2 µm, identically on both stacks. What is true is
  narrower: ratio 0.25 has exactly one grid point per delay, so at the *fitted* ratio the scale is
  never varied. That is why the fitted fibre has two conditions and not six, and why the nominal side
  is reported cut down to two for the comparison.

New: `queue_fitted_point.py`, `analyze_fitted_point.py`, the `fitted_v1` preset,
`results/FITTED_POINT.md`. `analyze_platform_drift_paired.py` now also emits the shift in Δ
(−0.1094) so its record file matches the corrected Table 3, reproduced from independent code.

---

## v1.3.0 -- 2026-09-22

A second revision pass, and the one that reaches the construction rather than its presentation. The
headline item is that **the compatible set was never computed the way the paper defines it**, and
computing it correctly changes a premise.

### The compatible set, recomputed

`analyze_compatible_set.py` fixed `nominal` as the reference of the inverted test. The definition
tests every candidate against the loss *minimiser*; testing against nominal makes nominal's own loss
increase identically zero, so no threshold can reject it. The script also read the
40-demonstration directory rather than the 98-demonstration grids, and took a 2.5% quantile where
the text says one-sided 5%. New `analyze_compatible_set_v2.py` and `rebuild_compatible_set.py`
replace it, with the search domain, loss, alpha and tolerance all as explicit arguments.

Three results follow, and the first two are better than what they replace:

- **The loss factorises.** Grouped by (d/k, delay), the 50 grid points fall into 26 groups. Within a
  group, a fourfold change of the common gain scale moves the mean loss by at most **7.2 µm**;
  between groups the range is **60 mm**, a factor of 8354 (8767 on the second stack). Over the
  sixteenfold range the policy sweeps actually use, the largest difference from nominal is
  **3.1 µm**. This is the structural-blindness result measured on the calibration objective instead
  of on a trajectory, and it is far sharper than the 0.141--0.207 mm the paper had been quoting.
- **The zero threshold degenerates.** Replay is deterministic, so the bootstrap resolves mean
  differences of ~1e-7 m and the rule rejects iso ×2 and ×4 over differences of 0.49 and 0.74
  *micrometres*. As the demonstration count grows the set collapses to the single argmin whatever the
  physics. The fix is a tolerance with a basis outside the conclusion, and the protocol supplies
  one: the two stacks disagree by **1.356 mm** at identical nominal parameters. The invariant
  directions clear that by factors of 440 and 75 000.
- **Nominal is excluded.** Both stacks independently prefer `s2_d0.5_delay1` -- ratio 0.25 with one
  step of delay -- and nominal ranks fifth of 26 groups, rejected at +2.25 mm (ManiSkill3) and
  +1.49 mm (original stack). It stays excluded at the 1.356 mm tolerance. Its distance from the
  optimum is the same order as the between-implementation disagreement, so we report its membership
  as borderline rather than picking a threshold that settles it.

The paper's verdicts were never computed over this set: every policy sweep is anchored at nominal.
They range over the **calibration-invisible fibre through the benchmark's operating point**, now
written `F_nom` and distinguished from `C_alpha` throughout, with the bounded ranges we actually
measured rather than "full scale axis"/"full torque axis". The consequence is that the ledger's
`E_theta` carries no coverage probability for the sets we use, which the appendix now states. The
ranking at the calibration-preferred setting is unmeasured and is named as the first follow-up.

### Statistics and presentation

- **Table 3's build figure was the wrong statistic.** 0.078 was the largest change in a *single*
  policy's success rate, not an effect on the policy difference, so it did not belong on a Δ axis.
  The quantity the argument needs is the shift in Δ: **−0.109** at nominal and −0.063 under the
  halved torque limit. Fig. 2's texture bar had the same problem (a single policy's rate range,
  0.400); it is now the span of Δ across the four variants, **0.160**. Every bar in Fig. 2 is now a
  Δ-quantity. The residual "budget can only reduce the small terms" ranking is gone.
- **The texture estimand restated.** A uniform average over four variants is still a rate; what it
  is not is the rate *conditional* on a variant. Under a complete enumeration the marginal carries
  no sampling error from that axis at all, so the 0.400 spread is the distance between the marginal
  and the four conditionals, not uncertainty in the published number.
- **`exact` withdrawn from the theory claims.** The common-scale invariance is first-order in the
  demonstrated regime and does not hold exactly under full rigid-body dynamics; the torque argument
  supports insensitivity over an interval of τ_max, not down to arbitrarily small limits. Stated as
  measured insensitivity over a stated domain throughout. The saturation mechanism for the one
  non-bitwise demonstration is now marked unverified -- commanded torques were not logged.
- **Appendix C's run counts were wrong.** "5/5" was the number of seed-set directories. The
  per-configuration truth is 48×5 and 16×4 for three conditions and 32×6, 32×5 for two others; set B
  holds 96 episodes on a 64-configuration grid, so ids 64--95 wrap and give those an extra
  observation. Eq. (eq:var) uses the per-configuration `S_c` and was always right; the table was not.
- **Observed coverage is not a guarantee.** The GP band's 0.91 is an empirical frequency over 300
  repetitions, below the nominal 0.95, with a Monte Carlo standard error of about 0.017. Relabelled
  throughout.
- **Fig. 6's data scope is now stated.** It uses the pre-fix 48-episode sweep, the only design that
  varies stiffness and damping independently, and is marked exploratory; the paper no longer
  cross-validates it against the current census table.
- **Table 8's counting errors** (five declaring pairs, not five one-sided declarations; three tasks,
  not four; six of the eight pairs share policy data) and §8.5's residual "makes verdicts
  reproducible" claim, corrected to consistent abstention.
- **§8.4's ending** still said the texture axis moved Δ by no more than 0.044, contradicting the
  0.160 two paragraphs earlier. The whole-parameter-family extrapolation is withdrawn; the
  conclusion is now limited to the conditions tested, with the real margin's lack of an interval
  stated. The WidowX replay evidence is no longer used to justify calibration-invisibility on the
  Google Robot embodiment.
- **The "systematic platform bias" reading is withdrawn.** Eight task×policy cells sharing tasks,
  policies and seeds are not eight independent platform replications, and a *t* interval over them
  does not estimate a real quantity. Reported as six of eight below, two matching, mean −0.038,
  descriptively. The "order of magnitude below 0.121" claim was wrong -- the ratio is 3.2 -- and is
  corrected.
- **The verdict count is model-dependent, and both models are now reported.** Eq. (eq:var) gives one
  resolvable ordering of four; a three-run block *t* interval gives two. We argue for the former
  because it matches the randomisation the reference lifecycle performs, and say so rather than
  choosing the model that preserves the headline.
- Per-pair intervals are now labelled as such against the ledger's joint events, instead of being
  presented as a simultaneous procedure.

---

## v1.2.0 -- 2026-09-22

The first release that changes a number rather than a word, and the first that adds episodes. A
revision pass found eight claims stated beyond what the data support; seven were corrected from the
existing records, and the eighth required 576 new episodes.

### The RNG lifecycle, and a claim withdrawn because of it

Our reproduction of the published SIMPLER bridge protocol matched its outer loop --- the
24-configuration census under `init_rng` in {0, 2, 4} --- but not the way the reference threads the
policy's randomness through it. `OctoInference` seeds `jax.random.PRNGKey(init_rng)` in `__init__`
and its `reset()` never touches the key, so one stream advances through every step of every episode
of a run. We sent the seed on every reset, and `octo_policy_server.py` re-seeded on receipt, so all
24 configurations within a run replayed **one identical noise realisation**.

`--policy-seed-stream` reproduces the reference lifecycle, and `queue_ms2_official_stream.py` re-ran
all 576 episodes under it. Three consequences:

- Agreement with the published table gets **worse**, from 0.026 to 0.038 mean absolute, and acquires
  a systematic offset: mean $-0.038$, 95% CI $[-0.074, -0.002]$, with seven of eight cells below the
  published value. The old lifecycle showed $-0.005$, $[-0.033, +0.022]$ --- no detectable offset.
- The across-run range of a cell's rate **halves**, 0.109 to 0.052. This is why the worse agreement
  is the more trustworthy number: re-seeding per episode made each run a single noise draw replicated
  across the grid, inflating the across-run variance, and a noisier estimator landing closer to a
  target is not evidence of fidelity. The platform gap was always there; our first run could not see
  it.
- **One claim is withdrawn.** We had reported that a faithful re-run of the published protocol
  reverses a published ordering, on carrot ($-0.056$ against the published $+0.014$). Under the
  reference lifecycle carrot gives $+0.028$, and no cell disagrees in sign with the published table.
  The reversal was our own re-seeding letting one unlucky stream decide the sign of a 0.014-sized
  difference. The manuscript now retracts four conclusions rather than three.

The server echoes the lifecycle it applied (`rng_mode`: `reseed` or `continue`) and the sweep asserts
it every episode, so a server without the patch fails loudly instead of quietly re-seeding. Both
result directories are kept; `analyze_official_protocol.py --compare` prints them side by side.

### Seven corrections from the existing records

- **The torque-limit invariance is not bitwise on every episode.** New
  `audit_exact_invariance.py` counts exact equality per episode: 97 of 98 on *both* stacks, the same
  demonstration being the exception on each, differing by 0.149 um and 0.050 mm. `check_iso_invariance.py`
  could not have caught this --- it reports millimetres, where 1e-12 m prints as 0.000 mm. Appendix A's
  point-mass argument now rests on the ordinary route, which does not need exactness.
- **The union bound omitted `nominal`.** The compatible set contains the fitted nominal parameter by
  construction, so an envelope over the invisible conditions alone does not cover it. Added to
  `make_core_table.py` and to Fig. 4, which share the estimator. No verdict changes, but it exposes
  that the eggplant small-vs-base declaration rests on a lower bound of **+0.000042**, and the
  paper's one point-vs-set disagreement on a point bound of +0.004. The generator now marks
  knife-edge rows so the two-decimal columns cannot carry them.
- **Fig. 6 was a different computation from the rung the text adopts.** It plotted a
  single-hyperparameter posterior and quoted a *pointwise* k=2 band, which declared on eggplant where
  the adopted simultaneous band abstains. `analyze_response_surface_v2.py` now draws the marginalised
  mean over the restricted plane and prints the caption's bounds.
- **Table 7 reported the configuration the text says it rejects.** Narrowing the strip also narrows
  the ground truth, so it is not a like-for-like comparison of one band; `make_table7.py` prints both
  extents, the table states which it uses, and the 0.85 minimum coverage of the narrowed variant is
  reported rather than only the 0.91.
- **Table 8's stability column conflated replicated declarations with agreed abstentions.** New
  `analyze_declaration_replication.py`: the union bound declared on one pair of eight and that
  declaration did not replicate (0 of 1); point calibration managed 1 of 5. The claim that valid
  declarations replicate better is withdrawn --- what the data support is more consistent abstention.
- **Sect. 8.4 compared the wrong pair of magnitudes.** Reaching abstention needs 0.070, not the 0.214
  separating the simulated and real margins, and the texture x condition span is 0.160, not the 0.044
  of the two dynamics conditions.
- **The texture finding is reframed.** The suite documents its variant aggregation, so
  "unreported"/"silently" is dropped throughout, as is the incommensurable "largest term in the
  budget" ranking: Table 3 and Fig. 2 now name each quantity's kind (a standard deviation, a paired
  shift, a range over four settings). The contribution is restated as an estimand argument --- the
  published quantity is a mean over a four-point population, so a single-variant reproduction targets
  something else and differs by up to 0.227.

`make_table5.py` is new and generates Tables 4 and 5, which had been computed by hand; it reproduces
the previously published values exactly on the old records, which is what validated it before the new
ones were read.

---

## v1.1.3 -- 2026-09-22

The manuscript now names **no version at all**. This is the actual fixed point; v1.1.2 was not.

Switching from a version DOI to the concept DOI removed one coupling, but replacing it with a prose
"the version corresponding to this manuscript is vX" reintroduced the identical one: that sentence
lives inside an archive, so the version it names is necessarily the one *before* the archive
containing the sentence. It can only ever be off by one, and it was -- v1.1.2 held the current text
while its own prose pointed at v1.1.1.

The statements now assert the property that is version-independent and is what a reader following
the pointer actually wants: the records and the scripts that regenerate every table and figure are
byte-identical across all versions, so any version reproduces the paper. That is verifiable from
`SHA256SUMS.txt` and does not decay.

Also: the release changelog now tabulates every version DOI, and `SUBMISSION_CHECKLIST.md` section 6
no longer contradicts itself about the two book citations.

---

## v1.1.2 -- 2026-09-22

The manuscript now cites the **concept DOI** ([10.5281/zenodo.22893458](https://doi.org/10.5281/zenodo.22893458))
rather than a version DOI, and names its corresponding version in prose instead.

This is the fixed point of the previous two releases. A version DOI is minted *by* the snapshot that
contains the manuscript, so the DOI string necessarily lands one commit after the archive it names:
the archived `main.tex` always cited the previous version's DOI, and re-tagging to close the gap
never converged. With the concept DOI the manuscript holds no version-specific identifier, so this
archive and every future one are byte-identical in that respect, and no further re-tagging is needed
for the citation to stay correct.

Exactness is not lost: the concept record lists every version with its own DOI, and what carries the
reproducibility claim is `SHA256SUMS.txt` and the regeneration scripts, which are identical across
all releases.

---

## v1.1.1 -- 2026-09-22

Punctuation-level release. No number, claim, figure or record changed.

- `references.bib`: RoboArena's author list carried `Mart{'i}n-Mart{'i}n` with the backslashes
  stripped, which would have copy-edited as an apostrophe rather than an accent. It never appeared
  in the rendered bibliography because apacite truncates that 26-author list, which is why only
  reading the source caught it.
- Sect. 5.5's scope remark said "five seed sets" flatly while Appendix C shows spoon and carrot have
  two. It now says where five exist and points at the appendix.
- Removed three packages loaded from the template's example preamble and never used.
- The comment on Table 3's drift row was a development note; replaced with a neutral pointer to the
  script whose docstring carries the derivation.
- `SUBMISSION_CHECKLIST.md` reconciled with the work it describes.

---

## v1.1.0 -- 2026-09-22

- Version DOI: [10.5281/zenodo.22895382](https://doi.org/10.5281/zenodo.22895382)
- Concept DOI: [10.5281/zenodo.22893458](https://doi.org/10.5281/zenodo.22893458) (always the newest version)

Strengthening pass on the manuscript, tagged so the archived snapshot matches the paper as
submitted. No evaluation was re-run and no record file changed; the episode data in v1.0.0 and
v1.1.0 are identical.

- **Figure 4 rebuilt.** It previously read `results/controller_sweep_gpu` directly and bootstrapped
  per episode. That directory is the pre-fix inference-server generation, which the manuscript
  disqualifies from being pooled with current data; a per-episode bootstrap targets the
  generalisation value where the standard estimand is the benchmark value; and its union ran over
  nine invisible conditions where the core table uses five. The caption consequently reported the
  compatible set abstaining on two tasks where the core table reports it declaring. `fig_delta` now
  calls `make_core_table.delta()` on the same seed sets and conditions, so the figure and the table
  are one computation and cannot diverge again.
- Appendices C and D written. C is generated by the new `scripts/make_appendix_c.py`.
- `scripts/analyze_platform_drift_paired.py` and `scripts/analyze_torque_shift_s5.py` added in this
  line of work; both print naive and corrected figures side by side rather than preferring one.
- Manuscript positioned against the domain-randomization literature, and five further
  reinforcements: excitation-range framing of the exact invariances, the asymmetric reading of the
  real-robot reference, reported GP hyperparameters, the seed-budget advice qualified to policies
  that consume a seed, and a limitation separating construction-level conclusions from
  instance-specific magnitudes.
- Bibliography completed: full author lists throughout, no abbreviated entries, all 21 references
  checked against publisher or proceedings records.
- Internal review notes excluded from the release.

---

## v1.0.0 -- 2026-09-22

First release, accompanying submission of the manuscript to *Autonomous Robots*.

- Version DOI: [10.5281/zenodo.22893459](https://doi.org/10.5281/zenodo.22893459)
- Concept DOI: [10.5281/zenodo.22893458](https://doi.org/10.5281/zenodo.22893458) (always the newest version)

- Evaluation harness, six resumable queues, and the configuration-census utilities.
- 784 per-episode record files (22.3 MB) covering every table and figure, plus the append-only
  `runs.jsonl` provenance logs.
- 14,064 per-episode replay trajectories (59.7 MB) behind the exact-invariance result.
- Analysis scripts that regenerate every table and figure from the records, including
  `analyze_fractal_reversal.py` and `analyze_torque_shift_s5.py`.
- The synthetic decidability track (Track S) with its cached cells, and the real-replicate track
  (Track R).
- `export_submission_figures.py`, which renders the six figures at journal geometry and audits them
  against the width and lettering requirements rather than emitting a breach silently.
- The Vulkan compatibility layer for headless rendering without a GPU.
- `SHA256SUMS.txt` over the 997 record and cached-analysis files.

### One number was reconciled just before this release

Table 3's implementation-build drift (+0.078) appeared not to reproduce -- a recomputation gave
0.023. The recorded value was right and the recomputation was wrong. Build drift is a paired
quantity, and the two directories hold different episode counts (96 against 64); because episode ids
beyond the grid wrap onto it, comparing each directory's own per-configuration mean measures
different effective scopes. Paired on the shared ids it reproduces 0.297 / 0.375 / 0.078 exactly.

`seed_sd` had the same flaw, so the policy-seed figure tightened from 0.0702 to 0.0672. Both
estimators now restrict to shared ids. This mattered beyond one cell: on the unpaired figures build
drift would have sat *below* policy-seed noise, reversing an ordering the manuscript asserts.
See `scripts/analyze_platform_drift_paired.py`.

---

## Note on release timing

The previous project in this line released `v1.0.0` before its manuscript settled, and the archived
snapshot then no longer matched the paper — `v1.1.0` was issued to repair it.

This project repeated that pattern before diagnosing it properly. The lesson is not only "freeze the
manuscript, then tag", which is good advice but insufficient: as long as the manuscript cites a
version DOI, any change to the manuscript makes the cited snapshot stale, and re-tagging moves the
gap rather than closing it. Citing the concept DOI removes the coupling, and is what a project in
this position should do from the first release.
