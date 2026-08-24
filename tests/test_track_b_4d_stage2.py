"""Track B stage 1-2 regression tests (arXiv:1502.01655 4D concrete operator).

SCOPE.  Stage 1-2 only.  Nothing here touches the quantum spectral weight W(p),
the spectral density rho(mu^2), the Wick rotation, P(s) or d_s.

These complement, and do not replace, tests/test_track_b_4d.py, which locks the
source-faithful kernel (a, delta_+ normalization, A9/A10/A11 moment conditions).
What is added here:

  1. the derived identity g = -Z e^{Z/2} E_2(Z/2), asserted rather than assumed,
     against BOTH integral implementations;
  2. a regression guard on the catastrophic IR cancellation, which used to make
     the stage-1 direct integral return the WRONG SIGN below Z ~ 1e-7 without
     raising, and which analysis/track_b_4d.py now refuses outright;
  3. the boundary values on the timelike cut, and the resulting
     argument-principle zero count (Eq. A37 stability).
"""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.track_b_4d import Z_MIN_DIRECT, g_spacelike        # noqa: E402
from analysis.track_b_4d_analytic import (                       # noqa: E402
    g_closed, g_closed_E2, im_g_A33, im_g_on_lower_cut, ir_correction,
    winding_number,
)
from analysis.track_b_4d_irsafe import R as R_sub                # noqa: E402
from analysis.track_b_4d_irsafe import g_ir_safe                 # noqa: E402


# ---------------------------------------------------------------- identities

def test_E1_and_E2_forms_agree():
    """E_2(w) = e^{-w} - w E_1(w), so the two closed forms are one function.
    Checked off the real axis too, since stage 2 needs the whole cut plane."""
    for Z in [0.1, 1.0, 5.0, 2 + 3j, -1 + 0.5j, 0.3 - 2j, -4 - 1j]:
        assert g_closed(Z) == pytest.approx(g_closed_E2(Z), rel=1e-12)


def test_closed_form_matches_the_source_faithful_integral():
    """The identity that licenses using the closed form at all.

    Definition of record is the Eq.(13)/(A36) integral in analysis/track_b_4d.py;
    1502.01655 does not contain this closed form.  If the identity is ever
    wrong, this is what says so.
    """
    # Upper end stops where the stage-1 quadrature is still trustworthy; the
    # large-Z behaviour of the closed form is checked separately against the
    # arbitrary-precision E_2 reference in test_closed_form_survives_large_Z.
    # Tolerance is set by the direct integral's own accuracy, which degrades
    # towards the IR end of its permitted range (1.4e-7 at Z = Z_MIN_DIRECT,
    # 3.8e-10 by Z = 1e-2), not by any doubt about the identity.
    for Z in [1e-4, 1e-2, 1e-1, 0.5, 1.0, 3.0, 10.0, 1e2, 1e3]:
        assert g_spacelike(Z) == pytest.approx(
            float(g_closed(Z).real), rel=1e-6)


def test_closed_form_matches_the_ir_safe_integral():
    """Same identity at the other end, where the direct integral cannot go."""
    for Z in [1e-10, 1e-8, 1e-6, 1e-4, 1e-2]:
        assert g_ir_safe(Z) == pytest.approx(float(g_closed(Z).real), rel=1e-6)


def test_g_is_imaginary_free_on_the_spacelike_axis():
    """Z > 0 is off the cut, so g is real there."""
    for Z in [1e-3, 1.0, 1e3]:
        assert abs(g_closed(Z).imag) < 1e-12 * abs(g_closed(Z).real)


# ------------------------------------------------- the IR cancellation defect

def test_ir_limit_holds_far_below_the_direct_integral_s_reach():
    """A8: g(Z) -> -Z, tested against the EXACT first correction rather than
    against 1.

    g/(-Z) - 1 = -(Z/2)(ln(2/Z) - gamma) is a real analytic correction: it is
    7e-6 at Z = 1e-6.  Demanding g/(-Z) = 1 to better than that would fail a
    correct implementation, which is what the first draft of this test did.
    """
    for Z in [1e-4, 1e-6, 1e-8]:
        observed = g_ir_safe(Z) / (-Z) - 1.0
        assert observed == pytest.approx(float(ir_correction(Z)), rel=2e-3)

    # The IR-safe integral has a floor of its own, four decades below the
    # stage-1 form but not infinitely far: at Z = 1e-10 it still gets the
    # LEADING term right, while the correction term is only good to ~30%.
    # Recorded rather than hidden, so nobody reads "IR-safe" as "exact".
    Z = 1e-10
    assert g_ir_safe(Z) / (-Z) == pytest.approx(1.0, rel=1e-8)
    ratio = (g_ir_safe(Z) / (-Z) - 1.0) / float(ir_correction(Z))
    assert 0.5 < ratio < 1.5


def test_ir_safe_convergence_is_monotone():
    """The stage-1 form fails this: its g/(-Z) turns back away from 1 below
    Z ~ 1e-5 as cancellation noise takes over."""
    err = [abs(g_ir_safe(Z) / (-Z) - 1.0) for Z in [1e-3, 1e-5, 1e-7, 1e-9]]
    assert all(b < a for a, b in zip(err, err[1:]))


