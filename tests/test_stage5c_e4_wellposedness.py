"""Candidate-independent regressions for 6a-E closure item 7."""

from types import SimpleNamespace

import numpy as np
import pytest
from scipy import special

import analysis.stage5c_e4_wellposedness as e4
from analysis.stage5c_e4_wellposedness import (
    E4_ADAPTIVE_IMPLEMENTATION_ID,
    E4_CUBATURE_ATOL,
    E4_CUBATURE_RTOL,
    E4_DENSITY_CHUNK_SIZE,
    E4_ENCLOSURE_LEVELS,
    E4_GAUSS_IMPLEMENTATION_ID,
    E4_GAUSS_ORDER,
    E4_MAX_SUBDIVISIONS,
    E4_MAX_ATOMS,
    E4_OUTWARD_ULPS,
    E4_THETA_SUITE,
    E4_TRANSVERSE_DIVISOR,
    E4ProtocolError,
    E4Reason,
    E4Status,
    conformal_density_lower_bound,
    evaluate_e4_wellposedness,
    leakage_diagnostics,
    pairing_operator_sup_bound,
)
from analysis.stage5c_hard_controls import CONTROL_THETA
from analysis.stage5c_measure_prereg import SMEARING_EPSILON
from analysis.stage5c_numerical_certification import CertificationReason


INTERIOR_ATOMS = np.asarray(
    [
        [0.72, 0.81, 0.31, 0.22],
        [0.61, 0.58, 0.24, 0.19],
        [0.43, 0.67, 0.11, 0.37],
    ],
    dtype=float,
)
INTERIOR_WEIGHTS = np.asarray([0.2, 0.5, 0.3], dtype=float)


def test_fixed_scale_and_numerical_resource_contract_are_not_caller_tuned():
    assert SMEARING_EPSILON == 1.0 / 16.0
    assert E4_THETA_SUITE == (-CONTROL_THETA, 0.0, CONTROL_THETA)
    assert E4_GAUSS_ORDER == 32
    assert E4_CUBATURE_RTOL == 2.0**-14
    assert E4_CUBATURE_ATOL == 2.0**-30
    assert E4_MAX_SUBDIVISIONS == 4096
    assert E4_MAX_ATOMS == 8128
    assert E4_DENSITY_CHUNK_SIZE == 128
    assert E4_ENCLOSURE_LEVELS == (16, 32, 64)
    assert E4_TRANSVERSE_DIVISOR == 4
    assert E4_OUTWARD_ULPS == 64


def test_gaussian_topology_rejects_boundary_contact_and_nonprobability_inputs():
    variants = (
        (np.asarray([[1.0, 0.8, 0.2, 0.1]]), np.asarray([1.0])),
        (np.asarray([[0.8, 0.8, 0.8, 0.1]]), np.asarray([1.0])),
        (np.asarray([[0.8, 0.8, 0.2, 0.1]]), np.asarray([0.9])),
        (np.asarray([[0.8, 0.8, 0.2, 0.1]]), np.asarray([-1.0])),
    )
    for atoms, weights in variants:
        with pytest.raises(E4ProtocolError):
            leakage_diagnostics(atoms, weights)
    with pytest.raises(E4ProtocolError):
        leakage_diagnostics(
            np.tile(np.asarray([[0.8, 0.8, 0.2, 0.2]]), (E4_MAX_ATOMS + 1, 1)),
            np.full(E4_MAX_ATOMS + 1, 1.0 / (E4_MAX_ATOMS + 1)),
        )


def test_box_and_causal_leakage_are_analytic_reported_and_not_renormalised():
    report = leakage_diagnostics(INTERIOR_ATOMS, INTERIOR_WEIGHTS)
    epsilon = SMEARING_EPSILON
    coordinate_mass = special.ndtr((1.0 - INTERIOR_ATOMS) / epsilon) - special.ndtr(
        -INTERIOR_ATOMS / epsilon
    )
    expected_box = float(INTERIOR_WEIGHTS @ np.prod(coordinate_mass, axis=1))
    gaps = INTERIOR_ATOMS[:, :2] - INTERIOR_ATOMS[:, 2:]
    expected_causal = float(
        INTERIOR_WEIGHTS
        @ np.prod(special.ndtr(gaps / (np.sqrt(2.0) * epsilon)), axis=1)
    )
    assert report.box_retained_mass == expected_box
    assert report.box_leakage >= 1.0 - expected_box
    assert report.causal_retained_mass == expected_causal
    assert report.causal_leakage >= 1.0 - expected_causal
    assert report.exact_contact_atom_mass == 0.0
    assert report.structurally_admissible


