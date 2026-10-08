# Item-7 Vultr host amendment — non-executable review draft

The old resource manifest pins EPYC 9V74, the August Python build, CPU quota 8,
and an 8 GiB cgroup memory limit. These pins reject the user's new Vultr host.
This draft proposes the measured replacement profile after three independently
audited 90-minute Docker survival passes. It keeps the runner's actual manifest
unchanged until the campaign image, launcher and exact-head review are complete.

## Base and changed files

Base: `4ef42fefc9fc5c2915afa7fd15c5162e3abcbbca`, tree
`4e2434e9806865f981f869ba3012b7ba044e7fc7` (merged PR #63).
Candidate: `docs/stage5c_e4_v02_vultr_host_manifest_candidate.json`.
Reported summary: `docs/stage5c_e4_v02_vultr_stub_reported_summary.json`.
No numerical/runner code, existing manifest, source pins, fixtures, solver
reference, evidence, job definitions, global/per-job caps, seed namespace,
arm ledger, endpoint or candidate kernel changes. Authorization remains NONE.
The candidate is not read by campaign.MANIFEST and is explicitly not promotable.

## Proposed host

Ubuntu 26.04 on the new user-controlled development host.
CPU model `AMD EPYC-Turin Processor`; CPUs 0/1 are SMT siblings: one physical
core, two logical CPUs. Supervisor CPU1 and worker CPU0 contend for physical
execution resources. Python build is exactly
`3.12.14 (main, Sep 29 2026, 15:01:18) [Clang 22.1.3 ]`.
Private cgroup v2 view: cpu.max `200000 100000`, memory.max `6442450944`,
memory.swap.max `0`; affinity [0,1]. No host swap, detached Docker daemon lifecycle,
foreground supervisor under init, no automatic restart, preserved output bind.
The old host's cgroup interfaces are reproduced, not its quotas/capacity.

The frozen stub image config digest is
`sha256:cd5a5b67382691aa7affdf89e8bd93312dde268a96ec099481175dddec9978eb`.
Its base registry digest is
`ubuntu@sha256:f144425ff09be612d6d9ad965196e9cdc23dae1f42110a8a11a3e9a8198759f7`.
Digest kinds are distinct. The local inspect RepoDigests string is retained by
raw evidence; its presence does not establish registry publication or supply a
campaign-image manifest digest. The stub contains no numerical dependencies.
Formal campaign image digest fields are null, never filled with the stub digest.

## Survival evidence and limits

The received raw archive has SHA-256
`bcd74b5297b4689cc0ee4ee841820b42dc0b76d7af9e0d4a56d3e415ce7f5adf`.
Independent audit of series/protocol files, complete heartbeat and observation
JSONL, summaries, container profiles and registrations against frozen source
pins and the stub assessor confirms three PASS results. Every elapsed and gap
value below matches the raw records exactly.

Each run has 541 complete heartbeats over 5400 seconds, elapsed
5400.004671048 / 5400.004532353001 / 5400.004529451 s; maximum heartbeat gaps
10.00118532200031 / 10.0008130540009 / 10.00081466499978 s. Boot ID is unchanged
across all three runs; image is identical, no OOM/restart, exit code 0.
The full heartbeat sequences and unchanged boot ID are the primary evidence of
continuous survival within each run. Later-turn live observations occurred about
121, 46 and 164 seconds after launch, respectively, and meet the formal criterion.
On a self-managed VM, process lifetime is independent of chat lifetime; these
early observations do not establish a causal connection to conversation turns.
Ephemeral boot/container/PID identities, exact tags and absolute timestamps
remain in private raw evidence and are omitted from this public summary.
The duplicate start rejection before round-3 observation did not create a failed
new attempt or alter the three recorded runs. The current stub streak display
counts a running incomplete attempt as zero; final closed series correctly says
three. Preserve that tested source rather than edit it during a frozen series.

These are three separate 90-minute observations, not one continuous 4.5-hour run,
not a 60000-second availability guarantee, and not numeric performance evidence.
All timings on the new profile remain cross-profile diagnostic only; old training
rows cannot be silently treated as hardware-comparable validation data. Existing
model-reference checks and their possible failures remain unchanged.

## Memory consistency

6 GiB = 6442450944 bytes. Aggregate parent+child RSS cap stays 2.5 GiB =
2684354560 bytes. Arithmetic remainder is 3.5 GiB = 3758096384 bytes, exceeding
3 GiB by 0.5 GiB. Original memory_preflight still requires
min(cgroup cap-current usage, host MemAvailable) >=3221225472 before allocation.
Preparation snapshot reported 6429761536 bytes minimum actual headroom.
That snapshot belongs to the stub preparation container, not the later campaign.
This is static consistency, not an ongoing 3 GiB reservation at peak RSS;
page cache, kernel memory and container processes also count against cgroup.
Child RSS 2 GiB, aggregate RSS 2.5 GiB and minimum preflight headroom 3 GiB remain
unchanged. Virtual address-space cap 32 GiB is not a physical memory allowance.

## Remaining exact-head review prerequisites

Raw archive receipt, hash and independent survival audit are complete. Claude's
independent review of head `8b20a15d` found no blocking issue; the evidence and
wording corrections in this revision still need exact amended-head review.

1. Build formal campaign image with pinned NumPy 2.3.5, SciPy 1.17.0,
   threadpoolctl 3.6.0, exact Python build and reviewed source. Freeze full
   campaign image/config digest and registry digest only if available. Verify
   dependency/runtime and Docker resource/lifecycle identity without timed probes.
2. Define/review how the host launcher verifies image and runtime before receipt
   gate; current campaign.check_runtime does not enforce Docker image identity.
   Do not mistake metadata in a candidate for implemented enforcement.
3. Confirm planned uninterrupted 60000-second window and actual campaign memory
   preflight on the operator-controlled host. Survival tests alone do not prove it.
4. Claude independently reviews the exact amended head, all preserved caps and
   comparability language. Promote a complete candidate into the executable
   manifest only after blockers are resolved. Recheck hash/source pins and CI.
5. After new executable manifest merges, retire the old external receipt bound to
   the old commit/manifest hash and obtain a new receipt bound to the reviewed
   new commit/tree/manifest, host, image and unique repo-external output directory.
   No old receipt may be used on Vultr; no receipt gate was called by this draft.

## Next PR: formal measurement container acceptance

The operator builds and tests the image over SSH and returns the outputs. The
next PR must implement and demonstrate the following before manifest promotion:

- Include Git and mount a complete clean checkout at `/repo:ro`, including its
  usable `.git` directory. A worktree pointer into an unmounted host path is not
  sufficient. Run the exact `git rev-parse HEAD` and `git status --porcelain`
  checks used by `check_receipt` under the final read-only mount and UID. Require
  the reviewed HEAD and empty status. Test any ownership/safe.directory or
  optional-lock configuration explicitly; do not assume read-only Git works.
- Keep the container root read-only and provide `--tmpfs /tmp` with a reviewed
  size bound. Smoke-test pinned NumPy/SciPy imports and writable temporary files
  with the final flags. Count tmpfs use against the same 6 GiB cgroup limit.
- Explicitly pass all six variables with `-e NAME=1`:
  `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`,
  `BLIS_NUM_THREADS`, `VECLIB_MAXIMUM_THREADS`, `NUMEXPR_NUM_THREADS`.
  Verify their effective values and threadpoolctl limits inside the container.
- Bind the receipt read-only and output writable from separate host directories
  outside the repo, for example `/custody/receipt.json:ro` and `/output:rw`.
  The receipt's `output_directory` must equal the container-visible resolved
  path used by the runner. Test mount resolution and permissions with dummy
  files; avoid invoking the real receipt gate during image smoke checks.
- Verify the exact campaign image/config digest, source pins, dependency/build
  versions, CPU affinity, cgroup limits and lifecycle before any receipt gate.
  Retain smoke evidence separately from campaign authorization and timed data.

The scientific screen remains unauthorized, items 8/9/10/12 OPEN and item 11
DRAFT; 6a-E remains PREREGISTRATION-INCOMPLETE. No scientific status is closed here.
