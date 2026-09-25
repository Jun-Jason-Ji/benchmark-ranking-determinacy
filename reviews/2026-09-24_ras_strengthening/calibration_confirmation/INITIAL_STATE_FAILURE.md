# Initial-state integrity failure, detected without outcome analysis

On 24 September 2026, completed-cell technical checks found that matching episode IDs and policy seeds did not produce matched initial physical states in the proposed spoon confirmation. No success field was inspected, and no policy gap, direction count, significance test or confirmatory p-value was computed for this diagnosis. The frozen analyzer was not changed or relaxed.

The source/metadata, actual built arm stiffness/damping/force, delay, 60-step horizon, session and reseeding checks passed for the inspected cells. The control and simulation frequencies are 5 Hz and 500 Hz. The **physical-state and initial-image pairing gate failed**.

| First-block comparison | Identical state and image hashes | Maximum actor position difference | Maximum actor rotation difference |
|---|---:|---:|---:|
| Octo-Base nominal versus Octo-Small nominal | 6 of 24 configurations | 15.3554 mm | 23.1980 degrees |
| Octo-Small nominal versus Octo-Small fitted | 10 of 24 configurations | 23.1956 mm | 35.7537 degrees |

Position differences are Euclidean distances between the stored three-coordinate actor positions. Rotation differences use twice the arccosine of the absolute inner product of normalized quaternions, so quaternion sign equivalence does not create a false difference. Maxima range over the task actors and the 24 configurations. These are initial-state measurements, not success effects.

For example, in configuration 2 the two nominal policies already differ in spoon position by approximately 2.9 mm and in orientation. Configuration 1 also shows nonzero spoon velocity in one nominal cell and zero velocity in the other. Thus the failure is not simply JSON serialization, a coordinate-norm mistake, or tiny rendering roundoff.

## Source-level mechanism to test

The installed ManiSkill3 source offers a plausible history-dependent reset mechanism:

1. `mani_skill/envs/sapien_env.py` clears velocities and calls `agent.reset()` before the task initializer.
2. `mani_skill/agents/base_agent.py:398` explicitly leaves robot joint positions unchanged when `init_qpos` is omitted. It clears velocities and generalized forces.
3. `mani_skill/envs/tasks/digital_twins/bridge_dataset_eval/base_env.py:357` places the task actors and calls the physics-settling routine before subsequently assigning the prescribed robot pose and joint positions.

Consequently, a previous rollout's robot configuration or controller state can potentially affect object settling on the next reset. This is consistent with the observed policy-dependent initial states. It is a source-supported mechanism hypothesis, not yet an isolated causal experiment. A fresh environment for each episode, or a fully specified canonical pre-settling robot/controller state, needs a separate outcome-blind technical validation before claiming that the pairing problem is solved.

## Consequences

The current collection does not pass its frozen physical-pairing gate and must not be used to report the planned confirmatory sign test. Technical attempts should be retained, with a prospective runtime/protocol amendment if a new collection is authorized. Changing the gate to a permissive numerical tolerance would not address centimetre-scale position and substantial orientation differences.

This finding also limits interpretation of historical comparisons that used the same reset implementation without storing and verifying paired initial physical states. Their observed differences remain descriptions of their executed protocols; attributing them solely to the controller operating point requires the separately controlled reset study. The finding is specific to the inspected ManiSkill3 execution path and is not evidence about the original ManiSkill2 reset behavior.

`INITIAL_STATE_FAILURE.json` records all 24 configuration/actor comparisons and SHA-256 hashes of the consumed audit files and installed source files. `compare_initial_states.py` regenerates it using only reset-state fields. `technical_prechecks/` preserves time-stamped interface checks. No original data, source file, study plan or frozen analyzer was overwritten by this audit.
