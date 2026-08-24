"""Track B stage 2: analytic structure of the 1502.01655 4D operator's g(Z).

SCOPE.  Stage 1-2 ONLY: the closed form on the cut plane, the boundary values on
the timelike cut, and the argument-principle zero count that implements the
paper's stability criterion (A37).  This module deliberately contains NO
spectral density, NO quantum spectral weight W(p), NO Wick rotation, NO P(s) and
NO spectral dimension.  Im g on the cut appears here purely as an analytic
boundary value -- it is an INPUT to the zero count, not the spectral density,
which carries extra 1/|B|^2 and theta(p^0) factors and belongs to stage 3.

-----------------------------------------------------------------------------
PROVENANCE -- read this before changing anything.

Definition of record for the Track B operator is, and remains,
    arXiv:1502.01655 Eq.(13)/(A7) + the concrete kernel of Eq.(11)/(A36),
implemented in analysis/track_b_4d.py.  1502.01655 does NOT contain the closed
form used below; the string "E_2" does not appear in that paper.  The closed
form is a DERIVED IDENTITY of ours:

    g(Z) = -Z e^{Z/2} E_2(Z/2)                         [ASS arXiv:1403.1622 Eq.(2.5),
                                                        stated there for the MINIMAL 2D
                                                        operator, not for 1502.01655]

i.e. the 4D concrete operator of 1502.01655 and the minimal 2D operator of ASS
produce the SAME dimensionless momentum-space function g(Z), even though their
position-space constructions live in different dimensions.  Two independent
confirmations, both reproduced as tests:

  (a) numerical: the Eq.(13) integral and the closed form agree to machine
      precision over eight decades in Z;
  (b) analytic: with E_2(w) = e^{-w} - w E_1(w) the closed form becomes
          g(Z) = -Z + (Z^2/2) e^{Z/2} E_1(Z/2),
      whose discontinuity across the cut gives
          Im g(-x - i0) = (pi/2) x^2 e^{-x/2},
      which is exactly the g_I that 1502.01655 Eq.(A33) *chooses* as the input
      from which it reconstructs the kernel f.  So the agreement is structural,
      not coincidental: the paper picked this g_I, and this g_I belongs to that g.

WORDING DISCIPLINE.  "Same g(Z)" is not "same theory".  The dimension D still
enters every downstream object independently through the momentum measure
d^D k / (2 pi)^D.  The same g placed in D = 2 and in D = 4 gives different
Green functions and different spectral dimensions.  Do not write that the 4D
operator "is" the 2D operator.

BRANCH PRESCRIPTION -- fixed by the source, not inferred.
The cut of E_1(Z/2) lies on Z <= 0, i.e. on timelike momenta, which is exactly
where the physics is.  Which bank is physical follows directly from
1502.01655 Eq.(12),
    B(p) = Lambda^2 lim_{eps->0+} g( (p + i p_eps)^2 / Lambda^2 ),
with p_eps an infinitesimal future-directed timelike vector, in the paper's
(-+++) signature.  Expanding,
    Z = p^2/Lambda^2 + 2i (p . p_eps)/Lambda^2 + O(eps^2),
and for future-directed timelike p one has p.p_eps < 0, hence Im Z < 0, while
p^2 < 0 gives Re Z < 0.  So physical future-directed timelike momenta sit on the
LOWER bank, Z = -x - i0, which is what this module uses.  Appendix A.3 states
the same thing from the other side (Im g > 0 below the cut, negative above), and
the module's own numerics reproduce it: see the __main__ table, where the lower
bank carries Im g > 0 and matches Eq.(A33).

Note this is a prescription each paper states in its own terms.  It happens to
agree with ASS here, but it was taken from 1502.01655 Eq.(12); do not settle
such questions by importing ASS's conventions, since the two papers share the
function g but not, a priori, its contour prescription.

A37 DOMAIN.  A37 is not vague about where stability must hold: it requires
g(Z) != 0 for all Z != 0 over the whole analytically continued complex Z domain.
The paper then verifies this in two pieces, and so does this module: an
argument-principle count over the interior of the cut plane (winding_number),
plus a separate non-vanishing check on the cut boundary itself, where zeros are
excluded by Im g != 0 (test_no_zeros_on_the_cut).  The split is an implementation
of A37, not a narrowing of it.
-----------------------------------------------------------------------------
"""
import numpy as np
from scipy import special

