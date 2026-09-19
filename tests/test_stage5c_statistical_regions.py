"""Candidate-independent regressions for 6a-E statistical regions."""

from dataclasses import replace
from fractions import Fraction
from types import SimpleNamespace

import numpy as np
import pytest

from analysis.stage5c_joint_matched_law import (
    JOINT_MATCHED_LAW_ID,
    MatchedLawEnsemble,
    _ENSEMBLE_PRODUCER_TOKEN,
    _seal_aggregated_ensemble,
    aggregate_joint_matched_laws,
)
from analysis.stage5c_numerical_certification import (
    CertificationProtocolError,
    CertificationReason,
    CertificationResult,
    CertificationStatus,
    EndpointCertificationProvenance,
    EndpointCertificationSourceRow,
    ErrorBudget,
    ImplementationEstimate,
    RATIO_ERROR_FACTORS,
    bind_endpoint_certification_rows,
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
    RegionBuildResult,
    E2Target,
    E3Claim,
    RegionProtocolError,
    RegionReason,
    RegionStatus,
    ScientificVerdict,
    StatisticalRegionInput,
    ValidatedNumericalHalfWidth,
    _exact_matched_error_radius,
    _REGION_RESULT_PRODUCER_TOKEN,
    _seal_clean_region_result,
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


def _implementation(error, identity):
    return ImplementationEstimate(
        np.diag([4.0, 1.0]),
        ErrorBudget(error, 0.0, 0.0, 0.0, 0.0, 1),
        identity,
    )


def _fixture_ensemble(**kwargs):
    # Test-only synthetic aggregate: boundary tests vary estimate/covariance
    # independently of their deliberately repeated endpoint rows.
    return _seal_aggregated_ensemble(
        MatchedLawEnsemble(**kwargs), producer_token=_ENSEMBLE_PRODUCER_TOKEN
    )


def _boundary_case(result, **replacement):
    # Test-only exact-equality probe for gates. Production results are sealed
    # only inside build_simultaneous_region.
    return _seal_clean_region_result(
        replace(result, region=replace(result.region, **replacement)),
        producer_token=_REGION_RESULT_PRODUCER_TOKEN,
    )


def _certification(arm_name, pool_identity, row_index, *, error=0.0, clean=True):
    matrix = np.diag([4.0, 1.0]) if clean else np.zeros((2, 2))
    errors = (0.0,) * row_index + (float(error),)
    first_rows = tuple(
        ImplementationEstimate(
            matrix,
            ErrorBudget(value, 0.0, 0.0, 0.0, 0.0, 1),
            f"{arm_name}-first-{index}",
        )
        for index, value in enumerate(errors)
    )
    second_rows = tuple(
        ImplementationEstimate(
            matrix,
            ErrorBudget(value, 0.0, 0.0, 0.0, 0.0, 1),
            f"{arm_name}-second-{index}",
        )
        for index, value in enumerate(errors)
    )
    source_rows = bind_endpoint_certification_rows(
        first_rows,
        second_rows,
        arm_name=arm_name,
        pool_identity=pool_identity,
    )
    return certify_pairing(source_rows[row_index])


def _certified_pool(arm_name, pool_identity, *, errors=(0.0,), clean=True):
    if np.isscalar(errors):
        errors = (float(errors),)
    matrix = np.diag([4.0, 1.0]) if clean else np.zeros((2, 2))
    first_rows = tuple(
        ImplementationEstimate(
            matrix,
            ErrorBudget(error, 0.0, 0.0, 0.0, 0.0, 1),
            f"{arm_name}-first-{row_index}",
        )
        for row_index, error in enumerate(errors)
    )
    second_rows = tuple(
        ImplementationEstimate(
            matrix,
            ErrorBudget(error, 0.0, 0.0, 0.0, 0.0, 1),
            f"{arm_name}-second-{row_index}",
        )
        for row_index, error in enumerate(errors)
    )
    source_rows = bind_endpoint_certification_rows(
        first_rows,
        second_rows,
        arm_name=arm_name,
        pool_identity=pool_identity,
    )
    return CertifiedEndpointPool(
        rows=tuple(certify_pairing(source_row) for source_row in source_rows)
    )


def _synthetic_ensemble(
    estimate,
    covariance,
    arm_names,
    cluster_pair_counts,
    *,
    error=0.0,
    pool_tag="radius",
):
    laws = []
    left_pools = []
    right_pools = []
    for cohort_index, count in enumerate(cluster_pair_counts):
        pool_identity = f"{pool_tag}-pool-{'--'.join(arm_names)}-{cohort_index}"
        left_pool = _certified_pool(arm_names[0], pool_identity, errors=error)
        right_pool = _certified_pool(arm_names[1], pool_identity, errors=error)
        indices = np.zeros(count, dtype=np.int64)
        matching = SimpleNamespace(
            calibration_identity=f"{pool_tag}-calibration-{cohort_index}",
            pool_identity=pool_identity,
            result=SimpleNamespace(left_indices=indices, right_indices=indices),
        )
        laws.append(
            SimpleNamespace(
                matched_pairs=count,
                arm_names=arm_names,
                law_id=JOINT_MATCHED_LAW_ID,
                matching=matching,
                left=np.repeat(left_pool.rows[0].endpoint[None, :], count, axis=0),
                right=np.repeat(right_pool.rows[0].endpoint[None, :], count, axis=0),
            )
        )
        left_pools.append(left_pool)
        right_pools.append(right_pool)
    ensemble = _fixture_ensemble(
        laws=tuple(laws),
        delta_mean=np.asarray(estimate, dtype=float),
        delta_mean_covariance=np.asarray(covariance, dtype=float),
        total_pairs=sum(cluster_pair_counts),
        independent_clusters=len(cluster_pair_counts),
    )
    return ensemble, tuple(left_pools), tuple(right_pools)


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
    ensemble, _, _ = _synthetic_ensemble(
        estimate,
        covariance,
        arm_names,
        (pairs_per_cluster,) * clusters,
    )
    return StatisticalRegionInput.from_ensemble(ensemble)


def _validated_radius(inputs, *, error=0.0):
    ensemble, left_pools, right_pools = _synthetic_ensemble(
        inputs.estimate,
        inputs.mean_covariance,
        inputs.arm_names,
        inputs.cluster_pair_counts,
        error=error,
    )
    assert (
        StatisticalRegionInput.from_ensemble(ensemble).source_ensemble_fingerprint
        == inputs.source_ensemble_fingerprint
    )
    return aggregate_matched_numerical_half_width(
        ensemble,
        left_pools,
        right_pools,
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
            matching=SimpleNamespace(
                pool_identity=f"adapter-pool-{cohort_index}",
                calibration_identity=f"adapter-calibration-{cohort_index}",
                result=SimpleNamespace(
                    left_indices=np.arange(192),
                    right_indices=np.arange(192),
                ),
            ),
            left=np.zeros((192, 2)),
            right=np.zeros((192, 2)),
        )
        for cohort_index in range(MIN_INDEPENDENT_COHORTS)
    )
    ensemble = _fixture_ensemble(
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
    assert len(inputs.source_ensemble_fingerprint) == 64


def test_region_adapter_requires_item2_producer_and_fresh_aggregate_payload():
    laws = tuple(
        SimpleNamespace(
            matched_pairs=192,
            arm_names=E1_ARM_NAMES,
            law_id=JOINT_MATCHED_LAW_ID,
            matching=SimpleNamespace(
                pool_identity=f"produced-pool-{index}",
                calibration_identity=f"produced-calibration-{index}",
                result=SimpleNamespace(
                    left_indices=np.arange(192), right_indices=np.arange(192)
                ),
            ),
            left=np.full((192, 2), (0.1 + index * 0.01, 0.0)),
            right=np.zeros((192, 2)),
            delta=np.full((192, 2), (0.1 + index * 0.01, 0.0)),
        )
        for index in range(2)
    )
    forged = MatchedLawEnsemble(
        laws=laws,
        delta_mean=np.array([100.0, 0.0]),
        delta_mean_covariance=np.eye(2),
        total_pairs=384,
        independent_clusters=2,
    )
    with pytest.raises(RegionProtocolError, match="item-2 aggregation"):
        StatisticalRegionInput.from_ensemble(forged)
    with pytest.raises(RegionProtocolError, match="item-2 aggregation"):
        aggregate_matched_numerical_half_width(forged, (), ())

    produced = aggregate_joint_matched_laws(laws)
    assert produced.producer_authenticated
    assert np.allclose(StatisticalRegionInput.from_ensemble(produced).estimate, [0.105, 0.0])
    object.__setattr__(produced, "delta_mean", np.array([100.0, 0.0]))
    with pytest.raises(RegionProtocolError, match="item-2 aggregation"):
        StatisticalRegionInput.from_ensemble(produced)
    produced = aggregate_joint_matched_laws(laws)
    produced.laws[0].left[0, 0] = 9.0
    with pytest.raises(RegionProtocolError, match="item-2 aggregation"):
        StatisticalRegionInput.from_ensemble(produced)


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
        calibration_identity="calibration-a",
        pool_identity=pool_ids[0],
        result=SimpleNamespace(
            left_indices=np.asarray([0, 2]), right_indices=np.asarray([1, 2])
        )
    )
    matching_b = SimpleNamespace(
        calibration_identity="calibration-b",
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
    ensemble = _fixture_ensemble(
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
        calibration_identity="malformed-calibration",
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
    ensemble = _fixture_ensemble(
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
    assert result.provenance.arm_name == E1_ARM_NAMES[0]
    assert result.provenance.pool_identity == "producer-pool"
    assert result.provenance.row_index == 0
    assert len(result.provenance.source_row_fingerprint) == 64
    pool = CertifiedEndpointPool(rows=(result,))
    assert pool.arm_name == E1_ARM_NAMES[0]
    assert pool.pool_identity == "producer-pool"
    assert pool.row_indices == (0,)


def test_item3_provenance_is_bound_to_the_actual_source_row_payload():
    first = (_implementation(1.0e-8, "actual-first"),)
    second = (_implementation(1.0e-8, "actual-second"),)
    source_rows = bind_endpoint_certification_rows(
        first,
        second,
        arm_name=E1_ARM_NAMES[0],
        pool_identity="actual-source-pool",
    )
    with pytest.raises(TypeError, match="only by pool binding"):
        EndpointCertificationSourceRow(
            first=first[0],
            second=second[0],
            provenance=EndpointCertificationProvenance(
                E1_ARM_NAMES[0], "forged-pool", 0
            ),
        )
    with pytest.raises(TypeError, match="unexpected keyword argument"):
        certify_pairing(
            first[0],
            second[0],
            provenance=EndpointCertificationProvenance(
                E1_ARM_NAMES[0], "forged-pool", 0
            ),
        )
    result = certify_pairing(source_rows[0])
    assert result.producer_authenticated
    assert result.provenance == source_rows[0].provenance
    assert len(result.provenance.source_row_fingerprint) == 64
    changed_rows = bind_endpoint_certification_rows(
        (_implementation(1.0e-4, "actual-first"),),
        second,
        arm_name=E1_ARM_NAMES[0],
        pool_identity="actual-source-pool",
    )
    assert (
        changed_rows[0].provenance.source_row_fingerprint
        != source_rows[0].provenance.source_row_fingerprint
    )


def test_bound_source_row_cannot_change_after_binding():
    rows = bind_endpoint_certification_rows(
        (_implementation(1.0e-8, "immutable-first"),),
        (_implementation(1.0e-8, "immutable-second"),),
        arm_name=E1_ARM_NAMES[0],
        pool_identity="immutable-source-pool",
    )
    row = rows[0]
    for estimate in (row.first, row.second):
        with pytest.raises(ValueError):
            estimate.matrix.setflags(write=True)
    assert certify_pairing(row).status is CertificationStatus.CLEAN

    # The checksum is checked at consumption even if a Python caller bypasses
    # the dataclass guard to replace a field rather than changing its array.
    object.__setattr__(row.first, "matrix", np.diag([8.0, 1.0]))
    with pytest.raises(CertificationProtocolError, match="payload changed"):
        certify_pairing(row)


def test_validated_numerical_width_has_no_public_construction_path():
    with pytest.raises(TypeError, match="only by matched aggregation"):
        ValidatedNumericalHalfWidth(
            values=np.zeros(2),
            independent_clusters=32,
            total_pairs=32 * 192,
            arm_names=E1_ARM_NAMES,
        )


def test_validated_width_is_bound_to_the_exact_source_ensemble():
    counts = (192,) * MIN_INDEPENDENT_COHORTS
    first_ensemble, first_left, first_right = _synthetic_ensemble(
        [0.0, 0.0],
        np.diag([1.0e-8, 1.0e-8]),
        E1_ARM_NAMES,
        counts,
        error=0.0,
        pool_tag="first",
    )
    second_ensemble, _, _ = _synthetic_ensemble(
        [0.0, 0.0],
        np.diag([1.0e-8, 1.0e-8]),
        E1_ARM_NAMES,
        counts,
        error=1.0e-5,
        pool_tag="second",
    )
    first_width = aggregate_matched_numerical_half_width(
        first_ensemble, first_left, first_right
    )
    second_inputs = StatisticalRegionInput.from_ensemble(second_ensemble)
    assert first_width.arm_names == second_inputs.arm_names
    assert first_width.independent_clusters == second_inputs.independent_clusters
    assert first_width.total_pairs == second_inputs.total_pairs
    assert first_width.joint_law_id == second_inputs.joint_law_id
    assert (
        first_width.source_ensemble_fingerprint
        != second_inputs.source_ensemble_fingerprint
    )
    with pytest.raises(RegionProtocolError, match="does not match"):
        build_simultaneous_region(
            second_inputs,
            local_alpha=0.01,
            numerical_half_width=first_width,
        )


def test_producer_bound_region_and_width_cannot_be_rewritten():
    ensemble, left_pools, right_pools = _synthetic_ensemble(
        [0.2, 0.0],
        np.diag([1.0e-8, 1.0e-8]),
        E1_ARM_NAMES,
        (192,) * MIN_INDEPENDENT_COHORTS,
        error=1.0e-5,
    )
    inputs = StatisticalRegionInput.from_ensemble(ensemble)
    width = aggregate_matched_numerical_half_width(ensemble, left_pools, right_pools)
    assert np.all(width.values > 0.0)
    for array in (width.values, inputs.estimate, inputs.mean_covariance):
        with pytest.raises(ValueError):
            array.setflags(write=True)
    assert build_simultaneous_region(
        inputs, local_alpha=0.01, numerical_half_width=width
    ).status is RegionStatus.CLEAN

    with pytest.raises(TypeError, match="only from a matched ensemble"):
        StatisticalRegionInput(
            estimate=np.array([0.2, 0.0]),
            mean_covariance=np.diag([1.0e-8, 1.0e-8]),
            independent_clusters=MIN_INDEPENDENT_COHORTS,
            total_pairs=192 * MIN_INDEPENDENT_COHORTS,
            cluster_pair_counts=(192,) * MIN_INDEPENDENT_COHORTS,
            arm_names=E1_ARM_NAMES,
            source_ensemble_fingerprint=width.source_ensemble_fingerprint,
        )


def test_clean_region_bounds_cannot_be_rewritten_before_scientific_gates():
    e1_result = _region([0.0, 0.0])
    region = e1_result.region
    assert region is not None
    for name in (
        "estimate", "lower", "upper", "normalized_lower", "normalized_upper",
        "standard_error", "statistical_half_width", "numerical_half_width",
    ):
        with pytest.raises(ValueError):
            getattr(region, name).setflags(write=True)
    assert evaluate_e1(e1_result).verdict is ScientificVerdict.FAIL

    e2_result = _region([0.2, 0.0], arm_names=E2_PLUS_ARM_NAMES)
    with pytest.raises(ValueError):
        e2_result.region.normalized_upper.setflags(write=True)
    assert evaluate_e2(e2_result, E2Target.PLUS).verdict is ScientificVerdict.FAIL

    e3_result = _region([0.0, 0.0], arm_names=("correct-support", "wrong-support"))
    with pytest.raises(ValueError):
        e3_result.region.lower.setflags(write=True)
    assert (
        evaluate_e3(e3_result, E3Claim.CORRECT_VS_WRONG_SUPPORT).verdict
        is ScientificVerdict.FAIL
    )
    for constant in (ENDPOINT_RANGE_WIDTHS, EQUIVALENCE_MARGIN, RATIO_ERROR_FACTORS):
        with pytest.raises(ValueError):
            constant.setflags(write=True)


def test_scientific_gates_reject_handmade_or_modified_clean_region():
    e1 = _region([0.0, 0.0])
    forged_e1 = RegionBuildResult(
        RegionStatus.CLEAN,
        RegionReason.CERTIFIED,
        replace(e1.region, normalized_lower=np.array([1.0, 0.0])),
    )
    with pytest.raises(RegionProtocolError, match="emitted by the builder"):
        evaluate_e1(forged_e1)
    object.__setattr__(e1, "region", forged_e1.region)
    with pytest.raises(RegionProtocolError, match="emitted by the builder"):
        evaluate_e1(e1)

    e2 = _region([0.2, 0.0], arm_names=E2_PLUS_ARM_NAMES)
    forged_e2 = RegionBuildResult(
        RegionStatus.CLEAN,
        RegionReason.CERTIFIED,
        replace(e2.region, normalized_lower=np.array([-0.01, -0.01]),
                normalized_upper=np.array([0.01, 0.01])),
    )
    with pytest.raises(RegionProtocolError, match="emitted by the builder"):
        evaluate_e2(forged_e2, E2Target.PLUS)

    e3 = _region([0.0, 0.0], arm_names=("correct-support", "wrong-support"))
    forged_e3 = RegionBuildResult(
        RegionStatus.CLEAN,
        RegionReason.CERTIFIED,
        replace(e3.region, lower=np.array([1.0, 0.0]), upper=np.array([2.0, 0.1])),
    )
    with pytest.raises(RegionProtocolError, match="emitted by the builder"):
        evaluate_e3(forged_e3, E3Claim.CORRECT_VS_WRONG_SUPPORT)


def test_item3_error_pool_must_match_joint_law_pool_arm_and_endpoint_rows():
    indices = np.asarray([0])
    matching = SimpleNamespace(
        calibration_identity="registered-calibration",
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
    ensemble = _fixture_ensemble(
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
    wrong_endpoint_ensemble = _fixture_ensemble(
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
    with pytest.raises(TypeError, match="only from a matched ensemble"):
        StatisticalRegionInput(
            estimate=np.zeros(2),
            mean_covariance=np.eye(2),
            independent_clusters=32,
            total_pairs=32,
            cluster_pair_counts=(1,) * 31,
            arm_names=E1_ARM_NAMES,
            source_ensemble_fingerprint="0" * 64,
        )
    with pytest.raises(TypeError, match="only from a matched ensemble"):
        StatisticalRegionInput(
            estimate=np.zeros(2),
            mean_covariance=np.eye(2),
            independent_clusters=32,
            total_pairs=32.0,
            cluster_pair_counts=(1,) * 32,
            arm_names=E1_ARM_NAMES,
            source_ensemble_fingerprint="0" * 64,
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
    equality = _boundary_case(
        equality,
        normalized_lower=np.asarray(
            [JOINT_EFFECT_FLOOR, equality.region.normalized_lower[1]]
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
    equality = _boundary_case(
        equality,
        normalized_upper=np.asarray(
            [EQUIVALENCE_MARGIN[0], equality.region.normalized_upper[1]]
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
    equality = _boundary_case(
        equality,
        lower=np.asarray(
            [E3_WRONG_SUPPORT_EFFECT_FLOOR, equality.region.lower[1]]
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
