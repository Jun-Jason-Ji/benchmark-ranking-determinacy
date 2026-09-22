"""Response-surface bound v2: simultaneous posterior band over the replay-compatible strip, with
hyperparameter marginalisation and a flatness gate.

Improvements over analyze_response_surface.py:
  * simultaneous 95% band: sample GP posterior functions on the strip grid (marginalising the (ℓ, σf)
    grid with weights ∝ exp(−NLL)); L = 2.5th percentile of the per-draw minimum, U = 97.5th percentile
    of the per-draw maximum. This bounds the whole strip, not one point at a time.
  * flatness gate per axis: paired bootstrap of Δ(c) − Δ(nominal) for every calibration-invisible
    condition on the axis; if any interval excludes 0 the surface model is not trusted on that axis.
    NOTE: the gate is a DIAGNOSTIC here, not a rung of the paper's ladder. Sect. 8.2 removed it,
    because on the synthetic track it lowered coverage on the between-settings surface (0.91-0.98 to
    0.89) and mis-fired on flat surfaces 16-20% of the time. The column is kept because it is
    informative about which axes the smoothness prior is doing work on, but no verdict in the
    manuscript is decided by it, and Fig. 6's caption does not invoke it.
Outputs analysis_response_surface_v2.md.
"""
import json
import sys
from pathlib import Path

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_response_surface import ENVS, DESIGN, EPS, SWEEP, ROOT, success, observations, rbf  # noqa: E402

RNG = np.random.default_rng(0)
ELLS = [0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0]
SFS = [0.02, 0.05, 0.1, 0.15, 0.2, 0.3]


def nll(X, y, se, ell, sf, m0):
    K = rbf(X, X, ell, sf) + np.diag(se ** 2)
    Lc = np.linalg.cholesky(K)
    a = np.linalg.solve(Lc.T, np.linalg.solve(Lc, y - m0))
    return 0.5 * (y - m0) @ a + np.log(np.diag(Lc)).sum() + 0.5 * len(y) * np.log(2 * np.pi)


def posterior(X, y, se, ell, sf, m0, Xs):
    K = rbf(X, X, ell, sf) + np.diag(se ** 2)
    Ks = rbf(Xs, X, ell, sf)
    Kss = rbf(Xs, Xs, ell, sf)
    Lc = np.linalg.cholesky(K)
    a = np.linalg.solve(Lc.T, np.linalg.solve(Lc, y - m0))
    mu = m0 + Ks @ a
    V = np.linalg.solve(Lc, Ks.T)
    cov = Kss - V.T @ V
    return mu, cov


def simultaneous_bounds(X, y, se, Xs, n_draws=4000):
    m0 = y.mean()
    grid = []
    for ell in ELLS:
        for sf in SFS:
            try:
                grid.append((ell, sf, nll(X, y, se, ell, sf, m0)))
            except np.linalg.LinAlgError:
                pass
    nl = np.array([g[2] for g in grid]); w = np.exp(-(nl - nl.min())); w /= w.sum()
    mins, maxs = [], []
    for (ell, sf, _), wi in zip(grid, w):
        k = int(round(wi * n_draws))
        if k == 0:
            continue
        mu, cov = posterior(X, y, se, ell, sf, m0, Xs)
        Lc = np.linalg.cholesky(cov + 1e-9 * np.eye(len(mu)))
        z = RNG.standard_normal((k, len(mu)))
        f = mu[None, :] + z @ Lc.T
        mins.append(f.min(1)); maxs.append(f.max(1))
    mins, maxs = np.concatenate(mins), np.concatenate(maxs)
    top = sorted(zip(w, grid), reverse=True)[:3]
    return float(np.percentile(mins, 2.5)), float(np.percentile(maxs, 97.5)), [(round(float(wi), 2), g[0], g[1]) for wi, g in top]


