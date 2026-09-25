# Prospective secondary half-torque control

This is a separate, locally prospective secondary study, added before any V3 comparative outcomes were inspected. It does not replace, modify or extend the V3 eight-block primary study. There is no external preregistration claim.

## Fixed design and timing

- Task: PutSpoonOnTableClothInScene-v1, the same 24 fixed configurations.
- Policies: Octo-Small and Octo-Base; existing servers, history 2, ensemble enabled, one action executed per query.
- Eight fixed seed bases: 431700100, 557900200, 683100300, 809300400, 947500500, 1089700600, 1231900700, 1393100800. Configuration c uses base + c.
- New condition: arm force limits multiplied by 0.5, nominal arm stiffness and damping, zero external action delay. All gripper/contact/density properties unchanged. Final success at control step 60.
- Additional collection: 8 blocks x 24 configurations x 2 policies = 384 rollouts in 16 complete cells. The comparator is the already planned 384 nominal rollouts in V3. Those baseline episodes are reused and must never be counted twice in the number of unique rollouts. The two studies jointly contain 1,152 unique rollouts if both complete.
- Fresh environment per episode, canonical nominal settling before force assignment, exact initial physical-state and image hashes against all 24 V3 configurations. Actual controller config and SAPIEN joint force/stiffness/damping read back; unchanged gripper/contact/mass; independent policy session reseeded per episode; full source/parameter/server audit.
- The hypotheses are frozen immediately, while V3 collection is ongoing and before any V3 outcome analysis. The separate adapter, execution and analysis code must be frozen before the first half-torque episode. V3 collection finishes without outcome inspection; then the fixed additional experiment launches after its technical gates pass. No result-dependent decision to collect or stop is allowed.
- Fixed maximum collection time: 75 minutes for the 384 new rollouts. A technical failure or incomplete cell makes the secondary result unavailable. No outcome-based restarts, extensions, added seeds or replacement of cells. V3 results remain reportable independently after its full design and audit pass.

## Secondary hypothesis

Within seed block b, let T_b be the Small-minus-Base success-rate gap under half torque minus the Small-minus-Base gap under nominal torque. Each gap is the equal-weight census mean over 24 configurations. T_b lies in [-2, 2]. All eight blocks are used, including ties.

The direction-agnostic null is the intersection P(T_b < 0) <= 1/2 and P(T_b > 0) <= 1/2. Its alternative is that one of the two strict directions occurs with probability greater than 1/2 under the specified independent, identically sampled seed-block working model. A zero belongs to neither strict direction and is never discarded.

Let k_minus and k_plus be the negative and positive block counts. The prespecified p value is min(1, 2 min(P[Binomial(8, 1/2) >= k_minus], P[Binomial(8, 1/2) >= k_plus])). The factor two corrects selection of direction. Eight matching signs yield p = 0.0078125; seven matching signs yield p = 0.0703125. This is a majority-direction repeatability test, not a test of a mean difference, a zero-effect test, or an equivalence test. Non-rejection does not support invariance.

The eight seed blocks are the inference units. Independence and identical sampling of blocks remain assumptions; different integer seeds alone do not establish them. Arbitrary dependence within a block, including across policies, conditions and configurations, is allowed. Sharing V3's nominal baseline makes the two study statistics dependent; it does not invalidate the marginal tests under their stated assumptions.

## Effect estimates and joint reporting

Report all eight exact integer contrast numerators, per-cell successes out of 24, each block shift, and the average shift. Secondary intervals are a Student-t working-model interval with 7 degrees of freedom and a bounded independent-block Hoeffding interval using the full support [-2, 2]. A zero observed block variance does not produce a point confidence interval. These mean intervals do not alter the majority-sign decision.

V3's original one-sided primary p value and this two-sided secondary p value retain their distinct labels. If making a combined two-claim declaration, additionally apply Holm across exactly these two p values at family level 0.05. Holm requires marginally valid p values but not independence, so shared baseline observations are not ignored or treated as independent data. No other result or alternative analysis is selected into this family after inspection.

## Scope and provenance

The study estimates a conditional effect of the declared force-limit perturbation within the corrected, canonical initialization protocol, fixed task/configuration population, policy implementations and simulator build. It does not establish real-world performance, cross-engine transfer, saturation as a mechanism, or a complete six-setting envelope. Historical operating-point effects remain protocol contrasts because their sequential reset behavior can change initial scenes. This separate control cannot retroactively repair historical pairing.

All raw records, frozen sources, technical-validation records and source hashes are retained. No partial success counts, directions or p values will be inspected before the full relevant study is collected. Technical checks inspect only completeness, seeds, states, images, lifecycle events and parameter/source integrity.
