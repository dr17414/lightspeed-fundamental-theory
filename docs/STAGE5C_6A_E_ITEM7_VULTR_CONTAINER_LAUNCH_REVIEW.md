# Vultr image and mandatory launch checks — review draft

Base: PR #64 merge `38971dcbf9f8e0683bb4c0a4e3f6d53274d46a6e`, tree
`6918bf2edd9c5746531ac90f07dde720148b2752`. This PR proposes the complete
Vultr profile in the executable manifest with implemented launch enforcement.
It remains REVIEW-DRAFT, authorization NONE, pending independent exact-head
review and merge. No external receipt, research timing probe, scientific seed,
arm ledger, endpoint or K is created/consumed/run. The PR #64 candidate file is
retained unchanged as historical review evidence.

## Audited image evidence

Received archive SHA-256:
`25089234215b3668f0ee0b45496318a6732f24e51c81b1f61a2f4ae5b4911f91`.
The independent reviewer matched all eight package source hashes in SHA256SUMS
and build-lock.json against the separately delivered package and read the PASS
implementation. Seven source files are absent from this archive but present in
that audited package; this is not an unresolved source-identity blocker.
The manifest retains these hashes in host_amendment.image_smoke.package_sources.

Build checkout is the base commit/tree above. NumPy 2.3.5, SciPy 1.17.0 and
threadpoolctl 3.6.0 are hash-locked with 137 allowed wheel hash entries and
installation requires hash verification. Base registry digest:
`ubuntu@sha256:f144425ff09be612d6d9ad965196e9cdc23dae1f42110a8a11a3e9a8198759f7`.
Exact local image/config ID:
`sha256:cf5c2502a59f57f2156be75c928c0c3b6db5b37e9a3f244e542662ccd5cc2f25`.
Registry manifest digest is null, RepoDigests empty; the image is unpublished.

Archived smoke exits 0 without OOM/restart. Root/repo/dummy receipt reject writes
with errno 30, output is writable, /tmp is 256 MiB tmpfs (268435456 bytes).
Git is clean/readable with complete .git and all original 34 pins match.
Python is exactly `3.12.14 (main, Sep 29 2026, 15:01:18) [Clang 22.1.3 ]`.
The dummy receipt says SMOKE-ONLY; receipt gate and numeric producer are not
called. Minimum actual headroom 6395158528 bytes is a snapshot, not a reservation.

NumPy/SciPy each load a bundled pthreads OpenBLAS 0.3.30 library, prefixes
libscipy_openblas64_ / libscipy_openblas, architecture=SkylakeX on Turin, one
thread. The manifest pins these fields and compares them before receipt read
and in every worker before numerical action. This kernel selection affects
timing; historical training and the new SMT/wheel/kernel profile remain
cross-profile diagnostics, never hardware-comparable qualification by assertion.

## Image custody and backup

The image exists only on the operator VM. Dockerfile apt-get installs Git/OS
packages without version locks (archived Git 2.53.0). Python/dependency tree
and wheel hashes record provenance but do not make the full image bit-reproducible.
VM/image deletion loses this reviewed artifact unless separately backed up.
Recommended before formal execution, with a new external backup path:

```bash
docker save --output /gpt/campaign-cf5c2502-backup.tar sha256:cf5c2502a59f57f2156be75c928c0c3b6db5b37e9a3f244e542662ccd5cc2f25
sha256sum /gpt/campaign-cf5c2502-backup.tar
```

Copy archive/hash to separate persistent storage; same-VM backup cannot protect
against VM deletion. This PR does not claim backup completion. After docker
load, verify the exact image ID and repeat launch preflight; a new host/checkout
needs the corresponding reviewed receipt. Rebuilding/different image requires
amendment, fresh evidence and independent review, never silent pin substitution.
Preserve the separately mounted complete runtime checkout as well.

## Implemented gate order

1. Host launcher prepare verifies a clean complete checkout, reviewed commit,
   all source pins, separate external custody/output/launch directories, fresh
   launch directory and unused campaign output. It creates a STOPPED container
   and checks Docker's actual inspect: image ID, entrypoint/command, UID/cwd,
   environment, CPU/memory/swap/shm, namespaces, root read-only, restart/init,
   capabilities/security, bounded tmpfs and exact bind sources/permissions.
   Extra/duplicate mounts fail closed. Only after PASS is inspection.json fsynced
   into the separate launch directory. Prepare never starts a receipt gate.
2. Host start rechecks checkout/tree/source/manifest/boot and re-inspects that
   same container, requiring status created, not running/exited/restarted.
   Only then calls docker start. Mismatch never starts the receipt-reading
   process; no auto-rebuild/image substitution/retry. Preserve rejected stopped
   containers for diagnosis.
