"""Amended contrast-free runner and adjudicator for Stage 5C 6a-S.

The executable boundary is deliberately one target arm at a time.  No function
in this module accepts numerical data from both targets.  The only cross-arm
operation combines categorical per-selector verdicts after both arm ledgers
have been independently adjudicated.

Importing this module never generates a sample.  Execution is allowed only
through the explicit ``run-arm`` command from a clean checkout whose HEAD
matches the recorded protocol commit.  The development dress rehearsal and
the replacement reserved arms use the same data path and adjudicator, with
closed, profile-specific seed manifests and committed prerequisite attestations.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from enum import Enum
import hashlib
from itertools import combinations
import json
import os
from pathlib import Path
import subprocess
from typing import Callable, Iterable

import numpy as np

from analysis.stage5c_hard_controls import (
    BlindedCase,
    CONTROL_THETA,
    ControlSample,
    sprinkle_control,
)
from analysis.stage5c_measure_prereg import (
    BLOCKS_PER_TARGET,
    CARDINALITIES,
    CASES_PER_BLOCK,
    MASS_TOLERANCE,
    MAX_MEAN_SIGNATURE_DISTANCE,
    MAX_RANDOM_LAW_ENERGY_DISTANCE,
    MIN_ESS_FRACTION,
    MIN_KISH_ESS,
    MIN_PAIR_COVERAGE,
    MIN_SELECTED_PAIRS,
    fourier_signature,
    mean_signature_distance,
    measure_diagnostics,
    normalised_weights,
    random_law_energy_statistic,
    uniform_pair_weights,
)
from analysis.stage5c_selector_family import (
    CAPACITY_LIMIT,
    SelectorDomainError,
    SelectorProtocolError,
    SelectorSelectionError,
    admissible_pairs,
    apply_selector,
    evaluation_order,
    family_capacity,
    relabel,
)


PROTOCOL_TAG = "stage5c-6a-s-runner-v2-amendment-001"
LEDGER_SCHEMA_VERSION = 2
TARGET_THETA = {"plus": CONTROL_THETA, "minus": -CONTROL_THETA}
DRESS_REHEARSAL_PROFILE = "development-dress-rehearsal"
REPLACEMENT_PROFILE = "replacement-reserved"
EXECUTION_PROFILES = (DRESS_REHEARSAL_PROFILE, REPLACEMENT_PROFILE)
DRESS_REHEARSAL_SEED_BASE = 3_100_000_000
REPLACEMENT_SEED_BASES = {"plus": 1_500_000_000, "minus": 1_400_000_000}
DRESS_REHEARSAL_ATTESTATION = Path(
    "docs/stage5c_6a_s_dress_rehearsal_attestation.json"
)
REPLACEMENT_PLUS_ATTESTATION = Path(
    "docs/stage5c_6a_s_replacement_plus_attestation.json"
)
DEVELOPMENT_LOG = Path("docs/stage5c_development_log.md")
EXPECTED_CASES_PER_ARM = len(CARDINALITIES) * BLOCKS_PER_TARGET * CASES_PER_BLOCK
EXPECTED_BLOCK_PAIRS_PER_SELECTOR = len(CARDINALITIES) * len(
    tuple(combinations(range(BLOCKS_PER_TARGET), 2))
)


class Verdict(str, Enum):
    PASS = "6a-S PASS"
    FAIL = "6a-S FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"
    PROTOCOL_INVALID = "PROTOCOL-INVALID"


class RunnerProtocolError(RuntimeError):
    """The execution attempted to violate the frozen runner contract."""


class LedgerValidationError(RunnerProtocolError):
    """An append-only ledger is malformed or has a broken hash chain."""


@dataclass(frozen=True)
class ArmSelectorVerdict:
    """Categorical output boundary; deliberately contains no numerical data."""

    target: str
    selector_name: str
    parameters: tuple
    verdict: Verdict
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class ArmAdjudication:
    execution_profile: str
    target: str
    protocol_commit: str
    selector_verdicts: tuple[ArmSelectorVerdict, ...]


@dataclass(frozen=True)
class CombinedSelectorVerdict:
    selector_name: str
    parameters: tuple
    verdict: Verdict
    arm_verdicts: tuple[tuple[str, str], ...]


def _canonical_json(value: dict) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


class AppendOnlyLedger:
    """Exclusive-create NDJSON ledger with an fsynced SHA256 hash chain."""

    def __init__(self, path: str | Path, header: dict):
        self.path = Path(path)
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_APPEND
        self._fd = os.open(self.path, flags, 0o600)
        try:
            directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
            directory_fd = os.open(self.path.parent, directory_flags)
            try:
                # Persist the newly created directory entry before any claim
                # can be written and before any reserved generator can run.
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        except Exception:
            os.close(self._fd)
            self._fd = None
            raise
        self._sequence = 0
        self._previous_sha256 = "0" * 64
        self.records: list[dict] = []
        self.append("run_header", **header)

    def append(self, record_type: str, **payload: object) -> dict:
        if self._fd is None:
            raise RunnerProtocolError("ledger is closed")
        core = {
            "sequence": self._sequence,
            "previous_sha256": self._previous_sha256,
            "record_type": record_type,
            **payload,
        }
        digest = hashlib.sha256(_canonical_json(core).encode("utf-8")).hexdigest()
        record = {**core, "record_sha256": digest}
        encoded = (_canonical_json(record) + "\n").encode("utf-8")
        view = memoryview(encoded)
        while view:
            written = os.write(self._fd, view)
            if written <= 0:
                raise OSError("ledger append made no progress")
            view = view[written:]
        os.fsync(self._fd)
        self.records.append(record)
        self._sequence += 1
        self._previous_sha256 = digest
        return record

    def close(self) -> None:
        if self._fd is not None:
            os.close(self._fd)
            self._fd = None

    def __enter__(self) -> "AppendOnlyLedger":
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()


def read_ledger(path: str | Path) -> tuple[dict, ...]:
    """Read and validate every record, sequence number, and hash-chain link."""

    def reject_constant(value: str) -> None:
        raise LedgerValidationError(f"non-finite JSON constant: {value}")

    records: list[dict] = []
    previous = "0" * 64
    with Path(path).open("r", encoding="utf-8") as handle:
        for sequence, line in enumerate(handle):
            try:
                record = json.loads(line, parse_constant=reject_constant)
            except (json.JSONDecodeError, LedgerValidationError) as exc:
                raise LedgerValidationError("invalid ledger JSON") from exc
            if not isinstance(record, dict):
                raise LedgerValidationError("ledger row must be an object")
            digest = record.get("record_sha256")
            core = {key: value for key, value in record.items() if key != "record_sha256"}
            expected = hashlib.sha256(_canonical_json(core).encode("utf-8")).hexdigest()
            if (
                record.get("sequence") != sequence
                or record.get("previous_sha256") != previous
                or digest != expected
            ):
                raise LedgerValidationError("ledger sequence or hash chain is broken")
            records.append(record)
            previous = digest
    if not records or records[0].get("record_type") != "run_header":
        raise LedgerValidationError("ledger must start with run_header")
    return tuple(records)


def _selector_token(name: str, parameters: tuple) -> str:
    return _canonical_json({"name": name, "parameters": list(parameters)})


def _opaque_case_id(order: np.ndarray) -> str:
    return "6AS-" + hashlib.sha256(np.asarray(order, dtype=np.bool_).tobytes()).hexdigest()[:24]


def _relabel_covariant(name: str, parameters: tuple, case: BlindedCase) -> bool:
    n = case.order.shape[0]
    permutation = np.roll(np.arange(n), 1)
    base = apply_selector(name, parameters, case)
    moved = apply_selector(name, parameters, relabel(case, permutation))
    expected = {(int(x), int(y)) for x, y in base}
    recovered = {(int(permutation[x]), int(permutation[y])) for x, y in moved}
    return expected == recovered


def _claim_then_generate(
    ledger: AppendOnlyLedger,
    *,
    target: str,
    n_index: int,
    block: int,
    case_index: int,
    seed: int,
    generator: Callable[[int, float, int], ControlSample],
) -> ControlSample:
    """Fsync a burned-seed claim before invoking the generator."""
    n = CARDINALITIES[n_index]
    ledger.append(
        "seed_claim",
        target=target,
        n=n,
        n_index=n_index,
        block=block,
        case=case_index,
        seed=seed,
        seed_state="BURNED_ON_CLAIM_BEFORE_GENERATION",
    )
    sample = generator(n, TARGET_THETA[target], seed)
    if (
        not isinstance(sample, ControlSample)
        or sample.seed != seed
        or sample.theta != TARGET_THETA[target]
        or sample.order.shape != (n, n)
        or sample.order.dtype != np.bool_
        or sample.coordinates.shape != (n, 2)
        or not np.all(np.isfinite(sample.coordinates))
        or np.any(sample.coordinates < 0.0)
        or np.any(sample.coordinates > 1.0)
    ):
        raise RunnerProtocolError("generator output violates the frozen sample schema")
    ledger.append(
        "sample_generated",
        target=target,
        n=n,
        n_index=n_index,
        block=block,
        case=case_index,
        seed=seed,
    )
    return sample


def _case_record(
    *,
    target: str,
    n: int,
    n_index: int,
    block: int,
    case_index: int,
    seed: int,
    case: BlindedCase,
    sample: ControlSample,
    selector_name: str,
    parameters: tuple,
) -> tuple[dict, np.ndarray | None]:
    token = _selector_token(selector_name, parameters)
    structural_s3 = set(vars(case)) == {"case_id", "order"}
    structural_s4 = family_capacity() == CAPACITY_LIMIT == len(evaluation_order())
    try:
        domain_pairs = int(admissible_pairs(case).shape[0])
        selection = apply_selector(selector_name, parameters, case)
    except (SelectorSelectionError, SelectorDomainError):
        return (
            {
                "target": target,
                "selector": token,
                "selector_name": selector_name,
                "parameters": list(parameters),
                "n": n,
                "n_index": n_index,
                "block": block,
                "case": case_index,
                "case_id": case.case_id,
                "seed": seed,
                "selected_pairs": 0,
                "domain_pairs": domain_pairs,
                "coverage": 0.0,
                "normalization": None,
                "total_mass": None,
                "total_variation": None,
                "kish_ess": 0.0,
                "ess_fraction": 0.0,
                "s1_pass": False,
                "s2_pass": True,
                "s3_pass": structural_s3,
                "s4_pass": structural_s4,
                "s6_pass": False,
            },
            None,
        )
    diagnostics = measure_diagnostics(len(selection), domain_pairs)
    weights, normalization = uniform_pair_weights(len(selection))
    probability = normalised_weights(weights, normalization)
    pair_coordinates = np.concatenate(
        [sample.coordinates[selection[:, 0]], sample.coordinates[selection[:, 1]]],
        axis=1,
    )
    signature = fourier_signature(pair_coordinates, probability)
    s1_pass = diagnostics.selected_pairs >= MIN_SELECTED_PAIRS
    s6_pass = bool(
        diagnostics.coverage >= MIN_PAIR_COVERAGE
        and diagnostics.normalization >= MIN_SELECTED_PAIRS
        and np.isfinite(diagnostics.normalization)
        and diagnostics.kish_ess >= MIN_KISH_ESS
        and diagnostics.ess_fraction >= MIN_ESS_FRACTION
        and abs(diagnostics.total_mass - 1.0) <= MASS_TOLERANCE
        and abs(diagnostics.total_variation - 1.0) <= MASS_TOLERANCE
    )
    return (
        {
            "target": target,
            "selector": token,
            "selector_name": selector_name,
            "parameters": list(parameters),
            "n": n,
            "n_index": n_index,
            "block": block,
            "case": case_index,
            "case_id": case.case_id,
            "seed": seed,
            **asdict(diagnostics),
            "s1_pass": s1_pass,
            "s2_pass": _relabel_covariant(selector_name, parameters, case),
            "s3_pass": structural_s3,
            "s4_pass": structural_s4,
            "s6_pass": s6_pass,
        },
        signature,
    )


def _execution_seed(
    execution_profile: str,
    target: str,
    n_index: int,
    block: int,
    case: int,
) -> int:
    """Return one seed from the closed Amendment-001 manifests."""
    if execution_profile not in EXECUTION_PROFILES:
        raise RunnerProtocolError("unregistered execution profile")
    if target not in TARGET_THETA:
        raise RunnerProtocolError("target must be one frozen arm")
    if execution_profile == DRESS_REHEARSAL_PROFILE and target != "plus":
        raise RunnerProtocolError("dress rehearsal is one plus-target arm only")
    indices = (
        (n_index, len(CARDINALITIES), "n_index"),
        (block, BLOCKS_PER_TARGET, "block"),
        (case, CASES_PER_BLOCK, "case"),
    )
    for value, upper, label in indices:
        if (
            not isinstance(value, int)
            or isinstance(value, bool)
            or not 0 <= value < upper
        ):
            raise RunnerProtocolError(f"{label} is outside the frozen manifest")
    base = (
        DRESS_REHEARSAL_SEED_BASE
        if execution_profile == DRESS_REHEARSAL_PROFILE
        else REPLACEMENT_SEED_BASES[target]
    )
    return base + 1_000_000 * n_index + 10_000 * block + case


def _seed_manifest(execution_profile: str, target: str) -> tuple[str, int]:
    if execution_profile == DRESS_REHEARSAL_PROFILE and target == "plus":
        return "development-3.1b", DRESS_REHEARSAL_SEED_BASE
    if execution_profile == REPLACEMENT_PROFILE and target in TARGET_THETA:
        return (
            "replacement-plus-1.5b" if target == "plus" else "reserved-minus-1.4b",
            REPLACEMENT_SEED_BASES[target],
        )
    raise RunnerProtocolError("execution profile and target are not registered together")


def _header(execution_profile: str, target: str, protocol_commit: str) -> dict:
    if target not in TARGET_THETA:
        raise RunnerProtocolError("target must be one frozen arm")
    if len(protocol_commit) != 40 or any(ch not in "0123456789abcdef" for ch in protocol_commit):
        raise RunnerProtocolError("protocol_commit must be one lowercase 40-hex SHA")
    manifest, seed_base = _seed_manifest(execution_profile, target)
    return {
        "schema_version": LEDGER_SCHEMA_VERSION,
        "protocol_tag": PROTOCOL_TAG,
        "protocol_commit": protocol_commit,
        "execution_profile": execution_profile,
        "target": target,
        "seed_manifest": manifest,
        "seed_base": seed_base,
        "expected_cases": EXPECTED_CASES_PER_ARM,
        "expected_selectors": CAPACITY_LIMIT,
        "expected_block_pairs_per_selector": EXPECTED_BLOCK_PAIRS_PER_SELECTOR,
        "between_target_numeric_data": "FORBIDDEN",
    }


def _sha256_path(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _attestation_requirement(
    execution_profile: str, target: str
) -> tuple[Path, str, str, str] | None:
    if execution_profile == DRESS_REHEARSAL_PROFILE:
        if target != "plus":
            raise RunnerProtocolError("dress rehearsal is one plus-target arm only")
        return None
    if execution_profile != REPLACEMENT_PROFILE:
        raise RunnerProtocolError("unregistered execution profile")
    if target == "plus":
        return (
            DRESS_REHEARSAL_ATTESTATION,
            DRESS_REHEARSAL_PROFILE,
            "plus",
            "DEV-0012",
        )
    if target == "minus":
        return (
            REPLACEMENT_PLUS_ATTESTATION,
            REPLACEMENT_PROFILE,
            "plus",
            "DEV-0013",
        )
    raise RunnerProtocolError("target must be one frozen arm")


def _assert_prerequisite_ledger(
    *,
    execution_profile: str,
    target: str,
    prerequisite_ledger: str | Path | None,
    repo_root: Path,
) -> None:
    """Require the committed lifecycle attestation before either reserved arm."""
    requirement = _attestation_requirement(execution_profile, target)
    if requirement is None:
        if prerequisite_ledger is not None:
            raise RunnerProtocolError("dress rehearsal accepts no prerequisite ledger")
        return
    if prerequisite_ledger is None:
        raise RunnerProtocolError("reserved execution requires its prerequisite ledger")
    attestation_path, required_profile, required_target, development_entry = requirement
    full_attestation_path = repo_root / attestation_path
    if not full_attestation_path.is_file():
        raise RunnerProtocolError("required committed prerequisite attestation is absent")
    try:
        attestation = json.loads(full_attestation_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RunnerProtocolError("prerequisite attestation is not valid JSON") from exc
    ledger_path = Path(prerequisite_ledger).resolve()
    try:
        ledger_path.relative_to(repo_root)
    except ValueError:
        pass
    else:
        raise RunnerProtocolError("prerequisite ledgers must be outside the git checkout")
    adjudication = adjudicate_arm_ledger(ledger_path)
    ledger_hash = _sha256_path(ledger_path)
    required_manifest, required_seed_base = _seed_manifest(
        required_profile, required_target
    )
    expected = {
        "schema_version": 1,
        "protocol_tag": PROTOCOL_TAG,
        "execution_profile": required_profile,
        "target": required_target,
        "ledger_sha256": ledger_hash,
        "ledger_protocol_commit": adjudication.protocol_commit,
        "seed_manifest": required_manifest,
        "seed_base": required_seed_base,
        "verdict_constraint": "NO_PROTOCOL_INVALID_OR_INCONCLUSIVE",
        "development_log_entry": development_entry,
    }
    if attestation != expected:
        raise RunnerProtocolError("prerequisite attestation disagrees with ledger")
    if (
        adjudication.execution_profile != required_profile
        or adjudication.target != required_target
        or any(
            row.verdict in {Verdict.PROTOCOL_INVALID, Verdict.INCONCLUSIVE}
            for row in adjudication.selector_verdicts
        )
    ):
        raise RunnerProtocolError("prerequisite ledger is not mechanically clean")
    development_log_path = repo_root / DEVELOPMENT_LOG
    try:
        development_log = development_log_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RunnerProtocolError("development log is unavailable") from exc
    if development_entry not in development_log or ledger_hash not in development_log:
        raise RunnerProtocolError("prerequisite is not recorded in the development log")


def run_target_arm(
    *,
    execution_profile: str,
    target: str,
    ledger_path: str | Path,
    protocol_commit: str,
    prerequisite_ledger: str | Path | None = None,
) -> ArmAdjudication:
    """Generate and adjudicate one frozen profile/target arm exactly once."""
    header = _header(execution_profile, target, protocol_commit)
    repo_root = _assert_execution_checkout(protocol_commit, ledger_path)
    _assert_prerequisite_ledger(
        execution_profile=execution_profile,
        target=target,
        prerequisite_ledger=prerequisite_ledger,
        repo_root=repo_root,
    )
    signatures: dict[tuple[str, int, int], list[np.ndarray]] = {}
    with AppendOnlyLedger(ledger_path, header) as ledger:
        try:
            for n_index, n in enumerate(CARDINALITIES):
                for block in range(BLOCKS_PER_TARGET):
                    for case_index in range(CASES_PER_BLOCK):
                        seed = _execution_seed(
                            execution_profile, target, n_index, block, case_index
                        )
                        sample = _claim_then_generate(
                            ledger,
                            target=target,
                            n_index=n_index,
                            block=block,
                            case_index=case_index,
                            seed=seed,
                            generator=sprinkle_control,
                        )
                        case = BlindedCase(_opaque_case_id(sample.order), sample.order.copy())
                        for name, parameters in evaluation_order():
                            row, signature = _case_record(
                                target=target,
                                n=n,
                                n_index=n_index,
                                block=block,
                                case_index=case_index,
                                seed=seed,
                                case=case,
                                sample=sample,
                                selector_name=name,
                                parameters=parameters,
                            )
                            ledger.append("causet_selector", **row)
                            if signature is not None:
                                signatures.setdefault(
                                    (row["selector"], n_index, block), []
                                ).append(signature)

            for name, parameters in evaluation_order():
                token = _selector_token(name, parameters)
                for n_index, n in enumerate(CARDINALITIES):
                    for left_block, right_block in combinations(
                        range(BLOCKS_PER_TARGET), 2
                    ):
                        left = np.asarray(signatures.get((token, n_index, left_block), []))
                        right = np.asarray(signatures.get((token, n_index, right_block), []))
                        if len(left) != CASES_PER_BLOCK or len(right) != CASES_PER_BLOCK:
                            continue
                        d_mean = mean_signature_distance(left, right)
                        signed_energy = random_law_energy_statistic(left, right)
                        d_law = float(np.sqrt(max(0.0, signed_energy)))
                        ledger.append(
                            "block_pair",
                            target=target,
                            selector=token,
                            selector_name=name,
                            parameters=list(parameters),
                            n=n,
                            n_index=n_index,
                            left_block=left_block,
                            right_block=right_block,
                            d_mean=d_mean,
                            signed_energy_u=signed_energy,
                            d_law=d_law,
                            s5_pass=bool(
                                d_mean <= MAX_MEAN_SIGNATURE_DISTANCE
                                and d_law <= MAX_RANDOM_LAW_ENERGY_DISTANCE
                            ),
                        )
            ledger.append(
                "arm_data_complete",
                target=target,
                seed_claim_count=EXPECTED_CASES_PER_ARM,
                sample_generated_count=EXPECTED_CASES_PER_ARM,
                selector_count=CAPACITY_LIMIT,
                block_pairs_per_selector=EXPECTED_BLOCK_PAIRS_PER_SELECTOR,
            )
        except (RunnerProtocolError, SelectorProtocolError) as exc:
            ledger.append(
                "terminal_error",
                target=target,
                category="protocol",
                message=str(exc),
            )
        except Exception as exc:
            ledger.append(
                "terminal_error",
                target=target,
                category="backend",
                message=type(exc).__name__,
            )

        adjudication = adjudicate_arm_records(tuple(ledger.records))
        for result in adjudication.selector_verdicts:
            ledger.append(
                "arm_selector_verdict",
                target=result.target,
                selector=_selector_token(result.selector_name, result.parameters),
                selector_name=result.selector_name,
                parameters=list(result.parameters),
                verdict=result.verdict.value,
                reasons=list(result.reasons),
            )
        ledger.append(
            "arm_complete",
            target=target,
            selector_verdict_count=len(adjudication.selector_verdicts),
        )
    return adjudication


def _records_before_verdicts(records: Iterable[dict]) -> tuple[dict, ...]:
    return tuple(
        row
        for row in records
        if row.get("record_type") not in {"arm_selector_verdict", "arm_complete"}
    )


def _finite_number(value: object) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and np.isfinite(value)
    )


def _registered_index(value: object, upper: int) -> bool:
    return (
        isinstance(value, int)
        and not isinstance(value, bool)
        and 0 <= value < upper
    )


def adjudicate_arm_records(records: Iterable[dict]) -> ArmAdjudication:
    """Apply S1-S6 and interruption semantics to one arm's records."""
    rows = _records_before_verdicts(records)
    headers = [row for row in rows if row.get("record_type") == "run_header"]
    if len(headers) != 1:
        raise LedgerValidationError("exactly one run_header is required")
    header = headers[0]
    execution_profile = header.get("execution_profile")
    target = header.get("target")
    protocol_commit = header.get("protocol_commit")
    global_invalid: list[str] = []
    global_inconclusive: list[str] = []
    if target not in TARGET_THETA:
        global_invalid.append("unregistered target")
    try:
        expected_header = _header(
            str(execution_profile), str(target), str(protocol_commit)
        )
    except RunnerProtocolError as exc:
        global_invalid.append(str(exc))
    else:
        if any(header.get(key) != value for key, value in expected_header.items()):
            global_invalid.append("run_header disagrees with frozen schema")
    allowed_types = {
        "run_header",
        "seed_claim",
        "sample_generated",
        "causet_selector",
        "block_pair",
        "arm_data_complete",
        "terminal_error",
    }
    if any(row.get("record_type") not in allowed_types for row in rows):
        global_invalid.append("unregistered record type")
    expected_selector_tokens = {
        _selector_token(name, parameters) for name, parameters in evaluation_order()
    }
    selector_rows = [
        row
        for row in rows
        if row.get("record_type") in {"causet_selector", "block_pair"}
    ]
    if any(row.get("selector") not in expected_selector_tokens for row in selector_rows):
        global_invalid.append("record references an unregistered selector")
    if any(
        row.get("target") != target
        for row in rows
        if row.get("record_type") != "run_header"
    ):
        global_invalid.append("mixed-target ledger")
    errors = [row for row in rows if row.get("record_type") == "terminal_error"]
    if any(row.get("category") == "protocol" for row in errors):
        global_invalid.append("runner protocol error")
    if any(row.get("category") == "backend" for row in errors):
        global_inconclusive.append("backend or resource interruption")
    completion = [
        row for row in rows if row.get("record_type") == "arm_data_complete"
    ]
    if not completion:
        global_inconclusive.append("arm data phase lacks completion marker")
    elif len(completion) != 1:
        global_invalid.append("duplicate arm data completion marker")
    else:
        expected_completion = {
            "target": target,
            "seed_claim_count": EXPECTED_CASES_PER_ARM,
            "sample_generated_count": EXPECTED_CASES_PER_ARM,
            "selector_count": CAPACITY_LIMIT,
            "block_pairs_per_selector": EXPECTED_BLOCK_PAIRS_PER_SELECTOR,
        }
        if any(completion[0].get(key) != value for key, value in expected_completion.items()):
            global_invalid.append("arm data completion marker disagrees with schema")

    claims = [row for row in rows if row.get("record_type") == "seed_claim"]
    generated = [row for row in rows if row.get("record_type") == "sample_generated"]
    claim_cells = {
        (row.get("n_index"), row.get("block"), row.get("case"), row.get("seed"))
        for row in claims
    }
    generated_cells = {
        (row.get("n_index"), row.get("block"), row.get("case"), row.get("seed"))
        for row in generated
    }
    if len(claim_cells) != len(claims) or len(generated_cells) != len(generated):
        global_invalid.append("duplicate seed record")
    claim_positions = {
        (row.get("n_index"), row.get("block"), row.get("case"), row.get("seed")): index
        for index, row in enumerate(rows)
        if row.get("record_type") == "seed_claim"
    }
    generated_positions = {
        (row.get("n_index"), row.get("block"), row.get("case"), row.get("seed")): index
        for index, row in enumerate(rows)
        if row.get("record_type") == "sample_generated"
    }
    for row in claims:
        try:
            expected = _execution_seed(
                str(execution_profile),
                str(target),
                row["n_index"],
                row["block"],
                row["case"],
            )
        except (KeyError, TypeError, ValueError, RunnerProtocolError):
            global_invalid.append("malformed seed claim")
            break
        if (
            row.get("seed") != expected
            or row.get("seed_state") != "BURNED_ON_CLAIM_BEFORE_GENERATION"
        ):
            global_invalid.append("seed manifest mismatch")
            break
    if len(claims) < EXPECTED_CASES_PER_ARM or len(generated) < EXPECTED_CASES_PER_ARM:
        global_inconclusive.append("incomplete reserved batch")
    if len(claims) > EXPECTED_CASES_PER_ARM or len(generated) > EXPECTED_CASES_PER_ARM:
        global_invalid.append("excess reserved samples")
    if not generated_cells.issubset(claim_cells):
        global_invalid.append("sample generated without prior seed claim")
    if any(
        cell not in claim_positions
        or claim_positions[cell] >= generated_position
        for cell, generated_position in generated_positions.items()
    ):
        global_invalid.append("sample generation did not follow its durable seed claim")
    expected_seed_cells: set[tuple[int, int, int, int]] = set()
    try:
        expected_seed_cells = {
            (
                n_index,
                block,
                case,
                _execution_seed(
                    str(execution_profile), str(target), n_index, block, case
                ),
            )
            for n_index in range(len(CARDINALITIES))
            for block in range(BLOCKS_PER_TARGET)
            for case in range(CASES_PER_BLOCK)
        }
    except RunnerProtocolError:
        global_invalid.append("run_header has no registered seed manifest")
    if claim_cells - expected_seed_cells or generated_cells - expected_seed_cells:
        global_invalid.append("unregistered reserved cell")

    results: list[ArmSelectorVerdict] = []
    for name, parameters in evaluation_order():
        token = _selector_token(name, parameters)
        causets = [
            row
            for row in rows
            if row.get("record_type") == "causet_selector"
            and row.get("selector") == token
        ]
        block_pairs = [
            row
            for row in rows
            if row.get("record_type") == "block_pair" and row.get("selector") == token
        ]
        invalid = list(global_invalid)
        fail: list[str] = []
        inconclusive = list(global_inconclusive)
        for row in causets:
            if (
                row.get("selector_name") != name
                or row.get("parameters") != list(parameters)
                or not _registered_index(row.get("n_index"), len(CARDINALITIES))
                or row.get("n") != CARDINALITIES[row["n_index"]]
                or not _registered_index(row.get("block"), BLOCKS_PER_TARGET)
                or not _registered_index(row.get("case"), CASES_PER_BLOCK)
                or not isinstance(row.get("case_id"), str)
                or any(
                    not isinstance(row.get(flag), bool)
                    for flag in ("s1_pass", "s2_pass", "s3_pass", "s4_pass", "s6_pass")
                )
            ):
                invalid.append("causet-selector schema mismatch")
                continue
            selected = row.get("selected_pairs")
            domain = row.get("domain_pairs")
            numeric_fields = (
                "coverage",
                "normalization",
                "total_mass",
                "total_variation",
                "kish_ess",
                "ess_fraction",
            )
            if (
                not isinstance(selected, int)
                or isinstance(selected, bool)
                or not isinstance(domain, int)
                or isinstance(domain, bool)
                or selected < 0
                or domain <= 0
                or selected > domain
            ):
                invalid.append("malformed causet count schema")
                continue
            try:
                expected_seed = _execution_seed(
                    str(execution_profile),
                    str(target),
                    row["n_index"],
                    row["block"],
                    row["case"],
                )
            except RunnerProtocolError:
                invalid.append("causet-selector uses unregistered seed manifest")
                continue
            if row.get("seed") != expected_seed:
                invalid.append("causet-selector seed mismatch")
            if selected == 0:
                computed_s1 = False
                computed_s6 = False
            elif not all(_finite_number(row.get(field)) for field in numeric_fields):
                inconclusive.append("non-finite causet diagnostic")
                continue
            else:
                if row["coverage"] != selected / domain:
                    invalid.append("stored pure transform mismatch: coverage")
                if row["normalization"] != selected:
                    invalid.append("stored exact identity mismatch: normalization")
                if (
                    abs(row["ess_fraction"] - row["kish_ess"] / selected)
                    > MASS_TOLERANCE
                ):
                    invalid.append("dimensionless recomputation mismatch: ESS fraction")
                if abs(row["ess_fraction"] - 1.0) > MASS_TOLERANCE:
                    invalid.append("dimensionless phi=1 identity mismatch: ESS fraction")
                computed_s1 = selected >= MIN_SELECTED_PAIRS
                computed_s6 = bool(
                    row["coverage"] >= MIN_PAIR_COVERAGE
                    and row["normalization"] >= MIN_SELECTED_PAIRS
                    and row["kish_ess"] >= MIN_KISH_ESS
                    and row["ess_fraction"] >= MIN_ESS_FRACTION
                    and abs(row["total_mass"] - 1.0) <= MASS_TOLERANCE
                    and abs(row["total_variation"] - 1.0) <= MASS_TOLERANCE
                )
            if row.get("s1_pass") is not computed_s1 or row.get("s6_pass") is not computed_s6:
                invalid.append("stored S1/S6 flags disagree with diagnostics")
        for row in block_pairs:
            if (
                row.get("selector_name") != name
                or row.get("parameters") != list(parameters)
                or not _registered_index(row.get("n_index"), len(CARDINALITIES))
                or row.get("n") != CARDINALITIES[row["n_index"]]
                or not _registered_index(row.get("left_block"), BLOCKS_PER_TARGET)
                or not _registered_index(row.get("right_block"), BLOCKS_PER_TARGET)
                or row["left_block"] >= row["right_block"]
                or not isinstance(row.get("s5_pass"), bool)
            ):
                invalid.append("S5 block-pair schema mismatch")
                continue
            fields = ("d_mean", "signed_energy_u", "d_law")
            if not all(_finite_number(row.get(field)) for field in fields):
                inconclusive.append("non-finite S5 diagnostic")
                continue
            expected_d_law = float(np.sqrt(max(0.0, row["signed_energy_u"])))
            if (
                row["d_mean"] < 0.0
                or row["d_law"] < 0.0
                or row["d_law"] != expected_d_law
            ):
                invalid.append("stored pure transform mismatch: signed-U to d_law")
            computed_s5 = bool(
                row["d_mean"] <= MAX_MEAN_SIGNATURE_DISTANCE
                and row["d_law"] <= MAX_RANDOM_LAW_ENERGY_DISTANCE
            )
            if row.get("s5_pass") is not computed_s5:
                invalid.append("stored S5 flag disagrees with diagnostics")
        if any(not row.get("s2_pass") for row in causets):
            invalid.append("S2 relabel covariance failure")
        if any(not row.get("s3_pass") for row in causets):
            invalid.append("S3 sector-blind boundary failure")
        if any(not row.get("s4_pass") for row in causets):
            invalid.append("S4 payload/capacity/ledger failure")
        if any(not row.get("s1_pass") for row in causets):
            fail.append("S1 selected-pair floor")
        if any(not row.get("s6_pass") for row in causets):
            fail.append("S6 measure/coverage/ESS floor")
        if any(not row.get("s5_pass") for row in block_pairs):
            fail.append("S5 block-pair threshold")
        if len(causets) < EXPECTED_CASES_PER_ARM:
            inconclusive.append("missing causet-selector rows")
        elif len(causets) > EXPECTED_CASES_PER_ARM:
            invalid.append("excess causet-selector rows")
        causet_cells = {
            (row.get("n_index"), row.get("block"), row.get("case"))
            for row in causets
        }
        expected_causet_cells = {
            (n_index, block, case)
            for n_index in range(len(CARDINALITIES))
            for block in range(BLOCKS_PER_TARGET)
            for case in range(CASES_PER_BLOCK)
        }
        if len(causet_cells) != len(causets) or causet_cells - expected_causet_cells:
            invalid.append("duplicate or unregistered causet-selector cell")
        if len(block_pairs) < EXPECTED_BLOCK_PAIRS_PER_SELECTOR:
            inconclusive.append("missing S5 block-pair rows")
        elif len(block_pairs) > EXPECTED_BLOCK_PAIRS_PER_SELECTOR:
            invalid.append("excess S5 block-pair rows")
        block_cells = {
            (row.get("n_index"), row.get("left_block"), row.get("right_block"))
            for row in block_pairs
        }
        expected_block_cells = {
            (n_index, left, right)
            for n_index in range(len(CARDINALITIES))
            for left, right in combinations(range(BLOCKS_PER_TARGET), 2)
        }
        if len(block_cells) != len(block_pairs) or block_cells - expected_block_cells:
            invalid.append("duplicate or unregistered S5 block pair")
        if invalid:
            verdict = Verdict.PROTOCOL_INVALID
            reasons = tuple(sorted(set(invalid)))
        elif fail:
            verdict = Verdict.FAIL
            reasons = tuple(sorted(set(fail)))
        elif inconclusive:
            verdict = Verdict.INCONCLUSIVE
            reasons = tuple(sorted(set(inconclusive)))
        else:
            verdict = Verdict.PASS
            reasons = ("S1-S6 complete and passed",)
        results.append(
            ArmSelectorVerdict(str(target), name, parameters, verdict, reasons)
        )
    return ArmAdjudication(
        str(execution_profile), str(target), str(protocol_commit), tuple(results)
    )


