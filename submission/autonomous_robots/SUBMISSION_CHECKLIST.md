# Submission preparation — verified revision, 23 September 2026

This checklist supersedes the earlier local closeout statements. Use the frozen files named in `submission/releases/README_FINAL.md`. No journal submission or new public release has been made.

## Completed

- English manuscript: **45 pages**, **246-word abstract** (hyphenated words and each mathematical expression counted as one), six keywords, 14 tables and six figures. Editable TeX, compiled bibliography, journal style and figure sources are included.
- All **24 cited works** have verified primary records. **16 verified DOIs** appear as actual PDF links, once each in the reference list; the other eight entries use authoritative URLs. Bibliography keys, internal references and author metadata have been checked. See `REFERENCE_VERIFICATION.md` for the inventory, corrections and access limitations.
- Both English and complete Chinese PDFs have zero compilation errors, undefined references/citations, BibTeX warnings, missing-character messages and overfull boxes. All pages were rendered and visually inspected. Remaining template warnings concern bookmark hierarchy, math in bookmark strings, and float placement; the printed title, content and tables are intact.
- English prose has been polished throughout. The point-rule direction is explicit, empirical compatibility diagnostics are distinguished from the sampled set actually evaluated, and simulation sensitivity is separated from real-world validation. The appendix records the prior corrections.
- Figure 3 and its configuration-level decomposition now use the same current five-Octo-seed scope and whole-run deduplication rule. The new CPU entry point `scripts/analyze_torque_scope_current.py --out output.json` reproduces that decomposition and records input hashes. This corrected stale summary values, not the episode records or headline findings.
- The companion package contains **16,857 source files / 16,862 files including package metadata**. All six CPU analyses ran successfully from that package; full inventory and hash checks passed before and after. The two-task operating-point evidence includes 120 paired files and 5,760 episodes with complete 64-/24-configuration censuses.
- The cover letter, plain-text paste version, interface declarations and evidence index are updated. At the author’s direction on 23 September 2026, Yizhou Zhao (Sino-French Institute, Renmin University of China; ORCID 0009-0004-7515-6322; yizhou-zhao@ruc.edu.cn) is the fifth author, immediately before Shengjie Guo, with the same CRediT roles: Software, Writing – review & editing. The latest author-supplied contribution statement also assigns Formal analysis and Project administration to Yi Li, and Software and Project administration to Xiaolei Zhang; both retain Writing – review & editing. The full seven-author statement agrees between the English manuscript, Chinese reading version and interface declarations. All four affiliations consistently include institution, city/region and country and omit postal codes; The Sino-French Institute affiliation uses Suzhou, China. Shengjie Guo’s affiliation includes the College of Computer and Information Engineering, Inner Mongolia Agricultural University, Hohhot, China. Other author details and funding are preserved. Statements and Declarations follow the references, as the journal requests.
- A complete **32-page Chinese reading translation** is supplied separately, with all sections, appendices, table text, captions and declarations. Formulas, data, reference keys and original figures are preserved. It is an author reading aid, not the journal manuscript.

- Typesetting pass: script paths and commands are mapped in the supplied evidence index rather than embedded in prose. Appendix B API identifiers can wrap; Appendix D uses short paragraphs; narrow-column bibliography entries are left-aligned. The Chinese contents fits on one page. The final editorial pass subsequently corrected Figure 1’s reciprocal ratio axis, Table 1’s corresponding condition order, legacy numerical attribution and scope statements using existing data. Author details, bibliography records and public-archive statements are unchanged; all 14 table numerical sequences, eight displayed equations and six figure assets remain synchronized between languages; repeated inline expressions were consolidated when captions were shortened.

- Final consistency pass: wrong table/column pointers, legacy observation-unit summaries, lifecycle comparison direction, study counts and over-broad claims were corrected. Figure 1 was redrawn from the same replay records; that editorial snapshot changed only `scripts/make_figures.py`; the subsequent figure/appendix revision also updated the package selector and added the compatibility-layer implementation and note. All six CPU analyses passed from the rebuilt companion, and its manifest was verified again. See the editorial correction report and `FINAL_VALIDATION.json` supplied with the delivery.

- Figure/Appendix revision: Figure 1 explicitly labels logarithmic axes, uses common vertical scaling, reports the small common-scale response and presents both delay settings as point intervals. The caption defines sampling, uncertainty, conditions and reference zeros. Appendix B was shortened to mechanism and validity boundaries; its API/build details and actual source now accompany the data package. Existing graph statistics are unchanged; Appendix A’s related prose summary was corrected to match them. Both languages, rendered pages, companion inventory and the six CPU analyses were verified.

