"""
Cross-check: repo's own continuum g(p^2)  vs  literature Eq.(15) of
Belenchia, Benincasa, Marciano, Modesto, arXiv:1507.00330 (PRD 93, 044017).

Paper d=2 minimal nonlocal d'Alembertian, momentum space (their Eq. 15):

  g^(2)(k^2) = a2 * rho
             + 2 rho * sum_{n=0..2} (b_n/n!) * gam^n
               * int_0^inf dxi  xi^(2n+1) e^{-gam xi^2} K_0( sqrt(k^2/rho) xi )

  a2 = -2 ;  b0 = 4, b1 = -8, b2 = 4 ;  gam printed as sqrt(pi)/4 in Eq.(15).

Their Eq.(3) general formula gives gamma_d = (pi/4)^((d-1)/2) / (d Gamma((d+1)/2)),
which for d=2 evaluates to 1/2, NOT sqrt(pi)/4.  We do not guess: we test the
candidates against the two limits the paper states independently
(IR: g -> -k^2 ; UV: g -> a2*rho = -2 rho) and against the repo's own
independently derived g.  Nothing is invented here.
"""
import numpy as np
from scipy import integrate, special

A2 = -2.0
B = [4.0, -8.0, 4.0]          # b_0, b_1, b_2  (paper divides by n!)


def g2_paper(k2, rho=1.0, gam=np.sqrt(np.pi) / 4.0):
    """Eq.(15) evaluated for real k2 > 0 (Euclidean / spacelike section)."""
    q = np.sqrt(k2 / rho)
    tot = 0.0
    for n in range(3):
        c = B[n] / special.factorial(n) * gam ** n

        def integrand(x, n=n):
            return x ** (2 * n + 1) * np.exp(-gam * x * x) * special.kv(0, q * x)

        I, _ = integrate.quad(integrand, 0, np.inf, limit=400,
                              epsabs=1e-13, epsrel=1e-11)
        tot += c * I
    return A2 * rho + 2.0 * rho * tot


# ---- repo's own operator, re-expressed in k^2 ------------------------------
# repo: g*xi^2 = -2 + 4 F(Lam),  Lam ~ rho/p^2.  Its IR limit g*xi^2*Lam -> -2
# fixes the normalisation to Lam = 2 rho / k^2  (so that g -> -k^2).
def K(z):
    return np.exp(-z) * (1.0 - 2.0 * z + 0.5 * z * z)


def g2_repo(k2, rho=1.0):
    Lam = 2.0 * rho / k2
    f = lambda r, s: np.exp(-s - r) * K(Lam * s * r)
    I, _ = integrate.dblquad(f, 0, np.inf, lambda _: 0, lambda _: np.inf,
                             epsabs=1e-12, epsrel=1e-10)
    return rho * (-2.0 + 4.0 * Lam * I)


if __name__ == '__main__':
    import warnings
    warnings.filterwarnings('ignore')
    rho = 1.0
    print("rho = 1.  IR target: g -> -k^2.   UV target: g -> a2*rho = -2.\n")
    hdr = f"{'k^2':>10} {'-k^2':>12} {'repo g':>13} " \
          f"{'Eq15 gam=sqrtpi/4':>19} {'Eq15 gam=1/2':>14} {'Eq15 gam=1/4':>14}"
    print(hdr)
    print("-" * len(hdr))
    for k2 in [1e-3, 1e-2, 1e-1, 0.5, 1.0, 2.0, 10.0, 100.0, 1e3, 1e4]:
        print(f"{k2:10.0e} {-k2:12.5f} {g2_repo(k2, rho):13.6f} "
              f"{g2_paper(k2, rho, np.sqrt(np.pi)/4):19.6f} "
              f"{g2_paper(k2, rho, 0.5):14.6f} "
              f"{g2_paper(k2, rho, 0.25):14.6f}")
