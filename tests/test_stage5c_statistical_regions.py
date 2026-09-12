"""Candidate-independent regressions for 6a-E statistical regions."""

from dataclasses import replace
from types import SimpleNamespace

import numpy as np
import pytest

from analysis.stage5c_joint_matched_law import JOINT_MATCHED_LAW_ID, MatchedLawEnsemble
from analysis.stage5c_statistical_regions import (
    E1_ARM_NAMES,
    E2_MINUS_ARM_NAMES,
    E2_PLUS_ARM_NAMES,
    E3_WRONG_SUPPORT_EFFECT_FLOOR,
    ENDPOINT_RANGE_WIDTHS,
    EQUIVALENCE_MARGIN,
    JOINT_EFFECT_FLOOR,
    MIN_INDEPENDENT_COHORTS,
    E2Target,
    E3Claim,
    RegionProtocolError,
    RegionReason,
    RegionStatus,
    ScientificVerdict,
    StatisticalRegionInput,
    aggregate_matched_numerical_half_width,
    build_simultaneous_region,
    df_only_reference_oracle,
    e2_null_pair_spec,
    evaluate_e1,
    evaluate_e2,
    evaluate_e3,
)


def test_e2_null_specs_use_the_same_frozen_target_with_distinct_future_arms():
    plus = e2_null_pair_spec(E2Target.PLUS)
    minus = e2_null_pair_spec(E2Target.MINUS)
    assert plus.theta == -minus.theta == 0.4
    assert plus.generator_source_id == minus.generator_source_id
    assert plus.arm_names == E2_PLUS_ARM_NAMES
    assert minus.arm_names == E2_MINUS_ARM_NAMES
    assert plus.arm_names[0] != plus.arm_names[1]
    assert minus.arm_names[0] != minus.arm_names[1]
    assert plus.requires_distinct_pool_identities
    assert minus.requires_distinct_pool_identities


def _inputs(
    estimate,
    *,
    arm_names=E1_ARM_NAMES,
    covariance=None,
    clusters=MIN_INDEPENDENT_COHORTS,
    pairs_per_cluster=192,
):
    if covariance is None:
        covariance = np.diag([1.0e-8, 1.0e-8])
    return StatisticalRegionInput(
        estimate=np.asarray(estimate, dtype=float),
        mean_covariance=np.asarray(covariance, dtype=float),
        independent_clusters=clusters,
        total_pairs=clusters * pairs_per_cluster,
        cluster_pair_counts=(pairs_per_cluster,) * clusters,
        arm_names=arm_names,
    )


def _region(estimate, *, arm_names=E1_ARM_NAMES, numerical=(0.0, 0.0)):
    return build_simultaneous_region(
        _inputs(estimate, arm_names=arm_names),
        local_alpha=0.01,
        numerical_half_width=np.asarray(numerical),
    )


def test_region_input_adapter_preserves_frozen_matched_law_provenance():
    laws = tuple(
        SimpleNamespace(
            matched_pairs=192,
            arm_names=E1_ARM_NAMES,
            law_id=JOINT_MATCHED_LAW_ID,
        )
        for _ in range(MIN_INDEPENDENT_COHORTS)
    )
    ensemble = MatchedLawEnsemble(
        laws=laws,
        delta_mean=np.asarray([0.2, 0.01]),
        delta_mean_covariance=np.diag([1.0e-4, 2.0e-4]),
        total_pairs=MIN_INDEPENDENT_COHORTS * 192,
        independent_clusters=MIN_INDEPENDENT_COHORTS,
    )
    inputs = StatisticalRegionInput.from_ensemble(ensemble)
    assert inputs.arm_names == E1_ARM_NAMES
    assert inputs.cluster_pair_counts == (192,) * MIN_INDEPENDENT_COHORTS
    assert inputs.total_pairs == MIN_INDEPENDENT_COHORTS * 192
    assert not inputs.estimate.flags.writeable
    assert not inputs.mean_covariance.flags.writeable


