# Benchmark value over the full configuration grid: PutEggplantInBasketScene-v1

The task has **64** initial configurations. A policy's benchmark value is its mean success over all of them. OpenVLA is deterministic, so a complete census is exact; Octo is stochastic, so its remaining error is policy noise, read off the spread across seed sets rather than from an episode bootstrap. A decision is declared only when every seed set agrees in sign on a complete census.

Sources are chosen per policy family: Octo uses the post-fix inference-server generation (A′ = `controller_sweep_gpu_replayA`, B, C), while OpenVLA, whose server is one unchanged Windows process throughout, uses its original directory in the first column (A = `controller_sweep_gpu`), where its complete census lives.

## Coverage and benchmark values

| policy | condition | A' | B | C | D | E |
|---|---|---|---|---|---|---|
| openvla-7b-4bit | nominal | 0.156 (64/64) | 0.146 (48/64 partial) | 0.146 (48/64 partial) | – | – |
| openvla-7b-4bit | force_x0.5 | 0.250 (64/64) | 0.333 (48/64 partial) | 0.375 (48/64 partial) | – | – |
| openvla-7b-4bit | iso_x0.25 | 0.172 (64/64) | – | – | – | – |
| openvla-7b-4bit | iso_x4.0 | 0.094 (64/64) | – | – | – | – |
| openvla-7b-4bit | fric_x0.4 | 0.047 (64/64) | – | – | – | – |
| openvla-7b-4bit | dens_x0.5 | 0.156 (64/64) | – | – | – | – |
| octo-small | nominal | 0.516 (64/64) | 0.461 (64/64) | 0.453 (64/64) | – | – |
| octo-small | force_x0.5 | 0.469 (64/64) | 0.500 (64/64) | 0.406 (64/64) | – | – |
| octo-small | iso_x0.25 | 0.516 (64/64) | 0.500 (48/64 partial) | 0.375 (64/64) | – | – |
| octo-small | iso_x4.0 | 0.625 (64/64) | 0.521 (48/64 partial) | 0.500 (64/64) | – | – |
| octo-small | fric_x0.4 | 0.391 (64/64) | 0.516 (64/64) | 0.484 (64/64) | – | – |
| octo-small | dens_x0.5 | 0.562 (64/64) | 0.479 (48/64 partial) | 0.438 (64/64) | – | – |
| octo-base | nominal | 0.375 (64/64) | 0.453 (64/64) | 0.500 (64/64) | – | – |
| octo-base | force_x0.5 | 0.344 (64/64) | 0.391 (64/64) | 0.453 (64/64) | – | – |
| octo-base | iso_x0.25 | 0.359 (64/64) | 0.438 (48/64 partial) | 0.375 (64/64) | – | – |
| octo-base | iso_x4.0 | 0.328 (64/64) | 0.500 (48/64 partial) | 0.297 (64/64) | – | – |
| octo-base | fric_x0.4 | 0.359 (64/64) | 0.430 (64/64) | 0.469 (64/64) | – | – |
| octo-base | dens_x0.5 | 0.375 (64/64) | 0.417 (48/64 partial) | 0.422 (64/64) | – | – |
| octo-small@hist1 | nominal | 0.344 (64/64) | 0.484 (64/64) | 0.391 (64/64) | – | – |
| octo-small@hist1 | force_x0.5 | 0.406 (64/64) | 0.375 (64/64) | 0.375 (64/64) | – | – |
| octo-small@hist1 | iso_x0.25 | 0.266 (64/64) | 0.312 (48/64 partial) | 0.266 (64/64) | – | – |
| octo-small@hist1 | iso_x4.0 | 0.453 (64/64) | 0.542 (48/64 partial) | 0.406 (64/64) | – | – |
| octo-small@hist1 | fric_x0.4 | 0.328 (64/64) | 0.396 (48/64 partial) | 0.297 (64/64) | – | – |
| octo-small@hist1 | dens_x0.5 | 0.422 (64/64) | 0.375 (48/64 partial) | 0.375 (64/64) | – | – |
| octo-base@hist1 | nominal | 0.344 (64/64) | 0.344 (64/64) | 0.391 (64/64) | – | – |
| octo-base@hist1 | force_x0.5 | 0.344 (64/64) | 0.297 (64/64) | 0.375 (64/64) | – | – |
| octo-base@hist1 | iso_x0.25 | 0.281 (64/64) | 0.292 (48/64 partial) | 0.391 (64/64) | – | – |
| octo-base@hist1 | iso_x4.0 | 0.328 (64/64) | 0.396 (48/64 partial) | 0.406 (64/64) | – | – |
| octo-base@hist1 | fric_x0.4 | 0.359 (64/64) | 0.354 (48/64 partial) | 0.484 (64/64) | – | – |
| octo-base@hist1 | dens_x0.5 | 0.344 (64/64) | 0.396 (48/64 partial) | 0.406 (64/64) | – | – |

