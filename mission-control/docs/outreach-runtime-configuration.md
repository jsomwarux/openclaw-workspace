# Outreach Runtime Configuration

Mission Control keeps four outreach capabilities outside source control: mandatory review and JT decision values plus the optional atomic review-authority write/read pair. An explicitly approved install generates all four independently and stores them in macOS Keychain. Runtime launch injects the configured set into Next.js and synchronizes the corresponding set to local Convex. The detailed capability contract lives in `docs/operations/outreach-capabilities.md`.

## Owned files

- `scripts/outreach-keychain-helper.swift`: source for the narrow Keychain helper.
- `scripts/outreach-runtime-secrets.mjs`: probes and rebuilds an absent or stale helper, installs/reads capabilities, resolves the current Tailscale login, injects Next.js runtime values, and synchronizes Convex.
- `../scripts/mission-control-start.sh`: launches Next.js through the runtime wrapper.
- `../scripts/mission-control-convex-sync.sh`: launches Convex through the runtime wrapper.

The compiled helper lives at `.runtime/outreach-keychain-helper` and is intentionally ignored. Before use, the wrapper executes the helper's silent versioned protocol probe. A fresh checkout builds it from checked-in Swift source, and an existing helper that lacks the current four-capability/read-optional protocol is rebuilt before any Keychain operation.

## Configuration sequence

This sequence rotates all four capabilities and therefore requires the explicit configuration approval boundary.

1. From `mission-control/`, run `node scripts/outreach-runtime-secrets.mjs install`.
2. Start the approved local Convex service.
3. Run `node scripts/outreach-runtime-secrets.mjs sync-convex`.
4. Restart the approved Mission Control Convex and Next.js services.
5. Verify the dashboard and task API return 200.
6. Verify protected outreach routes return 401 without a capability.
7. Run the synthetic no-send proof before enabling any caller.

The helper never prints capability values during install or service startup. Do not add a plaintext fallback, log environment values, or pass any capability through a command argument.

## Failure behavior

- Missing or stale helper: compile it from checked-in Swift source and require the current silent protocol probe before use.
- Missing or blank mandatory value, a partial authority pair, a present-but-blank authority value, or any collision: refuse service launch and synchronization.
- Both authority values absent: launch Next.js without authority variables and send explicit Convex deletion changes for both authority capabilities and the verifier actor ID, clearing stale direct-Convex authorization while preserving existing review/decision services.
- Missing Tailscale identity: refuse Next.js launch for the decision surface.
- Missing local Convex authority: refuse synchronization.
- Unknown downstream errors: return sanitized failures; never echo capability-bearing context.
