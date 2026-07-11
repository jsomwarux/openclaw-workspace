# CLAUDE.md — Mission Control

## Project Overview
**Name:** Mission Control  
**Type:** Internal dashboard web app  
**Stack:** Next.js 15 (App Router) · TypeScript · Convex · Tailwind CSS  
**Purpose:** Central hub for JT and Eve — tasks, crons, memory browser, agent team, audit trail

## Architecture

```
app/
  page.tsx           — Overview dashboard
  tasks/page.tsx     — Kanban task board (Convex real-time)
  calendar/page.tsx  — Cron jobs / scheduled tasks (reads ~/.openclaw/cron/jobs.json)
  memory/page.tsx    — Memory browser (reads ~/.openclaw/workspace/memory/)
  agents/page.tsx    — Agent team view (reads /api/agents)
  monitor/page.tsx   — Deployment monitor (placeholder, needs config)
  costs/page.tsx     — Cost dashboard (placeholder, needs config)
  audit/page.tsx     — Audit trail (reads ~/.openclaw/workspace/proofs/)
  api/
    tasks/route.ts   — HTTP API for Eve to write tasks via curl
    cron/route.ts    — Reads ~/.openclaw/cron/jobs.json
    memory/route.ts  — Reads workspace memory files
    proofs/route.ts  — Reads proofs JSONL files
    agents/route.ts  — Static agent definitions (update when new agents created)
convex/
  schema.ts          — Tasks table definition
  tasks.ts           — CRUD mutations and queries
components/
  Sidebar.tsx        — Fixed left nav
  ConvexClientProvider.tsx
lib/
  utils.ts           — cn(), formatRelative(), formatDate()
```

## Development Commands

```bash
# First-time setup
bun install
npx convex dev --local  # Runs Convex locally, no account needed

# Daily dev — two terminals
npx convex dev --local  # Terminal 1: keeps Convex backend running
bun run dev             # Terminal 2: Next.js on localhost:3000
```

## How Eve Writes Tasks

```bash
# Create a task
curl -X POST http://localhost:3000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Task title","assignee":"eve","priority":"high","project":"Consulting"}'

# Update task status
curl -X PATCH http://localhost:3000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"id":"<convex-id>","status":"done"}'

# List tasks
curl http://localhost:3000/api/tasks
```

Task descriptions with links should put each URL on its own line under a short label. The task board renders URLs as clickable links and uses `overflow-wrap: anywhere`; do not rely on one long sentence of inline Drive links.

`npm run build` must not write to the live `.next` directory while the LaunchAgent is running `next dev`; it uses `NEXT_DIST_DIR=.next-build` for isolated verification builds. If a manual build ever causes `Cannot find module './*.js'` from `.next/server/webpack-runtime.js`, recover with `launchctl kickstart -k gui/$(id -u)/com.openclaw.mission-control-next`.

After Slice 1, `/work` is the primary task lane. `/tasks` must redirect to `/work`; the old Kanban board lives at `/legacy/tasks`. Do not include legacy routes like `/tasks` as active aliases for primary lanes, or mobile will show legacy UI while highlighting the redesigned lane.

After Slice 1.1, `/consulting` is the primary Revenue cash-path cockpit, backed by North Star, pipeline, and active task data through `lib/mission-control/revenue.ts` and `/api/revenue`. The old consulting strategy screen lives at `/legacy/consulting`; do not restore it as the primary Revenue lane.

The `/work` lane must expose task status changes directly on mobile rows. Keep Todo/Doing/Done controls visible and backed by `PATCH /api/tasks`; do not hide status changes behind the small colored indicator.

The `/work` lane must sort by task importance before recency: high priority before medium before low, active/problem states before done within a priority tier, then newest updated as the tie-breaker. Priority must be visually encoded with distinct badges/rails so mobile users can scan importance without opening a task.

The `/work` inspection drawer is now an action surface, not a read-only note. Keep ranking explanation, evidence/context, status controls, priority controls, Defer, and Archive together in the drawer, all backed by `PATCH /api/tasks`.

