"""Shared candidate-independent planted suite for 6a-E items 3 and 6.

The constructions in this module are evaluator-side controls.  They never
load arm data, claim a seed, or construct a candidate kernel.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
from math import ceil, exp, fsum, hypot, ldexp, log2

import numpy as np
from numpy.polynomial.legendre import leggauss

from analysis.stage5c_numerical_certification import (
    ErrorBudget,
    ImplementationEstimate,
    rounding_gamma,
)
from analysis.stage5c_primary_invariant import (
    PRIMARY_ENDPOINT_TRACE_ID,
    primary_endpoint,
)


PLANTED_DOMAIN_ID = "stage5c-6a-e-shared-planted-domain-v0.1"
SUPPORT_MAPPING_ID = "sigma-c7-e3-null-support-map-v0.1"
ACCUMULATION_TRACE_ID = "pairing-accumulate-fixed-order-binary64-v0.1"
SWAP_RELABEL_TRACE_ID = "sector-swap-index-permutation-no-reaccumulation-v0.1"

PAIR_COUNT_DOMAIN = (32, 8128)
PAIR_COUNT_SUITE = (32, 512, 8128)
MATRIX_CONDITION_DOMAIN = (1.0, 7.0)
CANCELLATION_DOMAIN = (1.0, 8128.0)
CANCELLATION_SUITE = (1.0, 32.0, 8128.0)

# Candidate-independent binary64 feasibility envelope.  The scale endpoints
# are derived, rather than chosen as naked tolerances: reserve the exponent
# needed by the largest registered matrix coefficient (3), the largest
# cancellation condition, and the endpoint's quadratic operations.
_BINARY64 = np.finfo(np.float64)
_ARITHMETIC_MAGNIFICATION = 3.0 * CANCELLATION_DOMAIN[1]
_EXPONENT_MARGIN = ceil(log2(_ARITHMETIC_MAGNIFICATION))
MATRIX_SCALE_EXPONENT_DOMAIN = (
    ceil((_BINARY64.minexp + _EXPONENT_MARGIN) / 2),
    (_BINARY64.maxexp - 1 - _EXPONENT_MARGIN) // 2,
)
MATRIX_SCALE_DOMAIN = tuple(ldexp(1.0, exponent) for exponent in MATRIX_SCALE_EXPONENT_DOMAIN)
MATRIX_SCALE_SUITE = (MATRIX_SCALE_DOMAIN[0], 1.0, MATRIX_SCALE_DOMAIN[1])

CHIRAL_RATIO_DOMAIN = (2.0, 3.0)
DIFFUSION_DOMAIN = (0.5, 0.75)
WRONG_SUPPORT_LAMBDA_DOMAIN = (2.0, 2.5)


class PlantedProtocolError(ValueError):
    """A requested planted case lies outside the frozen typed domain."""


def _closed_domain(name: str, value: float, domain: tuple[float, float]) -> float:
    value = float(value)
    if not np.isfinite(value) or not domain[0] <= value <= domain[1]:
        raise PlantedProtocolError(f"{name} must lie in the closed domain {domain}")
    return value


def planted_matrix(kind: str, parameter: float, scale: float) -> np.ndarray:
    """Return one matrix in the complete item-6 algebraic planted domains."""

    scale = _closed_domain("scale", scale, MATRIX_SCALE_DOMAIN)
    if kind == "sector_blind":
        if parameter != 1.0:
            raise PlantedProtocolError("sector_blind parameter is fixed to 1")
        matrix = scale * np.eye(2, dtype=np.complex128)
    elif kind == "correct_chiral":
        ratio = _closed_domain("chiral ratio", parameter, CHIRAL_RATIO_DOMAIN)
        matrix = scale * np.diag([1.0, ratio]).astype(np.complex128)
    elif kind == "symmetric_diffusion":
        coupling = _closed_domain("diffusion coupling", parameter, DIFFUSION_DOMAIN)
        matrix = scale * np.asarray(
            [[1.0, coupling], [coupling, 1.0]], dtype=np.complex128
        )
    else:
        raise PlantedProtocolError("unknown planted matrix kind")
    condition = float(np.linalg.cond(matrix, p=2))
    if not MATRIX_CONDITION_DOMAIN[0] <= condition <= MATRIX_CONDITION_DOMAIN[1]:
        raise AssertionError("registered planted matrix escaped its condition domain")
    matrix.setflags(write=False)
    return matrix


def _support_integral(lambda_value: float, *, reversed_support: bool) -> float:
    lambda_value = _closed_domain(
        "wrong-support lambda", lambda_value, WRONG_SUPPORT_LAMBDA_DOMAIN
    )
    if reversed_support:
        return (lambda_value - 1.0 + exp(-lambda_value)) / lambda_value**2
    return (exp(lambda_value) - 1.0 - lambda_value) / lambda_value**2


def analytic_support_pairing(
    lambda_value: float, scale: float, *, reversed_support: bool
) -> np.ndarray:
    """Closed-form correct or actively reversed null-support pairing."""

    scale = _closed_domain("scale", scale, MATRIX_SCALE_DOMAIN)
    matrix = scale * np.diag(
        [_support_integral(lambda_value, reversed_support=reversed_support), 0.5]
    ).astype(np.complex128)
    matrix.setflags(write=False)
    return matrix


def support_density(points: np.ndarray, lambda_value: float, scale: float) -> np.ndarray:
    """Named scalar test density for the Sigma_C7/E3 support mapping."""

    lambda_value = _closed_domain(
        "wrong-support lambda", lambda_value, WRONG_SUPPORT_LAMBDA_DOMAIN
    )
    scale = _closed_domain("scale", scale, MATRIX_SCALE_DOMAIN)
    points = np.asarray(points, dtype=float)
    if points.shape[-1:] != (4,):
        raise PlantedProtocolError("support-density query must end in four coordinates")
    return scale * np.exp(lambda_value * (points[..., 0] - points[..., 2]))


def pair_support_gauss_legendre(
    lambda_value: float,
    scale: float,
    *,
    reversed_support: bool,
    order: int = 32,
) -> np.ndarray:
    """Directly integrate the fixed correct or active wrong-support map.

    Correct support uses ``u_x=a, u_y=a*s`` and its left-sector analogue.
    Active wrong support keeps the frame, density, normalization and output
    legs fixed, changing only to ``u_y=a, u_x=a*s`` (and analogously for v).
    """

    if isinstance(order, bool) or int(order) != order or order < 2:
        raise PlantedProtocolError("quadrature order must be an integer >= 2")
    lambda_value = _closed_domain(
        "wrong-support lambda", lambda_value, WRONG_SUPPORT_LAMBDA_DOMAIN
    )
    scale = _closed_domain("scale", scale, MATRIX_SCALE_DOMAIN)
    nodes, weights = leggauss(int(order))
    nodes = 0.5 * (nodes + 1.0)
    weights = 0.5 * weights
    a, s, transverse = np.meshgrid(nodes, nodes, nodes, indexing="ij")
    wa, ws, wt = np.meshgrid(weights, weights, weights, indexing="ij")
    cube_weight = wa * ws * wt
    if reversed_support:
        right_points = np.stack((a * s, transverse, a, transverse), axis=-1)
        left_points = np.stack((transverse, a * s, transverse, a), axis=-1)
    else:
        right_points = np.stack((a, transverse, a * s, transverse), axis=-1)
        left_points = np.stack((transverse, a, transverse, a * s), axis=-1)
    right = np.sum(cube_weight * a * support_density(right_points, lambda_value, scale))
    left = np.sum(cube_weight * a * support_density(left_points, lambda_value, scale))
    result = np.diag([right, left]).astype(np.complex128)
    result.setflags(write=False)
    return result


@dataclass(frozen=True)
class WrongSupportCertificate:
    gate_o: bool
    gate_e: bool
    correct_first_component_range: tuple[float, float]
    wrong_first_component_range: tuple[float, float]
    separation_gap: float
    support_mapping_id: str = SUPPORT_MAPPING_ID


def certify_wrong_support_domain() -> WrongSupportCertificate:
    """Analytically certify Gate O/E over the complete lambda domain.

    For lambda > 0 the correct right entry is above 1/2 and the reversed
    entry is below 1/2.  Hence their unordered diagonal spectra differ (Gate
    O).  The first primary component is monotone at both domain branches, so
    endpoint ranges are attained at the two registered boundary values.
    """

    lower, upper = WRONG_SUPPORT_LAMBDA_DOMAIN
    correct_right_minimum = _support_integral(lower, reversed_support=False)
    wrong_right_maximum = _support_integral(lower, reversed_support=True)
    gate_o = correct_right_minimum > 0.5 > wrong_right_maximum
    correct = tuple(
        float(primary_endpoint(analytic_support_pairing(value, 1.0, reversed_support=False)).split_minus_coupling)
        for value in (lower, upper)
    )
    wrong = tuple(
        float(primary_endpoint(analytic_support_pairing(value, 1.0, reversed_support=True)).split_minus_coupling)
        for value in (lower, upper)
    )
    correct_range = (min(correct), max(correct))
    wrong_range = (min(wrong), max(wrong))
    gap = correct_range[0] - wrong_range[1]
    return WrongSupportCertificate(
        gate_o=gate_o,
        gate_e=gap > 0.0,
        correct_first_component_range=correct_range,
        wrong_first_component_range=wrong_range,
        separation_gap=gap,
    )


@dataclass(frozen=True)
class AccumulationTrace:
    source_digest: str
    pair_count: int
    cancellation_condition: float
    accumulation_trace_id: str = ACCUMULATION_TRACE_ID


@dataclass(frozen=True)
class PlantedAccumulationCase:
    truth: np.ndarray
    forward: ImplementationEstimate
    reverse: ImplementationEstimate
    trace: AccumulationTrace


def _validate_pair_count(pair_count: int) -> int:
    if isinstance(pair_count, (bool, np.bool_)) or not isinstance(
        pair_count, (int, np.integer)
    ):
        raise PlantedProtocolError("pair_count must be a non-boolean integer")
    pair_count = int(pair_count)
    if not PAIR_COUNT_DOMAIN[0] <= pair_count <= PAIR_COUNT_DOMAIN[1]:
        raise PlantedProtocolError(f"pair_count must lie in {PAIR_COUNT_DOMAIN}")
    return pair_count


def planted_accumulation_case(
    truth: np.ndarray, pair_count: int, cancellation_condition: float
) -> PlantedAccumulationCase:
    """Build two accumulation orders with an independent analytic sum.

    The first two terms have weights ``(1+k)/2`` and ``(1-k)/2``; remaining
    terms are typed zeros.  Their exact sum is the supplied matrix and their
    absolute-weight sum is ``k``.  Thus pair count and cancellation condition
    can be stressed independently across their full shared domain.
    """

    pair_count = _validate_pair_count(pair_count)
    cancellation_condition = _closed_domain(
        "cancellation condition", cancellation_condition, CANCELLATION_DOMAIN
    )
    truth = np.asarray(truth, dtype=np.complex128)
    if truth.shape != (2, 2) or not np.all(np.isfinite(truth)):
        raise PlantedProtocolError("truth must be one finite 2x2 matrix")
    weights = np.zeros(pair_count, dtype=np.float64)
    weights[0] = 0.5 * (1.0 + cancellation_condition)
    weights[1] = 0.5 * (1.0 - cancellation_condition)
    terms = weights[:, None, None] * truth[None, :, :]

    def accumulate(order: range) -> np.ndarray:
        result = np.zeros((2, 2), dtype=np.complex128)
        for index in order:
            result = result + terms[index]
        return result

    forward_matrix = accumulate(range(pair_count))
    reverse_matrix = accumulate(range(pair_count - 1, -1, -1))
    term_norm_sum = fsum(
        hypot(
            *(float(value) for value in np.stack((term.real, term.imag), axis=-1).ravel())
        )
        for term in terms
    )
    # Four complex entries, hence eight real additions per accumulated term.
    additions = 8 * pair_count
    budget = ErrorBudget(
        quadrature=0.0,
        sampling_representation=rounding_gamma(4) * term_norm_sum,
        regulator=0.0,
        boundary_contact=0.0,
        accumulation_term_norm_sum=term_norm_sum,
        real_additions=additions,
    )
    digest_input = np.asarray(truth, dtype="<c16").tobytes() + weights.astype("<f8").tobytes()
    trace = AccumulationTrace(
        source_digest=sha256(digest_input).hexdigest(),
        pair_count=pair_count,
        cancellation_condition=cancellation_condition,
    )
    frozen_truth = truth.copy()
    frozen_truth.setflags(write=False)
    return PlantedAccumulationCase(
        truth=frozen_truth,
        forward=ImplementationEstimate(forward_matrix, budget, "planted-forward"),
        reverse=ImplementationEstimate(reverse_matrix, budget, "planted-reverse"),
        trace=trace,
    )


@dataclass(frozen=True)
class SwapTraceCertificate:
    clean: bool
    reason: "SwapTraceReason"
    source_digest_before: str
    source_digest_after: str
    reaccumulated: bool
    endpoint_bitwise_equal: bool | None
    accumulation_trace_id: str = ACCUMULATION_TRACE_ID
    relabel_trace_id: str = SWAP_RELABEL_TRACE_ID
    endpoint_trace_id: str = PRIMARY_ENDPOINT_TRACE_ID


class SwapTraceReason(str, Enum):
    CERTIFIED = "CERTIFIED"
    SOURCE_TRACE_MISMATCH = "SOURCE-TRACE-MISMATCH"
    REACCUMULATION_FORBIDDEN = "REACCUMULATION-FORBIDDEN"
    ENDPOINT_TRACE_MISMATCH = "ENDPOINT-TRACE-MISMATCH"
    RELABEL_MATRIX_MISMATCH = "RELABEL-MATRIX-MISMATCH"
    BITWISE_ENDPOINT_MISMATCH = "BITWISE-ENDPOINT-MISMATCH"


def evaluate_swap_trace(
    original: np.ndarray,
    swapped: np.ndarray,
    *,
    source_digest_before: str,
    source_digest_after: str,
    reaccumulated: bool,
    endpoint_trace_id: str,
) -> SwapTraceCertificate:
    """Fail closed on every typed exact-relabel trace obligation."""

    original = np.asarray(original, dtype=np.complex128)
    swapped = np.asarray(swapped, dtype=np.complex128)
    if (
        original.shape != (2, 2)
        or swapped.shape != (2, 2)
        or not np.all(np.isfinite(original))
        or not np.all(np.isfinite(swapped))
    ):
        raise PlantedProtocolError("swap trace matrices must be finite 2x2 arrays")
    if not isinstance(source_digest_before, str) or not source_digest_before:
        raise PlantedProtocolError("source_digest_before must be non-empty")
    if not isinstance(source_digest_after, str) or not source_digest_after:
        raise PlantedProtocolError("source_digest_after must be non-empty")
    if not isinstance(reaccumulated, (bool, np.bool_)):
        raise PlantedProtocolError("reaccumulated must be boolean")
    endpoint_bitwise_equal: bool | None = None
    if source_digest_before != source_digest_after:
        reason = SwapTraceReason.SOURCE_TRACE_MISMATCH
    elif reaccumulated:
        reason = SwapTraceReason.REACCUMULATION_FORBIDDEN
    elif endpoint_trace_id != PRIMARY_ENDPOINT_TRACE_ID:
        reason = SwapTraceReason.ENDPOINT_TRACE_MISMATCH
    elif not np.array_equal(swapped, original[::-1, ::-1]):
        reason = SwapTraceReason.RELABEL_MATRIX_MISMATCH
    else:
        original_endpoint = primary_endpoint(original).as_vector()
        swapped_endpoint = primary_endpoint(swapped).as_vector()
        endpoint_bitwise_equal = bool(np.array_equal(original_endpoint, swapped_endpoint))
        reason = (
            SwapTraceReason.CERTIFIED
            if endpoint_bitwise_equal
            else SwapTraceReason.BITWISE_ENDPOINT_MISMATCH
        )
    return SwapTraceCertificate(
        clean=reason is SwapTraceReason.CERTIFIED,
        reason=reason,
        source_digest_before=source_digest_before,
        source_digest_after=source_digest_after,
        reaccumulated=reaccumulated,
        endpoint_bitwise_equal=endpoint_bitwise_equal,
        endpoint_trace_id=endpoint_trace_id,
    )


def certify_exact_swap_trace(case: PlantedAccumulationCase) -> SwapTraceCertificate:
    """Certify sector swap as index relabeling of one accumulated matrix."""

    original = case.forward.matrix
    swapped = original[::-1, ::-1].copy()
    return evaluate_swap_trace(
        original,
        swapped,
        source_digest_before=case.trace.source_digest,
        source_digest_after=case.trace.source_digest,
        reaccumulated=False,
        endpoint_trace_id=PRIMARY_ENDPOINT_TRACE_ID,
    )


__all__ = [
    "ACCUMULATION_TRACE_ID",
    "CANCELLATION_DOMAIN",
    "CANCELLATION_SUITE",
    "CHIRAL_RATIO_DOMAIN",
    "DIFFUSION_DOMAIN",
    "MATRIX_CONDITION_DOMAIN",
    "MATRIX_SCALE_DOMAIN",
    "MATRIX_SCALE_EXPONENT_DOMAIN",
    "MATRIX_SCALE_SUITE",
    "PAIR_COUNT_DOMAIN",
    "PAIR_COUNT_SUITE",
    "PLANTED_DOMAIN_ID",
    "SUPPORT_MAPPING_ID",
    "SWAP_RELABEL_TRACE_ID",
    "WRONG_SUPPORT_LAMBDA_DOMAIN",
    "AccumulationTrace",
    "PlantedAccumulationCase",
    "PlantedProtocolError",
    "SwapTraceCertificate",
    "SwapTraceReason",
    "WrongSupportCertificate",
    "analytic_support_pairing",
    "certify_exact_swap_trace",
    "certify_wrong_support_domain",
    "evaluate_swap_trace",
    "pair_support_gauss_legendre",
    "planted_accumulation_case",
    "planted_matrix",
    "support_density",
]
