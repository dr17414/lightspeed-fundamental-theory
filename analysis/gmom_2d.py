"""
Stage 2, step 1: momentum-space function of the CONTINUUM-averaged nonlocal
d'Alembertian in d=2.  Pure analysis -- no discrete matrix, no BB^dagger.

Continuum-averaged operator (already validated in b_eps.py):
  Bbar phi(x) = (1/xi^2)[ -2 phi(x)
                 + 4 rho int_{J^-(x)} dV e^{-rho V}(1 - 2 rho V + (rho V)^2/2) phi(y) ]
with rho = 1/xi^2.

Act on a plane wave.  Lightcone separation (a,b), a,b>0 past-directed:
  V = ab/2,  dV = (1/2) da db.  Writing the plane-wave factor as
  exp(-(beta a + gamma b)) and substituting s=beta*a, r=gamma*b:

  int -> Lambda * int_0^inf int_0^inf ds dr e^{-s-r} K(Lambda s r),
  K(z) = e^{-z}(1 - 2z + z^2/2),   Lambda = rho/(2 beta gamma)  ~  rho/p^2

so the whole thing depends on ONE dimensionless variable Lambda ~ rho/p^2.
IR is Lambda -> infinity (p^2 -> 0);  UV is Lambda -> 0 (p^2 -> infinity).
"""
import numpy as np
from scipy import integrate

def K(z): return np.exp(-z)*(1.0 - 2.0*z + 0.5*z*z)

def F(Lam):
    """Lam * int int ds dr e^{-s-r} K(Lam s r)"""
    f = lambda r, s: np.exp(-s-r)*K(Lam*s*r)
    I, _ = integrate.dblquad(f, 0, np.inf, lambda _: 0, lambda _: np.inf,
                             epsabs=1e-12, epsrel=1e-10)
    return Lam*I

if __name__ == '__main__':
    print("g(Lambda) * xi^2 = -2 + 4 F(Lambda)      [Lambda ~ rho/p^2]")
    print()
    print(f"{'Lambda':>10} {'F':>14} {'g*xi^2':>14} {'g*xi^2*Lambda':>16}")
    print("-"*58)
    for Lam in [1e-4,1e-3,1e-2,1e-1,1,10,100,1000,1e4,1e5]:
        Fv=F(Lam); g=-2+4*Fv
        print(f"{Lam:10.0e} {Fv:14.6e} {g:14.6e} {g*Lam:16.6e}")
    print()
    print("IR  (Lambda -> inf, p^2 -> 0):  g*xi^2*Lambda -> const  =>  g ~ 1/Lambda ~ p^2  (recovers box)")
    print("UV  (Lambda -> 0,  p^2 -> inf): g*xi^2 -> -2 (constant)  =>  g SATURATES, does not grow")