def test_resolvable_interior_margins_satisfy_simple_leakage_bounds():
    tiny = np.nextafter(0.0, 1.0)
    almost_one = np.nextafter(1.0, 0.0)
    atoms = np.asarray([[almost_one, almost_one, tiny, tiny]])
    report = leakage_diagnostics(atoms, np.asarray([1.0]))
    assert report.box_leakage < 15.0 / 16.0
    assert report.causal_leakage < 0.75


def test_sub_ulp_strict_geometry_is_not_rejected_by_rounded_cdf_diagnostics():
    import mpmath as mp

    tiny = np.nextafter(0.0, 1.0)
    atoms = np.asarray([[2.0 * tiny, 2.0 * tiny, tiny, tiny]])
    report = leakage_diagnostics(atoms, np.asarray([1.0]))
    assert report.strict_geometry_validated
    assert report.box_retained_mass == 1.0 / 16.0
    assert report.box_leakage >= 15.0 / 16.0
    assert report.causal_retained_mass == 0.25
    assert report.causal_leakage >= 0.75
    assert report.structurally_admissible

    # At sufficient precision, the opposite-boundary tail is larger than the
    # positive subnormal displacement: the exact box mass is below 1/16.  The
    # valid strict bound uses the open-boundary limit instead.
    with mp.workdps(400):
        epsilon = mp.mpf(1) / 16
        centre = mp.mpf(float(tiny))
        phi = lambda value: (1 + mp.erf(value / mp.sqrt(2))) / 2
        centres = (2 * centre, 2 * centre, centre, centre)
        coordinate_masses = tuple(
            phi((1 - value) / epsilon) - phi(-value / epsilon)
            for value in centres
        )
        boundary_limit = mp.mpf("0.5") - phi(-1 / epsilon)
        exact_box_leakage = 1 - mp.fprod(coordinate_masses)
        valid_upper_limit = 1 - boundary_limit**4
        assert all(
            boundary_limit < value < mp.mpf("0.5")
            for value in coordinate_masses
        )
        assert mp.mpf(15) / 16 < exact_box_leakage < valid_upper_limit


def test_order_zero_pairing_bound_is_derived_from_the_complete_theta_domain():
    assert conformal_density_lower_bound(-CONTROL_THETA) == pytest.approx(0.6)
    assert conformal_density_lower_bound(CONTROL_THETA) == pytest.approx(0.8)
    assert pairing_operator_sup_bound(-CONTROL_THETA) == pytest.approx(
        1.0 / np.sqrt(1.2)
    )
    assert pairing_operator_sup_bound(CONTROL_THETA) == pytest.approx(
        1.0 / np.sqrt(1.6)
    )
    with pytest.raises(E4ProtocolError):
        pairing_operator_sup_bound(CONTROL_THETA + 0.01)


@pytest.mark.parametrize("theta", E4_THETA_SUITE)
def test_two_live_error_paths_certify_the_fixed_gaussian_pairing(theta):
    report = evaluate_e4_wellposedness(INTERIOR_ATOMS, INTERIOR_WEIGHTS, theta)
    assert report.status is E4Status.CLEAN
    assert report.clean
    assert report.gauss.implementation_id == E4_GAUSS_IMPLEMENTATION_ID
    assert report.adaptive.implementation_id == E4_ADAPTIVE_IMPLEMENTATION_ID
    assert report.adaptive_run.rule == "genz-malik"
    assert report.adaptive_run.converged
    assert report.reason is E4Reason.CERTIFIED
    assert report.gauss.error.quadrature > 0.0
    assert report.adaptive.error.quadrature > 0.0
    diagonal_values = np.stack(
        (report.gauss.matrix.diagonal().real, report.adaptive.matrix.diagonal().real)
    )
    assert np.all(diagonal_values >= report.enclosure.lower)
    assert np.all(diagonal_values <= report.enclosure.upper)
    assert np.array_equal(
        report.enclosure.lower, np.max(report.enclosure.level_lower, axis=0)
    )
    assert np.array_equal(
        report.enclosure.upper, np.min(report.enclosure.level_upper, axis=0)
    )
    level_widths = report.enclosure.level_upper - report.enclosure.level_lower
    assert np.all(np.diff(level_widths, axis=0) < 0.0)
    for estimate in (report.gauss, report.adaptive):
        assert estimate.error.sampling_representation == 0.0
        assert estimate.error.regulator == 0.0
        assert estimate.error.boundary_contact == 0.0
        assert estimate.error.rounding == 0.0
    assert report.certification.reason is CertificationReason.CERTIFIED


