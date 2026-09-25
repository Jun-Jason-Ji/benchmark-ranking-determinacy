# Calibration confirmation V3

This directory contains a separate controlled-initialization repetition of the spoon operating-point comparison. The outcome-blind reset validation passed all 96 prescribed resets and the coordinating agent authorized V3 execution after implementation checks.

The previous attempt is retained in `../calibration_confirmation/` and is unavailable for confirmatory inference because its prespecified initial-state gate failed. Its `V2_UNAVAILABLE_INVENTORY.json` records cell completion and file hashes without outcome statistics.

The statistical target, eight seed bases, 768-rollout budget and one-sided eight-block sign test are unchanged. The reset protocol is changed and explicitly narrows the interpretation to the new controlled-initialization execution. See `PLAN.md`.

Commands from the repository root:

```powershell
& '.venv-policy/Scripts/python.exe' 'reviews/2026-09-24_ras_strengthening/calibration_confirmation_v3/test_analysis.py'
& '.venv-policy/Scripts/python.exe' 'reviews/2026-09-24_ras_strengthening/calibration_confirmation_v3/run_confirmation.py' --freeze-only
$env:MS_ASSET_DIR = 'E:/research/the_world/data/maniskill-assets'
& '.venv-policy/Scripts/python.exe' 'reviews/2026-09-24_ras_strengthening/calibration_confirmation_v3/run_confirmation.py' --execute
```

The launcher uses the existing policy servers on ports 8767/8768 and the existing Windows simulation environment. It never starts or reconfigures services. `RUNNING.json` records its PID, `logs/` contains technical-only progress messages, and `COMPLETE.json` is written only after all 768 episodes pass collection checks. The 150-minute deadline applies to running subprocesses as well as cell launch times.

Set `MS_ASSET_DIR` in this process before launch so ManiSkill resolves the already validated assets before import. The first launch omitted that prerequisite and stopped before any environment reset or policy action; `STARTUP_ENVIRONMENT_NOTE.json` and `startup_attempts/` preserve that failure. The retry uses identical frozen source and the same protocol. No assets were downloaded and no system-wide environment variable was changed.

Only after completion run:

```powershell
& '.venv-policy/Scripts/python.exe' 'reviews/2026-09-24_ras_strengthening/calibration_confirmation_v3/analyze_confirmation.py'
```

The analyzer fails closed on an incomplete design or any scientific integrity gate. It reports the sign-based target separately from the secondary mean summaries. No confirmatory results from the failed V2 attempt are pooled into V3.
