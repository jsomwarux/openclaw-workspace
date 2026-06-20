"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { Archive, RefreshCw } from "lucide-react";
import { InspectionDrawer } from "@/components/mission-control/InspectionDrawer";
import { StateBlock } from "@/components/mission-control/StateBlock";
import { taskToSignal } from "@/lib/mission-control/adapters";
import { useMissionControlData } from "@/lib/mission-control/hooks";
import type { Signal, SignalPriority } from "@/lib/mission-control/types";
import { deferTaskPatch } from "@/lib/mission-control/work-actions";
import { filterWorkSignals, type WorkFilter } from "@/lib/mission-control/work-filters";
import { priorityBadgeClassName, priorityRailClassName } from "@/lib/mission-control/work-priority";
import { statusOptions, toTaskStatus, type TaskStatus } from "@/lib/mission-control/work-status";
import { cn, formatRelative } from "@/lib/utils";

const filters: { id: WorkFilter; label: string }[] = [
  { id: "all", label: "All" },
  { id: "jt", label: "JT" },
  { id: "eve", label: "Eve" },
  { id: "high", label: "High" },
  { id: "blocked", label: "Blocked/Stale" },
  { id: "done", label: "Done" },
];

function statusColor(status: Signal["status"]) {
  if (status === "done") return "bg-emerald-500";
  if (status === "failed" || status === "blocked") return "bg-red-500";
  if (status === "stale") return "bg-amber-500";
  if (status === "awaiting-decision" || status === "awaiting-approval") return "bg-[#f0883e]";
  return "bg-blue-500";
}

