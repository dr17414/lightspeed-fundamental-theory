"""Docker configuration and gate-order regressions; no real campaign/producer."""
import copy
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from benchmarks import stage5c_e4_v02_container_launch as launch
from benchmarks import stage5c_e4_v02_resource_campaign as campaign


def manifest():
    return json.loads(campaign.MANIFEST.read_text())


def fixture(mode="run"):
    # Independently retained actual image-smoke Docker shape, with new command
    # and the extra read-only launcher proof bind required by this PR.
    cid = "a" * 64
    paths = {k: "/external/" + k for k in ("repo", "custody", "output", "launch")}
    config = dict(Image=manifest()["host_amendment"]["execution_container"]["campaign_image_config_digest"],
                  Hostname=cid[:12], Entrypoint=["/opt/python/bin/python3.12"],
                  Cmd=["-m", launch.CAMPAIGN, "run", "--authorization", "/custody/receipt.json", "--output", "/output/campaign"]
                      if mode == "run" else ["-m", launch.LAUNCHER, "container-preflight"],
                  WorkingDir="/repo", User="0:0", StopTimeout=15, Volumes=None,
                  Env=[k + "=1" for k in launch.THREAD_ENV] +
                      ["PYTHONPATH=/opt/deps:/repo", "PYTHONNOUSERSITE=1", "PYTHONDONTWRITEBYTECODE=1",
                       "GIT_OPTIONAL_LOCKS=0", "GIT_CONFIG_COUNT=1", "GIT_CONFIG_KEY_0=safe.directory", "GIT_CONFIG_VALUE_0=/repo"])
    host = dict(NanoCpus=2000000000, CpuPeriod=0, CpuQuota=0, CpusetCpus="0,1", Memory=6442450944,
                MemorySwap=6442450944, ShmSize=67108864, CgroupnsMode="private", NetworkMode="none",
                ReadonlyRootfs=True, Init=True, Privileged=False, PidMode="", IpcMode="private", UTSMode="",
                RestartPolicy={"Name": "no", "MaximumRetryCount": 0}, AutoRemove=False,
                CapDrop=["ALL"], CapAdd=None, SecurityOpt=["no-new-privileges"],
                Tmpfs={"/tmp": "rw,nosuid,nodev,noexec,size=268435456,mode=1777"}, Binds=None, VolumesFrom=None)
    mounts = [dict(Type="bind", Source=paths[key], Destination="/"+key, RW=key == "output", Propagation="rprivate")
              for key in paths]
    host["Mounts"] = [dict(Type="bind", Source=m["Source"], Target=m["Destination"], ReadOnly=not m["RW"])
                      for m in mounts]
    state = dict(Status="created", Running=False, Pid=0, Paused=False, OOMKilled=False, Restarting=False, Dead=False, Error="")
    return dict(Id=cid, Image=config["Image"], Config=config, HostConfig=host,
                Mounts=mounts, State=state, RestartCount=0), paths


@pytest.mark.parametrize("mode", ["run", "preflight"])
def test_complete_stopped_inspection_passes(mode):
    inspection, paths = fixture(mode)
    launch.verify_inspection(manifest(), inspection, paths, mode, stopped=True)


