"""Preserve the submitted assessment and its frozen-policy provenance."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from benchmarks.stage5c_e4_v02_resource_methods import assess_held_out

DOCS = Path(__file__).resolve().parents[1] / "docs"


def read(name):
    return json.loads((DOCS / name).read_text())


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
    assert assess_held_out(manifest, reference, results["assessment_projection"]) == json.loads(raw)


def test_139_job_ledger_preserves_order_and_does_not_invent_missing_outcomes():
    results = read("stage5c_e4_v02_resource_run1_results.json")
    manifest = read("stage5c_e4_v02_resource_measurement_manifest.json")
    ledger = results["job_outcome_ledger"]
    assert len(ledger) == 139
    assert [r["job"] for r in ledger] == manifest["jobs"]
    assert [r["manifest_index_1_based"] for r in ledger] == list(range(1, 140))
    assert len({r["job_id"] for r in ledger}) == 139
    assert Counter(r["source"] for r in ledger) == {
        "ASSESSMENT-PROJECTION-NOT-RAW-RECORD": 37,
        "REVIEWER-SUMMARY-NOT-RAW-RECORD": 78,
        "OUTCOME-NOT-PROVIDED": 24,
    }
    for row in ledger:
        if row["source"] == "OUTCOME-NOT-PROVIDED":
            assert row["outcome"] is None and row["status"] is None
        if row["source"] == "REVIEWER-SUMMARY-NOT-RAW-RECORD":
            assert row["job"]["kind"] == "production"
            assert row["phase_cpu_seconds"] is None and row["phase_wall_seconds"] is None
    assert results["raw_archive_sha256"] is None
    assert results["raw_archive_available_to_pr_author"] is False
    assert results["raw_archive_preservation_verified"] is False
    assert results["receipt_verified"] is False
    assert results["execution_commit_verified"] is False
    assert results["qualification"] is False
    assert results["item7_adopt"] is False
