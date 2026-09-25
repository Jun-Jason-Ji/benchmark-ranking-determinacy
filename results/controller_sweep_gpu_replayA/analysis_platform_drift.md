# Policy-seed noise vs platform drift: PutEggplantInBasketScene-v1, 64-configuration census

A and A' share the policy seeds (base 20260918) and differ only in the server generation; A', B and C share the generation and differ in seeds. Everything is restricted to episode_id < 64 so each set covers each configuration once.

## Benchmark values

| set | condition | octo-small | octo-base | Δ (small − base) | n |
|---|---|---:|---:|---:|---:|
| A (09-18 16:46, pre-fix) | nominal | 0.547 | 0.297 | +0.250 | 64 |
| A (09-18 16:46, pre-fix) | force_x0.5 | 0.484 | 0.297 | +0.188 | 64 |
| A' (today, A's seeds) | nominal | 0.516 | 0.375 | +0.141 | 64 |
| A' (today, A's seeds) | force_x0.5 | 0.469 | 0.344 | +0.125 | 64 |
| B (09-18 23:05) | nominal | 0.484 | 0.516 | -0.031 | 64 |
| B (09-18 23:05) | force_x0.5 | 0.500 | 0.391 | +0.109 | 64 |
| C (09-19 20:34) | nominal | 0.453 | 0.500 | -0.047 | 64 |
| C (09-19 20:34) | force_x0.5 | 0.406 | 0.453 | -0.047 | 64 |

## A vs A': same seeds, different server generation

| policy | condition | A | A' | difference | per-episode agreement |
|---|---|---:|---:|---:|---:|
| octo-small | nominal | 0.547 | 0.516 | -0.031 | 0.88 (56/64) |
| octo-small | force_x0.5 | 0.484 | 0.469 | -0.016 | 0.80 (51/64) |
| octo-base | nominal | 0.297 | 0.375 | +0.078 | 0.73 (47/64) |
| octo-base | force_x0.5 | 0.297 | 0.344 | +0.047 | 0.80 (51/64) |

## Reading

- Platform drift (same seeds, different generation): mean |change| = 0.043, max = 0.078 over 4 policy×condition cells.
- Compare with the spread across seed sets on one generation (A', B, C) in the first table: if the A→A' change is of the same size as the A'/B/C spread, the earlier 'seed set' differences were at least partly server generation, and seed set A should be replaced by A' in every comparison.