@pytest.mark.parametrize("section,key,value", [
    (None, "Image", "sha256:"+"0"*64), (None, "RestartCount", 1),
    ("Config", "Image", "sha256:"+"0"*64), ("Config", "Entrypoint", ["/bin/sh"]),
    ("Config", "Cmd", ["-m", launch.CAMPAIGN, "run"]), ("Config", "Hostname", "replay"),
    ("Config", "WorkingDir", "/tmp"), ("Config", "User", "1000:1000"),
    ("Config", "StopTimeout", 60), ("Config", "Env", []), ("Config", "Volumes", {"/output": {}}),
    ("HostConfig", "NanoCpus", 8000000000), ("HostConfig", "CpuPeriod", 100000),
    ("HostConfig", "CpuQuota", 200000), ("HostConfig", "CpusetCpus", "0"),
    ("HostConfig", "Memory", 8589934592), ("HostConfig", "MemorySwap", -1),
    ("HostConfig", "ShmSize", 268435456), ("HostConfig", "CgroupnsMode", "host"),
    ("HostConfig", "NetworkMode", "bridge"), ("HostConfig", "ReadonlyRootfs", False),
    ("HostConfig", "Init", False), ("HostConfig", "Privileged", True),
    ("HostConfig", "PidMode", "host"), ("HostConfig", "IpcMode", "host"), ("HostConfig", "UTSMode", "host"),
    ("HostConfig", "RestartPolicy", {"Name": "always", "MaximumRetryCount": 0}),
    ("HostConfig", "AutoRemove", True), ("HostConfig", "CapDrop", []),
    ("HostConfig", "CapAdd", ["SYS_ADMIN"]), ("HostConfig", "SecurityOpt", []),
    ("HostConfig", "Tmpfs", {}), ("HostConfig", "Binds", ["/var/run/docker.sock:/docker.sock"]),
    ("HostConfig", "VolumesFrom", ["other"]),
    ("State", "OOMKilled", True), ("State", "Restarting", True), ("State", "Dead", True),
    ("State", "Error", "failed"), ("State", "Status", "exited"),
    ("State", "Running", True), ("State", "Pid", 42), ("State", "Paused", True),
])
def test_docker_mismatch_is_rejected(section, key, value):
    inspection, paths = fixture()
    (inspection if section is None else inspection[section])[key] = value
    with pytest.raises(launch.ContainerMismatch):
        launch.verify_inspection(manifest(), inspection, paths, "run", stopped=True)


@pytest.mark.parametrize("target", ["repo", "custody", "output", "launch"])
@pytest.mark.parametrize("field,value", [("Source", "/wrong"), ("RW", None), ("Type", "volume"), ("Propagation", "shared")])
def test_effective_bind_permissions_and_identity(target, field, value):
    inspection, paths = fixture()
    next(m for m in inspection["Mounts"] if m["Destination"] == "/"+target)[field] = value
    with pytest.raises(launch.ContainerMismatch):
        launch.verify_inspection(manifest(), inspection, paths, "run", stopped=True)


def test_missing_and_duplicate_mounts_fail_closed():
    inspection, paths = fixture()
    inspection["Mounts"][1] = copy.deepcopy(inspection["Mounts"][0])
    with pytest.raises(launch.ContainerMismatch, match="duplicate mount"):
        launch.verify_inspection(manifest(), inspection, paths, "run")
    del inspection["HostConfig"]["Memory"]
    with pytest.raises(launch.ContainerMismatch, match="malformed"):
        launch.verify_inspection(manifest(), inspection, paths, "run")


def test_thread_environment_each_value_is_checked():
    for key in launch.THREAD_ENV:
        inspection, paths = fixture()
        inspection["Config"]["Env"] = [x if not x.startswith(key+"=") else key+"=2" for x in inspection["Config"]["Env"]]
        with pytest.raises(launch.ContainerMismatch, match="thread"):
            launch.verify_inspection(manifest(), inspection, paths, "run")


def mountinfo():
    return "\n".join(f"{i} 1 0:1 / {p} {opts} - {fs} source rw" for i, (p, opts, fs) in enumerate([
        ("/", "ro,relatime", "overlay"), ("/repo", "ro,relatime", "ext4"),
        ("/custody", "ro,relatime", "ext4"), ("/launch", "ro,relatime", "ext4"),
        ("/output", "rw,relatime", "ext4"), ("/tmp", "rw,nosuid,nodev,noexec", "tmpfs")], 10))