- Caption revision: all six figures and fourteen tables have concise topic titles, with essential reading information in adjacent figure/table notes. Long interpretations were moved to the body. The Figure 6 exploratory-data boundary remains explicit. Numerical entries, displayed equations, references, figure assets and author metadata are unchanged; only incomplete verdict labels were completed. Both PDFs were rebuilt, all pages rendered, and every float checked at detail resolution across the review team. At the caption-revision stage the companion data/code archive was reused byte-for-byte. The subsequent format review below updates only the Figure 6 export code.

- Format review: the AI disclosure is an independent section after the conclusion in both languages. The class matches the currently linked official template byte-for-byte; the `2019/v0.1` internal header is not evidence of an outdated bundle. Full-width figure sizing is retained. Figure 6's embedded images were re-exported at 800 dpi from the same plotted arrays, with effective resolution verified at manuscript size; Figures 1–5 and all scientific text, values and statistical code are unchanged. The companion was rebuilt with only the export-script change. The generative-AI interface text matches the manuscript disclosure. Remaining review-spacing guidance is documented in the format audit: the generic manual requests double spacing, while the journal webpage recommends `iicol` without a spacing or line-number mandate; the compact layout is retained here.

- Prose-style review: the abstract normal-math reset is retained. All explicit prose-emphasis wrappers were reviewed in both languages; 137 English and 134 Chinese rhetorical wrappers were removed without altering wording or notation. Structural headings, first definitions and quoted claim labels remain; a subsequent table review removes the selectively bold table-body highlights. At that prose-review stage, table and figure source environments were unchanged. The subsequent table-weight review changes only table-body style wrappers; bibliography, figure assets and author metadata remain unchanged. Both PDFs were rebuilt and visually checked; no overfull boxes, undefined references or missing glyphs. The verified companion is reused unchanged.

- Table-weight review: all 14 tables were audited in both languages. Fourteen selective bold wrappers across eight tables per language were removed because no shared bold-data convention was defined. All data and wording are unchanged; the affected eight pages were visually checked, and all other pages retain identical text/font/geometry signatures.

## Actual submission choices

1. **Institutional eligibility:** the institution's accepted annual 中科院 1区/2区 TOP list remains unverified. This package does not assert that Autonomous Robots meets that requirement.
2. **Evidence access:** upload the companion package with the submission, or publish exactly this frozen release and cite its actual version DOI. The verified public latest version is v1.1.3, DOI `10.5281/zenodo.22896508`; it contains earlier results. The concept DOI `10.5281/zenodo.22893458` is a release-family identifier, not proof that this revision has been archived.
3. **Publication route:** select the subscription/non-OA route in the publisher's workflow, consistent with the stated preference. Complete the actual submission declarations using the supplied interface text.

## Submission-stage actions (not performed here)

- [ ] Enter the seven authors' contribution assignments in the actual submission-interface field, using `declarations_for_interface.md`, and compare with the frozen manuscript.
- [ ] Enter competing interests in its interface field; retain the required manuscript declaration too.
- [ ] Confirm all authors approve the final manuscript before submission. A CRediT role list does not itself record that approval.
- [ ] Follow any additional review-layout requirements displayed by the actual submission system; export a separately identified double-spaced copy if requested.

## Official requirements checked

