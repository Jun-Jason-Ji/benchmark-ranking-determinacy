"""Track S runner: coverage / false-declaration / power / width of the verdict methods on synthetic surfaces.

Usage: python benchmark/decidability_bench/run_track_s.py --reps 300 --out results/benchmark/track_s
Outputs track_s_results.json, track_s_summary.md, fig_track_s.png (matplotlib if available)."""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scenarios import surface, truth_bounds, sample_outcomes  # noqa: E402
from methods import REGISTRY, METHODS  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SURFACES = ["flat", "linear", "dip_sampled", "dip_unsampled"]
D0S = [0.0, 0.10, 0.20, 0.30]
NS = [24, 48, 96]


def run_cell(kind, d0, n, reps, seed):
    rng = np.random.default_rng(seed)
    f = surface(kind, d0)
    Ls, Us = truth_bounds(f)
    truth_sign = "+" if Ls > 0 else ("−" if Us < 0 else "0")
    acc = {m: dict(cover=0, false_declare=0, declare=0, width=0.0, plus=0, minus=0) for m in METHODS}
    gate_rej = 0
    for _ in range(reps):
        data = sample_outcomes(f, n, rng)
        for m in METHODS:
            lo, hi, s = REGISTRY[m](data, rng)
            a = acc[m]
            a["cover"] += int(lo <= Ls and hi >= Us)
            a["false_declare"] += int((s == "+" and Ls <= 0) or (s == "−" and Us >= 0))
            a["declare"] += int(s != "0")
            a["plus"] += int(s == "+"); a["minus"] += int(s == "−")
            a["width"] += hi - lo
        from methods import flatness_rejects
        gate_rej += int(flatness_rejects(data, rng))
    out = {m: {k: (v / reps) for k, v in a.items()} for m, a in acc.items()}
    return dict(surface=kind, d0=d0, n=n, reps=reps, L_true=Ls, U_true=Us, truth_sign=truth_sign, gate_reject_rate=gate_rej / reps, methods=out)


def _run_cell_star(spec):
    return run_cell(*spec)


def fmt(x):
    return f"{x:.2f}"


def summary_md(cells):
    L = ["# Track S: coverage of the verdict methods on synthetic surfaces", "",
         f"reps per cell = {cells[0]['reps']}; α = 0.05; p_base = 0.35; copula ρ = 0.3; strip extent |s| ≤ {__import__('scenarios').S_MAX}. "
         "cover = P([L̂,Û] ⊇ [L*,U*]); false = P(declared sign contradicts the strip truth); declare = P(sign declared); width = mean Û − L̂. "
         "Targets: cover ≥ 0.95, false ≤ 0.05; declare is power where truth_sign ≠ 0.", ""]
    for kind in SURFACES:
        L += [f"## {kind}", "", "| Δ₀ | n | truth [L*, U*] | sign | gate rej. | " + " | ".join(f"{m}: cover / false / declare / width" for m in METHODS) + " |",
              "|---|---:|---|---|---:|" + "|".join("---" for _ in METHODS) + "|"]
        for c in [c for c in cells if c["surface"] == kind]:
            row = f"| {c['d0']:.2f} | {c['n']} | [{c['L_true']:+.2f}, {c['U_true']:+.2f}] | {c['truth_sign']} | {fmt(c['gate_reject_rate'])} | "
            row += " | ".join(f"{fmt(c['methods'][m]['cover'])} / {fmt(c['methods'][m]['false_declare'])} / {fmt(c['methods'][m]['declare'])} / {fmt(c['methods'][m]['width'])}" for m in METHODS) + " |"
            L.append(row)
        L.append("")
    # headline aggregates
    L += ["## Aggregates (over Δ₀ and n)", "", "| surface | " + " | ".join(f"{m}: min cover / max false / mean declare (truth decidable) / mean width" for m in METHODS) + " |",
          "|---|" + "|".join("---" for _ in METHODS) + "|"]
    for kind in SURFACES:
        cs = [c for c in cells if c["surface"] == kind]
        parts = []
        for m in METHODS:
            cov = min(c["methods"][m]["cover"] for c in cs)
            fal = max(c["methods"][m]["false_declare"] for c in cs)
            dec = [c["methods"][m]["declare"] for c in cs if c["truth_sign"] != "0"]
            wid = np.mean([c["methods"][m]["width"] for c in cs])
            parts.append(f"{fmt(cov)} / {fmt(fal)} / {fmt(np.mean(dec)) if dec else 'n/a'} / {fmt(wid)}")
        L.append(f"| {kind} | " + " | ".join(parts) + " |")
    L.append("")
    return "\n".join(L)


