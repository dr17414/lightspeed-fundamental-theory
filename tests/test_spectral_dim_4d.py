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
