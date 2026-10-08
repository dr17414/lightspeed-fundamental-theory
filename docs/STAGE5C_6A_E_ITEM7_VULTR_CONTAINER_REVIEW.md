# Item-7 Vultr formal image and reviewed container launch path

The original executable manifest rejects the tested Vultr CPU/build/cgroup
profile. This PR replaces only its host profile and adds container_runtime
metadata plus one byte-pinned launcher. The numerical campaign/worker/methods,
139 jobs, all resource caps, 34 existing source/input pins, fixture bytes,
reference fits and scientific authorization remain unchanged. Authorization is
NONE. No resource campaign, scientific screen, seed, K, arm ledger or endpoint
is executed by this PR.

Base: PR #64 merge `38971dcbf9f8e0683bb4c0a4e3f6d53274d46a6e`, tree
`6918bf2edd9c5746531ac90f07dde720148b2752`.
The PR #64 candidate/review are historical snapshots and stay untouched; the
runner now proposed here reads the amended actual resource measurement manifest.
Its host becomes active only when this PR merges; execution additionally needs
a new reviewed external receipt and an operator-confirmed uninterrupted window.

## Independently audited original build and smoke

Archive SHA-256:
`25089234215b3668f0ee0b45496318a6732f24e51c81b1f61a2f4ae5b4911f91`.
Package SHA256SUMS and build-lock source hashes match the delivered scripts;
requirements.lock hash matches its archived bytes. Docker build output,
registration, inspect, container stdout, smoke.json and report agree.
Sanitized evidence: `stage5c_e4_v02_vultr_image_smoke_summary.json`.
Raw host IP/boot/container/PID identities, host paths and absolute timestamps
remain private; this PR does not publish the screenshot or original archive.

Formal candidate image config digest:
`sha256:cf5c2502a59f57f2156be75c928c0c3b6db5b37e9a3f244e542662ccd5cc2f25`.
Base registry digest:
`ubuntu@sha256:f144425ff09be612d6d9ad965196e9cdc23dae1f42110a8a11a3e9a8198759f7`.
The formal image differs from the previous survival stub. RepoDigests is empty;
the formal registry manifest digest remains null. No publication is claimed.
The built image contains Python/dependencies/Git and environment smoke scripts,
and uses a mounted repo. Its immutable default smoke targets the PR #64 merge.
The new launcher explicitly overrides that default with the reviewed mounted
guard; no rebuild or substitution of the pinned image is implied.

Audited profile: EPYC-Turin; Python
`3.12.14 (main, Sep 29 2026, 15:01:18) [Clang 22.1.3 ]`;
NumPy 2.3.5, SciPy 1.17.0, threadpoolctl 3.6.0; Git 2.53.0.
cpu.max is `200000 100000`, memory.max is 6442450944, memory.swap.max is 0.
All six thread variables equal 1; both NumPy and SciPy OpenBLAS pools report one
thread in default/limited contexts in supervisor and worker. The recorded BLAS
architecture string is library metadata, not the host CPU model pin.
The full read-only repo's exact Git HEAD/tree/status checks passed at the base
merge, together with all 34 existing byte pins. Root/repo/receipt writes failed
with EROFS; output write/fsync passed; campaign output leaf remained absent.
256 MiB /tmp tmpfs and 64 MiB /dev/shm are bounded inside the same 6 GiB cgroup.
Initial/final actual minimum headroom was 6425219072 / 6395158528 bytes.
Container exit was 0, OOM false, restart count 0, boot unchanged.
The evidence records receipt_gate_called=false and numeric_producer_called=false.

SMT remains one physical core shared by CPU0/CPU1. Old-profile timing/reference
rows stay diagnostic only. 6 GiB minus 2.5 GiB aggregate RSS leaves 3.5 GiB
arithmetically; the 3 GiB preflight requirement is a current snapshot, not a
continuous reservation. Cache, kernel, tmpfs and container processes also count.
Neither this short smoke nor the three 90-minute survival runs establishes a
60000-second execution guarantee or full-plan completion.

## Implemented launch checks

`tools/stage5c_vultr_container.py` is independently hashed in container_runtime;
the original 34 input pins retain their previous values.

- `plan` checks the complete clean checkout, caller-supplied reviewed commit/tree,
  all source pins, launcher hash and exact locally present amd64 image. It creates
  no container, reads no receipt and executes no campaign.
- `preflight` creates repo-external dummy custody/output/evidence directories.
  Dummy authorization is NONE and purpose ENVIRONMENT-PREFLIGHT-ONLY.
  It never calls the original campaign gate or a producer.
