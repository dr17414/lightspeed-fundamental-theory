"""Candidate-independent E4 well-posedness contract for Stage 5C 6a-E.

The fixed C8 regulator is part of the continuum target, not an approximation
that is silently sent to zero.  This module therefore separates three things:

* exact structural facts (Gaussian-mixture topology, zero extension, and no
  contact atom),
* reported regulator leakage across the box and causal-order boundaries, and
* live quadrature error for the typed continuum pairing.

It never reads an arm ledger, claims a 6a-E seed, forms an arm endpoint, or
imports a candidate kernel.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import fsum, hypot, sqrt

import numpy as np
from scipy import integrate, special

from analysis.stage5c_continuum_pairing import (
    PairingResult,
    conformal_volume_density,
    pair_retarded_gauss_legendre,
)
from analysis.stage5c_hard_controls import CONTROL_THETA
from analysis.stage5c_measure_prereg import (
    MASS_TOLERANCE,
    SMEARING_EPSILON,
)
from analysis.stage5c_numerical_certification import (
    CertificationResult,
    CertificationStatus,
    ErrorBudget,
    ImplementationEstimate,
    certify_pairing,
)


E4_CONTRACT_ID = "stage5c-6a-e-e4-wellposedness-v0.1"
E4_TOPOLOGY_ID = "finite-probability-gaussian-mixtures-fixed-epsilon-v0.1"
E4_LEAKAGE_ID = "ambient-gaussian-box-and-causal-leakage-v0.1"
E4_GAUSS_IMPLEMENTATION_ID = "gauss-legendre-32-with-cell-enclosure-v0.1"
E4_ADAPTIVE_IMPLEMENTATION_ID = "adaptive-genz-malik-with-cell-enclosure-v0.1"
E4_ENCLOSURE_ID = "positive-gaussian-characteristic-cell-enclosure-v0.1"

E4_THETA_DOMAIN = (-CONTROL_THETA, CONTROL_THETA)
E4_THETA_SUITE = (-CONTROL_THETA, 0.0, CONTROL_THETA)
E4_GAUSS_ORDER = 32
E4_CUBATURE_RTOL = 2.0**-14
E4_CUBATURE_ATOL = 2.0**-30
E4_MAX_SUBDIVISIONS = 4096
E4_MAX_ATOMS = 8128
E4_DENSITY_CHUNK_SIZE = 128
E4_ENCLOSURE_LEVELS = (16, 32, 64)
E4_TRANSVERSE_DIVISOR = 4
E4_OUTWARD_ULPS = 64


class E4ProtocolError(ValueError):
    """The requested object is outside the frozen E4 contract."""


class E4Status(str, Enum):
    CLEAN = "CLEAN"
    INCONCLUSIVE = "INCONCLUSIVE"


class E4Reason(str, Enum):
    CERTIFIED = "CERTIFIED"
    ADAPTIVE_RESOURCE_CAP = "ADAPTIVE_RESOURCE_CAP"
    NONFINITE_BACKEND = "NONFINITE_BACKEND"
    NUMERICAL_CERTIFICATION_INCONCLUSIVE = "NUMERICAL_CERTIFICATION_INCONCLUSIVE"
    STRUCTURAL_LEAKAGE_INVALID = "STRUCTURAL_LEAKAGE_INVALID"


@dataclass(frozen=True)
class LeakageDiagnostics:
    """Exact fixed-regulator diagnostics; none is a renormalisation factor."""

    box_retained_mass: float
    box_leakage: float
    causal_retained_mass: float
    causal_leakage: float
    exact_contact_atom_mass: float = 0.0
    strict_geometry_validated: bool = False
    box_leakage_bound_validated: bool = False
    causal_leakage_bound_validated: bool = False
    leakage_id: str = E4_LEAKAGE_ID

    @property
    def structurally_admissible(self) -> bool:
        # The strict inequalities are established from the input coordinates
        # before these binary64 diagnostics are evaluated.  For a positive
        # sub-ULP coordinate or gap, ndtr can round a factor to exactly 1/2.
        # The separate cancellation-safe box and causal checks preserve the
        # registered leakage gates while accounting for the permitted weight-
        # sum tolerance.  The causal calculation has no opposite-box tail.
        return bool(
            self.strict_geometry_validated
            and self.box_leakage_bound_validated
            and self.causal_leakage_bound_validated
            and np.isfinite(self.box_retained_mass)
            and 0.0 <= self.box_retained_mass <= 1.0
            and np.isfinite(self.box_leakage)
            and 0.0 <= self.box_leakage <= 1.0
            and np.isfinite(self.causal_retained_mass)
            and 0.0 <= self.causal_retained_mass <= 1.0
            and np.isfinite(self.causal_leakage)
            and 0.0 <= self.causal_leakage <= 1.0
            and self.exact_contact_atom_mass == 0.0
        )


@dataclass(frozen=True)
class CubatureRun:
    """One adaptive run and its non-certifying algorithm diagnostic."""

    matrix: np.ndarray
    error: float
    rule: str
    subdivisions: int
    solver_status: str

    def __post_init__(self) -> None:
        matrix = np.asarray(self.matrix, dtype=np.complex128)
        if matrix.shape != (2, 2):
            raise E4ProtocolError("cubature matrix must be 2x2")
        error = float(self.error)
        if np.isnan(error) or error < 0.0:
            raise E4ProtocolError("cubature diagnostic error must be non-negative")
        if (
            not isinstance(self.subdivisions, (int, np.integer))
            or self.subdivisions < 0
        ):
            raise E4ProtocolError("subdivisions must be a non-negative integer")
        frozen = matrix.copy()
        frozen.setflags(write=False)
        object.__setattr__(self, "matrix", frozen)
        object.__setattr__(self, "error", error)
        object.__setattr__(self, "subdivisions", int(self.subdivisions))
        if not isinstance(self.solver_status, str) or not self.solver_status:
            raise E4ProtocolError("solver_status must be a non-empty string")

    @property
    def converged(self) -> bool:
        return self.solver_status == "converged"


@dataclass(frozen=True)
class PairingEnclosure:
    """Outward interval for the two real diagonal pairing components."""

    lower: np.ndarray
    upper: np.ndarray
    level_lower: np.ndarray
    level_upper: np.ndarray
    levels: tuple[int, ...] = E4_ENCLOSURE_LEVELS
    enclosure_id: str = E4_ENCLOSURE_ID

    def __post_init__(self) -> None:
        lower = np.asarray(self.lower, dtype=float)
        upper = np.asarray(self.upper, dtype=float)
        level_lower = np.asarray(self.level_lower, dtype=float)
        level_upper = np.asarray(self.level_upper, dtype=float)
        if lower.shape != (2,) or upper.shape != (2,):
            raise E4ProtocolError("pairing enclosure endpoints must have shape (2,)")
        if not np.all(np.isfinite(lower)) or not np.all(np.isfinite(upper)):
            raise E4ProtocolError("pairing enclosure endpoints must be finite")
        if np.any(lower < 0.0) or np.any(lower > upper):
            raise E4ProtocolError("pairing enclosure must be ordered and non-negative")
        expected_level_shape = (len(self.levels), 2)
        if (
            level_lower.shape != expected_level_shape
            or level_upper.shape != expected_level_shape
        ):
            raise E4ProtocolError(
                f"level enclosure endpoints must have shape {expected_level_shape}"
            )
        if (
            not np.all(np.isfinite(level_lower))
            or not np.all(np.isfinite(level_upper))
            or np.any(level_lower < 0.0)
            or np.any(level_lower > level_upper)
        ):
            raise E4ProtocolError("every level enclosure must be finite and ordered")
        frozen_lower = lower.copy()
        frozen_upper = upper.copy()
        frozen_level_lower = level_lower.copy()
        frozen_level_upper = level_upper.copy()
        frozen_lower.setflags(write=False)
        frozen_upper.setflags(write=False)
        frozen_level_lower.setflags(write=False)
        frozen_level_upper.setflags(write=False)
        object.__setattr__(self, "lower", frozen_lower)
        object.__setattr__(self, "upper", frozen_upper)
        object.__setattr__(self, "level_lower", frozen_level_lower)
        object.__setattr__(self, "level_upper", frozen_level_upper)

    @property
    def widths(self) -> np.ndarray:
        values = np.nextafter(self.upper - self.lower, np.inf)
        values.setflags(write=False)
        return values

    def error_for(self, matrix: np.ndarray) -> float:
        """Frobenius distance from ``matrix`` to the farthest enclosure corner."""

        matrix = np.asarray(matrix, dtype=np.complex128)
        if matrix.shape != (2, 2) or not np.all(np.isfinite(matrix)):
            raise E4ProtocolError("implementation matrix must be finite and 2x2")
        diagonal = np.diag(matrix)
        real_error = np.maximum(
            np.abs(diagonal.real - self.lower),
            np.abs(self.upper - diagonal.real),
        )
        components = np.concatenate(
            (real_error, np.abs(diagonal.imag), np.abs(matrix[[0, 1], [1, 0]]))
        )
        return _up(hypot(*(float(value) for value in components)))


@dataclass(frozen=True)
class E4Report:
    """Complete candidate-independent E4 result for one fixed test density."""

    status: E4Status
    leakage: LeakageDiagnostics
    gauss: ImplementationEstimate
    adaptive: ImplementationEstimate
    enclosure: PairingEnclosure
    adaptive_run: CubatureRun
    certification: CertificationResult
    reason: E4Reason
    topology_id: str = E4_TOPOLOGY_ID
    contract_id: str = E4_CONTRACT_ID

    @property
    def clean(self) -> bool:
        return bool(
            self.status is E4Status.CLEAN
            and self.leakage.structurally_admissible
            and self.certification.status is CertificationStatus.CLEAN
        )


def _up(value: float) -> float:
    value = float(value)
    return 0.0 if value == 0.0 else float(np.nextafter(value, np.inf))


def _frobenius_upper(matrix: np.ndarray) -> float:
    components = np.stack((matrix.real, matrix.imag), axis=-1).ravel()
    return _up(hypot(*(float(value) for value in components)))


def _validated_theta(theta: float) -> float:
    theta = float(theta)
    if not np.isfinite(theta) or not E4_THETA_DOMAIN[0] <= theta <= E4_THETA_DOMAIN[1]:
        raise E4ProtocolError(f"theta must lie in {E4_THETA_DOMAIN}")
    return theta


def _validated_mixture(
    pair_coordinates: np.ndarray, probability_weights: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    atoms = np.asarray(pair_coordinates, dtype=float)
    weights = np.asarray(probability_weights, dtype=float)
    if atoms.ndim != 2 or atoms.shape[1:] != (4,) or len(atoms) == 0:
        raise E4ProtocolError("pair_coordinates must have shape (m,4), m > 0")
    if len(atoms) > E4_MAX_ATOMS:
        raise E4ProtocolError(f"E4 supports at most {E4_MAX_ATOMS} atoms")
    if not np.all(np.isfinite(atoms)) or np.any(atoms <= 0.0) or np.any(atoms >= 1.0):
        raise E4ProtocolError("E4 atoms must lie strictly inside the unit four-box")
    if np.any(atoms[:, 0] <= atoms[:, 2]) or np.any(atoms[:, 1] <= atoms[:, 3]):
        raise E4ProtocolError("every E4 atom must be a strict ordered causal pair")
    if weights.shape != (len(atoms),) or not np.all(np.isfinite(weights)):
        raise E4ProtocolError("one finite probability weight is required per atom")
    if np.any(weights < 0.0) or abs(float(weights.sum()) - 1.0) > MASS_TOLERANCE:
        raise E4ProtocolError("E4 mixture weights must be non-negative and sum to one")
    frozen_atoms = atoms.copy()
    frozen_weights = weights.copy()
    frozen_atoms.setflags(write=False)
    frozen_weights.setflags(write=False)
    return frozen_atoms, frozen_weights


def leakage_diagnostics(
    pair_coordinates: np.ndarray, probability_weights: np.ndarray
) -> LeakageDiagnostics:
    """Return analytic ambient-Gaussian leakage without renormalising the box.

    For one atom ``z``, the four box coordinates are independent, so retained
    mass is a product of normal-CDF differences.  The two causal differences
    have variance ``2 epsilon**2`` and are mutually independent.
    """

    atoms, weights = _validated_mixture(pair_coordinates, probability_weights)
    epsilon = SMEARING_EPSILON
    coordinate_mass = special.ndtr((1.0 - atoms) / epsilon) - special.ndtr(
        -atoms / epsilon
    )
    box_retained = float(weights @ np.prod(coordinate_mass, axis=1))
    gaps = atoms[:, :2] - atoms[:, 2:]
    causal_mass = special.ndtr(gaps / (sqrt(2.0) * epsilon))
    causal_retained = float(weights @ np.prod(causal_mass, axis=1))
    return LeakageDiagnostics(
        box_retained_mass=box_retained,
        box_leakage=_up(1.0 - box_retained),
        causal_retained_mass=causal_retained,
        causal_leakage=_up(1.0 - causal_retained),
        strict_geometry_validated=True,
        box_leakage_bound_validated=_box_mass_exceeds_one_sixteenth(
            atoms, weights
        ),
        causal_leakage_bound_validated=_causal_mass_exceeds_one_quarter(
            atoms, weights
        ),
    )


def _box_mass_exceeds_one_sixteenth(
    atoms: np.ndarray, weights: np.ndarray
) -> bool:
    """Test retained box mass > 1/16 without losing boundary-scale excess.

    For distance ``d`` to the nearest boundary, one coordinate has mass
    ``1/2 + delta`` where delta is the near-boundary CDF gain minus the
    opposite-boundary tail.  Keeping delta separate avoids rounding the mass
    to exactly 1/2 before the four-coordinate product is compared.
    """

    epsilon = SMEARING_EPSILON
    nearest = np.minimum(atoms, 1.0 - atoms)
    scaled = 1.0 / (sqrt(2.0) * epsilon)
    near_gain = 0.5 * special.erf(nearest * scaled)
    opposite_tail = 0.5 * special.erfc((1.0 - nearest) * scaled)
    delta = near_gain - opposite_tail
    log_mass_ratios = np.log1p(2.0 * delta)
    atom_excess = np.expm1(np.sum(log_mass_ratios, axis=1)) / 16.0
    normalization_offset = (fsum(float(weight) for weight in weights) - 1.0) / 16.0
    mixture_excess = fsum(
        [
            normalization_offset,
            *(
                float(weight) * float(excess)
                for weight, excess in zip(weights, atom_excess, strict=True)
            ),
        ]
    )
    return bool(np.isfinite(mixture_excess) and mixture_excess > 0.0)


def _causal_mass_exceeds_one_quarter(
    atoms: np.ndarray, weights: np.ndarray
) -> bool:
    """Test retained causal mass > 1/4 at gap and weight tolerances."""

    gaps = atoms[:, :2] - atoms[:, 2:]
    gain = 0.5 * special.erf(gaps / (2.0 * SMEARING_EPSILON))
    log_mass_ratios = np.log1p(2.0 * gain)
    atom_excess = np.expm1(np.sum(log_mass_ratios, axis=1)) / 4.0
    normalization_offset = (fsum(float(weight) for weight in weights) - 1.0) / 4.0
    mixture_excess = fsum(
        [
            normalization_offset,
            *(
                float(weight) * float(excess)
                for weight, excess in zip(weights, atom_excess, strict=True)
            ),
        ]
    )
    return bool(np.isfinite(mixture_excess) and mixture_excess > 0.0)


def conformal_density_lower_bound(theta: float) -> float:
    """Exact lower bound of p_theta on the registered q-product range."""

    theta = _validated_theta(theta)
    return 1.0 - 0.5 * theta if theta >= 0.0 else 1.0 + theta


def pairing_operator_sup_bound(theta: float) -> float:
    """Operator norm bound from density sup norm to matrix Frobenius norm.

    Each characteristic triangle has Lebesgue mass 1/2.  On the E4 theta
    domain, the conformal biweight is at most p_min**(-1/2), hence
    ``||<S_theta,r>||_F <= ||r||_infty / sqrt(2 p_min)``.
    """

    return 1.0 / sqrt(2.0 * conformal_density_lower_bound(theta))


def _outward(values: np.ndarray, direction: float) -> np.ndarray:
    """Apply the frozen binary64 margin used by the enclosure arithmetic."""

    values = np.asarray(values, dtype=float)
    margin = E4_OUTWARD_ULPS * np.maximum(
        np.abs(np.spacing(values)), np.nextafter(0.0, 1.0)
    )
    shifted = values + direction * margin
    return np.nextafter(shifted, -np.inf if direction < 0.0 else np.inf)


def _outward_nonnegative(values: np.ndarray, direction: float) -> np.ndarray:
    result = _outward(values, direction)
    return np.maximum(result, 0.0) if direction < 0.0 else result


def _positive_arithmetic_enclosure(
    values: np.ndarray, operation_count: int, direction: float
) -> np.ndarray:
    """Enclose positive-product/sum rounding under the binary64 model."""

    unit_roundoff = 0.5 * np.finfo(np.float64).eps
    scaled = operation_count * unit_roundoff
    if operation_count < 1 or scaled >= 1.0:
        raise E4ProtocolError("invalid positive-arithmetic operation bound")
    gamma = scaled / (1.0 - scaled)
    factor = 1.0 - gamma if direction < 0.0 else 1.0 + gamma
    return _outward_nonnegative(np.asarray(values, dtype=float) * factor, direction)


def _normal_interval_integral(
    edges: np.ndarray, centres: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Outward integrals of exp(-(x-centre)^2/(2 epsilon^2))."""

    lower_z = (edges[:-1, None] - centres[None, :]) / SMEARING_EPSILON
    upper_z = (edges[1:, None] - centres[None, :]) / SMEARING_EPSILON
    # Use the negative-tail identity when both endpoints are positive.  This
    # avoids subtracting two values rounded to one in boundary-far cells.
    cdf_difference = np.where(
        lower_z >= 0.0,
        special.ndtr(-lower_z) - special.ndtr(-upper_z),
        special.ndtr(upper_z) - special.ndtr(lower_z),
    )
    values = SMEARING_EPSILON * sqrt(2.0 * np.pi) * cdf_difference
    return _outward_nonnegative(values, -1.0), _outward(values, 1.0)


