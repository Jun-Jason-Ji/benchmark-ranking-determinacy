"""Track R: real sweep data, no ground truth. Methods are scored by verdict STABILITY across independent
replications: (a) two policy-seed sets on the same platform (results/controller_sweep_gpu vs _rep), and
(b) two simulation stacks with the same seeds (ManiSkill3 vs original SIMPLER main, results/controller_sweep_ms2).

For every dataset, policy pair and method we compute the verdict on replicate A and on replicate B and report:
  stable      = P(verdict_A == verdict_B)
  contradict  = P(both declared, opposite signs)
  unsupported = P(declared on one replicate, abstain on the other)
  declare     = P(declared) averaged over replicates
Methods: point (nominal CI), union_ctrl (min/max CI over the controller-invisible conditions iso x0.25, iso x4,
force x0.5), union_all (all five calibration-invisible conditions). A frozen manifest of the input files
(path, episodes, md5) is written next to the results.

Config grids (2026-09-19): a replication is only a replication when both sides evaluate the same initial
configurations. The two stacks share the spoon and carrot grids exactly (12 positions x 2 orientations), but NOT
the eggplant grid: ManiSkill3 uses 8 positions x 8 orientations while the original stack uses 8 x 3 with different
quaternions, so eggplant_stacks compares different benchmarks and is reported separately, not in the headline
aggregate. See results/controller_sweep_gpu_rep3/FINDING_seed_set_bug.md.

Usage: python benchmark/decidability_bench/run_track_r.py --n 48 --out results/benchmark/track_r"""
import argparse
import hashlib
import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

CONDS_CTRL = ["iso_x0.25", "iso_x4.0", "force_x0.5"]
CONDS_ALL = ["iso_x0.25", "iso_x4.0", "force_x0.5", "fric_x0.4", "dens_x0.5"]
DATASETS = [
    dict(name="eggplant_seedsets", kind="seed sets 20260918 vs 20270101 (ManiSkill3)",
         A=("results/controller_sweep_gpu", "PutEggplantInBasketScene-v1"), B=("results/controller_sweep_gpu_rep", "PutEggplantInBasketScene-v1"),
         policies=["octo-small", "octo-base", "octo-small@hist1", "octo-base@hist1"], grid_match=True),
    dict(name="eggplant_stacks", kind="ManiSkill3 vs original SIMPLER main (same seeds)",
         A=("results/controller_sweep_gpu", "PutEggplantInBasketScene-v1"), B=("results/controller_sweep_ms2", "PutEggplantInBasketScene-v0"),
         policies=["octo-small", "octo-base"], grid_match=False),  # 8x8 vs 8x3 orientations: different benchmarks
    dict(name="spoon_stacks", kind="ManiSkill3 vs original SIMPLER main (same seeds)",
         A=("results/controller_sweep_gpu", "PutSpoonOnTableClothInScene-v1"), B=("results/controller_sweep_ms2", "PutSpoonOnTableClothInScene-v0"),
         policies=["octo-small", "octo-base"], grid_match=True),
    dict(name="carrot_stacks", kind="ManiSkill3 vs original SIMPLER main (same seeds)",
         A=("results/controller_sweep_gpu", "PutCarrotOnPlateInScene-v1"), B=("results/controller_sweep_ms2", "PutCarrotOnPlateInScene-v0"),
         policies=["octo-small", "octo-base"], grid_match=True),
]
RNG = np.random.default_rng(0)


def load(root, policy, env, cond, n):
    f = ROOT / root / policy / env / f"{cond}.jsonl"
    d = {}
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                if r["episode_id"] < n:
                    d.setdefault(r["episode_id"], int(bool(r["success"])))
    return d


def manifest_entry(root, policy, env, cond, n):
    f = ROOT / root / policy / env / f"{cond}.jsonl"
    if not f.exists():
        return None
    b = f.read_bytes()
    return dict(path=str(f.relative_to(ROOT)).replace("\\", "/"), bytes=len(b), md5=hashlib.md5(b).hexdigest(), episodes_used=len(load(root, policy, env, cond, n)))