def test_linux_effective_mount_checks_and_nested_override():
    launch.verify_effective_mounts(mountinfo())
    for p in ("/", "/repo", "/custody", "/launch"):
        with pytest.raises(launch.ContainerMismatch):
            launch.verify_effective_mounts(mountinfo().replace(f"/ {p} ro,", f"/ {p} rw,"))
    with pytest.raises(launch.ContainerMismatch, match="nested"):
        launch.verify_effective_mounts(mountinfo()+"\n20 1 0:2 / /repo/analysis rw - tmpfs source rw")


def test_failed_container_gate_never_reads_receipt_or_calls_producer(monkeypatch, tmp_path, capsys):
    touched = []
    receipt = tmp_path / "receipt.json"
    real_read = Path.read_text
    def read(path, *a, **k):
        if path == receipt:
            touched.append("receipt")
        return real_read(path, *a, **k)
    monkeypatch.setattr(Path, "read_text", read)
    def rejected(*a, **k):
        raise launch.ContainerMismatch("wrong image")
    monkeypatch.setattr(launch, "check_before_receipt", rejected)
    monkeypatch.setattr(campaign, "worker", lambda *a: pytest.fail("producer called"))
    with pytest.raises(launch.ContainerMismatch, match="wrong image"):
        campaign.run_campaign(str(receipt), tmp_path/"uncreated")
    assert touched == [] and not (tmp_path/"uncreated").exists()
    record = json.loads(capsys.readouterr().err)
    assert record["event"] == "CONTAINER-PREFLIGHT-ABORT"
    assert record["receipt_gate_called"] is record["numeric_producer_called"] is False


def test_direct_campaign_entry_cannot_bypass_launcher():
    with pytest.raises(launch.ContainerMismatch, match="launcher"):
        launch.check_before_receipt(manifest())


@pytest.mark.parametrize("field", [None, "reviewed_commit", "reviewed_tree", "image_config_digest",
                                   "host_profile_sha256", "manifest_sha256", "output_directory",
                                   "host_boot_id", "host_output_directory"])
def test_new_receipt_binding_and_container_check_precedes_read(monkeypatch, field):
    current = manifest()
    image = current["host_amendment"]["execution_container"]["campaign_image_config_digest"]
    receipt = dict(authorization="DETERMINISTIC-RESOURCE-DEVELOPMENT-ONLY", reviewed_commit="c"*40,
                   reviewed_tree="d"*40, image_config_digest=image,
                   host_boot_id="boot", host_output_directory="/external/output",
                   host_profile_sha256=sha256(json.dumps(current["host"], sort_keys=True,
                                                        separators=(",", ":")).encode()).hexdigest(),
                   manifest_sha256=sha256(campaign.MANIFEST.read_bytes()).hexdigest(), output_directory="/output/campaign")
    if field:
        receipt[field] = "stale"
    order = []
    def guard(*a, **k):
        order.append("container-check")
        return {"reviewed_tree": "d"*40, "image_config_digest": image,
                "host_boot_id": "boot", "host_output_directory": "/external/output"}
    monkeypatch.setattr(launch, "check_before_receipt", guard)
    real_read = Path.read_text
    def read(path, *a, **k):
        if str(path) == "/custody/receipt.json":
            order.append("receipt-read")
            return json.dumps(receipt)
        return real_read(path, *a, **k)
    monkeypatch.setattr(Path, "read_text", read)
    monkeypatch.setattr(campaign.subprocess, "check_output", lambda cmd, **k:
                        "c"*40 if cmd[1] == "rev-parse" else "")
    if field:
        with pytest.raises(campaign.ResourceNotAuthorized, match="mismatch"):
            campaign.check_receipt("/custody/receipt.json", "/output/campaign")
    else:
        assert campaign.check_receipt("/custody/receipt.json", "/output/campaign") == receipt
    assert order == ["container-check", "receipt-read"]