## Δ = Octo − OpenVLA on the shared configurations

| pair | condition | seed set | configs compared | census | Δ |
|---|---|---|---:|---|---:|
| octo-small vs OpenVLA | nominal | A' | 64 | complete | +0.359 |
| octo-small vs OpenVLA | nominal | B | 48 | partial | +0.323 |
| octo-small vs OpenVLA | nominal | C | 48 | partial | +0.312 |
| octo-small vs OpenVLA | force_x0.5 | A' | 64 | complete | +0.219 |
| octo-small vs OpenVLA | force_x0.5 | B | 48 | partial | +0.188 |
| octo-small vs OpenVLA | force_x0.5 | C | 48 | partial | -0.021 |
| octo-small vs OpenVLA | iso_x0.25 | A' | 64 | complete | +0.344 |
| octo-small vs OpenVLA | iso_x0.25 | B | 48 | partial | +0.312 |
| octo-small vs OpenVLA | iso_x0.25 | C | 64 | complete | +0.203 |
| octo-small vs OpenVLA | iso_x4.0 | A' | 64 | complete | +0.531 |
| octo-small vs OpenVLA | iso_x4.0 | B | 48 | partial | +0.417 |
| octo-small vs OpenVLA | iso_x4.0 | C | 64 | complete | +0.406 |
| octo-small vs OpenVLA | fric_x0.4 | A' | 64 | complete | +0.344 |
| octo-small vs OpenVLA | fric_x0.4 | B | 64 | complete | +0.469 |
| octo-small vs OpenVLA | fric_x0.4 | C | 64 | complete | +0.438 |
| octo-small vs OpenVLA | dens_x0.5 | A' | 64 | complete | +0.406 |
| octo-small vs OpenVLA | dens_x0.5 | B | 48 | partial | +0.271 |
| octo-small vs OpenVLA | dens_x0.5 | C | 64 | complete | +0.281 |
| octo-base vs OpenVLA | nominal | A' | 64 | complete | +0.219 |
| octo-base vs OpenVLA | nominal | B | 48 | partial | +0.271 |
| octo-base vs OpenVLA | nominal | C | 48 | partial | +0.417 |
| octo-base vs OpenVLA | force_x0.5 | A' | 64 | complete | +0.094 |
| octo-base vs OpenVLA | force_x0.5 | B | 48 | partial | +0.083 |
| octo-base vs OpenVLA | force_x0.5 | C | 48 | partial | +0.125 |
| octo-base vs OpenVLA | iso_x0.25 | A' | 64 | complete | +0.188 |
| octo-base vs OpenVLA | iso_x0.25 | B | 48 | partial | +0.250 |
| octo-base vs OpenVLA | iso_x0.25 | C | 64 | complete | +0.203 |
| octo-base vs OpenVLA | iso_x4.0 | A' | 64 | complete | +0.234 |
| octo-base vs OpenVLA | iso_x4.0 | B | 48 | partial | +0.396 |
| octo-base vs OpenVLA | iso_x4.0 | C | 64 | complete | +0.203 |
| octo-base vs OpenVLA | fric_x0.4 | A' | 64 | complete | +0.312 |
| octo-base vs OpenVLA | fric_x0.4 | B | 64 | complete | +0.383 |
| octo-base vs OpenVLA | fric_x0.4 | C | 64 | complete | +0.422 |
| octo-base vs OpenVLA | dens_x0.5 | A' | 64 | complete | +0.219 |
| octo-base vs OpenVLA | dens_x0.5 | B | 48 | partial | +0.208 |
| octo-base vs OpenVLA | dens_x0.5 | C | 64 | complete | +0.266 |
| octo-small@hist1 vs OpenVLA | nominal | A' | 64 | complete | +0.188 |
| octo-small@hist1 vs OpenVLA | nominal | B | 48 | partial | +0.375 |
| octo-small@hist1 vs OpenVLA | nominal | C | 48 | partial | +0.229 |
| octo-small@hist1 vs OpenVLA | force_x0.5 | A' | 64 | complete | +0.156 |
| octo-small@hist1 vs OpenVLA | force_x0.5 | B | 48 | partial | +0.062 |
| octo-small@hist1 vs OpenVLA | force_x0.5 | C | 48 | partial | +0.021 |
| octo-small@hist1 vs OpenVLA | iso_x0.25 | A' | 64 | complete | +0.094 |
| octo-small@hist1 vs OpenVLA | iso_x0.25 | B | 48 | partial | +0.125 |
| octo-small@hist1 vs OpenVLA | iso_x0.25 | C | 64 | complete | +0.094 |
| octo-small@hist1 vs OpenVLA | iso_x4.0 | A' | 64 | complete | +0.359 |
| octo-small@hist1 vs OpenVLA | iso_x4.0 | B | 48 | partial | +0.438 |
| octo-small@hist1 vs OpenVLA | iso_x4.0 | C | 64 | complete | +0.312 |
| octo-small@hist1 vs OpenVLA | fric_x0.4 | A' | 64 | complete | +0.281 |
| octo-small@hist1 vs OpenVLA | fric_x0.4 | B | 48 | partial | +0.354 |
| octo-small@hist1 vs OpenVLA | fric_x0.4 | C | 64 | complete | +0.250 |
| octo-small@hist1 vs OpenVLA | dens_x0.5 | A' | 64 | complete | +0.266 |
| octo-small@hist1 vs OpenVLA | dens_x0.5 | B | 48 | partial | +0.167 |
| octo-small@hist1 vs OpenVLA | dens_x0.5 | C | 64 | complete | +0.219 |
| octo-base@hist1 vs OpenVLA | nominal | A' | 64 | complete | +0.188 |
| octo-base@hist1 vs OpenVLA | nominal | B | 48 | partial | +0.146 |
| octo-base@hist1 vs OpenVLA | nominal | C | 48 | partial | +0.292 |
| octo-base@hist1 vs OpenVLA | force_x0.5 | A' | 64 | complete | +0.094 |
| octo-base@hist1 vs OpenVLA | force_x0.5 | B | 48 | partial | -0.083 |
| octo-base@hist1 vs OpenVLA | force_x0.5 | C | 48 | partial | +0.042 |
| octo-base@hist1 vs OpenVLA | iso_x0.25 | A' | 64 | complete | +0.109 |
| octo-base@hist1 vs OpenVLA | iso_x0.25 | B | 48 | partial | +0.104 |
| octo-base@hist1 vs OpenVLA | iso_x0.25 | C | 64 | complete | +0.219 |
| octo-base@hist1 vs OpenVLA | iso_x4.0 | A' | 64 | complete | +0.234 |
| octo-base@hist1 vs OpenVLA | iso_x4.0 | B | 48 | partial | +0.292 |
| octo-base@hist1 vs OpenVLA | iso_x4.0 | C | 64 | complete | +0.312 |
| octo-base@hist1 vs OpenVLA | fric_x0.4 | A' | 64 | complete | +0.312 |
| octo-base@hist1 vs OpenVLA | fric_x0.4 | B | 48 | partial | +0.312 |
| octo-base@hist1 vs OpenVLA | fric_x0.4 | C | 64 | complete | +0.438 |
| octo-base@hist1 vs OpenVLA | dens_x0.5 | A' | 64 | complete | +0.188 |
| octo-base@hist1 vs OpenVLA | dens_x0.5 | B | 48 | partial | +0.188 |
| octo-base@hist1 vs OpenVLA | dens_x0.5 | C | 64 | complete | +0.250 |