def ci(a, b, nb=10000):
    e = sorted(set(a) & set(b))
    if len(e) < 12:
        return None
    d = np.array([a[i] - b[i] for i in e], float)
    m = d[RNG.integers(0, len(d), size=(nb, len(d)))].mean(1)
    return float(d.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def sign(lo, hi):
    return "+" if lo > 0 else ("−" if hi < 0 else "0")


def verdicts(root, env, pa, pb, n):
    out = {}
    nom = ci(load(root, pa, env, "nominal", n), load(root, pb, env, "nominal", n))
    out["point"] = sign(nom[1], nom[2]) if nom else None
    for name, conds in (("union_ctrl", CONDS_CTRL), ("union_all", CONDS_ALL)):
        cis = [ci(load(root, pa, env, c, n), load(root, pb, env, c, n)) for c in conds]
        cis = [c for c in cis if c]
        if len(cis) < len(conds):
            out[name] = None
        else:
            out[name] = sign(min(c[1] for c in cis), max(c[2] for c in cis))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=48)
    ap.add_argument("--out", default="results/benchmark/track_r")
    args = ap.parse_args()
    out = ROOT / args.out
    out.mkdir(parents=True, exist_ok=True)
    manifest, rows = [], []
    for ds in DATASETS:
        (rootA, envA), (rootB, envB) = ds["A"], ds["B"]
        for p in ds["policies"]:
            for c in ["nominal"] + CONDS_ALL:
                for root, env in ((rootA, envA), (rootB, envB)):
                    e = manifest_entry(root, p, env, c, args.n)
                    if e:
                        manifest.append(e)
        for pa, pb in itertools.combinations(ds["policies"], 2):
            va, vb = verdicts(rootA, envA, pa, pb, args.n), verdicts(rootB, envB, pa, pb, args.n)
            for m in ("point", "union_ctrl", "union_all"):
                if va[m] is None or vb[m] is None:
                    continue
                rows.append(dict(dataset=ds["name"], kind=ds["kind"], grid_match=ds["grid_match"], pair=f"{pa} vs {pb}", method=m, A=va[m], B=vb[m]))
    (out / "track_r_manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    (out / "track_r_rows.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
    L = [f"# Track R: verdict stability on real sweep data (episodes 0-{args.n - 1})", "",
         "No ground truth: a method is scored by whether its verdict on one replicate is reproduced on an independent replicate. "
         "stable = same verdict; contradict = both declared with opposite signs; unsupported = declared on one replicate, abstain on the other; declare = fraction declared.", ""]
    L += ["## Per dataset and method", "", "| dataset | replicates | same config grid | method | pairs | stable | contradict | unsupported | declare |",
          "|---|---|---|---|---:|---:|---:|---:|---:|"]
    agg = {}
    for ds in DATASETS:
        for m in ("point", "union_ctrl", "union_all"):
            rs = [r for r in rows if r["dataset"] == ds["name"] and r["method"] == m]
            if not rs:
                continue
            st = np.mean([r["A"] == r["B"] for r in rs]); co = np.mean([r["A"] != "0" and r["B"] != "0" and r["A"] != r["B"] for r in rs])
            un = np.mean([(r["A"] != "0") != (r["B"] != "0") for r in rs]); de = np.mean([(r["A"] != "0") + (r["B"] != "0") for r in rs]) / 2
            L.append(f"| {ds['name']} | {ds['kind']} | {'yes' if ds['grid_match'] else '**no**'} | {m} | {len(rs)} | {st:.2f} | {co:.2f} | {un:.2f} | {de:.2f} |")
            agg.setdefault(m, []).extend(rs)
    L += ["", "## Aggregate over datasets", "",
          "Headline = replications whose two sides evaluate the same configuration grid. The eggplant stack pair is listed "
          "separately because ManiSkill3 and the original stack use different eggplant orientation grids (8x8 vs 8x3).", "",
          "| scope | method | pairs | stable | contradict | unsupported | declare |", "|---|---|---:|---:|---:|---:|---:|"]
    for scope, keep in (("same-grid replications", True), ("all replications (legacy)", None)):
        for m, rs0 in agg.items():
            rs = [r for r in rs0 if keep is None or r["grid_match"]]
            if not rs:
                continue
            st = np.mean([r["A"] == r["B"] for r in rs]); co = np.mean([r["A"] != "0" and r["B"] != "0" and r["A"] != r["B"] for r in rs])
            un = np.mean([(r["A"] != "0") != (r["B"] != "0") for r in rs]); de = np.mean([(r["A"] != "0") + (r["B"] != "0") for r in rs]) / 2
            L.append(f"| {scope} | {m} | {len(rs)} | {st:.2f} | {co:.2f} | {un:.2f} | {de:.2f} |")
    L += ["", "## Verdicts per pair", "", "| dataset | pair | point A/B | union_ctrl A/B | union_all A/B |", "|---|---|---|---|---|"]
    seen = set()
    for r in rows:
        key = (r["dataset"], r["pair"])
        if key in seen:
            continue
        seen.add(key)
        get = lambda m: next((f"{x['A']}/{x['B']}" for x in rows if x["dataset"] == r["dataset"] and x["pair"] == r["pair"] and x["method"] == m), "n/a")
        L.append(f"| {r['dataset']} | {r['pair']} | {get('point')} | {get('union_ctrl')} | {get('union_all')} |")
    L += ["", f"Manifest: {len(manifest)} input files with md5 in `track_r_manifest.json`."]
    text = "\n".join(L)
    (out / "track_r_summary.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
