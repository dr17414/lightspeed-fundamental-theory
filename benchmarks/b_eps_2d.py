"""
B_eps_2d: smeared causal-set d'Alembertian, 1+1 Minkowski.
Formula taken verbatim from Dowker-Glaser / Sorkin -- no self-designed smearing.

    B_eps^(2) phi(x) = (eps/l^2)[ -2 phi(x) + 4 eps sum_{y<x} f_2(n,eps) phi(y) ]
    f_2(n,eps) = (1-eps)^n [ 1 - 2 eps n/(1-eps) + eps^2 n(n-1)/(2(1-eps)^2) ]
    eps = (l/xi)^2   ->   prefactor eps/l^2 = 1/xi^2

Rules obeyed:
  (1) original f_2, nothing invented;
  (2) xi held FIXED, eps = l^2/xi^2 shrinks as density rises;
  (3) Poisson point count N ~ Poisson(Nbar), l^2 = V/Nbar (the SET density,
      not the realised count);
  (4) three separate checks so a failure localises:
        T1  MC mean  ->  continuum smeared kernel   (is the code right?)
        T2  continuum smeared kernel  ->  box phi   (is xi small enough?)
        T3  std at fixed xi falls with density      (is smearing working?)

Geometry: lightcone coords u,v in [0,1]^2.  dt dx = (1/2) du dv, so the
Minkowski volume of the sprinkling region is V = 1/2 and rho = Nbar/V = 2 Nbar.
Interval volume between y=(u,v) and x=(U,W):  V(y,x) = (1/2)(U-u)(W-v).
Test field phi = u*v  =>  box phi = -4 exactly (box = -4 d_u d_v).
"""
import numpy as np
from scipy import integrate

U, W = 0.85, 0.85            # evaluation point
VOL = 0.5                    # Minkowski volume of [0,1]^2 in lightcone coords

def f2(n, eps):
    """numerically stable (1-eps)^n * polynomial"""
    q = eps/(1.0-eps)
    poly = 1.0 - 2.0*n*q + 0.5*n*(n-1)*q*q
    return np.exp(n*np.log1p(-eps))*poly

def dominance_counts(u, v):
    """n_i = #{j : u_j > u_i and v_j > v_i}  (interior count of I(y_i, x))"""
    M = len(u)
    out = np.empty(M, np.int64)
    step = max(1, 2_000_000//max(M, 1))
    for a in range(0, M, step):
        b = min(a+step, M)
        out[a:b] = ((u[None, :] > u[a:b, None]) &
                    (v[None, :] > v[a:b, None])).sum(1)
    return out

def B_eps_mc(Nbar, xi, seed, field):
    """one Poisson realisation"""
    rng = np.random.default_rng(seed)
    N = rng.poisson(Nbar)
    u = rng.random(N); v = rng.random(N)
    l2 = VOL/Nbar                       # set density, not realised N
    eps = l2/xi**2
    past = (u < U) & (v < W)
    up, vp = u[past], v[past]
    if len(up) == 0: return np.nan
    n = dominance_counts(up, vp)
    s = -2.0*field(U, W) + 4.0*eps*np.sum(f2(n, eps)*field(up, vp))
    return s/xi**2                      # eps/l^2 == 1/xi^2

def B_continuum(xi, field):
    """<B_eps> equals the bare mean with l -> xi:
       (1/xi^2)[ -2 phi(x) + 4 rho int dV e^{-rho V}(1 - 2 rho V + (rho V)^2/2) phi ]
       with rho = 1/xi^2 and dV = (1/2) du dv."""
    rho = 1.0/xi**2
    def integrand(v, u):
        Vy = 0.5*(U-u)*(W-v)
        z = rho*Vy
        return 0.5*np.exp(-z)*(1.0 - 2.0*z + 0.5*z*z)*field(u, v)
    I, _ = integrate.dblquad(integrand, 0, U, lambda _: 0, lambda _: W,
                             epsabs=1e-11, epsrel=1e-11)
    return (-2.0*field(U, W) + 4.0*rho*I)/xi**2

FIELDS = {"phi=1":  (lambda u, v: np.ones_like(u*v),  0.0),
          "phi=u":  (lambda u, v: u*np.ones_like(v),  0.0),
          "phi=v":  (lambda u, v: v*np.ones_like(u),  0.0),
          "phi=uv": (lambda u, v: u*v,               -4.0)}

if __name__ == '__main__':
    print("="*82)
    print(" T2  連續 smeared kernel -> box phi   (1+1，純解析)")
    print("="*82)
    XIS = [0.40, 0.30, 0.20, 0.15, 0.10]
    print(f"{'field':9} {'truth':>6}  " + "  ".join(f"{'xi='+f'{x:.2f}':>10}" for x in XIS))
    print("-"*82)
    for nm, (f, tr) in FIELDS.items():
        print(f"{nm:9} {tr:6.1f}  " + "  ".join(f"{B_continuum(x, f):10.4f}" for x in XIS))

    print()
    print("="*82)
    print(" T1 + T3  蒙地卡羅 (Poisson 計數, <N>=1000 起)")
    print("="*82)
    XI = 0.20; M = 100
    for nm, (f, tr) in FIELDS.items():
        cont = B_continuum(XI, f)
        print(f"\n  {nm}   xi={XI}   連續值={cont:9.4f}   真值={tr:5.1f}")
        print(f"    {'Nbar':>6} {'eps^(1/2)':>10} {'MC mean':>10} {'std err':>9} {'單次 std':>10} {'vs 連續':>9}")
        for Nbar in [1000, 2000, 4000, 8000]:
            v = np.array([B_eps_mc(Nbar, XI, s, f) for s in range(M)])
            m, sd = np.nanmean(v), np.nanstd(v); se = sd/np.sqrt(M)
            e12 = ((VOL/Nbar)/XI**2)**(1/2)
            print(f"    {Nbar:6d} {e12:10.4f} {m:10.4f} {se:9.4f} {sd:10.4f} {(m-cont)/se:8.2f}σ")
