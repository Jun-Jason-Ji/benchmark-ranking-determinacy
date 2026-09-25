# Replay initialization audit

Audit date: 2026-09-24. This is a read-only source and stored-array audit, without simulator execution, policy calls, or access to the ongoing V3 policy outcomes.

## Finding

The newly detected sequential **policy-scene** initialization failure does not, on the inspected evidence, invalidate the reported **replay loss** surfaces. The replay scripts explicitly realign and reset the robot for every demonstration. The ManiSkill3 replay uses an empty environment rather than the Bridge task's object-settling path. Across all 12,936 saved trajectories in eight replay scopes, the first recorded end-effector position and quaternion are byte-identical for each demonstration across conditions, including comparisons between replay scopes on the same simulator stack. All initialization-success flags are valid. This is evidence for consistent replay alignment, not a retrospective certificate of complete physical-state equality.

The common-scale and half-torque observations remain supported at their stated finite demonstration and setting scope. They should not be withdrawn because of the separate policy-scene reset defect, nor used to certify that old policy rollouts had matched initial scenes.

## Source trace

All paths below are relative to the repository root. Exact hashes of the inspected source files are in `REPLAY_SOURCE_SHA256.json`.

### ManiSkill3 replay

`scripts/replay_bridge_sysid.py` creates `Empty-v1` (line 126), captures a canonical joint configuration from the newly built condition environment (line 136), and starts every demonstration's inverse-kinematics search from that configuration (lines 160–172). Retry perturbations use a demonstration-specific deterministic random generator. The solution is installed with `agent.reset(q_full)` and an explicit `agent.controller.reset()` (lines 195–196). The robot root is lifted before alignment and the first end-effector pose is recorded before any replay action (lines 160–161 and 204–213). The external action-delay queue is initialized separately for every demonstration.

The currently installed `mani_skill/envs/tasks/empty_env.py` has only a ground scene and an empty `_initialize_episode` method (lines 38–43). It does not execute Bridge object settling. The installed agent reset sets joint positions, zeros joint velocities, and zeros generalized forces (base agent lines 398–408); the replay's additional controller reset initializes the target to the aligned robot state. The source comment describing a previous inherited-joint-state IK bug is consistent with the explicit canonical reset, but the comment alone is not treated as proof of a historical run.

### Original ManiSkill2 replay

`scripts/replay_bridge_sysid_ms2.py` uses the original headless Bridge environment. Each demonstration calls `env.reset(seed=0)`, lifts the robot root, solves IK for the first recorded real end-effector pose, and calls `u.agent.reset(cur_qpos)` (lines 222–231). This follows the alignment pattern in the upstream `tools/sysid/sysid.py`.

The editable Linux installation points to `third_party/SimplerEnv/ManiSkill2_real2sim`. In that source, `envs/custom_scenes/base_env.py` initializes the WidowX agent with a fixed joint vector (lines 261–299). `agents/base_agent.py` resets joint position, velocity, acceleration, and force, then selects the default controller (lines 154–160); selecting it resets the controller (lines 124–132). The pose-controller IK therefore starts from a reset joint vector, and the final agent reset refreshes the controller target after alignment. `agents/base_controller.py` reapplies drive properties during reset (lines 95–97).

The ManiSkill2 task can still contain initialized objects and their settling history. The replay archive does not contain complete object/contact state, so this audit does not establish that all nonrobot states match or directly prove absence of every possible contact. The intended replay is the reference protocol's lifted, free-space action replay. Stored end-effector alignment is exactly consistent across conditions.

## Stored-data verification

`audit_replay_initialization.py` checks every declared condition and all 98 declared demonstration IDs, validates array shapes and finite values, recomputes initial translation error, compares initial simulated position/quaternion bytes and complete ground-truth arrays, and recomputes the common-scale/torque comparisons. It imports NumPy only; no simulation is run. It produced `REPLAY_INITIALIZATION_RESULTS.json` and the 13,081-input SHA256 manifest `REPLAY_INITIALIZATION_INPUTS.json`.