def _same_variable_product_integral(
    edges: np.ndarray, first: np.ndarray, second: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Outward integral of two equal-width Gaussian factors in one variable."""

    midpoint = 0.5 * (first + second)
    lower_z = (
        sqrt(2.0) * (edges[:-1, None] - midpoint[None, :]) / SMEARING_EPSILON
    )
    upper_z = (
        sqrt(2.0) * (edges[1:, None] - midpoint[None, :]) / SMEARING_EPSILON
    )
    cdf_difference = np.where(
        lower_z >= 0.0,
        special.ndtr(-lower_z) - special.ndtr(-upper_z),
        special.ndtr(upper_z) - special.ndtr(lower_z),
    )
    prefactor = (
        SMEARING_EPSILON
        * sqrt(np.pi)
        * np.exp(-((first - second) ** 2) / (4.0 * SMEARING_EPSILON**2))
    )
    values = cdf_difference * prefactor[None, :]
    return _outward_nonnegative(values, -1.0), _outward(values, 1.0)


def _q_interval(edges: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    lower = edges[:-1]
    upper = edges[1:]
    at_lower = 6.0 * lower * lower - 6.0 * lower + 1.0
    at_upper = 6.0 * upper * upper - 6.0 * upper + 1.0
    minimum = np.minimum(at_lower, at_upper)
    minimum[(lower <= 0.5) & (upper >= 0.5)] = -0.5
    maximum = np.maximum(at_lower, at_upper)
    return _outward(minimum, -1.0), _outward(maximum, 1.0)


def _product_interval(
    first: tuple[np.ndarray, np.ndarray], second: tuple[np.ndarray, np.ndarray]
) -> tuple[np.ndarray, np.ndarray]:
    products = np.stack(
        (
            first[0] * second[0],
            first[0] * second[1],
            first[1] * second[0],
            first[1] * second[1],
        )
    )
    return _outward(np.min(products, axis=0), -1.0), _outward(
        np.max(products, axis=0), 1.0
    )


def _conformal_weight_cells(
    theta: float, pair_edges: np.ndarray, transverse_edges: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    pair_q = _q_interval(pair_edges)
    transverse_q = _q_interval(transverse_edges)
    q_product = _product_interval(
        (pair_q[0][:, None], pair_q[1][:, None]),
        (transverse_q[0][None, :], transverse_q[1][None, :]),
    )
    if theta >= 0.0:
        p_lower = 1.0 + theta * q_product[0]
        p_upper = 1.0 + theta * q_product[1]
    else:
        p_lower = 1.0 + theta * q_product[1]
        p_upper = 1.0 + theta * q_product[0]
    p_lower = _outward(p_lower, -1.0)
    p_upper = _outward(p_upper, 1.0)
    p_pair = _product_interval(
        (p_lower[:, None, :], p_upper[:, None, :]),
        (p_lower[None, :, :], p_upper[None, :, :]),
    )
    # x -> x^(-1/4) is decreasing on the positive conformal-density range.
    return _outward(p_pair[1] ** -0.25, -1.0), _outward(
        p_pair[0] ** -0.25, 1.0
    )


def _level_pairing_enclosure(
    atoms: np.ndarray, weights: np.ndarray, theta: float, pair_cells: int
) -> tuple[np.ndarray, np.ndarray]:
    """One dyadic enclosure level in direct (a,b,t) characteristic variables."""

    transverse_cells = pair_cells // E4_TRANSVERSE_DIVISOR
    pair_edges = np.linspace(0.0, 1.0, pair_cells + 1)
    transverse_edges = np.linspace(0.0, 1.0, transverse_cells + 1)
    weight_lower, weight_upper = _conformal_weight_cells(
        theta, pair_edges, transverse_edges
    )
    strictly_below = np.tril(
        np.ones((pair_cells, pair_cells), dtype=bool), k=-1
    )[:, :, None]
    diagonal_cover = np.eye(pair_cells, dtype=bool)[:, :, None]
    coefficient = (2.0 * np.pi * SMEARING_EPSILON**2) ** -2
    sector_bounds: list[tuple[float, float]] = []
    for sector in (0, 1):
        if sector == 0:
            a_centres, b_centres = atoms[:, 0], atoms[:, 2]
            first_t, second_t = atoms[:, 1], atoms[:, 3]
        else:
            a_centres, b_centres = atoms[:, 1], atoms[:, 3]
            first_t, second_t = atoms[:, 0], atoms[:, 2]
        a_interval = _normal_interval_integral(pair_edges, a_centres)
        b_interval = _normal_interval_integral(pair_edges, b_centres)
        t_interval = _same_variable_product_integral(
            transverse_edges, first_t, second_t
        )
        mass_lower = coefficient * np.einsum(
            "im,jm,km,m->ijk",
            a_interval[0],
            b_interval[0],
            t_interval[0],
            weights,
            optimize=True,
        )
        mass_upper = coefficient * np.einsum(
            "im,jm,km,m->ijk",
            a_interval[1],
            b_interval[1],
            t_interval[1],
            weights,
            optimize=True,
        )
        mixture_operations = 6 * len(atoms) + 16
        mass_lower = _positive_arithmetic_enclosure(
            mass_lower, mixture_operations, -1.0
        )
        mass_upper = _positive_arithmetic_enclosure(
            mass_upper, mixture_operations, 1.0
        )
        lower = float(np.sum(mass_lower * weight_lower, where=strictly_below))
        upper = float(
            np.sum(
                mass_upper * weight_upper,
                where=np.logical_or(strictly_below, diagonal_cover),
            )
        )
        below_cells = (
            pair_cells
            * (pair_cells - 1)
            // 2
            * transverse_cells
        )
        covered_cells = below_cells + pair_cells * transverse_cells
        sector_bounds.append(
            (
                float(
                    _positive_arithmetic_enclosure(
                        np.asarray(lower), 3 * below_cells + 8, -1.0
                    )
                ),
                float(
                    _positive_arithmetic_enclosure(
                        np.asarray(upper), 3 * covered_cells + 8, 1.0
                    )
                ),
            )
        )
    return (
        np.asarray([item[0] for item in sector_bounds]),
        np.asarray([item[1] for item in sector_bounds]),
    )


def pairing_enclosure(
    pair_coordinates: np.ndarray, probability_weights: np.ndarray, theta: float
) -> PairingEnclosure:
    """Intersect a frozen dyadic sequence of analytic positive-cell bounds.

    In direct characteristic coordinates ``(a,b,t)``, every Gaussian cell
    mass factorises into analytic one-dimensional integrals.  Full cells below
    ``b=a`` contribute to both bounds; diagonal cells contribute only to the
    upper bound.  Interval extrema of the conformal biweight complete the
    enclosure.  No adaptive-rule error estimate enters this calculation.
    """

    theta = _validated_theta(theta)
    atoms, weights = _validated_mixture(pair_coordinates, probability_weights)
    level_bounds = [
        _level_pairing_enclosure(atoms, weights, theta, level)
        for level in E4_ENCLOSURE_LEVELS
    ]
    level_lower = np.stack([item[0] for item in level_bounds])
    level_upper = np.stack([item[1] for item in level_bounds])
    lower = np.max(level_lower, axis=0)
    upper = np.min(level_upper, axis=0)
    return PairingEnclosure(
        lower=lower,
        upper=upper,
        level_lower=level_lower,
        level_upper=level_upper,
    )


def _mixture_density(atoms: np.ndarray, weights: np.ndarray):
    def density(points: np.ndarray) -> np.ndarray:
        points = np.asarray(points, dtype=float)
        flat = points.reshape((-1, 4))
        values = np.zeros(len(flat), dtype=float)
        coefficient = (2.0 * np.pi * SMEARING_EPSILON**2) ** -2
        # Fixed-size chunks prevent the maximum registered 8128-atom mixture
        # from creating an unbounded q-by-m-by-4 temporary array.  All terms
        # are non-negative and chunks are accumulated in source order.
        for start in range(0, len(atoms), E4_DENSITY_CHUNK_SIZE):
            stop = min(start + E4_DENSITY_CHUNK_SIZE, len(atoms))
            delta = flat[:, None, :] - atoms[None, start:stop, :]
            squared = np.sum(delta * delta, axis=2)
            values += np.exp(-squared / (2.0 * SMEARING_EPSILON**2)) @ weights[
                start:stop
            ]
        values *= coefficient
        return values.reshape(points.shape[:-1])

    return density


def _cubature_pairing(
    atoms: np.ndarray, weights: np.ndarray, theta: float, rule: str
) -> CubatureRun:
    """Integrate both characteristic sectors in one rule-specific traversal."""

    density = _mixture_density(atoms, weights)

    def integrand(cube_points: np.ndarray) -> np.ndarray:
        cube_points = np.asarray(cube_points, dtype=float)
        a, s, transverse = cube_points.T
        right_points = np.stack((a, transverse, a * s, transverse), axis=-1)
        left_points = np.stack((transverse, a, transverse, a * s), axis=-1)

        def entry(points: np.ndarray) -> np.ndarray:
            px = conformal_volume_density(points[:, 0], points[:, 1], theta)
            py = conformal_volume_density(points[:, 2], points[:, 3], theta)
            biweight = np.asarray(px * py, dtype=float) ** -0.25
            return a * biweight * density(points)

        right = entry(right_points)
        left = entry(left_points)
        zeros = np.zeros_like(right)
        return np.stack((right, zeros, left, zeros), axis=-1)

    result = integrate.cubature(
        integrand,
        np.zeros(3),
        np.ones(3),
        rule=rule,
        atol=E4_CUBATURE_ATOL,
        rtol=E4_CUBATURE_RTOL,
        max_subdivisions=E4_MAX_SUBDIVISIONS,
    )
    estimate = np.asarray(result.estimate, dtype=float)
    errors = np.abs(np.asarray(result.error, dtype=float))
    if estimate.shape != (4,) or errors.shape != (4,):
        raise RuntimeError(f"E4 {rule} cubature returned an invalid live error record")
    matrix = np.diag(
        [complex(estimate[0], estimate[1]), complex(estimate[2], estimate[3])]
    )
    return CubatureRun(
        matrix=matrix,
        error=(
            np.inf
            if not np.all(np.isfinite(errors))
            else _up(hypot(*(float(value) for value in errors)))
        ),
        rule=rule,
        subdivisions=int(result.subdivisions),
        solver_status=str(result.status),
    )


def _budget(quadrature: float) -> ErrorBudget:
    # The empirical Gaussian mixture, fixed regulator, zero extension, and
    # contact convention are exact inputs to this numerical problem.  They are
    # reported separately and therefore contribute zero approximation error.
    # The farthest-corner radius is centred on the returned binary64 matrix,
    # so it already covers discretisation *and* all arithmetic displacement of
    # that output.  The generic rounding slot is therefore exactly zero rather
    # than an incomplete recount of implementation-specific operations.
    return ErrorBudget(
        quadrature=quadrature,
        sampling_representation=0.0,
        regulator=0.0,
        boundary_contact=0.0,
        accumulation_term_norm_sum=0.0,
        real_additions=1,
    )


def evaluate_e4_wellposedness(
    pair_coordinates: np.ndarray, probability_weights: np.ndarray, theta: float
) -> E4Report:
    """Evaluate the frozen E4 contract on one candidate-independent density."""

    theta = _validated_theta(theta)
    atoms, weights = _validated_mixture(pair_coordinates, probability_weights)
    leakage = leakage_diagnostics(atoms, weights)
    density = _mixture_density(atoms, weights)

    fixed: PairingResult = pair_retarded_gauss_legendre(
        density, theta, order=E4_GAUSS_ORDER
    )
    gm = _cubature_pairing(atoms, weights, theta, "genz-malik")
    enclosure = pairing_enclosure(atoms, weights, theta)

    # Each implementation is compared to the farthest corner of an analytic
    # interval known to contain the exact pairing.  The adaptive solver's own
    # error estimate is retained only as a diagnostic and is never promoted to
    # a validated ErrorBudget component.
    fixed_error = enclosure.error_for(fixed.matrix)
    adaptive_matrix_finite = bool(np.all(np.isfinite(gm.matrix)))
    adaptive_output_finite = bool(adaptive_matrix_finite and np.isfinite(gm.error))
    adaptive_error = (
        enclosure.error_for(gm.matrix) if adaptive_matrix_finite else 0.0
    )
    gauss = ImplementationEstimate(
        fixed.matrix,
        _budget(fixed_error),
        E4_GAUSS_IMPLEMENTATION_ID,
    )
    adaptive = ImplementationEstimate(
        gm.matrix,
        _budget(adaptive_error),
        E4_ADAPTIVE_IMPLEMENTATION_ID,
    )
    certification = certify_pairing(gauss, adaptive)
    if not leakage.structurally_admissible:
        status = E4Status.INCONCLUSIVE
        reason = E4Reason.STRUCTURAL_LEAKAGE_INVALID
    elif not adaptive_output_finite:
        status = E4Status.INCONCLUSIVE
        reason = E4Reason.NONFINITE_BACKEND
    elif not gm.converged:
        status = E4Status.INCONCLUSIVE
        reason = E4Reason.ADAPTIVE_RESOURCE_CAP
    elif certification.status is not CertificationStatus.CLEAN:
        status = E4Status.INCONCLUSIVE
        reason = E4Reason.NUMERICAL_CERTIFICATION_INCONCLUSIVE
    else:
        status = E4Status.CLEAN
        reason = E4Reason.CERTIFIED
    return E4Report(
        status=status,
        leakage=leakage,
        gauss=gauss,
        adaptive=adaptive,
        enclosure=enclosure,
        adaptive_run=gm,
        certification=certification,
        reason=reason,
    )


__all__ = [
    "E4_ADAPTIVE_IMPLEMENTATION_ID",
    "E4_CONTRACT_ID",
    "E4_CUBATURE_ATOL",
    "E4_CUBATURE_RTOL",
    "E4_ENCLOSURE_ID",
    "E4_ENCLOSURE_LEVELS",
    "E4_GAUSS_IMPLEMENTATION_ID",
    "E4_GAUSS_ORDER",
    "E4_LEAKAGE_ID",
    "E4_DENSITY_CHUNK_SIZE",
    "E4_MAX_ATOMS",
    "E4_MAX_SUBDIVISIONS",
    "E4_OUTWARD_ULPS",
    "E4_THETA_DOMAIN",
    "E4_THETA_SUITE",
    "E4_TOPOLOGY_ID",
    "E4_TRANSVERSE_DIVISOR",
    "CubatureRun",
    "E4ProtocolError",
    "E4Report",
    "E4Reason",
    "E4Status",
    "LeakageDiagnostics",
    "PairingEnclosure",
    "conformal_density_lower_bound",
    "evaluate_e4_wellposedness",
    "leakage_diagnostics",
    "pairing_operator_sup_bound",
    "pairing_enclosure",
]
