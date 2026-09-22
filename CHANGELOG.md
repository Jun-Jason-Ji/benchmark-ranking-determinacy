# Changelog

Versions are tagged in git and archived on Zenodo. **A tag is a promise**: once Zenodo mints a DOI
for it, that snapshot is permanent and the manuscript will cite it. Tag only when the manuscript is
frozen — see the note at the foot of this file.

## Unreleased

Staged for the first release, alongside submission of the manuscript to *Autonomous Robots*.

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

### Known open item carried into the release

The implementation-build drift figure in Table 3 (+0.078) does not reproduce on recomputation, which
gives 0.023. Recorded in `REPRODUCIBILITY.md` and in a comment on that table row rather than quietly
corrected, because which value is right is not yet established.

---

## Note on release timing

The previous project in this line released `v1.0.0` before its manuscript settled, and the archived
snapshot then no longer matched the paper — `v1.1.0` was issued to repair it. Two DOIs now exist for
one result. That is recoverable but avoidable: freeze the manuscript, then tag.
