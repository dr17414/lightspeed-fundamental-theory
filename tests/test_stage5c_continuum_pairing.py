"""Mapping regressions for the candidate-independent 6a-E typed pairing.

No test in this file imports a candidate kernel, an arm ledger, a selector
runner, a 6a-E seed manifest, or the nonlinear primary invariant.
"""
from __future__ import annotations

import numpy as np
import pytest
from numpy.polynomial.legendre import leggauss

from analysis.stage5c_continuum_pairing import (
    BOUNDARY_ID,
    COORDINATE_ORDER,
    PRESCRIPTION_ID,
    SPIN_FRAME_ORDER,
    adjoint_pullback_density,
    conformal_volume_density,
    legendre_mode_2,
    pair_advanced_from_adjoint,
    pair_retarded_adaptive,
    pair_retarded_gauss_legendre,
    transform_global_basis,
)
from analysis.stage5c_hard_controls import (
    conformal_volume_density as hard_control_density,
)
from analysis.stage5c_hard_controls import legendre_mode_2 as hard_control_mode
from analysis.stage5c_measure_prereg import gaussian_mollifier_density


def constant_density(points: np.ndarray) -> np.ndarray:
    return np.ones(np.asarray(points).shape[:-1], dtype=float)


def test_result_records_the_complete_typed_contract():
    result = pair_retarded_gauss_legendre(constant_density, 0.0, order=4)
    assert result.coordinate_order == COORDINATE_ORDER == (
        "u_x",
        "v_x",
        "u_y",
        "v_y",
    )
    assert result.spin_frame_order == SPIN_FRAME_ORDER == ("U/R", "V/L")
    assert result.prescription == PRESCRIPTION_ID
    assert result.boundary == BOUNDARY_ID
    assert not result.matrix.flags.writeable


def test_conformal_family_maps_exactly_to_the_existing_hard_control_source():
    grid = np.linspace(0.0, 1.0, 17)
    u, v = np.meshgrid(grid, grid, indexing="ij")
    assert np.array_equal(legendre_mode_2(grid), hard_control_mode(grid))
    for theta in (-0.4, 0.0, 0.4):
        assert np.array_equal(
            conformal_volume_density(u, v, theta),
            hard_control_density(u, v, theta),
        )


@pytest.mark.parametrize(
    "implementation",
    (pair_retarded_gauss_legendre, pair_retarded_adaptive),
)
def test_flat_constant_density_has_exact_characteristic_volume(implementation):
    result = implementation(constant_density, 0.0)
    assert np.allclose(result.matrix, 0.5 * np.eye(2), atol=2.0e-12, rtol=0.0)


@pytest.mark.parametrize(
    ("coordinate", "expected"),
    (
        (0, np.diag([1.0 / 3.0, 1.0 / 4.0])),
        (1, np.diag([1.0 / 4.0, 1.0 / 3.0])),
    ),
)
def test_flat_polynomial_mapping_has_analytic_value(coordinate, expected):
    def density(points: np.ndarray) -> np.ndarray:
        return np.asarray(points)[..., coordinate]

    fixed = pair_retarded_gauss_legendre(density, 0.0, order=4).matrix
    adaptive = pair_retarded_adaptive(density, 0.0).matrix
    assert np.allclose(fixed, expected, atol=2.0e-12, rtol=0.0)
    assert np.allclose(adaptive, expected, atol=2.0e-12, rtol=0.0)


@pytest.mark.parametrize(
    "implementation,kwargs",
    (
        (pair_retarded_gauss_legendre, {"order": 16}),
        (pair_retarded_adaptive, {}),
    ),
)
def test_curved_pairing_equals_flat_pairing_of_biweighted_density(
    implementation, kwargs
):
    theta = 0.25

    def density(points: np.ndarray) -> np.ndarray:
        points = np.asarray(points)
        return 1.0 + points[..., 0] + 2.0 * points[..., 3]

    def biweighted(points: np.ndarray) -> np.ndarray:
        points = np.asarray(points)
        px = conformal_volume_density(points[..., 0], points[..., 1], theta)
        py = conformal_volume_density(points[..., 2], points[..., 3], theta)
        return density(points) * (px * py) ** -0.25

    curved = implementation(density, theta, **kwargs).matrix
    flat = implementation(biweighted, 0.0, **kwargs).matrix
    assert np.allclose(curved, flat, atol=2.0e-11, rtol=2.0e-11)


def test_acausal_test_density_pairs_to_zero_and_never_queries_outside_box():
    def acausal(points: np.ndarray) -> np.ndarray:
        points = np.asarray(points)
        assert np.all((0.0 <= points) & (points <= 1.0))
        return (
            (points[..., 2] > points[..., 0] + 0.05)
            & (points[..., 3] > points[..., 1] + 0.05)
        ).astype(float)

    fixed = pair_retarded_gauss_legendre(acausal, 0.25, order=16).matrix
    adaptive = pair_retarded_adaptive(acausal, 0.25).matrix
    assert np.array_equal(fixed, np.zeros((2, 2), dtype=np.complex128))
    assert np.array_equal(adaptive, np.zeros((2, 2), dtype=np.complex128))


