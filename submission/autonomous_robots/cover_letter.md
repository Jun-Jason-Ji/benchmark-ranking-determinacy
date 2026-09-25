# Cover letter — Autonomous Robots

Dear Editor-in-Chief,

We submit for consideration in *Autonomous Robots* our manuscript **“What Determines a Simulation Benchmark Ranking? Structural Blindness, Finite Configuration Grids, and Evaluation Budget in Simulation-Based Policy Comparison.”**

Simulation evaluations increasingly guide the selection of robot foundation policies for physical deployment. A ranking can therefore affect which policy a laboratory spends its robot time testing. We investigate when a benchmark's calibration data, configuration coverage and evaluation budget support such a comparison. Our audit of SIMPLER spans two embodiments and two simulator stacks, beginning with a reproduction of eight published rates at a mean absolute difference of 0.038. It establishes three empirical contributions.

**First, calibration sensitivity and policy-comparison sensitivity can diverge.** Free-space demonstration replay is weakly informative about common controller-gain rescaling and an inactive torque limit, yet changes along these directions affect policy gaps. An end-to-end case follows Octo-Small versus Octo-Base on eggplant through calibration sensitivity, a complete census of 64 configurations, five seed sets, confidence intervals and decisions. Across the evaluated settings, the estimated success-rate difference ranges from +0.055 to +0.174, with decisions ranging from abstention to a declared ordering.

**Second, the benchmark's configuration population is finite and explicitly enumerable.** Its episode indices cycle through 24 to 300 initial configurations, and the two ports enumerate different populations. A complete census removes configuration sampling error while leaving policy-seed variation and differences between simulator settings. We separately measure the influence of implementation and appearance choices; four robot texture variants with unchanged physics span 0.400 in one policy's success rate. These findings identify which uncertainty additional episodes can reduce and which choices require explicit reporting.

**Third, ranking decisions depend on analysis and operating point.** The published 72-episode budget resolves one or two of four reported orderings, depending on the variance model. Same-source recalibration on 98 demonstrations favours a different controller setting on both stacks; identity with the original fitted sample is unverified. Complete censuses on two tasks show different consequences. On eggplant, the point verdict changes from abstention to declaration, its paired gap change remains unresolved, and both set envelopes abstain. On spoon, the estimated gap falls from +0.396 to +0.125, a paired shift of −0.271 resolved under the reported sampling models; both point and set-envelope declarations become abstentions.

The resulting reporting recommendations are immediately usable: enumerate the configuration grid, identify the build and visual variant, and report the operating parameters alongside their calibration loss and the best loss found in the search. The accompanying frozen review package supplies the episode records, provenance logs, checksums and regeneration scripts. The manuscript identifies the earlier public v1.1.3 archive separately; the current package has not yet been deposited as a new public version.

The manuscript addresses evaluation of learned manipulation policies, connecting the journal's interests in robot learning, calibration and autonomous systems. The measurements concern one suite. We collected no new physical-robot results, and our set-valued audit supplies no general guarantee of deployment performance. Section 9 specifies a physical validation protocol with matched deployment conditions, a prespecified analysis and a power-based assessment of trial counts.

The work is original, is not under consideration elsewhere, and all authors approve the submission. We have no competing interests and received no funding. AI assistance with manuscript revision and analysis scripts is disclosed in the manuscript; the authors take responsibility for the study and its interpretation.

Thank you for considering the manuscript.

Sincerely,

Jun Ji, Bowen Tan, Yi Li, Xiaolei Zhang, Yizhou Zhao, Shengjie Guo, and Yi Sui (corresponding author)

College of Computer Science and Technology, Qingdao University, Qingdao, China · suiyi@qdu.edu.cn
