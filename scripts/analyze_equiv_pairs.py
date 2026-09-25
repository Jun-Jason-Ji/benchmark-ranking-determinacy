"""Calibration-equivalent condition pairs: conditions that free-space demo replay cannot distinguish
(verified in results/replay_sysid/sweep_v1/iso_invariance.md), compared on policy outcomes.

For each env and policy: paired (by episode_id) success difference between the two members of a pair.
For each env: the policy difference Δ = rate(octo-small) − rate(octo-base) under each member, and the
change of Δ across the pair. If Δ changes sign (with bootstrap support) across a calibration-equivalent
pair, that is a decision-relevant ambiguity witness with exactly equal calibration fit.

Usage: python scripts/analyze_equiv_pairs.py --root results/controller_sweep_gpu --out results/controller_sweep_gpu/analysis_equiv_pairs.md
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

PAIRS = [("stiff_x2.0", "damp_x0.5", "k/d ratio 2"), ("stiff_x0.5", "damp_x2.0", "k/d ratio 0.5"),
         ("force_x0.5", "nominal", "force limit inactive"),
         ("iso_x0.25", "nominal", "iso scale 0.25"), ("iso_x0.5", "nominal", "iso scale 0.5"),
         ("iso_x2.0", "nominal", "iso scale 2"), ("iso_x4.0", "nominal", "iso scale 4"),
         ("fric_x0.4", "nominal", "object friction 0.2"), ("fric_x2.5", "nominal", "object friction 1.25"),
         ("dens_x0.5", "nominal", "object density x0.5"), ("dens_x2.0", "nominal", "object density x2")]
POLICIES = ("octo-small", "octo-base")


def load(root):
    data = {}
    for jsonl in Path(root).rglob("*.jsonl"):
        env, policy, cond = jsonl.parent.name, jsonl.parent.parent.name, jsonl.stem
        eps = {}
        for line in jsonl.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                eps[r["episode_id"]] = int(bool(r["success"]))
        data.setdefault(env, {}).setdefault(policy, {})[cond] = eps
    return data


def boot(d, n=5000, seed=0):
    d = np.asarray(d, float)
    if len(d) == 0:
        return float("nan"), float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    m = d[rng.integers(0, len(d), size=(n, len(d)))].mean(axis=1)
    return float(d.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="results/controller_sweep_gpu")
    ap.add_argument("--out", default="results/controller_sweep_gpu/analysis_equiv_pairs.md")
    ap.add_argument("--envs", default=None, help="comma list to restrict")
    args = ap.parse_args()
    data = load(args.root)
    envs = sorted(data) if not args.envs else args.envs.split(",")
    L = ["# Calibration-equivalent condition pairs vs policy outcomes", "",
         "Pairs are indistinguishable by free-space demo replay (max trajectory difference < 0.1 mm over 40 demos). "
         "Paired by episode_id; bootstrap 95% intervals. Exploratory ManiSkill3/Windows platform.", ""]
    witnesses = []
    for env in envs:
        L += [f"## {env}", ""]
        L += ["### Within-policy: success(A) − success(B) for calibration-equivalent A, B", "",
              "| policy | pair | n | rate A | rate B | diff | 95% |", "|---|---|---:|---:|---:|---:|---|"]
        for pol in POLICIES:
            conds = data.get(env, {}).get(pol, {})
            for a, b, label in PAIRS:
                if a in conds and b in conds:
                    common = sorted(set(conds[a]) & set(conds[b]))
                    if not common:
                        continue
                    da = [conds[a][e] for e in common]; db = [conds[b][e] for e in common]
                    m, lo, hi = boot(np.array(da) - np.array(db))
                    L.append(f"| {pol} | {a} vs {b} ({label}) | {len(common)} | {np.mean(da):.3f} | {np.mean(db):.3f} | {m:+.3f} | [{lo:+.2f}, {hi:+.2f}] |")
        L += ["", "### Between-policy Δ = small − base under each member of the pair", "",
              "| pair | n | Δ under A | 95% | Δ under B | 95% | Δ(A) − Δ(B) | 95% | sign pattern |", "|---|---:|---:|---|---:|---|---:|---|---|"]
        ps, pb = data.get(env, {}).get("octo-small", {}), data.get(env, {}).get("octo-base", {})
        for a, b, label in PAIRS:
            if all(c in ps and c in pb for c in (a, b)):
                ea = sorted(set(ps[a]) & set(pb[a])); eb = sorted(set(ps[b]) & set(pb[b]))
                if not ea or not eb:
                    continue
                dA = np.array([ps[a][e] - pb[a][e] for e in ea]); dB = np.array([ps[b][e] - pb[b][e] for e in eb])
                mA, loA, hiA = boot(dA); mB, loB, hiB = boot(dB)
                common = sorted(set(ea) & set(eb))
                dd = np.array([(ps[a][e] - pb[a][e]) - (ps[b][e] - pb[b][e]) for e in common])
                mD, loD, hiD = boot(dd)
                sA = "+" if loA > 0 else ("−" if hiA < 0 else "0"); sB = "+" if loB > 0 else ("−" if hiB < 0 else "0")
                pattern = f"{sA}/{sB}"
                if (mA > 0 > mB) or (mA < 0 < mB):
                    pattern += " point-flip"
                    if (sA != "0" and sB != "0" and sA != sB):
                        pattern += " CI-supported"
                        witnesses.append((env, a, b))
                L.append(f"| {a} vs {b} ({label}) | {len(common)} | {mA:+.3f} | [{loA:+.2f}, {hiA:+.2f}] | {mB:+.3f} | [{loB:+.2f}, {hiB:+.2f}] | {mD:+.3f} | [{loD:+.2f}, {hiD:+.2f}] | {pattern} |")
        L.append("")
    L += ["## CI-supported ranking flips across calibration-equivalent pairs", ""]
    L += [f"- {e}: {a} vs {b}" for e, a, b in witnesses] if witnesses else ["None so far."]
    text = "\n".join(L)
    Path(args.out).write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
