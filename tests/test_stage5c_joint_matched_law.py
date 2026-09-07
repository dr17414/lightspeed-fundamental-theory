"""Candidate-independent regressions for 6a-E closure item 2."""

import numpy as np
import pytest

from analysis.stage5c_hard_controls import MIN_MATCHED_PAIRS
from analysis.stage5c_joint_matched_law import (
    CALIBRATION_ARM_CORRELATION_SUITE,
    CALIBRATION_MATCHED_COUNT_SUITE,
    GENERATOR_SOURCE_ID,
    JOINT_MATCHED_LAW_ID,
    MATCHER_SOURCE_ID,
    PAIRED_COVARIANCE_ID,
    JointLawProtocolError,
    MatchingReason,
    MatchingStatus,
    aggregate_joint_matched_laws,
    calibrate_paired_covariance,
    certify_matching,
    form_joint_matched_law,
    planted_joint_covariance,
    planted_matching_inputs,
)


def _certification(
    retained_pairs: int,
    *,
    pool_size: int = 256,
    identity_suffix: str = "default",
):
    calibration_left, calibration_right, pool_left, pool_right = planted_matching_inputs(
        retained_pairs, pool_size=pool_size
    )
    return certify_matching(
        calibration_left,
        calibration_right,
        pool_left,
        pool_right,
        calibration_identity=f"item2-planted-calibration-{identity_suffix}",
        pool_identity=(
            f"item2-planted-pool-{pool_size}-{retained_pairs}-{identity_suffix}"
        ),
    )


def test_source_record_identities_are_explicit_and_candidate_independent():
    assert GENERATOR_SOURCE_ID.startswith("stage5c-hard-controls-sprinkle-control")
    assert MATCHER_SOURCE_ID.startswith("stage5c-hard-controls-c8.1-matcher")
    assert JOINT_MATCHED_LAW_ID == "stage5c-6a-e-joint-matched-law-v0.1"
    assert PAIRED_COVARIANCE_ID.endswith("ddof1-v0.1")


def test_matching_clean_path_uses_all_frozen_c8_1_gates():
    result = _certification(256)
    assert result.status is MatchingStatus.CLEAN
    assert result.reasons == (MatchingReason.CERTIFIED,)
    assert result.result is not None
    assert len(result.result.left_indices) == 256
    assert len(result.unmatched_left_indices) == 0
    assert len(result.unmatched_right_indices) == 0
    assert result.result.coverage == 1.0
    assert result.result.max_standardized_mean_difference == 0.0
    assert result.result.max_ks_distance == 0.0


def test_matching_attrition_and_failure_are_typed_inconclusive():
    cohort_failure = _certification(MIN_MATCHED_PAIRS - 1)
    assert cohort_failure.status is MatchingStatus.INCONCLUSIVE
    assert cohort_failure.reasons == (MatchingReason.COHORT_TOO_SMALL,)
    assert len(cohort_failure.unmatched_left_indices) == 256 - (MIN_MATCHED_PAIRS - 1)
    assert len(cohort_failure.unmatched_right_indices) == 256 - (MIN_MATCHED_PAIRS - 1)

    coverage_failure = _certification(MIN_MATCHED_PAIRS, pool_size=600)
    assert coverage_failure.status is MatchingStatus.INCONCLUSIVE
    assert coverage_failure.reasons == (MatchingReason.COVERAGE_TOO_LOW,)

    matcher_failure = _certification(0)
    assert matcher_failure.status is MatchingStatus.INCONCLUSIVE
    assert matcher_failure.reasons == (MatchingReason.MATCHER_FAILURE,)
    assert matcher_failure.result is None


def test_calibration_scale_failure_and_stream_identity_collision_fail_closed():
    width = 11
    constant = np.zeros((256, width))
    result = certify_matching(
        constant,
        constant,
        constant,
        constant,
        calibration_identity="calibration",
        pool_identity="evaluation",
    )
    assert result.status is MatchingStatus.INCONCLUSIVE
    assert result.reasons == (MatchingReason.CALIBRATION_SCALE_INVALID,)
    with pytest.raises(JointLawProtocolError):
        certify_matching(
            constant,
            constant,
            constant,
            constant,
            calibration_identity="same-stream",
            pool_identity="same-stream",
        )


