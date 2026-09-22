# Cross-backend replication (carrot, same episode_ids and policy seeds)

CPU phase: Windows jax 0.4.20 CPU; GPU phase: WSL2 jax 0.5.3 CUDA. Same simulator process type, same seeds. Agreement = fraction of episodes with identical success outcome.

| policy | condition | n | CPU successes | GPU successes | outcome agreement |
|---|---|---:|---:|---:|---:|
| octo-small | nominal | 24 | 4 | 3 | 0.96 |
| octo-small | stiff_x0.5 | 24 | 3 | 2 | 0.88 |
| octo-small | stiff_x2.0 | 24 | 2 | 4 | 0.92 |
| octo-small | damp_x0.5 | 24 | 2 | 3 | 0.88 |
| octo-base | nominal | 24 | 3 | 2 | 0.88 |
| octo-base | stiff_x0.5 | 24 | 3 | 3 | 0.83 |

Interpretation: backend numerics change individual rollouts (agreement well below 1) while condition-level success rates stay within sampling noise; per-episode outcomes are therefore not reproducible across backends and all comparisons must be made within one backend.