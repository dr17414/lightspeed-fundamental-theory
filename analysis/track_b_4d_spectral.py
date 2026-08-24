"""Track B stage 3: quantum spectral structure of the 1502.01655 4D operator.

SCOPE.  Stage 3 only.  NO Wick rotation, NO P(s), NO spectral dimension.

-----------------------------------------------------------------------------
SOURCE TABLE
  Eq.(12)      B(p) = Lambda^2 lim_{eps->0+} g((p + i p_eps)^2 / Lambda^2),
               p_eps infinitesimal future-directed timelike, signature (-+++)
  Eq.(55)      Wtilde(p) = 2 Im B(p) theta(p^0) / |B(p)|^2
  Eq.(56)      quantum positivity: sgn Im B(p) = sgn p^0.  NOTE this is an
               EXTRA condition the author imposes to make the two-point
               function positive; it is NOT one of the six operator axioms of
               Sec. II.
  Eq.(72)-(73) the Sorkin-Johnston construction independently yields the same
               2 Im B / |B|^2 weight -- an internal consistency check by the
               author, not reimplemented here (see NOT IMPLEMENTED below)
  Eq.(85)      rho(-p^2) = Wtilde(p) / (2 pi), for p^0 > 0
  Eq.(85)-(86) rho(mu^2) = delta(mu^2) + rhotilde(mu^2), rhotilde a finite function
  Eq.(87)-(90) the continuum is interpreted as one-particle states of mass mu_j
               after discretising and taking Delta mu^2 -> 0

DERIVED HERE (project result, NOT printed in the paper).
Combining Eq.(12), (55) and (85) for future-directed timelike p, where
p^2 = -mu^2 and x = mu^2/Lambda^2 > 0 so that Z = -x - i0 (the physical bank,
fixed by Eq.(12); see analysis/track_b_4d_analytic.py):

    Wtilde   = (2 / Lambda^2) * g_I / (g_R^2 + g_I^2)
    rhotilde = (1 / (pi Lambda^2)) * g_I / (g_R^2 + g_I^2)

with, from the stage-2 closed form and E_1(-y - i0) = -Ei(y) + i pi,

    g_R(x) = x - (x^2/2) e^{-x/2} Ei(x/2)
    g_I(x) = (pi/2) x^2 e^{-x/2}      > 0 for x > 0

so positivity is analytically manifest: mu^2 > 0 => g_I > 0 => rhotilde > 0.

THE MASSLESS POLE IS NOT REPRESENTED HERE.  The full spectral density is
rho = delta(mu^2) + rhotilde.  Only rhotilde is implemented; a Dirac delta is
not a Python function and faking it with a narrow bump would repeat exactly the
mistake the stage-1 delta_+ normalization had to avoid.

-----------------------------------------------------------------------------
NO SUM RULE IS IMPOSED.  1502.01655 states Eq.(56) positivity and the Eq.(85)
decomposition; it does NOT state a Kallen-Lehmann normalisation such as
int rho dmu^2 = 1, so no such condition may be used as a literature acceptance
criterion.

That said, the continuum weight is computed here and it comes out at exactly 1
(50 digits, two independent subdivisions), which has an analytic explanation we
derived rather than found.  Let h(Z) = -1/g(Z) - 1/Z - 1/2.

  PREMISE, easy to skip and load-bearing: h has no poles off the cut ONLY
  because of the stage-2 stability result that g(Z) != 0 for every Z != 0 on the
  analytically continued domain (analysis/track_b_4d_analytic.py, Eq. A37).  Any
  extra zero of g would be a pole of 1/g and the argument collapses.  The 1/Z
  subtraction removes the one zero that does exist, at the origin.

Given that, h is analytic off the cut.  Since g ~= -Z at the origin, the residue
of -1/g there is 1; at large Z, g = a + b/Z gives -1/g = -1/a + b/(a^2 Z).  h
vanishes at infinity, so Cauchy gives

    int_0^inf dmu^2 rhotilde(mu^2)  =  b/a^2 - 1  =  8/4 - 1  =  1     (Lambda = 1)

So the sum rule is really the composite statement

    IR normalisation (g -> -Z)  +  UV coefficients (b/a^2)  +  stage-2 stability
        ==>  continuum weight = 1

which is stronger than a bare numerical coincidence, and is what makes it a
strong check on the whole normalisation chain Eq.(12) -> (55) -> (85): a stray factor of 2 or pi anywhere
in that chain would not leave an integer.  It also says the continuum carries
exactly the same total weight as the massless pole -- so the FULL rho integrates
to 2, not 1.  Anyone "fixing" that to 1 would be inventing a normalisation.

Classification: project-derived, not a statement of the paper, and used below as
a regression lock on our own arithmetic -- never as a literature criterion.

NOT IMPLEMENTED (deliberately): the Sorkin-Johnston cross-check of Eq.(72)-(73).
The paper uses it to confirm that two quantisation routes agree; reproducing it
needs the SJ formulae extracted from the source, which has not been done.  Do
not approximate it from the Eq.(55) side -- that would be circular.
-----------------------------------------------------------------------------
"""
import numpy as np
from scipy import special

__all__ = [
    "g_R", "g_I", "g_on_lower_bank", "B_timelike", "W_tilde",
    "rho_continuum", "rho_continuum_dimensionless",
    "RHO_TILDE_AT_ZERO_DIMENSIONLESS", "CONTINUUM_WEIGHT_DERIVED",
    "A_UV", "B_UV",
]

