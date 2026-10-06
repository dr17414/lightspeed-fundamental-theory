"""Review-gated deterministic development campaign; never a scientific screen.

No executable authorization is committed. Methods/fixtures may be verified now;
new timed jobs require a separate, explicitly approved, external review receipt.
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
import ctypes
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


def check_runtime(manifest, *, role="supervisor"):
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
    affinity = profile[role + "_affinity"]
    if model != profile["cpu_model"] or sorted(os.sched_getaffinity(0)) not in (
            profile["allowed_affinity"], profile["supervisor_affinity"], affinity):
        raise RuntimeError("CPU/affinity pin mismatch")
    os.sched_setaffinity(0, set(affinity))
    for path, expected in manifest["input_sha256"].items():
        if sha256((ROOT / path).read_bytes()).hexdigest() != expected:
            raise RuntimeError("input/source pin mismatch: " + path)


def memory_preflight():
    cgroup = int(Path("/sys/fs/cgroup/memory.max").read_text()) - int(Path("/sys/fs/cgroup/memory.current").read_text())
    available = int(next(line.split()[1] for line in Path("/proc/meminfo").read_text().splitlines()
                         if line.startswith("MemAvailable:"))) * 1024
    if min(cgroup, available) < 3 * 1024**3:
        raise RuntimeError("at least 3 GiB current host/cgroup memory headroom required")
    return {"cgroup_remaining_bytes": cgroup, "host_available_bytes": available}


class E4WallExpired(TimeoutError):
    pass


@contextmanager
def e4_deadline(seconds):
    """Same evaluate-only ITIMER_REAL scope as production; no whole-child alarm."""
    def expired(_signum, _frame):
        raise E4WallExpired("E4 evaluate wall cap")
    old_handler = signal.signal(signal.SIGALRM, expired)
    if signal.getitimer(signal.ITIMER_REAL) != (0.0, 0.0):
        signal.signal(signal.SIGALRM, old_handler)
        raise RuntimeError("worker already owns a real-time timer")
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old_handler)


def supervisor_limits(manifest):
    soft = manifest["supervisor_cpu_soft_cap"]
    hard = max(soft + 1, max(j["cpu_cap"] + 1 for j in manifest["jobs"]))
    # Children inherit a high hard limit, then lower it to their own cap+1.
    stop = {"expired": False}
    def expired(_signum, _frame):
        stop["expired"] = True
        signal.signal(signal.SIGXCPU, signal.SIG_IGN)
    stop["old_handler"] = signal.signal(signal.SIGXCPU, expired)
    try:
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        resource.setrlimit(resource.RLIMIT_CPU, (soft, hard))
    except BaseException:
        signal.signal(signal.SIGXCPU, stop["old_handler"])
        raise
    return stop


def worker_limits(job, *, address_space_cap=32*1024**3):
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    signal.signal(signal.SIGXCPU, signal.SIG_DFL)
    resource.setrlimit(resource.RLIMIT_CPU, (job["cpu_cap"], job["cpu_cap"]+1))
    resource.setrlimit(resource.RLIMIT_AS, (address_space_cap, address_space_cap))


def parent_death_guard(expected_parent):
    # Linux PR_SET_PDEATHSIG replaces the competing whole-child SIGALRM timer.
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(1, signal.SIGKILL, 0, 0, 0) != 0:
        raise OSError(ctypes.get_errno(), "PR_SET_PDEATHSIG failed")
    if os.getppid() != expected_parent:
        raise ResourceNotAuthorized("supervisor died before worker guard")


def announce_worker_identity():
    fields = Path('/proc/self/stat').read_text().rsplit(')', 1)[1].split()
    print(json.dumps({'event': 'WORKER-READY', 'namespace_pid': os.getpid(),
                      'proc_pid': int(os.readlink('/proc/self')), 'start_ticks': int(fields[19])}),
          file=sys.stderr, flush=True)


def read_worker_identity(path, pid):
    if path is None:
        return None
    for line in path.read_text().splitlines():
        try:
            value = json.loads(line)
        except ValueError:
            continue
        if value.get('event') == 'WORKER-READY' and value.get('namespace_pid') == pid:
            return value
    return None


def read_live_sample(pid, identity):
    # Take time BEFORE reading: a successfully read live process existed at this time.
    stamp = time.monotonic()
    if identity is None or identity['namespace_pid'] != pid:
        return None
    try:
        fields = Path(f"/proc/{identity['proc_pid']}/stat").read_text().rsplit(")", 1)[1].split()
        if fields[0] == "Z" or int(fields[19]) != identity['start_ticks']:
            return None
        ticks = os.sysconf("SC_CLK_TCK")
        return {"wall": stamp, "cpu": (int(fields[11])+int(fields[12])) / ticks,
                "rss": int(fields[21])*os.sysconf("SC_PAGE_SIZE"), "tick": 1/ticks}
    except (FileNotFoundError, ProcessLookupError):
        return None


def monitor_child(process, job, *, child_deadline, plan_deadline, cadence,
                  child_rss_cap, aggregate_rss_cap, stderr_path=None, cpu_stop=None):
    """Reap every path, including supervisor CPU expiry; no numerical work."""
    reason, sample, identity = None, None, None
    try:
        while True:
            if cpu_stop is not None and cpu_stop["expired"]:
                reason = "PLAN-PARENT-CPU-INCOMPLETE"
                break
            pid, wait_status, usage = os.wait4(process.pid, os.WNOHANG)
            if pid:
                process.returncode = os.waitstatus_to_exitcode(wait_status)
                return reason, usage, sample
            if identity is None:
                identity = read_worker_identity(stderr_path, process.pid)
            sample_now = read_live_sample(process.pid, identity)
            if sample_now is not None:
                sample = sample_now
            now = time.monotonic()
            if sample_now and (sample_now["rss"] > child_rss_cap or
                    sample_now["rss"] + resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024 > aggregate_rss_cap):
                reason = "MEMORY-CAP-ABORT"
            elif now >= plan_deadline:
                reason = "PLAN-WALL-BUDGET-INCOMPLETE"
            elif now >= child_deadline:
                reason = "WALL-CAP-CENSORED"
            if reason:
                break
            time.sleep(min(cadence, max(0, min(child_deadline, plan_deadline)-now)))
    except BaseException:
        try:
            os.kill(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        os.wait4(process.pid, 0)
        process.returncode = -signal.SIGKILL
        raise
    try:
        os.kill(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    _, wait_status, usage = os.wait4(process.pid, 0)
    process.returncode = os.waitstatus_to_exitcode(wait_status)
    return reason, usage, sample


def phase_lower_bounds(stderr_path, sample):
    """Last proven-live sample, never kill/reap time or another process's CPU clock."""
    starts = []
    for line in stderr_path.read_text().splitlines():
        try:
            value = json.loads(line)
        except ValueError:
            continue
        if value.get("event") == "PHASE-STARTED":
            starts.append(value)
        elif value.get("event") == "PHASE-FINISHED":
            return {}
    if len(starts) != 1 or sample is None or sample["wall"] < starts[0]["wall"]:
        return {}
    start = starts[0]
    return {"phase_wall_lower_bound_seconds": max(0, sample["wall"]-start["wall"]),
            "phase_cpu_lower_bound_seconds": max(0, sample["cpu"]-start["cpu"]-2*sample["tick"]),
            "phase_bound_source": "identity-verified last-live /proc sample; CPU subtracts two clock ticks"}


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
    print(json.dumps({"event": "PHASE-STARTED", "cpu": started_cpu, "wall": started_wall}),
          file=sys.stderr, flush=True)
    # Stress measures the instrumented phase, including start/end marker flushes.
    # Production's evaluate-only scope excludes the marker/setup entirely.
    if job["kind"] == "production":
        started_cpu, started_wall = time.process_time(), time.monotonic()
    try:
        if job["kind"] == "production":
            with e4_deadline(job["e4_wall_cap"]):
                started_cpu, started_wall = time.process_time(), time.monotonic()
                result = action()
                finished_cpu, finished_wall = time.process_time(), time.monotonic()
        else:
            result = action()
    except E4WallExpired:
        # Integral/report did not complete: elapsed phase is a lower bound, never a completed timing.
        record = {"outcome": "PRODUCTION-E4-WALL-CENSORED", "subdivisions": None,
                  "phase_wall_lower_bound_seconds": job["e4_wall_cap"],
                  "phase_cpu_lower_bound_seconds": time.process_time()-started_cpu,
                  "e4_wall_cap": job["e4_wall_cap"], "phase_clock_scope": "evaluate-only"}
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
    print(json.dumps({"event": "PHASE-FINISHED", "outcome": record["outcome"]}), file=sys.stderr, flush=True)
    censored = record["outcome"] == "PRODUCTION-E4-WALL-CENSORED"
    if job["kind"] == "stress":
        finished_cpu, finished_wall = time.process_time(), time.monotonic()
    elif record["outcome"] == "PRODUCTION-PROTOCOL-ERROR":
        finished_cpu, finished_wall = time.process_time(), time.monotonic()
    record.update(phase_cpu_seconds=None if censored else finished_cpu-started_cpu,
                  phase_wall_seconds=None if censored else finished_wall-started_wall,
                  threadpools=pools)
    return record


