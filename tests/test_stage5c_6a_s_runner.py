"""Structural tests for the amended contrast-free 6a-S runner."""

from dataclasses import fields
import hashlib
from inspect import signature
import json
import os
from pathlib import Path
import stat
import sys
from unittest.mock import patch

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analysis.stage5c_6a_s_runner import (  # noqa: E402
    BURN_REGISTRY,
    EXPECTED_BLOCK_PAIRS_PER_SELECTOR,
    EXPECTED_CASES_PER_ARM,
    PROTOCOL_INVARIANT_PATHS,
    DRESS_REHEARSAL_PROFILE,
    DRESS_REHEARSAL_SEED_BASE,
    REPLACEMENT_PROFILE,
    REPLACEMENT_SEED_BASES,
    AppendOnlyLedger,
    ArmAdjudication,
    ArmSelectorVerdict,
    CombinedSelectorVerdict,
    LedgerValidationError,
    RuntimeEnvironment,
    RunnerProtocolError,
    Verdict,
    _claim_then_generate,
    _assert_profile_unburned,
    _assert_prerequisite_ledger,
    _attestation_requirement,
    _execution_seed,
    _header,
    _protocol_invariant_digest,
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
)
from analysis.stage5c_selector_family import evaluation_order  # noqa: E402


COMMIT = "a" * 40
PROTOCOL_DIGEST = "b" * 64
REGISTRY_DIGEST = "c" * 64
RUNTIME_ENVIRONMENT = RuntimeEnvironment(
    "3.12.13 test runtime", "2.3.5", "1.17.0"
)


def _raw_header(target="plus", execution_profile=REPLACEMENT_PROFILE):
    return {
        "record_type": "run_header",
        **_header(
            execution_profile,
            target,
            COMMIT,
            PROTOCOL_DIGEST,
            REGISTRY_DIGEST,
            RUNTIME_ENVIRONMENT,
        ),
    }


