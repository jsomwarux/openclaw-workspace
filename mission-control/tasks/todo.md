## Plan — Mission Control redesign slice one (`/cockpit`) — 2026-10-03
Branch: claude/mc-redesign-slice-1 · Base: e5b9943 · Writer: claude-code · Plan and decisions: `tasks/implementation-notes.md`
- [x] Bundle committed unchanged; overrides recorded in DECISIONS section 0 (Confirmed 2026-10-03).
- [x] Phase 0 read-only check of the bundle against the backend; three questions asked and answered.
- [x] Test first: eligibility, order and tie-break, exceptions, slot lifting, action matrix, answer before Complete, Defer limits, run transitions 1 to 11, keyboard (no key for Approve/Reject), writes and retry, controller.
- [x] UI at `/cockpit`, desktop and 390 px, every designed state; Sidebar hidden on `/cockpit` only.
- [x] Verify: full suite, tsc, isolated build, diff check, browser interaction checks, mutation checks, screenshots against the prototype.
- [ ] Fresh-context review; pull request (not merged, not deployed).

## Plan — Growth OS Machine Contract v1 repair 1 (`/api/tasks/[id]` guard mapping) — 2026-09-27
Run: growth-os-mc-machine-contract-v1-repair1 · Branch: eve/growth-os-machine-contract-v1 · Start: b8903ed · Writer: claude-code
- [x] Verify clean worktree at b8903ed; baseline `bun test` 448 pass / 0 fail across 57 files.
- [x] RED — `lib/mission-control/task-id-route.test.ts` drives the real `app/api/tasks/[id]/route.ts` PATCH/DELETE with a stubbed Convex mutation: TRANSITION_REQUIRED and CLOSED → 409 on PATCH, TRANSITION_REQUIRED → 409 on DELETE, INVALID → 400, unrelated dependency error rethrown unchanged, legacy success calls and bodies unchanged. At the b8903ed route: 6 pass / 4 fail.
- [x] GREEN — wrap only the two `convex.mutation` calls with the existing `lanePacketDependencyErrorResponse`, mirroring `app/api/tasks/route.ts`. Focused: 10 pass / 0 fail; two mutation checks turn it red.
- [x] Verify: full `bun test` 458 pass / 0 fail (58 files); `tsc --noEmit --incremental false` exit 0; isolated `.next-build` build exit 0; loopback probe with Convex unreachable returns 500 with an empty body.
- [ ] Remove temporary node_modules symlink; commit explicit paths with trailers; write repair handoff; stop.

## Plan — Growth OS Machine Contract v1 (lane packets) — 2026-09-27
Run: growth-os-mc-machine-contract-v1 · Branch: eve/growth-os-machine-contract-v1 · Base: b301a84 · Writer: claude-code
- [x] Baseline before any change: full suite 329 pass / 0 fail across 51 files; `tsc --noEmit` exit 0.
- [x] RED/GREEN 1 — contract `lib/mission-control/lane-packet.ts`: typed eight-lane enum, envelope types, strict submission allowlist, forged-field and outreach-field rejection, server-derived fields, canonical payload hash, idempotent admission keyed by namespaced dedupeKey + admitted payload hash, conflict on open-different-payload or non-packet key collision.
- [x] RED/GREEN 2 — transitions `lib/mission-control/lane-packet-transitions.ts`: approval binds to current payloadHash; payload edit re-hashes and invalidates approval; external-action Done requires matching typed evidence (+ optional outcomeRef, never fabricated); reject/skip/no-action/expired closure requires a typed reason and writes no outcome; generic writes cannot done/archive/delete/reopen packets or snooze past expiry.
- [x] RED/GREEN 3 — Convex wiring: additive optional schema fields (tasks + focus); `admitLanePacket`, `transitionLanePacket`, internal `expireDueLanePackets`; guards on generic create/update/updateStatus/updatePipelineStage/upsert/remove; Convex-side capability checks. Outreach mutations untouched. (Deviation: two pinned inventory counts in `outreach-convex-contract.test.ts` updated 11→13 / 4→5; see notes.)
- [x] RED/GREEN 4 — `app/api/tasks/lane-packet/route.ts` via injected factory `lane-packet-route.ts`: POST create-only admission (`X-Lane-Packet-Capability`, 503 fail-closed, enumerated safe errors); PATCH transitions (JT identity + server-held decision capability for approve/reject/complete; producer capability or JT for skip/no-action). Generic `/api/tasks` rejects envelope fields.
- [x] RED/GREEN 5 — focus-driven scoring: focus row `mandate` + `laneCapacity`; `buildScoreContext` derives the mandate from the focus row (legacy rows keep consulting-cash, no row = none); cash/deadline/unblock/proof/risk/effort/freshness controls unchanged.
- [x] RED/GREEN 6 — single Today owner: `allocateToday` owns eligibility + sort + capacity + limit; `commandQueue` delegates; lane capacity, overflow, expiry, snooze; `commandBrief` consumes queue[0]; drawer explains Today rank from the scorer, not Priority Audit priority.
- [x] RED/GREEN 7 — fixtures: one Jobs + one LinkedIn packet admitted idempotently through the real Convex handler and rendered by the existing InspectionDrawer seven-field card (SSR render); drawer controls for approve / evidence-backed done / typed closure.
- [x] Docs: `docs/mission-control-lane-packet-contract.md`.
- [x] Verify: 448 pass / 0 fail (57 files); tsc exit 0; isolated `.next-build` build exit 0 (placeholder `NEXT_PUBLIC_CONVEX_URL=http://127.0.0.1:9`); `git diff --check` exit 0; credential scan clean; new tests clock-independent (131/131 at a shifted 2027 clock).
- [ ] Remove temporary node_modules symlink; commit explicit paths with Growth-OS-Run/Agent trailers; write handoff; stop (no push/merge/deploy).