def run_campaign(receipt_path, output_directory):
    start_wall = time.monotonic()  # Includes receipt, preflight, method verification and all jobs.
    receipt = check_receipt(receipt_path, output_directory)  # No timed execution before this gate.
    manifest = json.loads(MANIFEST.read_text())
    cpu_stop = None
    try:
        try:
            cpu_stop = supervisor_limits(manifest)
            check_runtime(manifest)
            initial_memory = memory_preflight()
            # Method checks are included in the campaign clock; new data cannot refit this reference.
            methods.verify_reference(methods.method_reference(), json.loads(REFERENCE.read_text()))
            json.loads(FIXTURES.read_text())
            if cpu_stop["expired"]:
                raise RuntimeError("supervisor CPU soft cap exhausted during preflight; no child started")
        except Exception as exc:
            print(json.dumps({"event": "PREFLIGHT-ABORT",
                              "outcome": "PLAN-PARENT-CPU-INCOMPLETE" if cpu_stop and cpu_stop["expired"] else "PREFLIGHT-ABORT",
                              "error_type": type(exc).__name__, "error": str(exc),
                              "reviewed_commit": receipt["reviewed_commit"],
                              "manifest_sha256": sha256(MANIFEST.read_bytes()).hexdigest(),
                              "output_directory": str(Path(output_directory).resolve()),
                              "output_directory_created": False, "worker_started": False,
                              "not_run_ids": [j["id"] for j in manifest["jobs"]],
                              "plan_wall_seconds": time.monotonic()-start_wall,
                              "parent_cpu_seconds": time.process_time()}, sort_keys=True),
                  file=sys.stderr, flush=True)
            raise
        return _run_preflighted_campaign(receipt_path, output_directory, receipt, manifest,
                                         cpu_stop, start_wall, initial_memory)
    finally:
        if cpu_stop is not None:
            signal.signal(signal.SIGXCPU, cpu_stop["old_handler"])


