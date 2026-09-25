# Replay-distance provenance and metric correction

Audit date: 24 September 2026. This is a read-only remeasurement of the frozen replay arrays; no simulation or new robot experiment was run. The manuscript was not edited by this audit.

## Finding and disposition

**P1: two distinctions had been lost in prose: the tested scaling range and the definition of position difference.** The historical checker, `scripts/check_iso_invariance.py`, computes `np.abs(ta - tb).max()`, the maximum absolute coordinate difference. It does not compute the Euclidean position distance. The 0.5–2 grids on both stacks also do not establish a measurement over 0.25–4. The latter range has a separate sweep on the original ManiSkill2 stack only.

This recheck uses a single, explicit geometric metric throughout: for matched demonstration trajectories under two settings, take the Euclidean norm of the three-coordinate position difference at each stored time step, then maximize over time, demonstrations, and the eligible setting pairs. These are differences **between replayed simulation trajectories**, not errors against the real demonstration. Coordinates are stored in metres. No interpolation between measured settings, continuous-parameter bound, rotation-distance bound, or unrecorded-state claim is implied.

The corrected maxima remain small and do not change the qualitative observation of replay insensitivity in these measured designs. The numerical and scope errors are nevertheless substantive reproducibility corrections and should be recorded as such.

## Exact remeasurement

| Scope and measured settings | Historical coordinate maximum | Euclidean maximum | Recommended reported value |
|---|---:|---:|---:|
| ManiSkill3 50-setting grid; same ratio and delay; common-scale range 0.5–2 | 0.13780593872070312 mm | 0.14687605036716456 mm | 0.147 mm |
| Original ManiSkill2 50-setting grid; same ratio and delay; common-scale range 0.5–2 | 0.20742416381835938 mm | 0.22389836246432270 mm | 0.224 mm |
| Original ManiSkill2 dedicated common-scale sweep; range 0.25–4 | 0.52332878112792969 mm | 0.56663463425747918 mm | 0.567 mm |
| ManiSkill3; half nominal torque limit versus nominal | 0.14901161193847656 µm | 0.21073424255447018 µm | 0.211 µm |
| Original ManiSkill2; half nominal torque limit versus nominal | 0.050067901611328125 mm | 0.054181146671622014 mm | 0.0542 mm |

The earlier ManiSkill3 number **0.141 mm is not reproduced** as the maximum coordinate or Euclidean distance from the frozen 50-setting grid. It must not be retained as a verified maximum. No hypothetical explanation of its origin is needed to use the corrected measurement.

Both torque comparisons have byte-identical position arrays on 97 of 98 demonstrations and byte-identical quaternion arrays on the same 97 of 98. Only demonstration 9 changes. The defensible phrase is “stored end-effector pose trajectories”; neither joint state nor commanded torque was stored or tested here.

## Argmax settings, trajectories, and time steps

All five Euclidean maxima occur on demonstration 9. Indices below are zero-based stored trajectory row indices, not elapsed seconds. Full paths, both endpoint settings, SHA-256 hashes, and displacement vectors for every pair are in `RESULTS.json`.

| Scope | First condition | Second condition | Time index | Displacement vector in metres |
|---|---|---|---:|---|
| ManiSkill3 grid | `s0.5_d0.5_delay0` | `s2_d2_delay0` | 47 | (-0.00001747906208038330, -0.000047713518142700195, 0.00013780593872070312) |
| Original-stack grid | `s0.5_d0.5_delay0` | `s2_d2_delay0` | 47 | (-0.00005224347114562988, 0.00006615370512008667, 0.00020742416381835938) |
| Original-stack extended scale | `iso_x0.25` | `iso_x4.0` | 47 | (-0.00013646483421325684, 0.00016905367374420166, 0.0005233287811279297) |
| ManiSkill3 torque | `nominal` | `force_x0.5` | 48 | (-0.00000014901161193847656, 0.00000014901161193847656, 0) |
| Original-stack torque | `nominal` | `force_x0.5` | 48 | (0.000020205974578857422, 0.0000045299530029296875, 0.000050067901611328125) |

The original-stack torque coordinate maximum occurs at time 47, whereas the Euclidean maximum occurs at time 48. Maximizing the separate coordinates and combining them would be incorrect; the reported Euclidean maximum uses coordinates from the same stored time step.

## Inputs, coverage, and missing-data policy

The five source directories are workspace-relative:

