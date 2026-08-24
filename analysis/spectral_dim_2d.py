"""
Stage 2, step 2: spectral dimension in d=2 from the causal-set-derived nonlocal
d'Alembertian.  EVERY prescription below is taken verbatim from

  Belenchia, Benincasa, Marciano, Modesto,
  "Spectral Dimension from Nonlocal Dynamics on Causal Sets",
  arXiv:1507.00330, Phys. Rev. D 93, 044017 (2016).      [BBMM]

Nothing is self-designed.  The three things Gate B was blocked on map onto
BBMM as follows:

  (1) REGULARIZATION  -- BBMM Eq.(5), originally from Aslanbeigi-Saravani-Sorkin
      (arXiv:1403.1622).  Because g -> a rho^{2/d} = const in the UV, the Green
      function has a delta-function divergence at coincidence; one subtracts the
      constant (a rho^{2/d})^{-1} from the momentum-space Green function, giving

          g_reg = a rho^{2/d} g / ( a rho^{2/d} - g ).

      BBMM stress this is manifestly Lorentzian and is physically motivated by
      the underlying theory being discrete, where no coincidence limit exists.

  (2) WICK ROTATION -- BBMM Sec. II B.  The operators are RETARDED, so their
      Laplace transform lives in the upper half complex k^0 plane and the
      retarded contour Gamma_R CANNOT be rotated (it would cross singularities).
      BBMM instead analytically continue g to the whole complex plane and use
      the FEYNMAN contour Gamma_F, which rotates freely.  Consequence for us:
      The full chain is and must remain:
          retarded g  ->  analytic continuation to the whole complex plane
                      ->  Feynman prescription (Gamma_F replaces Gamma_R)
                      ->  Wick rotation k^0 -> -i k^0
                      ->  Euclidean section, real k^2 > 0.
      Only at the END of that chain is every momentum spacelike, which is why
      we may evaluate g at REAL k^2 > 0 -- exactly where the Bessel-K
      representation Eq.(2)/(15) is real and single-valued (the cut sits on the
      negative real axis, principal value assumed).  The real integral in this
      file is therefore CONDITIONAL on having adopted that prescription; seeing
      "k^2 > 0" is not itself the Wick rotation.  Do NOT read this as licence to
      treat the Lorentzian retarded g as if it were already a Euclidean
      function -- the analytic continuation and contour choice are load-bearing
      steps that BBMM Sec. II B insists on.

  (3) P(s) -- BBMM Eq.(8) and Eq.(10):
          P(s) = int d^dk/(2pi)^d exp( s g_reg )  =  C_d int_0^inf dk k^{d-1} e^{s g_reg}
          d_s  = -2 dln P(s) / dln s
      C_d cancels in d_s.  Note the sign convention: g_reg < 0 on the whole
      Euclidean section, so exp(s g_reg) is a decaying Gaussian-like weight.
      This is BBMM's own convention (their Eq.(11) integrates e^{-k^d s}).

g^(2) itself is BBMM Eq.(15) with the coefficients they list,
  a2 = -2, b0 = 4, b1 = -8, b2 = 4,
and gamma_2 = 1/2.  On the value of gamma_2, BBMM Eq.(15) as *printed* carries
sqrt(pi)/4, which is inconsistent with three independent things:
  (i)   BBMM's own general Eq.(3), which gives gamma_2 = 1/2 at d = 2;
  (ii)  the source paper Aslanbeigi-Saravani-Sorkin (arXiv:1403.1622): its
        Eq.(3.6) gives C_2 = 1/2, and its Appendix C writes the d=2 kernel out
        explicitly as chi = 2 int ds s exp(-rho s^2 / 2) K_0(...), i.e. C_2 = 1/2
        in plain sight;
  (iii) ASS Eq.(2.5), an exact CLOSED FORM for d=2:
            rho^{-1} g^(2) = -Z e^{Z/2} E_2(Z/2),   Z = k^2/rho,
        which this file's gamma_2 = 1/2 evaluation matches to machine precision
        over nine decades (see gmom_2d_bbmm.py), while sqrt(pi)/4 does not --
        it gets even the SIGN wrong in the IR (g -> +0.2555 instead of -k^2).
We therefore use gamma_2 = 1/2.  Status of the discrepancy: BBMM Eq.(15) is
internally inconsistent with Eq.(3), with its own source, and with the closed
form; numerical and analytic cross-checks all support 1/2.  We record this as a
high-confidence typo judgement of OURS.  Absent a published erratum by the
authors, it must not be written up as though the authors had conceded it.

BUILT-IN CHECKS (all are BBMM's own analytic statements, not ours):
  C1  g   -> -k^2      as k^2 -> 0                       [BBMM Sec. II B]
  C2  g   -> a rho     as k^2 -> inf, a = -2             [BBMM Eq.(4)]
  C3  g_reg -> -(a^2/b) k^2 in UV for d=2                [BBMM Eq.(6)]
  C4  UNREGULARIZED d=2 spectral dimension is exactly d_s = 4 rho s
                                                         [BBMM Eq.(14)]
  C5  REGULARIZED d=2: d_s -> 2 as s -> 0, d_s -> 2 as s -> inf,
      with a maximum > 2 at intermediate s                [BBMM Fig. 2, top]
"""
import warnings

