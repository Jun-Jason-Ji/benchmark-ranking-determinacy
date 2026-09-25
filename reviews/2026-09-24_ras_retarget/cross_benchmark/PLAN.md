# Native ManiSkill external check: frozen design

Recorded 2026-09-24 before the non-nominal and full-budget runs. This is a local
prospective execution record, not an independently timestamped preregistration.
The feasibility pilot used 16 PickCube scenes at nominal settings only; its joint
and Cartesian PPO pipelines achieved 16/16 and 10/16 final successes. The pilot
scene seeds are excluded from the main evaluation sample below.

## Question and scope

Can the same finite-setting, paired-episode decision audit be executed on two
native ManiSkill tasks and public learned policies outside SIMPLER? This checks
workflow portability and sensitivity to specified execution settings. It does
not test real-world transfer, calibration-invisible directions, or a calibrated
physical uncertainty set. ManiSkill and SIMPLER share SAPIEN/PhysX ancestry, so
this is not an independent-physics-engine replication.

## Fixed design

- Tasks: native `PickCube-v1` and `PushCube-v1`, default Franka Panda embodiment.
- Policies: official state-input PPO actor means with `pd_joint_delta_pos` and
  `pd_ee_delta_pos`, fetched from the pinned revision recorded in the HF metadata.
  Compare these as two policy–controller pipelines, not identical action spaces.
- Backend: ManiSkill 3.0.1, SAPIEN 3.0.3, native GPU PhysX and built-in GPU IK.
  No SIMPLER scene, action adapter, reward, or policy checkpoint is used.
- 256 scene seeds per task: 2026092500 through 2026092755, paired across policies
  and settings. The actual initial joint and object states must match exactly.
  This sample is drawn from a continuously randomized task, not the benchmark's
  exhaustive configuration population. Deterministic actor means introduce no
  additional policy sampling seed. Policy training seeds are not replicated.
- Five arm execution settings: nominal `(k,d,F)=(1000,100,100)`; common gains
  multiplied by 0.5 and 2; force limit multiplied by 0.5 and 2. Gripper settings
  stay at defaults. Altering force/gains is an explicit robustness intervention,
  not a claim that all these settings fit any real calibration demonstrations.
- Run every task × policy × setting cell, each for exactly 50 control steps.
  Primary outcome is success at the final step. Ever-success is a diagnostic.
  Total primary sample: 2 × 2 × 5 × 256 = 5120 episodes.
- Keep null results and all cells. No selection of tasks, settings, or budgets
  based on observed ordering or significance. No expansion to more extreme
  interventions after inspection.

## Statistics

For each setting, the signed outcome is joint-pipeline success minus Cartesian-
pipeline success, taking values -1,0,+1 on matched scenes. Estimate the difference
by its scene average. Report a conservative 95% interval using exact binomial
intervals for the probabilities of +1 and -1 discordance: each component's
two-sided confidence level is 97.5% (tail probability 0.0125), then subtract the
component endpoints. This avoids degenerate bootstrap bounds at zero failures.
The finite-setting envelope takes the minimum lower and maximum upper bound.
The joint / Cartesian / abstain rule uses whether that envelope is wholly above
zero, wholly below zero, or crosses zero. Neither action ordering is privileged.

Uncertainty refers to the randomized initial-scene distribution under the stated
binomial sampling assumptions, conditional on these checkpoints and this build;
it is not uncertainty over training runs or real robots. Report the finite-sample
counts separately. Prefix budgets 32,64,128,256 are descriptive sensitivity
analyses; do not present a selectively chosen prefix as a primary result.

## Integrity gates

Verify checkpoint SHA256 against official LFS file hashes; require 50 steps and
finite observations; verify matching stored initial physical states; retain
per-episode logs and all nonzero exit codes. A failed cell is not a zero success
rate. Do not silently change the evaluator, controller, or task after results.
