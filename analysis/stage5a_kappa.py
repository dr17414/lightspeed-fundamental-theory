"""Stage 5A (revised): is the SECTOR PAIR canonical, modulo Aut(P) x S_2?

The observable is
    kappa(P) = | R_2(P) / (Aut(P) x S_2) |
where R_2(P) is the set of two-element realizers.  kappa = 1 means every
labelled realizer is either a relabelling of the true one or the global swap of
the two sectors -- i.e. the sector PAIR is canonical.

P(UPO) is NOT the right observable.  UPO is labelled uniqueness, and Winkler's
results say the limiting probabilities of rigidity / unique realizability /
unique orientability for random 2-orders all lie strictly between 0 and 1.  So
P(UPO) ~ 0.3-0.4 flat is the expected behaviour, not an anomaly, and it is too
strong a criterion for a theory in which labels are unphysical anyway.

-----------------------------------------------------------------------------
COMPUTING kappa WITHOUT COMPUTING Aut(P).

Realizers correspond to transitive orientations F of the incomparability graph:
L1 = P u F and L2 = P u F^-1 are linear orders with L1 n L2 = P, and F <-> F^-1
is the S_2 swap.

Now encode a realizer by its PERMUTATION DIAGRAM: let r1, r2 be the ranks in
L1, L2 and set pi(i) = r2 of the element with r1 = i.  Then

    x < y in P   <=>   i < j  and  pi(i) < pi(j).

pi is a permutation of positions, not of elements, so RELABELLING THE ELEMENTS
DOES NOT CHANGE IT.  Conversely, two realizers with the same pi are related by
the bijection matching equal L1-ranks, which is a poset automorphism.  Hence

    realizers are Aut(P)-equivalent  <=>  they have the same pi,

and the S_2 swap sends pi to pi^-1.  So

    kappa(P) = #{ pi from realizers } / (pi ~ pi^-1)

exactly, with no automorphism group computation anywhere.

-----------------------------------------------------------------------------
RETRACTION (was wrong in the previous version of this file).

It was claimed that if the parent realizer is unique then deleting an element
and restricting agrees automatically.  That does not follow.  Restricting a
realizer of P does give a realizer of P - {x}, but P - {x} may admit MORE
realizers: elements that x kept apart can become twins once x is gone.  A parent
with 2 implication classes can have a child with 4.  So the deletion test has
independent content and must be kept.

With kappa rather than UPO the content is sharper but still real: if
kappa(child) = 1 then every child realizer is a relabelling of the restricted
true one, so recovery is safe; the test is therefore whether kappa = 1 SURVIVES
deletion, not whether the labelled realizer is unchanged.

-----------------------------------------------------------------------------
ALSO FIXED: the 2+1D negative control now sprinkles into an Alexandrov interval
(a causal diamond), matching the 1+1D case, instead of a t x square box.  The
previous version conflated region shape with dimension.

WHAT THE NUMBERS SUPPORT, AND WHAT THEY DO NOT.  P(kappa = 1) rises with N
(0.765 at N = 20 to 0.96-1.00 by N >= 100), and finite-N counterexamples still
occur at N = 400.  That supports "highly canonical at the tested scales" and NOT
"asymptotically almost surely".  Do not pool the per-N frequencies into a single
Clopper-Pearson interval either: p = p(N) need not be one parameter, so a pooled
interval would be answering a question nobody asked.

NAMING, and the boundary that matters most.  What is established here is

    (C, <)  ->  { U, V } / S_2

a pair of canonical GLOBAL null orderings.  That is NOT

    a two-state internal degree of freedom at each event,

which is what Dirac chirality means: psi(x) = (psi_L(x), psi_R(x)).  U and V are
two total orders on the same set of events, not a local internal space.  The two
must not be quietly merged.

So the next question is not mixing.  It is whether (U, V) plus < suffice to
define, AT EACH EVENT, a local "advance along U" and "advance along V" successor
rule -- without picking it by hand on Hasse links.  If that fails, the result is
a precise Result B: order supplies two global null axes but not local chirality.
Only if the local shift exists does the question of amplitude-induced U/V mixing,
and whether it becomes a continuum mass term, arise.

A positive result here is a CANDIDATE CHIRAL PRECURSOR, not chirality.
"""
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components


# ------------------------------------------------------------------ sprinkling

def sprinkle_2d(N, rng):
    """Causal diamond in 1+1D.  In null coordinates the diamond is a square."""
    u, v = rng.random(N), rng.random(N)
    R = (u[:, None] < u[None, :]) & (v[:, None] < v[None, :])
    return R


def sprinkle_diamond(N, D, rng, batch=20000):
    """Uniform sprinkling into an Alexandrov interval of D-dim Minkowski,
    between the origin and (1, 0, ..., 0).  D = 2 reproduces sprinkle_2d up to
    coordinates; D = 3, 4 are the negative controls, now with the SAME region
    shape so that only the dimension differs."""
    d = D - 1
    pts = []
    while len(pts) < N:
        t = rng.random(batch)
        x = (rng.random((batch, d)) * 2 - 1) * 0.5
        r = np.linalg.norm(x, axis=1)
        keep = (r < t) & (r < 1 - t)
        for row, tt in zip(x[keep], t[keep]):
            pts.append((tt, row))
            if len(pts) >= N:
                break
    t = np.array([p[0] for p in pts])
    X = np.array([p[1] for p in pts])
    dt = t[None, :] - t[:, None]
    d2 = ((X[None, :, :] - X[:, None, :]) ** 2).sum(-1)
    return (dt > 0) & (dt ** 2 > d2)


