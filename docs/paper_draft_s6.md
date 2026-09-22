# Draft: Section 6 — Decision-Relevant Non-Identifiability (2026-09-20)

> **SUPERSEDED (2026-09-21). Do not cite this file.** The rewrite is
> `docs/paper_draft_s7_nonidentifiability.md`, and under the Option-A spine
> (`docs/paper_spine_2026-09-21.md`) this material is **§7**, not §6 — the new §6 is the published-protocol
> reproduction in `docs/paper_draft_s8.md`. This file is kept only so the pre-T2-A numbers remain auditable:
> §6.2's "3 of 17 disagree" (now 1), §6.5's between-condition sign reversal (withdrawn), and §6.6's
> "budget cannot explain the disagreement" (inverted — budget explained two of three). The original status
> note follows.

Status: **SUPERSEDED IN PART — rewrite required (2026-09-21).** The S=5 seed queue has finished and it
overturned the section's headline. Disagreements fall from 3 to 1; the per-condition sign reversal claimed in
§6.5 does not survive more seeds (density ×0.5: −0.021 at S=3 becomes +0.042 at S=5); and §6.6's conclusion
inverts — budget *did* explain two of the three. See
`results/controller_sweep_gpu_rep3/FINDING_t2a_seeds.md` for the replacement numbers and the honest
restatement. Do not quote §6.2, §6.5 or §6.6 below until they are rewritten; §6.3 and §6.4 (the torque
mechanism) are unaffected and still stand. All numbers are census-scope: the
task's configuration grid is fully enumerated, so configuration sampling error is zero and the intervals
carry policy noise only (§5.3). Sources: `results/CORE_TABLE.md`,
`results/controller_sweep_gpu_rep3/analysis_benchmark_value_union.md`,
`results/controller_sweep_gpu_rep3/FINDING_estimand_matters.md`.
Written in English for direct transfer to the manuscript; internal notes are in blockquotes.

---

## 6 Decision-Relevant Non-Identifiability

Section 4 showed that the calibration protocol cannot see certain parameter directions. That alone is not
interesting: an unidentifiable parameter matters only if moving it inside the compatible set changes an answer
someone acts on. This section shows that it does.

### 6.1 The claim, stated so it can fail

Fix a task, a pair of policies \(i, j\), and the compatible set \(C_\alpha\) of simulator parameters the
calibration data cannot distinguish (§3). Two verdicts are available:

* **point calibration** — the standard practice: evaluate at the fitted parameter \(\hat z\) alone, and
  declare \(i \succ j\) when the interval for \(\hat\Delta_{ij}(\hat z)\) excludes zero;
* **the union bound** — declare \(i \succ j\) only when every \(z \in C_\alpha\) agrees in sign, taking the
  interval \([\min_z \text{lo}(z), \max_z \text{hi}(z)]\).

The claim is that these disagree: point calibration declares orderings the calibration data cannot support.
Its **strong form** — that some \(z \in C_\alpha\) reverses a ranking's sign — is what a reader would expect
and would be the more dramatic result. **We report it as false.** Across every pair, task and condition we
measured, no calibration-invisible parameter reverses a sign-determined ranking. What happens instead is
weaker and, we argue, more consequential in practice: the parameter moves \(\Delta\) far enough to cross the
decision boundary, turning a declared ordering into an abstention.

> Internal: stating the strong form and reporting it false is deliberate — it is the honest form of the
> contribution and pre-empts the obvious reviewer question ("did you look for sign flips?"). Track S (§7)
> shows the ladder would catch a flip if one existed.

### 6.2 The core table

**Table 1** reports both verdicts for every policy pair on every task, with the provenance each number needs:
configurations covered, independent runs per policy, and the variance model. Of 17 rows, **3 disagree**
`[T2-A]`, all on the eggplant task with its 64-configuration grid:

| pair | point Δ | point verdict | union interval | union verdict |
|---|---:|---|---|---|
| octo-small vs octo-base@hist1 | +0.117 [+0.04, +0.20] | octo-small ≻ | [−0.03, +0.28] | abstain |
| octo-base vs octo-base@hist1 | +0.083 [+0.00, +0.17] | octo-base ≻ | [−0.10, +0.17] | abstain |
| octo-base@hist1 vs openvla-7b-4bit | +0.203 [+0.13, +0.28] | octo-base@hist1 ≻ | [−0.00, +0.42] | abstain |

The pattern across the full table is a margin threshold: pairs with \(|\Delta| \ge 0.29\) survive both
verdicts, pairs with \(|\Delta| \le 0.25\) do not. That threshold is not a free parameter — it is set by the
size of the parameter-induced shift measured in §6.3.

### 6.3 The mechanism: one parameter, measured on a complete census

The torque limit is the cleanest case. It is *exactly* invisible to calibration (§4.2 (ii)): along
demonstrated velocities the commanded torque never saturates, so replay loss is independent of it to
floating-point zero. Halving it therefore stays inside \(C_\alpha\) by construction, not by a fitting
tolerance.

On the 64-configuration eggplant census it moves the cross-family comparison as follows:

