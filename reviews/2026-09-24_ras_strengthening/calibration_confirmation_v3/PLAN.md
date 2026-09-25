# V3: prospective spoon check with controlled initialization

The separate outcome-blind reset validation passed all 96 prescribed resets, with zero full-state or image mismatches, before V3 collection. The coordinating agent authorized execution after implementation checks. `FROZEN_PLAN.json` records the final pre-execution source versions and time. Preparing or freezing these files does not itself launch policy evaluations.

## Why this is a separate protocol

The preceding attempt in `../calibration_confirmation/` failed its initial physical-state/image pairing gate. Matching episode identifiers did not ensure matching actor poses and velocities. Its preserved outcome-blind inventory is `V2_UNAVAILABLE_INVENTORY.json`; every completed and partial attempt is excluded from confirmatory analysis. No outcome summary, block-direction count or confirmatory p-value was computed to choose this restart.

V3 changes initialization: each episode receives a newly constructed environment, and object settling and episode reset occur under nominal controller parameters. Only after the canonical initial scene has been established are the selected arm-controller parameters applied to the new instance. The adapter must pass a separate outcome-blind test of all 24 configurations, repeated across nominal/fitted orderings, before any V3 rollout. Full initial physical states and initial RGB images must match exactly. Actual built/configured and physical drive parameters must match the selected operating point before the first policy action.

This is a **scope amendment**. V3 asks whether the historical negative operating-point contrast repeats under a controlled-initialization protocol. It does not claim that historical protocol differences isolated the controller effect, and it is not a bit-for-bit reproduction of the earlier reset implementation. The target remains a change in the Small–Base policy gap on this fixed 24-configuration spoon population, conditional on the new reset protocol and fixed execution build. There is no claim of real-world or cross-engine validation.

## Fixed design and unchanged hypotheses

- Task: ManiSkill3 `PutSpoonOnTableClothInScene-v1`, all 24 configured scenes.
- Policies: existing Octo-Small and Octo-Base servers, default two-frame history, action ensembling, execution horizon one. No checkpoint or server change is authorized.
- Conditions: nominal; fitted with stiffness times 2, damping times 0.5, and one control-step delay. Gripper, contact and object-density settings remain nominal.
- Outcome: final-success at exactly 60 control steps; no endpoint change or auxiliary search.
- Eight fixed policy-seed bases: 431700100, 557900200, 683100300, 809300400, 947500500, 1089700600, 1231900700, 1393100800. Episode c uses base+c, paired across policies and conditions.
- Each block has 24 configurations times two policies times two conditions = 96 episodes; total 768. Setting order alternates nominal/fitted and fitted/nominal across successive blocks.
- The same eight bases are retained because the previous attempt was rejected by an outcome-blind technical gate, all its records are excluded, and no outcome-selected seed replacement is made. The restart is disclosed; no failed-attempt observations enter the confirmation.
- One serial worker per policy is allowed, with two policy workers concurrent after other GPU studies have stopped. Each cell uses a distinct policy-client session; every response verifies the intended session and RNG reset. No service is started or reconfigured.

## Primary analysis: repeatability of direction

For complete block b, compute

`D_b = (Small fitted - Base fitted) - (Small nominal - Base nominal)`

from equally weighted means across the 24 configurations. The integer difference of success-count gaps, divided by 24, avoids numerical ambiguity about zero.

The prespecified one-sided test is `H0: P(D_b < 0) <= 1/2`. Count all eight blocks, with zeros nonnegative, and use the exact binomial upper tail at probability 1/2. Seven negative blocks give p=0.03515625; eight give p=0.00390625. Report the one-sided exact 95% lower bound for the negative-block probability. This test assumes independent identically sampled policy-seed blocks, permits arbitrary dependence within a block, and **does not test the mean shift**.

Report every block's four policy/condition rates and difference. Secondary summaries are the mean shift, a two-sided Student-t working-model interval across the eight blocks, and a conservative independent-block Hoeffding interval. The difference of two policy gaps lies in **[-2,2]**, not [-1,1]. A zero observed block variance is not converted into an exact point interval. No per-configuration p-value becomes a primary result.

The historical six-setting envelope and declaration/abstention transition are not confirmation targets. This experiment has only two operating points. It must be described as a locally prospective protocol, not external preregistration.

## Integrity, stopping and amendments

1. Before V3 collection, preserve the validated reset adapter, validation outputs, this plan, runner, launcher, analyzer, tests, imported historical implementation files and all hashes. The entire failed V2 collection remains unchanged in its original directory.
2. Require exact pairing of full initial simulator state and initial RGB image across policy, setting and block for each configuration. Store the state, image digest, actual applied parameters, code digests, runtime metadata, seed, and session. Keep condition-specific metadata and summaries without overwriting other cells.
3. Require 32 complete cells, exactly 24 unique episode IDs per cell, the fixed policy seeds, 60 steps and all technical gates. Technical retries may fill only missing episode IDs with the same seed/configuration. They are not new replicates. Preserve failed attempts and retry events.
4. Finish exactly eight blocks; do not stop for significance, inspect partial directional results, or add blocks. The evaluation wall-time ceiling is 150 minutes, enforced on the remaining subprocess budget. A failed or incomplete design has no confirmatory p-value.
5. Any further technical or scientific change must receive a separate documented amendment. No gate is silently relaxed. Launch occurs only after the reset validation passes and the coordinating agent authorizes execution.

No outcome from V3 is used to alter the design, select conditions or choose which blocks to report. Statistical independence remains a model assumption; seed uniqueness and matched state hashes verify distinct procedural claims.
