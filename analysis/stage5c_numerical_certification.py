"""Candidate-independent Stage 5C 6a-E numerical certification core.

The module certifies a *linear* 2x2 pairing before the nonlinear primary
endpoint is formed.  It does not load an arm ledger, generate a seed, construct
a candidate kernel, or evaluate an arm endpoint.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from fractions import Fraction
from math import fsum, hypot

import numpy as np

from analysis.stage5c_primary_invariant import COMPONENT_BOUNDS, primary_endpoint


CERTIFICATION_ID = "stage5c-6a-e-numerical-certification-v0.2"
FLOAT_DTYPE = np.float64
UNIT_ROUNDOFF = np.finfo(FLOAT_DTYPE).eps / 2.0
RATIO_ERROR_FACTORS = np.asarray([5.0, 2.0], dtype=FLOAT_DTYPE)
RATIO_ERROR_FACTORS.setflags(write=False)
PRIMARY_ENDPOINT_REAL_OPERATIONS = 32
_CERTIFICATION_PRODUCER_TOKEN = object()


class CertificationProtocolError(ValueError):
    """The caller violated the frozen certification schema."""


class CertificationStatus(str, Enum):
    CLEAN = "CLEAN"
    INCONCLUSIVE = "INCONCLUSIVE"


class CertificationReason(str, Enum):
    CERTIFIED = "CERTIFIED"
    NONFINITE_BACKEND = "NONFINITE-BACKEND"
    EXACT_ZERO = "EXACT-ZERO"
    NORM_INTERVAL_TOUCHES_ZERO = "NORM-INTERVAL-TOUCHES-ZERO"
    IMPLEMENTATION_DISAGREEMENT = "IMPLEMENTATION-DISAGREEMENT"
    PLANTED_GROUND_TRUTH_MISMATCH = "PLANTED-GROUND-TRUTH-MISMATCH"
    ERROR_BUDGET_UNBOUNDED = "ERROR-BUDGET-UNBOUNDED"
    RATIO_ERROR_UNBOUNDED = "RATIO-ERROR-UNBOUNDED"


@dataclass(frozen=True)
class EndpointCertificationProvenance:
    """Pool-row identity bound while the item-3 certification is produced."""

    arm_name: str
    pool_identity: str
    row_index: int

    def __post_init__(self) -> None:
        if not isinstance(self.arm_name, str) or not self.arm_name.strip():
            raise CertificationProtocolError("arm_name must be a non-empty identity")
        if not isinstance(self.pool_identity, str) or not self.pool_identity.strip():
            raise CertificationProtocolError("pool_identity must be a non-empty identity")
        if isinstance(self.row_index, (bool, np.bool_)) or not isinstance(
            self.row_index, (int, np.integer)
        ):
            raise CertificationProtocolError("row_index must be a non-boolean integer")
        if int(self.row_index) < 0:
            raise CertificationProtocolError("row_index must be non-negative")
        object.__setattr__(self, "row_index", int(self.row_index))


def _nonnegative_finite(name: str, value: float) -> float:
    value = float(value)
    if not np.isfinite(value) or value < 0.0:
        raise CertificationProtocolError(f"{name} must be finite and non-negative")
    return value


def _positive_integer(name: str, value: int) -> int:
    if isinstance(value, (bool, np.bool_)) or not isinstance(
        value, (int, np.integer)
    ):
        raise CertificationProtocolError(f"{name} must be a non-boolean integer")
    value = int(value)
    if value <= 0:
        raise CertificationProtocolError(f"{name} must be positive")
    return value


def rounding_gamma(real_additions: int) -> float:
    """Return Higham's gamma_n for binary64 real additions."""

    real_additions = _positive_integer("real_additions", real_additions)
    product = real_additions * UNIT_ROUNDOFF
    if product >= 1.0:
        raise CertificationProtocolError("real_additions * unit roundoff must be < 1")
    return float(np.nextafter(product / (1.0 - product), np.inf))


