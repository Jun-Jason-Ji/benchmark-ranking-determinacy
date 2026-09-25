# Benchmark value over the full configuration grid: PutCarrotOnPlateInScene-v1

The task has **24** initial configurations. A policy's benchmark value is its mean success over all of them. OpenVLA is deterministic, so a complete census is exact; Octo is stochastic, so its remaining error is policy noise, read off the spread across seed sets rather than from an episode bootstrap. A decision is declared only when every seed set agrees in sign on a complete census.

Sources are chosen per policy family: Octo uses the post-fix inference-server generation (A′ = `controller_sweep_gpu_replayA`, B, C), while OpenVLA, whose server is one unchanged Windows process throughout, uses its original directory in the first column (A = `controller_sweep_gpu`), where its complete census lives.

## Coverage and benchmark values

| policy | condition | A' | B | C | D | E |
|---|---|---|---|---|---|---|
| openvla-7b-4bit | nominal | 0.042 (24/24) | – | – | – | – |
| openvla-7b-4bit | force_x0.5 | 0.042 (24/24) | – | – | – | – |
| openvla-7b-4bit | iso_x0.25 | 0.083 (24/24) | – | – | – | – |
| openvla-7b-4bit | iso_x4.0 | 0.042 (24/24) | – | – | – | – |
| openvla-7b-4bit | fric_x0.4 | 0.000 (24/24) | – | – | – | – |
| openvla-7b-4bit | dens_x0.5 | 0.042 (24/24) | – | – | – | – |
| octo-small | nominal | 0.125 (24/24) | – | 0.042 (24/24) | – | – |
| octo-small | force_x0.5 | 0.125 (24/24) | – | 0.042 (24/24) | – | – |
| octo-small | iso_x0.25 | 0.042 (24/24) | – | 0.125 (24/24) | – | – |
| octo-small | iso_x4.0 | 0.125 (24/24) | – | 0.083 (24/24) | – | – |
| octo-small | fric_x0.4 | 0.083 (24/24) | – | 0.042 (24/24) | – | – |
| octo-small | dens_x0.5 | 0.083 (24/24) | – | 0.083 (24/24) | – | – |
| octo-base | nominal | 0.125 (24/24) | – | 0.125 (24/24) | – | – |
| octo-base | force_x0.5 | 0.167 (24/24) | – | 0.208 (24/24) | – | – |
| octo-base | iso_x0.25 | 0.125 (24/24) | – | 0.208 (24/24) | – | – |
| octo-base | iso_x4.0 | 0.125 (24/24) | – | 0.167 (24/24) | – | – |
| octo-base | fric_x0.4 | 0.083 (24/24) | – | 0.167 (24/24) | – | – |
| octo-base | dens_x0.5 | 0.083 (24/24) | – | 0.167 (24/24) | – | – |
| octo-small@hist1 | nominal | – | – | – | – | – |
| octo-small@hist1 | force_x0.5 | – | – | – | – | – |
| octo-small@hist1 | iso_x0.25 | – | – | – | – | – |
| octo-small@hist1 | iso_x4.0 | – | – | – | – | – |
| octo-small@hist1 | fric_x0.4 | – | – | – | – | – |
| octo-small@hist1 | dens_x0.5 | – | – | – | – | – |
| octo-base@hist1 | nominal | – | – | – | – | – |
| octo-base@hist1 | force_x0.5 | – | – | – | – | – |
| octo-base@hist1 | iso_x0.25 | – | – | – | – | – |
| octo-base@hist1 | iso_x4.0 | – | – | – | – | – |
| octo-base@hist1 | fric_x0.4 | – | – | – | – | – |
| octo-base@hist1 | dens_x0.5 | – | – | – | – | – |

## Δ = Octo − OpenVLA on the shared configurations

| pair | condition | seed set | configs compared | census | Δ |
|---|---|---|---:|---|---:|
| octo-small vs OpenVLA | nominal | A' | 24 | complete | +0.083 |
| octo-small vs OpenVLA | nominal | C | 24 | complete | +0.000 |
| octo-small vs OpenVLA | force_x0.5 | A' | 24 | complete | +0.083 |
| octo-small vs OpenVLA | force_x0.5 | C | 24 | complete | +0.000 |
| octo-small vs OpenVLA | iso_x0.25 | A' | 24 | complete | -0.042 |
| octo-small vs OpenVLA | iso_x0.25 | C | 24 | complete | +0.042 |
| octo-small vs OpenVLA | iso_x4.0 | A' | 24 | complete | +0.083 |
| octo-small vs OpenVLA | iso_x4.0 | C | 24 | complete | +0.042 |
| octo-small vs OpenVLA | fric_x0.4 | A' | 24 | complete | +0.083 |
| octo-small vs OpenVLA | fric_x0.4 | C | 24 | complete | +0.042 |
| octo-small vs OpenVLA | dens_x0.5 | A' | 24 | complete | +0.042 |
| octo-small vs OpenVLA | dens_x0.5 | C | 24 | complete | +0.042 |
| octo-base vs OpenVLA | nominal | A' | 24 | complete | +0.083 |
| octo-base vs OpenVLA | nominal | C | 24 | complete | +0.083 |
| octo-base vs OpenVLA | force_x0.5 | A' | 24 | complete | +0.125 |
| octo-base vs OpenVLA | force_x0.5 | C | 24 | complete | +0.167 |
| octo-base vs OpenVLA | iso_x0.25 | A' | 24 | complete | +0.042 |
| octo-base vs OpenVLA | iso_x0.25 | C | 24 | complete | +0.125 |
| octo-base vs OpenVLA | iso_x4.0 | A' | 24 | complete | +0.083 |
| octo-base vs OpenVLA | iso_x4.0 | C | 24 | complete | +0.125 |
| octo-base vs OpenVLA | fric_x0.4 | A' | 24 | complete | +0.083 |
| octo-base vs OpenVLA | fric_x0.4 | C | 24 | complete | +0.167 |
| octo-base vs OpenVLA | dens_x0.5 | A' | 24 | complete | +0.042 |
| octo-base vs OpenVLA | dens_x0.5 | C | 24 | complete | +0.125 |

