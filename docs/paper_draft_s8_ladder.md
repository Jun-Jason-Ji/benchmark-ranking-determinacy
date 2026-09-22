# Draft: Section 8 — A Verdict Ladder and Its Reach (2026-09-21)

New section. Under the old spine this material was §7 and ended on the synthetic coverage result; the
reframe (`paper_spine_2026-09-21.md`) makes it the paper's closing empirical section and requires it to end
on the delimiting negative result from `results/fractal_reversal/`.

Sources: `results/benchmark/track_s/FINDING_track_s.md` (and `track_s_smax2/`, `track_s_smax2_ell1/` for the
configuration study), `results/benchmark/track_r/track_r_summary.md`,
`results/fractal_reversal/analysis_fractal_reversal.md`, `scripts/analyze_fractal_reversal.py`.

Written in English for direct transfer to the manuscript; internal notes are in blockquotes.

---

## 8 A Verdict Ladder and Its Reach

Sections 4 through 7 establish that a simulation benchmark's ranking claims are underdetermined by the
evidence behind them, from three independent directions. This section asks what to do about it. The remedy
suggested by §3.3 is a set-valued verdict, and the question is what such a criterion buys, at what cost in
power, and where it stops working. We answer all three, and the third answer is negative.

### 8.1 Two rungs, with different guarantees

We evaluate two criteria beyond point calibration, and the distinction between their guarantees is the whole
design.

**The union bound** declares an ordering when every *sampled* parameter setting in \(C_\alpha\) agrees in
sign, using \(\big[\min_z \mathrm{lo}(z), \max_z \mathrm{hi}(z)\big]\). Its guarantee is of
**sampling-extremum** type: it is valid with respect to the extremes of \(\Delta(z)\) over the settings
actually run, and says nothing about values between them.

**A Gaussian-process simultaneous band** fits \(\Delta(z)\) over the parameter axes and requires the sign to
hold across a simultaneous band over the whole compatible region. Its guarantee is of **within-band** type
under a smoothness prior, and it therefore covers features that fall between sampled settings — at a cost in
power that §8.2 quantifies.

An earlier design had a third element, a flatness gate that chose between the two per axis. We removed it;
§8.2 explains why.

### 8.2 Coverage and power on synthetic ground truth

Because real data provide no ground truth about \(\Delta(z)\), we built a synthetic track in which the
response surface is known and the criteria can be scored directly: 300 repetitions per cell over four surface
families, crossed with true margins \(\Delta_0\) and episode budgets \(n\). **Table 7** reports, per surface,
the minimum coverage, the maximum error rate and the mean declaration rate on cells where the truth is
decidable.

| surface | point calibration | union bound | GP simultaneous band |
|---|---|---|---|
| flat | 0.92 / 0.05 / 0.53 | 1.00 / 0.00 / 0.24 | 1.00 / 0.00 / 0.14 |
| linear | 0.24 / 0.36 / 0.71 | 0.99 / 0.00 / 0.29 | 0.95 / 0.00 / 0.15 |
| dip at a sampled setting | 0.00 / 0.88 / 0.45 | 0.98 / 0.00 / 0.03 | 0.97 / 0.00 / 0.04 |
| dip between sampled settings | 0.00 / 0.85 / 0.43 | **0.22 / 0.17 / 0.21** | 0.91 / 0.00 / 0.08 |

Three results.

**(i) Point calibration's error rate rises with the episode budget.** On any non-flat surface the nominal
interval covers \(\Delta(\hat z)\) rather than the extremes over \(C_\alpha\), so more episodes shrink the
interval around a value that was never the quantity of interest. Concretely: on the linear surface at
\(\Delta_0 = 0.1\) the error rate goes from 0.13 at \(n = 24\) to 0.36 at \(n = 96\); on the sampled-dip
surface at \(\Delta_0 = 0.2\), from 0.26 to 0.88. This is the quantitative form of "more evaluation makes a
wrong conclusion more confident", and it is the cleanest motivation we can offer for the rest of the paper.

