"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { AlertTriangle, ArrowRight, CheckCircle2, Lightbulb, PackageCheck, RefreshCw, Rocket, Send } from "lucide-react";
import { InspectionDrawer } from "@/components/mission-control/InspectionDrawer";
import { StateBlock } from "@/components/mission-control/StateBlock";
import { useMissionControlData } from "@/lib/mission-control/hooks";
import { shipGroups, shipSummary } from "@/lib/mission-control/ship";
import type { Signal } from "@/lib/mission-control/types";
import { priorityBadgeClassName, priorityRailClassName } from "@/lib/mission-control/work-priority";
import { cn, formatRelative } from "@/lib/utils";

function MetricCard({
  label,
  value,
  detail,
  tone = "neutral",
  icon: Icon,
}: {
  label: string;
  value: number;
  detail: string;
  tone?: "neutral" | "good" | "warn" | "blue";
  icon: typeof Rocket;
}) {
  return (
    <div className="rounded-lg border border-[#20262d] bg-[#0d1014] p-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="font-mono text-[10px] uppercase tracking-[0.16em] text-zinc-500">{label}</p>
          <p className="mt-2 text-2xl font-semibold tracking-tight text-zinc-100">{value}</p>
        </div>
        <span
          className={cn(
            "rounded-md border p-2",
            tone === "good" && "border-emerald-500/30 bg-emerald-500/10 text-emerald-300",
            tone === "warn" && "border-[#f0883e]/30 bg-[#f0883e]/10 text-[#f0883e]",
            tone === "blue" && "border-blue-500/30 bg-blue-500/10 text-blue-300",
            tone === "neutral" && "border-[#20262d] bg-[#111] text-zinc-400",
          )}
        >
          <Icon size={16} />
        </span>
      </div>
      <p className="mt-3 text-xs leading-relaxed text-zinc-500">{detail}</p>
    </div>
  );
}

function ShipItem({ signal, onInspect }: { signal: Signal; onInspect: (signal: Signal) => void }) {
  return (
    <button
      type="button"
      onClick={() => onInspect(signal)}
      className={cn(
        "w-full border-l-2 border-y border-r border-[#20262d] bg-[#0f1316] p-3 text-left transition-colors hover:border-[#38414a]",
        priorityRailClassName(signal.priority),
      )}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <div className="mb-2 flex flex-wrap items-center gap-2">
            <span className={cn("rounded border px-2 py-0.5 text-[10px] uppercase", priorityBadgeClassName(signal.priority))}>
              {signal.priority ?? "none"}
            </span>
            <span className="rounded bg-[#16191d] px-2 py-0.5 text-[10px] uppercase text-zinc-500">{signal.status}</span>
          </div>
          <p className="line-clamp-2 text-sm font-medium leading-snug text-zinc-100">{signal.title}</p>
          <p className="mt-1 line-clamp-2 text-[11px] leading-relaxed text-zinc-600">
            {signal.context || signal.project || "No shipping context attached yet."}
          </p>
        </div>
        <span className="shrink-0 text-[10px] text-zinc-600">{formatRelative(signal.updatedAt)}</span>
      </div>
    </button>
  );
}

function ShipColumn({
  title,
  detail,
  signals,
  onInspect,
}: {
  title: string;
  detail: string;
  signals: Signal[];
  onInspect: (signal: Signal) => void;
}) {
  return (
    <section className="rounded-xl border border-[#20262d] bg-[#0d1014]">
      <div className="border-b border-[#20262d] p-4">
        <div className="flex items-start justify-between gap-3">
          <div>
            <h2 className="text-sm font-semibold text-zinc-100">{title}</h2>
            <p className="mt-1 text-xs leading-relaxed text-zinc-500">{detail}</p>
          </div>
          <span className="rounded bg-[#16191d] px-2 py-1 font-mono text-[10px] text-zinc-500">{signals.length}</span>
        </div>
      </div>
      <div className="divide-y divide-[#16191d]">
        {signals.length === 0 ? (
          <div className="p-4">
            <StateBlock kind="empty" title="No items here" detail="Ship work will appear when tasks or proofs map into this group." />
          </div>
        ) : (
          signals.slice(0, 8).map((signal) => <ShipItem key={signal.id} signal={signal} onInspect={onInspect} />)
        )}
      </div>
    </section>
  );
}

export default function ShipPage() {
  const { signals, loading, errors, refresh } = useMissionControlData();
  const [selected, setSelected] = useState<Signal | null>(null);
  const summary = useMemo(() => shipSummary(signals), [signals]);
  const groups = useMemo(() => shipGroups(signals), [signals]);

  return (
    <div className="min-h-screen bg-[#0a0b0d] p-4 sm:p-6">
      <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-purple-300">Ship</p>
          <h1 className="mt-1 text-2xl font-semibold tracking-tight text-zinc-100">Ship cockpit</h1>
          <p className="mt-1 max-w-2xl text-xs leading-relaxed text-zinc-500">
            App distribution, content shipping, release blockers, and proof coverage from current Mission Control signals.
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

      {errors.tasks && <StateBlock kind="error" title="/api/tasks unreachable" detail={errors.tasks} className="mb-4" />}

      <div className="grid gap-3 md:grid-cols-4">
        <MetricCard icon={Rocket} label="Active Ship Work" value={summary.active} detail="Open app, content, and launch work that can create distribution proof." tone="blue" />
        <MetricCard icon={AlertTriangle} label="High Priority" value={summary.high} detail="The shipping items competing hardest for attention right now." tone="warn" />
        <MetricCard icon={PackageCheck} label="Proofed Ships" value={summary.proofed} detail="Ship signals with verified evidence attached." tone="good" />
        <MetricCard icon={CheckCircle2} label="Blocked/Stale" value={summary.blocked} detail="Failures, stale work, or old items that need pruning." />
      </div>

      <section className="mt-4 rounded-lg border border-purple-500/30 bg-purple-950/10 p-4">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div className="flex items-start gap-3">
          <span className="rounded-md border border-purple-500/30 bg-purple-500/10 p-2 text-purple-300">
            <Send size={16} />
          </span>
          <div className="min-w-0">
            <p className="text-sm font-semibold text-zinc-100">Distribution rule</p>
            <p className="mt-1 text-xs leading-relaxed text-zinc-500">
              Ship lane favors proof-generating distribution: directory listings, ASO tests, share artifacts, content drafts, and launch gates. Build-only work stays lower unless it unlocks public proof.
            </p>
          </div>
          </div>
          <Link
            href="/passive-income"
            className="inline-flex w-fit items-center gap-2 rounded-md border border-emerald-500/30 bg-emerald-500/10 px-3 py-2 text-xs font-medium text-emerald-200 transition-colors hover:border-emerald-400/60 hover:bg-emerald-500/15"
          >
            <Lightbulb size={14} />
            Passive Income Board
            <ArrowRight size={13} />
          </Link>
        </div>
      </section>

      <div className="mt-5 grid gap-4 xl:grid-cols-3">
        <ShipColumn title="App Distribution" detail="Vista, Nash, Glow, and Action Arena acquisition or listing work." signals={groups.apps} onInspect={setSelected} />
        <ShipColumn title="Content Queue" detail="Drafts, teardown work, research-to-post items, and content surfaces." signals={groups.content} onInspect={setSelected} />
        <ShipColumn title="Release Gates" detail="App Store, launch, implementation, share-card, and proof-gated release tasks." signals={groups.releases} onInspect={setSelected} />
      </div>

      <InspectionDrawer signal={selected} onClose={() => setSelected(null)} />
    </div>
  );
}
