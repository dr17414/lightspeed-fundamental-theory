"""Candidate-independent regressions for 6a-E closure items 3 and 6."""

import numpy as np
import pytest

from analysis.stage5c_continuum_pairing import pair_retarded_gauss_legendre
from analysis.stage5c_numerical_certification import (
    CertificationProtocolError,
    CertificationReason,
    CertificationStatus,
    ErrorBudget,
    ImplementationEstimate,
    certify_pairing,
    rounding_gamma,
)
from analysis.stage5c_planted_certification import (
    CANCELLATION_SUITE,
    MATRIX_SCALE_SUITE,
    PAIR_COUNT_SUITE,
    SUPPORT_MAPPING_ID,
    WRONG_SUPPORT_LAMBDA_DOMAIN,
    PlantedProtocolError,
    SwapTraceReason,
    analytic_support_pairing,
    certify_exact_swap_trace,
    certify_wrong_support_domain,
    evaluate_swap_trace,
    pair_support_gauss_legendre,
    planted_accumulation_case,
    planted_matrix,
    support_density,
)
from analysis.stage5c_primary_invariant import (
    PRIMARY_ENDPOINT_TRACE_ID,
    primary_endpoint,
)


def _budget(error: float) -> ErrorBudget:
    return ErrorBudget(
        quadrature=error,
        sampling_representation=0.0,
        regulator=0.0,
        boundary_contact=0.0,
        accumulation_term_norm_sum=0.0,
        real_additions=1,
    )


def _estimate(matrix: np.ndarray, error: float, identity: str) -> ImplementationEstimate:
    return ImplementationEstimate(np.asarray(matrix, dtype=np.complex128), _budget(error), identity)


def test_error_budget_is_scale_aware_and_schema_is_fail_closed():
    budget = ErrorBudget(1.0, 2.0, 3.0, 4.0, 5.0, 17)
    assert budget.rounding >= rounding_gamma(17) * 5.0
    assert budget.total >= 10.0 + budget.rounding
    for bad in (-1.0, np.inf, np.nan):
        with pytest.raises(CertificationProtocolError):
            _budget(bad)
    with pytest.raises(CertificationProtocolError):
        ErrorBudget(0.0, 0.0, 0.0, 0.0, 0.0, True)
    with pytest.raises(CertificationProtocolError):
        ErrorBudget(np.finfo(np.float64).max, np.finfo(np.float64).max, 0.0, 0.0, 0.0, 1)
    with pytest.raises(CertificationProtocolError):
        _estimate(np.eye(3), 0.0, "bad-shape")


def test_nonfinite_exact_zero_and_near_zero_short_circuit_before_endpoint():
    nonfinite = certify_pairing(
        _estimate([[np.nan, 0.0], [0.0, 1.0]], 0.0, "first"),
        _estimate(np.eye(2), 0.0, "second"),
    )
    assert nonfinite.reason is CertificationReason.NONFINITE_BACKEND

    exact_zero = certify_pairing(
        _estimate(np.zeros((2, 2)), 0.0, "first"),
        _estimate(np.zeros((2, 2)), 0.0, "second"),
    )
    assert exact_zero.reason is CertificationReason.EXACT_ZERO

    near_zero = certify_pairing(
        _estimate(np.eye(2), 2.0, "first"),
        _estimate(np.eye(2), 2.0, "second"),
    )
    assert near_zero.reason is CertificationReason.NORM_INTERVAL_TOUCHES_ZERO
    huge = np.finfo(np.float64).max * np.eye(2)
    unbounded = certify_pairing(
        _estimate(huge, 0.0, "first"),
        _estimate(huge, 0.0, "second"),
    )
    assert unbounded.reason is CertificationReason.RATIO_ERROR_UNBOUNDED
    for result in (nonfinite, exact_zero, near_zero, unbounded):
        assert result.status is CertificationStatus.INCONCLUSIVE
        assert result.endpoint is None
        assert result.endpoint_error is None
        assert result.endpoint_lower is None
        assert result.endpoint_upper is None


def test_agreement_uses_error_balls_and_equality_is_closed():
    exact = _estimate(np.diag([4.0, 1.0]), 0.0, "exact-first")
    closed_boundary = certify_pairing(
        exact, _estimate(np.diag([4.0, 1.0]), 0.0, "exact-second")
    )
    assert closed_boundary.reason is CertificationReason.CERTIFIED
    assert closed_boundary.agreement_distance == closed_boundary.agreement_bound == 0.0

    first = _estimate(np.diag([4.0, 0.0]), 1.1, "first")
    second = _estimate(np.diag([6.0, 0.0]), 1.1, "second")
    boundary = certify_pairing(first, second)
    assert boundary.reason is CertificationReason.CERTIFIED
    assert boundary.agreement_distance <= boundary.agreement_bound

    outside = certify_pairing(first, _estimate(np.diag([6.3, 0.0]), 1.1, "second"))
    assert outside.reason is CertificationReason.IMPLEMENTATION_DISAGREEMENT
    assert outside.endpoint is None


def test_planted_truth_blocks_common_mode_bias_that_agreement_cannot_see():
    truth = np.diag([1.0, 2.0])
    biased = truth + 0.25 * np.eye(2)
    result = certify_pairing(
        _estimate(biased, 0.1, "first"),
        _estimate(biased, 0.1, "second"),
        planted_ground_truth=truth,
    )
    assert result.reason is CertificationReason.PLANTED_GROUND_TRUTH_MISMATCH
    assert result.endpoint is None