## Plan — Dedicated Create-Only Endpoint — 2026-09-14
- [x] Add failing route tests for new/existing create-only outcomes and the legacy no-POST boundary.
- [x] Implement `POST /api/tasks/create-only` with the existing atomic mutation and explicit marker.
- [x] Preserve and regression-test ordinary `/api/tasks` behavior.
- [x] Move the injected handler factory out of the App Router module after Next rejected the non-route export, then rerun focused/full tests, TypeScript, isolated build, and final diff review.
- [x] Update verifier evidence and commit locally without external actions.

## Plan — Atomic Create-Only Task Admission — 2026-09-11
- [x] Add a failing pure-helper test proving an existing dedupe key returns its ID without patching fields.
- [x] Add a failing route-selection test proving `POST /api/tasks?mode=create-only` uses the create-only mutation while normal POST remains upsert.
- [x] Implement the minimum atomic create-only Convex mutation and explicit route mode.
- [x] Run focused tests, full `bun test`, TypeScript, and isolated `.next-build` production build.
- [x] Record exact verification evidence, commit explicit paths, push, and open PR #1 without merging.

## Plan — Today Queue Truth Reconciliation — 2026-09-10
- [x] Reproduce the cohort/Altmark rendered-order mismatch and trace task-to-signal status mapping.
- [x] Add failing regression coverage proving stored `todo` stays `todo` in Today.
- [x] Implement truthful status mapping without changing the fixed Today scorer.
- [x] Reconcile the cohort and stale Altmark task metadata from current evidence.
- [x] Verify focused tests, full Mission Control tests, TypeScript, isolated build, live API state, and rendered queue.
- [x] Run a fresh-context verifier and record its verdict verbatim.

## Plan — Today Task Metadata Correction — 2026-08-31
- [x] Reproduce the rendered-order mismatch and trace it from Today through task normalization.
- [x] Add a failing regression test for scorer metadata dropped by the task API.
- [x] Preserve supported scorer metadata in task admission and reapply the approved task updates.
- [x] Verify the live computed Today queue, focused tests, and isolated build.

## Plan — Agent Operating System Integration — 2026-08-24
- [x] Add failing tests for task admission metadata, deduplicated upsert, work projections, and nightly validation parsing.
- [x] Extend Convex task schema/mutations, API preservation, adapters, and shared types with optional operating-system metadata.
- [x] Add Work projection filters and inspection detail without changing Today ranking or top-level navigation.
- [x] Repurpose the existing Overnight page and API as a read-only Nightly Validation view.
- [x] Run focused tests, TypeScript checking, and the isolated Mission Control build.
- [x] Update implementation notes with decisions, files, verification, and remaining blockers.

## Plan — Mission Control Functionality Review — 2026-08-10
- [x] Reproduce screenshot-reported Today page issues and inspect task mutation/data flow.
- [ ] Add regression coverage for primary action labels, self due-date labels, evidence-gap display, and audit value formatting.
- [ ] Patch Today page and inspection drawer so task controls persist and internal/raw fields stop leaking into the UI.
- [ ] Run unit tests, build verification, and focused browser/API checks.
- [ ] Review broader Mission Control configuration against the Aug 10 priority stack and record remaining risks.

