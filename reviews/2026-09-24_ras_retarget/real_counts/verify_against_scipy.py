"""Optional independent numerical verification, requiring NumPy and SciPy."""
import ast
import json
import math
from pathlib import Path

import numpy as np
import scipy
from scipy.stats import binomtest, pearsonr

import analyze_public_evidence as audit

root = Path(__file__).resolve().parent
data = json.loads((root / "analysis.json").read_text(encoding="utf-8"))
comparisons = []
for n in (24, 25, 27, 60, 75):
    for k in range(n + 1):
        for alpha in (.05, .05 / 6):
            expected = binomtest(k, n).proportion_ci(confidence_level=1-alpha, method="exact")
            actual = audit.clopper_pearson(k,n,alpha)
            comparisons.append(max(abs(actual[0]-expected.low),abs(actual[1]-expected.high)))
assert max(comparisons) < 1e-10
for pair in data["coke_sensitivity"]["hypothetical_paired_tables"]:
    expected = binomtest(pair["converged_only"], pair["converged_only"]+pair["checkpoint15_only"],p=.5).pvalue
    assert abs(expected-pair["exact_two_sided_p"]) < 1e-12

# Compile only the two published summary functions, never any evaluator/robot code.
tree = ast.parse((root / "sources/metrics.py").read_text(encoding="utf-8"))
funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in ("pearson_correlation","mean_maximum_rank_violation")]
module = ast.Module(body=funcs,type_ignores=[])
namespace = {"np":np,"Sequence":list}
exec(compile(module,"frozen_summary_functions","exec"),namespace)
for row in data["correlations"]:
    cells = [c for c in data["cells"] if c["task"] == row["task"] and
             (row["scope"] == "all_published_policies" or c["policy"] != "rt-2-x")]
    real, sim = [c["published_real_rate"] for c in cells],[c["published_sim_rate"] for c in cells]
    assert abs(float(pearsonr(real,sim).statistic)-row["pearson"]) < 1e-12
    assert abs(float(namespace["pearson_correlation"](sim,real))-row["source_pearson"]) < 1e-12
    assert abs(float(namespace["mean_maximum_rank_violation"](sim,real))-row["mmrv"]) < 1e-12
report = dict(passed=True, scipy_version=scipy.__version__, numpy_version=np.__version__,
              clopper_pearson_comparisons=len(comparisons), maximum_absolute_CP_error=max(comparisons),
              exact_mcnemar_tables_checked=len(data["coke_sensitivity"]["hypothetical_paired_tables"]),
              scipy_pearson_and_upstream_summary_rows_checked=len(data["correlations"]))
(root / "INDEPENDENT_NUMERICAL_VERIFICATION.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,indent=2))
