"""
Order-only benchmark: does the scale-resolved MM profile add information
that interval abundance S_m does not already provide?
=====================================================================
Per GPT's protocol.  Two purely order-theoretic observables, no operator,
no amplitude, computed on the SAME ensemble:

  (1) S_m  -- interval abundance (Glaser-Surya line, and the 2026
              graph-observables paper).  Established literature tool.
  (2) d_MM(N_I) -- scale-resolved MM profile.  Our candidate addition.
              NOT "nested" intervals: random sampling of p<q binned by |I(p,q)|.

Stress-test family (2026 paper's family, as far as we can reproduce it):
  3-layer KR, 5/10/25-layer orders, random transitive poset,
  1+1 lattice, 1+1 and 2+1 Poisson sprinklings.

Statistics: each causal set realization yields ONE profile; we report
ensemble mean +/- scatter over independent realizations.  Intervals inside
one realization are strongly correlated and are NOT independent samples.
"""
import numpy as np
from scipy.special import gamma
from scipy.optimize import brentq

def r_of_d(d): return gamma(d+1)*gamma(d/2)/(2*gamma(1.5*d))
def inv_r(r):
    if not np.isfinite(r): return np.nan
    if r >= 1-1e-9: return 1.0
    if r <= 1e-9:   return np.nan          # antichain interior: undefined
    try: return brentq(lambda d: r_of_d(d)-r, 1.0, 20.0)
    except: return np.nan

# ---------------- causal set family ----------------------------------------

def _close(o):
    """transitive closure (boolean, few iterations suffice for layered)"""
    A = o.copy()
    for _ in range(int(np.ceil(np.log2(max(o.shape[0], 2)))) + 1):
        A2 = A | ((A.astype(np.int32) @ A.astype(np.int32)) > 0)
        if (A2 == A).all(): break
        A = A2
    return A

def kr3(n, seed=0, p=0.5):
    rng = np.random.default_rng(seed)
    a, b = n//4, n//2
    o = np.zeros((n, n), bool)
    o[0:a, a:a+b] = rng.random((a, b)) < p
    o[a:a+b, a+b:] = rng.random((b, n-a-b)) < p
    return _close(o)

def layered(L):
    def f(n, seed=0, p=0.5):
        rng = np.random.default_rng(seed)
        bnd = np.linspace(0, n, L+1).astype(int)
        o = np.zeros((n, n), bool)
        for i in range(L-1):
            s1, e1 = bnd[i], bnd[i+1]; s2, e2 = bnd[i+1], bnd[i+2]
            o[s1:e1, s2:e2] = rng.random((e1-s1, e2-s2)) < p
        return _close(o)
    return f

def random_poset(n, seed=0, p=0.06):
    rng = np.random.default_rng(seed)
    o = np.triu(rng.random((n, n)) < p, 1)
    return _close(o)

def lattice_1p1(n, seed=0):
    s = int(np.ceil(np.sqrt(n)))           # FIX: return exactly n elements
    u, v = np.meshgrid(np.arange(s), np.arange(s), indexing='ij')
    u = u.ravel()[:n]; v = v.ravel()[:n]
    o = (u[:, None] < u[None, :]) & (v[:, None] < v[None, :])
    return o

def sprinkle(dim):
    def f(n, seed=0):
        rng = np.random.default_rng(seed); pts = []
        while len(pts) < n:
            m = 3*(n-len(pts))+20
            t = rng.random(m); x = (rng.random((m, dim-1))-0.5)*2
            ok = np.linalg.norm(x, axis=1) < np.minimum(t, 1-t)
            for tt, xx in zip(t[ok], x[ok]):
                if len(pts) < n: pts.append((tt, xx))
        pts.sort(key=lambda P: P[0])
        T = np.array([P[0] for P in pts]); X = np.array([P[1] for P in pts])
        o = np.zeros((n, n), bool)
        for i in range(n):
            o[i] = (T-T[i]) > np.linalg.norm(X-X[i], axis=1)
        return o
    return f

FAMILY = {
    "KR_3layer":    kr3,
    "layered_5":    layered(5),
    "layered_10":   layered(10),
    "layered_25":   layered(25),
    "random_poset": random_poset,
    "lattice_1p1":  lattice_1p1,
    "sprinkle_1p1": sprinkle(2),
    "sprinkle_2p1": sprinkle(3),
}
TRUE_D = {"sprinkle_1p1": 2, "sprinkle_2p1": 3, "lattice_1p1": 2}

# ---------------- the two observables --------------------------------------

def interior_sizes(o):
    """number of elements STRICTLY between p and q, for every related pair.
    Paper's inclusive cardinality |I[p,q]| = interior + 2."""
    A = o.astype(np.int32)
    return (A @ A)[o]

def abundance(o, m_lo=2, m_hi=8):
    """Interval abundance in the 2026-paper convention:
         S_m = n * (#{pairs with inclusive |I[p,q]| = m}) / (#{related pairs})
       m is INCLUSIVE cardinality, so a link has m=2.
       Returns array over m = m_lo .. m_hi."""
    n = o.shape[0]
    interior = interior_sizes(o)
    if interior.size == 0: return np.full(m_hi-m_lo+1, np.nan)
    incl = interior + 2
    denom = float(interior.size)
    return np.array([n*(incl == m).sum()/denom for m in range(m_lo, m_hi+1)])

BINS = [(4,8),(8,16),(16,32),(32,64),(64,128)]
def mm_profile(o, nsample=6000, seed=0):
    """Returns {bin_centre: (r, d_MM)}.  Bin centres are INTERIOR element
    counts k (inclusive cardinality = k+2).  r kept so that r=0 (antichain
    interior) survives as a signal rather than collapsing to nan."""
    n = o.shape[0]; rng = np.random.default_rng(seed)
    rows = []
    idx = np.argwhere(o)
    if len(idx) == 0: return {}
    pick = idx[rng.integers(0, len(idx), min(nsample, 4*len(idx)))]
    for i, j in pick:
        m = o[i, :] & o[:, j]
        k = int(m.sum())
        if k < 4: continue
        sub = o[np.ix_(m, m)]
        rows.append((k, sub.sum()/(k*(k-1)/2)))
    if not rows: return {}
    rows = np.array(rows); out = {}
    for lo, hi in BINS:
        sel = rows[(rows[:,0] >= lo) & (rows[:,0] < hi)]
        if len(sel) < 20: continue
        rbar = sel[:,1].mean()
        out[(lo+hi)//2] = (rbar, inv_r(rbar))
    return out
