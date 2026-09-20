"""Candidate-independent falsifier for a CLEAN-implies-small-error shortcut."""

import numpy as np

from analysis.stage5c_e4_wellposedness import E4Status, evaluate_e4_wellposedness
from analysis.stage5c_numerical_certification import CertificationStatus
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

    # These are certified bounds, not observed arm effects.  Even one CLEAN
    # source row cannot be assumed to satisfy a uniform per-row margin cap.
    normalized_error = report.certification.endpoint_error / ENDPOINT_RANGE_WIDTHS
    assert np.all(normalized_error > EQUIVALENCE_MARGIN)
