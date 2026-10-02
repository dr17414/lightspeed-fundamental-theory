"""Deterministic harness checks; no cap-length benchmark, RNG, or screen."""

from types import SimpleNamespace

import numpy as np
import pytest

from benchmarks import stage5c_e4_v02_resource_characterization as harness
from analysis import stage5c_e4_wellposedness_v02 as v02
from analysis.stage5c_hard_controls import BlindedCase, order_from_uv
from analysis.stage5c_selector_family import apply_selector


def test_missing_thread_pin_is_rejected_before_probe(monkeypatch):
    for name in harness.THREAD_ENV:
        monkeypatch.setenv(name, "1")
    harness.check_thread_environment()
    monkeypatch.delenv("OPENBLAS_NUM_THREADS")
    with pytest.raises(RuntimeError, match="OPENBLAS_NUM_THREADS"):
        harness.check_thread_environment()


@pytest.mark.parametrize("n", harness.N_VALUES)
def test_registered_selectors_have_reachable_large_count_witnesses(n):
    fixtures = harness.geometry_fixtures(n)
    def count(fixture, selector, parameters=()):
        case = BlindedCase("DEVELOPMENT-ONLY", order_from_uv(fixtures[fixture]))
        return len(apply_selector(selector, parameters, case))
    assert count("chain", "all_relations") == n * (n - 1) // 2
    assert count("two_layers", "links") == n * n // 4
    # A complete tie block enters just one midquantile band: selected count
    # is not bounded by one fifth of the total pair count.
    assert count("two_layers", "endpoint_depth_mass_band", (.4, .6)) == n * n // 4
    for middle in range(1, 5):
        assert count(f"interval_bridge_{middle}", "interval_exact", (middle,)) == (n - middle)**2 // 4


def test_stress_primitive_is_bitwise_equal_to_production_integrand(monkeypatch):
    captured = []
    def capture(function, *args, **kwargs):
        captured.append(function)
        return SimpleNamespace(estimate=np.zeros(4), error=np.zeros(4),
                               subdivisions=0, status="converged")
    monkeypatch.setattr(v02.integrate, "cubature", capture)
    atoms = np.array([[.72, .81, .31, .22], [.61, .58, .24, .19], [.43, .67, .11, .37]])
    weights = np.array([.2, .5, .3])
    v02._cubature_pairing(atoms, weights, .4, "genz-malik", atol=2.0**-40)
    points = np.array([[.1, .2, .3], [.9, .8, .7], [.5, .5, .5],
                       [0., .3, 1.], [1., 0., .4], [.8, 1., 0.]])
    assert np.array_equal(captured[0](points), harness.stress_integrand(atoms, weights, .4)(points))


def test_selector_count_inventory_is_fixture_only_and_includes_empty_strata():
    rows = harness.selector_counts()
    assert len(rows) == 3 * 12 * 11
    assert {row["category"] for row in rows} == {"SELECTED", "DOMAIN-EMPTY", "SELECTION-EMPTY"}
    assert all(0 <= row["selected_pairs"] <= row["N"] * (row["N"] - 1) // 2 for row in rows)
    for n in harness.N_VALUES:
        for fixture in harness.geometry_fixtures(n):
            group = [r for r in rows if r["N"] == n and r["fixture"] == fixture]
            relation_count = next(r["selected_pairs"] for r in group if r["selector"] == "all_relations")
            bands = sum(r["selected_pairs"] for r in group if r["selector"] == "endpoint_depth_mass_band")
            low_cardinality = sum(r["selected_pairs"] for r in group
                                  if r["selector"] in ("links", "interval_exact"))
            assert bands == relation_count
            assert sum(r["selected_pairs"] for r in group) == 2 * relation_count + low_cardinality
            assert low_cardinality <= relation_count
