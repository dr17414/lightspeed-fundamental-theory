"""Regression locks for the non-executable item-7 v0.2 proposal."""

from fractions import Fraction
import json
from pathlib import Path

import numpy as np

import analysis.stage5c_e4_wellposedness as e4
from analysis.stage5c_e4_wellposedness import E4Status, evaluate_e4_wellposedness
from analysis.stage5c_statistical_regions import ENDPOINT_RANGE_WIDTHS


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "docs" / "stage5c_e4_item7_amendment_candidate_v0.2.json"


def _round_toward_zero(value: Fraction) -> float:
    rounded = float(value)
    if Fraction.from_float(rounded) > value:
        rounded = float(np.nextafter(rounded, 0.0))
    return rounded


def _candidate_report(atom: list[float], monkeypatch):
    atoms = np.asarray([atom], dtype=float)
    weights = np.ones(1)
    monkeypatch.setattr(e4, "E4_ENCLOSURE_LEVELS", (64, 128, 256))
    enclosure = e4.pairing_enclosure(atoms, weights, theta=0.4)
    scale = max(Fraction.from_float(float(value)) for value in enclosure.upper)
    effective = min(Fraction(1, 2**30), scale / 2**14)
    atol = _round_toward_zero(effective)
    assert atol > 0.0
    monkeypatch.setattr(e4, "E4_CUBATURE_ATOL", atol)
    return evaluate_e4_wellposedness(atoms, weights, theta=0.4)


def test_proposal_is_non_executable_and_does_not_mutate_frozen_v01():
    payload = json.loads(CANDIDATE.read_text(encoding="utf-8"))
    assert payload["state"] == "AMENDMENT-REVIEW-PENDING"
    assert payload["executable"] is False
    assert payload["authorization"] == "NONE"
    assert payload["candidate_identities"] == {
        "contract": "stage5c-6a-e-e4-wellposedness-v0.2",
        "gauss_implementation": "gauss-legendre-32-with-cell-enclosure-v0.2",
        "adaptive_implementation": (
            "adaptive-genz-malik-scale-aware-with-cell-enclosure-v0.2"
        ),
        "enclosure": "positive-gaussian-characteristic-cell-enclosure-v0.2",
    }
    assert payload["candidate_constants"] == {
        "cubature_rtol_numerator": 1,
        "cubature_rtol_denominator": 16384,
        "cubature_atol_cap_numerator": 1,
        "cubature_atol_cap_denominator": 1073741824,
        "enclosure_levels": [64, 128, 256],
        "max_subdivisions": 4096,
        "max_atoms": 8128,
        "density_chunk_size": 128,
    }
    assert payload["effective_atol_policy"]["zero_nonfinite_or_underflow"] == (
        "INCONCLUSIVE_BEFORE_ADAPTIVE"
    )
    assert payload["retained_execution_caps"] == {
        "per_e4_wall_seconds": 900,
        "total_cpu_seconds": 57600,
        "address_space_bytes": 34359738368,
    }

    assert e4.E4_CONTRACT_ID == "stage5c-6a-e-e4-wellposedness-v0.1"
    assert e4.E4_CUBATURE_ATOL == 2.0**-30
    assert e4.E4_ENCLOSURE_LEVELS == (16, 32, 64)


def test_non_executable_candidate_is_not_imported_by_production_analysis():
    for path in (ROOT / "analysis").glob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert CANDIDATE.name not in source
        assert "STAGE5C_6A_E_ITEM7_AMENDMENT_PROPOSAL" not in source


def test_combined_candidate_clears_only_the_three_registered_witnesses(monkeypatch):
    reports = [
        _candidate_report([0.70, 0.70, 0.05, 0.05], monkeypatch),
        _candidate_report([0.80, 0.80, 0.20, 0.20], monkeypatch),
        _candidate_report([0.55, 0.55, 0.45, 0.45], monkeypatch),
    ]
    normalized = [
        report.certification.endpoint_error / ENDPOINT_RANGE_WIDTHS
        for report in reports
    ]

    assert all(report.status is E4Status.CLEAN for report in reports)
    assert all(0 < report.adaptive_run.subdivisions < 4096 for report in reports)
    assert all(np.all(error < 1.0 / 40.0) for error in normalized)
    assert np.allclose(normalized[0], [0.0057989343, 0.0069587212], rtol=2e-8)
    assert np.allclose(normalized[1], [0.0027908232, 0.0033489878], rtol=2e-8)
    assert np.allclose(normalized[2], [0.0195584221, 0.0234701065], rtol=2e-8)