**(ii) The union bound attains its guarantee, and only its guarantee.** Where the extremum of \(\Delta(z)\)
falls on a sampled setting it has coverage ≥ 0.98 with error rate 0 and the highest power of any valid rung
(declaration rate 0.98 on the flat surface at \(\Delta_0 = 0.3\), \(n = 96\)). Where the decisive feature
falls *between* sampled settings it fails outright: coverage 0.22 and error rate 0.17. The paper must — and
here does — state its guarantee as sampling-extremum rather than as set-wide.

**(iii) The GP band covers all four families at ≥ 0.91 with error rate 0, and pays for it in power.** Its
declaration rate on the flat surface at \(\Delta_0 = 0.3\), \(n = 96\) is 0.47, and barely grows from
\(n = 48\) to \(n = 96\), because the band extrapolates half a grid step beyond the sampled range and the
posterior diverges at the ends. Restricting the band to the sampled range raises that rate to 0.77 and
restores monotonicity in \(n\), at a coverage cost on the between-settings dip (0.91 → 0.85). We adopt the
restricted configuration.

We also report a configuration we **rejected**, because it is a methodological point rather than a tuning
detail. Imposing a lower bound on the GP length scale equal to the sampling spacing doubles power again
(flat-surface declaration 0.22 → 0.40, linear 0.17 → 0.30) but assumes the surface is smooth at exactly the
scale where the dip families are not, and coverage collapses to 0.45–0.83 with error rates up to 0.10. A
response-surface method's power can be bought only with prior assumptions, and the stronger the prior the
more brittle the method is to the features it did not sample.

Finally, the flatness gate we removed: with 13 design points the GP already fits the sampled-dip surface, so
the gate only lowered coverage on the between-settings surface (0.91–0.98 → 0.89), and it mis-fired on flat
surfaces 16–20% of the time. Its original motivation was that the contact axis has only three sampled points;
the correct response there is to use the union bound on that axis and state its guarantee, not to gate.

### 8.3 Stability on real replicate data

Synthetic ground truth cannot tell us whether the real surfaces resemble any of the four families. So we also
score the criteria on real data by replication: a verdict is *stable* if an independent replicate of the same
evaluation reproduces it. **Table 8**, over the eight replications whose two sides enumerate the same
configuration grid:

| criterion | pairs | stable | contradict | unsupported | declare |
|---|---:|---:|---:|---:|---:|
| point calibration | 8 | 0.50 | 0.00 | 0.50 | 0.38 |
| union bound, controller axes | 8 | 0.88 | 0.00 | 0.12 | 0.06 |
| union bound, all axes | 8 | 1.00 | 0.00 | 0.00 | **0.00** |

Point calibration reproduces half of its own verdicts. The union bound over the controller axes reproduces
0.88 of them. But the last row must be read with its final column: the all-axes union bound achieves perfect
stability by **never declaring anything** on this data. That is not a success, it is the degenerate end of the
conservatism dial, and we report it as such — a criterion that abstains always is perfectly reproducible and
perfectly useless. The useful reading of the table is the middle row, where a real gain in stability
(0.50 → 0.88) is bought with a real loss in declarations (0.38 → 0.06).

> Internal: a reviewer will go straight to that 1.00 and then to the declare column. Saying it first is worth
> more than the row is. The grid-match caveat also belongs in the caption: an earlier version of this table
> included a ninth replication whose two sides used different eggplant orientation grids (8×8 vs 8×3) and so
> compared two different estimands; `track_r_summary.md` carries the correction and the legacy numbers.

### 8.4 The delimiting experiment: a pair the real robot reverses

Everything to this point is internal to the simulator. The criterion is conservative where we can check
conservatism, and stabilises verdicts where we can check stability, but neither test asks whether it protects
against being *wrong about the real robot*. There is one place in this benchmark where that can be asked
without hardware.

The reference implementation publishes real-robot and simulated success rates for the same policies on the
same task. On pick-coke-can the two orderings disagree on three of fifteen policy pairs, all with small real
margins; of those, exactly one has both checkpoints publicly available:

