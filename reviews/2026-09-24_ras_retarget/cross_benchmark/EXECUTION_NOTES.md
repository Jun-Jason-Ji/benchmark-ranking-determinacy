# Execution notes

- Native GPU smoke passed after loading the unchanged official PhysX GPU DLL from
  this audit directory, bypassing the default user-cache path. No global package,
  driver, service, or autostart setting was changed. The upstream ManiSkill support
  matrix still lists Windows GPU simulation as unsupported; successful execution
  here is evidence for this recorded local build, not a claim of vendor support
  or equality to the training build. This must remain a limitation of the check.
- During the PickCube grid, static inspection found that PushCube names the cube
  actor `obj` and its target `goal_region`, whereas PickCube uses `cube` and
  `goal_site`. The logger was generalized before any PushCube grid run to record
  those equivalent initial-state fields. Physics, actor inference, setting values,
  seeds, and outcomes were unchanged. Each record retains its evaluator hash.
- Training metadata identifies the original policy-export ManiSkill commit as
  `baab60ede2e89167c1b7aaed41a9aa8e690a9d1e`; evaluation uses installed 3.0.1.
  Nominal pilot performance is therefore an interface check, not reproduction of
  an original published PPO success rate.
- Sampling clarification from source inspection: the task draws object/goal
  coordinates from a batched torch stream initialized by the first reset seed;
  the enhanced-determinism robot joint initialization also uses its per-slot RNG.
  Thus each recorded `reset_seed` is the requested vector seed argument, not a
  promise that running that scalar seed alone reconstructs the same entire scene.
  The scientific unit is a sampled initial physical state, identified by its
  recorded joint/object/goal state and slot in the fixed-size batch. Prefix-budget
  analyses use prefixes of this frozen sample, not reruns with fewer vector slots.
- Final audit distinguished the prespecified final-step outcome from the
  prospectively logged ever-success diagnostic used prominently by official PPO
  examples. PushCube joint PPO reaches success on 256/256 nominal scenes but
  retains it at step 50 on 2/256. Cartesian PPO has 200/256 ever-success and 78/256
  final success. All settings and both definitions are reported; the endpoint
  was not changed to obtain a preferred ordering. Additional interval analysis
  across definitions is a secondary sensitivity analysis without a simultaneous
  post-selection guarantee across metrics.
- The export-commit actor class and official vector wrapper independently
  reproduced both nominal PushCube outcome vectors (0 disagreements for either
  final or ever success). Historical/current observation arrays agreed exactly
  at every control step. Action bounds, control frequency, physics frequency,
  horizon, truncation and manually recomputed goal-distance/height predicates
  were checked. Current PushCube allows 5 mm rather than 1 mm height tolerance;
  substituting the old criterion leaves both nominal counts unchanged. Changed
  training rewards do not enter inference. This rules out the checked interface
  bugs; it does not identify every cause of historical/current performance drift.
- The complete primary grid comprises 5120 rollouts. The nominal feasibility
  pilot comprises 32 distinct rollouts; parity verification repeats 512 existing
  scene/pipeline combinations and contributes no new independent evidence.
- Raw records retain the evaluator's initial `experiment` string ending in
  `pilot`; this is an inherited metadata label, not a description of the full
  grid's scope. The `args`, path, frozen PLAN, GRID_PROGRESS and 256 per-cell
  records identify the complete grid. Original outcome files remain unchanged.
- The first evaluator version is preserved byte-for-byte under
  `run_native_policies_v1.py` and matches SHA256
  `8a4ce14d3fd7aa2e5476c857781a599252b116e53d3f5916d8ba76facacd90fd`.
  The source hash in each episode file was evaluated at result serialization;
  a process spanning the logger-only edit could therefore record the later hash.
  Both versions have identical PickCube execution and logging semantics, and no
  PushCube primary cell started before the field-name accommodation was in place.