## Plan — Passive Income Ship Lane Fix — 2026-07-09
- [x] Add regression coverage for Ship nav surfacing Passive Income and for enriched idea records.
- [x] Restore Passive Income as a visible Ship cockpit entry point.
- [x] Enrich passive-income API records with score rationale, score dimensions, source file path, freshness, and decision-quality fallbacks.
- [x] Redesign `/passive-income` as a decision board with ranked rationale, filters, score breakdown, and expanded details.
- [x] Run focused tests, build verification, and local page/API checks.

## Plan — Passive Income Scout Handoff Hardening — 2026-06-21
- [x] Add failing regression coverage for deterministic same-day Scout handoff creation.
- [x] Implement a script-first Scout handoff generator using fresh local signal files.
- [x] Patch the Scout cron prompt to create the handoff artifact before optional LLM research.
- [x] Verify handoff checks, tests, cron payload, and file budgets.

## Plan — Content Swipe Optimization Fixes — 2026-06-15
- [x] Add a deterministic @jts_14 X reference-ledger generator for swipe runs.
- [x] Generate and validate the missing 2026-06-15 ledger artifact.
- [x] Wire content distribution verification to require a valid ledger when requested.
- [x] Update content/x-research rules with the generator command and verification path.
- [x] Log the operational lesson, weekly recap, and proof after verification.

## Plan — Stop Slop Voice Guard Integration — 2026-06-07
- [x] Add regression coverage for Stop Slop gaps: false agency, narrator distance, vague declaratives, Wh-openers, pull-quote endings, and high-confidence passive voice.
- [x] Patch `scripts/jt_voice_guard.py` with enforceable checks while preserving JT-specific qualifiers and proof rhythm.
- [x] Update content voice docs and content-generation skill with the adopted delta, not the whole external skill.
- [x] Verify regression tests, good JT sample pass, syntax, proof guard, and Mission Control task state.

## Plan — JT Toolkit Synthesis — 2026-06-02
- [x] Clone and fully inventory `jsomwarux/jt-claude-toolkit`.
- [x] Compare Claude plugin output against OpenClaw skills, plugin, agents, and routing docs.
- [x] Add the missing high-value portable skills and agent manuals.
- [x] Update routing/plugin/project docs and Mission Control agent registry.
- [x] Validate frontmatter/plugin JSON/registry JSON and log proof.

## Plan — Screenshot Mission Control Tasks — 2026-05-27
- [x] Verify AI Ops Teardown weekly cron run, output files, delivery, and duplicate-task state.
- [x] Refactor outreach-pipeline cron into script-first deterministic stages.
- [x] Run the first Opportunity Intake Gate audit and save the report.
- [ ] Update Mission Control, daily note, weekly recap, and proof logs after each completed task.
- [ ] Run verification guards before final closeout.

## Plan — Content Pipeline Quality Audit — 2026-05-31
- [x] Map all active scrape, storage, analysis, and generation lanes by platform/niche.
- [x] Identify weak gates where references can be stale, cross-platform, cross-niche, or only prompt-asserted.
- [x] Add deterministic validation for platform/niche reference mechanics in saved content artifacts.
- [x] Patch active content generation cron prompts to require narrow filtered swipe/reference fetches and saved hook mappings.
- [x] Run content, cron, routing, and proof verification before closeout.

## Plan — Capability Routing System — 2026-05-31
- [x] Create a durable capability routing map for JT's work.
- [x] Add skills for LinkedIn corpus intake and client proof capture.
- [x] Add agent manuals for corpus maintenance and client proof packaging.
- [x] Register new agents in Mission Control.
- [x] Add project instructions for the consulting pipeline.
- [x] Scaffold a portable Codex plugin bundle only if it adds useful packaging.
- [x] Validate skills/plugin/frontmatter and log closeout.

## Plan — AI Ops Teardown Drive Sync — 2026-05-31
- [x] Add deterministic Drive upload planner for teardown + content-bank draft bundles.
- [x] Upload the latest bundle to organized Google Drive folders.
- [x] Wire weekly agent/cron instructions to run Drive sync automatically.
- [x] Verify tests, Drive upload output, prompt wiring, and bootstrap file sizes.
## Plan — Create-Only Capability Handshake — 2026-09-14
- [x] Add failing response-contract tests for created/existing create-only results and normal upsert.
- [x] Implement the smallest route response helper and wire it into POST `/api/tasks`.
- [x] Reuse the local Mission Control dependency tree via an ignored clone-local symlink; both checked-in lockfiles are stale and clean installs would create unrelated churn.
- [x] Rerun focused tests, the full Mission Control test suite, TypeScript, and the isolated build with the standard local Convex address required for page-data collection; review the final diff.
- [x] Record verifier-ready evidence and commit the bounded patch locally.
## Plan — immutable outreach decision contract — 2026-09-14
- [x] Add failing domain tests for exact candidate/draft binding and immutable JT decision.
- [x] Add the specialized Convex mutation/query without exposing decision fields to generic writes.
- [x] Add failing API contract tests and a dedicated read/write endpoint.
- [x] Add minimal approve/reject controls to eligible review cards.
- [x] Run full tests, TypeScript, production build, and diff checks.
- [x] Commit explicit paths only; do not push or deploy.

