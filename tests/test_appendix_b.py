"""
test_appendix_b.py
===================
Regression test for 零時光網／因果相位網 研究進度與AI交接文件 v1.0, Appendix B.

Purpose
-------
1. Confirms (empirically, on random finite causal sets) that the naive
   retarded operator
       (D_C psi)_i = sum_{j prec i} f(|I(j,i)|) U_ij psi_j
   is always strictly lower-triangular under any linear extension, hence
   nilpotent, hence det(D_C - mI) = (-m)^(rN) FOR ANY causal structure --
   the determinant cannot see the causal relations at all. This is the
   "已否定" result in Sec. 8 / Appendix B: det(D_C - m) cannot be used to
   select geometry.

2. Confirms that the Sec. 9.2 diagnostic fix -- combining R_C with its
   adjoint into a block operator -- genuinely escapes this degeneracy:
   chain vs. antichain (the two most extreme causal structures on the
   same number of events) give very different determinants once the
   adjoint block is included.

Run with: python3 test_appendix_b.py
(or drop into a tests/ folder and run with pytest -- the assert
statements at the bottom already work as pytest test functions if you
rename them test_*() and remove the __main__ guard.)
"""

import numpy as np


def random_causal_set(n, p=0.4, seed=None):
    """order[i, j] == True means event i precedes event j.
    Relations are only ever set for i < j, so the natural index order
    is automatically a valid linear extension -- this mirrors the
    document's own construction exactly."""
    rng = np.random.default_rng(seed)
    order = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p:
                order[i, j] = True
    changed = True
    while changed:  # transitive closure
        changed = False
        for i in range(n):
            for j in range(n):
                if order[i, j]:
                    for k in range(n):
                        if order[j, k] and not order[i, k]:
                            order[i, k] = True
                            changed = True
    return order


def interval_size(order, i, j):
    n = order.shape[0]
    return sum(1 for k in range(n) if order[i, k] and order[k, j])


def build_DC(order, r=2, seed=None):
    """(D psi)_i = sum_{j prec i} f(|I(j,i)|) U_ij psi_j, with an
    arbitrary nontrivial f and arbitrary complex U_ij -- exactly the
    original Sec. 8.1 proposal, kept as general as possible on purpose."""
    n = order.shape[0]
    rng = np.random.default_rng(seed)
    N = n * r
    D = np.zeros((N, N), dtype=complex)
    for i in range(n):
        for j in range(n):
            if order[j, i]:
                s = interval_size(order, j, i)
                f = 1.0 + s + 0.3 * s ** 2
                Uij = rng.normal(size=(r, r)) + 1j * rng.normal(size=(r, r))
                D[i * r:(i + 1) * r, j * r:(j + 1) * r] = f * Uij
    return D


def build_Qtest(order, r, m, seed):
    """Sec. 9.2's diagnostic: Q = [[mI, R_C], [R_C^dagger, -mI]]."""
    Rc = build_DC(order, r=r, seed=seed)
    N = Rc.shape[0]
    top = np.hstack([m * np.eye(N), Rc])
    bot = np.hstack([Rc.conj().T, -m * np.eye(N)])
    return np.vstack([top, bot])


def test_appendix_b_degeneracy():
    """det(D_C - mI) must equal (-m)^(rN) for EVERY random causal set."""
    for trial in range(8):
        n, r, m = 7, 2, 0.6 + 0.1 * trial
        order = random_causal_set(n, p=0.45, seed=trial)
        D = build_DC(order, r=r, seed=trial + 500)
        N = n * r
        det_actual = np.linalg.det(D - m * np.eye(N))
        det_predicted = (-m) ** N
        assert np.isclose(det_actual, det_predicted, rtol=1e-6, atol=1e-6), (
            f"trial {trial}: got {det_actual}, expected {det_predicted} -- "
            "if this fails, the triangularity argument itself is broken "
            "and Appendix B needs to be revisited, not celebrated."
        )


def test_chain_equals_antichain():
    """The two most extreme causal structures must be indistinguishable
    to det(D_C - mI) -- this is the sharpest illustration of Sec. 8's
    point: the determinant reads only the diagonal, i.e. only N and m."""
    n, r, m = 6, 1, 0.5
    chain = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for j in range(i + 1, n):
            chain[i, j] = True
    antichain = np.zeros((n, n), dtype=bool)
    D_chain = build_DC(chain, r=r, seed=1)
    D_anti = build_DC(antichain, r=r, seed=1)
    det_chain = np.linalg.det(D_chain - m * np.eye(n * r))
    det_anti = np.linalg.det(D_anti - m * np.eye(n * r))
    assert np.isclose(det_chain, det_anti)
    assert np.isclose(det_chain, (-m) ** (n * r))
    return det_chain, det_anti


def test_section_9_2_fix_is_structure_sensitive():
    """Once R_C is combined with its adjoint, chain and antichain must
    stop being degenerate -- confirming Sec. 9.2 is a genuine escape
    route, not just a hopeful guess."""
    n, r, m = 6, 1, 0.5
    chain = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for j in range(i + 1, n):
            chain[i, j] = True
    antichain = np.zeros((n, n), dtype=bool)
    det_chain = np.linalg.det(build_Qtest(chain, r, m, seed=1))
    det_anti = np.linalg.det(build_Qtest(antichain, r, m, seed=1))
    assert not np.isclose(det_chain, det_anti), (
        "if this ever fails, the Sec. 9.2 fix has stopped being "
        "structure-sensitive and needs to be re-derived before any "
        "further work builds on it."
    )
    return det_chain, det_anti


if __name__ == "__main__":
    test_appendix_b_degeneracy()
    print("[PASS] det(D_C - mI) = (-m)^(rN) for all random causal sets tested.")

    dc, da = test_chain_equals_antichain()
    print(f"[PASS] chain det = {dc:.6g}   antichain det = {da:.6g}   (identical, as predicted)")

    qc, qa = test_section_9_2_fix_is_structure_sensitive()
    print(f"[PASS] Sec 9.2 fix: chain det = {qc:.6g}   antichain det = {qa:.6g}   (now DIFFERENT)")

    print("\nAll Appendix B / Sec 9.2 claims in the handoff document check out numerically.")
