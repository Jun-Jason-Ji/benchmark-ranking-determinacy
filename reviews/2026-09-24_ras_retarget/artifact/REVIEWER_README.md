# Reviewer entry point: local policy-ranking audit component

This artifact is a small analysis component accompanying the manuscript. It provides an explicit input contract and protected ranking decisions for repeated finite configuration censuses. It does not run a robot simulator, download checkpoints, contact a service, or claim automatic support for arbitrary benchmarks.

## Contents

- [Package scope and statistical assumptions](policy_rank_audit/README.md).
- [Locally installable wheel](policy_rank_audit/dist/policy_rank_audit-0.1.0-py3-none-any.whl), version 0.1.0. It has no runtime dependencies and has not been published on PyPI.
- [Source code](policy_rank_audit/src/policy_rank_audit/core.py) and [CLI](policy_rank_audit/src/policy_rank_audit/cli.py).
- [Input manifest](policy_rank_audit/examples/manifest.json), [complete synthetic CSV](policy_rank_audit/examples/complete.csv), and [incomplete synthetic CSV](policy_rank_audit/examples/incomplete.csv).
- [Complete-example output](policy_rank_audit/checks/complete_audit.json), [incomplete-example output](policy_rank_audit/checks/incomplete_audit.json), and [allocation output](policy_rank_audit/checks/allocation.json).
- [Tests](policy_rank_audit/tests/test_audit.py) and [installation/test/CLI verification record](policy_rank_audit/checks/verification.json).

All example CSV outcomes are explicitly synthetic. They demonstrate software behaviour and do not add robot evidence to the paper. The manuscript's historical experiments retain their original estimands and inference units; this artifact has not silently replaced their analysis.

## Five-minute reproduction

Use Python 3.10 or newer. From the `policy_rank_audit` directory:

```sh
python -m pip install --no-index --no-deps dist/policy_rank_audit-0.1.0-py3-none-any.whl
policy-rank-audit audit examples/complete.csv --manifest examples/manifest.json --out complete_audit.json
policy-rank-audit audit examples/incomplete.csv --manifest examples/manifest.json --out incomplete_audit.json
policy-rank-audit allocate examples/allocation.json --out allocation.json
python -m unittest discover -s tests -v
```

The complete 144-row example declares A better than B after Holm correction and abstains on the other two pairs. The incomplete 143-row example intentionally exits with code 2, writes a missing-inventory diagnostic, and supplies no complete envelope. The allocation illustration spends its continuous budget of 100 exactly. Twelve targeted tests pass in the supplied verification record.

## What a reviewer should inspect

The manifest declares one implementation build, the equal-configuration mean-difference estimand, all expected cells and the independent complete-run unit. Missing cells, duplicate rows, unsupported independence, fewer than two runs, and zero empirical variance cannot generate an apparently certain interval. Direction is enforced before the two-direction correction; Holm uses the full declared pair family, including unsupported cases.

Where supported by the input declarations, uncertainty is a normal working-model estimate across complete independent runs. Two runs are only the minimum required to estimate variance; they do not justify accurate normal approximation. Neither finite-sample coverage nor a bound on sim-to-real bias is supplied. The allocation utility solves only a continuous fixed-variance weighted-mean problem, not a complete robot-experiment or power-design problem.

The verification record includes the installed wheel hash. Installation was checked in a project-local target and did not alter the simulator environments or publish the package externally.
