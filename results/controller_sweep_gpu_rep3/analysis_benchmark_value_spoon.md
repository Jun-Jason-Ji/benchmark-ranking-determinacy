# Benchmark value over the full configuration grid: PutSpoonOnTableClothInScene-v1

The task has **24** initial configurations. A policy's benchmark value is its mean success over all of them. OpenVLA is deterministic, so a complete census is exact; Octo is stochastic, so its remaining error is policy noise, read off the spread across seed sets rather than from an episode bootstrap. A decision is declared only when every seed set agrees in sign on a complete census.

## Coverage and benchmark values

| policy | condition | A | B | C |
|---|---|---|---|---|
| openvla-7b-4bit | nominal | 0.000 (24/24) | – | – |
| openvla-7b-4bit | force_x0.5 | 0.000 (24/24) | – | – |
| openvla-7b-4bit | iso_x0.25 | 0.000 (24/24) | – | – |
| openvla-7b-4bit | iso_x4.0 | 0.000 (24/24) | – | – |
| openvla-7b-4bit | fric_x0.4 | 0.000 (24/24) | – | – |
| openvla-7b-4bit | dens_x0.5 | 0.000 (24/24) | – | – |
| octo-small | nominal | 0.312 (24/24) | – | – |
| octo-small | force_x0.5 | 0.302 (24/24) | – | – |
| octo-small | iso_x0.25 | 0.281 (24/24) | – | – |
| octo-small | iso_x4.0 | 0.354 (24/24) | – | – |
| octo-small | fric_x0.4 | 0.198 (24/24) | – | – |
| octo-small | dens_x0.5 | 0.344 (24/24) | – | – |
| octo-base | nominal | 0.083 (24/24) | – | – |
| octo-base | force_x0.5 | 0.104 (24/24) | – | – |
| octo-base | iso_x0.25 | 0.021 (24/24) | – | – |
| octo-base | iso_x4.0 | 0.062 (24/24) | – | – |
| octo-base | fric_x0.4 | 0.083 (24/24) | – | – |
| octo-base | dens_x0.5 | 0.042 (24/24) | – | – |
| octo-small@hist1 | nominal | 0.312 (24/24) | – | – |
| octo-small@hist1 | force_x0.5 | 0.240 (24/24) | – | – |
| octo-small@hist1 | iso_x0.25 | 0.240 (24/24) | – | – |
| octo-small@hist1 | iso_x4.0 | 0.292 (24/24) | – | – |
| octo-small@hist1 | fric_x0.4 | 0.198 (24/24) | – | – |
| octo-small@hist1 | dens_x0.5 | 0.219 (24/24) | – | – |
| octo-base@hist1 | nominal | 0.167 (24/24) | – | – |
| octo-base@hist1 | force_x0.5 | 0.125 (24/24) | – | – |
| octo-base@hist1 | iso_x0.25 | 0.167 (24/24) | – | – |
| octo-base@hist1 | iso_x4.0 | 0.292 (24/24) | – | – |
| octo-base@hist1 | fric_x0.4 | 0.208 (24/24) | – | – |
| octo-base@hist1 | dens_x0.5 | 0.208 (24/24) | – | – |

## Δ = Octo − OpenVLA on the shared configurations

