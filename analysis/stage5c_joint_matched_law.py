"""Candidate-independent joint matched-law contract for Stage 5C 6a-E.

This module freezes the C8 generator/matcher interface and the paired
covariance schema.  It never loads an arm ledger, claims a formal 6a-E seed,
forms a candidate kernel, or chooses an E1/E2 scientific region.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256

import numpy as np
from scipy.stats import binom, f

from analysis.stage5c_hard_controls import (
    COMPONENT_CALIPER,
    EUCLIDEAN_CALIPER,
    FEATURE_NAMES,
    MAX_ABSOLUTE_SMD,
    MAX_KS_DISTANCE,
    MIN_MATCH_COVERAGE,
    MIN_MATCHED_PAIRS,
    MatchResult,
    calibration_scale,
    match_controls,
)


JOINT_MATCHED_LAW_ID = "stage5c-6a-e-joint-matched-law-v0.1"
GENERATOR_SOURCE_ID = "stage5c-hard-controls-sprinkle-control-p-theta-v0.1"
MATCHER_SOURCE_ID = "stage5c-hard-controls-c8.1-matcher-v0.1"
PAIRED_COVARIANCE_ID = "stage5c-paired-delta-covariance-ddof1-v0.1"
CALIBRATION_SUITE_ID = "stage5c-item2-null-calibration-v0.1"
CALIBRATION_STREAM_ID = "development-only-item2-null-calibration-not-6a-e"

# The statistical planted domain is tied to already-frozen structural bounds:
# the lower cohort size is the C8.1 floor and the upper size is twice that
# floor.  The arm correlation domain stays strictly inside the positive-
# definite boundary |rho| < 1; its symmetric stress points are not scientific
# thresholds and do not allocate confirmatory error.
CALIBRATION_MATCHED_COUNT_DOMAIN = (MIN_MATCHED_PAIRS, 2 * MIN_MATCHED_PAIRS)
CALIBRATION_MATCHED_COUNT_SUITE = CALIBRATION_MATCHED_COUNT_DOMAIN
CALIBRATION_ARM_CORRELATION_DOMAIN = (-0.75, 0.75)
CALIBRATION_ARM_CORRELATION_SUITE = (-0.75, 0.0, 0.75)
CALIBRATION_NOMINAL_COVERAGE = 0.95
CALIBRATION_ACCEPTANCE_CONFIDENCE = 0.999
CALIBRATION_COVARIANCE_Z_LIMIT = 6.0
CALIBRATION_REPLICATIONS = 2048
CALIBRATION_INDEPENDENT_CLUSTERS = 32


class JointLawProtocolError(ValueError):
    """The requested object violates the frozen item-2 schema."""


class MatchingStatus(str, Enum):
    CLEAN = "CLEAN"
    INCONCLUSIVE = "INCONCLUSIVE"


class MatchingReason(str, Enum):
    CERTIFIED = "CERTIFIED"
    CALIBRATION_SCALE_INVALID = "CALIBRATION-SCALE-INVALID"
    MATCHER_FAILURE = "MATCHER-FAILURE"
    COHORT_TOO_SMALL = "COHORT-TOO-SMALL"
    COVERAGE_TOO_LOW = "COVERAGE-TOO-LOW"
    SMD_BALANCE_FAILED = "SMD-BALANCE-FAILED"
    KS_BALANCE_FAILED = "KS-BALANCE-FAILED"


@dataclass(frozen=True)
class MatchingCertification:
    """Typed result of the C8.1 certification stage.

    Indices and nuisance diagnostics may be retained for audit, but scientific
    endpoint arrays are neither accepted nor stored by this stage.
    """

    status: MatchingStatus
    reasons: tuple[MatchingReason, ...]
    result: MatchResult | None
    scale: np.ndarray | None
    calibration_identity: str
    pool_identity: str
    unmatched_left_indices: np.ndarray | None = None
    unmatched_right_indices: np.ndarray | None = None
    matcher_source_id: str = MATCHER_SOURCE_ID

    @property
    def clean(self) -> bool:
        return self.status is MatchingStatus.CLEAN


@dataclass(frozen=True)
class PairedCovariance:
    """Complete two-arm block covariance and its paired-delta reduction."""

    joint_covariance: np.ndarray
    left_covariance: np.ndarray
    right_covariance: np.ndarray
    cross_covariance: np.ndarray
    delta_covariance: np.ndarray
    covariance_id: str = PAIRED_COVARIANCE_ID


@dataclass(frozen=True)
class JointMatchedLaw:
    """Empirical joint matched-pair law with uniform one-to-one weights."""

    arm_names: tuple[str, str]
    left: np.ndarray
    right: np.ndarray
    delta: np.ndarray
    weights: np.ndarray
    joint_mean: np.ndarray
    left_mean: np.ndarray
    right_mean: np.ndarray
    delta_mean: np.ndarray
    covariance: PairedCovariance
    matching: MatchingCertification
    law_id: str = JOINT_MATCHED_LAW_ID

    @property
    def matched_pairs(self) -> int:
        return len(self.weights)


@dataclass(frozen=True)
class MatchedLawEnsemble:
    """Independent matched-cohort clusters and robust mean covariance."""

    laws: tuple[JointMatchedLaw, ...]
    delta_mean: np.ndarray
    delta_mean_covariance: np.ndarray
    total_pairs: int
    independent_clusters: int
    law_id: str = JOINT_MATCHED_LAW_ID


@dataclass(frozen=True)
class NullCalibrationReport:
    """Calibration-only diagnostics, separate from E1/E2 region choices."""

    matched_pairs: int
    independent_clusters: int
    arm_correlation: float
    replications: int
    covariance_mode: str
    covariance_max_z: float
    covariance_consistent: bool
    coverage_count: int
    coverage_acceptance_counts: tuple[int, int]
    empirical_coverage: float
    empirical_type_i_error: float
    coverage_calibrated: bool
    stream_identity: str
    suite_id: str = CALIBRATION_SUITE_ID


def _readonly(array: np.ndarray, *, dtype: np.dtype | type = float) -> np.ndarray:
    result = np.asarray(array, dtype=dtype).copy()
    result.setflags(write=False)
    return result


def _feature_pool(name: str, value: np.ndarray) -> np.ndarray:
    result = np.asarray(value, dtype=float)
    if result.ndim != 2 or result.shape[1] != len(FEATURE_NAMES):
        raise JointLawProtocolError(
            f"{name} must have shape (pool_size, {len(FEATURE_NAMES)})"
        )
    if len(result) < 2 or not np.all(np.isfinite(result)):
        raise JointLawProtocolError(f"{name} must be a finite pool with at least two rows")
    return result


def _identity(name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise JointLawProtocolError(f"{name} must be a non-empty typed identity")
    return value


def _readonly_match_result(result: MatchResult) -> MatchResult:
    return MatchResult(
        left_indices=_readonly(result.left_indices, dtype=np.int64),
        right_indices=_readonly(result.right_indices, dtype=np.int64),
        distances=_readonly(result.distances),
        coverage=result.coverage,
        max_standardized_mean_difference=result.max_standardized_mean_difference,
        max_ks_distance=result.max_ks_distance,
    )


def certify_matching(
    calibration_left: np.ndarray,
    calibration_right: np.ndarray,
    pool_left: np.ndarray,
    pool_right: np.ndarray,
    *,
    calibration_identity: str,
    pool_identity: str,
) -> MatchingCertification:
    """Run the frozen C8.1 matching lifecycle without accepting endpoints.

    Calibration pools and evaluation pools are separate arguments.  Their
    stream disjointness is a future item-9 custody obligation; the typed
    identities recorded here give that runner an explicit comparison surface.
    """

    calibration_identity = _identity("calibration_identity", calibration_identity)
    pool_identity = _identity("pool_identity", pool_identity)
    if calibration_identity == pool_identity:
        raise JointLawProtocolError("calibration and evaluation pool identities must differ")
    cal_left = _feature_pool("calibration_left", calibration_left)
    cal_right = _feature_pool("calibration_right", calibration_right)
    left = _feature_pool("pool_left", pool_left)
    right = _feature_pool("pool_right", pool_right)
    if cal_left.shape != cal_right.shape:
        raise JointLawProtocolError("calibration feature pools must have equal shape")
    if left.shape != right.shape:
        raise JointLawProtocolError("evaluation feature pools must have equal shape")

    try:
        scale = calibration_scale(cal_left, cal_right)
    except ValueError:
        return MatchingCertification(
            MatchingStatus.INCONCLUSIVE,
            (MatchingReason.CALIBRATION_SCALE_INVALID,),
            None,
            None,
            calibration_identity,
            pool_identity,
        )
    if not np.all(np.isfinite(scale)):
        return MatchingCertification(
            MatchingStatus.INCONCLUSIVE,
            (MatchingReason.CALIBRATION_SCALE_INVALID,),
            None,
            None,
            calibration_identity,
            pool_identity,
        )
    try:
        result = match_controls(
            left,
            right,
            scale,
            component_caliper=COMPONENT_CALIPER,
            euclidean_caliper=EUCLIDEAN_CALIPER,
        )
    except ValueError:
        return MatchingCertification(
            MatchingStatus.INCONCLUSIVE,
            (MatchingReason.MATCHER_FAILURE,),
            None,
            _readonly(scale),
            calibration_identity,
            pool_identity,
        )

    result = _readonly_match_result(result)
    unmatched_left = _readonly(
        np.setdiff1d(np.arange(len(left)), result.left_indices, assume_unique=True),
        dtype=np.int64,
    )
    unmatched_right = _readonly(
        np.setdiff1d(np.arange(len(right)), result.right_indices, assume_unique=True),
        dtype=np.int64,
    )
    reasons: list[MatchingReason] = []
    if len(result.left_indices) < MIN_MATCHED_PAIRS:
        reasons.append(MatchingReason.COHORT_TOO_SMALL)
    if result.coverage < MIN_MATCH_COVERAGE:
        reasons.append(MatchingReason.COVERAGE_TOO_LOW)
    if result.max_standardized_mean_difference > MAX_ABSOLUTE_SMD:
        reasons.append(MatchingReason.SMD_BALANCE_FAILED)
    if result.max_ks_distance > MAX_KS_DISTANCE:
        reasons.append(MatchingReason.KS_BALANCE_FAILED)
    if reasons:
        return MatchingCertification(
            MatchingStatus.INCONCLUSIVE,
            tuple(reasons),
            result,
            _readonly(scale),
            calibration_identity,
            pool_identity,
            unmatched_left_indices=unmatched_left,
            unmatched_right_indices=unmatched_right,
        )
    return MatchingCertification(
        MatchingStatus.CLEAN,
        (MatchingReason.CERTIFIED,),
        result,
        _readonly(scale),
        calibration_identity,
        pool_identity,
        unmatched_left_indices=unmatched_left,
        unmatched_right_indices=unmatched_right,
    )


def form_joint_matched_law(
    matching: MatchingCertification,
    left_endpoints: np.ndarray,
    right_endpoints: np.ndarray,
    *,
    arm_names: tuple[str, str],
) -> JointMatchedLaw:
    """Form the empirical joint law only after matching is certified CLEAN."""

    # This check deliberately precedes even np.asarray on endpoint inputs.  A
    # runner can therefore pass sentinel/lazy objects and prove that cohort
    # failure short-circuits before scientific values are touched.
    if not matching.clean or matching.result is None:
        raise JointLawProtocolError("endpoint law is NOT-EVALUATED unless matching is CLEAN")
    if (
        not isinstance(arm_names, tuple)
        or len(arm_names) != 2
        or any(not isinstance(name, str) or not name.strip() for name in arm_names)
    ):
        raise JointLawProtocolError("arm_names must be two non-empty ordered identities")
    left = np.asarray(left_endpoints, dtype=float)
    right = np.asarray(right_endpoints, dtype=float)
    if left.ndim != 2 or right.ndim != 2 or left.shape[1:] != (2,) or right.shape[1:] != (2,):
        raise JointLawProtocolError("each endpoint pool must have shape (pool_size, 2)")
    if not np.all(np.isfinite(left)) or not np.all(np.isfinite(right)):
        raise JointLawProtocolError("endpoint pools must be finite")
    indices_left = matching.result.left_indices
    indices_right = matching.result.right_indices
    if len(left) <= int(indices_left.max()) or len(right) <= int(indices_right.max()):
        raise JointLawProtocolError("endpoint pools do not cover the certified match indices")

    paired_left = left[indices_left]
    paired_right = right[indices_right]
    delta = paired_left - paired_right
    count = len(delta)
    joint = np.hstack((paired_left, paired_right))
    joint_covariance = np.cov(joint, rowvar=False, ddof=1)
    left_covariance = joint_covariance[:2, :2]
    right_covariance = joint_covariance[2:, 2:]
    cross_covariance = joint_covariance[:2, 2:]
    delta_covariance = (
        left_covariance
        + right_covariance
        - cross_covariance
        - cross_covariance.T
    )
    direct_delta_covariance = np.cov(delta, rowvar=False, ddof=1)
    identity_residual = float(
        np.linalg.norm(delta_covariance - direct_delta_covariance, ord="fro")
    )
    identity_scale = float(np.linalg.norm(joint_covariance, ord="fro"))
    # The block reduction uses four 2x2 blocks while the oracle directly
    # centers two delta columns.  Bound their different binary64 reduction
    # paths relative to the complete joint second-moment scale, including the
    # exact-zero case without introducing a dimensional absolute tolerance.
    identity_bound = 64.0 * np.finfo(float).eps * identity_scale
    if identity_residual > identity_bound:
        raise AssertionError("joint covariance blocks do not reproduce paired deltas")
    covariance = PairedCovariance(
        _readonly(joint_covariance),
        _readonly(left_covariance),
        _readonly(right_covariance),
        _readonly(cross_covariance),
        _readonly(delta_covariance),
    )
    weights = np.full(count, 1.0 / count)
    return JointMatchedLaw(
        arm_names=arm_names,
        left=_readonly(paired_left),
        right=_readonly(paired_right),
        delta=_readonly(delta),
        weights=_readonly(weights),
        joint_mean=_readonly(joint.mean(axis=0)),
        left_mean=_readonly(paired_left.mean(axis=0)),
        right_mean=_readonly(paired_right.mean(axis=0)),
        delta_mean=_readonly(delta.mean(axis=0)),
        covariance=covariance,
        matching=matching,
    )


def aggregate_joint_matched_laws(
    laws: tuple[JointMatchedLaw, ...],
) -> MatchedLawEnsemble:
    """Estimate mean covariance with independent matched cohorts as clusters.

    Pairs within one Hungarian assignment are not assumed independent.  The
    CR1 cluster sandwich therefore uses complete matched cohorts as sampling
    units and permits their retained pair counts to differ.
    """

    if not isinstance(laws, tuple) or len(laws) < 2:
        raise JointLawProtocolError("at least two independent matched cohorts are required")
    if any(law.law_id != JOINT_MATCHED_LAW_ID for law in laws):
        raise JointLawProtocolError("all cohorts must use the frozen joint-law identity")
    arm_names = laws[0].arm_names
    if any(law.arm_names != arm_names for law in laws):
        raise JointLawProtocolError("all cohorts must use the same ordered arm identities")
    calibration_identities = [law.matching.calibration_identity for law in laws]
    pool_identities = [law.matching.pool_identity for law in laws]
    if len(set(calibration_identities)) != len(laws):
        raise JointLawProtocolError("matched cohorts require independent calibration identities")
    if len(set(pool_identities)) != len(laws):
        raise JointLawProtocolError("matched cohorts require independent evaluation-pool identities")

    total_pairs = sum(law.matched_pairs for law in laws)
    delta_sum = sum((law.delta.sum(axis=0) for law in laws), start=np.zeros(2))
    delta_mean = delta_sum / total_pairs
    cluster_scores = np.vstack(
        [
            (law.delta - delta_mean).sum(axis=0) / total_pairs
            for law in laws
        ]
    )
    cluster_count = len(laws)
    mean_covariance = (
        cluster_count
        / (cluster_count - 1)
        * (cluster_scores.T @ cluster_scores)
    )
    return MatchedLawEnsemble(
        laws=laws,
        delta_mean=_readonly(delta_mean),
        delta_mean_covariance=_readonly(mean_covariance),
        total_pairs=total_pairs,
        independent_clusters=cluster_count,
    )


def planted_joint_covariance(arm_correlation: float) -> np.ndarray:
    """Known 4D Gaussian covariance for candidate-independent calibration."""

    rho = float(arm_correlation)
    if not np.isfinite(rho) or not (
        CALIBRATION_ARM_CORRELATION_DOMAIN[0]
        <= rho
        <= CALIBRATION_ARM_CORRELATION_DOMAIN[1]
    ):
        raise JointLawProtocolError(
            f"arm_correlation must lie in {CALIBRATION_ARM_CORRELATION_DOMAIN}"
        )
    component_covariance = np.asarray([[1.0, 0.25], [0.25, 1.5]])
    covariance = np.block(
        [
            [component_covariance, rho * component_covariance],
            [rho * component_covariance, component_covariance],
        ]
    )
    if np.linalg.eigvalsh(covariance).min() <= 0.0:
        raise AssertionError("registered planted joint covariance is not positive definite")
    return _readonly(covariance)


def _calibration_rng(*, matched_pairs: int, arm_correlation: float) -> tuple[np.random.Generator, str]:
    identity = (
        f"{CALIBRATION_STREAM_ID}|m={matched_pairs}|rho={arm_correlation.hex()}|"
        f"B={CALIBRATION_INDEPENDENT_CLUSTERS}|R={CALIBRATION_REPLICATIONS}"
    )
    digest = sha256(identity.encode("ascii")).digest()
    seed = int.from_bytes(digest[:16], "big")
    return np.random.Generator(np.random.PCG64DXSM(seed)), sha256(identity.encode("ascii")).hexdigest()


def calibrate_paired_covariance(
    matched_pairs: int,
    arm_correlation: float,
    *,
    covariance_mode: str = "paired",
) -> NullCalibrationReport:
    """Check consistency and null coverage on a known joint Gaussian law.

    The Hotelling region is a calibration instrument only.  It does not choose
    or authorize the future E1/E2 region.  ``independent-marginals`` is the
    registered falsifier: it deliberately drops both cross-arm covariance
    blocks and must be rejected by the coverage check when rho is negative.
    """

    if isinstance(matched_pairs, (bool, np.bool_)) or not isinstance(
        matched_pairs, (int, np.integer)
    ):
        raise JointLawProtocolError("matched_pairs must be a non-boolean integer")
    matched_pairs = int(matched_pairs)
    if not (
        CALIBRATION_MATCHED_COUNT_DOMAIN[0]
        <= matched_pairs
        <= CALIBRATION_MATCHED_COUNT_DOMAIN[1]
    ):
        raise JointLawProtocolError(
            f"matched_pairs must lie in {CALIBRATION_MATCHED_COUNT_DOMAIN}"
        )
    if covariance_mode not in {"paired", "independent-marginals"}:
        raise JointLawProtocolError("unknown covariance_mode")
    joint_covariance = planted_joint_covariance(arm_correlation)
    rng, stream_identity = _calibration_rng(
        matched_pairs=matched_pairs, arm_correlation=float(arm_correlation)
    )
    # Each row below is an independent matched-cohort mean.  Its covariance is
    # the known pair-level joint covariance divided by the equal planted
    # within-cluster pair count.  The inferential degrees of freedom are B-1,
    # never B*m-1.
    samples = rng.multivariate_normal(
        np.zeros(4),
        joint_covariance / matched_pairs,
        size=(CALIBRATION_REPLICATIONS, CALIBRATION_INDEPENDENT_CLUSTERS),
        method="cholesky",
    )
    left = samples[:, :, :2]
    right = samples[:, :, 2:]
    delta = left - right
    delta_centered = delta - delta.mean(axis=1, keepdims=True)
    delta_covariances = np.einsum(
        "rmi,rmj->rij", delta_centered, delta_centered
    ) / (CALIBRATION_INDEPENDENT_CLUSTERS - 1)

    true_delta_cluster_covariance = (
        joint_covariance[:2, :2]
        + joint_covariance[2:, 2:]
        - joint_covariance[:2, 2:]
        - joint_covariance[2:, :2]
    ) / matched_pairs
    covariance_standard_error = np.sqrt(
        (
            true_delta_cluster_covariance**2
            + np.outer(
                np.diag(true_delta_cluster_covariance),
                np.diag(true_delta_cluster_covariance),
            )
        )
        / (
            CALIBRATION_REPLICATIONS
            * (CALIBRATION_INDEPENDENT_CLUSTERS - 1)
        )
    )
    covariance_max_z = float(
        np.max(
            np.abs(delta_covariances.mean(axis=0) - true_delta_cluster_covariance)
            / covariance_standard_error
        )
    )

    if covariance_mode == "paired":
        region_covariances = delta_covariances
    else:
        left_centered = left - left.mean(axis=1, keepdims=True)
        right_centered = right - right.mean(axis=1, keepdims=True)
        left_covariances = np.einsum(
            "rmi,rmj->rij", left_centered, left_centered
        ) / (CALIBRATION_INDEPENDENT_CLUSTERS - 1)
        right_covariances = np.einsum(
            "rmi,rmj->rij", right_centered, right_centered
        ) / (CALIBRATION_INDEPENDENT_CLUSTERS - 1)
        region_covariances = left_covariances + right_covariances

    delta_means = delta.mean(axis=1)
    inverse_covariances = np.linalg.inv(region_covariances)
    t_squared = CALIBRATION_INDEPENDENT_CLUSTERS * np.einsum(
        "ri,rij,rj->r", delta_means, inverse_covariances, delta_means
    )
    dimension = 2
    threshold = (
        dimension
        * (CALIBRATION_INDEPENDENT_CLUSTERS - 1)
        / (CALIBRATION_INDEPENDENT_CLUSTERS - dimension)
        * f.ppf(
            CALIBRATION_NOMINAL_COVERAGE,
            dimension,
            CALIBRATION_INDEPENDENT_CLUSTERS - dimension,
        )
    )
    coverage_count = int(np.count_nonzero(t_squared <= threshold))
    lower, upper = binom.interval(
        CALIBRATION_ACCEPTANCE_CONFIDENCE,
        CALIBRATION_REPLICATIONS,
        CALIBRATION_NOMINAL_COVERAGE,
    )
    acceptance_counts = (int(lower), int(upper))
    empirical_coverage = coverage_count / CALIBRATION_REPLICATIONS
    return NullCalibrationReport(
        matched_pairs=matched_pairs,
        independent_clusters=CALIBRATION_INDEPENDENT_CLUSTERS,
        arm_correlation=float(arm_correlation),
        replications=CALIBRATION_REPLICATIONS,
        covariance_mode=covariance_mode,
        covariance_max_z=covariance_max_z,
        covariance_consistent=covariance_max_z <= CALIBRATION_COVARIANCE_Z_LIMIT,
        coverage_count=coverage_count,
        coverage_acceptance_counts=acceptance_counts,
        empirical_coverage=empirical_coverage,
        empirical_type_i_error=1.0 - empirical_coverage,
        coverage_calibrated=acceptance_counts[0] <= coverage_count <= acceptance_counts[1],
        stream_identity=stream_identity,
    )


def planted_matching_inputs(
    retained_pairs: int,
    *,
    pool_size: int = 256,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Build a ground-truth matching/attrition case without arm endpoints."""

    if not 0 <= retained_pairs <= pool_size or pool_size < 2:
        raise JointLawProtocolError("retained_pairs must lie between zero and pool_size")
    grid = np.linspace(-1.0, 1.0, pool_size)
    calibration_left = np.column_stack(
        [np.roll(grid, shift) for shift in range(len(FEATURE_NAMES))]
    )
    calibration_right = calibration_left[::-1].copy()
    scale = calibration_scale(calibration_left, calibration_right)
    pool_left = np.zeros((pool_size, len(FEATURE_NAMES)))
    pool_right = np.zeros_like(pool_left)
    pool_right[retained_pairs:] = 4.0 * scale
    return tuple(
        _readonly(value)
        for value in (calibration_left, calibration_right, pool_left, pool_right)
    )


__all__ = [
    "CALIBRATION_ARM_CORRELATION_DOMAIN",
    "CALIBRATION_ARM_CORRELATION_SUITE",
    "CALIBRATION_INDEPENDENT_CLUSTERS",
    "CALIBRATION_MATCHED_COUNT_DOMAIN",
    "CALIBRATION_MATCHED_COUNT_SUITE",
    "CALIBRATION_REPLICATIONS",
    "CALIBRATION_SUITE_ID",
    "GENERATOR_SOURCE_ID",
    "JOINT_MATCHED_LAW_ID",
    "JointLawProtocolError",
    "JointMatchedLaw",
    "MatchedLawEnsemble",
    "MATCHER_SOURCE_ID",
    "MatchingCertification",
    "MatchingReason",
    "MatchingStatus",
    "NullCalibrationReport",
    "PAIRED_COVARIANCE_ID",
    "PairedCovariance",
    "calibrate_paired_covariance",
    "aggregate_joint_matched_laws",
    "certify_matching",
    "form_joint_matched_law",
    "planted_joint_covariance",
    "planted_matching_inputs",
]
