# Outreach Runtime Configuration

Mission Control keeps four outreach capabilities outside source control: mandatory review and JT decision values plus the optional atomic review-authority write/read pair. An explicitly approved install generates all four independently, validates them pairwise, and stores one versioned capability-set item with a single macOS Keychain update/add. Runtime launch injects the configured set into Next.js and synchronizes the corresponding set to local Convex. The detailed capability contract lives in `docs/operations/outreach-capabilities.md`.

## Owned files

- `scripts/outreach-keychain-helper.swift`: source for the narrow versioned-set Keychain helper.
- `scripts/outreach-runtime-secrets.mjs`: owns the filesystem lock, source-stamped helper replacement, set/legacy reads, rotation validation, Tailscale login resolution, Next.js injection, and Convex synchronization.
- `../scripts/mission-control-start.sh`: launches Next.js through the runtime wrapper.
- `../scripts/mission-control-convex-sync.sh`: launches Convex through the runtime wrapper.

The compiled helper lives at `.runtime/outreach-keychain-helper` and is intentionally ignored. Before use, the wrapper checks both its silent v3 protocol probe and `.runtime/outreach-keychain-helper.sha256`, which must match the checked-in Swift source. A missing helper, a protocol mismatch, or a source-stamp mismatch triggers a rebuild to a private temporary executable. The wrapper validates that executable, sets owner-only permissions, and atomically renames the helper and its owner-only source stamp into place while holding the capability lock.

Every helper validation, capability read, explicit install, and Convex sync runs under the owner-only `.runtime/outreach-capability.lock`. The lock remains held from probe through use, so another cooperating runtime cannot swap the helper or rotate between related reads. Capability output is captured through private pipes only; it is never inherited by a terminal or logged.

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

- Missing or stale helper/source stamp: privately compile from checked-in Swift source, require the current silent protocol probe, and atomically replace it under the lock.
- Missing or blank mandatory value, a partial authority pair, a present-but-blank authority value, or any collision: refuse service launch and synchronization.
- Both authority values absent: launch Next.js without authority variables and send explicit Convex deletion changes for both authority capabilities and the verifier actor ID, clearing stale direct-Convex authorization while preserving existing review/decision services.
- Missing versioned set: under the same owner-only lock, read only the legacy review and decision items and treat authority as absent. A later explicit install must migrate to the single set item.
- Failed explicit rotation: preserve the prior set because rotation uses one Keychain item update/add; never fall back to partially updated individual items.
- Insecure or contended runtime lock: fail closed rather than read across generations.
- Missing Tailscale identity: refuse Next.js launch for the decision surface.
- Missing local Convex authority: refuse synchronization.
- Unknown downstream errors: return sanitized failures; never echo capability-bearing context.
