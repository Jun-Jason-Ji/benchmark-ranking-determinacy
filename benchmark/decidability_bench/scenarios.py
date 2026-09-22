"""Track S scenario generator: ground-truth Δ(z) surfaces on the (log2 k, log2 d) plane and paired
Bernoulli outcomes with common random numbers (Gaussian copula shared across conditions and policies).

Design points and the compatible strip are identical to the real analysis pipeline
(scripts/analyze_response_surface.py: DESIGN, EPS)."""
from statistics import NormalDist

import numpy as np

DESIGN = {"nominal": (0, 0), "stiff_x0.5": (-1, 0), "stiff_x2.0": (1, 0), "damp_x0.5": (0, -1), "damp_x2.0": (0, 1),
          "stiff_x0.25": (-2, 0), "stiff_x4.0": (2, 0), "damp_x0.25": (0, -2), "damp_x4.0": (0, 2),
          "iso_x0.25": (-2, -2), "iso_x0.5": (-1, -1), "iso_x2.0": (1, 1), "iso_x4.0": (2, 2)}
EPS = 0.25
STRIP_CONDS = [c for c, (u, v) in DESIGN.items() if abs(u - v) <= EPS]  # nominal + 4 iso points
ISO_CONDS = [c for c in STRIP_CONDS if c != "nominal"]

P_BASE = 0.35   # weaker policy's success rate (mid-success regime, as selected for near-tied pairs)
RHO = 0.3       # copula correlation induced by common random numbers
_ND = NormalDist()


def surface(kind, d0):
    """Return Δ(u, v) as a vectorised function. s = (u+v)/2 (invisible scale axis), r = u−v (visible ratio axis)."""
    def f(u, v):
        u, v = np.asarray(u, float), np.asarray(v, float)
        s, r = (u + v) / 2.0, u - v
        vis = -0.05 * r ** 2
        if kind == "flat":
            return d0 + vis
        if kind == "linear":
            return d0 + 0.04 * s + vis
        if kind == "dip_sampled":
            return d0 - 0.25 * np.exp(-(s + 2.0) ** 2 / (2 * 0.5 ** 2)) + vis
        if kind == "dip_unsampled":
            return d0 - 0.25 * np.exp(-(s - 1.5) ** 2 / (2 * 0.3 ** 2)) + vis
        raise ValueError(kind)
    return f


import os
S_MAX = float(os.environ.get("DB_SMAX", "2.5"))  # strip extent along the scale axis; 2.5 = extrapolate 0.5 beyond the sampled ±2 (as in analysis v2), 2.0 = sampled range only


def strip_grid(n_s=81, n_r=5):
    """Points covering the compatible strip: s ∈ [−S_MAX, S_MAX], r ∈ [−EPS, EPS] (u = s + r/2, v = s − r/2)."""
    s = np.linspace(-S_MAX, S_MAX, n_s)
    r = np.linspace(-EPS, EPS, n_r)
    S, R = np.meshgrid(s, r, indexing="ij")
    return np.stack([(S + R / 2).ravel(), (S - R / 2).ravel()], 1)


def truth_bounds(delta_fn, grid=None):
    grid = strip_grid() if grid is None else grid
    vals = delta_fn(grid[:, 0], grid[:, 1])
    return float(vals.min()), float(vals.max())


def sample_outcomes(delta_fn, n, rng):
    """Returns dict cond -> (succ_A[n], succ_B[n]) with shared per-episode latent (common random numbers)."""
    xi = rng.standard_normal(n)
    out = {}
    for c, (u, v) in DESIGN.items():
        pb = P_BASE
        pa = float(np.clip(pb + delta_fn(u, v), 0.02, 0.98))
        za = np.sqrt(RHO) * xi + np.sqrt(1 - RHO) * rng.standard_normal(n)
        zb = np.sqrt(RHO) * xi + np.sqrt(1 - RHO) * rng.standard_normal(n)
        out[c] = ((za < _ND.inv_cdf(pa)).astype(int), (zb < _ND.inv_cdf(pb)).astype(int))
    return out
