# Draft: Sections 9–10 (2026-09-21)

Spine: `docs/paper_spine_2026-09-21.md`. §9 absorbs the two new entries the fractal result requires; §10
closes on the quantitative comparison that motivates the whole paper.

Written in English for direct transfer to the manuscript; internal notes are in blockquotes.

---

## 9 Limitations

We list these in descending order of how much they should change a reader's confidence, rather than in the
order that flatters the paper.

**1. The criterion's central negative result rests on a single policy pair.** §8.4 shows the union bound
declaring an ordering the real robot reverses, and that is one pair, on one task, on one embodiment. It is
the only pair in this benchmark for which the published real and simulated orderings disagree *and* both
checkpoints are public, so it is the only such test available to us — but a single counterexample establishes
that the criterion's reach is limited, not how often the limit is reached. A reader should conclude that a
union-bound declaration is not a sim-to-real guarantee, and should not conclude that such declarations are
usually wrong. On the 17 pairs where we have no real-robot ground truth we cannot say which way they fall.

**2. No hardware of our own.** Every simulated number here is ours; every real-robot number is quoted from
the reference implementation's published tables. Those are the values the benchmark itself is validated
against, and using them is what makes §8.4 possible without a laboratory, but they carry their own unreported
uncertainty: they are single-protocol real evaluations, and the pair in §8.4 has a real margin of 0.067 which
is of the same order as the seed noise we measure in simulation. We attempted to obtain independent
hardware results through two public evaluation services; one endpoint was offline throughout this work and
the other's queue allocation could not be confirmed (dates and transcripts in App. D). A replication of
§8.4's pair on a real WidowX or Google robot is the single most valuable follow-up, and it is out of our
reach.

**3. Narrow coverage of policies, embodiments and tasks.** Three model families (two Octo variants with three
deployment configurations, OpenVLA, two RT-1 checkpoints), two embodiments, and four tasks. OpenVLA is run
4-bit quantised, which we did not control against a bf16 baseline; the torque mechanism in §7.4 is a claim
about the quantised model as deployed. The dependence of decision-relevance on the task-policy pair (§7.4,
third check) means our coverage is exactly the wrong shape for extrapolation: we show the effect exists on
one task and is nearly absent on another, and we cannot say which of the two is typical.

**4. The strong form of the non-identifiability claim is false in our data.** No calibration-invisible
parameter reverses a sign-determined ranking anywhere we looked (§7.1), and the one between-condition sign
reversal we once claimed did not survive a larger budget (§7.5). The weak form — abstention rather than
reversal — holds, and is concentrated in the low-budget regime.

**5. The compatible set is sampled, not covered.** The union bound evaluates a discrete set of parameter
settings, so its guarantee is of sampling-extremum type, and §8.2 shows it failing (coverage 0.22) precisely
when the decisive feature lies between sampled settings. The GP rung addresses this under a smoothness prior
whose failure mode we also measure. On the contact axis we have three sampled points, which is too few for
the GP rung to be trustworthy, so those axes use the union bound and inherit its limitation.

**6. Low success rates produce many abstentions, and some are ours rather than the data's.** Several tasks sit
at success rates of 0.1 to 0.5, where even a complete 24-configuration census at three seeds gives half-widths
of 0.05 to 0.13. §7.2 documents two disagreements that dissolved when we added seeds, and §8.4 documents an
abstention we declined to claim for the same reason. We have applied the \(h \to 0\) test wherever the budget
allowed, but for the ms2-stack rows of Table 6, which have one run per configuration, we cannot.

**7. Implementation-build drift is separated on two policies only.** The 0.078 figure and the 0.73–0.88
episode-level agreement come from a controlled re-run of two Octo policies across inference-stack versions.
We treat \(\pi\) as an axis of the same kind as \(z\) (§3.1) on that basis, which is thinner evidence than
the rest of §5 rests on.

**8. Part of the platform work is exploratory.** The ManiSkill3/Windows configuration was used for the
sweeps, with the original reference stack used for cross-checking; the two agree on the replay invariances to
sub-millimetre (§4.3) and on the union-bound verdicts in Table 6, but they differ on point verdicts for one
task, and their eggplant configuration grids differ so that per-episode comparison is undefined there. Rows
are labelled by stack throughout and should not be pooled.

> Internal: item 1 must be first. The temptation is to bury a negative about our own criterion below the
> conventional "no hardware" item, and a reviewer who reorders it will trust the rest less.

---

## 10 Conclusion

We asked which ranking claims a calibrated simulation benchmark's own evidence determines, and answered it on
a widely used sim-to-real evaluation suite. The calibration protocol is exactly uninformative about a common
scaling of the joint gains and about the torque limit — 0.141 mm and bitwise zero on two independent
simulator stacks. The benchmark's initial states form a finite population of 24 to 300 configurations rather
than a sample, so enumerating them sets configuration sampling error to zero, and two widely used ports of
the suite enumerate different populations. And following the published protocol exactly reproduces its rates
to 0.026 while showing that its own 72-episode budget resolves one of the four orderings it reports, with a
second reversing sign under re-run.

The quantitative comparison that these three findings converge on is the paper's practical message. On the
eggplant census, a single seed set gives a half-width of ±0.108; the reference protocol's three seeds give
±0.062; ten seeds would give ±0.034. Against that, the shift induced by one calibration-invisible parameter
is 0.141, the spread across the four robot texture variants the benchmark silently averages over is 0.400,
and the sim-to-real gap on the one pair we can check against real ground truth is 0.21 — pointing the other
way. **The terms that evaluation budget can reduce are the small ones.** A practitioner who responds to an
ambiguous benchmark result by running more episodes is buying down the least significant digit, and — on any
non-flat response surface — is making a possibly wrong conclusion more confident while doing so (§8.2).

What we recommend follows from where each term sits. Report the estimand and the budget, because a rate
difference means something different as a benchmark value over an enumerated population than as a
generalisation value over sampled scenes, and the correct interval differs accordingly. Enumerate the
configuration grid, since it is finite and the marginal episode past it carries no information. Report which
implementation build and which visual variant a number came from, because the variant axis turns out to carry
the largest variance in our budget and it is currently averaged over without mention. Spend budget on seeds
before episodes. And use a set-valued verdict — but for the role it can actually fill.

That last point is where our own expectations were corrected. We built the compatible-set criterion expecting
to show that it repairs unreliable rankings, and what we can show is narrower: it detects when a benchmark's
evidence cannot decide, it makes verdicts reproducible where point calibration is a coin flip, and it changes
the answer on 3 of 17 pairs at the budgets practitioners use — falling to 1 of 17 when we spend five seed sets
over a full census. It does not protect against a model gap that no value of the parameters expresses, and on
the single pair where published real-robot results contradict the simulator, it declares the ordering the real
robot reverses. A criterion of this kind bounds the ambiguity it can represent. On at least one pair that is
not the ambiguity that matters, and we know of no way to discover that fact from simulation alone.

> Internal: the last paragraph is the one to protect in revision. It states the limitation of our own
> contribution in the conclusion rather than only in §9, which is the structural choice that makes the rest
> of the paper's numbers believable. If a reviewer asks for a more confident ending, the answer is that the
> confident version is the one T2-A and §8.4 refuted.
