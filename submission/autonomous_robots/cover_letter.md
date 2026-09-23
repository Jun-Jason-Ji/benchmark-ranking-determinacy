# Cover letter — Autonomous Robots

> Fill in the date, and the Editor-in-Chief's name if you want to address them directly (I have not
> filled that in because I did not verify who currently holds the post — "Dear Editor-in-Chief" is
> safe and standard). Then export to PDF. Author details are already in, taken from the block
> supplied on 2026-09-21. A longer version, with the full reproduction detail and the qualifications
> spelled out, is kept as `cover_letter_long.md` in case a revision round calls for it.

---

Dear Editor-in-Chief,

We submit for consideration in *Autonomous Robots* our manuscript **"What Determines a Simulation
Benchmark Ranking? Structural Blindness, Finite Configuration Grids, and Evaluation Budget in
Simulation-Based Policy Comparison."**

Simulation suites that mirror real evaluation scenes are now routinely used to rank robot foundation
policies, and their published tables are read as rankings. The usual question asked of such a suite
is how well it correlates with reality. We ask the question that comes first, and that can be
answered without a robot: **given the demonstrations a simulator was calibrated on, the
configurations it enumerates and the episodes it runs, which ranking claims does that evidence
determine?** We begin from a faithful reproduction rather than a critique — following the reference
protocol down to the pseudo-random-number lifecycle its inference wrapper implies, on a different
operating system with a software rasteriser, we reproduce the published rates to a mean absolute
difference of 0.038 across eight cells.

Three findings follow. **Demonstration-replay calibration is structurally blind in identifiable
directions:** free-space teleoperated demonstrations cannot see a common rescaling of the joint PD
gains, nor a torque limit that never activates. A sixteenfold gain rescaling moves the replay
objective by at most 3.1×10⁻⁶ of its own composite units, against 1.36×10⁻³ between two independent
implementations of the same dynamics. These follow from the protocol's excitation range, so better
fitting does not remove them. **The benchmark's initial states are a finite, enumerable population:**
the episode index fixes the configuration modulo 24 to 300, episodes past that count are exact
repeats, and two widely used ports enumerate *different* grids. **Ranking claims turn on choices the
evidence does not settle:** the reference protocol's 72-episode budget resolves one or two of its
four orderings depending on the variance model, and re-applying the calibration protocol to 98
demonstrations from the same public dataset disfavours the shipped controller setting on both
stacks — where a complete census moves the verdict from abstention to a declaration, on a change in
the policy difference that is not itself resolved.

We are careful about how far that last finding reads. Our demonstrations come from the same public
BridgeData V2 release the reference calibration draws on, verified to the byte, but we did not
establish that they are the same trajectories the reference parameters were fitted on. **This is a
re-calibration audit on same-source demonstrations, not a demonstration that the original fit
contradicted itself** (§4.3). The actionable consequence needs only the weaker claim: no suite we
know of reports its operating point together with how that point stands against its own calibration
objective, so a reader cannot tell whether a published verdict is the verdict at the setting the
calibration evidence prefers. That costs nothing to fix and we recommend it.

The manuscript reports where our own proposed remedy stops. A set-valued verdict over the
calibration-invisible directions changes 1 of 17 pairwise verdicts at five seed sets over a complete
census. The strong form of our claim — that a calibration-invisible parameter reverses a
sign-determined ranking — is **false in our data**, and on a selected pair whose published real and
simulated means point opposite ways the criterion declares the ordering those means reverse. Four
conclusions of our own are retracted, each after we ran the experiment designed to test it.

**On scope.** We ran no robot; where real-robot ground truth is needed we use the rates published
alongside the benchmark, which are the values the suite is itself validated against. Section 9
specifies the validating experiment rather than noting that hardware was unavailable: the two
checkpoints, the deployment conditions that must be matched, the analysis rule and operating point
frozen in advance, and a trial count sized by power rather than by interval width. We understand the
journal prefers manuscripts carrying real-robot performance data while accepting simulation-only work
whose path to the real world is set out adequately, and we have tried to meet that standard
explicitly. Every table and figure regenerates from the released episode records by released scripts,
archived with a DOI.

The work is original, is not under consideration elsewhere, and all authors approve the submission.
We have no competing interests and received no funding. A large language model assisted with writing
and with the analysis scripts, as declared in the manuscript; the study design, the experiments and
the interpretation are ours.

Thank you for considering the manuscript.

Sincerely,

Jun Ji, Bowen Tan, Yi Li, Xiaolei Zhang, Shengjie Guo, and Yi Sui (corresponding author)
College of Computer Science and Technology, Qingdao University · suiyi@qdu.edu.cn
