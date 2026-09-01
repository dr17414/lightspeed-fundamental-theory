"""Structural tests for the committed smearing/normalisation/6a-S prereg."""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analysis.stage5c_measure_prereg import (  # noqa: E402
    BLOCKS_PER_TARGET,
    CARDINALITIES,
    CASES_PER_BLOCK,
    FOURIER_FREQUENCIES,
    MASS_TOLERANCE,
    SMEARING_EPSILON,
    TARGET_SEED_BASES,
    MeasureProtocolError,
    fourier_signature,
    gaussian_mollifier_density,
    mean_signature_distance,
    measure_diagnostics,
    normalised_weights,
    passes_s1_s6,
    passes_s5,
    preregistered_seed,
    random_law_energy_distance,
    uniform_pair_weights,
)


def test_seed_manifest_is_unique_and_separates_targets():
    seeds = {
        preregistered_seed(target, n_index, block, case)
        for target in TARGET_SEED_BASES
        for n_index in range(len(CARDINALITIES))
        for block in range(BLOCKS_PER_TARGET)
        for case in range(CASES_PER_BLOCK)
    }
    expected = 2 * len(CARDINALITIES) * BLOCKS_PER_TARGET * CASES_PER_BLOCK
    assert len(seeds) == expected
    assert min(seeds) >= 1_300_000_000
    assert max(seeds) < 1_500_000_000


def test_seed_manifest_rejects_unregistered_cells():
    for arguments in [
        ("other", 0, 0, 0),
        ("plus", len(CARDINALITIES), 0, 0),
        ("plus", 0, BLOCKS_PER_TARGET, 0),
        ("plus", 0, 0, CASES_PER_BLOCK),
    ]:
        with pytest.raises(MeasureProtocolError):
            preregistered_seed(*arguments)


def test_phi_one_and_pair_count_normalisation_make_probability_measure():
    weights, normalization = uniform_pair_weights(137)
    probability = normalised_weights(weights, normalization)
    assert normalization == 137.0
    assert np.all(weights == 1.0)
    assert probability.sum() == pytest.approx(1.0, abs=MASS_TOLERANCE)
    diagnostics = measure_diagnostics(137, 901)
    assert diagnostics.total_mass == pytest.approx(1.0)
    assert diagnostics.total_variation == pytest.approx(1.0)
    assert diagnostics.kish_ess == pytest.approx(137.0)
    assert diagnostics.ess_fraction == pytest.approx(1.0)
    assert passes_s1_s6(diagnostics)


def test_s1_s6_floors_are_not_silently_excluded():
    assert not passes_s1_s6(measure_diagnostics(31, 100))
    assert not passes_s1_s6(measure_diagnostics(32, 10_000))
    with pytest.raises(MeasureProtocolError):
        measure_diagnostics(0, 100)
    with pytest.raises(MeasureProtocolError):
        measure_diagnostics(101, 100)


def test_fourier_grid_is_exact_first_nonzero_shell():
    assert FOURIER_FREQUENCIES.shape == (80, 4)
    scaled = FOURIER_FREQUENCIES / (2.0 * np.pi)
    assert set(np.unique(scaled)) == {-1.0, 0.0, 1.0}
    assert not np.any(np.all(scaled == 0.0, axis=1))
    assert not FOURIER_FREQUENCIES.flags.writeable


def test_gaussian_regulator_is_linear_and_uses_frozen_scale():
    atoms = np.array([[0.2, 0.3, 0.7, 0.8], [0.4, 0.1, 0.9, 0.6]])
    query = np.array([[0.3, 0.2, 0.8, 0.7], [0.1, 0.1, 0.1, 0.1]])
    left = gaussian_mollifier_density(query, atoms, np.array([0.25, 0.75]))
    right = (
        0.25 * gaussian_mollifier_density(query, atoms[:1], np.array([1.0]))
        + 0.75 * gaussian_mollifier_density(query, atoms[1:], np.array([1.0]))
    )
    assert SMEARING_EPSILON == 1.0 / 16.0
    assert np.allclose(left, right, rtol=1e-13, atol=0.0)


def test_signature_is_relabel_invariant_and_gaussian_damped():
    atoms = np.array(
        [
            [0.1, 0.2, 0.7, 0.8],
            [0.2, 0.4, 0.6, 0.9],
            [0.3, 0.1, 0.8, 0.7],
        ]
    )
    probability = np.array([0.2, 0.3, 0.5])
    signature = fourier_signature(atoms, probability)
    permutation = np.array([2, 0, 1])
    moved = fourier_signature(atoms[permutation], probability[permutation])
    assert np.allclose(signature, moved, rtol=0.0, atol=1e-15)
    assert np.all(np.abs(signature) <= 1.0)


def test_same_target_metrics_are_zero_on_identical_blocks():
    rng = np.random.default_rng(41)
    signatures = rng.normal(size=(12, 80)) + 1j * rng.normal(size=(12, 80))
    assert mean_signature_distance(signatures, signatures) == 0.0
    assert random_law_energy_distance(signatures, signatures) == 0.0
    assert passes_s5(signatures, signatures)


def test_same_target_metrics_detect_a_large_shift():
    left = np.zeros((8, 80), dtype=complex)
    right = np.ones((8, 80), dtype=complex)
    assert mean_signature_distance(left, right) == pytest.approx(1.0)
    assert random_law_energy_distance(left, right) > 0.2
    assert not passes_s5(left, right)


def test_measure_api_rejects_wrong_shapes_mass_and_domain():
    with pytest.raises(MeasureProtocolError):
        fourier_signature(np.zeros((3, 3)), np.ones(3) / 3)
    with pytest.raises(MeasureProtocolError):
        fourier_signature(np.zeros((3, 4)), np.ones(3))
    with pytest.raises(MeasureProtocolError):
        fourier_signature(np.full((3, 4), 2.0), np.ones(3) / 3)
    with pytest.raises(MeasureProtocolError):
        normalised_weights(np.array([1.0, -1.0]), 1.0)
