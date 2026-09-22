# Draft: Section 8 — Reproducing the Published Protocol (2026-09-20)

> **RENUMBERED TO §6 (2026-09-21).** Under the Option-A spine (`docs/paper_spine_2026-09-21.md`) this is a
> headline contribution (C4) and moves ahead of the machinery: a reader should meet "the published budget
> resolves 1 of 4 rankings" before being asked to care about compatible sets. The prose below stands as
> written; only the section numbers change (§8.1→§6.1, §8.2→§6.2, §8.3→§6.3, §8.4→§6.4), and internal
> cross-references to "§6" in this file now mean **§7**
> (`docs/paper_draft_s7_nonidentifiability.md`). The verdict-ladder section that used to be §7 is now §8
> (`docs/paper_draft_s8_ladder.md`) — note the filename collision and rename both files at manuscript
> assembly time.

Status: evidence settled (`results/controller_sweep_ms2_official/FINDING_official_protocol.md`, collected
2026-09-20 12:48–13:51). Written in English for direct transfer to the manuscript; internal notes are in
blockquotes and are not part of the manuscript text.

---

## 8 Reproducing the Published Protocol

Everything so far was measured on our own pipeline. Two questions follow. Does that pipeline reproduce the
numbers the benchmark publishes — and, if it does, what does the *published* evaluation budget itself resolve?

### 8.1 The protocol, followed exactly

The reference implementation's `scripts/octo_bridge.sh` evaluates each Bridge task with
`--obj-episode-range 0 24` and `init_rng ∈ {0, 2, 4}`: a complete enumeration of the task's 24 initial
configurations, repeated under three fixed policy seeds, for the 72 episodes that form the denominator of the
published rates. Within one sweep the seed is held fixed — `OctoInference` draws the same `PRNGKey(init_rng)`
at every reset — so the three sweeps are three draws of policy noise over one fixed configuration set, not 72
independent samples.

We reproduced this on the original SIMPLER stack (ManiSkill2\_real2sim + SAPIEN 2.2.2), running headless in
WSL through the Vulkan compatibility layer of Appendix B, with the policies served by our own HTTP inference
server rather than in-process. Published values are read from the pinned `simpler_env/utils/metrics.py`.

> Internal: `controller_sweep_ms2.py --policy-seed-fixed` was added for exactly this; without it our sweeps
> advance the seed per episode, which is the ManiSkill3 port's convention and a different estimand (§5.2).

### 8.2 The reproduction agrees

**Table 4.** Our 72-episode reproduction against the published values.

| Task | Policy | seed 0 | seed 2 | seed 4 | pooled (n/72) | published | difference |
|---|---|---:|---:|---:|---:|---:|---:|
| eggplant in basket | octo-small | 0.583 | 0.458 | 0.625 | 0.556 | 0.569 | −0.013 |
| eggplant in basket | octo-base | 0.375 | 0.458 | 0.583 | 0.472 | 0.431 | +0.041 |
| spoon on towel | octo-small | 0.375 | 0.333 | 0.583 | 0.431 | 0.472 | −0.041 |
| spoon on towel | octo-base | 0.042 | 0.083 | 0.125 | 0.083 | 0.125 | −0.042 |
| carrot on plate | octo-small | 0.042 | 0.042 | 0.125 | 0.069 | 0.097 | −0.028 |
| carrot on plate | octo-base | 0.125 | 0.125 | 0.125 | 0.125 | 0.083 | +0.042 |
| stack cube | octo-small | 0.083 | 0.042 | 0.000 | 0.042 | 0.042 | −0.000 |
| stack cube | octo-base | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | +0.000 |

Across the eight cells the mean signed difference is −0.005, the mean absolute difference 0.026, and the
largest 0.042. For comparison, the policy-seed noise we measure on the 64-configuration eggplant census is
±0.108 at half-width for a single seed set and ±0.062 for three (§5.4). Every discrepancy is well inside that
band. A different operating system, a software-rendered rasteriser, a different Vulkan path and an
out-of-process policy server move the published numbers by less than one seed's worth of noise, which is the
external-validity check the rest of the paper rests on.

### 8.3 What the published budget resolves

The same table answers a second question, and the answer is less comfortable. The three fixed seeds disagree
with each other by considerably more than we differ from the published value: the across-seed range of a cell
averages 0.109 and reaches 0.250 (spoon, octo-small: 0.333 to 0.583). Applying the census estimator of §5.3 —
the configuration set is fully enumerated, so only policy noise remains — to the octo-small vs octo-base
comparison the published protocol is built to support:

**Table 5.** What the published 72-episode budget resolves. Census interval: policy noise only, S = 3 seeds
over a complete 24-configuration enumeration. Naive interval: the binomial-over-72 a reader of the published
table would compute.

| Task | our Δ | census 95% | naive binomial 95% | verdict at this budget | published Δ |
|---|---:|---|---|---|---:|
| eggplant | +0.083 | [−0.047, +0.214] | [−0.079, +0.246] | abstain | +0.138 |
| spoon | +0.347 | [+0.235, +0.459] | [+0.216, +0.478] | octo-small > octo-base | +0.347 |
| carrot | −0.056 | [−0.137, +0.026] | [−0.152, +0.041] | abstain | **+0.014** |
| stack | +0.042 | [−0.005, +0.089] | [−0.004, +0.088] | abstain | +0.042 |

Three observations.

**(i) One of four orderings is resolvable.** Only the spoon comparison excludes zero. On the other three
tasks the published protocol reports a rate difference its own budget cannot distinguish from noise. This is
not a criticism of the reference implementation — the published tables report rates, not rankings — but
readers do compare those rates across policies, and on three of four tasks that comparison is unsupported.

**(ii) One ordering reverses.** On carrot the published values place octo-small above octo-base (+0.014);
our faithful reproduction places octo-base above octo-small (−0.056). Both magnitudes are far inside the
seed noise, and the published value lies comfortably within our interval, so this is not a contradiction —
it is the same non-resolvable comparison resolved differently by chance in two runs of the identical
protocol. It is, however, a concrete instance of the failure mode this paper is about: a ranking read off a
benchmark table that a re-run of the same benchmark does not reproduce.

**(iii) Removing configuration sampling error is not enough.** The census interval is tighter than the naive
binomial one, but only slightly, and it changes no verdict. With three seeds per configuration the
per-configuration policy variance dominates, so enumerating the configuration grid — which sets the sampling
error to exactly zero — buys much less than practitioners expect. Budget is spent better on seeds than on
episodes; §5.5 quantifies that trade.

### 8.4 What this section licenses

The published numbers carry an unreported uncertainty of roughly ±0.06 at three seeds, of the same order as
the parameter-induced shift of 0.14–0.23 that §6 attributes to a calibration-invisible torque limit. That
these two are comparable is the paper's central quantitative claim, and §8.2 establishes that we can say it
about the benchmark as published, not merely about our port of it.

> Internal: when contacting the SIMPLER authors, lead with §8.2 (their pipeline reproduces to 0.026) and
> frame §8.3 as a budget property of any 72-episode protocol, not an error on their part. The carrot
> reversal in particular should be presented as evidence for the uncertainty claim, not as a defect report.
