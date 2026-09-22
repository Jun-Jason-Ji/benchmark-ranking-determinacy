"""Table 4 and Table 5 from the official-protocol runs, for either RNG lifecycle.

Table 5 was originally computed by hand, which is why it could not be re-derived when the RNG
lifecycle changed. This script implements the two estimators the manuscript defines and runs both
result roots through identical code.

Census interval -- Eq. (eq:var) of Sect. 5.4. The 24-configuration grid is fully enumerated, so
configuration sampling error is zero and only policy noise remains:

    Var(hat Delta) = N^-2 * sum_c [ s_A^2(c)/S_c + s_B^2(c)/R_c ]

with s^2(c) the sample variance of a policy's outcomes at configuration c across the S runs and
S_c, R_c the run counts there. With one run per configuration this degenerates to the binomial
interval, which is the manuscript's point that a census does not narrow an interval; replicates do.

Naive interval -- what a reader of the published table would compute: two independent binomials over
72 episodes each.

The lifecycle matters for this table in a way that is easy to miss. Under --policy-seed-fixed the
server re-seeds on every reset, so all 24 configurations in a run share one noise realisation; the
three runs are then three draws of policy noise, and s^2(c) across them is large. Under
--policy-seed-stream each episode advances one stream, so a run averages 24 independent draws and
the across-run spread is much smaller. Both are valid inputs to Eq. (eq:var); only the second is the
reference protocol.

Usage:
  python scripts/make_table5.py --root results/controller_sweep_ms2_official_stream
  python scripts/make_table5.py --compare results/controller_sweep_ms2_official
"""
import argparse
import ast
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "third_party/SimplerEnv/simpler_env/utils/metrics.py"
SEEDS = [0, 2, 4]
Z = 1.959963985
TASKS = [("eggplant", "widowx_put_eggplant_in_basket", "PutEggplantInBasketScene-v0"),
         ("spoon", "widowx_spoon_on_towel", "PutSpoonOnTableClothInScene-v0"),
         ("carrot", "widowx_carrot_on_plate", "PutCarrotOnPlateInScene-v0"),
         ("stack", "widowx_stack_cube", "StackGreenCubeOnYellowCubeBakedTexInScene-v0")]
A, B = "octo-small", "octo-base"


def published():
    src = METRICS.read_text(encoding="utf-8")
    m = re.search(r"SIMPLER_PERF\s*=\s*(\{.*?\n\})", src, re.S)
    try:
        return ast.literal_eval(m.group(1)) if m else {}
    except Exception:
        return {}


def outcomes(root, policy, env):
    """{episode_id: [outcome per seed]} -- the episode id IS the configuration id here, because the
    official protocol runs --obj-episode-range 0 24 on a 24-configuration grid, so there is exactly
    one episode per configuration per seed."""
    per = {}
    for s in SEEDS:
        f = root / f"seed{s}" / policy / env / "nominal.jsonl"
        if not f.exists():
            continue
        seen = set()
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            e = r["episode_id"]
            if e in seen:
                continue
            seen.add(e)
            per.setdefault(e, []).append(int(bool(r["success"])))
    return per


def census(root, env):
    """Eq. (eq:var) over the shared configuration grid. Returns (delta, half_width, N, S)."""
    pa, pb = outcomes(root, A, env), outcomes(root, B, env)
    cfgs = sorted(set(pa) & set(pb))
    if not cfgs:
        return None
    ma = np.array([np.mean(pa[c]) for c in cfgs])
    mb = np.array([np.mean(pb[c]) for c in cfgs])
    n = len(cfgs)
    var = 0.0
    for c in cfgs:
        for obs in (pa[c], pb[c]):
            k = len(obs)
            # ddof=1 needs two runs; with one run the term is 0 and the estimator degenerates to the
            # binomial interval, computed below from the pooled rate instead.
            var += (float(np.var(obs, ddof=1)) / k) if k > 1 else 0.0
    var /= n ** 2
    d = float(ma.mean() - mb.mean())
    s = min(min(len(v) for v in pa.values()), min(len(v) for v in pb.values()))
    if var == 0.0 and s == 1:
        ra, rb = float(ma.mean()), float(mb.mean())
        var = ra * (1 - ra) / n + rb * (1 - rb) / n
    return d, Z * float(np.sqrt(var)), n, s


def block_t(root, env):
    """Sensitivity: treat each of the three runs as the replication unit, not each configuration.

    A paired t interval on the three whole-census block differences Delta_s = rate_A(s) - rate_B(s).
    This is the right model if the noise varies between runs and not within them, which is what our
    earlier per-episode-re-seeding lifecycle produced; under the reference lifecycle each episode
    draws from its own point in one advancing stream, so within-run variation is real and this model
    ignores it. Reported because it changes the headline count from one resolvable ordering to two,
    and a reader should see that the count depends on the model rather than only on the data.
    Two degrees of freedom, so t(0.975, 2) = 4.302653.
    """
    pa, pb = outcomes(root, A, env), outcomes(root, B, env)
    cfgs = sorted(set(pa) & set(pb))
    if not cfgs:
        return None
    k = min(min(len(pa[c]) for c in cfgs), min(len(pb[c]) for c in cfgs))
    if k < 2:
        return None
    blocks = [float(np.mean([pa[c][s] for c in cfgs]) - np.mean([pb[c][s] for c in cfgs]))
              for s in range(k)]
    m, sd = float(np.mean(blocks)), float(np.std(blocks, ddof=1))
    tcrit = 4.302653 if k == 3 else None
    if tcrit is None:
        try:
            from scipy import stats
            tcrit = float(stats.t.ppf(0.975, k - 1))
        except Exception:
            return None
    h = tcrit * sd / np.sqrt(k)
    return m, float(h), blocks


