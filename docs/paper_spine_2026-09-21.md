# Paper Spine — Option A (2026-09-21)

**Supersedes** the contribution ledger in `paper_outline_Q2_2026-09-20.md` §2 and the one-sentence thesis in
its §1. The section structure in that outline's §3 still holds, with §6 demoted (see C5 below) and a new
headline section promoted out of §8.3.

**Why the spine moved.** Two results landed after the 09-20 outline was written. T2-A (S=5 seeds) cut the
point-vs-set disagreement from 3 pairs to 1 and retracted §6.5 entirely, so C4 can no longer carry a title.
The fractal real-vs-sim reversal queue then finished, and it is adverse: over the dynamics compatible set the
union bound *declares* the ordering the real robot reverses. Under the old spine that is a wound; under this
spine it is a measurement of where the criterion's reach ends, which is a result we can state and defend.

Target: **Autonomous Robots** (Springer), RAS backup. Journal, rolling submission, no deadline.

Written in English for direct transfer to the manuscript; internal notes are in blockquotes.

---

## Title

**What Determines a Simulation Benchmark Ranking? Structural Blindness, Finite Configuration Grids, and
Evaluation Budget in Simulation-Based Policy Comparison**

> Alternatives: *"Are Simulation-Based Policy Rankings Determined by Their Own Evidence? An Audit of a
> Sim-to-Real Evaluation Benchmark"* — more confrontational, better for a conference. The chosen title keeps
> the three evidence sources in view, which is what the ledger below actually delivers.

## Thesis, one sentence

**A simulation benchmark's policy ranking is not determined by the evidence used to produce it: the
calibration data is exactly uninformative about part of the dynamics, the benchmark is a finite
configuration population whose largest variance source is a visual variant it averages over silently, and
the published evaluation budget resolves one of the four rankings it reports — and we measure how far a
set-valued verdict repairs this, including where it does not.**