@pytest.mark.parametrize("fault", [None, "container-id", "mode", "manifest", "boot", "mount", "packages"])
def test_effective_container_guard_rejects_stale_proof_before_runtime(monkeypatch, tmp_path, fault):
    inspection, paths = fixture()
    raw = campaign.MANIFEST.read_bytes()
    proof = dict(version=1, mode="run", container_id=inspection["Id"], paths=paths, inspection=inspection,
                 reviewed_commit="c"*40, reviewed_tree="d"*40, manifest_sha256=sha256(raw).hexdigest(), host_boot_id="boot")
    if fault == "container-id": proof["container_id"] = "b"*64
    if fault == "mode": proof["mode"] = "preflight"
    if fault == "manifest": proof["manifest_sha256"] = "0"*64
    if fault == "boot": proof["host_boot_id"] = "old-boot"
    actual_mounts = mountinfo().replace("/ /launch ro,", "/ /launch rw,") if fault == "mount" else mountinfo()
    calls = []
    monkeypatch.setattr(launch, "ROOT", Path("/repo"))
    proof_path = tmp_path/"proof.json"
    proof_path.write_text(json.dumps(proof))
    monkeypatch.setattr(launch, "PROOF", proof_path)
    monkeypatch.setattr(launch.socket, "gethostname", lambda: "a"*12)
    monkeypatch.setattr(launch.Path, "cwd", lambda: Path("/repo"))
    monkeypatch.setattr(launch.os, "geteuid", lambda: 0)
    monkeypatch.setattr(launch, "git_identity", lambda *a: ("c"*40, "d"*40))
    real_read = Path.read_text
    def read(path, *a, **k):
        if str(path) == "/proc/sys/kernel/random/boot_id": return "boot"
        if str(path) == "/proc/self/mountinfo": return actual_mounts
        if str(path) == "/custody/receipt.json": pytest.fail("receipt read before numerical child PASS")
        return real_read(path, *a, **k)
    monkeypatch.setattr(Path, "read_text", read)
    monkeypatch.setattr(campaign, "check_runtime", lambda *a: calls.append("runtime"))
    def packages(*a):
        calls.append("packages")
        if fault == "packages":
            raise RuntimeError("numerical preflight subprocess failed")
    monkeypatch.setattr(campaign, "check_numerical_runtime_in_subprocess", packages)
    monkeypatch.setattr(campaign, "memory_preflight", lambda: {"headroom": 4*1024**3})
    if fault == "packages":
        with pytest.raises(RuntimeError, match="numerical preflight subprocess"):
            campaign.check_receipt("/custody/receipt.json", "/output/campaign")
        assert calls == ["runtime", "packages"]
    elif fault:
        with pytest.raises(launch.ContainerMismatch):
            launch.check_before_receipt(manifest())
        assert calls == []
    else:
        result = launch.check_before_receipt(manifest())
        assert result["receipt_gate_called"] is result["numeric_producer_called"] is False
        assert calls == ["runtime", "packages"]


def prepared_host(tmp_path, monkeypatch):
    repo = tmp_path/"repo"
    (repo/"docs").mkdir(parents=True)
    raw = json.dumps(manifest()).encode()
    mf = repo/"docs"/campaign.MANIFEST.name
    mf.write_bytes(raw)
    paths = {k: str(tmp_path/k) for k in ("repo", "custody", "output", "launch")}
    for k in ("custody", "output", "launch"):
        Path(paths[k]).mkdir()
    (Path(paths["custody"])/"receipt.json").write_text("receipt must never be read in host prepare/start")
    monkeypatch.setattr(launch, "git_identity", lambda p: ("c"*40, "d"*40))
    monkeypatch.setattr(launch, "verify_sources", lambda *a: None)
    inspected, _ = fixture("preflight")
    for m in inspected["Mounts"]:
        m["Source"] = paths[m["Destination"][1:]]
    for m in inspected["HostConfig"]["Mounts"]:
        m["Source"] = paths[m["Target"][1:]]
    return paths, inspected


