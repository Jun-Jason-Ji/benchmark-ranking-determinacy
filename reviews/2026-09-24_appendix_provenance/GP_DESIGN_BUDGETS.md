# Figure 6: observation budgets and source scope

Audit date: 2026-09-24. This report inventories the data consumed by the empirical response-surface analysis without fitting a GP, regenerating figures, or modifying simulation results. The accompanying `GP_DESIGN_BUDGETS.json` contains the exact 13-by-3 design inventory, 78 raw input-file hashes, and six supporting-source hashes.

## Finding

The statement "48 episodes per condition" is not correct for Figure 6. The empirical GP uses **24--96 paired episode observations per design point**, with episode-level standard errors. All 39 budgets independently read from the raw JSONL files exactly match the budgets printed in the retained earlier report `results/controller_sweep_gpu/analysis_response_surface.md`, lines 13--15. Thus the discrepancy is present in the figure's documented analysis scope, not merely a conjecture based on later additions to input files.

The fitting code reads all common episode IDs for Octo-Small and Octo-Base in each condition. It does not cap every cell at 48. The second-version posterior calculation imports that reader, and the submission figure exporter invokes that second version. This correction changes the description of the existing analysis; no new result is supplied by this audit.

## Table suitable for Supplementary Material S1

Entries below are **paired episode observations per policy at each design point**, not total file rows, independent configurations, or independently collected reference-protocol runs. Multipliers are relative to nominal. Common gain scale changes stiffness and damping by the same factor.

| Design point | Carrot | Spoon | Eggplant |
|---|---:|---:|---:|
| Nominal | 48 | 48 | 96 |
| Stiffness ×0.5 | 48 | 48 | 48 |
| Stiffness ×2 | 48 | 48 | 48 |
| Damping ×0.5 | 48 | 48 | 48 |
| Damping ×2 | 48 | 48 | 48 |
| Stiffness ×0.25 | 24 | 24 | 24 |
| Stiffness ×4 | 24 | 24 | 24 |
| Damping ×0.25 | 24 | 24 | 24 |
| Damping ×4 | 24 | 24 | 24 |
| Common gain scale ×0.25 | 96 | 48 | 96 |
| Common gain scale ×0.5 | 96 | 48 | 48 |
| Common gain scale ×2 | 48 | 48 | 48 |
| Common gain scale ×4 | 96 | 48 | 96 |

For carrot and spoon, the initial-configuration population has size 24. Their paired episode counts of 24, 48 and 96 therefore cover all 24 configurations with respectively one, two and four observations per configuration under the per-episode random-seed schedule. For eggplant, the population has size 64: 24 and 48 paired observations cover only 24 and 48 configurations; 96 paired observations cover all 64, with two observations for configurations 0--31 and one for configurations 32--63. Consequently, the old empirical GP analysis combines partial and complete configuration coverage and uses episode-level weighting; it is not the later uniformly weighted configuration-census estimator.

Budget distribution across the 13 design points:

| Task | Points with 24 paired observations | Points with 48 | Points with 96 |
|---|---:|---:|---:|
| Carrot | 4 | 6 | 3 |
| Spoon | 4 | 9 | 0 |
| Eggplant | 4 | 6 | 3 |

## Input selection and verification

- The audit reproduces the existing reader's selection rule: construct a dictionary by episode ID for each policy, then use the intersection of IDs. The code would retain the last record for a duplicated ID, but no duplicates occur in these 78 files.
- For spoon nominal and common scales 0.25 and 4, the Octo-Small files each contain 96 records while Octo-Base has 48. Only the common 48 IDs enter the analysis. Counts of total rows alone would misdescribe those design points.
- All paired IDs in this inventory are contiguous from zero to one less than the reported paired budget. Configuration coverage was computed with the task-specific modulo mapping, separately from observation counts.
- The inventory includes per-policy successes on the paired IDs, unmatched IDs, paired IDs, configuration coverage, and a histogram of observations per configuration. It contains enough detail to distinguish all these counts without rerunning a GP.
- Every one of the 39 current paired budgets agrees with the named observation count in the retained older response-surface report. This verifies the budget description. It does not constitute a new statistical validation of the GP or its episode-level variance assumptions.

## Source IDs and package requirements

| ID | Repository-relative source | Role |
|---|---|---|
| G01 | `results/controller_sweep_gpu/analysis_response_surface.md` | Retained report, including the 39 explicit per-point budgets on lines 13--15 |
| G02 | `scripts/analyze_response_surface.py` | Thirteen design locations, raw-file reader, intersection of episode IDs and episode-level standard errors |
| G03 | `scripts/analyze_response_surface_v2.py` | Imports the same observations; computes and plots the adopted posterior envelope |
| G04 | `scripts/export_submission_figures.py` | Calls the second-version analysis for Figure 6 |
| G05 | `scripts/task_configs.py` | Initial-configuration populations and episode-ID modulo mapping |
| G06 | `results/controller_sweep_gpu/analysis_response_surface_v2.md` | Retained posterior bounds used in the manuscript |

Raw sources GR01--GR78 are listed with full paths and SHA-256 values in the JSON inventory. They cover two policies at each of thirteen design points on each of three tasks. Their ordering follows design point, then task (carrot, spoon, eggplant), then policy (Octo-Small, Octo-Base). The supplementary source archive should contain the six supporting sources and all 78 raw files. The source reports retain historical terminology, which is corrected in the supplement; their original text should not be rewritten to make the record appear cleaner.

## Recommended manuscript wording

> Figure 6 uses an older exploratory sweep with 24--96 paired episode observations per design point and episode-level standard errors. The per-point budgets and configuration coverage are recorded in Supplementary Material S1. This scope differs from the later configuration-census analyses.

The shorter caption wording is:

> Older exploratory sweep; 24--96 paired episode observations per design point, with episode-level standard errors. Budgets and configuration coverage: Supplementary Material S1.

Do not globally replace every reference to a 48-episode sweep: the separate empirical re-evaluation analysis must be checked against its own input selection.
