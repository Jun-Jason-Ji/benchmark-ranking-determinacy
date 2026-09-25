# Outcome-blind fresh-reset validation

This technical protocol is recorded before running the new reset tests. It does
not collect policy rollouts, inspect success fields, select an effect direction,
or change any earlier failed data. Installed packages remain unchanged.

The failed sequential-reset path may permit a previous robot pose/controller to
affect object settling. Test a fresh native environment for every episode,
constructed with nominal robot/contact parameters, then explicitly reset to the
requested scene under nominal gains. Only after the reset and rendering are
complete, assign the requested arm controller gains to the new instance and
write those gains to its actual SAPIEN joints. No physics step occurs between
recording the canonical initial state and beginning the rollout. Delay is an
external action-queue property and is not simulated in this test.

Test all 24 spoon configuration IDs in four complete passes: nominal, fitted,
fitted, nominal. Every pass uses fresh constructions inside the same outer
process. Fitted means stiffness multiplied by 2, damping by 0.5, unchanged force
limit, and an externally applied one-step delay. Verify exact full-state
dictionary and initial RGB equality across all four copies of each scene.
Save all initial states, image hashes and canonical PNGs. The equality gate is
exact; no physical tolerance will be substituted for a failure.

Read back controller config and actual joint gains after application and after
controller.reset(), confirming that resetting the controller does not undo the
condition. Verify gripper joint properties and actor mass/contact properties
remain unchanged, initial state does not change on parameter assignment, and
the controller and renderer reference the active new environment. On exit,
verify the closed environment's scene and agent references have been cleared.
No inference-server request or policy action is made. The test logs source
hashes, package versions, timestamps, 5 Hz control/500 Hz physics and timings.

If fresh constructions in one process fail exact equality, preserve their
records and report the failure before considering process isolation. Do not
relax equality or silently discard any scene. The run is bounded to 96 resets;
the first pass also supplies a runtime estimate for the proposed 768-rollout
controlled-initialization study.
