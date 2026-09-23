"""Multiplicity across policy pairs: what survives a Holm correction over the 17 bridge rows.

Appendix A2 states that our intervals are computed per policy pair and that the ledger's $E_{MC}$ is
a joint event over pairs, so a family of per-pair statements would have to be inflated before it
could enter the ledger -- and that we had not performed the inflation. This script performs it, so
the manuscript can report the corrected counts rather than only the caveat.

What is and is not being corrected. Across CONDITIONS no correction is needed: a false envelope
declaration requires one particular condition's own lower bound to exceed its own truth, and that
condition is fixed by the surface rather than chosen from the data, so the false-declaration rate is
at most alpha for any finite condition set (Sect. 3.3). Across PAIRS the error event does not pin
down which interval failed, so the usual multiplicity problem applies and a correction is required.

Method. For each pair we form the z statistic Delta/se from Eq. (eq:var) -- the same estimator the
core table uses -- and the two-sided p value erfc(|z|/sqrt 2). For the envelope the relevant p is
not the smallest of the per-condition ones but the LARGEST: the envelope declares only when every
condition agrees in sign, which makes it an intersection-union test, and an IUT rejects exactly when
each component test rejects. Holm's step-down procedure at alpha = 0.05 is then applied over the 17
bridge pairs; it controls the family-wise error rate without any independence assumption, which
matters because the pairs are not independent -- they are drawn from four Octo variants plus OpenVLA
on shared policy data.

The surviving count is the intersection of "declared without correction" with "still rejected after
it", because a correction can only remove declarations. Reporting the corrected rejection count on
its own would be wrong in both directions: it can flag a pair whose envelope straddles zero, and it
cannot promote an abstention.

Holm is the right default here rather than Benjamini-Hochberg. The claim a reader takes from the
core table is "each of these declared orderings holds", which is a family-wise statement; a
false-discovery-rate procedure would license a different and weaker reading. We print BH alongside
it so the choice is inspectable rather than inherited.

Two findings, and the second is the one the manuscript reports.

The envelope's p values are maxima over conditions and so start larger, which is why its set of
declarations is the smaller of the two before any correction. That it also loses the larger SHARE of
them under Holm (10 to 5, against point calibration's 11 to 9) is a fact about these records and not
a theorem: an IUT p value being larger does not by itself determine how a step-down procedure over a
different index -- pairs, not conditions -- will treat it.

The quantity the manuscript reports is the DISAGREEMENT between the two rules, and it moves the
other way: 1 of 17 uncorrected, **4 of 17** under Holm. Under a common error-control standard across
pairs the two rules disagree more, not less, because the correction removes more of the envelope's
declarations. Reporting only "10 to 5" drops the comparison that matters.

Neither number says the criterion decides better. Four extra abstentions are four abstentions; with
no true ordering for these pairs we cannot tell an avoided false declaration from a surrendered
correct one. And Holm needs valid input p values, which these are only under the normal
approximation and the variance imputation of Sect. 5.4 -- a correction does not repair a calibration
problem in what it corrects. This file is a sensitivity analysis under a stated working model.

Usage:  python scripts/analyze_multiplicity.py [--alpha 0.05] [--out results/MULTIPLICITY.md]
"""
import argparse
import itertools
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import make_core_table as mct  # noqa: E402
from task_configs import n_configs  # noqa: E402

FRACTAL = "GraspSingleOpenedCokeCanInScene-v0"


def norm_sf(z):
    """Two-sided tail of the standard normal, via erfc -- no scipy dependency."""
    return math.erfc(abs(z) / math.sqrt(2.0))


def holm(pvals, alpha):
    """Holm step-down. Returns the reject/accept decision per input index."""
    order = sorted(range(len(pvals)), key=lambda i: pvals[i])
    m = len(pvals)
    out = [False] * m
    for rank, i in enumerate(order):
        if pvals[i] <= alpha / (m - rank):
            out[i] = True
        else:
            break                      # step-down: stop at the first failure
    return out


def bh(pvals, alpha):
    """Benjamini-Hochberg step-up, reported as a contrast to Holm."""
    order = sorted(range(len(pvals)), key=lambda i: pvals[i])
    m = len(pvals)
    k = 0
    for rank, i in enumerate(order, start=1):
        if pvals[i] <= alpha * rank / m:
            k = rank
    out = [False] * m
    for rank, i in enumerate(order, start=1):
        if rank <= k:
            out[i] = True
    return out


