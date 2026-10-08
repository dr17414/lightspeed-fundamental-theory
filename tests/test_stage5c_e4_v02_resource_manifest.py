"""Method/input/gate regressions only; never execute a new timed probe."""
import copy
import json
from hashlib import sha256
import numpy as np
import pytest
from benchmarks import stage5c_e4_v02_resource_methods as methods
from benchmarks import stage5c_e4_v02_resource_campaign as campaign


def test_all_frozen_source_and_input_byte_pins_match():
    manifest = json.loads(campaign.MANIFEST.read_text())
    for path, expected in manifest["input_sha256"].items():
        assert sha256((campaign.ROOT / path).read_bytes()).hexdigest() == expected, path


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


def test_training_coefficients_preclude_unanimous_pass_before_measurement():
    reference = json.loads(campaign.REFERENCE.read_text())
    assert all(not methods.model_agreement_possible(reference, clock, 8128, s)
               for clock in ("cpu_seconds", "wall_seconds") for s in (4096, 128, 1024))


def test_censored_phase_lower_bound_reaches_model_invalid_path():
    manifest = json.loads(campaign.MANIFEST.read_text())
    reference = json.loads(campaign.REFERENCE.read_text())
    maximum = max(methods.predict_stress(reference, clock, k.split(':', 1)[1], 8128, 4096)
                  for clock in ('cpu_seconds', 'wall_seconds') for k in reference['fits']
                  if k.startswith(clock+':stress_'))
    record = dict(job_id='direct-8128-4096', outcome='WALL-CAP-CENSORED',
                  phase_cpu_lower_bound_seconds=2*maximum, phase_wall_lower_bound_seconds=2*maximum)
    result = methods.assess_held_out(manifest, reference, [record])
    assert all(model['rows'][0]['verdict'] == 'MODEL-INVALID' for model in result['models'].values())
    assert result['model_set_verdict'] == 'INSUFFICIENT-EVIDENCE'
    assert result['primary_model'] == 'stress_affine'
    record.pop('phase_cpu_lower_bound_seconds'); record.pop('phase_wall_lower_bound_seconds')
    result = methods.assess_held_out(manifest, reference, [record])
    assert all(model['rows'][0]['verdict'] == 'INSUFFICIENT-EVIDENCE' for model in result['models'].values())


def test_production_phase_scope_and_setup_allowance_are_frozen():
    manifest = json.loads(campaign.MANIFEST.read_text())
    production = [j for j in manifest['jobs'] if j['kind'] == 'production']
    assert all(j['e4_wall_cap'] == 900 and j['setup_allowance'] == 120 and j['wall_cap'] == 1020 and j['cpu_cap'] == 1100
               for j in production)
    assert manifest['poll_cadence_seconds'] == .5
    assert manifest['supervisor_cpu_soft_cap'] == 600
    assert manifest['supervisor_cpu_inherited_hard_cap'] == max(j['cpu_cap']+1 for j in manifest['jobs'])


def test_no_receipt_blocks_before_resource_mutation_or_producer(monkeypatch, tmp_path):
    def forbidden(*args, **kwargs):
        raise AssertionError("execution must not pass the review gate")
    monkeypatch.setattr(campaign.resource, "setrlimit", forbidden)
    monkeypatch.setattr(campaign, "worker", forbidden)
    with pytest.raises(campaign.ResourceNotAuthorized, match="receipt required"):
        campaign.run_campaign(None, tmp_path / "uncreated")
    assert not (tmp_path / "uncreated").exists()


def test_memory_preflight_abort_retains_all_unstarted_jobs(monkeypatch, tmp_path):
    # Simulate supervisor preflight only; no receipt, resource change or child probe is created.
    output = tmp_path / "simulated-records"
    monkeypatch.setattr(campaign, "check_receipt", lambda *a: {"reviewed_commit": "test-only"})
    monkeypatch.setattr(campaign.resource, "setrlimit", lambda *a: None)
    monkeypatch.setattr(campaign, "check_runtime", lambda *a: None)
    monkeypatch.setattr(campaign, "check_numerical_runtime_in_subprocess", lambda *a, **k: None)
    original_read = campaign.Path.read_text
    monkeypatch.setattr(campaign.Path, "read_text", lambda p, *a, **k:
                        '{}' if str(p) == "test-only-receipt" else original_read(p, *a, **k))
    memory_calls = iter([{"host_available_bytes": 4*1024**3, "cgroup_remaining_bytes": 4*1024**3}, None])
    def memory():
        result = next(memory_calls)
        if result is None:
            raise RuntimeError("insufficient simulated headroom")
        return result
    monkeypatch.setattr(campaign, "memory_preflight", memory)
    def forbidden(*a, **k):
        raise AssertionError("no probe may start after failed preflight")
    monkeypatch.setattr(campaign.subprocess, "Popen", forbidden)
    campaign.run_campaign("test-only-receipt", output)
    records = [json.loads(line) for line in (output / "records.jsonl").read_text().splitlines()]
    abort = next(r for r in records if r.get("outcome") == "MEMORY-PREFLIGHT-ABORT")
    manifest = json.loads(campaign.MANIFEST.read_text())
    assert abort["not_run_ids"] == [j["id"] for j in manifest["jobs"]]
    assert records[-1]["outcome"] == "MEMORY-PREFLIGHT-ABORT"
