"use client";

import { Archive, Clock3, X } from "lucide-react";
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
}: InspectionDrawerProps) {
  if (!signal) return null;

  const currentStatus = toTaskStatus(signal.status);
  const isTask = signal.source === "task";

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
          <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-500">Why This Is Ranked Here</p>
          <p className="mt-2 text-xs leading-relaxed text-zinc-300">{rankingExplanation(signal)}</p>
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
          </div>
        </section>
      </aside>
    </div>
  );
}