3. Container, BEFORE opening receipt, requires /repo and read-only launch proof,
   matching hostname/container ID/boot/manifest and clean reviewed commit/tree.
   It checks effective Linux mounts, rejecting writable protected mounts and
   nested overrides, then actual CPU/SMT/affinity, cpu.max, memory.max/swap.max,
   Python build, source bytes, package versions, OpenBLAS pools and fresh memory
   headroom. Imports/inspection call no solver/producer.
4. Then read external receipt: require exact reviewed commit AND tree, image ID,
   canonical host profile hash, host boot ID, host output directory, manifest hash
   and container-visible output path.
   Keep the existing limits/runtime/memory/method/fixture preflight and job gates.

Missing proof/direct CLI outside the reviewed container rejects before receipt
read. CONTAINER-PREFLIGHT-ABORT stderr records no receipt gate, no producer, no
campaign output creation. Missing receipt argument rejects immediately without
numerical imports/resource mutations. Preflight-only mode never validates a
receipt, fits a method reference, allocates a worker or calls a numeric producer.

Operator and host Docker daemon are trusted. Read-only proof is a host inspection
handoff, not cryptographically authenticated live Docker attestation. No Docker
socket is mounted. Host admins must not docker update, replace proof/receipt or
mutate bind sources while prepared/running. Actual cgroup/mount checks do not
defeat an administrator who can forge evidence or alter the host.

## Exact-head acceptance before merge, then reviewed execution

Image Python/dependencies stay pinned; /repo:ro mounts the NEW reviewed complete
checkout. Historical smoke at the base is not execution evidence for this new
launcher. BEFORE MERGE, repeat **preflight-only** against the exact proposed
PR head/tree with final flags/proof mount and a dummy SMOKE-ONLY receipt,
running from that clean PR checkout. Return the logs/inspect/exit evidence for
independent exact-head review; manifest promotion remains review-pending:

```bash
python -m benchmarks.stage5c_e4_v02_container_launch prepare --repo /gpt/reviewed-checkout --custody /gpt/preflight-custody --output /gpt/preflight-output --launch /gpt/preflight-launch --reviewed-commit REVIEWED_PR_HEAD_SHA --mode preflight
python -m benchmarks.stage5c_e4_v02_container_launch start --launch /gpt/preflight-launch
```

Directories must exist, preflight-launch be empty, custody contain receipt.json.
Retain Docker logs, inspect and exit status for the printed same container ID;
require CONTAINER-PREFLIGHT-PASS and exit 0 without OOM/restart and archive it.
After this acceptance and independent review, merge the approved exact tree.
Recheck the clean merged checkout through a fresh preflight-only launch (merge
commit/manifest identity must match the new receipt). Then retire the old receipt,
issue a new external development-only receipt bound
to reviewed merge commit/tree, manifest, image and host profile, and confirm an
uninterrupted 60000-second window. Three separate 90-minute passes do not prove it.
host_profile_sha256 is SHA-256 of UTF-8 JSON of manifest.host with sort_keys=True,
separators=(",", ":"), no trailing newline. Receipt output_directory is
/output/campaign; receipt host_output_directory equals the verified launch proof paths.output
(the host parent corresponding to /output); host_boot_id equals the verified
current boot ID. These fields prevent using the same receipt on a replacement
boot or a different empty host output directory. Preserve that unique directory.
Authorized run uses fresh custody/output/launch paths and --mode run through
the same prepare/start sequence. This draft does not authorize that run.

## Preserved constraints and validation limits

All 139 jobs/order, 57600 aggregate CPU / 60000 wall seconds, per-job caps,
2 GiB child / 2.5 GiB aggregate RSS, 32 GiB address space, 3 GiB headroom,
fixtures, solver reference, training evidence, analysis and scientific
runner/registry stay unchanged. Original 33 non-campaign pins stay unchanged;
campaign pin updates for guard/runtime code, one launcher pin is added (35 total).
No refit/new data selects thresholds. Items 8/9/10/12 remain OPEN, item 11 DRAFT,
6a-E PREREGISTRATION-INCOMPLETE; no scientific status closes here.
Local negative tests and fake-Docker gate ordering are not actual Vultr launcher
execution evidence. Real revised-launcher exact-head preflight remains a BEFORE-MERGE prerequisite;
new merged-checkout/receipt identity is rechecked before formal execution.

Local validation: `python -m pytest -q tests/` → 541 passed, 5 pre-existing
warnings; targeted launcher/manifest tests → 97 passed. Local interpreter is
Python 3.12.14 (Aug 25 build), NumPy 2.3.5 / SciPy 1.17.0 / threadpoolctl 3.6.0.
It is a regression environment, not the pinned Sep 29 Vultr execution runtime.
`python verify_integrity.py` and `git diff --check` pass. CI retains its pinned
Python 3.12.13 configuration and explicitly installs pinned threadpoolctl 3.6.0
for the new pool-identity regression test; no CI result is claimed before that run completes.
