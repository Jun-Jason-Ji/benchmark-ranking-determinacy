# Changelog

Versions are tagged in git and archived on Zenodo. **A tag is a promise**: once Zenodo mints a DOI
for it, that snapshot is permanent and the manuscript will cite it. Tag only when the manuscript is
frozen — see the note at the foot of this file.

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
snapshot then no longer matched the paper — `v1.1.0` was issued to repair it. Two DOIs now exist for
one result. That is recoverable but avoidable: freeze the manuscript, then tag.