import numpy as np
from scipy import integrate, interpolate, special

warnings.filterwarnings('ignore')

A2 = -2.0
BCO = [4.0, -8.0, 4.0]
GAMMA2 = 0.5                      # BBMM Eq.(3) with d=2


# --------------------------------------------------------------------------
# g^(2)(k^2) on the Euclidean section, BBMM Eq.(15) with gamma_2 = 1/2.
#
# Numerical note: g = a*rho + 2*rho*S and the regularization needs the
# DENOMINATOR u := a*rho - g = -2*rho*S.  Forming u as (a*rho - g) would
# subtract two numbers that both tend to -2 in the UV and lose all precision.
# We therefore carry u itself, which the quadrature returns directly and
# accurately.  This is a floating-point precaution, not a change of formula.
# --------------------------------------------------------------------------
B_UV = 8.0          # BBMM Eq.(4) constant b for d=2, extracted numerically
                    # below: u*k^2 -> -8.000000 stable over 4 decades.
K2_LO, K2_HI = 1e-8, 1e8


def u_raw(k2, rho=1.0):
    """u = a*rho - g = -2*rho*sum_n (b_n/n!) gamma^n int dx x^{2n+1} e^{-gamma x^2} K_0(qx)"""
    q = np.sqrt(k2 / rho)
    tot = 0.0
    for n in range(3):
        c = BCO[n] / special.factorial(n) * GAMMA2 ** n
        I, _ = integrate.quad(
            lambda x, n=n: x ** (2 * n + 1) * np.exp(-GAMMA2 * x * x)
            * special.kv(0, q * x),
            0, np.inf, limit=500, epsabs=1e-16, epsrel=1e-13)
        tot += c * I
    return -2.0 * rho * tot


def build(rho=1.0, npts=1201):
    """Return (g, u) as callables valid on k^2 in (0, inf)."""
    L = np.linspace(np.log10(K2_LO), np.log10(K2_HI), npts)
    uv = np.array([u_raw(10.0 ** x, rho) for x in L])
    assert np.all(uv < 0), "u must be negative"
    spl = interpolate.CubicSpline(L, np.log10(-uv))

    def u_of(k2):
        k2 = np.asarray(k2, float)
        Lv = np.log10(k2)
        mid = -10.0 ** spl(np.clip(Lv, L[0], L[-1]))
        ir = A2 * rho + k2                       # g -> -k^2   (BBMM IR limit)
        uvb = -B_UV * rho ** 2 / k2              # BBMM Eq.(4) form
        return np.where(Lv < L[0], ir, np.where(Lv > L[-1], uvb, mid))

    def g_of(k2):
        return A2 * rho - u_of(k2)

    return g_of, u_of


def g_reg_of(g_of, u_of, rho=1.0):
    """BBMM Eq.(5):  g_reg = a rho^{2/d} g / (a rho^{2/d} - g) = a*rho*g/u."""
    return lambda k2: A2 * rho * g_of(k2) / u_of(k2)


# --------------------------------------------------------------------------
# BBMM Eq.(10)/(8): P(s) and d_s.  d=2  =>  int dk k (...) = (1/2) int dz (...)
# --------------------------------------------------------------------------
def d_s(gfun, s, zlo=1e-16, zhi=1e16, npts=200000):
    """d_s = -2 s * <g> where <g> = int dz g e^{sg} / int dz e^{sg}."""
    L = np.linspace(np.log(zlo), np.log(zhi), npts)
    z = np.exp(L)
    g = gfun(z)
    w = s * g
    w = w - w.max()                       # stabilise; cancels in the ratio
    e = np.exp(w) * z                     # z from dz = z dL
    num = np.trapezoid(g * e, L)
    den = np.trapezoid(e, L)
    return -2.0 * s * num / den


