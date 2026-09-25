# Prospective repeatability check of the spoon operating-point effect

This local plan is recorded before collecting any of the new policy-seed outcomes. It is motivated by the historical spoon result; it is not an externally registered study or a new task selection blind to previous results.

## Fixed design

Use the existing validated ManiSkill3 Windows WidowX evaluator, Octo-Small and Octo-Base servers, default two-frame history, all 24 spoon configurations and the registered 60-step final-success criterion. Compare the nominal controller with the previously selected fitted controller (stiffness x2, damping x0.5, one control-step delay). No new parameter search, task selection, threshold tuning or auxiliary fibre sweep is performed.

Evaluate eight new independent policy-seed blocks. Each block uses one seed per configuration; the same seed/configuration is paired across the two policies and two operating points. Seed bases are 431700100, 557900200, 683100300, 809300400, 947500500, 1089700600, 1231900700 and 1393100800. Each block contains 24 configurations x 2 policies x 2 settings = 96 episodes; total 768. These seeds are distinct from all historical sets used in the published comparison. The task's initial configurations deliberately remain the same finite population.

Each policy executes its jobs serially, with two policy workers allowed concurrently after the native-task GPU collection has ended. Setting order alternates across blocks. Each client has a unique session. Every episode checks the server's returned reseeding mode/seed and each step's returned session. Initial simulator states and images are hashed and recorded, along with effective controller settings, code hashes and server metadata. No server is restarted and no service/startup setting is changed.

## Fixed target and analysis

For each complete block b, calculate D_b = (Small - Base at fitted) - (Small - Base at nominal), using equally weighted means over the 24 configurations. The primary confirmatory question is **repeatability of the direction across independent seed blocks**, not a distribution-free assertion about the population mean shift.

Test H0: P(D_b < 0) <= 1/2 with a one-sided exact binomial test on eight blocks, counting zeros as nonnegative. The prespecified alternative is a negative change, motivated by the historical result. Reject at alpha=0.05; seven or eight negative blocks meet this criterion. Give the one-sided exact 95% lower bound for the negative-block probability. This primary test requires independent identically sampled policy-seed blocks; it permits arbitrary dependence within a block and does not test E[D_b]=0.

Report all eight D_b, nominal/fitted policy rates, the mean D, and a two-sided Student-t interval across blocks as a secondary normal-working-model summary. Also show a conservative distribution-free bounded-mean interval over blocks, even if uninformative. Keep any per-configuration analysis secondary and state its dependence assumptions. Do not pool these selected new runs with historical discovery data for the confirmatory test.

The historical declaration/abstention transition and its six-setting envelope are not themselves the primary confirmation target: this small study compares only two operating points. Regardless of p value, report whether the effect's direction and scale repeat, without declaring all original conclusions confirmed.

## Stop and integrity rules

Complete exactly eight blocks. Do not stop for significance or add blocks after inspecting outcomes. A technical failure is logged; preserve incomplete records and retry only missing episodes with the same seed/configuration. If a source/runtime change is needed, record it and test duplicated technical-check records separately. Do not count retries as new independent samples.

Allow up to 150 minutes of evaluation wall time based on historical episode timings. If the complete design cannot be collected, retain the partial data and label the confirmatory result unavailable; do not substitute a partial-test p value. No hardware evaluation or cross-platform equivalence is claimed.
