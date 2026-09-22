# Compatible-set calibration vs point calibration (Experiment B, first instantiation)

Replay residuals: 40 BridgeData V2 demos, ManiSkill3 free-space replay (results/replay_sysid/grid). Compatibility rule: paired bootstrap 95% lower bound of mean(err_c − err_nominal) ≤ 0 (not significantly worse than nominal). Sweep data: results/controller_sweep_gpu (all available episodes per condition; n shown).

## Replay compatibility of sweep conditions

| sweep condition | replay condition | class | mean Δerr vs nominal | 95% | compatible |
|---|---|---|---:|---|---|
| nominal | s1_d1_delay0 | ctrl | +0.0000 | [+0.0000, +0.0000] | yes |
| stiff_x0.5 | s0.5_d1_delay0 | ctrl | +0.0099 | [+0.0075, +0.0123] | no |
| stiff_x2.0 | s2_d1_delay0 | ctrl | +0.0060 | [+0.0045, +0.0073] | no |
| damp_x0.5 | s1_d0.5_delay0 | ctrl | +0.0060 | [+0.0045, +0.0073] | no |
| damp_x2.0 | s1_d2_delay0 | ctrl | +0.0099 | [+0.0075, +0.0123] | no |
| delay_1 | s1_d1_delay1 | ctrl | +0.0069 | [+0.0044, +0.0094] | no |
| stiff_x0.25 | — | ctrl_untested | untested | — | excluded (untested) |
| stiff_x4.0 | — | ctrl_untested | untested | — | excluded (untested) |
| damp_x0.25 | — | ctrl_untested | untested | — | excluded (untested) |
| damp_x4.0 | — | ctrl_untested | untested | — | excluded (untested) |
| delay_2 | — | ctrl_untested | untested | — | excluded (untested) |
| iso_x0.25 | s0.5_d0.5_delay0 | ctrl_invisible | 0 (invisible) | — | yes (by construction) |
| iso_x0.5 | s0.5_d0.5_delay0 | ctrl_invisible | 0 (invisible) | — | yes (by construction) |
| iso_x2.0 | s2_d2_delay0 | ctrl_invisible | 0 (invisible) | — | yes (by construction) |
| iso_x4.0 | s2_d2_delay0 | ctrl_invisible | 0 (invisible) | — | yes (by construction) |
| force_x0.5 | s1_d1_delay0 | ctrl_invisible | 0 (invisible) | — | yes (by construction) |
| fric_x0.4 | — | contact_invisible | 0 (invisible) | — | yes (by construction) |
| fric_x2.5 | — | contact_invisible | 0 (invisible) | — | yes (by construction) |
| dens_x0.5 | — | contact_invisible | 0 (invisible) | — | yes (by construction) |
| dens_x2.0 | — | contact_invisible | 0 (invisible) | — | yes (by construction) |

## Verdicts per task: point (nominal) vs compatible-set (controller-only) vs compatible-set (controller + contact)

Δ = rate(octo-small) − rate(octo-base), paired by episode. Set verdict uses L = min CI-lower, U = max CI-upper over compatible conditions.

### carrot

| condition | class | in set | n | Δ | 95% |
|---|---|---|---:|---:|---|
| nominal | ctrl | yes | 48 | -0.021 | [-0.15, +0.10] |
| stiff_x0.5 | ctrl | no | 48 | -0.062 | [-0.19, +0.06] |
| stiff_x2.0 | ctrl | no | 48 | -0.042 | [-0.15, +0.06] |
| damp_x0.5 | ctrl | no | 48 | -0.042 | [-0.15, +0.06] |
| damp_x2.0 | ctrl | no | 48 | -0.083 | [-0.23, +0.06] |
| delay_1 | ctrl | no | 48 | +0.021 | [-0.08, +0.12] |
| stiff_x0.25 | ctrl_untested | no | 24 | +0.083 | [+0.00, +0.21] |
| stiff_x4.0 | ctrl_untested | no | 24 | -0.042 | [-0.12, +0.00] |
| damp_x0.25 | ctrl_untested | no | 24 | -0.042 | [-0.17, +0.08] |
| damp_x4.0 | ctrl_untested | no | 24 | -0.083 | [-0.29, +0.12] |
| delay_2 | ctrl_untested | no | 24 | +0.000 | [+0.00, +0.00] |
| iso_x0.25 | ctrl_invisible | yes | 96 | -0.021 | [-0.08, +0.04] |
| iso_x0.5 | ctrl_invisible | yes | 96 | -0.062 | [-0.14, +0.00] |
| iso_x2.0 | ctrl_invisible | yes | 48 | -0.062 | [-0.17, +0.04] |
| iso_x4.0 | ctrl_invisible | yes | 96 | +0.000 | [-0.08, +0.08] |
| force_x0.5 | ctrl_invisible | yes | 48 | +0.000 | [-0.10, +0.12] |
| fric_x0.4 | contact_invisible | yes | 24 | -0.042 | [-0.21, +0.12] |
| fric_x2.5 | contact_invisible | yes | 24 | -0.042 | [-0.21, +0.12] |
| dens_x0.5 | contact_invisible | yes | 24 | +0.042 | [-0.08, +0.21] |
| dens_x2.0 | contact_invisible | yes | 24 | -0.083 | [-0.21, +0.00] |

