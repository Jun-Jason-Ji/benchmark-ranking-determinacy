from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
from pathlib import Path
from statistics import NormalDist, mean, variance

FIELDS = {"task", "policy", "condition", "configuration", "replicate", "success"}
ESTIMAND = "equal_configuration_mean_success_difference"


class AuditInputError(ValueError):
    """The input is inconsistent with the declared finite evaluation design."""


def _unique_strings(value, label, minimum=1):
    if not isinstance(value, list) or len(value) < minimum or not all(isinstance(v, str) and v.strip() for v in value):
        raise AuditInputError(f"{label}: expected at least {minimum} nonempty string identifiers")
    if len(set(value)) != len(value):
        raise AuditInputError(f"{label}: duplicate identifiers would double-count observations")
    return value


def _finite_number(value, label):
    if isinstance(value, bool):
        raise AuditInputError(f"{label}: boolean is not a numeric design parameter")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise AuditInputError(f"{label}: expected a finite number") from exc
    if not math.isfinite(number):
        raise AuditInputError(f"{label}: expected a finite number")
    return number


def directional_iut(differences, standard_errors):
    """Normal working-model p value, enforcing one common direction over conditions.

    One-sided evidence is intersected BEFORE the two-direction correction.
    Neither independence across conditions nor paired policies is implied.
    """
    if not differences or len(differences) != len(standard_errors):
        raise AuditInputError("IUT requires nonempty matching effect and uncertainty vectors")
    diffs = [_finite_number(x, "difference") for x in differences]
    ses = [_finite_number(x, "standard error") for x in standard_errors]
    if any(x <= 0 for x in ses):
        raise AuditInputError("IUT requires positive estimated standard errors")
    p_positive = max(.5 * math.erfc(d / se / math.sqrt(2)) for d, se in zip(diffs, ses))
    p_negative = max(.5 * math.erfc(-d / se / math.sqrt(2)) for d, se in zip(diffs, ses))
    return {"positive_iut_p": p_positive, "negative_iut_p": p_negative,
            "two_direction_p": min(1., 2 * min(p_positive, p_negative))}


def holm_adjust(pvalues):
    """Holm adjustment over the full declared family, including unsupported p=1 cases."""
    p = [_finite_number(v, "p value") for v in pvalues]
    if any(v < 0 or v > 1 for v in p):
        raise AuditInputError("p values must be in [0,1]")
    order = sorted(range(len(p)), key=lambda i: (p[i], i))
    out, previous = [1.] * len(p), 0.
    for rank, index in enumerate(order):
        previous = max(previous, min(1., (len(p)-rank)*p[index]))
        out[index] = previous
    return out


