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
throughout.

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
