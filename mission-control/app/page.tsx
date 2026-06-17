"use client";

import { useState } from "react";
import { AlertTriangle, ArrowRight, CheckCircle2, CircleDollarSign, RefreshCw } from "lucide-react";
import { InspectionDrawer } from "@/components/mission-control/InspectionDrawer";
import { StateBlock } from "@/components/mission-control/StateBlock";
import { useMissionControlData } from "@/lib/mission-control/hooks";
import type { Signal } from "@/lib/mission-control/types";
import { cn, formatRelative } from "@/lib/utils";

function bandClass(signal: Signal) {
  if (signal.band === "high" || signal.status === "failed" || signal.status === "blocked") {
    return "border-l-red-400";
  }
  if (signal.band === "medium" || signal.status === "stale") return "border-l-amber-400";
  return "border-l-zinc-600";
}

function ActionCard({ signal, onInspect }: { signal: Signal; onInspect: (signal: Signal) => void }) {
  return (
    <button
      onClick={() => onInspect(signal)}
      className={cn(
        "w-full rounded-lg border border-[#20262d] border-l-2 bg-[#0f1316] p-3 text-left transition-colors hover:border-[#38414a]",
        bandClass(signal),
      )}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-2">
            <span className="rounded bg-[#16191d] px-1.5 py-0.5 text-[9px] font-semibold uppercase tracking-wider text-[#f0883e]">
              {signal.status.replace(/-/g, " ")}
            </span>
            <span className="text-[10px] uppercase text-zinc-600">{signal.lane}</span>
          </div>
          <p className="mt-2 text-sm font-semibold leading-snug text-zinc-100">{signal.title}</p>
          <p className="mt-1 line-clamp-2 text-[11px] leading-relaxed text-zinc-500">
            {signal.context || signal.project || "No context attached yet."}
          </p>
        </div>
        <div className="flex flex-col items-end gap-1">
          <span className="rounded border border-[#2b333c] bg-[#0b0d0f] px-2 py-1 font-mono text-xs font-semibold text-zinc-200">
            {signal.score ?? 0}
          </span>
          <span className="text-[9px] uppercase text-zinc-600">score</span>
        </div>
      </div>
      <div className="mt-3 flex items-center justify-between text-[10px] text-zinc-600">
        <span>{signal.project || signal.source}</span>
        <span className="flex items-center gap-1 text-emerald-400">
          Inspect <ArrowRight size={10} />
        </span>
      </div>
    </button>
  );
}

function MiniSignal({ signal, onInspect }: { signal: Signal; onInspect: (signal: Signal) => void }) {
  return (
    <button
      onClick={() => onInspect(signal)}
      className="w-full rounded-md border border-[#20262d] bg-[#0f1316] p-3 text-left hover:border-[#38414a]"
    >
      <div className="flex items-center justify-between gap-2">
        <p className="truncate text-xs font-medium text-zinc-200">{signal.title}</p>
        <span className="shrink-0 text-[9px] uppercase text-zinc-600">{signal.source}</span>
      </div>
      <p className="mt-1 text-[10px] text-zinc-600">{formatRelative(signal.updatedAt)}</p>
    </button>
  );
}

