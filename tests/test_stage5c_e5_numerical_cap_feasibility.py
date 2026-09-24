"""Candidate-independent falsifier for a CLEAN-implies-small-error shortcut."""

from fractions import Fraction
from math import sqrt

import numpy as np
from scipy import special

from analysis.stage5c_e4_wellposedness import (
    E4Status,
    E4_CUBATURE_ATOL,
    SMEARING_EPSILON,
    evaluate_e4_wellposedness,
    leakage_diagnostics,
)
from analysis.stage5c_hard_controls import BlindedCase, order_from_uv
from analysis.stage5c_measure_prereg import normalised_weights, uniform_pair_weights
from analysis.stage5c_numerical_certification import (
    CertificationStatus,
    bind_endpoint_certification_rows,
    certify_pairing,
)
from analysis.stage5c_selector_family import apply_selector
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


def test_gate_a_deterministic_clean_shortcut_has_selector_e4_counterexample():
    """A real selector handoff can be valid while the E4 leakage gate fails."""

    for n in (64, 96, 128):
        # No RNG or arm data: this is a deterministic point in the full
        # continuous p_theta support.  Both coordinates increase, so the
        # causet is a chain and the real links selector returns N-1 pairs.
        tiny = np.nextafter(0.0, 1.0)
        coordinate = tiny * np.arange(1, n + 1, dtype=float)
        points = np.column_stack((coordinate, coordinate))
        case = BlindedCase(f"gate-a-support-witness-{n}", order_from_uv(points))
        pairs = apply_selector("links", (), case)
        assert pairs.shape == (n - 1, 2)

        # Use the production adapter orientation and production uniform measure.
        atoms = np.concatenate(
            (points[pairs[:, 1]], points[pairs[:, 0]]), axis=1
        )
        weights, normalization = uniform_pair_weights(len(pairs))
        probability = normalised_weights(weights, normalization)
        leakage = leakage_diagnostics(atoms, probability)

        assert leakage.strict_geometry_validated
        assert not leakage.box_leakage_bound_validated
        assert not leakage.causal_leakage_bound_validated
        assert not leakage.structurally_admissible


def test_gate_a_geometric_margin_dominates_registered_uniform_weight_deficit():
    """The proposed geometric core clears both leakage gates without RNG."""

    margin = 1.0e-12
    atom_count_limit = 8128

    # Exhaust the complete registered atom-count range.  The maximum negative
    # exact-dyadic normalization displacement occurs at m=3987 and is tiny
    # relative to the frozen gate excess at the proposed geometric margin.
    worst_deficit = Fraction(0)
    worst_count = 0
    for count in range(1, atom_count_limit + 1):
        weight = Fraction.from_float(float(1.0 / count))
        deficit = 1 - count * weight
        if deficit > worst_deficit:
            worst_deficit = deficit
            worst_count = count
    assert worst_count == 3987
    assert worst_deficit == Fraction(1987, 2**64)

    scaled = 1.0 / (sqrt(2.0) * SMEARING_EPSILON)
    boundary_gain = 0.5 * special.erf(margin * scaled)
    opposite_tail = 0.5 * special.erfc((1.0 - margin) * scaled)
    box_atom_excess = float(
        np.expm1(4.0 * np.log1p(2.0 * (boundary_gain - opposite_tail)))
        / 16.0
    )
    causal_gain = 0.5 * special.erf(margin / (2.0 * SMEARING_EPSILON))
    causal_atom_excess = float(
        np.expm1(2.0 * np.log1p(2.0 * causal_gain)) / 4.0
    )
    exact_weight_sum = 1 - worst_deficit
    box_mixture_excess = (
        -worst_deficit / 16
        + exact_weight_sum * Fraction.from_float(box_atom_excess)
    )
    causal_mixture_excess = (
        -worst_deficit / 4
        + exact_weight_sum * Fraction.from_float(causal_atom_excess)
    )
    assert np.isclose(box_atom_excess, 3.1915382432e-12, rtol=1.0e-11)
    assert np.isclose(causal_atom_excess, 4.5135166684e-12, rtol=1.0e-11)
    assert np.isclose(float(box_mixture_excess), 3.1915315110e-12, rtol=1.0e-11)
    assert np.isclose(
        float(causal_mixture_excess), 4.5134897395e-12, rtol=1.0e-11
    )

    # This is the worst atom count for the exact weight deficit.  Every atom
    # is at least margin from the box boundary and has both causal gaps equal
    # to margin.  The production leakage calculation must still pass both
    # strict gates after accounting for that deficit.
    atoms = np.tile(
        np.asarray([[2.0 * margin, 2.0 * margin, margin, margin]]),
        (worst_count, 1),
    )
    weights, normalization = uniform_pair_weights(worst_count)
    probability = normalised_weights(weights, normalization)
    leakage = leakage_diagnostics(atoms, probability)
    assert leakage.box_leakage_bound_validated
    assert leakage.causal_leakage_bound_validated
    assert leakage.structurally_admissible

    # Under p_theta the one-coordinate marginals are exactly uniform.  A
    # union bound over boundary strips and all unordered coordinate pairs
    # therefore controls the complement of the geometric rule set.
    n = 128
    complement_upper = 4.0 * n * margin + 2.0 * n * (n - 1) * margin
    single_row_budget = 0.10 / (2.0 * 768.0 * 32.0)
    assert np.isclose(complement_upper, 3.3024e-8, rtol=0.0, atol=1.0e-22)
    assert complement_upper < single_row_budget


def test_gate_a_failure_budget_ledger_closes_exactly_without_bucket_recycling():
    """The proof-development buckets and reserve exactly exhaust the envelope."""

    n = 128
    margin = Fraction(1, 10**12)
    cohorts = 32
    rows_per_arm = 768
    clean_failure_budget = Fraction(1, 10)

    row_budget = clean_failure_budget / (2 * rows_per_arm * cohorts)
    geometric_budget = 4 * n * margin + 2 * n * (n - 1) * margin
    remainder = row_budget - geometric_budget
    proof_bucket = remainder / 4

    assert row_budget == Fraction(1, 491520)
    assert geometric_budget == Fraction(129, 3906250000)
    assert remainder == Fraction(48035549, 24000000000000)
    assert proof_bucket == Fraction(48035549, 96000000000000)

    # Three non-recyclable proof buckets plus one unallocated reserve.  The
    # exact identity prevents a rounded table from silently over-spending.
    selector = proof_bucket
    adaptive_backend = proof_bucket
    certification = proof_bucket
    unallocated_reserve = proof_bucket
    assert (
        geometric_budget
        + selector
        + adaptive_backend
        + certification
        + unallocated_reserve
        == row_budget
    )
    assert 2 * rows_per_arm * cohorts * row_budget == clean_failure_budget
