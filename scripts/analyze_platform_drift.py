"""Separate policy-seed noise from platform drift.

Seed sets A (2026-09-18 16:46), B (09-18 23:05) and C (09-19 20:34) differ in their policy seeds AND in the
inference-server generation they were collected on: the XLA determinism flags (--xla_gpu_deterministic_ops,
--xla_gpu_autotune_level=0) and the per-session isolation were added between them. A' (results/
controller_sweep_gpu_replayA) re-runs **A's seeds on today's servers**, so

  A  vs A' : same seeds, different server generation  -> platform drift
  A' vs B, A' vs C : different seeds, same generation -> policy-seed noise

Reports per policy and condition the benchmark value on the shared configurations, the per-episode agreement
between A and A', and the resulting Δ(small − base) under each label.

Usage: python scripts/analyze_platform_drift.py
"""
import argparse
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from task_configs import config_id, n_configs  # noqa: E402

SETS = {"A (09-18 16:46, pre-fix)": "results/controller_sweep_gpu",
        "A' (today, A's seeds)": "results/controller_sweep_gpu_replayA",
        "B (09-18 23:05)": "results/controller_sweep_gpu_rep",
        "C (09-19 20:34)": "results/controller_sweep_gpu_rep3"}
PAIR = ("octo-small", "octo-base")


def load(root, policy, env, cond, limit):
    f = ROOT / root / policy / env / f"{cond}.jsonl"
    d = {}
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                if r["episode_id"] < limit:
                    d.setdefault(r["episode_id"], int(bool(r["success"])))
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default="PutEggplantInBasketScene-v1")
    ap.add_argument("--conditions", default="nominal,force_x0.5")
    ap.add_argument("--out", default="results/controller_sweep_gpu_replayA/analysis_platform_drift.md",
                    help="generated tables only; the narrative lives in FINDING_platform_drift.md and is never overwritten")
    args = ap.parse_args()
    env, conds = args.env, args.conditions.split(",")
    total = n_configs(env)
    L = [f"# Policy-seed noise vs platform drift: {env}, {total}-configuration census", "",
         "A and A' share the policy seeds (base 20260918) and differ only in the server generation; A', B and C "
         "share the generation and differ in seeds. Everything is restricted to episode_id < "
         f"{total} so each set covers each configuration once.", ""]
    data = {}
    for label, root in SETS.items():
        for p in PAIR:
            for c in conds:
                d = load(root, p, env, c, total)
                if d:
                    data[(label, p, c)] = d
    L += ["## Benchmark values", "", "| set | condition | " + " | ".join(PAIR) + " | Δ (small − base) | n |",
          "|---|---|---:|---:|---:|---:|"]
    for label in SETS:
        for c in conds:
            a, b = data.get((label, PAIR[0], c)), data.get((label, PAIR[1], c))
            if not a or not b:
                continue
            eps = sorted(set(a) & set(b))
            L.append(f"| {label} | {c} | {np.mean([a[e] for e in eps]):.3f} | {np.mean([b[e] for e in eps]):.3f} | "
                     f"{np.mean([a[e] - b[e] for e in eps]):+.3f} | {len(eps)} |")
    L.append("")
    L += ["## A vs A': same seeds, different server generation", "",
          "| policy | condition | A | A' | difference | per-episode agreement |", "|---|---|---:|---:|---:|---:|"]
    drift = []
    for p in PAIR:
        for c in conds:
            a = data.get(("A (09-18 16:46, pre-fix)", p, c))
            b = data.get(("A' (today, A's seeds)", p, c))
            if not a or not b:
                continue
            eps = sorted(set(a) & set(b))
            if not eps:
                continue
            ra, rb = np.mean([a[e] for e in eps]), np.mean([b[e] for e in eps])
            agree = np.mean([a[e] == b[e] for e in eps])
            drift.append(rb - ra)
            L.append(f"| {p} | {c} | {ra:.3f} | {rb:.3f} | {rb - ra:+.3f} | {agree:.2f} ({int(agree * len(eps))}/{len(eps)}) |")
    L.append("")
    if drift:
        L += ["## Reading", "",
              f"- Platform drift (same seeds, different generation): mean |change| = {np.mean(np.abs(drift)):.3f}, "
              f"max = {np.max(np.abs(drift)):.3f} over {len(drift)} policy×condition cells.",
              "- Compare with the spread across seed sets on one generation (A', B, C) in the first table: if the A→A' "
              "change is of the same size as the A'/B/C spread, the earlier 'seed set' differences were at least partly "
              "server generation, and seed set A should be replaced by A' in every comparison.", ""]
    text = "\n".join(L)
    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
