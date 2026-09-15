# Outreach Runtime Configuration

Mission Control keeps the outreach review and JT decision capabilities outside source control. The two values are generated independently, stored in macOS Keychain, injected into Next.js at launch, and synchronized to the local Convex environment.

## Owned files

- `scripts/outreach-keychain-helper.swift`: source for the narrow Keychain helper.
- `scripts/outreach-runtime-secrets.mjs`: compiles the helper when absent, installs/reads capabilities, resolves the current Tailscale login, injects Next.js runtime values, and synchronizes Convex.
- `../scripts/mission-control-start.sh`: launches Next.js through the runtime wrapper.
- `../scripts/mission-control-convex-sync.sh`: launches Convex through the runtime wrapper.

The compiled helper lives at `.runtime/outreach-keychain-helper` and is intentionally ignored. A fresh checkout rebuilds it from the checked-in Swift source when first needed.

## Configuration sequence

This sequence rotates both capabilities and therefore requires the explicit configuration approval boundary.

1. From `mission-control/`, run `node scripts/outreach-runtime-secrets.mjs install`.
2. Start the approved local Convex service.
3. Run `node scripts/outreach-runtime-secrets.mjs sync-convex`.
4. Restart the approved Mission Control Convex and Next.js services.
5. Verify the dashboard and task API return 200.
6. Verify protected outreach routes return 401 without a capability.
7. Run the synthetic no-send proof before enabling any caller.

The helper never prints capability values during install or service startup. Do not add a plaintext fallback, log environment values, or pass either capability through a command argument.

## Failure behavior

- Missing helper: compile it from checked-in Swift source.
- Missing, blank, or equal capabilities: refuse service launch or protected work.
- Missing Tailscale identity: refuse Next.js launch for the decision surface.
- Missing local Convex authority: refuse synchronization.
- Unknown downstream errors: return sanitized failures; never echo capability-bearing context.
