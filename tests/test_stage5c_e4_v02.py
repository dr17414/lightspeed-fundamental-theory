"""Deterministic v0.2 component checks; never run_screen, RNG, or seed burn."""

from dataclasses import replace
from fractions import Fraction
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from analysis import stage5c_e4_wellposedness as v01
from analysis import stage5c_e4_wellposedness_v02 as v02
from analysis import stage5c_e5_screen as screen
from analysis.stage5c_hard_controls import BlindedCase, MatchResult, order_from_uv
from analysis.stage5c_selector_family import apply_selector
from analysis.stage5c_numerical_certification import (
    CertificationProtocolError,
    CertificationStatus,
    bind_endpoint_certification_rows,
    certify_pairing,
)
from analysis.stage5c_statistical_regions import CertifiedEndpointPool, ENDPOINT_RANGE_WIDTHS
from analysis.stage5c_joint_matched_law import (
    MatchingCertification, MatchingReason, MatchingStatus,
    aggregate_joint_matched_laws, form_joint_matched_law,
)
from analysis.stage5c_statistical_regions import (
    E1_ARM_NAMES, RegionProtocolError, RegionReason, StatisticalRegionInput,
    aggregate_matched_numerical_half_width, build_simultaneous_region,
)


def _enclosure(scale):
    return v02.PairingEnclosure(
        lower=np.zeros(2), upper=np.full(2, scale),
        level_lower=np.zeros((3, 2)), level_upper=np.full((3, 2), scale),
    )


def test_constants_and_identities_match_approved_candidate():
    payload = json.loads((Path(__file__).resolve().parents[1] / "docs" /
                          "stage5c_e4_item7_amendment_candidate_v0.2.json").read_text())
    assert payload["candidate_identities"] == {
        "contract": v02.E4_CONTRACT_ID,
        "gauss_implementation": v02.E4_GAUSS_IMPLEMENTATION_ID,
        "adaptive_implementation": v02.E4_ADAPTIVE_IMPLEMENTATION_ID,
        "enclosure": v02.E4_ENCLOSURE_ID,
    }
    assert payload["unchanged_identities"] == {
        "topology": v02.E4_TOPOLOGY_ID, "leakage": v02.E4_LEAKAGE_ID,
    }
    assert tuple(payload["candidate_constants"]["enclosure_levels"]) == v02.E4_ENCLOSURE_LEVELS
    assert v02.E4_CUBATURE_RTOL == 2.0**-14
    assert v02.E4_CUBATURE_ATOL_CAP == 2.0**-30
    assert (v02.E4_MAX_ATOMS, v02.E4_MAX_SUBDIVISIONS, v02.E4_DENSITY_CHUNK_SIZE) == (8128, 4096, 128)
    assert v01.E4_ENCLOSURE_LEVELS == (16, 32, 64)
    assert v01.E4_CONTRACT_ID.endswith("v0.1")


@pytest.mark.parametrize("exact,expected", [
    (Fraction(0), None),
    (Fraction(1, 2**1075), None),
    (Fraction(3, 2**1076), None),
    (Fraction(3, 2**1075), float.fromhex("0x0.0000000000001p-1022")),
    (Fraction(1, 2**48), 2.0**-48),
    (Fraction(1), 2.0**-30),
])
def test_exact_dyadic_tolerance_zero_underflow_rounding_and_cap(exact, expected):
    scale = float(exact * 2**14)
    assert v02.effective_atol(_enclosure(scale)) == expected
    if expected is not None and expected < v02.E4_CUBATURE_ATOL_CAP:
        assert Fraction.from_float(expected) <= exact
        assert Fraction.from_float(float(np.nextafter(expected, np.inf))) > exact


@pytest.mark.parametrize("scale", [np.inf, np.nan, -1.0])
def test_enclosure_invariant_violations_remain_protocol_errors(scale):
    with pytest.raises(v02.E4ProtocolError):
        _enclosure(scale)


@pytest.mark.parametrize("scale", [0.0, float.fromhex("0x0.0000000000001p-1022")])
def test_undefined_tolerance_skips_adaptive_without_synthetic_payload(monkeypatch, scale):
    # Branch unit test; the real screen seam below uses no mocked producer.
    monkeypatch.setattr(v02, "pairing_enclosure", lambda *args: _enclosure(scale))
    def forbidden(*args, **kwargs):
        raise AssertionError("undefined tolerance must not invoke adaptive")
    monkeypatch.setattr(v02, "_cubature_pairing", forbidden)
    report = v02.evaluate_e4_wellposedness(np.array([[.7, .7, .05, .05]]), np.ones(1), .4)
    assert report.reason is v02.E4Reason.ADAPTIVE_TOLERANCE_UNDEFINED
    assert not report.clean
    for field in ("effective_atol", "adaptive", "adaptive_run", "certification"):
        assert getattr(report, field) is None
    assert report.gauss is not None and report.enclosure is not None
    with pytest.raises(v02.E4ProtocolError, match="null fields"):
        replace(report, effective_atol=0.0)


