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

# 6a-S operational gates: d_mean uses an equivalence margin, while d_law is a
# gross-breakage tripwire.  Both are fixed before the reserved streams are
# touched and apply to every selector, target, N, and pair of independent
# blocks.  Neither is a theorem of full weak convergence or law stability.
MAX_MEAN_SIGNATURE_DISTANCE = 0.20
MAX_RANDOM_LAW_ENERGY_DISTANCE = 0.20
MIN_SELECTED_PAIRS = 32
MIN_PAIR_COVERAGE = 0.005
MIN_KISH_ESS = 32.0
MIN_ESS_FRACTION = 0.95
MASS_TOLERANCE = 1.0e-12

# One representative from every conjugate pair in the first non-zero Fourier
# shell on the dimensionless unit 4-cube.  For real measures F(-w)=conj(F(w)),
# so this is 40 complex / 80 real degrees of freedom, with no duplicated data.
def _canonical_half_shell(index: tuple[int, ...]) -> bool:
    return next(component for component in index if component != 0) > 0


FOURIER_FREQUENCIES = np.asarray(
    [
        tuple(2.0 * np.pi * k for k in index)
        for index in product((-1, 0, 1), repeat=4)
        if index != (0, 0, 0, 0) and _canonical_half_shell(index)
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
    for name, value in (("n_index", n_index), ("block", block), ("case", case)):
        if isinstance(value, (bool, np.bool_)) or not isinstance(
            value, (int, np.integer)
        ):
            raise MeasureProtocolError(f"{name} must be a non-boolean integer")
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
) -> np.ndarray:
    """Evaluate the fixed mass-one Gaussian regulator R_epsilon nu on R^4."""
    query = np.asarray(query_points, dtype=float)
    atoms = _validated_pair_coordinates(pair_coordinates)
    weights = np.asarray(probability_weights, dtype=float)
    if query.ndim != 2 or query.shape[1:] != (4,) or not np.all(np.isfinite(query)):
        raise MeasureProtocolError("query points must be one finite (q,4) array")
    if weights.shape != (atoms.shape[0],) or np.any(weights < 0.0):
        raise MeasureProtocolError("one non-negative weight is required per atom")
    epsilon = SMEARING_EPSILON
    squared = np.sum((query[:, None, :] - atoms[None, :, :]) ** 2, axis=2)
    coefficient = (2.0 * np.pi * epsilon**2) ** -2
    return coefficient * (np.exp(-squared / (2.0 * epsilon**2)) @ weights)


def fourier_signature(
    pair_coordinates: np.ndarray,
    probability_weights: np.ndarray,
) -> np.ndarray:
    """Finite spectral signature of the regulated probability measure."""
    atoms = _validated_pair_coordinates(pair_coordinates)
    weights = np.asarray(probability_weights, dtype=float)
    if weights.shape != (atoms.shape[0],) or np.any(weights < 0.0):
        raise MeasureProtocolError("one non-negative weight is required per atom")
    if abs(float(weights.sum()) - 1.0) > MASS_TOLERANCE:
        raise MeasureProtocolError("Fourier signature requires probability weights")
    epsilon = SMEARING_EPSILON
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


def _real_signature_embedding(signatures: np.ndarray) -> np.ndarray:
    value = np.asarray(signatures, dtype=complex)
    return np.concatenate([value.real, value.imag], axis=1) / np.sqrt(
        len(FOURIER_FREQUENCIES)
    )


def random_law_energy_statistic(left: np.ndarray, right: np.ndarray) -> float:
    """Signed unbiased U-statistic for the energy distance squared.

    The finite-sample value may be negative.  Keeping that sign is essential:
    including the within-block diagonal terms would create a positive null bias
    driven by per-causet dispersion and selected-pair count.
    """
    a = np.asarray(left, dtype=complex)
    b = np.asarray(right, dtype=complex)
    if a.ndim != 2 or b.ndim != 2 or a.shape[1:] != b.shape[1:]:
        raise MeasureProtocolError("signature blocks must share feature dimension")
    if a.shape[1] != len(FOURIER_FREQUENCIES) or min(len(a), len(b)) < 2:
        raise MeasureProtocolError("signature blocks violate the frozen schema")
    ar = _real_signature_embedding(a)
    br = _real_signature_embedding(b)

    cross = float(
        np.linalg.norm(ar[:, None, :] - br[None, :, :], axis=2).mean()
    )

    def off_diagonal_average(x: np.ndarray) -> float:
        distances = np.linalg.norm(x[:, None, :] - x[None, :, :], axis=2)
        return float(distances.sum() / (len(x) * (len(x) - 1)))

    return 2.0 * cross - off_diagonal_average(ar) - off_diagonal_average(br)


def random_law_energy_distance(left: np.ndarray, right: np.ndarray) -> float:
    """Non-negative reporting transform of the signed U-statistic."""
    return float(np.sqrt(max(0.0, random_law_energy_statistic(left, right))))


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
    "random_law_energy_statistic",
    "uniform_pair_weights",
]
