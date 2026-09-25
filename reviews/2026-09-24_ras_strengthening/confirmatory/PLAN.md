# Native-task confirmatory evaluation: frozen local protocol

Recorded before any run on the new scene sample, 2026-09-24. This is a local
prospective execution protocol, not an externally registered study. The earlier
study motivated the hypotheses; all its outcomes and its post-hoc analysis remain
unchanged. New outcome files are kept in this directory only.

## Primary question

On new sampled scenes, does the previously observed PushCube ordering difference
between ever-success by step 50 and success at step 50 persist? PickCube is a
specified contrast task. The target is these fixed public policy--controller
pipelines under this simulator build, not algorithms across training seeds,
real-world transfer, calibration-invisible parameter directions, or cross-engine
generalization.

## Fixed design and budget

- Two tasks: native ManiSkill `PickCube-v1` and `PushCube-v1`, Franka Panda.
- Two public PPO pipelines per task: joint-position increments and Cartesian-
  position increments; deterministic actor means, unchanged verified checkpoints.
- Five fixed arm settings: nominal (stiffness 1000, damping 100, force limit 100),
  common stiffness/damping multiplied by 0.5 or 2, and force limit multiplied by
  0.5 or 2. Gripper parameters remain at native defaults.
- Four fresh vectorized batches, each containing 256 sampled initial states.
  Batch seed-vector starts are 731250001, 893460001, 1135790001, 1579130001;
  each vector contains its start through start+255. The first seed controls a
  batched torch stream for task randomization; per-slot seeds also control robot
  reset noise. A seed number alone is not treated as a physical scene identity.
- All four batches are evaluated in every task/pipeline/setting combination:
  1024 scene pairs per task and setting, 20480 total rollouts.
- Each rollout executes exactly 100 steps at 20 Hz control / 100 Hz physics.
  At step 50 the two primary endpoints are read from the unmodified first
  50 steps. Continuing to step 100 does not change these primary observations.
- GPU compute budget: up to 25 minutes wall time for the complete primary run.
  Exceeding the budget or a technical failure is recorded, not treated as a
  failure outcome. No optional sample-size stopping or selective cell omission.
  A single process per task/pipeline reuses its native environment across
  batches and settings, with explicit resets and gain assignment before each cell.

## Endpoint family and confirmatory criteria

Primary endpoints, fixed now:

1. Ever-success: at least one successful control step among steps 1--50.
2. Endpoint success: successful at control step 50, with no requirement of
   continuous success before that step.

For each endpoint, the signed difference is joint-pipeline success minus
Cartesian-pipeline success on exactly paired physical scenes. The primary family
has 2 tasks × 2 endpoints × 5 settings = 20 differences. With family error
alpha=0.05, allocate alpha_cell=0.0025 to each two-sided difference interval.
Each of its two discordance probabilities receives an exact Clopper--Pearson
interval with two-sided error alpha_cell/2=0.00125, equivalently each tail
0.000625. Subtract component bounds to form the paired-difference interval.
This union-bound construction gives simultaneous coverage at least 0.95 for
all 20 fixed differences under independent-scene binomial sampling assumptions.
No independence across settings, endpoints, or tasks is required for the union
bound. Finite-setting envelopes use the minimum lower and maximum upper bound.

Confirm the PushCube observation only if its ever-success envelope is strictly
positive and its endpoint-success envelope is strictly negative on this new
sample. Confirm the PickCube contrast if both envelopes are strictly positive.
Report each component decision even if the overall conjunction does not pass.
All 20 differences, four envelopes, and per-batch counts are reported. This
protocol is not changed to fit the new outcomes.

## Predetermined descriptive diagnostics

- Full binary success sequence for every rollout, steps 1--100.
- Ever-success by step 100, success at step 100, and at least 10 consecutive
  successful steps within steps 1--50 or 1--100 (0.5 s at 20 Hz).
- First successful step, longest successful run, and success lost by the horizon
  among trajectories that previously succeeded.
- These diagnose the distinction between reaching and sustaining a task state.
  They are not additional confirmatory endpoints and receive no selected
  significance claims or unreported searches over dwell duration/horizon.

## Integrity gates

- Preserve source and plan hashes before execution; check unchanged model hashes
  against the earlier verified official LFS metadata.
- Save initial simulator state dictionaries, explicit joint/object/target states,
  initial observations, parameter assignments, control/physics frequencies,
  complete success sequences, and final/50-step object/target states.
- Verify exact physical-state pairing across all policy/settings in each batch,
  distinct sampled states, and zero overlap with the earlier study and pilot.
- Check 100 steps, finite observations, and complete 80 batch/pipeline/setting
  cells; failed executions are neither silently replaced nor counted as failures.
- Retain any source-level runtime adjustment separately, without overwriting old
  data or retrospectively calling an altered result preregistered.
- Inference is conditional on the current build/checkpoints and independent
  randomized-scene model. Batch-wise results and a conservative finite-sample
  concentration-bound sensitivity will make the assumed observation unit visible.
