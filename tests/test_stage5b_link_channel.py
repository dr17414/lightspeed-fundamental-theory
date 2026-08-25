"""Regression tests for Stage 5B-2 limited Result B.

These tests pin three independent claims:
  * the rank diagnostic must be three-valued to respect the global U<->V swap;
  * independent monotone null-coordinate reparameterisations preserve the order
    and the rank diagnostic while a metric comparison can change;
  * remote population outside an empty link interval can flip the rank channel
    while preserving every pre-existing order relation and preserving the link.

None of these tests claims that all possible local two-state structures are
forbidden.  The scope is the metric link-channel target and this rank-based chi.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.stage5b_link_channel import (  # noqa: E402
    BOTTOM,
    benchmark,
    flip_by_remote_population,
    link_matrix,
    metric_channel,
    order_from_uv,
    rank_array,
    rank_channel,
    sprinkle_2d_with_coords,
)


def test_tie_is_bottom_and_sector_swap_is_covariant():
    rU = np.array([0, 1, 2, 3])
    rV = np.array([0, 1, 3, 2])
    assert rank_channel(rU, rV, 0, 1) == BOTTOM

    # For non-ties, swapping the two global orders swaps the channel name.
    assert rank_channel(rU, rV, 0, 2) == "V"
    assert rank_channel(rV, rU, 0, 2) == "U"


def test_monotone_reparameterisation_preserves_order_and_rank_channel():
    rng = np.random.default_rng(55002)
    u, v, R = sprinkle_2d_with_coords(300, rng)
    L = link_matrix(R)
    rU, rV = rank_array(u), rank_array(v)

    uf = u ** 3
    vg = v ** 0.25
    assert np.array_equal(order_from_uv(uf, vg), R)
    assert np.array_equal(rank_array(uf), rU)
    assert np.array_equal(rank_array(vg), rV)

    # The pure rank observable is unchanged on every link.
    for x, y in zip(*np.nonzero(L)):
        assert rank_channel(rU, rV, x, y) == rank_channel(
            rank_array(uf), rank_array(vg), x, y
        )

    # But the coordinate metric diagnostic changes for a nonzero set of links.
    flips = 0
    for x, y in zip(*np.nonzero(L)):
        flips += metric_channel(u, v, x, y) != metric_channel(uf, vg, x, y)
    assert flips > 0


def test_remote_population_can_flip_rank_channel_without_breaking_link():
    rng = np.random.default_rng(7)
    u, v, R = sprinkle_2d_with_coords(120, rng)
    L = link_matrix(R)
    rU, rV = rank_array(u), rank_array(v)

    # Pick the smallest nonzero rank-margin link for a compact witness.
    cand = []
    for x, y in zip(*np.nonzero(L)):
        ch = rank_channel(rU, rV, x, y)
        if ch != BOTTOM:
            margin = abs((rU[y] - rU[x]) - (rV[y] - rV[x]))
            cand.append((margin, x, y))
    _, x, y = min(cand)

    _, _, res = flip_by_remote_population(u, v, x, y)
    assert res.old_channel in ("U", "V")
    assert res.new_channel in ("U", "V")
    assert res.old_channel != res.new_channel
    assert res.old_relation_preserved
    assert res.link_preserved
    assert res.all_added_outside_interval


def test_source_of_record_benchmark_is_pinned():
    b = benchmark(seed=55002, N=300, interventions=60)
    assert b["links"] == 1328
    assert b["ties"] == 16
    assert b["intervention_flips"] == 60
    assert b["interventions"] == 60
    assert b["median_added"] == 3.0
    assert b["all_old_relations_preserved"]
    assert b["all_links_preserved"]
    assert b["all_added_outside_interval"]
    assert b["conformal_metric_flips"] == 150
    assert b["conformal_metric_comparable"] == 1328


def test_rank_diagnostic_is_correlated_but_not_identical_to_metric_target():
    b = benchmark(seed=55002, N=300, interventions=60)
    assert 0.95 < b["non_tie_agreement"] < 0.99
    assert 0.005 < b["tie_fraction"] < 0.03
