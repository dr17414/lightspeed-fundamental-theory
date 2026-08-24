"""
Regression tests for the d=2 spectral dimension pipeline.

Every assertion below is a statement made by
  Belenchia, Benincasa, Marciano, Modesto, arXiv:1507.00330 (PRD 93, 044017)
about their own operators.  None is a target we invented.  If a future change
to analysis/spectral_dim_2d.py silently swaps in a different regularization,
a different Wick-rotation convention, or a different P(s), these break.
"""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.spectral_dim_2d import (  # noqa: E402
    A2, B_UV, GAMMA2, build, d_s, d_s_cutoff, g_reg_of,
)

RHO = 1.0


@pytest.fixture(scope="module")
def ops():
    g_of, u_of = build(RHO, npts=241)
    return g_of, u_of, g_reg_of(g_of, u_of, RHO)


def test_gamma2_is_the_general_formula_value():
    """BBMM Eq.(3): gamma_d = (pi/4)^((d-1)/2) / (d Gamma((d+1)/2)); d=2 -> 1/2.

    Eq.(15) as printed carries sqrt(pi)/4 instead.  We lock 1/2 because it is
    confirmed by three independent sources: BBMM's own Eq.(3); Aslanbeigi-
    Saravani-Sorkin arXiv:1403.1622 Eq.(3.6) and Appendix C (which writes
    exp(-rho s^2 / 2) explicitly); and the ASS Eq.(2.5) closed form
    -Z e^{Z/2} E_2(Z/2), matched to machine precision in test_closed_form below.
    This is our own high-confidence typo judgement, not a published erratum.
    """
    from scipy.special import gamma as G
    d = 2
    assert GAMMA2 == pytest.approx((np.pi / 4) ** ((d - 1) / 2) / (d * G((d + 1) / 2)))
    assert GAMMA2 != pytest.approx(np.sqrt(np.pi) / 4)


def test_closed_form_2d(ops):
    """ASS arXiv:1403.1622 Eq.(2.5): rho^{-1} g^(2)(p) = -Z e^{Z/2} E_2(Z/2).

    This is an EXACT closed form for d=2 and is the strongest available check on
    the whole momentum-space construction, superseding the numerical agreement
    with this repo's own derivation.  It also independently fixes a = -2 and
    b = 8 via its Z -> infinity expansion -2 + 8/Z (ASS Eq.(2.8)).
    """
    import mpmath as mp
    mp.mp.dps = 40
    g_of, _, _ = ops
    for k2 in [1e-3, 1e-2, 1e-1, 1.0, 1e1, 1e2, 1e3]:
        Z = mp.mpf(k2) / RHO
        closed = float(RHO * (-Z * mp.exp(Z / 2) * mp.expint(2, Z / 2)))
        assert float(g_of(k2)) == pytest.approx(closed, rel=1e-6)


def test_ir_limit_recovers_box(ops):
    """BBMM Sec.II B: by construction g -> -k^2 as k^2 -> 0, in every dimension."""
    g_of, _, _ = ops
    for k2 in [1e-6, 1e-5, 1e-4]:
        assert float(g_of(k2)) / (-k2) == pytest.approx(1.0, rel=2e-3)


def test_uv_limit_saturates_at_a_rho(ops):
    """BBMM Eq.(4): g -> a rho^{2/d} + b rho^{2/d+1} (k^2)^{-d/2}, a^(2) = -2."""
    g_of, _, _ = ops
    assert float(g_of(1e7)) == pytest.approx(A2 * RHO, abs=1e-5)
    # and the subleading coefficient b is the one the UV branch uses
    for k2 in [1e4, 1e6]:
        assert (float(g_of(k2)) - A2 * RHO) * k2 == pytest.approx(B_UV, rel=1e-3)


def test_regularized_uv_slope(ops):
    """BBMM Eq.(6): g_reg -> -(a^2/b) rho^{2/d-1} (k^2)^{d/2}; d=2 -> -0.5 k^2."""
    _, _, greg = ops
    predicted = -(A2 ** 2) / B_UV
    for k2 in [1e6, 1e8, 1e10]:
        assert float(greg(k2)) / k2 == pytest.approx(predicted, rel=1e-4)


def test_regularized_ir_slope(ops):
    """Regularization must not disturb the IR: g_reg -> -k^2 as well."""
    _, _, greg = ops
    for k2 in [1e-6, 1e-4]:
        assert float(greg(k2)) / k2 == pytest.approx(-1.0, rel=2e-3)


@pytest.mark.parametrize("s", [1e-3, 1e-2, 1e-1, 1.0])
def test_unregularized_ds_is_exactly_four_rho_s(ops, s):
    """BBMM Eq.(14): WITHOUT regularization, d=2 gives d_s = 4 rho s exactly.

    This is the sharpest available check on the P(s) definition and on the
    Euclidean (Wick-rotated) section, because it is an exact closed form.
    """
    g_of, _, _ = ops
    assert d_s_cutoff(g_of, s, lam=1e-8, Lam=1e7) == pytest.approx(4 * RHO * s, rel=1e-4)


def test_regularized_ds_flows_two_to_two_with_a_bump(ops):
    """BBMM Fig.2 (top): in d=2, d_s -> 2 as s -> 0 AND as s -> inf, with a
    maximum above the Hausdorff dimension at s of order the nonlocality scale."""
    _, _, greg = ops
    assert d_s(greg, 1e-4) == pytest.approx(2.0, abs=5e-3)
    assert d_s(greg, 1e4) == pytest.approx(2.0, abs=5e-3)

    # The SHAPE is the acceptance condition: two-to-two with an overshoot.
    # BBMM Fig.2 is a plot, and its caption only says the maximum sits near the
    # nonlocality scale.  We therefore bound the peak loosely and do NOT treat
    # its precise location or height as a literature acceptance criterion.
    ss = np.logspace(-1, 1.5, 12)
    ds = np.array([d_s(greg, s) for s in ss])
    assert ds.max() > 2.15
    peak = ss[int(np.argmax(ds))]
    assert 0.3 < peak < 10.0


def test_ds_never_drops_below_two(ops):
    """d=2 asymptotes the Hausdorff dimension FROM ABOVE (BBMM Sec.IV)."""
    _, _, greg = ops
    for s in np.logspace(-3, 3, 13):
        assert d_s(greg, s) > 1.999