| source | rt-1-converged | rt-1-15pct | margin |
|---|---:|---:|---:|
| published real robot | 0.853 | 0.920 | **−0.067** (15pct better) |
| published simulation | 0.857 | 0.710 | **+0.147** (converged better) |
| our nominal census | 0.863 | 0.717 | +0.147 |

Our reproduction of the published simulated rates is +0.006 and +0.007 — the pipeline reproduces the
disagreement faithfully, which is what makes the pair usable as a test. The question is whether the union
bound *abstains* on a pair the simulator gets wrong. It is the sharpest available test of the criterion,
because we know the answer the simulator should not have given.

We ran both checkpoints over the complete 300-configuration census under nominal conditions plus the two
calibration-invisible conditions that moved verdicts on bridge — the torque limit (exactly invisible, §4.2)
and object friction — for 1,800 episodes total. The result is adverse:

| criterion | set | bound | verdict |
|---|---|---|---|
| point calibration | nominal only | [+0.083, +0.210] | declare converged ≻ 15pct |
| union bound | dynamics compatible set, 3 cells | L = **+0.070**, U = +0.240 | **declare converged ≻ 15pct** |
| published real robot | — | −0.067 | 15pct ≻ converged |

**The criterion declares the ordering the real robot reverses.** Widening from the point to the set moved the
lower bound from +0.083 to +0.070. The three conditions span margins of 0.133 to 0.177 — a total spread of
0.044 — while the correction needed to reach abstention is about 0.21. The torque limit and object friction
are nowhere near the binding constraint on this pair.

Nor does the largest hidden variable we know of rescue it. Because this run puts a second policy on the same
300-configuration grid, it also settles the question left open by §5's texture-variant result: whether a
visual variant that carries no physics can flip a *ranking* rather than merely inflate a single policy's
variance. Adding `urdf_version` as a fourth set dimension (12 cells of 75 configurations each) does turn the
verdict to abstention, L = −0.067 — but the abstention is of the second kind identified in §7.5. All twelve
cells have **positive** point margins, from +0.053 to +0.213, and not one places 15pct above converged with
interval support. The bound reaches zero only through interval width at 75 configurations per cell, so as the
budget grows L tends to +0.053 and the abstention dissolves. By our own test in §7.5 it is our power, not a
parameter fact, and we decline to claim it as a success of the criterion.

The conclusion we draw is about the criterion's reach. The sim-to-real gap on this pair is roughly 0.21 in
the margin, and 0.20 in one policy's own rate (15pct: 0.920 real against 0.717 simulated). No direction in
the dynamics compatible set, and not the texture axis either, moves the simulated margin by more than 0.044.
Whatever produces the reversal lies outside the parameter family that demonstration replay can constrain —
which is, in the ledger of §3.4, a statement that \(b_{ij}\) is large on this pair and that a criterion built
on \(E_\theta\) and \(E_{MC}\) cannot see it.

> Internal: resist the temptation to present the ctrl+vis abstention as the headline. It would be the
> comfortable result and §7.5's own test rules it out. The paper's credibility on the other five sections
> depends on applying that test symmetrically — we used it to withdraw a claim we liked in §7, so we have to
> use it to reject one we would like here.

### 8.5 What the ladder is for

Taken together the three tests place the criterion precisely. It bounds the ambiguity that the calibration
data leaves in the parameters it can represent: there it is conservative by construction (§8.2), it makes
verdicts reproducible where point calibration is a coin flip (§8.3), and it changes the verdict on 3 of 17
pairs at the budgets practitioners use (§7.2). It does not bound, and cannot bound, the ambiguity arising
from a model gap that no setting of those parameters expresses — and §8.4 exhibits a pair where that second
ambiguity is five times the first and points the other way.

We therefore do not recommend the union bound as a device for deciding which policy is better. We recommend
it as a device for detecting when a benchmark's own evidence cannot decide, which is a weaker and more
defensible role, and for which §8.2 and §8.3 are the relevant evidence. A declaration from it is not a
sim-to-real guarantee; §8.4 is the counterexample that makes that sentence necessary.