__all__ = [
    "g_closed", "g_closed_E2", "im_g_on_lower_cut", "im_g_A33",
    "ir_correction", "winding_number", "CUT_SIDE",
]

CUT_SIDE = -1.0        # physical boundary value taken at Z = -x + CUT_SIDE*i0
_I0 = 1e-25            # infinitesimal used to select the branch


_ASYMP_RE = 60.0        # switch to the asymptotic series beyond this Re(w)
_ASYMP_K = 20


def _ew_E1(w):
    """e^w E_1(w), evaluated so that it does not overflow.

    Taken naively, e^{Z/2} overflows for Z > ~1418 while E_1(Z/2) underflows to
    zero, and the product comes out as nan -- which is what the first draft of
    this module did at Z = 1e4.  For large Re(w) the standard asymptotic series
    (DLMF 6.12.1) gives the product directly:
        emw E_1(w) ~ (1/w) sum_k (-1)^k k! / w^k .
    At Re(w) > 60 truncating at k = 20 leaves a remainder of order 1e-17, and
    the series is at its most accurate on the positive real axis, which is
    exactly where the overflow problem lives.  Near and on the cut (Re(w) < 0)
    the direct product is used, where e^w is small and E_1 is large but both
    stay well inside double range for the contour radii used here.
    """
    w = np.asarray(w, dtype=np.complex128)
    out = np.empty_like(w)
    big = w.real > _ASYMP_RE
    if np.any(~big):
        ws = w[~big]
        out[~big] = np.exp(ws) * special.exp1(ws)
    if np.any(big):
        ws = w[big]
        acc = np.zeros_like(ws)
        term = np.ones_like(ws)
        for k in range(_ASYMP_K):
            if k:
                term = term * (-k) / ws
            acc = acc + term
        out[big] = acc / ws
    return out


def g_closed(Z):
    """g(Z) = -Z + (Z^2/2) e^{Z/2} E_1(Z/2), on the cut plane and on either
    edge of the cut (pass Z with a small imaginary part to select the edge).
    Fast path; this is the evaluator, not the definition of record."""
    Z = np.asarray(Z, dtype=np.complex128)
    return -Z + (Z * Z / 2.0) * _ew_E1(Z / 2.0)


def g_closed_E2(Z, dps=40):
    """The literal ASS Eq.(2.5) form  -Z e^{Z/2} E_2(Z/2), evaluated in
    arbitrary precision.

    Deliberately NOT built on _ew_E1: it computes E_2 from an independent
    implementation (mpmath) so that the identity E_2(w) = e^{-w} - w E_1(w),
    which is what connects the ASS form to the fast path above, is exercised
    rather than assumed.  Slow; reference use only.
    """
    import mpmath as mp
    old, mp.mp.dps = mp.mp.dps, dps
    try:
        def one(z):
            z = mp.mpc(z)
            return complex(-z * mp.exp(z / 2) * mp.expint(2, z / 2))
        arr = np.asarray(Z, dtype=np.complex128)
        if arr.ndim == 0:
            return np.complex128(one(complex(arr)))
        return np.array([one(complex(z)) for z in arr.ravel()]).reshape(arr.shape)
    finally:
        mp.mp.dps = old


def im_g_on_lower_cut(x):
    """Im g at Z = -x - i0, from the closed form.  x > 0 (timelike)."""
    x = np.asarray(x, dtype=float)
    return g_closed(-x + CUT_SIDE * 1j * _I0).imag


def ir_correction(Z):
    """The exact first correction to the IR limit A8.

    With E_1(w) = -gamma - ln w + O(w),
        g(Z) / (-Z) - 1  =  -(Z/2) ( ln(2/Z) - gamma )  + O(Z^2 ln Z).
    Worth having explicitly: the departure from -Z at Z = 1e-6 is 7e-6 in
    relative terms, which is a real analytic correction and NOT quadrature
    error.  A test that demands g/(-Z) = 1 to better than that is testing the
    wrong thing, and will "fail" on a correct implementation.
    """
    Z = np.asarray(Z, dtype=float)
    return -(Z / 2.0) * (np.log(2.0 / Z) - np.euler_gamma)