The Command cockpit must include an attention brief, not a placeholder "last seen" block. Keep the `/` brief backed by `lib/mission-control/command-brief.ts`, summarizing top action, latest proof, urgent JT count, revenue pressure, and risk count from current signals.

After Slice 1.4, `/ship` is the primary Ship lane. `/vibe` redirects to `/ship`, and the old Vibe Marketing reference lives at `/legacy/vibe`. Do not restore `/vibe` as the primary Ship surface. The Ship lane should stay focused on app distribution, content shipping, release gates, proof coverage, and blocked/stale work from current Mission Control signals.

After the 2026-07-09 fix, `/passive-income` remains a live Ship subpage and must stay discoverable from the `/ship` cockpit. It is a decision board over `memory/passive-income/`, not a legacy redirect: keep ranked ideas, score rationale, scorecard dimensions, source file, search/filter/sort controls, and expanded detail fields visible.

After Slice 1.5, `/machine` is the primary Machine lane. `/agents` redirects to `/machine`, and the old Agent Team reference lives at `/legacy/agents`. Do not restore `/agents` as the primary Machine surface. The Machine lane should stay focused on cron health, agent posture, cost pressure, automation risks, and recent system work from current Mission Control signals.

After Slice 1.6, `/evidence` is the primary Evidence lane. `/audit` redirects to `/evidence`, and the old Audit Trail reference lives at `/legacy/audit`. Do not restore `/audit` as the primary Evidence surface. The Evidence lane should stay focused on buyer-readable proof, system receipts, content proof assets, and proof gaps from current proof signals.

After Slice 1.7, `/health` is the primary Health lane. `/monitor` and `/costs` redirect to `/health`, and the old Deployment Monitor and Cost Dashboard references live at `/legacy/monitor` and `/legacy/costs`. Do not restore `/monitor` or `/costs` as primary Health surfaces. The Health lane should stay focused on ops failures, cost pressure, stale risk, and recovery work from current signals and cost data.

## Cockpit contract

The `/` cockpit renders four bands, in this order:
1. **Cash strip** — one full-width line: collected / $10K gate / weighted / days left.
2. **NOW** — exactly one card, the top `commandQueue` item, at roughly triple the visual weight of anything else on the page.
3. **UP NEXT** — queue items 2–7 as compact rows, first reason chip and age only.
4. **Three collapsed strips** — Waiting on others, Eve has it, Risk (Risk renders only when its count is above zero).

No numeric score renders on the cockpit. Rank is communicated through reason-code chips (`lib/mission-control/reason-codes.ts`), never a number. The score itself appears only inside `InspectionDrawer`, beside the full reasonCodes list and the task's `priorityAudit` trail.

Primary nav is three lanes: **Cockpit** (`/`), **Money** (`/consulting`), **Systems** (`/machine`, aliasing the machine, evidence, and health surfaces). `/work`, `/ship`, `/evidence`, and `/health` remain live routes reachable from their cockpits, but they are not nav entries. Do not re-add them to the nav.

## Architecture Decisions

- **Convex for tasks only** — real-time sync, both JT and Eve can write, persists across sessions
- **File system API routes** — memory, cron, proofs are read-only from local files; no sync needed
- **Dark theme throughout** — emerald accent (#10b981), near-black background (#0a0a0a)
- **No authentication** — localhost only, no auth needed

## Adding a New Agent

1. Update `app/api/agents/route.ts` → add to AGENTS array
2. Update `MEMORY.md` → add to "Active Agents" section

## Adding Monitor/Cost Data

- `app/api/monitor/route.ts` — add VM, wallet, domain data sources
- `app/api/costs/route.ts` — wire to OpenClaw token logs or manual tracking

## Code Style

- TypeScript strict mode
- `cn()` for className composition
- Tailwind only — no CSS modules
- Client components: "use client" at top
- Server API routes: in `app/api/`
- Minimal deps: lucide-react for icons, date-fns for dates, clsx+twMerge for classnames

## Started
2026-02-21 · Owner: JT