| Scope | Conditions | Trajectories | Initial TCP mismatches |
|---|---:|---:|---:|
| ManiSkill3 original grid | 50 | 4,900 | 0 |
| ManiSkill3 one-factor sweep | 7 | 686 | 0 |
| ManiSkill3 fitted-ratio sweep | 5 | 490 | 0 |
| ManiSkill2 original grid | 50 | 4,900 | 0 |
| ManiSkill2 one-factor sweep | 7 | 686 | 0 |
| ManiSkill2 extended common scale | 5 | 490 | 0 |
| ManiSkill2 additional fitted-ratio settings | 4 | 392 | 0 |
| ManiSkill2 fitted-force probe | 4 | 392 | 0 |
| Total | | 12,936 | 0 |

The four additional ManiSkill2 fitted-ratio settings omit the fitted point already present in the original grid; this is not a missing planned condition. All compared ground-truth arrays agree. Initial translation residuals are 0.0503–0.0997 mm on ManiSkill3 and 0.00578–0.0778 mm on ManiSkill2, consistently across each stack's replay scopes. These are IK alignment residuals relative to the demonstration, not condition-dependent mismatches.

Recomputed quantities relevant to the manuscript:

- Within the original grids, the maximum Euclidean displacement between trajectories at equal gain ratio is 0.146876 mm on ManiSkill3 and 0.223898 mm on ManiSkill2. The maximum groupwise spread of mean composite replay loss is 7.16896e-6 and 7.18983e-6, respectively.
- The separate ManiSkill2 common-scale range 0.25–4 has a maximum Euclidean trajectory displacement of 0.566635 mm. Its all-pairs mean-loss spread is 3.83850e-6. This all-pairs quantity differs from the manuscript's explicitly nominal-referenced mean-loss change and must not replace that quantity without changing the definition.
- Halving nominal torque limits gives byte-identical stored end-effector positions and quaternions for 97/98 demonstrations on each stack. The exceptional maximum Euclidean differences are 0.210734 micrometres on ManiSkill3 and 0.0541811 mm on ManiSkill2.
- At the separate fitted operating point, the ManiSkill2 half-torque probe gives 96/98 byte-identical trajectories; the two residual maximum displacements are 0.0860522 mm and 0.00122446 mm. The nominal 97/98 statement must not be generalized to this fitted probe.
- Wider fitted-ratio probes have different bounds (0.983769 mm on ManiSkill3 and 0.906688 mm for the four additional ManiSkill2 settings). The smaller original-grid bounds are not bounds on these wider fitted-ratio designs.

## Provenance and remaining limits

The replay run metadata identifies the simulator protocol, conditions, demonstration IDs, nominal parameters, and upstream Simpler commit `06accaca93535902d408da4855f21cece12bceb7`. It does not record the exact executed local script hash at collection time. The original runs began on 2026-09-19, before the first tracked repository commit inspected here, so present source hashes are an audit of the available implementation, not a cryptographic reconstruction of historical execution. The earliest tracked script version already contains the canonical-reset logic.

The saved arrays contain `sim_p`, `sim_q`, `gt_p`, `gt_q`, translation errors, and rotation errors. They do not contain initial full joint/rigid-body state, controller internals, contact traces, or commanded torques. Equal TCP poses alone cannot exclude redundant joint configurations; the explicit canonical IK source path provides the complementary implementation evidence. Equal replay trajectories do not prove an inactive-saturation mechanism. The wording should remain that weak replay sensitivity is observed on these demonstrations and settings, with the mechanism unconfirmed by the stored data.

No replacement replay experiment is required by this audit. If stronger mechanistic or bitwise full-state claims are desired later, a new outcome-blind replay protocol should save full initial articulation/body state and torque/contact sequences with source hashes at collection time. Such a study would be new evidence and should not silently overwrite the historical replay archive.
