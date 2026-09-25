"""Response-surface version of the compatible-set bound (proposal 5.3): fit a Gaussian-process surface
Δ(u, v) over the controller plane u = log2(stiffness scale), v = log2(damping scale) from the paired
per-condition estimates, then bound Δ over the replay-compatible strip |u − v| ≤ eps (ratio ≈ 1) with the
posterior band, instead of taking extremes over the few sampled conditions.

Numpy-only GP: RBF kernel + constant mean, heteroscedastic noise = bootstrap SE^2 of each condition mean,
hyperparameters (length scale, signal sd) by marginal-likelihood grid search.
Outputs analysis_response_surface.md and results/figures/fig_response_surface.png.
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
SWEEP = ROOT / "results/controller_sweep_gpu"
ENVS = {"carrot": "PutCarrotOnPlateInScene-v1", "spoon": "PutSpoonOnTableClothInScene-v1", "eggplant": "PutEggplantInBasketScene-v1"}
DESIGN = {"nominal": (0, 0), "stiff_x0.5": (-1, 0), "stiff_x2.0": (1, 0), "damp_x0.5": (0, -1), "damp_x2.0": (0, 1),
          "stiff_x0.25": (-2, 0), "stiff_x4.0": (2, 0), "damp_x0.25": (0, -2), "damp_x4.0": (0, 2),
          "iso_x0.25": (-2, -2), "iso_x0.5": (-1, -1), "iso_x2.0": (1, 1), "iso_x4.0": (2, 2)}
EPS = 0.25  # half-width of the compatible strip in log2 ratio units (ratio 0.7 = 0.51 is already excluded by replay)


def success(policy, env, cond):
    f = SWEEP / policy / env / f"{cond}.jsonl"
    if not f.exists():
        return {}
    return {json.loads(l)["episode_id"]: int(bool(json.loads(l)["success"])) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()}


def observations(env):
    X, y, se, names = [], [], [], []
    for c, (u, v) in DESIGN.items():
        S, B = success("octo-small", env, c), success("octo-base", env, c)
        common = sorted(set(S) & set(B))
        if len(common) < 12:
            continue
        d = np.array([S[i] - B[i] for i in common], float)
        X.append((u, v)); y.append(d.mean()); se.append(d.std(ddof=1) / np.sqrt(len(d)) + 1e-6); names.append(f"{c} (n={len(d)})")
    return np.array(X, float), np.array(y), np.array(se), names


def rbf(A, B, ell, sf):
    d2 = ((A[:, None, :] - B[None, :, :]) ** 2).sum(-1)
    return sf ** 2 * np.exp(-0.5 * d2 / ell ** 2)


def fit_gp(X, y, se):
    best = None
    m0 = y.mean()
    for ell in [0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0]:
        for sf in [0.02, 0.05, 0.1, 0.15, 0.2, 0.3]:
            K = rbf(X, X, ell, sf) + np.diag(se ** 2)
            try:
                Lc = np.linalg.cholesky(K)
            except np.linalg.LinAlgError:
                continue
            a = np.linalg.solve(Lc.T, np.linalg.solve(Lc, y - m0))
            nll = 0.5 * (y - m0) @ a + np.log(np.diag(Lc)).sum() + 0.5 * len(y) * np.log(2 * np.pi)
            if best is None or nll < best[0]:
                best = (nll, ell, sf)
    return best[1], best[2], m0


def predict(X, y, se, ell, sf, m0, Xs):
    K = rbf(X, X, ell, sf) + np.diag(se ** 2)
    Ks = rbf(Xs, X, ell, sf)
    Kss = rbf(Xs, Xs, ell, sf)
    Lc = np.linalg.cholesky(K)
    a = np.linalg.solve(Lc.T, np.linalg.solve(Lc, y - m0))
    mu = m0 + Ks @ a
    V = np.linalg.solve(Lc, Ks.T)
    var = np.clip(np.diag(Kss) - (V * V).sum(0), 1e-12, None)
    return mu, np.sqrt(var)


def main():
    g = np.linspace(-2.5, 2.5, 61)
    U, Vv = np.meshgrid(g, g, indexing="ij")
    Xs = np.stack([U.ravel(), Vv.ravel()], 1)
    strip = np.abs(Xs[:, 0] - Xs[:, 1]) <= EPS
    L = ["# Response-surface bound over the replay-compatible controller strip", "",
         f"GP over (log2 stiffness scale, log2 damping scale); compatible strip |u − v| ≤ {EPS} (ratio ≈ 1). "
         "Bounds: min/max over the strip of posterior mean ∓/± k·sd, k = 2 (pointwise) and k = 3 (crude simultaneous).", "",
         "| task | n obs | length scale | signal sd | bound k=2 | verdict k=2 | bound k=3 | verdict k=3 | point (nominal) |", "|---|---:|---:|---:|---|---|---|---|---|"]
    fig, axes = plt.subplots(1, 3, figsize=(6.85, 2.9))  # 174 mm journal full-column width
    out = {}
    for ax, (name, env) in zip(axes, ENVS.items()):
        X, y, se, names = observations(env)
        ell, sf, m0 = fit_gp(X, y, se)
        mu, sd = predict(X, y, se, ell, sf, m0, Xs)
        res = {}
        for k in (2, 3):
            lo = (mu - k * sd)[strip].min(); hi = (mu + k * sd)[strip].max()
            res[k] = (lo, hi, "small better" if lo > 0 else ("base better" if hi < 0 else "abstain"))
        nom = names.index(next(n for n in names if n.startswith("nominal")))
        pv = y[nom] - 1.96 * se[nom]
        point = "small better" if pv > 0 else ("base better" if y[nom] + 1.96 * se[nom] < 0 else "abstain")
        L.append(f"| {name} | {len(y)} | {ell:g} | {sf:g} | [{res[2][0]:+.2f}, {res[2][1]:+.2f}] | {res[2][2]} | [{res[3][0]:+.2f}, {res[3][1]:+.2f}] | {res[3][2]} | {point} |")
        out[name] = dict(ell=ell, sf=sf, k2=res[2], k3=res[3], point=point, obs=list(zip(names, y.tolist(), se.tolist())))
        im = ax.imshow(mu.reshape(U.shape).T, origin="lower", extent=[-2.5, 2.5, -2.5, 2.5], cmap="RdBu_r", vmin=-0.4, vmax=0.4)
        ax.plot([-2.5, 2.5], [-2.5 - EPS, 2.5 - EPS], "k--", lw=0.8); ax.plot([-2.5, 2.5], [-2.5 + EPS, 2.5 + EPS], "k--", lw=0.8)
        ax.scatter(X[:, 0], X[:, 1], c=y, cmap="RdBu_r", vmin=-0.4, vmax=0.4, edgecolors="k", s=40)
        ax.set_xlabel("log$_2$ stiffness scale", fontsize=8)
        ax.tick_params(labelsize=8)
        if ax is axes[0]:
            ax.set_ylabel("log$_2$ damping scale", fontsize=8)
        # Bounds, hyperparameters and verdicts go in the caption, not inside the figure file
        # (the journal forbids titles in figures, and at 174 mm they do not fit anyway).
        ax.set_title(name, fontsize=8.5)
    cb = fig.colorbar(im, ax=axes, label="posterior mean $\\Delta$", shrink=0.85)
    cb.ax.tick_params(labelsize=8)
    cb.set_label("posterior mean $\\Delta$", size=8)
    (ROOT / "results/figures").mkdir(exist_ok=True)
    fig.savefig(ROOT / "results/figures/fig_response_surface.png", dpi=180, bbox_inches="tight"); plt.close(fig)
    L += ["", "Observations per task (condition, Δ, SE):", ""]
    for name, o in out.items():
        L.append(f"- {name}: " + "; ".join(f"{n}: {v:+.3f}±{s:.3f}" for n, v, s in o["obs"]))
    L += ["", "Caveats: 13 design points; SE from per-episode paired differences; k=3 is a crude simultaneous factor, not a certified band. "
          "Delay, force limit and contact parameters are separate axes and are not in this surface."]
    text = "\n".join(L)
    (SWEEP / "analysis_response_surface.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
