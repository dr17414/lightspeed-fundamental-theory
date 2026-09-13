"""Candidate-independent regressions for 6a-E statistical regions."""

from dataclasses import replace
from fractions import Fraction
from types import SimpleNamespace

import numpy as np
import pytest

from analysis.stage5c_joint_matched_law import JOINT_MATCHED_LAW_ID, MatchedLawEnsemble
from analysis.stage5c_numerical_certification import (
    CertificationReason,
    CertificationResult,
    CertificationStatus,
    EndpointCertificationProvenance,
    ErrorBudget,
    ImplementationEstimate,
    certify_pairing,
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
    _exact_matched_error_radius,
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


def _implementation(error, identity):
    return ImplementationEstimate(
        np.diag([4.0, 1.0]),
        ErrorBudget(error, 0.0, 0.0, 0.0, 0.0, 1),
        identity,
    )


def _certification(arm_name, pool_identity, row_index, *, error=0.0, clean=True):
    provenance = EndpointCertificationProvenance(
        arm_name=arm_name,
        pool_identity=pool_identity,
        row_index=row_index,
    )
    if clean:
        return certify_pairing(
            _implementation(error, f"{arm_name}-first-{row_index}"),
            _implementation(error, f"{arm_name}-second-{row_index}"),
            provenance=provenance,
        )
    return certify_pairing(
        ImplementationEstimate(
            np.zeros((2, 2)),
            ErrorBudget(0.0, 0.0, 0.0, 0.0, 0.0, 1),
            f"{arm_name}-first-{row_index}",
        ),
        ImplementationEstimate(
            np.zeros((2, 2)),
            ErrorBudget(0.0, 0.0, 0.0, 0.0, 0.0, 1),
            f"{arm_name}-second-{row_index}",
        ),
        provenance=provenance,
    )


def _certified_pool(arm_name, pool_identity, *, errors=(0.0,), clean=True):
    if np.isscalar(errors):
        errors = (float(errors),)
    return CertifiedEndpointPool(
        rows=tuple(
            _certification(
                arm_name, pool_identity, row_index, error=error, clean=clean
            )
            for row_index, error in enumerate(errors)
        )
    )


def _validated_radius(inputs, *, error=0.0):
    pool_identity = f"radius-pool-{'--'.join(inputs.arm_names)}"
    left_pool = _certified_pool(inputs.arm_names[0], pool_identity, errors=error)
    right_pool = _certified_pool(inputs.arm_names[1], pool_identity, errors=error)
    count = inputs.cluster_pair_counts[0]
    indices = np.zeros(count, dtype=np.int64)
    matching = SimpleNamespace(
        pool_identity=pool_identity,
        result=SimpleNamespace(left_indices=indices, right_indices=indices),
    )
    left = np.repeat(left_pool.rows[0].endpoint[None, :], count, axis=0)
    right = np.repeat(right_pool.rows[0].endpoint[None, :], count, axis=0)
    law = SimpleNamespace(
        matched_pairs=count,
        arm_names=inputs.arm_names,
        law_id=JOINT_MATCHED_LAW_ID,
        matching=matching,
        left=left,
        right=right,
    )
    ensemble = MatchedLawEnsemble(
        laws=(law,) * inputs.independent_clusters,
        delta_mean=inputs.estimate,
        delta_mean_covariance=inputs.mean_covariance,
        total_pairs=inputs.total_pairs,
        independent_clusters=inputs.independent_clusters,
    )
    return aggregate_matched_numerical_half_width(
        ensemble,
        (left_pool,) * inputs.independent_clusters,
        (right_pool,) * inputs.independent_clusters,
    )


def _region(estimate, *, arm_names=E1_ARM_NAMES, numerical_error=0.0):
    inputs = _inputs(estimate, arm_names=arm_names)
    return build_simultaneous_region(
        inputs,
        local_alpha=0.01,
        numerical_half_width=_validated_radius(inputs, error=numerical_error),
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
    with_numerical = _region([0.2, 0.0], numerical_error=1.0e-5)
    assert no_numerical.status is RegionStatus.CLEAN
    assert no_numerical.region.reference_df == MIN_INDEPENDENT_COHORTS - 1
    assert with_numerical.region.reference_df != MIN_INDEPENDENT_COHORTS * 192 - 1
    assert all(
        Fraction.from_float(float(standard_error)) ** 2
        >= Fraction.from_float(1.0e-8)
        for standard_error in no_numerical.region.standard_error
    )
    assert np.all(
        with_numerical.region.numerical_half_width
        > no_numerical.region.numerical_half_width
    )
    assert np.all(with_numerical.region.lower < no_numerical.region.lower)
    assert np.all(with_numerical.region.upper > no_numerical.region.upper)
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
    left_pools = tuple(
        _certified_pool(E1_ARM_NAMES[0], pool_id, errors=(1e-8, 9e-8, 2e-8))
        for pool_id in pool_ids
    )
    right_pools = tuple(
        _certified_pool(E1_ARM_NAMES[1], pool_id, errors=(9e-8, 5e-8, 6e-8))
        for pool_id in pool_ids
    )
    matchings = (matching_a, matching_b)
    laws = tuple(
        SimpleNamespace(
            matched_pairs=2,
            arm_names=E1_ARM_NAMES,
            law_id=JOINT_MATCHED_LAW_ID,
            matching=matching,
            left=np.vstack(
                [left_pool.rows[int(index)].endpoint for index in matching.result.left_indices]
            ),
            right=np.vstack(
                [right_pool.rows[int(index)].endpoint for index in matching.result.right_indices]
            ),
        )
        for matching, left_pool, right_pool in zip(
            matchings, left_pools, right_pools, strict=True
        )
    )
    ensemble = MatchedLawEnsemble(
        laws=laws,
        delta_mean=np.zeros(2),
        delta_mean_covariance=np.eye(2),
        total_pairs=4,
        independent_clusters=2,
    )
    radius = aggregate_matched_numerical_half_width(
        ensemble, left_pools, right_pools
    )
    selected = tuple(
        (
            left_pool.rows[int(left_index)].endpoint_error,
            right_pool.rows[int(right_index)].endpoint_error,
        )
        for matching, left_pool, right_pool in zip(
            matchings, left_pools, right_pools, strict=True
        )
        for left_index, right_index in zip(
            matching.result.left_indices, matching.result.right_indices, strict=True
        )
    )
    expected = _exact_matched_error_radius(selected, total_pairs=4)
    assert np.array_equal(radius.values, expected)
    assert not radius.values.flags.writeable
    assert radius.total_pairs == ensemble.total_pairs
    assert radius.arm_names == E1_ARM_NAMES


def test_item3_error_average_does_not_overflow_before_division():
    large = np.full(2, np.finfo(float).max / 4.0)
    radius = _exact_matched_error_radius(
        ((large, large),) * 4,
        total_pairs=4,
    )
    assert np.all(np.isfinite(radius))
    assert np.all(radius >= np.finfo(float).max / 2.0)


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
    left_pool = _certified_pool(E1_ARM_NAMES[0], "malformed")
    right_pool = _certified_pool(E1_ARM_NAMES[1], "malformed")
    with pytest.raises(RegionProtocolError, match="matched indices"):
        aggregate_matched_numerical_half_width(
            ensemble, (left_pool, left_pool), (right_pool, right_pool)
        )


def test_item3_error_pool_requires_clean_frozen_certification_provenance():
    direct = CertificationResult(
        status=CertificationStatus.CLEAN,
        reason=CertificationReason.CERTIFIED,
        agreement_distance=0.0,
        agreement_bound=0.0,
        matrix=np.eye(2),
        matrix_error=0.0,
        norm_lower=1.0,
        norm_upper=1.0,
        endpoint=np.zeros(2),
        endpoint_error=np.zeros(2),
        endpoint_lower=np.zeros(2),
        endpoint_upper=np.zeros(2),
        provenance=EndpointCertificationProvenance(E1_ARM_NAMES[0], "pool", 0),
    )
    assert not direct.producer_authenticated
    with pytest.raises(RegionProtocolError, match="emitted"):
        CertifiedEndpointPool(rows=(direct,))
    with pytest.raises(RegionProtocolError, match="CLEAN"):
        _certified_pool(E1_ARM_NAMES[0], "pool", clean=False)
    first = _certification(E1_ARM_NAMES[0], "pool", 0)
    wrong_row = _certification(E1_ARM_NAMES[0], "pool", 2)
    with pytest.raises(RegionProtocolError, match="row indices"):
        CertifiedEndpointPool(rows=(first, wrong_row))
    other_pool = _certification(E1_ARM_NAMES[0], "other-pool", 1)
    with pytest.raises(RegionProtocolError, match="share producer-bound"):
        CertifiedEndpointPool(rows=(first, other_pool))


def test_item3_certifier_emits_the_pool_identity_consumed_by_the_adapter():
    result = _certification(E1_ARM_NAMES[0], "producer-pool", 0)
    assert result.producer_authenticated
    assert result.provenance == EndpointCertificationProvenance(
        E1_ARM_NAMES[0], "producer-pool", 0
    )
    pool = CertifiedEndpointPool(rows=(result,))
    assert pool.arm_name == E1_ARM_NAMES[0]
    assert pool.pool_identity == "producer-pool"
    assert pool.row_indices == (0,)


def test_validated_numerical_width_has_no_public_construction_path():
    with pytest.raises(TypeError, match="only by matched aggregation"):
        ValidatedNumericalHalfWidth(
            values=np.zeros(2),
            independent_clusters=32,
            total_pairs=32 * 192,
            arm_names=E1_ARM_NAMES,
        )


def test_item3_error_pool_must_match_joint_law_pool_arm_and_endpoint_rows():
    indices = np.asarray([0])
    matching = SimpleNamespace(
        pool_identity="registered-pool",
        result=SimpleNamespace(left_indices=indices, right_indices=indices),
    )
    left = _certified_pool(E1_ARM_NAMES[0], "registered-pool")
    right = _certified_pool(E1_ARM_NAMES[1], "registered-pool")
    endpoints = np.vstack((left.rows[0].endpoint,))
    law = SimpleNamespace(
        matched_pairs=1,
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
        total_pairs=2,
        independent_clusters=2,
    )
    wrong_pool = _certified_pool(E1_ARM_NAMES[0], "other-pool")
    with pytest.raises(RegionProtocolError, match="provenance"):
        aggregate_matched_numerical_half_width(
            ensemble, (wrong_pool, wrong_pool), (right, right)
        )
    wrong_endpoint_law = SimpleNamespace(**{**law.__dict__, "left": endpoints + 0.01})
    wrong_endpoint_ensemble = MatchedLawEnsemble(
        laws=(wrong_endpoint_law, wrong_endpoint_law),
        delta_mean=np.zeros(2),
        delta_mean_covariance=np.eye(2),
        total_pairs=2,
        independent_clusters=2,
    )
    with pytest.raises(RegionProtocolError, match="do not match"):
        aggregate_matched_numerical_half_width(
            wrong_endpoint_ensemble, (left, left), (right, right)
        )
    wrong_arm = _certified_pool(E1_ARM_NAMES[1], "registered-pool")
    with pytest.raises(RegionProtocolError, match="arm identity"):
        aggregate_matched_numerical_half_width(
            ensemble, (wrong_arm, wrong_arm), (right, right)
        )


def test_item3_radius_encloses_exact_binary64_pair_addition_and_average():
    count = 192
    left_value = 2.1286740303373657
    right_value = 0.8897833198641344
    left = np.full(2, left_value)
    right = np.full(2, right_value)
    radius = _exact_matched_error_radius(
        ((left, right),) * count,
        total_pairs=count,
    )
    exact = Fraction.from_float(left_value) + Fraction.from_float(right_value)
    assert Fraction.from_float(float(radius[0])) >= exact
    assert radius[0] == np.nextafter(float(exact), np.inf)


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
        numerical_half_width=_validated_radius(inputs),
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
        raw_boundary + e1_base.region.upper[0], np.inf
    )
    e1_boundary = _region([e1_mean, 0.0])
    assert e1_boundary.region.lower[0] == raw_boundary
    assert e1_boundary.region.normalized_lower[0] == JOINT_EFFECT_FLOOR
    assert evaluate_e1(e1_boundary).verdict is ScientificVerdict.FAIL

    e2_base = _region([0.0, 0.0], arm_names=E2_PLUS_ARM_NAMES)
    e2_mean = np.nextafter(
        raw_boundary - e2_base.region.upper[0], -np.inf
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


def test_e3_equivalence_uses_directed_normalized_bounds_at_raw_rounding_gap():
    arm_names = ("sector-blind-null-A", "sector-blind-null-B")
    base = _region([0.0, 0.0], arm_names=arm_names)
    estimate = np.nextafter(0.15 - base.region.upper[0], -np.inf)
    boundary = _region([estimate, 0.0], arm_names=arm_names)
    assert boundary.region.upper[0] == 0.15
    assert boundary.region.upper[0] < ENDPOINT_RANGE_WIDTHS[0] * JOINT_EFFECT_FLOOR
    assert boundary.region.normalized_upper[0] == EQUIVALENCE_MARGIN[0]
    assert (
        evaluate_e3(boundary, E3Claim.SECTOR_BLIND_NULL).verdict
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
