"""Deterministic resource characterization, never a screen or qualification.

Require single-thread environment variables before importing numerical code.
Adaptive stress transcribes the production integrand but forces zero solver
tolerances. It measures a fixed subdivision budget, not a v0.2 report or a
reachable production exhaustion event. No producer globals are modified.
"""

from __future__ import annotations

import argparse
from hashlib import sha1
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time


THREAD_ENV = (
    "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
    "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS",
)
N_VALUES = (64, 96, 128)
ATOMS = (252, 1008, 2016, 4560, 8128)
SUBDIVISION_BUDGETS = (128, 256, 512, 1024, 2048, 4096)
DEFAULT_PROBES = (
    ("enclosure", 2016, None), ("enclosure", 4560, None), ("enclosure", 8128, None),
    ("adaptive_stress", 252, 4096), ("adaptive_stress", 1008, 4096),
    ("adaptive_stress", 2016, 256), ("adaptive_stress", 4560, 256),
    ("adaptive_stress", 8128, 256), ("adaptive_stress", 8128, 512),
)


def check_thread_environment():
    wrong = {name: os.environ.get(name) for name in THREAD_ENV if os.environ.get(name) != "1"}
    if wrong:
        raise RuntimeError(f"set all thread pins to 1 before numerical imports: {wrong}")


def pin_one_cpu():
    allowed = sorted(os.sched_getaffinity(0))
    os.sched_setaffinity(0, {allowed[0]})
    return allowed


def source_blobs():
    root = Path(__file__).resolve().parents[1]
    paths = [*sorted((root / "analysis").glob("*.py")), Path(__file__).resolve()]
    return {
        str(path.relative_to(root)): sha1(
            b"blob " + str(path.stat().st_size).encode() + b"\0" + path.read_bytes()
        ).hexdigest()
        for path in paths
    }


def metadata():
    def read_optional(path):
        try:
            return Path(path).read_text().strip()
        except OSError:
            return None
    return {
        "state": "CHARACTERIZATION-NOT-QUALIFICATION", "authorization": "NONE",
        "seed_or_generator_calls": 0, "python": sys.version,
        "versions": {name: importlib.metadata.version(name)
                     for name in ("numpy", "scipy", "threadpoolctl")},
        "thread_environment": {name: os.environ.get(name) for name in THREAD_ENV},
        "affinity": sorted(os.sched_getaffinity(0)), "platform": platform.platform(),
        "cpu_model": next((line.split(":", 1)[1].strip()
                           for line in Path("/proc/cpuinfo").read_text().splitlines()
                           if line.startswith("model name")), None),
        "cgroup_cpu_max": read_optional("/sys/fs/cgroup/cpu.max"),
        "cgroup_memory_max": read_optional("/sys/fs/cgroup/memory.max"),
        "source_blobs": source_blobs(),
    }


