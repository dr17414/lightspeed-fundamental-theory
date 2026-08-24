"""
Regression tests for the d=4 spectral dimension pipeline (Track A replication).

Verifies key limits and constants for the 4D GCB operator, including
the IR limit, UV limit, regularized UV limit, and spectral dimension flow.
"""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.spectral_dim_D import build, d_s, C_D, b_uv, COEFFS  # noqa: E402

RHO = 1.0


@pytest.fixture(scope="module")
def ops_4d():
    # Build 4D operators. Using npts=241 for quick testing while maintaining cubic spline accuracy.
    g_of, u_of, greg = build(4, zlo=1e-6, zhi=1e6, npts=241)
    return g_of, u_of, greg


def test_4d_constants():
    """Verify analytical constants for d=4:
    a4 = -4 / sqrt(6)
    C4 = pi / 24
    bUV = 32 * pi / sqrt(6)
    """
    a4 = -4.0 / np.sqrt(6.0)
    C4 = np.pi / 24.0
    bUV = 32.0 * np.pi / np.sqrt(6.0)

    assert COEFFS[4]['a'] == pytest.approx(a4)
    assert C_D(4) == pytest.approx(C4)
    assert b_uv(4) == pytest.approx(bUV)

    # The full b_n list, ASS arXiv:1403.1622 Eq.(2.12).  Worth asserting
    # explicitly: the one real transcription error found in this line of work
    # was a mis-copied coefficient (BBMM Eq.(15)'s gamma_2), and b_uv() above
    # only ever touches b_0, so b_1..b_3 are otherwise unguarded.
    s6 = np.sqrt(6.0)
    assert COEFFS[4]['b'] == pytest.approx(
        [4.0 / s6, -36.0 / s6, 64.0 / s6, -32.0 / s6])


def test_4d_ir_limit(ops_4d):
    """Verify IR limit: g(Z)/(-Z) -> 1 as Z -> 0."""
    g_of, _, _ = ops_4d
    # Z < zlo (1e-6) is extrapolated using the asymptotic IR form
    for Z in [1e-8, 1e-7]:
        assert float(g_of(Z)) / (-Z) == pytest.approx(1.0, rel=1e-3)
    # Z = 1e-6 (boundary of the spline grid zlo) is verified within 5%
    assert float(g_of(1e-6)) / (-1e-6) == pytest.approx(1.0, rel=5e-2)


def test_4d_uv_limit(ops_4d):
    """Verify UV limit: (g(Z) - a4) * Z^2 -> bUV as Z -> inf."""
    g_of, _, _ = ops_4d
    a4 = COEFFS[4]['a']
    bUV = b_uv(4)
    for Z in [1e5, 1e6, 1e7]:
        assert (float(g_of(Z)) - a4) * Z ** 2 == pytest.approx(bUV, rel=1e-3)


def test_4d_regularized_uv_slope(ops_4d):
    """Verify regularized UV slope: g_reg(Z)/Z^2 -> -(a4^2 / bUV) as Z -> inf."""
    _, _, greg = ops_4d
    a4 = COEFFS[4]['a']
    bUV = b_uv(4)
    predicted = -(a4 ** 2) / bUV
    for Z in [1e5, 1e6, 1e7]:
        assert float(greg(Z)) / Z ** 2 == pytest.approx(predicted, rel=1e-3)


def test_4d_g_stays_inside_the_regularization_domain(ops_4d):
    """DOMAIN SAFETY for BBMM Eq.(5): g_reg = a*g/(a - g).

    The denominator is (a - g).  If g~ reached a at any finite Z > 0 the
    regularized operator would have a pole on the Euclidean section and the
    P(s) integral of stage 4 would be ill-defined.  a < g~ < 0 throughout is
    what makes the pipeline well posed, so it is asserted rather than assumed.
    (g~ approaches a only asymptotically, as Z -> inf.)
    """
    g_of, _, _ = ops_4d
    a4 = COEFFS[4]['a']
    g = g_of(np.logspace(-6, 6, 400))
    assert np.all(g < 0.0)
    assert np.all(g > a4)


def test_4d_regularization_preserves_ir(ops_4d):
    """The regularization must fix the UV without disturbing the IR:
    g_reg(Z) -> -Z as Z -> 0, as the unregularized g~ does (ASS Eq. 3.13).
    Only the regularized UV slope is checked elsewhere; this pins the other end.
    """
    _, _, greg = ops_4d
    for Z in [1e-8, 1e-7]:
        assert float(greg(Z)) / (-Z) == pytest.approx(1.0, rel=1e-3)


def test_4d_ds_rises_monotonically_before_the_overshoot(ops_4d):
    """The 4D flow runs UV -> IR without doubling back on the way up."""
    _, _, greg = ops_4d
    ss = np.logspace(-4, 0.5, 10)
    ds_vals = np.array([d_s(greg, s, 4) for s in ss])
    assert np.all(np.diff(ds_vals) > 0)


def test_4d_ds_limits_and_overshoot(ops_4d):
    """Verify spectral dimension limits and qualitative behavior in d=4:
    - s -> 0: d_s -> 2
    - s -> infinity: d_s -> 4
    - intermediate overshoot: max(d_s) > 4
    
    The peak location and exact height (s ≈ 10, d_s ≈ 4.17) are not written as
    precise assertions (only qualitative checks) as per requirements.
    """
    _, _, greg = ops_4d

    # s -> 0: d_s -> 2
    ds_0 = d_s(greg, 1e-4, 4)
    assert ds_0 == pytest.approx(2.0, abs=5e-2)

    # s -> infinity: d_s -> 4
    ds_inf = d_s(greg, 1e4, 4)
    assert ds_inf == pytest.approx(4.0, abs=5e-2)

    # intermediate overshoot: max(d_s) > 4
    ss = np.logspace(0, 2, 9)
    ds_vals = [d_s(greg, s, 4) for s in ss]
    max_ds = max(ds_vals)
    assert max_ds > 4.0

    # Qualitative numerical observations (not hard asserts)
    peak_idx = np.argmax(ds_vals)
    peak_s = ss[peak_idx]
    print(f"\n[4D Numerical Observation] Peak observed: d_s = {max_ds:.4f} at s = {peak_s:.2f}")
