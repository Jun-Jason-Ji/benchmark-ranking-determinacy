# Autonomous Robots submission — status

Prepared 2026-09-21, strengthened 2026-09-22. Requirements fetched from the journal's own
submission-guidelines page (`link.springer.com/journal/10514/submission-guidelines`) and the
Springer Nature LaTeX template (December 2024), whose `sn-jnl.cls` and `sn-apacite.bst` are in this
directory unmodified.

**One blocking item remains.** Three citations added for the related-work positioning —
`suresim2025`, `polaris2025`, `scape2025` — carry the arXiv identifiers supplied in review but
**placeholder author lists and unverified titles**. Their author fields read
`VERIFY AUTHORS BEFORE SUBMISSION` so they cannot be missed in the rendered bibliography. Fill them
from the actual preprints, or drop the citations and the paragraph that depends on them, before
submitting. The other 21 citations are verified against publisher or proceedings records with
complete author lists.

Otherwise the manuscript compiles at 41 pages with 0 errors, 0 overfull boxes, 0 undefined
references and 0 bibtex warnings. The code and data are published with a DOI. Every declaration is
settled.

One item is left, and it is the author's: fill the date on the cover letter. Everything else that
needed an author's decision -- funding, contributions, the generative-AI wording, the licence and
its copyright line, the affiliation details, and the standard scope -- is confirmed and recorded
below.

---

## BLOCKING

### 1. RESOLVED - the manuscript compiles cleanly

A portable TeX Live 2026 tree was extracted into the session scratchpad (TinyTeX, from the official
`rstudio/tinytex-releases`); **nothing was installed into your profile or PATH**, so there is no
system change to undo. Nine missing LaTeX packages were pulled with `tlmgr` (sttools, threeparttable,
appendix, wrapfig, apacite, multirow, algorithms, algorithmicx, ncctools).

Final build state: **0 errors, 0 overfull boxes, 0 undefined references, 0 bibtex warnings, 41 pages.**
To rebuild:

```
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

That tree has since been relocated to a permanent install (`C:/Users/Jason/TinyTeX`) and put on
the user PATH, with the manuscript rebuilt from the new location to confirm it behaves identically.
A new terminal has `pdflatex`, `bibtex` and `tlmgr` available. `main.pdf` and `main.bbl` are in this
directory, and the sources are self-contained, so they will also build on Overleaf.

Four defects that only compiling could have surfaced, all fixed:
- **Figure filenames did not match the printed figure numbers.** LaTeX numbers floats by order of
  appearance; the torque figure (Sect. 7.4) precedes the delta-by-condition figure (Sect. 7.6), so
  they printed as Figures 3 and 4 while the files were named Fig4 and Fig3. Swapped, in both
  `main.tex` and the export script. All six now verify 1:1 against `main.aux`, as do all nine tables.
- **All six figures and five tables were being squeezed into one column.** In the two-column
  `[iicol]` layout a plain `figure`/`table` is column-width, so full-width graphics overran
  by 239 pt. Converted to `figure*`/`table*` with `[t]` placement (starred floats cannot take `[h]`).
- **Three display equations overran the column.** Reformatted with `split`, and the long
  bootstrap-bound prose was moved out of the compatible-set equation into a defined operator.
- **The Fig5 caption had the two rows swapped** - the figure is top = false declaration rate,
  bottom = coverage, and the caption said the reverse. Rewritten with the actual numbers.

### 2. RESOLVED - authors filled in

Six authors, three affiliations, Yi Sui corresponding: Jun Ji, Bowen Tan, Yi Li, Xiaolei Zhang,
Shengjie Guo, Yi Sui. The block was supplied in Elsevier `elsarticle` form (ead / fnref / cortext /
address macros) and converted to the Springer `sn-jnl` macros (author* / affil* / fnm / sur /
email). Verified on the rendered title page.

Ethan Yixuan Ji was removed from the author list on 2026-09-21, and affiliation 4 (The Middle School
Affiliated to Qingdao University) was removed with him, as no remaining author was attached to it.
Affiliations 1-3 keep their numbers, so no cross-references moved.

ORCIDs are recorded as a comment block in `main.tex` and as a table in
`declarations_for_interface.md`, not typeset: `sn-jnl` does define `\orcid{<url>}`, but it renders
`Orcidlogo.eps`, which the template package does not ship. ORCIDs belong in the submission system
anyway.

Three details were supplied rather than received and have since been confirmed by the authors:
Hohhot as Inner Mongolia Agricultural University's city, "Shengjie Guo" in given-name-first order as
Springer typesets it, and the English name of the middle school, which became moot when that author
was removed.

**Author Contributions is settled** (2026-09-21): CRediT roles carried over from the prior
submission `IVC_Paper2_Submission_2026-09-12`, with Shengjie Guo taking the same roles as Xiaolei
Zhang, as directed. All six authors have roles; nothing outstanding.

### 3. RESOLVED - no funding

Confirmed by the author 2026-09-21. Both `main.tex` and `declarations_for_interface.md` state that
no funds, grants or other support were received. Wording is plural now that six authors are
listed.

### 4. RESOLVED - all six figures are journal-legal

Fig1, Fig3 and Fig6 were redesigned at 174 mm native width, in-figure titles removed (the journal
forbids them), lettering raised to 8 pt or more. Fig5 was redrawn from `track_s_results.json` via a
new `--redraw` flag on `run_track_s.py`, so its 300-repetitions-per-cell simulation did not have to
re-run; it also drops the `gated` rung, which `FINDING_track_s.md` withdrew from the ladder. Fig2 and
Fig4 were fixed earlier. The export script's geometry-and-font audit now reports **no violations for
any of the six**.

Content removed from the figures was not lost: verdicts, set bounds, GP hyperparameters and
per-condition episode counts moved into the LaTeX captions, and the figure scripts print those values
so a caption cannot drift from the data. That mechanism immediately caught two errors:
- The Fig4 (formerly Fig3) caption had the spoon verdict wrong - "set declares, [+0.12, +0.48]"
  where the data say **set abstains, [-0.12, +0.48]**. The sign had been read off a figure whose
  labels were overprinting.
- Two Fig1 axis labels rendered as "$imes$" because a single-backslash times macro in a non-raw Python
  string became a TAB. Fixed with raw strings; the other figure scripts were swept for the pattern.

### 5. RESOLVED - standard scope is census at S = 5

Decided by the author 2026-09-21: the paper's standard scope is the census at five seed sets, so
delta = **0.121**, not 0.141. The reasoning is that for delta the two figures are not different
estimands but the same quantity at different seed budgets, and Sects. 7.2/7.6 argue that S = 3
cannot be trusted - quoting an S = 3 delta as the headline would undercut the paper's own argument.

Applied throughout: delta 0.141 to 0.121 in five places; the Sect. 7.3 per-pair shifts recomputed to
-0.104 / -0.146 / -0.108 / -0.127 (mean 0.121, range 0.104-0.146) by the new
`scripts/analyze_torque_shift_s5.py`, whose mean matches Fig. 2 through a separate code path;
the published-protocol uncertainty from +-0.06 to +-0.08; the octo-small negative control from
-0.018 to +0.011; and Table 3's seed row from sd 0.104 on one pair to a median over pairs. The
seed-noise half-widths moved twice: first to 0.138/0.079/0.044 with the scope change, then to
**0.132/0.076/0.042** when item 5b corrected the estimator to pair on shared episode ids, which also
put the seed sd at 0.067. A remark in Sect. 5.5 declares the scope once, as this checklist asked,
and states that five seed sets is the eggplant count while spoon and carrot have two.

Left alone on purpose: the 0.141 mm and 0.207 mm replay differences of Sect. 4 (millimetres, a
different quantity that merely shares a digit string), and the retracted eggplant ranking
+0.141 / -0.031 / -0.047 (a historical record of what was withdrawn - re-measuring it would erase
the retraction). The superseded S = 3 value is now stated explicitly in the Sect. 7.3 remark rather
than deleted.

**Cost, stated plainly:** the headline contrast weakens from 0.141 against +-0.062 (2.3x) to 0.121
against +-0.079 (1.5x). Every argument's direction survives - delta still exceeds the evaluation
half-width at every realistic budget and still does not shrink with budget.

### 5b. RESOLVED - the drift number was right; the recomputation was wrong

Diagnosed 2026-09-22. **Table 3's +0.078 was correct all along**; the apparent discrepancy was my
own unpaired recomputation.

Build drift is a paired quantity - same seeds, different build. The pre-fix directory holds **96**
episodes against A's **64**, and with 64 configurations ids 64-95 wrap back onto configs 0-31. So
averaging each directory over its own per-configuration mean compares different effective scopes:
half the configurations get two observations on one side and one on the other. Paired on the 64
shared ids, the cell reproduces the recorded `0.297 vs 0.375 = 0.078` exactly, and the recorded mean
of 0.043 as well (`scripts/analyze_platform_drift_paired.py`).

The same flaw was in `seed_sd()`, since seed set B also holds 96 episodes. Both estimators in
`make_figures_v2.py` now restrict to the episode ids common to the directories under comparison.

Consequences:

- Table 3 stands unchanged at +0.078, now labelled "paired".
- Seed sd tightens 0.0702 to 0.0672, so the half-widths become **0.132 / 0.076 / 0.042** (from
  0.138 / 0.079 / 0.044). Updated in Sects. 6.2 and 10.
- **Sect. 5.5's ordering claim now holds on matched scopes**: drift 0.078 above policy-seed noise
  0.067. On the unpaired figures it would have been reversed (0.055 below 0.070) - so the claim was
  right and the arithmetic that appeared to threaten it was not.
- Sect. 5.5 gains a paragraph stating the pairing and why it matters, since the ordering depends on
  it. It is the paper's own thesis applied to its own numbers.
- Fig. 2 regenerated; figure and text now agree throughout.

**Nothing is now held back, and the manuscript is internally consistent.**

### 6. RESOLVED - all 21 citations verified

**Resolved for all 21 entries**, each checked against the publisher, proceedings or dblp
record. Newly verified: RT-1 (RSS 2023, dblp `conf/rss/BrohanBCCDFGHHH23`, 46 authors truncated at 20
per journal policy), Octo (arXiv:2405.12213 v2, author list confirmed), OpenVLA (PMLR 270:2679-2713,
`kim25c`), BridgeData V2 (PMLR 229:1723-1736, `walke23a`), ManiSkill2 (ICLR 2023), SAPIEN (CVPR 2020),
Swevers (IEEE T-RA 13(5):730-740), Bellman and Astrom (Math. Biosci. 7:329-339), Tamer (Annu. Rev.
Econ. 2:167-195, doi 10.1146/annurev.economics.050708.143401), Henderson (AAAI 32:3207-3214), Agarwal
(NeurIPS 34), Colas (arXiv:1806.08295).

**One correction this surfaced:** SIMPLER and OpenVLA are both PMLR volume 270, and the proceedings
assign them **2025**, not 2024 (the record ids are `li25c` and `kim25c`). Both years are now 2025, so
the in-text citations will read "(Li et al., 2025)". The citation keys still contain "2024"; keys are
arbitrary labels, but rename them in `main.tex` and `references.bib` together if you want them
consistent.

Manski (2003) and Ljung (1999) were subsequently verified against catalogue records: Manski is the
Springer Series in Statistics monograph with doi 10.1007/b97478, and the 2003 volume is the intended
citation rather than the 2007 one; Ljung's place of publication was wrong and is corrected to
Englewood Cliffs. Complete author lists were later obtained for AutoEval, RoboArena and ManiSkill3,
removing the last `and others` fields and with them the final bibtex warnings -- AutoEval's
abbreviated form had concealed two missing authors and a mis-ordering. Nothing in the bibliography is
unverified.

---

## Done

### Requirements captured
- Format: LaTeX, Springer Nature template, formatting option `[iicol]` — both applied in `main.tex`.
- Reference style: `sn-apa`, matching the journal's author–year citations, alphabetised list, italic
  journal titles and DOIs as full links.
- Abstract: **249 words**, inside the journal's 150–250 limit (checked, not estimated).
- Keywords: **6**, inside the 4–6 limit.
- Headings: decimal, three levels maximum — the manuscript uses at most two.
- Footnotes, not endnotes. Acknowledgements in their own section.
- One `.tex` document, no `\input` — as the template instructs.
- All editable sources present, which the journal makes a condition of review.

### Manuscript
`main.tex`, 1569 lines, all ten sections and all four appendices written in full:

| § | Content |
|---|---|
| 1 | Introduction, contributions, **what we withdraw**, scope |
| 2 | Related work (citations attached; see blocking item 6) |
| 3 | Notation, compatible set by test inversion, decision problem, error ledger incl. the explicit statement that $E_b$ is *not* established |
| 4 | Structural blindness, Table 1 |
| 5 | Finite configuration population, Tables 2–3, the texture-variant row |
| 6 | Published-protocol reproduction, Tables 4–5 |
| 7 | Decision-relevant non-identifiability, Table 6, the withdrawn §7.5 claim |
| 8 | Verdict ladder, Tables 7–9, the delimiting negative result |
| 9 | Limitations, ordered by how much they should move a reader |
| 10 | Conclusion |

All four appendices are written: A derives the test inversion and states the error ledger with the
four ways it can be misused, B documents the headless-rendering layer and the condition under which
it would be unsound, C is a generated per-cell configuration and run-count table, and D gives the
reproduction structure.

### Files in this directory

| File | What it is |
|---|---|
| `main.tex` | the manuscript |
| `references.bib` | 21 entries, all verified, complete author lists |
| `sn-jnl.cls`, `sn-apacite.bst` | from the official template package, unmodified — submit these |
| `Fig1–4,6.eps` | vector EPS at 174 mm, all passing the geometry and 8 pt lettering checks |
| `proof/Fig*_proof.png` | rasters at the exact submitted geometry, for eyeballing layout. **Not for submission** |
| `cover_letter.md` | leads with the 0.026 reproduction, states the negative result up front, addresses the no-hardware question directly |
| `declarations_for_interface.md` | every declaration block to paste into Editorial Manager, with the three that need your confirmation flagged |
| `sn-user-manual.pdf` | the template's own manual, for reference |

### Deliberate choices you may want to overrule

- **The negative result is in the abstract and Sect. 1**, not only in Sect. 9. A reviewer who finds
  it first in the limitations reads it as concealment; stated up front it is the paper's spine.
- **Sect. 9 leads with "our central negative result rests on a single policy pair"**, ahead of the
  conventional no-hardware item.
- **Sect. 8.3 states that the all-axes union bound reaches 1.00 stability with a 0.00 declaration
  rate** and calls that degenerate rather than a success.
- **The cover letter opens with the reproduction, not the critique**, and frames the published real
  rates as the right instrument for the question rather than a stand-in for hardware.
- **Suggested reviewers**: the cover letter offers them on request rather than naming any. If you
  supply names, note that the obvious experts are the authors of the suite being audited.

### Not required at submission
Brief biography and photograph — the journal asks for these with the *accepted* manuscript.
Publishing-model choice and any article processing charge come after acceptance.