def geometry_fixtures(n):
    import numpy as np

    def layers(sizes):
        result = []
        for index, size in enumerate(sizes):
            low, high = (index + .1) / len(sizes), (index + .9) / len(sizes)
            u = np.linspace(low, high, size) if size > 1 else np.array([(low + high) / 2])
            result.append(np.column_stack((u, low + high - u)))
        return np.vstack(result)

    rank = np.arange(n)
    axis = (rank + .5) / n
    bits = (n - 1).bit_length()
    reverse = np.array([int(f"{int(i):0{bits}b}"[::-1], 2) for i in rank])
    result = {
        "chain": np.column_stack((axis, axis)),
        "antichain": np.column_stack((axis, axis[::-1])),
        "two_layers": layers((n // 2, n - n // 2)),
        "four_layers": layers((n // 4,) * 4),
        "bit_reversal": np.column_stack((axis, (reverse + .5) / 2**bits)),
    }
    for multiplier in (5, 17, 31):
        result[f"modular_{multiplier}"] = np.column_stack((axis, ((rank * multiplier) % n + .5) / n))
    for middle in range(1, 5):
        first = (n - middle) // 2
        result[f"interval_bridge_{middle}"] = layers((first, middle, n - middle - first))
    return result


def selector_counts():
    from analysis.stage5c_hard_controls import BlindedCase, order_from_uv
    from analysis.stage5c_selector_family import (
        SelectorDomainError, SelectorSelectionError, apply_selector, evaluation_order,
    )
    rows = []
    for n in N_VALUES:
        for fixture, points in geometry_fixtures(n).items():
            case = BlindedCase("DEVELOPMENT-ONLY-COUNT", order_from_uv(points))
            for name, parameters in evaluation_order():
                try:
                    count = len(apply_selector(name, parameters, case))
                    category = "SELECTED"
                except SelectorDomainError:
                    count, category = 0, "DOMAIN-EMPTY"
                except SelectorSelectionError:
                    count, category = 0, "SELECTION-EMPTY"
                rows.append({"N": n, "fixture": fixture, "selector": name,
                             "parameters": list(parameters), "selected_pairs": count,
                             "category": category})
    return rows


def stress_integrand(atoms, weights, theta):
    """Exact production primitive transcription; parity is tested separately."""
    import numpy as np
    from analysis.stage5c_continuum_pairing import conformal_volume_density
    from analysis.stage5c_e4_wellposedness import _mixture_density
    density = _mixture_density(atoms, weights)

    def integrand(cube_points):
        a, s, transverse = np.asarray(cube_points, dtype=float).T
        right_points = np.stack((a, transverse, a * s, transverse), axis=-1)
        left_points = np.stack((transverse, a, transverse, a * s), axis=-1)

        def entry(points):
            px = conformal_volume_density(points[:, 0], points[:, 1], theta)
            py = conformal_volume_density(points[:, 2], points[:, 3], theta)
            biweight = np.asarray(px * py, dtype=float) ** -.25
            return a * biweight * density(points)

        right, left = entry(right_points), entry(left_points)
        zeros = np.zeros_like(right)
        return np.stack((right, zeros, left, zeros), axis=-1)
    return integrand


def run_probe(stage, count, budget):
    import numpy as np
    from scipy import integrate
    from threadpoolctl import threadpool_info
    from analysis import stage5c_e4_wellposedness_v02 as v02
    from analysis.stage5c_e5_screen import _e4_deadline
    from analysis.stage5c_measure_prereg import normalised_weights, uniform_pair_weights

    pools = threadpool_info()
    if not pools or any(pool["num_threads"] != 1 for pool in pools):
        raise RuntimeError(f"numerical thread pools do not match qualification pin: {pools}")
    base = np.array([[.72, .81, .31, .22], [.61, .58, .24, .19], [.43, .67, .11, .37]])
    atoms = base[np.arange(count) % 3]
    weights, normalization = uniform_pair_weights(count)
    weights = normalised_weights(weights, normalization)
    atoms, weights = v02._validated_mixture(atoms, weights)
    function = stress_integrand(atoms, weights, .4) if stage == "adaptive_stress" else None
    cpu_started, wall_started = time.process_time(), time.monotonic()
    record = {"stage": stage, "atoms": count, "fixture": "cyclic_three_atom_interior",
              "subdivision_budget": budget, "threadpools": pools, "cpu_clock": "time.process_time",
              "scope": "phase only, excludes imports/setup and other E4/schedule costs"}
    try:
        with _e4_deadline():
            if stage == "enclosure":
                result = v02.pairing_enclosure(atoms, weights, .4)
                record.update(outcome="COMPLETED", levels=list(result.levels))
            else:
                result = integrate.cubature(function, np.zeros(3), np.ones(3), rule="genz-malik",
                                            atol=0.0, rtol=0.0, max_subdivisions=budget, workers=1)
                if result.subdivisions != budget or result.status == "converged":
                    raise RuntimeError("stress did not exhaust the specified subdivision budget")
                record.update(outcome="FORCED-BUDGET-EXHAUSTED", subdivisions=int(result.subdivisions),
                              solver_status=str(result.status), stress_atol=0.0, stress_rtol=0.0,
                              production_report=False)
    except TimeoutError:
        record.update(outcome="WALL-CAP-TIMEOUT", subdivisions=None, production_report=False)
    record.update(cpu_seconds=time.process_time() - cpu_started,
                  wall_seconds=time.monotonic() - wall_started,
                  process_peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("selector-counts", "probe", "suite"))
    parser.add_argument("--stage", choices=("enclosure", "adaptive_stress"), default="enclosure")
    parser.add_argument("--atoms", type=int, choices=ATOMS, default=2016)
    parser.add_argument("--subdivisions", type=int, choices=SUBDIVISION_BUDGETS, default=256)
    args = parser.parse_args()
    if sys.platform != "linux":
        parser.error("Linux affinity/resource units are required")
    check_thread_environment()
    allowed = pin_one_cpu()
    resource.setrlimit(resource.RLIMIT_AS, (32 * 1024**3, 32 * 1024**3))
    resource.setrlimit(resource.RLIMIT_CPU, (57600, 57600))
    common = metadata()
    common["allowed_affinity_before_pin"] = allowed
    if args.mode == "selector-counts":
        print(json.dumps({**common, "selector_count_rows": selector_counts()}, indent=2))
    elif args.mode == "probe":
        budget = args.subdivisions if args.stage == "adaptive_stress" else None
        print(json.dumps({**common, "probe": run_probe(args.stage, args.atoms, budget)}, indent=2))
    else:
        # Fresh process per phase: ru_maxrss is never inherited across probes.
        # Emit each completed result immediately so an interrupted suite retains it.
        print(json.dumps({"suite_environment": common, "probe_plan": DEFAULT_PROBES}), flush=True)
        for stage, count, budget in DEFAULT_PROBES:
            command = [sys.executable, "-m", "benchmarks.stage5c_e4_v02_resource_characterization",
                       "probe", "--stage", stage, "--atoms", str(count)]
            if budget is not None:
                command += ["--subdivisions", str(budget)]
            completed = subprocess.run(command, check=True, capture_output=True, text=True)
            print(json.dumps(json.loads(completed.stdout)), flush=True)


if __name__ == "__main__":
    main()
