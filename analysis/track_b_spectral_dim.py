"""Stage 4 adapter: the 1502.01655 concrete 4D operator, fed through the SAME
spectral-dimension pipeline used for Track A.

CONTROL VARIABLE.  Everything numerical is shared with Track A via
analysis.spectral_dim_D.build_operator: the log-Z grid, the cubic spline in
log10(-u), the interpolation, BBMM Eq.(5) regularization, the D = 4 momentum
measure, d_s(), the s grid and the quadrature settings.  The only per-operator
inputs are a, u_raw, u_ir, u_uv -- i.e. the operator itself.

Forcing the two tracks to share asymptotics would NOT be a tighter control; it
would replace one operator with the other.  Track A's minimal GCB has
u ~ -b/Z^(D/2); Track B has u ~ -8/Z.  That difference IS the physics under
comparison.

WHY BBMM Eq.(5) IS APPLIED TO TRACK B AT ALL.  1502.01655 does not compute a
spectral dimension and does not regularize.  We apply BBMM's regularization
because its stated motivation carries over unchanged: Track B's g also
saturates to a constant a = -2 in the UV, so its Green function has the same
coincidence-limit delta divergence.  That is a PROJECT INFERENCE, not a step
either paper takes, and the comparison is only as fair as that inference.

-----------------------------------------------------------------------------
THE STABLE u.  g -> -2 in the UV, so u = a - g = -2 - g is a difference of two
numbers that both tend to -2, and in double precision it is destroyed: at
Z = 1e6 the naive form gives -8.0001773e-6 against the true -7.9999520e-6.
So u is taken from the asymptotic series instead, derived from
e^w E_1(w) ~ (1/w) sum_k (-1)^k k!/w^k with w = Z/2:

    g(Z) ~ -2 + 8/Z - 48/Z^2 + 384/Z^3 - 3840/Z^4 + 46080/Z^5 - ...
    u(Z) ~ -sum_{n>=1} (-1)^(n+1) 2^(n+1) (n+1)! / Z^n

CAUTION: this is an ASYMPTOTIC, DIVERGENT series.  The terms (n+1)! 2^(n+1)
eventually beat Z^-n, with the smallest term near n ~ Z/2, so a fixed
truncation is only safe at large Z.

Truncation error against an 80-digit mpmath reference, at the switch Z = 200:
     6 terms -> 1.9e-08        12 terms -> 3.9e-14        16 terms -> 1.8e-16
An earlier version used 6 terms and claimed the error was "far below double
precision"; that was wrong by eight orders, and it silently set the floor on the
spline-vs-direct comparison (which then read 1.4e-9 -- an artefact of the
evaluator, not the interpolation).  12 terms is used instead: the optimal
truncation at Z = 200 sits near n ~ 100, so 12 is nowhere near the divergent
regime, and it puts the evaluator below the spline error it is meant to measure.
Do not lower Z_SERIES_SWITCH or _NTERMS without re-running that comparison.

Below the switch, u is computed from the closed form, where g is not yet close
enough to a for the subtraction to hurt.
-----------------------------------------------------------------------------
"""
import numpy as np
from scipy import special

from analysis.spectral_dim_D import build_operator

__all__ = ["A_B", "B_UV_B", "BETA_UV_B", "u_series", "u_raw_B", "u_ir_B",
           "u_uv_B", "build_track_b", "g_direct", "g_reg_direct",
           "Z_SERIES_SWITCH"]

A_B = -2.0                 # g -> a
B_UV_B = 8.0               # u ~ -b/Z^beta with beta = 1
BETA_UV_B = 1.0
Z_SERIES_SWITCH = 200.0
_NTERMS = 12


def _ew_E1(w):
    """e^w E_1(w) without overflow (see track_b_4d_analytic for the rationale)."""
    w = np.asarray(w, dtype=float)
    out = np.empty_like(w)
    big = w > 60.0
    if np.any(~big):
        ws = w[~big]
        out[~big] = np.exp(ws) * special.exp1(ws)
    if np.any(big):
        ws = w[big]
        acc = np.zeros_like(ws)
        term = np.ones_like(ws)
        for k in range(20):
            if k:
                term = term * (-k) / ws
            acc = acc + term
        out[big] = acc / ws
    return out


def u_series(Z, nterms=_NTERMS):
    """u ~ -sum_{n=1..N} (-1)^(n+1) 2^(n+1) (n+1)! / Z^n.  Asymptotic; large Z only."""
    Z = np.asarray(Z, dtype=float)
    acc = np.zeros_like(Z)
    for n in range(1, nterms + 1):
        acc += (-1.0) ** (n + 1) * 2.0 ** (n + 1) * special.factorial(n + 1) / Z ** n
    return -acc


