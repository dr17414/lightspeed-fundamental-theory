"""Track B stage 3 regression tests: quantum spectral weight and rhotilde.

SCOPE.  Stage 3 only -- no Wick rotation, no P(s), no spectral dimension.

Each test says which of the four categories it belongs to:
  [SOURCE]   a condition 1502.01655 states, used as an acceptance criterion
  [DERIVED]  a project result, locked as a regression on our own arithmetic,
             explicitly NOT a literature acceptance criterion
  [CONSIST]  agreement between two of our own modules
  [NUMERIC]  a guard on floating-point behaviour, not physics
"""
import os
import sys

import numpy as np
import pytest
from scipy import integrate, optimize

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.track_b_4d_analytic import g_closed                 # noqa: E402
from analysis.track_b_4d_spectral import (                        # noqa: E402
    A_UV, B_UV, CONTINUUM_WEIGHT_DERIVED, RHO_TILDE_AT_ZERO_DIMENSIONLESS,
    B_timelike, W_tilde, g_I, g_R, g_on_lower_bank, rho_continuum,
    rho_continuum_dimensionless,
)

XS = np.logspace(-6, 2, 300)


# ------------------------------------------------------------------ [CONSIST]

def test_cut_values_agree_with_the_stage2_closed_form():
    """[CONSIST] g_R + i g_I must be the stage-2 g_closed evaluated on the lower
    bank.  Stage 3 rewrites it in terms of Ei to keep everything real; if that
    rewriting is wrong, everything downstream is wrong."""
    for x in [1e-4, 1e-2, 0.5, 1.0, 3.0, 10.0, 50.0]:
        assert g_on_lower_bank(x) == pytest.approx(
            complex(g_closed(-x - 1e-25j)), rel=1e-10)


def test_B_is_Lambda_squared_times_g():
    """[SOURCE] Eq.(12): B(p) = Lambda^2 g(Z).  Checked at two scales, so that
    Lambda cannot silently enter with the wrong power."""
    for Lam in [1.0, 3.0]:
        for mu2 in [0.1, 1.0, 10.0]:
            assert B_timelike(mu2, Lam) == pytest.approx(
                Lam**2 * g_on_lower_bank(mu2 / Lam**2), rel=1e-12)


# ------------------------------------------------------------------- [SOURCE]

def test_quantum_positivity_on_the_future_bank():
    """[SOURCE] Eq.(56): sgn Im B = sgn p^0.  For future-directed timelike p,
    which is the lower bank Z = -x - i0 by Eq.(12), Im B > 0."""
    assert np.all(g_I(XS) > 0.0)
    assert np.all(B_timelike(XS).imag > 0.0)


def test_past_bank_has_the_opposite_sign():
    """[SOURCE] The other half of Eq.(56).  Reality of the operator makes the
    two banks conjugate, so past-directed timelike momenta must give Im B < 0."""
    for x in [0.1, 1.0, 10.0]:
        assert complex(g_closed(-x + 1e-25j)).imag < 0.0
        assert complex(g_closed(-x + 1e-25j)).imag == pytest.approx(
            -float(g_I(x)), rel=1e-10)


def test_W_tilde_is_nonnegative():
    """[SOURCE] Eq.(55) with Eq.(56) holding."""
    assert np.all(W_tilde(XS) >= 0.0)


def test_W_tilde_matches_its_definition():
    """[SOURCE] Eq.(55): Wtilde = 2 Im B / |B|^2, term by term."""
    for Lam in [1.0, 2.5]:
        for mu2 in [1e-3, 1.0, 25.0]:
            B = B_timelike(mu2, Lam)
            assert W_tilde(mu2, Lam) == pytest.approx(
                2.0 * B.imag / abs(B) ** 2, rel=1e-12)


def test_rho_is_W_over_two_pi():
    """[SOURCE] Eq.(85): rho(-p^2) = Wtilde(p) / (2 pi) for p^0 > 0."""
    for mu2 in [1e-3, 1.0, 25.0]:
        assert rho_continuum(mu2) == pytest.approx(
            W_tilde(mu2) / (2 * np.pi), rel=1e-12)


def test_rho_continuum_is_positive():
    """[SOURCE] The point of Eq.(56): the continuum spectral density is positive,
    so the quantum theory has no negative-norm continuum states.  This is the
    property Track A is suspected to lack."""
    assert np.all(rho_continuum(XS) > 0.0)


def test_rho_continuum_is_finite_everywhere_including_the_endpoint():
    """[SOURCE] Eq.(86) calls rhotilde a finite function.  Finiteness at
    mu^2 -> 0 is the non-obvious part, since g_R and g_I both vanish there."""
    vals = rho_continuum_dimensionless(np.logspace(-12, 3, 500))
    assert np.all(np.isfinite(vals))
    assert np.all(vals > 0.0)


# ------------------------------------------------------------------ [DERIVED]

def test_massless_endpoint_value():
    """[DERIVED] As x -> 0, g_R ~ x and g_I ~ (pi/2) x^2, so
    g_I/|g|^2 -> pi/2 and Lambda^2 rhotilde(0+) -> 1/2."""
    for x in [1e-8, 1e-10, 1e-12]:
        assert float(rho_continuum_dimensionless(x)) == pytest.approx(
            RHO_TILDE_AT_ZERO_DIMENSIONLESS, rel=1e-5)


