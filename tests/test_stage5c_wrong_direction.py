"""Regressions for the candidate-independent wrong-direction E3 boundary.

The genuine wrong-support intervention is still PENDING because its typed
selector object does not exist.  These tests lock only the completed algebraic
boundary and executable falsifiers; they do not invent that missing object.
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analysis.stage5c_primary_invariant import (  # noqa: E402
    planted_classes,
    primary_endpoint,
)

SWAP = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
LEFT_MODE, RIGHT_MODE = 1.0, 2.4


def _vector(matrix):
    return primary_endpoint(matrix).as_vector()


def _stress_witnesses():
    """Non-adopted matrices: algebraic stress witnesses, not E3 controls."""
    return {
        "sector_transposing": np.array(
            [[0.0, LEFT_MODE], [RIGHT_MODE, 0.0]], dtype=complex
        ),
        "co_propagating": np.array(
            [[LEFT_MODE, 0.0], [RIGHT_MODE, 0.0]], dtype=complex
        ),
    }


def test_global_sector_swap_is_gauge_for_every_registered_class():
    for matrix in planted_classes().values():
        assert np.allclose(_vector(SWAP @ matrix @ SWAP), _vector(matrix), atol=1e-12)


def test_chiral_orbit_is_exactly_the_two_sector_orderings():
    chiral = np.diag([LEFT_MODE, RIGHT_MODE]).astype(complex)
    expected = (chiral, SWAP @ chiral @ SWAP)
    for first_phase, second_phase in ((0.0, 0.0), (0.3, -1.7), (2.1, 0.8)):
        phases = np.diag(np.exp(1j * np.array([first_phase, second_phase])))
        assert np.allclose(phases @ chiral @ phases.conj().T, expected[0])
        moved = (SWAP @ phases) @ chiral @ (SWAP @ phases).conj().T
        assert np.allclose(moved, expected[1])
    assert not np.allclose(expected[0], expected[1])


def test_outside_orbit_is_not_sufficient_for_endpoint_separation():
    triangular = np.array([[1.0, 0.9], [0.0, 1j]], dtype=complex)
    co_propagating = np.array([[np.sqrt(2.0), 0.0], [0.9, 0.0]], dtype=complex)
    # Monomial conjugation preserves the unordered multiset of diagonal entries.
    assert sorted(np.diag(triangular), key=str) != sorted(
        np.diag(co_propagating), key=str
    )
    assert np.allclose(_vector(triangular), _vector(co_propagating), atol=1e-12)


def test_collision_value_matches_the_registered_falsifier():
    triangular = np.array([[1.0, 0.9], [0.0, 1j]], dtype=complex)
    assert np.allclose(_vector(triangular), [0.7117437722419929, 0.2882562277580071])


def test_positive_real_formula_is_exact_but_only_pairwise():
    for left, right, off_diagonal in (
        (1.0, 2.4, 0.8),
        (0.5, 3.0, 1.5),
        (2.0, 2.1, 0.2),
    ):
        triangular = np.array([[left, off_diagonal], [0.0, right]], dtype=complex)
        norm_squared = float(np.vdot(triangular, triangular).real)
        expected_sum = 1.0 - 2.0 * np.real(left * np.conj(right)) / norm_squared
        assert np.isclose(_vector(triangular).sum(), expected_sum)
        assert expected_sum < 1.0


def test_co_propagating_endpoint_components_sum_to_one():
    for left, right in ((1.0, 2.4), (0.5, 3.0), (2.0, 2.1)):
        matrix = np.array([[left, 0.0], [right, 0.0]], dtype=complex)
        assert np.isclose(_vector(matrix).sum(), 1.0)


def test_stress_witnesses_are_not_silently_registered_as_planted_classes():
    registered = set(planted_classes())
    proposed = set(_stress_witnesses())
    assert proposed.isdisjoint(registered)
    assert registered == {
        "sector_blind",
        "chiral_decoupled",
        "symmetric_diffusion",
        "blind_jordan_degeneration",
        "chiral_triangular_degeneration",
    }
