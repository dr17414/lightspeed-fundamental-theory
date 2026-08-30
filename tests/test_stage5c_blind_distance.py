"""Regressions for the C3b blind-variety distance contract.

The value-level blind set B_1 = {A (x) f} is the rank-one Segre cone, not a
linear subspace.  These tests call the evaluator source-of-record directly;
they do not define a candidate kernel.
"""

import numpy as np

from analysis.stage5c_blind_distance import (
    blind_distance,
    blind_statistics,
    fiber_action_row_major,
    rho,
    rho_upper_bound,
)


SWAP = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)


def _random_kernel(rng, pairs=120):
    return rng.normal(size=(4, pairs)) + 1j * rng.normal(size=(4, pairs))


def test_c1_distance_equals_the_best_rank_one_residual():
    rng = np.random.default_rng(0)
    kernel = _random_kernel(rng)
    best = np.inf
    for _ in range(3000):
        direction = rng.normal(size=4) + 1j * rng.normal(size=4)
        direction /= np.linalg.norm(direction)
        factor = direction.conj() @ kernel
        best = min(best, float(np.linalg.norm(kernel - np.outer(direction, factor))))
    analytic = blind_distance(kernel)
    assert analytic <= best + 1e-9
    assert best - analytic < 0.05 * analytic


def test_rank_one_members_of_the_blind_variety_have_zero_distance():
    rng = np.random.default_rng(1)
    for _ in range(200):
        endomorphism = rng.normal(size=4) + 1j * rng.normal(size=4)
        factor = rng.normal(size=120) + 1j * rng.normal(size=120)
        assert blind_distance(np.outer(endomorphism, factor)) < 1e-10


def test_row_major_action_matches_direct_conjugation():
    rng = np.random.default_rng(2)
    for _ in range(100):
        matrix = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
        phases = np.diag(np.exp(1j * rng.uniform(0.0, 2.0 * np.pi, 2)))
        for basis in (phases, SWAP @ phases):
            direct = (basis @ matrix @ basis.conj().T).reshape(-1, order="C")
            represented = fiber_action_row_major(basis) @ matrix.reshape(-1, order="C")
            assert np.allclose(represented, direct)


def test_c2_rho_is_invariant_under_basis_group_and_weighted_relabelling():
    rng = np.random.default_rng(3)
    kernel = _random_kernel(rng)
    weights = rng.uniform(0.5, 2.0, kernel.shape[1])
    reference = rho(kernel, weights)
    for _ in range(200):
        phases = np.diag(np.exp(1j * rng.uniform(0.0, 2.0 * np.pi, 2)))
        for basis in (phases, SWAP @ phases):
            assert np.isclose(
                rho(fiber_action_row_major(basis) @ kernel, weights), reference
            )
    permutation = rng.permutation(kernel.shape[1])
    assert np.isclose(rho(kernel[:, permutation], weights[permutation]), reference)


def test_separable_pair_weights_preserve_the_blind_variety():
    rng = np.random.default_rng(4)
    endomorphism = rng.normal(size=4)
    factor = rng.normal(size=120)
    weights = rng.uniform(0.5, 2.0, 120)
    assert blind_distance(np.outer(endomorphism, factor), weights) < 1e-10


def test_left_and_right_actions_preserve_rank_but_entrywise_weighting_need_not():
    rng = np.random.default_rng(5)
    blind = np.outer(rng.normal(size=4), rng.normal(size=120))
    left = rng.normal(size=(4, 4))
    right = rng.normal(size=(120, 120))
    assert blind_distance(left @ blind) < 1e-9
    assert blind_distance(blind @ right) < 1e-9

    nonseparable = blind.copy()
    nonseparable[0] *= np.linspace(1.0, 5.0, 120)
    assert blind_distance(nonseparable) > 1e-6


def test_rho_upper_bound_depends_on_pair_dimension_and_is_attained():
    for pair_dimension in (1, 2, 3, 8):
        rank_bound = min(4, pair_dimension)
        kernel = np.zeros((4, pair_dimension), dtype=complex)
        for index in range(rank_bound):
            kernel[index, index] = 1.0
        expected = np.sqrt(1.0 - 1.0 / rank_bound)
        assert np.isclose(rho_upper_bound(pair_dimension), expected)
        assert np.isclose(rho(kernel), expected)


def test_exact_zero_is_identified_as_blind_and_rho_is_not_silently_defined():
    kernel = np.zeros((4, 12), dtype=complex)
    result = blind_statistics(kernel)
    assert result.exact_zero
    assert result.blind_distance == 0.0
    assert result.rho is None
    try:
        rho(kernel)
    except ValueError as error:
        assert "exact-zero blind kernel" in str(error)
    else:
        raise AssertionError("exact zero must take the explicit C3b FAIL branch")


def test_degenerate_leading_singular_values_leave_distance_ratio_well_defined():
    kernel = np.zeros((4, 120), dtype=complex)
    kernel[0, :50] = 1.0
    kernel[1, 50:100] = 1.0
    result = blind_statistics(kernel)
    assert result.leading_degenerate
    assert np.isclose(result.rho, 1.0 / np.sqrt(2.0))


def test_decoupled_reference_value_matches_the_delivered_gram_formula():
    rng = np.random.default_rng(6)
    for ratio in (1.0, 0.5, 0.2):
        left = rng.normal(size=400)
        right = ratio * rng.normal(size=400)
        kernel = np.zeros((4, 400))
        kernel[0], kernel[3] = left, right
        gram = np.array([[left @ left, left @ right], [right @ left, right @ right]])
        eigenvalues = np.sort(np.linalg.eigvalsh(gram))
        predicted = np.sqrt(eigenvalues[0] / np.sum(eigenvalues))
        assert np.isclose(rho(kernel), predicted, atol=1e-9)


def test_orthogonal_balanced_sectors_give_one_over_root_two():
    rng = np.random.default_rng(7)
    left = rng.normal(size=400)
    raw = rng.normal(size=400)
    right = raw - (left @ raw) / (left @ left) * left
    left /= np.linalg.norm(left)
    right /= np.linalg.norm(right)
    kernel = np.zeros((4, 400))
    kernel[0], kernel[3] = left, right
    assert np.isclose(rho(kernel), 1.0 / np.sqrt(2.0), atol=1e-9)

    correlated = np.zeros((4, 400))
    correlated[0], correlated[3] = left, (left + right) / np.sqrt(2.0)
    assert not np.isclose(rho(correlated), 1.0 / np.sqrt(2.0), atol=1e-3)


def test_proportional_sectors_collapse_to_the_blind_variety():
    rng = np.random.default_rng(8)
    base = rng.normal(size=400)
    kernel = np.zeros((4, 400))
    kernel[0], kernel[3] = base, 2.5 * base
    assert rho(kernel) < 1e-10