def _frobenius_upper(matrix: np.ndarray) -> float:
    components = np.stack((matrix.real, matrix.imag), axis=-1).ravel()
    value = hypot(*(float(value) for value in components))
    return 0.0 if value == 0.0 else float(np.nextafter(value, np.inf))


def _up(value: float) -> float:
    value = float(value)
    return value if value == 0.0 else float(np.nextafter(value, np.inf))


def _down_nonnegative(value: float) -> float:
    value = float(value)
    return value if value == 0.0 else float(np.nextafter(value, 0.0))


def _fraction_upper(value: Fraction) -> float:
    """Return a binary64 upper bound for one nonnegative exact fraction."""

    if value == 0:
        return 0.0
    rounded = float(value)
    if rounded == 0.0:
        return float(np.nextafter(0.0, np.inf))
    if Fraction.from_float(rounded) < value:
        rounded = float(np.nextafter(rounded, np.inf))
    return rounded


def _certified_midpoint(
    first: np.ndarray, second: np.ndarray
) -> tuple[np.ndarray, float]:
    """Round the exact componentwise midpoint and enclose its absolute error.

    Forming ``0.5 * first + 0.5 * second`` is not covered by a relative
    ``gamma_n`` model when either multiplication enters gradual underflow.
    Each stored binary64 component is therefore lifted to an exact rational,
    averaged exactly, and rounded once.  The Frobenius norm of the eight exact
    rounding residuals is then enclosed upward, including subnormal residuals.
    """

    midpoint = np.empty((2, 2), dtype=np.complex128)
    component_errors: list[float] = []
    for index in np.ndindex(first.shape):
        rounded_components: list[float] = []
        for first_component, second_component in (
            (first[index].real, second[index].real),
            (first[index].imag, second[index].imag),
        ):
            exact = (
                Fraction.from_float(float(first_component))
                + Fraction.from_float(float(second_component))
            ) / 2
            rounded = float(exact)
            residual = abs(exact - Fraction.from_float(rounded))
            rounded_components.append(rounded)
            component_errors.append(_fraction_upper(residual))
        midpoint[index] = complex(*rounded_components)
    center_error = hypot(*component_errors)
    return midpoint, _up(center_error)


@dataclass(frozen=True)
class ErrorBudget:
    """Validated Frobenius error sources for one implementation.

    Every explicit component is already a bound in matrix Frobenius norm.
    ``accumulation_term_norm_sum`` is the sum of the Frobenius norms of the
    terms in their frozen accumulation order; it maps binary64 roundoff to the
    actual matrix scale and cancellation condition.
    """

    quadrature: float
    sampling_representation: float
    regulator: float
    boundary_contact: float
    accumulation_term_norm_sum: float
    real_additions: int

    def __post_init__(self) -> None:
        for name in (
            "quadrature",
            "sampling_representation",
            "regulator",
            "boundary_contact",
            "accumulation_term_norm_sum",
        ):
            object.__setattr__(self, name, _nonnegative_finite(name, getattr(self, name)))
        object.__setattr__(
            self, "real_additions", _positive_integer("real_additions", self.real_additions)
        )
        rounding_gamma(self.real_additions)
        try:
            combined = fsum(
                (
                    self.quadrature,
                    self.sampling_representation,
                    self.regulator,
                    self.boundary_contact,
                    self.rounding,
                )
            )
        except OverflowError as exc:
            raise CertificationProtocolError("combined error budget must be finite") from exc
        if not np.isfinite(combined):
            raise CertificationProtocolError("combined error budget must be finite")

    @property
    def rounding(self) -> float:
        return _up(
            rounding_gamma(self.real_additions) * self.accumulation_term_norm_sum
        )

    @property
    def total(self) -> float:
        value = fsum(
            (
                self.quadrature,
                self.sampling_representation,
                self.regulator,
                self.boundary_contact,
                self.rounding,
            )
        )
        return 0.0 if value == 0.0 else float(np.nextafter(value, np.inf))


