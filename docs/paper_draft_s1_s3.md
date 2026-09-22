# Draft: Sections 1–3 (2026-09-21)

Spine: `docs/paper_spine_2026-09-21.md`. Numbering follows the reframe there — the reproduction section is
§6 (prose in `paper_draft_s8.md`), decision-relevant non-identifiability is §7 (rewrite in
`paper_draft_s7_nonidentifiability.md`), the verdict ladder is §8.

Written in English for direct transfer to the manuscript; internal notes are in blockquotes.

---

## 1 Introduction

A simulator that has been calibrated against real demonstrations is increasingly treated as evidence about
which robot policy is better. Simulation suites that mirror real evaluation scenes are used to compare
foundation policies at a scale no physical laboratory can match, and their published tables are read as
rankings: this policy beats that one on this task. The appeal is obvious. A physical evaluation of a single
policy on a single task costs hours of robot time and is difficult to reproduce; a simulated one costs
minutes and is, in principle, exactly repeatable.

The standard question asked of such a suite is how well it correlates with reality, and it is usually
answered with a correlation coefficient or a rank agreement over a handful of policies. This paper asks a
question that comes before that one, and that can be answered without a robot:

> **Given the evidence actually used to build and run a simulation benchmark — the demonstrations it was
> calibrated on, the configurations it enumerates, and the episodes it runs — which ranking claims does that
> evidence determine?**

The distinction matters because a correlation study treats the simulator's output as a measurement with some
error attached, whereas our question asks whether the output is a well-defined function of the inputs at all.
If two simulator configurations are equally consistent with every piece of calibration data and they disagree
about which policy wins, then no amount of correlation analysis repairs the ranking: the evidence simply does
not contain the answer. This is the distinction between *identifiability* and *statistical power*, and one of
our findings is that practitioners systematically conflate them — including, at two points in this project's
history, us.

We answer the question on a widely used sim-to-real evaluation suite for manipulation, across two embodiments
(a WidowX bridge setup and a Google-robot fractal setup), eight policy configurations across three model
families, and a complete enumeration of every task's configuration grid. Three findings, each independent of the others.

**The calibration protocol is structurally blind (§4).** The protocol identifies some dynamics parameters and
is *exactly* uninformative about others. Replaying 98 real demonstrations, we show analytically and then
empirically that a common scaling of the joint PD gains and the value of the torque limit leave the replay
trajectory unchanged — the first because the free-space response depends only on the ratio `d/k`, the second
because commanded torque never saturates along demonstrated velocities. The measured effect is 0.141 mm on
one simulator stack and 0.207 mm on a second, independent one for the gain scaling, and *bitwise zero* for
the torque limit. These are structural invariances of the protocol, not flat regions of a noisy objective, so
no improvement in fitting technique removes them.

**The benchmark is a finite configuration population, not a sample (§5).** The episode index determines the
initial state modulo the size of the task's configuration grid — 24 configurations for three bridge tasks, 64
for one port's eggplant task, 300 for the fractal coke-can task. Episodes beyond that count are exact
repeats, so the common practice of "running more episodes" stops buying information about configurations at a
threshold most users never learn. Two widely used ports of the same suite enumerate *different* grids, which
means a number computed on one is not comparable to a number computed on the other. Enumerating the grid
drives configuration sampling error to exactly zero, and what remains is instructive: policy-seed noise of
standard deviation 0.055, implementation-build drift of 0.078 — and, larger than either by a factor of five,
the suite's own silent averaging over four robot *texture* variants, across which one policy's success rate
ranges over 0.400. That last parameter changes the colour of the robot model, carries no physics whatsoever,
and is invisible to replay calibration for exactly that reason.

**The published protocol does not resolve the rankings it reports (§6).** We follow the reference protocol
exactly and reproduce the published success rates to a mean absolute difference of 0.026 across eight cells,
and on the second embodiment to +0.003 and −0.040 — so the pipeline is faithful, which is what licenses the
rest. At that same 72-episode budget, only one of the four policy orderings the protocol reports is
statistically resolvable, and on one task a faithful re-run of the identical protocol *reverses the published
sign*. Both values sit far inside the seed noise, so this is not a contradiction; it is the same
non-resolvable comparison resolved differently by chance twice, which is precisely the failure mode the paper
is about.