def test_clean_ratio_region_contains_every_sampled_matrix_in_error_ball():
    center = np.asarray([[2.0, 0.4j], [-0.3, -1.0j]], dtype=np.complex128)
    radius = 0.02
    result = certify_pairing(
        _estimate(center, radius, "first"),
        _estimate(center, radius, "second"),
        planted_ground_truth=center,
    )
    assert result.reason is CertificationReason.CERTIFIED
    rng = np.random.default_rng(941)
    for _ in range(2000):
        direction = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
        direction /= np.linalg.norm(direction, ord="fro")
        perturbed = center + rng.uniform(0.0, radius) * direction
        endpoint = primary_endpoint(perturbed).as_vector()
        assert np.all(endpoint >= result.endpoint_lower)
        assert np.all(endpoint <= result.endpoint_upper)


def test_complete_matrix_domains_share_one_scale_and_condition_envelope():
    families = (
        ("sector_blind", 1.0),
        ("correct_chiral", 2.0),
        ("correct_chiral", 3.0),
        ("symmetric_diffusion", 0.5),
        ("symmetric_diffusion", 0.75),
    )
    for scale in MATRIX_SCALE_SUITE:
        for kind, parameter in families:
            matrix = planted_matrix(kind, parameter, scale)
            assert 1.0 <= np.linalg.cond(matrix) <= 7.0
    with pytest.raises(PlantedProtocolError):
        planted_matrix("correct_chiral", 3.01, 1.0)


def test_shared_near_zero_and_swap_grid_is_certifiable():
    for scale in MATRIX_SCALE_SUITE:
        truth = planted_matrix("symmetric_diffusion", 0.5, scale)
        for pair_count in PAIR_COUNT_SUITE:
            for cancellation in CANCELLATION_SUITE:
                case = planted_accumulation_case(truth, pair_count, cancellation)
                result = certify_pairing(
                    case.forward,
                    case.reverse,
                    planted_ground_truth=case.truth,
                )
                assert result.reason is CertificationReason.CERTIFIED
                trace = certify_exact_swap_trace(case)
                assert trace.clean
                assert trace.reason is SwapTraceReason.CERTIFIED
                assert not trace.reaccumulated


def test_swap_trace_failure_suite_is_typed_and_fail_closed():
    case = planted_accumulation_case(np.diag([1.0, 2.0]), 32, 1.0)
    original = case.forward.matrix
    swapped = original[::-1, ::-1].copy()
    common = dict(
        original=original,
        swapped=swapped,
        source_digest_before=case.trace.source_digest,
        source_digest_after=case.trace.source_digest,
        reaccumulated=False,
        endpoint_trace_id=PRIMARY_ENDPOINT_TRACE_ID,
    )
    variants = (
        ({"source_digest_after": "0" * 64}, SwapTraceReason.SOURCE_TRACE_MISMATCH),
        ({"reaccumulated": True}, SwapTraceReason.REACCUMULATION_FORBIDDEN),
        ({"endpoint_trace_id": "wrong"}, SwapTraceReason.ENDPOINT_TRACE_MISMATCH),
        ({"swapped": swapped + np.eye(2)}, SwapTraceReason.RELABEL_MATRIX_MISMATCH),
    )
    for changes, reason in variants:
        result = evaluate_swap_trace(**(common | changes))
        assert not result.clean
        assert result.reason is reason


def test_support_mapping_has_independent_analytic_and_production_anchors():
    for lambda_value in WRONG_SUPPORT_LAMBDA_DOMAIN:
        for scale in MATRIX_SCALE_SUITE:
            density = lambda points, l=lambda_value, s=scale: support_density(points, l, s)
            production = pair_retarded_gauss_legendre(density, 0.0, order=32).matrix
            correct = pair_support_gauss_legendre(
                lambda_value, scale, reversed_support=False, order=32
            )
            wrong = pair_support_gauss_legendre(
                lambda_value, scale, reversed_support=True, order=32
            )
            analytic_correct = analytic_support_pairing(
                lambda_value, scale, reversed_support=False
            )
            analytic_wrong = analytic_support_pairing(
                lambda_value, scale, reversed_support=True
            )
            scale_atol = 4096.0 * np.finfo(np.float64).eps * scale
            assert np.allclose(production, analytic_correct, rtol=0.0, atol=scale_atol)
            assert np.allclose(correct, analytic_correct, rtol=0.0, atol=scale_atol)
            assert np.allclose(wrong, analytic_wrong, rtol=0.0, atol=scale_atol)


def test_wrong_support_gate_o_and_complete_domain_gate_e_are_separate():
    certificate = certify_wrong_support_domain()
    assert certificate.support_mapping_id == SUPPORT_MAPPING_ID
    assert certificate.gate_o
    assert certificate.gate_e
    assert certificate.separation_gap > 0.0
    assert (
        certificate.wrong_first_component_range[1]
        < certificate.correct_first_component_range[0]
    )


def test_primary_endpoint_swap_is_bitwise_exact_not_merely_close():
    rng = np.random.default_rng(782)
    for _ in range(10000):
        matrix = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
        swapped = matrix[::-1, ::-1]
        assert np.array_equal(
            primary_endpoint(matrix).as_vector(),
            primary_endpoint(swapped).as_vector(),
        )
