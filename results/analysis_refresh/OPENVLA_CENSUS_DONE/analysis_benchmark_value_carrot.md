# Benchmark value over the full configuration grid: PutCarrotOnPlateInScene-v1

The task has **24** initial configurations. A policy's benchmark value is its mean success over all of them. OpenVLA is deterministic, so a complete census is exact; Octo is stochastic, so its remaining error is policy noise, read off the spread across seed sets rather than from an episode bootstrap. A decision is declared only when every seed set agrees in sign on a complete census.

## Coverage and benchmark values

| policy | condition | A' | B | C |
|---|---|---|---|---|
| openvla-7b-4bit | nominal | – | – | – |
| openvla-7b-4bit | force_x0.5 | – | – | – |
| openvla-7b-4bit | iso_x0.25 | – | – | – |
| openvla-7b-4bit | iso_x4.0 | – | – | – |
| openvla-7b-4bit | fric_x0.4 | – | – | – |
| openvla-7b-4bit | dens_x0.5 | – | – | – |
| octo-small | nominal | 0.125 (24/24) | – | 0.042 (24/24) |
| octo-small | force_x0.5 | 0.125 (24/24) | – | 0.042 (24/24) |
| octo-small | iso_x0.25 | 0.042 (24/24) | – | 0.125 (24/24) |
| octo-small | iso_x4.0 | 0.125 (24/24) | – | 0.083 (24/24) |
| octo-small | fric_x0.4 | 0.083 (24/24) | – | 0.042 (24/24) |
| octo-small | dens_x0.5 | 0.083 (24/24) | – | 0.083 (24/24) |
| octo-base | nominal | 0.125 (24/24) | – | 0.125 (24/24) |
| octo-base | force_x0.5 | 0.167 (24/24) | – | 0.208 (24/24) |
| octo-base | iso_x0.25 | 0.125 (24/24) | – | 0.208 (24/24) |
| octo-base | iso_x4.0 | 0.125 (24/24) | – | 0.167 (24/24) |
| octo-base | fric_x0.4 | 0.083 (24/24) | – | 0.167 (24/24) |
| octo-base | dens_x0.5 | 0.083 (24/24) | – | 0.167 (24/24) |
| octo-small@hist1 | nominal | – | – | – |
| octo-small@hist1 | force_x0.5 | – | – | – |
| octo-small@hist1 | iso_x0.25 | – | – | – |
| octo-small@hist1 | iso_x4.0 | – | – | – |
| octo-small@hist1 | fric_x0.4 | – | – | – |
| octo-small@hist1 | dens_x0.5 | – | – | – |
| octo-base@hist1 | nominal | – | – | – |
| octo-base@hist1 | force_x0.5 | – | – | – |
| octo-base@hist1 | iso_x0.25 | – | – | – |
| octo-base@hist1 | iso_x4.0 | – | – | – |
| octo-base@hist1 | fric_x0.4 | – | – | – |
| octo-base@hist1 | dens_x0.5 | – | – | – |

## Δ = Octo − OpenVLA on the shared configurations

| pair | condition | seed set | configs compared | census | Δ |
|---|---|---|---:|---|---:|

## Census estimator: Δ with policy-noise interval only

With every configuration enumerated, the configuration-sampling error is zero by construction; the interval below covers only the policy noise of the stochastic policy and the run-to-run noise of the deterministic one, and it shrinks as 1/sqrt(runs). Anything that survives it is not a sampling artefact.

| pair | condition | configs | census | Octo runs / OpenVLA runs | Δ | 95% (policy noise) | decision | variance model |
|---|---|---:|---|---|---:|---|---|---|

## Point calibration vs union bound over the compatible set (census intervals)

Point = the nominal condition alone, the usual practice. Union = the ranking must hold at every calibration-invisible condition, so the interval is [min lower bound, max upper bound] over `force_x0.5`, `iso_x0.25`, `iso_x4.0`, `fric_x0.4`, `dens_x0.5`. A pair where the two disagree is one where point calibration declares a ranking the calibration data cannot support.

| pair | point Δ | point verdict | union interval | union verdict | disagreement |
|---|---:|---|---|---|---|

## Decision change per pair

| pair | nominal | force_x0.5 | iso_x0.25 | iso_x4.0 | fric_x0.4 | dens_x0.5 | change | sign agreement across runs |
|---|---|---|---|---|---|---|---|---|
| octo-small vs OpenVLA | – | – | – | – | – | – | – → – → – → – → – → – | – / – / – / – / – / – |
| octo-base vs OpenVLA | – | – | – | – | – | – | – → – → – → – → – → – | – / – / – / – / – / – |
| octo-small@hist1 vs OpenVLA | – | – | – | – | – | – | – → – → – → – → – → – | – / – / – / – / – / – |
| octo-base@hist1 vs OpenVLA | – | – | – | – | – | – | – → – → – → – → – → – | – / – / – / – / – / – |
