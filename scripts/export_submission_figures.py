"""Re-render the paper figures as submission-ready EPS for Autonomous Robots.

The journal requires vector graphics in EPS, sans-serif lettering (Helvetica or Arial) at 8-12 pt, figure
files named Fig1.eps, Fig2.eps, ..., and no captions inside the figure files. Lines and lettering
remain vector artwork. Figure 6 also contains heatmaps and a colour bar; export those raster
components at 800 dpi so they remain above 600 dpi after scaling to the manuscript's text width.

Rather than edit the four figure scripts, this one imports them, overrides the font family (their rcParams
set DejaVu Sans first, which is neither Helvetica nor Arial), and patches Figure.savefig so that every PNG
they write also lands as the correctly numbered EPS in the submission directory.

Figure numbering follows order of appearance in main.tex (which is what LaTeX prints):
  Fig1  replay identifiability (bowl vs flat)          scripts/make_figures.py
  Fig2  uncertainty budget                             scripts/make_figures_v2.py
  Fig3  torque effect by orientation                  scripts/make_figures_v2.py
  Fig4  delta by condition                             scripts/make_figures.py
  Fig5  track S coverage                               benchmark/decidability_bench/run_track_s.py  [see note]
  Fig6  GP response surface and simultaneous band      scripts/analyze_response_surface_v2.py

Fig5 is redrawn from run_track_s.py's cached cells (track_s_results.json) rather than recomputing its
300 repetitions per cell.

Usage: python scripts/export_submission_figures.py

Figure 6 also has a direct PDF counterpart, written using the existing
Fig6-eps-converted-to.pdf compatibility name. It avoids Ghostscript downsampling
and font-conversion issues while preserving the same Matplotlib scene.
"""
import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "submission/autonomous_robots"
sys.path.insert(0, str(ROOT / "scripts"))

# stem of the PNG a figure script writes -> submission figure number
FIGNUM = {
    "fig_replay_identifiability": 1,
    "fig_uncertainty_budget": 2,
    # Numbering follows order of appearance in main.tex, which is what LaTeX prints and what the
    # journal requires the filenames to match: the torque figure (Sect. 7.4) precedes the
    # delta-by-condition figure (Sect. 7.6), so it is Fig3, not Fig4.
    "fig_torque_by_orientation": 3,
    "fig_delta_by_condition": 4,
    "fig_track_s": 5,
    "fig_response_surface": 6,
}
# Journal column widths in inches: 84 mm single column, 174 mm full width (max height 234 mm).
MM = 1 / 25.4
W_SINGLE, W_FULL, H_MAX = 84 * MM, 174 * MM, 234 * MM
# All six are wide multi-panel charts and span both columns. Do NOT move one to single column by scaling:
# font sizes are absolute points, so halving the canvas keeps 9 pt text over half the plot area and the
# labels collide. A single-column figure has to be redesigned at that size, not rescaled.
FULL_WIDTH = {1, 2, 3, 4, 5, 6}

_orig_savefig = Figure.savefig
_written = []
_problems = []