def _run_preflighted_campaign(receipt_path, output_directory, receipt, manifest,
                              cpu_stop, start_wall, initial_memory):
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
              "receipt": json.loads(Path(receipt_path).read_text()), "method_verified": True,
              "initial_memory": initial_memory, "actual_python": sys.version})
        for index, job in enumerate(manifest["jobs"]):
            if cpu_stop["expired"]:
                status = "PLAN-PARENT-CPU-INCOMPLETE"
                emit({"outcome": status, "not_run_ids": [x["id"] for x in manifest["jobs"][index:]]})
                break
            # Reserve full parent soft cap, child hard-limit tail and collection margin.
            if children_cpu + job["cpu_cap"] + 2 + manifest["supervisor_cpu_soft_cap"] > manifest["total_cpu_cap"]:
                status = "PLAN-CPU-BUDGET-INCOMPLETE"
                emit({"outcome": status, "not_run_ids": [x["id"] for x in manifest["jobs"][index:]]})
                break
            plan_deadline = start_wall + manifest["total_wall_cap"] - manifest["wall_cleanup_margin"]
            if time.monotonic() + job["wall_cap"] + manifest["wall_startup_margin"] > plan_deadline:
                status = "PLAN-WALL-BUDGET-INCOMPLETE"
                emit({"outcome": status, "not_run_ids": [x["id"] for x in manifest["jobs"][index:]]})
                break
            try:
                memory = memory_preflight()
            except RuntimeError as exc:
                status = "MEMORY-PREFLIGHT-ABORT"
                emit({"outcome": status, "error": str(exc),
                      "not_run_ids": [x["id"] for x in manifest["jobs"][index:]]})
                break
            # Recheck after preflight/fsync setup before spending an attempt.
            if time.monotonic() + job["wall_cap"] + manifest["wall_startup_margin"] > plan_deadline:
                status = "PLAN-WALL-BUDGET-INCOMPLETE"
                emit({"outcome": status, "not_run_ids": [x["id"] for x in manifest["jobs"][index:]]})
                break
            if cpu_stop["expired"]:
                status = "PLAN-PARENT-CPU-INCOMPLETE"
                emit({"outcome": status, "not_run_ids": [x["id"] for x in manifest["jobs"][index:]]})
                break
            emit({"job_id": job["id"], "outcome": "ATTEMPT-STARTED", "memory_preflight": memory})
            out, err = directory / (job["id"]+".json"), directory / (job["id"]+".stderr")
            with out.open("x") as stdout, err.open("x") as stderr:
                command = [sys.executable, "-m", "benchmarks.stage5c_e4_v02_resource_campaign", "worker", "--job", str(index)]
                environment = dict(os.environ, STAGE5C_RESOURCE_REVIEW_RECEIPT=str(Path(receipt_path).resolve()),
                                   STAGE5C_RESOURCE_OUTPUT_DIRECTORY=str(directory),
                                   STAGE5C_RESOURCE_PARENT_PID=str(os.getpid()),
                                   STAGE5C_RESOURCE_REVIEWED_COMMIT=receipt["reviewed_commit"])
                began = time.monotonic()  # Whole-child cap starts before spawn, including imports.
                child_deadline = began + job["wall_cap"]
                deadline_source = "plan" if plan_deadline <= child_deadline else "per-child"
                if cpu_stop["expired"]:
                    status = "PLAN-PARENT-CPU-INCOMPLETE"
                    emit({"job_id": job["id"], "outcome": status, "worker_started": False})
                    emit({"outcome": "NOT-RUN", "not_run_ids": [x["id"] for x in manifest["jobs"][index+1:]]})
                    break
                process = subprocess.Popen(command, cwd=ROOT, stdout=stdout, stderr=stderr, env=environment)
                reason, usage, sample = monitor_child(
                    process, job, child_deadline=child_deadline, plan_deadline=plan_deadline,
                    cadence=manifest["poll_cadence_seconds"], child_rss_cap=manifest["child_rss_cap_bytes"],
                    aggregate_rss_cap=manifest["aggregate_parent_child_rss_cap_bytes"], stderr_path=err, cpu_stop=cpu_stop)
            cpu = usage.ru_utime + usage.ru_stime
            children_cpu += cpu
            record = {"job_id": job["id"], "role": job["role"], "child_total_cpu_seconds": cpu,
                      "child_total_wall_seconds": time.monotonic()-began,
                      "child_peak_rss_bytes": usage.ru_maxrss*1024,
                      "parent_peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                      "memory_preflight": memory, "worker_deadline_source": deadline_source,
                      "child_deadline_monotonic": child_deadline, "plan_deadline_monotonic": plan_deadline,
                      "supervisor_affinity": manifest["host"]["supervisor_affinity"],
                      "worker_affinity": manifest["host"]["worker_affinity"]}
            record["sum_of_parent_child_peaks_bytes"] = record["parent_peak_rss_bytes"]+record["child_peak_rss_bytes"]
            if usage.ru_maxrss*1024 > 2*1024**3 or record["sum_of_parent_child_peaks_bytes"] > 5*1024**3//2:
                reason = "MEMORY-CAP-ABORT"
            if reason:
                record.update(outcome=reason, phase_cpu_seconds=None, phase_wall_seconds=None,
                              phase_cost_bound="UNKNOWN; whole-child cost is not a phase lower bound")
            elif process.returncode == -signal.SIGXCPU:
                record.update(outcome="CPU-CAP-CENSORED", phase_cpu_seconds=None, phase_wall_seconds=None)
            elif process.returncode != 0:
                record.update(outcome="IMPLEMENTATION-ABORT", exit_code=process.returncode)
                reason = "IMPLEMENTATION-ABORT"
            else:
                record.update(json.loads(out.read_text()))
            if job["kind"] == "stress" and record["outcome"] in ("WALL-CAP-CENSORED", "CPU-CAP-CENSORED"):
                record.update(phase_lower_bounds(err, sample))
                if "phase_wall_lower_bound_seconds" in record:
                    record["phase_cost_bound"] = "instrumented stress phase lower bound; includes start-marker flush"
            emit(record)
            if cpu_stop["expired"]:
                reason = "PLAN-PARENT-CPU-INCOMPLETE"
            if reason in ("MEMORY-CAP-ABORT", "IMPLEMENTATION-ABORT", "PLAN-WALL-BUDGET-INCOMPLETE", "PLAN-PARENT-CPU-INCOMPLETE"):
                status = reason
                emit({"outcome": "NOT-RUN", "not_run_ids": [x["id"] for x in manifest["jobs"][index+1:]]})
                break
        final_wall, final_parent_cpu = time.monotonic()-start_wall, time.process_time()-start_cpu
        if cpu_stop["expired"]:
            status = "PLAN-PARENT-CPU-INCOMPLETE"
        if status == "PLAN-COMPLETE":
            if final_wall > manifest["total_wall_cap"]:
                status = "PLAN-WALL-BUDGET-INCOMPLETE"
            elif final_parent_cpu + children_cpu > manifest["total_cpu_cap"]:
                status = "PLAN-CPU-BUDGET-INCOMPLETE"
        summary = {"record_type": "TERMINAL-SUMMARY", "summary_revision": 1,
                   "outcome": status, "plan_wall_seconds": final_wall,
                   "parent_cpu_seconds": final_parent_cpu, "children_cpu_seconds": children_cpu,
                   "total_accounted_cpu_seconds": final_parent_cpu+children_cpu,
                   "production_schedule_cpu_bound": False}
        emit(summary)
        # A signal arriving during the final write/fsync cannot interrupt the checkpoint.
        # Append a corrected terminal summary if the flag was set in that interval.
        if cpu_stop["expired"] and status != "PLAN-PARENT-CPU-INCOMPLETE":
            parent_cpu = time.process_time()-start_cpu
            summary.update(summary_revision=2, supersedes_previous_summary=True,
                           outcome="PLAN-PARENT-CPU-INCOMPLETE", plan_wall_seconds=time.monotonic()-start_wall,
                           parent_cpu_seconds=parent_cpu, total_accounted_cpu_seconds=parent_cpu+children_cpu)
            emit(summary)


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
        # Guard before costly imports/runtime checks; verify after prctl to close parent-death race.
        expected_parent = os.environ.get("STAGE5C_RESOURCE_PARENT_PID")
        if expected_parent is None:
            raise ResourceNotAuthorized("internal supervisor parent required")
        parent_death_guard(int(expected_parent))
        announce_worker_identity()
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
        if args.job is None or not 0 <= args.job < len(manifest["jobs"]):
            raise ResourceNotAuthorized("internal job index required")
        job = manifest["jobs"][args.job]
        worker_limits(job, address_space_cap=manifest["child_address_space_cap_bytes"])
        check_runtime(manifest, role="worker")
        print(json.dumps(worker(job, json.loads(FIXTURES.read_text()))))


if __name__ == "__main__":
    main()
