"""Regressions for the Stage 5C primary invariant endpoint.

The universal one-scalar lower bound is an analytic topological statement and
is not claimed to be proved by finite tests.  These tests lock its premises,
the explicit two-vector construction, and executable falsifiers.
"""

import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analysis.stage5c_primary_invariant import (  # noqa: E402
    COMPONENT_BOUNDS,
    ambient_norm_squared,
    holomorphic_family,
    planted_classes,
    primary_endpoint,
    unnormalised_components,
)

SWAP = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)


def _vector(matrix):
    return primary_endpoint(matrix).as_vector()


def test_endpoint_is_real_and_invariant_under_the_full_basis_group():
    rng = np.random.default_rng(0)
    matrix = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    reference = _vector(matrix)
    assert reference.dtype == np.float64
    for _ in range(500):
        phases = np.diag(np.exp(1j * rng.uniform(0.0, 2.0 * np.pi, 2)))
        for basis in (phases, SWAP @ phases):
            moved = basis @ matrix @ basis.conj().T
            assert np.allclose(_vector(moved), reference, atol=1e-12)


def test_both_components_have_degree_two_and_endpoint_is_scale_invariant():
    rng = np.random.default_rng(1)
    matrix = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    raw = np.array(unnormalised_components(matrix))
    endpoint = _vector(matrix)
    for scale in (0.01, 3.7, 250.0):
        assert np.allclose(
            unnormalised_components(scale * matrix), raw * scale**2
        )
        assert np.isclose(
            ambient_norm_squared(scale * matrix),
            scale**2 * ambient_norm_squared(matrix),
        )
        assert np.allclose(_vector(scale * matrix), endpoint, atol=1e-10)


def test_component_bounds_hold_and_all_extrema_are_attained():
    rng = np.random.default_rng(2)
    lower = np.array([bound[0] for bound in COMPONENT_BOUNDS])
    upper = np.array([bound[1] for bound in COMPONENT_BOUNDS])
    for _ in range(20000):
        matrix = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
        vector = _vector(matrix)
        assert np.all(vector >= lower - 1e-9)
        assert np.all(vector <= upper + 1e-9)
    assert np.allclose(_vector(SWAP), [-1.0, 1.0])
    assert np.allclose(_vector(np.diag([1.0, -1.0])), [2.0, 0.0])
    assert np.allclose(_vector(np.array([[0.0, 1.0], [0.0, 0.0]])), [0.0, 1.0])


def test_invalid_or_vanishing_inputs_are_not_reported_as_endpoints():
    for bad in (
        np.zeros((2, 2), dtype=complex),
        np.zeros((3, 3), dtype=complex),
        np.array([[np.nan, 0.0], [0.0, 1.0]]),
    ):
        with pytest.raises(ValueError):
            primary_endpoint(bad)
    with pytest.raises(ValueError):
        primary_endpoint(
            1e-6 * np.eye(2, dtype=complex), minimum_norm_squared=1e-10
        )
    with pytest.raises(ValueError):
        primary_endpoint(np.eye(2), minimum_norm_squared=-1.0)


def test_five_registered_algebraic_classes_have_distinct_sign_patterns():
    classes = planted_classes()
    expected = {
        "sector_blind": (0, 0),
        "chiral_decoupled": (1, 0),
        "symmetric_diffusion": (-1, 1),
        "blind_jordan_degeneration": (0, 1),
        "chiral_triangular_degeneration": (1, 1),
    }
    observed = {}
    for name, matrix in classes.items():
        vector = _vector(matrix)
        observed[name] = tuple(int(np.sign(x)) for x in vector)
    assert observed == expected
    for first, second in combinations(classes, 2):
        assert not np.allclose(_vector(classes[first]), _vector(classes[second]))


def test_each_selected_coordinate_is_indispensable_for_this_pair():
    classes = planted_classes()
    blind = _vector(classes["sector_blind"])
    chiral = _vector(classes["chiral_decoupled"])
    jordan = _vector(classes["blind_jordan_degeneration"])
    assert np.isclose(blind[1], chiral[1])  # drop first: blind == chiral
    assert np.isclose(blind[0], jordan[0])  # drop second: blind == Jordan


def test_original_two_branch_p1_is_false_and_stays_falsified():
    """Q/N^2-S/N^2 has opposite signs on chiral and Jordan branches."""
    scalar = 1.3
    for parameter in (1e-6, 0.01, 0.4, 2.0):
        chiral = np.diag([scalar, scalar + parameter]).astype(complex)
        jordan = scalar * np.eye(2) + np.array(
            [[0.0, parameter], [0.0, 0.0]], dtype=complex
        )
        assert _vector(chiral)[0] > 0.0
        assert _vector(jordan)[0] == 0.0
        # The old three-vector scalar Q/N^2-S/N^2 is positive vs negative.
        old_chiral = abs(chiral[0, 0] - chiral[1, 1]) ** 2 / ambient_norm_squared(chiral)
        old_jordan = -abs(jordan[0, 1]) ** 2 / ambient_norm_squared(jordan)
        assert old_chiral > 0.0 > old_jordan


def test_three_nonblind_branches_share_the_blind_limit():
    """Executable premises only; the star-to-line no-go is proved analytically."""
    scalar = 1.3
    origin = _vector(scalar * np.eye(2))
    for parameter in (1e-2, 1e-4, 1e-6):
        matrices = (
            np.diag([scalar, scalar + parameter]),
            scalar * np.eye(2) + np.array([[0.0, parameter], [0.0, 0.0]]),
            np.array([[scalar, parameter], [parameter, scalar]]),
        )
        assert all(np.linalg.norm(_vector(matrix) - origin) < 2.0 * parameter for matrix in matrices)


def test_holomorphic_family_fails_on_both_degeneration_pairs():
    classes = planted_classes()
    for ideal, degenerate in (
        ("sector_blind", "blind_jordan_degeneration"),
        ("chiral_decoupled", "chiral_triangular_degeneration"),
    ):
        assert np.allclose(
            holomorphic_family(classes[ideal]), holomorphic_family(classes[degenerate])
        )
        assert not np.allclose(_vector(classes[ideal]), _vector(classes[degenerate]))


def test_absolute_product_uses_the_unique_nonnegative_branch():
    matrix = np.array([[0.3 + 0.2j, 1.0 + 2.0j], [-0.7 + 0.4j, -0.1j]])
    first, second = unnormalised_components(matrix)
    a, b, c, d = matrix.ravel()
    assert np.isclose(first, abs(a - d) ** 2 - 2.0 * np.sqrt(abs((b * c) * np.conj(b * c))))
    assert np.isclose(second, abs(b) ** 2 + abs(c) ** 2)
