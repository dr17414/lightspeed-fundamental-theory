"""Candidate-independent evaluator primitives for the Stage 5C C3b contract.

The value-level blind set is the rank-one Segre cone in
End(F) (x) C^D.  This module computes only its weighted Frobenius distance.
It does not define a candidate kernel and cannot replace the required
program-level source/capability audit.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json

import numpy as np


FIBER_SLOTS = 4


@dataclass(frozen=True)
class BlindDistanceStatistics:
    pair_dimension: int
    singular_values: tuple[float, float, float, float]
    weighted_norm: float
    blind_distance: float
    rho: float | None
    rho_upper_bound: float
    exact_zero: bool
    leading_degenerate: bool


def fiber_action_row_major(basis: np.ndarray) -> np.ndarray:
    """Return the action on slots (UU, UV, VU, VV).

    For row-major vectorisation,
    vec_row(B A B^dagger) = (B kron conjugate(B)) vec_row(A).
    """

    basis = np.asarray(basis, dtype=complex)
    if basis.shape != (2, 2):
        raise ValueError("basis must have shape (2, 2)")
    return np.kron(basis, basis.conj())


def rho_upper_bound(pair_dimension: int) -> float:
    """Sharp nonzero-kernel bound sqrt(1 - 1/min(4, D))."""

    if pair_dimension < 1:
        raise ValueError("pair domain must be nonempty")
    rank_bound = min(FIBER_SLOTS, pair_dimension)
    return float(np.sqrt(1.0 - 1.0 / rank_bound))


def weighted_kernel_matrix(
    kernel: np.ndarray, pair_weights: np.ndarray | None = None
) -> np.ndarray:
    """Apply the authorised separable pair weighting to a 4 x D kernel."""

    kernel = np.asarray(kernel, dtype=complex)
    if kernel.ndim != 2 or kernel.shape[0] != FIBER_SLOTS:
        raise ValueError("kernel must have shape (4, D)")
    if kernel.shape[1] < 1:
        raise ValueError("pair domain must be nonempty")
    if not np.all(np.isfinite(kernel)):
        raise ValueError("kernel entries must be finite")
    if pair_weights is None:
        return kernel.copy()
    weights = np.asarray(pair_weights, dtype=float)
    if weights.shape != (kernel.shape[1],):
        raise ValueError("pair_weights must have shape (D,)")
    if not np.all(np.isfinite(weights)) or np.any(weights <= 0.0):
        raise ValueError("pair_weights must be finite and strictly positive")
    return kernel * np.sqrt(weights)[None, :]


def blind_statistics(
    kernel: np.ndarray,
    pair_weights: np.ndarray | None = None,
    *,
    degeneracy_rtol: float = 1e-12,
    degeneracy_atol: float = 1e-14,
) -> BlindDistanceStatistics:
    """Compute the unique distance statistics, never a best factorisation."""

    weighted = weighted_kernel_matrix(kernel, pair_weights)
    raw_values = np.linalg.svd(weighted, compute_uv=False)
    values = np.zeros(FIBER_SLOTS, dtype=float)
    values[: raw_values.size] = raw_values
    total_squared = float(np.sum(values**2))
    distance_squared = float(np.sum(values[1:] ** 2))
    norm = float(np.sqrt(total_squared))
    distance = float(np.sqrt(max(0.0, distance_squared)))
    exact_zero = total_squared == 0.0
    ratio = None if exact_zero else float(distance / norm)
    leading_degenerate = bool(
        not exact_zero
        and values.size > 1
        and np.isclose(
            values[0], values[1], rtol=degeneracy_rtol, atol=degeneracy_atol
        )
    )
    return BlindDistanceStatistics(
        pair_dimension=weighted.shape[1],
        singular_values=tuple(float(value) for value in values),
        weighted_norm=norm,
        blind_distance=distance,
        rho=ratio,
        rho_upper_bound=rho_upper_bound(weighted.shape[1]),
        exact_zero=exact_zero,
        leading_degenerate=leading_degenerate,
    )


def blind_distance(kernel: np.ndarray, pair_weights: np.ndarray | None = None) -> float:
    return blind_statistics(kernel, pair_weights).blind_distance


def rho(kernel: np.ndarray, pair_weights: np.ndarray | None = None) -> float:
    """Return rho for a nonzero kernel; exact zero needs an explicit FAIL branch."""

    result = blind_statistics(kernel, pair_weights)
    if result.rho is None:
        raise ValueError("rho is undefined for the exact-zero blind kernel")
    return result.rho


def _source_of_record_payload() -> dict[str, object]:
    """Deterministic evaluator self-check; contains no candidate construction."""

    rank_one = np.outer(
        np.array([1.0, 2.0j, -0.5, 3.0], dtype=complex),
        np.linspace(0.5, 2.0, 8, dtype=float),
    )
    balanced = np.zeros((4, 8), dtype=complex)
    balanced[0, :4] = 1.0
    balanced[3, 4:] = 1.0
    return {
        "contract": "C3b rank-one blind-variety distance",
        "scope": "evaluation-only; source/capability audit remains independent",
        "rank_one": asdict(blind_statistics(rank_one)),
        "balanced_rank_two": asdict(blind_statistics(balanced)),
    }


if __name__ == "__main__":
    print(json.dumps(_source_of_record_payload(), indent=2, sort_keys=True))
