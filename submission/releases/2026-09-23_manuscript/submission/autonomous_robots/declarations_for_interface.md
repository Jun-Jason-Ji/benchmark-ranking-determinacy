# Declarations — to paste into the Editorial Manager submission interface

The journal's guidelines are explicit on this point: **only the declaration information submitted via
the interface appears in the published version.** The same text is in `main.tex` under
"Declarations", but entering it in the manuscript alone is not sufficient. Copy each block below into
the corresponding interface field.

Review every one of these before submitting — several are assertions about the authors, not about
the research. The confirmed author, funding and competing-interest statements are retained below.
The current results will be supplied in a frozen companion review package; a version-specific
public deposit matching that package has not yet been verified. The AI disclosure records the tools
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
The episode-level records underlying this manuscript will be supplied in a frozen companion review
package. The package will include append-only JSON Lines files by policy, task and simulator
condition, per-run provenance logs recording the port branch, inference-stack version and random
seeds, and a SHA256SUMS.txt manifest identifying the frozen files. Earlier releases are available
through the concept DOI https://doi.org/10.5281/zenodo.22893458; they do not contain all records
added for the current manuscript. A version-specific public deposit matching the current review
package has not yet been verified, and the concept DOI should not be read as confirmation that the
current results are publicly archived. Development is at
https://github.com/Jun-Jason-Ji/benchmark-ranking-determinacy. The real-robot reference values used
in Section 8.4 are the published values distributed with the benchmark's own source and are not
ours to redistribute; the manuscript cites their location.
```

> Archive status checked against `CHANGELOG.md` on 2026-09-23: its DOI table ends at v1.1.2 and
> explicitly describes versions absent from the table as not yet archived. The current manuscript
> includes later results. Its frozen review package and corresponding checksum manifest must be
> identified separately from those earlier archives; a current version-specific deposit remains
> unverified.

## Materials availability

```
Not applicable.
```

## Code availability

```
The evaluation harness, configuration-census utilities, resumable evaluation queues, analysis and
figure-generation scripts, and Vulkan compatibility layer will be supplied with the frozen
companion review package. REPRODUCIBILITY.md gives the commands for regenerating the manuscript's
tables and figures from the accompanying records. Original code is licensed under MIT; evaluation
records and outputs derived from third-party simulators, policies and demonstration data are
governed by the package's NOTICE file. Development is at
https://github.com/Jun-Jason-Ji/benchmark-ranking-determinacy. Earlier code releases are available
through https://doi.org/10.5281/zenodo.22893458. A version-specific public deposit of the current
scripts and matching records has not yet been verified.
```

> Keep the code, records, regeneration instructions and checksum manifest together in the frozen
> companion review package. The earlier archived releases are not a substitute for that package.

## Author contributions

> ✅ Settled 2026-09-21. CRediT roles carried over from the authors' prior submission
> (`IVC_Paper2_Submission_2026-09-12`); Shengjie Guo, who is new to this paper, takes the same roles
> as Xiaolei Zhang, as directed. Paste as CRediT roles if the interface offers them, otherwise as the
> prose block below.

```
CRediT authorship contribution statement

Jun Ji: Data curation, Methodology, Formal analysis, Resources, Writing – original draft.
Bowen Tan: Software, Formal analysis, Writing – review & editing.
Yi Li: Supervision, Project administration, Writing – review & editing.
Xiaolei Zhang: Supervision, Project administration, Writing – review & editing.
Shengjie Guo: Supervision, Project administration, Writing – review & editing.
Yi Sui: Supervision, Validation, Writing – review & editing.
```

> Note for the interface: journal policy requires every listed author to have contributed
> substantially and to have approved the manuscript, and this is the statement that asserts it.

## Authors, affiliations and ORCIDs (for the interface author fields)

Order as submitted. Yi Sui is the corresponding author.

| # | Author | Affiliation | Email | ORCID |
|---|---|---|---|---|
| 1 | Jun Ji | Qingdao University (1) | junji@qdu.edu.cn | 0000-0003-3194-2183 |
| 2 | Bowen Tan | HKUST (2) | btanab@connect.ust.hk | 0009-0007-0554-9261 |
| 3 | Yi Li | Qingdao University (1) | ly2005@qdu.edu.cn | 0000-0002-4185-3152 |
| 4 | Xiaolei Zhang | Qingdao University (1) | zhangxiaolei@qdu.edu.cn | 0000-0002-0122-4554 |
| 5 | Shengjie Guo | Inner Mongolia Agricultural University (3) | guosj@emails.imau.edu.cn | 0009-0004-6852-4836 |
| 6 | **Yi Sui** (corresponding) | Qingdao University (1) | suiyi@qdu.edu.cn | 0009-0001-8081-5183 |

Affiliations as typeset:

1. College of Computer Science and Technology, Qingdao University, Qingdao 266071, China
2. The Hong Kong University of Science and Technology, Hong Kong SAR, China
3. Inner Mongolia Agricultural University, Hohhot, China

> Ethan Yixuan Ji was removed from the author list on 2026-09-21, and affiliation 4 (The Middle
> School Affiliated to Qingdao University) went with him, since no remaining author was attached to
> it. The other three affiliation numbers are unchanged.
>
> ✅ Confirmed by the authors 2026-09-22: **Hohhot** as Inner Mongolia Agricultural University's
> city, and **Shengjie Guo** in given-name-first order as Springer typesets it. Nothing outstanding
> in this section.

## Generative AI disclosure

> Updated 2026-09-23 to include the tools and assistance used during manuscript preparation and
> the subsequent submission review. This statement assigns responsibility to the authors without
> implying that every design or analytical decision was made without AI assistance.

```
Generative AI tools (Anthropic Claude and OpenAI ChatGPT/Codex) assisted with drafting and revising
the manuscript and submission materials, developing analysis and figure-generation scripts, and
checking statistical calculations and consistency of reporting. Quantitative results are computed
from the episode records by the analysis scripts. The authors take full responsibility for the
study design, conduct of the experiments, analysis, interpretation and final content. No AI system
is listed as an author.
```

---

## Other interface fields to expect

- **Title, abstract, keywords** — the abstract in `main.tex` is 208 words, inside the journal's
  150–250 limit. Keywords are the six in `main.tex`; the limit is 4–6.
- **Corresponding author** with an active email address, and ORCID if you have one (16 digits).
- **Suggested reviewers** — follow the submission system's requirements. If supplied, choose
  relevant expertise and disclose actual conflicts; benchmark authorship alone is not a reason to
  exclude a qualified reviewer. No reviewer names have been invented or submitted in this closeout.
- **Brief biography and photograph** — the journal requires these *with the accepted manuscript*,
  not at submission. Nothing to do now.
- **Publishing model** — hybrid; the Open Choice option carries an article processing charge. This is
  selected after acceptance.
