"""Frozen candidate-independent smearing/normalisation/6a-S preregistration.

This module defines evaluator-side measure primitives only.  It does not
construct, import, execute, or inspect a candidate kernel, and it does not
compare the two target arms.  The numerical 6a-S run is deliberately separate:
this source must be committed before any reserved seed below is generated.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

import numpy as np


# Fixed-cardinality sprinklings in the unit null-coordinate square.  The
# Gaussian acts on ordered pair space (u_x, v_x, u_y, v_y).
CARDINALITIES = (64, 96, 128)
CASES_PER_BLOCK = 64
BLOCKS_PER_TARGET = 4
TARGET_SEED_BASES = {"plus": 1_300_000_000, "minus": 1_400_000_000}
SMEARING_EPSILON = 1.0 / 16.0

# 6a-S equivalence margins.  They are fixed before the reserved streams are
# touched and apply to every selector, target, N, and pair of independent
# blocks.  They are operational finite-resolution gates, not a theorem of full
# weak convergence.
MAX_MEAN_SIGNATURE_DISTANCE = 0.20
MAX_RANDOM_LAW_ENERGY_DISTANCE = 0.20
MIN_SELECTED_PAIRS = 32
MIN_PAIR_COVERAGE = 0.005
MIN_KISH_ESS = 32.0
MIN_ESS_FRACTION = 0.95
MASS_TOLERANCE = 1.0e-12

# First non-zero Fourier shell on the dimensionless unit 4-cube.  This fixed,
# target-independent grid has no optimiser, random features, or fitted scale.
FOURIER_FREQUENCIES = np.asarray(
    [
        tuple(2.0 * np.pi * k for k in index)
        for index in product((-1, 0, 1), repeat=4)
        if index != (0, 0, 0, 0)
    ],
    dtype=float,
)
FOURIER_FREQUENCIES.setflags(write=False)


class MeasureProtocolError(ValueError):
    """The caller or supplied data violate the frozen 6a-S contract."""


@dataclass(frozen=True)
class MeasureDiagnostics:
    """Candidate-independent S1/S6 diagnostics for one selected pair measure."""

    selected_pairs: int
    domain_pairs: int
    coverage: float
    normalization: float
    total_mass: float
    total_variation: float
    kish_ess: float
    ess_fraction: float


def preregistered_seed(target: str, n_index: int, block: int, case: int) -> int:
    """Map one 6a-S cell to a unique PCG64DXSM seed.

    No seed returned here may be used by 6a-E or candidate evaluation.  A seed
    becomes burned when the corresponding sample is first generated.
    """
    if target not in TARGET_SEED_BASES:
        raise MeasureProtocolError("target must be 'plus' or 'minus'")
    if not 0 <= n_index < len(CARDINALITIES):
        raise MeasureProtocolError("n_index is outside the frozen sequence")
    if not 0 <= block < BLOCKS_PER_TARGET:
        raise MeasureProtocolError("block is outside the frozen block range")
    if not 0 <= case < CASES_PER_BLOCK:
        raise MeasureProtocolError("case is outside the frozen block range")
    return TARGET_SEED_BASES[target] + 1_000_000 * n_index + 10_000 * block + case


def uniform_pair_weights(selected_pairs: int) -> tuple[np.ndarray, float]:
    """Return phi=1 and N_C=|Sigma(C)| for the C8 induced probability measure."""
    if not isinstance(selected_pairs, (int, np.integer)) or selected_pairs <= 0:
        raise MeasureProtocolError("selected_pairs must be a positive integer")
    weights = np.ones(int(selected_pairs), dtype=float)
    return weights, float(selected_pairs)


def normalised_weights(weights: np.ndarray, normalization: float) -> np.ndarray:
    value = np.asarray(weights, dtype=float)
    if value.ndim != 1 or value.size == 0 or not np.all(np.isfinite(value)):
        raise MeasureProtocolError("weights must be one finite non-empty vector")
    if np.any(value < 0.0):
        raise MeasureProtocolError("the frozen C8 smearing weights are non-negative")
    if not np.isfinite(normalization) or normalization <= 0.0:
        raise MeasureProtocolError("normalization must be finite and positive")
    return value / float(normalization)


def kish_effective_sample_size(probability_weights: np.ndarray) -> float:
    value = np.asarray(probability_weights, dtype=float)
    if value.ndim != 1 or value.size == 0 or np.any(value < 0.0):
        raise MeasureProtocolError("probability_weights must be non-negative")
    denominator = float(np.dot(value, value))
    if denominator <= 0.0 or not np.isfinite(denominator):
        raise MeasureProtocolError("effective sample size is undefined")
    total = float(value.sum())
    return total * total / denominator


def measure_diagnostics(selected_pairs: int, domain_pairs: int) -> MeasureDiagnostics:
    if not isinstance(domain_pairs, (int, np.integer)) or domain_pairs <= 0:
        raise MeasureProtocolError("domain_pairs must be a positive integer")
    if selected_pairs > domain_pairs:
        raise MeasureProtocolError("selection cannot exceed its causal-pair domain")
    weights, normalization = uniform_pair_weights(selected_pairs)
    probability = normalised_weights(weights, normalization)
    ess = kish_effective_sample_size(probability)
    return MeasureDiagnostics(
        selected_pairs=int(selected_pairs),
        domain_pairs=int(domain_pairs),
        coverage=float(selected_pairs / domain_pairs),
        normalization=normalization,
        total_mass=float(probability.sum()),
        total_variation=float(np.abs(probability).sum()),
        kish_ess=ess,
        ess_fraction=float(ess / selected_pairs),
    )


def passes_s1_s6(diagnostics: MeasureDiagnostics) -> bool:
    """Apply the frozen per-causet numerical floors without exclusions."""
    return bool(
        diagnostics.selected_pairs >= MIN_SELECTED_PAIRS
        and diagnostics.coverage >= MIN_PAIR_COVERAGE
        and abs(diagnostics.total_mass - 1.0) <= MASS_TOLERANCE
        and abs(diagnostics.total_variation - 1.0) <= MASS_TOLERANCE
        and diagnostics.kish_ess >= MIN_KISH_ESS
        and diagnostics.ess_fraction >= MIN_ESS_FRACTION
    )


def _validated_pair_coordinates(pair_coordinates: np.ndarray) -> np.ndarray:
    coordinates = np.asarray(pair_coordinates, dtype=float)
    if coordinates.ndim != 2 or coordinates.shape[1:] != (4,):
        raise MeasureProtocolError("pair coordinates must have shape (m,4)")
    if coordinates.shape[0] == 0 or not np.all(np.isfinite(coordinates)):
        raise MeasureProtocolError("pair coordinates must be finite and non-empty")
    if np.any(coordinates < 0.0) or np.any(coordinates > 1.0):
        raise MeasureProtocolError("coordinates must lie in the frozen unit box")
    return coordinates


def gaussian_mollifier_density(
    query_points: np.ndarray,
    pair_coordinates: np.ndarray,
    probability_weights: np.ndarray,
    *,
    epsilon: float = SMEARING_EPSILON,
) -> np.ndarray:
    """Evaluate the fixed mass-one Gaussian regulator R_epsilon nu on R^4."""
    query = np.asarray(query_points, dtype=float)
    atoms = _validated_pair_coordinates(pair_coordinates)
    weights = np.asarray(probability_weights, dtype=float)
    if query.ndim != 2 or query.shape[1:] != (4,) or not np.all(np.isfinite(query)):
        raise MeasureProtocolError("query points must be one finite (q,4) array")
    if weights.shape != (atoms.shape[0],) or np.any(weights < 0.0):
        raise MeasureProtocolError("one non-negative weight is required per atom")
    if not np.isfinite(epsilon) or epsilon <= 0.0:
        raise MeasureProtocolError("epsilon must be finite and positive")
    squared = np.sum((query[:, None, :] - atoms[None, :, :]) ** 2, axis=2)
    coefficient = (2.0 * np.pi * epsilon**2) ** -2
    return coefficient * (np.exp(-squared / (2.0 * epsilon**2)) @ weights)


def fourier_signature(
    pair_coordinates: np.ndarray,
    probability_weights: np.ndarray,
    *,
    epsilon: float = SMEARING_EPSILON,
) -> np.ndarray:
    """Finite spectral signature of the regulated probability measure."""
    atoms = _validated_pair_coordinates(pair_coordinates)
    weights = np.asarray(probability_weights, dtype=float)
    if weights.shape != (atoms.shape[0],) or np.any(weights < 0.0):
        raise MeasureProtocolError("one non-negative weight is required per atom")
    if abs(float(weights.sum()) - 1.0) > MASS_TOLERANCE:
        raise MeasureProtocolError("Fourier signature requires probability weights")
    phase = atoms @ FOURIER_FREQUENCIES.T
    raw = weights @ np.exp(1j * phase)
    regulator = np.exp(
        -0.5 * epsilon**2 * np.sum(FOURIER_FREQUENCIES**2, axis=1)
    )
    return raw * regulator


def mean_signature_distance(left: np.ndarray, right: np.ndarray) -> float:
    """L-infinity distance between two block-mean complex signatures."""
    a = np.asarray(left, dtype=complex)
    b = np.asarray(right, dtype=complex)
    if a.ndim != 2 or b.ndim != 2 or a.shape[1:] != b.shape[1:]:
        raise MeasureProtocolError("signature blocks must share feature dimension")
    if a.shape[1] != len(FOURIER_FREQUENCIES) or min(len(a), len(b)) < 2:
        raise MeasureProtocolError("signature blocks violate the frozen schema")
    return float(np.max(np.abs(a.mean(axis=0) - b.mean(axis=0))))


def random_law_energy_distance(left: np.ndarray, right: np.ndarray) -> float:
    """Energy distance between laws of finite regulated-measure signatures.

    Complex signatures are embedded in R^160 and divided by sqrt(80), fixing a
    dimension-independent scale.  The non-negative V-statistic is used.
    """
    a = np.asarray(left, dtype=complex)
    b = np.asarray(right, dtype=complex)
    if a.ndim != 2 or b.ndim != 2 or a.shape[1:] != b.shape[1:]:
        raise MeasureProtocolError("signature blocks must share feature dimension")
    if a.shape[1] != len(FOURIER_FREQUENCIES) or min(len(a), len(b)) < 2:
        raise MeasureProtocolError("signature blocks violate the frozen schema")
    scale = np.sqrt(len(FOURIER_FREQUENCIES))
    ar = np.concatenate([a.real, a.imag], axis=1) / scale
    br = np.concatenate([b.real, b.imag], axis=1) / scale

    def average_distance(x: np.ndarray, y: np.ndarray) -> float:
        return float(np.linalg.norm(x[:, None, :] - y[None, :, :], axis=2).mean())

    squared = (
        2.0 * average_distance(ar, br)
        - average_distance(ar, ar)
        - average_distance(br, br)
    )
    return float(np.sqrt(max(0.0, squared)))


def passes_s5(left: np.ndarray, right: np.ndarray) -> bool:
    return bool(
        mean_signature_distance(left, right) <= MAX_MEAN_SIGNATURE_DISTANCE
        and random_law_energy_distance(left, right)
        <= MAX_RANDOM_LAW_ENERGY_DISTANCE
    )


__all__ = [
    "BLOCKS_PER_TARGET",
    "CARDINALITIES",
    "CASES_PER_BLOCK",
    "FOURIER_FREQUENCIES",
    "MASS_TOLERANCE",
    "MAX_MEAN_SIGNATURE_DISTANCE",
    "MAX_RANDOM_LAW_ENERGY_DISTANCE",
    "MIN_ESS_FRACTION",
    "MIN_KISH_ESS",
    "MIN_PAIR_COVERAGE",
    "MIN_SELECTED_PAIRS",
    "SMEARING_EPSILON",
    "TARGET_SEED_BASES",
    "MeasureDiagnostics",
    "MeasureProtocolError",
    "fourier_signature",
    "gaussian_mollifier_density",
    "kish_effective_sample_size",
    "mean_signature_distance",
    "measure_diagnostics",
    "normalised_weights",
    "passes_s1_s6",
    "passes_s5",
    "preregistered_seed",
    "random_law_energy_distance",
    "uniform_pair_weights",
]
