"""
Stage 2, step 3: the D-dimensional GCB spectrum g~(Z), and the d=4 spectral
dimension.  All formulae verbatim from

  [ASS]  Aslanbeigi, Saravani, Sorkin, "Generalized Causal Set d'Alembertians",
         arXiv:1403.1622, JHEP 06 (2014) 024.
  [BBMM] Belenchia, Benincasa, Marciano, Modesto, arXiv:1507.00330,
         Phys. Rev. D 93, 044017 (2016).

Working in rho = 1 units throughout, so Z = p.p and g~(Z) = rho^{-2/D} g_rho.
Every quantity below is one of ASS's dimensionless objects.

  ASS (3.8)   g~(Z) = a + 2(2pi)^{D/2-1} Z^{(2-D)/4}
                        * sum_n (b_n/n!) C_D^n
                          int_0^inf ds s^{D(n+1/2)} e^{-C_D s^D} K_{D/2-1}(sqrt(Z) s)
  ASS (3.6)   C_D = (pi/4)^{(D-1)/2} / (D Gamma((D+1)/2))
  ASS (3.13)  IR:  g~(Z) -> -Z
  ASS (3.16)  UV:  g~(Z) -> a + 2^{D-1} pi^{D/2-1} Gamma(D/2) b_0 Z^{-D/2}
  BBMM (5)    g~_reg(Z) = a g~ / (a - g~)
  BBMM (6)    UV: g~_reg -> -(a^2/b_UV) Z^{D/2}
  BBMM (8,10) P(s) = C int_0^inf dk k^{D-1} e^{s g~_reg(k^2)},  d_s = -2 dlnP/dlns

NOTE ON gamma_2 / C_2 (settles the open item flagged in gmom_2d_bbmm.py):
ASS (3.6) gives C_2 = (pi/4)^{1/2}/(2 Gamma(3/2)) = 1/2, and ASS Appendix C
writes the d=2 kernel out explicitly as chi = 2 int ds s e^{-rho s^2/2} K_0(...),
i.e. C_2 = 1/2 in plain sight.  BBMM Eq.(15) prints sqrt(pi)/4 instead.  The
source paper therefore confirms 1/2 directly; BBMM Eq.(15)'s factor is a typo.

NOTE ON WICK ROTATION (do not delete): evaluating g~ at real Z > 0 below is
legitimate ONLY because we have adopted BBMM's prescription in full --
the retarded operator's g is first analytically continued to the whole complex
plane, the Feynman contour Gamma_F replaces the retarded Gamma_R (Gamma_R cannot
be rotated; it would cross singularities), and only then does k^0 -> -i k^0 map
every momentum onto the spacelike/Euclidean section Z > 0.  Seeing "Z > 0" is
not itself the Wick rotation; it is the end state of that prescription.  Do not
treat the Lorentzian retarded g~ as if it were already a Euclidean function.
"""
import warnings

import numpy as np
from scipy import integrate, interpolate, special

warnings.filterwarnings('ignore')

# ASS (2.2) and (2.12).  b_n as listed; the 1/n! is applied in the formula.
COEFFS = {
    2: dict(a=-2.0, b=[4.0, -8.0, 4.0]),
    4: dict(a=-4.0 / np.sqrt(6), b=[4.0 / np.sqrt(6), -36.0 / np.sqrt(6),
                                    64.0 / np.sqrt(6), -32.0 / np.sqrt(6)]),
}


def C_D(D):
    """ASS (3.6)."""
    return (np.pi / 4) ** ((D - 1) / 2) / (D * special.gamma((D + 1) / 2))


def b_uv(D):
    """ASS (3.16) subleading coefficient: 2^{D-1} pi^{D/2-1} Gamma(D/2) b_0."""
    b0 = COEFFS[D]['b'][0]
    return 2 ** (D - 1) * np.pi ** (D / 2 - 1) * special.gamma(D / 2) * b0


def u_raw(Z, D):
    """u := a - g~(Z), computed directly (never as a difference of two numbers
    that both tend to a).  From ASS (3.8), u = -(the whole sum term)."""
    a_ = COEFFS[D]['a']  # noqa: F841  (kept for readability of the relation)
    bs = COEFFS[D]['b']
    cd = C_D(D)
    nu = D / 2 - 1
    q = np.sqrt(Z)
    tot = 0.0
    for n, bn in enumerate(bs):
        c = bn / special.factorial(n) * cd ** n
        I, _ = integrate.quad(
            lambda s, n=n: s ** (D * (n + 0.5)) * np.exp(-cd * s ** D)
            * special.kv(nu, q * s),
            0, np.inf, limit=800, epsabs=1e-16, epsrel=1e-13)
        tot += c * I
    pref = 2 * (2 * np.pi) ** (D / 2 - 1) * Z ** ((2 - D) / 4)
    return -pref * tot


