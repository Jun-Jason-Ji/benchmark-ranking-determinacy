# Declarations — to paste into the journal submission system

The journal requires **author contributions and competing interests** to be entered through
the submission interface; for these two categories, the interface entries determine the final
published statements. The manuscript also retains its required declarations after the references.
Copy the applicable blocks into the corresponding fields; uploading the manuscript does not
complete this step. The interface has not been filled or submitted by this preparation workflow.

Review every one of these before submitting — several are assertions about the authors, not about
the research. The confirmed author, funding and competing-interest statements are retained below.
The current results are supplied in a frozen companion review package, which has not yet been
published as a new public archive. The AI disclosure records the tools
used through this revision.

---

## Funding

> ✅ Confirmed 2026-09-21: no funding of any kind.

```
The authors declare that no funds, grants, or other support were received during the preparation of
this manuscript.
```

## Competing interests

```
The authors have no relevant financial or non-financial interests to disclose.
```

## Ethics approval and consent to participate

```
Not applicable. This study involves no human participants and no animals. All experiments were
conducted in simulation, and the real-robot reference values used for comparison are previously
published figures distributed with the benchmark's own source.
```

## Consent for publication

```
Not applicable.
```

## Data availability

```
Episode-level evaluation records, replay trajectories and analysis inputs are supplied in the frozen
companion review package, with a file manifest, SHA-256 checksums and the scope of the included
experiments. The records identify policy, task, simulator condition, inference build and random
seeds. Development is at https://github.com/Jun-Jason-Ji/benchmark-ranking-determinacy.
As verified on 23 September 2026, the latest public archive is v1.1.3,
https://doi.org/10.5281/zenodo.22896508; the concept DOI
https://doi.org/10.5281/zenodo.22893458 indexes the release history. That earlier archive is
not interchangeable with the current review snapshot, which includes additional evaluation data.
The current snapshot is supplied with this submission and identified by its accompanying manifest;
it has not yet been published as a new public archive. The real-robot reference
values in Section 8.4 come from the benchmark's published source tables, whose location
is cited, rather than from experiments conducted for this study.
```

> Public GitHub, Zenodo and DOI-registry metadata were checked on 2026-09-23: the latest published
> release is v1.1.3, DOI `10.5281/zenodo.22896508`. The current manuscript includes later results.
> Its frozen review package must be identified separately; no new public deposition was performed.

## Materials availability

```
Not applicable.
```

## Code availability

```
The companion review package supplies the analysis scripts and reproduction instructions. The
project repository also contains the evaluation harness, configuration-census utilities, resumable
queues and Vulkan compatibility layer described in Appendix B. Original code is released
under the MIT licence; records and outputs derived from third-party simulators, policies and
demonstrations remain subject to the third-party terms identified in the accompanying notices. The review evidence index maps the main claims
to their records and analysis commands. The current review snapshot should be used when reproducing
the manuscript rather than an earlier archived version.
```

> Keep the code, records, regeneration instructions and checksum manifest together in the frozen
> companion review package. The earlier archived releases are not a substitute for that package.

## Author contributions

> Updated from the authors’ explicit contribution statement on 2026-09-23.
> Enter these assignments as CRediT roles if supported, otherwise paste the prose below.

```
Author contributions.

Jun Ji: Data curation, Methodology, Formal analysis, Resources, Writing – original draft.
Bowen Tan: Software, Formal analysis, Writing – review & editing.
Yi Li: Formal analysis, Project administration, Writing – review & editing.
Xiaolei Zhang: Software, Project administration, Writing – review & editing.
Yizhou Zhao: Software, Writing – review & editing.
Shengjie Guo: Software, Writing – review & editing.
Yi Sui: Supervision, Validation, Writing – review & editing.
```

> Before submission, the corresponding author should confirm every listed author
> meets the authorship requirements and approves the final manuscript. The CRediT list
> records contributions; it is not, by itself, a record of final approval.

## Authors, affiliations and ORCIDs (for the interface author fields)

