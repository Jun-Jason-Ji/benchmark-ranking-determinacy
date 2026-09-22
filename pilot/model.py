"""Exact confidence-set geometry for a synthetic two-parameter linear model.

This is an analytical mechanism check, not a robot simulator. No SciPy needed.
"""
from statistics import NormalDist
import math

import numpy as np


BOX = (0.0, 1.0)
S = np.array([1.0, 1.0]) / math.sqrt(2.0)
D = np.array([1.0, -1.0]) / math.sqrt(2.0)
G = np.array([1.0, -1.0])
DIRECTIONS = np.array([S, D, [1.0, 0.0], [0.0, 1.0]])


def chi_square_quantile(rank, alpha):
    """Exact elementary quantiles for ranks 0, 1, 2."""
    if not 0 < alpha < 1:
        raise ValueError("alpha must lie in (0, 1)")
    if rank == 0:
        return 0.0
    if rank == 1:
        return NormalDist().inv_cdf(1 - alpha / 2) ** 2
    if rank == 2:
        return -2 * math.log(alpha)
    raise ValueError("only ranks 0, 1 and 2 are supported")


def fit(x, y):
    a = x.T @ x
    center = np.linalg.pinv(a, rcond=1e-12) @ x.T @ y
    rank = int(np.linalg.matrix_rank(a, tol=1e-10))
    return a, center, rank


def contains(a, center, radius2, theta, box=BOX):
    theta = np.asarray(theta)
    return bool(np.all(theta >= box[0]) and np.all(theta <= box[1])
                and (theta - center) @ a @ (theta - center) <= radius2 + 1e-10)


def linear_extrema(a, center, radius2, g=G, box=BOX):
    """Continuous extrema on {theta in box: (theta-center)'A(...)<=r^2}.

    In 2D a linear functional reaches its extremum at either an unconstrained
    ellipsoid support point, a box corner, or an ellipse/box-edge intersection.
    In rank-one cases an interior optimum either has equal-value boundary
    representatives or is constant; enumerating edges thus also suffices.
    Returns None for an empty intersection. Numerical roundoff remains possible.
    """
    a = np.asarray(a, dtype=float)
    center = np.asarray(center, dtype=float)
    g = np.asarray(g, dtype=float)
    lo, hi = box
    candidates = []

    def add(z):
        if (np.all(z >= lo - 1e-9) and np.all(z <= hi + 1e-9)
                and (z - center) @ a @ (z - center) <= radius2 + 1e-8):
            candidates.append(np.clip(z, lo, hi))

    for u in (lo, hi):
        for v in (lo, hi):
            add(np.array([u, v]))

    if np.linalg.matrix_rank(a, tol=1e-10) == 2:
        direction = np.linalg.solve(a, g)
        denominator = float(g @ direction)
        if denominator > 1e-20:
            offset = math.sqrt(max(radius2, 0) / denominator) * direction
            add(center + offset)
            add(center - offset)

    for fixed_dim in (0, 1):
        free_dim = 1 - fixed_dim
        for fixed_value in (lo, hi):
            fixed_offset = fixed_value - center[fixed_dim]
            aa = a[free_dim, free_dim]
            bb = 2 * a[fixed_dim, free_dim] * fixed_offset
            cc = a[fixed_dim, fixed_dim] * fixed_offset ** 2 - radius2
            if aa > 1e-14:
                disc = bb ** 2 - 4 * aa * cc
                if disc >= -1e-10:
                    root = math.sqrt(max(disc, 0))
                    for offset in ((-bb - root) / (2 * aa),
                                   (-bb + root) / (2 * aa)):
                        z = center.copy()
                        z[fixed_dim] = fixed_value
                        z[free_dim] += offset
                        add(z)
            elif abs(bb) > 1e-14:
                z = center.copy()
                z[fixed_dim] = fixed_value
                z[free_dim] -= cc / bb
                add(z)

    # Covers a degenerate singleton inside the box (zero-radius full rank).
    add(center)
    if not candidates:
        return None
    values = np.array([g @ z for z in candidates])
    return (float(values.min()), float(values.max()),
            candidates[int(values.argmin())].tolist(),
            candidates[int(values.argmax())].tolist())


def confidence_interval(a, center, rank, sigma, alpha, g=G):
    radius2 = sigma ** 2 * chi_square_quantile(rank, alpha)
    return radius2, linear_extrema(a, center, radius2, g)


def contrast_wald(a, center, sigma, alpha, g=G):
    """Classical scalar interval when g is estimable; otherwise box range.

    Valid for this single prespecified contrast and fixed response-independent
    design. It does not share the simultaneous parameter-set guarantee.
    """
    pinv = np.linalg.pinv(a, rcond=1e-12)
    if np.linalg.norm(g - a @ pinv @ g) > 1e-7:
        return -1.0, 1.0
    half_width = NormalDist().inv_cdf(1 - alpha / 2) * sigma * math.sqrt(g @ pinv @ g)
    estimate = float(g @ center)
    return max(-1.0, estimate - half_width), min(1.0, estimate + half_width)


def classify(lower, upper, delta):
    return 1 if lower > delta else (-1 if upper < -delta else 0)


def select_order(method, pool_x, initial_x, rng, ridge):
    """Selections depend on visible inputs only, never hidden outcomes."""
    remaining = list(range(len(pool_x)))
    a = initial_x.T @ initial_x
    order = []
    while remaining:
        if method == "random":
            chosen = remaining[int(rng.integers(len(remaining)))]
        else:
            scores = []
            for idx in remaining:
                candidate_a = a + np.outer(pool_x[idx], pool_x[idx]) + ridge * np.eye(2)
                if method == "d_opt":
                    score = np.linalg.slogdet(candidate_a)[1]
                elif method == "c_opt":
                    score = -float(G @ np.linalg.solve(candidate_a, G))
                else:
                    raise ValueError(method)
                scores.append(score)
            # Stable tie-breaking, identical metadata available to all methods.
            chosen = remaining[int(np.argmax(scores))]
        order.append(chosen)
        a += np.outer(pool_x[chosen], pool_x[chosen])
        remaining.remove(chosen)
    return order
