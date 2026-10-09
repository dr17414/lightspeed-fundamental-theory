"""Preserve the submitted assessment and its frozen-policy provenance."""
from collections import Counter
from copy import deepcopy
from hashlib import sha256
import json
import math
from pathlib import Path

import pytest

from benchmarks.stage5c_e4_v02_resource_methods import assess_held_out

DOCS = Path(__file__).resolve().parents[1] / "docs"


def read(name):
    return json.loads((DOCS / name).read_text())


def assert_assessment_replay_matches(actual, expected):
    # Some CI power predictions differ by one ULP across runtimes. Preserve every
    # measured value/verdict exactly; this is not a scientific residual tolerance.
    assert {k: v for k, v in actual.items() if k != "models"} == {
        k: v for k, v in expected.items() if k != "models"
    }
    assert actual["models"].keys() == expected["models"].keys()
    for name, model in expected["models"].items():
        replay = actual["models"][name]
        assert replay.keys() == model.keys()
        assert replay["verdict"] == model["verdict"]
        assert len(replay["rows"]) == len(model["rows"])
        for row, original in zip(replay["rows"], model["rows"], strict=True):
            assert row.keys() == original.keys()
            assert {k: v for k, v in row.items() if k != "prediction"} == {
                k: v for k, v in original.items() if k != "prediction"
            }
            prediction, frozen_prediction = row["prediction"], original["prediction"]
            assert math.isfinite(prediction) and math.isfinite(frozen_prediction)
            if ":stress_power_" in name:
                assert abs(prediction - frozen_prediction) <= math.ulp(frozen_prediction)
            else:
                assert prediction == frozen_prediction


def test_submitted_assessment_is_preserved_and_matches_frozen_policy():
    raw = (DOCS / "stage5c_e4_v02_resource_run1_assessment.json").read_bytes()
    results = read("stage5c_e4_v02_resource_run1_results.json")
    manifest = read("stage5c_e4_v02_resource_measurement_manifest.json")
    reference = read("stage5c_e4_v02_resource_method_reference.json")
    assert len(raw) == 290261
    assert sha256(raw).hexdigest() == results["assessment_sha256"] == (
        "7dd51e7e54f1306a1f2a439f8440caf3e220ce216a33ca4c2d9f20aee5ad2326"
    )
    assert sha256((DOCS / "stage5c_e4_v02_resource_measurement_manifest.json").read_bytes()).hexdigest() == results["manifest_sha256"]
    assert_assessment_replay_matches(
        assess_held_out(manifest, reference, results["assessment_projection"]), json.loads(raw)
    )
    evidence_raw = (DOCS / results["raw_evidence_artifact"]).read_bytes()
    assert sha256(evidence_raw).hexdigest() == results["raw_evidence_artifact_sha256"]
    evidence = json.loads(evidence_raw)
    assert_assessment_replay_matches(
        assess_held_out(manifest, reference, evidence["job_records"]), json.loads(raw)
    )


@pytest.mark.parametrize("change", ["power_one_ulp", "power_two_ulps", "observed", "verdict", "affine"])
def test_replay_comparison_only_allows_one_ulp_in_power_predictions(change):
    original = read("stage5c_e4_v02_resource_run1_assessment.json")
    changed = deepcopy(original)
    model = "cpu_seconds:stress_affine" if change == "affine" else "cpu_seconds:stress_power_p0.9_q0.9"
    row = changed["models"][model]["rows"][0]
    if change == "verdict":
        row["verdict"] = ("MODEL-INVALID" if row["verdict"] == "POINTWISE-MODEL-CHECK-PASS"
                          else "POINTWISE-MODEL-CHECK-PASS")
    else:
        field = "observed" if change == "observed" else "prediction"
        row[field] = math.nextafter(row[field], math.inf)
        if change == "power_two_ulps":
            row[field] = math.nextafter(row[field], math.inf)
    if change == "power_one_ulp":
        assert_assessment_replay_matches(changed, original)
    else:
        with pytest.raises(AssertionError):
            assert_assessment_replay_matches(changed, original)


