"""Candidate-independent statistical regions for Stage 5C 6a-E.

This module fixes the E1/E2 simultaneous-region form and the finite-causet
E3 component rules.  It consumes only the already-frozen matched-cohort law;
it never loads an arm ledger, claims a formal 6a-E seed, forms an arm
endpoint, or imports a candidate kernel.

Multiplicity-adjusted local alpha values are supplied by future closure item
8.  The region shape, degrees of freedom, endpoint scaling, scientific
boundaries, and strict boundary semantics are fixed here.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from math import isfinite

import numpy as np
from scipy.stats import t

from analysis.stage5c_hard_controls import CONTROL_THETA
from analysis.stage5c_joint_matched_law import (
    CALIBRATION_MATCHED_COUNT_DOMAIN,
    GENERATOR_SOURCE_ID,
    JOINT_MATCHED_LAW_ID,
    MatchedLawEnsemble,
)
from analysis.stage5c_numerical_certification import (
    CERTIFICATION_ID,
    CertificationResult,
    CertificationStatus,
    EndpointCertificationProvenance,
)
from analysis.stage5c_planted_certification import certify_wrong_support_domain

STATISTICAL_REGION_ID = "stage5c-6a-e-simultaneous-t-rectangle-v0.1"
DF_ONLY_ORACLE_ID = "stage5c-6a-e-df-only-t-reference-oracle-v0.1"
NUMERICAL_PROPAGATION_ID = "stage5c-6a-e-matched-endpoint-error-propagation-v0.1"
_NUMERICAL_WIDTH_PRODUCER_TOKEN = object()

# The first primary component has sharp range [-1, 2], while the second has
# sharp range [0, 1].  Dividing by these widths gives each coordinate one unit
# of full-domain scale without using an observed covariance or direction.
ENDPOINT_RANGE_WIDTHS = np.asarray([3.0, 1.0])
ENDPOINT_RANGE_WIDTHS.setflags(write=False)

# A 1/20 full-range dead zone is a declared candidate-independent evaluator
# convention.  E1 must clear the closed box and E2 must lie strictly inside
# its open interior.  Equality always fails.
JOINT_EFFECT_FLOOR = 1.0 / 20.0
EQUIVALENCE_MARGIN = np.asarray([JOINT_EFFECT_FLOOR, JOINT_EFFECT_FLOOR])
EQUIVALENCE_MARGIN.setflags(write=False)

# Item 2 calibrated the matched-cohort reference law at B=32.  Smaller B is
# not allowed to form a scientific region.  Item 8 may impose a larger power-
# derived floor but may not lower this structural floor.
MIN_INDEPENDENT_COHORTS = 32
# The earlier C8 control already capped each local claim at alpha=0.01.
# Closure item 8 may allocate a smaller value, but may not loosen this cap.
MAX_LOCAL_ALPHA = 0.01

E1_ARM_NAMES = ("T-plus", "T-minus")
E2_PLUS_ARM_NAMES = ("T-plus-null-A", "T-plus-null-B")
E2_MINUS_ARM_NAMES = ("T-minus-null-A", "T-minus-null-B")

# Domain-wide analytic E3 effects from the closed planted source-of-record.
# Chiral and symmetric-diffusion magnitudes are at least 1/5.  Their frozen
# floors reserve half that gap.  The active wrong-support floor similarly
# reserves half its exact complete-domain separation gap.
E3_CHIRAL_EFFECT_FLOOR = 1.0 / 10.0
E3_DIFFUSION_EFFECT_FLOOR = 1.0 / 10.0
E3_WRONG_SUPPORT_EFFECT_FLOOR = (
    certify_wrong_support_domain().separation_gap / 2.0
)


class RegionProtocolError(ValueError):
    """The caller or supplied object violates the item-4/5 region schema."""


class RegionStatus(str, Enum):
    CLEAN = "CLEAN"
    INCONCLUSIVE = "INCONCLUSIVE"


class RegionReason(str, Enum):
    CERTIFIED = "CERTIFIED"
    COHORT_TOO_SMALL = "COHORT-TOO-SMALL"
    PAIR_COUNT_OUTSIDE_CALIBRATION = "PAIR-COUNT-OUTSIDE-CALIBRATION"
    NONFINITE_INPUT = "NONFINITE-INPUT"
    COVARIANCE_INVALID = "COVARIANCE-INVALID"
    DEGENERATE_MARGINAL_VARIANCE = "DEGENERATE-MARGINAL-VARIANCE"


class ScientificVerdict(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_EVALUATED = "NOT-EVALUATED"


class E2Target(str, Enum):
    PLUS = "T-plus"
    MINUS = "T-minus"


class E3Claim(str, Enum):
    CHIRAL_VS_BLIND = "correct-chiral-minus-sector-blind"
    DIFFUSION_VS_BLIND = "symmetric-diffusion-minus-sector-blind"
    CORRECT_VS_WRONG_SUPPORT = "correct-support-minus-wrong-support"
    SECTOR_BLIND_NULL = "sector-blind-null-A-minus-null-B"


@dataclass(frozen=True)
class E2NullPairSpec:
    """Two independent future pools from one frozen target generator."""

    target: E2Target
    theta: float
    arm_names: tuple[str, str]
    generator_source_id: str = GENERATOR_SOURCE_ID
    requires_distinct_pool_identities: bool = True


@dataclass(frozen=True)
class CertifiedEndpointPool:
    """A pool whose identities were bound by the item-3 producer."""

    rows: tuple[CertificationResult, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.rows, tuple) or not self.rows:
            raise RegionProtocolError("rows must be a non-empty tuple of certifications")
        provenances: list[EndpointCertificationProvenance] = []
        for expected_index, row in enumerate(self.rows):
            if not isinstance(row, CertificationResult):
                raise RegionProtocolError("each endpoint row must be a CertificationResult")
            if not row.producer_authenticated:
                raise RegionProtocolError(
                    "each endpoint row must be emitted by the item-3 certifier"
                )
            if row.status is not CertificationStatus.CLEAN or not row.is_clean:
                raise RegionProtocolError("every endpoint certification must be CLEAN")
            if row.certification_id != CERTIFICATION_ID:
                raise RegionProtocolError("endpoint certification identity is not frozen")
            if not isinstance(row.provenance, EndpointCertificationProvenance):
                raise RegionProtocolError(
                    "every endpoint certification requires producer-bound provenance"
                )
            if row.provenance.row_index != expected_index:
                raise RegionProtocolError(
                    "producer-bound row indices must cover the original pool in order"
                )
            provenances.append(row.provenance)
            endpoint = np.asarray(row.endpoint, dtype=float)
            error = np.asarray(row.endpoint_error, dtype=float)
            if (
                endpoint.shape != (2,)
                or error.shape != (2,)
                or not np.all(np.isfinite(endpoint))
                or not np.all(np.isfinite(error))
                or np.any(error < 0.0)
            ):
                raise RegionProtocolError(
                    "CLEAN endpoint rows require finite endpoint/error two-vectors"
                )
        if any(
            provenance.arm_name != provenances[0].arm_name
            or provenance.pool_identity != provenances[0].pool_identity
            for provenance in provenances[1:]
        ):
            raise RegionProtocolError(
                "all endpoint rows must share producer-bound arm and pool identities"
            )

    @property
    def arm_name(self) -> str:
        provenance = self.rows[0].provenance
        assert provenance is not None
        return provenance.arm_name

    @property
    def pool_identity(self) -> str:
        provenance = self.rows[0].provenance
        assert provenance is not None
        return provenance.pool_identity

    @property
    def row_indices(self) -> tuple[int, ...]:
        return tuple(range(len(self.rows)))


@dataclass(frozen=True, init=False)
class ValidatedNumericalHalfWidth:
    """Opaque output of matched item-3 error propagation for one region input."""

    values: np.ndarray
    independent_clusters: int
    total_pairs: int
    arm_names: tuple[str, str]
    certification_id: str
    propagation_id: str
    joint_law_id: str
    _producer_token: object

    def __new__(cls, *args: object, **kwargs: object) -> ValidatedNumericalHalfWidth:
        raise TypeError(
            "ValidatedNumericalHalfWidth is produced only by matched aggregation"
        )

    @classmethod
    def _from_aggregation(
        cls,
        *,
        values: np.ndarray,
        independent_clusters: int,
        total_pairs: int,
        arm_names: tuple[str, str],
        producer_token: object,
    ) -> ValidatedNumericalHalfWidth:
        if producer_token is not _NUMERICAL_WIDTH_PRODUCER_TOKEN:
            raise RegionProtocolError(
                "validated numerical half-widths are aggregation-only"
            )
        instance = object.__new__(cls)
        object.__setattr__(instance, "values", values)
        object.__setattr__(instance, "independent_clusters", independent_clusters)
        object.__setattr__(instance, "total_pairs", total_pairs)
        object.__setattr__(instance, "arm_names", arm_names)
        object.__setattr__(instance, "certification_id", CERTIFICATION_ID)
        object.__setattr__(instance, "propagation_id", NUMERICAL_PROPAGATION_ID)
        object.__setattr__(instance, "joint_law_id", JOINT_MATCHED_LAW_ID)
        object.__setattr__(instance, "_producer_token", producer_token)
        instance._validate()
        return instance

    def _validate(self) -> None:
        values = np.asarray(self.values, dtype=float)
        if (
            values.shape != (2,)
            or not np.all(np.isfinite(values))
            or np.any(values < 0.0)
        ):
            raise RegionProtocolError(
                "validated numerical half-width must be one finite non-negative two-vector"
            )
        if (
            isinstance(self.independent_clusters, (bool, np.bool_))
            or not isinstance(self.independent_clusters, (int, np.integer))
            or self.independent_clusters < 2
        ):
            raise RegionProtocolError("numerical-width cluster count is invalid")
        if (
            isinstance(self.total_pairs, (bool, np.bool_))
            or not isinstance(self.total_pairs, (int, np.integer))
            or self.total_pairs <= 0
        ):
            raise RegionProtocolError("numerical-width pair count is invalid")
        if (
            not isinstance(self.arm_names, tuple)
            or len(self.arm_names) != 2
            or any(not isinstance(name, str) or not name for name in self.arm_names)
        ):
            raise RegionProtocolError("numerical-width arm identities are invalid")
        if self.certification_id != CERTIFICATION_ID:
            raise RegionProtocolError("numerical-width certification identity is not frozen")
        if self.propagation_id != NUMERICAL_PROPAGATION_ID:
            raise RegionProtocolError("numerical-width propagation identity is not frozen")
        if self.joint_law_id != JOINT_MATCHED_LAW_ID:
            raise RegionProtocolError("numerical-width joint-law identity is not frozen")
        frozen = values.copy()
        frozen.setflags(write=False)
        object.__setattr__(self, "values", frozen)
        object.__setattr__(self, "independent_clusters", int(self.independent_clusters))
        object.__setattr__(self, "total_pairs", int(self.total_pairs))

    @property
    def producer_authenticated(self) -> bool:
        return (
            getattr(self, "_producer_token", None)
            is _NUMERICAL_WIDTH_PRODUCER_TOKEN
        )


_E2_NULL_SPECS = {
    E2Target.PLUS: E2NullPairSpec(
        E2Target.PLUS,
        CONTROL_THETA,
        E2_PLUS_ARM_NAMES,
    ),
    E2Target.MINUS: E2NullPairSpec(
        E2Target.MINUS,
        -CONTROL_THETA,
        E2_MINUS_ARM_NAMES,
    ),
}


def e2_null_pair_spec(target: E2Target) -> E2NullPairSpec:
    """Return the no-RNG E2 generator contract for one target.

    Item 9 must later bind each A/B arm to a distinct fresh pool identity and
    seed stream.  This function deliberately does not accept or generate a
    seed and cannot invoke the generator.
    """

    if not isinstance(target, E2Target):
        raise RegionProtocolError("target must be a registered E2Target")
    return _E2_NULL_SPECS[target]


@dataclass(frozen=True)
class StatisticalRegionInput:
    """Typed adapter output from the frozen matched-law ensemble."""

    estimate: np.ndarray
    mean_covariance: np.ndarray
    independent_clusters: int
    total_pairs: int
    cluster_pair_counts: tuple[int, ...]
    arm_names: tuple[str, str]
    joint_law_id: str = JOINT_MATCHED_LAW_ID

    def __post_init__(self) -> None:
        estimate = np.asarray(self.estimate, dtype=float)
        covariance = np.asarray(self.mean_covariance, dtype=float)
        if estimate.shape != (2,):
            raise RegionProtocolError("estimate must have shape (2,)")
        if covariance.shape != (2, 2):
            raise RegionProtocolError("mean_covariance must have shape (2,2)")
        if (
            isinstance(self.independent_clusters, (bool, np.bool_))
            or not isinstance(self.independent_clusters, (int, np.integer))
            or self.independent_clusters < 2
        ):
            raise RegionProtocolError("independent_clusters must be an integer >= 2")
        if (
            isinstance(self.total_pairs, (bool, np.bool_))
            or not isinstance(self.total_pairs, (int, np.integer))
            or self.total_pairs <= 0
        ):
            raise RegionProtocolError("total_pairs must be a positive integer")
        if len(self.cluster_pair_counts) != int(self.independent_clusters):
            raise RegionProtocolError("one pair count is required per independent cohort")
        if any(
            isinstance(value, (bool, np.bool_))
            or not isinstance(value, (int, np.integer))
            or value <= 0
            for value in self.cluster_pair_counts
        ):
            raise RegionProtocolError("cluster pair counts must be positive integers")
        if sum(int(value) for value in self.cluster_pair_counts) != self.total_pairs:
            raise RegionProtocolError("cluster pair counts must sum to total_pairs")
        if (
            not isinstance(self.arm_names, tuple)
            or len(self.arm_names) != 2
            or any(not isinstance(name, str) or not name for name in self.arm_names)
        ):
            raise RegionProtocolError("arm_names must be two non-empty ordered identities")
        if self.joint_law_id != JOINT_MATCHED_LAW_ID:
            raise RegionProtocolError("input does not use the frozen matched-law identity")
        frozen_estimate = estimate.copy()
        frozen_covariance = covariance.copy()
        frozen_estimate.setflags(write=False)
        frozen_covariance.setflags(write=False)
        object.__setattr__(self, "estimate", frozen_estimate)
        object.__setattr__(self, "mean_covariance", frozen_covariance)
        object.__setattr__(self, "independent_clusters", int(self.independent_clusters))
        object.__setattr__(self, "total_pairs", int(self.total_pairs))
        object.__setattr__(
            self,
            "cluster_pair_counts",
            tuple(int(value) for value in self.cluster_pair_counts),
        )

    @classmethod
    def from_ensemble(cls, ensemble: MatchedLawEnsemble) -> StatisticalRegionInput:
        if not isinstance(ensemble, MatchedLawEnsemble):
            raise RegionProtocolError("region input must come from MatchedLawEnsemble")
        if ensemble.law_id != JOINT_MATCHED_LAW_ID:
            raise RegionProtocolError("ensemble does not use the frozen matched-law identity")
        if len(ensemble.laws) != ensemble.independent_clusters:
            raise RegionProtocolError("ensemble cluster count does not match its laws")
        if not ensemble.laws:
            raise RegionProtocolError("ensemble must contain matched laws")
        arm_names = ensemble.laws[0].arm_names
        if any(law.arm_names != arm_names for law in ensemble.laws):
            raise RegionProtocolError("ensemble laws do not share ordered arm identities")
        if any(law.law_id != JOINT_MATCHED_LAW_ID for law in ensemble.laws):
            raise RegionProtocolError("ensemble contains a non-frozen matched law")
        counts = tuple(law.matched_pairs for law in ensemble.laws)
        return cls(
            estimate=ensemble.delta_mean,
            mean_covariance=ensemble.delta_mean_covariance,
            independent_clusters=ensemble.independent_clusters,
            total_pairs=ensemble.total_pairs,
            cluster_pair_counts=counts,
            arm_names=arm_names,
        )


@dataclass(frozen=True)
class SimultaneousRectangle:
    """Bonferroni two-coordinate Student-t rectangle plus numerical error."""

    estimate: np.ndarray
    lower: np.ndarray
    upper: np.ndarray
    normalized_lower: np.ndarray
    normalized_upper: np.ndarray
    standard_error: np.ndarray
    statistical_half_width: np.ndarray
    numerical_half_width: np.ndarray
    local_alpha: float
    critical_value: float
    reference_df: int
    arm_names: tuple[str, str]
    region_id: str = STATISTICAL_REGION_ID

    def __post_init__(self) -> None:
        for name in (
            "estimate",
            "lower",
            "upper",
            "normalized_lower",
            "normalized_upper",
            "standard_error",
            "statistical_half_width",
            "numerical_half_width",
        ):
            value = np.asarray(getattr(self, name), dtype=float)
            if value.shape != (2,) or not np.all(np.isfinite(value)):
                raise RegionProtocolError(f"{name} must be one finite two-vector")
            frozen = value.copy()
            frozen.setflags(write=False)
            object.__setattr__(self, name, frozen)
        if np.any(self.lower > self.upper):
            raise RegionProtocolError("region bounds must be ordered")


@dataclass(frozen=True)
class RegionBuildResult:
    status: RegionStatus
    reason: RegionReason
    region: SimultaneousRectangle | None

    @property
    def clean(self) -> bool:
        return self.status is RegionStatus.CLEAN and self.region is not None


@dataclass(frozen=True)
class ScientificGateReport:
    claim_id: str
    verdict: ScientificVerdict
    reason: str
    region: SimultaneousRectangle | None


@dataclass(frozen=True)
class DfOnlyOracleReport:
    independent_clusters: int
    matched_pairs_per_cluster: int
    local_alpha: float
    dimension: int
    correct_df: int
    falsifier_df: int
    per_coordinate_nominal_coverage: float
    correct_coverage: float
    falsifier_coverage: float
    coverage_gap: float
    falsifier_detected: bool
    oracle_id: str = DF_ONLY_ORACLE_ID


def _local_alpha(value: float) -> float:
    alpha = float(value)
    if not isfinite(alpha) or not 0.0 < alpha <= MAX_LOCAL_ALPHA:
        raise RegionProtocolError(
            f"local_alpha must lie in (0, {MAX_LOCAL_ALPHA}]"
        )
    return alpha


def _numerical_half_width(
    inputs: StatisticalRegionInput, value: ValidatedNumericalHalfWidth
) -> np.ndarray:
    if not isinstance(value, ValidatedNumericalHalfWidth):
        raise RegionProtocolError(
            "numerical_half_width must be a ValidatedNumericalHalfWidth"
        )
    if not value.producer_authenticated:
        raise RegionProtocolError(
            "numerical_half_width must be emitted by matched aggregation"
        )
    if (
        value.independent_clusters != inputs.independent_clusters
        or value.total_pairs != inputs.total_pairs
        or value.arm_names != inputs.arm_names
        or value.joint_law_id != inputs.joint_law_id
    ):
        raise RegionProtocolError("numerical half-width does not match region input")
    return value.values


def _fraction_bound(value: Fraction, direction: float) -> float:
    """Round an exact dyadic/rational value in one directed binary64 sense."""

    try:
        rounded = float(value)
    except OverflowError as exc:
        raise RegionProtocolError("exact interval operation exceeds binary64") from exc
    if not isfinite(rounded):
        raise RegionProtocolError("exact interval operation exceeds binary64")
    rounded_fraction = Fraction.from_float(rounded)
    if (direction < 0.0 and rounded_fraction > value) or (
        direction > 0.0 and rounded_fraction < value
    ):
        with np.errstate(over="ignore", invalid="ignore"):
            rounded = float(np.nextafter(rounded, direction))
        if not isfinite(rounded):
            raise RegionProtocolError("exact interval operation exceeds binary64")
    return rounded


def _fraction_lower(value: Fraction) -> float:
    return _fraction_bound(value, -np.inf)


def _fraction_upper(value: Fraction) -> float:
    return _fraction_bound(value, np.inf)


def _sqrt_upper(value: float) -> float:
    """Return a directed-up binary64 square-root enclosure."""

    nearest = float(np.sqrt(value))
    if not isfinite(nearest):
        raise RegionProtocolError("square-root enclosure exceeds binary64")
    if Fraction.from_float(nearest) ** 2 < Fraction.from_float(float(value)):
        nearest = float(np.nextafter(nearest, np.inf))
    return nearest


def _binary64_array_equal(first: np.ndarray, second: np.ndarray) -> bool:
    """Compare endpoint payloads bit-for-bit, including signed zero."""

    first_array = np.ascontiguousarray(first, dtype=np.float64)
    second_array = np.ascontiguousarray(second, dtype=np.float64)
    return first_array.shape == second_array.shape and bool(
        np.array_equal(first_array.view(np.uint64), second_array.view(np.uint64))
    )


def build_simultaneous_region(
    inputs: StatisticalRegionInput,
    *,
    local_alpha: float,
    numerical_half_width: ValidatedNumericalHalfWidth,
) -> RegionBuildResult:
    """Build the frozen two-coordinate region, or fail before it is formed.

    The CR1 object already estimates covariance of the two-dimensional mean.
    We use only its marginal variances, so singular or ill-conditioned cross-
    covariance never triggers a ridge, pseudo-inverse, or chosen projection.
    Exact zero marginal variance remains fail-closed.
    """

    if not isinstance(inputs, StatisticalRegionInput):
        raise RegionProtocolError("inputs must be StatisticalRegionInput")
    alpha = _local_alpha(local_alpha)
    numerical = _numerical_half_width(inputs, numerical_half_width)
    if inputs.independent_clusters < MIN_INDEPENDENT_COHORTS:
        return RegionBuildResult(
            RegionStatus.INCONCLUSIVE,
            RegionReason.COHORT_TOO_SMALL,
            None,
        )
    if any(
        not CALIBRATION_MATCHED_COUNT_DOMAIN[0]
        <= count
        <= CALIBRATION_MATCHED_COUNT_DOMAIN[1]
        for count in inputs.cluster_pair_counts
    ):
        return RegionBuildResult(
            RegionStatus.INCONCLUSIVE,
            RegionReason.PAIR_COUNT_OUTSIDE_CALIBRATION,
            None,
        )
    estimate = inputs.estimate
    covariance = inputs.mean_covariance
    if not np.all(np.isfinite(estimate)) or not np.all(np.isfinite(covariance)):
        return RegionBuildResult(
            RegionStatus.INCONCLUSIVE,
            RegionReason.NONFINITE_INPUT,
            None,
        )
    # Max-entry scaling and half-before-add symmetrization avoid introducing
    # overflow merely while validating otherwise finite binary64 inputs.
    covariance_scale = max(float(np.max(np.abs(covariance))), np.finfo(float).tiny)
    symmetry_tolerance = 64.0 * np.finfo(float).eps * covariance_scale
    with np.errstate(over="ignore", invalid="ignore"):
        asymmetry = float(np.max(np.abs(covariance - covariance.T)))
    if not isfinite(asymmetry) or asymmetry > symmetry_tolerance:
        return RegionBuildResult(
            RegionStatus.INCONCLUSIVE,
            RegionReason.COVARIANCE_INVALID,
            None,
        )
    symmetric = 0.5 * covariance + 0.5 * covariance.T
    eigen_tolerance = 64.0 * np.finfo(float).eps * covariance_scale
    try:
        eigenvalues = np.linalg.eigvalsh(symmetric)
    except np.linalg.LinAlgError:
        return RegionBuildResult(
            RegionStatus.INCONCLUSIVE,
            RegionReason.COVARIANCE_INVALID,
            None,
        )
    if not np.all(np.isfinite(eigenvalues)) or float(eigenvalues.min()) < -eigen_tolerance:
        return RegionBuildResult(
            RegionStatus.INCONCLUSIVE,
            RegionReason.COVARIANCE_INVALID,
            None,
        )
    marginal_variances = np.diag(symmetric)
    if np.any(marginal_variances <= 0.0):
        return RegionBuildResult(
            RegionStatus.INCONCLUSIVE,
            RegionReason.DEGENERATE_MARGINAL_VARIANCE,
            None,
        )
    reference_df = inputs.independent_clusters - 1
    dimension = 2
    critical = float(t.ppf(1.0 - alpha / (2.0 * dimension), reference_df))
    if not isfinite(critical):
        return RegionBuildResult(
            RegionStatus.INCONCLUSIVE,
            RegionReason.NONFINITE_INPUT,
            None,
        )
    try:
        standard_error = np.asarray(
            [_sqrt_upper(float(value)) for value in marginal_variances]
        )
        statistical = np.asarray(
            [
                _fraction_upper(
                    Fraction.from_float(critical)
                    * Fraction.from_float(float(standard_error[index]))
                )
                for index in range(2)
            ]
        )
        total = np.asarray(
            [
                _fraction_upper(
                    Fraction.from_float(float(statistical[index]))
                    + Fraction.from_float(float(numerical[index]))
                )
                for index in range(2)
            ]
        )
        lower = np.asarray(
            [
                _fraction_lower(
                    Fraction.from_float(float(estimate[index]))
                    - Fraction.from_float(float(total[index]))
                )
                for index in range(2)
            ]
        )
        upper = np.asarray(
            [
                _fraction_upper(
                    Fraction.from_float(float(estimate[index]))
                    + Fraction.from_float(float(total[index]))
                )
                for index in range(2)
            ]
        )
        normalized_lower = np.asarray(
            [
                _fraction_lower(
                    Fraction.from_float(float(lower[index]))
                    / Fraction.from_float(float(ENDPOINT_RANGE_WIDTHS[index]))
                )
                for index in range(2)
            ]
        )
        normalized_upper = np.asarray(
            [
                _fraction_upper(
                    Fraction.from_float(float(upper[index]))
                    / Fraction.from_float(float(ENDPOINT_RANGE_WIDTHS[index]))
                )
                for index in range(2)
            ]
        )
    except RegionProtocolError:
        return RegionBuildResult(
            RegionStatus.INCONCLUSIVE,
            RegionReason.NONFINITE_INPUT,
            None,
        )
    if not all(
        np.all(np.isfinite(value))
        for value in (
            standard_error,
            statistical,
            total,
            lower,
            upper,
            normalized_lower,
            normalized_upper,
        )
    ):
        return RegionBuildResult(
            RegionStatus.INCONCLUSIVE,
            RegionReason.NONFINITE_INPUT,
            None,
        )
    region = SimultaneousRectangle(
        estimate=estimate,
        lower=lower,
        upper=upper,
        normalized_lower=normalized_lower,
        normalized_upper=normalized_upper,
        standard_error=standard_error,
        statistical_half_width=statistical,
        numerical_half_width=numerical,
        local_alpha=alpha,
        critical_value=critical,
        reference_df=reference_df,
        arm_names=inputs.arm_names,
    )
    return RegionBuildResult(RegionStatus.CLEAN, RegionReason.CERTIFIED, region)


def aggregate_matched_numerical_half_width(
    ensemble: MatchedLawEnsemble,
    left_endpoint_pools: tuple[CertifiedEndpointPool, ...],
    right_endpoint_pools: tuple[CertifiedEndpointPool, ...],
) -> ValidatedNumericalHalfWidth:
    """Propagate item-3 endpoint enclosures through the matched mean contrast.

    Each supplied pool contains typed CLEAN item-3 results and binds its arm,
    matching-pool identity, endpoint row, and registered certification ID.
    The frozen matcher indices are applied here; unmatched rows contribute
    nothing.  Exact rational triangle sums and the same total-pair weights as
    item 2 give a directed-upward half-width for the ensemble contrast.
    """

    inputs = StatisticalRegionInput.from_ensemble(ensemble)
    if (
        not isinstance(left_endpoint_pools, tuple)
        or not isinstance(right_endpoint_pools, tuple)
        or len(left_endpoint_pools) != inputs.independent_clusters
        or len(right_endpoint_pools) != inputs.independent_clusters
    ):
        raise RegionProtocolError("one left/right certified endpoint pool is required per cohort")
    matched_error_pairs: list[tuple[np.ndarray, np.ndarray]] = []
    for law, left_pool, right_pool in zip(
        ensemble.laws, left_endpoint_pools, right_endpoint_pools, strict=True
    ):
        if (
            not isinstance(left_pool, CertifiedEndpointPool)
            or not isinstance(right_pool, CertifiedEndpointPool)
        ):
            raise RegionProtocolError(
                "endpoint pools must use the typed CertifiedEndpointPool adapter"
            )
        if left_pool.arm_name != law.arm_names[0] or right_pool.arm_name != law.arm_names[1]:
            raise RegionProtocolError("certified endpoint-pool arm identity mismatch")
        if (
            left_pool.pool_identity != law.matching.pool_identity
            or right_pool.pool_identity != law.matching.pool_identity
        ):
            raise RegionProtocolError("certified endpoint-pool provenance mismatch")
        if law.matching.result is None:
            raise RegionProtocolError("matched law is missing its certified indices")
        left_indices = np.asarray(law.matching.result.left_indices)
        right_indices = np.asarray(law.matching.result.right_indices)
        if (
            left_indices.ndim != 1
            or right_indices.ndim != 1
            or left_indices.dtype.kind not in "iu"
            or right_indices.dtype.kind not in "iu"
            or len(left_indices) != law.matched_pairs
            or len(right_indices) != law.matched_pairs
            or np.any(left_indices < 0)
            or np.any(right_indices < 0)
            or np.any(left_indices >= len(left_pool.rows))
            or np.any(right_indices >= len(right_pool.rows))
        ):
            raise RegionProtocolError("matched indices are malformed or outside error pools")
        selected_left = tuple(left_pool.rows[int(index)] for index in left_indices)
        selected_right = tuple(right_pool.rows[int(index)] for index in right_indices)
        certified_left = np.vstack([row.endpoint for row in selected_left])
        certified_right = np.vstack([row.endpoint for row in selected_right])
        if not _binary64_array_equal(certified_left, law.left) or not _binary64_array_equal(
            certified_right, law.right
        ):
            raise RegionProtocolError("certified endpoint rows do not match the joint law")
        for left_row, right_row in zip(selected_left, selected_right, strict=True):
            matched_error_pairs.append(
                (left_row.endpoint_error, right_row.endpoint_error)
            )
    try:
        radius = _exact_matched_error_radius(
            tuple(matched_error_pairs), total_pairs=inputs.total_pairs
        )
    except RegionProtocolError as exc:
        raise RegionProtocolError("aggregated numerical half-width must be finite") from exc
    return ValidatedNumericalHalfWidth._from_aggregation(
        values=radius,
        independent_clusters=inputs.independent_clusters,
        total_pairs=inputs.total_pairs,
        arm_names=inputs.arm_names,
        producer_token=_NUMERICAL_WIDTH_PRODUCER_TOKEN,
    )


def _exact_matched_error_radius(
    error_pairs: tuple[tuple[np.ndarray, np.ndarray], ...], *, total_pairs: int
) -> np.ndarray:
    """Exact-rational pair addition and averaging after provenance validation."""

    if len(error_pairs) != total_pairs or total_pairs <= 0:
        raise RegionProtocolError("error-pair count must equal total_pairs")
    component_totals = [Fraction(0), Fraction(0)]
    for left_error, right_error in error_pairs:
        left = np.asarray(left_error, dtype=float)
        right = np.asarray(right_error, dtype=float)
        if (
            left.shape != (2,)
            or right.shape != (2,)
            or not np.all(np.isfinite(left))
            or not np.all(np.isfinite(right))
            or np.any(left < 0.0)
            or np.any(right < 0.0)
        ):
            raise RegionProtocolError("matched endpoint errors must be finite two-vectors")
        for component in range(2):
            component_totals[component] += Fraction.from_float(
                float(left[component])
            ) + Fraction.from_float(float(right[component]))
    return np.asarray(
        [
            _fraction_upper(component_totals[component] / total_pairs)
            for component in range(2)
        ],
        dtype=float,
    )


def _not_evaluated(claim_id: str, result: RegionBuildResult) -> ScientificGateReport:
    return ScientificGateReport(
        claim_id,
        ScientificVerdict.NOT_EVALUATED,
        result.reason.value,
        None,
    )


def evaluate_e1(result: RegionBuildResult) -> ScientificGateReport:
    """Require the entire simultaneous region to clear the closed effect box."""

    claim_id = "E1:T-plus-minus-T-minus"
    if not result.clean:
        return _not_evaluated(claim_id, result)
    region = result.region
    assert region is not None
    if region.arm_names != E1_ARM_NAMES:
        raise RegionProtocolError("E1 ordered arm identities do not match the frozen contrast")
    passes = bool(
        np.any(region.normalized_lower > JOINT_EFFECT_FLOOR)
        or np.any(region.normalized_upper < -JOINT_EFFECT_FLOOR)
    )
    return ScientificGateReport(
        claim_id,
        ScientificVerdict.PASS if passes else ScientificVerdict.FAIL,
        "REGION-STRICTLY-OUTSIDE-EFFECT-BOX"
        if passes
        else "JOINT-EFFECT-FLOOR-NOT-CLEARED",
        region,
    )


def evaluate_e2(result: RegionBuildResult, target: E2Target) -> ScientificGateReport:
    """Require the full simultaneous region inside the open null-equivalence box."""

    if not isinstance(target, E2Target):
        raise RegionProtocolError("target must be a registered E2Target")
    claim_id = f"E2:{target.value}-null-equivalence"
    if not result.clean:
        return _not_evaluated(claim_id, result)
    region = result.region
    assert region is not None
    expected_names = (
        E2_PLUS_ARM_NAMES if target is E2Target.PLUS else E2_MINUS_ARM_NAMES
    )
    if region.arm_names != expected_names:
        raise RegionProtocolError("E2 arm identities do not match the registered null target")
    passes = bool(
        np.all(region.normalized_lower > -EQUIVALENCE_MARGIN)
        and np.all(region.normalized_upper < EQUIVALENCE_MARGIN)
    )
    return ScientificGateReport(
        claim_id,
        ScientificVerdict.PASS if passes else ScientificVerdict.FAIL,
        "REGION-STRICTLY-INSIDE-EQUIVALENCE-BOX"
        if passes
        else "EQUIVALENCE-MARGIN-NOT-CLEARED",
        region,
    )


@dataclass(frozen=True)
class _E3Rule:
    arm_names: tuple[str, str]
    directions: tuple[int, int]
    floors: tuple[float, float]


_E3_RULES = {
    E3Claim.CHIRAL_VS_BLIND: _E3Rule(
        ("correct-chiral", "sector-blind"),
        (1, 0),
        (E3_CHIRAL_EFFECT_FLOOR, 0.0),
    ),
    E3Claim.DIFFUSION_VS_BLIND: _E3Rule(
        ("symmetric-diffusion", "sector-blind"),
        (-1, 1),
        (E3_DIFFUSION_EFFECT_FLOOR, E3_DIFFUSION_EFFECT_FLOOR),
    ),
    E3Claim.CORRECT_VS_WRONG_SUPPORT: _E3Rule(
        ("correct-support", "wrong-support"),
        (1, 0),
        (E3_WRONG_SUPPORT_EFFECT_FLOOR, 0.0),
    ),
    E3Claim.SECTOR_BLIND_NULL: _E3Rule(
        ("sector-blind-null-A", "sector-blind-null-B"),
        (0, 0),
        (0.0, 0.0),
    ),
}


def evaluate_e3(result: RegionBuildResult, claim: E3Claim) -> ScientificGateReport:
    """Apply the registered complete-domain E3 component rule."""

    if not isinstance(claim, E3Claim):
        raise RegionProtocolError("claim must be a registered E3Claim")
    claim_id = f"E3:{claim.value}"
    if not result.clean:
        return _not_evaluated(claim_id, result)
    region = result.region
    assert region is not None
    rule = _E3_RULES[claim]
    if region.arm_names != rule.arm_names:
        raise RegionProtocolError("E3 arm identities do not match the registered claim")
    component_passes: list[bool] = []
    for index, direction in enumerate(rule.directions):
        if direction > 0:
            component_passes.append(region.lower[index] > rule.floors[index])
        elif direction < 0:
            component_passes.append(region.upper[index] < -rule.floors[index])
        else:
            component_passes.append(
                region.normalized_lower[index] > -EQUIVALENCE_MARGIN[index]
                and region.normalized_upper[index] < EQUIVALENCE_MARGIN[index]
            )
    passes = all(component_passes)
    return ScientificGateReport(
        claim_id,
        ScientificVerdict.PASS if passes else ScientificVerdict.FAIL,
        "ALL-REGISTERED-COMPONENT-RULES-CLEARED"
        if passes
        else "E3-COMPONENT-RULE-NOT-CLEARED",
        region,
    )


def df_only_reference_oracle() -> DfOnlyOracleReport:
    """Analytically expose a df-only reference-law error.

    The standard error/covariance target is held fixed.  The falsifier changes
    only the Student reference degrees of freedom from B-1 to B*m-1.  Under a
    Gaussian cohort-mean oracle, the true pivot is exactly t_(B-1), so both
    coverages below are distribution-CDF evaluations rather than Monte Carlo
    estimates.
    """

    independent_clusters = 32
    matched_pairs_per_cluster = 192
    local_alpha = MAX_LOCAL_ALPHA
    dimension = 2
    tail = local_alpha / (2.0 * dimension)
    correct_df = independent_clusters - 1
    falsifier_df = independent_clusters * matched_pairs_per_cluster - 1
    correct_critical = float(t.ppf(1.0 - tail, correct_df))
    falsifier_critical = float(t.ppf(1.0 - tail, falsifier_df))
    correct_coverage = float(2.0 * t.cdf(correct_critical, correct_df) - 1.0)
    falsifier_coverage = float(2.0 * t.cdf(falsifier_critical, correct_df) - 1.0)
    nominal = 1.0 - local_alpha / dimension
    gap = correct_coverage - falsifier_coverage
    return DfOnlyOracleReport(
        independent_clusters=independent_clusters,
        matched_pairs_per_cluster=matched_pairs_per_cluster,
        local_alpha=local_alpha,
        dimension=dimension,
        correct_df=correct_df,
        falsifier_df=falsifier_df,
        per_coordinate_nominal_coverage=nominal,
        correct_coverage=correct_coverage,
        falsifier_coverage=falsifier_coverage,
        coverage_gap=gap,
        falsifier_detected=bool(
            abs(correct_coverage - nominal) <= 32.0 * np.finfo(float).eps
            and falsifier_coverage < nominal
            and gap > 0.0
        ),
    )


__all__ = [
    "DF_ONLY_ORACLE_ID",
    "E1_ARM_NAMES",
    "E2_MINUS_ARM_NAMES",
    "E2_PLUS_ARM_NAMES",
    "E3_CHIRAL_EFFECT_FLOOR",
    "E3_DIFFUSION_EFFECT_FLOOR",
    "E3_WRONG_SUPPORT_EFFECT_FLOOR",
    "ENDPOINT_RANGE_WIDTHS",
    "EQUIVALENCE_MARGIN",
    "JOINT_EFFECT_FLOOR",
    "MAX_LOCAL_ALPHA",
    "MIN_INDEPENDENT_COHORTS",
    "NUMERICAL_PROPAGATION_ID",
    "STATISTICAL_REGION_ID",
    "CertifiedEndpointPool",
    "ValidatedNumericalHalfWidth",
    "E2NullPairSpec",
    "E2Target",
    "E3Claim",
    "RegionBuildResult",
    "RegionProtocolError",
    "RegionReason",
    "RegionStatus",
    "ScientificGateReport",
    "ScientificVerdict",
    "SimultaneousRectangle",
    "StatisticalRegionInput",
    "aggregate_matched_numerical_half_width",
    "build_simultaneous_region",
    "df_only_reference_oracle",
    "e2_null_pair_spec",
    "evaluate_e1",
    "evaluate_e2",
    "evaluate_e3",
]
