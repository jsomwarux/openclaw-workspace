# Outreach Review Snapshot Contract Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Persist the exact immutable outreach review context on its Mission Control task, assign at most two server-owned review cycles atomically, and bind JT's decision to the exact snapshot hash.

**Architecture:** Replace generic task-shaped outreach admission with a typed snapshot submission. A pure domain module validates/canonicalizes/hashes snapshots and resolves atomic cycle admission; Convex stores the embedded object and derives displayed task fields. Dedicated HTTP routes expose exact POST/count/decision contracts while generic task routes stay incapable of authority writes.

**Tech Stack:** Next.js 15 route handlers, Convex mutations/queries, TypeScript, Web Crypto SHA-256/HMAC-SHA-256, Bun tests.

---

## Chunk 1: Snapshot domain and atomic admission

### Task 1: Canonical snapshot contract

**Files:**
- Modify: `lib/mission-control/outreach-review.ts`
- Modify: `lib/mission-control/outreach-review.test.ts`

- [ ] Write failing tests for exact typed fields, unknown/server-field rejection, size limits, deterministic versioned canonical hashing, and altered snapshot hashes.
- [ ] Include canonical-ID/path alias tests plus a literal golden canonical JSON/SHA-256 vector, key-order, array-order, UTF-8, lone-surrogate, and every-field hash tests.
- [ ] Run the focused test and confirm failures are caused by missing contract behavior.
- [ ] Implement validation, recursive canonical JSON, SHA-256 hashing, display derivation, and snapshot types.
- [ ] Run focused tests green.

### Task 2: Atomic two-cycle resolver

**Files:**
- Modify: `lib/mission-control/outreach-review.ts`
- Modify: `lib/mission-control/outreach-review.test.ts`

- [ ] Write failing tests for full-set validation before exact retry, cycle 1/2 allocation, reset attempts, third-attempt rejection, and corrupt server state (duplicate hash/cycle, gaps, malformed identity, >2).
- [ ] Run focused tests RED.
- [ ] Implement the pure admission resolver used inside one Convex mutation.
- [ ] Run focused tests GREEN.

## Chunk 2: Schema, mutation, and HTTP owner contract

### Task 3: Persist and query the embedded snapshot

**Files:**
- Modify: `convex/schema.ts`
- Modify: `convex/tasks.ts`
- Modify: `lib/mission-control/outreach-convex-contract.test.ts`
- Create: `lib/mission-control/outreach-convex-integration.test.ts`

- [ ] Write failing source-contract and real-handler optimistic fake-DB integration tests proving typed persistence, server-derived task fields, indexed atomic candidate/cohort query, exact response fields, read-only count state, two transactions reading the same version then retrying on write conflict, two concurrent identical submissions create one task, two concurrent distinct submissions create cycles 1/2, and a third creates nothing.
- [ ] Add direct registered Convex handler tests proving review/decision mutations and queries reject missing, wrong, and swapped capabilities before any database access.
- [ ] Run focused tests RED.
- [ ] Extend the embedded schema and implement the mutation/query using the pure resolver.
- [ ] Run focused tests GREEN.

### Task 4: Exact review HTTP contract

**Files:**
- Modify: `app/api/tasks/outreach-review/route.ts`
- Modify: `lib/mission-control/outreach-review-route.ts`
- Modify: `lib/mission-control/outreach-review-route.test.ts`

- [ ] Write failing tests for exact POST response, dropped/unknown fields, server-owned field forgery, every exact public error body/status, capability-protected read-only count state, and sanitized POST/GET dependency failures.
- [ ] Run focused tests RED.
- [ ] Implement POST/GET handlers with capability validation and exact response projection.
- [ ] Run focused tests GREEN.

## Chunk 3: Exact decision and display binding

### Task 5: Bind decision to snapshot hash

**Files:**
- Modify: `lib/mission-control/outreach-decision.ts`
- Modify: `lib/mission-control/outreach-decision.test.ts`
- Modify: `lib/mission-control/outreach-decision-route.ts`
- Modify: `lib/mission-control/outreach-decision-route.test.ts`
- Modify: `convex/tasks.ts`

- [ ] Write failing tests for missing/mismatched snapshot hash, first-decision `todo` requirement, atomic close to `done`, and exact GET/POST identity.
- [ ] Cover same-value REJECT retry after closure, reversal rejection, pending/approved/rejected/absent state projections, archived absence, decision GET capability, 404 task code, and sanitized POST/GET failures.
- [ ] Run focused tests RED.
- [ ] Extend decision types/resolvers/routes/mutation/query.
- [ ] Run focused tests GREEN.

### Task 6: Render only the persisted immutable snapshot

**Files:**
- Modify: `lib/mission-control/types.ts`
- Modify: `lib/mission-control/adapters.ts`
- Modify: `lib/mission-control/adapters.test.ts`
- Modify: `lib/mission-control/outreach-decision-display.ts`
- Modify: `lib/mission-control/outreach-decision-display.test.ts`
- Modify: `components/mission-control/OutreachDecisionControls.tsx`

- [ ] Write failing tests proving displayed subject/body/report/bindings come from the snapshot and altered generic description cannot change decision context.
- [ ] Run focused tests RED.
- [ ] Carry the complete snapshot through the adapter and render it beside controls bound to its hash.
- [ ] Run focused tests GREEN.

## Chunk 4: Regression and evidence

### Task 7: Protect generic paths and verify integration

**Files:**
- Modify as required: generic admission/upsert tests
- Modify: `lib/mission-control/task-admission.ts`
- Modify: `lib/mission-control/task-admission.test.ts`
- Modify: `lib/mission-control/task-upsert.ts`
- Modify: `lib/mission-control/task-upsert.test.ts`
- Modify: `lib/mission-control/outreach-convex-contract.test.ts`
- Modify: `convex/tasks.ts` (`updateStatus`, `update`, `remove`, `updatePipelineStage`, `autoArchive`, `backfillClientIds`)
- Modify: `CLAUDE.md`
- Modify: `tasks/todo.md`
- Modify: `tasks/implementation-notes.html`

- [ ] Add hostile regression cases for marker/snapshot/cycle forgery and update/status/archive/remove/pipeline-stage/upsert/auto-archive/backfill/bulk paths, plus unchanged create-only behavior.
- [ ] Run all focused outreach tests.
- [ ] Run `bun test`.
- [ ] Run `bunx tsc --noEmit --incremental false`.
- [ ] Run `NEXT_PUBLIC_CONVEX_URL=http://127.0.0.1:3210 bun run build`.
- [ ] Run diff, ancestry, and secret/error-leak scans.
- [ ] Commit explicit paths locally; do not push, deploy, or configure environments.
