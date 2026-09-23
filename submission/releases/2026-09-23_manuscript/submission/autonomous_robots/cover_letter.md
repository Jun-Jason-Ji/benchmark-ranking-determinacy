# Cover letter — Autonomous Robots

Dear Editor-in-Chief,

We submit for consideration in *Autonomous Robots* our manuscript **“What Determines a Simulation Benchmark Ranking? Structural Blindness, Finite Configuration Grids, and Evaluation Budget in Simulation-Based Policy Comparison.”**

Simulation evaluations increasingly guide the selection of robot foundation policies for physical deployment. A ranking can therefore affect which policy a laboratory spends its robot time testing. We investigate when a benchmark's calibration data, configuration coverage and evaluation budget support such a comparison. Our audit of SIMPLER spans two embodiments and two simulator stacks, beginning with a reproduction of eight published rates at a mean absolute difference of 0.038. It establishes three empirical contributions.

**First, calibration sensitivity and policy-comparison sensitivity can diverge.** Free-space demonstration replay is weakly informative about common controller-gain rescaling and an inactive torque limit, yet changes along these directions affect policy gaps. An end-to-end case follows Octo-small versus Octo-base on eggplant through calibration sensitivity, a complete census of 64 configurations, five seed sets, confidence intervals and decisions. Across the evaluated settings, the estimated success-rate difference ranges from +0.055 to +0.174, with decisions ranging from abstention to a declared ordering.

**Second, the benchmark's configuration population is finite and explicitly enumerable.** Its episode indices cycle through 24 to 300 initial configurations, and the two ports enumerate different populations. A complete census removes configuration sampling error while leaving policy-seed variation and differences between simulator settings. We separately measure the influence of implementation and appearance choices; four robot texture variants with unchanged physics span 0.400 in one policy's success rate. These findings identify which uncertainty additional episodes can reduce and which choices require explicit reporting.

**Third, the evidence supporting an individual ranking depends on the analysis and operating point.** At the published 72-episode budget, only one or two of four reported orderings are resolved, depending on the variance model. Reapplying the calibration protocol to 98 demonstrations from the same public dataset disfavours the shipped controller on both stacks. Moving to the preferred setting changes one point verdict from abstention to declaration, although the change in the policy difference itself is unresolved. We explicitly distinguish this same-source recalibration from reconstruction of the original fitted sample.

The resulting reporting recommendations are immediately usable: enumerate the configuration grid, identify the build and visual variant, and report the operating parameters alongside their calibration loss and the best loss found in the search. A frozen companion review package will supply the episode records, provenance logs, checksums and regeneration scripts. The manuscript links earlier public archives; a version-specific public deposit of the current package has not yet been verified.

The manuscript addresses evaluation of learned manipulation policies, connecting the journal's interests in robot learning, calibration and autonomous systems. The measurements concern one suite. We collected no new physical-robot results, and our set-valued audit supplies no general guarantee of deployment performance. Section 9 specifies a physical validation protocol with matched deployment conditions, a prespecified analysis and a power-based assessment of trial counts.

The work is original, is not under consideration elsewhere, and all authors approve the submission. We have no competing interests and received no funding. AI assistance with writing and analysis scripts is disclosed in the manuscript; the authors take responsibility for the study and its interpretation.

Thank you for considering the manuscript.

Sincerely,

Jun Ji, Bowen Tan, Yi Li, Xiaolei Zhang, Shengjie Guo, and Yi Sui (corresponding author)

College of Computer Science and Technology, Qingdao University · suiyi@qdu.edu.cn