Order as submitted. Yi Sui is the corresponding author.

Updated at the authors' direction on 2026-09-23: Yizhou Zhao is fifth, immediately before Shengjie Guo. His CRediT roles match Shengjie Guo's. The supplied institutional identities, emails and ORCIDs are preserved. Affiliation addresses uniformly use institution, city/region and country, without postal codes. On 2026-09-24, the authors specified Sino-French Institute for Yizhou Zhao and the College of Computer and Information Engineering for Shengjie Guo. The Sino-French Institute is at RUC’s Suzhou campus, so affiliation 3 uses Suzhou. The department names and city are synchronized with both manuscript languages and CITATION.cff.

| # | Author | Affiliation | Email | ORCID |
|---|---|---|---|---|
| 1 | Jun Ji | Qingdao University (1) | junji@qdu.edu.cn | 0000-0003-3194-2183 |
| 2 | Bowen Tan | HKUST (2) | btanab@connect.ust.hk | 0009-0007-0554-9261 |
| 3 | Yi Li | Qingdao University (1) | ly2005@qdu.edu.cn | 0000-0002-4185-3152 |
| 4 | Xiaolei Zhang | Qingdao University (1) | zhangxiaolei@qdu.edu.cn | 0000-0002-0122-4554 |
| 5 | Yizhou Zhao | Sino-French Institute, Renmin University of China (3) | yizhou-zhao@ruc.edu.cn | 0009-0004-7515-6322 |
| 6 | Shengjie Guo | College of Computer and Information Engineering, Inner Mongolia Agricultural University (4) | guosj@emails.imau.edu.cn | 0009-0004-6852-4836 |
| 7 | **Yi Sui** (corresponding) | Qingdao University (1) | suiyi@qdu.edu.cn | 0009-0001-8081-5183 |

Affiliations as typeset:

1. College of Computer Science and Technology, Qingdao University, Qingdao, China
2. The Hong Kong University of Science and Technology, Hong Kong SAR, China
3. Sino-French Institute, Renmin University of China, Suzhou, China
4. College of Computer and Information Engineering, Inner Mongolia Agricultural University, Hohhot, China

> Ethan Yixuan Ji was removed from the author list on 2026-09-21, and affiliation 4 (The Middle
> School Affiliated to Qingdao University) went with him, since no remaining author was attached to
> it. That historical removal is retained for the record; the current affiliation numbers are shown above.
>
> ✅ Confirmed by the authors 2026-09-22: **Hohhot** as Inner Mongolia Agricultural University's
> city, and **Shengjie Guo** in given-name-first order as Springer typesets it. Nothing outstanding
> in this section.

## Generative AI disclosure

> Updated 2026-09-23 to include the tools and assistance used during manuscript preparation and
> the subsequent submission review. This statement assigns responsibility to the authors without
> implying that every design or analytical decision was made without AI assistance.
> The block below matches the independent Use of generative AI section following the conclusion.

```
Large language models (OpenAI ChatGPT/Codex) assisted with manuscript revision, analysis scripts. Quantitative results are computed from the recorded episodes by the supplied
scripts. The authors are responsible for the study design, verification and interpretation of the
results and the final manuscript; no language model is listed as an author.
```

---

## Other interface fields to expect

- **Title, abstract, keywords** — use the final abstract in `main.tex`, verified within the journal's
  150–250 limit. Keywords are the six in `main.tex`; the limit is 4–6.
- **Corresponding author** with an active email address, and ORCID if you have one (16 digits).
- **Suggested reviewers** — follow the submission system's requirements. If supplied, choose
  relevant expertise and disclose actual conflicts; benchmark authorship alone is not a reason to
  exclude a qualified reviewer. No reviewer names have been invented or submitted in this closeout.
- **Brief biography and photograph** — the journal requires these *with the accepted manuscript*,
  not at submission. Nothing to do now.
- **Publishing model** — hybrid; the Open Choice option carries an article processing charge. This is
  selected after acceptance.
