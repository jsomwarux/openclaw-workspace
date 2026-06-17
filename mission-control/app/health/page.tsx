"use client";

import { useMemo, useState } from "react";
import { AlertTriangle, CheckCircle2, HeartPulse, RefreshCw, ShieldAlert, TimerReset, WalletCards } from "lucide-react";
import { InspectionDrawer } from "@/components/mission-control/InspectionDrawer";
import { StateBlock } from "@/components/mission-control/StateBlock";
import { healthGroups, healthSummary } from "@/lib/mission-control/health";
import { useMissionControlData } from "@/lib/mission-control/hooks";
import type { Signal } from "@/lib/mission-control/types";
import { cn, formatRelative } from "@/lib/utils";

function money(value: number | null | undefined) {
  if (value === null || value === undefined) return "-";
  return `$${value.toFixed(2)}`;
}

function Metric({
  label,
  value,
  detail,
  tone = "neutral",
}: {
  label: string;
  value: string | number;
  detail: string;
  tone?: "neutral" | "good" | "warn" | "bad";
}) {
  const toneClass = {
    neutral: "border-[#252525] bg-[#101010] text-zinc-100",
    good: "border-emerald-500/25 bg-emerald-500/10 text-emerald-200",
    warn: "border-amber-500/25 bg-amber-500/10 text-amber-200",
    bad: "border-red-500/25 bg-red-500/10 text-red-200",
  }[tone];

  return (
    <div className={cn("border p-4", toneClass)}>
      <p className="text-[10px] uppercase tracking-[0.18em] text-zinc-500">{label}</p>
      <p className="mt-2 font-mono text-2xl font-semibold">{value}</p>
      <p className="mt-2 text-xs leading-relaxed text-zinc-500">{detail}</p>
    </div>
  );
}

function signalTone(signal: Signal) {
  if (signal.status === "failed" || signal.status === "blocked") return "border-red-500/30 bg-red-500/10 text-red-300";
  if (signal.status === "stale" || signal.ageDays >= 14) return "border-amber-500/30 bg-amber-500/10 text-amber-300";
  return "border-emerald-500/25 bg-emerald-500/10 text-emerald-300";
}

function HealthItem({ signal, onInspect }: { signal: Signal; onInspect: (signal: Signal) => void }) {
  return (
    <button
      type="button"
      onClick={() => onInspect(signal)}
      className="w-full border border-[#252525] bg-[#101010] p-3 text-left transition-colors hover:border-emerald-500/30"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <div className="mb-2 flex flex-wrap items-center gap-2">
            <span className={cn("rounded border px-2 py-0.5 text-[10px] uppercase", signalTone(signal))}>
              {signal.status}
            </span>
            <span className="rounded bg-[#171717] px-2 py-0.5 text-[10px] uppercase text-zinc-500">
              {signal.lane}
            </span>
          </div>
          <p className="line-clamp-2 text-sm font-medium leading-snug text-zinc-100">{signal.title}</p>
          <p className="mt-1 line-clamp-2 text-[11px] leading-relaxed text-zinc-500">
            {signal.context ?? signal.project ?? "No health context attached."}
          </p>
        </div>
        <span className="shrink-0 text-[10px] text-zinc-600">{formatRelative(signal.updatedAt)}</span>
      </div>
    </button>
  );
}

function HealthRail({
  title,
  detail,
  icon: Icon,
  items,
  onInspect,
}: {
  title: string;
  detail: string;
  icon: typeof HeartPulse;
  items: Signal[];
  onInspect: (signal: Signal) => void;
}) {
  return (
    <section className="border border-[#252525] bg-[#0f0f0f]">
      <div className="border-b border-[#202020] p-4">
        <div className="flex items-start gap-3">
          <span className="rounded border border-emerald-500/25 bg-emerald-500/10 p-2 text-emerald-300">
            <Icon size={15} />
          </span>
          <div className="min-w-0">
            <div className="flex items-center gap-2">
              <h2 className="text-sm font-semibold text-zinc-100">{title}</h2>
              <span className="rounded bg-[#171717] px-2 py-0.5 font-mono text-[10px] text-zinc-500">{items.length}</span>
            </div>
            <p className="mt-1 text-xs leading-relaxed text-zinc-500">{detail}</p>
          </div>
        </div>
      </div>
      <div className="divide-y divide-[#171717]">
        {items.length === 0 ? (
          <div className="p-4">
            <StateBlock kind="empty" title="No health items" detail="This rail is clear in the current signal feed." />
          </div>
        ) : (
          items.slice(0, 8).map((signal) => <HealthItem key={signal.id} signal={signal} onInspect={onInspect} />)
        )}
      </div>
    </section>
  );
}

