"use client";

import { AlertTriangle, Bot, CheckCircle2, Clock, RefreshCw, ServerCog, WalletCards, XCircle } from "lucide-react";
import { StateBlock } from "@/components/mission-control/StateBlock";
import { machineGroups, machineSummary } from "@/lib/mission-control/machine";
import { useMissionControlData } from "@/lib/mission-control/hooks";
import type { Signal } from "@/lib/mission-control/types";
import { cn } from "@/lib/utils";

function fmtMoney(value: number | null | undefined) {
  if (value === null || value === undefined) return "-";
  return `$${value.toFixed(2)}`;
}

function fmtTime(value?: number | null) {
  if (!value) return "No run recorded";
  return new Date(value).toLocaleString("en-US", { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" });
}

function statusClass(signal: Signal) {
  if (signal.status === "failed" || signal.status === "blocked") return "border-red-500/30 bg-red-500/10 text-red-300";
  if (signal.status === "in-progress") return "border-amber-500/30 bg-amber-500/10 text-amber-300";
  if (signal.status === "stale") return "border-zinc-500/30 bg-zinc-500/10 text-zinc-300";
  return "border-emerald-500/25 bg-emerald-500/10 text-emerald-300";
}

function Metric({
  label,
  value,
  tone = "neutral",
}: {
  label: string;
  value: string | number;
  tone?: "neutral" | "good" | "warn" | "bad";
}) {
  const toneClass = {
    neutral: "text-zinc-100",
    good: "text-emerald-300",
    warn: "text-amber-300",
    bad: "text-red-300",
  }[tone];

  return (
    <div className="border border-[#2a2a2a] bg-[#111] p-4">
      <p className="mb-1 text-[10px] uppercase tracking-widest text-zinc-500">{label}</p>
      <p className={cn("font-mono text-2xl font-semibold", toneClass)}>{value}</p>
    </div>
  );
}

function SignalRow({ signal }: { signal: Signal }) {
  const raw = signal.raw as { lastRun?: number | null; nextRun?: number | null; currentTask?: string } | undefined;
  return (
    <div className="border border-[#2a2a2a] bg-[#101010] p-3">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="truncate text-xs font-medium text-zinc-100">{signal.title}</p>
          <p className="mt-1 line-clamp-2 text-[10px] leading-relaxed text-zinc-500">
            {raw?.currentTask ?? signal.eveRead ?? signal.context ?? `Last: ${fmtTime(raw?.lastRun)} · Next: ${fmtTime(raw?.nextRun)}`}
          </p>
        </div>
        <span className={cn("shrink-0 rounded border px-2 py-0.5 text-[9px] font-medium", statusClass(signal))}>
          {signal.status.replace("-", " ")}
        </span>
      </div>
    </div>
  );
}

function Rail({
  title,
  icon: Icon,
  items,
  empty,
}: {
  title: string;
  icon: typeof ServerCog;
  items: Signal[];
  empty: string;
}) {
  return (
    <section>
      <div className="mb-3 flex items-center gap-2">
        <Icon size={14} className="text-emerald-400" />
        <h2 className="text-xs font-semibold uppercase tracking-widest text-zinc-400">{title}</h2>
      </div>
      <div className="space-y-2">
        {items.slice(0, 8).map((signal) => (
          <SignalRow key={signal.id} signal={signal} />
        ))}
        {items.length === 0 && <StateBlock kind="empty" title={empty} detail="No current machine signal in this rail." />}
      </div>
    </section>
  );
}

export default function MachinePage() {
  const { costs, errors, lastUpdated, loading, refresh, signals } = useMissionControlData();
  const summary = machineSummary(signals);
  const groups = machineGroups(signals);
  const costAlerts = costs?.alerts ?? [];
  const riskTone = summary.risks > 0 || costAlerts.length > 0 ? "bad" : "good";

  return (
    <main className="mx-auto max-w-6xl px-4 py-5 sm:px-6 sm:py-6">
      <header className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-[10px] uppercase tracking-[0.22em] text-emerald-400">Machine</p>
          <h1 className="mt-1 text-xl font-semibold text-zinc-100">System health cockpit</h1>
          <p className="mt-1 max-w-2xl text-xs leading-relaxed text-zinc-500">
            Cron reliability, agent posture, cost pressure, and automation risks from the existing Mission Control backplane.
          </p>
        </div>
        <button
          onClick={refresh}
          className="inline-flex items-center justify-center gap-2 border border-[#2a2a2a] px-3 py-2 text-xs text-zinc-300 transition-colors hover:border-emerald-500/40 hover:text-emerald-300"
        >
          <RefreshCw size={13} className={loading ? "animate-spin" : ""} />
          Refresh
        </button>
      </header>

      {Object.keys(errors).length > 0 && (
        <div className="mb-4 border border-amber-500/30 bg-amber-500/10 px-3 py-2 text-xs text-amber-200">
          Degraded data: {Object.entries(errors).map(([key, value]) => `${key} ${value}`).join(" · ")}
        </div>
      )}

      <section className="mb-5 grid grid-cols-2 gap-3 lg:grid-cols-5">
        <Metric label="Cron Jobs" value={summary.cronsTotal} tone={summary.cronsFailed ? "bad" : "good"} />
        <Metric label="Failed" value={summary.cronsFailed} tone={summary.cronsFailed ? "bad" : "good"} />
        <Metric label="Agents Active" value={summary.agentsActive} tone="good" />
        <Metric label="Cost Today" value={fmtMoney(costs?.today?.total_usd)} tone={costAlerts.length ? "bad" : "neutral"} />
        <Metric label="Risks" value={summary.risks + costAlerts.length} tone={riskTone} />
      </section>

      <section className="mb-6 border border-[#2a2a2a] bg-[#111] p-4">
        <div className="flex items-center gap-2">
          {summary.cronsFailed || costAlerts.length ? (
            <XCircle size={14} className="text-red-400" />
          ) : (
            <CheckCircle2 size={14} className="text-emerald-400" />
          )}
          <p className="text-sm font-medium text-zinc-100">
            {summary.cronsFailed || costAlerts.length
              ? "Machine needs review"
              : "Machine posture is clear"}
          </p>
        </div>
        <p className="mt-2 text-xs leading-relaxed text-zinc-500">
          {summary.cronsFailed
            ? `${summary.cronsFailed} cron signal is failing.`
            : "No failing cron signals are in the current Mission Control adapter feed."}{" "}
          {costAlerts.length
            ? `${costAlerts.length} cost alert is active.`
            : "No cost alerts are active."}{" "}
          Last refresh {lastUpdated ? fmtTime(lastUpdated) : "pending"}.
        </p>
      </section>

      <div className="grid gap-6 lg:grid-cols-2">
        <Rail title="Cron Health" icon={Clock} items={groups.crons} empty="No cron data loaded" />
        <Rail title="Agent Posture" icon={Bot} items={groups.agents} empty="No agent data loaded" />
        <Rail title="Cost Pressure" icon={WalletCards} items={groups.costs} empty="No cost pressure tasks" />
        <Rail title="Automation Work" icon={AlertTriangle} items={groups.work} empty="No active machine work" />
      </div>
    </main>
  );
}
