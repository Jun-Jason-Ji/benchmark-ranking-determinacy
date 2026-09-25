# Secondary controlled-initialization half-torque study

This directory contains a fixed secondary control, not an extension selected from V3 outcomes. `HYPOTHESIS_FREEZE.json` pins its scientific plan before any V3 comparison was analyzed. `FROZEN_PLAN.json` and `FROZEN_ANALYSIS.json` pin the implementation before collection. The completed validation used 48 outcome-free resets and matched all prior V3 state and RGB hashes.

There are 384 additional rollouts. The 384 V3 nominal rollouts are shared baselines, so V3 plus this study contains 1,152 unique rollouts, not 1,536. The 75-minute collection cap is fixed.

## Execution

Run from the project root only after V3 collection completes. The launcher checks completion, existing server identities, all frozen source hashes and technical validation. It sets the existing asset directory only for its subprocesses. It starts no services and refuses a previous collection attempt rather than overwriting it.

```powershell
& '.venv-policy/Scripts/python.exe' 'reviews/2026-09-24_ras_strengthening/calibration_torque_control/run_torque_control.py' --execute
```

`RUNNING.json` records the process and start time; logs display technical cell progress without outcome counts. `COMPLETE.json` is the successful full-design marker. `TECHNICAL_FAILURE.json` marks a failure, with all partial data retained and no secondary claim.

After both studies complete:

```powershell
& '.venv-policy/Scripts/python.exe' 'reviews/2026-09-24_ras_strengthening/calibration_torque_control/analyze_torque.py'
```

This CPU-only analyzer first validates all frozen dependencies, invokes the existing frozen V3 analyzer, then validates all 16 half-torque cells against their actual V3 nominal baselines. It outputs `ANALYSIS.json` and `ANALYSIS.md`, including all eight block contrasts, the two-sided majority-direction test, secondary mean intervals, and two-test Holm results. Reusing baseline observations does not require independence between the two marginal tests. The analysis does require the stated independent seed-block sampling assumptions.

Non-rejection is not evidence of equivalence. A sign-test result is not a mean-effect result. This is a conditional simulator study with controlled initialization, not real-world or cross-engine validation and not a retroactive repair of historical reset pairing.