def figure(cells, path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:  # pragma: no cover
        print("no matplotlib:", e); return
    # Journal geometry: 174 mm full-column width, all lettering at 8 pt or more, no in-figure title
    # (Autonomous Robots forbids titles inside figure files; the panel labels name the surface, and
    # the interpretation lives in the caption). The `gated` rung is omitted: FINDING_track_s.md
    # withdrew it from the ladder, so plotting it here would contradict the paper.
    plt.rcParams["font.family"] = ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"]
    shown = [m for m in METHODS if m != "gated"]
    # Display scientific method names while retaining the cached method keys.
    method_labels = {"point": "Point calibration", "union": "Union envelope",
                     "gp_sim": "GP simultaneous band"}
    fig, axes = plt.subplots(2, len(SURFACES), figsize=(6.85, 4.6), sharey="row", sharex=True)
    colors = {"point": "#888", "union": "#0b5d8a", "gp_sim": "#a1541a", "gated": "#1d7a3e"}
    for j, kind in enumerate(SURFACES):
        for m in shown:
            for n, ls in zip(NS, [":", "--", "-"]):
                cs = sorted([c for c in cells if c["surface"] == kind and c["n"] == n], key=lambda c: c["d0"])
                x = [c["d0"] for c in cs]
                axes[0, j].plot(x, [c["methods"][m]["false_declare"] for c in cs], ls, color=colors[m],
                                marker="o", ms=2.5, lw=1.2, label=f"{method_labels[m]}, n={n}" if j == 0 else None)
                axes[1, j].plot(x, [c["methods"][m]["cover"] for c in cs], ls, color=colors[m],
                                marker="o", ms=2.5, lw=1.2)
        axes[0, j].axhline(0.05, color="k", lw=0.6)
        axes[1, j].axhline(0.95, color="k", lw=0.6)
        axes[0, j].set_title(kind.replace("_", " "), fontsize=8.5)
        axes[1, j].set_xlabel(r"$\Delta_0$", fontsize=8)
        for r in (0, 1):
            axes[r, j].tick_params(labelsize=8)
    axes[0, 0].set_ylabel("false declaration rate", fontsize=8)
    axes[1, 0].set_ylabel(r"coverage of $[L^*, U^*]$", fontsize=8)
    # Nine legend entries do not fit inside a 43 mm panel at 8 pt, so the legend goes under the grid.
    h, lab = axes[0, 0].get_legend_handles_labels()
    fig.legend(h, lab, fontsize=8, ncol=3, loc="lower center", frameon=False,
               bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout(rect=(0, 0.10, 1, 1))
    fig.savefig(path, dpi=300)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=300)
    ap.add_argument("--out", default="results/benchmark/track_s")
    ap.add_argument("--surfaces", default=",".join(SURFACES))
    ap.add_argument("--seed", type=int, default=20260919)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--redraw", action="store_true",
                    help="redraw the figure from track_s_results.json without recomputing the cells")
    args = ap.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    if args.redraw:
        cells = json.loads((out / "track_s_results.json").read_text(encoding="utf-8"))
        figure(cells, out / "fig_track_s.png")
        print(f"redrew {out / 'fig_track_s.png'} from {len(cells)} cached cells")
        return
    specs = [(kind, d0, n, args.reps, args.seed + 1000 * SURFACES.index(kind) + 100 * D0S.index(d0) + NS.index(n))
             for kind in args.surfaces.split(",") for d0 in D0S for n in NS]
    cells = []
    t0 = time.time()
    if args.workers > 1:
        from multiprocessing import Pool
        pool = Pool(args.workers)
        it = pool.imap(_run_cell_star, specs)
    else:
        it = map(_run_cell_star, specs)
    for cell in it:
        cells.append(cell)
        print(f"{time.time() - t0:7.0f}s {cell['surface']:14s} d0={cell['d0']:.2f} n={cell['n']:3d} truth=[{cell['L_true']:+.2f},{cell['U_true']:+.2f}] " +
              " ".join(f"{m}:{cell['methods'][m]['cover']:.2f}/{cell['methods'][m]['false_declare']:.2f}/{cell['methods'][m]['declare']:.2f}" for m in METHODS), flush=True)
        (out / "track_s_results.json").write_text(json.dumps(cells, indent=1), encoding="utf-8")
    order = {(k, d, n): i for i, (k, d, n, *_r) in enumerate(specs)}
    cells.sort(key=lambda c: order[(c["surface"], c["d0"], c["n"])])
    (out / "track_s_summary.md").write_text(summary_md(cells), encoding="utf-8")
    figure(cells, out / "fig_track_s.png")
    print("TRACK_S_DONE", out)


if __name__ == "__main__":
    main()