def test_region_uses_cluster_df_bonferroni_and_adds_numerical_error():
    no_numerical = _region([0.2, 0.0])
    with_numerical = _region([0.2, 0.0], numerical=(0.01, 0.02))
    assert no_numerical.status is RegionStatus.CLEAN
    assert no_numerical.region.reference_df == MIN_INDEPENDENT_COHORTS - 1
    assert with_numerical.region.reference_df != MIN_INDEPENDENT_COHORTS * 192 - 1
    assert np.allclose(
        with_numerical.region.lower,
        no_numerical.region.lower - np.asarray([0.01, 0.02]),
    )
    assert np.allclose(
        with_numerical.region.upper,
        no_numerical.region.upper + np.asarray([0.01, 0.02]),
    )
    assert np.allclose(
        with_numerical.region.normalized_lower,
        with_numerical.region.lower / ENDPOINT_RANGE_WIDTHS,
    )


def test_item3_endpoint_errors_follow_match_indices_and_total_pair_weights():
    matching_a = SimpleNamespace(
        result=SimpleNamespace(
            left_indices=np.asarray([0, 2]), right_indices=np.asarray([1, 2])
        )
    )
    matching_b = SimpleNamespace(
        result=SimpleNamespace(
            left_indices=np.asarray([1, 2]), right_indices=np.asarray([0, 2])
        )
    )
    laws = tuple(
        SimpleNamespace(
            matched_pairs=2,
            arm_names=E1_ARM_NAMES,
            law_id=JOINT_MATCHED_LAW_ID,
            matching=matching,
        )
        for matching in (matching_a, matching_b)
    )
    ensemble = MatchedLawEnsemble(
        laws=laws,
        delta_mean=np.zeros(2),
        delta_mean_covariance=np.eye(2),
        total_pairs=4,
        independent_clusters=2,
    )
    left = (
        np.asarray([[1.0, 10.0], [99.0, 99.0], [2.0, 20.0]]),
        np.asarray([[99.0, 99.0], [3.0, 30.0], [4.0, 40.0]]),
    )
    right = (
        np.asarray([[99.0, 99.0], [5.0, 50.0], [6.0, 60.0]]),
        np.asarray([[7.0, 70.0], [99.0, 99.0], [8.0, 80.0]]),
    )
    radius = aggregate_matched_numerical_half_width(ensemble, left, right)
    expected = np.asarray([(1 + 5 + 2 + 6 + 3 + 7 + 4 + 8) / 4, 90.0])
    assert np.all(radius >= expected)
    assert np.all(radius <= np.nextafter(expected, np.inf))
    assert not radius.flags.writeable


def test_item3_error_average_does_not_overflow_before_division():
    matching = SimpleNamespace(
        result=SimpleNamespace(
            left_indices=np.asarray([0, 1]), right_indices=np.asarray([0, 1])
        )
    )
    laws = tuple(
        SimpleNamespace(
            matched_pairs=2,
            arm_names=E1_ARM_NAMES,
            law_id=JOINT_MATCHED_LAW_ID,
            matching=matching,
        )
        for _ in range(2)
    )
    ensemble = MatchedLawEnsemble(
        laws=laws,
        delta_mean=np.zeros(2),
        delta_mean_covariance=np.eye(2),
        total_pairs=4,
        independent_clusters=2,
    )
    large = np.full((2, 2), np.finfo(float).max / 4.0)
    radius = aggregate_matched_numerical_half_width(
        ensemble,
        (large, large),
        (large, large),
    )
    assert np.all(np.isfinite(radius))
    assert np.all(radius >= np.finfo(float).max / 2.0)


def test_item3_error_propagation_rejects_malformed_matched_indices():
    matching = SimpleNamespace(
        result=SimpleNamespace(
            left_indices=np.asarray([-1, 1]), right_indices=np.asarray([0, 1])
        )
    )
    laws = tuple(
        SimpleNamespace(
            matched_pairs=2,
            arm_names=E1_ARM_NAMES,
            law_id=JOINT_MATCHED_LAW_ID,
            matching=matching,
        )
        for _ in range(2)
    )
    ensemble = MatchedLawEnsemble(
        laws=laws,
        delta_mean=np.zeros(2),
        delta_mean_covariance=np.eye(2),
        total_pairs=4,
        independent_clusters=2,
    )
    errors = (np.zeros((2, 2)), np.zeros((2, 2)))
    with pytest.raises(RegionProtocolError, match="matched indices"):
        aggregate_matched_numerical_half_width(ensemble, errors, errors)