def _patched_savefig(self, fname, **kw):
    """Write the original PNG, then an EPS sibling named FigN.eps in the submission directory."""
    out = _orig_savefig(self, fname, **kw)
    stem = Path(str(fname)).stem
    n = FIGNUM.get(stem)
    if n is None:
        return out
    target_w = W_FULL if n in FULL_WIDTH else W_SINGLE
    w, h = self.get_size_inches()
    # Scale to the journal column width, preserving aspect, and clamp the height.
    scale = target_w / w
    new_h = min(h * scale, H_MAX)
    self.set_size_inches(target_w, new_h)
    # Font sizes are absolute points, so a large shrink keeps the text the same physical size over a much
    # smaller plot area and the labels collide. Below ~0.9 the figure needs redesigning at journal width
    # (usually: stack the panels, shorten tick labels, move in-figure titles into the caption), not scaling.
    # Also check the journal's 8-12 pt lettering floor against the smallest text actually in the figure.
    pts = [t.get_fontsize() for t in self.findobj(matplotlib.text.Text) if t.get_text().strip()]
    smallest = min(pts) * scale if pts else None
    if scale < 0.9 or (smallest is not None and smallest < 8):
        _problems.append((n, scale, smallest, w * 25.4))
    OUT.mkdir(parents=True, exist_ok=True)
    eps = OUT / f"Fig{n}.eps"
    kw2 = {k: v for k, v in kw.items() if k in ("bbox_inches", "pad_inches")}
    # An EPS container does not make imshow/colorbar artists vector. The
    # default 100 dpi gave Fig6 only about 92 dpi after manuscript scaling.
    eps_options = {"dpi": 800} if n == 6 else {}
    _orig_savefig(self, eps, format="eps", **eps_options, **kw2)
    if n == 6:
        # Keep the compatibility filename used by the LaTeX build, but write
        # directly from this scene to preserve image resolution and fonts.
        with matplotlib.rc_context({"pdf.fonttype": 42}):
            _orig_savefig(self, OUT / "Fig6-eps-converted-to.pdf",
                          format="pdf", dpi=800, **kw2)
    # A proof raster at the exact submitted geometry, so the layout can be eyeballed for label collisions
    # at the size the journal will print. Not submitted; EPS is the deliverable.
    _orig_savefig(self, OUT / "proof" / f"Fig{n}_proof.png", format="png", dpi=200, **kw2)
    self.set_size_inches(w, h)
    _written.append((n, eps, target_w / MM, new_h / MM))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--single", help="convert one existing figure stem only (e.g. fig_track_s)")
    args = ap.parse_args()

    Figure.savefig = _patched_savefig
    # Journal requirement: Helvetica or Arial. Their scripts put DejaVu Sans first; override before any
    # text object is created, since matplotlib bakes font properties at artist creation.
    plt.rcParams["font.family"] = ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"]

    if args.single:
        src = ROOT / "results/figures" / f"{args.single}.png"
        print(f"--single: re-run the owning script for {src.name}; this flag only reports the target size")
        n = FIGNUM.get(args.single)
        w = (W_FULL if n in FULL_WIDTH else W_SINGLE) / MM
        print(f"  {args.single} -> Fig{n}.eps at {w:.0f} mm wide")
        return

    import make_figures  # noqa: E402
    import make_figures_v2  # noqa: E402

    for fn in (make_figures.fig_replay, make_figures.fig_delta, make_figures.fig_eggplant):
        try:
            fn()
        except Exception as e:  # a figure whose inputs are absent should not block the rest
            print(f"  SKIP {fn.__name__}: {type(e).__name__}: {e}")
    for fn in (make_figures_v2.fig_uncertainty_budget, make_figures_v2.fig_torque_by_orientation):
        try:
            fn()
        except Exception as e:
            print(f"  SKIP {fn.__name__}: {type(e).__name__}: {e}")
    try:
        # v2, not v1: v1 draws a single-hyperparameter posterior and reports a pointwise k=2 band,
        # which is not the rung Sect. 8.2 adopts. v2 draws the marginalised mean and prints the
        # restricted simultaneous band the caption quotes, from the same computation.
        import analyze_response_surface_v2
        analyze_response_surface_v2.main()
    except Exception as e:
        print(f"  SKIP analyze_response_surface_v2: {type(e).__name__}: {e}")
    # Track S: redraw from the cached cells rather than recomputing 300 repetitions per cell.
    try:
        import json
        sys.path.insert(0, str(ROOT / "benchmark/decidability_bench"))
        import run_track_s
        cache = ROOT / "results/benchmark/track_s/track_s_results.json"
        cells = json.loads(cache.read_text(encoding="utf-8"))
        run_track_s.figure(cells, ROOT / "results/figures/fig_track_s.png")
    except Exception as e:
        print(f"  SKIP run_track_s: {type(e).__name__}: {e}")

    print()
    for n, path, w, h in sorted(_written):
        print(f"  Fig{n}.eps  {w:.0f} x {h:.0f} mm  {path.stat().st_size / 1024:.0f} KB")
    missing = sorted(set(FIGNUM.values()) - {n for n, *_ in _written})
    if missing:
        print(f"\n  NOT regenerated: {', '.join('Fig' + str(m) for m in missing)} "
              f"-- re-run the owning script (see this file's docstring).")
    if _problems:
        print("\n  NEEDS REDESIGN AT JOURNAL WIDTH (scaling alone will not do it):")
        for n, scale, smallest, native_mm in sorted(_problems):
            why = []
            if scale < 0.9:
                why.append(f"native {native_mm:.0f} mm wide -> scaled to {scale:.0%}")
            if smallest is not None and smallest < 8:
                why.append(f"smallest lettering {smallest:.1f} pt after scaling (floor 8 pt)")
            print(f"    Fig{n}: " + "; ".join(why))
        print("    Fix by stacking panels, shortening tick labels, and moving in-figure titles into the")
        print("    caption (the journal forbids titles inside figure files anyway).")


if __name__ == "__main__":
    main()