def test_139_job_ledger_matches_archived_start_result_pairs():
    results = read("stage5c_e4_v02_resource_run1_results.json")
    manifest = read("stage5c_e4_v02_resource_measurement_manifest.json")
    ledger = results["job_outcome_ledger"]
    assert len(ledger) == 139
    assert [r["job"] for r in ledger] == manifest["jobs"]
    assert [r["manifest_index_1_based"] for r in ledger] == list(range(1, 140))
    assert len({r["job_id"] for r in ledger}) == 139
    evidence = read(results["raw_evidence_artifact"])
    records = evidence["job_records"]
    assert len(records) == 278
    assert Counter(r["source"] for r in ledger) == {"ARCHIVE-RAW-JOB-RECORD": 139}
    assert Counter(r["outcome"] for r in ledger) == {
        "PRODUCTION-REPORT": 78, "FORCED-BUDGET-EXHAUSTED": 61,
    }
    for index, row in enumerate(ledger):
        start, result = records[2*index:2*index+2]
        assert start["job_id"] == result["job_id"] == row["job_id"]
        assert start["outcome"] == "ATTEMPT-STARTED"
        assert row["outcome"] == result["outcome"]
        assert row["status"] == result.get("status")
        assert row["phase_cpu_seconds"] == result["phase_cpu_seconds"]
        assert row["phase_wall_seconds"] == result["phase_wall_seconds"]
        assert row["child_total_cpu_seconds"] == result["child_total_cpu_seconds"]
        assert row["child_total_wall_seconds"] == result["child_total_wall_seconds"]
        assert row["start_line_1_based"] == 2*index+2
        assert row["result_line_1_based"] == 2*index+3
        if row["job"]["kind"] == "production":
            assert row["status"] == "CLEAN"
            assert row["phase_wall_seconds"] < row["job"]["e4_wall_cap"]
    assert results["raw_archive_sha256"] == evidence["raw_archive_sha256"] == (
        "8c26b6574ce12956474779434f24ad54e940584dbf3ecc43c9c582fd792b06bf"
    )
    assert results["raw_archive_available_to_pr_author"] is True
    assert results["receipt_verified"] is True
    assert results["execution_commit_verified"] is True
    assert results["receipt_consumed"] is True
    assert results["qualification"] is False
    assert results["item7_adopt"] is False


def test_resource_accounting_is_reproducible_from_all_archived_job_records():
    results = read("stage5c_e4_v02_resource_run1_results.json")
    evidence = read(results["raw_evidence_artifact"])
    rows = evidence["job_records"][1::2]
    terminal = evidence["terminal_summary"]
    audit = results["execution_audit"]
    assert terminal == audit["terminal_summary"]
    assert terminal["outcome"] == "PLAN-COMPLETE"
    cpu_sum = sum(r["child_total_cpu_seconds"] for r in rows)
    assert cpu_sum == audit["summed_job_child_cpu_seconds"]
    assert terminal["children_cpu_seconds"] - cpu_sum == audit["preflight_child_cpu_residual_seconds"]
    assert terminal["total_accounted_cpu_seconds"] == terminal["children_cpu_seconds"] + terminal["parent_cpu_seconds"]
    assert max(r["child_peak_rss_bytes"] for r in rows) == audit["peak_child_rss_bytes"]
    assert max(r["sum_of_parent_child_peaks_bytes"] for r in rows) == audit["max_sum_of_parent_child_peaks_bytes"]
    assert len(evidence["member_inventory"]) == 283
    assert len(evidence["record_line_sha256_including_newline"]) == evidence["raw_record_count"] == 280
    assert evidence["container_final_state"]["ExitCode"] == 0
    assert evidence["container_final_state"]["OOMKilled"] is False
    assert evidence["restart_count"] == 0
    assert evidence["header_without_receipt"]["method_verified"] is True
    assert evidence["stderr_event_counts"] == {"WORKER-READY": 139, "PHASE-STARTED": 139, "PHASE-FINISHED": 139}
    assert evidence["receipt_and_launch_identity"]["pf3_separate_archive_available"] is False
