"""Stage-1 regression tests for arXiv:1502.01655 Track B 4D operator."""
import os
import sys
import numpy as np
import pytest
from scipy import integrate

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analysis.track_b_4d import A, DELTA_COEFF, f_smooth, delta_g, g_spacelike


def test_source_constants_a36():
    assert A == -2.0
    assert DELTA_COEFF == pytest.approx(4.0 / np.pi)


def test_delta_plus_contribution_is_8_over_Z():
    # Direct finite-epsilon evaluation of the distributional term in Eq. A7:
    # 4*pi Z^-1/2 * (4/pi) * (sqrt(eps)/2) K1(sqrt(Z eps)) -> 8/Z.
    from scipy.special import kv
    for Z in [1e-2, 1.0, 1e2]:
        target = 8.0 / Z
        for eps in [1e-8, 1e-10, 1e-12]:
            finite_eps = (8.0 * np.sqrt(eps) / np.sqrt(Z)) * kv(1, np.sqrt(Z * eps))
            assert finite_eps == pytest.approx(target, rel=5e-6)
        assert delta_g(Z) == pytest.approx(target)


def test_ir_moments_a9():
    # A9: int f(s^2) s^(2k+1) ds = 0, k=0,1,2.
    # For delta_+, only k=0 survives in eps->0: alpha/2 = 2/pi.
    for k in [0, 1, 2]:
        smooth, _ = integrate.quad(
            lambda s: float(f_smooth(s*s)) * s**(2*k+1),
            0.0, np.inf, epsabs=1e-13, epsrel=1e-12,
        )
        delta = DELTA_COEFF / 2.0 if k == 0 else 0.0
        assert smooth + delta == pytest.approx(0.0, abs=2e-11)


def test_ir_log_moment_a10():
    # A10: int f(s^2) s^5 ln(s) ds = -4/pi.
    # delta_+ term vanishes as eps^2 ln eps.
    val, _ = integrate.quad(
        lambda s: float(f_smooth(s*s)) * s**5 * np.log(s),
        0.0, np.inf, epsabs=1e-12, epsrel=1e-11,
    )
    assert val == pytest.approx(-4.0 / np.pi, rel=1e-10)


def test_ir_log_moment_a11():
    # A11: a + 2*pi int f(s^2) s^3 ln(s) ds = 0.
    # delta_+ term vanishes as eps ln eps.
    val, _ = integrate.quad(
        lambda s: float(f_smooth(s*s)) * s**3 * np.log(s),
        0.0, np.inf, epsabs=1e-12, epsrel=1e-11,
    )
    assert A + 2.0 * np.pi * val == pytest.approx(0.0, abs=1e-10)


def test_spacelike_ir_recovers_box_a8():
    # A8: g(Z)->-Z.  Direct quadrature becomes cancellation-sensitive too close
    # to zero, so use a conservative window and convergence-to-one criterion.
    vals = []
    for Z in [1e-2, 1e-3, 1e-4]:
        vals.append(g_spacelike(Z) / (-Z))
    assert vals[-1] == pytest.approx(1.0, rel=1e-3)
    assert abs(vals[-1] - 1.0) < abs(vals[-2] - 1.0) < abs(vals[-3] - 1.0)


def test_stage1_domain_is_explicitly_spacelike_only():
    with pytest.raises(ValueError):
        g_spacelike(-1.0)
    with pytest.raises(ValueError):
        g_spacelike(0.0)
