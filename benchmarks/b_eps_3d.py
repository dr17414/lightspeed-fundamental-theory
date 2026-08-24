"""
B_eps_3d: smeared causal-set d'Alembertian in 2+1 Minkowski.

Coefficients (Dowker-Glaser, cross-verified against the stated numerical value
to 15 digits before use):
    C^(3)  = (1, -27/8, 9/4)
    beta_3 = (pi/(3*sqrt(2)))**(2/3) / Gamma(5/3) = 0.906658729670436
    alpha_3 = -beta_3

    B_eps^(d) phi(x) = (eps^(2/d)/l^2)[ alpha_d phi(x)
                                        + beta_d eps sum_{y<x} f_d(n,eps) phi(y) ]
    eps = (l/xi)^d ;  for d=3 the prefactor eps^(2/3)/l^2 collapses to 1/xi^2
    f_3(n,eps) = (1-eps)^n [ 1 - (27/8) n q + (9/8) n(n-1) q^2 ],  q = eps/(1-eps)

GEOMETRY -- deliberately NOT a causal diamond.
The past lightcone of any interior point of a diamond pokes out through the
diamond's lower boundary, which is the finite-size correction E(xi,L) that
Dowker-Glaser had to subtract.  Instead we sprinkle into exactly the truncated
past cone of the evaluation point,
    P = {(t,r) : 0 < t < T,  r < T - t},
so the Monte Carlo and the continuum integral cover the SAME region and the
T1 check (MC -> continuum) is clean.  The truncation at t=0 is still a finite
-size effect, but it now shows up only in T2 (continuum -> box phi), where it
is supposed to, and it dies away as xi << T.

Volume of P: pi*T^3/3.  Interval volume in 2+1: V(tau) = (pi/12) tau^3.
Test field phi = t^2  =>  box phi = -2  (box = -d_t^2 + d_x^2 + d_y^2).
"""
import numpy as np
from scipy.special import gamma as Gamma
from scipy import integrate

T = 1.0
BETA3 = (np.pi/(3*np.sqrt(2)))**(2/3)/Gamma(5/3)
ALPHA3 = -BETA3
C3 = (1.0, -27/8, 9/4)
VOL_P = np.pi*T**3/3

def f3(n, eps):
    q = eps/(1.0-eps)
    poly = 1.0 - (27/8)*n*q + (9/8)*n*(n-1)*q*q
    return np.exp(n*np.log1p(-eps))*poly

def sample_cone(N, rng):
    """uniform in P: density in t is proportional to (T-t)^2"""
    s = T*rng.random(N)**(1/3)                 # s = T - t
    t = T - s
    r = s*np.sqrt(rng.random(N))
    th = 2*np.pi*rng.random(N)
    return t, r*np.cos(th), r*np.sin(th)

def B3_mc(Nbar, xi, seed, field):
    rng = np.random.default_rng(seed)
    N = rng.poisson(Nbar)
    t, x, y = sample_cone(N, rng)
    l3 = VOL_P/Nbar                            # set density, not realised N
    eps = l3/xi**3
    # n_i = #{ j : y_i < z_j < x }   (all points are already in the past of x)
    n = np.empty(N, np.int64)                  # chunked: N^2 matrix is too big
    step = max(1, 4_000_000//max(N, 1))
    for a in range(0, N, step):
        b = min(a+step, N)
        dt = t[None, :] - t[a:b, None]
        dr = np.sqrt((x[None, :]-x[a:b, None])**2 + (y[None, :]-y[a:b, None])**2)
        n[a:b] = ((dt > dr) & (dt > 0)).sum(1)
    s = ALPHA3*field(T) + BETA3*eps*np.sum(f3(n, eps)*field(t))
    return s/xi**2

def B3_continuum(xi, field):
    """<B_eps> = bare mean with l -> xi.  rho_xi = 1/xi^3.
       dV = dDelta * 2*pi*tau*dtau over the same truncated cone."""
    rho = 1.0/xi**3
    def inner(tau, D):
        V = (np.pi/12)*tau**3
        z = rho*V
        lay = C3[0] + C3[1]*z + C3[2]*z*z/2
        return 2*np.pi*tau*np.exp(-z)*lay*field(T-D)
    I, _ = integrate.dblquad(inner, 0, T, lambda _: 0, lambda D: D,
                             epsabs=1e-10, epsrel=1e-9)
    return (ALPHA3*field(T) + BETA3*rho*I)/xi**2

FIELDS = {"phi=1":  (lambda t: np.ones_like(t),  0.0),
          "phi=t":  (lambda t: t,                0.0),
          "phi=t^2":(lambda t: t*t,             -2.0)}

if __name__ == '__main__':
    print("="*82)
    print(" T2  連續 smeared kernel -> box phi   (2+1，純解析)")
    print("="*82)
    XIS = [0.40, 0.30, 0.20, 0.15, 0.10]
    print(f"{'field':9} {'truth':>6}  " + "  ".join(f"{'xi='+f'{x:.2f}':>10}" for x in XIS))
    print("-"*82)
    for nm, (f, tr) in FIELDS.items():
        print(f"{nm:9} {tr:6.1f}  " + "  ".join(f"{B3_continuum(x, f):10.4f}" for x in XIS))

    print()
    print("="*82)
    print(" T1 + T3  蒙地卡羅 (Poisson 計數, <N>=1000 起)")
    print("="*82)
    XI = 0.20; M = 100
    for nm, (f, tr) in FIELDS.items():
        cont = B3_continuum(XI, f)
        print(f"\n  {nm}   xi={XI}   連續值={cont:9.4f}   真值={tr:5.1f}")
        print(f"    {'Nbar':>6} {'eps^(1/3)':>10} {'MC mean':>10} {'std err':>9} {'單次 std':>10} {'vs 連續':>9}")
        for Nbar in [1000, 2000, 4000, 8000]:
            v = np.array([B3_mc(Nbar, XI, s, f) for s in range(M)])
            m, sd = np.nanmean(v), np.nanstd(v); se = sd/np.sqrt(M)
            e13 = ((VOL_P/Nbar)/XI**3)**(1/3)
            print(f"    {Nbar:6d} {e13:10.4f} {m:10.4f} {se:9.4f} {sd:10.4f} {(m-cont)/se:8.2f}σ")
