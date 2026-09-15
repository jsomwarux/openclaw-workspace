# Mission Control Outreach Runtime Configuration Claim

**Date:** 2026-09-15
**Branch:** `eve/mc-outreach-runtime-config`
**Base:** `master@10ba8982e1fcedf8b0e09da38bfe2c15812abcff`

## Claim

The live outreach capability runtime/configuration delta is isolated into a reproducible source-controlled branch. A fresh checkout can compile the ignored Keychain helper from checked-in Swift source, inject distinct review/decision capabilities into Next.js, synchronize only those values to local Convex, derive JT identity from Tailscale, and launch the approved Mission Control services without placing capability values in source or command arguments.

## Included scope

- Keychain Swift helper source and Node runtime wrapper.
- Next.js and Convex launcher integration.
- Local Convex environment synchronization.
- Wrapped stable-error-code handling and regression coverage.
- Ignored runtime directory and configuration/recovery runbook.

## Verification evidence

- `bun test`: 204 passed, 0 failed.
- `bunx tsc --noEmit`: exit 0.
- `bash -n` on both launchers: exit 0.
- Fresh Swift helper compilation: exit 0; generated executable present.
- `bun run build`: 41 routes generated successfully using the ignored local Convex environment.
- `git diff --check`: required before commit.

## Boundaries

No capability value is committed or printed. No live capability was rotated. No service was restarted. No deployment, activation, schedule, send, or external mutation occurred.

## Verifier status

**PENDING.** A fresh non-builder must inspect the exact commit and return `CONFIRM` before this work is reported complete or pushed.
