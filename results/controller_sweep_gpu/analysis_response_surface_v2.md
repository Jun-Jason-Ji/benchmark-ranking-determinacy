# Response-surface bound v2: simultaneous 95% band over the compatible strip + flatness gate

Strip |log2 k − log2 d| ≤ 0.25; GP hyperparameters marginalised over a (ℓ, σf) grid with weights ∝ exp(−NLL); 4000 posterior function draws; L/U = 2.5th pct of draw-minimum / 97.5th pct of draw-maximum. Flatness gate: paired Δ(c) − Δ(nominal) over the calibration-invisible controller conditions; '*' = rejects flatness.

Two evaluation ranges are reported: **restricted** to the sampled design range (|u|, |v| ≤ 2), which is the configuration the paper adopts, and **extended** half a grid step beyond it (≤ 2.5). The figure draws the restricted one.

| task | restricted band (adopted) | verdict | extended band | verdict | top (weight, ℓ, σf) | flatness gate (controller-invisible) | union bound verdict |
|---|---|---|---|---|---|---|---|
| carrot | [-0.10, +0.03] | abstain | [-0.11, +0.04] | abstain | [(0.13, 0.5, 0.02), (0.12, 0.75, 0.02), (0.12, 1.0, 0.02)] | iso_x0.25: -0.04 [-0.17, +0.06]; iso_x0.5: -0.10 [-0.25, +0.02]; iso_x2.0: -0.04 [-0.17, +0.06]; iso_x4.0: +0.08 [-0.04, +0.23]; force_x0.5: +0.02 [+0.00, +0.06] | abstain |
| spoon | [+0.03, +0.43] | small better | [+0.01, +0.46] | small better | [(0.13, 0.5, 0.05), (0.12, 0.75, 0.05), (0.09, 0.75, 0.1)] | iso_x0.25: -0.06 [-0.23, +0.10]; iso_x0.5: +0.04 [-0.08, +0.19]; iso_x2.0: -0.15 [-0.29, +0.00]; iso_x4.0: +0.02 [-0.12, +0.19]; force_x0.5: -0.06 [-0.15, +0.02] | abstain |
| eggplant | [-0.06, +0.36] | abstain (gated → union bound) | [-0.10, +0.36] | abstain | [(0.06, 0.5, 0.05), (0.06, 0.75, 0.05), (0.05, 1.0, 0.05)] | iso_x0.25: -0.21 [-0.36, -0.06] *; iso_x0.5: -0.02 [-0.19, +0.15]; iso_x2.0: -0.10 [-0.25, +0.04]; iso_x4.0: -0.02 [-0.18, +0.14]; force_x0.5: -0.02 [-0.17, +0.11] | abstain |

## Contact axes (1-D, same method; gate over friction/density conditions)

| task | axis | simultaneous bound | verdict | flatness gate | union verdict (controller+contact) |
|---|---|---|---|---|---|
| carrot | friction | [-0.17, +0.11] | abstain | fric_x0.4: -0.08 [-0.29, +0.17]; fric_x2.5: -0.08 [-0.25, +0.08] | abstain |
| carrot | density | [-0.15, +0.11] | abstain | dens_x0.5: +0.00 [-0.12, +0.12]; dens_x2.0: -0.12 [-0.29, +0.04] | abstain |
| spoon | friction | [-0.01, +0.41] | abstain | fric_x0.4: -0.21 [-0.46, +0.00]; fric_x2.5: -0.12 [-0.42, +0.12] | abstain |
| spoon | density | [+0.09, +0.37] | small better | dens_x0.5: -0.08 [-0.25, +0.08]; dens_x2.0: -0.12 [-0.29, +0.04] | abstain |
| eggplant | friction | [-0.03, +0.33] | abstain (gated → union bound) | fric_x0.4: -0.16 [-0.29, -0.02] *; fric_x2.5: -0.12 [-0.42, +0.17] | abstain |
| eggplant | density | [-0.00, +0.40] | abstain | dens_x0.5: -0.14 [-0.27, +0.00]; dens_x2.0: +0.00 [-0.38, +0.38] | abstain |

Reading: the simultaneous band is the certified-style version of the strip bound under the GP model; the gate says whether the model's smoothness assumption is contradicted by the paired data on that axis. Where gated, report the union bound instead.

Figure: `results/figures/fig_response_surface.png` -- the marginalised posterior mean over the restricted plane, i.e. the same computation as the adopted band above. Caption values for the paper's Fig. 6 are the restricted columns of the first table, verbatim:

- carrot: [-0.10, +0.03], abstain
- spoon: [+0.03, +0.43], small better
- eggplant: [-0.06, +0.36], abstain (flatness gate rejects; report the union bound)