A_UV = -2.0          # g -> a + b/Z at large Z
B_UV = 8.0
RHO_TILDE_AT_ZERO_DIMENSIONLESS = 0.5        # Lambda^2 * rhotilde(0+)
CONTINUUM_WEIGHT_DERIVED = B_UV / A_UV**2 - 1.0     # = 1, see docstring

_EI_MAX = 600.0      # above this, e^{-x/2} Ei(x/2) is done asymptotically


def g_R(x):
    """Re g(-x - i0) = x - (x^2/2) e^{-x/2} Ei(x/2), x = mu^2/Lambda^2 > 0.

    For large x both e^{-x/2} and Ei(x/2) overflow/underflow separately, so the
    product is taken from its asymptotic series there:
        e^{-x/2} Ei(x/2) ~ (2/x)(1 + 2/x + 8/x^2 + 48/x^3 + ...)
    giving g_R -> -2 - 8/x - 48/x^2, i.e. the a + b/Z tail with a = -2, b = 8.
    """
    x = np.asarray(x, dtype=float)
    out = np.empty_like(x)
    lo = x < _EI_MAX
    if np.any(lo):
        xl = x[lo]
        out[lo] = xl - (xl * xl / 2.0) * np.exp(-xl / 2.0) * special.expi(xl / 2.0)
    if np.any(~lo):
        xh = x[~lo]
        out[~lo] = -2.0 - 8.0 / xh - 48.0 / (xh * xh)
    return out


# Large-x tail: g_I becomes negligible against g_R, so rhotilde -> g_I/(pi g_R^2)
# with decay rate 1/2 set by e^{-x/2}.  Substituting g_R -> -2 to get the tidier
# x^2 e^{-x/2}/8 is asymptotically right but numerically poor: g_R approaches -2
# only as -2 - 8/x - 48/x^2, still 31% off at x = 20, and by the time it is
# within 1% the exponential has underflowed.  Tests use the rate form instead.


def g_I(x):
    """Im g(-x - i0) = (pi/2) x^2 e^{-x/2}.  Strictly positive for x > 0, which
    is Eq.(56) positivity for future-directed timelike momenta."""
    x = np.asarray(x, dtype=float)
    return (np.pi / 2.0) * x * x * np.exp(-x / 2.0)


def g_on_lower_bank(x):
    """g(-x - i0) as a complex number."""
    return g_R(x) + 1j * g_I(x)


def B_timelike(mu2, Lambda=1.0):
    """B(p) at p^2 = -mu^2 on the physical (future-directed timelike) bank,
    from Eq.(12): B = Lambda^2 g(Z) with Z = -mu^2/Lambda^2 - i0."""
    x = np.asarray(mu2, dtype=float) / Lambda**2
    return Lambda**2 * g_on_lower_bank(x)


def W_tilde(mu2, Lambda=1.0):
    """Eq.(55) for future-directed timelike p (theta(p^0) = 1 there):
    Wtilde = 2 Im B / |B|^2 = (2/Lambda^2) g_I / (g_R^2 + g_I^2)."""
    x = np.asarray(mu2, dtype=float) / Lambda**2
    gr, gi = g_R(x), g_I(x)
    return (2.0 / Lambda**2) * gi / (gr * gr + gi * gi)


def rho_continuum(mu2, Lambda=1.0):
    """Eq.(85): rhotilde(mu^2) = Wtilde/(2 pi).  The massless delta(mu^2) piece
    of Eq.(86) is NOT included -- see the module docstring."""
    return W_tilde(mu2, Lambda) / (2.0 * np.pi)


def rho_continuum_dimensionless(x):
    """Lambda^2 * rhotilde, as a function of x = mu^2/Lambda^2.  Dimensionless,
    so Lambda drops out; used to check that Lambda enters only as Lambda^-2."""
    gr, gi = g_R(x), g_I(x)
    return (1.0 / np.pi) * gi / (gr * gr + gi * gi)


if __name__ == "__main__":
    from scipy import integrate, optimize

    print("Track B stage 3 -- continuum spectral density\n")
    print(f"{'x = mu^2/L^2':>13} {'g_R':>13} {'g_I':>13} {'L^2 rhotilde':>14}")
    for x in [1e-6, 1e-3, 0.1, 1.0, 2.0, 2.6943, 5.0, 10.0, 20.0]:
        print(f"{x:13.4g} {float(g_R(x)):13.6f} {float(g_I(x)):13.6e} "
              f"{float(rho_continuum_dimensionless(x)):14.8f}")

    x0 = optimize.brentq(lambda t: float(g_R(t)), 1.0, 10.0)
    print(f"\ng_R changes sign at x0 = {x0:.10f}  (mu = {np.sqrt(x0):.6f} Lambda)")
    print(f"  there g_I = {float(g_I(x0)):.6f} and L^2 rhotilde = "
          f"{float(rho_continuum_dimensionless(x0)):.6f} = 1/(pi g_I)")
    print("  -> at this mass Re g vanishes, so g_I is the only thing keeping")
    print("     g away from zero.  Concrete, not decorative.")

    tot, err = integrate.quad(
        lambda t: float(rho_continuum_dimensionless(t)), 0, 300, limit=600)
    print(f"\ncontinuum weight  int dmu^2 rhotilde = {tot:.10f}  (err {err:.1e})")
    print(f"  derived value b/a^2 - 1 = {CONTINUUM_WEIGHT_DERIVED:.10f}")
    print("  project-derived, NOT a statement of 1502.01655, NOT an acceptance")
    print("  criterion.  Full rho = delta + rhotilde therefore integrates to 2.")