**carrot: point = abstain; set (controller) = abstain; set (controller + contact) = abstain.**

### spoon

| condition | class | in set | n | Δ | 95% |
|---|---|---|---:|---:|---|
| nominal | ctrl | yes | 48 | +0.292 | [+0.15, +0.44] |
| stiff_x0.5 | ctrl | no | 48 | +0.250 | [+0.10, +0.40] |
| stiff_x2.0 | ctrl | no | 48 | +0.208 | [+0.06, +0.35] |
| damp_x0.5 | ctrl | no | 48 | +0.146 | [+0.04, +0.27] |
| damp_x2.0 | ctrl | no | 48 | +0.208 | [+0.06, +0.38] |
| delay_1 | ctrl | no | 48 | +0.000 | [-0.12, +0.12] |
| stiff_x0.25 | ctrl_untested | no | 24 | +0.167 | [+0.04, +0.33] |
| stiff_x4.0 | ctrl_untested | no | 24 | +0.083 | [+0.00, +0.21] |
| damp_x0.25 | ctrl_untested | no | 24 | +0.042 | [+0.00, +0.12] |
| damp_x4.0 | ctrl_untested | no | 24 | +0.208 | [+0.04, +0.38] |
| delay_2 | ctrl_untested | no | 24 | +0.000 | [-0.17, +0.17] |
| iso_x0.25 | ctrl_invisible | yes | 48 | +0.229 | [+0.10, +0.35] |
| iso_x0.5 | ctrl_invisible | yes | 48 | +0.333 | [+0.19, +0.48] |
| iso_x2.0 | ctrl_invisible | yes | 48 | +0.146 | [+0.00, +0.29] |
| iso_x4.0 | ctrl_invisible | yes | 48 | +0.312 | [+0.17, +0.46] |
| force_x0.5 | ctrl_invisible | yes | 48 | +0.229 | [+0.10, +0.35] |
| fric_x0.4 | contact_invisible | yes | 24 | +0.083 | [-0.12, +0.29] |
| fric_x2.5 | contact_invisible | yes | 24 | +0.167 | [-0.04, +0.38] |
| dens_x0.5 | contact_invisible | yes | 24 | +0.208 | [+0.00, +0.42] |
| dens_x2.0 | contact_invisible | yes | 24 | +0.167 | [+0.04, +0.33] |

**spoon: point = small better; set (controller) = abstain; set (controller + contact) = abstain.**

### eggplant

| condition | class | in set | n | Δ | 95% |
|---|---|---|---:|---:|---|
| nominal | ctrl | yes | 96 | +0.208 | [+0.09, +0.32] |
| stiff_x0.5 | ctrl | no | 48 | +0.354 | [+0.17, +0.52] |
| stiff_x2.0 | ctrl | no | 48 | +0.125 | [-0.02, +0.27] |
| damp_x0.5 | ctrl | no | 48 | +0.083 | [-0.10, +0.25] |
| damp_x2.0 | ctrl | no | 48 | +0.250 | [+0.06, +0.44] |
| delay_1 | ctrl | no | 48 | +0.312 | [+0.12, +0.50] |
| stiff_x0.25 | ctrl_untested | no | 24 | +0.083 | [-0.08, +0.25] |
| stiff_x4.0 | ctrl_untested | no | 24 | +0.208 | [-0.04, +0.46] |
| damp_x0.25 | ctrl_untested | no | 24 | +0.125 | [-0.12, +0.38] |
| damp_x4.0 | ctrl_untested | no | 24 | +0.375 | [+0.17, +0.58] |
| delay_2 | ctrl_untested | no | 24 | +0.375 | [+0.17, +0.58] |
| iso_x0.25 | ctrl_invisible | yes | 48 | +0.062 | [-0.10, +0.23] |
| iso_x0.5 | ctrl_invisible | yes | 48 | +0.208 | [+0.04, +0.38] |
| iso_x2.0 | ctrl_invisible | yes | 48 | +0.125 | [-0.02, +0.27] |
| iso_x4.0 | ctrl_invisible | yes | 48 | +0.208 | [+0.02, +0.40] |
| force_x0.5 | ctrl_invisible | yes | 48 | +0.146 | [-0.02, +0.31] |
| fric_x0.4 | contact_invisible | yes | 96 | +0.052 | [-0.07, +0.18] |
| fric_x2.5 | contact_invisible | yes | 24 | +0.167 | [-0.04, +0.38] |
| dens_x0.5 | contact_invisible | yes | 96 | +0.073 | [-0.04, +0.19] |
| dens_x2.0 | contact_invisible | yes | 24 | +0.292 | [+0.00, +0.54] |

**eggplant: point = small better; set (controller) = abstain; set (controller + contact) = abstain.**

## Summary

| task | point verdict | set verdict (controller) | set verdict (controller + contact) |
|---|---|---|---|
| carrot | abstain | abstain | abstain |
| spoon | small better | abstain | abstain |
| eggplant | small better | abstain | abstain |

Reading: where the set verdict abstains while the point verdict decides, the ranking conclusion depends on parameters the calibration data cannot constrain. Where both agree, the conclusion is robust to calibration ambiguity within the tested ranges.