## Census estimator: Δ with policy-noise interval only

With every configuration enumerated, the configuration-sampling error is zero by construction; the interval below covers only the policy noise of the stochastic policy and the run-to-run noise of the deterministic one, and it shrinks as 1/sqrt(runs). Anything that survives it is not a sampling artefact.

| pair | condition | configs | census | Octo runs / OpenVLA runs | Δ | 95% (policy noise) | decision | variance model |
|---|---|---:|---|---|---:|---|---|---|
| octo-small vs OpenVLA | nominal | 24 | **complete** | 2 / 1 | +0.042 | [-0.016, +0.099] | abstain | empirical / single run (run-to-run noise unmeasured) |
| octo-small vs OpenVLA | force_x0.5 | 24 | **complete** | 2 / 1 | +0.042 | [-0.016, +0.099] | abstain | empirical / single run (run-to-run noise unmeasured) |
| octo-small vs OpenVLA | iso_x0.25 | 24 | **complete** | 2 / 1 | +0.000 | [-0.058, +0.058] | abstain | empirical / single run (run-to-run noise unmeasured) |
| octo-small vs OpenVLA | iso_x4.0 | 24 | **complete** | 2 / 1 | +0.062 | [+0.022, +0.103] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-small vs OpenVLA | fric_x0.4 | 24 | **complete** | 2 / 1 | +0.062 | [+0.022, +0.103] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-small vs OpenVLA | dens_x0.5 | 24 | **complete** | 2 / 1 | +0.042 | [-0.040, +0.123] | abstain | empirical / single run (run-to-run noise unmeasured) |
| octo-base vs OpenVLA | nominal | 24 | **complete** | 2 / 1 | +0.083 | [+0.026, +0.141] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-base vs OpenVLA | force_x0.5 | 24 | **complete** | 2 / 1 | +0.146 | [+0.075, +0.217] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-base vs OpenVLA | iso_x0.25 | 24 | **complete** | 2 / 1 | +0.083 | [-0.017, +0.183] | abstain | empirical / single run (run-to-run noise unmeasured) |
| octo-base vs OpenVLA | iso_x4.0 | 24 | **complete** | 2 / 1 | +0.104 | [+0.013, +0.195] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-base vs OpenVLA | fric_x0.4 | 24 | **complete** | 2 / 1 | +0.125 | [+0.043, +0.207] | Octo> | empirical / single run (run-to-run noise unmeasured) |
| octo-base vs OpenVLA | dens_x0.5 | 24 | **complete** | 2 / 1 | +0.083 | [+0.002, +0.165] | Octo> | empirical / single run (run-to-run noise unmeasured) |

## Point calibration vs union bound over the compatible set (census intervals)

Point = the nominal condition alone, the usual practice. Union = the ranking must hold at every calibration-invisible condition, so the interval is [min lower bound, max upper bound] over `force_x0.5`, `iso_x0.25`, `iso_x4.0`, `fric_x0.4`, `dens_x0.5`. A pair where the two disagree is one where point calibration declares a ranking the calibration data cannot support.

| pair | point Δ | point verdict | union interval | union verdict | disagreement |
|---|---:|---|---|---|---|
| octo-small vs OpenVLA | +0.042 | abstain | [-0.058, +0.123] | abstain | no |
| octo-base vs OpenVLA | +0.083 | Octo> | [-0.017, +0.217] | abstain | **yes** |

## Decision change per pair

| pair | nominal | force_x0.5 | iso_x0.25 | iso_x4.0 | fric_x0.4 | dens_x0.5 | change | sign agreement across runs |
|---|---|---|---|---|---|---|---|---|
| octo-small vs OpenVLA | abstain | abstain | abstain | Octo> | Octo> | abstain | abstain → abstain → abstain → Octo> → Octo> → abstain | mixed / mixed / mixed / same sign / same sign / same sign |
| octo-base vs OpenVLA | Octo> | Octo> | abstain | Octo> | Octo> | Octo> | Octo> → Octo> → abstain → Octo> → Octo> → Octo> | same sign / same sign / same sign / same sign / same sign / same sign |
| octo-small@hist1 vs OpenVLA | – | – | – | – | – | – | – → – → – → – → – → – | – / – / – / – / – / – |
| octo-base@hist1 vs OpenVLA | – | – | – | – | – | – | – → – → – → – → – → – | – / – / – / – / – / – |