export default function HealthPage() {
  const { costs, errors, lastUpdated, loading, refresh, signals } = useMissionControlData();
  const [selected, setSelected] = useState<Signal | null>(null);
  const summary = useMemo(() => healthSummary(signals, costs), [costs, signals]);
  const groups = useMemo(() => healthGroups(signals), [signals]);
  const costAlerts = costs?.alerts ?? [];
  const costToday = costs?.today?.total_usd ?? null;
  const costPace = costs?.month?.pace_usd ?? null;

  return (
    <main className="mx-auto max-w-6xl px-4 py-5 sm:px-6 sm:py-6">
      <header className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-[10px] uppercase tracking-[0.22em] text-emerald-400">Health</p>
          <h1 className="mt-1 text-xl font-semibold text-zinc-100">Ops health cockpit</h1>
          <p className="mt-1 max-w-2xl text-xs leading-relaxed text-zinc-500">
            Failures, stale risk, cost pressure, and recovery work across the current Mission Control signal feed.
          </p>
        </div>
        <button
          onClick={refresh}
          className="inline-flex w-fit items-center justify-center gap-2 border border-[#2a2a2a] px-3 py-2 text-xs text-zinc-300 transition-colors hover:border-emerald-500/40 hover:text-emerald-300"
        >
          <RefreshCw size={13} className={loading ? "animate-spin" : ""} />
          Refresh
        </button>
      </header>

      {Object.keys(errors).length > 0 && (
        <StateBlock kind="error" title="Some health data is degraded" detail={Object.entries(errors).map(([key, value]) => `${key}: ${value}`).join(" · ")} className="mb-4" />
      )}

      <section className="mb-5 grid grid-cols-2 gap-3 lg:grid-cols-5">
        <Metric label="Posture" value={summary.posture === "clear" ? "Clear" : "Review"} detail="Overall ops state from failures, stale items, and cost alerts." tone={summary.posture === "clear" ? "good" : "warn"} />
        <Metric label="Failures" value={summary.failures} detail="Failed or blocked signals needing inspection." tone={summary.failures ? "bad" : "good"} />
        <Metric label="Stale Risk" value={summary.stale} detail="Stale or old signals that can hide drift." tone={summary.stale ? "warn" : "good"} />
        <Metric label="Cost Today" value={money(costToday)} detail={`Monthly pace ${money(costPace)}.`} tone={costAlerts.length ? "bad" : "neutral"} />
        <Metric label="Recovery Work" value={summary.recoveryWork} detail="Open cleanup, guard, restart, or recovery work." tone={summary.recoveryWork ? "warn" : "good"} />
      </section>

      <section className={cn("mb-5 border p-4", summary.posture === "clear" ? "border-emerald-500/25 bg-emerald-500/10" : "border-amber-500/25 bg-amber-500/10")}>
        <div className="flex items-start gap-3">
          <span className={cn("rounded border p-2", summary.posture === "clear" ? "border-emerald-500/25 bg-emerald-500/10 text-emerald-300" : "border-amber-500/25 bg-amber-500/10 text-amber-300")}>
            {summary.posture === "clear" ? <CheckCircle2 size={16} /> : <AlertTriangle size={16} />}
          </span>
          <div className="min-w-0">
            <p className="text-sm font-medium text-zinc-100">
              {summary.posture === "clear" ? "No active health review needed" : "Health needs a review pass"}
            </p>
            <p className="mt-1 text-xs leading-relaxed text-zinc-500">
              {summary.failures} failures, {summary.stale} stale risks, {summary.costAlerts} cost alerts. Last refresh{" "}
              {lastUpdated ? new Date(lastUpdated).toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" }) : "pending"}.
            </p>
          </div>
        </div>
      </section>

      {costAlerts.length > 0 && (
        <section className="mb-5 space-y-2">
          {costAlerts.map((alert: { level?: string; message?: string }, index: number) => (
            <div key={`${alert.message}-${index}`} className="border border-red-500/25 bg-red-500/10 px-3 py-2 text-xs text-red-200">
              {alert.level ?? "alert"}: {alert.message ?? "Cost alert"}
            </div>
          ))}
        </section>
      )}

      <div className="grid gap-4 xl:grid-cols-2">
        <HealthRail title="Ops Failures" detail="Failed or blocked machine, health, and cross-lane signals." icon={ShieldAlert} items={groups.failures} onInspect={setSelected} />
        <HealthRail title="Cost Pressure" detail="Cost, token, budget, wallet, or runaway-spend signals." icon={WalletCards} items={groups.costs} onInspect={setSelected} />
        <HealthRail title="Stale Risk" detail="Old or stale signals that can hide drift if ignored." icon={TimerReset} items={groups.stale} onInspect={setSelected} />
        <HealthRail title="Recovery Work" detail="Cleanup, restart, guard, monitor, and health follow-up work." icon={HeartPulse} items={groups.recovery} onInspect={setSelected} />
      </div>

      <InspectionDrawer signal={selected} onClose={() => setSelected(null)} />
    </main>
  );
}
