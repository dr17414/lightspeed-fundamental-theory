"""Stage 5C D.1 item 3 - residual-power reference probe.

Executes the frozen pre-registration in docs/STAGE5C_D1_3_REFERENCE_PROBE.md.
No candidate kernel is defined, evaluated, or observed anywhere in this module.

Layer 1 reads sealed coordinates and is evaluator-side only.  Layer 2 receives
relation matrices only.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

import numpy as np

from analysis.stage5c_hard_controls import (
    BlindedCase,
    CONTROL_THETA,
    baseline_features,
    calibration_scale,
    construction_payload,
    match_controls,
    sprinkle_control,
)

PROTOCOL_TAG = "stage5c-d1-3-v1"

N_ELEMENTS = 96
POOL_SIZE = 768
BLOCK_STRIDE = 10_000_000
SEGMENT_STRIDE = 1_000_000
PQ_BASE = 1_100_000_000
NULL_BASE = 1_200_000_000
CALIBRATION_BLOCKS = (0, 1, 2)
WITNESS_BLOCKS = (3, 4, 5)

BANK_INTERVAL_ORDERS = tuple(range(5, 13))
BANK_QUANTILES = tuple(round(0.1 * k, 1) for k in range(1, 10))
BANK_EIGENVALUES = 8

RIDGE_LAMBDA = 1.0
KERNEL_BANDWIDTH = 0.12
PROBE_S = (0.05, 0.05)
PROBE_T = (0.50, 0.05)

RANDOMIZATION_DRAWS = 200_000
EFFECT_FLOOR = 0.30
EQUIVALENCE_MARGIN = 0.15
FAMILY_ALPHA = 0.01

MIN_PAIRS_PER_BLOCK = 192
MIN_COVERAGE = 0.35
MAX_SMD = 0.20
MAX_KS = 0.18
MIN_Q_PAIRS = 576
MIN_N_PAIRS = 900


def claim_stream(claim: str) -> np.random.Generator:
    """Frozen Monte Carlo stream: SHA256(tag|claim)[:8] little-endian."""
    digest = hashlib.sha256(f"{PROTOCOL_TAG}|{claim}".encode()).digest()
    return np.random.Generator(
        np.random.PCG64DXSM(int.from_bytes(digest[:8], "little"))
    )


def segment_seeds(base: int, block: int, segment: int) -> range:
    start = base + BLOCK_STRIDE * block + SEGMENT_STRIDE * segment
    return range(start, start + POOL_SIZE)


def order_feature_bank(case: BlindedCase) -> np.ndarray:
    """43-dim bank behind the frozen ``BlindedCase`` API boundary.

    The extractor receives only an opaque id and a copied relation matrix.  It
    cannot access coordinates, theta, seeds, oracle values, or target labels.
    """
    if set(vars(case)) != {"case_id", "order"}:
        raise ValueError("Layer-2 payload contains forbidden metadata")
    r = np.asarray(case.order, dtype=bool)
    n = r.shape[0]
    denominator = n * (n - 1) / 2
    counts = np.asarray(r, dtype=np.int32) @ np.asarray(r, dtype=np.int32)

    abundance = [
        float(np.sum(r & (counts == m)) / denominator) for m in BANK_INTERVAL_ORDERS
    ]

    past_sizes = r.sum(axis=0) / n
    future_sizes = r.sum(axis=1) / n

    # Repo convention gives minimal elements depth 1; the bank uses minimal = 0.
    predecessor_count = r.sum(axis=0)
    depth = np.ones(n, dtype=np.int32)
    for y in np.argsort(predecessor_count, kind="stable"):
        predecessors = np.flatnonzero(r[:, y])
        if predecessors.size:
            depth[y] = 1 + int(depth[predecessors].max())
    past_depth = depth.astype(float) - 1.0
    height = float(past_depth.max())
    if height <= 0.0:
        raise ValueError("degenerate causet: zero height")
    normalized_depth = past_depth / height

    quantiles = [
        *np.quantile(past_sizes, BANK_QUANTILES, method="linear"),
        *np.quantile(future_sizes, BANK_QUANTILES, method="linear"),
        *np.quantile(normalized_depth, BANK_QUANTILES, method="linear"),
    ]

    symmetric = np.asarray(r, dtype=float)
    symmetric = symmetric + symmetric.T
    eigenvalues = np.linalg.eigvalsh(symmetric)[::-1][:BANK_EIGENVALUES] / n

    return np.asarray([*abundance, *quantiles, *eigenvalues], dtype=float)


def _truncated_area(centre: tuple[float, float]) -> float:
    low = np.maximum(np.asarray(centre) - KERNEL_BANDWIDTH, 0.0)
    high = np.minimum(np.asarray(centre) + KERNEL_BANDWIDTH, 1.0)
    return float((high[0] - low[0]) * (high[1] - low[1]))


def _smoothed_density(points: np.ndarray, centre: tuple[float, float]) -> float:
    low = np.maximum(np.asarray(centre) - KERNEL_BANDWIDTH, 0.0)
    high = np.minimum(np.asarray(centre) + KERNEL_BANDWIDTH, 1.0)
    inside = (
        (points[:, 0] >= low[0])
        & (points[:, 0] <= high[0])
        & (points[:, 1] >= low[1])
        & (points[:, 1] <= high[1])
    )
    n = points.shape[0]
    return (int(inside.sum()) + 0.5) / ((n + 1) * _truncated_area(centre))


def oracle_contrast(points: np.ndarray) -> float:
    """Layer 1 estimator; evaluator-side only.  Deliberately shrunk, not unbiased."""
    return 0.25 * (
        np.log(_smoothed_density(points, PROBE_S))
        - np.log(_smoothed_density(points, PROBE_T))
    )


@dataclass(frozen=True)
class Segment:
    baseline: np.ndarray
    bank: np.ndarray
    oracle: np.ndarray


def build_segment(theta: float, seeds: range, want_bank: bool) -> Segment:
    baseline, bank, oracle = [], [], []
    for seed in seeds:
        sample = sprinkle_control(N_ELEMENTS, theta, seed)
        baseline.append(baseline_features(sample.order))
        if want_bank:
            payload = construction_payload(sample)
            if set(payload) != {"order"}:
                raise ValueError("construction payload contains forbidden metadata")
            # The id is a function of the already-allowed order only; it adds no
            # seed, target, coordinate, or oracle channel.  The extractor above
            # ignores it and consumes only the copied relation matrix.
            case_id = "RP-" + hashlib.sha256(payload["order"].tobytes()).hexdigest()[:24]
            case = BlindedCase(case_id=case_id, order=payload["order"])
            bank.append(order_feature_bank(case))
            oracle.append(oracle_contrast(sample.coordinates))
    return Segment(
        np.asarray(baseline),
        np.asarray(bank) if want_bank else np.empty((0, 0)),
        np.asarray(oracle) if want_bank else np.empty(0),
    )


@dataclass(frozen=True)
class Block:
    scale: np.ndarray
    left: Segment
    right: Segment
    pairs_left: np.ndarray
    pairs_right: np.ndarray
    coverage: float
    max_smd: float
    max_ks: float

    @property
    def pairs(self) -> int:
        return int(self.pairs_left.size)

    def gate_ok(self) -> bool:
        return (
            self.pairs >= MIN_PAIRS_PER_BLOCK
            and self.coverage >= MIN_COVERAGE
            and self.max_smd <= MAX_SMD
            and self.max_ks <= MAX_KS
        )


def build_block(base: int, block: int, null_arm: bool) -> Block:
    left_theta = CONTROL_THETA
    right_theta = CONTROL_THETA if null_arm else -CONTROL_THETA
    scale_left = build_segment(left_theta, segment_seeds(base, block, 0), False)
    scale_right = build_segment(right_theta, segment_seeds(base, block, 1), False)
    left = build_segment(left_theta, segment_seeds(base, block, 2), True)
    right = build_segment(right_theta, segment_seeds(base, block, 3), True)
    scale = calibration_scale(scale_left.baseline, scale_right.baseline)
    matched = match_controls(left.baseline, right.baseline, scale)
    return Block(
        scale,
        left,
        right,
        matched.left_indices,
        matched.right_indices,
        matched.coverage,
        matched.max_standardized_mean_difference,
        matched.max_ks_distance,
    )


def _fit_residualizer(bank: np.ndarray, baseline: np.ndarray) -> np.ndarray:
    design = np.hstack([np.ones((baseline.shape[0], 1)), baseline])
    coefficients, *_ = np.linalg.lstsq(design, bank, rcond=None)
    return coefficients


def _apply_residualizer(
    bank: np.ndarray, baseline: np.ndarray, coefficients: np.ndarray
) -> np.ndarray:
    design = np.hstack([np.ones((baseline.shape[0], 1)), baseline])
    return bank - design @ coefficients


def _fit_ridge(features: np.ndarray, labels: np.ndarray) -> tuple[float, np.ndarray]:
    centred = features - features.mean(axis=0)
    target = labels - labels.mean()
    gram = centred.T @ centred + RIDGE_LAMBDA * np.eye(features.shape[1])
    beta = np.linalg.solve(gram, centred.T @ target)
    intercept = float(labels.mean() - features.mean(axis=0) @ beta)
    return intercept, beta


@dataclass(frozen=True)
class FrozenProbe:
    coefficients: np.ndarray
    centre: np.ndarray
    scale: np.ndarray
    intercept: float
    beta: np.ndarray

    def score(self, bank: np.ndarray, baseline: np.ndarray) -> np.ndarray:
        residual = _apply_residualizer(bank, baseline, self.coefficients)
        standardized = (residual - self.centre) / self.scale
        return self.intercept + standardized @ self.beta


def fit_probe(
    bank: np.ndarray, baseline: np.ndarray, labels: np.ndarray
) -> FrozenProbe:
    coefficients = _fit_residualizer(bank, baseline)
    residual = _apply_residualizer(bank, baseline, coefficients)
    centre = residual.mean(axis=0)
    scale = residual.std(axis=0, ddof=0)
    if np.any(scale == 0.0):
        raise ValueError("zero-SD column in calibration split: verdict INCONCLUSIVE")
    standardized = (residual - centre) / scale
    intercept, beta = _fit_ridge(standardized, labels)
    return FrozenProbe(coefficients, centre, scale, intercept, beta)


def paired_signflip(deltas: np.ndarray, claim: str) -> tuple[float, float, float]:
    """Returns (observed mean, standardized effect, add-one two-sided p)."""
    rng = claim_stream(claim)
    observed = float(deltas.mean())
    effect = observed / float(deltas.std(ddof=1))
    extreme = 0
    for _ in range(RANDOMIZATION_DRAWS):
        signs = rng.integers(0, 2, deltas.size) * 2 - 1
        if abs(float((deltas * signs).mean())) >= abs(observed):
            extreme += 1
    return observed, effect, (extreme + 1) / (RANDOMIZATION_DRAWS + 1)


def unpaired_permutation(
    left: np.ndarray, right: np.ndarray, claim: str
) -> tuple[float, float, float]:
    rng = claim_stream(claim)
    observed = float(left.mean() - right.mean())
    pooled = np.sqrt((left.var(ddof=1) + right.var(ddof=1)) / 2.0)
    effect = observed / float(pooled)
    combined = np.concatenate([left, right])
    cut = left.size
    extreme = 0
    for _ in range(RANDOMIZATION_DRAWS):
        shuffled = rng.permutation(combined)
        if abs(float(shuffled[:cut].mean() - shuffled[cut:].mean())) >= abs(observed):
            extreme += 1
    return observed, effect, (extreme + 1) / (RANDOMIZATION_DRAWS + 1)


def tost_equivalence(deltas: np.ndarray) -> tuple[float, float]:
    """Two one-sided t tests against +-EQUIVALENCE_MARGIN on the standardized mean."""
    from scipy import stats

    n = deltas.size
    effect = float(deltas.mean() / deltas.std(ddof=1))
    standard_error = 1.0 / np.sqrt(n)
    lower = stats.t.sf((effect + EQUIVALENCE_MARGIN) / standard_error, df=n - 1)
    upper = stats.t.cdf((effect - EQUIVALENCE_MARGIN) / standard_error, df=n - 1)
    return effect, float(max(lower, upper))


def holm(pvalues: dict[str, float], alpha: float = FAMILY_ALPHA) -> dict[str, bool]:
    ordered = sorted(pvalues.items(), key=lambda item: item[1])
    total = len(ordered)
    verdict: dict[str, bool] = {}
    still_rejecting = True
    for rank, (name, value) in enumerate(ordered):
        threshold = alpha / (total - rank)
        still_rejecting = still_rejecting and value <= threshold
        verdict[name] = still_rejecting
    return verdict


def adjudicate(results: dict) -> str:
    """Apply every frozen cohort, instrument, direction, and effect gate."""
    if not all(row["gate_ok"] for row in results["blocks"].values()):
        return "INCONCLUSIVE"
    if results["Q"]["n"] < MIN_Q_PAIRS or results["N"]["n"] < MIN_N_PAIRS:
        return "INCONCLUSIVE"

    p_arm = results["P"]
    n_arm = results["N"]
    if not (
        p_arm["holm_significant"]
        and p_arm["observed"] > 0.0
        and p_arm["effect"] >= EFFECT_FLOOR
    ):
        return "INCONCLUSIVE"
    if not (
        n_arm["holm_significant"]
        and abs(n_arm["effect"]) < EQUIVALENCE_MARGIN
    ):
        return "INCONCLUSIVE"

    layer1 = results["layer1"]
    if not (
        layer1["holm_significant"]
        and layer1["observed"] > 0.0
        and layer1["effect"] >= EFFECT_FLOOR
    ):
        return "CONTROL-DEAD"

    q_arm = results["Q"]
    if not (
        q_arm["holm_significant"]
        and q_arm["observed"] > 0.0
        and q_arm["effect"] >= EFFECT_FLOOR
    ):
        return "CONTROL-UNFAIR-RISK"
    return "CONTROL-VIABLE"


def _stack_matched(blocks, tag, block_ids):
    bank, base, oracle, labels = [], [], [], []
    for b in block_ids:
        blk = blocks[(tag, b)]
        for seg, idx, y in (
            (blk.left, blk.pairs_left, +1.0),
            (blk.right, blk.pairs_right, -1.0),
        ):
            bank.append(seg.bank[idx])
            base.append(seg.baseline[idx])
            oracle.append(seg.oracle[idx])
            labels.append(np.full(idx.size, y))
    return (
        np.vstack(bank),
        np.vstack(base),
        np.concatenate(oracle),
        np.concatenate(labels),
    )


def _stack_pools(blocks, tag, block_ids):
    bank, base, labels = [], [], []
    for b in block_ids:
        blk = blocks[(tag, b)]
        for seg, y in ((blk.left, +1.0), (blk.right, -1.0)):
            bank.append(seg.bank)
            base.append(seg.baseline)
            labels.append(np.full(seg.bank.shape[0], y))
    return np.vstack(bank), np.vstack(base), np.concatenate(labels)


def run_protocol() -> dict:
    """Single sealed witness revelation; all four claims computed together."""
    blocks = {}
    for tag, base, null in (("pq", PQ_BASE, False), ("null", NULL_BASE, True)):
        for b in CALIBRATION_BLOCKS + WITNESS_BLOCKS:
            blocks[(tag, b)] = build_block(base, b, null)

    results: dict = {"blocks": {}}
    for (tag, b), blk in blocks.items():
        results["blocks"][f"{tag}{b}"] = dict(
            pairs=blk.pairs,
            coverage=blk.coverage,
            max_smd=blk.max_smd,
            max_ks=blk.max_ks,
            gate_ok=blk.gate_ok(),
        )

    cb, cx, _, cy = _stack_matched(blocks, "pq", CALIBRATION_BLOCKS)
    probe = fit_probe(cb, cx, cy)
    wb, wx, wo, wy = _stack_matched(blocks, "pq", WITNESS_BLOCKS)
    score = probe.score(wb, wx)
    q_deltas = score[wy > 0] - score[wy < 0]
    for name, deltas in (
        ("Q", q_deltas),
        ("layer1", wo[wy > 0] - wo[wy < 0]),
    ):
        observed, effect, p = paired_signflip(deltas, name)
        results[name] = dict(n=int(deltas.size), observed=observed, effect=effect, p=p)

    cb, cx, cy = _stack_pools(blocks, "pq", CALIBRATION_BLOCKS)
    probe = fit_probe(cb, cx, cy)
    wb, wx, wy = _stack_pools(blocks, "pq", WITNESS_BLOCKS)
    score = probe.score(wb, wx)
    observed, effect, p = unpaired_permutation(score[wy > 0], score[wy < 0], "P")
    results["P"] = dict(n=int((wy > 0).sum()), observed=observed, effect=effect, p=p)

    cb, cx, _, cy = _stack_matched(blocks, "null", CALIBRATION_BLOCKS)
    probe = fit_probe(cb, cx, cy)
    wb, wx, _, wy = _stack_matched(blocks, "null", WITNESS_BLOCKS)
    score = probe.score(wb, wx)
    deltas = score[wy > 0] - score[wy < 0]
    effect, p = tost_equivalence(deltas)
    results["N"] = dict(n=int(deltas.size), effect=effect, p=p)

    claims = {k: results[k]["p"] for k in ("Q", "layer1", "P", "N")}
    for name, significant in holm(claims).items():
        results[name]["holm_significant"] = bool(significant)
    results["verdict"] = adjudicate(results)
    return results


def main() -> None:
    results = run_protocol()
    print("block   pairs coverage  maxSMD   maxKS  gate")
    for name, row in results["blocks"].items():
        print(
            "%-7s %5d  %.4f   %.4f  %.4f  %s"
            % (
                name,
                row["pairs"],
                row["coverage"],
                row["max_smd"],
                row["max_ks"],
                "OK" if row["gate_ok"] else "FAIL",
            )
        )
    print("\nclaim     n   effect        p          holm")
    for name in ("layer1", "P", "N", "Q"):
        row = results[name]
        print(
            "%-7s %5d  %+.4f  %.3e  %s"
            % (name, row["n"], row["effect"], row["p"], row["holm_significant"])
        )
    print("\nverdict:", results["verdict"])


if __name__ == "__main__":
    main()
