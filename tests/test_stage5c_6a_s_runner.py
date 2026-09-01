"""Structural tests for the frozen contrast-free 6a-S runner."""

from dataclasses import fields
from inspect import signature
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analysis.stage5c_6a_s_runner import (  # noqa: E402
    EXPECTED_BLOCK_PAIRS_PER_SELECTOR,
    EXPECTED_CASES_PER_ARM,
    AppendOnlyLedger,
    ArmAdjudication,
    ArmSelectorVerdict,
    CombinedSelectorVerdict,
    LedgerValidationError,
    RunnerProtocolError,
    Verdict,
    _claim_then_generate,
    _header,
    _selector_token,
    adjudicate_arm_ledger,
    adjudicate_arm_records,
    combine_arm_adjudications,
    read_ledger,
    run_target_arm,
    write_combined_ledger,
)
from analysis.stage5c_measure_prereg import (  # noqa: E402
    BLOCKS_PER_TARGET,
    CARDINALITIES,
    CASES_PER_BLOCK,
    preregistered_seed,
)
from analysis.stage5c_selector_family import evaluation_order  # noqa: E402


COMMIT = "a" * 40


def _raw_header(target="plus"):
    return {"record_type": "run_header", **_header(target, COMMIT)}


def _complete_records(target="plus"):
    records = [_raw_header(target)]
    for n_index, n in enumerate(CARDINALITIES):
        for block in range(BLOCKS_PER_TARGET):
            for case in range(CASES_PER_BLOCK):
                seed = preregistered_seed(target, n_index, block, case)
                common = {
                    "target": target,
                    "n": n,
                    "n_index": n_index,
                    "block": block,
                    "case": case,
                    "seed": seed,
                }
                records.append(
                    {
                        "record_type": "seed_claim",
                        **common,
                        "seed_state": "BURNED_ON_CLAIM_BEFORE_GENERATION",
                    }
                )
                records.append({"record_type": "sample_generated", **common})
                for name, parameters in evaluation_order():
                    records.append(
                        {
                            "record_type": "causet_selector",
                            **common,
                            "selector": _selector_token(name, parameters),
                            "selector_name": name,
                            "parameters": list(parameters),
                            "case_id": f"synthetic-{n_index}-{block}-{case}",
                            "selected_pairs": 64,
                            "domain_pairs": 256,
                            "coverage": 0.25,
                            "normalization": 64.0,
                            "total_mass": 1.0,
                            "total_variation": 1.0,
                            "kish_ess": 64.0,
                            "ess_fraction": 1.0,
                            "s1_pass": True,
                            "s2_pass": True,
                            "s3_pass": True,
                            "s4_pass": True,
                            "s6_pass": True,
                        }
                    )
    for name, parameters in evaluation_order():
        token = _selector_token(name, parameters)
        for n_index, n in enumerate(CARDINALITIES):
            for left in range(BLOCKS_PER_TARGET):
                for right in range(left + 1, BLOCKS_PER_TARGET):
                    records.append(
                        {
                            "record_type": "block_pair",
                            "target": target,
                            "selector": token,
                            "selector_name": name,
                            "parameters": list(parameters),
                            "n": n,
                            "n_index": n_index,
                            "left_block": left,
                            "right_block": right,
                            "d_mean": 0.05,
                            "signed_energy_u": -0.001,
                            "d_law": 0.0,
                            "s5_pass": True,
                        }
                    )
    return records


def _verdict_map(result):
    return {
        (row.selector_name, row.parameters): row.verdict
        for row in result.selector_verdicts
    }


def test_frozen_counts_cover_every_expected_cell():
    assert EXPECTED_CASES_PER_ARM == 3 * 4 * 64 == 768
    assert EXPECTED_BLOCK_PAIRS_PER_SELECTOR == 3 * 6 == 18
    assert len(evaluation_order()) == 11
    assert tuple(signature(run_target_arm).parameters) == (
        "target",
        "ledger_path",
        "protocol_commit",
    )
    assert _header("plus", COMMIT)["between_target_numeric_data"] == "FORBIDDEN"


def test_ledger_is_exclusive_fsynced_and_hash_chained(tmp_path):
    path = tmp_path / "arm.ndjson"
    with AppendOnlyLedger(path, _header("plus", COMMIT)) as ledger:
        ledger.append("terminal_error", target="plus", category="backend", message="test")
    records = read_ledger(path)
    assert [row["sequence"] for row in records] == [0, 1]
    assert records[1]["previous_sha256"] == records[0]["record_sha256"]
    with pytest.raises(FileExistsError):
        AppendOnlyLedger(path, _header("plus", COMMIT))


def test_hash_chain_detects_tampering(tmp_path):
    path = tmp_path / "arm.ndjson"
    with AppendOnlyLedger(path, _header("plus", COMMIT)):
        pass
    record = json.loads(path.read_text(encoding="utf-8"))
    record["target"] = "minus"
    path.write_text(json.dumps(record) + "\n", encoding="utf-8")
    with pytest.raises(LedgerValidationError):
        read_ledger(path)