def test_adaptive_error_estimate_is_diagnostic_not_a_validated_budget():
    report = evaluate_e4_wellposedness(
        INTERIOR_ATOMS, INTERIOR_WEIGHTS, CONTROL_THETA
    )
    assert report.adaptive_run.error < report.adaptive.error.quadrature
    assert report.adaptive.error.quadrature == report.enclosure.error_for(
        report.adaptive.matrix
    )


def test_adaptive_resource_exhaustion_is_inconclusive(monkeypatch):
    def exhausted(*args, **kwargs):
        return SimpleNamespace(
            estimate=np.asarray([0.004, 0.0, 0.002, 0.0]),
            error=np.zeros(4),
            subdivisions=E4_MAX_SUBDIVISIONS,
            status="not_converged",
        )

    monkeypatch.setattr(e4.integrate, "cubature", exhausted)
    report = evaluate_e4_wellposedness(
        INTERIOR_ATOMS, INTERIOR_WEIGHTS, CONTROL_THETA
    )
    assert report.status is E4Status.INCONCLUSIVE
    assert report.reason is E4Reason.ADAPTIVE_RESOURCE_CAP
    assert not report.clean


def test_nonfinite_adaptive_backend_is_inconclusive(monkeypatch):
    def nonfinite(*args, **kwargs):
        return SimpleNamespace(
            estimate=np.asarray([np.nan, 0.0, 0.002, 0.0]),
            error=np.full(4, np.inf),
            subdivisions=1,
            status="converged",
        )

    monkeypatch.setattr(e4.integrate, "cubature", nonfinite)
    report = evaluate_e4_wellposedness(
        INTERIOR_ATOMS, INTERIOR_WEIGHTS, CONTROL_THETA
    )
    assert report.status is E4Status.INCONCLUSIVE
    assert report.reason is E4Reason.NONFINITE_BACKEND
    assert report.certification.reason is CertificationReason.NONFINITE_BACKEND
    assert not report.clean


def test_nonfinite_adaptive_error_with_finite_matrix_is_inconclusive(monkeypatch):
    def nonfinite_error(*args, **kwargs):
        return SimpleNamespace(
            estimate=np.asarray([0.004, 0.0, 0.002, 0.0]),
            error=np.full(4, np.inf),
            subdivisions=1,
            status="converged",
        )

    monkeypatch.setattr(e4.integrate, "cubature", nonfinite_error)
    report = evaluate_e4_wellposedness(
        INTERIOR_ATOMS, INTERIOR_WEIGHTS, CONTROL_THETA
    )
    assert np.all(np.isfinite(report.adaptive.matrix))
    assert not np.isfinite(report.adaptive_run.error)
    assert report.status is E4Status.INCONCLUSIVE
    assert report.reason is E4Reason.NONFINITE_BACKEND
    assert not report.clean


def test_boundary_near_and_near_contact_plants_remain_well_defined():
    atoms = np.asarray(
        [
            [0.999, 0.999, 0.001, 0.001],
            [0.5002, 0.7002, 0.5001, 0.7001],
        ]
    )
    report = evaluate_e4_wellposedness(atoms, np.asarray([0.5, 0.5]), CONTROL_THETA)
    assert report.clean
    assert report.leakage.box_leakage > 0.0
    assert report.leakage.causal_leakage > 0.0


@pytest.mark.parametrize("theta", (-0.41, 0.41, np.nan, np.inf))
def test_unregistered_theta_fails_before_any_pairing(theta):
    with pytest.raises(E4ProtocolError):
        evaluate_e4_wellposedness(INTERIOR_ATOMS, INTERIOR_WEIGHTS, theta)
