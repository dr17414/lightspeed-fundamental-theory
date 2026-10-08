"""Two-phase Docker launcher for the reviewed development campaign.

Prepare creates a STOPPED container and verifies Docker's actual configuration.
Start re-inspects that same stopped container before starting its receipt gate.
The container checks the read-only host inspection and effective Linux runtime.
No Docker socket is mounted; the operator and host Docker daemon are trusted.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/stage5c_e4_v02_resource_measurement_manifest.json"
PROOF = Path("/launch/inspection.json")
THREAD_ENV = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
              "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS")
PYTHON = "/opt/python/bin/python3.12"
CAMPAIGN = "benchmarks.stage5c_e4_v02_resource_campaign"
LAUNCHER = "benchmarks.stage5c_e4_v02_container_launch"
RECEIPT = "/custody/receipt.json"
OUTPUT = "/output/campaign"


class ContainerMismatch(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ContainerMismatch(message)


def container_command(mode):
    require(mode in ("preflight", "run"), "unknown launch mode")
    if mode == "preflight":
        return ["-m", LAUNCHER, "container-preflight"]
    return ["-m", CAMPAIGN, "run", "--authorization", RECEIPT, "--output", OUTPUT]


def verify_inspection(manifest, inspection, paths, mode, *, stopped=False):
    """Fail closed on actual inspect fields, not on a claimed PASS/flag list."""
    try:
        expected = manifest["host_amendment"]["execution_container"]
        config, host, state = inspection["Config"], inspection["HostConfig"], inspection["State"]
        cid = inspection["Id"]
        require(len(cid) == 64 and all(c in "0123456789abcdef" for c in cid), "container ID")
        require(inspection["Image"] == expected["campaign_image_config_digest"] == config["Image"], "image ID")
        require(config["Hostname"] == cid[:12], "container hostname")
        require(config["Entrypoint"] == [PYTHON] and config["Cmd"] == container_command(mode), "entrypoint/command")
        require(config["WorkingDir"] == "/repo" and config["User"] == "0:0", "working directory/UID")
        require(config["StopTimeout"] == 15, "stop timeout")
        env = dict(item.split("=", 1) for item in config["Env"])
        require(all(env.get(k) == "1" for k in THREAD_ENV), "thread environment")
        require(env.get("PYTHONPATH") == "/opt/deps:/repo" and env.get("PYTHONNOUSERSITE") == "1"
                and env.get("PYTHONDONTWRITEBYTECODE") == "1", "Python import environment")
        require(env.get("GIT_OPTIONAL_LOCKS") == "0" and env.get("GIT_CONFIG_COUNT") == "1"
                and env.get("GIT_CONFIG_KEY_0") == "safe.directory"
                and env.get("GIT_CONFIG_VALUE_0") == "/repo", "read-only Git environment")
        require(host["NanoCpus"] == 2000000000 and host["CpuPeriod"] == 0 and host["CpuQuota"] == 0
                and host["CpusetCpus"] == "0,1", "CPU Docker parameters")
        require(host["Memory"] == expected["memory_limit_bytes"]
                and host["MemorySwap"] == expected["memory_swap_total_bytes"], "memory Docker parameters")
        require(host["ShmSize"] == expected["shm_bytes"] and host["CgroupnsMode"] == "private", "shm/cgroup namespace")
        require(host["NetworkMode"] == "none" and host["ReadonlyRootfs"] is True
                and host["Init"] is True and host["Privileged"] is False, "isolation parameters")
        require(host["PidMode"] == "" and host["IpcMode"] == "private" and host["UTSMode"] == "", "namespaces")
        require(host["RestartPolicy"] == {"Name": "no", "MaximumRetryCount": 0}
                and inspection["RestartCount"] == 0 and host["AutoRemove"] is False, "restart/lifecycle")
        require(host["CapDrop"] == ["ALL"] and host["CapAdd"] in (None, [])
                and host["SecurityOpt"] == ["no-new-privileges"], "capabilities/security options")
        require(host["Tmpfs"] == {"/tmp": "rw,nosuid,nodev,noexec,size=268435456,mode=1777"}, "tmpfs bound")
        require(not host.get("Binds") and not host.get("VolumesFrom") and not config.get("Volumes"), "extra mounts")
        desired = {"/repo": (paths["repo"], False), "/custody": (paths["custody"], False),
                   "/output": (paths["output"], True), "/launch": (paths["launch"], False)}
        mounts = inspection["Mounts"]
        require(len(mounts) == len(desired), "mount count")
        require(len({m["Destination"] for m in mounts}) == len(mounts), "duplicate mount")
        for m in mounts:
            require(m["Destination"] in desired, "unexpected mount")
            source, writable = desired[m["Destination"]]
            require(m["Type"] == "bind" and m["Source"] == source and m["RW"] is writable
                    and m["Propagation"] == "rprivate", "mount source/permissions")
        requested = host["Mounts"]
        require(len(requested) == 4, "requested mount count")
        require(len({m["Target"] for m in requested}) == 4, "duplicate requested mount")
        for m in requested:
            require(m["Target"] in desired, "unexpected requested mount")
            source, writable = desired[m["Target"]]
            require(m["Type"] == "bind" and m["Source"] == source
                    and m.get("ReadOnly", False) is (not writable), "requested mount")
        require(state["OOMKilled"] is False and state["Restarting"] is False
                and state["Dead"] is False and state["Error"] == "", "container state")
        if stopped:
            require(state["Status"] == "created" and state["Running"] is False
                    and state["Pid"] == 0 and not state["Paused"], "container must be new and stopped")
    except (KeyError, TypeError, ValueError, AttributeError) as exc:
        raise ContainerMismatch("missing/malformed Docker inspection") from exc


def docker(*args):
    return subprocess.check_output(["docker", *args], text=True).strip()


def inspect_container(cid):
    result = json.loads(docker("inspect", cid))
    require(isinstance(result, list) and len(result) == 1, "one Docker inspection required")
    return result[0]


def git_identity(repo):
    require((repo / ".git").is_dir(), "complete checkout with .git directory required")
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()
    require(not git("status", "--porcelain"), "clean reviewed checkout required")
    return git("rev-parse", "HEAD"), git("rev-parse", "HEAD^{tree}")


def verify_sources(manifest, repo):
    for name, digest in manifest["input_sha256"].items():
        require(sha256((repo / name).read_bytes()).hexdigest() == digest, "source pin: " + name)


def host_prepare(repo, custody, output, launch, reviewed_commit, *, mode="preflight"):
    """Does not start a container, read a receipt or call a numeric producer."""
    repo, custody, output, launch = (Path(p).resolve(strict=True) for p in (repo, custody, output, launch))
    require(all(p.is_dir() for p in (repo, custody, output, launch)), "mount directories required")
    external = (custody, output, launch)
    require(all(not p.is_relative_to(repo) and not repo.is_relative_to(p) for p in external), "external mounts required")
    require(all(not a.is_relative_to(b) and not b.is_relative_to(a)
                for i, a in enumerate(external) for b in external[i+1:]), "separate non-overlapping mounts")
    require(not any(launch.iterdir()), "fresh empty launch directory required")
    require(not (output / "campaign").exists(), "campaign output must be unused")
    require((custody / "receipt.json").is_file() and not (custody / "receipt.json").is_symlink(), "receipt file required")
    head, tree = git_identity(repo)
    require(head == reviewed_commit, "reviewed commit mismatch")
    raw = (repo / MANIFEST.relative_to(ROOT)).read_bytes()
    manifest = json.loads(raw)
    verify_sources(manifest, repo)
    image = manifest["host_amendment"]["execution_container"]["campaign_image_config_digest"]
    paths = {k: str(p) for k, p in zip(("repo", "custody", "output", "launch"), (repo, custody, output, launch))}
    command = ["create", "--name", "lightspeed-campaign-" + uuid.uuid4().hex,
               "--cpus", "2", "--cpuset-cpus", "0,1", "--memory", "6g", "--memory-swap", "6g",
               "--shm-size", "67108864", "--cgroupns", "private", "--network", "none",
               "--read-only", "--restart", "no", "--init", "--user", "0:0", "--stop-timeout", "15",
               "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
               "--tmpfs", "/tmp:rw,nosuid,nodev,noexec,size=268435456,mode=1777"]
    for target, key, ro in (("/repo", "repo", True), ("/custody", "custody", True),
                            ("/output", "output", False), ("/launch", "launch", True)):
        require("," not in paths[key], "comma in bind path")
        command += ["--mount", f"type=bind,src={paths[key]},dst={target}" + (",readonly" if ro else "")]
    for key in THREAD_ENV:
        command += ["-e", key + "=1"]
    cid = docker(*command, image, *container_command(mode))
    inspection = inspect_container(cid)
    require(inspection["Id"] == cid, "Docker create/inspect ID mismatch")
    verify_inspection(manifest, inspection, paths, mode, stopped=True)
    proof = {"version": 1, "mode": mode, "container_id": cid, "paths": paths,
             "reviewed_commit": head, "reviewed_tree": tree, "manifest_sha256": sha256(raw).hexdigest(),
             "host_boot_id": Path("/proc/sys/kernel/random/boot_id").read_text().strip(), "inspection": inspection}
    with (launch / "inspection.json").open("x") as file:
        json.dump(proof, file, sort_keys=True, indent=2)
        file.flush()
        os.fsync(file.fileno())
    return {"event": "CONTAINER-PREPARED-NOT-STARTED", "container_id": cid, "mode": mode}


def host_start(launch):
    """Fresh inspection must pass before Docker starts the receipt-reading process."""
    launch = Path(launch).resolve(strict=True)
    proof = json.loads((launch / "inspection.json").read_text())
    require(proof["paths"]["launch"] == str(launch), "launch directory mismatch")
    repo = Path(proof["paths"]["repo"])
    raw = (repo / MANIFEST.relative_to(ROOT)).read_bytes()
    require(sha256(raw).hexdigest() == proof["manifest_sha256"], "manifest changed after prepare")
    require(git_identity(repo) == (proof["reviewed_commit"], proof["reviewed_tree"]), "checkout changed after prepare")
    require(Path("/proc/sys/kernel/random/boot_id").read_text().strip() == proof["host_boot_id"], "host rebooted")
    manifest = json.loads(raw)
    verify_sources(manifest, repo)
    inspection = inspect_container(proof["container_id"])
    require(inspection["Id"] == proof["container_id"], "container identity mismatch")
    verify_inspection(manifest, inspection, proof["paths"], proof["mode"], stopped=True)
    # Container configuration is fixed at create. Host admins must not update it
    # or mutate bind sources during a prepared/running campaign (trusted boundary).
    return {"event": "CONTAINER-STARTED", "container_id": docker("start", proof["container_id"]), "mode": proof["mode"]}


def read_mounts(text):
    mounts = {}
    for line in text.splitlines():
        left, right = line.split(" - ", 1)
        fields, fs = left.split(), right.split()
        mounts[fields[4]] = (set(fields[5].split(",")), fs[0])
    return mounts


def verify_effective_mounts(text):
    mounts = read_mounts(text)
    for target in ("/", "/repo", "/custody", "/launch"):
        require(target in mounts and "ro" in mounts[target][0], "effective read-only mount: " + target)
    require("/output" in mounts and "rw" in mounts["/output"][0], "effective writable output")
    require("/tmp" in mounts and mounts["/tmp"][1] == "tmpfs"
            and {"rw", "nosuid", "nodev", "noexec"} <= mounts["/tmp"][0], "effective tmpfs mount")
    require(not any(p.startswith(root + "/") for p in mounts
                    for root in ("/repo", "/custody", "/launch", "/output")), "nested mount overrides")


def check_before_receipt(manifest, *, mode="run"):
    """Inspect proof + effective runtime checked without opening the receipt."""
    require(ROOT == Path("/repo"), "campaign requires reviewed container launcher")
    proof = json.loads(PROOF.read_text())
    require(proof["version"] == 1 and proof["mode"] == mode, "launch proof version/mode")
    require(sha256(MANIFEST.read_bytes()).hexdigest() == proof["manifest_sha256"], "launch manifest hash")
    require(proof["container_id"] == proof["inspection"]["Id"]
            and socket.gethostname() == proof["container_id"][:12], "effective container identity")
    require(os.geteuid() == 0 and Path.cwd() == Path("/repo"), "effective UID/working directory")
    require(Path("/proc/sys/kernel/random/boot_id").read_text().strip() == proof["host_boot_id"], "effective boot identity")
    verify_inspection(manifest, proof["inspection"], proof["paths"], mode, stopped=True)
    verify_effective_mounts(Path("/proc/self/mountinfo").read_text())
    require(git_identity(ROOT) == (proof["reviewed_commit"], proof["reviewed_tree"]), "effective clean checkout")
    require(not Path(OUTPUT).exists(), "campaign output already exists")
    from benchmarks import stage5c_e4_v02_resource_campaign as campaign
    campaign.check_runtime(manifest)
    campaign.check_numerical_runtime(manifest)
    memory = campaign.memory_preflight()
    return {"event": "CONTAINER-PREFLIGHT-PASS", "container_id": proof["container_id"],
            "image_config_digest": proof["inspection"]["Image"], "manifest_sha256": proof["manifest_sha256"],
            "reviewed_commit": proof["reviewed_commit"], "reviewed_tree": proof["reviewed_tree"],
            "host_boot_id": proof["host_boot_id"], "host_output_directory": proof["paths"]["output"],
            "memory": memory, "numeric_producer_called": False, "receipt_gate_called": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "start", "container-preflight"))
    parser.add_argument("--repo")
    parser.add_argument("--custody")
    parser.add_argument("--output")
    parser.add_argument("--launch")
    parser.add_argument("--reviewed-commit")
    parser.add_argument("--mode", choices=("preflight", "run"), default="preflight")
    args = parser.parse_args()
    if args.action == "prepare":
        require(all((args.repo, args.custody, args.output, args.launch, args.reviewed_commit)), "prepare arguments required")
        result = host_prepare(args.repo, args.custody, args.output, args.launch, args.reviewed_commit, mode=args.mode)
    elif args.action == "start":
        require(args.launch is not None, "launch directory required")
        result = host_start(args.launch)
    else:
        require(ROOT == Path("/repo"), "container only")
        result = check_before_receipt(json.loads(MANIFEST.read_text()), mode="preflight")
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
