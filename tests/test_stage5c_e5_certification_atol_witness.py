"""Deterministic Gate-A witness for the frozen adaptive absolute tolerance.

The construction uses registered causet sizes and the real selector-to-E4
handoff.  It calls no generator, RNG, seed namespace, arm data, or candidate
kernel.  The lower-tolerance comparison is development-only sensitivity: it
does not amend the frozen producer or certify a replacement constant.
"""

import numpy as np

import analysis.stage5c_e4_wellposedness as e4
from analysis.stage5c_e4_wellposedness import (
    E4Reason,
    E4Status,
    E4_CUBATURE_ATOL,
    evaluate_e4_wellposedness,
)
from analysis.stage5c_hard_controls import BlindedCase, order_from_uv
from analysis.stage5c_measure_prereg import normalised_weights, uniform_pair_weights
from analysis.stage5c_numerical_certification import (
    CertificationReason,
    CertificationStatus,
)
from analysis.stage5c_selector_family import apply_selector


def _single_relation_case(n: int) -> tuple[np.ndarray, BlindedCase]:
    """Embed one causal pair in an otherwise incomparable registered-N case."""

    tail_u = np.linspace(0.951, 0.999, n - 2)
    points = np.vstack(
        (
            [0.05, 0.05],
            [0.70, 0.70],
            np.column_stack((tail_u, 1.0 - tail_u)),
        )
    )
    # This witness lies deep inside the already delivered R_geo rule set:
    # every boundary and same-coordinate pairwise gap is much larger than
    # rho=gamma=1e-12.
    for coordinate in points.T:
        assert np.min(coordinate) > 1.0e-12
        assert np.max(coordinate) < 1.0 - 1.0e-12
        assert np.min(np.diff(np.sort(coordinate))) > 1.0e-12
    return points, BlindedCase(f"gate-a-atol-witness-{n}", order_from_uv(points))


def _production_report(points: np.ndarray, case: BlindedCase, selector: str):
    pairs = apply_selector(selector, (), case)
    assert pairs.tolist() == [[0, 1]]
    atoms = np.concatenate((points[pairs[:, 1]], points[pairs[:, 0]]), axis=1)
    weights, normalization = uniform_pair_weights(len(pairs))
    probability = normalised_weights(weights, normalization)
    return atoms, evaluate_e4_wellposedness(atoms, probability, theta=0.4)


def test_registered_n_real_selector_handoff_hits_item3_under_frozen_atol():
    for n in (64, 96, 128):
        points, case = _single_relation_case(n)
        for selector in ("all_relations", "links"):
            atoms, report = _production_report(points, case, selector)

            assert atoms.tolist() == [[0.70, 0.70, 0.05, 0.05]]
            assert report.leakage.structurally_admissible
            assert report.adaptive_run.converged
            assert report.adaptive_run.subdivisions == 0
            assert E4_CUBATURE_ATOL > np.max(report.enclosure.upper)
            assert np.max(report.enclosure.widths) < 9.0e-14

            # The cell enclosure and fixed-rule budget are narrow, but the
            # zero-subdivision adaptive output lies far below that enclosure.
            assert report.gauss.error.total < 6.4e-14
            assert report.adaptive.error.total > 9.2e-12
            assert report.status is E4Status.INCONCLUSIVE
            assert report.reason is E4Reason.NUMERICAL_CERTIFICATION_INCONCLUSIVE
            assert report.certification.status is CertificationStatus.INCONCLUSIVE
            assert (
                report.certification.reason
                is CertificationReason.NORM_INTERVAL_TOUCHES_ZERO
            )
            assert report.certification.norm_lower < 0.0


def test_development_only_lower_atol_isolates_the_scale_mismatch(monkeypatch):
    points, case = _single_relation_case(64)
    atoms, frozen = _production_report(points, case, "all_relations")

    # This is a counterfactual sensitivity run, not a producer amendment.
    monkeypatch.setattr(e4, "E4_CUBATURE_ATOL", 2.0**-50)
    weights, normalization = uniform_pair_weights(1)
    refined = evaluate_e4_wellposedness(
        atoms, normalised_weights(weights, normalization), theta=0.4
    )

    assert np.array_equal(frozen.gauss.matrix, refined.gauss.matrix)
    assert np.array_equal(frozen.enclosure.lower, refined.enclosure.lower)
    assert np.array_equal(frozen.enclosure.upper, refined.enclosure.upper)
    assert frozen.adaptive_run.subdivisions == 0
    assert refined.adaptive_run.subdivisions > 0
    assert frozen.adaptive.error.total > 9.2e-12
    assert refined.adaptive.error.total < 6.8e-14
    assert frozen.certification.reason is CertificationReason.NORM_INTERVAL_TOUCHES_ZERO
    assert refined.status is E4Status.CLEAN
    assert refined.reason is E4Reason.CERTIFIED
    assert refined.certification.status is CertificationStatus.CLEAN
    assert refined.certification.norm_lower > 9.1e-12