def naive(root, env):
    """Two independent binomials over all episodes, which is what the published table invites."""
    pa, pb = outcomes(root, A, env), outcomes(root, B, env)
    va = [x for v in pa.values() for x in v]
    vb = [x for v in pb.values() for x in v]
    if not va or not vb:
        return None
    ra, rb = float(np.mean(va)), float(np.mean(vb))
    se = float(np.sqrt(ra * (1 - ra) / len(va) + rb * (1 - rb) / len(vb)))
    return ra - rb, Z * se, len(va), len(vb)


def verdict(lo, hi):
    return "octo-small > octo-base" if lo > 0 else ("octo-base > octo-small" if hi < 0 else "abstain")


def report(label, root, pub):
    print(f"\n## {label}\n")
    print("| Task | our Δ | census 95% | naive binomial 95% | verdict | published Δ | n/S |")
    print("|---|---:|---|---|---|---:|---|")
    res = {}
    for name, task, env in TASKS:
        cen, nai = census(root, env), naive(root, env)
        if cen is None or nai is None:
            continue
        d, h, n, s = cen
        dn, hn, na, nb = nai
        pa = pub.get(task, {}).get(A)
        pb_ = pub.get(task, {}).get(B)
        pd = f"{pa - pb_:+.3f}" if pa is not None and pb_ is not None else "–"
        v = verdict(d - h, d + h)
        res[name] = dict(delta=d, lo=d - h, hi=d + h, verdict=v,
                         published=(pa - pb_) if pa is not None and pb_ is not None else None)
        print(f"| {name} | {d:+.3f} | [{d - h:+.3f}, {d + h:+.3f}] | "
              f"[{dn - hn:+.3f}, {dn + hn:+.3f}] | {v} | {pd} | {n}/{s} |")
    dec = [k for k, v in res.items() if v["verdict"] != "abstain"]
    print(f"\nresolvable orderings: {len(dec)} of {len(res)}" + (f"  ({', '.join(dec)})" if dec else ""))
    print("\nSensitivity -- three-run block t interval (2 df), replication unit = the run:")
    bdec = []
    for name, task, env in TASKS:
        bt = block_t(root, env)
        if bt is None:
            continue
        m, h, blocks = bt
        v = verdict(m - h, m + h)
        if v != "abstain":
            bdec.append(name)
        print(f"  {name:9s} blocks {[f'{b:+.4f}' for b in blocks]}  "
              f"[{m - h:+.4f}, {m + h:+.4f}]  {v}")
    print(f"  -> resolvable under the block model: {len(bdec)} of {len(TASKS)}"
          + (f"  ({', '.join(bdec)})" if bdec else ""))
    flips = [k for k, v in res.items()
             if v["published"] is not None and v["delta"] * v["published"] < 0]
    print("sign disagreements with the published Δ: "
          + (", ".join(f"{k} (ours {res[k]['delta']:+.3f} vs published {res[k]['published']:+.3f})"
                       for k in flips) if flips else "none"))
    # Across-run spread of each cell's rate: the quantity Sect. 6.3 quotes as 0.109, and the one
    # most changed by the lifecycle.
    rng = []
    for name, task, env in TASKS:
        for p in (A, B):
            per = outcomes(root, p, env)
            if not per:
                continue
            rates = [float(np.mean([per[c][i] for c in sorted(per) if i < len(per[c])]))
                     for i in range(SEEDS.__len__())]
            rng.append(max(rates) - min(rates))
    if rng:
        print(f"across-run range of a cell's rate: mean {np.mean(rng):.3f}, max {np.max(rng):.3f}")
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="results/controller_sweep_ms2_official_stream")
    ap.add_argument("--compare", default=None)
    args = ap.parse_args()
    pub = published()
    a = report(args.root, ROOT / args.root, pub)
    if args.compare:
        b = report(args.compare, ROOT / args.compare, pub)
        print("\n## What the lifecycle changes\n")
        print("| Task | verdict, " + args.root.split('/')[-1] + " | verdict, "
              + args.compare.split('/')[-1] + " |")
        print("|---|---|---|")
        for k in a:
            if k in b:
                print(f"| {k} | {a[k]['delta']:+.3f} {a[k]['verdict']} | "
                      f"{b[k]['delta']:+.3f} {b[k]['verdict']} |")


if __name__ == "__main__":
    main()
