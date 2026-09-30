"""Deterministic, assessment-only probes for a possible item-7 amendment.

These tests do not change the frozen E4 producer.  They compare temporary
development tolerances on candidate-independent atoms without RNG, seeds,
arm data, matching, or a candidate kernel.
"""

import numpy as np

import analysis.stage5c_e4_wellposedness as e4
from analysis.stage5c_e4_wellposedness import E4Status, evaluate_e4_wellposedness
from analysis.stage5c_numerical_certification import CertificationStatus
from analysis.stage5c_statistical_regions import ENDPOINT_RANGE_WIDTHS


def _report(atoms: np.ndarray, atol: float, monkeypatch):
    monkeypatch.setattr(e4, "E4_CUBATURE_ATOL", float(atol))
    return evaluate_e4_wellposedness(
        np.asarray(atoms, dtype=float),
        np.full(len(atoms), 1.0 / len(atoms)),
        theta=0.4,
    )


def _scale_upper_atol(frozen_report) -> float:
    """One development candidate, not a frozen replacement rule."""

    return min(
        2.0**-30,
        (2.0**-14) * float(np.max(frozen_report.enclosure.upper)),
    )


def test_direct_enclosure_width_is_too_loose_but_scaled_upper_clears_witness(
    monkeypatch,
):
    atoms = np.asarray([[0.70, 0.70, 0.05, 0.05]])
    frozen = _report(atoms, 2.0**-30, monkeypatch)
    direct_width = _report(atoms, np.max(frozen.enclosure.widths), monkeypatch)
    scale_upper = _report(atoms, _scale_upper_atol(frozen), monkeypatch)

    assert frozen.status is E4Status.INCONCLUSIVE
    assert direct_width.status is E4Status.INCONCLUSIVE
    assert direct_width.adaptive_run.subdivisions == 0

    assert scale_upper.status is E4Status.CLEAN
    assert scale_upper.certification.status is CertificationStatus.CLEAN
    assert 0 < scale_upper.adaptive_run.subdivisions < e4.E4_MAX_SUBDIVISIONS
    assert scale_upper.certification.norm_lower > 0.0


def test_scaled_upper_changes_existing_clean_error_but_not_wide_cell_mechanism(
    monkeypatch,
):
    near_zero_atoms = np.asarray([[0.80, 0.80, 0.20, 0.20]])
    frozen_near_zero = _report(near_zero_atoms, 2.0**-30, monkeypatch)
    scaled_near_zero = _report(
        near_zero_atoms, _scale_upper_atol(frozen_near_zero), monkeypatch
    )
    frozen_error = frozen_near_zero.certification.endpoint_error / ENDPOINT_RANGE_WIDTHS
    scaled_error = scaled_near_zero.certification.endpoint_error / ENDPOINT_RANGE_WIDTHS

    assert frozen_near_zero.status is E4Status.CLEAN
    assert scaled_near_zero.status is E4Status.CLEAN
    assert np.all(frozen_error > 3.0)
    assert np.all(scaled_error < 1.0 / 40.0)
    assert not np.array_equal(
        frozen_near_zero.certification.endpoint_error,
        scaled_near_zero.certification.endpoint_error,
    )

    # The separate wide-cell witness remains governed by its analytic cell
    # enclosure.  Its scale leaves the frozen absolute cap active, so changing
    # the small-norm policy does not repair that mechanism.
    wide_atoms = np.asarray([[0.55, 0.55, 0.45, 0.45]])
    frozen_wide = _report(wide_atoms, 2.0**-30, monkeypatch)
    assert _scale_upper_atol(frozen_wide) == 2.0**-30
    scaled_wide = _report(wide_atoms, _scale_upper_atol(frozen_wide), monkeypatch)
    assert np.array_equal(
        frozen_wide.certification.endpoint_error,
        scaled_wide.certification.endpoint_error,
    )