def test_right_inverse_uses_zero_incoming_boundary_and_removes_zero_modes():
    theta = 0.25
    nodes, weights = leggauss(16)
    unit_nodes = 0.5 * (nodes + 1.0)
    unit_weights = 0.5 * weights

    u_x, v_x = 0.67, 0.38
    u_y = u_x * unit_nodes
    p_right = conformal_volume_density(u_y, v_x, theta)
    dp_du = theta * (12.0 * u_y - 6.0) * legendre_mode_2(v_x)
    psi_right = u_y * (1.0 + v_x)
    derivative_right = (
        0.25 * p_right ** -0.75 * dp_du * psi_right
        + p_right**0.25 * (1.0 + v_x)
    )
    reconstructed_right = (
        conformal_volume_density(u_x, v_x, theta) ** -0.25
        * u_x
        * np.sum(unit_weights * derivative_right)
    )
    assert reconstructed_right == pytest.approx(u_x * (1.0 + v_x), abs=2.0e-14)

    v_y = v_x * unit_nodes
    p_left = conformal_volume_density(u_x, v_y, theta)
    dp_dv = theta * legendre_mode_2(u_x) * (12.0 * v_y - 6.0)
    psi_left = v_y * (1.0 + u_x)
    derivative_left = (
        0.25 * p_left ** -0.75 * dp_dv * psi_left
        + p_left**0.25 * (1.0 + u_x)
    )
    reconstructed_left = (
        conformal_volume_density(u_x, v_x, theta) ** -0.25
        * v_x
        * np.sum(unit_weights * derivative_left)
    )
    assert reconstructed_left == pytest.approx(v_x * (1.0 + u_x), abs=2.0e-14)


def test_advanced_pairing_is_the_frozen_retarded_adjoint():
    def density(points: np.ndarray) -> np.ndarray:
        points = np.asarray(points)
        return (1.0 + points[..., 0] + 3.0 * points[..., 3]) * (1.0 + 0.4j)

    advanced = pair_advanced_from_adjoint(density, 0.25, order=18).matrix
    pulled = adjoint_pullback_density(density)
    expected = np.conjugate(
        pair_retarded_gauss_legendre(pulled, 0.25, order=18).matrix
    ).T
    assert np.allclose(advanced, expected, atol=0.0, rtol=0.0)


def test_global_phase_and_sector_swap_follow_similarity_convention():
    matrix = pair_retarded_gauss_legendre(
        lambda points: 1.0 + np.asarray(points)[..., 0], 0.0, order=4
    ).matrix
    phase = np.diag([np.exp(0.37j), np.exp(-0.19j)])
    swap = np.asarray([[0.0, 1.0], [1.0, 0.0]])
    assert np.allclose(transform_global_basis(matrix, phase), matrix, atol=1.0e-15)
    assert np.allclose(
        transform_global_basis(matrix, swap), matrix[::-1, ::-1], atol=0.0
    )


def test_two_implementations_agree_on_planted_fixed_gaussian_measure():
    atoms = np.asarray(
        [
            [0.18, 0.27, 0.09, 0.11],
            [0.73, 0.66, 0.44, 0.38],
            [0.51, 0.35, 0.22, 0.19],
        ],
        dtype=float,
    )
    weights = np.asarray([0.2, 0.5, 0.3], dtype=float)

    def density(points: np.ndarray) -> np.ndarray:
        points = np.asarray(points)
        return gaussian_mollifier_density(
            points.reshape((-1, 4)), atoms, weights
        ).reshape(points.shape[:-1])

    fixed = pair_retarded_gauss_legendre(density, 0.25, order=28).matrix
    adaptive = pair_retarded_adaptive(
        density, 0.25, epsabs=2.0e-7, epsrel=5.0e-6
    ).matrix
    assert np.allclose(fixed, adaptive, atol=3.0e-6, rtol=3.0e-6)


@pytest.mark.parametrize("theta", (-1.0, 2.0, np.nan, np.inf))
def test_invalid_conformal_domain_fails_closed(theta):
    with pytest.raises(ValueError):
        pair_retarded_gauss_legendre(constant_density, theta)


def test_invalid_algorithm_controls_fail_closed():
    with pytest.raises(ValueError):
        pair_retarded_gauss_legendre(constant_density, 0.0, order=1)
    with pytest.raises(ValueError):
        pair_retarded_adaptive(constant_density, 0.0, epsabs=0.0)
    with pytest.raises(ValueError):
        pair_advanced_from_adjoint(
            constant_density, 0.0, implementation="unregistered"
        )
    with pytest.raises(ValueError):
        pair_retarded_gauss_legendre(lambda _points: 1.0, 0.0, order=4)
    with pytest.raises(ValueError):
        pair_retarded_gauss_legendre(
            lambda points: np.full(np.asarray(points).shape[:-1], np.nan),
            0.0,
            order=4,
        )
