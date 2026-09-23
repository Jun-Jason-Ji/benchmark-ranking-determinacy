# Cover letter — Autonomous Robots

> Fill in the date, and the Editor-in-Chief's name if you want to address them directly (I have not
> filled that in because I did not verify who currently holds the post — "Dear Editor-in-Chief" is
> safe and standard). Then export to PDF. Author details are already in, taken from the block
> supplied on 2026-09-21.

---

Dear Editor-in-Chief,

We submit for consideration in *Autonomous Robots* our manuscript **"What Determines a Simulation
Benchmark Ranking? Structural Blindness, Finite Configuration Grids, and Evaluation Budget in
Simulation-Based Policy Comparison."**

Simulation suites that mirror real evaluation scenes are now routinely used to rank robot foundation
policies, and their published tables are read as rankings. The usual question asked of such a suite
is how well it correlates with reality. This manuscript asks a question that comes first, and that
can be answered without a robot: given the demonstrations a simulator was calibrated on, the
configurations it enumerates and the episodes it runs, which ranking claims does that evidence
actually determine?

**We begin from a faithful reproduction rather than a critique.** Following the reference protocol —
including the pseudo-random-number lifecycle its inference wrapper implies — on a different operating
system with a software rasteriser and an out-of-process inference server, we reproduce the published
success rates to a mean absolute difference of 0.038 across eight cells, and on a second embodiment
to +0.003 and −0.040. The differences are one-signed: six of the eight fall below the published
value, two match it, mean −0.038. We deliberately do not turn that into a platform constant — the
eight cells share tasks, policies and seeds, so they are not eight independent replications — and we
do not claim it is negligible relative to the paper's effects, since 0.038 is about a third of the
0.121 torque shift and the largest single cell (0.111) is close to it. What the check licenses is
narrower: every effect we report is a difference between two policies measured in the same
configuration on one pipeline, and we compare our absolute rates against published absolute rates
only in that section. We would ask that the reproduction be read as the starting point of the paper.

From there, three independent findings:

1. The calibration protocol is uninformative about two parameter directions, for structural reasons
   rather than as a fitting tolerance. Grouping the 50-point replay grid by gain ratio and execution
   delay, a common rescaling of the joint PD gains moves the calibration loss by at most 3.1e−6 over
   the sixteenfold range our sweeps use, and halving the torque limit leaves the replayed trajectory
   *bitwise* unchanged on 97 of 98 demonstrations, on two independent stacks. The scale to judge
   those against is the 1.36e−3 by which the two stacks disagree at *identical* nominal parameters —
   all in the composite units of the replay objective, which adds metres to radians and is not a
   length —
   so the parameter effects are two to five orders of magnitude below the protocol's own resolution
   floor. These are properties of the protocol's excitation range, not flat regions of a noisy
   objective, so better fitting does not remove them.

   The same computation produced a result we did not expect and report prominently: the replay loss
   is minimised not at the simulator's shipped controller setting but at ratio 0.25 with one step of
   delay, on both stacks independently, and the shipped setting is rejected against that minimiser.
   Every published rate is computed at the shipped setting, and so was every measurement in our
   paper until this revision: Section 7.7 now re-runs the complete eggplant census at the preferred
   setting as well, so the operating point is measured rather than assumed. We restructured
   Section 4 around this and separated the compatible set from the calibration-invisible fibre
   through the benchmark's operating point.

   We then measured the consequence rather than leaving it as a caveat. Re-running the complete
   64-configuration census at the calibration-preferred setting — same configurations, same policy
   seeds episode for episode — moves the policy difference by only 0.031, and that is enough to
   carry the *point-calibration* verdict from abstention to a declaration (Section 7.7). The
   set-valued verdict abstains at both operating points, which is the contrast we draw: the
   operating point is not pinned down by the calibration evidence, at the budgets in use it decides
   the point answer, and the criterion we propose is the one that does not move. We think this is
   the paper's sharpest single result, and it also delimits our own proposed remedy: a criterion
   defined over the calibration-*invisible* directions cannot see a disagreement that lies in the
   directions the calibration *identifies*.

