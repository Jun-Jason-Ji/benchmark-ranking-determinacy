# Benchmark value over the full configuration grid: PutEggplantInBasketScene-v1

The task has **64** initial configurations. A policy's benchmark value is its mean success over all of them. OpenVLA is deterministic, so a complete census is exact; Octo is stochastic, so its remaining error is policy noise, read off the spread across seed sets rather than from an episode bootstrap. A decision is declared only when every seed set agrees in sign on a complete census.

Sources are chosen per policy family: Octo uses the post-fix inference-server generation (A′ = `controller_sweep_gpu_replayA`, B, C), while OpenVLA, whose server is one unchanged Windows process throughout, uses its original directory in the first column (A = `controller_sweep_gpu`), where its complete census lives.

## Coverage and benchmark values

| policy | condition | A' | B | C | D | E |
|---|---|---|---|---|---|---|
| openvla-7b-4bit | nominal | 0.156 (64/64) | 0.146 (48/64 partial) | 0.146 (48/64 partial) | – | – |
| openvla-7b-4bit | force_x0.5 | 0.250 (64/64) | 0.333 (48/64 partial) | 0.375 (48/64 partial) | – | – |
| octo-small | nominal | 0.516 (64/64) | 0.461 (64/64) | 0.453 (64/64) | – | – |
| octo-small | force_x0.5 | 0.469 (64/64) | 0.500 (64/64) | 0.406 (64/64) | – | – |
| octo-base | nominal | 0.375 (64/64) | 0.453 (64/64) | 0.500 (64/64) | – | – |
| octo-base | force_x0.5 | 0.344 (64/64) | 0.391 (64/64) | 0.453 (64/64) | – | – |
| octo-small@hist1 | nominal | 0.344 (64/64) | 0.484 (64/64) | 0.391 (64/64) | – | – |
| octo-small@hist1 | force_x0.5 | 0.406 (64/64) | 0.375 (64/64) | 0.375 (64/64) | – | – |
| octo-base@hist1 | nominal | 0.344 (64/64) | 0.344 (64/64) | 0.391 (64/64) | – | – |
| octo-base@hist1 | force_x0.5 | 0.344 (64/64) | 0.297 (64/64) | 0.375 (64/64) | – | – |

## Δ = Octo − OpenVLA on the shared configurations

| pair | condition | seed set | configs compared | census | Δ |
|---|---|---|---:|---|---:|
| octo-small vs OpenVLA | nominal | A' | 64 | complete | +0.359 |
| octo-small vs OpenVLA | nominal | B | 48 | partial | +0.323 |
| octo-small vs OpenVLA | nominal | C | 48 | partial | +0.312 |
| octo-small vs OpenVLA | force_x0.5 | A' | 64 | complete | +0.219 |
| octo-small vs OpenVLA | force_x0.5 | B | 48 | partial | +0.188 |
| octo-small vs OpenVLA | force_x0.5 | C | 48 | partial | -0.021 |
| octo-base vs OpenVLA | nominal | A' | 64 | complete | +0.219 |
| octo-base vs OpenVLA | nominal | B | 48 | partial | +0.271 |
| octo-base vs OpenVLA | nominal | C | 48 | partial | +0.417 |
| octo-base vs OpenVLA | force_x0.5 | A' | 64 | complete | +0.094 |
| octo-base vs OpenVLA | force_x0.5 | B | 48 | partial | +0.083 |
| octo-base vs OpenVLA | force_x0.5 | C | 48 | partial | +0.125 |
| octo-small@hist1 vs OpenVLA | nominal | A' | 64 | complete | +0.188 |
| octo-small@hist1 vs OpenVLA | nominal | B | 48 | partial | +0.375 |
| octo-small@hist1 vs OpenVLA | nominal | C | 48 | partial | +0.229 |
| octo-small@hist1 vs OpenVLA | force_x0.5 | A' | 64 | complete | +0.156 |
| octo-small@hist1 vs OpenVLA | force_x0.5 | B | 48 | partial | +0.062 |
| octo-small@hist1 vs OpenVLA | force_x0.5 | C | 48 | partial | +0.021 |
| octo-base@hist1 vs OpenVLA | nominal | A' | 64 | complete | +0.188 |
| octo-base@hist1 vs OpenVLA | nominal | B | 48 | partial | +0.146 |
| octo-base@hist1 vs OpenVLA | nominal | C | 48 | partial | +0.292 |
| octo-base@hist1 vs OpenVLA | force_x0.5 | A' | 64 | complete | +0.094 |
| octo-base@hist1 vs OpenVLA | force_x0.5 | B | 48 | partial | -0.083 |
| octo-base@hist1 vs OpenVLA | force_x0.5 | C | 48 | partial | +0.042 |

