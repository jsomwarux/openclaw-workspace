# Mission Control Lane-Packet Runtime Authority Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Provision bounded local lane-packet authority without admitting a live packet or weakening existing outreach secret handling.

**Architecture:** Add a v4 Keychain helper/set containing the existing outreach capabilities plus two new distinct lane-packet capabilities. Preserve v3 fallback, transport runtime values only over the private FD3 channel, inject the login only into Next, and synchronize only capabilities to Convex.

**Tech Stack:** Swift Security framework, Node.js 22 ESM, Bun tests, Next.js 15, local Convex, macOS Keychain and LaunchAgents.

---

## Chunk 1: Versioned capability contract

### Task 1: Specify v4 set and runtime mappings

**Files:**
- Modify: `mission-control/lib/mission-control/outreach-runtime-secrets.test.ts`
- Modify: `mission-control/scripts/outreach-keychain-helper.swift`
- Modify: `mission-control/scripts/outreach-runtime-secrets.mjs`

- [x] Add failing tests for the v4 helper path/protocol, six-field set schema, distinctness across all six capabilities, Next mapping, Convex mapping, and v3 fallback with lane variables absent.
- [x] Run the focused suite and confirm failures are caused by missing v4 behavior.
- [x] Implement the minimal v4 helper/set reader, validator, runtime mapping, and Convex changes.
- [x] Re-run the focused suite and confirm it passes.
- [ ] Commit the versioned contract.

### Task 2: Prove protected transport and failure behavior

**Files:**
- Modify: `mission-control/lib/mission-control/outreach-runtime-secrets.test.ts`
- Modify: `mission-control/scripts/outreach-runtime-secrets.mjs`

- [x] Add failing tests for inherited lane-variable removal, v4 mismatch refusal, partial/colliding set refusal, nonsecret installer arguments, and zero capability serialization to stdout/stderr.
- [x] Run the focused suite and confirm the expected failures.
- [x] Implement minimal cleanup and fail-closed behavior.
- [ ] Run focused and full Mission Control suites, TypeScript, build, and `git diff --check`.
- [ ] Commit the protected transport implementation.

## Chunk 2: Local install and runtime proof

### Task 3: Install and synchronize bounded authority

**Files:**
- Modify: `mission-control/docs/outreach-runtime-configuration.md`
- Create: `memory/job-state/handoffs/growth-os-mc-runtime-authority-v1.md`

- [ ] Record pre-change service, helper-hash, task-ID, and database rollback evidence without reading secret values.
- [ ] Run the approved `install` path so the helper generates/stores the v4 set internally.
- [ ] Run protected Convex synchronization.
- [ ] Restart only the two approved Mission Control LaunchAgents.
- [ ] Verify health, 401 for missing/wrong producer authority, 404 for a nonexistent JT transition, exact task-ID equality, and no live lane-packet rows.

### Task 4: Close proof and preserve later gates

**Files:**
- Modify: `memory/job-state/ai-workflow-growth-os.md`
- Modify: `memory/job-state/ai-workflow-growth-os-restart-handoff.md`
- Modify: `docs/superpowers/plans/2026-09-24-ai-workflow-growth-os-completion.md`
- Modify: `MEMORY.md`
- Modify: `memory/2026-09-27.md`
- Modify: `memory/weekly-recaps/current-week.md`
- Modify: `memory/content/recent-builds.md`
- Modify: `memory/content-voice.md`

- [ ] Run fresh full verification and the proof guard.
- [ ] Log the runtime-authority proof with no secret values.
- [ ] Advance the next gate to one controlled admission/replay proof; keep Decagon application and all external actions closed.
- [ ] Record exact rollback and security notes.
