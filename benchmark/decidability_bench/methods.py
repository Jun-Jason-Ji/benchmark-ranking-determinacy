"""Verdict methods evaluated by the benchmark. All take the same input:
    data: dict cond -> (succ_A[n], succ_B[n])   (paired by index = episode_id)
and return (L, U, verdict) where verdict ∈ {"+", "−", "0"} is the CI-supported sign over the compatible strip.

`gp_sim` reuses nll/posterior/ELLS/SFS from scripts/analyze_response_surface_v2.py so the benchmark exercises
the same code path as the real analysis."""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from analyze_response_surface_v2 import nll, posterior, ELLS as _ELLS_ALL, SFS  # noqa: E402
import os
ELL_MIN = float(os.environ.get("DB_ELL_MIN", "0"))  # lower bound on the GP length-scale grid (log2 units); 1.0 = design spacing
ELLS = [e for e in _ELLS_ALL if e >= ELL_MIN]
from scenarios import DESIGN, STRIP_CONDS, ISO_CONDS, strip_grid  # noqa: E402

GRID = strip_grid(n_s=41, n_r=3)
METHODS = ["point", "union", "gp_sim", "gated"]


def paired_ci(a, b, rng, n_boot=2000, alpha=0.05):
    d = (a - b).astype(float)
    idx = rng.integers(0, len(d), size=(n_boot, len(d)))
    m = d[idx].mean(1)
    return float(d.mean()), float(np.percentile(m, 100 * alpha / 2)), float(np.percentile(m, 100 * (1 - alpha / 2)))


def sign(lo, hi):
    return "+" if lo > 0 else ("−" if hi < 0 else "0")


def point(data, rng, **kw):
    a, b = data["nominal"]
    _, lo, hi = paired_ci(a, b, rng)
    return lo, hi, sign(lo, hi)


def union(data, rng, **kw):
    los, his = [], []
    for c in STRIP_CONDS:
        a, b = data[c]
        _, lo, hi = paired_ci(a, b, rng)
        los.append(lo); his.append(hi)
    lo, hi = min(los), max(his)
    return lo, hi, sign(lo, hi)


def _observations(data):
    X, y, se = [], [], []
    for c, (u, v) in DESIGN.items():
        a, b = data[c]
        d = (a - b).astype(float)
        X.append((u, v)); y.append(d.mean()); se.append(d.std(ddof=1) / np.sqrt(len(d)) + 1e-6)
    return np.array(X, float), np.array(y), np.array(se)


def gp_sim(data, rng, n_draws=1000, **kw):
    X, y, se = _observations(data)
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
        mu, cov = posterior(X, y, se, ell, sf, m0, GRID)
        Lc = np.linalg.cholesky(cov + 1e-9 * np.eye(len(mu)))
        f = mu[None, :] + rng.standard_normal((k, len(mu))) @ Lc.T
        mins.append(f.min(1)); maxs.append(f.max(1))
    mins, maxs = np.concatenate(mins), np.concatenate(maxs)
    lo, hi = float(np.percentile(mins, 2.5)), float(np.percentile(maxs, 97.5))
    return lo, hi, sign(lo, hi)


def flatness_rejects(data, rng):
    a0, b0 = data["nominal"]
    d0 = (a0 - b0).astype(float)
    for c in ISO_CONDS:
        a, b = data[c]
        _, lo, hi = paired_ci((a - b).astype(float) - d0, np.zeros(len(d0)), rng)
        if lo > 0 or hi < 0:
            return True
    return False


def gated(data, rng, **kw):
    if flatness_rejects(data, rng):
        lo, hi, s = union(data, rng)
        return lo, hi, s
    return gp_sim(data, rng, **kw)


REGISTRY = {"point": point, "union": union, "gp_sim": gp_sim, "gated": gated}
