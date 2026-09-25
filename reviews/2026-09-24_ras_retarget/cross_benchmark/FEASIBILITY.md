# Independent benchmark feasibility and adoption decision

## Decision

Adopt a bounded native ManiSkill check on PickCube and PushCube with official
learned PPO pipelines. The full design is in PLAN.md and results are emitted only
after all 20 cells pass validation. Present it as portability of a finite-setting
decision audit. Do not present it as replication of calibration invisibility,
real-world ordering validation, or generalization across physics engines.

## What was actually available

- Host: Windows 10.0.26200, NVIDIA RTX 5060 Laptop GPU, 8151 MiB GPU memory,
  driver 616.92. No GPU process was active at inspection.
- Installed: ManiSkill 3.0.1 / SAPIEN 3.0.3 / PyTorch 2.7.1+cu128; original
  SIMPLER, its ManiSkill3 port, and Octo code were already present.
- No local LIBERO, RoboCasa, Isaac Lab or GR00T repository/checkpoint was found in
  the inspected project directories or Windows robotics environment. This is an
  inventory result, not a claim that those frameworks cannot be installed.
- The existing WSL distribution is Ubuntu-24.04. The native Windows state-input
  path was sufficient; no new Linux environment was created or reconfigured.
- Official ManiSkill model exports contain 1.1–1.2 MB PPO checkpoints for both
  selected tasks and both control interfaces. These are executable learned
  policies, not random-action baselines or hand-designed toy comparators.
- CPU native task smoke succeeded. GPU native task smoke succeeded after loading
  the official 78 MB PhysX archive from this directory. The unchanged DLL was
  activated only in each process; no system-wide installation or service change
  was made. GPU support on Windows is not guaranteed by upstream documentation.

## Why not count other apparent routes as a second benchmark

- A SIMPLER ManiSkill3/GR00T port retains the original task suite and assets; it
  is an implementation/backend comparison, not independent task evidence.
- BridgeData/DROID demonstrations do not supply matched outcomes for these
  evaluated checkpoints; they are not a direct replacement for policy evaluation.
- Adding random policies to an arbitrary simulator would test plumbing while
  saying little about successful robot policy comparison.
- Installing a completely new benchmark, visual policy dependencies, and several
  large checkpoints is a separate replication project. It should be driven by a
  falsifiable hypothesis and frozen protocol, not merely the count of named
  benchmarks in a manuscript.

## Scientific gain and limitations

The native check changes the task definitions, robot embodiment (Franka), policy
family (PPO), observation regime (state), and controller interfaces. It tests
whether point and finite-set decisions can be made transparently from paired
episode logs outside the SIMPLER task suite. It also retains a simple task with a
potentially stable ordering rather than selecting only reversal cases.

It shares SAPIEN/PhysX lineage with SIMPLER. The chosen perturbation set has no
real calibration evidence behind it, and the study does not claim otherwise.
Different PPO control interfaces are different policy–controller pipelines; the
comparison is not an algorithm leaderboard. Only two tasks and one checkpoint
per pipeline/task are evaluated. The default stochastic task distribution is
sampled, not exhausted. Native-task results should therefore occupy a compact
external-check subsection, not replace the main SIMPLER calibration argument.

## Reproducibility

Use ENVIRONMENT.json for exact package and source hashes, HF metadata for the
pinned public model revision, PLAN.md for the fixed task/setting/budget design,
EXECUTION_NOTES.md for implementation accommodations, full_grid/*.json for
per-episode outcomes and initial states, and RESULTS.json for independent count,
hash and scene-matching assertions. CROSS_BENCHMARK_EVIDENCE.zip contains the
small evidence set but intentionally omits reproducibly downloadable binaries.

The original Python environment, installed packages, existing experimental data,
manuscript sources and Chinese reading version were not modified by this task.

## Primary sources checked

1. Official ManiSkill code and support matrix:
   https://github.com/mani-skill/ManiSkill
2. Official model exports, pinned dataset revision:
   https://huggingface.co/datasets/haosulab/ManiSkill_Demonstrations/tree/d674485bbffdd533914e52d272fdda34c0515608/demos
3. Official PPO export recipe:
   https://github.com/mani-skill/ManiSkill/blob/main/scripts/data_generation/rl.sh
4. Native reset / RNG semantics:
   https://maniskill.readthedocs.io/en/latest/user_guide/concepts/rng.html
5. Official PhysX binary release:
   https://github.com/sapien-sim/physx-precompiled/releases/tag/105.1-physx-5.3.1.patch0
6. ManiSkill3 formal publication:
   https://www.roboticsproceedings.org/rss21/p021.pdf