@dataclass(frozen=True)
class ImplementationEstimate:
    matrix: np.ndarray
    error: ErrorBudget
    implementation_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.error, ErrorBudget):
            raise CertificationProtocolError("error must be an ErrorBudget")
        matrix = np.asarray(self.matrix, dtype=np.complex128)
        if matrix.shape != (2, 2):
            raise CertificationProtocolError("implementation matrix must have shape (2, 2)")
        if not isinstance(self.implementation_id, str) or not self.implementation_id:
            raise CertificationProtocolError("implementation_id must be non-empty")
        matrix = matrix.copy()
        matrix.setflags(write=False)
        object.__setattr__(self, "matrix", matrix)


@dataclass(frozen=True)
class CertificationResult:
    status: CertificationStatus
    reason: CertificationReason
    agreement_distance: float | None
    agreement_bound: float | None
    matrix: np.ndarray | None
    matrix_error: float | None
    norm_lower: float | None
    norm_upper: float | None
    endpoint: np.ndarray | None
    endpoint_error: np.ndarray | None
    endpoint_lower: np.ndarray | None
    endpoint_upper: np.ndarray | None
    provenance: EndpointCertificationProvenance | None = None
    certification_id: str = CERTIFICATION_ID
    _producer_token: object | None = field(
        default=None, init=False, repr=False, compare=False
    )

    def __post_init__(self) -> None:
        if self.provenance is not None and not isinstance(
            self.provenance, EndpointCertificationProvenance
        ):
            raise CertificationProtocolError(
                "provenance must be EndpointCertificationProvenance or None"
            )
        for name in ("matrix", "endpoint", "endpoint_error", "endpoint_lower", "endpoint_upper"):
            value = getattr(self, name)
            if value is not None:
                frozen = np.asarray(value).copy()
                frozen.setflags(write=False)
                object.__setattr__(self, name, frozen)

    @property
    def is_clean(self) -> bool:
        return self.status is CertificationStatus.CLEAN

    @property
    def producer_authenticated(self) -> bool:
        """Whether this result was emitted by ``certify_pairing``."""

        return self._producer_token is _CERTIFICATION_PRODUCER_TOKEN


def _producer_result(**kwargs: object) -> CertificationResult:
    """Create one item-3 result and attach the module-private producer seal."""

    result = CertificationResult(**kwargs)
    object.__setattr__(result, "_producer_token", _CERTIFICATION_PRODUCER_TOKEN)
    return result


def _inconclusive(
    reason: CertificationReason,
    *,
    agreement_distance: float | None = None,
    agreement_bound: float | None = None,
    matrix: np.ndarray | None = None,
    matrix_error: float | None = None,
    norm_lower: float | None = None,
    norm_upper: float | None = None,
    provenance: EndpointCertificationProvenance | None = None,
) -> CertificationResult:
    return _producer_result(
        status=CertificationStatus.INCONCLUSIVE,
        reason=reason,
        agreement_distance=agreement_distance,
        agreement_bound=agreement_bound,
        matrix=matrix,
        matrix_error=matrix_error,
        norm_lower=norm_lower,
        norm_upper=norm_upper,
        endpoint=None,
        endpoint_error=None,
        endpoint_lower=None,
        endpoint_upper=None,
        provenance=provenance,
    )


