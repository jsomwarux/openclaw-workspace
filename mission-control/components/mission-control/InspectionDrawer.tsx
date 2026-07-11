"use client";

import { Archive, Clock3, UserPlus, X } from "lucide-react";
import { useTaskAudit } from "@/lib/mission-control/hooks";
import { reasonChips, reasonToneClassName } from "@/lib/mission-control/reason-codes";
import type { Signal } from "@/lib/mission-control/types";
import { priorityOptions, rankingExplanation } from "@/lib/mission-control/work-actions";
import { priorityBadgeClassName } from "@/lib/mission-control/work-priority";
import { statusOptions, toTaskStatus, type TaskStatus } from "@/lib/mission-control/work-status";
import { cn, formatRelative } from "@/lib/utils";
import { StateBlock } from "./StateBlock";

type InspectionDrawerProps = {
  signal: Signal | null;
  onClose: () => void;
  updating?: boolean;
  onStatusChange?: (signal: Signal, status: TaskStatus) => void;
  onPriorityChange?: (signal: Signal, priority: NonNullable<Signal["priority"]>) => void;
  onArchive?: (signal: Signal) => void;
  onDefer?: (signal: Signal) => void;
  onSnooze?: (signal: Signal) => void;
  onNotNow?: (signal: Signal) => void;
  onHandToEve?: (signal: Signal) => void;
};

function statusClass(status: Signal["status"]) {
  if (status === "failed" || status === "blocked") return "text-red-300 border-red-900/60 bg-red-950/20";
  if (status === "stale") return "text-amber-300 border-amber-900/60 bg-amber-950/20";
  if (status === "done") return "text-emerald-300 border-emerald-900/60 bg-emerald-950/20";
  return "text-blue-300 border-blue-900/60 bg-blue-950/20";
}