def collect():
    """One record per bridge policy pair: point and envelope statistics."""
    mct.SETS_MS3 = dict(mct.SEED_SETS_OCTO)
    rows = []
    for label, env, override in mct.TASKS:
        if env == FRACTAL:
            continue                   # a different embodiment and a different question
        sets = override or mct.SETS_MS3
        avail = [p for p in mct.POLICIES
                 if any((ROOT / r / p / env).exists() for r in sets.values())]
        for a, b in itertools.combinations(avail, 2):
            nom = mct.delta(sets, a, b, env, "nominal")
            if not nom:
                continue
            inv = [r for r in (mct.delta(sets, a, b, env, c) for c in mct.INVISIBLE) if r]
            if not inv:
                continue
            env_rs = inv + [nom]
            lo = min(r["lo"] for r in env_rs)
            hi = max(r["hi"] for r in env_rs)
            # The envelope declares only if EVERY condition agrees in sign, so it is an
            # intersection-union test: it rejects exactly when each per-condition test rejects, and
            # its p value is therefore the LARGEST of the per-condition p values, not the smallest.
            # That is the same fact as the no-correction-across-conditions argument of Sect. 3.3 seen
            # from the other side. An earlier version of this script took the condition whose bound
            # lay nearest zero, which is not the binding one when a condition's interval straddles
            # zero, and it reported envelope "rejections" for pairs whose envelope abstains.
            ps = [norm_sf(r["delta"] / r["se"]) if r["se"] > 0 else 0.0 for r in env_rs]
            worst = env_rs[max(range(len(ps)), key=lambda i: ps[i])]
            rows.append(dict(
                task=label, a=a, b=b, n=nom["n"],
                d=nom["delta"], se=nom["se"], lo=nom["lo"], hi=nom["hi"],
                env_lo=lo, env_hi=hi, p_env=max(ps),
                env_d=worst["delta"], env_se=worst["se"], n_cond=len(env_rs),
            ))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--out", default="results/MULTIPLICITY.md")
    args = ap.parse_args()

    rows = collect()
    for r in rows:
        r["p_point"] = norm_sf(r["d"] / r["se"]) if r["se"] > 0 else 0.0

    pp = [r["p_point"] for r in rows]
    pe = [r["p_env"] for r in rows]
    hp, he = holm(pp, args.alpha), holm(pe, args.alpha)
    bp, be = bh(pp, args.alpha), bh(pe, args.alpha)

    def dec_point(r):
        return r["lo"] > 0 or r["hi"] < 0

    def dec_env(r):
        return r["env_lo"] > 0 or r["env_hi"] < 0

    # A correction can only remove declarations, never add them, so the surviving count is the
    # intersection of "declared uncorrected" with "rejected after correction".
    n_point = sum(1 for r in rows if dec_point(r))
    n_env = sum(1 for r in rows if dec_env(r))
    s_hp = sum(1 for i, r in enumerate(rows) if dec_point(r) and hp[i])
    s_bp = sum(1 for i, r in enumerate(rows) if dec_point(r) and bp[i])
    s_he = sum(1 for i, r in enumerate(rows) if dec_env(r) and he[i])
    s_be = sum(1 for i, r in enumerate(rows) if dec_env(r) and be[i])

    # The paper's headline quantity is the DISAGREEMENT -- point declares where the envelope does
    # not -- so the corrected version of that is what has to be compared, not each rule's own count.
    # Reading only "the envelope went from 10 to 5" drops the comparison: under a common error-control
    # standard across pairs the two rules disagree MORE, not less.
    dis_raw = [i for i, r in enumerate(rows) if dec_point(r) and not dec_env(r)]
    dis_holm = [i for i, r in enumerate(rows)
                if (dec_point(r) and hp[i]) and not (dec_env(r) and he[i])]
    dis_bh = [i for i, r in enumerate(rows)
              if (dec_point(r) and bp[i]) and not (dec_env(r) and be[i])]

    L = [f"# Multiplicity across the {len(rows)} bridge policy pairs", "",
         "Per-pair intervals are what the core table reports, and the ledger's $E_{MC}$ is a joint "
         "event over pairs, so the counts have to be corrected before they can be read as "
         "\"each of these orderings holds\". This file performs the correction that "
         "Appendix A.2 previously only flagged as missing. Correction is needed across **pairs** "
         "and not across **conditions**: a false envelope declaration requires one particular "
         "condition's own lower bound to exceed its own truth, and that condition is fixed by the "
         "surface rather than selected from the data (Sect. 3.3).", "",
         f"Estimator: Eq. (eq:var), run observation unit, $\\alpha = {args.alpha}$. The $z$ for a "
         "pair is $\\hat\\Delta/\\mathrm{se}$ at nominal. The envelope "
         "declares only when every condition agrees, so it is an intersection-union test and its $p$ "
         "is the LARGEST of the per-condition $p$ values. Holm then controls the family-wise error "
         "rate over pairs without an independence assumption, "
         "which matters because these pairs share policy data. Benjamini-Hochberg is printed "
         "beside it because the choice between a family-wise and a false-discovery reading is a "
         "choice about what the table claims, not a technicality.", "",
         "| task | pair | $n$ | point $\\Delta$ [95%] | $p$ | Holm | BH | envelope | IUT $p$ | Holm | BH |",
         "|---|---|---:|---|---:|---|---|---|---:|---|---|"]
    for i, r in enumerate(rows):
        L.append(
            f"| {r['task']} | `{r['a']}` vs `{r['b']}` | {r['n']} | "
            f"{r['d']:+.3f} [{r['lo']:+.3f}, {r['hi']:+.3f}] | {r['p_point']:.2e} | "
            f"{'**yes**' if hp[i] else 'no'} | {'yes' if bp[i] else 'no'} | "
            f"[{r['env_lo']:+.3f}, {r['env_hi']:+.3f}] | {r['p_env']:.2e} | "
            f"{'**yes**' if he[i] else 'no'} | {'yes' if be[i] else 'no'} |")

    L += ["", "## Counts", "",
          "| standard applied over the 17 pairs | point declares | envelope declares | "
          "point declares, envelope abstains |", "|---|---:|---:|---:|",
          f"| no correction across pairs | {n_point} | {n_env} | **{len(dis_raw)}** |",
          f"| Holm at $\\alpha$ = {args.alpha} | {s_hp} | {s_he} | **{len(dis_holm)}** |",
          f"| Benjamini-Hochberg at {args.alpha} | {s_bp} | {s_be} | **{len(dis_bh)}** |", "",
          "The last column is the quantity the manuscript reports, and it is the one to read. Under a "
          "common error-control standard across pairs the two rules disagree on "
          f"**{len(dis_holm)} of {len(rows)}** pairs, not {len(dis_raw)}: the correction removes more "
          "of the envelope's declarations than of point calibration's, so it turns agreements into "
          "disagreements. Quoting only the envelope's own fall from "
          f"{n_env} to {s_he} drops that comparison.", "",
          "What this does **not** show is that the extra abstentions are corrections. They are "
          "abstentions. Without the true ordering for these pairs we cannot say whether each one "
          "avoided a false declaration or gave up a correct one, and the two rules are answering "
          "different questions in any case -- one about a single setting, one about agreement across "
          "a set of settings. What is established is that a declaration is sensitive to the "
          "parameter set and to the error-control standard; that a set-valued rule improves "
          "real-world decision accuracy is not established here and we do not claim it.", ""]
    if dis_holm:
        L += ["Pairs on which the two rules disagree after Holm: "
              + "; ".join(f"`{rows[i]['a']}` vs `{rows[i]['b']}` ({rows[i]['task']})"
                          for i in dis_holm) + ".", ""]

    lost_p = [f"`{r['a']}` vs `{r['b']}` ({r['task']}, lower bound {r['lo']:+.4f})"
              for i, r in enumerate(rows) if dec_point(r) and not hp[i]]
    lost_e = [f"`{r['a']}` vs `{r['b']}` ({r['task']}, envelope bound "
              f"{(r['env_lo'] if r['env_lo'] > 0 else r['env_hi']):+.4f})"
              for i, r in enumerate(rows) if dec_env(r) and not he[i]]
    if lost_p:
        L += ["Point declarations that do not survive Holm: " + "; ".join(lost_p) + ".", ""]
    if lost_e:
        L += ["Envelope declarations that do not survive Holm: " + "; ".join(lost_e) + ".", ""]
    L += ["The knife-edge declarations of Sect. 7.2 are the ones to watch here: a bound of "
          "$+0.0091$ or $+0.0095$ carries a $p$ far too large to survive a step-down procedure over "
          "17 hypotheses, which is the concrete form of the caveat in Appendix A.2. Whether the "
          "corrected or the uncorrected count is the right one to quote depends on what is being "
          "claimed -- a reader interested in one named pair wants the uncorrected interval, a "
          "reader who scans the table for whichever orderings it declares wants the corrected "
          "one -- and we report both rather than choosing for them.", ""]

    text = "\n".join(L)
    (ROOT / args.out).write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
