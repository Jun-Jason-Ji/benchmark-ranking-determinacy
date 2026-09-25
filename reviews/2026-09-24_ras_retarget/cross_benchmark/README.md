# Native ManiSkill decision-audit evidence

Read RESULTS.md for findings and PLAN.md for the design fixed before the complete
grid. FEASIBILITY.md and EXECUTION_NOTES.md state the scope and implementation
limits. This is an independent-task check outside SIMPLER, not a real-robot or
calibration-identifiability validation.

Both success definitions are reported. The primary final-step metric asks about
success retained at step 50; ever-success asks whether it occurs by that step.
For PushCube these lead to opposite pipeline orderings. INTERFACE_AUDIT.json
records an independent official-actor/vector-wrapper replay that reproduced
all nominal outcome indicators and ruled out the checked observation-order,
control-frequency, timeout and success-predicate mistakes. The secondary metric
comparison is descriptive, without a joint post-selection confidence guarantee.

## Analyze the included evidence without a GPU

With NumPy and SciPy installed:

```text
python analyze_grid.py
python check_interval.py
```

The analysis verifies 20 complete cells, 256 distinct initial states per task,
exact state matching across policy/setting cells, checkpoint hashes, and outcome
counts before writing results. The checkpoint verification requires the four
small public weight files, which are retained locally but excluded from the ZIP.
If analyzing the small ZIP, first download them using the pinned locations below.

The interval check enumerates all multinomial outcomes for n=16 over 231 choices
of discordance probabilities. It checks the implementation numerically; the
mathematical coverage argument remains exact-binomial marginal coverage plus
the union bound. It does not use or tune to the robot outcomes.

## Public weights

Base URL:

```text
https://huggingface.co/datasets/haosulab/ManiSkill_Demonstrations/resolve/d674485bbffdd533914e52d272fdda34c0515608/demos/
```

Append each path and save under the specified local name:

| Upstream path | Local name |
|---|---|
| PickCube-v1/rl/ppo_pd_joint_delta_pos_ckpt.pt | ppo_pd_joint_delta_pos_ckpt.pt |
| PickCube-v1/rl/ppo_pd_ee_delta_pos_ckpt.pt | ppo_pd_ee_delta_pos_ckpt.pt |
| PushCube-v1/rl/ppo_pd_joint_delta_pos_ckpt.pt | PushCube_ppo_pd_joint_delta_pos_ckpt.pt |
| PushCube-v1/rl/ppo_pd_ee_delta_pos_ckpt.pt | PushCube_ppo_pd_ee_delta_pos_ckpt.pt |

Exact official LFS hashes are in the two `hf_*_tree.json` records and RESULTS.json.
Each file is approximately 1.2 MB. Public policy training/export metadata is
included, but its success-only demonstration trajectories are not used to infer
evaluation success rates.

## Re-run the robot evaluation

Use a fresh directory containing these scripts and metadata, without copying the
included full_grid result directory. Use the package versions in ENVIRONMENT.json,
the four verified weights above, and the unchanged official PhysX GPU DLL from
the recorded release. Unpack its Windows DLL archive into `physx_runtime` beside
the scripts. Then run:

```text
python run_grid.py
python analyze_grid.py
```

The runner never overwrites an existing cell. Each cell is a fresh process with
256 vectorized scenes, ensuring identical batch size and seeds throughout. It
loads only the policy actor weights (`weights_only=True`); no training or random
action policy is run. No image generation, system-wide DLL installation, driver
modification, service or startup registration is involved.

Windows GPU support is not guaranteed by the upstream support matrix. These
components completed the recorded local evaluation; this is not a guarantee for
another machine or an equivalence claim about Linux, CPU and GPU backends.

## Artifact contents and licenses

CROSS_BENCHMARK_EVIDENCE.zip contains all small scripts, public metadata, per-trial
results, execution logs, source hashes, interpretation notes and its own manifest.
Public runtime binaries and weights are not redistributed in the archive. The
downloaded upstream PPO source is retained for architecture provenance, with
the installed ManiSkill Apache-2.0 and third-party license files. Our evaluator
does not import or execute the upstream training script.

The scientific outputs are success counts and intervals, not a claimed gain in
policy performance or a new PPO method. All failures, negative results and
abstentions are retained. Chinese manuscript files were not changed.