Having established that ranking claims are underdetermined from three independent directions, we ask what can
be done about it (§7, §8). The natural remedy is a set-valued verdict: declare an ordering only when it holds
for every simulator parameter the calibration data cannot exclude. We measure that criterion's reach, and we
report both halves of the answer. It is conservative as designed on synthetic ground truth where the point
criterion's error rate *rises* with episode count to 0.88, and it stabilises verdicts on real replicate data.
At the one- to three-seed budgets the literature actually uses, it disagrees with point calibration on 3 of 17
policy pairs — but when we spend more seeds, two of those three disagreements turn out to have been our own
insufficient power, leaving one. And on the single policy pair for which published real-robot results
contradict the simulator, the criterion over the dynamics compatible set *declares the ordering the real robot
reverses*. Its reach stops at the parameter family the calibration data can constrain, and the sim-to-real
gap on that pair lies outside it.

### 1.1 Contributions

1. **C1 (§4)** An exact structural non-identifiability in demonstration-replay calibration, established
   analytically and confirmed on two independent simulator stacks to sub-millimetre agreement.
2. **C2 (§5)** The identification of the benchmark as a finite configuration population, with the
   configuration count per task, the demonstration that two widely used ports evaluate different benchmarks,
   and the consequences for what "more episodes" can buy.
3. **C3 (§5)** An estimand taxonomy and an uncertainty budget in which the largest measured term is a visual
   variant the benchmark averages over without reporting it.
4. **C4 (§6)** A faithful reproduction of the published protocol which shows that its own budget resolves one
   of the four orderings it reports, and that one ordering reverses under re-run.
5. **C5 (§7)** A decision-relevant instance of non-identifiability — an exactly invisible torque limit that
   displaces a policy difference by 0.141 and moves verdicts from decidable to abstaining — stated, after our
   own larger-budget replication, as a property of the evaluation budget rather than of parameter sign.
6. **C6 (§8)** A verdict ladder with its coverage and power measured on synthetic ground truth and its
   stability measured on real replicates, together with the negative result that delimits it: on the one pair
   with contradicting real-robot ground truth, the criterion declares the wrong ordering.
7. **C7 (App. B–D)** Reproducibility assets, including the original reference stack running headless on a
   GPU-less host through a purpose-built Vulkan compatibility layer, the configuration-census protocol, and
   append-only provenance logs for every episode reported here.

### 1.2 What we withdraw

Three conclusions of our own are retracted in this paper, each after we ran the experiment designed to test
it:

1. **"Eggplant nominal: octo-small beats octo-base."** Declared from one seed set with a per-episode
   bootstrap, interval [+0.08, +0.32]. Three same-generation seed sets give +0.141, −0.031 and −0.047.
   Withdrawn (§5.4).
2. **"The torque effect replicates across two seed sets."** The episode index fully determines the
   configuration, and the policy in question decodes deterministically, so the two "seed sets" were repeat
   runs of identical rollouts. Withdrawn and replaced by a configuration-census protocol (§5.3).
3. **"Budget cannot explain the point-versus-set disagreements."** Taking the census from three to five seed
   sets resolved two of the three disagreements, and dissolved the one between-condition sign reversal we had
   claimed (density ×0.5: −0.021 at three seeds, +0.042 at five). Withdrawn; §7 states the weaker conclusion
   the data supports (§7.5).

Four further ranking-flip candidates seen at 24 and 48 episodes were withdrawn before being claimed, when
adding episodes removed them. We list all of this in the body rather than in a limitations section because a
reader's estimate of how much to trust our surviving claims should be calibrated by how the non-surviving
ones died.

> Internal: the count is three retractions — matching the project log — plus four withdrawn candidates that
> were never asserted. Do not renumber these without re-checking `FINDING_t2a_seeds.md` §4.

### 1.3 Scope