def test_two_phase_host_order_and_reinspection_before_start(monkeypatch, tmp_path):
    paths, inspected = prepared_host(tmp_path, monkeypatch)
    calls = []
    def docker(*args):
        calls.append(args[0])
        return inspected["Id"] if args[0] in ("create", "start") else json.dumps([inspected])
    monkeypatch.setattr(launch, "docker", docker)
    result = launch.host_prepare(*(paths[k] for k in ("repo", "custody", "output", "launch")), "c"*40)
    assert result["event"] == "CONTAINER-PREPARED-NOT-STARTED"
    assert calls == ["create", "inspect"]
    launch.host_start(paths["launch"])
    assert calls == ["create", "inspect", "inspect", "start"]
    calls.clear()
    inspected["HostConfig"]["MemorySwap"] = -1
    with pytest.raises(launch.ContainerMismatch):
        launch.host_start(paths["launch"])
    assert calls == ["inspect"]


def test_bad_image_prepare_never_starts_or_writes_pass_proof(monkeypatch, tmp_path):
    paths, inspected = prepared_host(tmp_path, monkeypatch)
    inspected["Image"] = "sha256:"+"0"*64
    calls = []
    def docker(*args):
        calls.append(args[0])
        return inspected["Id"] if args[0] == "create" else json.dumps([inspected])
    monkeypatch.setattr(launch, "docker", docker)
    with pytest.raises(launch.ContainerMismatch, match="image"):
        launch.host_prepare(*(paths[k] for k in ("repo", "custody", "output", "launch")), "c"*40)
    assert calls == ["create", "inspect"]
    assert not (Path(paths["launch"])/"inspection.json").exists()


def test_openblas_version_kernel_thread_and_pool_count(monkeypatch):
    import threadpoolctl
    pools = copy.deepcopy(manifest()["host"]["blas_pools"])
    monkeypatch.setattr(threadpoolctl, "threadpool_info", lambda: pools)
    assert campaign.check_numerical_runtime(manifest()) == pools
    for key, value in (("version", "0.3.29"), ("architecture", "Zen"), ("num_threads", 2)):
        original = pools[0][key]
        pools[0][key] = value
        with pytest.raises(RuntimeError, match="OpenBLAS"):
            campaign.check_numerical_runtime(manifest())
        pools[0][key] = original
    pools.pop()
    with pytest.raises(RuntimeError, match="OpenBLAS"):
        campaign.check_numerical_runtime(manifest())