def test_structural_leakage_precedes_tolerance_derivation(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("leakage failure must stop before tolerance/adaptive")
    monkeypatch.setattr(v02, "effective_atol", forbidden)
    monkeypatch.setattr(v02, "_cubature_pairing", forbidden)
    report = v02.evaluate_e4_wellposedness(
        np.array([[2e-200, 2e-200, 1e-200, 1e-200]]), np.ones(1), .4,
    )
    assert report.reason is v02.E4Reason.STRUCTURAL_LEAKAGE_INVALID
    assert report.status is v02.E4Status.INCONCLUSIVE
    assert not report.leakage.box_leakage_bound_validated
    assert not report.clean
    assert report.enclosure.levels == (64, 128, 256)
    assert all(getattr(report, f) is None for f in
               ("effective_atol", "adaptive", "adaptive_run", "certification"))


@pytest.mark.parametrize("n", [64, 96, 128])
@pytest.mark.parametrize("selector", ["all_relations", "links"])
def test_real_screen_member_classifies_skipped_adaptive_without_namespace_abort(n, selector):
    tail_u = np.linspace(.1, .9, n - 2)
    points = np.vstack(([1e-200, 1e-200], [2e-200, 2e-200],
                        np.column_stack((tail_u, (1.0 - tail_u) * 1e-201))))
    order = order_from_uv(points)
    case = BlindedCase("v02-leakage-seam", order)
    assert apply_selector(selector, (), case).tolist() == [[0, 1]]
    sample = SimpleNamespace(order=order, coordinates=points, theta=.4)
    assert screen._one_member(sample, selector, (), e4_contract="v0.2") == "E4-OR-ITEM3-NONCLEAN"


@pytest.mark.parametrize("atom,expected,subdivisions", [
    ([.70, .70, .05, .05], [.0057989343, .0069587212], 49),
    ([.80, .80, .20, .20], [.0027908232, .0033489878], 68),
    ([.55, .55, .45, .45], [.0195584221, .0234701065], 158),
])
def test_actual_v02_producer_reproduces_development_witnesses(atom, expected, subdivisions):
    report = v02.evaluate_e4_wellposedness(np.array([atom]), np.ones(1), .4)
    assert report.clean and report.reason is v02.E4Reason.CERTIFIED
    assert report.contract_id == v02.E4_CONTRACT_ID
    assert report.enclosure.enclosure_id == v02.E4_ENCLOSURE_ID
    assert report.enclosure.levels == (64, 128, 256)
    assert report.adaptive_run.subdivisions == subdivisions
    assert report.effective_atol == v02.effective_atol(report.enclosure)
    assert np.allclose(report.certification.endpoint_error / ENDPOINT_RANGE_WIDTHS,
                       expected, rtol=2e-8)
    for estimate in (report.gauss, report.adaptive):
        assert estimate.error.quadrature == report.enclosure.error_for(estimate.matrix)
        assert estimate.error.rounding == 0.0


def test_asymmetric_max_policy_and_min_counterfactual_resource_cap(monkeypatch):
    atoms, weights = np.array([[.7, .3, .05, .2]]), np.ones(1)
    report = v02.evaluate_e4_wellposedness(atoms, weights, .4)
    assert report.clean and report.adaptive_run.subdivisions == 83
    assert max(report.enclosure.upper) / min(report.enclosure.upper) > 1e11
    assert np.all(report.certification.endpoint_error / ENDPOINT_RANGE_WIDTHS < 1 / 40)
    def counterfactual(enclosure):
        exact = Fraction.from_float(float(min(enclosure.upper))) / 2**14
        return min(v02.E4_CUBATURE_ATOL_CAP, v02._down_binary64(exact))
    monkeypatch.setattr(v02, "effective_atol", counterfactual)
    failed = v02.evaluate_e4_wellposedness(atoms, weights, .4)
    assert failed.reason is v02.E4Reason.ADAPTIVE_RESOURCE_CAP
    assert not failed.clean and failed.adaptive_run.subdivisions == 4096


@pytest.mark.parametrize("nonfinite,solver_status,expected", [
    (True, "not_converged", v02.E4Reason.NONFINITE_BACKEND),
    (False, "not_converged", v02.E4Reason.ADAPTIVE_RESOURCE_CAP),
    (False, "converged", v02.E4Reason.NUMERICAL_CERTIFICATION_INCONCLUSIVE),
])
def test_post_adaptive_reason_precedence(monkeypatch, nonfinite, solver_status, expected):
    def backend(*args, atol):
        assert 0.0 < atol <= v02.E4_CUBATURE_ATOL_CAP
        return v02.CubatureRun(
            matrix=np.diag([np.nan, 0.0]) if nonfinite else np.zeros((2, 2)),
            error=np.inf if nonfinite else 0.0, rule="genz-malik",
            subdivisions=4096, solver_status=solver_status,
        )
    monkeypatch.setattr(v02, "_cubature_pairing", backend)
    report = v02.evaluate_e4_wellposedness(np.array([[.7, .7, .05, .05]]), np.ones(1), .4)
    assert report.reason is expected
    assert not report.clean


def test_v02_item3_rows_are_rebound_and_v01_seal_cannot_be_reused():
    atoms, weights = np.array([[.8, .8, .2, .2]]), np.ones(1)
    old = v01.evaluate_e4_wellposedness(atoms, weights, .4)
    new = v02.evaluate_e4_wellposedness(atoms, weights, .4)
    assert old.clean and new.clean
    def bind(report):
        return bind_endpoint_certification_rows(
            (report.gauss,), (report.adaptive,),
            arm_name="DEVELOPMENT-ONLY", pool_identity="v02-revalidation-fixture",
        )[0]
    old_row, new_row = bind(old), bind(new)
    assert old_row.provenance.source_row_fingerprint != new_row.provenance.source_row_fingerprint
    certified = certify_pairing(new_row)
    assert certified.status is CertificationStatus.CLEAN
    assert certified.producer_authenticated
    assert np.array_equal(certified.endpoint_error, new.certification.endpoint_error)
    assert CertifiedEndpointPool((certified,)).rows == (certified,)
    object.__setattr__(old_row, "first", new.gauss)
    object.__setattr__(old_row, "second", new.adaptive)
    with pytest.raises(CertificationProtocolError, match="fingerprint|payload|source"):
        certify_pairing(old_row)


def test_actual_v02_rows_rebuild_item4_5_width_and_reject_v01_width():
    # Deterministic component fixture: repeated endpoints are not independent
    # scientific observations. Matching indices are a fixed typed fixture;
    # joint-law, certification, width, and region producers are all real.
    atoms = (np.array([[.8, .8, .2, .2]]), np.array([[.7, .3, .05, .2]]))
    reports = {
        label: tuple(module.evaluate_e4_wellposedness(atom, np.ones(1), .4)
                     for atom in atoms)
        for label, module in (("v01", v01), ("v02", v02))
    }
    assert all(report.clean for group in reports.values() for report in group)
    widths, inputs_by_version = {}, {}
    for version, group in reports.items():
        laws, left_pools, right_pools = [], [], []
        for cohort in range(32):
            pool_id = f"DEVELOPMENT-ONLY-rebinding-{cohort}"
            pools = []
            for side, arm in enumerate(E1_ARM_NAMES):
                report = group[(side + cohort) % 2]
                sources = bind_endpoint_certification_rows(
                    (report.gauss,) * 192, (report.adaptive,) * 192,
                    arm_name=arm, pool_identity=pool_id,
                )
                pools.append(CertifiedEndpointPool(tuple(certify_pairing(row) for row in sources)))
            matching = MatchingCertification(
                status=MatchingStatus.CLEAN, reasons=(MatchingReason.CERTIFIED,),
                result=MatchResult(np.arange(192), np.arange(192), np.zeros(192), 1.0, 0.0, 0.0),
                scale=np.ones(11), calibration_identity=f"DEVELOPMENT-ONLY-calibration-{cohort}",
                pool_identity=pool_id,
            )
            laws.append(form_joint_matched_law(
                matching, np.vstack([row.endpoint for row in pools[0].rows]),
                np.vstack([row.endpoint for row in pools[1].rows]), arm_names=E1_ARM_NAMES,
            ))
            left_pools.append(pools[0])
            right_pools.append(pools[1])
        ensemble = aggregate_joint_matched_laws(tuple(laws))
        assert ensemble.producer_authenticated
        inputs = StatisticalRegionInput.from_ensemble(ensemble)
        width = aggregate_matched_numerical_half_width(ensemble, tuple(left_pools), tuple(right_pools))
        expected = group[0].certification.endpoint_error + group[1].certification.endpoint_error
        assert np.all(width.values >= expected)
        assert np.allclose(width.values, expected, rtol=1e-14, atol=0.0)
        region = build_simultaneous_region(inputs, local_alpha=.007, numerical_half_width=width)
        # E4 characteristic matrices are diagonal: the second endpoint is
        # exactly zero. Preserve the existing zero-variance fail-closed gate.
        assert not region.clean and region.region is None
        assert region.reason is RegionReason.DEGENERATE_MARGINAL_VARIANCE
        widths[version], inputs_by_version[version] = width, inputs
    assert widths["v01"].source_ensemble_fingerprint != widths["v02"].source_ensemble_fingerprint
    with pytest.raises(RegionProtocolError, match="does not match"):
        build_simultaneous_region(inputs_by_version["v02"], local_alpha=.007,
                                  numerical_half_width=widths["v01"])
