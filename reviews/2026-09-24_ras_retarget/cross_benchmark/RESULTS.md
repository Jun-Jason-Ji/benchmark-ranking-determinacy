# Native ManiSkill external check: complete results

This is a workflow portability check on native Franka manipulation tasks. It is not an independent physics-engine replication, a real-robot validation, or a calibration-identifiability experiment. All 20 planned cells were retained.

The primary difference is joint-space PPO minus Cartesian-position PPO. Counts use final-step success after 50 steps on the same 256 initial scenes. Intervals concern the randomized initial-scene distribution under the stated sampling assumptions; the observed finite sample is not an exhaustive benchmark census.

| Task | Nominal difference [95% interval] | Five-setting envelope | Verdict |
|---|---:|---:|---|
| PickCube-v1 | +0.352 [+0.253, +0.439] | [+0.180, +0.498] | joint |
| PushCube-v1 | -0.297 [-0.373, -0.210] | [-0.494, -0.103] | cartesian |

## Full planned grid

| Task | Setting | Joint successes / 256 | Cartesian successes / 256 | Paired difference | 95% interval |
|---|---|---:|---:|---:|---:|
| PickCube-v1 | nominal | 249 | 159 | +0.352 | [+0.253, +0.439] |
| PickCube-v1 | gain_half | 242 | 170 | +0.281 | [+0.180, +0.373] |
| PickCube-v1 | gain_double | 247 | 142 | +0.410 | [+0.309, +0.498] |
| PickCube-v1 | force_half | 247 | 168 | +0.309 | [+0.212, +0.395] |
| PickCube-v1 | force_double | 249 | 153 | +0.375 | [+0.279, +0.459] |
| PushCube-v1 | nominal | 2 | 78 | -0.297 | [-0.373, -0.210] |
| PushCube-v1 | gain_half | 10 | 59 | -0.191 | [-0.273, -0.103] |
| PushCube-v1 | gain_double | 8 | 78 | -0.273 | [-0.360, -0.178] |
| PushCube-v1 | force_half | 0 | 65 | -0.254 | [-0.320, -0.178] |
| PushCube-v1 | force_double | 2 | 109 | -0.418 | [-0.494, -0.328] |

## Success-definition sensitivity (recorded diagnostic)

The prespecified primary outcome is final-step success. Official PPO examples prominently report ever-success. These answer different questions: reaching the goal at least once versus retaining success at step 50. Both were recorded in every cell; the primary outcome was not changed after observing the distinction.

| Task | Nominal ever-success joint / Cartesian | Difference [95% interval] | Five-setting ever-success envelope | Verdict |
|---|---:|---:|---:|---|
| PickCube-v1 | 250/256 / 159/256 | +0.355 [+0.258, +0.441] | [+0.196, +0.494] | joint |
| PushCube-v1 | 256/256 / 200/256 | +0.219 [+0.146, +0.283] | [+0.091, +0.378] | joint |

### Complete ever-success diagnostic

| Task | Setting | Joint successes / 256 | Cartesian successes / 256 | Paired difference | 95% interval |
|---|---|---:|---:|---:|---:|
| PickCube-v1 | nominal | 250 | 159 | +0.355 | [+0.258, +0.441] |
| PickCube-v1 | gain_half | 246 | 170 | +0.297 | [+0.196, +0.388] |
| PickCube-v1 | gain_double | 250 | 145 | +0.410 | [+0.313, +0.494] |
| PickCube-v1 | force_half | 249 | 169 | +0.312 | [+0.218, +0.397] |
| PickCube-v1 | force_double | 250 | 155 | +0.371 | [+0.275, +0.455] |
| PushCube-v1 | nominal | 256 | 200 | +0.219 | [+0.146, +0.283] |
| PushCube-v1 | gain_half | 256 | 177 | +0.309 | [+0.228, +0.378] |
| PushCube-v1 | gain_double | 254 | 212 | +0.164 | [+0.091, +0.231] |
| PushCube-v1 | force_half | 256 | 201 | +0.215 | [+0.143, +0.278] |
| PushCube-v1 | force_double | 256 | 182 | +0.289 | [+0.210, +0.357] |

## Prespecified descriptive prefix budgets

| Task | Scenes | Nominal verdict | Envelope verdict | Envelope |
|---|---:|---|---|---:|
| PickCube-v1 | 32 | joint | abstain | [-0.038, +0.617] |
| PickCube-v1 | 64 | joint | joint | [+0.133, +0.554] |
| PickCube-v1 | 128 | joint | joint | [+0.162, +0.537] |
| PickCube-v1 | 256 | joint | joint | [+0.180, +0.498] |
| PushCube-v1 | 32 | abstain | abstain | [-0.617, +0.082] |
| PushCube-v1 | 64 | cartesian | abstain | [-0.629, +0.006] |
| PushCube-v1 | 128 | cartesian | cartesian | [-0.540, -0.076] |
| PushCube-v1 | 256 | cartesian | cartesian | [-0.494, -0.103] |

## Integrity and interpretation

- All four checkpoints match their official Hugging Face LFS SHA256. No training was performed.
- Within each task, all ten policy–setting cells share identical recorded initial joint, object and goal states; all 256 states are distinct.
- Initial scenes are paired; actor means are deterministic. There are no additional policy sampling replications or independent training runs.
- Five arm settings were fixed before full evaluation: nominal, half/double common gain, and half/double force limit. These are deliberate robustness interventions, not a real-data-compatible calibration set.
- Published export metadata comes from an earlier ManiSkill build. No equivalence to the original training or published benchmark score is assumed.
- The public ManiSkill support table does not guarantee Windows GPU support. The recorded unchanged native components ran successfully on this local Windows build; operating-system portability remains untested.
- This two-task check broadens embodiment, task, policy family and observation modality, but shares SAPIEN/PhysX lineage with SIMPLER and does not establish universal benchmark generalization.
- Null and abstention results are retained; neither tasks nor intervention magnitudes were selected after the grid outcomes.

## Sources

- Official code: https://github.com/mani-skill/ManiSkill
- Official policy export and demonstrations: https://huggingface.co/datasets/haosulab/ManiSkill_Demonstrations/tree/d674485bbffdd533914e52d272fdda34c0515608/demos
- Native task interface and RNG: https://maniskill.readthedocs.io/en/latest/user_guide/concepts/rng.html
- ManiSkill3 formal publication: https://www.roboticsproceedings.org/rss21/p021.pdf
