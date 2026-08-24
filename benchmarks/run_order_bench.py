"""
run_order_bench.py
==================
Runs the order-only benchmarks, computing:
  (1) S_m - interval abundance (for m = 2 .. 8, inclusive cardinality)
  (2) d_MM(N_I) - scale-resolved Myrheim-Meyer profile
across the family of posets in order_bench.py.
"""
import numpy as np
from order_bench import FAMILY, abundance, mm_profile

def run_benchmarks():
    print("=" * 80)
    print(" Causal Set Order-Only Benchmarks")
    print("=" * 80)
    print(f"{'Poset Family':18} | {'Abundance S_m (m = 2 .. 8)':36} | {'MM Profile (bin: d_MM)':22}")
    print("-" * 80)
    
    n = 200  # number of events
    
    for name, gen in FAMILY.items():
        # Generate poset
        o = gen(n, seed=42) if name != "lattice_1p1" else gen(n)
        
        # Calculate interval abundance S_m
        s_m = abundance(o)
        s_m_str = "[" + ", ".join(f"{x:.2f}" if np.isfinite(x) else "NaN" for x in s_m) + "]"
        
        # Calculate scale-resolved MM profile
        profile = mm_profile(o, nsample=2000, seed=42)
        if profile:
            profile_str = ", ".join(f"{k}: {val[1]:.2f}" for k, val in profile.items())
        else:
            profile_str = "None"
            
        print(f"{name:18} | {s_m_str:36} | {profile_str:22}")
        
if __name__ == "__main__":
    run_benchmarks()
