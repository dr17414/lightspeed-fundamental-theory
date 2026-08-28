"""Regressions for the Stage 5C section 1.4 basis-group analysis.

Evaluator-side algebra only. No candidate kernel is defined here.
"""

from itertools import product

import numpy as np


SWAP = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)


def s2_family(m):
    a, b, c, d = m[0, 0], m[0, 1], m[1, 0], m[1, 1]
    return (a + d, a * d, b + c, b * c, (a - d) * (b - c))


def monomial_family(m):
    a, b, c, d = m[0, 0], m[0, 1], m[1, 0], m[1, 1]
    return (a + d, a * d, b * c)


def discriminant(m):
    return np.trace(m) ** 2 - 4.0 * np.linalg.det(m)


def _random_matrix(rng):
    return rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))


def _same_s2_orbit(first, second):
    return np.array_equal(first, second) or np.array_equal(SWAP @ first @ SWAP, second)


def test_proposition_2_s2_family_is_invariant():
    rng = np.random.default_rng(0)
    for _ in range(2000):
        matrix = _random_matrix(rng)
        assert np.allclose(s2_family(SWAP @ matrix @ SWAP), s2_family(matrix))


def test_proposition_2_s2_family_separates_a_finite_exact_grid():
    """Unlike random collision counting, this deliberately creates collisions."""
    buckets = {}
    for entries in product((-1, 0, 1), repeat=4):
        matrix = np.array(entries, dtype=complex).reshape(2, 2)
        key = s2_family(matrix)
        for previous in buckets.get(key, []):
            assert _same_s2_orbit(previous, matrix)
        buckets.setdefault(key, []).append(matrix)


def test_proposition_2_generator_relation_including_degenerate_cases():
    rng = np.random.default_rng(1)
    cases = [
        np.zeros((2, 2), dtype=complex),
        np.eye(2, dtype=complex),
        np.array([[0, 1], [0, 0]], dtype=complex),
    ] + [_random_matrix(rng) for _ in range(100)]
    for matrix in cases:
        sa, pa, sb, pb, q = s2_family(matrix)
        assert np.allclose(q**2, (sa**2 - 4 * pa) * (sb**2 - 4 * pb))


def test_proposition_3_monomial_family_is_invariant_for_compact_and_noncompact_tori():
    rng = np.random.default_rng(2)
    for _ in range(1000):
        matrix = _random_matrix(rng)
        modulus = np.exp(rng.uniform(-3.0, 3.0))
        phase = np.exp(1j * rng.uniform(0.0, 2.0 * np.pi))
        scale = np.diag([modulus * phase, 1.0]).astype(complex)
        for basis in (scale, SWAP @ scale):
            conjugated = basis @ matrix @ np.linalg.inv(basis)
            assert np.allclose(monomial_family(conjugated), monomial_family(matrix))


def test_trace_and_determinant_are_incomplete_for_the_monomial_group():
    first = np.array([[1.0, 0.0], [0.0, 2.0]], dtype=complex)
    second = np.array([[0.0, 1.0], [-2.0, 3.0]], dtype=complex)
    assert np.isclose(np.trace(first), np.trace(second))
    assert np.isclose(np.linalg.det(first), np.linalg.det(second))
    assert not np.isclose(first[0, 1] * first[1, 0], second[0, 1] * second[1, 0])


def test_monomial_holomorphic_family_cannot_separate_orbit_closure_degenerations():
    blind = 1.7 * np.eye(2, dtype=complex)
    blind_jordan = blind + np.array([[0.0, 0.8], [0.0, 0.0]], dtype=complex)
    chiral = np.diag([1.0, 2.4]).astype(complex)
    chiral_triangular = chiral + np.array([[0.0, 0.8], [0.0, 0.0]], dtype=complex)
    assert np.allclose(monomial_family(blind), monomial_family(blind_jordan))
    assert np.allclose(monomial_family(chiral), monomial_family(chiral_triangular))
    assert not np.allclose(s2_family(blind), s2_family(blind_jordan))
    assert not np.allclose(s2_family(chiral), s2_family(chiral_triangular))


def test_compact_real_invariant_separates_zero_from_nilpotent():
    zero = np.zeros((2, 2), dtype=complex)
    nilpotent = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)

    def off_diagonal_power(matrix):
        return abs(matrix[0, 1]) ** 2 + abs(matrix[1, 0]) ** 2

    rng = np.random.default_rng(3)
    for _ in range(500):
        phases = np.diag(np.exp(1j * rng.uniform(0, 2 * np.pi, 2)))
        for basis in (phases, SWAP @ phases):
            rotated = basis @ nilpotent @ np.conjugate(basis).T
            assert np.isclose(off_diagonal_power(rotated), off_diagonal_power(nilpotent))
    assert not np.isclose(off_diagonal_power(zero), off_diagonal_power(nilpotent))


