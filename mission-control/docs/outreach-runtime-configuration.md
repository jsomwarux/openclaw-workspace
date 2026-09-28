# Outreach Runtime Configuration

Mission Control keeps four outreach capabilities and two lane-packet capabilities outside source control. An explicitly approved v4 install preserves the validated existing outreach values, generates only the distinct lane-packet producer and decision values inside the Keychain helper, and stores one six-capability set with a single macOS Keychain update/add. Runtime launch injects the configured set plus the trusted JT login into Next.js and synchronizes the capabilities, but never the login, to local Convex. The detailed outreach capability contract lives in `docs/operations/outreach-capabilities.md`; the lane-packet contract lives in `docs/mission-control-lane-packet-contract.md`.

## Owned files

- `scripts/outreach-keychain-helper.swift`: source for the narrow versioned-set Keychain helper.
- `scripts/outreach-keychain-helper-v4.swift`: source for the six-capability migration helper.
- `scripts/outreach-runtime-secrets.mjs`: owns advisory-lock re-execution, stable-helper validation, owner-routed set/legacy reads, rotation validation, Tailscale login resolution, Next.js injection, and bounded Convex synchronization.
- `../scripts/mission-control-start.sh`: launches Next.js through the runtime wrapper.
- `../scripts/mission-control-convex-sync.sh`: launches Convex through the runtime wrapper.

The legacy compiled helper remains at `.runtime/outreach-keychain-helper`. It owns the existing review and decision Keychain items and must never be replaced, recompiled, or used for versioned-set access. The v3 helper remains at `.runtime/outreach-keychain-helper-v3` and exclusively owns the four-capability v1 set. The v4 helper lives at `.runtime/outreach-keychain-helper-v4` and exclusively owns the six-capability v2 set. Each version privately compiles from its pinned source, validates its silent protocol probe, publishes its owner-only source stamp before the helper, and refuses any later protocol/source mismatch. Published helpers are never replaced in place because doing so could invalidate Keychain ACL ownership.

Every helper validation, capability read, explicit install, and Convex sync is re-executed under macOS `/usr/bin/lockf` using the owner-only regular file `.runtime/outreach-capability.lock`. The internal mode requires a guarded flag and environment marker. The advisory lock is kernel-released when the process exits or dies, avoiding stale directory locks. For `run-next` and `run-convex`, the parent creates private pipe file descriptor 3; the locked child requires it to be a FIFO or socket whose device/inode identity differs from stdout and stderr, then returns the environment only through it. Regular files, terminals, missing descriptors, and aliases to stdout or stderr fail before any helper or Keychain access. Standard output and standard error never carry capability serialization. Values never appear in arguments, inherited terminal output, or logs. Helper commands, compilation, lock acquisition, and Convex fetches all have bounded timeouts.

## Lane-packet authority configuration sequence

This sequence preserves the existing four outreach capabilities and generates the two lane-packet capabilities. It requires the explicit runtime-authority configuration approval boundary.

1. From `mission-control/`, run `node scripts/outreach-runtime-secrets.mjs install`. This validates the v4 helper, current Tailscale identity, and existing four-capability set, then migrates the existing values through helper stdin. The helper generates only the two lane values and writes one new v2 capability-set item. The atomic Keychain update/add is terminal: install performs no readback or other fallible work after a successful store.
2. Start the approved local Convex service.
3. Run `node scripts/outreach-runtime-secrets.mjs sync-convex`.
4. Restart the approved Mission Control Convex and Next.js services.
5. Verify the dashboard and task API return 200.
6. Verify protected outreach and lane-packet routes return 401 without a capability.
7. Verify a JT transition against a nonexistent task returns 404, proving decision authority is configured without creating a task.
8. Confirm the exact task-ID set is unchanged. Live packet admission remains a separate approval.

The helper never prints capability values during install or service startup. Do not add a plaintext fallback, log environment values, or pass any capability through a command argument.

## Failure behavior

- Missing v3 or v4 helper: privately compile and validate the needed version, then publish its stamp first and stable helper path last without touching earlier helper bytes. A stamp-only interrupted publish is recoverable by recompilation.
- Existing v3 or v4 protocol/source-stamp mismatch: fail closed. Do not overwrite it; ship another versioned helper path and explicit migration instead.
- Missing or blank mandatory value, a partial authority pair, a present-but-blank authority value, or any collision: refuse service launch and synchronization.
- Both authority values absent: launch Next.js without authority variables and send explicit Convex deletion changes for both authority capabilities and the verifier actor ID, clearing stale direct-Convex authorization while preserving existing review/decision services.
- Missing v4 set: v4 reports absence, then v3 or the unchanged legacy helper supplies the existing outreach values; lane authority remains absent and stale lane variables are deleted. A later explicit install writes the v2 set through stable v4.
- Failed preflight or Keychain update/add: preserve the prior set because rotation uses one Keychain item update/add; never fall back to partially updated individual items. A successful terminal store is the completed rotation and cannot be reclassified as failure by post-write readback.
- Contended or timed-out advisory lock/helper/Convex operation: fail closed. Process death releases the kernel lock automatically; retry only after confirming the prior process ended.
- Missing Tailscale identity: refuse Next.js launch for the decision surface.
- Missing local Convex authority: refuse synchronization.
- Unknown downstream errors: return sanitized failures; never echo capability-bearing context.