def adjudicate_arm_ledger(path: str | Path) -> ArmAdjudication:
    records = read_ledger(path)
    expected_rows = [row for row in records if row.get("record_type") == "arm_selector_verdict"]
    completion_rows = [row for row in records if row.get("record_type") == "arm_complete"]
    result = adjudicate_arm_records(records)
    if expected_rows:
        if len(expected_rows) != CAPACITY_LIMIT or len(
            {row.get("selector") for row in expected_rows}
        ) != CAPACITY_LIMIT:
            raise LedgerValidationError("stored arm verdict schema is not one row per selector")
        for row in expected_rows:
            token = row.get("selector")
            matches = [
                value
                for value in result.selector_verdicts
                if _selector_token(value.selector_name, value.parameters) == token
            ]
            if (
                len(matches) != 1
                or row.get("target") != result.target
                or row.get("selector_name") != matches[0].selector_name
                or row.get("parameters") != list(matches[0].parameters)
                or not isinstance(row.get("reasons"), list)
            ):
                raise LedgerValidationError("stored arm verdict row violates schema")
        observed = {
            row.get("selector"): row.get("verdict") for row in expected_rows
        }
        calculated = {
            _selector_token(row.selector_name, row.parameters): row.verdict.value
            for row in result.selector_verdicts
        }
        if observed != calculated:
            raise LedgerValidationError("stored arm verdicts do not match adjudicator")
        if (
            len(completion_rows) != 1
            or completion_rows[0].get("target") != result.target
            or completion_rows[0].get("selector_verdict_count") != CAPACITY_LIMIT
        ):
            raise LedgerValidationError("completed arm ledger lacks one valid arm_complete row")
    elif completion_rows:
        raise LedgerValidationError("arm_complete exists without stored selector verdicts")
    return result


