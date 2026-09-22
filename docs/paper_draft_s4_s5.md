# Draft: Sections 4 and 5 (2026-09-20)

Status: sections whose evidence is already settled. Numbers marked `[pending]` are refreshed from
`scripts/make_core_table.py` / `scripts/make_figures_v2.py` once the census queue finishes.
Written in English for direct transfer to the manuscript; internal notes are in blockquotes and are not part
of the manuscript text.

---

## 4 The Calibration Protocol Is Structurally Blind

### 4.1 Setup

SIMPLER-style calibration fits simulator parameters by replaying recorded real demonstrations: the recorded
end-effector targets are fed to the simulated controller, and the parameters are chosen to minimise the
deviation between simulated and recorded trajectories. Let \(z\) collect the joint PD stiffness \(k\), damping
\(d\), torque limit \(\tau_{\max}\), execution delay, and the contact parameters (object friction, density).
Write \(L(z)\) for the replay loss on the demonstration set.

### 4.2 An exact invariance, not a weak one

Two directions in \(z\) leave \(L\) exactly unchanged.

**(i) Common scaling of the PD gains.** Under free-space replay the joint response to a target is, to the order
that the demonstrations excite, first order with time constant \(d/k\). Scaling \((k, d) \mapsto (ck, cd)\)
leaves the time constant, hence the trajectory, unchanged. This is a *structural* invariance of the protocol,
not a flat region of a noisy objective.

**(ii) The torque limit.** Along demonstrated velocities the commanded torque never reaches \(\tau_{\max}\), so
the saturation is inactive and the trajectory is independent of its value.

> Internal: the ratio direction \(d/k\) and the execution delay *are* identified, and both produce the expected
> bowl-shaped loss curves; the claim is specific to the two directions above.

### 4.3 Empirical confirmation on two independent simulator stacks

We replayed 98 BridgeData V2 demonstrations on (a) the ManiSkill3 port and (b) the original SIMPLER main
stack (ManiSkill2\_real2sim + SAPIEN 2.2.2), the latter running headless in WSL through a purpose-built
Vulkan layer (Appendix B).

| Direction | ManiSkill3 | Original stack | Verdict |
|---|---|---|---|
| Common scale \(c \in \{0.25, 0.5, 2, 4\}\) | max trajectory difference 0.141 mm | 0.207 mm | invariant |
| Torque limit \(\times 0.5\) | difference exactly 0 (bitwise) | exactly 0 | invisible |
| Ratio \(d/k\) \(\times\{0.5, 2\}\) | paired error increase +0.0089 [+0.0073, +0.0105] / +0.0064 [+0.0055, +0.0072] | same sign and order | identified |
| Execution delay 1 step | clearly identified | clearly identified | identified |

All 14 iso-scale groups fall below a 1 mm tolerance; the agreement between the two stacks is sub-millimetre.
**Figure 1** contrasts the bowl-shaped loss along the identified directions with the flat loss along the
invariant ones.

> Sources: `results/replay_sysid/{sweep_v1,grid}/iso_invariance.md`,
> `results/replay_sysid_ms2/FINDING_original_stack.md`.

### 4.4 The compatible set

Inverting the calibration test therefore yields a compatible set of the form

\[
C_\alpha = \{d/k \approx \text{point estimate}\} \times (\text{full scale axis}) \times
(\text{full torque axis}) \times (\text{full contact axes}),
\]

i.e. the calibration data constrains one direction tightly and leaves the others completely free. Ratio
settings \(\times 0.25, 0.5, 2, 4\) and the delayed-execution settings are excluded (error-increment lower
bounds +0.004 to +0.008); nothing excludes any value of the common scale or the torque limit.

**The question of this paper is what a policy ranking computed inside \(C_\alpha\) is worth.**

---

## 5 What a Finite Benchmark Measures

### 5.1 The benchmark is a finite population of configurations

Both widely used ports map the episode index onto a fixed grid of initial states:

```
pos  = (episode_id mod (n_xy · n_quat)) div n_quat
quat =  episode_id mod  n_quat
```

so the number of distinct initial configurations is \(n_{xy} \cdot n_{quat}\), and any episode index beyond
that repeats an earlier scene exactly. Object scale is drawn from the asset table but every object has a
single admissible scale, so it adds no variation.