## Census estimator: Δ with policy-noise interval only

With every configuration enumerated, the configuration-sampling error is zero by construction; the interval below covers only the policy noise of the stochastic policy and the run-to-run noise of the deterministic one, and it shrinks as 1/sqrt(runs). Anything that survives it is not a sampling artefact.

| pair | condition | configs | census | Octo runs / OpenVLA runs | Δ | 95% (policy noise) | decision | variance model |
|---|---|---:|---|---|---:|---|---|---|
| octo-small vs OpenVLA | nominal | 64 | **complete** | 3 / 2 | +0.320 | [+0.245, +0.396] | Octo> | empirical / empirical |
| octo-small vs OpenVLA | force_x0.5 | 64 | **complete** | 3 / 3 | +0.187 | [+0.121, +0.254] | Octo> | empirical / empirical |
| octo-small vs OpenVLA | iso_x0.25 | 64 | **complete** | 3 / 1 | +0.286 | [+0.221, +0.352] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-small vs OpenVLA | iso_x4.0 | 64 | **complete** | 3 / 1 | +0.464 | [+0.405, +0.522] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-small vs OpenVLA | fric_x0.4 | 64 | **complete** | 3 / 1 | +0.417 | [+0.353, +0.480] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-small vs OpenVLA | dens_x0.5 | 64 | **complete** | 3 / 1 | +0.341 | [+0.276, +0.406] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-base vs OpenVLA | nominal | 64 | **complete** | 3 / 2 | +0.286 | [+0.209, +0.364] | Octo> | empirical / empirical |
| octo-base vs OpenVLA | force_x0.5 | 64 | **complete** | 3 / 3 | +0.125 | [+0.054, +0.196] | Octo> | empirical / empirical |
| octo-base vs OpenVLA | iso_x0.25 | 64 | **complete** | 3 / 1 | +0.216 | [+0.151, +0.281] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-base vs OpenVLA | iso_x4.0 | 64 | **complete** | 3 / 1 | +0.271 | [+0.198, +0.344] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-base vs OpenVLA | fric_x0.4 | 64 | **complete** | 3 / 1 | +0.372 | [+0.315, +0.429] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-base vs OpenVLA | dens_x0.5 | 64 | **complete** | 3 / 1 | +0.247 | [+0.176, +0.319] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-small@hist1 vs OpenVLA | nominal | 64 | **complete** | 3 / 2 | +0.250 | [+0.175, +0.325] | Octo> | empirical / empirical |
| octo-small@hist1 vs OpenVLA | force_x0.5 | 64 | **complete** | 3 / 3 | +0.115 | [+0.046, +0.183] | Octo> | empirical / empirical |
| octo-small@hist1 vs OpenVLA | iso_x0.25 | 64 | **complete** | 3 / 1 | +0.099 | [+0.042, +0.156] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-small@hist1 vs OpenVLA | iso_x4.0 | 64 | **complete** | 3 / 1 | +0.362 | [+0.290, +0.434] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-small@hist1 vs OpenVLA | fric_x0.4 | 64 | **complete** | 3 / 1 | +0.286 | [+0.229, +0.344] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-small@hist1 vs OpenVLA | dens_x0.5 | 64 | **complete** | 3 / 1 | +0.237 | [+0.173, +0.301] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-base@hist1 vs OpenVLA | nominal | 64 | **complete** | 3 / 2 | +0.203 | [+0.128, +0.278] | Octo> | empirical / empirical |
| octo-base@hist1 vs OpenVLA | force_x0.5 | 64 | **complete** | 3 / 3 | +0.068 | [-0.000, +0.135] | abstain | empirical / empirical |
| octo-base@hist1 vs OpenVLA | iso_x0.25 | 64 | **complete** | 3 / 1 | +0.141 | [+0.078, +0.203] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-base@hist1 vs OpenVLA | iso_x4.0 | 64 | **complete** | 3 / 1 | +0.273 | [+0.212, +0.335] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-base@hist1 vs OpenVLA | fric_x0.4 | 64 | **complete** | 3 / 1 | +0.354 | [+0.292, +0.416] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-base@hist1 vs OpenVLA | dens_x0.5 | 64 | **complete** | 3 / 1 | +0.214 | [+0.153, +0.274] | Octo> | empirical / single run (run-to-run noise unmeasured) |

