# Native-task prospective confirmation

This package preserves a new evaluation of the specific public PPO policies and
native ManiSkill tasks used in the earlier exploratory study. It is not a
real-robot experiment, a new benchmark, or cross-engine validation. The two
policies in each task use different controllers, so the object of comparison is
the complete fixed policy--controller pipeline.

## Reading order

1. `PLAN.md` and `FROZEN_BEFORE_EXECUTION.json`: hypotheses, sample, settings,
   endpoints, simultaneous confidence family and decision thresholds recorded
   locally before any new scene was evaluated. This is not external registration.
2. `RUNTIME_AMENDMENT_V2.md` and `FROZEN_RUNTIME_AMENDMENT_V2.json`: a narrow
   PyTorch runtime correction after the first saved cell. The original script,
   failure log and first cell are retained unchanged. No outcome summaries were
   computed before the correction; the seeds and statistical plan did not change.
3. `RESULTS.md` / `RESULTS.json`: every primary contrast, envelope, per-batch count
   and prespecified descriptive diagnostic, regardless of direction.
4. `AUDIT.json`: independent reconstruction of success from the saved 50/100-step
   states, exact-binomial interval cross-check, source hashes, and technical-repeat
   equivalence. The repeated first cell is not counted as additional evidence.

## Observation unit and success definitions

The unit is a randomized initial physical scene. Four independently seeded batch
streams each generate 256 scenes. The scalar seed vector also controls per-slot
robot reset noise, while task randomization uses a batched torch stream. Therefore
one scalar seed is not a sufficient scene identifier. Exact initial states are
stored and matched across policies and settings. There are 1024 distinct scene
pairs per task/setting; these are draws from the native randomization procedure,
not a complete census of the benchmark's continuous scene distribution.

Different seeds and absence of duplicate states establish separation from the
earlier data, not stochastic independence. The finite-sample coverage statement
assumes independently, identically sampled scenes in the simulated randomization
model. Settings and endpoints need not be independent for the confidence-family
union bound.

The two primary outcomes are ever-success during control steps 1--50 and success
at step 50. Both use the same native success predicate and the same trajectories.
Endpoint success does not mean uninterrupted success or continuous holding.
Steps 51--100 and success for ten consecutive steps are predetermined descriptive
diagnostics, with no additional significance claim. Success sequences include all
100 control steps; object, goal and robot states are saved initially and at steps
50/100. Actions continue after successful steps, and every rollout ends at step
100. The first 50 steps form the primary comparison.

The primary family contains 20 fixed joint-minus-Cartesian differences, spanning
two tasks, two endpoints and five settings. For each difference, the two paired
discordance probabilities receive Clopper--Pearson intervals with tail probability
0.000625. Their component bounds are subtracted. The union bound gives simultaneous
coverage of at least 95% over the family under the stated scene-sampling model.
Five-setting envelopes cover only the tested finite settings, not a continuous
parameter range or unknown physical robot.

## CPU-only reproduction

In the full project, with NumPy and SciPy installed:

```text
python reviews/2026-09-24_ras_strengthening/confirmatory/analyze_confirmatory_v2.py
python reviews/2026-09-24_ras_strengthening/confirmatory/audit_saved_evidence.py
```

The first command reads all 80 completed cells and checks state pairing, old/new
sample separation and source metadata before recomputing results. The second
also verifies the installed source and runtime binary against the prior build;
it therefore requires that installation. The portable analysis included in the
evidence ZIP instead reads its bundled prior-state references and needs only
NumPy/SciPy; it does not require a GPU or public policy weights.

After extracting `CONFIRMATORY_EVIDENCE.zip`, run from its `confirmatory` folder:

```text
python analyze_portable.py
```

## Evaluation environment and public checkpoints

The full installed-source hashes and binary provenance are preserved in
`prior_reference/ENVIRONMENT.json`. The environment is Windows, Python 3.11.16,
ManiSkill 3.0.1, SAPIEN 3.0.3, torch 2.7.1+cu128, gymnasium 1.3.0, and an NVIDIA
RTX 5060 Laptop GPU. The official PhysX GPU library is loaded only within each
process; no system file, service or auto-start setting is changed. Upstream's
support matrix does not guarantee this Windows GPU configuration, so the results
are explicitly tied to this recorded build. The native task/observation/controller
interface was independently checked in the earlier evidence package.

Pinned public checkpoint base URL:

```text
https://huggingface.co/datasets/haosulab/ManiSkill_Demonstrations/resolve/d674485bbffdd533914e52d272fdda34c0515608/demos/
```

Append `PickCube-v1/rl/` or `PushCube-v1/rl/`, followed by
`ppo_pd_joint_delta_pos_ckpt.pt` or `ppo_pd_ee_delta_pos_ckpt.pt`. Official LFS
hashes are in the bundled `hf_*_tree.json` records; each raw cell records the
checkpoint hash actually verified before evaluation. Third-party checkpoints
and the 237 MB runtime DLL are excluded from the evidence ZIP; their sources and
hashes are retained. Evaluation in the full project uses the existing files in
the earlier cross-benchmark directory.

The evaluated checkpoints were trained/exported from an earlier ManiSkill
revision. The current study evaluates them under the recorded installation and
does not claim reproduction of official training scores. No calibration
demonstrations exist for the tested arm-setting perturbations, so they are not
called calibration-invisible directions.