| Task | Original stack | ManiSkill3 port |
|---|---:|---:|
| Put eggplant in basket | 8 × 3 = **24** | 8 × 8 = **64** |
| Put spoon on towel | 12 × 2 = 24 | 12 × 2 = 24 |
| Put carrot on plate | 12 × 2 = 24 | 12 × 2 = 24 |
| Stack green on yellow cube | 24 × 1 = 24 | 24 × 1 = 24 |

Three consequences follow, and all three are visible in published practice.

1. **Beyond the grid, episodes are exact repeats.** A "96-episode" evaluation of the eggplant task on the
   ManiSkill3 port is 64 distinct scenes, 32 of which are visited twice.
2. **The two ports do not evaluate the same benchmark.** For the eggplant task they differ in the number of
   orientations (3 vs 8) and in the quaternion values themselves (best matching pair has \(|\langle q_1, q_2
   \rangle| = 0.54\)). An episode index therefore does not denote the same scene across ports, and per-episode
   agreement between them is meaningless. Spoon and carrot share their grids exactly — and indeed their
   cross-port per-episode agreement is 0.71–0.96, against chance level for the eggplant task. That contrast is
   the control for this diagnosis.
3. **One scene is worth 1/24 or 1/64.** On a 24-configuration task, any reported difference below 0.042 is
   less than one scene.

### 5.2 The official protocol is already a census

The reference evaluation script runs each bridge task with `--obj-episode-range 0 24` under
`init_rng ∈ {0, 2, 4}`: the **complete 24-configuration census repeated under three fixed policy seeds**, 72
episodes, which is exactly the denominator of the published table (e.g. 31/72 = 0.431 and 41/72 = 0.569 for the
two Octo variants on the eggplant task). The ManiSkill3 port's evaluation script instead defaults to 100
episodes indexed as `seed + i`, aligning with neither the grid nor the seed repetition.

> Internal: this is the single most useful fact for readers — the community's own reference protocol already
> does the right thing, and the drift is in what downstream work does with it.

### 5.3 What counts as a replicate depends on the policy

| Policy | Source of randomness | Changing the policy seed | Legitimate replication axis |
|---|---|---|---|
| Octo (diffusion action head) | `jax.random.PRNGKey(seed)` enters sampling | produces a new sample | configuration × seed |
| OpenVLA (greedy decoding) | `do_sample=False`; the seed is unused | produces **nothing new** | configuration only |

Empirically, two "seed sets" of the deterministic policy are record-identical in 48 of 48 episodes. For such a
policy, "replicated across seed sets" is vacuous, and the configuration grid — which can be enumerated — is the
only sampling axis.

### 5.4 Two estimands, two intervals

| Estimand | Uncertainty | Estimator |
|---|---|---|
| **(i) The benchmark value** — the number this benchmark reports | configuration sampling error is zero after a census; only policy noise and run-to-run numerical noise remain | \(\mathrm{Var}(\hat\Delta) = N^{-2}\sum_c [s^2_A(c)/S_c + s^2_B(c)/R_c]\) |
| **(ii) The generalisation value** — performance on comparable scenes | configuration sampling **and** policy noise | paired bootstrap **clustered by configuration** |

Three implementation points matter and are easy to get wrong:

- With a single run per configuration, estimator (i) degenerates to the ordinary binomial interval. **A census
  does not narrow an interval; replicates do.** Enumerate the grid first (which removes double counting), then
  add runs (which removes policy noise).
- Record-identical re-runs of a deterministic policy must be merged into one observation, or the variance is
  halved for free.
- Estimator (ii) must cluster by configuration. In our data this widens intervals by a median factor of 1.04 on
  the 64-configuration task and up to 1.33 on a 24-configuration task run for 96 episodes, and changes no
  verdict — but the effective sample size must be reported honestly.

### 5.5 The evaluation protocol and the implementation build are themselves invisible parameters

Holding the configuration grid fixed, we separated two further sources by re-running one seed set's seeds on a
newer inference-server build (`A′`):

