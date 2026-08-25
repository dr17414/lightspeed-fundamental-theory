"""Regression tests for Stage 5A: kappa = |R_2(P) / (Aut(P) x S_2)|.

WHY THIS FILE EXISTS.  The kappa computation rests on one claim: the permutation
diagram pi is a complete invariant for Aut(P)-orbits of realizers, so kappa can
be counted without ever constructing Aut(P).  That claim was checked against
brute force in a session transcript, which is not a reproducible artifact.  The
cross-check belongs here, where CI runs it.

The brute-force reference computes, independently and with no shared code path:
  * all transitive orientations of the incomparability graph, by enumerating
    2^m assignments and testing transitivity;
  * all automorphisms of P, by enumerating N! permutations;
  * the orbit count under Aut(P) x S_2 directly.

Fixed kappa > 1 examples are pinned so the test cannot pass merely by agreeing
on the easy kappa = 1 case.
"""
import itertools
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.stage5a_kappa import (  # noqa: E402
    implication_classes, kappa, realizer_permutations, sprinkle_2d,
    sprinkle_diamond,
)

# Pinned instances, found by search and verified by brute force below.
KAPPA_1 = np.array([[0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0], [0, 0, 0, 1, 0]], dtype=bool)
KAPPA_2 = np.array([[0, 1, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 0]], dtype=bool)
KAPPA_3 = np.array([[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 1, 1, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0]], dtype=bool)


# ------------------------------------------------------------- brute reference

def brute_transitive_orientations(R):
    N = R.shape[0]
    G = ~(R | R.T)
    np.fill_diagonal(G, False)
    E = [(a, b) for a in range(N) for b in range(a + 1, N) if G[a, b]]
    assert len(E) <= 18, "brute reference is exponential; keep instances tiny"
    out = []
    for mask in range(1 << len(E)):
        F = np.zeros((N, N), dtype=bool)
        for k, (a, b) in enumerate(E):
            F[a, b] = bool(mask >> k & 1)
            F[b, a] = not F[a, b]
        if not (F @ F & ~F).any():
            out.append(F.copy())
    return out


def brute_automorphisms(R):
    N = R.shape[0]
    assert N <= 8, "brute reference is N!; keep instances tiny"
    return [np.array(p) for p in itertools.permutations(range(N))
            if np.array_equal(R[np.ix_(np.array(p), np.array(p))], R)]


def brute_kappa(R):
    """Orbit count of transitive orientations under Aut(P) x S_2, computed
    directly.  Shares no code with realizer_permutations()."""
    TOs = brute_transitive_orientations(R)
    A = brute_automorphisms(R)
    keys = []
    for F in TOs:
        orb = set()
        for p in A:
            Fp = F[np.ix_(p, p)]
            orb.add(Fp.tobytes())
            orb.add(Fp.T.tobytes())          # the S_2 swap
        keys.append(min(orb))
    return len(set(keys))


# ------------------------------------------------------------------- the tests

@pytest.mark.parametrize("R,expected", [(KAPPA_1, 1), (KAPPA_2, 2), (KAPPA_3, 3)])
def test_pinned_instances(R, expected):
    """kappa > 1 cases are pinned, so agreement cannot come from the easy case
    alone."""
    assert kappa(R) == expected
    assert brute_kappa(R) == expected


def test_kappa_matches_brute_force_orbit_count():
    """The load-bearing claim: pi is a complete invariant for Aut(P)-orbits."""
    rng = np.random.default_rng(20260825)
    checked = 0
    for N in (5, 6, 7):
        for _ in range(10):
            R = sprinkle_2d(N, rng)
            got = realizer_permutations(R)
            if got in ("dim>2", None):
                continue
            assert len(got) == brute_kappa(R)
            checked += 1
    assert checked >= 25


def test_sprinklings_are_always_dimension_two():
    """A 1+1D sprinkling is by construction the intersection of the u and v
    orders, so the incomparability graph must be a comparability graph."""
    rng = np.random.default_rng(5)
    for N in (20, 50, 100):
        _, ok, _, _ = implication_classes(sprinkle_2d(N, rng))
        assert ok


def test_true_coordinates_are_among_the_realizers():
    """Sanity on the encoding: the sealed (u, v) must appear as a realizer."""
    rng = np.random.default_rng(11)
    N = 30
    u, v = rng.random(N), rng.random(N)
    R = (u[:, None] < u[None, :]) & (v[:, None] < v[None, :])
    pis = realizer_permutations(R)
    assert pis not in ("dim>2", None)
    o1 = np.argsort(u)
    pos2 = np.empty(N, int)
    pos2[np.argsort(v)] = np.arange(N)
    pi = tuple(pos2[o1])
    inv = tuple(np.argsort(np.array(pi)))
    assert min(pi, inv) in pis


def test_kappa_one_is_common_at_moderate_N():
    """Trend check only.  Deliberately loose: the point of record is the
    benchmark table, not this bound.  P(kappa=1) is a measured frequency, NOT a
    proof of asymptotic almost-sure uniqueness -- 40/40 has a 95% Clopper-Pearson
    interval of [0.912, 1.0], so it does not license "almost surely"."""
    rng = np.random.default_rng(2026)
    hits = sum(kappa(sprinkle_2d(100, rng)) == 1 for _ in range(20))
    assert hits >= 16


def test_higher_dimensional_diamonds_are_not_dimension_two():
    """Negative control, matched region shape: at N >= 40 a 2+1D or 3+1D
    sprinkling into an Alexandrov interval should essentially never be an order
    of dimension 2.  Below N ~ 20 the test has little discriminating power, which
    is itself the point."""
    rng = np.random.default_rng(77)
    for D in (3, 4):
        fakes = sum(implication_classes(sprinkle_diamond(40, D, rng))[1]
                    for _ in range(8))
        assert fakes == 0


def test_deletion_can_increase_the_number_of_implication_classes():
    """Pins the retraction: a UPO parent need NOT have a UPO child.  Restricting
    a realizer gives *a* realizer of the child, but the child may admit more --
    elements kept apart by the deleted event can become twins.  So the deletion
    test has independent content and must not be dropped."""
    rng = np.random.default_rng(20260825)
    found = False
    for _ in range(4000):
        R = sprinkle_2d(7, rng)
        cls, ok, _, _ = implication_classes(R)
        if not (ok and len(cls) == 2):
            continue
        for x in range(7):
            m = np.ones(7, bool)
            m[x] = False
            c2, ok2, _, _ = implication_classes(R[np.ix_(m, m)])
            if ok2 and len(c2) > 2:
                found = True
                break
        if found:
            break
    assert found