def test_real_openblas_loading_in_fresh_interpreter():
    # A fresh exec prevents earlier tests from accidentally loading SciPy's BLAS.
    # Observe real libraries, not a replacement for threadpool_info. CPU kernels
    # may vary in CI, so only the count and prefix multiset are compared here.
    script = '''
import json, sys
from benchmarks import stage5c_e4_v02_resource_campaign as campaign
assert 'numpy' not in sys.modules and 'scipy' not in sys.modules
manifest = json.loads(campaign.MANIFEST.read_text())
pools = campaign.load_numerical_runtime(manifest)
assert len(pools) == 2
assert sorted(p['prefix'] for p in pools) == sorted(p['prefix'] for p in manifest['host']['blas_pools'])
assert all(name in sys.modules for name in ('scipy.linalg', 'scipy.integrate', 'scipy.optimize'))
print(json.dumps(pools))
'''
    env = dict(os.environ, **{k: "1" for k in campaign.THREAD_ENV})
    result = subprocess.run([sys.executable, "-c", script], cwd=campaign.ROOT,
                            env=env, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
    assert len(json.loads(result.stdout)) == 2


def test_real_numerical_preflight_keeps_supervisor_free_of_numerical_libraries():
    script = '''
import importlib.abc, json, os, resource, subprocess, sys
from benchmarks import stage5c_e4_v02_resource_campaign as campaign
class NoNumericalImports(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in ('numpy', 'scipy'):
            raise AssertionError('supervisor numerical import: ' + fullname)
sys.meta_path.insert(0, NoNumericalImports())
manifest = json.loads(campaign.MANIFEST.read_text())
# Observe the local CPU in another fresh process, without faking library data.
# Production pins are untouched; this test must also run on CI's other CPUs.
observer = "import json; from benchmarks import stage5c_e4_v02_resource_campaign as c; print(json.dumps(c.load_numerical_runtime(json.loads(c.MANIFEST.read_text()))))"
pools = json.loads(subprocess.check_output([sys.executable, '-c', observer], text=True))
assert len(pools) == 2
assert sorted(p['prefix'] for p in pools) == sorted(p['prefix'] for p in manifest['host']['blas_pools'])
for expected, actual in zip(manifest['host']['blas_pools'], pools):
    expected['architecture'] = actual['architecture']
before = resource.getrusage(resource.RUSAGE_CHILDREN)
for verify_method in (False, True):
    checked = campaign.check_numerical_runtime_in_subprocess(manifest, verify_method=verify_method)
    assert len(checked) == 2
    assert sorted(p['prefix'] for p in checked) == sorted(p['prefix'] for p in pools)
    assert not any(k.split('.')[0] in ('numpy', 'scipy') for k in sys.modules)
after = resource.getrusage(resource.RUSAGE_CHILDREN)
assert after.ru_utime + after.ru_stime > before.ru_utime + before.ru_stime
# A genuine missing-pool rejection propagates back without loading the parent.
manifest['host']['blas_pools'].pop()
try:
    campaign.check_numerical_runtime_in_subprocess(manifest)
except RuntimeError as exc:
    assert 'OpenBLAS version/kernel/thread pool pin mismatch' in str(exc)
else:
    raise AssertionError('missing pool must fail')
assert not any(k.split('.')[0] in ('numpy', 'scipy') for k in sys.modules)
'''
    env = dict(os.environ, **{k: "1" for k in campaign.THREAD_ENV},
               STAGE5C_RESOURCE_REVIEW_RECEIPT="/nonexistent-do-not-open-receipt")
    result = subprocess.run([sys.executable, "-c", script], cwd=campaign.ROOT,
                            env=env, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("fault", ["exit", "timeout", "json", "report"])
def test_numerical_preflight_subprocess_fails_closed(monkeypatch, fault):
    def failed(command, **kwargs):
        assert command[-1] == "numerical-preflight"
        assert kwargs["timeout"] == 30 and kwargs["check"] is True
        assert json.loads(kwargs["input"]) == manifest()
        if fault == "exit":
            raise subprocess.CalledProcessError(1, command, stderr="OpenBLAS mismatch")
        if fault == "timeout":
            raise subprocess.TimeoutExpired(command, kwargs["timeout"])
        stdout = "not JSON" if fault == "json" else json.dumps(
            {"event": "NUMERICAL-PREFLIGHT-PASS", "method_verified": True, "threadpools": []})
        return subprocess.CompletedProcess(command, 0, stdout=stdout)
    monkeypatch.setattr(campaign.subprocess, "run", failed)
    with pytest.raises(RuntimeError, match="numerical preflight subprocess"):
        campaign.check_numerical_runtime_in_subprocess(manifest())


def test_numerical_caps_and_all_non_launcher_sources_remain_frozen():
    candidate = json.loads((campaign.ROOT/"docs/stage5c_e4_v02_vultr_host_manifest_candidate.json").read_text())
    current = manifest()
    changed = {"host", "host_amendment", "input_sha256", "state", "launch_contract"}
    assert {k:v for k,v in candidate.items() if k not in changed} == {k:v for k,v in current.items() if k not in changed}
    for name, digest in candidate["input_sha256"].items():
        if name != "benchmarks/stage5c_e4_v02_resource_campaign.py":
            assert current["input_sha256"][name] == digest
    assert len(current["input_sha256"]) == 35
    assert current["authorization"] == "NONE"
    assert current["host"]["blas_pools"][0]["version"] == "0.3.30"
    assert all(p["architecture"] == "SkylakeX" for p in current["host"]["blas_pools"])