We make no claim about which policy is actually better on any real robot, and we ran no hardware ourselves.
Where real-robot ground truth is needed — in §8's delimiting experiment — we use the success rates published
alongside the benchmark for the same policies and task, which are the reference values the benchmark itself
is validated against. Two public evaluation services that would have provided independent hardware results
were unavailable during this work: one endpoint was offline throughout (documented with dates in App. D) and
the other's queue allocation could not be confirmed. Our claims are about what the simulated evidence
determines, which is a question about the benchmark rather than about the robot.

---

## 2 Related Work

**Simulation-based evaluation of manipulation policies.** Recent evaluation suites construct simulated scenes
that mirror real evaluation setups, calibrate the simulator against real demonstrations, and report success
rates intended to be comparable with real-robot numbers. Parallel efforts pursue automated real-robot
evaluation and distributed evaluation across laboratories. All of these are motivated by the cost and
irreproducibility of physical evaluation, and all are validated by some form of sim-to-real agreement: rank
correlation, mean absolute difference, or per-task scatter against real rates. Our work takes such a suite as
its object of study rather than as a tool, and asks not how closely it agrees with reality but which of its
own outputs are determined by its own inputs.

**Identifiability and system identification.** That not every parameter of a dynamical model can be recovered
from a given excitation is classical, and structural identifiability analysis is standard in system
identification. Robot calibration practice generally acknowledges it in the form of excitation design:
trajectories are chosen to make the parameters of interest observable. The gap we address is that
demonstration-replay calibration does not get to choose its excitation — the demonstrations are whatever
humans happened to teleoperate, they are free-space and slow, and the resulting blindness is inherited rather
than designed. We treat the blind directions not as a nuisance to be reduced but as a set to be propagated,
which connects to the next literature.

**Partial identification and set-valued inference.** When data do not pin down a parameter, one can report
the set of values consistent with the data and the corresponding set of implied conclusions, rather than a
point estimate and a confidence interval around it. This tradition is well developed in econometrics, and
model-confidence-set procedures provide the specific device we use: invert a test to obtain the collection of
models the data cannot distinguish, then require a conclusion to hold across that collection. Our
contribution is not methodological novelty here but instantiation and measurement — we construct the
compatible set for a real calibration protocol, propagate it to policy rankings, and quantify what the
resulting criterion does and does not buy, including a case where it fails.

**Reproducibility and statistical practice in learned-policy evaluation.** Sensitivity of reinforcement
learning results to random seeds, and the resulting unreliability of small-sample comparisons, is documented
and has produced concrete recommendations on reporting. Our §5 contributes two items that this literature
does not cover for simulated robot benchmarks: the initial-state grid is finite and enumerable, so the
configuration axis is a population rather than a sample and its sampling error can be driven to exactly zero;
and the *implementation build* — the port branch plus the inference stack version — behaves as an
unreported parameter of the same order as the ones being studied. The first changes which bootstrap is
correct; the second means that even a perfectly specified bootstrap understates the uncertainty of a number
copied from a published table.

> Internal: citations to be filled at submission. Keep this section free of specific numbers — reviewers read
> §2 for positioning, and every number here duplicates one in §4–§8.

---

## 3 Problem Setup

### 3.1 Notation

Let \(z\) denote the simulator's physical parameters (joint PD gains, torque limits, contact friction and
density), and let \(\pi\) denote the **implementation build**: the port branch, the renderer path and the
policy inference stack version. A task provides a finite set \(\mathcal{C}\) of initial configurations. A
policy \(i\) run from configuration \(c\) under parameters \(z\) and build \(\pi\) with internal random source
\(\sigma\) either succeeds or fails, written \(s_i(c, z, \sigma; \pi) \in \{0, 1\}\). The simulated difference
between two policies is

\[
\Delta^{sim}_{ij}(z; \pi) = \frac{1}{|\mathcal{C}|} \sum_{c \in \mathcal{C}}
\Big[ \mathbb{E}_\sigma\, s_i(c, z, \sigma; \pi) - \mathbb{E}_\sigma\, s_j(c, z, \sigma; \pi) \Big],
\]