def im_g_A33(x):
    """The g_I that 1502.01655 Eq.(A33) selects: (pi/2) x^2 e^{-x/2}."""
    x = np.asarray(x, dtype=float)
    return (np.pi / 2.0) * x * x * np.exp(-x / 2.0)


def winding_number(R=100.0, eps=1e-6, n=3000):
    """Argument-principle count of zeros of g on the cut plane, i.e.

        N - P = (1/2 pi i) oint_C g'(Z)/g(Z) dZ

    evaluated as the winding of g along C, where C is the positively oriented
    boundary of {eps < |Z| < R, -pi < arg Z < pi}: out along the lower edge of
    the cut, round the large circle, back along the upper edge, then clockwise
    round the small circle at the origin.

    g has no poles on this domain, so the result is the number of zeros.  The
    simple zero at Z = 0 is EXCLUDED by the small circle, so stability in the
    sense of 1502.01655 Eq.(A37) -- no zeros other than Z = 0 -- corresponds to
    the answer 0.

    Zeros lying exactly ON the cut are not enclosed by C and are therefore not
    counted here; they are excluded separately by Im g > 0 on the cut, which is
    the mechanism of the paper's own positivity-implies-stability argument
    (A38-A42).  See test_no_zeros_on_the_cut.

    A37 requires no zeros anywhere in the analytically continued complex Z
    domain except Z = 0; this function covers the interior of the cut plane and
    the cut boundary is handled separately (see the module docstring).

    Note the practical ceiling on R: the closed form multiplies e^{Z/2}, which
    underflows, by E_1(Z/2), which overflows, so R beyond a few hundred loses
    the product in double precision.
    """
    lo = np.log(R / eps)
    # 1) lower edge of the cut, from -eps outward to -R
    t = -eps * np.exp(lo * np.linspace(0.0, 1.0, n + 1))
    seg1 = t + CUT_SIDE * 1j * _I0
    # 2) large circle, arg from -pi to +pi
    th = np.linspace(-np.pi, np.pi, 4 * n + 1)[1:]
    seg2 = R * np.exp(1j * th)
    # 3) upper edge of the cut, from -R back in to -eps
    t = -R * np.exp(-lo * np.linspace(0.0, 1.0, n + 1))
    seg3 = t - CUT_SIDE * 1j * _I0
    # 4) small circle at the origin, arg from +pi to -pi (clockwise)
    th = np.linspace(np.pi, -np.pi, n + 1)[1:]
    seg4 = eps * np.exp(1j * th)

    path = np.concatenate([seg1, seg2, seg3, seg4])
    vals = g_closed(path)
    if np.any(vals == 0):
        raise ValueError("g vanishes on the contour; move R or eps")
    d = np.diff(np.angle(vals))
    d = (d + np.pi) % (2 * np.pi) - np.pi          # unwrap step by step
    return float(d.sum() / (2 * np.pi))


if __name__ == "__main__":
    print("Track B stage 2 -- analytic structure of g(Z)\n")
    print("physical edge of the cut: Im g at Z = -x -+ i0")
    print(f"{'x':>8} {'Im g(-x-i0)':>16} {'Im g(-x+i0)':>16} {'A33 g_I':>16}")
    for x in [0.5, 1.0, 2.0, 5.0, 10.0]:
        lower = float(g_closed(-x - 1j * _I0).imag)
        upper = float(g_closed(-x + 1j * _I0).imag)
        print(f"{x:8.1f} {lower:16.10f} {upper:16.10f} {float(im_g_A33(x)):16.10f}")
    print("  -> the LOWER edge carries Im g > 0 and matches Eq.(A33).\n")

    print("argument-principle zero count on the cut plane (Z = 0 excluded)")
    print(f"{'R':>8} {'eps':>10} {'n':>7} {'N':>14}")
    for R, eps, n in [(20.0, 1e-4, 3000), (50.0, 1e-5, 3000),
                      (100.0, 1e-6, 3000), (300.0, 1e-6, 6000)]:
        print(f"{R:8.0f} {eps:10.0e} {n:7d} {winding_number(R, eps, n):14.8f}")
    print("  -> N = 0: no zeros besides Z = 0, i.e. A37 stability holds.")
