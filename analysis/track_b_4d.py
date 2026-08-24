"""Track B, stage 1: 4D operator of Saravani--Aslanbeigi, arXiv:1502.01655.

This module implements ONLY the source-faithful position/momentum kernel on the
real spacelike section Z>0.  It deliberately does not yet implement
complex-plane stability, quantum spectral density, Wick rotation, P(s), or d_s.

Primary source: arXiv:1502.01655 v2
  Eq. (9)/(A1): position-space retarded operator
  Eq. (11)/(A36): a=-2 and f(u)=4/pi delta_+(u) + f_g(u)
  Eq. (13)/(A7): g(Z) Bessel-K representation
  Eq. (A8): IR target g(Z)->-Z
  Eqs. (A9)--(A11): equivalent IR moment conditions

The distribution delta_+(u) is defined by the paper as
    delta_+(u) = lim_{eps->0+} delta(u-eps)     [below A18].
In Eq. (A7), f is evaluated at u=s^2.  Therefore
    delta(s^2-eps) = delta(s-sqrt(eps))/(2 sqrt(eps)),  s>=0.
Its exact contribution to g is
    lim 4*pi*Z^(-1/2)*(4/pi)*(sqrt(eps)/2)*K1(sqrt(Z*eps)) = 8/Z.
This term MUST be kept analytically; approximating the delta by a narrow
Gaussian changes the normalization and destroys the IR cancellations.
"""

import numpy as np
from scipy import integrate, special

A = -2.0
DELTA_COEFF = 4.0 / np.pi


def f_smooth(u):
    """Smooth part of Eq. (A36), with u>=0."""
    u = np.asarray(u)
    return -np.exp(-u / 2.0) * (24.0 - 12.0 * u + u * u) / (4.0 * np.pi)


def delta_g(Z):
    """Exact delta_+ contribution to g(Z) after eps->0+: 8/Z."""
    Z = np.asarray(Z)
    return 8.0 / Z


def smooth_g_integral(Z):
    """Smooth contribution to Eq. (A7) for real spacelike Z>0.

    Returns the term added to a + 8/Z.
    """
    Z = float(Z)
    if not np.isfinite(Z) or Z <= 0.0:
        raise ValueError("stage-1 implementation is restricted to real Z>0")
    q = np.sqrt(Z)

    def integrand(s):
        poly = 24.0 * s**2 - 12.0 * s**4 + s**6
        return np.exp(-s * s / 2.0) * poly * special.kv(1, q * s)

    val, _ = integrate.quad(
        integrand, 0.0, np.inf, limit=600, epsabs=1e-13, epsrel=1e-11
    )
    return -val / q


def g_spacelike(Z):
    """Eq. (A7)/(13) for the concrete 4D example, on real Z>0."""
    Z = np.asarray(Z, dtype=float)
    if Z.ndim == 0:
        z = float(Z)
        if not np.isfinite(z) or z <= 0.0:
            raise ValueError("stage-1 implementation is restricted to real Z>0")
        return A + float(delta_g(z)) + smooth_g_integral(z)
    if np.any(~np.isfinite(Z)) or np.any(Z <= 0.0):
        raise ValueError("stage-1 implementation is restricted to real Z>0")
    return np.array([A + float(delta_g(z)) + smooth_g_integral(z) for z in Z])