def test_large_mass_tail():
    """[DERIVED] The tail is numerator-dominated: g_I becomes negligible against
    g_R, so Lambda^2 rhotilde -> g_I / (pi g_R^2), and the decay is governed by
    the e^{-x/2} in g_I.

    The often-quoted form x^2 e^{-x/2} / 8 substitutes g_R -> -2, but that limit
    is approached only as -2 - 8/x - 48/x^2 and is still 31% off at x = 20 and
    ~8% at x = 100; by the time g_R is within 1% of -2 (x ~ 1e3) the exponential
    has underflowed.  So the useful statement is the one below, not that form.
    """
    for x in [20.0, 30.0, 40.0]:
        gr, gi = float(g_R(x)), float(g_I(x))
        assert gi * gi < 1e-3 * gr * gr
        assert float(rho_continuum_dimensionless(x)) == pytest.approx(
            gi / (np.pi * gr * gr), rel=1e-3)


def test_tail_decay_rate_is_one_half():
    """[DERIVED] -d ln(rhotilde) / dx -> 1/2, the rate set by e^{-x/2} in g_I.
    Stated as a rate so that it is testable in the range where the numbers are
    still representable."""
    x = np.array([20.0, 25.0, 30.0, 35.0, 40.0, 60.0, 100.0])
    ln = np.log(rho_continuum_dimensionless(x))
    slope = np.diff(ln) / np.diff(x)
    assert np.all(slope > -0.5)
    assert np.all(slope < -0.35)
    assert np.all(np.diff(slope) < 0.0)
    assert slope[-1] < -0.47


def test_rho_continuum_decreases_over_the_scanned_range():
    """[NUMERIC OBSERVATION, locked as regression -- NOT proved]

    Over x in [1e-4, 1e2] rhotilde falls monotonically from 1/(2 Lambda^2) and
    shows no resonance peak, even though Re g crosses zero inside this range.
    We have NOT proved d(rhotilde)/dx < 0 for all 0 < x < inf.
    """
    vals = rho_continuum_dimensionless(np.logspace(-4, 2, 600))
    assert np.all(np.diff(vals) < 0.0)


def test_positivity_is_load_bearing_for_stability():
    """[DERIVED] Re g(-x - i0) crosses zero near x0 = 2.6943.  At that mass Im g
    is the only component keeping g away from zero.  Scope: IF g_R is held fixed
    and g_I is driven to zero, an on-cut zero appears at x0; this does not claim
    arbitrary changes to g_I must destabilize the operator there."""
    x0 = optimize.brentq(lambda t: float(g_R(t)), 1.0, 10.0)
    assert x0 == pytest.approx(2.6943105, rel=1e-6)
    assert float(g_I(x0)) > 0.0
    assert abs(complex(g_on_lower_bank(x0))) == pytest.approx(
        float(g_I(x0)), rel=1e-6)
    assert float(rho_continuum_dimensionless(x0)) == pytest.approx(
        1.0 / (np.pi * float(g_I(x0))), rel=1e-8)


def test_continuum_weight_equals_b_over_a_squared_minus_one():
    """[DERIVED -- NOT A LITERATURE CRITERION]

    The analytic argument also depends on stage-2 stability: without the result
    that g has no additional zeros, 1/g would have extra poles and the Cauchy
    argument would fail.  With h(Z) = -1/g(Z) - 1/Z - 1/2, IR residue + UV
    coefficients + stage-2 stability give int dmu^2 rhotilde = b/a^2 - 1 = 1.
    The full rho = delta(mu^2) + rhotilde therefore integrates to 2, not 1.
    """
    tot, err = integrate.quad(
        lambda t: float(rho_continuum_dimensionless(t)), 0.0, 300.0, limit=600)
    assert err < 1e-6
    assert tot == pytest.approx(CONTINUUM_WEIGHT_DERIVED, abs=1e-7)
    assert CONTINUUM_WEIGHT_DERIVED == pytest.approx(B_UV / A_UV**2 - 1.0)


def test_Lambda_enters_only_as_an_overall_inverse_square():
    """[DERIVED] rhotilde(mu^2; Lambda) = Lambda^-2 F(mu^2/Lambda^2)."""
    for Lam in [0.5, 2.0, 7.0]:
        for x in [0.1, 1.0, 8.0]:
            assert rho_continuum(x * Lam**2, Lam) == pytest.approx(
                float(rho_continuum_dimensionless(x)) / Lam**2, rel=1e-12)


# ------------------------------------------------------------------ [NUMERIC]

def test_no_overflow_at_large_mass():
    """[NUMERIC] Large-x g_R switches to its asymptotic series to avoid the
    underflow/overflow product e^{-x/2} Ei(x/2)."""
    assert np.all(np.isfinite(g_R(np.array([1e3, 1e5, 1e8]))))
    for x in [599.0, 601.0]:
        assert float(g_R(x)) == pytest.approx(-2.0 - 8.0 / x - 48.0 / x**2,
                                              rel=1e-6)