> The load-bearing change from the 09-20 thesis: it no longer promises that invisible parameters *change
> rankings* (C4's strong form is false, and its weak form now appears in 1 of 17 pairs). It promises that
> ranking claims are underdetermined, which is what all three evidence lines independently support.

---

## Contribution ledger (submission order)

| # | Contribution | Evidence | Strength |
|---|---|---|---|
| **C1** | **Exact structural non-identifiability.** SIMPLER-style free-space replay identifies the joint PD ratio `d/k` and the execution delay; a common `(k,d)` scaling and the torque limit are *exactly* invariant — not weakly identified. 98 BridgeData V2 demonstrations, two independent simulator stacks: max trajectory difference 0.141 mm (ManiSkill3) / 0.207 mm (original SIMPLER main) under common scaling, and **bitwise zero** under torque ×0.5. Ratio and delay give the expected bowl-shaped loss (error increments +0.004 to +0.008). | `replay_sysid/{sweep_v1,grid}/iso_invariance.md`, `replay_sysid_ms2/FINDING_original_stack.md`, Fig. 1 | **strong** — analytic + dual-stack |
| **C2** | **The benchmark is a finite configuration population, not a sample.** `episode_id` determines the initial state modulo `n_xy·n_quat`: 24 configurations for ms2 eggplant/spoon/carrot, 64 for ms3 eggplant, 300 for fractal coke-can (4 URDF variants × 3 can orientations × 25 xy). Beyond that count episodes are exact repeats. **Two widely used ports evaluate different benchmarks** (eggplant: 3 vs 8 orientations, different quaternions, best-match dot product 0.54). The official protocol is already a census × 3 fixed seeds = 72 episodes; the literature commonly runs it once. | `docs/methods_census_2026-09-19.md §1`, `FINDING_seed_set_bug.md`, `FINDING_cross_stack_eggplant.md`, `scripts/task_configs.py` | **strong** — verifiable by reading code |
| **C3** | **Estimand and an uncertainty budget that inverts the usual priorities.** Two legitimate estimands (benchmark value vs generalisation value); deterministic policies have no seed axis, so a census is exact. Enumerating the grid sets configuration sampling error to **exactly zero** and leaves: policy-seed noise sd **0.055**, implementation-build drift **0.078** (episode-level agreement 0.73–0.88 across inference-stack versions), parameter displacement **0.141** on the complete census (0.133–0.161 by pair; the wider 0.14–0.23 range is the retracted 48-configuration measurement), and — largest known hidden variable — the benchmark's silent averaging over 4 robot **texture** variants, range **0.400** (octo-base per-variant: 0.000 / 0.280 / 0.013 / 0.400, sd 0.199). `urdf_version` changes only texture colour, carries no physics, and is invisible to replay calibration by construction. | `FINDING_platform_drift.md`, `FINDING_estimand_matters.md`, `fractal_validation/FINDING_urdf_variance.md`, Fig. 2, Table 3 | **strong** — includes our own falsification |
| **C4** | **The published protocol does not resolve the rankings it reports.** Following it exactly reproduces the published rates to mean absolute difference **0.026** (max 0.042) over 8 cells, and on the second embodiment to +0.003 (octo-base coke-can 0.173 vs 0.170) and −0.040 (rt-1-x 0.527 vs 0.567) — so the pipeline is trustworthy. At that same 72-episode budget, **only 1 of 4 octo-small vs octo-base orderings is decidable** (spoon, +0.347 [+0.235, +0.459]); on carrot a faithful re-run **reverses the published sign** (ours −0.056, published +0.014, both far inside seed noise). Across-seed range within a cell averages 0.109 and reaches 0.250. | `paper_draft_s8.md` §8.2–8.3, Tables 4–5, `FINDING_official_protocol.md` | **strong** — promoted to headline; needs no machinery to state |
| **C5** | **A decision-relevant instance of non-identifiability, stated as a budget property.** Torque ×0.5 — exactly invisible to calibration (C1) — raises OpenVLA's eggplant benchmark value from 0.156 to 0.271 on the complete 64-configuration census (+0.115), displacing four cross-family Δ by 0.133–0.161 (mean **0.141**) and moving pairs with margin ≲0.2 from *decidable* to *abstain*; margin 0.35 survives. Mechanism on the census: positive in 7 of 8 orientations, gain anticorrelated with nominal success (r = −0.44), 13 of 51 outright failures rescued. Negative control (octo-small) flat and directionless. **The strong form is false**: no calibration-invisible parameter reverses a sign-determined ranking anywhere we looked. And the weak form is budget-dependent — at the 1–3 seed budgets common in the literature, 3 of 17 pairs disagree between point and set; at S=5, **1 of 17**. | `FINDING_openvla_torque_replicated.md`, `FINDING_t2a_seeds.md`, `FINDING_estimand_matters.md §2d`, `CORE_TABLE.md`, Figs. 3–4 | **medium** — demoted from headline; one task, one surviving pair |
| **C6** | **A verdict ladder with its reach measured — including where it stops.** Point calibration / union bound / GP simultaneous band. On synthetic ground truth the point criterion's error rate *rises* with episode count (to 0.88); the union bound attains its sampling-extremum guarantee; the GP band is valid but low-powered (0.47 → 0.77 when not extrapolating). On real data, verdict stability: point 0.50, union_ctrl 0.88, union_all 1.00. **The negative result that delimits it:** on the one policy pair where published real-robot results contradict the simulator (rt-1-converged vs rt-1-15pct on coke-can — real 0.853 vs 0.920, sim 0.857 vs 0.710), 1,800 census episodes show the union bound over the dynamics compatible set **declaring the ordering the real robot reverses** (L = +0.070). Adding the texture variant as a set dimension yields abstention (L = −0.067), but all 12 cells have positive point margins, so that abstention is our own power and does not survive more episodes. The criterion's reach stops at the dynamics family it can represent. | `benchmark/track_s/FINDING_track_s.md`, `benchmark/track_r/track_r_summary.md`, `fractal_reversal/` (new), Figs. 5–6 | **medium-strong** — synthetic coverage + real-ground-truth failure |
| **C7** | **Reproducibility assets.** Original SIMPLER main running headless on a GPU-less WSL host via a purpose-built Vulkan layer faking `VK_KHR_external_semaphore_fd`; the configuration-census protocol; append-only `runs.jsonl` provenance; six resumable queues. | `third_party/vk_fakesemfd/`, `scripts/task_configs.py`, `PROVENANCE_AUDIT_2026-09-19.md` | medium — appendix / release value |

**Negative results and self-retractions are stated as an asset, in §1.** Claims of our own that the paper
withdraws:

1. The "two-seed-set replication" of the OpenVLA torque effect — withdrawn because `episode_id` fully
   determines the configuration and OpenVLA inference is deterministic, so those were repeat runs.
2. "Eggplant nominal octo-small > octo-base" — withdrawn; three same-generation seed sets give
   +0.141 / −0.031 / −0.047.
3. T2-A: the point-vs-set disagreement count (3 → 1) **and** §6.5's between-condition sign reversal
   (density ×0.5: −0.021 at S=3 → +0.042 at S=5), which fall together because the same queue refuted both.

Separately, four 24/48-episode ranking-flip candidates were withdrawn *before being claimed*, when adding
episodes removed them. The fractal result in C6 is not a retraction of a published claim but an adverse
outcome for the method, and is reported as such.

> Internal: count reconciled 2026-09-21 against `FINDING_t2a_seeds.md` §4, which names the three and calls
> T2-A the third. The four candidates are not in the count because they were never asserted; §1.2 of
> `paper_draft_s1_s3.md` states them in that separate sentence for exactly this reason. "Three retractions"
> in the abstract is therefore correct as written.

> Internal: the retraction list is the strongest available answer to "how do we know the rest is reliable."
> It goes in §1 as a short paragraph, not buried in §9. Independent falsifications that we ran ourselves and
> acted on are a stronger reliability argument than any number of confirmations.

---

## Abstract (draft)

Simulation benchmarks are increasingly used to rank robot foundation policies, and a calibrated simulator is
treated as evidence about which policy is better. We ask a question prior to "how well does simulation
correlate with reality": given the evidence actually used to build and run such a benchmark, which ranking
claims does that evidence determine? We answer on a widely used sim-to-real evaluation suite, across two
embodiments, eight policy configurations across three model families, and a complete enumeration of each
task's configuration grid.

Three findings. First, the calibration protocol is structurally blind: replaying 98 real demonstrations
identifies the joint-controller ratio and the execution delay, but a common gain scaling and the torque limit
leave the replay trajectory unchanged — by 0.14–0.21 mm and bitwise exactly, respectively, on two independent
simulator stacks. Second, the benchmark is a finite configuration population rather than a sample: the
episode index determines the initial state modulo 24 to 300 configurations, two widely used ports of the
suite enumerate different grids, and enumerating the grid — which sets configuration sampling error to zero —
leaves policy-seed noise (sd 0.055), implementation-build drift (0.078) and, largest of all, the suite's
silent averaging over four robot texture variants whose success rates span 0.400. Third, following the
published protocol exactly reproduces the published rates to 0.026 mean absolute difference, and shows that
the same 72-episode budget resolves only one of the four policy orderings it reports, while a second reverses
sign under faithful re-run.

We then measure what a set-valued verdict over the calibration-compatible parameters buys, and where it
stops. It is conservative as designed on synthetic ground truth and stabilises verdicts on real data, and at
the one- to three-seed budgets common in practice it disagrees with point calibration on 3 of 17 policy
pairs. But on the single pair for which published real-robot results contradict the simulator, 1,800 census
episodes show it declaring the ordering the real robot reverses: the sim-to-real gap on that pair lies
outside the dynamics family the calibration data can constrain. We report three retractions of our own
claims, and conclude that simulation-based ranking claims must state their estimand and budget, and that a
compatible-set criterion bounds the ambiguity it can represent — not the ambiguity that matters most.

> Internal: ~330 words, trim to ~250 for AuRo. First cut candidates: the parenthetical variance numbers in
> paragraph 2 (keep 0.400, drop 0.055/0.078), and the embodiment/policy inventory in paragraph 1.
> Do **not** cut the last sentence of paragraph 3 — the honest statement of the failure is what makes the
> rest credible, and a reviewer who finds it only in §9 will read it as concealment.

---

## Section map after the reframe

| § | Content | Status |
|---|---|---|
| 1 | Introduction: the three evidence lines, C1–C7, the retraction paragraph, explicit scope | ✅ `paper_draft_s1_s3.md` §1 |
| 2 | Related work: sim-to-real evaluation, identifiability, partial identification, evaluation reproducibility | ✅ `paper_draft_s1_s3.md` §2 — citations still to fill |
| 3 | Problem setup: notation, compatible set by test inversion, the decision problem, the error ledger | ✅ `paper_draft_s1_s3.md` §3 |
| 4 | Structural blindness (C1) | ✅ `paper_draft_s4_s5.md` |
| 5 | What a finite benchmark measures (C2+C3) | ✅ `paper_draft_s4_s5.md` — URDF-variant row added 09-21 |
| 6 | Reproducing the published protocol (C4) — **promoted from §8** | ✅ `paper_draft_s8.md` (header notes the renumber) |
| 7 | Decision-relevant non-identifiability (C5) — **demoted, rewritten** | ✅ `paper_draft_s7_nonidentifiability.md`; old `paper_draft_s6.md` kept for audit only |
| 8 | The verdict ladder and its reach (C6), ending on the fractal negative | ✅ `paper_draft_s8_ladder.md` |
| 9 | Limitations | ✅ `paper_draft_s9_s10.md` §9 |
| 10 | Conclusion | ✅ `paper_draft_s9_s10.md` §10 |

**Filename collision to resolve at assembly:** `paper_draft_s8.md` is the new §6 and `paper_draft_s8_ladder.md`
is the new §8. Rename both when the manuscript is assembled rather than now, so the header notes stay
meaningful.

> Renumbering note: the reproduction section moves from 8 to 6 because it is now a headline contribution and
> should precede the machinery, not follow it. A reader should meet "the published budget resolves 1 of 4
> rankings" before being asked to care about compatible sets.

## Open items before submission

Done 2026-09-21:

- ✅ `CORE_TABLE.md` regenerated with the fractal reversal pair (18 rows; disagreement count stays 1). Its
  union bound [+0.07, +0.24] matches `analyze_fractal_reversal.py` exactly through a separate code path.
  The generator now also prints each task's condition count, because the fractal row unions over 2 conditions
  where the bridge rows union over 5 and the two must not be read as equally strong.
- ✅ `analysis_fractal_reversal.md` + `scripts/analyze_fractal_reversal.py`, and a **draft**
  `FINDING_fractal_reversal.md` that needs your sign-off (the hand-written/generated split is your rule).
- ✅ §5.5 gains the texture-variant row, and Fig. 2 is regenerated with a fourth bar at 0.400 (palette slot 3,
  re-validated: worst adjacent CVD ΔE 9.2, normal-vision 16.3; the aqua contrast WARN is covered by the
  per-bar direct labels). The "irreducible" bracket now spans both the torque and texture rows.
- ✅ All remaining sections drafted (§1–§3, §7, §8, §9, §10).

**Blocking, and needs your decision:**

1. **Two aggregations are in circulation for the uncertainty budget, and the figure and the text disagree.**
   Fig. 2 and `make_figures_v2.py` compute medians/maxima over all Octo pairs and both core conditions at
   S = 5: single-seed half-width 0.138, three seeds 0.079, ten seeds 0.044, build drift 0.055, torque shift
   0.121. The prose in §5.5, §7.6 and `theory_protocol.md §6.1` uses the headline pair on the 64-configuration
   eggplant census at S = 3: ±0.108 / ±0.062 / ±0.034, drift 0.078, shift 0.141. Both are defensible; shipping
   one in the figure and the other in the text is not. The gaps are not cosmetic — 0.121 vs 0.141 on the
   quantity §7.6 calls δ, and 0.055 vs 0.078 on build drift. Pick the paper's standard scope, state it once
   in §5, and regenerate whichever side does not match. **The abstract currently quotes the prose set.**
2. §2's citations are placeholders.
3. Cover letter: lead with C4's reproduction (0.026), and frame the real-robot question as answered by
   published reference values on two embodiments rather than deferred.
