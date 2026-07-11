"use client";

import { useState, type ReactNode } from "react";
import { AlertTriangle, Bell, Bot, ChevronDown, ChevronRight, CircleDollarSign } from "lucide-react";
import { InspectionDrawer } from "@/components/mission-control/InspectionDrawer";
import { StateBlock } from "@/components/mission-control/StateBlock";
import { useMissionControlData } from "@/lib/mission-control/hooks";
import { primaryActionVerb, reasonChips, reasonToneClassName } from "@/lib/mission-control/reason-codes";
import type { Signal, SignalPriority } from "@/lib/mission-control/types";
import { cn, formatRelative } from "@/lib/utils";

const DAY_MS = 24 * 60 * 60 * 1000;
const SNOOZE_DAYS = 7;

type TaskPatch = {
  status?: string;
  priority?: SignalPriority;
  assignee?: "jt" | "eve" | "both";
  pipelineStage?: string;
  snoozedUntil?: number;
  waitingOn?: Signal["waitingOn"];
};

function ReasonChipRow({ codes, limit }: { codes?: string[]; limit?: number }) {
  const chips = reasonChips(codes);
  const shown = limit ? chips.slice(0, limit) : chips;
  if (shown.length === 0) return null;

  return (
    <div className="flex flex-wrap items-center gap-1.5">
      {shown.map((chip) => (
        <span
          key={chip.code}
          title={chip.code}
          className={cn("rounded border px-2 py-0.5 text-[10px] font-medium", reasonToneClassName[chip.tone])}
        >
          {chip.label}
        </span>
      ))}
    </div>
  );
}

function CollapsedStrip({
  title,
  count,
  tone,
  icon: Icon,
  children,
}: {
  title: string;
  count: number;
  tone: "neutral" | "eve" | "risk";
  icon: typeof Bell;
  children: ReactNode;
}) {
  const [open, setOpen] = useState(false);
  const toneClass =
    tone === "risk" ? "text-red-300" : tone === "eve" ? "text-purple-300" : "text-zinc-400";

  return (
    <section className="rounded-lg border border-[#20262d] bg-[#0d1014]">
      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        className="flex w-full items-center justify-between gap-3 px-4 py-3 text-left"
      >
        <span className={cn("flex items-center gap-2 font-mono text-[11px] uppercase tracking-wider", toneClass)}>
          <Icon size={13} />
          {title} ({count})
        </span>
        {open ? <ChevronDown size={14} className="text-zinc-600" /> : <ChevronRight size={14} className="text-zinc-600" />}
      </button>
      {open && <div className="space-y-2 border-t border-[#16191d] p-3">{children}</div>}
    </section>
  );
}