def test_closed_form_survives_large_Z():
    """Naively, e^{Z/2} overflows and E_1(Z/2) underflows past Z ~ 1418, and
    their product comes out nan.  The scaled evaluator must not."""
    for Z in [1e2, 1e3, 1e4, 1e6]:
        v = g_closed(Z)
        assert np.isfinite(v.real)
        assert v.real == pytest.approx(float(g_closed_E2(Z).real), rel=1e-8)


def test_direct_integral_refuses_the_deep_ir_instead_of_returning_garbage():
    """The stage-1 direct integral used to return a POSITIVE number below
    Z ~ 1e-7, silently, where g must be negative for all Z > 0.  It now refuses.

    Keeping only a correct alternative path would not have closed the bug: a
    public function that quietly returns the wrong sign is still reachable.  So
    the guard itself is asserted here, together with the fact that it does not
    encroach on the range the direct integral genuinely handles.
    """
    assert float(g_closed(1e-9).real) < 0.0
    with pytest.raises(ValueError):
        g_spacelike(1e-9)
    with pytest.raises(ValueError):
        g_spacelike(Z_MIN_DIRECT / 10.0)
    # still usable where it is valid, and agreeing with the closed form there
    assert g_spacelike(Z_MIN_DIRECT) == pytest.approx(
        float(g_closed(Z_MIN_DIRECT).real), rel=1e-5)


def test_R_subtraction_is_accurate_at_small_argument():
    """R(x) = K_1(x) - 1/x - (x/2)ln(x/2) - (x/4)(2 gamma - 1) = O(x^3 ln x).
    Computing it as written loses the very cancellation it exists to avoid, so
    the series branch is checked against a 40-digit reference."""
    mp = pytest.importorskip("mpmath")
    mp.mp.dps = 40
    for x in [1e-4, 1e-3, 1e-2, 0.1, 1.0]:
        ref = float(mp.besselk(1, x) - 1 / mp.mpf(x)
                    - (mp.mpf(x) / 2) * mp.log(mp.mpf(x) / 2)
                    - (mp.mpf(x) / 4) * (2 * mp.euler - 1))
        assert float(R_sub(x)) == pytest.approx(ref, rel=1e-12)


# ------------------------------------------------------- cut and boundary values

def test_lower_cut_edge_reproduces_the_A33_choice():
    """Im g(-x - i0) = (pi/2) x^2 e^{-x/2}, which is exactly the g_I that
    1502.01655 Eq.(A33) selects and then reconstructs the kernel f from.  This
    is the analytic half of the cross-paper identification."""
    for x in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
        assert float(im_g_on_lower_cut(x)) == pytest.approx(
            float(im_g_A33(x)), rel=1e-10)


def test_the_two_edges_are_conjugate_and_the_lower_one_is_positive():
    """Reality of the operator forces g(Zbar) = conj(g(Z)), so the two banks are
    conjugate.  Which one is physical is fixed by 1502.01655 Eq.(12): with
    Z = (p + i p_eps)^2 / Lambda^2 and p_eps infinitesimal future-directed
    timelike in (-+++) signature, future-directed timelike p gives p.p_eps < 0,
    hence Im Z < 0 -- the LOWER bank.  Appendix A.3 states the same from the
    other direction (Im g > 0 below the cut), which is what is asserted here.
    """
    for x in [0.5, 2.0, 8.0]:
        lo = float(g_closed(-x - 1e-25j).imag)
        up = float(g_closed(-x + 1e-25j).imag)
        assert lo == pytest.approx(-up, rel=1e-10)
        assert lo > 0.0


def test_no_zeros_on_the_cut():
    """Zeros on the cut are not enclosed by the contour used below, so they are
    excluded here instead: Im g > 0 strictly for x > 0, hence g != 0.  This is
    the mechanism of the paper's positivity-implies-stability argument
    (A38-A42), so the two stability routes meet at this assertion."""
    x = np.logspace(-3, 2, 400)
    assert np.all(im_g_on_lower_cut(x) > 0.0)


# ----------------------------------------------------------------- stability

@pytest.mark.parametrize("R,eps,n", [(20.0, 1e-4, 2000),
                                     (100.0, 1e-6, 3000),
                                     (300.0, 1e-6, 4000)])
def test_argument_principle_finds_no_zeros_besides_the_origin(R, eps, n):
    """Eq.(A37): stability requires g(Z) != 0 for every Z != 0.

    The contour is the boundary of {eps < |Z| < R} on the cut plane, so the
    simple zero at the origin is excluded and a stable operator must give 0.
    """
    assert winding_number(R, eps, n) == pytest.approx(0.0, abs=1e-3)


def test_winding_number_detects_a_planted_zero():
    """Sanity check on the counter itself: a control function with one known
    zero inside the contour must return 1, so that the 0 above is a real
    statement about g and not an artefact of the contour bookkeeping."""
    import analysis.track_b_4d_analytic as mod

    real_g = mod.g_closed
    try:
        mod.g_closed = lambda Z: np.asarray(Z, dtype=np.complex128) - (3.0 + 1.0j)
        assert mod.winding_number(20.0, 1e-4, 2000) == pytest.approx(1.0, abs=1e-3)
    finally:
        mod.g_closed = real_g