2. The benchmark's initial states are a finite population, not a sample. The episode index fixes the
   initial state modulo 24 to 300 configurations, so episodes beyond that count are exact repeats;
   two widely used ports of the same suite enumerate *different* grids and therefore do not evaluate
   the same benchmark. Enumerating the grid drives configuration sampling error to exactly zero, and
   among the terms that remain is the suite's documented averaging over four robot *texture*
   variants — a parameter that carries no physics at all, across which one policy's success rate
   ranges over 0.400. Our contribution there is not that the step is hidden but what it implies for
   the estimand: the published quantity is a mean over a four-point *variant* population, not the
   rate at any one variant, so a single-variant reproduction measures a different thing and differs
   by up to 0.227. Both are rates; what differs is what they are rates over.

3. At the reference protocol's own 72-episode budget, one of the four policy orderings it reports is
   statistically resolvable under the variance model its own randomisation implies, and two under a
   coarser model; we report both rather than pick one. On carrot the published difference is +0.014
   and ours is +0.028 with an interval of [−0.039, +0.094] — a number whose sign its own budget does
   not determine. We reproduce the protocol down to the pseudo-random-number lifecycle its wrapper
   implies (seeded once per run, one stream advancing across episodes, rather than re-seeded each
   episode), and Section 6 reports what that choice changes: it halves the across-run spread of a
   cell's rate, moves the mean difference from the published rates from −0.005 to −0.038, and it is
   the reason we withdraw a sign reversal we had previously claimed.

We then measure what a set-valued verdict over the calibration-invisible conditions buys — and we
report where it fails. On a selected policy pair — one of five in the published tables whose
simulated and real means point opposite ways — the criterion declares the ordering those published
means reverse. We state that in the abstract and in Section 1 rather than burying it, because it
delimits our own proposed remedy. Two honest qualifications travel with it: the published real rates
carry no intervals, so we claim only that the declaration has no real-robot warranty, not that it is
demonstrably wrong; and the pair was chosen with the audit in hand, so it is a case study rather
than a held-out test. Concretely, abstention would have required the bound to lose 0.070 on its
lower end; the dynamics conditions we ran span 0.044, while the gap between the simulated and the
published real margin is 0.214 and points the other way.

**On statistical scope.** We want to be direct about one limit, because a reader could otherwise
mistake the paper for offering a guarantee. The compatible-set construction selects its reference
from the same demonstrations it then tests against, which is a post-selection problem: under a null
of equally good candidates at our grid size and demonstration count, the procedure retains a true
best candidate about 53% of the time rather than 95%. We therefore make **no coverage claim** for
it, describe it as an empirical compatibility rule, and report a split-sample variant that does
carry an approximate level. The paper's substantive conclusion — that the benchmark's shipped
controller setting is excluded by its own replay objective — holds under that valid variant on both
simulator stacks and across five random splits, which is why we keep it.

**On the absence of our own hardware.** We ran no robot. Where real-robot ground truth is required,
we use the success rates published alongside the benchmark for the same policies and task — the
reference values the benchmark is itself validated against. We would argue this is the right
instrument for the question rather than a substitute for the right one: the claim under test is about
what the *simulated* evidence determines, and the comparison that tests it is against the benchmark's
own published real rates. We did attempt to obtain independent hardware results through two public
evaluation services; one endpoint was offline throughout this work and the other's queue allocation
could not be confirmed. Both attempts are documented with dates in the appendix, and a hardware
replication of the pair in Section 8.4 is named as the single most valuable follow-up.

**On negative results.** The manuscript retracts four conclusions of our own, each after we ran the
experiment designed to test it, and reports the strong form of its central claim as false. We list
these in Section 1.2 rather than in the limitations, on the view that a reader's confidence in the
surviving claims should be calibrated by how the others died. We hope this is read as the paper's
method rather than as a weakness in it.

All episode-level records, the evaluation harness, the configuration-census utilities and the
analysis scripts that generate every table and figure are released openly. The manuscript is original,
is not under consideration elsewhere, and has not been published previously. No large language model
is listed as an author.

We would be glad to suggest reviewers if that is useful to you.

Thank you for your consideration.

Yours sincerely,

Yi Sui, on behalf of all authors
College of Computer Science and Technology, Qingdao University, Qingdao 266071, China
suiyi@qdu.edu.cn

Co-authors: Jun Ji, Yi Li, Xiaolei Zhang (Qingdao University); Bowen Tan (The Hong Kong University
of Science and Technology); Shengjie Guo (Inner Mongolia Agricultural University).
