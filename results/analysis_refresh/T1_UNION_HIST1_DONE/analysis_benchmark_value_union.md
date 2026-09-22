# Benchmark value over the full configuration grid: PutEggplantInBasketScene-v1

The task has **64** initial configurations. A policy's benchmark value is its mean success over all of them. OpenVLA is deterministic, so a complete census is exact; Octo is stochastic, so its remaining error is policy noise, read off the spread across seed sets rather than from an episode bootstrap. A decision is declared only when every seed set agrees in sign on a complete census.

## Coverage and benchmark values

| policy | condition | A' | B | C |
|---|---|---|---|---|
| openvla-7b-4bit | nominal | – | 0.146 (48/64 partial) | 0.146 (48/64 partial) |
| openvla-7b-4bit | force_x0.5 | – | 0.333 (48/64 partial) | 0.375 (48/64 partial) |
| openvla-7b-4bit | iso_x0.25 | – | – | – |
| openvla-7b-4bit | iso_x4.0 | – | – | – |
| openvla-7b-4bit | fric_x0.4 | – | – | – |
| openvla-7b-4bit | dens_x0.5 | – | – | – |
| octo-small | nominal | 0.516 (64/64) | 0.461 (64/64) | 0.453 (64/64) |
| octo-small | force_x0.5 | 0.469 (64/64) | 0.500 (64/64) | 0.406 (64/64) |
| octo-small | iso_x0.25 | 0.516 (64/64) | 0.500 (48/64 partial) | 0.375 (64/64) |
| octo-small | iso_x4.0 | 0.625 (64/64) | 0.521 (48/64 partial) | 0.500 (64/64) |
| octo-small | fric_x0.4 | 0.391 (64/64) | 0.516 (64/64) | 0.484 (64/64) |
| octo-small | dens_x0.5 | 0.562 (64/64) | 0.479 (48/64 partial) | 0.438 (64/64) |
| octo-base | nominal | 0.375 (64/64) | 0.453 (64/64) | 0.500 (64/64) |
| octo-base | force_x0.5 | 0.344 (64/64) | 0.391 (64/64) | 0.453 (64/64) |
| octo-base | iso_x0.25 | 0.359 (64/64) | 0.438 (48/64 partial) | 0.375 (64/64) |
| octo-base | iso_x4.0 | 0.328 (64/64) | 0.500 (48/64 partial) | 0.297 (64/64) |
| octo-base | fric_x0.4 | 0.359 (64/64) | 0.430 (64/64) | 0.469 (64/64) |
| octo-base | dens_x0.5 | 0.375 (64/64) | 0.417 (48/64 partial) | 0.422 (64/64) |
| octo-small@hist1 | nominal | 0.344 (64/64) | 0.484 (64/64) | 0.391 (64/64) |
| octo-small@hist1 | force_x0.5 | 0.406 (64/64) | 0.375 (64/64) | 0.375 (64/64) |
| octo-small@hist1 | iso_x0.25 | 0.266 (64/64) | 0.312 (48/64 partial) | 0.266 (64/64) |
| octo-small@hist1 | iso_x4.0 | 0.453 (64/64) | 0.542 (48/64 partial) | 0.406 (64/64) |
| octo-small@hist1 | fric_x0.4 | 0.328 (64/64) | 0.396 (48/64 partial) | 0.297 (64/64) |
| octo-small@hist1 | dens_x0.5 | 0.422 (64/64) | 0.375 (48/64 partial) | 0.375 (64/64) |
| octo-base@hist1 | nominal | 0.344 (64/64) | 0.344 (64/64) | 0.391 (64/64) |
| octo-base@hist1 | force_x0.5 | 0.344 (64/64) | 0.297 (64/64) | 0.375 (64/64) |
| octo-base@hist1 | iso_x0.25 | 0.281 (64/64) | 0.292 (48/64 partial) | 0.391 (64/64) |
| octo-base@hist1 | iso_x4.0 | 0.328 (64/64) | 0.396 (48/64 partial) | 0.406 (64/64) |
| octo-base@hist1 | fric_x0.4 | 0.359 (64/64) | 0.354 (48/64 partial) | 0.484 (64/64) |
| octo-base@hist1 | dens_x0.5 | 0.344 (64/64) | 0.396 (48/64 partial) | 0.406 (64/64) |

## Δ = Octo − OpenVLA on the shared configurations

