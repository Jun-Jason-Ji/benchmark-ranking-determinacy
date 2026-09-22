"""Extract published aggregate scores without executing third-party source.

These are upstream reported results, not new robot or simulator executions.
"""
import ast
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "third_party/SimplerEnv/simpler_env/utils/metrics.py"
OUT = ROOT / "research_audit"


def literal_tables(source):
    found = {}
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in {"REAL_PERF", "SIMPLER_PERF"}:
                    found[target.id] = ast.literal_eval(node.value)
    if set(found) != {"REAL_PERF", "SIMPLER_PERF"}:
        raise ValueError("Expected literal upstream result tables were not found")
    return found


def main():
    OUT.mkdir(exist_ok=True)
    raw = SOURCE.read_bytes()
    tables = literal_tables(raw.decode())
    rows = []
    for task, policies in tables["REAL_PERF"].items():
        for policy, real in policies.items():
            rows.append({
                "task": task, "policy": policy,
                "real_success_reported": real,
                "sim_success_reported": tables["SIMPLER_PERF"][task][policy],
                "public_checkpoint_candidate": policy != "rt-2-x",
                "reexecution_status": "not_executed",
                "real_trial_count": "unknown_pending_protocol_audit",
                "score_version": "original_SIMPLER_Octo_1.0_not_1.5",
            })
    with (OUT / "simpler_published_scores.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "source_url": "https://github.com/simpler-env/SimplerEnv/blob/06accaca93535902d408da4855f21cece12bceb7/simpler_env/utils/metrics.py",
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "tasks": len(tables["REAL_PERF"]), "task_policy_cells": len(rows),
        "public_checkpoint_candidate_cells": sum(r["public_checkpoint_candidate"] for r in rows),
        "excluded_from_reexecution": ["rt-2-x"],
        "evidence": "Upstream published aggregate scores; not new observations",
        "limitations": [
            "Checkpoint availability does not prove weight/version and control protocol alignment.",
            "Octo 1.5 checkpoints must not be matched to original Octo 1.0 labels.",
            "Trial counts and scene strata not inferred from rounded success rates.",
            "Do not synthesize episodes from aggregate means for cluster bootstrap.",
        ],
    }
    (OUT / "simpler_manifest.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
