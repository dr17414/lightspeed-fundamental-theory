"""Audit-only frozen-E4 screen. Importing this module never generates inputs.

The execution entrypoint stays locked until a separately reviewed, committed
authorization artifact is present on clean main. This is not a 6a-E arm runner.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from fractions import Fraction
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time
from typing import Iterator

import numpy as np
import scipy

from analysis.stage5c_e4_wellposedness import E4ProtocolError, evaluate_e4_wellposedness
from analysis.stage5c_hard_controls import BlindedCase, sprinkle_control
from analysis.stage5c_measure_prereg import normalised_weights, uniform_pair_weights
from analysis.stage5c_selector_family import (
    SelectorDomainError,
    SelectorProtocolError,
    SelectorSelectionError,
    apply_selector,
    evaluation_order,
)


N_VALUES = (64, 96, 128)
THETA_VALUES = (-0.4, 0.4)
REPETITIONS = 4
SEED_BASE = 6_000_000_000
SEED_LAST = SEED_BASE + 23
MAX_CPU_SECONDS = 16 * 3600
MAX_E4_WALL_SECONDS = 900
MAX_RSS_BYTES = 32 * 1024**3
AUTHORIZATION = "docs/stage5c_e5_screen_authorization.json"  # deliberately absent
ATTESTATION = "docs/stage5c_e5_screen_attestation.json"  # committed after any attempt
PROTOCOL = "docs/STAGE5C_6A_E_FROZEN_E4_SCREEN_PROTOCOL_DRAFT.md"
RUNNER = "analysis/stage5c_e5_screen.py"
FROZEN_BLOBS = {
    "analysis/stage5c_hard_controls.py": "32f593c0b710b4c591fb7746c7014d72784da554",
    "analysis/stage5c_selector_family.py": "9b9bb5497e0dc432eb63939b47bede0070bd8120",
    "analysis/stage5c_measure_prereg.py": "0b05b1fc913da77b4f1824fbf7901c52734efc19",
    "analysis/stage5c_e4_wellposedness.py": "a96d368f75b03b1fc0317cb20dd34dfd9de2f581",
    "analysis/stage5c_continuum_pairing.py": "8b32a3cf7a8ef23e5abae1e397f179c18ef3711e",
    "analysis/stage5c_numerical_certification.py": "deae60470abfddf2d636a4b3fd9160bbfebccc91",
    "analysis/stage5c_primary_invariant.py": "6756fd1dae86065fc209b99a4b8cedb57efdaaac",
    "docs/stage5c_6a_s_burn_registry.json": "74a0299fd251e598beb34293c2f9b0880c2b3368",
}
CATEGORIES = (
    "SELECTOR-OR-ATOM-INVALID",
    "E4-OR-ITEM3-NONCLEAN",
    "CLEAN-LOW",
    "CLEAN-MID",
    "CLEAN-NEAR",
    "CLEAN-OVER",
)


class ScreenNotAuthorized(RuntimeError):
    """Any missing approval, provenance, runtime, or custody check blocks RNG."""


class ScreenIntegrityFailure(RuntimeError):
    """Runner count invariants failed after the one-shot burn-log claim."""


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ("git", *args), cwd=root, check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def _check_single_use(root: Path, auth: dict, burn_path: Path, report_path: Path) -> None:
    # Both paths are part of the committed authorization. A second invocation
    # cannot choose fresh filenames while the first attempt awaits attestation.
    if os.path.lexists(root / ATTESTATION):
        raise ScreenNotAuthorized("screen already executed; seeds are burned")
    output_paths = auth.get("output_paths")
    if not isinstance(output_paths, dict) or set(output_paths) != {"burn_log", "report"}:
        raise ScreenNotAuthorized("authorization must pin both output paths")
    for label, actual in (("burn_log", burn_path), ("report", report_path)):
        declared = output_paths[label]
        if (not isinstance(declared, str) or not Path(declared).is_absolute()
                or Path(declared).resolve() != Path(declared)
                or actual != Path(declared)):
            raise ScreenNotAuthorized("audit output path differs from authorization")
        if os.path.lexists(actual):
            raise ScreenNotAuthorized("audit output already claimed; seeds are burned")


def _preflight(root: Path, burn_path: Path, report_path: Path) -> dict:
    auth_path = root / AUTHORIZATION
    if not auth_path.is_file():
        raise ScreenNotAuthorized("reviewed screen authorization is absent")
    try:
        if _git(root, "branch", "--show-current") != "main":
            raise ScreenNotAuthorized("screen requires committed main")
        if _git(root, "status", "--porcelain"):
            raise ScreenNotAuthorized("screen requires a clean checkout")
        if _git(root, "ls-files", "--error-unmatch", AUTHORIZATION) != AUTHORIZATION:
            raise ScreenNotAuthorized("authorization must be committed")
        auth = json.loads(auth_path.read_text(encoding="utf-8"))
        if auth.get("state") != "AUTHORIZED":
            raise ScreenNotAuthorized("screen authorization is not active")
        _check_single_use(root, auth, burn_path, report_path)
        expected = auth.get("blob_shas", {})
        if set(expected) != {RUNNER, PROTOCOL, *FROZEN_BLOBS}:
            raise ScreenNotAuthorized("authorization must pin runner, protocol, and frozen sources")
        for path, sha in expected.items():
            if sha != _git(root, "rev-parse", f"HEAD:{path}") or (
                path in FROZEN_BLOBS and sha != FROZEN_BLOBS[path]
            ):
                raise ScreenNotAuthorized(f"source blob changed: {path}")
        if tuple(auth.get("seed_range", ())) != (SEED_BASE, SEED_LAST):
            raise ScreenNotAuthorized("diagnostic seed range changed")
        if auth.get("resource_limits") != {
            "cpu_seconds": MAX_CPU_SECONDS,
            "e4_wall_seconds": MAX_E4_WALL_SECONDS,
            "rss_bytes": MAX_RSS_BYTES,
        }:
            raise ScreenNotAuthorized("resource caps changed")
        if auth.get("sys_version") != sys.version or (
            sys.version_info[:3] != (3, 12, 13)
            or np.__version__ != "2.3.5"
            or scipy.__version__ != "1.17.0"
        ):
            raise ScreenNotAuthorized("runtime identity changed")
        registry = json.loads(
            (root / "docs/stage5c_6a_s_burn_registry.json").read_text(encoding="utf-8")
        )
        # Frozen 6a-S manifest's maximal offset, including N/block/case indices.
        for entry in registry["entries"]:
            base = entry["seed_base"]
            if not (base + 2_030_063 < SEED_BASE or base > SEED_LAST):
                raise ScreenNotAuthorized("diagnostic namespace overlaps burned 6a-S")
        if len(evaluation_order()) != 11:
            raise ScreenNotAuthorized("selector family capacity changed")
        for path in (burn_path, report_path):
            if path.exists() or root in path.resolve().parents or path.resolve() == root:
                raise ScreenNotAuthorized("audit outputs must be fresh and outside repo")
            if not path.parent.is_dir():
                raise ScreenNotAuthorized("audit output directory is missing")
        if burn_path.resolve() == report_path.resolve():
            raise ScreenNotAuthorized("burn and report outputs must be separate")
        # Use an enforceable address-space cap; a lower existing hard cap is fine.
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        cap = min(MAX_RSS_BYTES, hard) if hard != resource.RLIM_INFINITY else MAX_RSS_BYTES
        if cap <= 0:
            raise ScreenNotAuthorized("address-space cap is unavailable")
        resource.setrlimit(resource.RLIMIT_AS, (cap, hard))
        if resource.getrlimit(resource.RLIMIT_AS)[0] > MAX_RSS_BYTES:
            raise ScreenNotAuthorized("memory limit not enforced")
        return {"main_commit": _git(root, "rev-parse", "HEAD"), "auth": auth}
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        raise ScreenNotAuthorized("preflight failed before any generator call") from exc


def _category(error: np.ndarray | None, *, clean: bool) -> str:
    """Classify a CLEAN raw error using exact binary64 rational comparisons."""
    if not clean or error is None:
        return "E4-OR-ITEM3-NONCLEAN"
    value = np.asarray(error, dtype=float)
    if value.shape != (2,) or not np.all(np.isfinite(value)) or np.any(value < 0):
        return "E4-OR-ITEM3-NONCLEAN"
    magnitude = max(Fraction.from_float(float(value[0])) / 3,
                    Fraction.from_float(float(value[1])))
    if magnitude < Fraction(1, 160):
        return "CLEAN-LOW"
    if magnitude < Fraction(1, 80):
        return "CLEAN-MID"
    if magnitude < Fraction(1, 40):
        return "CLEAN-NEAR"
    return "CLEAN-OVER"


def _one_member(sample: object, name: str, parameters: tuple) -> str:
    # The selector sees the order and a constant case id, never target/coordinates.
    try:
        case = BlindedCase(case_id="AUDIT-ONLY", order=sample.order)
        pairs = apply_selector(name, parameters, case)
        atoms = np.concatenate(
            (sample.coordinates[pairs[:, 0]], sample.coordinates[pairs[:, 1]]),
            axis=1,
        )
        weights, normalization = uniform_pair_weights(len(pairs))
        probability_weights = normalised_weights(weights, normalization)
        with _e4_deadline():
            report = evaluate_e4_wellposedness(atoms, probability_weights, sample.theta)
    except (SelectorDomainError, SelectorSelectionError, SelectorProtocolError,
            E4ProtocolError, IndexError, ValueError):
        # Only known schema/atom violations are counted as invalid.
        return "SELECTOR-OR-ATOM-INVALID"
    return _category(report.certification.endpoint_error, clean=report.clean)


@contextmanager
def _e4_deadline() -> Iterator[None]:
    if not hasattr(signal, "SIGALRM"):
        raise ScreenNotAuthorized("hard per-E4 wall clock enforcement unavailable")
    def expired(_signum: int, _frame: object) -> None:
        raise TimeoutError("E4 wall clock cap")
    old_handler = signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, MAX_E4_WALL_SECONDS)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old_handler)


def _burn(fd: int, n: int, theta: float, repetition: int, seed: int) -> None:
    line = json.dumps({"N": n, "theta": theta, "rep": repetition, "seed": seed},
                      separators=(",", ":"), sort_keys=True) + "\n"
    os.write(fd, line.encode("utf-8"))
    os.fsync(fd)  # durable claim precedes the generator


def _sync_directory(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _write_once(path: Path, report: dict) -> None:
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        payload = json.dumps(report, sort_keys=True, ensure_ascii=False).encode("utf-8")
        os.write(fd, payload + b"\n")
        os.fsync(fd)
    finally:
        os.close(fd)


def run_screen(root: Path, burn_path: Path, report_path: Path) -> dict:
    """Run only after a separate main-committed authorization passes preflight."""
    root, burn_path, report_path = root.resolve(), burn_path.resolve(), report_path.resolve()
    identity = _preflight(root, burn_path, report_path)
    started = time.monotonic()
    cpu_started = time.process_time()
    counts = {
        f"j={j},N={n},theta={theta:+.1f}": {category: 0 for category in CATEGORIES}
        for n in N_VALUES for theta in THETA_VALUES
        for j in range(1, len(evaluation_order()) + 1)
    }
    calls = 0
    fd = os.open(burn_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        try:
            # Persist the new burn-log directory entry before the first seed.
            _sync_directory(burn_path.parent)
            for i, n in enumerate(N_VALUES):
                for t, theta in enumerate(THETA_VALUES):
                    for repetition in range(REPETITIONS):
                        seed = SEED_BASE + 8 * i + 4 * t + repetition
                        _burn(fd, n, theta, repetition, seed)
                        sample = sprinkle_control(n, theta, seed)
                        for j, (name, params) in enumerate(evaluation_order(), 1):
                            key = f"j={j},N={n},theta={theta:+.1f}"
                            category = _one_member(sample, name, params)
                            if category not in CATEGORIES:
                                raise ScreenIntegrityFailure("unknown screen count category")
                            counts[key][category] += 1
                            calls += 1
                            if (time.process_time() - cpu_started > MAX_CPU_SECONDS
                                    or resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                                    * 1024 > MAX_RSS_BYTES):
                                raise TimeoutError("audit resource cap")
            if calls != 264 or any(sum(row.values()) != 4 for row in counts.values()):
                raise ScreenIntegrityFailure("screen count integrity failure")
            status = ("SCREEN-OBSTRUCTION" if any(
                row["SELECTOR-OR-ATOM-INVALID"] or row["E4-OR-ITEM3-NONCLEAN"]
                or row["CLEAN-OVER"] for row in counts.values()
            ) else "SCREEN-NO-OBSTRUCTION")
            result = {"status": status, "counts": counts}
        except ScreenIntegrityFailure:
            result = {"status": "SCREEN-INTEGRITY-FAILURE"}
        except BaseException:
            # No partial row counts or raw numerical payload are published.
            result = {"status": "SCREEN-INCOMPLETE"}
        result.update({
            "calls": calls, "source_main": identity["main_commit"],
            "sys_version": sys.version, "numpy": np.__version__, "scipy": scipy.__version__,
            "cpu_seconds": time.process_time() - cpu_started,
            "wall_seconds": time.monotonic() - started,
            "rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
        })
        _write_once(report_path, result)
        return result
    finally:
        os.close(fd)


def main() -> None:
    parser = argparse.ArgumentParser(description="Approved audit-only E4 screen")
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--burn-log", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    result = run_screen(args.repo, args.burn_log, args.report)
    if result["status"] in {"SCREEN-INCOMPLETE", "SCREEN-INTEGRITY-FAILURE"}:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