export default function WorkPage() {
  const { tasks, loading, errors, refresh } = useMissionControlData();
  const [filter, setFilter] = useState<WorkFilter>("all");
  const [selected, setSelected] = useState<Signal | null>(null);
  const [updatingId, setUpdatingId] = useState<string | null>(null);
  const [localTasks, setLocalTasks] = useState<any[] | null>(null);

  const sourceTasks = localTasks ?? tasks;
  const taskSignals = useMemo(() => sourceTasks.map(taskToSignal), [sourceTasks]);
  const filtered = useMemo(() => filterWorkSignals(taskSignals, filter), [filter, taskSignals]);
  const doneCount = useMemo(() => taskSignals.filter((signal) => signal.status === "done").length, [taskSignals]);

  async function updateTask(
    signal: Signal,
    patch: { status?: TaskStatus | "archived"; priority?: SignalPriority },
    options: { closeDrawer?: boolean } = {},
  ) {
    if (signal.source !== "task") return;
    const updatedAt = Date.now();
    setUpdatingId(signal.id);
    setLocalTasks((prev) =>
      (prev ?? tasks).map((item) => (item._id === signal.id ? { ...item, ...patch, updatedAt } : item)),
    );
    setSelected((current) => {
      if (!current || current.id !== signal.id) return current;
      const raw = typeof current.raw === "object" && current.raw ? current.raw : {};
      return taskToSignal({ ...raw, _id: current.id, title: current.title, assignee: current.owner, priority: current.priority ?? "medium", ...patch, updatedAt } as any);
    });
    try {
      await fetch("/api/tasks", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: signal.id, ...patch }),
      });
      await refresh();
      setLocalTasks(null);
      if (options.closeDrawer) setSelected(null);
    } finally {
      setUpdatingId(null);
    }
  }

  async function updateStatus(signal: Signal, nextStatus: TaskStatus) {
    await updateTask(signal, { status: nextStatus });
  }

  async function updatePriority(signal: Signal, priority: SignalPriority) {
    await updateTask(signal, { priority });
  }

  async function deferTask(signal: Signal) {
    await updateTask(signal, deferTaskPatch());
  }

  async function archiveTask(signal: Signal) {
    await updateTask(signal, { status: "archived" }, { closeDrawer: true });
  }

  function StatusControls({ signal }: { signal: Signal }) {
    const currentStatus = toTaskStatus(signal.status);
    const busy = updatingId === signal.id;

    return (
      <div className="flex min-w-0 flex-wrap gap-1.5 md:justify-end" aria-label={`Status for ${signal.title}`}>
        {statusOptions.map((option) => {
          const active = option.value === currentStatus;
          return (
            <button
              key={option.value}
              type="button"
              onClick={() => updateStatus(signal, option.value)}
              disabled={busy || active}
              className={cn(
                "h-8 rounded-md border px-2.5 text-[11px] font-medium transition-colors",
                active
                  ? "border-emerald-500/40 bg-emerald-500/10 text-emerald-300"
                  : "border-[#20262d] bg-[#0f1316] text-zinc-500 hover:border-[#38414a] hover:text-zinc-200",
                busy && "cursor-wait opacity-70",
              )}
            >
              {option.label}
            </button>
          );
        })}
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0b0d] p-4 sm:p-6">
      <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-blue-300">Work</p>
          <h1 className="mt-1 text-2xl font-semibold tracking-tight text-zinc-100">Task router</h1>
          <p className="mt-1 text-xs text-zinc-500">
            Active Convex tasks for routing, with recently completed work kept in Done until archival.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Link
            href="/history"
            className="flex w-fit items-center gap-2 rounded-md border border-[#20262d] bg-[#0f1316] px-3 py-2 text-xs text-zinc-300 hover:border-[#38414a]"
          >
            <Archive size={13} />
            History
          </Link>
          <button
            onClick={refresh}
            className="flex w-fit items-center gap-2 rounded-md border border-[#20262d] bg-[#0f1316] px-3 py-2 text-xs text-zinc-300 hover:border-[#38414a]"
          >
            <RefreshCw size={13} className={loading ? "animate-spin" : ""} />
            Refresh
          </button>
        </div>
      </div>

      {errors.tasks && <StateBlock kind="error" title="/api/tasks unreachable" detail={errors.tasks} className="mb-4" />}

      <div className="mb-4 flex flex-wrap gap-2">
        {filters.map((item) => (
          <button
            key={item.id}
            onClick={() => setFilter(item.id)}
            className={cn(
              "rounded-md border px-3 py-1.5 text-xs transition-colors",
              filter === item.id
                ? "border-blue-800 bg-blue-950/40 text-blue-300"
                : "border-[#20262d] bg-[#0f1316] text-zinc-500 hover:text-zinc-200",
            )}
          >
            {item.label}
            {item.id === "done" && doneCount > 0 ? <span className="ml-1 text-[10px] text-zinc-500">{doneCount}</span> : null}
          </button>
        ))}
      </div>

      <section className="rounded-xl border border-[#20262d] bg-[#0d1014]">
        <div className="grid grid-cols-[18px_1fr_96px_110px_90px_180px] gap-3 border-b border-[#20262d] px-4 py-3 font-mono text-[10px] uppercase tracking-wider text-zinc-600 max-md:hidden">
          <span />
          <span>Task</span>
          <span>Owner</span>
          <span>Priority</span>
          <span>Updated</span>
          <span className="text-right">Status</span>
        </div>
        <div className="divide-y divide-[#16191d]">
          {loading && filtered.length === 0 ? (
            <div className="p-4">
              <StateBlock kind="loading" title="Loading work lane" detail="Pulling current task data." />
            </div>
          ) : filtered.length === 0 ? (
            <div className="p-4">
              <StateBlock kind="empty" title="No tasks match this filter" detail="Clear filters or check the legacy task board." />
            </div>
          ) : (
            filtered.map((signal) => (
              <div
                key={signal.id}
                className={cn(
                  "grid grid-cols-1 gap-3 border-l-2 px-4 py-4 hover:bg-white/[0.02] md:grid-cols-[18px_1fr_96px_110px_90px_180px] md:items-center md:py-3",
                  priorityRailClassName(signal.priority),
                )}
              >
                <span className={cn("hidden h-3 w-3 rounded-full md:block", statusColor(signal.status), updatingId === signal.id && "animate-pulse")} />
                <button onClick={() => setSelected(signal)} className="min-w-0 text-left">
                  <p className="truncate text-sm font-medium text-zinc-100">{signal.title}</p>
                  <p className="mt-0.5 line-clamp-1 text-[11px] text-zinc-600">{signal.context || signal.project || signal.status}</p>
                </button>
                <div className="flex flex-wrap items-center gap-2 md:contents">
                  <span className="w-fit rounded bg-[#16191d] px-2 py-1 text-[10px] uppercase text-zinc-400">{signal.owner}</span>
                  <span className={cn("w-fit rounded border px-2 py-1 text-[10px] uppercase", priorityBadgeClassName(signal.priority))}>
                    {signal.priority ?? "none"}
                  </span>
                  <span className="text-[10px] text-zinc-600">{formatRelative(signal.updatedAt)}</span>
                </div>
                <StatusControls signal={signal} />
              </div>
            ))
          )}
        </div>
      </section>

      <InspectionDrawer
        signal={selected}
        onClose={() => setSelected(null)}
        updating={selected ? updatingId === selected.id : false}
        onStatusChange={updateStatus}
        onPriorityChange={updatePriority}
        onDefer={deferTask}
        onArchive={archiveTask}
      />
    </div>
  );
}
