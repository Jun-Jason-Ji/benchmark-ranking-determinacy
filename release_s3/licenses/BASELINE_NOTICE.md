# Third-party components

This release is a code-and-aggregate release. It vendors no upstream source and redistributes no
model weights or simulator assets: `third_party/`, `data/` and `checkpoints/` are excluded from the
archive. The components below are obtained from their own upstreams and are governed by their own
licences and terms, which take precedence over this repository's licence for anything derived from
them.

Licence names are deliberately not asserted here. Check each upstream at the version you use — they
change, and a stale claim in a NOTICE file is worse than none.

| Component | Used for | Upstream |
|---|---|---|
| SimplerEnv | the evaluation suite under study; source of the published real and simulated reference rates in `simpler_env/utils/metrics.py` | github.com/simpler-env/SimplerEnv |
| ManiSkill2 / ManiSkill2_real2sim | the original reference simulator stack (Sects. 4, 6, 8.4) | github.com/haosulab/ManiSkill2 |
| ManiSkill3 | the second simulator port (the controller sweeps) | github.com/haosulab/ManiSkill |
| SAPIEN | physics and rendering backend for the original stack | github.com/haosulab/SAPIEN |
| Octo | evaluated policy, two sizes and three deployment configurations | github.com/octo-models/octo |
| OpenVLA | evaluated policy, run 4-bit quantised | github.com/openvla/openvla |
| RT-1 checkpoints (`rt-1-converged`, `rt-1-15pct`, `rt-1-x`) | evaluated policies; the reversal pair of Sect. 8.4 | distributed with SimplerEnv |
| BridgeData V2 | the 98 demonstrations replayed for calibration (Sect. 4.3) | rail-berkeley.github.io/bridgedata |

## Our own additions

- `third_party/vk_fakesemfd/` — a Vulkan layer that fakes `VK_KHR_external_semaphore_fd` so the
  original stack renders headless on a host without a GPU (Appendix B). Written for this work.
- `scripts/`, `benchmark/` — the harness, queues and analyses. Written for this work.

## On the real-robot reference values

Section 8.4 compares against real-robot success rates that are published as part of the benchmark's
own source and are not ours to redistribute. The manuscript cites their location; this release does
not copy them.