export default function CommandPage() {
  const { queue, eveHandling, risk, revenue, brief, loading, degraded, lastUpdated, refresh } = useMissionControlData();
  const [selected, setSelected] = useState<Signal | null>(null);

  return (
    <div className="min-h-screen bg-[#0a0b0d] p-4 sm:p-6">
      <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-[#f0883e]">Command</p>
          <h1 className="mt-1 text-2xl font-semibold tracking-tight text-zinc-100">Mission Control cockpit</h1>
          <p className="mt-1 text-xs text-zinc-500">
            Decision queue, money path, Eve activity, and machine risk from current data.
          </p>
        </div>
        <button
          onClick={refresh}
          className="flex w-fit items-center gap-2 rounded-md border border-[#20262d] bg-[#0f1316] px-3 py-2 text-xs text-zinc-300 hover:border-[#38414a]"
        >
          <RefreshCw size={13} className={loading ? "animate-spin" : ""} />
          Refresh
        </button>
      </div>

      {degraded.length > 0 && (
        <StateBlock
          kind="stale"
          title="Some data routes are degraded"
          detail={`Showing cached or partial data for: ${degraded.join(", ")}.`}
          className="mb-4"
        />
      )}

      <section className="mb-4 grid gap-3 lg:grid-cols-[1.2fr_1fr_1fr_1fr]">
        <div className="rounded-lg border border-emerald-900/40 bg-emerald-950/10 p-4">
          <div className="flex items-center gap-2 text-emerald-300">
            <CircleDollarSign size={16} />
            <span className="font-mono text-[10px] uppercase tracking-wider">Revenue cockpit</span>
          </div>
          <p className="mt-3 text-2xl font-semibold text-zinc-100">{revenue.active}</p>
          <p className="text-[11px] text-zinc-500">active revenue-path tasks</p>
        </div>
        <div className="rounded-lg border border-[#20262d] bg-[#0f1316] p-4">
          <p className="font-mono text-[10px] uppercase tracking-wider text-zinc-600">High priority</p>
          <p className="mt-3 text-2xl font-semibold text-zinc-100">{revenue.high}</p>
          <p className="text-[11px] text-zinc-500">revenue/job items</p>
        </div>
        <div className="rounded-lg border border-[#20262d] bg-[#0f1316] p-4">
          <p className="font-mono text-[10px] uppercase tracking-wider text-zinc-600">Completed</p>
          <p className="mt-3 text-2xl font-semibold text-zinc-100">{revenue.done}</p>
          <p className="text-[11px] text-zinc-500">closed revenue-path tasks</p>
        </div>
        <div className="rounded-lg border border-[#20262d] bg-[#0f1316] p-4">
          <p className="font-mono text-[10px] uppercase tracking-wider text-zinc-600">Cost today</p>
          <p className="mt-3 text-2xl font-semibold text-zinc-100">
            {revenue.costToday == null ? "unknown" : `$${Number(revenue.costToday).toFixed(2)}`}
          </p>
          <p className="text-[11px] text-zinc-500">{revenue.costAlerts.length} cost alerts</p>
        </div>
      </section>

      <div className="grid gap-4 xl:grid-cols-[1fr_360px]">
        <section className="rounded-xl border border-[#20262d] bg-[#0d1014] p-4">
          <div className="mb-3 flex items-center justify-between">
            <div>
              <p className="font-mono text-[10px] uppercase tracking-wider text-[#f0883e]">Needs You Now</p>
              <p className="text-[11px] text-zinc-600">Ranked JT-owned decisions, capped at 7.</p>
            </div>
            <span className="rounded bg-[#16191d] px-2 py-1 font-mono text-[10px] text-zinc-500">{queue.length}/7</span>
          </div>
          <div className="space-y-2">
            {loading && queue.length === 0 ? (
              <StateBlock kind="loading" title="Ranking current work" detail="Pulling tasks, crons, proofs, agents, and costs." />
            ) : queue.length === 0 ? (
              <StateBlock kind="empty" title="Queue clear" detail="Nothing currently needs JT. Eve-owned work stays out of this queue." />
            ) : (
              queue.map((signal) => <ActionCard key={signal.id} signal={signal} onInspect={setSelected} />)
            )}
          </div>
        </section>

        <aside className="space-y-4">
          <section className="rounded-xl border border-[#20262d] bg-[#0d1014] p-4">
            <div className="mb-3 flex items-center gap-2">
              <CheckCircle2 size={14} className="text-purple-300" />
              <p className="font-mono text-[10px] uppercase tracking-wider text-purple-300">Eve Is Handling</p>
            </div>
            <div className="space-y-2">
              {eveHandling.length === 0 ? (
                <StateBlock kind="empty" title="No Eve-owned work in flight" />
              ) : (
                eveHandling.map((signal) => <MiniSignal key={signal.id} signal={signal} onInspect={setSelected} />)
              )}
            </div>
          </section>

          <section className="rounded-xl border border-[#20262d] bg-[#0d1014] p-4">
            <div className="mb-3 flex items-center gap-2">
              <AlertTriangle size={14} className="text-red-300" />
              <p className="font-mono text-[10px] uppercase tracking-wider text-red-300">Risk & Drift</p>
            </div>
            <div className="space-y-2">
              {risk.length === 0 ? (
                <StateBlock kind="empty" title="No obvious drift" detail="Failed, stale, and blocked signals are clear." />
              ) : (
                risk.map((signal) => <MiniSignal key={signal.id} signal={signal} onInspect={setSelected} />)
              )}
            </div>
          </section>

          <section className="rounded-xl border border-[#20262d] bg-[#0d1014] p-4">
            <p className="font-mono text-[10px] uppercase tracking-wider text-emerald-300">Command Brief</p>
            <p className="mt-2 text-sm font-semibold leading-snug text-zinc-100">{brief.headline}</p>
            <div className="mt-3 space-y-3 text-xs">
              <button
                type="button"
                onClick={() => brief.topAction && setSelected(brief.topAction)}
                disabled={!brief.topAction}
                className="w-full rounded-md border border-[#20262d] bg-[#0f1316] p-3 text-left disabled:cursor-default disabled:opacity-60"
              >
                <span className="block text-[10px] font-semibold uppercase tracking-wider text-zinc-600">Top action</span>
                <span className="mt-1 block line-clamp-2 text-zinc-300">
                  {brief.topAction?.title ?? "No JT action pressure."}
                </span>
              </button>
              <button
                type="button"
                onClick={() => brief.latestProof && setSelected(brief.latestProof)}
                disabled={!brief.latestProof}
                className="w-full rounded-md border border-[#20262d] bg-[#0f1316] p-3 text-left disabled:cursor-default disabled:opacity-60"
              >
                <span className="block text-[10px] font-semibold uppercase tracking-wider text-zinc-600">Latest proof</span>
                <span className="mt-1 block line-clamp-2 text-zinc-300">
                  {brief.latestProof?.title ?? "No proof signal loaded yet."}
                </span>
              </button>
            </div>
            <div className="mt-3 grid grid-cols-3 gap-2 text-center">
              <div className="rounded-md border border-[#20262d] bg-[#0f1316] p-2">
                <p className="text-sm font-semibold text-zinc-100">{brief.urgentJtCount}</p>
                <p className="text-[9px] uppercase text-zinc-600">urgent</p>
              </div>
              <div className="rounded-md border border-[#20262d] bg-[#0f1316] p-2">
                <p className="text-sm font-semibold text-zinc-100">{brief.revenuePressure}</p>
                <p className="text-[9px] uppercase text-zinc-600">revenue</p>
              </div>
              <div className="rounded-md border border-[#20262d] bg-[#0f1316] p-2">
                <p className="text-sm font-semibold text-zinc-100">{brief.riskCount}</p>
                <p className="text-[9px] uppercase text-zinc-600">risk</p>
              </div>
            </div>
            <p className="mt-3 text-[11px] leading-relaxed text-zinc-600">
              {lastUpdated ? `Refreshed ${formatRelative(lastUpdated)}.` : "Waiting for first refresh."}
            </p>
          </section>
        </aside>
      </div>

      <InspectionDrawer signal={selected} onClose={() => setSelected(null)} />
    </div>
  );
}
