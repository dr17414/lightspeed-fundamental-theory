"""IR-safe evaluation of the Track B g(Z), for review before merging PR #7.

PROBLEM.  The stage-1 form
    g(Z) = a + 8/Z + 4 pi Z^{-1/2} int ds s^2 f_smooth(s^2) K_1(sqrt(Z) s)
is exact but numerically unusable as Z -> 0: the 8/Z term and the integral must
cancel to produce a result of size Z.  Measured on the branch as it stands:

    Z = 1e-4   ->  ~9 decimal digits cancelled
    Z = 1e-6   ->  ~13 digits cancelled, and g/(-Z) has already turned back
                   AWAY from 1 (0.99995 at 1e-5, 0.99931 at 1e-6)

So the IR limit is confirmed only over about two usable decades, and the
monotone-convergence assertion in test_spacelike_ir_recovers_box_a8 holds only
because the window stops at 1e-4.  One more decade and it fails on noise.

FIX.  Do the cancellation analytically, using the paper's own IR conditions.
With the small-argument expansion (DLMF 10.31.1)
    K_1(x) = 1/x + (x/2) ln(x/2) + (x/4)(2 gamma - 1) + O(x^3 ln x),
the three subtracted pieces integrate to exactly the three divergent/constant
terms, each killed by one of the paper's own conditions:

    1/x  piece      -> (4 pi / Z) int s f(s^2) ds            = 0   by A9, k=0
                       (this is precisely what cancels 8/Z)
    ln(sqrt(Z)/2)   -> 2 pi ln(sqrt(Z)/2) int s^3 f(s^2) ds  = 0   by A9, k=1
    (2 gamma -1)    -> pi (2 gamma - 1) int s^3 f(s^2) ds    = 0   by A9, k=1
    ln s  piece     -> 2 pi int s^3 f(s^2) ln s ds           = -a  by A11

Summing: a + [0 + (-a)] = 0, so every term of order Z^{-1} and Z^0 cancels
identically, leaving

    g(Z) = 4 pi Z^{-1/2} int_0^inf ds s^2 f_smooth(s^2) R(sqrt(Z) s),
    R(x) := K_1(x) - 1/x - (x/2) ln(x/2) - (x/4)(2 gamma - 1) = O(x^3 ln x).

The delta_+ term contributes 8 Z^{-1/2} sqrt(eps) R(sqrt(Z eps)) -> 0, so it
drops out of this form entirely -- its whole job was to supply the 8/Z that
A9(k=0) cancels.  No free parameters, no new prescription: this is the paper's
own Eqs. (A9)/(A11) used to reorganise the arithmetic.

VALIDATED RANGE.  This form is good for the leading term down to Z ~ 1e-10 and
for the first correction -(Z/2)(ln(2/Z) - gamma) down to Z ~ 1e-8; at Z = 1e-10
the correction is only accurate to about 30%, and by Z ~ 1e-12 the form breaks
down in its turn.  Four decades better than the direct integral, not exact.
Below the validated range, use the closed form in track_b_4d_analytic.py.

R itself must be evaluated by series for small x (computing K_1 then subtracting
1/x reintroduces the same cancellation), and directly for large x.  The form is
IR-safe but UV-unsafe (the subtracted terms grow while K_1 decays), so it is a
complement to the stage-1 form, not a replacement: use this for Z < ~1e-2 and
the direct form above it.  They are cross-checked against each other below.
"""
import warnings

import numpy as np
from scipy import integrate, special

warnings.filterwarnings('ignore')

GAMMA = float(np.euler_gamma)
A = -2.0
XSWITCH = 2.0          # series below, direct above


def R_series(x, kmax=40):
    """R(x) via DLMF 10.31.1 with the k=0 terms removed analytically."""
    x = np.asarray(x, float)
    h = x / 2.0
    s1 = np.zeros_like(x)      # ln(x/2) * [I_1(x) - x/2]
    s2 = np.zeros_like(x)      # -(x/4) * sum_{k>=1} (psi(k+1)+psi(k+2)) (x^2/4)^k /(k!(k+1)!)
    for k in range(1, kmax):
        c = 1.0 / (special.factorial(k) * special.factorial(k + 1))
        s1 += h ** (2 * k + 1) * c
        s2 += (special.digamma(k + 1) + special.digamma(k + 2)) * c * h ** (2 * k)
    return np.log(h) * s1 - (x / 4.0) * s2


def R_direct(x):
    x = np.asarray(x, float)
    return (special.kv(1, x) - 1.0 / x - (x / 2.0) * np.log(x / 2.0)
            - (x / 4.0) * (2 * GAMMA - 1.0))


def R(x):
    x = np.asarray(x, float)
    return np.where(x < XSWITCH, R_series(np.minimum(x, XSWITCH)),
                    R_direct(np.maximum(x, XSWITCH)))


def g_ir_safe(Z):
    """g(Z) with the Z^-1 and Z^0 terms cancel analytically."""
    Z = float(Z)
    if not np.isfinite(Z) or Z <= 0.0:
        raise ValueErro("real Z > 0 only")
    q = np.sqrt(Z)
    # 4 pi s^2 f_smooth(s^2) = -(24 s^2 - 12 s^4 + s^6) e^{-s^2/2}
    val, _ = integrate.quad(
        lambda s: -np.exp(-s * s / 2.0) * (24 * s**2 - 12 * s**4 + s**6)
        * float(R(q * s)),
        0.0, np.inf, limit=800, epsabs=1e-16, epsrel=1e-13)
    return val / q


if __name__ == '__main__':
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from analysis.track_b_4d import g_spacelike

    import mpmath as mp
    mp.mp.dps = 40
    print("R(x): series vs 40-digit reference")
    for x in [1e-3, 1e-2, 0.1, 1.0, 2.0, 5.0]:
        ref = float(mp.besselk(1, x) - 1 / mp.mpf(x) - (mp.mpf(x) / 2) * mp.log(mp.mpf(x) / 2)
                    - (mp.mpf(x) / 4) * (2 * mp.euler - 1))
        print(f"  x={x:8.0e}  R={float(R(x)):+.12e}  ref={ref:+.12e}  "
              f"rel={abs(float(R(x))-ref)/abs(ref):.2e}")

    print("\ncross-check of the two forms, and the IR limit")
    print(f"{'Z':>9} {'g (stage-1)':>16} {'g (IR-safe)':>16} {'rel diff':>10} "
          f"{'g_safe/(-Z)':>13}")
    for L in [0, -1, -2, -3, -4, -5, -6, -8, -10, -12]:
        Z = 10.0 ** L
        gs = g_ir_safe(Z)
        try:
            g1 = g_spacelike(Z)
            rd = abs(g1 - gs) / abs(gs)
            print(f"{Z:9.0e} {g1:16.8e} {gs:16.8e} {rd:10.2e} {gs/(-Z):13.9f}")
        except Exception:
            print(f"{Z:9.0e} {'--':>16} {gs:16.8e} {'--':>10} {gs/(-Z):13.9f}")
