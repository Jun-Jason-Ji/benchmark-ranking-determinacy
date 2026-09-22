# Draft: Section 7 — Decision-Relevant Non-Identifiability (2026-09-21)

**Replaces** `paper_draft_s6.md`, which carried the pre-T2-A numbers and is retained only for provenance.
Changes: §6.2's "3 of 17 disagree" becomes 1 of 17 and is restated as a budget claim; §6.5 (between-condition
sign reversal) is **deleted**, not weakened, because the effect it described does not exist at S = 5; §6.6's
conclusion is **inverted** — budget explained two of the three. The mechanism subsections (old §6.3, §6.4)
survive verbatim and appear here as §7.3 and §7.4.

Demoted from headline to worked example per `paper_spine_2026-09-21.md`: the paper's claim that ranking
evidence is underdetermined now rests on §4–§6, and this section's job is to show the mechanism concretely
on one parameter and to be honest about how much of it survived a larger budget.

All numbers are census-scope: the configuration grid is fully enumerated, so configuration sampling error is
zero and the intervals carry policy noise only (§5.3). Sources: `results/CORE_TABLE.md`,
`results/controller_sweep_gpu_rep3/{analysis_benchmark_value_union.md,FINDING_t2a_seeds.md}`,
`results/controller_sweep_gpu_rep3/FINDING_estimand_matters.md`.

Written in English for direct transfer to the manuscript; internal notes are in blockquotes.

---

## 7 Decision-Relevant Non-Identifiability

Sections 4 and 5 showed that the calibration protocol cannot see certain parameter directions and that the
benchmark's own budget leaves its rankings unresolved. Neither observation is interesting on its own: an
unidentifiable parameter matters only if moving it inside the compatible set changes an answer someone acts
on. This section establishes that it can, measures how large the effect is, and reports how much of it
survives when the evaluation budget is increased — which is less than we first claimed.

### 7.1 The claim, stated so it can fail

Fix a task, a policy pair \((i, j)\) and the compatible set \(C_\alpha\) of §3.2. Point calibration declares
\(i \succ j\) when the interval for \(\hat\Delta_{ij}(\hat z)\) excludes zero; the union bound declares only
when every \(z \in C_\alpha\) agrees in sign. The claim under test is that these two criteria disagree —
that point calibration declares orderings the calibration data cannot support.

Two forms are worth separating.

* The **strong form**: some \(z \in C_\alpha\) reverses a ranking's sign, so that the simulator's answer to
  "which policy is better" depends on a parameter the calibration data is silent about. **We report this as
  false.** Across every pair, task and condition we measured, no calibration-invisible parameter reverses a
  sign-determined ranking. We also once believed we had found a weaker version of it — a between-condition
  sign change on one pair — and withdrew that too; see §7.5.
* The **weak form**: the parameter moves \(\Delta\) far enough to cross the decision boundary, turning a
  declared ordering into an abstention. **This holds, and it is budget-dependent** — which is the finding
  that replaced our original, stronger claim.

> Internal: stating the strong form and reporting it false is deliberate — it is the honest form of the
> contribution and pre-empts the obvious reviewer question ("did you look for sign flips?"). §8 shows the
> ladder would catch a flip if one existed.

### 7.2 The core table, and what a larger budget did to it

**Table 6** reports both verdicts for every policy pair on every task, with the provenance each number needs:
configurations covered, independent runs per policy, and the variance model. Of 17 rows, **one** disagrees:

| pair (eggplant, 64-configuration census, S = 5) | point Δ | point verdict | union interval | union verdict |
|---|---:|---|---|---|
| octo-base vs octo-base@hist1 | +0.069 [+0.00, +0.13] | octo-base ≻ | [−0.06, +0.12] | abstain |

At three seed sets, three rows disagreed. The two that no longer do were resolved by spending seeds, not by
any change of method:

| pair | union interval at S = 3 | at S = 5 | outcome |
|---|---|---|---|
| octo-small vs octo-base@hist1 | [−0.03, +0.28] abstain | [+0.01, +0.24] declare | withdrawn — our power |
| octo-base@hist1 vs OpenVLA | [−0.00, +0.42] abstain | [+0.02, +0.43] declare | withdrawn — our power |
| octo-base vs octo-base@hist1 | [−0.10, +0.17] abstain | [−0.06, +0.12] abstain | survives |

The decisive cell is `octo-base@hist1` vs OpenVLA under torque ×0.5, where Δ = +0.068 with interval
[−0.000, +0.135] at S = 3 and +0.073 with [+0.017, +0.128] at S = 5. A lower bound sitting exactly on zero
became a lower bound above it, and the disagreement evaporated. We had pre-committed to this test and to
withdrawing the row if it went this way (the S = 3 draft of this section said so in as many words), which is
why the surviving count is one rather than three.