- [Author guidelines](https://link.springer.com/journal/10514/submission-guidelines): 150–250-word abstract, 4–6 keywords, editable sources, declaration placement and submission-interface fields.
- [Aims and scope](https://link.springer.com/journal/10514/aims-and-scope): physical-robot evidence is preferred; simulation-only studies should explain a route to physical validation. The manuscript states its existing evidence and unexecuted physical-validation plan distinctly.
- [Publishing options](https://link.springer.com/journal/10514/how-to-publish-with-us): hybrid journal with a subscription route.

AI statement revision (23 September 2026): the first sentence now reads exactly: "Large language models (OpenAI ChatGPT/Codex) assisted with manuscript revision, analysis scripts." The quantitative-results and author-responsibility sentences are preserved. The interface declaration and Chinese reading version are synchronized.

## Previous stage: reader-facing method language (24 September 2026)

Configuration identifiers and file locators in the manuscript have been replaced by scientific
descriptions. The sampling lifecycle, observation units and physical perturbations are retained;
implementation identifiers are mapped in the reviewer evidence index. Figures 4/5 and the
condition-table generator use descriptive display labels without changing keys or numerical
results. The companion was rebuilt to include the shared label module. All 14 tables preserve
their values; both PDFs were rebuilt and all pages rendered and reviewed. The preceding AI
statement revision, authorship, affiliations and reference identities are unchanged.

## Previous stage: journal-style revision (24 September 2026)

The English manuscript is 45 pages and the Chinese reading copy is 32 pages. The abstract and
author-supplied declarations are unchanged. The editorial comparison uses eight downloaded articles
with verified identities and documented author/publisher versions; these were not mechanically
added to the bibliography. Source changes are logged individually. Numeric table entries, displayed
equations, reference keys and figure data were verified unchanged. Figure 2 now has embedded Arial
9.5 pt text at 160 mm width and text contrast at least 7.94:1. All pages were rendered and reviewed;
the final changed pages were reviewed again. The companion includes the bounded Figure 2 display
change. Earlier stage descriptions above are historical, not claims that no subsequent edit occurred.

## Previous stage: model and task naming (24 September 2026)

Both manuscript languages use consistent prose names for RT-1 checkpoints, Octo models and
single-frame-history variants. Tables define their compact policy labels locally. Figures 3 and 4
were updated only in labels/font embedding; all numerical inputs and plotting data remain unchanged.
The current English PDF has 45 pages and the Chinese reading PDF has 32 pages. All pages were
rendered; changed tables, figures and policy comparisons were inspected at full-page resolution.
The last two changed pages were rechecked. No errors, undefined references, missing characters,
BibTeX warnings or overfull boxes remain. Existing template bookmark/float warnings are logged.
The review evidence index gives exact mappings back to unchanged record/configuration keys.
All table measurements, displayed equations, citations, abstract, authorship and declarations are
unchanged. The companion was regenerated and verified; no experiment or GP fitting was repeated.

## Previous stage: author departments (24 September 2026)

Yizhou Zhao: Sino-French Institute, Renmin University of China, Suzhou, China.
Shengjie Guo: College of Computer and Information Engineering, Inner Mongolia Agricultural University, Hohhot, China.
Both manuscript languages, the submission-interface fields, the evidence index and CITATION.cff agree.
The city for the Sino-French Institute follows RUC's own Suzhou campus contact information.
Only the title page changes visually in either manuscript; all remaining rendered pages match the previous release.
Author order, email, ORCID, contribution roles and scientific content remain unchanged.

## Previous stage: Table 2 layout and prose punctuation (24 September 2026)

Table 2 has a centred natural-width title, body and note. The task-name mapping is in the main text.
Long dash insertions and transitions were edited individually in 77 English paragraphs; six Chinese paragraphs were synchronized.
All table bodies, figure assets, numerical tokens, formulas, citation commands, author information and declarations remain unchanged.
Independent semantic checks and visual QA passed. Both PDFs remain 45/32 pages; no errors, undefined references, missing glyphs, BibTeX warnings or overfull boxes.
The companion archive from the author-department update is reused unchanged. The release entry point pins the current submission and reading PDFs.

## Previous stage: definition emphasis (24 September 2026)

Only the defined term “calibration-invisible fibre” is italicized; its operating-point qualifier is upright. The Chinese copy uses the same emphasis scope. Wording, scientific content and declarations are unchanged. Full changed pages passed visual QA; all other rendered pages match the preceding release.

## Previous stage: coverage reporting wording (24 September 2026)

Section 5.6 spells out the number of configurations covered and the total number of configurations; a slash no longer stands between the two counts. The reporting list has parallel grammar and preserves replication independence, variance-model options, estimand and simulator/build provenance. Both language copies were updated. Scientific values, formulas, references and tables remain unchanged; all changed pages passed visual QA.

## Previous stage: Section 7.1 heading (24 September 2026)

Section 7.1 is titled “Strong and weak forms”, avoiding repetition of the parent title and reducing the English heading from three lines to one. The Chinese heading and contents are synchronized. Template font, size, numbering, labels, all body text and scientific content are unchanged. All affected pages passed visual QA.

## Current stage: provenance and statistical consistency (24 September 2026)

- Supply Supplementary Material S1 PDF and its provenance-source archive with the manuscript.
- Appendix E's development history has moved to S1; substantive negative evidence remains in the paper.
- Four early candidates and all 39 Figure 6 design budgets are traceable to stored records.
- The corrected directional-IUT code and cached output preserve all headline counts.
- Manuscript template and cover letter still target Autonomous Robots. A potential RAS submission
  needs a separate journal-specific conversion and length review; it has not been submitted.
- The 2025 CAS public records show Autonomous Robots major Q3/non-TOP and RAS major Q2/non-TOP.
  If TOP or robotics-subcategory Q2 is mandatory, RAS does not meet that condition.
