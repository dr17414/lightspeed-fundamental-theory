"""Stage 5C primary invariant endpoint ``I_G``.

Evaluator-side algebra only.  No candidate kernel is defined, evaluated, or
observed here.  The endpoint is the fixed two-component real invariant vector
documented in ``docs/STAGE5C_D1_3_PRIMARY_INVARIANT.md``.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

COMPONENT_NAMES = ("split_minus_coupling", "off_diagonal_power")
COMPONENT_BOUNDS = ((-1.0, 2.0), (0.0, 1.0))
# Declared evaluator convention: this value is not derived from the invariant
# algebra.  Changing it is a protocol amendment, not a corrective bug fix.
COUPLING_COEFFICIENT = 2.0


@dataclass(frozen=True)
class InvariantEndpoint:
    """The primary real invariant vector and its normalising squared norm."""

    split_minus_coupling: float
    off_diagonal_power: float
    ambient_norm_squared: float

    def as_vector(self) -> np.ndarray:
        return np.array(
            [self.split_minus_coupling, self.off_diagonal_power], dtype=float
        )


def _validated_matrix(matrix: np.ndarray) -> np.ndarray:
    value = np.asarray(matrix, dtype=complex)
    if value.shape != (2, 2):
        raise ValueError("primary endpoint requires one finite 2x2 matrix")
    if not np.all(np.isfinite(value.real)) or not np.all(np.isfinite(value.imag)):
        raise ValueError("primary endpoint requires one finite 2x2 matrix")
    return value


def ambient_norm_squared(matrix: np.ndarray) -> float:
    """Return the committed G-invariant Frobenius norm squared."""
    value = _validated_matrix(matrix)
    return float(np.vdot(value, value).real)


def unnormalised_components(matrix: np.ndarray) -> tuple[float, float]:
    """Return ``Q - 2|W|`` and ``S``; both are homogeneous of degree two."""
    value = _validated_matrix(matrix)
    a, b, c, d = value[0, 0], value[0, 1], value[1, 0], value[1, 1]
    q = abs(a - d) ** 2
    s = abs(b) ** 2 + abs(c) ** 2
    abs_w = abs(b * c)
    return float(q - COUPLING_COEFFICIENT * abs_w), float(s)


def primary_endpoint(
    matrix: np.ndarray, *, minimum_norm_squared: float = 0.0
) -> InvariantEndpoint:
    """Evaluate ``I_G(M)``.

    ``minimum_norm_squared`` is a pre-registered non-triviality threshold, not
    a fit parameter.  At or below it the ratio is not reported and the endpoint
    gate is INCONCLUSIVE.  C3b's separate exact-zero verdict is unchanged.
    """
    if not np.isfinite(minimum_norm_squared) or minimum_norm_squared < 0.0:
        raise ValueError("minimum_norm_squared must be finite and non-negative")
    value = _validated_matrix(matrix)
    norm_squared = ambient_norm_squared(value)
    if norm_squared <= minimum_norm_squared:
        raise ValueError(
            "ambient norm is at or below the non-triviality gate: endpoint undefined"
        )
    first, second = unnormalised_components(value)
    return InvariantEndpoint(
        split_minus_coupling=first / norm_squared,
        off_diagonal_power=second / norm_squared,
        ambient_norm_squared=norm_squared,
    )


def holomorphic_family(matrix: np.ndarray) -> np.ndarray:
    """Disqualified holomorphic-only family, retained only as a falsifier."""
    value = _validated_matrix(matrix)
    a, b, c, d = value[0, 0], value[0, 1], value[1, 0], value[1, 1]
    return np.array([a + d, a * d, b * c])


def planted_classes(
    scalar: float = 1.3,
    left_mode: float = 1.0,
    right_mode: float = 2.4,
    off_diagonal: float = 0.8,
    diffusion: float = 0.6,
) -> dict[str, np.ndarray]:
    """Five currently registered algebraic planted classes.

    This list does not discharge the still-unresolved wrong-direction control.
    """
    identity = np.eye(2, dtype=complex)
    upper = np.array([[0.0, off_diagonal], [0.0, 0.0]], dtype=complex)
    return {
        "sector_blind": scalar * identity,
        "chiral_decoupled": np.diag([left_mode, right_mode]).astype(complex),
        "symmetric_diffusion": np.array(
            [[scalar, diffusion], [diffusion, scalar]], dtype=complex
        ),
        "blind_jordan_degeneration": scalar * identity + upper,
        "chiral_triangular_degeneration": (
            np.diag([left_mode, right_mode]).astype(complex) + upper
        ),
    }


def _source_of_record() -> None:
    classes = planted_classes()
    print("class                          first      second  sign pattern")
    for name, matrix in classes.items():
        vector = primary_endpoint(matrix).as_vector()
        pattern = "".join("+" if x > 1e-12 else "-" if x < -1e-12 else "0" for x in vector)
        print(f"{name:30s} {vector[0]:10.6f} {vector[1]:10.6f}  {pattern}")
    print("component bounds:", COMPONENT_BOUNDS)


if __name__ == "__main__":
    _source_of_record()
