"use client";

import { useMemo, useState } from "react";
import { AlertTriangle, FileCheck2, FolderOpen, RefreshCw, ShieldCheck, Sparkles } from "lucide-react";
import { InspectionDrawer } from "@/components/mission-control/InspectionDrawer";
import { StateBlock } from "@/components/mission-control/StateBlock";
import { evidenceGroups, evidenceSummary } from "@/lib/mission-control/evidence";
import { useMissionControlData } from "@/lib/mission-control/hooks";
import type { Signal } from "@/lib/mission-control/types";
import { cn, formatRelative } from "@/lib/utils";

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
    neutral: "border-[#242424] bg-[#101010] text-zinc-100",
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

function proofStatusClass(signal: Signal) {
  if (signal.status === "failed") return "border-red-500/30 bg-red-500/10 text-red-300";
  if (signal.evidence.some((ref) => ref.quality === "gap")) return "border-amber-500/30 bg-amber-500/10 text-amber-300";
  return "border-emerald-500/25 bg-emerald-500/10 text-emerald-300";
}

function EvidenceItem({ signal, onInspect }: { signal: Signal; onInspect: (signal: Signal) => void }) {
  const proofCount = signal.evidence.filter((ref) => ref.quality === "verified").length;
  const hasGap = signal.evidence.some((ref) => ref.quality === "gap");

  return (
    <button
      type="button"
      onClick={() => onInspect(signal)}
      className="w-full border border-[#242424] bg-[#101010] p-3 text-left transition-colors hover:border-emerald-500/30"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <div className="mb-2 flex flex-wrap items-center gap-2">
            <span className={cn("rounded border px-2 py-0.5 text-[10px] uppercase", proofStatusClass(signal))}>
              {hasGap ? "gap" : signal.status}
            </span>
            <span className="rounded bg-[#171717] px-2 py-0.5 text-[10px] uppercase text-zinc-500">
              {proofCount} refs
            </span>
          </div>
          <p className="line-clamp-2 text-sm font-medium leading-snug text-zinc-100">{signal.title}</p>
          <p className="mt-1 line-clamp-2 text-[11px] leading-relaxed text-zinc-500">
            {signal.context ?? "Proof entry from the local audit trail."}
          </p>
        </div>
        <span className="shrink-0 text-[10px] text-zinc-600">{formatRelative(signal.updatedAt)}</span>
      </div>
    </button>
  );
}

function EvidenceRail({
  title,
  detail,
  icon: Icon,
  items,
  onInspect,
}: {
  title: string;
  detail: string;
  icon: typeof ShieldCheck;
  items: Signal[];
  onInspect: (signal: Signal) => void;
}) {
  return (
    <section className="border border-[#242424] bg-[#0f0f0f]">
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
            <StateBlock kind="empty" title="No proof here" detail="Evidence will appear here when proof logs or tasks map into this group." />
          </div>
        ) : (
          items.slice(0, 8).map((signal) => <EvidenceItem key={signal.id} signal={signal} onInspect={onInspect} />)
        )}
      </div>
    </section>
  );
}

export default function EvidencePage() {
  const { errors, loading, refresh, signals } = useMissionControlData();
  const [selected, setSelected] = useState<Signal | null>(null);
  const summary = useMemo(() => evidenceSummary(signals), [signals]);
  const groups = useMemo(() => evidenceGroups(signals), [signals]);

  return (
    <main className="mx-auto max-w-6xl px-4 py-5 sm:px-6 sm:py-6">
      <header className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-[10px] uppercase tracking-[0.22em] text-emerald-400">Evidence</p>
          <h1 className="mt-1 text-xl font-semibold text-zinc-100">Proof ledger</h1>
          <p className="mt-1 max-w-2xl text-xs leading-relaxed text-zinc-500">
            Buyer-readable proof, system receipts, content assets, and proof gaps from the existing audit trail.
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

      {errors.proofs && <StateBlock kind="error" title="/api/proofs unreachable" detail={errors.proofs} className="mb-4" />}

      <section className="mb-5 grid grid-cols-2 gap-3 lg:grid-cols-4">
        <Metric label="Proof Entries" value={summary.total} detail="Recent proof signals pulled from proof logs." tone="good" />
        <Metric label="Verified" value={summary.verified} detail="Entries with at least one verified file or artifact reference." tone="good" />
        <Metric label="Gaps" value={summary.gaps} detail="Entries missing usable proof references." tone={summary.gaps ? "warn" : "good"} />
        <Metric label="Failures" value={summary.failures} detail="Proof entries that recorded failed outcomes." tone={summary.failures ? "bad" : "good"} />
      </section>

      <section className="mb-5 border border-emerald-500/25 bg-emerald-500/10 p-4">
        <div className="flex items-start gap-3">
          <span className="rounded border border-emerald-500/25 bg-emerald-500/10 p-2 text-emerald-300">
            <Sparkles size={16} />
          </span>
          <div className="min-w-0">
            <p className="text-sm font-medium text-zinc-100">Latest proof: {summary.latestTitle}</p>
            <p className="mt-1 text-xs leading-relaxed text-zinc-500">
              Evidence lane turns the audit trail into a trust surface: what can be shown to buyers, what proves system reliability, and where proof references are missing.
            </p>
          </div>
        </div>
      </section>

      <div className="grid gap-4 xl:grid-cols-2">
        <EvidenceRail title="Buyer Proof" detail="Client, job, consulting, and revenue-adjacent receipts." icon={ShieldCheck} items={groups.buyer} onInspect={setSelected} />
        <EvidenceRail title="System Proof" detail="Mission Control, automation, cron, agent, and infrastructure receipts." icon={FileCheck2} items={groups.system} onInspect={setSelected} />
        <EvidenceRail title="Content Assets" detail="Posts, teardown drafts, proof assets, and distribution-ready artifacts." icon={FolderOpen} items={groups.content} onInspect={setSelected} />
        <EvidenceRail title="Proof Gaps" detail="Entries that need better files, links, or buyer-readable references." icon={AlertTriangle} items={groups.gaps} onInspect={setSelected} />
      </div>

      <InspectionDrawer signal={selected} onClose={() => setSelected(null)} />
    </main>
  );
}
