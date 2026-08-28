"""Algebraic regressions for the Stage 5C D.1-3 observable-contract draft.

These tests constrain evaluator typing only.  They define no candidate kernel.
"""

import numpy as np


def test_sector_swap_does_not_make_trace_and_determinant_complete():
    """An S2-invariant scalar can distinguish matrices with equal tr and det."""
    zero = np.zeros((2, 2), dtype=complex)
    nilpotent = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)
    swap = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)

    assert np.trace(zero) == np.trace(nilpotent)
    assert np.linalg.det(zero) == np.linalg.det(nilpotent)

    def swap_invariant(matrix):
        return matrix[0, 1] + matrix[1, 0]

    assert swap_invariant(swap @ nilpotent @ swap) == swap_invariant(nilpotent)
    assert swap_invariant(zero) != swap_invariant(nilpotent)


def test_cross_fiber_trace_is_not_invariant_under_independent_endpoint_bases():
    """Bx M By^-1 is not a similarity transformation when Bx != By."""
    matrix = np.array([[1.0, 2.0], [3.0, 4.0]], dtype=complex)
    basis_x = np.array([[2.0, 0.0], [0.0, 1.0]], dtype=complex)
    basis_y = np.eye(2, dtype=complex)
    transformed = basis_x @ matrix @ np.linalg.inv(basis_y)

    assert np.trace(transformed) != np.trace(matrix)
    assert np.linalg.det(transformed) != np.linalg.det(matrix)

    global_similarity = basis_x @ matrix @ np.linalg.inv(basis_x)
    assert np.isclose(np.trace(global_similarity), np.trace(matrix))
    assert np.isclose(np.linalg.det(global_similarity), np.linalg.det(matrix))