def boot(d, n=10000):
    d = np.asarray(d, float)
    m = d[RNG.integers(0, len(d), size=(n, len(d)))].mean(1)
    return float(d.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def flatness_gate(env, conds):
    """paired Δ(c) − Δ(nominal) for each condition; returns (any_reject, details)."""
    S0, B0 = success("octo-small", env, "nominal"), success("octo-base", env, "nominal")
    det, rej = [], False
    for c in conds:
        S, B = success("octo-small", env, c), success("octo-base", env, c)
        common = sorted(set(S) & set(B) & set(S0) & set(B0))
        if len(common) < 12:
            continue
        m, lo, hi = boot([(S[i] - B[i]) - (S0[i] - B0[i]) for i in common])
        r = lo > 0 or hi < 0
        rej |= r
        det.append(f"{c}: {m:+.2f} [{lo:+.2f}, {hi:+.2f}]{' *' if r else ''}")
    return rej, det


def verdict(lo, hi):
    return "small better" if lo > 0 else ("base better" if hi < 0 else "abstain")


# Half-width of the plane the band is evaluated over. The design points reach +-2, so RESTRICTED is
# the sampled range and EXTENDED goes half a grid step beyond it. Sect. 8.2 of the paper adopts the
# restricted configuration -- it raises power and restores monotonicity in n, at a coverage cost on
# the between-settings dip -- so RESTRICTED is what this script reports as the headline and what the
# figure draws. EXTENDED is reported alongside it because the choice is a methodological one and a
# reader should see both numbers rather than take the adopted one on trust.
RESTRICTED, EXTENDED = 2.0, 2.5


def strip_grid(half, n=41):
    g = np.linspace(-half, half, n)
    U, V = np.meshgrid(g, g, indexing="ij")
    Xs_all = np.stack([U.ravel(), V.ravel()], 1)
    return Xs_all[np.abs(Xs_all[:, 0] - Xs_all[:, 1]) <= EPS]


def marginal_mean(X, y, se, Xs):
    """Posterior mean averaged over the (ell, sf) grid with the same weights the band uses.

    The figure has to draw the surface the band was computed from. Plotting a single-hyperparameter
    fit next to a marginalised band is how Fig. 6 came to quote bounds from a different computation
    than the one the text adopts; sharing this function removes that possibility.
    """
    m0 = y.mean()
    grid = []
    for ell in ELLS:
        for sf in SFS:
            try:
                grid.append((ell, sf, nll(X, y, se, ell, sf, m0)))
            except np.linalg.LinAlgError:
                pass
    nl = np.array([g[2] for g in grid]); w = np.exp(-(nl - nl.min())); w /= w.sum()
    acc = np.zeros(len(Xs))
    for (ell, sf, _), wi in zip(grid, w):
        mu, _ = posterior(X, y, se, ell, sf, m0, Xs)
        acc += wi * mu
    return acc


def make_figure(rows, half=RESTRICTED):
    """Draw the marginalised posterior mean over the plane the adopted band is evaluated on."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    g = np.linspace(-half, half, 41)
    U, V = np.meshgrid(g, g, indexing="ij")
    Xs_all = np.stack([U.ravel(), V.ravel()], 1)
    fig, axes = plt.subplots(1, 3, figsize=(6.85, 2.9))  # 174 mm journal full width
    im = None
    for ax, (name, X, y, mu_all) in zip(axes, rows):
        im = ax.imshow(mu_all.reshape(U.shape).T, origin="lower",
                       extent=[-half, half, -half, half], cmap="RdBu_r", vmin=-0.4, vmax=0.4)
        ax.plot([-half, half], [-half - EPS, half - EPS], "k--", lw=0.8)
        ax.plot([-half, half], [-half + EPS, half + EPS], "k--", lw=0.8)
        ax.scatter(X[:, 0], X[:, 1], c=y, cmap="RdBu_r", vmin=-0.4, vmax=0.4, edgecolors="k", s=40)
        ax.set_xlabel("log$_2$ stiffness scale", fontsize=8)
        ax.tick_params(labelsize=8)
        ax.set_xlim(-half, half); ax.set_ylim(-half, half)
        if ax is axes[0]:
            ax.set_ylabel("log$_2$ damping scale", fontsize=8)
        ax.set_title(name, fontsize=8.5)
    cb = fig.colorbar(im, ax=axes, shrink=0.85)
    cb.ax.tick_params(labelsize=8)
    cb.set_label("marginalised posterior mean $\\Delta$", size=8)
    d = ROOT / "results/figures"
    d.mkdir(exist_ok=True)
    fig.savefig(d / "fig_response_surface.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    return d / "fig_response_surface.png"


def main():
    out = SWEEP / "analysis_response_surface_v2.md"
    Xs = strip_grid(RESTRICTED)
    Xs_ext = strip_grid(EXTENDED)
    L = ["# Response-surface bound v2: simultaneous 95% band over the compatible strip + flatness gate", "",
         f"Strip |log2 k − log2 d| ≤ {EPS}; GP hyperparameters marginalised over a (ℓ, σf) grid with weights ∝ exp(−NLL); "
         "4000 posterior function draws; L/U = 2.5th pct of draw-minimum / 97.5th pct of draw-maximum. "
         "Flatness gate: paired Δ(c) − Δ(nominal) over the calibration-invisible controller conditions; '*' = rejects flatness.", "",
         f"Two evaluation ranges are reported: **restricted** to the sampled design range "
         f"(|u|, |v| ≤ {RESTRICTED:g}), which is the configuration the paper adopts, and **extended** "
         f"half a grid step beyond it (≤ {EXTENDED:g}). The figure draws the restricted one.", "",
         "| task | restricted band (adopted) | verdict | extended band | verdict | top (weight, ℓ, σf) | flatness gate (controller-invisible) | union bound verdict |",
         "|---|---|---|---|---|---|---|---|"]
    union = json.loads((SWEEP / "analysis_compatible_set.json").read_text(encoding="utf-8"))["summary"] if (SWEEP / "analysis_compatible_set.json").exists() else {}
    rows, verdicts = [], {}
    for name, env in ENVS.items():
        X, y, se, names = observations(env)
        lo, hi, top = simultaneous_bounds(X, y, se, Xs)
        lo_e, hi_e, _ = simultaneous_bounds(X, y, se, Xs_ext)
        rej, det = flatness_gate(env, ["iso_x0.25", "iso_x0.5", "iso_x2.0", "iso_x4.0", "force_x0.5"])
        ub = union.get(name, {}).get("set_controller", "n/a")
        gate = " (gated → union bound)" if rej else ""
        L.append(f"| {name} | [{lo:+.2f}, {hi:+.2f}] | {verdict(lo, hi)}{gate} | "
                 f"[{lo_e:+.2f}, {hi_e:+.2f}] | {verdict(lo_e, hi_e)} | {top} | {'; '.join(det)} | {ub} |")
        verdicts[name] = dict(lo=lo, hi=hi, verdict=verdict(lo, hi), gated=bool(rej),
                              lo_ext=lo_e, hi_ext=hi_e, verdict_ext=verdict(lo_e, hi_e), top=top)
        g = np.linspace(-RESTRICTED, RESTRICTED, 41)
        U, V = np.meshgrid(g, g, indexing="ij")
        rows.append((name, X, y, marginal_mean(X, y, se, np.stack([U.ravel(), V.ravel()], 1))))
    L += ["", "## Contact axes (1-D, same method; gate over friction/density conditions)", "", "| task | axis | simultaneous bound | verdict | flatness gate | union verdict (controller+contact) |", "|---|---|---|---|---|---|"]
    axes = {"friction": {"fric_x0.4": np.log2(0.4), "nominal": 0.0, "fric_x2.5": np.log2(2.5)}, "density": {"dens_x0.5": -1.0, "nominal": 0.0, "dens_x2.0": 1.0}}
    for name, env in ENVS.items():
        for axname, pts in axes.items():
            X, y, se = [], [], []
            for c, u in pts.items():
                S, B = success("octo-small", env, c), success("octo-base", env, c)
                common = sorted(set(S) & set(B))
                if len(common) < 12:
                    continue
                d = np.array([S[i] - B[i] for i in common], float)
                X.append((u, 0.0)); y.append(d.mean()); se.append(d.std(ddof=1) / np.sqrt(len(d)) + 1e-6)
            if len(y) < 3:
                continue
            X, y, se = np.array(X), np.array(y), np.array(se)
            xs = np.linspace(X[:, 0].min(), X[:, 0].max(), 41); Xs1 = np.stack([xs, np.zeros_like(xs)], 1)
            lo, hi, top = simultaneous_bounds(X, y, se, Xs1)
            rej, det = flatness_gate(env, [c for c in pts if c != "nominal"])
            ub = union.get(name, {}).get("set_controller_contact", "n/a")
            L.append(f"| {name} | {axname} | [{lo:+.2f}, {hi:+.2f}] | {verdict(lo, hi)}{' (gated → union bound)' if rej else ''} | {'; '.join(det)} | {ub} |")
    L += ["", "Reading: the simultaneous band is the certified-style version of the strip bound under the GP model; the gate says whether the model's "
          "smoothness assumption is contradicted by the paired data on that axis. Where gated, report the union bound instead."]
    png = make_figure(rows)
    L += ["", f"Figure: `{png.relative_to(ROOT).as_posix()}` -- the marginalised posterior mean over the "
          "restricted plane, i.e. the same computation as the adopted band above. Caption values for "
          "the paper's Fig. 6 are the restricted columns of the first table, verbatim:", ""]
    for name, v in verdicts.items():
        L.append(f"- {name}: [{v['lo']:+.2f}, {v['hi']:+.2f}], {v['verdict']}"
                 + (" (flatness gate rejects; report the union bound)" if v["gated"] else ""))
    text = "\n".join(L)
    out.write_text(text, encoding="utf-8")
    print(text)
    print("\nFig6 caption values (restricted simultaneous band, the adopted rung):")
    for name, v in verdicts.items():
        print(f"  {name}: [{v['lo']:+.3f}, {v['hi']:+.3f}] {v['verdict']}"
              f"{'  GATED' if v['gated'] else ''}   extended: [{v['lo_ext']:+.3f}, {v['hi_ext']:+.3f}] {v['verdict_ext']}")


if __name__ == "__main__":
    main()