def _validate_categorical_arm(arm: ArmAdjudication) -> None:
    _header(arm.execution_profile, arm.target, arm.protocol_commit)
    if arm.execution_profile != REPLACEMENT_PROFILE:
        raise RunnerProtocolError("only replacement-reserved arms may be combined")
    expected = {
        _selector_token(name, parameters) for name, parameters in evaluation_order()
    }
    observed = [
        _selector_token(row.selector_name, row.parameters)
        for row in arm.selector_verdicts
    ]
    if len(observed) != CAPACITY_LIMIT or set(observed) != expected:
        raise RunnerProtocolError("arm verdict schema is not exactly one row per selector")
    if any(
        row.target != arm.target
        or not isinstance(row.verdict, Verdict)
        or not isinstance(row.reasons, tuple)
        or any(not isinstance(reason, str) for reason in row.reasons)
        for row in arm.selector_verdicts
    ):
        raise RunnerProtocolError("categorical arm row violates the frozen schema")


def combine_arm_adjudications(
    plus: ArmAdjudication, minus: ArmAdjudication
) -> tuple[CombinedSelectorVerdict, ...]:
    """Combine categorical verdicts only; no numeric cross-arm path exists."""
    _validate_categorical_arm(plus)
    _validate_categorical_arm(minus)
    arms = {plus.target: plus, minus.target: minus}
    if set(arms) != {"plus", "minus"}:
        raise RunnerProtocolError("combination requires one plus and one minus arm")
    plus_map = {
        _selector_token(row.selector_name, row.parameters): row
        for row in arms["plus"].selector_verdicts
    }
    minus_map = {
        _selector_token(row.selector_name, row.parameters): row
        for row in arms["minus"].selector_verdicts
    }
    expected = {_selector_token(name, parameters) for name, parameters in evaluation_order()}
    if set(plus_map) != expected or set(minus_map) != expected:
        raise RunnerProtocolError("arm verdict schema is incomplete")
    precedence = {
        Verdict.PASS: 0,
        Verdict.INCONCLUSIVE: 1,
        Verdict.FAIL: 2,
        Verdict.PROTOCOL_INVALID: 3,
    }
    combined: list[CombinedSelectorVerdict] = []
    for name, parameters in evaluation_order():
        token = _selector_token(name, parameters)
        rows = (plus_map[token], minus_map[token])
        verdict = max((row.verdict for row in rows), key=precedence.__getitem__)
        combined.append(
            CombinedSelectorVerdict(
                name,
                parameters,
                verdict,
                tuple((row.target, row.verdict.value) for row in rows),
            )
        )
    return tuple(combined)


