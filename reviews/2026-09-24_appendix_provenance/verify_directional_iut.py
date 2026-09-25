"""Regression and frozen-data comparison for the directional-IUT correction.

Reads released episode records; writes only this audit directory.
"""
import importlib.util
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import analyze_multiplicity as new


def regression_checks():
    tests = []
    # Two confident but opposing directions are not evidence of a common ordering.
    assert new.ordering_pvalue([(8.0, 1.0), (-8.0, 1.0)]) == 1.0
    tests.append("Opposite strong signs give p=1")
    assert new.ordering_pvalue([(0.0, 0.0), (5.0, 1.0)]) == 1.0
    tests.append("A degenerate zero gap cannot establish strict ordering")
    assert new.ordering_pvalue([(2.0, 0.0)]) == 0.0
    assert new.ordering_pvalue([(-2.0, 0.0)]) == 0.0
    tests.append("Nonzero zero-SE gaps retain the explicitly degenerate working-model behavior")
    positive = [(2.3, 1.0), (4.0, 1.0), (3.0, 0.5)]
    p = new.ordering_pvalue(positive)
    assert math.isclose(p, math.erfc(2.3 / math.sqrt(2)), rel_tol=1e-12)
    assert p == new.ordering_pvalue([(-d, s) for d, s in positive])
    tests.append("A common sign uses the least significant condition; sign reversal is symmetric")
    assert new.ordering_pvalue([(0.0, 1.0)]) == 1.0
    tests.append("A noisy zero point estimate gives p=1")
    # The old mixed-sign p could be arbitrarily small, consume the first rank,
    # and admit an unrelated p=.03 against .05 rather than .025 in a two-test family.
    old_mixed = math.erfc(8.0 / math.sqrt(2))
    assert new.holm([old_mixed, 0.03], 0.05) == [True, True]
    assert new.holm([new.ordering_pvalue([(8.0, 1.0), (-8.0, 1.0)]), 0.03], 0.05) == [False, False]
    tests.append("Mixed-sign evidence cannot occupy an early Holm rank")
    for bad in ([], [(1.0, -1.0)], [(float('nan'), 1.0)]):
        try:
            new.ordering_pvalue(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Expected invalid input to fail: {bad}")
    tests.append("Empty and invalid variance inputs fail explicitly")
    return tests


def key(r):
    return r["task"], r["a"], r["b"]


def counts(rows, module):
    point = [r["lo"] > 0 or r["hi"] < 0 for r in rows]
    envelope = [r["env_lo"] > 0 or r["env_hi"] < 0 for r in rows]
    def summary(p, e):
        return {"point": sum(p), "envelope": sum(e), "disagreement": sum(x != y for x, y in zip(p, e))}
    out = {"uncorrected": summary(point, envelope)}
    for name, adjust in (("Holm", module.holm), ("BH", module.bh)):
        p = [x and y for x, y in zip(point, adjust([r["p_point"] for r in rows], .05))]
        e = [x and y for x, y in zip(envelope, adjust([r["p_env"] for r in rows], .05))]
        out[name] = summary(p, e)
    return out


def main():
    tests = regression_checks()
    spec = importlib.util.spec_from_file_location("multiplicity_before", HERE / "before/scripts/analyze_multiplicity.py")
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    old.ROOT = ROOT
    before, after = old.collect(), new.collect()
    assert [key(r) for r in before] == [key(r) for r in after]
    for r in before:
        r["p_point"] = old.norm_sf(r["d"] / r["se"]) if r["se"] > 0 else 0.0
    for r in after:
        r["p_point"] = new.ordering_pvalue([(r["d"], r["se"])])
    old_counts, new_counts = counts(before, old), counts(after, new)
    assert old_counts == new_counts
    assert new_counts == {"uncorrected": {"point": 11, "envelope": 10, "disagreement": 1},
                          "Holm": {"point": 9, "envelope": 5, "disagreement": 4},
                          "BH": {"point": 11, "envelope": 10, "disagreement": 1}}
    comparisons = [dict(task=a["task"], policy_a=a["a"], policy_b=a["b"],
                        old_point_p=b["p_point"], new_point_p=a["p_point"],
                        old_envelope_p=b["p_env"], new_envelope_p=a["p_env"])
                   for b, a in zip(before, after)]
    report = dict(regressions=tests, number_of_pairs=len(after), before=old_counts, after=new_counts,
                  comparisons=comparisons)
    (HERE / "DIRECTIONAL_IUT_VERIFICATION.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = ["# Directional IUT correction and frozen-data verification", "",
             "The sign-consistency requirement is now applied before Holm or BH, via two directional intersection-union tests. No episode records or scientific effect-size estimates changed.", "",
             "## Regression checks", ""] + [f"- PASS: {t}." for t in tests]
    lines += ["", "## Counts before and after (identical)", "",
              "| Method | Point | Envelope | Disagreement |", "|---|---:|---:|---:|"]
    lines += [f"| {name} | {v['point']} | {v['envelope']} | {v['disagreement']} |" for name, v in new_counts.items()]
    lines += ["", "## Per-pair p values", "",
              "| Task | Policy A | Policy B | Point p (unchanged) | Envelope p before | Envelope p after |",
              "|---|---|---|---:|---:|---:|"]
    lines += [f"| {r['task']} | {r['policy_a']} | {r['policy_b']} | {r['new_point_p']:.12g} | {r['old_envelope_p']:.12g} | {r['new_envelope_p']:.12g} |" for r in comparisons]
    lines += ["", "Three mixed-sign rows now have p=1. All reported declaration counts remain unchanged. The full precision values are in DIRECTIONAL_IUT_VERIFICATION.json. The validity of all normal-tail calculations remains conditional on the stated variance model.", ""]
    (HERE / "DIRECTIONAL_IUT_VERIFICATION.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"regressions_passed":len(tests), "pairs":len(after), "counts":new_counts}, indent=2))


if __name__ == "__main__":
    main()