The honest general statement is therefore **about the evaluation budget**:

> At the budgets the literature actually uses — a single seed, or the reference protocol's three — point
> calibration declares orderings the union bound does not support, on 3 of 17 policy pairs. At five seed sets
> over a complete configuration census, one remains. The criterion's value is concentrated in the budget
> regime practitioners are actually in.

This is weaker than the claim we set out to make, and it remains useful: we are aware of no published
evaluation that runs five seed sets over a full configuration census, and the reference protocol itself uses
three. The surviving pair is also instructive about *why* it survives. It is not that its \(\Delta\) changes
sign across conditions — §7.5 — but that its nominal interval is barely decidable (lower bound +0.004) while
the union bound takes the minimum lower bound over conditions, which friction ×0.4 supplies at −0.063. It is
a margin-and-width phenomenon, not a parameter-sign phenomenon, and it should be described as such.

### 7.3 The mechanism: one parameter, measured on a complete census

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
policy (OpenVLA) moving, not four independent effects.

> Internal: an earlier version of this analysis, on 48 of the 64 configurations, put the shift at 0.23–0.25
> and had two pairs crossing. The partial census overstated the effect. Every effect size in this paper is
> census-scope for this reason, and the correction is recorded in `FINDING_estimand_matters.md` §5 rather
> than silently applied. The table above is the S = 3 measurement; at S = 5 the last row's torque interval
> becomes [+0.017, +0.128] (§7.2) and no row crosses. Keep both, and say which is which.

### 7.4 Why it is not an artefact

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

### 7.5 A withdrawn claim: there is no between-condition sign reversal

An earlier version of this section reported that one pair, `octo-base` vs `octo-base@hist1`, reversed sign
across the compatible set — Δ = −0.021 under density ×0.5 against positive values under the other five
conditions — and argued from it that this pair's abstention was a fact about the parameters rather than about
our budget, and so could never be removed by more evaluation. **We withdraw that.** At five seed sets the
same cell reads +0.042 [−0.022, +0.106], and all six conditions have point estimates at or above −0.000:

| condition | Δ at S = 5 | 95% |
|---|---:|---|
| nominal | +0.069 | [+0.004, +0.133] |
| force ×0.5 | +0.050 | [−0.016, +0.116] |
| iso ×0.25 | +0.030 | [−0.033, +0.092] |
| iso ×4.0 | +0.006 | [−0.059, +0.072] |
| friction ×0.4 | −0.000 | [−0.063, +0.063] |
| density ×0.5 | +0.042 | [−0.022, +0.106] |

The distinction the withdrawn claim was reaching for is nevertheless real and worth keeping, because §8 needs
it. As the evaluation half-width \(h \to 0\) the union bound converges to
\(\big[\min_c \Delta_c, \max_c \Delta_c\big]\), which does **not** shrink with budget. An abstention that
survives \(h \to 0\) is a parameter fact; one that dissolves as \(h\) falls was a power artefact. Our own
three-to-five-seed experiment is the clean demonstration of the second case — and §8.4 uses the same test to
show that an abstention we might have been tempted to claim as a success of the criterion is also of the
second kind.

### 7.6 What determines whether a ranking can be declared

The general statement the evidence supports is a comparison of two quantities. A ranking can be declared when
\(|\hat\Delta|\) exceeds the parameter-induced shift \(\delta\) **plus** the evaluation half-width \(h\).
Enumerating the configuration grid drives the sampling part of \(h\) to zero; more seeds shrink the rest,
as \(1/\sqrt{S}\) — from 0.075–0.088 at three seed sets to 0.058–0.068 at five. The parameter-induced shift
\(\delta \approx 0.141\) does not move, by construction.

The two regimes this produces are the practical content of the section. At the budget the reference protocol
uses — 24 configurations, three seeds — a pair's half-width is 0.05–0.13 (§6.3), which is at or above
\(\delta\); there the two error sources are not even separable, and a practitioner cannot tell an
identifiability problem from a power problem. Our census at S = 5 pushes \(h\) below \(\delta\), and only
then does the comparison become meaningful. The recommendation follows directly: report the estimand and the
budget, and spend budget on seeds before episodes (§5.5), because only then does the residual ambiguity that
*cannot* be bought down become visible.

> Internal: this replaces old §6.6, whose headline was "budget cannot explain the disagreement". It can, and
> did, for two of three. What survives is the \(\delta\)-versus-\(h\) framing, which is the part of that
> section that was never budget-dependent.