| pair | condition | seed set | configs compared | census | Δ |
|---|---|---|---:|---|---:|
| octo-small vs OpenVLA | nominal | A | 24 | complete | +0.312 |
| octo-small vs OpenVLA | force_x0.5 | A | 24 | complete | +0.302 |
| octo-small vs OpenVLA | iso_x0.25 | A | 24 | complete | +0.281 |
| octo-small vs OpenVLA | iso_x4.0 | A | 24 | complete | +0.354 |
| octo-small vs OpenVLA | fric_x0.4 | A | 24 | complete | +0.198 |
| octo-small vs OpenVLA | dens_x0.5 | A | 24 | complete | +0.344 |
| octo-base vs OpenVLA | nominal | A | 24 | complete | +0.083 |
| octo-base vs OpenVLA | force_x0.5 | A | 24 | complete | +0.104 |
| octo-base vs OpenVLA | iso_x0.25 | A | 24 | complete | +0.021 |
| octo-base vs OpenVLA | iso_x4.0 | A | 24 | complete | +0.062 |
| octo-base vs OpenVLA | fric_x0.4 | A | 24 | complete | +0.083 |
| octo-base vs OpenVLA | dens_x0.5 | A | 24 | complete | +0.042 |
| octo-small@hist1 vs OpenVLA | nominal | A | 24 | complete | +0.312 |
| octo-small@hist1 vs OpenVLA | force_x0.5 | A | 24 | complete | +0.240 |
| octo-small@hist1 vs OpenVLA | iso_x0.25 | A | 24 | complete | +0.240 |
| octo-small@hist1 vs OpenVLA | iso_x4.0 | A | 24 | complete | +0.292 |
| octo-small@hist1 vs OpenVLA | fric_x0.4 | A | 24 | complete | +0.198 |
| octo-small@hist1 vs OpenVLA | dens_x0.5 | A | 24 | complete | +0.219 |
| octo-base@hist1 vs OpenVLA | nominal | A | 24 | complete | +0.167 |
| octo-base@hist1 vs OpenVLA | force_x0.5 | A | 24 | complete | +0.125 |
| octo-base@hist1 vs OpenVLA | iso_x0.25 | A | 24 | complete | +0.167 |
| octo-base@hist1 vs OpenVLA | iso_x4.0 | A | 24 | complete | +0.292 |
| octo-base@hist1 vs OpenVLA | fric_x0.4 | A | 24 | complete | +0.208 |
| octo-base@hist1 vs OpenVLA | dens_x0.5 | A | 24 | complete | +0.208 |

## Census estimator: Δ with policy-noise interval only

With every configuration enumerated, the configuration-sampling error is zero by construction; the interval below covers only the policy noise of the stochastic policy and the run-to-run noise of the deterministic one, and it shrinks as 1/sqrt(runs). Anything that survives it is not a sampling artefact.

| pair | condition | configs | census | Octo runs / OpenVLA runs | Δ | 95% (policy noise) | decision | variance model |
|---|---|---:|---|---|---:|---|---|---|
| octo-small vs OpenVLA | nominal | 24 | **complete** | 1 / 1 | +0.312 | [+0.127, +0.498] | Octo> | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |
| octo-small vs OpenVLA | force_x0.5 | 24 | **complete** | 1 / 1 | +0.302 | [+0.118, +0.486] | Octo> | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |
| octo-small vs OpenVLA | iso_x0.25 | 24 | **complete** | 1 / 1 | +0.281 | [+0.101, +0.461] | Octo> | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |
| octo-small vs OpenVLA | iso_x4.0 | 24 | **complete** | 1 / 1 | +0.354 | [+0.163, +0.546] | Octo> | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |
| octo-small vs OpenVLA | fric_x0.4 | 24 | **complete** | 1 / 1 | +0.198 | [+0.039, +0.357] | Octo> | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |
| octo-small vs OpenVLA | dens_x0.5 | 24 | **complete** | 1 / 1 | +0.344 | [+0.154, +0.534] | Octo> | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |
| octo-base vs OpenVLA | nominal | 24 | **complete** | 1 / 1 | +0.083 | [-0.027, +0.194] | abstain | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |
| octo-base vs OpenVLA | force_x0.5 | 24 | **complete** | 1 / 1 | +0.104 | [-0.018, +0.226] | abstain | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |
| octo-base vs OpenVLA | iso_x0.25 | 24 | **complete** | 1 / 1 | +0.021 | [-0.036, +0.078] | abstain | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |
| octo-base vs OpenVLA | iso_x4.0 | 24 | **complete** | 1 / 1 | +0.062 | [-0.034, +0.159] | abstain | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |
| octo-base vs OpenVLA | fric_x0.4 | 24 | **complete** | 1 / 1 | +0.083 | [-0.027, +0.194] | abstain | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |
| octo-base vs OpenVLA | dens_x0.5 | 24 | **complete** | 1 / 1 | +0.042 | [-0.038, +0.122] | abstain | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |
| octo-small@hist1 vs OpenVLA | nominal | 24 | **complete** | 1 / 1 | +0.312 | [+0.127, +0.498] | Octo> | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |
| octo-small@hist1 vs OpenVLA | force_x0.5 | 24 | **complete** | 1 / 1 | +0.240 | [+0.069, +0.410] | Octo> | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |
| octo-small@hist1 vs OpenVLA | iso_x0.25 | 24 | **complete** | 1 / 1 | +0.240 | [+0.069, +0.410] | Octo> | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |
| octo-small@hist1 vs OpenVLA | iso_x4.0 | 24 | **complete** | 1 / 1 | +0.292 | [+0.110, +0.474] | Octo> | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |
| octo-small@hist1 vs OpenVLA | fric_x0.4 | 24 | **complete** | 1 / 1 | +0.198 | [+0.039, +0.357] | Octo> | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |
| octo-small@hist1 vs OpenVLA | dens_x0.5 | 24 | **complete** | 1 / 1 | +0.219 | [+0.053, +0.384] | Octo> | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |
| octo-base@hist1 vs OpenVLA | nominal | 24 | **complete** | 1 / 1 | +0.167 | [+0.018, +0.316] | Octo> | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |
| octo-base@hist1 vs OpenVLA | force_x0.5 | 24 | **complete** | 1 / 1 | +0.125 | [-0.007, +0.257] | abstain | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |
| octo-base@hist1 vs OpenVLA | iso_x0.25 | 24 | **complete** | 1 / 1 | +0.167 | [+0.018, +0.316] | Octo> | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |
| octo-base@hist1 vs OpenVLA | iso_x4.0 | 24 | **complete** | 1 / 1 | +0.292 | [+0.110, +0.474] | Octo> | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |
| octo-base@hist1 vs OpenVLA | fric_x0.4 | 24 | **complete** | 1 / 1 | +0.208 | [+0.046, +0.371] | Octo> | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |
| octo-base@hist1 vs OpenVLA | dens_x0.5 | 24 | **complete** | 1 / 1 | +0.208 | [+0.046, +0.371] | Octo> | binomial fallback (1 run/config) / single run (run-to-run noise unmeasured) |