| pair | condition | seed set | configs compared | census | Δ |
|---|---|---|---:|---|---:|
| octo-small vs OpenVLA | nominal | A' | 48 | partial | +0.354 |
| octo-small vs OpenVLA | nominal | B | 48 | partial | +0.323 |
| octo-small vs OpenVLA | nominal | C | 48 | partial | +0.312 |
| octo-small vs OpenVLA | force_x0.5 | A' | 48 | partial | +0.146 |
| octo-small vs OpenVLA | force_x0.5 | B | 48 | partial | +0.188 |
| octo-small vs OpenVLA | force_x0.5 | C | 48 | partial | -0.021 |
| octo-base vs OpenVLA | nominal | A' | 48 | partial | +0.229 |
| octo-base vs OpenVLA | nominal | B | 48 | partial | +0.271 |
| octo-base vs OpenVLA | nominal | C | 48 | partial | +0.417 |
| octo-base vs OpenVLA | force_x0.5 | A' | 48 | partial | -0.021 |
| octo-base vs OpenVLA | force_x0.5 | B | 48 | partial | +0.083 |
| octo-base vs OpenVLA | force_x0.5 | C | 48 | partial | +0.125 |
| octo-small@hist1 vs OpenVLA | nominal | A' | 48 | partial | +0.188 |
| octo-small@hist1 vs OpenVLA | nominal | B | 48 | partial | +0.375 |
| octo-small@hist1 vs OpenVLA | nominal | C | 48 | partial | +0.229 |
| octo-small@hist1 vs OpenVLA | force_x0.5 | A' | 48 | partial | +0.083 |
| octo-small@hist1 vs OpenVLA | force_x0.5 | B | 48 | partial | +0.062 |
| octo-small@hist1 vs OpenVLA | force_x0.5 | C | 48 | partial | +0.021 |
| octo-base@hist1 vs OpenVLA | nominal | A' | 48 | partial | +0.250 |
| octo-base@hist1 vs OpenVLA | nominal | B | 48 | partial | +0.146 |
| octo-base@hist1 vs OpenVLA | nominal | C | 48 | partial | +0.292 |
| octo-base@hist1 vs OpenVLA | force_x0.5 | A' | 48 | partial | +0.021 |
| octo-base@hist1 vs OpenVLA | force_x0.5 | B | 48 | partial | -0.083 |
| octo-base@hist1 vs OpenVLA | force_x0.5 | C | 48 | partial | +0.042 |

## Census estimator: Δ with policy-noise interval only

With every configuration enumerated, the configuration-sampling error is zero by construction; the interval below covers only the policy noise of the stochastic policy and the run-to-run noise of the deterministic one, and it shrinks as 1/sqrt(runs). Anything that survives it is not a sampling artefact.

| pair | condition | configs | census | Octo runs / OpenVLA runs | Δ | 95% (policy noise) | decision | variance model |
|---|---|---:|---|---|---:|---|---|---|
| octo-small vs OpenVLA | nominal | 48 | partial | 3 / 1 | +0.330 | [+0.264, +0.395] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-small vs OpenVLA | force_x0.5 | 48 | partial | 3 / 2 | +0.097 | [+0.026, +0.169] | Octo> | empirical / empirical |
| octo-base vs OpenVLA | nominal | 48 | partial | 3 / 1 | +0.306 | [+0.238, +0.373] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-base vs OpenVLA | force_x0.5 | 48 | partial | 3 / 2 | +0.056 | [-0.023, +0.134] | abstain | empirical / empirical |
| octo-small@hist1 vs OpenVLA | nominal | 48 | partial | 3 / 1 | +0.264 | [+0.199, +0.329] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-small@hist1 vs OpenVLA | force_x0.5 | 48 | partial | 3 / 2 | +0.049 | [-0.027, +0.124] | abstain | empirical / empirical |
| octo-base@hist1 vs OpenVLA | nominal | 48 | partial | 3 / 1 | +0.229 | [+0.167, +0.292] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-base@hist1 vs OpenVLA | force_x0.5 | 48 | partial | 3 / 2 | -0.014 | [-0.090, +0.063] | abstain | empirical / empirical |

## Point calibration vs union bound over the compatible set (census intervals)

Point = the nominal condition alone, the usual practice. Union = the ranking must hold at every calibration-invisible condition, so the interval is [min lower bound, max upper bound] over `force_x0.5`, `iso_x0.25`, `iso_x4.0`, `fric_x0.4`, `dens_x0.5`. A pair where the two disagree is one where point calibration declares a ranking the calibration data cannot support.

| pair | point Δ | point verdict | union interval | union verdict | disagreement |
|---|---:|---|---|---|---|
| octo-small vs OpenVLA | +0.330 | Octo> | [+0.026, +0.169] | Octo> | no |
| octo-base vs OpenVLA | +0.306 | Octo> | [-0.023, +0.134] | abstain | **yes** |
| octo-small@hist1 vs OpenVLA | +0.264 | Octo> | [-0.027, +0.124] | abstain | **yes** |
| octo-base@hist1 vs OpenVLA | +0.229 | Octo> | [-0.090, +0.063] | abstain | **yes** |

## Decision change per pair

| pair | nominal | force_x0.5 | iso_x0.25 | iso_x4.0 | fric_x0.4 | dens_x0.5 | change | sign agreement across runs |
|---|---|---|---|---|---|---|---|---|
| octo-small vs OpenVLA | Octo> | Octo> | – | – | – | – | Octo> → Octo> → – → – → – → – | same sign / mixed / – / – / – / – |
| octo-base vs OpenVLA | Octo> | abstain | – | – | – | – | Octo> → abstain → – → – → – → – | same sign / mixed / – / – / – / – |
| octo-small@hist1 vs OpenVLA | Octo> | abstain | – | – | – | – | Octo> → abstain → – → – → – → – | same sign / same sign / – / – / – / – |
| octo-base@hist1 vs OpenVLA | Octo> | abstain | – | – | – | – | Octo> → abstain → – → – → – → – | same sign / mixed / – / – / – / – |
