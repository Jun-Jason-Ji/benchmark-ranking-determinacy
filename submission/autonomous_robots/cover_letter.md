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

**We begin from a faithful reproduction rather than a critique.** Following the reference protocol
exactly, on a different operating system with a software rasteriser and an out-of-process inference
server, we reproduce the published success rates to a mean absolute difference of 0.026 across eight
cells, and on a second embodiment to +0.003 and −0.040. The pipeline agrees with the benchmark as
published. That agreement is what licenses everything else, and we would ask that it be read as the
starting point of the paper.

From there, three independent findings:

1. The calibration protocol is *exactly* uninformative about two parameter directions. A common
   scaling of the joint PD gains and the value of the torque limit leave the replay trajectory
   unchanged — by 0.141 mm and 0.207 mm on two independent simulator stacks for the first, and
   bitwise zero for the second. These are structural invariances of the protocol, not flat regions
   of a noisy objective, so better fitting does not remove them.

2. The benchmark's initial states are a finite population, not a sample. The episode index fixes the
   initial state modulo 24 to 300 configurations, so episodes beyond that count are exact repeats;
   two widely used ports of the same suite enumerate *different* grids and therefore do not evaluate
   the same benchmark. Enumerating the grid drives configuration sampling error to exactly zero, and
   the largest remaining term in the uncertainty budget turns out to be the suite's own unreported
   averaging over four robot *texture* variants, across which one policy's success rate ranges over
   0.400 — a parameter that carries no physics at all.

3. At the reference protocol's own 72-episode budget, only one of the four policy orderings it
   reports is statistically resolvable, and on one task a faithful re-run of the identical protocol
   reverses the published sign. Both values sit far inside the seed noise, so this is not a
   contradiction; it is the same non-resolvable comparison resolved differently by chance twice.

We then measure what a set-valued verdict over the calibration-compatible parameters buys — and we
report where it fails. On the one policy pair in this benchmark whose published real-robot results
contradict the simulator, the criterion declares the ordering the real robot reverses. We state that
in the abstract and in Section 1 rather than burying it, because it delimits our own proposed remedy:
a compatible-set criterion bounds the ambiguity it can represent, and on that pair the ambiguity that
matters is five times larger and points the other way.

**On the absence of our own hardware.** We ran no robot. Where real-robot ground truth is required,
we use the success rates published alongside the benchmark for the same policies and task — the
reference values the benchmark is itself validated against. We would argue this is the right
instrument for the question rather than a substitute for the right one: the claim under test is about
what the *simulated* evidence determines, and the comparison that tests it is against the benchmark's
own published real rates. We did attempt to obtain independent hardware results through two public
evaluation services; one endpoint was offline throughout this work and the other's queue allocation
could not be confirmed. Both attempts are documented with dates in the appendix, and a hardware
replication of the pair in Section 8.4 is named as the single most valuable follow-up.

**On negative results.** The manuscript retracts three conclusions of our own, each after we ran the
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
