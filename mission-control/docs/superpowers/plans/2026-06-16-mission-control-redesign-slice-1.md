# Mission Control Redesign Slice 1 Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first useful Mission Control cockpit slice: 7-lane shell, Command decision queue, Work lane, client-side signal normalization, ranking tests, inspection drawer, and durable states.

**Architecture:** Keep the current Next.js app and API routes. Add a small client-side domain layer in `lib/mission-control/` that maps existing tasks, crons, proofs, agents, and costs into normalized `Signal` objects, scores JT-owned decision items, and powers the new Command/Work screens. Defer the `/api/signals` backend abstraction until the UI proves useful with real data.

**Tech Stack:** Next.js 15 App Router, TypeScript, Tailwind CSS, Convex-backed `/api/tasks`, local file-system API routes, Bun test for pure TypeScript tests.

---

## Repo Reality

- Existing app shell: `app/layout.tsx` renders `components/Sidebar.tsx` and a left-offset `<main>`.
- Existing nav has 15 visible tabs: Overview, Tasks, Pipeline, Vibe Marketing, Passive, Schedule, Memory, Agents, Monitor, Costs, History, Audit, Overnight, Skills, Systems.
- Existing task schema supports `todo`, `in-progress`, `done`, `archived`; no native blocked/approval states.
- Existing task priority supports `high`, `medium`, `low`; no native P0/P1/P2.
- Existing APIs already exist for tasks, cron, proofs, agents, costs, pipeline, passive income, overnight, memory, and skills.
- There is no test framework configured, but Bun is installed and can run focused TypeScript tests with `bun test`.

## File Structure

- Create: `lib/mission-control/types.ts` for normalized data contracts.
- Create: `lib/mission-control/score.ts` for pure ranking logic.
- Create: `lib/mission-control/score.test.ts` for TDD coverage.
- Create: `lib/mission-control/adapters.ts` for current API shape to `Signal` mappings.
- Create: `lib/mission-control/hooks.ts` for client data fetching and state composition.
- Create: `components/mission-control/StateBlock.tsx` for empty/loading/error/stale states.
- Create: `components/mission-control/InspectionDrawer.tsx` for signal/task detail.
- Modify: `components/Sidebar.tsx` to 7-lane navigation with old-route active mapping.
- Modify: `app/page.tsx` to become the Command cockpit.
- Create: `app/work/page.tsx` as the new Work lane.
- Keep: `app/tasks/page.tsx` intact for now, reachable through redirect or legacy route if needed.

## Chunk 1: Domain Model And Scoring

### Task 1: Score Function

**Files:**
- Create: `lib/mission-control/types.ts`
- Create: `lib/mission-control/score.ts`
- Test: `lib/mission-control/score.test.ts`

- [ ] Write tests for `computeScore`, `scoreBand`, `needsJT`, and `commandQueue`.
- [ ] Run `bun test lib/mission-control/score.test.ts` and confirm tests fail because implementation does not exist.
- [ ] Implement minimal score function and queue sorter.
- [ ] Re-run `bun test lib/mission-control/score.test.ts` and confirm pass.

### Task 2: Existing Data Adapters

**Files:**
- Modify: `lib/mission-control/types.ts`
- Create: `lib/mission-control/adapters.ts`
- Test: `lib/mission-control/adapters.test.ts`

- [ ] Write adapter tests for task, cron, proof, and agent examples from current API shapes.
- [ ] Run adapter tests and confirm failures.
- [ ] Implement adapter functions without changing backend schemas.
- [ ] Re-run adapter tests and confirm pass.

## Chunk 2: Shell And Shared UI

### Task 3: Seven-Lane Sidebar

**Files:**
- Modify: `components/Sidebar.tsx`

- [ ] Replace visible nav with Command, Work, Revenue, Ship, Machine, Evidence, Health.
- [ ] Map old routes to active lanes so legacy pages still feel coherent.
- [ ] Mobile bottom nav shows Queue, Work, Revenue, Machine, Health or the closest five useful lanes.
- [ ] Keep current dark theme and existing Tailwind style.

### Task 4: Shared State And Drawer Components

**Files:**
- Create: `components/mission-control/StateBlock.tsx`
- Create: `components/mission-control/InspectionDrawer.tsx`

- [ ] Build small reusable state blocks for loading, empty, error, stale, proof gap.
- [ ] Build a drawer that can show a normalized signal with context, evidence links, raw source metadata, and disabled action placeholders.
- [ ] Keep drawer controlled by local state for Slice 1; search-param deep link can wait.

## Chunk 3: Command And Work Screens

### Task 5: Client Data Hook

**Files:**
- Create: `lib/mission-control/hooks.ts`

- [ ] Fetch tasks, crons, proofs, agents, and costs with existing API routes.
- [ ] Preserve stale previous data when a route fails.
- [ ] Return `signals`, `degraded`, `loading`, `errors`, and small revenue/health summaries.

### Task 6: Command Cockpit

**Files:**
- Modify: `app/page.tsx`

- [ ] Replace generic overview grid with Command cockpit.
- [ ] Render revenue cockpit from task/pipeline-derived approximations and cost data where available.
- [ ] Render `Needs You Now` using `commandQueue(signals)` capped at 7.
- [ ] Render `Eve Is Handling` from Eve-owned in-progress signals.
- [ ] Render `Risk & Drift` from failed cron/proof gap/stale items.
- [ ] Show state blocks for loading, empty, degraded, and error conditions.

### Task 7: Work Lane

**Files:**
- Create: `app/work/page.tsx`

- [ ] Render task-router table/cards from current task data.
- [ ] Add filters for all, JT, Eve, blocked/stale approximation, high priority.
- [ ] Support status cycling through the existing `/api/tasks` PATCH route.
- [ ] Use inspection drawer for details and evidence links.

## Chunk 4: Verification

### Task 8: Checks

**Commands:**
- `bun test lib/mission-control/score.test.ts lib/mission-control/adapters.test.ts`
- `bunx tsc --noEmit`
- `bun run build`

- [ ] Run focused tests.
- [ ] Run TypeScript check.
- [ ] Run isolated Next build using current `NEXT_DIST_DIR=.next-build` script.
- [ ] Start or verify local dev server.
- [ ] Use Playwright screenshots for desktop and mobile Command/Work pages.
- [ ] Fix overlap, blank state, or runtime errors before reporting done.