export default function CockpitPage() {
  const { queue, eveHandling, waitingOn, risk, cash, cashPending, loading, degraded, lastUpdated, refresh } =
    useMissionControlData();
  const [selected, setSelected] = useState<Signal | null>(null);
  const [updatingId, setUpdatingId] = useState<string | null>(null);

  const now = Date.now();
  const nowCard = queue[0] ?? null;
  const upNext = queue.slice(1, 7);

  async function patchTask(signal: Signal, patch: TaskPatch, options: { closeDrawer?: boolean } = {}) {
    if (signal.source !== "task") return;
    setUpdatingId(signal.id);
    try {
      await fetch("/api/tasks", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: signal.id, ...patch }),
      });
      await refresh();
      if (options.closeDrawer) setSelected(null);
    } finally {
      setUpdatingId(null);
    }
  }

  function nudge(signal: Signal) {
    if (!signal.waitingOn) return;
    return patchTask(signal, { waitingOn: { ...signal.waitingOn, since: Date.now() } }, { closeDrawer: true });
  }

  async function runPrimaryAction(signal: Signal) {
    const verb = primaryActionVerb(signal);
    if (verb === "Approve") return patchTask(signal, { status: "done" });
    if (verb === "Nudge") return nudge(signal);
    if (verb === "Mark sent") return patchTask(signal, { pipelineStage: "sent" });
    setSelected(signal);
  }

  return (
    <div className="min-h-screen bg-[#0a0b0d] p-4 sm:p-6">
      <div className="mb-4 flex flex-wrap items-baseline justify-between gap-2">
        <div>
          <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-[#f0883e]">Cockpit</p>
          <h1 className="mt-1 text-xl font-semibold tracking-tight text-zinc-100">One decision at a time</h1>
        </div>
        <p className="font-mono text-[10px] uppercase tracking-wider text-zinc-600">
          {lastUpdated ? `updated ${formatRelative(lastUpdated)}` : "loading…"}
        </p>
      </div>

      {degraded.length > 0 && (
        <StateBlock
          kind="stale"
          title="Some data routes are degraded"
          detail={`Showing cached or partial data for: ${degraded.join(", ")}.`}
          className="mb-4"
        />
      )}

      {/* Band 1 — cash strip */}
      <section
        className={cn(
          "mb-5 flex items-center gap-3 rounded-lg border px-4 py-3",
          cashPending
            ? "border-[#20262d] bg-[#0f1316] text-zinc-500"
            : cash.available
              ? "border-emerald-900/40 bg-emerald-950/10 text-emerald-300"
              : "border-amber-900/60 bg-amber-950/20 text-amber-300",
        )}
      >
        <CircleDollarSign size={16} className="shrink-0" />
        <p className="font-mono text-xs tracking-wide sm:text-sm">{cashPending ? "reading cash metrics…" : cash.text}</p>
      </section>

      {/* Band 2 — NOW */}
      <section className="mb-5">
        <p className="mb-2 font-mono text-[11px] uppercase tracking-[0.2em] text-[#f0883e]">Now</p>
        {loading && !nowCard ? (
          <StateBlock kind="loading" title="Ranking current work" detail="Pulling tasks, crons, proofs, agents, and cash." />
        ) : !nowCard ? (
          <StateBlock kind="empty" title="Queue clear. Protect the block." />
        ) : (
          <article className="rounded-xl border-2 border-[#f0883e]/40 bg-[#12161a] p-6 shadow-[0_0_40px_-20px_rgba(240,136,62,0.5)] sm:p-8">
            <div className="flex flex-wrap items-center gap-2 text-[10px] uppercase tracking-wider">
              <span className="rounded bg-[#f0883e]/10 px-2 py-1 font-semibold text-[#f0883e]">
                {nowCard.status.replace(/-/g, " ")}
              </span>
              <span className="text-zinc-600">{nowCard.lane}</span>
              <span className="text-zinc-600">{formatRelative(nowCard.updatedAt)}</span>
            </div>

            <h2 className="mt-4 text-2xl font-semibold leading-tight tracking-tight text-zinc-50 sm:text-3xl">
              {nowCard.title}
            </h2>
            <p className="mt-3 line-clamp-2 text-sm leading-relaxed text-zinc-400">
              {nowCard.context || nowCard.project || "No context attached yet."}
            </p>

            <div className="mt-5">
              <ReasonChipRow codes={nowCard.reasonCodes} />
            </div>

            <div className="mt-6 flex flex-wrap items-center gap-3">
              <button
                type="button"
                disabled={updatingId === nowCard.id}
                onClick={() => runPrimaryAction(nowCard)}
                className="h-11 rounded-md bg-[#f0883e] px-6 text-sm font-semibold text-[#12161a] transition-opacity hover:opacity-90 disabled:opacity-60"
              >
                {updatingId === nowCard.id ? "Saving…" : primaryActionVerb(nowCard)}
              </button>
              <button
                type="button"
                onClick={() => setSelected(nowCard)}
                className="h-11 rounded-md border border-[#2b333c] px-4 text-sm text-zinc-400 transition-colors hover:border-[#38414a] hover:text-zinc-200"
              >
                Inspect
              </button>
            </div>
          </article>
        )}
      </section>

      {/* Band 3 — UP NEXT */}
      <section className="mb-5">
        <p className="mb-2 font-mono text-[11px] uppercase tracking-[0.2em] text-zinc-600">Up next</p>
        {upNext.length === 0 ? (
          <StateBlock kind="empty" title="Nothing else is queued behind this." />
        ) : (
          <div className="divide-y divide-[#16191d] overflow-hidden rounded-lg border border-[#20262d] bg-[#0d1014]">
            {upNext.map((signal) => (
              <button
                key={signal.id}
                type="button"
                onClick={() => setSelected(signal)}
                className="flex w-full items-center gap-3 px-4 py-3 text-left transition-colors hover:bg-white/[0.02]"
              >
                <span className="min-w-0 flex-1">
                  <span className="block truncate text-sm text-zinc-200">{signal.title}</span>
                  <span className="mt-1 block text-[10px] uppercase text-zinc-600">
                    {signal.project || signal.lane}
                  </span>
                </span>
                <ReasonChipRow codes={signal.reasonCodes} limit={1} />
                <span className="w-16 shrink-0 text-right text-[10px] text-zinc-600">{signal.ageDays}d</span>
              </button>
            ))}
          </div>
        )}
      </section>

      {/* Band 4 — collapsed strips */}
      <div className="space-y-3">
        <CollapsedStrip title="Waiting on others" count={waitingOn.length} tone="neutral" icon={Bell}>
          {waitingOn.length === 0 ? (
            <StateBlock kind="empty" title="Nobody owes you anything right now." />
          ) : (
            waitingOn.map((signal) => {
              const days = Math.max(0, Math.floor((now - (signal.waitingOn?.since ?? now)) / DAY_MS));
              return (
                <div
                  key={signal.id}
                  className="flex items-center gap-3 rounded-md border border-[#20262d] bg-[#0f1316] px-3 py-2"
                >
                  <button
                    type="button"
                    onClick={() => setSelected(signal)}
                    className="min-w-0 flex-1 truncate text-left text-xs text-zinc-300"
                  >
                    <span className="font-medium text-zinc-100">{signal.waitingOn?.who}</span>
                    <span className="text-zinc-600"> · </span>
                    {signal.waitingOn?.what}
                    <span className="text-zinc-600"> · {days}d</span>
                  </button>
                  <button
                    type="button"
                    disabled={updatingId === signal.id}
                    onClick={() => nudge(signal)}
                    className="h-8 shrink-0 rounded-md border border-[#2b333c] bg-[#12161a] px-3 text-[11px] font-medium text-zinc-300 transition-colors hover:border-[#f0883e]/50 hover:text-[#f0883e] disabled:opacity-60"
                  >
                    {updatingId === signal.id ? "…" : "Nudge"}
                  </button>
                </div>
              );
            })
          )}
        </CollapsedStrip>

        <CollapsedStrip title="Eve has it" count={eveHandling.length} tone="eve" icon={Bot}>
          {eveHandling.length === 0 ? (
            <StateBlock kind="empty" title="No Eve-owned work in flight." />
          ) : (
            eveHandling.map((signal) => {
              const attention = signal.status === "failed" || signal.status === "stale";
              return (
                <button
                  key={signal.id}
                  type="button"
                  onClick={() => setSelected(signal)}
                  className={cn(
                    "flex w-full items-center justify-between gap-3 rounded-md border px-3 py-2 text-left",
                    attention
                      ? "border-amber-900/60 bg-amber-950/20 text-amber-200"
                      : "border-[#20262d] bg-[#0f1316] text-zinc-300",
                  )}
                >
                  <span className="min-w-0 flex-1 truncate text-xs">{signal.title}</span>
                  <span className="shrink-0 text-[10px] uppercase text-zinc-600">
                    {attention ? signal.status : formatRelative(signal.updatedAt)}
                  </span>
                </button>
              );
            })
          )}
        </CollapsedStrip>

        {risk.length > 0 && (
          <CollapsedStrip title="Risk" count={risk.length} tone="risk" icon={AlertTriangle}>
            {risk.map((signal) => (
              <button
                key={signal.id}
                type="button"
                onClick={() => setSelected(signal)}
                className="flex w-full items-center justify-between gap-3 rounded-md border border-red-900/50 bg-red-950/10 px-3 py-2 text-left"
              >
                <span className="min-w-0 flex-1 truncate text-xs text-zinc-200">{signal.title}</span>
                <span className="shrink-0 text-[10px] uppercase text-red-300">{signal.status}</span>
              </button>
            ))}
          </CollapsedStrip>
        )}
      </div>

      <InspectionDrawer
        signal={selected}
        onClose={() => setSelected(null)}
        updating={Boolean(selected && updatingId === selected.id)}
        onSnooze={(signal) =>
          patchTask(signal, { snoozedUntil: Date.now() + SNOOZE_DAYS * DAY_MS }, { closeDrawer: true })
        }
        onNotNow={(signal) => patchTask(signal, { status: "archived" }, { closeDrawer: true })}
        onHandToEve={(signal) => patchTask(signal, { assignee: "eve" }, { closeDrawer: true })}
      />
    </div>
  );
}