def test_nonclean_matching_short_circuits_before_endpoint_inputs_are_touched():
    class UnreadableEndpoint:
        def __array__(self, *unused_args, **unused_kwargs):
            raise AssertionError("endpoint input was read after matching failure")

    with pytest.raises(JointLawProtocolError, match="NOT-EVALUATED"):
        form_joint_matched_law(
            _certification(MIN_MATCHED_PAIRS - 1),
            UnreadableEndpoint(),
            UnreadableEndpoint(),
            arm_names=("left", "right"),
        )


def test_joint_law_preserves_pairs_cross_covariance_and_uniform_weights():
    matching = _certification(256)
    rng = np.random.Generator(np.random.PCG64DXSM(710_002))
    joint = rng.multivariate_normal(np.zeros(4), planted_joint_covariance(-0.5), size=256)
    law = form_joint_matched_law(
        matching,
        joint[:, :2],
        joint[:, 2:],
        arm_names=("synthetic-left", "synthetic-right"),
    )
    assert law.matched_pairs == 256
    assert np.isclose(law.weights.sum(), 1.0)
    assert np.array_equal(law.delta, law.left - law.right)
    assert np.allclose(
        law.covariance.delta_covariance,
        np.cov(law.delta, rowvar=False, ddof=1),
        rtol=32.0 * np.finfo(float).eps,
        atol=0.0,
    )
    independent_marginals = (
        law.covariance.left_covariance + law.covariance.right_covariance
    )
    assert not np.allclose(independent_marginals, law.covariance.delta_covariance)
    assert all(not array.flags.writeable for array in (law.left, law.right, law.delta, law.weights))


def test_cluster_covariance_uses_independent_matched_cohorts_not_pair_count_df():
    rng = np.random.Generator(np.random.PCG64DXSM(710_003))
    laws = []
    for block in range(8):
        matching = _certification(256, identity_suffix=f"block-{block}")
        joint = rng.multivariate_normal(
            np.zeros(4), planted_joint_covariance(-0.5), size=256
        )
        laws.append(
            form_joint_matched_law(
                matching,
                joint[:, :2],
                joint[:, 2:],
                arm_names=("synthetic-left", "synthetic-right"),
            )
        )
    ensemble = aggregate_joint_matched_laws(tuple(laws))
    block_means = np.vstack([law.delta_mean for law in laws])
    assert ensemble.independent_clusters == 8
    assert ensemble.total_pairs == 8 * 256
    assert np.allclose(ensemble.delta_mean, block_means.mean(axis=0))
    assert np.allclose(
        ensemble.delta_mean_covariance,
        np.cov(block_means, rowvar=False, ddof=1) / len(laws),
        rtol=64.0 * np.finfo(float).eps,
        atol=0.0,
    )
    with pytest.raises(JointLawProtocolError, match="calibration identities"):
        aggregate_joint_matched_laws((laws[0], laws[0]))


@pytest.mark.parametrize("matched_pairs", CALIBRATION_MATCHED_COUNT_SUITE)
@pytest.mark.parametrize("arm_correlation", CALIBRATION_ARM_CORRELATION_SUITE)
def test_paired_covariance_consistency_and_null_region_calibration_are_separate(
    matched_pairs, arm_correlation
):
    report = calibrate_paired_covariance(matched_pairs, arm_correlation)
    assert report.covariance_mode == "paired"
    assert report.independent_clusters == 32
    assert report.covariance_consistent
    assert report.coverage_calibrated
    assert np.isclose(report.empirical_type_i_error, 1.0 - report.empirical_coverage)


def test_misspecified_independent_marginal_covariance_is_detected():
    correct = calibrate_paired_covariance(MIN_MATCHED_PAIRS, -0.75)
    wrong = calibrate_paired_covariance(
        MIN_MATCHED_PAIRS,
        -0.75,
        covariance_mode="independent-marginals",
    )
    assert correct.coverage_calibrated
    assert wrong.covariance_consistent  # the estimator is right; the region schema is not
    assert not wrong.coverage_calibrated
    assert wrong.empirical_type_i_error > correct.empirical_type_i_error
    assert wrong.stream_identity == correct.stream_identity


def test_statistical_planted_domain_rejects_unregistered_inputs():
    with pytest.raises(JointLawProtocolError):
        planted_joint_covariance(0.751)
    with pytest.raises(JointLawProtocolError):
        calibrate_paired_covariance(MIN_MATCHED_PAIRS - 1, 0.0)
    with pytest.raises(JointLawProtocolError):
        calibrate_paired_covariance(MIN_MATCHED_PAIRS, 0.0, covariance_mode="guess")
