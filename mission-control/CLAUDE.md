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
