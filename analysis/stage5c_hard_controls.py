"""Candidate-independent hard controls for Stage 5C C8.4.

This module deliberately contains no candidate kernel.  It constructs two
1+1-dimensional continuum targets whose finite sprinklings remain permutation
orders, while their continuum massless-chiral transfer targets have opposite
directions.  The two targets are designed to agree on easy nuisance summaries:
they have the same spacetime volume, uniform null-coordinate marginals, and an
exact ordering fraction of 1/2 in expectation.

The conformal-volume density on the unit null square is

    p_theta(u, v) = 1 + theta * q(u) * q(v),
    q(z) = 6 z**2 - 6 z + 1,

with theta = +/- CONTROL_THETA.  Taking

    ds^2 = -2 p_theta(u, v) du dv

makes p_theta du dv the physical volume measure without changing the causal
order.  Conditional on N, a Poisson sprinkling is therefore an iid sample from
p_theta.  The construction-facing payload contains only the order matrix; the
target sign and coordinates are evaluation-only metadata.

Status: feasibility implementation, not a Freeze-1a declaration.  The final
freeze must incorporate this control together with the remaining Appendix D.1
deliverables in one commit, as required by docs/STAGE5C_ACCEPTANCE.md.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json

import numpy as np
from scipy.optimize import linear_sum_assignment


CONTROL_THETA = 0.4
SOURCE_POINT = (0.05, 0.05)
SINK_POINT = (0.50, 0.05)
HEIGHT_CDF_BINS = (0.2, 0.4, 0.6, 0.8)
INTERVAL_ORDERS = (1, 2, 3, 4)
COMPONENT_CALIPER = 1.0
EUCLIDEAN_CALIPER = 2.0
MIN_MATCH_COVERAGE = 0.35
MIN_MATCHED_PAIRS = 192
MAX_ABSOLUTE_SMD = 0.20
MAX_KS_DISTANCE = 0.18
SOURCE_OF_RECORD_POOL_SIZE = 768
SOURCE_OF_RECORD_BASES = {
    "calibration_plus": 510_000_000,
    "calibration_minus": 520_000_000,
    "validation_plus": 530_000_000,
    "validation_minus": 540_000_000,
}
REPLICATION_BASES = (
    (910_000_000, 911_000_000, 912_000_000, 913_000_000),
    (920_000_000, 921_000_000, 922_000_000, 923_000_000),
    (930_000_000, 931_000_000, 932_000_000, 933_000_000),
    (940_000_000, 941_000_000, 942_000_000, 943_000_000),
)
FEATURE_NAMES = (
    "relation_density",
    "link_density",
    "height_over_sqrt_n",
    *(f"height_cdf_{q:.1f}" for q in HEIGHT_CDF_BINS),
    *(f"interval_abundance_{m}" for m in INTERVAL_ORDERS),
)


@dataclass(frozen=True)
class ControlSample:
    """One control causet plus sealed evaluator metadata."""

    order: np.ndarray
    coordinates: np.ndarray
    theta: float
    seed: int


@dataclass(frozen=True)
class MatchResult:
    left_indices: np.ndarray
    right_indices: np.ndarray
    distances: np.ndarray
    coverage: float
    max_standardized_mean_difference: float
    max_ks_distance: float


@dataclass(frozen=True)
class BlindedCase:
    """Construction-facing case: opaque id plus order, and nothing else."""

    case_id: str
    order: np.ndarray


def legendre_mode_2(z: np.ndarray | float) -> np.ndarray | float:
    """Shifted Legendre P_2, orthogonal to constants and linear functions."""
    return 6.0 * np.asarray(z) ** 2 - 6.0 * np.asarray(z) + 1.0


def conformal_volume_density(
    u: np.ndarray | float, v: np.ndarray | float, theta: float
) -> np.ndarray | float:
    """Normalized positive density p_theta on the unit null square."""
    if not (-1.0 < theta < 2.0):
        raise ValueError("theta must lie in (-1, 2) so p_theta is positive")
    return 1.0 + theta * legendre_mode_2(u) * legendre_mode_2(v)


def order_from_uv(coordinates: np.ndarray) -> np.ndarray:
    u, v = np.asarray(coordinates, dtype=float).T
    return (u[:, None] < u[None, :]) & (v[:, None] < v[None, :])


def _rng(seed: int) -> np.random.Generator:
    # Name the bit generator explicitly so the manifest does not depend on a
    # future change to numpy.default_rng's default.
    return np.random.Generator(np.random.PCG64DXSM(seed))


def sprinkle_control(n: int, theta: float, seed: int) -> ControlSample:
    """Fixed-N (Poisson-conditioned) sprinkling from p_theta by rejection."""
    if n < 2:
        raise ValueError("n must be at least 2")
    if not (-1.0 < theta < 2.0):
        raise ValueError("theta must lie in (-1, 2)")

    rng = _rng(seed)
    # q(u)q(v) is in [-1/2, 1].
    envelope = 1.0 + (theta if theta >= 0.0 else -0.5 * theta)
    chunks: list[np.ndarray] = []
    accepted = 0
    while accepted < n:
        batch = max(256, 3 * (n - accepted))
        points = rng.random((batch, 2))
        probability = conformal_volume_density(
            points[:, 0], points[:, 1], theta
        ) / envelope
        kept = points[rng.random(batch) < probability]
        chunks.append(kept)
        accepted += len(kept)
    coordinates = np.concatenate(chunks, axis=0)[:n]
    return ControlSample(
        order=order_from_uv(coordinates),
        coordinates=coordinates,
        theta=float(theta),
        seed=int(seed),
    )


def construction_payload(sample: ControlSample) -> dict[str, np.ndarray]:
    """The only payload that a future construction runner may receive."""
    return {"order": sample.order.copy()}


def blind_batch(
    samples: list[ControlSample], blinding_seed: int
) -> tuple[tuple[BlindedCase, ...], dict[str, int]]:
    """Randomize invocation order and split construction/evaluator views.

    The first return value is the only object passed to a future construction
    runner.  The second maps opaque case ids back to evaluator-side sample
    indices and must remain sealed until construction outputs are committed.
    """
    rng = _rng(blinding_seed)
    permutation = rng.permutation(len(samples))
    cases: list[BlindedCase] = []
    evaluator_index: dict[str, int] = {}
    for source_index in permutation:
        case_id = "C8-" + hashlib.sha256(rng.bytes(32)).hexdigest()[:24]
        case = BlindedCase(
            case_id=case_id,
            order=samples[int(source_index)].order.copy(),
        )
        cases.append(case)
        evaluator_index[case_id] = int(source_index)
    return tuple(cases), evaluator_index


def _open_interval_counts(order: np.ndarray) -> np.ndarray:
    a = np.asarray(order, dtype=np.int32)
    return a @ a


def baseline_features(order: np.ndarray) -> np.ndarray:
    """Exact C8.1 nuisance vector used by the feasibility benchmark.

    Height distribution means the empirical CDF of the longest-chain depth of
    each event, divided by the whole-causet height, at the four frozen bins.
    Interval abundance A_m is the number of related pairs whose open interval
    has m elements, divided by C(N,2).  A_0 is separately called link density.
    """
    r = np.asarray(order, dtype=bool)
    if r.ndim != 2 or r.shape[0] != r.shape[1]:
        raise ValueError("order must be a square matrix")
    n = r.shape[0]
    denominator = n * (n - 1) / 2
    intervals = _open_interval_counts(r)
    links = r & (intervals == 0)

    # Every relation increases both null coordinates, so sorting by the number
    # of predecessors is a valid intrinsic topological order.  Ties cannot be
    # related and need no label-dependent tie-break.
    predecessor_count = r.sum(axis=0)
    depth = np.ones(n, dtype=np.int32)
    for y in np.argsort(predecessor_count, kind="stable"):
        predecessors = np.flatnonzero(r[:, y])
        if predecessors.size:
            depth[y] = 1 + int(depth[predecessors].max())
    whole_height = int(depth.max())
    height_cdf = [
        float(np.mean(depth / whole_height <= q)) for q in HEIGHT_CDF_BINS
    ]
    abundance = [
        float(np.sum(r & (intervals == m)) / denominator)
        for m in INTERVAL_ORDERS
    ]
    return np.asarray(
        [
            float(r.sum() / denominator),
            float(links.sum() / denominator),
            float(whole_height / np.sqrt(n)),
            *height_cdf,
            *abundance,
        ]
    )


def calibration_scale(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    """Pooled calibration SD; no candidate output enters this calculation."""
    pooled = np.vstack([np.asarray(left, float), np.asarray(right, float)])
    scale = pooled.std(axis=0, ddof=1)
    if np.any(scale <= 0.0):
        raise ValueError("calibration produced a zero-variance nuisance feature")
    return scale


def expected_ordering_fraction(theta: float) -> float:
    """Analytic comparability probability for two iid p_theta points.

    q is orthogonal to both 1 and z on [0,1].  Expanding
    2 * integral p_theta(u,v) F_theta(u,v) du dv therefore cancels every
    theta-dependent term, leaving 1/2 exactly.  The argument applies throughout
    the positive-density parameter domain; theta is validated for consistency.
    """
    if not (-1.0 < theta < 2.0):
        raise ValueError("theta must lie in (-1, 2)")
    return 0.5


def _ks_distance(x: np.ndarray, y: np.ndarray) -> float:
    values = np.sort(np.concatenate([x, y]))
    fx = np.searchsorted(np.sort(x), values, side="right") / len(x)
    fy = np.searchsorted(np.sort(y), values, side="right") / len(y)
    return float(np.max(np.abs(fx - fy)))


def match_controls(
    left: np.ndarray,
    right: np.ndarray,
    scale: np.ndarray,
    *,
    component_caliper: float = COMPONENT_CALIPER,
    euclidean_caliper: float = EUCLIDEAN_CALIPER,
) -> MatchResult:
    """Maximum-cardinality optimal matching under fixed calipers.

    Invalid edges receive a cost larger than every possible valid assignment.
    Hungarian assignment then minimizes total standardized distance; invalid
    pairs are discarded.  Equal pool sizes are required so coverage has one
    unambiguous denominator.
    """
    x = np.asarray(left, float)
    y = np.asarray(right, float)
    scale = np.asarray(scale, float)
    if x.shape != y.shape or x.ndim != 2:
        raise ValueError("left and right feature pools must have equal 2D shape")
    if x.shape[1] != len(scale):
        raise ValueError("scale length does not match feature count")
    delta = np.abs((x[:, None, :] - y[None, :, :]) / scale)
    distance = np.sqrt(np.sum(delta**2, axis=2))
    invalid = (delta.max(axis=2) > component_caliper) | (
        distance > euclidean_caliper
    )
    cost = distance.copy()
    # One invalid edge costs more than an entire perfect assignment of valid
    # edges.  The first optimization criterion is therefore exact maximum
    # cardinality; total distance breaks ties among maximum-cardinality matches.
    invalid_cost = (len(x) + 1) * (euclidean_caliper + 1.0)
    cost[invalid] = invalid_cost
    left_indices, right_indices = linear_sum_assignment(cost)
    keep = ~invalid[left_indices, right_indices]
    left_indices = left_indices[keep]
    right_indices = right_indices[keep]
    if len(left_indices) < 2:
        raise ValueError("matching retained fewer than two pairs")

    xm = x[left_indices]
    ym = y[right_indices]
    pooled_sd = np.sqrt((xm.var(axis=0, ddof=1) + ym.var(axis=0, ddof=1)) / 2)
    mean_delta = np.abs(xm.mean(axis=0) - ym.mean(axis=0))
    smd = np.divide(
        mean_delta,
        pooled_sd,
        out=np.zeros_like(mean_delta),
        where=pooled_sd > 0.0,
    )
    ks = np.asarray([_ks_distance(xm[:, k], ym[:, k]) for k in range(x.shape[1])])
    return MatchResult(
        left_indices=left_indices,
        right_indices=right_indices,
        distances=distance[left_indices, right_indices],
        coverage=float(len(left_indices) / len(x)),
        max_standardized_mean_difference=float(smd.max()),
        max_ks_distance=float(ks.max()),
    )


def log_chiral_transfer(
    theta: float,
    source: tuple[float, float] = SOURCE_POINT,
    sink: tuple[float, float] = SINK_POINT,
) -> float:
    """External continuum target for one massless chiral characteristic.

    For g_theta = p_theta eta in two dimensions, conformal covariance gives
    D_g(p_theta**(-1/4) psi_flat) = p_theta**(-3/4) D_eta psi_flat.
    Along a flat chiral characteristic the logarithmic field transfer is thus
    (log p(source) - log p(sink))/4.  Coordinates and theta stay evaluator-only.
    """
    ps = float(conformal_volume_density(*source, theta))
    pt = float(conformal_volume_density(*sink, theta))
    return 0.25 * float(np.log(ps / pt))


def sample_hash(sample: ControlSample) -> str:
    """Canonical RNG/hash-manifest entry for one sealed sample."""
    header = json.dumps(
        {"n": len(sample.coordinates), "seed": sample.seed, "theta": sample.theta},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")
    body = np.asarray(sample.coordinates, dtype="<f8").tobytes(order="C")
    return hashlib.sha256(header + b"\n" + body).hexdigest()


def feature_pool(n: int, theta: float, seeds: range) -> np.ndarray:
    return np.vstack(
        [baseline_features(sprinkle_control(n, theta, seed).order) for seed in seeds]
    )


def kappa_one_feature_pool(
    n: int, theta: float, seeds: range
) -> tuple[np.ndarray, np.ndarray]:
    """Filter by the candidate-independent Stage-5A ``kappa == 1`` domain.

    The retained seed list is returned so the attrition and exact truncation
    used by the domain audit remain reproducible.  Importing ``kappa`` lazily
    keeps the ordinary C8.4 benchmark independent of the expensive realizer
    enumeration.
    """
    from analysis.stage5a_kappa import kappa

    features: list[np.ndarray] = []
    retained_seeds: list[int] = []
    for seed in seeds:
        sample = sprinkle_control(n, theta, seed)
        if kappa(sample.order) == 1:
            features.append(baseline_features(sample.order))
            retained_seeds.append(seed)
    if not features:
        raise ValueError("kappa=1 filter retained no samples")
    return np.vstack(features), np.asarray(retained_seeds, dtype=np.int64)


def _normalize_seed_bases(
    seed_bases: dict[str, int] | tuple[int, int, int, int] | None,
) -> dict[str, int]:
    if seed_bases is None:
        return dict(SOURCE_OF_RECORD_BASES)
    if isinstance(seed_bases, tuple):
        if len(seed_bases) != 4:
            raise ValueError("seed-base tuple must have four entries")
        return dict(zip(SOURCE_OF_RECORD_BASES, map(int, seed_bases)))
    if set(seed_bases) != set(SOURCE_OF_RECORD_BASES):
        raise ValueError("seed-base mapping has the wrong split keys")
    return {key: int(value) for key, value in seed_bases.items()}


def benchmark(
    n: int = 96,
    pool_size: int = SOURCE_OF_RECORD_POOL_SIZE,
    seed_bases: dict[str, int] | tuple[int, int, int, int] | None = None,
) -> dict[str, object]:
    """Deterministic feasibility benchmark with disjoint calibration/validation."""
    if pool_size < 64:
        raise ValueError("pool_size must be at least 64")
    bases = _normalize_seed_bases(seed_bases)
    cp = feature_pool(
        n,
        CONTROL_THETA,
        range(bases["calibration_plus"], bases["calibration_plus"] + pool_size),
    )
    cm = feature_pool(
        n,
        -CONTROL_THETA,
        range(bases["calibration_minus"], bases["calibration_minus"] + pool_size),
    )
    vp = feature_pool(
        n,
        CONTROL_THETA,
        range(bases["validation_plus"], bases["validation_plus"] + pool_size),
    )
    vm = feature_pool(
        n,
        -CONTROL_THETA,
        range(bases["validation_minus"], bases["validation_minus"] + pool_size),
    )
    scale = calibration_scale(cp, cm)
    matched = match_controls(vp, vm, scale)

    first_plus = sprinkle_control(n, CONTROL_THETA, bases["validation_plus"])
    first_minus = sprinkle_control(n, -CONTROL_THETA, bases["validation_minus"])
    return {
        "n": n,
        "pool_size_per_target": pool_size,
        "theta": CONTROL_THETA,
        "feature_names": FEATURE_NAMES,
        "matched_pairs": len(matched.left_indices),
        "coverage": matched.coverage,
        "max_smd": matched.max_standardized_mean_difference,
        "max_ks": matched.max_ks_distance,
        "median_distance": float(np.median(matched.distances)),
        "p90_distance": float(np.quantile(matched.distances, 0.9)),
        "log_transfer_plus": log_chiral_transfer(CONTROL_THETA),
        "log_transfer_minus": log_chiral_transfer(-CONTROL_THETA),
        "first_validation_plus_sha256": sample_hash(first_plus),
        "first_validation_minus_sha256": sample_hash(first_minus),
        "seed_bases": bases,
        "chain_counts": {
            "calibration_plus": int(np.sum(cp[:, 0] == 1.0)),
            "calibration_minus": int(np.sum(cm[:, 0] == 1.0)),
            "validation_plus": int(np.sum(vp[:, 0] == 1.0)),
            "validation_minus": int(np.sum(vm[:, 0] == 1.0)),
        },
    }


def replication_benchmarks(
    n: int = 96, pool_size: int = SOURCE_OF_RECORD_POOL_SIZE
) -> tuple[dict[str, object], ...]:
    """Run the four frozen cross-seed feasibility replications."""
    return tuple(
        benchmark(n=n, pool_size=pool_size, seed_bases=bases)
        for bases in REPLICATION_BASES
    )


def kappa_one_benchmark(
    n: int = 96,
    pool_size: int = SOURCE_OF_RECORD_POOL_SIZE,
    seed_bases: dict[str, int] | tuple[int, int, int, int] | None = None,
) -> dict[str, object]:
    """Filter-then-match audit for a candidate domain restricted to kappa=1.

    Equal raw pools need not retain equal counts.  The frozen audit rule keeps
    the first ``min(count_plus, count_minus)`` samples in ascending seed order
    within each split before scaling or matching.  No candidate output or
    target-local continuum metadata participates in that truncation.
    """
    if pool_size < 64:
        raise ValueError("pool_size must be at least 64")
    bases = _normalize_seed_bases(seed_bases)
    cp, cp_seeds = kappa_one_feature_pool(
        n,
        CONTROL_THETA,
        range(bases["calibration_plus"], bases["calibration_plus"] + pool_size),
    )
    cm, cm_seeds = kappa_one_feature_pool(
        n,
        -CONTROL_THETA,
        range(bases["calibration_minus"], bases["calibration_minus"] + pool_size),
    )
    vp, vp_seeds = kappa_one_feature_pool(
        n,
        CONTROL_THETA,
        range(bases["validation_plus"], bases["validation_plus"] + pool_size),
    )
    vm, vm_seeds = kappa_one_feature_pool(
        n,
        -CONTROL_THETA,
        range(bases["validation_minus"], bases["validation_minus"] + pool_size),
    )
    calibration_count = min(len(cp), len(cm))
    validation_count = min(len(vp), len(vm))
    scale = calibration_scale(cp[:calibration_count], cm[:calibration_count])
    matched = match_controls(vp[:validation_count], vm[:validation_count], scale)
    return {
        "n": n,
        "raw_pool_size_per_target": pool_size,
        "retained_counts": {
            "calibration_plus": len(cp_seeds),
            "calibration_minus": len(cm_seeds),
            "validation_plus": len(vp_seeds),
            "validation_minus": len(vm_seeds),
        },
        "calibration_count_per_target_after_truncation": calibration_count,
        "validation_count_per_target_after_truncation": validation_count,
        "matched_pairs": len(matched.left_indices),
        "coverage": matched.coverage,
        "max_smd": matched.max_standardized_mean_difference,
        "max_ks": matched.max_ks_distance,
        "seed_bases": bases,
    }


if __name__ == "__main__":
    print(json.dumps(benchmark(), indent=2, sort_keys=True))