def certify_pairing(
    first: ImplementationEstimate,
    second: ImplementationEstimate,
    *,
    planted_ground_truth: np.ndarray | None = None,
    provenance: EndpointCertificationProvenance | None = None,
) -> CertificationResult:
    """Certify two implementations and only then form the primary endpoint.

    Agreement uses the closed error-ball condition
    ``||M1-M2||_F <= eta1+eta2``.  Certified nonzero uses the strict open
    condition ``||(M1+M2)/2||_F - (eta1+eta2)/2 > 0``.  Equality therefore
    passes agreement but fails the nontriviality gate.

    ``planted_ground_truth`` is permitted only for candidate-independent
    feasibility controls.  It prevents two identically biased implementations
    from turning agreement into a mapping certificate.
    """

    if provenance is not None and not isinstance(
        provenance, EndpointCertificationProvenance
    ):
        raise CertificationProtocolError(
            "provenance must be EndpointCertificationProvenance or None"
        )
    if first.implementation_id == second.implementation_id:
        raise CertificationProtocolError("the two implementation identities must differ")

    matrices = (first.matrix, second.matrix)
    if any(not np.all(np.isfinite(matrix)) for matrix in matrices):
        return _inconclusive(
            CertificationReason.NONFINITE_BACKEND, provenance=provenance
        )

    eta_first = first.error.total
    eta_second = second.error.total
    agreement_distance = _frobenius_upper(first.matrix - second.matrix)
    try:
        eta_sum = fsum((eta_first, eta_second))
    except OverflowError:
        return _inconclusive(
            CertificationReason.ERROR_BUDGET_UNBOUNDED, provenance=provenance
        )
    if not np.isfinite(eta_sum):
        return _inconclusive(
            CertificationReason.ERROR_BUDGET_UNBOUNDED, provenance=provenance
        )
    # A proof of d <= E compares an upper enclosure of d to a lower enclosure
    # of E.  The separately computed upper enclosure is used for propagation.
    agreement_bound = _down_nonnegative(eta_sum)
    eta_sum_upper = _up(eta_sum)
    if not np.isfinite(eta_sum_upper):
        return _inconclusive(
            CertificationReason.ERROR_BUDGET_UNBOUNDED,
            agreement_distance=agreement_distance,
            agreement_bound=agreement_bound,
            provenance=provenance,
        )
    if agreement_distance > agreement_bound:
        return _inconclusive(
            CertificationReason.IMPLEMENTATION_DISAGREEMENT,
            agreement_distance=agreement_distance,
            agreement_bound=agreement_bound,
            provenance=provenance,
        )

    if planted_ground_truth is not None:
        truth = np.asarray(planted_ground_truth, dtype=np.complex128)
        if truth.shape != (2, 2) or not np.all(np.isfinite(truth)):
            raise CertificationProtocolError(
                "planted_ground_truth must be one finite 2x2 matrix"
            )
        if (
            _frobenius_upper(first.matrix - truth) > eta_first
            or _frobenius_upper(second.matrix - truth) > eta_second
        ):
            return _inconclusive(
                CertificationReason.PLANTED_GROUND_TRUTH_MISMATCH,
                agreement_distance=agreement_distance,
                agreement_bound=agreement_bound,
                provenance=provenance,
            )

    matrix, center_rounding = _certified_midpoint(first.matrix, second.matrix)
    matrix_error_value = 0.5 * eta_sum_upper + center_rounding
    matrix_error = (
        0.0
        if matrix_error_value == 0.0
        else float(np.nextafter(matrix_error_value, np.inf))
    )
    norm = hypot(
        *(float(value) for value in np.stack((matrix.real, matrix.imag), axis=-1).ravel())
    )
    if not np.isfinite(norm):
        return _inconclusive(
            CertificationReason.RATIO_ERROR_UNBOUNDED,
            agreement_distance=agreement_distance,
            agreement_bound=agreement_bound,
            matrix=matrix,
            matrix_error=matrix_error,
            provenance=provenance,
        )
    norm_down = _down_nonnegative(norm)
    norm_up = _up(norm)
    norm_lower = float(np.nextafter(norm_down - matrix_error, -np.inf))
    norm_upper = _up(norm_up + matrix_error)

    if np.array_equal(first.matrix, np.zeros((2, 2), dtype=np.complex128)) and np.array_equal(
        second.matrix, np.zeros((2, 2), dtype=np.complex128)
    ) and matrix_error == 0.0:
        return _inconclusive(
            CertificationReason.EXACT_ZERO,
            agreement_distance=agreement_distance,
            agreement_bound=agreement_bound,
            matrix=matrix,
            matrix_error=matrix_error,
            norm_lower=0.0,
            norm_upper=0.0,
            provenance=provenance,
        )

    if norm_lower <= 0.0:
        return _inconclusive(
            CertificationReason.NORM_INTERVAL_TOUCHES_ZERO,
            agreement_distance=agreement_distance,
            agreement_bound=agreement_bound,
            matrix=matrix,
            matrix_error=matrix_error,
            norm_lower=norm_lower,
            norm_upper=norm_upper,
            provenance=provenance,
        )

    if matrix_error == 0.0:
        denominator_perturbation = 0.0
    else:
        try:
            norm_error_sum = fsum((2.0 * norm_up, matrix_error))
        except OverflowError:
            norm_error_sum = np.inf
        with np.errstate(over="ignore", invalid="ignore"):
            denominator_perturbation = _up(matrix_error * _up(norm_error_sum))
    denominator_lower = _down_nonnegative(norm_lower * norm_lower)
    if denominator_lower == 0.0:
        return _inconclusive(
            CertificationReason.RATIO_ERROR_UNBOUNDED,
            agreement_distance=agreement_distance,
            agreement_bound=agreement_bound,
            matrix=matrix,
            matrix_error=matrix_error,
            norm_lower=norm_lower,
            norm_upper=norm_upper,
            provenance=provenance,
        )
    with np.errstate(over="ignore", invalid="ignore"):
        ratio_error = np.asarray(
            [
                _up(factor * denominator_perturbation / denominator_lower)
                for factor in RATIO_ERROR_FACTORS
            ],
            dtype=FLOAT_DTYPE,
        )
    if not np.all(np.isfinite(ratio_error)):
        return _inconclusive(
            CertificationReason.RATIO_ERROR_UNBOUNDED,
            agreement_distance=agreement_distance,
            agreement_bound=agreement_bound,
            matrix=matrix,
            matrix_error=matrix_error,
            norm_lower=norm_lower,
            norm_upper=norm_upper,
            provenance=provenance,
        )
    endpoint_scale = max(abs(value) for value in matrix.ravel())
    endpoint = primary_endpoint(matrix / endpoint_scale).as_vector()
    endpoint_rounding = rounding_gamma(PRIMARY_ENDPOINT_REAL_OPERATIONS) * np.maximum(
        1.0, np.abs(endpoint)
    )
    endpoint_error = np.nextafter(ratio_error + endpoint_rounding, np.inf)
    if not np.all(np.isfinite(endpoint_error)):
        return _inconclusive(
            CertificationReason.RATIO_ERROR_UNBOUNDED,
            agreement_distance=agreement_distance,
            agreement_bound=agreement_bound,
            matrix=matrix,
            matrix_error=matrix_error,
            norm_lower=norm_lower,
            norm_upper=norm_upper,
            provenance=provenance,
        )

    component_lower = np.asarray([bound[0] for bound in COMPONENT_BOUNDS], dtype=float)
    component_upper = np.asarray([bound[1] for bound in COMPONENT_BOUNDS], dtype=float)
    lower = np.maximum(
        component_lower, np.nextafter(endpoint - endpoint_error, -np.inf)
    )
    upper = np.minimum(
        component_upper, np.nextafter(endpoint + endpoint_error, np.inf)
    )
    return _producer_result(
        status=CertificationStatus.CLEAN,
        reason=CertificationReason.CERTIFIED,
        agreement_distance=agreement_distance,
        agreement_bound=agreement_bound,
        matrix=matrix,
        matrix_error=matrix_error,
        norm_lower=norm_lower,
        norm_upper=norm_upper,
        endpoint=endpoint,
        endpoint_error=endpoint_error,
        endpoint_lower=lower,
        endpoint_upper=upper,
        provenance=provenance,
    )


__all__ = [
    "CERTIFICATION_ID",
    "FLOAT_DTYPE",
    "PRIMARY_ENDPOINT_REAL_OPERATIONS",
    "RATIO_ERROR_FACTORS",
    "UNIT_ROUNDOFF",
    "CertificationProtocolError",
    "CertificationReason",
    "CertificationResult",
    "CertificationStatus",
    "EndpointCertificationProvenance",
    "ErrorBudget",
    "ImplementationEstimate",
    "certify_pairing",
    "rounding_gamma",
]