def _complete_records(target="plus", execution_profile=REPLACEMENT_PROFILE):
    records = [_raw_header(target, execution_profile)]
    for n_index, n in enumerate(CARDINALITIES):
        for block in range(BLOCKS_PER_TARGET):
            for case in range(CASES_PER_BLOCK):
                seed = _execution_seed(
                    execution_profile, target, n_index, block, case
                )
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
    records.append(
        {
            "record_type": "arm_data_complete",
            "target": target,
            "seed_claim_count": EXPECTED_CASES_PER_ARM,
            "sample_generated_count": EXPECTED_CASES_PER_ARM,
            "selector_count": 11,
            "block_pairs_per_selector": EXPECTED_BLOCK_PAIRS_PER_SELECTOR,
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
        "execution_profile",
        "target",
        "ledger_path",
        "protocol_commit",
        "prerequisite_ledger",
    )
    header = _header(
        REPLACEMENT_PROFILE,
        "plus",
        COMMIT,
        PROTOCOL_DIGEST,
        REGISTRY_DIGEST,
        RUNTIME_ENVIRONMENT,
    )
    assert header["between_target_numeric_data"] == "FORBIDDEN"
    assert header["seed_manifest"] == "replacement-plus-1.5b"
    assert header["seed_base"] == 1_500_000_000
    assert header["runtime_environment"] == {
        "python": RUNTIME_ENVIRONMENT.python,
        "numpy": RUNTIME_ENVIRONMENT.numpy,
        "scipy": RUNTIME_ENVIRONMENT.scipy,
    }


def test_amended_seed_manifests_are_closed_and_nonoverlapping():
    assert _execution_seed(DRESS_REHEARSAL_PROFILE, "plus", 0, 0, 0) == (
        DRESS_REHEARSAL_SEED_BASE
    )
    assert _execution_seed(REPLACEMENT_PROFILE, "plus", 0, 0, 0) == (
        REPLACEMENT_SEED_BASES["plus"]
    )
    assert _execution_seed(REPLACEMENT_PROFILE, "minus", 0, 0, 0) == (
        REPLACEMENT_SEED_BASES["minus"]
    )
    assert len(
        {
            _execution_seed(profile, target, n_index, block, case)
            for profile, target in (
                (DRESS_REHEARSAL_PROFILE, "plus"),
                (REPLACEMENT_PROFILE, "plus"),
                (REPLACEMENT_PROFILE, "minus"),
            )
            for n_index in range(len(CARDINALITIES))
            for block in range(BLOCKS_PER_TARGET)
            for case in range(CASES_PER_BLOCK)
        }
    ) == 3 * EXPECTED_CASES_PER_ARM
    with pytest.raises(RunnerProtocolError):
        _execution_seed(DRESS_REHEARSAL_PROFILE, "minus", 0, 0, 0)
    for bad in (True, 1.0, "0"):
        with pytest.raises(RunnerProtocolError):
            _execution_seed(REPLACEMENT_PROFILE, "plus", bad, 0, 0)


def test_protocol_invariant_digest_covers_every_frozen_scientific_file(tmp_path):
    for index, relative_path in enumerate(PROTOCOL_INVARIANT_PATHS):
        path = tmp_path / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(f"frozen-{index}\n".encode())
    baseline = _protocol_invariant_digest(tmp_path)
    assert len(baseline) == 64
    for relative_path in PROTOCOL_INVARIANT_PATHS:
        path = tmp_path / relative_path
        original = path.read_bytes()
        path.write_bytes(original + b"changed\n")
        assert _protocol_invariant_digest(tmp_path) != baseline
        path.write_bytes(original)


def test_burn_registry_rejects_a_registered_profile_before_execution(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    original_hash = "1" * 64
    registry = {
        "schema_version": 1,
        "entries": [
            {
                "execution_profile": "original-reserved-v1",
                "target": "plus",
                "seed_base": 1_300_000_000,
                "ledger_sha256": original_hash,
                "development_log_entry": "DEV-0011",
            }
        ],
    }
    (docs / "stage5c_development_log.md").write_text(
        f"DEV-0011 {original_hash}\n", encoding="utf-8"
    )
    registry_path = tmp_path / BURN_REGISTRY
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    assert _assert_profile_unburned(
        execution_profile=DRESS_REHEARSAL_PROFILE,
        target="plus",
        repo_root=tmp_path,
    ) == hashlib.sha256(registry_path.read_bytes()).hexdigest()

    dress_hash = "2" * 64
    registry["entries"].append(
        {
            "execution_profile": DRESS_REHEARSAL_PROFILE,
            "target": "plus",
            "seed_base": DRESS_REHEARSAL_SEED_BASE,
            "ledger_sha256": dress_hash,
            "development_log_entry": "DEV-0012",
        }
    )
    (docs / "stage5c_development_log.md").write_text(
        f"DEV-0011 {original_hash}\nDEV-0012 {dress_hash}\n", encoding="utf-8"
    )
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    assert len(
        _assert_profile_unburned(
            execution_profile=REPLACEMENT_PROFILE,
            target="plus",
            repo_root=tmp_path,
        )
    ) == 64
    with pytest.raises(RunnerProtocolError, match="already burned"):
        _assert_profile_unburned(
            execution_profile=DRESS_REHEARSAL_PROFILE,
            target="plus",
            repo_root=tmp_path,
        )

    registry["entries"] = []
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    with pytest.raises(RunnerProtocolError, match="append-only lifecycle prefix"):
        _assert_profile_unburned(
            execution_profile=DRESS_REHEARSAL_PROFILE,
            target="plus",
            repo_root=tmp_path,
        )


def test_burn_registry_gate_runs_before_ledger_creation_or_seed_claim(tmp_path):
    with patch(
        "analysis.stage5c_6a_s_runner._assert_execution_checkout",
        return_value=tmp_path,
    ), patch(
        "analysis.stage5c_6a_s_runner._protocol_invariant_digest",
        return_value=PROTOCOL_DIGEST,
    ), patch(
        "analysis.stage5c_6a_s_runner._assert_profile_unburned",
        side_effect=RunnerProtocolError("already burned"),
    ), patch(
        "analysis.stage5c_6a_s_runner._assert_prerequisite_ledger"
    ) as prerequisite, patch(
        "analysis.stage5c_6a_s_runner.AppendOnlyLedger"
    ) as ledger:
        with pytest.raises(RunnerProtocolError, match="already burned"):
            run_target_arm(
                execution_profile=DRESS_REHEARSAL_PROFILE,
                target="plus",
                ledger_path=tmp_path / "must-not-exist.ndjson",
                protocol_commit=COMMIT,
            )
    prerequisite.assert_not_called()
    ledger.assert_not_called()


def test_ledger_is_exclusive_fsynced_and_hash_chained(tmp_path):
    path = tmp_path / "arm.ndjson"
    synced_types = []
    real_fsync = os.fsync

    def observe_fsync(fd):
        kind = "directory" if stat.S_ISDIR(os.fstat(fd).st_mode) else "file"
        synced_types.append(kind)
        return real_fsync(fd)

    with patch("analysis.stage5c_6a_s_runner.os.fsync", side_effect=observe_fsync):
        with AppendOnlyLedger(
            path,
            _header(
                REPLACEMENT_PROFILE,
                "plus",
                COMMIT,
                PROTOCOL_DIGEST,
                REGISTRY_DIGEST,
                RUNTIME_ENVIRONMENT,
            ),
        ) as ledger:
            ledger.append(
                "terminal_error", target="plus", category="backend", message="test"
            )
    assert synced_types[0] == "directory"
    assert "file" in synced_types[1:]
    records = read_ledger(path)
    assert [row["sequence"] for row in records] == [0, 1]
    assert records[1]["previous_sha256"] == records[0]["record_sha256"]
    with pytest.raises(FileExistsError):
        AppendOnlyLedger(
            path,
            _header(
                REPLACEMENT_PROFILE,
                "plus",
                COMMIT,
                PROTOCOL_DIGEST,
                REGISTRY_DIGEST,
                RUNTIME_ENVIRONMENT,
            ),
        )


def test_hash_chain_detects_tampering(tmp_path):
    path = tmp_path / "arm.ndjson"
    with AppendOnlyLedger(
        path,
        _header(
            REPLACEMENT_PROFILE,
            "plus",
            COMMIT,
            PROTOCOL_DIGEST,
            REGISTRY_DIGEST,
            RUNTIME_ENVIRONMENT,
        ),
    ):
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

    with AppendOnlyLedger(
        path,
        _header(
            DRESS_REHEARSAL_PROFILE,
            "plus",
            COMMIT,
            PROTOCOL_DIGEST,
            REGISTRY_DIGEST,
            RUNTIME_ENVIRONMENT,
        ),
    ) as ledger:
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


def test_kish_roundoff_at_real_pair_scale_uses_dimensionless_identity():
    records = _complete_records()
    causet = next(row for row in records if row.get("record_type") == "causet_selector")
    selected = 4_000
    kish_ess = selected + 1.864464138634503e-11
    causet.update(
        selected_pairs=selected,
        domain_pairs=4_096,
        coverage=selected / 4_096,
        normalization=float(selected),
        kish_ess=kish_ess,
        ess_fraction=kish_ess / selected,
    )
    result = adjudicate_arm_records(records)
    assert {row.verdict for row in result.selector_verdicts} == {Verdict.PASS}


def test_dimensionless_ess_relation_and_pure_transform_are_independently_locked():
    records = _complete_records()
    causet = next(row for row in records if row.get("record_type") == "causet_selector")
    causet["kish_ess"] = 48.0
    assert Verdict.PROTOCOL_INVALID in {
        row.verdict for row in adjudicate_arm_records(records).selector_verdicts
    }

    records = _complete_records()
    block = next(row for row in records if row.get("record_type") == "block_pair")
    block.update(
        signed_energy_u=0.01,
        d_law=float(np.nextafter(0.1, np.inf)),
    )
    assert Verdict.PROTOCOL_INVALID in {
        row.verdict for row in adjudicate_arm_records(records).selector_verdicts
    }


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

    records = _complete_records()
    records.pop()
    assert {row.verdict for row in adjudicate_arm_records(records).selector_verdicts} == {
        Verdict.INCONCLUSIVE
    }

    malformed = _complete_records()
    malformed[0]["execution_profile"] = DRESS_REHEARSAL_PROFILE
    assert {
        row.verdict for row in adjudicate_arm_records(malformed).selector_verdicts
    } == {Verdict.PROTOCOL_INVALID}


def test_claim_must_precede_generation_and_unknown_selector_is_invalid():
    records = _complete_records()
    claim_index = next(
        index for index, row in enumerate(records) if row.get("record_type") == "seed_claim"
    )
    generated_index = next(
        index
        for index, row in enumerate(records)
        if row.get("record_type") == "sample_generated"
    )
    records[claim_index], records[generated_index] = (
        records[generated_index],
        records[claim_index],
    )
    assert {row.verdict for row in adjudicate_arm_records(records).selector_verdicts} == {
        Verdict.PROTOCOL_INVALID
    }

    records = _complete_records()
    forged = dict(next(row for row in records if row.get("record_type") == "block_pair"))
    forged.update(
        selector='{"name":"unregistered","parameters":[]}',
        selector_name="unregistered",
    )
    records.insert(-1, forged)
    assert {row.verdict for row in adjudicate_arm_records(records).selector_verdicts} == {
        Verdict.PROTOCOL_INVALID
    }


def _categorical_arm(
    target,
    verdict=Verdict.PASS,
    commit=COMMIT,
    execution_profile=REPLACEMENT_PROFILE,
    protocol_digest=PROTOCOL_DIGEST,
    registry_digest=REGISTRY_DIGEST,
    runtime_environment=RUNTIME_ENVIRONMENT,
):
    return ArmAdjudication(
        execution_profile,
        target,
        commit,
        protocol_digest,
        registry_digest,
        runtime_environment,
        tuple(
            ArmSelectorVerdict(target, name, parameters, verdict, ("synthetic",))
            for name, parameters in evaluation_order()
        ),
    )


def test_reserved_profiles_require_committed_clean_predecessors(tmp_path):
    assert _attestation_requirement(DRESS_REHEARSAL_PROFILE, "plus") is None
    assert _attestation_requirement(REPLACEMENT_PROFILE, "plus")[3] == "DEV-0012"
    assert _attestation_requirement(REPLACEMENT_PROFILE, "minus")[3] == "DEV-0013"

    repo_root = tmp_path / "repo"
    docs = repo_root / "docs"
    docs.mkdir(parents=True)
    ledger = tmp_path / "dress.ndjson"
    ledger.write_bytes(b"synthetic dress ledger\n")
    ledger_hash = hashlib.sha256(ledger.read_bytes()).hexdigest()
    dress = _categorical_arm(
        "plus", execution_profile=DRESS_REHEARSAL_PROFILE
    )
    attestation = {
        "schema_version": 1,
        "protocol_tag": "stage5c-6a-s-runner-v2-amendment-001",
        "execution_profile": DRESS_REHEARSAL_PROFILE,
        "target": "plus",
        "protocol_invariant_digest": PROTOCOL_DIGEST,
        "burn_registry_sha256_at_start": REGISTRY_DIGEST,
        "runtime_environment": {
            "python": RUNTIME_ENVIRONMENT.python,
            "numpy": RUNTIME_ENVIRONMENT.numpy,
            "scipy": RUNTIME_ENVIRONMENT.scipy,
        },
        "ledger_sha256": ledger_hash,
        "ledger_protocol_commit": COMMIT,
        "seed_manifest": "development-3.1b",
        "seed_base": DRESS_REHEARSAL_SEED_BASE,
        "verdict_constraint": "NO_PROTOCOL_INVALID_OR_INCONCLUSIVE",
        "development_log_entry": "DEV-0012",
    }
    (docs / "stage5c_6a_s_dress_rehearsal_attestation.json").write_text(
        json.dumps(attestation), encoding="utf-8"
    )
    (docs / "stage5c_development_log.md").write_text(
        f"DEV-0012 {ledger_hash}\n", encoding="utf-8"
    )

    def adjudicate_then_replace(snapshot):
        assert snapshot == b"synthetic dress ledger\n"
        ledger.write_bytes(b"changed after immutable snapshot\n")
        return dress

    with patch(
        "analysis.stage5c_6a_s_runner._adjudicate_arm_snapshot",
        side_effect=adjudicate_then_replace,
    ):
        _assert_prerequisite_ledger(
            execution_profile=REPLACEMENT_PROFILE,
            target="plus",
            prerequisite_ledger=ledger,
            repo_root=repo_root,
            current_protocol_invariant_digest=PROTOCOL_DIGEST,
            current_runtime_environment=RUNTIME_ENVIRONMENT,
        )

    ledger.write_bytes(b"synthetic dress ledger\n")
    with patch(
        "analysis.stage5c_6a_s_runner._adjudicate_arm_snapshot", return_value=dress
    ):
        with pytest.raises(RunnerProtocolError, match="not mechanically clean"):
            _assert_prerequisite_ledger(
                execution_profile=REPLACEMENT_PROFILE,
                target="plus",
                prerequisite_ledger=ledger,
                repo_root=repo_root,
                current_protocol_invariant_digest="d" * 64,
                current_runtime_environment=RUNTIME_ENVIRONMENT,
            )
        with pytest.raises(RunnerProtocolError, match="not mechanically clean"):
            _assert_prerequisite_ledger(
                execution_profile=REPLACEMENT_PROFILE,
                target="plus",
                prerequisite_ledger=ledger,
                repo_root=repo_root,
                current_protocol_invariant_digest=PROTOCOL_DIGEST,
                current_runtime_environment=RuntimeEnvironment(
                    "3.12.13 other build", "2.3.5", "1.17.0"
                ),
            )

    invalid_dress = _categorical_arm(
        "plus",
        verdict=Verdict.PROTOCOL_INVALID,
        execution_profile=DRESS_REHEARSAL_PROFILE,
    )
    with patch(
        "analysis.stage5c_6a_s_runner._adjudicate_arm_snapshot",
        return_value=invalid_dress,
    ), pytest.raises(RunnerProtocolError):
        _assert_prerequisite_ledger(
            execution_profile=REPLACEMENT_PROFILE,
            target="plus",
            prerequisite_ledger=ledger,
            repo_root=repo_root,
            current_protocol_invariant_digest=PROTOCOL_DIGEST,
            current_runtime_environment=RUNTIME_ENVIRONMENT,
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


def test_combiner_uses_frozen_precedence_and_records_staged_commits():
    plus = _categorical_arm("plus", Verdict.FAIL)
    minus = _categorical_arm("minus", Verdict.INCONCLUSIVE)
    assert {row.verdict for row in combine_arm_adjudications(plus, minus)} == {
        Verdict.FAIL
    }
    invalid = _categorical_arm("minus", Verdict.PROTOCOL_INVALID)
    assert {row.verdict for row in combine_arm_adjudications(plus, invalid)} == {
        Verdict.PROTOCOL_INVALID
    }
    staged = combine_arm_adjudications(
        plus, _categorical_arm("minus", commit="b" * 40)
    )
    assert {row.verdict for row in staged} == {Verdict.FAIL}
    with pytest.raises(RunnerProtocolError, match="ordered plus then minus"):
        combine_arm_adjudications(
            _categorical_arm("minus"), _categorical_arm("plus")
        )
    with pytest.raises(RunnerProtocolError):
        combine_arm_adjudications(
            plus, _categorical_arm("minus", protocol_digest="d" * 64)
        )
    with pytest.raises(RunnerProtocolError, match="runtime environments"):
        combine_arm_adjudications(
            plus,
            _categorical_arm(
                "minus",
                runtime_environment=RuntimeEnvironment(
                    "3.12.13 other build", "2.3.5", "1.17.0"
                ),
            ),
        )
    forged_rows = list(_categorical_arm("minus").selector_verdicts)
    forged_rows[0] = ArmSelectorVerdict(
        "plus",
        forged_rows[0].selector_name,
        forged_rows[0].parameters,
        forged_rows[0].verdict,
        forged_rows[0].reasons,
    )
    with pytest.raises(RunnerProtocolError):
        combine_arm_adjudications(
            plus,
            ArmAdjudication(
                REPLACEMENT_PROFILE,
                "minus",
                COMMIT,
                PROTOCOL_DIGEST,
                REGISTRY_DIGEST,
                RUNTIME_ENVIRONMENT,
                tuple(forged_rows),
            ),
        )


def test_stored_verdicts_are_recomputed_not_trusted(tmp_path):
    path = tmp_path / "partial.ndjson"
    with AppendOnlyLedger(
        path,
        _header(
            REPLACEMENT_PROFILE,
            "plus",
            COMMIT,
            PROTOCOL_DIGEST,
            REGISTRY_DIGEST,
            RUNTIME_ENVIRONMENT,
        ),
    ) as ledger:
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
