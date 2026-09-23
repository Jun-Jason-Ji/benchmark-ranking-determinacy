# Submission closeout status — 2026-09-23

This file supersedes earlier readiness statements. The previous checklist is preserved at
`reviews/2026-09-23_submission_closeout/SUBMISSION_CHECKLIST_before_closeout.md` in the working
repository. Prepared materials have not been submitted or newly deposited in a public archive.

## Local preparation completed

- The manuscript is **47 pages**, with an approximately **231-word abstract** and six keywords. It was rebuilt
  with the installed TeX Live runtime. Final checks found no compilation errors, undefined
  citations/references, BibTeX warnings, or overfull boxes. Hyperref reports non-blocking PDF
  bookmark hierarchy/math-string warnings; these do not affect the printed text or references.
- All pages were rendered for layout inspection, with detailed inspection of the edited
  inference argument, evidence table, conclusion and availability statements. No visible text
  clipping or table/figure overlap was found.
- The cover letter is approximately **582 words**, focused on three empirical contributions,
  practical reporting recommendations, the study's scope and existing author declarations.
- The false-declaration argument distinguishes a fixed direction (0.025) from either direction
  (0.05). Finite-set range coverage remains at least 0.95 under valid component bounds.
- The evidence table explicitly identifies MS2 replay bounds and MS3 policy results. It does not
  claim that one measured stack bounds an unmeasured sweep on the other stack.
- Both operating points have all six evaluated conditions on both eggplant and spoon. Eggplant's
  set envelopes abstain and its paired shift remains unresolved. Spoon's gap changes from 0.3958
  to 0.1250; its primary paired-shift interval is [-0.4580, -0.0837]. Both spoon declarations become
  abstentions. The two-seed-block and limited-task qualifications remain explicit.
- `REVIEW_EVIDENCE_INDEX.md` maps the principal findings to records, scripts and interpretation
  boundaries. `scripts/reproduce_review_evidence.py` regenerates five headline analyses into a
  new external directory without launching any simulation evaluation.
- The final companion data/code snapshot contains **16,848 source files / 16,853 package files**.
  Full verification passed, all five analyses ran from that snapshot, and verification passed
  again afterwards. Its manifest digest is recorded in the evidence index. The older root
  `SHA256SUMS.txt` is not the identifier for this snapshot.
- Funding, authors, affiliations, ORCIDs, contribution assignments and competing-interest fields
  preserve the previously supplied values. AI assistance is disclosed for both Claude and
  OpenAI ChatGPT/Codex; current availability wording does not assert unverified archival publication.

## Deliverable structure

The manuscript package supplies PDF, editable TeX, bibliography, figures, cover letter, interface
declarations, this checklist and the evidence index. The companion package supplies the cached
records, replay trajectories, required analysis inputs, scripts, licences and pinned dependencies.
Each package has its own manifest and verifier; final ZIP checksums identify the delivered archives.
`submission/releases/` is the working repository's final delivery directory.

Do not deliver incomplete/superseded QA packages. Use the final two-task snapshot named in the
delivery record, whose scope matches the compiled manuscript. Inclusion of historical
quarantined records is for traceability; the analysis scripts retain their filtering rules.

## Matters to resolve at actual submission

1. **Venue eligibility:** the institution's accepted annual 中科院 1区/2区 TOP list has not been
   supplied or verified. This package does not assert that Autonomous Robots meets that requirement.
2. **Evidence access:** provide the companion package with the submission, or deposit this exact
   frozen release and record its version-specific identifier. The public concept DOI indexes earlier
   releases and is not verification that this review snapshot has already been archived. The current
   manuscript states that limitation honestly.
3. **Submission choices:** use the previously supplied author information and complete the actual
   submission declarations as corresponding author. Autonomous Robots offers a subscription route;
   the journal is hybrid, and non-OA publication is a publishing choice, not a manuscript edit.

These are external submission/eligibility steps, not reasons to add unplanned experiments.

## Official requirements checked

- [Author guidelines](https://link.springer.com/journal/10514/submission-guidelines): abstract
  150–250 words, 4–6 keywords, editable sources and submission-interface declarations.
- [Aims and scope](https://link.springer.com/journal/10514/aims-and-scope): physical-robot data are
  preferred; mathematical/simulation-only work must detail a path to real-world performance.
- [Publication options](https://link.springer.com/journal/10514/how-to-publish-with-us): subscription
  and open-access routes are available.