def _manifest(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise AuditInputError("manifest schema_version must be 1")
    metadata = data.get("metadata", {})
    if not isinstance(metadata.get("build"), str) or not metadata["build"].strip():
        raise AuditInputError("metadata.build must identify the single implementation build")
    if metadata.get("estimand") != ESTIMAND:
        raise AuditInputError(f"metadata.estimand must be {ESTIMAND!r}")
    for key in ("independent_runs", "independent_policy_evaluations"):
        if not isinstance(metadata.get(key), bool):
            raise AuditInputError(f"metadata.{key} must be explicitly true or false")
    if metadata.get("replicate_unit") != "complete_independent_census_run":
        raise AuditInputError("replicate_unit must identify complete independent census runs, not episodes or configuration IDs")
    tasks = data.get("tasks")
    if not isinstance(tasks, dict) or not tasks:
        raise AuditInputError("manifest.tasks must be a nonempty object")
    for task, spec in tasks.items():
        if not isinstance(task, str) or not task:
            raise AuditInputError("task identifiers must be nonempty strings")
        for field in ("policies", "conditions", "configurations", "replicates"):
            _unique_strings(spec.get(field), f"{task}.{field}", 2 if field == "policies" else 1)
    return data


def audit_csv(csv_path, manifest_path, alpha=.05):
    alpha = _finite_number(alpha, "alpha")
    if not 0 < alpha < 1:
        raise AuditInputError("alpha must be strictly between zero and one")
    plan = _manifest(manifest_path)
    metadata, tasks = plan["metadata"], plan["tasks"]
    observations = {}
    with Path(csv_path).open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None or set(reader.fieldnames) != FIELDS or len(reader.fieldnames) != len(FIELDS):
            raise AuditInputError("CSV columns must be exactly task,policy,condition,configuration,replicate,success")
        for line, row in enumerate(reader, 2):
            if None in row or any(row[f] is None for f in FIELDS):
                raise AuditInputError(f"line {line}: missing or extra CSV cells")
            task = row["task"]
            if task not in tasks:
                raise AuditInputError(f"line {line}: task not in manifest")
            for singular, plural in (("policy","policies"),("condition","conditions"),("configuration","configurations"),("replicate","replicates")):
                if row[singular] not in tasks[task][plural]:
                    raise AuditInputError(f"line {line}: {singular} not in the predeclared inventory")
            key = tuple(row[f] for f in ("task","policy","condition","configuration","replicate"))
            if key in observations:
                raise AuditInputError(f"line {line}: duplicate observation key; repeated rows are not independent runs")
            value = _finite_number(row["success"], f"line {line} success")
            if value not in (0., 1.):
                raise AuditInputError(f"line {line}: success must be binary 0 or 1")
            observations[key] = value

    coverage, pairs = [], []
    z = NormalDist().inv_cdf(1-alpha/2)
    for task, spec in tasks.items():
        expected = list(itertools.product([task], spec["policies"], spec["conditions"],spec["configurations"],spec["replicates"]))
        missing = [list(key) for key in expected if key not in observations]
        complete = not missing
        summaries = {}
        for policy, condition in itertools.product(spec["policies"],spec["conditions"]):
            run_means = {}
            for replicate in spec["replicates"]:
                keys = [(task,policy,condition,c,replicate) for c in spec["configurations"]]
                if all(k in observations for k in keys):
                    run_means[replicate] = mean(observations[k] for k in keys)
            summaries[(policy,condition)] = run_means
        coverage.append({"task":task,"expected_observations":len(expected),
                         "observed_observations":len(expected)-len(missing),"complete_inventory":complete,
                         "expected_configurations":len(spec["configurations"]),
                         "expected_conditions":len(spec["conditions"]),
                         "expected_runs_per_policy_condition":len(spec["replicates"]),
                         "missing_observations":missing,
                         "complete_runs":[{"policy":p,"condition":c,"n":len(r)} for (p,c),r in summaries.items()]})
        for a,b in itertools.combinations(spec["policies"],2):
            reasons = []
            if not complete:
                reasons.append("incomplete_predeclared_inventory")
            if not metadata["independent_runs"]:
                reasons.append("independent_run_assumption_not_supported")
            if not metadata["independent_policy_evaluations"]:
                reasons.append("independent_policy_assumption_not_supported")
            if len(spec["replicates"]) < 2:
                reasons.append("fewer_than_two_independent_census_runs")
            estimates = []
            for condition in spec["conditions"]:
                ra, rb = list(summaries[(a,condition)].values()),list(summaries[(b,condition)].values())
                # Descriptive averages are only formed from COMPLETE planned runs;
                # no partial configuration mean is silently substituted.
                gap = mean(ra)-mean(rb) if ra and rb else None
                entry = {"condition":condition,"mean_a":mean(ra) if ra else None,
                         "mean_b":mean(rb) if rb else None,"gap":gap,
                         "runs_a":len(ra),"runs_b":len(rb),"standard_error":None,"interval":None}
                if not reasons:
                    se2 = variance(ra)/len(ra)+variance(rb)/len(rb)
                    if se2 <= 0:
                        reasons.append(f"zero_empirical_variance:{condition}")
                    else:
                        entry["standard_error"] = math.sqrt(se2)
                estimates.append(entry)
            item = {"task":task,"policy_a":a,"policy_b":b,"conditions":estimates,
                    "eligible":not reasons,"unsupported_reasons":reasons,"envelope":None,
                    "unadjusted_verdict":"abstain_unsupported" if reasons else "abstain",
                    "raw_p":1.,"iut":None}
            if not reasons:
                for entry in estimates:
                    d,se = entry["gap"],entry["standard_error"]
                    entry["interval"] = [d-z*se,d+z*se]
                lo = min(e["interval"][0] for e in estimates)
                hi = max(e["interval"][1] for e in estimates)
                item["envelope"] = [lo,hi]
                item["iut"] = directional_iut([e["gap"] for e in estimates],[e["standard_error"] for e in estimates])
                item["raw_p"] = item["iut"]["two_direction_p"]
                item["unadjusted_verdict"] = "a_better" if lo > 0 else ("b_better" if hi < 0 else "abstain")
            else:
                # Never leak a partially computed interval from a failed complete-envelope gate.
                for entry in estimates:
                    entry["standard_error"] = None
            pairs.append(item)
    adjusted = holm_adjust([p["raw_p"] for p in pairs])
    for pair,padj in zip(pairs,adjusted):
        pair["holm_adjusted_p"] = padj
        pair["holm_verdict"] = pair["unadjusted_verdict"] if pair["eligible"] and padj <= alpha else (
            "abstain" if pair["eligible"] else "abstain_unsupported")
    return {"schema_version":1,"metadata":metadata,"alpha":alpha,
            "input_sha256":{"csv":hashlib.sha256(Path(csv_path).read_bytes()).hexdigest(),
                            "manifest":hashlib.sha256(Path(manifest_path).read_bytes()).hexdigest()},
            "inference":"Normal working model with estimated variance across complete independent census runs; no finite-sample or real-world coverage guarantee.",
            "family":"All manifest policy pairs across all manifest tasks, including unsupported pairs with p=1.",
            "family_size":len(pairs),"coverage":coverage,"pairs":pairs,
            "limitations":["Manifest assertions do not verify build identity or independence in the physical data.",
                           "Replicate IDs are run labels, not proof of independence; shared seeds do not establish policy pairing.",
                           "Complete configuration coverage does not eliminate stochastic policy variation.",
                           "Two runs are a minimum for variance estimation, not evidence that a normal approximation is accurate.",
                           "No inference outside the declared finite condition/configuration inventory; no sim-to-real bias certificate."]}


def allocate(plan):
    """Continuous cost-weighted Neyman allocation for a fixed weighted mean.

    Minimise sum_i (w_i sigma_i)^2 / n_i subject to sum_i c_i n_i = B.
    This is not a discrete or globally optimal robot experimental design.
    """
    budget = _finite_number(plan.get("budget"), "budget")
    if budget <= 0:
        raise AuditInputError("budget must be positive")
    rows = plan.get("strata")
    if not isinstance(rows,list) or not rows:
        raise AuditInputError("strata must be a nonempty list")
    _unique_strings([r.get("id") for r in rows],"stratum IDs")
    clean = []
    for r in rows:
        w,s,c = [_finite_number(r.get(k),f"{r['id']}.{k}") for k in ("weight","sigma","cost")]
        if w < 0 or s < 0 or c <= 0:
            raise AuditInputError("weights and sigmas must be nonnegative; costs strictly positive")
        clean.append({"id":r["id"],"weight":w,"sigma":s,"cost":c})
    if not math.isclose(sum(r["weight"] for r in clean),1.,rel_tol=0.,abs_tol=1e-9):
        raise AuditInputError("weights must sum to one for the declared weighted-mean estimand")
    denominator = sum(r["weight"]*r["sigma"]*math.sqrt(r["cost"]) for r in clean)
    if denominator <= 0:
        raise AuditInputError("all weighted pilot sigmas are zero; no supported allocation preference")
    predicted_variance = 0.
    for r in clean:
        r["continuous_runs"] = budget*r["weight"]*r["sigma"]/(math.sqrt(r["cost"])*denominator)
        r["allocated_cost"] = r["cost"]*r["continuous_runs"]
        if r["continuous_runs"] > 0:
            predicted_variance += (r["weight"]*r["sigma"])**2/r["continuous_runs"]
    return {"schema_version":1,"budget":budget,"allocated_cost":sum(r["allocated_cost"] for r in clean),
            "strata":clean,"model_predicted_variance":predicted_variance,
            "objective":"Minimise weighted-mean variance under fixed pilot variances and independent stratum sampling.",
            "limitations":["Continuous allocation only; rounding, minimum replication and fixed setup costs are not solved.",
                           "Pilot sigmas are treated as known; zero estimates are not proof of deterministic outcomes.",
                           "Does not optimise task/configuration selection, ranking error, set width, or a complete robot validation design.",
                           "No sample-size or power guarantee is implied."]}