- Before starting either mode's container, the host uses docker create and
  inspect to check actual immutable Image, command/entrypoint, UID, working dir,
  resource/security/lifecycle flags, tmpfs, six env pins, Python/Git env and the
  three bind sources/destinations/read-write modes. It rejects already-running
  containers and rechecks clean reviewed source/boot before docker start.
- The mounted container guard verifies its manifest hash, full Git HEAD/tree/
  clean status, all source/launcher pins, unchanged boot, host CPU/SMT/Python,
  cgroup/swap, read-only root/repo/custody, writable output, bounded tmpfs,
  pinned numerical imports/single-thread pools and current >=3 GiB headroom.
  Supervisor affinity becomes CPU1 before dependency imports. The original
  worker still independently selects CPU0 through its unchanged runtime checks.
- `start` additionally requires a freshly signed repo-external receipt, a fresh
  empty output parent and explicit --confirm-uninterrupted-60000-seconds. It
  reserves the output parent before container creation, preventing silent reuse
  after a partial failure. The guard repeats the extended receipt bindings and
  execs the unchanged original campaign; that campaign then performs its own
  existing receipt/runtime/preflight checks. The new guard has no solver/probe.

The image/runtime enforcement is in this reviewed launch path, not magically
inside campaign.check_runtime. Direct invocation of the numerical module is not
the supported Docker execution path. The trusted host operator controls Docker,
mounts and the receipt; these checks are operational invariants, not remote
attestation or protection against a hostile root user. Pre-exec environment
checks precede the unchanged campaign's authoritative resource clock.

## Pending target-host acceptance before merge

The original image smoke did not run this new guard or mount this new manifest.
Unit tests and a passing base-image smoke cannot substitute for that check.
On Vultr, clone into a fresh repo-external location, detach to the exact PR head,
and use the full head/tree supplied with this PR:

```bash
git clone https://github.com/dr17414/lightspeed-fundamental-theory.git /gpt/lightspeed-container-review
cd /gpt/lightspeed-container-review
git checkout --detach REVIEWED_PR_HEAD
python3 tools/stage5c_vultr_container.py plan --expected-commit REVIEWED_PR_HEAD --expected-tree REVIEWED_PR_TREE
python3 tools/stage5c_vultr_container.py preflight --expected-commit REVIEWED_PR_HEAD --expected-tree REVIEWED_PR_TREE --evidence-directory /gpt/item7-container-preflight-evidence
tar -czf /gpt/item7-container-preflight-evidence.tar.gz -C /gpt item7-container-preflight-evidence
sha256sum /gpt/item7-container-preflight-evidence.tar.gz
```

Replace placeholders with the exact full SHAs, not main or an inferred branch
head. Do not reuse an existing checkout or evidence directory. Retain any failed
created/exited container and logs for diagnosis; do not automatically retry.
Return the plan/preflight JSON and evidence archive. This round uses only its
generated dummy receipt; no old or new real receipt is mounted.
The preflight container has a 180-second deadline; only that container is
stopped on timeout. No automatic removal, restart or retry is performed.

Claude's independent exact-head review and passing new-head Vultr preflight
are merge prerequisites. Local validation: 50 targeted tests passed (existing
resource manifest/harness/characterization plus 11 new mocked contract tests);
integrity and whitespace checks pass. No Docker execution was performed here.

## New receipt and later campaign

Only after the reviewed amendment merges: retire the old external receipt,
confirm the merged tree matches the approved one, obtain a new external receipt,
and confirm the uninterrupted 60000-second window. The original manifest hash
was `28b5e698b192b65a0d20ae00f15137816a57dc040004ee4afe7d29d5e17ee23e`;
it cannot authorize the amended manifest. Keep receipt issuance outside this PR.

The new receipt must bind authorization DETERMINISTIC-RESOURCE-DEVELOPMENT-ONLY,
reviewed_commit, reviewed_tree, manifest_sha256, container_image_config_digest,
host_boot_id, host_output_parent and output_directory. Commit/tree/hash must be
the final merged reviewed checkout and manifest bytes, not this draft's base.
host_output_parent is the canonical, unique host path of a newly created empty
directory; output_directory is the container-visible `/output/campaign`.
Receipt is a regular `receipt.json` in a separate repo-external custody directory,
mounted read-only. Output parent mounts writable. Fresh evidence is outside both.
No real receipt or boot identity is committed; no actual start command is
executed as part of review. Authorization NONE in the manifest remains a policy
statement; the external reviewed receipt is the separate execution gate.

Scientific closure remains unchanged: 6a-E PREREGISTRATION-INCOMPLETE,
items 8/9/10/12 OPEN, item 11 DRAFT. No result closes a scientific question.