| Source | Isolation | Magnitude |
|---|---|---|
| Policy seed | same build, different seeds | benchmark value 0.375 / 0.516 / 0.500; \(\mathrm{sd}(\Delta) = 0.104\) on the headline pair |
| Implementation build | same seeds, newer build | +0.078 on one policy, and **only 0.73–0.88 of episodes reproduce** |
| **Robot texture variant** | same build, same seeds, `urdf_version` only | per-variant success 0.000 / 0.280 / 0.013 / 0.400 on one policy — **range 0.400**, sd 0.199 |

The third row is the largest entry in this paper's uncertainty budget, and it is the one a reader of the
published tables cannot see at all. `urdf_version` selects among four recolourings of the robot model. It
changes no physical property — not a mass, not a friction coefficient, not a joint limit — and the published
figure for this task is the mean over all four. On the fractal coke-can census the four variants give one
policy 0.000, 0.280, 0.013 and 0.400, so evaluating on a single variant displaces the reported number by
−0.173 to +0.227 relative to the four-variant mean. For comparison, the can's physical orientation, which
does change the dynamics, spans only 0.140.

This axis is invisible to replay calibration for the same reason the torque limit is (§4.2): it never enters
the demonstration trajectory. Unlike the torque limit, it is not even a physical parameter, which makes it the
paper's sharpest illustration that "calibration-invisible" is a property of the protocol's coverage rather
than of physics. Whether it can flip a *ranking* rather than inflate one policy's variance is a separate
question, and §8.4 answers it on a second policy over the same grid: it does not, on the pair we can test.

> Sources for this row: `results/fractal_validation/FINDING_urdf_variance.md`,
> `results/fractal_reversal/analysis_fractal_reversal.md`.

Two practical consequences:

1. **One seed set plus a per-episode bootstrap declares rankings that do not hold.** In our own data,
   \(\Delta(\text{small}-\text{base}) = +0.250\,[+0.08, +0.32]\) declared one Octo variant better; three seed
   sets from a single build give \(+0.141 / -0.031 / -0.047\). We retract that verdict. The interval was wrong
   because it treated one seed draw per configuration as the population.
2. **Never pool replicates across builds.** Doing so inflated the measured seed standard deviation from 0.055
   to 0.093 — about half of the apparent "seed noise" was build drift.

Finally, the three same-build values of one policy bracket the published figure (0.431), which indicates that
**published three-decimal benchmark numbers carry roughly ±0.07 of unreported seed uncertainty.**

**Figure 2** places the sources on one axis, each computed from the episode records by
`scripts/make_figures_v2.py`: evaluation half-width at 1, 3 and 10 seeds (0.138 / 0.079 / 0.044),
implementation build (0.055), the shift caused by the calibration-invisible torque limit (0.121), and the
robot texture variant (range 0.400, from per-variant rates 0.000 / 0.280 / 0.013 / 0.400). Only the first
shrinks, as \(1/\sqrt{S}\); the rest do not shrink at all, and the largest of them is not a physical
parameter.

> Internal — **two aggregations are in circulation and must be labelled before submission.** The figure's
> numbers are medians/maxima over all Octo pairs and both core conditions at five seed sets. The numbers
> quoted in §5.5's text above and in `theory_protocol.md §6.1` (single-seed half-width ±0.108, three seeds
> ±0.062, ten seeds ±0.034; build drift 0.078; shift 0.141) are for the headline pair on the 64-configuration
> eggplant census at three seed sets. Both are defensible; quoting one in the text and the other in the
> figure is not. Decide which is the paper's standard scope, state it once, and regenerate whichever side
> does not match. The gap is not small — 0.121 vs 0.141 on the shift, and 0.055 vs 0.078 on build drift.

> Sources: `results/controller_sweep_gpu_replayA/FINDING_platform_drift.md`,
> `results/controller_sweep_gpu_rep3/FINDING_estimand_matters.md`,
> `results/controller_sweep_gpu/NOTE_cluster_bootstrap.md`, `results/PROVENANCE_AUDIT_2026-09-19.md`.

### 5.6 Reporting requirements

Every number in this paper carries: configurations covered / total; independent runs per configuration, and
whether they are genuinely independent for that policy; the variance model (empirical, binomial fallback, or
unmeasured); which estimand it targets; and the port and build it was collected on. We log the last of these
per run in an append-only `runs.jsonl`, having discovered that a per-directory metadata file is overwritten by
the next run and makes the provenance of already-collected episodes unrecoverable.
