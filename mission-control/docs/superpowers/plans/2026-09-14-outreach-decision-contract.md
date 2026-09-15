# Outreach Decision Contract Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add one immutable JT outreach decision to an existing Mission Control review task, bound to the exact candidate and draft SHA, with a specialized write path and fail-closed read path for `jt-ops`.

**Architecture:** The existing task remains the only human decision record. A dedicated Convex mutation writes an optional `outreachDecision` object exactly once after verifying the task's `candidateId` and `draftSha256`; generic task writes cannot carry the decision. A dedicated API supports JT's approve/reject action and exact candidate/draft lookup, while the review drawer exposes the two actions only for outreach review tasks.

**Tech Stack:** Next.js 15 App Router, TypeScript, Convex, Bun tests, React/Tailwind.

---

## Chunk 1: Immutable owner contract

### Task 1: Domain rules and schema

**Files:**
- Create: `lib/mission-control/outreach-decision.ts`
- Create: `lib/mission-control/outreach-decision.test.ts`
- Modify: `convex/schema.ts`
- Modify: `convex/tasks.ts`
- Modify: `lib/mission-control/task-admission.ts`

- [x] Write failing tests for exact candidate/draft binding, first-decision immutability, same-value idempotence, rejection of reversal/mismatch, and generic-input stripping.
- [x] Run focused tests and confirm RED for missing behavior.
- [x] Implement the minimal pure resolver, schema fields, specialized mutation/query, and generic mutation identity guards.
- [x] Run focused tests and confirm GREEN.

### Task 2: Dedicated API contract

**Files:**
- Create: `lib/mission-control/outreach-decision-route.ts`
- Create: `lib/mission-control/outreach-decision-route.test.ts`
- Create: `app/api/tasks/outreach-decision/route.ts`

- [x] Write failing route-handler tests for server-owned `decidedBy`/`decidedAt`, approve/reject, exact lookup, absent/mismatch fail-closed behavior, malformed SHA, and controlled errors.
- [x] Run focused tests and confirm RED.
- [x] Implement injected GET/POST handlers and thin Convex route wiring.
- [x] Run focused tests and confirm GREEN.

## Chunk 2: Review-card controls

### Task 3: Minimal UI

**Files:**
- Create: `components/mission-control/OutreachDecisionControls.tsx`
- Create: `lib/mission-control/outreach-decision-display.test.ts`
- Create: `lib/mission-control/outreach-decision-display.ts`
- Modify: `components/mission-control/InspectionDrawer.tsx`
- Modify: `lib/mission-control/types.ts`
- Modify: `lib/mission-control/adapters.ts`

- [x] Write failing tests for review-task eligibility and immutable decided-state display.
- [x] Run focused tests and confirm RED.
- [x] Implement a small approve/reject control that calls only the specialized endpoint and renders the recorded immutable decision.
- [x] Run focused tests and confirm GREEN.

## Chunk 3: Verification and handoff

### Task 4: Full validation

**Files:**
- Modify: `tasks/todo.md`
- Modify: `tasks/implementation-notes.html`

- [x] Run all Bun tests.
- [x] Run TypeScript with no emit.
- [x] Run isolated production build.
- [x] Run `git diff --check` and inspect exact changed files.
- [x] Update implementation notes and task checklist with observed evidence.
- [x] Commit explicit paths only; do not push or deploy.
