"""Candidate-independent falsifier for a CLEAN-implies-small-error shortcut."""

import numpy as np

from analysis.stage5c_e4_wellposedness import (
    E4Status,
    E4_CUBATURE_ATOL,
    evaluate_e4_wellposedness,
)
from analysis.stage5c_numerical_certification import (
    CertificationStatus,
    bind_endpoint_certification_rows,
    certify_pairing,
)
from analysis.stage5c_statistical_regions import (
    ENDPOINT_RANGE_WIDTHS,
    EQUIVALENCE_MARGIN,
)


def test_live_e4_clean_does_not_imply_e2_compatible_numerical_width():
    # One fixed-scale, strict-interior analytic Gaussian mixture; no arm,
    # official seed, matched law, or candidate kernel is constructed.
    report = evaluate_e4_wellposedness(
        np.asarray([[0.55, 0.55, 0.45, 0.45]]),
        np.asarray([1.0]),
        theta=0.4,
    )
    assert report.leakage.structurally_admissible
    assert report.status is E4Status.CLEAN
    assert report.certification.status is CertificationStatus.CLEAN
    assert report.certification.producer_authenticated
    assert report.certification.endpoint_error is not None

    # Bind the two live estimates to one audit-only source row; the same large
    # bound survives the exact row-provenance production route used by item 4.
    source_row, = bind_endpoint_certification_rows(
        (report.gauss,), (report.adaptive,),
        arm_name="item8-falsifier-only", pool_identity="item8-no-formal-pool",
    )
    certified = certify_pairing(source_row)
    assert certified.status is CertificationStatus.CLEAN
    assert certified.producer_authenticated
    assert certified.provenance is source_row.provenance
    assert np.array_equal(certified.endpoint_error, report.certification.endpoint_error)

    # These are certified error bounds, not observed scientific arm effects.
    normalized_error = certified.endpoint_error / ENDPOINT_RANGE_WIDTHS
    assert np.all(normalized_error > EQUIVALENCE_MARGIN)


def _audit_only_certification(atoms: list[list[float]]):
    """Rebind candidate-independent E4 estimates; never form an arm endpoint."""

    report = evaluate_e4_wellposedness(
        np.asarray(atoms), np.full(len(atoms), 1.0 / len(atoms)), theta=0.4
    )
    assert report.status is E4Status.CLEAN
    row, = bind_endpoint_certification_rows(
        (report.gauss,), (report.adaptive,),
        arm_name="item8-scaling-audit-only", pool_identity="no-formal-pool",
    )
    certified = certify_pairing(row)
    assert certified.status is CertificationStatus.CLEAN
    assert certified.producer_authenticated
    assert np.array_equal(certified.endpoint_error, report.certification.endpoint_error)
    return report, certified


def test_near_zero_ratio_witness_and_aggregation_counterexamples():
    pathological = [0.8, 0.8, 0.2, 0.2]
    single, single_cert = _audit_only_certification([pathological])
    diluted, diluted_cert = _audit_only_certification(
        [pathological, [0.6, 0.6, 0.4, 0.4]]
    )
    persistent, persistent_cert = _audit_only_certification(
        [pathological, [0.801, 0.801, 0.199, 0.199]]
    )

    # The cell enclosure is narrow.  The adaptive output can nonetheless
    # depart from the fixed output by a large fraction of the tiny norm.
    assert single.leakage.causal_leakage < 1e-9
    assert np.max(single.enclosure.widths) < 4e-12
    assert single.adaptive_run.converged
    assert single.adaptive_run.subdivisions == 0
    assert E4_CUBATURE_ATOL > np.max(single.enclosure.upper)
    assert single_cert.agreement_distance > 3e-10
    assert single_cert.norm_upper / single_cert.norm_lower > 2.0
    assert np.all(single_cert.endpoint_error / ENDPOINT_RANGE_WIDTHS > 3.0)

    # An atom with substantial pairing mass dilutes this one witness; simply
    # increasing the atom count does not guarantee dilution.
    assert diluted_cert.norm_lower > 0.2
    assert np.all(diluted_cert.endpoint_error / ENDPOINT_RANGE_WIDTHS < EQUIVALENCE_MARGIN)
    assert persistent.leakage.causal_leakage < 1e-9
    assert np.all(persistent_cert.endpoint_error / ENDPOINT_RANGE_WIDTHS > 3.0)


def test_boundary_cell_bound_has_no_automatic_atom_count_decay():
    near_diagonal = [0.55, 0.55, 0.45, 0.45]
    single, single_cert = _audit_only_certification([near_diagonal])
    repeated, repeated_cert = _audit_only_certification([near_diagonal] * 4)

    # The Gaussian mixture, causal retained fraction and its wide frozen cell
    # enclosure remain the same after exact equal-weight repetition.
    assert np.isclose(single.leakage.causal_leakage, repeated.leakage.causal_leakage)
    assert np.allclose(single.enclosure.widths, repeated.enclosure.widths, rtol=1e-10)
    assert np.all(single_cert.endpoint_error / ENDPOINT_RANGE_WIDTHS > EQUIVALENCE_MARGIN)
    assert np.all(repeated_cert.endpoint_error / ENDPOINT_RANGE_WIDTHS > EQUIVALENCE_MARGIN)
    assert np.allclose(single_cert.endpoint_error, repeated_cert.endpoint_error, rtol=1e-10)