def u_raw_B(Z):
    """u(Z) = a - g(Z) for the Track B operator, evaluated stably everywhere."""
    Z = np.asarray(Z, dtype=float)
    out = np.empty_like(Z)
    hi = Z > Z_SERIES_SWITCH
    if np.any(~hi):
        z = Z[~hi]
        g = -z + (z * z / 2.0) * _ew_E1(z / 2.0)
        out[~hi] = A_B - g
    if np.any(hi):
        out[hi] = u_series(Z[hi])
    return out


def u_ir_B(Z):
    """IR: g -> -Z, so u = a - g -> a + Z.  Same form as Track A's IR branch --
    both operators share the IR condition, only the UV differs."""
    return A_B + np.asarray(Z, dtype=float)


def u_uv_B(Z):
    """UV: u -> -8/Z.  beta = 1, against Track A's beta = D/2 = 2."""
    return -B_UV_B / np.asarray(Z, dtype=float)


def build_track_b(zlo, zhi, npts=801):
    """Same builder, same grid, same spline, same regularization as Track A."""
    return build_operator(A_B, lambda Z: float(u_raw_B(np.array([Z]))[0]),
                          u_ir_B, u_uv_B, zlo, zhi, npts)


def g_direct(Z):
    """g(Z) without the spline.

    NAME: "direct", not "exact".  Above Z_SERIES_SWITCH this still uses the
    truncated asymptotic series, so it is not exact; it is simply the
    spline-free path.  Keeping the two ideas apart matters because there are two
    different checks in play:

      * high-precision mpmath reference  vs  u_raw_B / this function
            -> validates the EVALUATOR (see tests/test_stage4_comparison.py)
      * this function  vs  the spline build
            -> validates the INTERPOLATION only

    Calling this one "exact" invites the second check to be read as the first.

    NOT simply -Z + (Z^2/2) e^{Z/2} E_1(Z/2): that form is -Z + Z(1 - 2/Z + ...)
    and the two leading terms cancel, so above Z ~ 5e16 (where the ulp of Z
    exceeds 1) it returns garbage of order 1 and g_reg comes out POSITIVE.  This
    is the mirror image of the u problem -- g is accurate where u is not, and
    vice versa -- so each is taken from its own accurate side:

        Z <= Z_SERIES_SWITCH : g from the closed form, u = a - g
        Z >  Z_SERIES_SWITCH : u from the series,      g = a - u

    Note the reverse substitution is equally bad: at small Z, u ~= a + Z rounds
    to exactly a in double precision, so g = a - u would give 0 instead of -Z.
    Neither variable is safe on both sides; the switch is required.
    """
    Z = np.asarray(Z, dtype=float)
    out = np.empty_like(Z)
    hi = Z > Z_SERIES_SWITCH
    if np.any(~hi):
        z = Z[~hi]
        out[~hi] = -z + (z * z / 2.0) * _ew_E1(z / 2.0)
    if np.any(hi):
        out[hi] = A_B - u_series(Z[hi])
    return out


def g_reg_direct(Z):
    """BBMM Eq.(5) applied to the spline-free operator.  See g_direct on the
    "direct" vs "exact" distinction."""
    Z = np.asarray(Z, dtype=float)
    return A_B * g_direct(Z) / u_raw_B(Z)


if __name__ == "__main__":
    from analysis.spectral_dim_D import build, d_s

    ZLO, ZHI, NPTS = 1e-6, 1e6, 801
    _, _, gregA = build(4, ZLO, ZHI, NPTS)
    _, u_ofB, gregB = build_track_b(ZLO, ZHI, NPTS)

    print("Stage 4: same pipeline, same grid, only the operator differs\n")
    print(f"  zlo={ZLO:g}  zhi={ZHI:g}  npts={NPTS}   D=4\n")
    print(f"{'s':>10} {'Track A d_s':>14} {'Track B d_s':>14}")
    for s in [1e-4, 1e-2, 1e-1, 1.0, 3.1623, 10.0, 1e2, 1e4]:
        print(f"{s:10.4g} {d_s(gregA, s, 4):14.6f} {d_s(gregB, s, 4):14.6f}")

    Z = np.logspace(-6, 6, 500)
    err = np.abs(u_ofB(Z) / u_raw_B(Z) - 1.0).max()
    print(f"\nTrack B spline vs direct u:  max rel err = {err:.3e}")

    worst = max(abs(d_s(gregB, s, 4) - d_s(g_reg_direct, s, 4))
                for s in np.logspace(-4, 4, 17))
    print(f"Track B spline vs direct d_s: max abs diff = {worst:.3e}")
    print("\n  d_s^UV = D/beta:  Track A beta=2 -> 2,  Track B beta=1 -> 4")
