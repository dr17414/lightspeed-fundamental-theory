# Item-7 Vultr host amendment — non-executable review draft

The old resource manifest pins EPYC 9V74, the August Python build, CPU quota 8,
and an 8 GiB cgroup memory limit. These pins reject the user's new Vultr host.
This draft proposes the measured replacement profile after three reported
90-minute Docker survival passes. It keeps the runner's actual manifest unchanged
until the image, evidence and exact-head review are complete.

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

User-pasted report shows all three runs PASS, 541 heartbeats each, elapsed
5400.004671048 / 5400.004532353001 / 5400.004529451 s; maximum heartbeat gaps
10.00118532200031 / 10.0008130540009 / 10.00081466499978 s. Same reported boot/image,
no OOM/restart, exit code 0. Each run has a live observation in a genuinely later
conversation turn; the raw evidence retains exact tags and timestamps. Ephemeral boot/container/PID
identities and absolute per-run timestamps are omitted from this public summary
and kept in user-hosted evidence for private independent review.
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

1. Receive and independently audit original series.json, protocol files, all
   heartbeat/observation JSONL, summaries, Docker registration/profile/logs;
   retain archive SHA-256. Posted summary is explicitly not the raw archive.
2. Build formal campaign image with pinned NumPy 2.3.5, SciPy 1.17.0,
   threadpoolctl 3.6.0, exact Python build and reviewed source. Freeze full
   campaign image/config digest and registry digest only if available. Verify
   dependency/runtime and Docker resource/lifecycle identity without timed probes.
3. Define/review how the host launcher verifies image and runtime before receipt
   gate; current campaign.check_runtime does not enforce Docker image identity.
   Do not mistake metadata in a candidate for implemented enforcement.
4. Confirm planned uninterrupted 60000-second window and actual campaign memory
   preflight on the operator-controlled host. Survival tests alone do not prove it.
5. Claude independently reviews the exact amended head, all preserved caps and
   comparability language. Promote a complete candidate into the executable
   manifest only after blockers are resolved. Recheck hash/source pins and CI.
6. After new executable manifest merges, retire the old external receipt bound to
   the old commit/manifest hash and obtain a new receipt bound to the reviewed
   new commit/tree/manifest, host, image and unique repo-external output directory.
   No old receipt may be used on Vultr; no receipt gate was called by this draft.

The scientific screen remains unauthorized, items 8/9/10/12 OPEN and item 11
DRAFT; 6a-E remains PREREGISTRATION-INCOMPLETE. No scientific status is closed here.
