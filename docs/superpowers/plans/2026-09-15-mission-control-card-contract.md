# Mission Control Seven-Field Card Contract Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give every Mission Control task real typed fields for why, exact steps, paste-ready prompt, paste/use destination, done condition, and append-only feedback, while preserving the existing title field and outreach immutability.

**Architecture:** Extend the existing task schema and generic task admission path with optional backward-compatible fields. Feedback is written only through a dedicated append mutation/API action so generic create/update/upsert paths cannot replace history. The inspection drawer renders the card fields and provides the feedback input for generic tasks; immutable outreach snapshots remain protected by their existing specialized contract.

**Tech Stack:** Next.js 15, TypeScript, Convex, Bun test, Tailwind CSS.

---

### Task 1: Typed card data contract

**Files:**
- Modify: `mission-control/convex/schema.ts`
- Modify: `mission-control/convex/tasks.ts`
- Modify: `mission-control/lib/mission-control/task-admission.ts`
- Modify: `mission-control/lib/mission-control/types.ts`
- Modify: `mission-control/lib/mission-control/adapters.ts`
- Test: `mission-control/lib/mission-control/task-admission.test.ts`
- Test: `mission-control/lib/mission-control/adapters.test.ts`

- [ ] Add failing tests proving exact steps, prompt, destination, and existing feedback are carried into a Signal.
- [ ] Add optional typed fields without changing legacy callers.
- [ ] Verify focused tests pass.

### Task 2: Append-only feedback owner path

**Files:**
- Modify: `mission-control/convex/tasks.ts`
- Modify: `mission-control/app/api/tasks/route.ts`
- Create: `mission-control/lib/mission-control/task-feedback.ts`
- Create: `mission-control/lib/mission-control/task-feedback.test.ts`

- [ ] Add failing tests proving blank feedback is rejected and one new entry appends without replacing prior entries.
- [ ] Add a dedicated append action; reject direct feedback replacement through generic task admission.
- [ ] Preserve outreach snapshot immutability.
- [ ] Verify focused tests pass.

### Task 3: Card renderer and feedback box

**Files:**
- Modify: `mission-control/lib/mission-control/inspection-display.ts`
- Modify: `mission-control/lib/mission-control/inspection-display.test.ts`
- Modify: `mission-control/components/mission-control/InspectionDrawer.tsx`
- Modify: `mission-control/app/page.tsx`

- [ ] Add failing display tests for all card sections.
- [ ] Render exact steps as an ordered list and prompt as copyable preformatted text with destination.
- [ ] Add a real feedback textarea/button backed by the append API.
- [ ] Verify focused tests pass.

### Task 4: Documentation and full verification

**Files:**
- Modify: `mission-control/CLAUDE.md`
- Modify: `tasks/todo.md`
- Modify: `tasks/implementation-notes.html`

- [ ] Document the seven-field contract and append-only rule.
- [ ] Run `bun test`.
- [ ] Run `bunx tsc --noEmit`.
- [ ] Run the isolated production build.
- [ ] Inspect the exact diff and secret scan.
- [ ] Commit the reviewed local branch and stop at the push boundary.