def build_operator(a, u_raw, u_ir, u_uv, zlo, zhi, npts=801):
    """Generic operator builder.  The NUMERICAL METHOD is shared; the PHYSICS is
    supplied per operator.

    This split is the control variable for the Track A / Track B comparison.
    Everything about how the answer is computed -- log-Z grid, cubic spline,
    interpolation, the regularization formula, the momentum measure, d_s() --
    is identical for both tracks.  What differs is only the operator itself:

        a      : the UV constant, g -> a
        u_raw  : u(Z) = a - g(Z), evaluated directly (never as a - g, which
                 cancels catastrophically once g is near a)
        u_ir   : u as Z -> 0, used below zlo
        u_uv   : u as Z -> inf, used above zhi

    The previous build(D, ...) hard-coded the UV branch as u ~ -b_uv/Z^(D/2).
    That is correct for the minimal GCB family and WRONG for any operator with a
    different subleading power.  Feeding Track B (u ~ -8/Z) through it would
    force u ~ 1/Z^2 above zhi and manufacture d_s^UV -> 2 -- i.e. it would
    overwrite Track B's physics with Track A's and then "find" that they agree.
    Forcing a shared asymptotic is not a controlled comparison; it is a changed
    operator.
    """
    L = np.linspace(np.log10(zlo), np.log10(zhi), npts)
    uv = np.array([u_raw(10.0 ** x) for x in L])
    if not np.all(uv < 0):
        bad = 10.0 ** L[uv >= 0]
        raise AssertionError(f"u must be negative; failed at Z = {bad[:5]}")
    spl = interpolate.CubicSpline(L, np.log10(-uv))

    def u_of(Z):
        Z = np.asarray(Z, float)
        Lv = np.log10(Z)
        mid = -10.0 ** spl(np.clip(Lv, L[0], L[-1]))
        return np.where(Lv < L[0], u_ir(Z), np.where(Lv > L[-1], u_uv(Z), mid))

    g_of = lambda Z: a - u_of(Z)
    g_reg = lambda Z: a * g_of(Z) / u_of(Z)          # BBMM (5)
    return g_of, u_of, g_reg


def build(D, zlo, zhi, npts=801):
    """Minimal GCB of ASS, dimension D.  Thin wrapper over build_operator with
    that family's own asymptotics: u -> a + Z in the IR [ASS (3.13)] and
    u -> -b_uv/Z^(D/2) in the UV [ASS (3.16)].  Behaviour is unchanged."""
    a_ = COEFFS[D]['a']
    bU = b_uv(D)
    return build_operator(
        a_,
        lambda Z: u_raw(Z, D),
        lambda Z: a_ + Z,
        lambda Z: -bU / Z ** (D / 2),
        zlo, zhi, npts)


def d_s(gfun, s, D, zlo=1e-18, zhi=1e18, npts=300000):
    """BBMM (8)+(10).  int dk k^{D-1} f(k^2) = (1/2) int dZ Z^{D/2-1} f(Z)."""
    L = np.linspace(np.log(zlo), np.log(zhi), npts)
    Z = np.exp(L)
    g = gfun(Z)
    w = s * g
    w -= w.max()
    meas = np.exp(w) * Z ** (D / 2)      # Z^{D/2-1} * Z  (dZ = Z dL)
    return -2.0 * s * np.trapezoid(g * meas, L) / np.trapezoid(meas, L)


if __name__ == '__main__':
    for D, (zlo, zhi) in [(2, (1e-8, 1e8)), (4, (1e-6, 1e6))]:
        a_ = COEFFS[D]['a']
        bU = b_uv(D)
        print("=" * 78)
        print(f" D = {D}   a = {a_:.8f}   C_D = {C_D(D):.8f}   b_UV = {bU:.6f}")
        print("=" * 78)
        g_of, u_of, greg = build(D, zlo, zhi)

        print(f"{'Z':>10} {'g~':>14} {'g~/(-Z)':>11} {'(g~-a)Z^(D/2)':>15} "
              f"{'g~_reg':>15} {'g~_reg/Z^(D/2)':>16}")
        for Z in [zlo * 100, 1e-2, 1.0, 1e2, zhi / 100]:
            g = float(g_of(Z)); gr = float(greg(Z))
            print(f"{Z:10.0e} {g:14.6e} {g/(-Z):11.6f} "
                  f"{(g-a_)*Z**(D/2):15.6f} {gr:15.6e} {gr/Z**(D/2):16.6f}")
        print(f"  IR check  g~/(-Z) -> 1        [ASS 3.13]")
        print(f"  UV check  (g~-a)Z^(D/2) -> b_UV = {bU:.6f}   [ASS 3.16]")
        print(f"  reg UV    g~_reg/Z^(D/2) -> -(a^2/b_UV) = {-a_**2/bU:.6f}  [BBMM 6]")

        print(f"\n  spectral dimension (rho = 1), Hausdorff = {D}")
        print(f"  {'s':>12} {'d_s':>12}")
        ss = np.logspace(-4, 4, 17)
        ds = [d_s(greg, s, D) for s in ss]
        for s, v in zip(ss, ds):
            print(f"  {s:12.4g} {v:12.6f}")
        print(f"    s->0   : {ds[0]:.6f}    [BBMM: -> 2 in every D]")
        print(f"    s->inf : {ds[-1]:.6f}    [BBMM: -> Hausdorff = {D}]")
        print()
