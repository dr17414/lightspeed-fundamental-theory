"""Review-gated deterministic development campaign; never a scientific screen.

No executable authorization is committed. Methods/fixtures may be verified now;
new timed jobs require a separate, explicitly approved, external review receipt.
"""
from __future__ import annotations
import argparse
import importlib.metadata
from hashlib import sha256
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time

from benchmarks import stage5c_e4_v02_resource_methods as methods
ROOT = methods.ROOT
MANIFEST = ROOT / "docs/stage5c_e4_v02_resource_measurement_manifest.json"
FIXTURES = ROOT / "docs/stage5c_e4_v02_resource_fixture_bytes.json"
REFERENCE = ROOT / "docs/stage5c_e4_v02_resource_method_reference.json"
THREAD_ENV = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
              "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS")


class ResourceNotAuthorized(RuntimeError):
    pass


def check_receipt(path, directory):
    if path is None:
        raise ResourceNotAuthorized("external exact-commit review receipt required")
    receipt_path, output = Path(path).resolve(), Path(directory).resolve()
    if receipt_path.is_relative_to(ROOT) or output.is_relative_to(ROOT):
        raise ResourceNotAuthorized("receipt/output must be outside the repository")
    receipt = json.loads(receipt_path.read_text())
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if (receipt.get("authorization") != "DETERMINISTIC-RESOURCE-DEVELOPMENT-ONLY"
            or receipt.get("reviewed_commit") != head
            or receipt.get("manifest_sha256") != sha256(MANIFEST.read_bytes()).hexdigest()
            or receipt.get("output_directory") != str(output)):
        raise ResourceNotAuthorized("review receipt mismatch")
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT):
        raise ResourceNotAuthorized("clean reviewed checkout required")
    return receipt


def check_runtime(manifest):
    # Called before numerical imports in both supervisor and workers.
    if sys.platform != "linux" or any(os.environ.get(k) != "1" for k in THREAD_ENV):
        raise RuntimeError("Linux and six thread env=1 pins required")
    profile = manifest["host"]
    if sys.version.split()[0] != profile["python"]:
        raise RuntimeError("campaign Python pin mismatch")
    if sys.version != profile["sys_version"]:
        raise RuntimeError("campaign Python build pin mismatch")
    for field, file in (("cgroup_cpu_max", "/sys/fs/cgroup/cpu.max"),
                        ("cgroup_memory_max", "/sys/fs/cgroup/memory.max")):
        if Path(file).read_text().strip() != profile[field]:
            raise RuntimeError("host/cgroup pin mismatch")
    model = next(line.split(":", 1)[1].strip() for line in Path("/proc/cpuinfo").read_text().splitlines()
                 if line.startswith("model name"))
    if model != profile["cpu_model"] or sorted(os.sched_getaffinity(0)) not in (profile["allowed_affinity"], [0]):
        raise RuntimeError("CPU/affinity pin mismatch")
    os.sched_setaffinity(0, {0})
    for path, expected in manifest["input_sha256"].items():
        if sha256((ROOT / path).read_bytes()).hexdigest() != expected:
            raise RuntimeError("input/source pin mismatch: " + path)


def memory_preflight():
    cgroup = int(Path("/sys/fs/cgroup/memory.max").read_text()) - int(Path("/sys/fs/cgroup/memory.current").read_text())
    available = int(next(line.split()[1] for line in Path("/proc/meminfo").read_text().splitlines()
                         if line.startswith("MemAvailable:"))) * 1024
    if min(cgroup, available) < 3 * 1024**3:
        raise RuntimeError("at least 3 GiB current host/cgroup memory headroom required")


def worker(job, fixtures):
    import numpy as np
    import scipy
    from threadpoolctl import threadpool_info
    from analysis import stage5c_e4_wellposedness_v02 as v02
    from analysis.stage5c_measure_prereg import uniform_pair_weights, normalised_weights
    from benchmarks.stage5c_e4_v02_resource_characterization import stress_integrand
    if np.__version__ != "2.3.5" or scipy.__version__ != "1.17.0":
        raise RuntimeError("numerical dependency pin mismatch")
    if importlib.metadata.version("threadpoolctl") != "3.6.0":
        raise RuntimeError("threadpoolctl pin mismatch")
    pools = threadpool_info()
    if not pools or any(p["num_threads"] != 1 for p in pools):
        raise RuntimeError("actual thread pools must all be one")
    if job["kind"] == "production":
        atoms, weights = methods.load_case(fixtures, job["case_index"])
        theta = float.fromhex(job["theta_hex"])
        action = lambda: v02.evaluate_e4_wellposedness(atoms, weights, theta)
    else:
        base = np.array([[float.fromhex(x) for x in row] for row in fixtures["stress"]["base_atoms_hex"]])
        atoms = base[np.arange(job["atoms"]) % 3]
        weights, normalization = uniform_pair_weights(len(atoms))
        weights = normalised_weights(weights, normalization)
        function = stress_integrand(atoms, weights, float.fromhex(fixtures["stress"]["theta_hex"]))
        action = lambda: scipy.integrate.cubature(function, np.zeros(3), np.ones(3), rule="genz-malik",
                                                  atol=0., rtol=0., max_subdivisions=job["s"], workers=1)
    started_cpu, started_wall = time.process_time(), time.monotonic()
    try:
        result = action()
    except v02.E4ProtocolError as exc:
        record = {"outcome": "PRODUCTION-PROTOCOL-ERROR", "error": str(exc), "subdivisions": None}
    else:
        if job["kind"] == "production":
            record = {"outcome": "PRODUCTION-REPORT", "status": result.status.value,
                      "reason": result.reason.value, "selected_count": len(atoms),
                      "subdivisions": None if result.adaptive_run is None else result.adaptive_run.subdivisions,
                      "adaptive_skipped": result.adaptive_run is None}
        else:
            if result.subdivisions != job["s"] or result.status == "converged":
                raise RuntimeError("forced-budget stress did not exhaust")
            record = {"outcome": "FORCED-BUDGET-EXHAUSTED", "subdivisions": result.subdivisions,
                      "production_report": False}
    record.update(phase_cpu_seconds=time.process_time()-started_cpu,
                  phase_wall_seconds=time.monotonic()-started_wall, threadpools=pools)
    return record


