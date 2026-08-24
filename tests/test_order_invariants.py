"""
test_order_invariants.py
========================
Unit tests for causal-set order invariants.
Verifies transitivity, irreflexivity, antisymmetry, and generator sanity checks
across the entire FAMILY of posets in order_bench.py.
"""
import sys
import os
import numpy as np

# Ensure benchmarks folder is in python module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../benchmarks')))

from order_bench import FAMILY

def test_poset_invariants():
    """Verify transitivity, irreflexivity, and antisymmetry for all generators in FAMILY."""
    n = 200  # use a moderate size for fast and reliable test runs
    for name, gen in FAMILY.items():
        o = gen(n, seed=42) if name != "lattice_1p1" else gen(n)
        
        # T1: Irreflexivity: no element is related to itself (diagonal must be all False)
        refl = int(np.diag(o).sum())
        assert refl == 0, f"{name} violates irreflexivity: self-related elements found"
        
        # T2: Antisymmetry: if i < j, then not (j < i) (symmetric pairs must be all False)
        anti = int((o & o.T).sum())
        assert anti == 0, f"{name} violates antisymmetry: cycle of length 2 found"
        
        # T3: Transitivity: if i < j and j < k, then i < k
        # Computed using np.int32 multiplication to prevent path count overflow (int8 overflow).
        A = o.astype(np.int32)
        bad = int(((A @ A > 0) & ~o).sum())
        assert bad == 0, f"{name} violates transitivity: related pairs (i<j, j<k) exist without i<k"

def test_lattice_exact_size():
    """Verify that lattice_1p1(N) does not silently produce a different number of events than N."""
    for n in [10, 50, 100, 144, 200]:
        o = FAMILY["lattice_1p1"](n)
        assert o.shape == (n, n), (
            f"lattice_1p1({n}) returned shape {o.shape}, expected {(n, n)}. "
            f"If the grid size does not permit exactly N elements, it must not silently mismatch."
        )
