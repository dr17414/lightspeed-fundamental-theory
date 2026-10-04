"""Method/input/gate regressions only; never execute a new timed probe."""
import copy
import json
import numpy as np
import pytest
from benchmarks import stage5c_e4_v02_resource_methods as methods
from benchmarks import stage5c_e4_v02_resource_campaign as campaign


def test_nnls_known_boundary_solution_and_rank_failure():
    result = methods.fit_nnls([[1, 0], [1, 0], [0, 1]], [2, 1, -1])
    assert np.allclose([float.fromhex(x) for x in result["coefficients_hex"]], [1.5, 0])
    assert result["active_positive"] == [True, False]
    with pytest.raises(ValueError, match="NOT-IDENTIFIED"):
        methods.fit_nnls([[1, 1], [2, 2]], [1, 2])


def test_pinned_training_method_reference_and_active_set_drift():
    reference = json.loads(campaign.REFERENCE.read_text())
    actual = methods.method_reference()
    methods.verify_reference(actual, reference)
    assert len(actual["fits"]) == 44
    assert actual["fits"]["cpu_seconds:stress_affine"]["rank"] == 4
    assert actual["fits"]["cpu_seconds:stress_affine"]["residual_df"] == 3
    changed = copy.deepcopy(reference)
    changed["fits"]["cpu_seconds:stress_affine"]["active_positive"][0] ^= True
    with pytest.raises(ValueError, match="active-set"):
        methods.verify_reference(actual, changed)


def test_exact_fixture_regeneration_and_real_adapter_bytes():
    fixtures = json.loads(campaign.FIXTURES.read_text())
    assert methods.build_fixtures() == fixtures
    assert len(fixtures["coordinates"]) == 36
    assert len(fixtures["cases"]) == 39
    for i, case in enumerate(fixtures["cases"]):
        atoms, weights = methods.load_case(fixtures, i)
        assert len(atoms) == case["selected_count"] == len(weights)
    for n in (64, 96, 128):
        case = next(c for c in fixtures["cases"] if c["N"] == n and c["selector"] == "all_relations"
                    and "max_count_per_member" in c["selection_reasons"])
        assert case["fixture"] == "chain" and case["selected_count"] == n*(n-1)//2


def test_coordinate_mutation_is_detected_before_producer():
    fixtures = json.loads(campaign.FIXTURES.read_text())
    fixtures["coordinates"][fixtures["cases"][0]["coordinate_key"]]["sha256"] = "0"*64
    with pytest.raises(ValueError, match="coordinate bytes"):
        methods.load_case(fixtures, 0)


def test_residual_boundary_is_fixed_and_censoring_never_passes():
    assert methods.residual_verdict(100, 90) == "POINTWISE-MODEL-CHECK-PASS"
    assert methods.residual_verdict(100, 110) == "POINTWISE-MODEL-CHECK-PASS"
    assert methods.residual_verdict(100, 89.99) == "MODEL-INVALID"
    assert methods.residual_verdict(100, 110.01) == "MODEL-INVALID"
    assert methods.residual_verdict(100, 95, censored=True) == "INSUFFICIENT-EVIDENCE"
    assert methods.residual_verdict(100, 80, censored=True) == "MODEL-INVALID"


def test_plan_order_roles_and_total_caps_are_frozen():
    manifest = json.loads(campaign.MANIFEST.read_text())
    fixtures = json.loads(campaign.FIXTURES.read_text())
    assert methods.build_plan(fixtures) == manifest["jobs"]
    assert len(manifest["jobs"]) == 139
    assert manifest["jobs"][0]["id"] == "direct-8128-4096"
    assert sum(j["kind"] == "production" for j in manifest["jobs"]) == 78
    assert manifest["total_cpu_cap"] == 57600
    assert manifest["total_wall_cap"] == 60000
    assert manifest["authorization"] == "NONE"


def test_missing_held_out_rows_are_retained_as_insufficient():
    manifest = json.loads(campaign.MANIFEST.read_text())
    reference = json.loads(campaign.REFERENCE.read_text())
    result = methods.assess_held_out(manifest, reference, [])
    assert len(result["models"]) == 34
    assert result["model_set_verdict"] == "INSUFFICIENT-EVIDENCE"
    assert all(len(m["rows"]) == 37 for m in result["models"].values())
    assert all(r["outcome"] == "NOT-RUN" for m in result["models"].values() for r in m["rows"])


def test_no_receipt_blocks_before_resource_mutation_or_producer(monkeypatch, tmp_path):
    def forbidden(*args, **kwargs):
        raise AssertionError("execution must not pass the review gate")
    monkeypatch.setattr(campaign.resource, "setrlimit", forbidden)
    monkeypatch.setattr(campaign, "worker", forbidden)
    with pytest.raises(campaign.ResourceNotAuthorized, match="receipt required"):
        campaign.run_campaign(None, tmp_path / "uncreated")
    assert not (tmp_path / "uncreated").exists()