def test_cohort_and_covariance_failures_short_circuit_region_formation():
    too_small = build_simultaneous_region(
        _inputs([0.0, 0.0], clusters=MIN_INDEPENDENT_COHORTS - 1),
        local_alpha=0.01,
        numerical_half_width=np.zeros(2),
    )
    assert too_small.status is RegionStatus.INCONCLUSIVE
    assert too_small.reason is RegionReason.COHORT_TOO_SMALL
    assert too_small.region is None

    outside_calibration = build_simultaneous_region(
        _inputs([0.0, 0.0], pairs_per_cluster=385),
        local_alpha=0.01,
        numerical_half_width=np.zeros(2),
    )
    assert outside_calibration.status is RegionStatus.INCONCLUSIVE
    assert outside_calibration.reason is RegionReason.PAIR_COUNT_OUTSIDE_CALIBRATION
    assert outside_calibration.region is None

    indefinite = build_simultaneous_region(
        _inputs([0.0, 0.0], covariance=[[1.0, 2.0], [2.0, 1.0]]),
        local_alpha=0.01,
        numerical_half_width=np.zeros(2),
    )
    assert indefinite.reason is RegionReason.COVARIANCE_INVALID
    assert indefinite.region is None

    degenerate = build_simultaneous_region(
        _inputs([0.0, 0.0], covariance=[[1.0, 0.0], [0.0, 0.0]]),
        local_alpha=0.01,
        numerical_half_width=np.zeros(2),
    )
    assert degenerate.reason is RegionReason.DEGENERATE_MARGINAL_VARIANCE
    assert degenerate.region is None


def test_malformed_alpha_numerical_radius_and_identity_fail_closed():
    with pytest.raises(RegionProtocolError):
        build_simultaneous_region(
            _inputs([0.0, 0.0]),
            local_alpha=0.011,
            numerical_half_width=np.zeros(2),
        )
    with pytest.raises(RegionProtocolError):
        build_simultaneous_region(
            _inputs([0.0, 0.0]),
            local_alpha=0.01,
            numerical_half_width=np.asarray([-1.0, 0.0]),
        )
    with pytest.raises(RegionProtocolError):
        StatisticalRegionInput(
            estimate=np.zeros(2),
            mean_covariance=np.eye(2),
            independent_clusters=32,
            total_pairs=32,
            cluster_pair_counts=(1,) * 31,
            arm_names=E1_ARM_NAMES,
        )
    with pytest.raises(RegionProtocolError, match="total_pairs"):
        StatisticalRegionInput(
            estimate=np.zeros(2),
            mean_covariance=np.eye(2),
            independent_clusters=32,
            total_pairs=32.0,
            cluster_pair_counts=(1,) * 32,
            arm_names=E1_ARM_NAMES,
        )


def test_finite_inputs_that_overflow_region_arithmetic_fail_typed_closed():
    result = build_simultaneous_region(
        _inputs([np.finfo(float).max, 0.0], covariance=np.eye(2)),
        local_alpha=0.01,
        numerical_half_width=np.asarray([np.finfo(float).max, 0.0]),
    )
    assert result.status is RegionStatus.INCONCLUSIVE
    assert result.reason is RegionReason.NONFINITE_INPUT
    assert result.region is None


def test_e1_requires_the_entire_region_to_clear_the_closed_effect_box():
    base = _region([0.0, 0.0])
    half_width = base.region.statistical_half_width
    passing_mean = np.asarray(
        [ENDPOINT_RANGE_WIDTHS[0] * JOINT_EFFECT_FLOOR + half_width[0] + 1.0e-6, 0.0]
    )
    equality_mean = np.asarray(
        [ENDPOINT_RANGE_WIDTHS[0] * JOINT_EFFECT_FLOOR + half_width[0], 0.0]
    )
    assert evaluate_e1(_region(passing_mean)).verdict is ScientificVerdict.PASS
    equality = _region(equality_mean)
    equality = replace(
        equality,
        region=replace(
            equality.region,
            normalized_lower=np.asarray(
                [JOINT_EFFECT_FLOOR, equality.region.normalized_lower[1]]
            ),
        ),
    )
    assert equality.region.normalized_lower[0] == JOINT_EFFECT_FLOOR
    assert evaluate_e1(equality).verdict is ScientificVerdict.FAIL