def test_seed_claim_is_durable_before_generator_call(tmp_path):
    path = tmp_path / "claim.ndjson"

    class DeliberateStop(RuntimeError):
        pass

    def generator(_n, _theta, seed):
        records = read_ledger(path)
        assert records[-1]["record_type"] == "seed_claim"
        assert records[-1]["seed"] == seed == 3_100_000_000
        raise DeliberateStop

    with AppendOnlyLedger(path, _header("plus", COMMIT)) as ledger:
        with pytest.raises(DeliberateStop):
            _claim_then_generate(
                ledger,
                target="plus",
                n_index=0,
                block=0,
                case_index=0,
                seed=3_100_000_000,
                generator=generator,
            )
    assert [row["record_type"] for row in read_ledger(path)] == [
        "run_header",
        "seed_claim",
    ]


def test_complete_single_arm_adjudicates_all_selectors_pass():
    result = adjudicate_arm_records(_complete_records())
    assert result.target == "plus"
    assert len(result.selector_verdicts) == 11
    assert {row.verdict for row in result.selector_verdicts} == {Verdict.PASS}


def test_floor_and_s5_failures_are_mechanical():
    records = _complete_records()
    token = _selector_token("all_relations", ())
    causet = next(
        row
        for row in records
        if row.get("record_type") == "causet_selector" and row.get("selector") == token
    )
    causet.update(
        selected_pairs=31,
        coverage=31 / 256,
        normalization=31.0,
        kish_ess=31.0,
        s1_pass=False,
        s6_pass=False,
    )
    result = adjudicate_arm_records(records)
    assert _verdict_map(result)[("all_relations", ())] == Verdict.FAIL

    records = _complete_records()
    block = next(
        row
        for row in records
        if row.get("record_type") == "block_pair" and row.get("selector") == token
    )
    block.update(d_mean=0.201, s5_pass=False)
    result = adjudicate_arm_records(records)
    assert _verdict_map(result)[("all_relations", ())] == Verdict.FAIL


def test_structural_failure_or_forged_gate_flag_is_protocol_invalid():
    records = _complete_records()
    causet = next(row for row in records if row.get("record_type") == "causet_selector")
    causet["s2_pass"] = False
    assert {row.verdict for row in adjudicate_arm_records(records).selector_verdicts} >= {
        Verdict.PROTOCOL_INVALID
    }

    records = _complete_records()
    block = next(row for row in records if row.get("record_type") == "block_pair")
    block["d_mean"] = 0.25
    block["s5_pass"] = True
    assert Verdict.PROTOCOL_INVALID in {
        row.verdict for row in adjudicate_arm_records(records).selector_verdicts
    }


def test_interruption_is_inconclusive_and_mixed_target_is_invalid():
    result = adjudicate_arm_records([_raw_header()])
    assert {row.verdict for row in result.selector_verdicts} == {Verdict.INCONCLUSIVE}

    records = _complete_records()
    records[1]["target"] = "minus"
    assert {row.verdict for row in adjudicate_arm_records(records).selector_verdicts} == {
        Verdict.PROTOCOL_INVALID
    }


def _categorical_arm(target, verdict=Verdict.PASS, commit=COMMIT):
    return ArmAdjudication(
        target,
        commit,
        tuple(
            ArmSelectorVerdict(target, name, parameters, verdict, ("synthetic",))
            for name, parameters in evaluation_order()
        ),
    )


def test_cross_arm_boundary_contains_categorical_verdicts_only(tmp_path):
    assert [field.name for field in fields(ArmSelectorVerdict)] == [
        "target",
        "selector_name",
        "parameters",
        "verdict",
        "reasons",
    ]
    assert [field.name for field in fields(CombinedSelectorVerdict)] == [
        "selector_name",
        "parameters",
        "verdict",
        "arm_verdicts",
    ]
    plus = _categorical_arm("plus")
    minus = _categorical_arm("minus")
    output = tmp_path / "combined.ndjson"
    rows = write_combined_ledger(output, plus, minus)
    assert {row.verdict for row in rows} == {Verdict.PASS}
    text = output.read_text(encoding="utf-8")
    for forbidden in ("d_mean", "d_law", "signed_energy", "coordinates", "signature"):
        assert forbidden not in text


def test_combiner_uses_frozen_precedence_and_matching_commit():
    plus = _categorical_arm("plus", Verdict.FAIL)
    minus = _categorical_arm("minus", Verdict.INCONCLUSIVE)
    assert {row.verdict for row in combine_arm_adjudications(plus, minus)} == {
        Verdict.FAIL
    }
    invalid = _categorical_arm("minus", Verdict.PROTOCOL_INVALID)
    assert {row.verdict for row in combine_arm_adjudications(plus, invalid)} == {
        Verdict.PROTOCOL_INVALID
    }
    with pytest.raises(RunnerProtocolError):
        combine_arm_adjudications(plus, _categorical_arm("minus", commit="b" * 40))


def test_stored_verdicts_are_recomputed_not_trusted(tmp_path):
    path = tmp_path / "partial.ndjson"
    with AppendOnlyLedger(path, _header("plus", COMMIT)) as ledger:
        for name, parameters in evaluation_order():
            ledger.append(
                "arm_selector_verdict",
                target="plus",
                selector=_selector_token(name, parameters),
                selector_name=name,
                parameters=list(parameters),
                verdict=Verdict.PASS.value,
                reasons=["forged"],
            )
    with pytest.raises(LedgerValidationError):
        adjudicate_arm_ledger(path)