- `results/replay_sysid_100/grid`: all 50 settings, 98 declared demonstrations each; 14 nontrivial equal-ratio/equal-delay groups.
- `results/replay_sysid_ms2/grid`: all 50 settings, 98 declared demonstrations each; 14 nontrivial equal-ratio/equal-delay groups.
- `results/replay_sysid_ms2/iso_ratio_v1`: all five settings, 98 declared demonstrations each; one equal-ratio/equal-delay group.
- `results/replay_sysid_100/sweep_v1`: the nominal and half-torque settings, 98 declared demonstrations each.
- `results/replay_sysid_ms2/sweep_v1`: the nominal and half-torque settings, 98 declared demonstrations each.

Exactly **10,796 input files** are pinned: run metadata, selected condition records, and the corresponding trajectory NPZ files. All source paths, sizes, and SHA-256 hashes are in `INPUT_MANIFEST.json` and `INPUT_SHA256SUMS.txt`.

**Missing-input allowance is zero.** For each selected condition, the script requires exactly the 98 distinct demonstration IDs declared by that directory's metadata. It rejects missing IDs, extra IDs, duplicate records, missing NPZ files, incompatible trajectory shapes, inconsistent step counts, nonfinite values, or changed recorded ground-truth trajectories across conditions. It neither intersects available IDs silently nor skips missing trajectories. Ground-truth arrays provide a matched-input check; the reported distances still compare the simulated arrays.

The script checks the coordinate/Euclidean norm inequalities for every matched trajectory comparison. For the torque byte-equality counts it compares dtype, shape, and array bytes independently for position and quaternion. The first successful complete run reports zero failures for every coverage/alignment check.

Pinned script SHA-256: `9e7b5118a99efeb951a77ad538dcd52bf71e00ea2f7953d06b7bf8ee4193a20f`.

Pinned input-manifest SHA-256: `36bc7f7f2b00f4c229111b6b3f63132129c66f9b9d06d03238caacb739c0d366`.

## Manuscript replacement map

Line numbers reflect the files inspected during integration and may move as the main editor works. Only replay-position measurements are affected.

1. `submission/ras/main.tex`, replay-sensitivity paragraph near line 154: define “maximum Euclidean position differences”; shared 0.5–2 range gives **0.147 mm on ManiSkill3** and **0.224 mm on the original stack**; the **original-stack-only** 0.25–4 sweep gives **0.567 mm**. Torque residuals are **0.211 µm on ManiSkill3** and **0.0542 mm on the original stack**. These numerical changes were already visible in the working main file when this audit report was written.
2. `submission/ras/supplementary_methods.tex`, sensitivity-domain explanation near lines 137–143: “measurements confirm over ×1/4 to ×4” needs the explicit scope **on the original stack**. Shared two-stack measurement range is 0.5–2. The symbolic finite domain can remain if its stack/sampling scope is stated; it is not a measured continuous-domain guarantee.
3. `submission/ras/supplementary_methods.tex`, torque-limit checks near lines 503–507: **0.0542 mm in Euclidean position on the original stack**, not the unqualified historical 0.050 mm. The number was already updated in the working file at report time; its stack attribution still needed to be explicit.
4. In both paragraphs, “97 of 98 trajectories bitwise identical” should mean the **stored end-effector pose trajectories**, not the full hidden simulator state.

Do **not** perform a global numerical substitution. Examples of unaffected values include the +0.141 policy-gap estimate near supplementary line 297; the 0.133–0.161, mean 0.141 torque-induced *policy-gap* shifts near line 517; the +0.050 policy gap near line 563; the public nominal +0.147 policy gap; composite replay-loss bounds (including 3.3×10^-7 and 7.2×10^-6); and all success probabilities. Their units, estimands, and computations are different. Historical frozen releases and the frozen Chinese version were not edited by this audit.

## Reproduce

From the repository root, with Python and NumPy installed:

```powershell
python reviews/2026-09-24_ras_retarget/real_counts/replay_scope_recheck/recheck_replay_distances.py --verify-inputs
```

`--verify-inputs` first checks every source file against the pinned hashes, rejects input drift, and then recomputes the measurements with exact-inventory checking. A second run with this flag completed successfully on 24 September 2026 (exit code 0): all 10,796 input hashes matched and all five maxima were reproduced. Omitting it is suitable only for an initial run that intentionally creates a new manifest. All generated outputs remain in this audit directory. The historical checker and raw inputs are not overwritten.

`RESULTS.json` is the complete machine-readable evidence, `SUMMARY.csv` is the compact five-row result, and this report records the manuscript-facing interpretation and correction.