@pytest.mark.parametrize(
    ("target", "arm_names"),
    [(E2Target.PLUS, E2_PLUS_ARM_NAMES), (E2Target.MINUS, E2_MINUS_ARM_NAMES)],
)
def test_e2_requires_both_null_regions_strictly_inside_open_margin(target, arm_names):
    passing = _region([0.0, 0.0], arm_names=arm_names)
    assert evaluate_e2(passing, target).verdict is ScientificVerdict.PASS

    half_width = passing.region.statistical_half_width
    equality_mean = np.asarray(
        [EQUIVALENCE_MARGIN[0] * ENDPOINT_RANGE_WIDTHS[0] - half_width[0], 0.0]
    )
    equality = _region(equality_mean, arm_names=arm_names)
    equality = replace(
        equality,
        region=replace(
            equality.region,
            normalized_upper=np.asarray(
                [EQUIVALENCE_MARGIN[0], equality.region.normalized_upper[1]]
            ),
        ),
    )
    assert equality.region.normalized_upper[0] == EQUIVALENCE_MARGIN[0]
    assert evaluate_e2(equality, target).verdict is ScientificVerdict.FAIL


@pytest.mark.parametrize(
    ("claim", "arm_names", "estimate"),
    [
        (E3Claim.CHIRAL_VS_BLIND, ("correct-chiral", "sector-blind"), (0.2, 0.0)),
        (
            E3Claim.DIFFUSION_VS_BLIND,
            ("symmetric-diffusion", "sector-blind"),
            (-0.2, 0.2),
        ),
        (
            E3Claim.CORRECT_VS_WRONG_SUPPORT,
            ("correct-support", "wrong-support"),
            (2.0 * E3_WRONG_SUPPORT_EFFECT_FLOOR, 0.0),
        ),
        (
            E3Claim.SECTOR_BLIND_NULL,
            ("sector-blind-null-A", "sector-blind-null-B"),
            (0.0, 0.0),
        ),
    ],
)
def test_e3_registered_component_rules_are_simultaneous(claim, arm_names, estimate):
    report = evaluate_e3(_region(estimate, arm_names=arm_names), claim)
    assert report.verdict is ScientificVerdict.PASS


def test_e3_does_not_allow_arm_relabel_or_component_boundary_equality():
    with pytest.raises(RegionProtocolError, match="arm identities"):
        evaluate_e3(
            _region([0.2, 0.0], arm_names=("sector-blind", "correct-chiral")),
            E3Claim.CHIRAL_VS_BLIND,
        )

    base = _region([0.0, 0.0], arm_names=("correct-support", "wrong-support"))
    equality_mean = np.asarray(
        [E3_WRONG_SUPPORT_EFFECT_FLOOR + base.region.statistical_half_width[0], 0.0]
    )
    equality = _region(
        equality_mean,
        arm_names=("correct-support", "wrong-support"),
    )
    equality = replace(
        equality,
        region=replace(
            equality.region,
            lower=np.asarray(
                [E3_WRONG_SUPPORT_EFFECT_FLOOR, equality.region.lower[1]]
            ),
        ),
    )
    assert equality.region.lower[0] == E3_WRONG_SUPPORT_EFFECT_FLOOR
    assert (
        evaluate_e3(equality, E3Claim.CORRECT_VS_WRONG_SUPPORT).verdict
        is ScientificVerdict.FAIL
    )


def test_inconclusive_region_never_becomes_a_scientific_fail():
    result = build_simultaneous_region(
        _inputs([0.0, 0.0], clusters=31),
        local_alpha=0.01,
        numerical_half_width=np.zeros(2),
    )
    report = evaluate_e1(result)
    assert report.verdict is ScientificVerdict.NOT_EVALUATED
    assert report.region is None


def test_df_only_falsifier_has_an_exact_analytic_coverage_oracle():
    report = df_only_reference_oracle()
    assert report.correct_df == 31
    assert report.falsifier_df == 32 * 192 - 1
    assert report.correct_coverage == pytest.approx(
        report.per_coordinate_nominal_coverage, abs=1.0e-14
    )
    assert report.falsifier_coverage < report.per_coordinate_nominal_coverage
    assert report.local_alpha == 0.01
    assert report.coverage_gap > 0.003
    assert report.falsifier_detected