export function InspectionDrawer({
  signal,
  onClose,
  updating = false,
  onStatusChange,
  onPriorityChange,
  onArchive,
  onDefer,
  onSnooze,
  onNotNow,
  onHandToEve,
}: InspectionDrawerProps) {
  const auditTaskId = signal?.source === "task" ? signal.id : null;
  const { entries: audit, loading: auditLoading } = useTaskAudit(auditTaskId);

  if (!signal) return null;

  const currentStatus = toTaskStatus(signal.status);
  const isTask = signal.source === "task";
  const chips = reasonChips(signal.reasonCodes);
  const hasSecondaryActions = Boolean(onSnooze || onNotNow || onHandToEve);
  const hasWorkActions = Boolean(onDefer || onArchive);

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/70" onClick={onClose}>
      <aside
        className="h-full w-full max-w-lg overflow-y-auto border-l border-[#20262d] bg-[#0d1014] p-5 shadow-2xl"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="flex items-start justify-between gap-4">
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <span className={cn("rounded border px-2 py-0.5 text-[10px] font-semibold uppercase", statusClass(signal.status))}>
                {signal.status}
              </span>
              <span className="rounded border border-[#20262d] bg-[#111] px-2 py-0.5 text-[10px] uppercase text-zinc-500">
                {signal.source} · {signal.lane}
              </span>
            </div>
            <h2 className="mt-3 text-lg font-semibold leading-snug text-zinc-100">{signal.title}</h2>
            <p className="mt-1 text-[11px] text-zinc-600">
              {signal.project ? `${signal.project} · ` : ""}
              Updated {formatRelative(signal.updatedAt)}
            </p>
          </div>
          <button onClick={onClose} className="rounded p-1 text-zinc-500 hover:bg-white/5 hover:text-zinc-200">
            <X size={16} />
          </button>
        </div>

        <section className="mt-6">
          <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-500">Context</p>
          <p className="mt-2 whitespace-pre-wrap text-xs leading-relaxed text-zinc-300">
            {signal.context || "No extra context attached yet."}
          </p>
        </section>

        {signal.eveRead && (
          <section className="mt-6 rounded-lg border border-purple-900/40 bg-purple-950/10 p-3">
            <p className="text-[10px] font-semibold uppercase tracking-wider text-purple-300">Eve's Read</p>
            <p className="mt-2 text-xs leading-relaxed text-zinc-300">{signal.eveRead}</p>
          </section>
        )}

        <section className="mt-6">
          <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-500">Evidence</p>
          <div className="mt-2 space-y-2">
            {signal.evidence.length > 0 ? (
              signal.evidence.map((ref, index) =>
                ref.href ? (
                  <a
                    key={`${ref.label}-${index}`}
                    href={ref.href.startsWith("http") ? ref.href : undefined}
                    target="_blank"
                    rel="noreferrer"
                    className="block rounded border border-[#20262d] bg-[#111] p-3 text-xs text-emerald-300 hover:border-emerald-900/60"
                  >
                    {ref.label}
                    <span className="ml-2 text-[10px] uppercase text-zinc-600">{ref.quality}</span>
                  </a>
                ) : (
                  <StateBlock key={`${ref.label}-${index}`} kind="gap" title={ref.label} detail="No clickable evidence link is available." />
                ),
              )
            ) : (
              <StateBlock kind="gap" title="Evidence gap" detail="This item has no proof reference yet." />
            )}
          </div>
        </section>

        <section className="mt-6 rounded-lg border border-[#20262d] bg-[#0b0d0f] p-3">
          <div className="flex items-start justify-between gap-3">
            <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-500">Why This Is Ranked Here</p>
            <span className="shrink-0 rounded border border-[#2b333c] bg-[#0f1316] px-2 py-1 font-mono text-xs font-semibold text-zinc-200">
              {signal.score ?? 0}
              <span className="ml-1 text-[9px] font-normal uppercase text-zinc-600">score</span>
            </span>
          </div>
          <p className="mt-2 text-xs leading-relaxed text-zinc-300">{rankingExplanation(signal)}</p>

          <div className="mt-3">
            <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-600">Reason codes</p>
            {chips.length > 0 ? (
              <div className="mt-2 flex flex-wrap gap-1.5">
                {chips.map((chip) => (
                  <span
                    key={chip.code}
                    title={chip.code}
                    className={cn(
                      "rounded border px-2 py-0.5 text-[10px] font-medium",
                      reasonToneClassName[chip.tone],
                    )}
                  >
                    {chip.label}
                  </span>
                ))}
              </div>
            ) : (
              <p className="mt-2 text-[11px] text-zinc-600">
                The scorer attached no reason codes, so this item is ranked on recency alone.
              </p>
            )}
          </div>

          <div className="mt-4">
            <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-600">Rank audit</p>
            {!isTask ? (
              <p className="mt-2 text-[11px] text-zinc-600">Only tasks carry a rank audit trail.</p>
            ) : auditLoading ? (
              <p className="mt-2 text-[11px] text-zinc-600">Loading audit trail…</p>
            ) : audit.length === 0 ? (
              <p className="mt-2 text-[11px] text-zinc-600">No rank changes recorded for this task yet.</p>
            ) : (
              <ol className="mt-2 space-y-2">
                {audit.map((entry) => (
                  <li key={entry._id} className="rounded border border-[#20262d] bg-[#0f1316] p-2">
                    <div className="flex items-center justify-between gap-2 text-[10px] uppercase text-zinc-600">
                      <span>{entry.field}</span>
                      <span>
                        {entry.source} · {formatRelative(entry.ts)}
                      </span>
                    </div>
                    <p className="mt-1 text-[11px] text-zinc-300">
                      {entry.oldValue || "—"} → {entry.newValue || "—"}
                    </p>
                    {entry.evidence && <p className="mt-1 text-[11px] leading-relaxed text-zinc-500">{entry.evidence}</p>}
                  </li>
                ))}
              </ol>
            )}
          </div>
        </section>

        <section className="mt-6 rounded-lg border border-[#20262d] bg-[#0b0d0f] p-3">
          <div className="flex items-center justify-between gap-3">
            <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-500">Actions</p>
            {updating && <span className="text-[10px] uppercase text-blue-300">Saving</span>}
          </div>

          <div className="mt-4 space-y-4">
            <div>
              <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-600">Status</p>
              <div className="mt-2 grid grid-cols-3 gap-2">
                {statusOptions.map((option) => {
                  const active = option.value === currentStatus;
                  return (
                    <button
                      key={option.value}
                      type="button"
                      disabled={!isTask || updating || active}
                      onClick={() => onStatusChange?.(signal, option.value)}
                      className={cn(
                        "h-9 rounded-md border px-2 text-xs font-medium transition-colors",
                        active
                          ? "border-emerald-500/40 bg-emerald-500/10 text-emerald-300"
                          : "border-[#20262d] bg-[#101318] text-zinc-400 hover:border-[#38414a] hover:text-zinc-100",
                        (!isTask || updating) && "cursor-not-allowed opacity-60",
                      )}
                    >
                      {option.label}
                    </button>
                  );
                })}
              </div>
            </div>

            <div>
              <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-600">Priority</p>
              <div className="mt-2 grid grid-cols-3 gap-2">
                {priorityOptions.map((option) => {
                  const active = option.value === signal.priority;
                  return (
                    <button
                      key={option.value}
                      type="button"
                      disabled={!isTask || updating || active}
                      onClick={() => onPriorityChange?.(signal, option.value)}
                      className={cn(
                        "h-9 rounded-md border px-2 text-xs font-medium transition-colors",
                        active
                          ? priorityBadgeClassName(option.value)
                          : "border-[#20262d] bg-[#101318] text-zinc-400 hover:border-[#38414a] hover:text-zinc-100",
                        (!isTask || updating) && "cursor-not-allowed opacity-60",
                      )}
                    >
                      {option.label}
                    </button>
                  );
                })}
              </div>
            </div>

            {hasSecondaryActions && (
              <div className="grid grid-cols-3 gap-2">
                <button
                  type="button"
                  disabled={!isTask || updating}
                  onClick={() => onSnooze?.(signal)}
                  className="flex h-10 items-center justify-center gap-1.5 rounded-md border border-[#20262d] bg-[#101318] px-2 text-xs font-medium text-zinc-300 transition-colors hover:border-[#38414a] disabled:cursor-not-allowed disabled:opacity-60"
                  title="Hide this item from the queue for seven days"
                >
                  <Clock3 size={13} />
                  Snooze 7d
                </button>
                <button
                  type="button"
                  disabled={!isTask || updating}
                  onClick={() => onNotNow?.(signal)}
                  className="flex h-10 items-center justify-center gap-1.5 rounded-md border border-zinc-700 bg-zinc-900/80 px-2 text-xs font-medium text-zinc-300 transition-colors hover:border-zinc-500 disabled:cursor-not-allowed disabled:opacity-60"
                  title="Archive this item out of the queue"
                >
                  <Archive size={13} />
                  Not now
                </button>
                <button
                  type="button"
                  disabled={!isTask || updating}
                  onClick={() => onHandToEve?.(signal)}
                  className="flex h-10 items-center justify-center gap-1.5 rounded-md border border-purple-500/30 bg-purple-500/10 px-2 text-xs font-medium text-purple-200 transition-colors hover:border-purple-400/50 disabled:cursor-not-allowed disabled:opacity-60"
                  title="Reassign this item to Eve"
                >
                  <UserPlus size={13} />
                  Hand to Eve
                </button>
              </div>
            )}

            {hasWorkActions && (
              <div className="grid grid-cols-2 gap-2">
                <button
                  type="button"
                  disabled={!isTask || updating}
                  onClick={() => onDefer?.(signal)}
                  className="flex h-10 items-center justify-center gap-2 rounded-md border border-amber-500/30 bg-amber-500/10 px-3 text-xs font-medium text-amber-200 transition-colors hover:border-amber-400/50 disabled:cursor-not-allowed disabled:opacity-60"
                  title="Move to low priority without marking done"
                >
                  <Clock3 size={13} />
                  Defer
                </button>
                <button
                  type="button"
                  disabled={!isTask || updating}
                  onClick={() => onArchive?.(signal)}
                  className="flex h-10 items-center justify-center gap-2 rounded-md border border-zinc-700 bg-zinc-900/80 px-3 text-xs font-medium text-zinc-300 transition-colors hover:border-zinc-500 disabled:cursor-not-allowed disabled:opacity-60"
                  title="Archive this task"
                >
                  <Archive size={13} />
                  Archive
                </button>
              </div>
            )}
          </div>
        </section>
      </aside>
    </div>
  );
}