def d_s_cutoff(gfun, s, lam, Lam, npts=200000):
    """Same, but with BBMM's explicit IR cutoff lam and UV cutoff Lam on k
    (their Eq.(13)); z = k^2 so the z-range is [lam^2, Lam^2]."""
    L = np.linspace(np.log(lam ** 2), np.log(Lam ** 2), npts)
    z = np.exp(L)
    g = gfun(z)
    w = s * g
    w = w - w.max()
    e = np.exp(w) * z
    return -2.0 * s * np.trapezoid(g * e, L) / np.trapezoid(e, L)


# --------------------------------------------------------------------------
if __name__ == '__main__':
    rho = 1.0
    print("building g^(2) table (BBMM Eq.15, gamma_2 = 1/2) ...", flush=True)
    g_of, u_of = build(rho)
    greg = g_reg_of(g_of, u_of, rho)

    print("\n" + "=" * 76)
    print(" C1/C2  limits of the UNREGULARIZED g  [BBMM Sec.IIB, Eq.(4)]")
    print("=" * 76)
    print(f"{'k^2':>10} {'g':>14} {'g/(-k^2)':>12} {'g - a*rho':>14} "
          f"{'b_fit=(g-a)k^2':>16}")
    for k2 in [1e-6, 1e-4, 1e-2, 1e2, 1e4, 1e6]:
        g = float(g_of(k2))
        print(f"{k2:10.0e} {g:14.6e} {g/(-k2):12.6f} {g-A2*rho:14.6e} "
              f"{(g-A2*rho)*k2:16.6f}")
    print("  C1: g/(-k^2) -> 1 in the IR.   C2: g -> -2.   b -> 8 (BBMM Eq.4).")

    print("\n" + "=" * 76)
    print(" C3  UV slope of the REGULARIZED g_reg  [BBMM Eq.(6)]")
    print("=" * 76)
    print("     predicted  g_reg/k^2 -> -(a^2/b) = -(4/8) = -0.5")
    print(f"{'k^2':>10} {'g_reg':>16} {'g_reg/k^2':>14}")
    for k2 in [1e-4, 1e0, 1e2, 1e4, 1e6, 1e8, 1e10]:
        gr = float(greg(k2))
        print(f"{k2:10.0e} {gr:16.6e} {gr/k2:14.6f}")
    print("  IR end -> -1 (recovers box), UV end -> -0.5.  Both quadratic,")
    print("  which is why d=2 has d_s = 2 at BOTH ends (BBMM Fig.2 top).")

    print("\n" + "=" * 76)
    print(" C4  UNREGULARIZED d=2 must give exactly d_s = 4 rho s  [BBMM Eq.(14)]")
    print("=" * 76)
    print(f"{'s':>10} {'d_s (numeric)':>16} {'4 rho s':>12} {'ratio':>10}")
    for s in [1e-3, 1e-2, 1e-1, 1.0]:
        num = d_s_cutoff(g_of, s, lam=1e-8, Lam=1e7)
        print(f"{s:10.0e} {num:16.6f} {4*rho*s:12.6f} {num/(4*rho*s):10.6f}")

    print("\n" + "=" * 76)
    print(" C5  REGULARIZED d=2 spectral dimension  [BBMM Fig.2, top panel]")
    print("=" * 76)
    print(f"{'s':>12} {'d_s':>12}")
    ss = np.concatenate([np.logspace(-4, -1, 7), np.logspace(-1, 1, 9)[1:],
                         np.logspace(1, 4, 7)[1:]])
    ds = [d_s(greg, s) for s in ss]
    for s, v in zip(ss, ds):
        print(f"{s:12.4g} {v:12.6f}")
    i = int(np.argmax(ds))
    print(f"\n  s -> 0   : d_s = {ds[0]:.6f}   (BBMM: -> 2)")
    print(f"  maximum  : d_s = {ds[i]:.6f} at s = {ss[i]:.4g}  (BBMM: max at s ~ 1 for rho=1)")
    print(f"  s -> inf : d_s = {ds[-1]:.6f}   (BBMM: -> Hausdorff = 2, from above)")