| pair | nominal Δ | torque ×0.5 Δ | shift |
|---|---:|---:|---:|
| octo-small vs OpenVLA | +0.320 [+0.245, +0.396] | +0.187 [+0.121, +0.254] | −0.133 |
| octo-base vs OpenVLA | +0.286 [+0.209, +0.364] | +0.125 [+0.054, +0.196] | −0.161 |
| octo-small@hist1 vs OpenVLA | +0.250 [+0.175, +0.325] | +0.115 [+0.046, +0.183] | −0.135 |
| octo-base@hist1 vs OpenVLA | +0.203 [+0.128, +0.278] | +0.068 [−0.000, +0.135] | −0.135 |

The shift is 0.133–0.161, mean 0.141, and it is remarkably uniform across pairs — consistent with a single
policy (OpenVLA) moving, not four independent effects. The last pair, whose nominal margin is smallest,
crosses the boundary: its torque-condition interval has lower bound −0.000, so the union verdict abstains
while point calibration declares. `[T2-A]`

> Internal: an earlier version of this analysis, on 48 of the 64 configurations, put the shift at 0.23–0.25
> and had two pairs crossing. The partial census overstated the effect. Every effect size in this paper is
> census-scope for this reason, and the correction is recorded in `FINDING_estimand_matters.md` §5 rather
> than silently applied.

### 6.4 Why it is not an artefact

Three checks.

**It is a property of one policy, and a large one.** At the single-policy level, halving the torque limit
raises OpenVLA's eggplant benchmark value from 0.156 to 0.271 on the complete 64-configuration census
(+0.115), while octo-small, run as a negative control over the same census, moves by −0.018 and the other
three Octo policies by −0.06 to +0.02 with no consistent direction. The asymmetry has a mechanism: OpenVLA
emits larger single-step displacements, so at the nominal limit it pushes the eggplant away or re-grasps
repeatedly on contact; the `info`-level counters agree (grasp rate +0.12/+0.18, fewer repeated gripper
closures).

**It is broad, not driven by a few configurations.** Over the complete census 16 configurations improve, 42
are unchanged and 6 degrade, and the mean change is positive in 7 of the 8 eggplant orientations (−0.04 to
+0.29). The gain is anticorrelated with nominal success (r = −0.44): of the 51 configurations where OpenVLA
fails outright at the nominal limit, 13 are rescued. The parameter repairs failures rather than padding
successes. The same decomposition for octo-small is flat and directionless — 15 improve, 15 degrade, 2 of 8
orientations positive — which is what a policy that never saturates the limit should look like.
(`scripts/analyze_torque_mechanism.py`.)

**It is task-dependent in the direction the mechanism predicts.** On the spoon task (24-configuration
complete census) the same parameter barely moves Δ at all — −0.01 to −0.07 across the four cross-family
pairs, against −0.14 on eggplant — and changes no verdict. Eggplant is where contact torque saturates for a
large-displacement policy; spoon is not. A calibration-invisible parameter is therefore not uniformly
dangerous: its decision-relevance is a property of the task-policy pair, which is precisely why it cannot be
argued away a priori and has to be enumerated.

### 6.5 Sign reversals do exist between conditions — just not enough to flip a ranking

One pair does reverse sign across the compatible set: `octo-base vs octo-base@hist1` has Δ = −0.021 under
density ×0.5 against positive values under the other five conditions. The reversal is well inside the
interval, so it does not license the claim "the ranking flips"; it does mean this pair's abstention is a
fact about the parameters, not about our budget, and no amount of extra evaluation will remove it. The
distinction matters: as evaluation half-width \(h \to 0\) the union bound converges to
\([\min_c \Delta_c, \max_c \Delta_c]\), which does **not** shrink with budget. An abstention that survives
\(h \to 0\) is a parameter fact; one that dissolves was a power artefact. Section 6.6 separates the two
empirically.

### 6.6 Budget cannot explain the disagreement `[T2-A]`

To show the disagreements are not our own low power, we take the eggplant census from 3 to 5 seed sets.
On that census a pair's half-width at S = 3 is 0.075–0.088 (Table 1); since it falls as
\(1/\sqrt{S}\), S = 5 brings it to 0.058–0.068, while the parameter-induced shift of 0.141 stays
where it is by construction. `[T2-A: report which of the three disagreements survive; the `octo-base@hist1`
vs OpenVLA cell, whose lower bound is currently −0.000, is the one that could go either way. If it becomes
decidable, we withdraw it from the count and report two.]`

The general statement the experiment supports is a comparison of two quantities: a ranking can be declared
when \(|\hat\Delta|\) exceeds the parameter-induced shift \(\delta\) **plus** the evaluation half-width
\(h\). Enumerating the configuration grid drives the sampling part of \(h\) to zero, and more seeds shrink
the rest; \(\delta \approx 0.141\) does not move. At the budget the published protocol uses — 24 configurations, three seeds — a pair's half-width
is 0.05–0.13 (§8.3), i.e. at or above \(\delta\), so there the two error sources are not even
separable. Our census at S = 5 pushes \(h\) below \(\delta\), and only then does the comparison
become meaningful at all. **Parameter ambiguity, not evaluation noise, is the binding error source**, and it is the one
that more evaluation cannot reduce.