## Plan — outreach decision authority hardening — 2026-09-15
- [x] Reproduce unauthenticated JT stamping, direct mutation access, and generic review-marker forgery with hostile tests.
- [x] Require configured Tailscale JT identity for decision writes and fail closed when identity/config is absent.
- [x] Require a server capability at every Convex outreach admission/decision mutation without logging or returning it.
- [x] Add an atomic specialized outreach-review admission path and make generic task writes reject its server-owned marker.
- [x] Run focused/full tests, TypeScript, production build, and diff/security checks.
- [x] Commit explicit paths only; do not push or deploy.

## Plan — immutable outreach review snapshot — 2026-09-15
- [x] Reproduce generic updateStatus/update/upsert/delete/autoArchive mutations and archived-decision authorization.
- [x] Replace field-specific protection with a single guard that blocks every generic mutation of a server-admitted review task.
- [x] Apply the guard to every task mutation path and keep auto-archive/backfill from mutating review snapshots.
- [x] Require a non-archived exact task for outreach authorization.
- [x] Run focused/full tests, TypeScript, build, and security/diff checks.
- [x] Commit explicit paths only; do not push or deploy.

## Plan — split outreach capabilities and clean ancestry — 2026-09-15
- [x] Reproduce shared-capability privilege escalation and legacy-decision bulk mutation.
- [x] Split review-admission and JT-decision capabilities through Next and Convex.
- [x] Exclude both review markers and legacy decisions from auto-archive/backfill.
- [x] Rebuild the outreach work from current `origin/master` without unrelated ancestry.
- [x] Run clean-branch tests, TypeScript, build, security scan, and diff audit.
- [x] Commit locally without push, deployment, or environment changes.

## Plan — reject capability collisions — 2026-09-15
- [x] Reproduce equal capability authorization at review, decision, and direct mutation boundaries.
- [x] Centralize nonblank, distinct, constant-time capability validation without logging values.
- [x] Run focused/full tests, TypeScript, build, diff, ancestry, and security scans.
- [x] Commit locally without push, deployment, or environment changes.

## Plan — sanitize outreach errors and use a proven secret comparison — 2026-09-15
- [x] RED: prove admission/decision dependency errors cannot leak capability or internal details.
- [x] RED: cover equal, unequal, and different-length capability comparison with a platform cryptographic primitive.
- [x] Map only enumerated safe route errors; return a generic 500 for every unknown dependency failure.
- [x] Replace the handwritten JavaScript comparator with Web Crypto HMAC-SHA-256 verification and await it at HTTP/Convex boundaries.
- [x] Run focused/full tests, TypeScript, build, diff, ancestry, and secret-leak scans.
- [x] Commit explicit paths locally without push, deployment, or environment changes.

## Plan — immutable outreach review owner snapshot and cycle contract — 2026-09-15
- [x] Approve the embedded-task architecture, canonical request, hash domain/version, and two-cycle owner semantics before implementation.
- [x] Establish RED tests for complete persisted context, canonical hashing, field/size rejection, generic forgery, exact decision binding, and UI provenance.
- [x] Implement atomic review admission/count, persisted snapshot display, exact decision lookup, and generic lifecycle immutability.
- [x] Prove optimistic retry behavior for concurrent duplicate, distinct, and third-attempt admissions through registered handlers.
- [x] Document the exact cross-repo API contract for `jt-ops`.
- [x] Run final full tests, TypeScript, isolated production build, diff/security scans, and local commit for fresh non-builder verification.
## Plan — Outreach runtime configuration packaging — 2026-09-15
- [x] Isolate only the live Mission Control runtime/configuration delta from unrelated workspace changes.
- [x] Add RED/GREEN coverage for rebuilding the ignored Keychain helper from checked-in Swift source.
- [x] Package Keychain injection, local Convex synchronization, Tailscale identity resolution, launcher integration, and wrapped error-code handling.
- [x] Document the explicit capability rotation, synchronization, restart, and no-send verification sequence.
- [x] Run the full Bun suite, TypeScript, shell syntax, Swift compilation, production build, and diff checks.
- [ ] Obtain a fresh non-builder CONFIRM before reporting complete or pushing.
