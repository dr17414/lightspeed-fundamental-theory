"""Reproducible deterministic development evidence; not screen authorization.

Run from the repository root with python -m benchmarks.stage5c_e4_v02_validation.
No generator, random stream, namespace, matching, or arm ledger is accessed.
Resource mode measures one repeated-atom input, never a 264-call screen.
"""

from __future__ import annotations

import argparse
from dataclasses import fields, is_dataclass
from enum import Enum
from hashlib import sha1
import json
from pathlib import Path
import resource
import sys
import time

import numpy as np
import scipy

from analysis import stage5c_e4_wellposedness as v01
from analysis import stage5c_e4_wellposedness_v02 as v02
from analysis.stage5c_e5_screen import _e4_deadline, MAX_CPU_SECONDS, MAX_RSS_BYTES
from analysis.stage5c_measure_prereg import normalised_weights, uniform_pair_weights


FIXTURES = {
    "gate_a": ([[.70, .70, .05, .05]], [1.0]),
    "near_zero": ([[.80, .80, .20, .20]], [1.0]),
    "wide_cell": ([[.55, .55, .45, .45]], [1.0]),
    "asymmetric": ([[.70, .30, .05, .20]], [1.0]),
    "leakage_invalid": ([[2e-200, 2e-200, 1e-200, 1e-200]], [1.0]),
    "interior": ([[.72, .81, .31, .22], [.61, .58, .24, .19],
                   [.43, .67, .11, .37]], [.2, .5, .3]),
    "boundary_contact": ([[.999, .999, .001, .001], [.5002, .7002, .5001, .7001]], [.5, .5]),
}


def payload(value):
    """Public numerical fields only, with exact binary64 hex strings."""
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {f.name: payload(getattr(value, f.name)) for f in fields(value)
                if not f.name.startswith("_")}
    if isinstance(value, np.ndarray):
        return payload(value.tolist())
    if isinstance(value, (list, tuple)):
        return [payload(v) for v in value]
    if isinstance(value, (float, np.floating)):
        return float(value).hex()
    if isinstance(value, complex):
        return {"real": value.real.hex(), "imag": value.imag.hex()}
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def source_blobs():
    root = Path(__file__).resolve().parents[1]
    paths = [*sorted((root / "analysis").glob("*.py")), Path(__file__).resolve()]
    result = {}
    for path in paths:
        data = path.read_bytes()
        result[str(path.relative_to(root))] = sha1(
            b"blob " + str(len(data)).encode() + b"\0" + data
        ).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("payload-diff", "resource"))
    parser.add_argument("--atoms", type=int, choices=(1, 3, 64, 2016, 4560, 8128), default=1)
    args = parser.parse_args()
    if sys.platform != "linux":
        parser.error("resource accounting requires Linux ru_maxrss units")
    resource.setrlimit(resource.RLIMIT_AS, (MAX_RSS_BYTES, MAX_RSS_BYTES))
    resource.setrlimit(resource.RLIMIT_CPU, (MAX_CPU_SECONDS, MAX_CPU_SECONDS))
    result = {
        "state": "DEVELOPMENT-EVIDENCE-NOT-RESOURCE-QUALIFICATION",
        "authorization": "NONE", "seed_or_generator_calls": 0,
        "python": sys.version, "numpy": np.__version__, "scipy": scipy.__version__,
        "source_blobs": source_blobs(),
    }
    if args.mode == "payload-diff":
        rows = []
        for name, (atoms, weights) in FIXTURES.items():
            for theta in ((-.4, 0.0, .4) if name == "interior" else (.4,)):
                row = {"fixture": name, "theta": theta}
                for label, producer in (("v0.1", v01), ("v0.2", v02)):
                    with _e4_deadline():
                        report = producer.evaluate_e4_wellposedness(np.array(atoms), np.array(weights), theta)
                    row[label] = payload(report)
                rows.append(row)
        result["rows"] = rows
    else:
        atoms = np.repeat(np.array(FIXTURES["gate_a"][0]), args.atoms, axis=0)
        weights, normalization = uniform_pair_weights(args.atoms)
        weights = normalised_weights(weights, normalization)
        wall_started, cpu_started = time.monotonic(), time.process_time()
        usage_started = resource.getrusage(resource.RUSAGE_SELF)
        with _e4_deadline():
            report = v02.evaluate_e4_wellposedness(atoms, weights, .4)
        cpu_seconds, wall_seconds = time.process_time() - cpu_started, time.monotonic() - wall_started
        usage_finished = resource.getrusage(resource.RUSAGE_SELF)
        rss_bytes = usage_finished.ru_maxrss * 1024
        result["probe"] = {
            "fixture": "repeated_gate_a_atom", "atoms": args.atoms,
            "cpu_seconds": cpu_seconds, "wall_seconds": wall_seconds,
            "process_peak_rss_bytes": rss_bytes,
            "getrusage_cpu_diagnostic_seconds": (
                usage_finished.ru_utime + usage_finished.ru_stime
                - usage_started.ru_utime - usage_started.ru_stime
            ),
            "cpu_clock": "time.process_time", "status": report.status.value,
            "reason": report.reason.value,
            "subdivisions": report.adaptive_run.subdivisions if report.adaptive_run else None,
            "within_observed_caps": cpu_seconds <= MAX_CPU_SECONDS and wall_seconds <= 900 and rss_bytes <= MAX_RSS_BYTES,
        }
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