# ------------------------------------------------------- implication classes

class DSU:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, a):
        while self.p[a] != a:
            self.p[a] = self.p[self.p[a]]
            a = self.p[a]
        return a

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


def implication_classes(R):
    """Golumbic forcing classes on directed edges of the incomparability graph.
    Returns (classes, comparability_ok) where classes maps root -> list of (a,b)."""
    N = R.shape[0]
    G = ~(R | R.T)
    np.fill_diagonal(G, False)
    dsu = DSU(N * N)
    idx = lambda a, b: a * N + b

    for a in range(N):
        nb = np.flatnonzero(G[a])
        if nb.size < 2:
            continue
        sub = ~G[np.ix_(nb, nb)]
        np.fill_diagonal(sub, False)
        _, lab = connected_components(csr_matrix(sub), directed=False)
        first = {}
        for k, l in enumerate(lab):
            if l in first:
                dsu.union(idx(a, nb[first[l]]), idx(a, nb[k]))
                dsu.union(idx(nb[first[l]], a), idx(nb[k], a))
            else:
                first[l] = k

    ea, eb = np.nonzero(G)
    classes = {}
    ok = True
    for a, b in zip(ea, eb):
        r = dsu.find(idx(a, b))
        classes.setdefault(r, []).append((a, b))
        if dsu.find(idx(b, a)) == r:
            ok = False
    return classes, ok, dsu, G


# --------------------------------------------------------------------- kappa

def _is_transitive_tournament(T):
    """T is a tournament (exactly one of (a,b),(b,a) for every pair).  Such a
    tournament is transitive iff its outdegrees are a permutation of
    0, 1, ..., N-1 -- O(N^2) instead of the O(N^3) boolean matrix product."""
    N = T.shape[0]
    d = np.sort(T.sum(axis=1))
    return bool((d == np.arange(N)).all())


def realizer_permutations(R, max_classes=14, max_combos=4096):
    """All realizers, encoded as label-free permutation diagrams pi.

    Returns None if the instance is too branchy to enumerate (recorded, not
    silently dropped)."""
    N = R.shape[0]
    classes, ok, dsu, G = implication_classes(R)
    if not ok:
        return "dim>2"
    idx = lambda a, b: a * N + b

    # pair each class with its reverse; keep one representative per pair
    roots = list(classes)
    partner = {}
    for r in roots:
        a, b = classes[r][0]
        partner[r] = dsu.find(idx(b, a))
    reps, seen = [], set()
    for r in roots:
        if r in seen:
            continue
        seen.add(r)
        seen.add(partner[r])
        reps.append(r)
    k = len(reps)
    if k > max_classes or (1 << k) > max_combos:
        return None

    pis = set()
    for mask in range(1 << k):
        F = np.zeros((N, N), dtype=bool)
        for i, r in enumerate(reps):
            src = classes[r] if (mask >> i & 1) else classes[partner[r]]
            for a, b in src:
                F[a, b] = True
        # BOTH linear orders must be checked.  L1 = P u F and L2 = P u F^-1 are
        # separate conditions; verifying only L1 leaves a mirror-image gap.  No
        # counterexample (L1 valid, L2 invalid) has been found by exhaustive
        # search to N = 7 or in thousands of random 2D orders, but the
        # mathematical condition is two-sided and is now written as such.
        L1 = R | F
        L2 = R | F.T
        if not (_is_transitive_tournament(L1) and _is_transitive_tournament(L2)):
            continue
        r1 = L1.sum(axis=1)                # bigger = earlier; ranks are unique
        r2 = L2.sum(axis=1)
        o1 = np.argsort(-r1)
        pos2 = np.empty(N, int)
        pos2[np.argsort(-r2)] = np.arange(N)
        pi = tuple(pos2[o1])
        inv = tuple(np.argsort(np.array(pi)))
        pis.add(min(pi, inv))
    return pis


def clopper_pearson(k, n, alpha=0.05):
    """Two-sided Clopper-Pearson interval, valid only for INDEPENDENT Bernoulli
    trials.  Used for the per-N sprinkling frequencies (independent draws) and
    for parent-level deletion outcomes.  NOT used for child-level deletion
    counts, where five children share a parent, nor for a pooled fraction across
    several N, where p = p(N) need not be the same parameter."""
    from scipy.stats import beta
    lo = beta.ppf(alpha / 2, k, n - k + 1) if k > 0 else 0.0
    hi = beta.ppf(1 - alpha / 2, k + 1, n - k) if k < n else 1.0
    return float(lo), float(hi)


def kappa(R):
    out = realizer_permutations(R)
    if out in ("dim>2", None):
        return out
    return len(out)


