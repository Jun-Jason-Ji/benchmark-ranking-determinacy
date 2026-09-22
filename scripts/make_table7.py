"""Rebuild Table 7 (coverage / error / power by response-surface family) from a Track S cache.

Table 7 was written from results/benchmark/track_s, the configuration in which the GP band
extrapolates half a grid step past the sampled range. Sect. 8.2 adopts the *restricted* band
(results/benchmark/track_s_smax2, strip extent |s| <= 2), so the published GP column described a
configuration the paper does not use, and understated its coverage cost on the between-settings dip.

This prints the table for whichever cache is named, so the choice is explicit and the two can be
compared side by side. Declaration rate is averaged over the decidable cells only (truth_sign != 0),
which is what "power" means here; coverage and error are the min and max over all cells of the
surface, as the caption states.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SURFACES = [("flat", "Flat"), ("linear", "Linear"),
            ("dip_sampled", "Dip at a sampled setting"), ("dip_unsampled", "Dip between settings")]
METHODS = [("point", "Point calibration"), ("union", "Union bound"), ("gp_sim", "GP simultaneous band")]


def load(name):
    p = ROOT / "results/benchmark" / name / "track_s_results.json"
    return json.loads(p.read_text(encoding="utf-8"))


def summarise(cells, surface, method):
    rows = [c for c in cells if c["surface"] == surface]
    if not rows:
        return None
    m = [c["methods"][method] for c in rows]
    dec = [c["methods"][method]["declare"] for c in rows if str(c["truth_sign"]) != "0"]
    return (min(x["cover"] for x in m), max(x["false_declare"] for x in m),
            sum(dec) / len(dec) if dec else float("nan"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="track_s_smax2",
                    help="track_s_smax2 = restricted band (adopted); track_s = extrapolating band")
    ap.add_argument("--compare", default=None, help="second cache to print alongside")
    args = ap.parse_args()
    for name in [args.cache] + ([args.compare] if args.compare else []):
        cells = load(name)
        surfaces = {c["surface"] for c in cells}
        missing = [s for s, _ in SURFACES if s not in surfaces]
        print(f"\n## {name}   ({len(cells)} cells)" + (f"   MISSING: {missing}" if missing else ""))
        print("Surface & " + " & ".join(lbl for _, lbl in METHODS) + r" \\")
        for key, label in SURFACES:
            vals = []
            for mk, _ in METHODS:
                r = summarise(cells, key, mk)
                vals.append("n/a" if r is None else f"{r[0]:.2f} / {r[1]:.2f} / {r[2]:.2f}")
            print(f"{label} & " + " & ".join(vals) + r" \\")


if __name__ == "__main__":
    main()
