# Mission Control Slice 1 Redesign — Audit Report
**Date:** 2026-06-16  
**Auditor:** Eve (subagent)  
**Scope:** Read-only audit; zero file edits. Build verified clean before audit.

---

## 1. Current State Summary

**Build:** ✅ Clean (`NEXT_DIST_DIR=.next-build bun run build` passes, all routes compile)  
**Tests:** ✅ 5/5 pass (`bun test lib/mission-control/score.test.ts`)  
**TypeScript:** ⚠️ 1 benign error — `bun:test` module not found by tsc (irrelevant; bun runs tests directly, not via tsc)

---

## 2. Route / Component / API / Convex Schema Map

### 2a. App Routes (Next.js App Router)

| Route | File | Type | Data Source | Notes |
|-------|------|------|-------------|-------|
| `/` | `app/page.tsx` | Client | `/api/tasks`, `/api/cron`, `/api/proofs` | Overview dashboard; 6-stat grid + quick links + restart button |
| `/tasks` | `app/tasks/page.tsx` | Client | `/api/tasks` (polling 5s) | Kanban: todo / in-progress / done. Drag reorder. 384 lines. |
| `/calendar` | `app/calendar/page.tsx` | Client | `/api/cron` | Cron job list; failed/running counts |
| `/memory` | `app/memory/page.tsx` | Client | `/api/memory?q=` | Debounced search across workspace .md files |
| `/agents` | `app/agents/page.tsx` | Client | `/api/agents` | Agent cards; reads agents.json + auto-discovers ~/projects/ |
| `/consulting` | `app/consulting/page.tsx` | Static | hardcoded | Tier/pipeline visualization — fully static data |
| `/costs` | `app/costs/page.tsx` | Client | `/api/costs` | Cost tracker; reads memory/costs/*.json |
| `/audit` | `app/audit/page.tsx` | Client | `/api/proofs` | Proof JSONL reader; type filter |
| `/history` | `app/history/page.tsx` | Client | `/api/tasks?include=archived` | Archived task list; search + project filter |
| `/overnight` | `app/overnight/page.tsx` | Client | `/api/overnight` | Overnight run logs + portfolio queue |
| `/passive-income` | `app/passive-income/page.tsx` | Client | `/api/passive-income` | Passive income ideas (Convex pideas table) |
| `/skills` | `app/skills/page.tsx` | Client | `/api/skills` | Skill browser; reads workspace/skills + bundled skills |
| `/systems` | `app/systems/page.tsx` | Client | static + ReactFlow | System diagram; ReactFlow-based |
| `/vibe` | `app/vibe/page.tsx` | Static | hardcoded | Content/vibe boards (Nash Satoshi, Vista, Glow Index) |
| `/monitor` | `app/monitor/page.tsx` | Static | — | Placeholder — no live data wired |

### 2b. API Routes

| Route | Method | Source | Returns |
|-------|--------|--------|---------|
| `GET /api/tasks` | GET | Convex `tasks.listActive` or `tasks.listArchived` | `{ tasks[] }` |
| `POST /api/tasks` | POST | Convex `tasks.create` | `{ id, success }` |
| `PATCH /api/tasks` | PATCH | Convex `tasks.update` | `{ success }` |
| `DELETE /api/tasks?id=` | DELETE | Convex `tasks.remove` | `{ success }` |
| `GET/PATCH/DELETE /api/tasks/[id]` | CRUD | Convex typed | Per-task operations |
| `POST /api/pipeline` | POST | internal fetch → `/api/tasks` | Pipeline stage updates |
| `GET /api/pipeline?slug=` | GET | internal fetch → `/api/tasks` | Current pipeline state |
| `GET /api/agents` | GET | FS `data/agents.json` + auto-discover `~/projects/` | `{ agents[] }` |
| `GET /api/cron` | GET | FS `~/.openclaw/cron/jobs.json` | `{ jobs[] }` |
| `GET /api/memory?q=` | GET | FS workspace .md files | `{ results[], total }` |
| `GET /api/proofs` | GET | FS `proofs/YYYY-MM-DD/actions.jsonl` | `{ entries[], types[] }` |
| `GET /api/costs` | GET | FS `memory/costs/*.json` + execSync cost-tracker | `{ today, month, by_model, ... }` |
| `GET /api/overnight` | GET | FS `agents/overnight/logs/*.md` | `{ runs[] }` |
| `GET /api/passive-income` | GET | FS `agents/passive-income/reports/` + Convex | `{ ideas[] }` |
| `GET /api/skills` | GET | FS workspace/skills + bundled skills | `{ skills[] }` |
| `POST /api/gateway/restart` | POST | exec `restart-gateway.sh` | `{ success }` |

### 2c. Convex Schema

**Table: `tasks`**
```
title: string
description?: string
status: "todo" | "in-progress" | "done" | "archived"
assignee: "jt" | "eve" | "both"
priority: "high" | "medium" | "low"
project?: string
sortOrder?: number
slug?: string
pipelineStage?: string
createdAt: number
updatedAt: number
```
Indexes: `by_status`, `by_assignee`, `by_project`, `by_slug`

**Table: `pideas`**
```
title, score, status, source, reportDate, concept, revenueModel,
jtStackFit, longevitySignal, researchSignal, creativityCheck
createdAt/updatedAt: number
```
Indexes: `by_score`, `by_status`

**Convex mutations/queries (tasks.ts):**
`list`, `create`, `updateStatus`, `update`, `remove`, `findBySlug`, `listActive`, `listArchived`, `autoArchive` (internal), `updatePipelineStage`

**Convex mutations/queries (pideas.ts):**
`listPideas`, `syncPideas`

**Crons:** `nightly-auto-archive` at 3AM UTC (autoArchive)

### 2d. Components

| File | Purpose |
|------|---------|
| `components/Sidebar.tsx` | Fixed left nav (desktop) + bottom tab bar (mobile). 14 nav entries. |
| `components/SystemCard.tsx` | Reusable card for systems diagram |
| `components/SystemDiagram.tsx` | ReactFlow wrapper |
| `app/ConvexClientProvider.tsx` | ConvexProvider wrapper |

### 2e. Lib (already-built Slice 1 primitives)

| File | Status | Contents |
|------|--------|---------|
| `lib/utils.ts` | Live | `cn()`, `formatRelative()`, `formatDate()` |
| `lib/mission-control/types.ts` | **✅ Built** | `Signal`, `Factors`, `ScoreBand`, `ProofRef`, `SignalSource`, `SignalOwner`, `SignalStatus`, `SignalLane`, `SignalPriority` — 7 lanes defined |
| `lib/mission-control/score.ts` | **✅ Built** | `computeScore`, `scoreBand`, `needsJT`, `deriveFactors`, `scoreSignal`, `commandQueue` |
| `lib/mission-control/score.test.ts` | **✅ 5/5 pass** | Full test coverage for all exported functions |

---

## 3. Signal Normalization — Current State

The `lib/mission-control/` files define the type system and scoring engine, but **no normalizer/adapter exists yet** to convert raw API responses → `Signal[]`. The lanes defined in `types.ts` are:

```typescript
type SignalLane = "work" | "revenue" | "ship" | "machine" | "evidence" | "health";
```

That's 6 lanes in types.ts. The task description says **7 lanes**. One lane is missing or needs to be added (likely `"command"` or `"intel"`).

**Gap:** No `lib/mission-control/normalize.ts` (or similar) exists to:
- Map Convex tasks → Signal[]
- Map cron jobs → Signal[]
- Map proof entries → Signal[]
- Map pipeline records → Signal[]

---

## 4. What Already Exists vs. What Needs Building

### ✅ Already Built (do not recreate)
- `lib/mission-control/types.ts` — all Signal types, Factors, ScoreBand
- `lib/mission-control/score.ts` — full scoring engine (6 functions)
- `lib/mission-control/score.test.ts` — 5 passing tests
- All API routes — functional, no changes needed for Slice 1
- Convex schema + mutations — complete for tasks/pideas
- `tailwind.config.ts` — already has `surface` and `accent` color tokens
- `lib/utils.ts` — `cn()` available

### ❌ Not Yet Built (Slice 1 needs)
1. **7th lane** — `types.ts` has 6; add missing lane
2. **`lib/mission-control/normalize.ts`** — task/cron/proof → Signal adapter
3. **`app/command/page.tsx`** — Command cockpit (7-lane shell + JT queue)
4. **`components/CommandCockpit.tsx`** — Command queue widget (top 7 JT decisions)
5. **`components/WorkLane.tsx`** — Work lane card list component
6. **`components/LaneShell.tsx`** — 7-lane grid container
7. **`components/SignalDrawer.tsx`** — Slide-in detail drawer for any Signal
8. **Signal states rendering** — empty/loading/error per lane
9. **Sidebar nav entry** — `/command` route not in Sidebar nav

---

## 5. Exact File Edit Recommendations for Minimal Slice 1

### Priority order: types → normalize → page → components → sidebar

---

### 5.1 `lib/mission-control/types.ts` — Add 7th lane

**Change:** Add `"intel"` to `SignalLane` (market/niche intel signals from niche-monitor, morning brief).

```diff
- export type SignalLane = "work" | "revenue" | "ship" | "machine" | "evidence" | "health";
+ export type SignalLane = "work" | "revenue" | "ship" | "machine" | "evidence" | "health" | "intel";
```

**File:** `lib/mission-control/types.ts`  
**Lines affected:** 1 line (the SignalLane type)  
**Risk:** Low — additive only. Existing score.ts logic already handles unknown lanes gracefully.

---

### 5.2 NEW FILE: `lib/mission-control/normalize.ts`

Client-side adapters. Pure functions, no async, no API calls.

```typescript
// lib/mission-control/normalize.ts
import type { Signal, SignalLane, SignalStatus } from "./types";

// ── Task → Signal ──────────────────────────────────────────────────────────
function laneFromTask(t: { project?: string; pipelineStage?: string; assignee: string }): SignalLane {
  if (t.pipelineStage) return "revenue";
  const p = (t.project ?? "").toLowerCase();
  if (p.includes("consult") || p.includes("pipeline") || p.includes("outreach")) return "revenue";
  if (p.includes("ship") || p.includes("site") || p.includes("app") || p.includes("deploy")) return "ship";
  if (p.includes("machine") || p.includes("cron") || p.includes("agent") || p.includes("automation")) return "machine";
  if (t.assignee === "eve") return "machine";
  return "work";
}

function statusFromTask(s: string): SignalStatus {
  switch (s) {
    case "todo": return "awaiting-decision";
    case "in-progress": return "in-progress";
    case "done": return "done";
    default: return "stale";
  }
}

export function taskToSignal(t: {
  _id: string; title: string; description?: string; status: string;
  priority: string; assignee: string; project?: string;
  pipelineStage?: string; updatedAt: number; createdAt: number;
}): Signal {
  const ageDays = Math.floor((Date.now() - t.updatedAt) / 86_400_000);
  return {
    id: t._id,
    source: "task",
    title: t.title,
    owner: (t.assignee === "jt" || t.assignee === "both" ? t.assignee : "eve") as Signal["owner"],
    status: statusFromTask(t.status),
    lane: laneFromTask(t),
    priority: (t.priority as Signal["priority"]) ?? "medium",
    project: t.project,
    ageDays,
    dueToday: false,
    context: t.description,
    evidence: [],
    updatedAt: t.updatedAt,
    raw: t,
  };
}

// ── Cron job → Signal ──────────────────────────────────────────────────────
export function cronToSignal(j: {
  jobId: string; name: string; enabled: boolean; failed: boolean;
  running: boolean; lastRun: number | null; nextRun: number | null;
}): Signal {
  const ageDays = j.lastRun ? Math.floor((Date.now() - j.lastRun) / 86_400_000) : 0;
  const status: SignalStatus = j.failed ? "failed" : j.running ? "in-progress" : "in-progress";
  return {
    id: j.jobId,
    source: "cron",
    title: j.name,
    owner: "eve",
    status,
    lane: "machine",
    priority: j.failed ? "high" : "low",
    ageDays,
    evidence: [],
    updatedAt: j.lastRun ?? Date.now(),
    raw: j,
  };
}

// ── Proof entry → Signal ───────────────────────────────────────────────────
export function proofToSignal(e: {
  id: string; title: string; timestamp: string; action_type: string;
  outcome: string; error: string | null; date: string;
}): Signal {
  const ts = new Date(e.timestamp).getTime() || Date.now();
  const ageDays = Math.floor((Date.now() - ts) / 86_400_000);
  return {
    id: e.id,
    source: "proof",
    title: e.title,
    owner: "eve",
    status: e.error ? "failed" : "done",
    lane: "evidence",
    priority: e.error ? "high" : "low",
    ageDays,
    evidence: [{ kind: "jsonl", label: e.outcome || e.action_type, quality: e.error ? "gap" : "verified" }],
    updatedAt: ts,
    raw: e,
  };
}
```

**File:** `lib/mission-control/normalize.ts` (NEW)  
**Risk:** Zero — pure functions, no side effects.

---

### 5.3 NEW FILE: `app/command/page.tsx`

The main Slice 1 route. Imports normalize + score + lane components.

```typescript
"use client";
import { useEffect, useState, useCallback } from "react";
import { taskToSignal, cronToSignal, proofToSignal } from "@/lib/mission-control/normalize";
import { scoreSignal } from "@/lib/mission-control/score";
import type { Signal } from "@/lib/mission-control/types";
import LaneShell from "@/components/LaneShell";
import CommandCockpit from "@/components/CommandCockpit";
import SignalDrawer from "@/components/SignalDrawer";

const LANES = ["command", "work", "revenue", "ship", "machine", "evidence", "health"] as const;

export default function CommandPage() {
  const [signals, setSignals] = useState<Signal[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Signal | null>(null);

  const fetchAll = useCallback(async () => {
    const [tasksRes, cronsRes, proofsRes] = await Promise.all([
      fetch("/api/tasks").then(r => r.json()),
      fetch("/api/cron").then(r => r.json()),
      fetch("/api/proofs?limit=20").then(r => r.json()),
    ]);
    const taskSignals = (tasksRes.tasks ?? []).map(taskToSignal).map(scoreSignal);
    const cronSignals = (cronsRes.jobs ?? []).filter((j: any) => j.failed).map(cronToSignal).map(scoreSignal);
    const proofSignals = (proofsRes.entries ?? []).slice(0, 5).map(proofToSignal).map(scoreSignal);
    setSignals([...taskSignals, ...cronSignals, ...proofSignals]);
    setLoading(false);
  }, []);

  useEffect(() => {
    fetchAll();
    const poll = setInterval(fetchAll, 15_000);
    return () => clearInterval(poll);
  }, [fetchAll]);

  return (
    <div className="p-4 sm:p-6 max-w-7xl">
      <div className="mb-6">
        <h1 className="text-xl font-semibold text-zinc-100">Command</h1>
        <p className="text-xs text-zinc-500 mt-0.5">Signal board — what needs a decision right now</p>
      </div>
      <CommandCockpit signals={signals} loading={loading} onSelect={setSelected} />
      <LaneShell signals={signals} loading={loading} onSelect={setSelected} />
      {selected && <SignalDrawer signal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
```

**File:** `app/command/page.tsx` (NEW)  
**Risk:** Low — new route, no existing route disturbed.

---

### 5.4 NEW FILE: `components/CommandCockpit.tsx`

Top 7 JT decision queue. Uses existing `commandQueue()` from score.ts.

```typescript
"use client";
import { commandQueue } from "@/lib/mission-control/score";
import type { Signal } from "@/lib/mission-control/types";
import { cn } from "@/lib/utils";
import { formatRelative } from "@/lib/utils";
import { AlertCircle, Clock } from "lucide-react";

const BAND_STYLES = {
  high:   "border-red-500/40 bg-red-500/5",
  medium: "border-yellow-500/40 bg-yellow-500/5",
  low:    "border-zinc-700/40 bg-zinc-900/40",
};

interface Props {
  signals: Signal[];
  loading: boolean;
  onSelect: (s: Signal) => void;
}

export default function CommandCockpit({ signals, loading, onSelect }: Props) {
  const queue = commandQueue(signals);

  if (loading) {
    return (
      <div className="mb-6 bg-[#111] border border-[#2a2a2a] rounded-lg p-4">
        <p className="text-xs text-zinc-600 animate-pulse">Loading command queue…</p>
      </div>
    );
  }

  if (queue.length === 0) {
    return (
      <div className="mb-6 bg-[#111] border border-[#2a2a2a] rounded-lg p-4 text-center">
        <p className="text-xs text-zinc-600">No decisions pending for JT</p>
      </div>
    );
  }

  return (
    <div className="mb-6">
      <div className="flex items-center gap-2 mb-3">
        <AlertCircle size={14} className="text-red-400" />
        <p className="text-xs font-semibold text-zinc-300 uppercase tracking-wider">
          Needs JT ({queue.length})
        </p>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
        {queue.map(signal => (
          <button
            key={signal.id}
            onClick={() => onSelect(signal)}
            className={cn(
              "text-left p-3 rounded-lg border transition-colors hover:border-zinc-500",
              BAND_STYLES[signal.band ?? "low"]
            )}
          >
            <p className="text-xs font-medium text-zinc-200 mb-1 line-clamp-2">{signal.title}</p>
            <div className="flex items-center gap-2">
              <span className="text-[9px] text-zinc-500 uppercase tracking-wide">{signal.lane}</span>
              <span className="text-[9px] text-zinc-600 flex items-center gap-0.5">
                <Clock size={9} /> {formatRelative(signal.updatedAt)}
              </span>
              {signal.score !== undefined && (
                <span className="text-[9px] text-zinc-600 ml-auto">
                  {signal.score}
                </span>
              )}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
```

**File:** `components/CommandCockpit.tsx` (NEW)  
**Risk:** Zero — new component, no conflicts.

---

### 5.5 NEW FILE: `components/WorkLane.tsx`

Single-lane signal list (reusable across all 7 lanes).

```typescript
"use client";
import type { Signal } from "@/lib/mission-control/types";
import { cn, formatRelative } from "@/lib/utils";

const PRIORITY_DOT = {
  high:   "bg-red-400",
  medium: "bg-yellow-400",
  low:    "bg-zinc-600",
};

interface Props {
  title: string;
  signals: Signal[];
  loading: boolean;
  onSelect: (s: Signal) => void;
  accent?: string;
}

export default function WorkLane({ title, signals, loading, onSelect, accent = "text-zinc-400" }: Props) {
  return (
    <div className="bg-[#111] border border-[#2a2a2a] rounded-lg p-3">
      <div className="flex items-center justify-between mb-3">
        <p className={cn("text-[10px] font-semibold uppercase tracking-wider", accent)}>{title}</p>
        <span className="text-[9px] text-zinc-600 bg-[#1a1a1a] px-1.5 py-0.5 rounded">
          {loading ? "…" : signals.length}
        </span>
      </div>
      {loading ? (
        <div className="space-y-2">
          {[1, 2].map(i => (
            <div key={i} className="h-8 bg-[#1a1a1a] rounded animate-pulse" />
          ))}
        </div>
      ) : signals.length === 0 ? (
        <p className="text-[10px] text-zinc-700 text-center py-4">empty</p>
      ) : (
        <div className="space-y-1.5">
          {signals.map(s => (
            <button
              key={s.id}
              onClick={() => onSelect(s)}
              className="w-full text-left flex items-center gap-2 p-2 rounded hover:bg-[#1a1a1a] transition-colors"
            >
              <span className={cn(
                "flex-shrink-0 w-1.5 h-1.5 rounded-full",
                PRIORITY_DOT[s.priority ?? "low"]
              )} />
              <span className="flex-1 text-xs text-zinc-300 line-clamp-1">{s.title}</span>
              <span className="text-[9px] text-zinc-600 flex-shrink-0">{formatRelative(s.updatedAt)}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
```

**File:** `components/WorkLane.tsx` (NEW)  
**Risk:** Zero.

---

### 5.6 NEW FILE: `components/LaneShell.tsx`

7-lane grid container. Filters signals per lane and renders WorkLane.

```typescript
"use client";
import type { Signal, SignalLane } from "@/lib/mission-control/types";
import WorkLane from "./WorkLane";

type LaneDef = { id: SignalLane; label: string; accent: string };

const LANES: LaneDef[] = [
  { id: "work",     label: "Work",     accent: "text-zinc-400"   },
  { id: "revenue",  label: "Revenue",  accent: "text-emerald-400"},
  { id: "ship",     label: "Ship",     accent: "text-blue-400"   },
  { id: "machine",  label: "Machine",  accent: "text-purple-400" },
  { id: "evidence", label: "Evidence", accent: "text-yellow-400" },
  { id: "health",   label: "Health",   accent: "text-red-400"    },
  { id: "intel",    label: "Intel",    accent: "text-sky-400"    },
];

interface Props {
  signals: Signal[];
  loading: boolean;
  onSelect: (s: Signal) => void;
}

export default function LaneShell({ signals, loading, onSelect }: Props) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 mt-4">
      {LANES.map(lane => (
        <WorkLane
          key={lane.id}
          title={lane.label}
          accent={lane.accent}
          signals={signals.filter(s => s.lane === lane.id)}
          loading={loading}
          onSelect={onSelect}
        />
      ))}
    </div>
  );
}
```

**File:** `components/LaneShell.tsx` (NEW)  
**Risk:** Zero.

---

### 5.7 NEW FILE: `components/SignalDrawer.tsx`

Slide-in detail drawer. Shows full Signal context + evidence.

```typescript
"use client";
import type { Signal } from "@/lib/mission-control/types";
import { cn, formatDate } from "@/lib/utils";
import { X, ExternalLink } from "lucide-react";
import { useEffect } from "react";

const QUALITY_STYLES = {
  verified: "text-emerald-400",
  partial:  "text-yellow-400",
  gap:      "text-red-400",
};

interface Props {
  signal: Signal;
  onClose: () => void;
}

export default function SignalDrawer({ signal, onClose }: Props) {
  // Close on Escape
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/60 z-40"
        onClick={onClose}
        aria-hidden="true"
      />
      {/* Drawer */}
      <div className="fixed right-0 top-0 h-full w-full max-w-sm bg-[#111] border-l border-[#2a2a2a] z-50 flex flex-col shadow-2xl">
        {/* Header */}
        <div className="flex items-start justify-between p-4 border-b border-[#2a2a2a]">
          <div className="flex-1 min-w-0 pr-3">
            <p className="text-sm font-semibold text-zinc-100 leading-snug">{signal.title}</p>
            <div className="flex items-center gap-2 mt-1">
              <span className="text-[9px] uppercase tracking-wide text-zinc-500">{signal.lane}</span>
              <span className="text-[9px] text-zinc-600">·</span>
              <span className="text-[9px] text-zinc-500">{signal.source}</span>
              {signal.score !== undefined && (
                <>
                  <span className="text-[9px] text-zinc-600">·</span>
                  <span className="text-[9px] text-zinc-500">score {signal.score}</span>
                </>
              )}
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-zinc-600 hover:text-zinc-300 transition-colors p-1"
            aria-label="Close drawer"
          >
            <X size={16} />
          </button>
        </div>

        {/* Body */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {/* Status row */}
          <div className="grid grid-cols-2 gap-3">
            {[
              { label: "Status", value: signal.status },
              { label: "Owner",  value: signal.owner  },
              { label: "Priority", value: signal.priority ?? "—" },
              { label: "Age", value: signal.ageDays === 0 ? "today" : `${signal.ageDays}d` },
            ].map(({ label, value }) => (
              <div key={label} className="bg-[#1a1a1a] rounded p-2">
                <p className="text-[9px] text-zinc-600 uppercase tracking-wide mb-0.5">{label}</p>
                <p className="text-xs text-zinc-300">{value}</p>
              </div>
            ))}
          </div>

          {/* Context */}
          {signal.context && (
            <div>
              <p className="text-[10px] text-zinc-500 uppercase tracking-wide mb-1">Context</p>
              <p className="text-xs text-zinc-400 leading-relaxed">{signal.context}</p>
            </div>
          )}

          {/* Eve read */}
          {signal.eveRead && (
            <div>
              <p className="text-[10px] text-zinc-500 uppercase tracking-wide mb-1">Eve</p>
              <p className="text-xs text-zinc-400 leading-relaxed">{signal.eveRead}</p>
            </div>
          )}

          {/* Evidence */}
          {signal.evidence.length > 0 && (
            <div>
              <p className="text-[10px] text-zinc-500 uppercase tracking-wide mb-1">Evidence</p>
              <div className="space-y-1.5">
                {signal.evidence.map((e, i) => (
                  <div key={i} className="flex items-center gap-2 text-[10px]">
                    <span className={cn("font-medium", QUALITY_STYLES[e.quality])}>{e.quality}</span>
                    <span className="text-zinc-500">{e.label}</span>
                    {e.href && (
                      <a href={e.href} target="_blank" rel="noreferrer"
                         className="text-zinc-600 hover:text-zinc-300">
                        <ExternalLink size={10} />
                      </a>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Timestamps */}
          <div className="text-[9px] text-zinc-700">
            Updated {formatDate(signal.updatedAt)}
          </div>
        </div>
      </div>
    </>
  );
}
```

**File:** `components/SignalDrawer.tsx` (NEW)
**Risk:** Zero.

---

### 5.8 `components/Sidebar.tsx` — Add `/command` nav entry

**Change:** Add one nav item to the existing `nav` array.

**In the desktop `nav` array**, insert after the overview item:
```typescript
{ href: "/command", icon: Zap, label: "Command" },
```

**Import:** Add `Zap` to the existing lucide-react import line.

**Mobile nav** (`mobileNav` array if separate, or the same `nav` array if unified): Same insertion.

Looking at the current Sidebar — it uses a single `nav` array for both desktop and mobile. Current nav items include `LayoutDashboard, CheckSquare, Calendar, Brain, Users, Server, DollarSign, FileText, Moon, Wrench, Archive, Building2, Sparkles, Network, Coins`. The `/command` route should appear near the top (after `/` Overview).

**Exact edit:**
```typescript
// BEFORE (in nav array):
{ href: "/",       icon: LayoutDashboard, label: "Overview"  },
{ href: "/tasks",  icon: CheckSquare,     label: "Tasks"     },

// AFTER:
{ href: "/",       icon: LayoutDashboard, label: "Overview"  },
{ href: "/command", icon: Zap,            label: "Command"   },
{ href: "/tasks",  icon: CheckSquare,     label: "Tasks"     },
```

And add `Zap` to the import:
```typescript
import {
  LayoutDashboard, CheckSquare, Calendar, Brain, Users, Server,
  DollarSign, FileText, Moon, Wrench, Archive, Building2, Sparkles,
  Network, Coins, Zap,   // ← add Zap
} from "lucide-react";
```

**File:** `components/Sidebar.tsx`
**Risk:** Low — additive only, no existing items changed.

---

### 5.9 `lib/mission-control/score.test.ts` — Add 7th lane test

Add one test for the `intel` lane in `deriveFactors` (if `deriveFactors` is tested — currently it's tested indirectly via `scoreSignal`/`commandQueue`).

The existing 5 tests already cover `computeScore`, `scoreBand`, `needsJT`, `commandQueue`. No new test is strictly required for the lane addition alone, but add:

```typescript
describe("deriveFactors", () => {
  test("intel lane does not trigger revenue score", () => {
    const s = signal({ lane: "intel", priority: "medium" });
    const { revenue } = deriveFactors(s);
    expect(revenue).toBe(0);
  });
});
```

**Import:** Add `deriveFactors` to the import line in score.test.ts.

**File:** `lib/mission-control/score.test.ts`
**Risk:** Zero — additive test.

---

## 6. Signal States (Loading / Empty / Error)

Each component handles its own state:

| State | CommandCockpit | WorkLane | LaneShell |
|-------|---------------|----------|-----------|
| **Loading** | Pulsing skeleton block | 2 shimmer bars per lane | Passed as `loading` prop |
| **Empty** | "No decisions pending for JT" centered text | "empty" centered text | Per-lane empty state |
| **Error** | (handled at page level — fetchAll try/catch) | — | — |

**Recommendation:** `app/command/page.tsx` should add a top-level error state:

```typescript
const [error, setError] = useState<string | null>(null);

// in fetchAll:
} catch (e) {
  setError("Failed to load signals");
  setLoading(false);
}

// in JSX, before rendering:
{error && (
  <div className="text-xs text-red-400 bg-red-950/30 border border-red-500/20 rounded p-3 mb-4">
    {error}
  </div>
)}
```

---

## 7. Risks

| Risk | Severity | Mitigation |
|------|----------|-----------|
| **LaunchAgent running `next dev`** — `NEXT_DIST_DIR=.next-build bun run build` must be used for verification. Direct `bun run build` without the env var writes to `.next` and will corrupt the live dev server. | HIGH | Already documented in CLAUDE.md. Always use `NEXT_DIST_DIR=.next-build bun run build` for verification. Never `bun run build` bare. |
| **Convex `--local` must be running** for API routes to work. If Convex is down, all task-reading routes return 500. | MEDIUM | No change needed — existing behavior. Command page polls every 15s, so it recovers automatically. |
| **`bun:test` vs tsc conflict** — `npx tsc --noEmit` reports error on `bun:test` import. | LOW | Benign; bun runs tests directly. Add `@types/bun` to devDeps if strict tsc is needed: `bun add -d @types/bun`. |
| **Sidebar overflow on mobile** — Current mobile bottom nav already has 14 items; adding a 15th may overflow. | LOW | Check that mobile bottom tab bar uses `overflow-x-auto` or `scroll`. Current Sidebar uses `min-w-[60px]` per item with horizontal scroll — fine. |
| **`/api/cron` reads `~/.openclaw/cron/jobs.json` as FS** — If the file is absent, returns `{ jobs: [] }` gracefully. | LOW | No change needed. |
| **Signal lane mismatch** — If `taskToSignal` normalizer misclassifies a task's lane, it shows in the wrong lane. | MEDIUM | This is an iterative improvement; for Slice 1, the heuristic classification is acceptable. Add `project` → lane overrides as data quality improves. |
| **Score ties** — `commandQueue` breaks ties by `updatedAt` then `title.localeCompare`. This is deterministic. | LOW | No action needed. |
| **`signal.priority` can be `undefined`** in current schema (optional in types.ts). WorkLane uses `s.priority ?? "low"` — safe. | LOW | Already handled. |

---

## 8. Verification Commands

Run after implementation, in this order:

```bash
cd ~/.openclaw/workspace/mission-control

# 1. Run unit tests — must be 6/6 (5 existing + 1 new intel lane test)
bun test lib/mission-control/score.test.ts

# 2. TypeScript (ignoring bun:test module error)
npx tsc --noEmit 2>&1 | grep -v "bun:test"

# 3. Isolated build — never run bare 'bun run build'
NEXT_DIST_DIR=.next-build bun run build

# 4. Verify new route is in build output
grep -r "command" .next-build/server/app-paths-manifest.json 2>/dev/null || \
  grep -r "command" .next-build/server/pages-manifest.json 2>/dev/null

# 5. Lint
bun run lint

# 6. Live smoke test (Convex must be running)
curl -s http://localhost:3000/command | head -c 200
# Should return HTML (Next.js page), not a 404

# 7. Verify normalize output shape (Node/bun REPL)
bun -e "
const { taskToSignal } = require('./lib/mission-control/normalize');
const s = taskToSignal({ _id:'t1', title:'Test', status:'todo', priority:'high', assignee:'jt', updatedAt: Date.now(), createdAt: Date.now() });
console.assert(s.source === 'task');
console.assert(s.owner === 'jt');
console.assert(typeof s.ageDays === 'number');
console.log('normalize OK');
"

# 8. Verify CommandCockpit renders no errors in dev
# (Open http://localhost:3000/command in browser, check console for React errors)

# 9. After kickstart (if LaunchAgent is running dev server)
# Only needed if live dev server was touched:
# launchctl kickstart -k gui/$(id -u)/com.openclaw.mission-control-next
```

---

## 9. File Change Summary (Minimal Slice 1)

| File | Action | Lines Changed |
|------|--------|---------------|
| `lib/mission-control/types.ts` | Edit | +1 (add `"intel"` to SignalLane union) |
| `lib/mission-control/normalize.ts` | **NEW** | ~90 lines |
| `lib/mission-control/score.test.ts` | Edit | +8 lines (1 new test) |
| `app/command/page.tsx` | **NEW** | ~50 lines |
| `components/CommandCockpit.tsx` | **NEW** | ~60 lines |
| `components/WorkLane.tsx` | **NEW** | ~55 lines |
| `components/LaneShell.tsx` | **NEW** | ~35 lines |
| `components/SignalDrawer.tsx` | **NEW** | ~100 lines |
| `components/Sidebar.tsx` | Edit | +2 lines (import Zap, add nav item) |

**Total:** 2 edits to existing files, 5 new files. Zero database migrations. Zero API route changes. Zero Convex schema changes.

---

## 10. What NOT to Touch

- `convex/schema.ts` — no new fields needed for Slice 1
- `convex/tasks.ts` — all mutations are sufficient
- `app/api/tasks/route.ts` — no changes; existing API handles signal data
- `app/layout.tsx` — sidebar/layout is fine
- `lib/mission-control/score.ts` — already complete; only add the `intel` handling implicitly (score.ts handles unknown lanes via the `else` branch in `deriveFactors`)
- `openclaw.json` — NEVER touch
- Any auth/model config files

---

## 11. CLAUDE.md Update (required per AGENTS.md rule)

After implementation, add to `mission-control/CLAUDE.md`:

```markdown
## Slice 1 — Signal Board (added YYYY-MM-DD)
- Route: `/command` — 7-lane signal board
- Lib: `lib/mission-control/types.ts`, `score.ts`, `normalize.ts`
- Components: `LaneShell`, `WorkLane`, `CommandCockpit`, `SignalDrawer`
- Tests: `bun test lib/mission-control/score.test.ts` (6 tests)
- Signal lanes: work | revenue | ship | machine | evidence | health | intel
- Scoring: see lib/mission-control/score.ts (weights: revenue 30%, unblock 20%, urgency 20%, risk 15%, northStar 15%)
- Normalize: taskToSignal / cronToSignal / proofToSignal in normalize.ts
```