if __name__ == "__main__":
    # Independent stream per block.  Previously one shared rng meant that
    # changing the N=400 trial count silently shifted every later table -- a
    # source-of-record fragility of exactly the kind this project has been
    # burned by.  Adding an N=800 row must not renumber the negative control.
    rng_retraction = np.random.default_rng(20260825)
    rng_main = np.random.default_rng(11001)
    rng_deletion = np.random.default_rng(22002)
    rng_negative = np.random.default_rng(33003)

    rng = rng_retraction
    print("RETRACTION CHECK: does a UPO parent always have a UPO child?")
    found = 0
    for _ in range(4000):
        R = sprinkle_2d(7, rng)
        cls, ok, _, _ = implication_classes(R)
        if not (ok and len(cls) == 2):
            continue
        for x in range(7):
            m = np.ones(7, bool)
            m[x] = False
            Rc = R[np.ix_(m, m)]
            c2, ok2, _, _ = implication_classes(Rc)
            if ok2 and len(c2) > 2:
                print(f"  counterexample: parent 2 classes -> child {len(c2)} "
                      f"classes after deleting element {x}")
                found += 1
                break
        if found:
            break
    if not found:
        print("  none found in 4000 draws")

    print("\nMAIN: kappa = |R_2 / (Aut x S_2)| for 1+1D sprinklings")
    print("  P(kappa=1) is a MEASURED FREQUENCY with a 95% Clopper-Pearson")
    print("  interval, not evidence of asymptotic almost-sure uniqueness.")
    print(f"{'N':>6} {'trials':>7} {'kappa=1':>9} {'P(kappa=1)':>12} "
          f"{'95% CP':>18} {'P(UPO)':>9} {'skip':>6}")
    for N, T in ((20, 200), (50, 150), (100, 80), (200, 40), (400, 40)):
        k1 = upo = skip = done = 0
        for _ in range(T):
            R = sprinkle_2d(N, rng_main)
            cls, ok, _, _ = implication_classes(R)
            upo += (ok and len(cls) == 2)
            kk = kappa(R)
            if kk is None:
                skip += 1
                continue
            done += 1
            k1 += (kk == 1)
        lo, hi = clopper_pearson(k1, max(done, 1))
        print(f"{N:>6} {T:>7} {k1:>9} {k1 / max(done, 1):>12.3f} "
              f"{f'[{lo:.3f}, {hi:.3f}]':>18} {upo / T:>9.3f} {skip:>6}")

    print("\nDELETION STABILITY: does kappa = 1 survive removing one element?")
    print("  The 5 children of a parent SHARE that parent, so they are not")
    print("  independent Bernoulli trials.  Raw child counts are reported")
    print("  WITHOUT a child-level interval; the independent unit is the")
    print("  parent, so the interval is given for 'all 5 deletions survived'.")
    print(f"{'N':>6} {'parents':>8} {'children':>9} {'kept':>6} "
          f"{'clean parents':>14} {'95% CP (parent)':>20}")
    for N, T in ((50, 30), (100, 20)):
        par = ch = kept = clean = 0
        for _ in range(T):
            R = sprinkle_2d(N, rng_deletion)
            if kappa(R) != 1:
                continue
            par += 1
            ok_all = True
            for x in rng_deletion.choice(N, 5, replace=False):
                m = np.ones(N, bool)
                m[x] = False
                kk = kappa(R[np.ix_(m, m)])
                # Fail loudly rather than skip.  A skipped child used to leave
                # ok_all untouched, so a parent could be counted as clean on the
                # strength of children that were never evaluated.  No skips occur
                # at these N (children = 5 x parents confirms it), but the silent
                # path must not exist.
                assert kk != "dim>2", (
                    "an induced subposet of a dimension-2 poset is still the "
                    "intersection of the same two linear orders restricted, so "
                    "dimension cannot rise under deletion; this is a bug, not "
                    "a property of the data")
                assert kk is not None, (
                    "enumeration cap hit; raise max_classes/max_combos rather "
                    "than dropping the sample")
                ch += 1
                if kk == 1:
                    kept += 1
                else:
                    ok_all = False
            clean += ok_all
        lo, hi = clopper_pearson(clean, max(par, 1))
        print(f"{N:>6} {par:>8} {ch:>9} {kept:>6} "
              f"{clean / max(par, 1):>14.3f} {f'[{lo:.3f}, {hi:.3f}]':>20}")

    print("\nNEGATIVE CONTROL: matched causal diamonds, how often does dim<=2?")
    print(f"{'N':>6} {'D=2':>8} {'D=3':>8} {'D=4':>8}")
    for N, T in ((10, 120), (20, 120), (40, 60), (80, 30)):
        row = []
        for D in (2, 3, 4):
            c = 0
            for _ in range(T):
                R = sprinkle_diamond(N, D, rng_negative)
                _, ok, _, _ = implication_classes(R)
                c += ok
            row.append(c / T)
        print(f"{N:>6} {row[0]:>8.3f} {row[1]:>8.3f} {row[2]:>8.3f}")
