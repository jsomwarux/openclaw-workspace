# Outreach Runtime Configuration

Mission Control keeps four outreach capabilities outside source control: mandatory review and JT decision values plus the optional atomic review-authority write/read pair. An explicitly approved install generates all four independently, validates them pairwise, and stores one versioned capability-set item with a single macOS Keychain update/add. Runtime launch injects the configured set into Next.js and synchronizes the corresponding set to local Convex. The detailed capability contract lives in `docs/operations/outreach-capabilities.md`.

## Owned files

- `scripts/outreach-keychain-helper.swift`: source for the narrow versioned-set Keychain helper.
- `scripts/outreach-runtime-secrets.mjs`: owns advisory-lock re-execution, stable-helper validation, owner-routed set/legacy reads, rotation validation, Tailscale login resolution, Next.js injection, and bounded Convex synchronization.
- `../scripts/mission-control-start.sh`: launches Next.js through the runtime wrapper.
- `../scripts/mission-control-convex-sync.sh`: launches Convex through the runtime wrapper.

The legacy compiled helper remains at `.runtime/outreach-keychain-helper`. It owns the existing review and decision Keychain items and must never be replaced, recompiled, or used for v3 set access. The v3 helper has a separate stable path, `.runtime/outreach-keychain-helper-v3`, and exclusively owns the versioned capability-set item. When v3 is absent, the wrapper privately compiles it and validates its silent v3 probe before publication. It atomically renames the owner-only `.runtime/outreach-keychain-helper-v3.sha256` stamp first and the helper last. A crash between those renames leaves no published helper and is safely recompilable; no set can be installed until both published artifacts validate. Once v3 exists, a protocol or source-stamp mismatch fails closed with explicit version-bump/migration guidance; it is never replaced in place because doing so could invalidate Keychain ACL ownership.

Every helper validation, capability read, explicit install, and Convex sync is re-executed under macOS `/usr/bin/lockf` using the owner-only regular file `.runtime/outreach-capability.lock`. The internal mode requires a guarded flag and environment marker. The advisory lock is kernel-released when the process exits or dies, avoiding stale directory locks. For `run-next` and `run-convex`, the parent creates private pipe file descriptor 3; the locked child requires that writable descriptor and returns the environment only through it. Standard output and standard error never carry capability serialization, and a forged internal invocation without the private descriptor fails before any helper or Keychain access. Values never appear in arguments, inherited terminal output, or logs. Helper commands, compilation, lock acquisition, and Convex fetches all have bounded timeouts.

## Configuration sequence

This sequence rotates all four capabilities and therefore requires the explicit configuration approval boundary.

1. From `mission-control/`, run `node scripts/outreach-runtime-secrets.mjs install`. This migrates any legacy installation by writing one new v1 capability-set item; it does not update four independent items.
2. Start the approved local Convex service.
3. Run `node scripts/outreach-runtime-secrets.mjs sync-convex`.
4. Restart the approved Mission Control Convex and Next.js services.
5. Verify the dashboard and task API return 200.
6. Verify protected outreach routes return 401 without a capability.
7. Run the synthetic no-send proof before enabling any caller.

The helper never prints capability values during install or service startup. Do not add a plaintext fallback, log environment values, or pass any capability through a command argument.

## Failure behavior

- Missing v3 helper: privately compile and validate, then publish its stamp first and stable helper path last without touching legacy bytes. A stamp-only interrupted publish is recoverable by recompilation.
- Existing v3 protocol/source-stamp mismatch: fail closed. Do not overwrite it; ship a new versioned helper path and explicit migration instead.
- Missing or blank mandatory value, a partial authority pair, a present-but-blank authority value, or any collision: refuse service launch and synchronization.
- Both authority values absent: launch Next.js without authority variables and send explicit Convex deletion changes for both authority capabilities and the verifier actor ID, clearing stale direct-Convex authorization while preserving existing review/decision services.
- Missing versioned set: v3 reports absence, then the unchanged legacy helper reads only its own review and decision items under the same advisory lock; authority remains absent. A later explicit install writes the set through stable v3.
- Failed explicit rotation: preserve the prior set because rotation uses one Keychain item update/add; never fall back to partially updated individual items.
- Contended or timed-out advisory lock/helper/Convex operation: fail closed. Process death releases the kernel lock automatically; retry only after confirming the prior process ended.
- Missing Tailscale identity: refuse Next.js launch for the decision surface.
- Missing local Convex authority: refuse synchronization.
- Unknown downstream errors: return sanitized failures; never echo capability-bearing context.