def test_noncompact_orbit_closes_on_zero_and_forbids_a_continuous_positive_invariant_norm():
    nilpotent = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)
    for scale in (1e-2, 1e-5, 1e-9):
        basis = np.diag([scale, 1.0]).astype(complex)
        moved = basis @ nilpotent @ np.linalg.inv(basis)
        assert np.allclose(moved, scale * nilpotent)
        assert np.allclose(monomial_family(moved), monomial_family(nilpotent))
        assert np.linalg.norm(moved) < 2.0 * scale
    # Any continuous invariant norm would be constant along this orbit yet
    # converge to its value at zero, contradicting positive definiteness.


def test_local_endpoint_bases_give_relative_determinant_but_not_relative_trace():
    matrix = np.array([[2.0, 3.0], [5.0, 7.0]], dtype=complex)
    ax, bx, ay, by = 2.0, 3.0, 5.0, 7.0
    left, right = np.diag([ax, bx]), np.diag([ay, by])
    transformed = left @ matrix @ np.linalg.inv(right)
    weight = ax * bx / (ay * by)

    assert np.isclose(transformed[0, 0] * transformed[1, 1], weight * matrix[0, 0] * matrix[1, 1])
    assert np.isclose(transformed[0, 1] * transformed[1, 0], weight * matrix[0, 1] * matrix[1, 0])
    assert np.isclose(
        transformed[0, 0] * transformed[1, 1] / (transformed[0, 1] * transformed[1, 0]),
        matrix[0, 0] * matrix[1, 1] / (matrix[0, 1] * matrix[1, 0]),
    )
    assert np.isclose(np.linalg.det(transformed), weight * np.linalg.det(matrix))
    # A relative invariant would have one matrix-independent character. E11
    # and E22 instead receive different weights.
    assert not np.isclose(ax / ay, bx / by)


def test_central_scalars_are_in_the_kernel_of_similarity_action():
    rng = np.random.default_rng(4)
    matrix = _random_matrix(rng)
    for scalar in (2.0, -1.3j, 0.7 + 0.2j):
        basis = scalar * np.eye(2, dtype=complex)
        assert np.allclose(basis @ matrix @ np.linalg.inv(basis), matrix)


def test_passive_gl_change_preserves_moved_sector_projectors_but_not_fixed_slots():
    pu = np.diag([1.0, 0.0]).astype(complex)
    pv = np.diag([0.0, 1.0]).astype(complex)
    mixing = np.array([[1.0, 1.0], [0.0, 1.0]], dtype=complex)
    moved_u = mixing @ pu @ np.linalg.inv(mixing)
    moved_v = mixing @ pv @ np.linalg.inv(mixing)
    assert np.allclose(moved_u @ moved_u, moved_u)
    assert np.allclose(moved_v @ moved_v, moved_v)
    assert np.allclose(moved_u + moved_v, np.eye(2))
    assert np.allclose(moved_u @ moved_v, np.zeros((2, 2)))
    assert not (
        (np.allclose(moved_u, pu) and np.allclose(moved_v, pv))
        or (np.allclose(moved_u, pv) and np.allclose(moved_v, pu))
    )


def test_monomial_group_preserves_the_unordered_fixed_sector_projectors():
    pu = np.diag([1.0, 0.0]).astype(complex)
    pv = np.diag([0.0, 1.0]).astype(complex)
    for basis in (np.diag([2.0, 3.0]), SWAP @ np.diag([2.0, 3.0])):
        moved = [basis @ projector @ np.linalg.inv(basis) for projector in (pu, pv)]
        assert all(any(np.allclose(item, target) for target in (pu, pv)) for item in moved)


def test_discriminant_is_only_a_sufficient_non_scalar_witness():
    blind = np.diag([1.7, 1.7]).astype(complex)
    chiral = np.diag([1.0, 2.4]).astype(complex)
    nilpotent = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)
    assert np.isclose(discriminant(blind), 0.0)
    assert np.isclose(discriminant(chiral), (1.0 - 2.4) ** 2)
    assert not np.allclose(chiral, np.trace(chiral) / 2.0 * np.eye(2))
    assert np.isclose(discriminant(nilpotent), 0.0)
    assert not np.allclose(nilpotent, np.trace(nilpotent) / 2.0 * np.eye(2))
