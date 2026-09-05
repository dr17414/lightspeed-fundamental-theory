"""Typed candidate-independent continuum pairing for Stage 5C 6a-E item 1.

This module implements the retarded massless propagation-representation
distribution fixed in ``docs/STAGE5C_6A_E_TYPED_PAIRING.md``.  It deliberately
does not import a candidate kernel, arm ledger, selector runner, seed manifest,
or the nonlinear primary invariant.

Coordinate order is always ``(u_x, v_x, u_y, v_y)``.  The canonical spin-frame
order is ``(U/R, V/L)``.  The returned matrix is the *linear* distribution-test
measure pairing; it is not a scientific endpoint.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy import integrate


COORDINATE_ORDER = ("u_x", "v_x", "u_y", "v_y")
SPIN_FRAME_ORDER = ("U/R", "V/L")
PRESCRIPTION_ID = "stage5c-6a-e-typed-pairing-v0.1"
BOUNDARY_ID = "diamond-zero-incoming-no-reflection-zero-extension"

TestDensity = Callable[[np.ndarray], np.ndarray | complex | float]


@dataclass(frozen=True)
class PairingResult:
    """Typed output of one linear continuum pairing implementation."""

    matrix: np.ndarray
    theta: float
    implementation: str
    coordinate_order: tuple[str, ...] = field(
        default=COORDINATE_ORDER, init=False
    )
    spin_frame_order: tuple[str, ...] = field(default=SPIN_FRAME_ORDER, init=False)
    prescription: str = field(default=PRESCRIPTION_ID, init=False)
    boundary: str = field(default=BOUNDARY_ID, init=False)

    def __post_init__(self) -> None:
        matrix = np.asarray(self.matrix, dtype=np.complex128)
        if matrix.shape != (2, 2):
            raise ValueError("pairing matrix must have shape (2, 2)")
        if not np.all(np.isfinite(matrix)):
            raise ValueError("pairing matrix must be finite")
        object.__setattr__(self, "theta", _validated_theta(self.theta))
        if not self.implementation:
            raise ValueError("implementation identity must be non-empty")
        matrix = matrix.copy()
        matrix.setflags(write=False)
        object.__setattr__(self, "matrix", matrix)


def legendre_mode_2(z: np.ndarray | float) -> np.ndarray | float:
    """The fixed shifted Legendre mode q(z)."""

    values = np.asarray(z)
    result = 6.0 * values**2 - 6.0 * values + 1.0
    return float(result) if result.ndim == 0 else result


def conformal_volume_density(
    u: np.ndarray | float, v: np.ndarray | float, theta: float
) -> np.ndarray | float:
    """Return p_theta on the unit null square after validating theta."""

    theta = _validated_theta(theta)
    result = 1.0 + theta * legendre_mode_2(u) * legendre_mode_2(v)
    if np.any(np.asarray(result) <= 0.0):
        raise ValueError("p_theta must be positive on the pairing domain")
    return result


def _validated_theta(theta: float) -> float:
    theta = float(theta)
    if not np.isfinite(theta) or not (-1.0 < theta < 2.0):
        raise ValueError("theta must be finite and lie in (-1, 2)")
    return theta


def _density_values(density: TestDensity, points: np.ndarray) -> np.ndarray:
    """Evaluate one vectorized density and enforce its exact scalar-output type."""

    points = np.asarray(points, dtype=float)
    expected = points.shape[:-1]
    if points.shape[-1:] != (4,):
        raise ValueError("test-density query must end in four coordinates")
    values = np.asarray(density(points), dtype=np.complex128)
    if values.shape != expected:
        raise ValueError("test density must return one scalar per query point")
    if not np.all(np.isfinite(values)):
        raise ValueError("test density must be finite on every query point")
    return values


def _conformal_biweight(points: np.ndarray, theta: float) -> np.ndarray:
    points = np.asarray(points, dtype=float)
    px = conformal_volume_density(points[..., 0], points[..., 1], theta)
    py = conformal_volume_density(points[..., 2], points[..., 3], theta)
    return np.asarray(px * py, dtype=float) ** -0.25


def _unit_gauss_legendre(order: int) -> tuple[np.ndarray, np.ndarray]:
    if isinstance(order, bool) or int(order) != order or order < 2:
        raise ValueError("Gauss-Legendre order must be an integer >= 2")
    nodes, weights = leggauss(int(order))
    return 0.5 * (nodes + 1.0), 0.5 * weights


def pair_retarded_gauss_legendre(
    density: TestDensity, theta: float, *, order: int = 24
) -> PairingResult:
    """Pair by independent fixed-order tensor Gauss-Legendre quadrature.

    Each characteristic triangle is mapped to a unit cube.  This function does
    not call the adaptive implementation or share any quadrature accumulator
    with it.
    """

    theta = _validated_theta(theta)
    nodes, weights = _unit_gauss_legendre(order)
    a, s, transverse = np.meshgrid(nodes, nodes, nodes, indexing="ij")
    wa, ws, wt = np.meshgrid(weights, weights, weights, indexing="ij")
    cube_weight = wa * ws * wt

    right_points = np.stack((a, transverse, a * s, transverse), axis=-1)
    right = np.sum(
        cube_weight
        * a
        * _conformal_biweight(right_points, theta)
        * _density_values(density, right_points)
    )

    left_points = np.stack((transverse, a, transverse, a * s), axis=-1)
    left = np.sum(
        cube_weight
        * a
        * _conformal_biweight(left_points, theta)
        * _density_values(density, left_points)
    )

    return PairingResult(
        matrix=np.diag(np.asarray([right, left], dtype=np.complex128)),
        theta=theta,
        implementation="gauss-legendre-characteristic-cube",
    )


def _adaptive_scalar(
    density: TestDensity,
    theta: float,
    sector: str,
    epsabs: float,
    epsrel: float,
) -> complex:
    """Adaptive Genz-Malik cubature with an independently built integrand."""

    if sector not in {"right", "left"}:
        raise ValueError("unknown spin sector")

    def integrand(cube_points: np.ndarray) -> np.ndarray:
        cube_points = np.asarray(cube_points, dtype=float)
        a, s, transverse = cube_points.T
        if sector == "right":
            points = np.stack((a, transverse, a * s, transverse), axis=-1)
        else:
            points = np.stack((transverse, a, transverse, a * s), axis=-1)
        values = (
            a
            * _conformal_biweight(points, theta)
            * _density_values(density, points)
        )
        return np.stack((values.real, values.imag), axis=-1)

    result = integrate.cubature(
        integrand,
        np.zeros(3),
        np.ones(3),
        rule="genz-malik",
        atol=epsabs,
        rtol=epsrel,
        max_subdivisions=4096,
    )
    if result.status != "converged":
        raise RuntimeError(
            f"adaptive cubature did not certify convergence for {sector} sector"
        )
    estimate = np.asarray(result.estimate, dtype=float)
    return complex(estimate[0], estimate[1])


def pair_retarded_adaptive(
    density: TestDensity,
    theta: float,
    *,
    epsabs: float = 1.0e-10,
    epsrel: float = 1.0e-10,
) -> PairingResult:
    """Pair by independent adaptive Genz-Malik characteristic cubature."""

    theta = _validated_theta(theta)
    if not np.isfinite(epsabs) or not np.isfinite(epsrel):
        raise ValueError("adaptive tolerances must be finite")
    if epsabs <= 0.0 or epsrel <= 0.0:
        raise ValueError("adaptive tolerances must be positive")

    right = _adaptive_scalar(density, theta, "right", epsabs, epsrel)
    left = _adaptive_scalar(density, theta, "left", epsabs, epsrel)
    return PairingResult(
        matrix=np.diag(np.asarray([right, left], dtype=np.complex128)),
        theta=theta,
        implementation="adaptive-genz-malik-characteristic-cube",
    )


def adjoint_pullback_density(density: TestDensity) -> TestDensity:
    """Return r^sharp(x,y)=conj(r(y,x)) for the advanced-adjoint identity."""

    def pulled(points: np.ndarray) -> np.ndarray:
        points = np.asarray(points, dtype=float)
        swapped = points[..., [2, 3, 0, 1]]
        return np.conjugate(_density_values(density, swapped))

    return pulled


def pair_advanced_from_adjoint(
    density: TestDensity,
    theta: float,
    *,
    implementation: str = "gauss-legendre",
    order: int = 24,
    epsabs: float = 1.0e-10,
    epsrel: float = 1.0e-10,
) -> PairingResult:
    """Evaluate S_A(x,y)=S_R(y,x)^dagger through the adjoint identity."""

    pulled = adjoint_pullback_density(density)
    if implementation == "gauss-legendre":
        retarded = pair_retarded_gauss_legendre(pulled, theta, order=order)
    elif implementation == "adaptive":
        retarded = pair_retarded_adaptive(
            pulled, theta, epsabs=epsabs, epsrel=epsrel
        )
    else:
        raise ValueError("implementation must be 'gauss-legendre' or 'adaptive'")
    return PairingResult(
        matrix=np.conjugate(retarded.matrix).T,
        theta=retarded.theta,
        implementation=f"advanced-adjoint-via-{retarded.implementation}",
    )


def transform_global_basis(matrix: np.ndarray, basis: np.ndarray) -> np.ndarray:
    """Apply the frozen mixed-index global similarity convention."""

    matrix = np.asarray(matrix, dtype=np.complex128)
    basis = np.asarray(basis, dtype=np.complex128)
    if matrix.shape != (2, 2) or basis.shape != (2, 2):
        raise ValueError("matrix and basis must both have shape (2, 2)")
    if not np.all(np.isfinite(matrix)) or not np.all(np.isfinite(basis)):
        raise ValueError("matrix and basis must be finite")
    if abs(np.linalg.det(basis)) == 0.0:
        raise ValueError("basis must be invertible")
    return basis @ matrix @ np.linalg.inv(basis)
