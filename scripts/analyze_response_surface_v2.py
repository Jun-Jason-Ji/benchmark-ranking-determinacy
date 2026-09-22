"""Response-surface bound v2: simultaneous posterior band over the replay-compatible strip, with
hyperparameter marginalisation and a flatness gate.

Improvements over analyze_response_surface.py:
  * simultaneous 95% band: sample GP posterior functions on the strip grid (marginalising the (ℓ, σf)
    grid with weights ∝ exp(−NLL)); L = 2.5th percentile of the per-draw minimum, U = 97.5th percentile
    of the per-draw maximum. This bounds the whole strip, not one point at a time.
  * flatness gate per axis: paired bootstrap of Δ(c) − Δ(nominal) for every calibration-invisible
    condition on the axis; if any interval excludes 0 the surface model is not trusted on that axis and
    the union bound (analysis_compatible_set.md) is reported instead.
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
from analyze_response_surface import ENVS, DESIGN, EPS, SWEEP, success, observations, rbf  # noqa: E402

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


def main():
    out = SWEEP / "analysis_response_surface_v2.md"
    g = np.linspace(-2.5, 2.5, 41)
    U, V = np.meshgrid(g, g, indexing="ij")
    Xs_all = np.stack([U.ravel(), V.ravel()], 1)
    Xs = Xs_all[np.abs(Xs_all[:, 0] - Xs_all[:, 1]) <= EPS]
    L = ["# Response-surface bound v2: simultaneous 95% band over the compatible strip + flatness gate", "",
         f"Strip |log2 k − log2 d| ≤ {EPS}; GP hyperparameters marginalised over a (ℓ, σf) grid with weights ∝ exp(−NLL); "
         "4000 posterior function draws; L/U = 2.5th pct of draw-minimum / 97.5th pct of draw-maximum. "
         "Flatness gate: paired Δ(c) − Δ(nominal) over the calibration-invisible controller conditions; '*' = rejects flatness.", "",
         "| task | controller strip: simultaneous bound | verdict | top (weight, ℓ, σf) | flatness gate (controller-invisible) | union bound verdict |", "|---|---|---|---|---|---|"]
    union = json.loads((SWEEP / "analysis_compatible_set.json").read_text(encoding="utf-8"))["summary"] if (SWEEP / "analysis_compatible_set.json").exists() else {}
    for name, env in ENVS.items():
        X, y, se, names = observations(env)
        lo, hi, top = simultaneous_bounds(X, y, se, Xs)
        rej, det = flatness_gate(env, ["iso_x0.25", "iso_x0.5", "iso_x2.0", "iso_x4.0", "force_x0.5"])
        ub = union.get(name, {}).get("set_controller", "n/a")
        L.append(f"| {name} | [{lo:+.2f}, {hi:+.2f}] | {verdict(lo, hi)}{' (gated → union bound)' if rej else ''} | {top} | {'; '.join(det)} | {ub} |")
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
    text = "\n".join(L)
    out.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