## Point calibration vs union bound over the compatible set (census intervals)

Point = the nominal condition alone, the usual practice. Union = the ranking must hold at every calibration-invisible condition, so the interval is [min lower bound, max upper bound] over `force_x0.5`, `iso_x0.25`, `iso_x4.0`, `fric_x0.4`, `dens_x0.5`. A pair where the two disagree is one where point calibration declares a ranking the calibration data cannot support.

| pair | point Δ | point verdict | union interval | union verdict | disagreement |
|---|---:|---|---|---|---|
| octo-small vs OpenVLA | +0.312 | Octo> | [+0.039, +0.546] | Octo> | no |
| octo-base vs OpenVLA | +0.083 | abstain | [-0.038, +0.226] | abstain | no |
| octo-small@hist1 vs OpenVLA | +0.312 | Octo> | [+0.039, +0.474] | Octo> | no |
| octo-base@hist1 vs OpenVLA | +0.167 | Octo> | [-0.007, +0.474] | abstain | **yes** |

## Decision change per pair

| pair | nominal | force_x0.5 | iso_x0.25 | iso_x4.0 | fric_x0.4 | dens_x0.5 | change | sign agreement across runs |
|---|---|---|---|---|---|---|---|---|
| octo-small vs OpenVLA | Octo> | Octo> | Octo> | Octo> | Octo> | Octo> | Octo> → Octo> → Octo> → Octo> → Octo> → Octo> | same sign / same sign / same sign / same sign / same sign / same sign |
| octo-base vs OpenVLA | abstain | abstain | abstain | abstain | abstain | abstain | abstain → abstain → abstain → abstain → abstain → abstain | same sign / same sign / same sign / same sign / same sign / same sign |
| octo-small@hist1 vs OpenVLA | Octo> | Octo> | Octo> | Octo> | Octo> | Octo> | Octo> → Octo> → Octo> → Octo> → Octo> → Octo> | same sign / same sign / same sign / same sign / same sign / same sign |
| octo-base@hist1 vs OpenVLA | Octo> | abstain | Octo> | Octo> | Octo> | Octo> | Octo> → abstain → Octo> → Octo> → Octo> → Octo> | same sign / same sign / same sign / same sign / same sign / same sign |