and \(\Delta^{real}_{ij}\) denotes the corresponding real-robot difference. Three properties of this
definition carry the weight of §5 and are stated here because they are easy to overlook: the sum over
\(\mathcal{C}\) is over a **population**, not a sample; \(\sigma\) is degenerate for deterministically
decoding policies, so for those the benchmark value is measurable exactly; and \(\mathcal{C}\) itself depends
on \(\pi\), so two builds with different grids yield two different estimands that cannot be paired per
episode.

### 3.2 The compatible set

Calibration observes real demonstrations and scores a candidate \(z\) by a replay loss \(L(z)\). Rather than
reporting the minimiser \(\hat z\), we invert a one-sided test at level \(\alpha\): a parameter setting is
**compatible** if its per-demonstration error is not significantly worse than the best,

\[
C_\alpha = \Big\{ z : \text{the paired bootstrap } (1-\alpha) \text{ lower bound of }
\mathbb{E}\big[L(z) - L(\hat z)\big] \le 0 \Big\},
\]

so \(C_\alpha\) contains every parameter the calibration data cannot reject. Directions in which the loss is
*exactly* invariant (§4.2) belong to \(C_\alpha\) by construction and at every magnitude, which is a stronger
statement than "the data are consistent with a range of values": there is no range, the axis is unconstrained.
Parameters the replay cannot observe at all — contact friction and object density never appear in a free-space
trajectory — are likewise unconstrained, and we flag them separately because their compatibility is a
property of the protocol's coverage rather than of its precision.

### 3.3 The decision problem

Given \(C_\alpha\), an evaluation budget and a policy pair, we must either declare an ordering or abstain. Two
criteria are compared throughout:

* **point calibration**, standard practice: evaluate at \(\hat z\) alone and declare \(i \succ j\) when the
  interval for \(\hat\Delta_{ij}(\hat z)\) excludes zero;
* **the union bound**: declare only when every \(z \in C_\alpha\) agrees in sign, using the interval
  \(\big[\min_{z} \mathrm{lo}(z),\ \max_{z} \mathrm{hi}(z)\big]\).

A third rung, a Gaussian-process simultaneous band over the parameter axes, is introduced in §8 for the case
where the decisive parameter value may lie *between* the settings we sampled; the union bound's guarantee is
of sampling-extremum type and does not cover that case.

### 3.4 The error ledger

Writing \([L_{ij}, U_{ij}]\) for the union-bound interval, the claim "\(i\) is genuinely better in practice"
requires three events to hold simultaneously: that the true parameter lies in the compatible set,
\(E_\theta = \{z^* \in C_\alpha\}\) with \(P(E_\theta) \ge 1 - \alpha\); that the evaluation intervals cover
the simulated differences uniformly over the set, \(E_{MC}\) with \(P(E_{MC}) \ge 1 - \gamma\); and that the
sim-to-real bias is bounded, \(E_b = \{|\Delta^{real}_{ij} - \Delta^{sim}_{ij}(z^*)| \le b_{ij}\}\) with
\(P(E_b) \ge 1 - \beta\). On the intersection every real difference lies in \([L_{ij} - b_{ij},
U_{ij} + b_{ij}]\), and a union bound gives \(1 - \alpha - \beta - \gamma\) without requiring independence.

We are deliberate about which of these this paper establishes. \(E_{MC}\) is what §5–§7 measure, and
enumerating \(\mathcal{C}\) removes one of its two components exactly. \(E_\theta\) is what §4 characterises,
and its width dominates the ledger. \(E_b\) we do **not** establish: we have no per-pair sim-to-real bias
bound, and §8's delimiting experiment is best understood as evidence that on at least one pair \(b_{ij}\) is
large enough to swamp everything else — 0.21 in a quantity whose other terms are 0.04 to 0.15. A criterion
built on \(E_\theta\) and \(E_{MC}\) alone bounds the ambiguity it can represent, and that is the honest
description of what the ladder in §8 delivers.

> Internal: §3.4 is where a sharp reviewer will look for overreach, so it states the \(E_b\) gap before §8
> does. The formal ledger is `docs/theory_protocol.md §6`; the per-event caveats there (per-pair \(\beta\)
> cannot be written as a joint event; \(E_\theta\) presumes a \(z^*\) exists; GP posterior sd must not be
> dropped into \(\gamma\) unvalidated) should be reproduced in an appendix.