def write_combined_ledger(
    path: str | Path,
    plus: ArmAdjudication,
    minus: ArmAdjudication,
) -> tuple[CombinedSelectorVerdict, ...]:
    combined = combine_arm_adjudications(plus, minus)
    with AppendOnlyLedger(
        path,
        {
            "schema_version": LEDGER_SCHEMA_VERSION,
            "protocol_tag": PROTOCOL_TAG,
            "protocol_commit": minus.protocol_commit,
            "arm_protocol_commits": [
                ["plus", plus.protocol_commit],
                ["minus", minus.protocol_commit],
            ],
            "execution_profile": REPLACEMENT_PROFILE,
            "target": "categorical-verdicts-only",
            "between_target_numeric_data": "ABSENT_BY_SCHEMA",
        },
    ) as ledger:
        for row in combined:
            ledger.append(
                "selector_verdict",
                selector_name=row.selector_name,
                parameters=list(row.parameters),
                verdict=row.verdict.value,
                arm_verdicts=[list(value) for value in row.arm_verdicts],
            )
    return combined


def _assert_execution_checkout(
    protocol_commit: str, ledger_path: str | Path
) -> Path:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True
    ).stdout.strip()
    origin_main = subprocess.run(
        ["git", "rev-parse", "refs/remotes/origin/main"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    dirty = subprocess.run(
        ["git", "status", "--porcelain"], check=True, capture_output=True, text=True
    ).stdout
    repo_root = Path(
        subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    ).resolve()
    output = Path(ledger_path).resolve()
    try:
        output.relative_to(repo_root)
    except ValueError:
        pass
    else:
        raise RunnerProtocolError("formal ledgers must be outside the git checkout")
    if head != protocol_commit or origin_main != protocol_commit or dirty:
        raise RunnerProtocolError(
            "formal execution requires clean HEAD == origin/main == protocol_commit"
        )
    return repo_root


def _main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run-arm")
    run_parser.add_argument("execution_profile", choices=EXECUTION_PROFILES)
    run_parser.add_argument("target", choices=tuple(TARGET_THETA))
    run_parser.add_argument("ledger")
    run_parser.add_argument("--protocol-commit", required=True)
    run_parser.add_argument("--prerequisite-ledger")
    combine_parser = subparsers.add_parser("combine")
    combine_parser.add_argument("plus_ledger")
    combine_parser.add_argument("minus_ledger")
    combine_parser.add_argument("output_ledger")
    args = parser.parse_args()
    if args.command == "run-arm":
        result = run_target_arm(
            execution_profile=args.execution_profile,
            target=args.target,
            ledger_path=args.ledger,
            protocol_commit=args.protocol_commit,
            prerequisite_ledger=args.prerequisite_ledger,
        )
        print(_canonical_json({
            "execution_profile": result.execution_profile,
            "target": result.target,
            "protocol_commit": result.protocol_commit,
            "verdicts": [
                {
                    "selector_name": row.selector_name,
                    "parameters": list(row.parameters),
                    "verdict": row.verdict.value,
                    "reasons": list(row.reasons),
                }
                for row in result.selector_verdicts
            ],
        }))
    else:
        plus = adjudicate_arm_ledger(args.plus_ledger)
        minus = adjudicate_arm_ledger(args.minus_ledger)
        combined = write_combined_ledger(args.output_ledger, plus, minus)
        print(_canonical_json({
            "protocol_commit": minus.protocol_commit,
            "arm_protocol_commits": [
                ["plus", plus.protocol_commit],
                ["minus", minus.protocol_commit],
            ],
            "verdicts": [
                {
                    "selector_name": row.selector_name,
                    "parameters": list(row.parameters),
                    "verdict": row.verdict.value,
                    "arm_verdicts": [list(value) for value in row.arm_verdicts],
                }
                for row in combined
            ],
        }))


if __name__ == "__main__":
    _main()


__all__ = [
    "DRESS_REHEARSAL_PROFILE",
    "DRESS_REHEARSAL_SEED_BASE",
    "EXECUTION_PROFILES",
    "EXPECTED_BLOCK_PAIRS_PER_SELECTOR",
    "EXPECTED_CASES_PER_ARM",
    "LEDGER_SCHEMA_VERSION",
    "PROTOCOL_TAG",
    "REPLACEMENT_PROFILE",
    "REPLACEMENT_SEED_BASES",
    "AppendOnlyLedger",
    "ArmAdjudication",
    "ArmSelectorVerdict",
    "CombinedSelectorVerdict",
    "LedgerValidationError",
    "RunnerProtocolError",
    "Verdict",
    "adjudicate_arm_ledger",
    "adjudicate_arm_records",
    "combine_arm_adjudications",
    "read_ledger",
    "run_target_arm",
    "write_combined_ledger",
]
