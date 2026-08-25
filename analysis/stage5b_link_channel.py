"""Stage 5B-2: global null-sector link diagnostic and its locality limits.

Scope
-----
Stage 5A established a candidate *global* two-sector precursor in 1+1D:
    (C, <) -> {U, V} / S_2.
This file tests a deliberately simple order+number diagnostic on causal links,

    chi(x<.y) = U      if Delta r_U > Delta r_V
                 V      if Delta r_V > Delta r_U
                 BOTTOM if Delta r_U = Delta r_V,

where r_U,r_V are ranks in the two global total orders.  BOTTOM is required by
U<->V covariance: a tie is invariant under the swap and therefore cannot be
assigned to either named sector without an extra convention.

The file does NOT claim that chi is chirality or a microscopic local channel.
It records two limits:
  1. Pure causal order fixes only conformal structure.  Independent monotone
     u->f(u), v->g(v) preserve the 1+1D order but can change a metric target such
     as sign(Delta u - Delta v).  Number/volume information is therefore needed
     to select a metric representative.  This is a scope statement about a
     metric link-direction target, not a no-go for every possible two-state
     internal space.
  2. The rank diagnostic uses population in strips outside the empty link
     Alexandrov interval.  A constructive link-external intervention can change
     chi while preserving all old-old order relations and preserving the target
     pair as a link.  The benchmark separately requires an intrinsic order-depth
     threshold, so "outside the interval" is not misreported as independent
     remoteness evidence.  Hence this particular chi is not a microscopic
     link-local rule.

Independent literature constraint
---------------------------------
Bombelli, Henson & Sorkin, "Discreteness without symmetry breaking: a theorem",
arXiv:gr-qc/0605006, prove that there is no equivariant measurable map from a
Poisson sprinkling of full Minkowski spacetime to a spacetime direction, even
locally; a finite-valency Lorentz-equivariant graph assignment is a consequence.
Therefore checkerboard-like intrinsic nearest-neighbour direction selection is
not an allowed mainline construction.  This literature theorem is separate from
this file's project-level rank/intervention tests.

This stage deliberately stops before any fermionic kernel K is proposed.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

BOTTOM = "BOTTOM"
REMOTE_MIN_OLD_INTERVAL = 5


def sprinkle_2d_with_coords(N: int, rng: np.random.Generator):
    """Uniform 1+1D causal-diamond sprinkling in null-square coordinates."""
    u = rng.random(N)
    v = rng.random(N)
    R = (u[:, None] < u[None, :]) & (v[:, None] < v[None, :])
    return u, v, R


def order_from_uv(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    return (u[:, None] < u[None, :]) & (v[:, None] < v[None, :])


def rank_array(values: np.ndarray) -> np.ndarray:
    """0-based rank in the strictly ordered finite sample."""
    order = np.argsort(values)
    ranks = np.empty(len(values), dtype=int)
    ranks[order] = np.arange(len(values))
    return ranks


def link_matrix(R: np.ndarray) -> np.ndarray:
    """Transitive reduction relation x<.y for a finite poset relation matrix."""
    A = R.astype(np.int32)
    has_middle = (A @ A) > 0
    return R & ~has_middle


def rank_channel(rU: np.ndarray, rV: np.ndarray, x: int, y: int) -> str:
    """Three-valued S_2-equivariant rank channel for a related pair x<y."""
    dU = int(rU[y] - rU[x])
    dV = int(rV[y] - rV[x])
    if dU > dV:
        return "U"
    if dV > dU:
        return "V"
    return BOTTOM


def metric_channel(u: np.ndarray, v: np.ndarray, x: int, y: int) -> str:
    """Coordinate diagnostic used only as a sealed continuum benchmark."""
    du = float(u[y] - u[x])
    dv = float(v[y] - v[x])
    if du > dv:
        return "U"
    if dv > du:
        return "V"
    return BOTTOM


def channels_on_links(u: np.ndarray, v: np.ndarray):
    R = order_from_uv(u, v)
    L = link_matrix(R)
    rU, rV = rank_array(u), rank_array(v)
    out = []
    for x, y in zip(*np.nonzero(L)):
        out.append((x, y, rank_channel(rU, rV, x, y), metric_channel(u, v, x, y)))
    return R, L, out


@dataclass(frozen=True)
class InterventionResult:
    old_channel: str
    new_channel: str
    added: int
    old_dU: int
    old_dV: int
    new_dU: int
    new_dV: int
    old_relation_preserved: bool
    link_preserved: bool
    old_interval_to_y_counts: tuple[int, ...]


def _is_link(R: np.ndarray, x: int, y: int) -> bool:
    return bool(R[x, y] and not np.any(R[x] & R[:, y]))


def flip_by_link_external_population(
    u: np.ndarray, v: np.ndarray, x: int, y: int
) -> tuple[np.ndarray, np.ndarray, InterventionResult]:
    """Constructively flip rank_channel using population outside I(x,y).

    If chi=U, add points with u<u_x but v_x<v<v_y. They increase Delta r_V
    only. If chi=V, use the exchanged construction. No old coordinates move,
    so every old-old order relation is exactly preserved. Because the target
    pair remains a link, no added point lies in the open Alexandrov interval.

    The returned ``old_interval_to_y_counts`` is the independent intrinsic
    separation diagnostic: for every added point w it counts only *pre-existing*
    events z with w<z<y. The source-of-record benchmark requires this count to
    be at least REMOTE_MIN_OLD_INTERVAL for every added point; link preservation
    itself is not treated as evidence of remoteness.
    """
    R0 = order_from_uv(u, v)
    if not _is_link(R0, x, y):
        raise ValueError("intervention target must be a causal link")
    rU0, rV0 = rank_array(u), rank_array(v)
    old = rank_channel(rU0, rV0, x, y)
    if old == BOTTOM:
        raise ValueError("cannot define a flip direction for a tie")
    dU0 = int(rU0[y] - rU0[x])
    dV0 = int(rV0[y] - rV0[x])
    nadd = abs(dU0 - dV0) + 1

    # Put the active coordinate near the x-side of its slab and the other
    # coordinate on the low outer wing. This tends to create substantial
    # causal depth to y, but the benchmark accepts a candidate only after the
    # order-theoretic depth has been measured; coordinates are not the criterion.
    frac = np.linspace(0.04, 0.12, nadd)
    lowfrac = np.linspace(0.02, 0.08, nadd)
    if old == "U":
        # Increase only the V-rank gap.
        unew = u[x] * lowfrac
        vnew = v[x] + frac * (v[y] - v[x])
    else:
        # Increase only the U-rank gap.
        unew = u[x] + frac * (u[y] - u[x])
        vnew = v[x] * lowfrac

    n0 = len(u)
    ua = np.concatenate([u, unew])
    va = np.concatenate([v, vnew])
    Ra = order_from_uv(ua, va)
    rUa, rVa = rank_array(ua), rank_array(va)
    new = rank_channel(rUa, rVa, x, y)
    dUa = int(rUa[y] - rUa[x])
    dVa = int(rVa[y] - rVa[x])

    # Intrinsic depth: count only old events in each I(w,y), so the intervention
    # cannot make itself look remote by adding its own intermediate points.
    old_depths = []
    for k in range(n0, len(ua)):
        old_depths.append(int(np.sum(Ra[k, :n0] & Ra[:n0, y])))

    result = InterventionResult(
        old_channel=old,
        new_channel=new,
        added=nadd,
        old_dU=dU0,
        old_dV=dV0,
        new_dU=dUa,
        new_dV=dVa,
        old_relation_preserved=bool(np.array_equal(Ra[:n0, :n0], R0)),
        link_preserved=_is_link(Ra, x, y),
        old_interval_to_y_counts=tuple(old_depths),
    )
    return ua, va, result


def benchmark(seed: int = 55002, N: int = 300, interventions: int = 60):
    """Deterministic source-of-record benchmark for Stage 5B-2."""
    rng = np.random.default_rng(seed)
    u, v, R = sprinkle_2d_with_coords(N, rng)
    L = link_matrix(R)
    rU, rV = rank_array(u), rank_array(v)
    links = list(zip(*np.nonzero(L)))

    non_tie = []
    agree = 0
    ties = 0
    for x, y in links:
        rc = rank_channel(rU, rV, x, y)
        mc = metric_channel(u, v, x, y)
        if rc == BOTTOM:
            ties += 1
        else:
            non_tie.append((x, y))
            agree += (rc == mc)

    # Conformal-order witness: order and ranks are unchanged, while the metric
    # diagnostic need not be.  The transformed points are NOT a uniform
    # sprinkling in the transformed coordinates; this is only a witness that
    # the metric target is not pure-order data.
    uf = u ** 3
    vg = v ** 0.25
    assert np.array_equal(order_from_uv(uf, vg), R)
    assert np.array_equal(rank_array(uf), rU)
    assert np.array_equal(rank_array(vg), rV)
    metric_flips = 0
    metric_comparable = 0
    for x, y in links:
        before = metric_channel(u, v, x, y)
        after = metric_channel(uf, vg, x, y)
        if before != BOTTOM and after != BOTTOM:
            metric_comparable += 1
            metric_flips += (before != after)

    # Constructive witness, not an unbiased population estimate. Sort by rank
    # margin, but accept a link only if every added point is intrinsically
    # order-separated from y by at least REMOTE_MIN_OLD_INTERVAL old events.
    candidates = sorted(
        [
            (abs(int(rU[y] - rU[x]) - int(rV[y] - rV[x])), x, y)
            for x, y in non_tie
        ],
        key=lambda t: (t[0], t[1], t[2]),
    )
    results = []
    candidates_scanned = 0
    for _, x, y in candidates:
        candidates_scanned += 1
        _, _, res = flip_by_link_external_population(u, v, x, y)
        if min(res.old_interval_to_y_counts) < REMOTE_MIN_OLD_INTERVAL:
            continue
        results.append(res)
        if len(results) == interventions:
            break
    if len(results) != interventions:
        raise RuntimeError(
            f"only {len(results)} links met intrinsic order-depth threshold "
            f"{REMOTE_MIN_OLD_INTERVAL}"
        )
    all_depths = [d for r in results for d in r.old_interval_to_y_counts]

    return {
        "N": N,
        "links": len(links),
        "ties": ties,
        "tie_fraction": ties / len(links),
        "non_tie_agreement": agree / max(len(non_tie), 1),
        "conformal_metric_flips": metric_flips,
        "conformal_metric_comparable": metric_comparable,
        "conformal_flip_fraction": metric_flips / max(metric_comparable, 1),
        "interventions": len(results),
        "intervention_flips": sum(r.old_channel != r.new_channel for r in results),
        "median_added": float(np.median([r.added for r in results])) if results else float("nan"),
        "total_added": int(sum(r.added for r in results)),
        "remote_min_old_interval_threshold": REMOTE_MIN_OLD_INTERVAL,
        "remote_candidates_scanned": candidates_scanned,
        "min_old_interval_to_y": int(min(all_depths)),
        "median_old_interval_to_y": float(np.median(all_depths)),
        "max_old_interval_to_y": int(max(all_depths)),
        "all_old_relations_preserved": all(r.old_relation_preserved for r in results),
        "all_links_preserved": all(r.link_preserved for r in results),
    }


if __name__ == "__main__":
    b = benchmark()
    for k, val in b.items():
        print(f"{k}: {val}")
