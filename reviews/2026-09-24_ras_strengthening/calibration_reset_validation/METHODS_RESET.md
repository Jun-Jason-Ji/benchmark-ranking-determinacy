# Controlled initialization for the local calibration comparison

## Suggested manuscript wording

An outcome-blind integrity check identified unmatched initial states in the
first attempted confirmation. Matching configuration identifiers and policy
seeds was insufficient under the inspected sequential-reset implementation.
In the first completed block, nominal Octo-Base versus nominal Octo-Small
matched both the full-state and image hashes in 6 of 24 configurations; nominal
versus fitted Octo-Small matched in 10 of 24. The latter comparison included
initial actor differences of up to 23.2 mm and 35.8 degrees. The affected
collection failed its prespecified pairing gate and was excluded from
confirmatory outcome analysis; its records were retained.

We therefore defined a controlled-initialization protocol. Each episode uses a
new environment constructed and reset with nominal robot and contact
parameters. After settling and generation of the initial observation, the
requested arm stiffness and damping are assigned to that environment's
controller and physical joints. No simulation step occurs between this
assignment and the start of evaluation. Force limits, gripper parameters,
object masses and contact materials remain unchanged. Execution delay is
implemented separately by the episode's action queue. Every environment is
closed before the next episode is constructed, and controller references are
obtained from the current instance.

Before collecting outcomes for the controlled protocol, we tested all 24 spoon configurations in
four passes, nominal/fitted/fitted/nominal, comprising 96 fresh constructions
inside one process. For every configuration, all four full initial-state
dictionaries and initial RGB images were exactly identical. Controller
configuration and physical-joint readback agreed; gripper and object properties
were unchanged, and controller reset preserved the applied gains and initial
state. These checks validate the controlled initialization for this recorded
implementation, without assuming that configuration identifiers alone establish
physical pairing. The subsequent comparison concerns this explicitly controlled
protocol rather than a reproduction of historical sequential-reset results.
Two additional Python processes independently recreated the 24 nominal and 24
fitted initializations, respectively; all 48 states and images also matched the
saved canonical references exactly.

## Interpretation boundary

The installed source provides a plausible mechanism: the general reset clears
robot velocities without necessarily restoring joint positions, while the
Bridge task settles its objects before assigning its prescribed robot pose.
Consequently, prior episode state could affect the following reset. This is a
source-supported causal hypothesis, not an isolated causal demonstration. The
fresh-environment validation establishes a practical way to obtain identical
initial conditions; it does not separately identify which component of the old
reset path caused each discrepancy. The diagnosis applies to the inspected
ManiSkill3 path, not the original ManiSkill2 implementation.

Historical comparisons without recorded, paired physical initial states remain
descriptions of their executed protocols. Their differences should not be
attributed solely to the changed controller operating point. The controlled
follow-up needs its own frozen protocol and complete analysis, regardless of
whether its direction agrees with the earlier observations.

## Technical evidence and timing

- Source/plan freeze: `FROZEN_TECHNICAL_PROTOCOL.json`, recorded before this test.
- Complete records: `reset_records.jsonl`; 24 canonical input PNGs are preserved.
- 96/96 exact full-state and image matches; no policy requests and no success
  fields read. `AUDIT.json` independently verifies the saved states, decoded PNG
  hashes, parameter assignments, object properties and source hashes on CPU.
- Additional cross-process tests: `CROSS_PROCESS_nominal.json` and
  `CROSS_PROCESS_fitted.json`; both are 24/24 exact matches. These follow-up
  technical checks were recorded separately from the original 96-test protocol.
- Fitted gains are stiffness ×2 and damping ×0.5; force limits are nominal.
  Simulation and control frequencies are 500 Hz and 5 Hz.
- Total validation time: 31.56 s, including close/check/log/image-save overhead.
  Mean construction/reset time: 0.195 s; median 0.190 s; maximum 0.849 s.
  For 768 episodes, construction/reset alone projects to approximately 150 s.
  Scaling the full validation wall time gives approximately 253 s, including
  test-only recording overhead; neither estimate includes policy inference or
  rollout time.
- Validated adapter: `fresh_reset.py`, SHA-256
  `eaf31d93d9ab7486b9b88ab0c486b4407d5878b01df9e9e7967c895a98a35fa1`.

The exact earlier maxima reported by the initial-state audit are 23.1956 mm and
35.7537 degrees for nominal versus fitted Octo-Small, and 15.3554 mm and 23.1980
degrees for the two nominal policies. These are initial actor-state
discrepancies, not policy performance differences.
