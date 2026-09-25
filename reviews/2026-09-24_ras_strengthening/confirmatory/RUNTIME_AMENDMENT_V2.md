# Runtime amendment, version 2

The locally frozen protocol, seeds, endpoints, sample size, setting grid,
confidence family and decision criteria are unchanged. The first evaluator
completed one cell (PickCube, joint controller, nominal, batch 0) and then failed
at the next environment reset. Its traceback reports PyTorch's prohibition on
an in-place update to an inference tensor outside InferenceMode. Reusing a
controller after a rollout in `torch.inference_mode()` caused this incompatibility.

The version-2 executor changes this context to `torch.no_grad()`, preserving
deterministic actor evaluation without inference-tensor restrictions. Paths and
source-hash validation are updated to separate version-2 outputs. A fresh full
run uses exactly the same prespecified scenes; the original successful cell and
failed execution are retained. The repeated first cell will be compared for
identical physical states and success sequences. No primary outcome summaries
were computed or inspected before this correction. This correction is not
described as an independently preregistered study or hidden by overwriting the
original frozen record. It is a technical amendment after one cell was generated.

The original failed executor consumed 53.38 seconds. The replacement run has a
fixed 1440-second execution limit, keeping combined process runtime below the
original 1500-second compute allocation. Both failures and completed results
remain in the evidence package. The new analysis is the original frozen analysis
with only raw-directory and evaluator/manifest filename substitutions; no
statistical formulas or result-selection logic changed.
