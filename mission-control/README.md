# 🌿 Mission Control

Central dashboard for JT & Eve.

## First-Time Setup (5 minutes)

### 1. Install dependencies
```bash
cd ~/.openclaw/workspace/mission-control
bun install
```

### 2. Set up Convex locally (no account needed)
```bash
npx convex dev --local
```
This runs Convex entirely on your machine — no account, no cloud, no browser login.
State is stored in `~/.convex/`. It writes `.env.local` automatically.

**Keep this terminal running** — it syncs your schema and serves the local backend.

### 3. Start the app (new terminal)
```bash
bun run dev
```

Open [http://localhost:3000](http://localhost:3000)

---

## After Initial Setup

Every time you want to use it, two terminals:
```bash
# Terminal 1 — Convex local backend
npx convex dev --local

# Terminal 2 — Next.js
bun run dev
```

---

## Eve Writes Tasks

While the app is running, Eve can add tasks programmatically:

```bash
curl -X POST http://localhost:3000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Research Nash Satoshi niche expansion","assignee":"eve","priority":"high","project":"Nash Satoshi"}'
```

---

## What Each Section Does

| Section | Data Source | Real-time? |
|---------|------------|-----------|
| Overview | Convex + local files | ✅ tasks |
| Tasks | Convex | ✅ yes |
| Schedule | `~/.openclaw/cron/jobs.json` | Refresh only |
| Memory | `~/.openclaw/workspace/memory/` | Refresh only |
| Agents | Static definitions in `api/agents/route.ts` | No |
| Monitor | Configurable (placeholder) | — |
| Costs | Configurable (placeholder) | — |
| Audit Trail | `~/.openclaw/workspace/proofs/` | Refresh only |
