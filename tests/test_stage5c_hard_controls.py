"""Regression tests for the candidate-independent Stage 5C C8.4 controls."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.stage5a_kappa import implication_classes, kappa  # noqa: E402
from analysis.stage5c_hard_controls import (  # noqa: E402
    CONTROL_THETA,
    FEATURE_NAMES,
    MAX_ABSOLUTE_SMD,
    MAX_KS_DISTANCE,
    MIN_MATCH_COVERAGE,
    MIN_MATCHED_PAIRS,
    REPLICATION_BASES,
    SOURCE_OF_RECORD_BASES,
    SOURCE_OF_RECORD_POOL_SIZE,
    baseline_features,
    benchmark,
    blind_batch,
    conformal_volume_density,
    construction_payload,
    expected_ordering_fraction,
    legendre_mode_2,
    log_chiral_transfer,
    kappa_one_feature_pool,
    replication_benchmarks,
    sample_hash,
    sprinkle_control,
)


def test_density_normalization_marginals_and_positivity():
    """Numerically cross-check the polynomial identities used in the proof."""
    z = np.linspace(0.0, 1.0, 2001)
    q = legendre_mode_2(z)
    assert abs(np.trapezoid(q, z)) < 1e-6
    assert abs(np.trapezoid(z * q, z)) < 1e-6
    for theta in (CONTROL_THETA, -CONTROL_THETA):
        density = conformal_volume_density(z[:, None], z[None, :], theta)
        assert density.min() > 0.0
        # Integrating over either coordinate gives the uniform marginal.
        marginal = np.trapezoid(density, z, axis=1)
        assert np.max(np.abs(marginal - 1.0)) < 1e-6
        assert expected_ordering_fraction(theta) == 0.5


def test_every_control_sample_is_dimension_at_most_two():
    """The sealed null orders explicitly realize every generated causet."""
    for theta, base in ((CONTROL_THETA, 610_000_000), (-CONTROL_THETA, 620_000_000)):
        for seed in range(base, base + 8):
            sample = sprinkle_control(64, theta, seed)
            classes, comparability_ok, _, _ = implication_classes(sample.order)
            assert comparability_ok
            assert len(classes) >= 2


def test_construction_payload_seals_target_metadata():
    sample = sprinkle_control(32, CONTROL_THETA, 630_000_000)
    payload = construction_payload(sample)
    assert set(payload) == {"order"}
    assert np.array_equal(payload["order"], sample.order)
    assert payload["order"] is not sample.order


def test_blinded_batch_hides_labels_seeds_coordinates_and_invocation_grouping():
    samples = [
        sprinkle_control(24, theta, 650_000_000 + i)
        for i, theta in enumerate([CONTROL_THETA] * 8 + [-CONTROL_THETA] * 8)
    ]
    cases, evaluator_index = blind_batch(samples, blinding_seed=660_000_000)
    assert len(cases) == len(samples)
    assert set(evaluator_index) == {case.case_id for case in cases}
    assert all(set(vars(case)) == {"case_id", "order"} for case in cases)
    recovered_signs = [np.sign(samples[evaluator_index[c.case_id]].theta) for c in cases]
    assert recovered_signs != [1.0] * 8 + [-1.0] * 8
    assert len(set(case.case_id for case in cases)) == len(cases)


def test_baseline_features_are_label_invariant():
    sample = sprinkle_control(64, CONTROL_THETA, 640_000_000)
    permutation = np.random.default_rng(41).permutation(len(sample.order))
    relabelled = sample.order[np.ix_(permutation, permutation)]
    assert len(baseline_features(sample.order)) == len(FEATURE_NAMES)
    assert np.allclose(
        baseline_features(sample.order), baseline_features(relabelled), atol=0.0
    )


def test_continuum_targets_have_predeclared_opposite_direction():
    plus = log_chiral_transfer(CONTROL_THETA)
    minus = log_chiral_transfer(-CONTROL_THETA)
    assert plus > 0.08
    assert minus < -0.08
    assert plus - minus > 0.17


def test_rng_hash_manifest_is_pinned():
    plus = sprinkle_control(96, CONTROL_THETA, 530_000_000)
    minus = sprinkle_control(96, -CONTROL_THETA, 540_000_000)
    assert sample_hash(plus) == (
        "25d01daed468657e4bbbf646cba8ec2b6b4c74e2d2df356de3c9e204d1ee7795"
    )
    assert sample_hash(minus) == (
        "a0bffe5ee999152688750469c36d779c3735a4148e415cd38d67a65b10db8970"
    )


def test_matching_benchmark_is_nontrivial_and_balanced():
    """CI reruns the complete source-of-record feasibility benchmark."""
    result = benchmark(n=96, pool_size=SOURCE_OF_RECORD_POOL_SIZE)
    assert SOURCE_OF_RECORD_POOL_SIZE == 768
    assert result["seed_bases"] == SOURCE_OF_RECORD_BASES
    assert len(REPLICATION_BASES) == 4
    assert result["matched_pairs"] == 361
    assert np.isclose(result["coverage"], 0.4700520833333333)
    assert np.isclose(result["max_smd"], 0.16158546089604894)
    assert np.isclose(result["max_ks"], 0.10803324099722988)
    assert np.isclose(result["median_distance"], 1.6655190336322285)
    assert np.isclose(result["p90_distance"], 1.904361142701321)
    assert all(count == 0 for count in result["chain_counts"].values())
    assert result["matched_pairs"] >= MIN_MATCHED_PAIRS
    assert result["coverage"] >= MIN_MATCH_COVERAGE
    assert result["max_smd"] <= MAX_ABSOLUTE_SMD
    assert result["max_ks"] <= MAX_KS_DISTANCE


def test_kappa_one_domain_filter_uses_the_stage5a_observable():
    seeds = range(670_000_000, 670_000_008)
    features, retained = kappa_one_feature_pool(32, CONTROL_THETA, seeds)
    expected = [
        seed
        for seed in seeds
        if kappa(sprinkle_control(32, CONTROL_THETA, seed).order) == 1
    ]
    assert retained.tolist() == expected
    assert features.shape == (len(expected), len(FEATURE_NAMES))


def test_replication_runner_uses_all_frozen_seed_blocks():
    results = replication_benchmarks(n=32, pool_size=64)
    assert tuple(
        tuple(result["seed_bases"].values()) for result in results
    ) == REPLICATION_BASES
