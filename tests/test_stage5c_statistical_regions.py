"""Candidate-independent regressions for 6a-E statistical regions."""

from dataclasses import replace
from fractions import Fraction
from types import SimpleNamespace

import numpy as np
import pytest

from analysis.stage5c_joint_matched_law import JOINT_MATCHED_LAW_ID, MatchedLawEnsemble
from analysis.stage5c_numerical_certification import (
    CERTIFICATION_ID,
    CertificationReason,
    CertificationResult,
    CertificationStatus,
)
from analysis.stage5c_statistical_regions import (
    CertifiedEndpointPool,
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
    ValidatedNumericalHalfWidth,
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


def _validated_radius(inputs, values=(0.0, 0.0)):
    return ValidatedNumericalHalfWidth(
        values=np.asarray(values, dtype=float),
        independent_clusters=inputs.independent_clusters,
        total_pairs=inputs.total_pairs,
        arm_names=inputs.arm_names,
    )


def _region(estimate, *, arm_names=E1_ARM_NAMES, numerical=(0.0, 0.0)):
    inputs = _inputs(estimate, arm_names=arm_names)
    return build_simultaneous_region(
        inputs,
        local_alpha=0.01,
        numerical_half_width=_validated_radius(inputs, numerical),
    )


def _certification(endpoint, error, *, clean=True, certification_id=CERTIFICATION_ID):
    endpoint = np.asarray(endpoint, dtype=float)
    error = np.asarray(error, dtype=float)
    return CertificationResult(
        status=CertificationStatus.CLEAN if clean else CertificationStatus.INCONCLUSIVE,
        reason=(
            CertificationReason.CERTIFIED
            if clean
            else CertificationReason.IMPLEMENTATION_DISAGREEMENT
        ),
        agreement_distance=0.0,
        agreement_bound=0.0,
        matrix=np.eye(2) if clean else None,
        matrix_error=0.0 if clean else None,
        norm_lower=1.0 if clean else None,
        norm_upper=1.0 if clean else None,
        endpoint=endpoint if clean else None,
        endpoint_error=error if clean else None,
        endpoint_lower=endpoint - error if clean else None,
        endpoint_upper=endpoint + error if clean else None,
        certification_id=certification_id,
    )


def _certified_pool(arm_name, pool_identity, endpoints, errors):
    return CertifiedEndpointPool(
        arm_name=arm_name,
        pool_identity=pool_identity,
        row_indices=tuple(range(len(endpoints))),
        rows=tuple(
            _certification(endpoint, error)
            for endpoint, error in zip(endpoints, errors, strict=True)
        ),
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
    assert all(
        Fraction.from_float(float(standard_error)) ** 2
        >= Fraction.from_float(1.0e-8)
        for standard_error in no_numerical.region.standard_error
    )
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
    pool_ids = ("cohort-a", "cohort-b")
    matching_a = SimpleNamespace(
        pool_identity=pool_ids[0],
        result=SimpleNamespace(
            left_indices=np.asarray([0, 2]), right_indices=np.asarray([1, 2])
        )
    )
    matching_b = SimpleNamespace(
        pool_identity=pool_ids[1],
        result=SimpleNamespace(
            left_indices=np.asarray([1, 2]), right_indices=np.asarray([0, 2])
        )
    )
    left_errors = (
        np.asarray([[1.0, 10.0], [99.0, 99.0], [2.0, 20.0]]),
        np.asarray([[99.0, 99.0], [3.0, 30.0], [4.0, 40.0]]),
    )
    right_errors = (
        np.asarray([[99.0, 99.0], [5.0, 50.0], [6.0, 60.0]]),
        np.asarray([[7.0, 70.0], [99.0, 99.0], [8.0, 80.0]]),
    )
    left_endpoints = (
        np.asarray([[0.0, 0.0], [0.1, 0.1], [0.2, 0.2]]),
        np.asarray([[0.3, 0.3], [0.4, 0.4], [0.5, 0.5]]),
    )
    right_endpoints = (
        np.asarray([[0.6, 0.6], [0.7, 0.7], [0.8, 0.8]]),
        np.asarray([[0.9, 0.9], [1.0, 1.0], [1.1, 1.1]]),
    )
    matchings = (matching_a, matching_b)
    laws = tuple(
        SimpleNamespace(
            matched_pairs=2,
            arm_names=E1_ARM_NAMES,
            law_id=JOINT_MATCHED_LAW_ID,
            matching=matching,
            left=left_endpoint[matching.result.left_indices],
            right=right_endpoint[matching.result.right_indices],
        )
        for matching, left_endpoint, right_endpoint in zip(
            matchings, left_endpoints, right_endpoints, strict=True
        )
    )
    ensemble = MatchedLawEnsemble(
        laws=laws,
        delta_mean=np.zeros(2),
        delta_mean_covariance=np.eye(2),
        total_pairs=4,
        independent_clusters=2,
    )
    left_pools = tuple(
        _certified_pool(E1_ARM_NAMES[0], pool_id, endpoints, errors)
        for pool_id, endpoints, errors in zip(
            pool_ids, left_endpoints, left_errors, strict=True
        )
    )
    right_pools = tuple(
        _certified_pool(E1_ARM_NAMES[1], pool_id, endpoints, errors)
        for pool_id, endpoints, errors in zip(
            pool_ids, right_endpoints, right_errors, strict=True
        )
    )
    radius = aggregate_matched_numerical_half_width(
        ensemble, left_pools, right_pools
    )
    expected = np.asarray([(1 + 5 + 2 + 6 + 3 + 7 + 4 + 8) / 4, 90.0])
    assert np.all(radius.values >= expected)
    assert np.all(radius.values <= np.nextafter(expected, np.inf))
    assert not radius.values.flags.writeable
    assert radius.total_pairs == ensemble.total_pairs
    assert radius.arm_names == E1_ARM_NAMES


def test_item3_error_average_does_not_overflow_before_division():
    endpoints = np.zeros((2, 2))
    matchings = tuple(
        SimpleNamespace(
            pool_identity=f"large-{index}",
            result=SimpleNamespace(
                left_indices=np.asarray([0, 1]), right_indices=np.asarray([0, 1])
            ),
        )
        for index in range(2)
    )
    laws = tuple(
        SimpleNamespace(
            matched_pairs=2,
            arm_names=E1_ARM_NAMES,
            law_id=JOINT_MATCHED_LAW_ID,
            matching=matching,
            left=endpoints,
            right=endpoints,
        )
        for matching in matchings
    )
    ensemble = MatchedLawEnsemble(
        laws=laws,
        delta_mean=np.zeros(2),
        delta_mean_covariance=np.eye(2),
        total_pairs=4,
        independent_clusters=2,
    )
    large = np.full((2, 2), np.finfo(float).max / 4.0)
    left_pools = tuple(
        _certified_pool(E1_ARM_NAMES[0], matching.pool_identity, endpoints, large)
        for matching in matchings
    )
    right_pools = tuple(
        _certified_pool(E1_ARM_NAMES[1], matching.pool_identity, endpoints, large)
        for matching in matchings
    )
    radius = aggregate_matched_numerical_half_width(
        ensemble,
        left_pools,
        right_pools,
    )
    assert np.all(np.isfinite(radius.values))
    assert np.all(radius.values >= np.finfo(float).max / 2.0)


def test_item3_error_propagation_rejects_malformed_matched_indices():
    matching = SimpleNamespace(
        pool_identity="malformed",
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
            left=np.zeros((2, 2)),
            right=np.zeros((2, 2)),
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
    left_pool = _certified_pool(
        E1_ARM_NAMES[0], "malformed", np.zeros((2, 2)), np.zeros((2, 2))
    )
    right_pool = _certified_pool(
        E1_ARM_NAMES[1], "malformed", np.zeros((2, 2)), np.zeros((2, 2))
    )
    with pytest.raises(RegionProtocolError, match="matched indices"):
        aggregate_matched_numerical_half_width(
            ensemble, (left_pool, left_pool), (right_pool, right_pool)
        )


def test_item3_error_pool_requires_clean_frozen_certification_provenance():
    with pytest.raises(RegionProtocolError, match="CLEAN"):
        CertifiedEndpointPool(
            arm_name=E1_ARM_NAMES[0],
            pool_identity="pool",
            row_indices=(0,),
            rows=(_certification([0.0, 0.0], [0.0, 0.0], clean=False),),
        )
    with pytest.raises(RegionProtocolError, match="identity"):
        CertifiedEndpointPool(
            arm_name=E1_ARM_NAMES[0],
            pool_identity="pool",
            row_indices=(0,),
            rows=(
                _certification(
                    [0.0, 0.0],
                    [0.0, 0.0],
                    certification_id="wrong-certification",
                ),
            ),
        )
    with pytest.raises(RegionProtocolError, match="row_indices"):
        CertifiedEndpointPool(
            arm_name=E1_ARM_NAMES[0],
            pool_identity="pool",
            row_indices=(1,),
            rows=(_certification([0.0, 0.0], [0.0, 0.0]),),
        )


def test_item3_error_pool_must_match_joint_law_pool_arm_and_endpoint_rows():
    indices = np.asarray([0, 1])
    matching = SimpleNamespace(
        pool_identity="registered-pool",
        result=SimpleNamespace(left_indices=indices, right_indices=indices),
    )
    endpoints = np.asarray([[0.1, 0.2], [0.3, 0.4]])
    law = SimpleNamespace(
        matched_pairs=2,
        arm_names=E1_ARM_NAMES,
        law_id=JOINT_MATCHED_LAW_ID,
        matching=matching,
        left=endpoints,
        right=endpoints,
    )
    ensemble = MatchedLawEnsemble(
        laws=(law, law),
        delta_mean=np.zeros(2),
        delta_mean_covariance=np.eye(2),
        total_pairs=4,
        independent_clusters=2,
    )
    errors = np.zeros((2, 2))
    left = _certified_pool(E1_ARM_NAMES[0], "registered-pool", endpoints, errors)
    right = _certified_pool(E1_ARM_NAMES[1], "registered-pool", endpoints, errors)
    wrong_pool = _certified_pool(E1_ARM_NAMES[0], "other-pool", endpoints, errors)
    with pytest.raises(RegionProtocolError, match="provenance"):
        aggregate_matched_numerical_half_width(
            ensemble, (wrong_pool, wrong_pool), (right, right)
        )
    wrong_endpoint = _certified_pool(
        E1_ARM_NAMES[0], "registered-pool", endpoints + 0.01, errors
    )
    with pytest.raises(RegionProtocolError, match="do not match"):
        aggregate_matched_numerical_half_width(
            ensemble, (wrong_endpoint, wrong_endpoint), (right, right)
        )
    wrong_arm = _certified_pool(
        E1_ARM_NAMES[1], "registered-pool", endpoints, errors
    )
    with pytest.raises(RegionProtocolError, match="arm identity"):
        aggregate_matched_numerical_half_width(
            ensemble, (wrong_arm, wrong_arm), (right, right)
        )


def test_item3_radius_encloses_exact_binary64_pair_addition_and_average():
    count = 192
    indices = np.arange(count)
    endpoints = np.zeros((count, 2))
    left_value = 2.1286740303373657
    right_value = 0.8897833198641344
    left_errors = np.full((count, 2), left_value)
    right_errors = np.full((count, 2), right_value)
    laws = []
    left_pools = []
    right_pools = []
    for cohort in range(2):
        pool_identity = f"rounding-{cohort}"
        matching = SimpleNamespace(
            pool_identity=pool_identity,
            result=SimpleNamespace(left_indices=indices, right_indices=indices),
        )
        laws.append(
            SimpleNamespace(
                matched_pairs=count,
                arm_names=E1_ARM_NAMES,
                law_id=JOINT_MATCHED_LAW_ID,
                matching=matching,
                left=endpoints,
                right=endpoints,
            )
        )
        left_pools.append(
            _certified_pool(
                E1_ARM_NAMES[0], pool_identity, endpoints, left_errors
            )
        )
        right_pools.append(
            _certified_pool(
                E1_ARM_NAMES[1], pool_identity, endpoints, right_errors
            )
        )
    ensemble = MatchedLawEnsemble(
        laws=tuple(laws),
        delta_mean=np.zeros(2),
        delta_mean_covariance=np.eye(2),
        total_pairs=2 * count,
        independent_clusters=2,
    )
    radius = aggregate_matched_numerical_half_width(
        ensemble, tuple(left_pools), tuple(right_pools)
    )
    exact = Fraction.from_float(left_value) + Fraction.from_float(right_value)
    assert Fraction.from_float(float(radius.values[0])) >= exact
    assert radius.values[0] == np.nextafter(float(exact), np.inf)


def test_cohort_and_covariance_failures_short_circuit_region_formation():
    too_small_inputs = _inputs(
        [0.0, 0.0], clusters=MIN_INDEPENDENT_COHORTS - 1
    )
    too_small = build_simultaneous_region(
        too_small_inputs,
        local_alpha=0.01,
        numerical_half_width=_validated_radius(too_small_inputs),
    )
    assert too_small.status is RegionStatus.INCONCLUSIVE
    assert too_small.reason is RegionReason.COHORT_TOO_SMALL
    assert too_small.region is None

    outside_inputs = _inputs([0.0, 0.0], pairs_per_cluster=385)
    outside_calibration = build_simultaneous_region(
        outside_inputs,
        local_alpha=0.01,
        numerical_half_width=_validated_radius(outside_inputs),
    )
    assert outside_calibration.status is RegionStatus.INCONCLUSIVE
    assert outside_calibration.reason is RegionReason.PAIR_COUNT_OUTSIDE_CALIBRATION
    assert outside_calibration.region is None

    indefinite_inputs = _inputs(
        [0.0, 0.0], covariance=[[1.0, 2.0], [2.0, 1.0]]
    )
    indefinite = build_simultaneous_region(
        indefinite_inputs,
        local_alpha=0.01,
        numerical_half_width=_validated_radius(indefinite_inputs),
    )
    assert indefinite.reason is RegionReason.COVARIANCE_INVALID
    assert indefinite.region is None

    degenerate_inputs = _inputs(
        [0.0, 0.0], covariance=[[1.0, 0.0], [0.0, 0.0]]
    )
    degenerate = build_simultaneous_region(
        degenerate_inputs,
        local_alpha=0.01,
        numerical_half_width=_validated_radius(degenerate_inputs),
    )
    assert degenerate.reason is RegionReason.DEGENERATE_MARGINAL_VARIANCE
    assert degenerate.region is None


def test_malformed_alpha_numerical_radius_and_identity_fail_closed():
    inputs = _inputs([0.0, 0.0])
    with pytest.raises(RegionProtocolError):
        build_simultaneous_region(
            inputs,
            local_alpha=0.011,
            numerical_half_width=_validated_radius(inputs),
        )
    with pytest.raises(RegionProtocolError):
        build_simultaneous_region(
            inputs,
            local_alpha=0.01,
            numerical_half_width=np.asarray([-1.0, 0.0]),
        )
    wrong_inputs = _inputs([0.0, 0.0], arm_names=E2_PLUS_ARM_NAMES)
    with pytest.raises(RegionProtocolError, match="does not match"):
        build_simultaneous_region(
            inputs,
            local_alpha=0.01,
            numerical_half_width=_validated_radius(wrong_inputs),
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
    inputs = _inputs([np.finfo(float).max, 0.0], covariance=np.eye(2))
    result = build_simultaneous_region(
        inputs,
        local_alpha=0.01,
        numerical_half_width=_validated_radius(
            inputs, [np.finfo(float).max, 0.0]
        ),
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


def test_region_builder_outward_rounds_raw_boundary_before_strict_gates():
    e1_base = _region([0.0, 0.0])
    raw_boundary = ENDPOINT_RANGE_WIDTHS[0] * JOINT_EFFECT_FLOOR
    e1_mean = np.nextafter(
        raw_boundary + e1_base.region.statistical_half_width[0], np.inf
    )
    e1_boundary = _region([e1_mean, 0.0])
    assert e1_boundary.region.lower[0] == raw_boundary
    assert e1_boundary.region.normalized_lower[0] == JOINT_EFFECT_FLOOR
    assert evaluate_e1(e1_boundary).verdict is ScientificVerdict.FAIL

    e2_base = _region([0.0, 0.0], arm_names=E2_PLUS_ARM_NAMES)
    e2_mean = np.nextafter(
        raw_boundary - e2_base.region.statistical_half_width[0], -np.inf
    )
    e2_boundary = _region([e2_mean, 0.0], arm_names=E2_PLUS_ARM_NAMES)
    assert e2_boundary.region.upper[0] == raw_boundary
    assert e2_boundary.region.normalized_upper[0] >= EQUIVALENCE_MARGIN[0]
    assert (
        evaluate_e2(e2_boundary, E2Target.PLUS).verdict
        is ScientificVerdict.FAIL
    )


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
    inputs = _inputs([0.0, 0.0], clusters=31)
    result = build_simultaneous_region(
        inputs,
        local_alpha=0.01,
        numerical_half_width=_validated_radius(inputs),
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
