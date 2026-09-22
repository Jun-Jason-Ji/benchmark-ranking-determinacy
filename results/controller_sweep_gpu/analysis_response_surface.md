# Response-surface bound over the replay-compatible controller strip

GP over (log2 stiffness scale, log2 damping scale); compatible strip |u − v| ≤ 0.25 (ratio ≈ 1). Bounds: min/max over the strip of posterior mean ∓/± k·sd, k = 2 (pointwise) and k = 3 (crude simultaneous).

| task | n obs | length scale | signal sd | bound k=2 | verdict k=2 | bound k=3 | verdict k=3 | point (nominal) |
|---|---:|---:|---:|---|---|---|---|---|
| carrot | 13 | 0.5 | 0.02 | [-0.08, +0.01] | abstain | [-0.10, +0.03] | abstain | abstain |
| spoon | 13 | 0.5 | 0.05 | [+0.10, +0.33] | small better | [+0.05, +0.37] | small better | small better |
| eggplant | 13 | 0.5 | 0.05 | [+0.03, +0.30] | small better | [-0.01, +0.34] | abstain | small better |

Observations per task (condition, Δ, SE):

- carrot: nominal (n=48): -0.021±0.063; stiff_x0.5 (n=48): -0.062±0.063; stiff_x2.0 (n=48): -0.042±0.051; damp_x0.5 (n=48): -0.042±0.051; damp_x2.0 (n=48): -0.083±0.072; stiff_x0.25 (n=24): +0.083±0.058; stiff_x4.0 (n=24): -0.042±0.042; damp_x0.25 (n=24): -0.042±0.073; damp_x4.0 (n=24): -0.083±0.103; iso_x0.25 (n=96): -0.021±0.033; iso_x0.5 (n=96): -0.062±0.036; iso_x2.0 (n=48): -0.062±0.055; iso_x4.0 (n=96): +0.000±0.044
- spoon: nominal (n=48): +0.292±0.073; stiff_x0.5 (n=48): +0.250±0.076; stiff_x2.0 (n=48): +0.208±0.079; damp_x0.5 (n=48): +0.146±0.059; damp_x2.0 (n=48): +0.208±0.079; stiff_x0.25 (n=24): +0.167±0.078; stiff_x4.0 (n=24): +0.083±0.058; damp_x0.25 (n=24): +0.042±0.042; damp_x4.0 (n=24): +0.208±0.085; iso_x0.25 (n=48): +0.229±0.068; iso_x0.5 (n=48): +0.333±0.075; iso_x2.0 (n=48): +0.146±0.073; iso_x4.0 (n=48): +0.312±0.080
- eggplant: nominal (n=96): +0.208±0.061; stiff_x0.5 (n=48): +0.354±0.092; stiff_x2.0 (n=48): +0.125±0.077; damp_x0.5 (n=48): +0.083±0.093; damp_x2.0 (n=48): +0.250±0.096; stiff_x0.25 (n=24): +0.083±0.083; stiff_x4.0 (n=24): +0.208±0.134; damp_x0.25 (n=24): +0.125±0.139; damp_x4.0 (n=24): +0.375±0.101; iso_x0.25 (n=96): +0.000±0.063; iso_x0.5 (n=48): +0.208±0.084; iso_x2.0 (n=48): +0.125±0.077; iso_x4.0 (n=96): +0.188±0.068

Caveats: 13 design points; SE from per-episode paired differences; k=3 is a crude simultaneous factor, not a certified band. Delay, force limit and contact parameters are separate axes and are not in this surface.