## Census estimator: Δ with policy-noise interval only

With every configuration enumerated, the configuration-sampling error is zero by construction; the interval below covers only the policy noise of the stochastic policy and the run-to-run noise of the deterministic one, and it shrinks as 1/sqrt(runs). Anything that survives it is not a sampling artefact.

| pair | condition | configs | census | Octo runs / OpenVLA runs | Δ | 95% (policy noise) | decision | variance model |
|---|---|---:|---|---|---:|---|---|---|
| octo-small vs OpenVLA | nominal | 64 | **complete** | 3 / 2 | +0.320 | [+0.245, +0.396] | Octo> | empirical / empirical |
| octo-small vs OpenVLA | force_x0.5 | 64 | **complete** | 3 / 3 | +0.187 | [+0.121, +0.254] | Octo> | empirical / empirical |
| octo-base vs OpenVLA | nominal | 64 | **complete** | 3 / 2 | +0.286 | [+0.209, +0.364] | Octo> | empirical / empirical |
| octo-base vs OpenVLA | force_x0.5 | 64 | **complete** | 3 / 3 | +0.125 | [+0.054, +0.196] | Octo> | empirical / empirical |
| octo-small@hist1 vs OpenVLA | nominal | 64 | **complete** | 3 / 2 | +0.250 | [+0.175, +0.325] | Octo> | empirical / empirical |
| octo-small@hist1 vs OpenVLA | force_x0.5 | 64 | **complete** | 3 / 3 | +0.115 | [+0.046, +0.183] | Octo> | empirical / empirical |
| octo-base@hist1 vs OpenVLA | nominal | 64 | **complete** | 3 / 2 | +0.203 | [+0.128, +0.278] | Octo> | empirical / empirical |
| octo-base@hist1 vs OpenVLA | force_x0.5 | 64 | **complete** | 3 / 3 | +0.068 | [-0.000, +0.135] | abstain | empirical / empirical |

## Point calibration vs union bound over the compatible set (census intervals)

Point = the nominal condition alone, the usual practice. Union = the ranking must hold at every calibration-invisible condition, so the interval is [min lower bound, max upper bound] over `force_x0.5`. A pair where the two disagree is one where point calibration declares a ranking the calibration data cannot support.

| pair | point Δ | point verdict | union interval | union verdict | disagreement |
|---|---:|---|---|---|---|
| octo-small vs OpenVLA | +0.320 | Octo> | [+0.121, +0.254] | Octo> | no |
| octo-base vs OpenVLA | +0.286 | Octo> | [+0.054, +0.196] | Octo> | no |
| octo-small@hist1 vs OpenVLA | +0.250 | Octo> | [+0.046, +0.183] | Octo> | no |
| octo-base@hist1 vs OpenVLA | +0.203 | Octo> | [-0.000, +0.135] | abstain | **yes** |

## Decision change per pair

| pair | nominal | force_x0.5 | change | sign agreement across runs |
|---|---|---|---|---|
| octo-small vs OpenVLA | Octo> | Octo> | Octo> → Octo> | same sign / mixed |
| octo-base vs OpenVLA | Octo> | Octo> | Octo> → Octo> | same sign / same sign |
| octo-small@hist1 vs OpenVLA | Octo> | Octo> | Octo> → Octo> | same sign / same sign |
| octo-base@hist1 vs OpenVLA | Octo> | abstain | Octo> → abstain | same sign / mixed |