def run_campaign(receipt_path, output_directory):
    start_wall = time.monotonic()  # Includes receipt, preflight, method verification and all jobs.
    receipt = check_receipt(receipt_path, output_directory)  # No timed execution before this gate.
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    manifest = json.loads(MANIFEST.read_text())
    check_runtime(manifest)
    memory_preflight()
    # Methods checks precede the campaign clock. No new data can refit this reference.
    methods.verify_reference(methods.method_reference(), json.loads(REFERENCE.read_text()))
    fixtures = json.loads(FIXTURES.read_text())
    directory = Path(output_directory).resolve()
    directory.mkdir(parents=True, exist_ok=False)  # One attempt; no resume or overwrite.
    start_cpu = 0.0  # Whole supervisor process CPU, including imports/method verification.
    preflight_children = resource.getrusage(resource.RUSAGE_CHILDREN)
    children_cpu = preflight_children.ru_utime + preflight_children.ru_stime  # Includes preflight git commands.
    status = "PLAN-COMPLETE"
    with (directory / "records.jsonl").open("x") as stream:
        def emit(value):
            stream.write(json.dumps(value, sort_keys=True) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        emit({"state": "DEVELOPMENT-NOT-QUALIFICATION", "manifest_sha256": sha256(MANIFEST.read_bytes()).hexdigest(),
              "receipt": json.loads(Path(receipt_path).read_text()), "method_verified": True})
        for index, job in enumerate(manifest["jobs"]):
            # Reserve full parent CPU cap plus 2 s kernel/collection margin per admitted child.
            if children_cpu + job["cpu_cap"] + 2 + 120 > manifest["total_cpu_cap"]:
                status = "PLAN-CPU-BUDGET-INCOMPLETE"
                emit({"outcome": status, "not_run_ids": [x["id"] for x in manifest["jobs"][index:]]})
                break
            if time.monotonic()-start_wall >= manifest["total_wall_cap"]-5:
                status = "PLAN-WALL-BUDGET-INCOMPLETE"
                emit({"outcome": status, "not_run_ids": [x["id"] for x in manifest["jobs"][index:]]})
                break
            memory_preflight()
            emit({"job_id": job["id"], "outcome": "ATTEMPT-STARTED"})
            out, err = directory / (job["id"]+".json"), directory / (job["id"]+".stderr")
            with out.open("x") as stdout, err.open("x") as stderr:
                command = [sys.executable, "-m", "benchmarks.stage5c_e4_v02_resource_campaign", "worker", "--job", str(index)]
                environment = dict(os.environ, STAGE5C_RESOURCE_REVIEW_RECEIPT=str(Path(receipt_path).resolve()),
                                   STAGE5C_RESOURCE_OUTPUT_DIRECTORY=str(directory),
                                   STAGE5C_RESOURCE_PARENT_PID=str(os.getpid()),
                                   STAGE5C_RESOURCE_REVIEWED_COMMIT=receipt["reviewed_commit"],
                                   STAGE5C_RESOURCE_WALL_DEADLINE=str(min(time.monotonic()+job["wall_cap"],
                                                                       start_wall+manifest["total_wall_cap"]-5)))
                process = subprocess.Popen(command, cwd=ROOT, stdout=stdout, stderr=stderr, env=environment)
                began = time.monotonic()
                reason = None
                while True:
                    pid, wait_status, usage = os.wait4(process.pid, os.WNOHANG)
                    if pid:
                        process.returncode = os.waitstatus_to_exitcode(wait_status)
                        break
                    try:
                        rss = int(Path(f"/proc/{process.pid}/statm").read_text().split()[1]) * os.sysconf("SC_PAGE_SIZE")
                    except (FileNotFoundError, IndexError):
                        rss = 0
                    if rss > 2*1024**3 or rss + resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024 > 5*1024**3//2:
                        reason = "MEMORY-CAP-ABORT"
                    elif time.monotonic()-start_wall >= manifest["total_wall_cap"]-5:
                        reason = "PLAN-WALL-BUDGET-INCOMPLETE"
                    elif time.monotonic()-began >= job["wall_cap"]:
                        reason = "WALL-CAP-CENSORED"
                    if reason:
                        os.kill(process.pid, signal.SIGKILL)
                        _, wait_status, usage = os.wait4(process.pid, 0)
                        process.returncode = os.waitstatus_to_exitcode(wait_status)
                        break
                    time.sleep(.05)
            cpu = usage.ru_utime + usage.ru_stime
            children_cpu += cpu
            record = {"job_id": job["id"], "role": job["role"], "child_total_cpu_seconds": cpu,
                      "child_total_wall_seconds": time.monotonic()-began,
                      "child_peak_rss_bytes": usage.ru_maxrss*1024}
            if usage.ru_maxrss*1024 > 2*1024**3:
                reason = "MEMORY-CAP-ABORT"
            if reason:
                record.update(outcome=reason, phase_cpu_seconds=None, phase_wall_seconds=None,
                              phase_cost_bound="UNKNOWN; whole-child cost is not a phase lower bound")
            elif process.returncode == -signal.SIGALRM:
                record.update(outcome="WALL-CAP-CENSORED", phase_cpu_seconds=None, phase_wall_seconds=None)
            elif process.returncode == -signal.SIGXCPU:
                record.update(outcome="CPU-CAP-CENSORED", phase_cpu_seconds=None, phase_wall_seconds=None)
            elif process.returncode != 0:
                record.update(outcome="IMPLEMENTATION-ABORT", exit_code=process.returncode)
                reason = "IMPLEMENTATION-ABORT"
            else:
                record.update(json.loads(out.read_text()))
            emit(record)
            if reason in ("MEMORY-CAP-ABORT", "IMPLEMENTATION-ABORT", "PLAN-WALL-BUDGET-INCOMPLETE"):
                status = reason
                emit({"outcome": "NOT-RUN", "not_run_ids": [x["id"] for x in manifest["jobs"][index+1:]]})
                break
        emit({"outcome": status, "plan_wall_seconds": time.monotonic()-start_wall,
              "parent_cpu_seconds": time.process_time()-start_cpu, "children_cpu_seconds": children_cpu,
              "total_accounted_cpu_seconds": time.process_time()-start_cpu+children_cpu,
              "production_schedule_cpu_bound": False})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("run", "worker"))
    parser.add_argument("--authorization")
    parser.add_argument("--output")
    parser.add_argument("--job", type=int)
    args = parser.parse_args()
    if args.mode == "run":
        run_campaign(args.authorization, args.output)
    else:
        # Internal worker requires the supervisor's reviewed receipt too.
        receipt_path = os.environ.get("STAGE5C_RESOURCE_REVIEW_RECEIPT")
        directory = os.environ.get("STAGE5C_RESOURCE_OUTPUT_DIRECTORY")
        if str(os.getppid()) != os.environ.get("STAGE5C_RESOURCE_PARENT_PID"):
            raise ResourceNotAuthorized("internal supervisor parent required")
        if receipt_path is None or directory is None:
            raise ResourceNotAuthorized("inherited review receipt required")
        receipt = json.loads(Path(receipt_path).read_text())
        if (receipt.get("authorization") != "DETERMINISTIC-RESOURCE-DEVELOPMENT-ONLY"
                or receipt.get("reviewed_commit") != os.environ.get("STAGE5C_RESOURCE_REVIEWED_COMMIT")
                or receipt.get("manifest_sha256") != sha256(MANIFEST.read_bytes()).hexdigest()
                or receipt.get("output_directory") != str(Path(directory).resolve())):
            raise ResourceNotAuthorized("inherited review receipt mismatch")
        # No git/subprocess in the worker: supervisor checked the reviewed checkout;
        # check_runtime below independently verifies every source/input byte pin.
        manifest = json.loads(MANIFEST.read_text())
        check_runtime(manifest)
        if args.job is None or not 0 <= args.job < len(manifest["jobs"]):
            raise ResourceNotAuthorized("internal job index required")
        job = manifest["jobs"][args.job]
        resource.setrlimit(resource.RLIMIT_CPU, (job["cpu_cap"], job["cpu_cap"]+1))
        resource.setrlimit(resource.RLIMIT_AS, (32*1024**3, 32*1024**3))
        remaining = float(os.environ["STAGE5C_RESOURCE_WALL_DEADLINE"]) - time.monotonic()
        if remaining <= 0:
            raise RuntimeError("internal wall deadline already exhausted")
        signal.signal(signal.SIGALRM, signal.SIG_DFL)
        signal.alarm(max(1, int(remaining)))
        print(json.dumps(worker(job, json.loads(FIXTURES.read_text()))))


if __name__ == "__main__":
    main()
