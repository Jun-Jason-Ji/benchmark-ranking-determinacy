# Declarations — to paste into the Editorial Manager submission interface

The journal's guidelines are explicit on this point: **only the declaration information submitted via
the interface appears in the published version.** The same text is in `main.tex` under
"Declarations", but entering it in the manuscript alone is not sufficient. Copy each block below into
the corresponding interface field.

Review every one of these before submitting — several are assertions about the authors, not about
the research. All of them are settled, including the archived DOI and the generative-AI wording.
Nothing in this file is outstanding.

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
All episode-level records underlying the results are openly available in the archived release at
https://doi.org/10.5281/zenodo.22893458, which resolves to the current version and lists every version with its own DOI.
The records and the scripts that regenerate every table and figure are byte-identical across all
versions to date, so any version reproduces the results reported here. Development is at https://github.com/Jun-Jason-Ji/benchmark-ranking-determinacy. They are append-only JSON Lines
files, one per policy, task and simulator condition, together with the per-run provenance log
recording the port branch, inference-stack version and random seeds for every episode, and
SHA256SUMS.txt over the 997 record files. The real-robot reference values used in Section 8.4 are
the published values distributed with the benchmark's own source and are not ours to redistribute;
the manuscript cites their location.
```

> ✅ Published 2026-09-22. The statements cite the **concept DOI 10.5281/zenodo.22893458**, which always resolves to the
> newest version, and name **no version at all**.
>
> Both of those are deliberate, and the second took two attempts to get right. A version DOI is
> minted by the snapshot that contains the manuscript, so it necessarily lands one commit after the
> archive it names; re-tagging to close that gap moves it rather than closing it. Naming a version
> in prose instead has exactly the same defect for exactly the same reason. The statements therefore
> assert the property that is version-independent and is what a reader following the pointer
> actually needs: the records and regeneration scripts are byte-identical across every version, so
> any of them reproduces the paper. That is verifiable from `SHA256SUMS.txt` and does not decay.
>
> Repository: https://github.com/Jun-Jason-Ji/benchmark-ranking-determinacy

## Materials availability

```
Not applicable.
```

## Code availability

```
The evaluation harness, the configuration-census utilities, the resumable evaluation queues, the
analysis scripts that generate every table and figure in this paper, and the Vulkan compatibility
layer that allows the original reference stack to render headless on a host without a GPU are openly
available in the same archived release, https://doi.org/10.5281/zenodo.22893458, under the MIT
licence for original code; evaluation records and outputs derived from third-party simulators,
policies and demonstration data are governed by the NOTICE file in that release.
REPRODUCIBILITY.md gives the commands that regenerate every table and figure from the records.
```

> ✅ Same archived release: https://doi.org/10.5281/zenodo.22893458 — MIT for original code, with records and
> derived outputs governed by the NOTICE file in the release.

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

> ✅ Settled 2026-09-22. Shortened at the authors' direction to state the use without enumerating
> it. The last two clauses are kept for policy rather than length: Springer requires the disclosure,
> and states that language models cannot be authors. Worth re-checking the journal's current wording
> at submission time, since these policies change.

```
A large language model (Anthropic Claude) was used to assist with writing and revising the
manuscript, and to help write the analysis and figure-generation scripts. The study design, the
experiments and the interpretation of results are the authors' own; all quantitative results are
computed from the episode records by the released scripts. The authors have verified the content and
take full responsibility for it, and no language model is listed as an author.
```

---

## Other interface fields to expect

- **Title, abstract, keywords** — the abstract in `main.tex` is 247 words, inside the journal's
  150–250 limit. Keywords are the six in `main.tex`; the limit is 4–6.
- **Corresponding author** with an active email address, and ORCID if you have one (16 digits).
- **Suggested reviewers** — usually optional. If you supply them, avoid anyone from the groups whose
  benchmark the paper audits; the paper is a reproduction-plus-critique of their suite and a reviewer
  from that group is both an obvious choice and an awkward one. Note that the cover letter offers
  suggestions on request.
- **Brief biography and photograph** — the journal requires these *with the accepted manuscript*,
  not at submission. Nothing to do now.
- **Publishing model** — hybrid; the Open Choice option carries an article processing charge. This is
  selected after acceptance.