## Point calibration vs union bound over the compatible set (census intervals)

Point = the nominal condition alone, the usual practice. Union = the ranking must hold at every calibration-invisible condition, so the interval is [min lower bound, max upper bound] over `force_x0.5`, `iso_x0.25`, `iso_x4.0`, `fric_x0.4`, `dens_x0.5`. A pair where the two disagree is one where point calibration declares a ranking the calibration data cannot support.

| pair | point Δ | point verdict | union interval | union verdict | disagreement |
|---|---:|---|---|---|---|
| octo-small vs OpenVLA | +0.320 | Octo> | [+0.121, +0.522] | Octo> | no |
| octo-base vs OpenVLA | +0.286 | Octo> | [+0.054, +0.429] | Octo> | no |
| octo-small@hist1 vs OpenVLA | +0.250 | Octo> | [+0.042, +0.434] | Octo> | no |
| octo-base@hist1 vs OpenVLA | +0.203 | Octo> | [-0.000, +0.416] | abstain | **yes** |

## Decision change per pair

| pair | nominal | force_x0.5 | iso_x0.25 | iso_x4.0 | fric_x0.4 | dens_x0.5 | change | sign agreement across runs |
|---|---|---|---|---|---|---|---|---|
| octo-small vs OpenVLA | Octo> | Octo> | Octo> | Octo> | Octo> | Octo> | Octo> → Octo> → Octo> → Octo> → Octo> → Octo> | same sign / mixed / same sign / same sign / same sign / same sign |
| octo-base vs OpenVLA | Octo> | Octo> | Octo> | Octo> | Octo> | Octo> | Octo> → Octo> → Octo> → Octo> → Octo> → Octo> | same sign / same sign / same sign / same sign / same sign / same sign |
| octo-small@hist1 vs OpenVLA | Octo> | Octo> | Octo> | Octo> | Octo> | Octo> | Octo> → Octo> → Octo> → Octo> → Octo> → Octo> | same sign / same sign / same sign / same sign / same sign / same sign |
| octo-base@hist1 vs OpenVLA | Octo> | abstain | Octo> | Octo> | Octo> | Octo> | Octo> → abstain → Octo> → Octo> → Octo> → Octo> | same sign / mixed / same sign / same sign / same sign / same sign |
