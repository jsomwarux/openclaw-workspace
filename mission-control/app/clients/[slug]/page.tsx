"use client";

import { use, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { ArrowLeft, Check, ChevronDown, ChevronRight, FileCheck2, Loader2 } from "lucide-react";
import { InspectionDrawer } from "@/components/mission-control/InspectionDrawer";
import { StateBlock } from "@/components/mission-control/StateBlock";
import { taskToSignal } from "@/lib/mission-control/adapters";
import { formatMoney } from "@/lib/mission-control/cash-strip";
import {
  nextMilestone,
  stageBadgeClassName,
  stageLabel,
  type ClientTask,
  type EnrichedClient,
} from "@/lib/mission-control/clients";
import type { Signal, SignalPriority } from "@/lib/mission-control/types";
import { priorityBadgeClassName, priorityRailClassName, sortWorkSignals } from "@/lib/mission-control/work-priority";
import { cn, formatRelative } from "@/lib/utils";

function statusColor(status: Signal["status"]) {
  if (status === "done") return "bg-emerald-500";
  if (status === "failed" || status === "blocked") return "bg-red-500";
  if (status === "stale") return "bg-amber-500";
  if (status === "awaiting-decision" || status === "awaiting-approval") return "bg-[#f0883e]";
  return "bg-blue-500";
}

export default function ClientDetailPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = use(params);
  const [client, setClient] = useState<EnrichedClient | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selected, setSelected] = useState<Signal | null>(null);
  const [updatingId, setUpdatingId] = useState<string | null>(null);
  const [proofPromptId, setProofPromptId] = useState<string | null>(null);
  const [proofValue, setProofValue] = useState("");
  const [showOlder, setShowOlder] = useState(false);

  async function load() {
    try {
      const res = await fetch("/api/clients");
      if (!res.ok) throw new Error(`/api/clients returned ${res.status}`);
      const json = await res.json();
      const found = (json.clients ?? []).find((c: EnrichedClient) => c.slug === slug) ?? null;
      setClient(found);
      setError(found ? null : `No client found for "${slug}"`);
    } catch (e) {
      setError(e instanceof Error ? e.message : "failed to load");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [slug]);

  const openSignals = useMemo(
    () => (client ? sortWorkSignals(client.openTasks.map((t) => taskToSignal(t as any))) : []),
    [client],
  );

  // All completion flows through the existing /api/tasks PATCH mutation.
  async function patchTask(id: string, patch: Record<string, unknown>) {
    setUpdatingId(id);
    try {
      await fetch("/api/tasks", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id, ...patch }),
      });
      await load();
      setSelected(null);
    } finally {
      setUpdatingId(null);
    }
  }

  // proofRequired tasks must not close without an evidence URL/path.
  function requestComplete(signal: Signal) {
    if (signal.proofRequired) {
      setSelected(null);
      setProofValue("");
      setProofPromptId(signal.id);
      return;
    }
    void patchTask(signal.id, { status: "done" });
  }

  function confirmProofComplete(signal: Signal) {
    const evidence = proofValue.trim();
    if (!evidence) return;
    const base = (signal.context ?? "").trim();
    const description = base ? `${base}\n\nProof: ${evidence}` : `Proof: ${evidence}`;
    setProofPromptId(null);
    void patchTask(signal.id, { status: "done", description });
  }

  function updateStatus(signal: Signal, status: "todo" | "in-progress" | "done") {
    if (status === "done") return requestComplete(signal);
    void patchTask(signal.id, { status });
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0a0b0d] p-4 sm:p-6">
        <StateBlock kind="loading" title="Loading client" detail="Reading client status, tasks, and proof assets." />
      </div>
    );
  }

  if (error || !client) {
    return (
      <div className="min-h-screen bg-[#0a0b0d] p-4 sm:p-6">
        <Link href="/clients" className="mb-4 inline-flex items-center gap-1.5 text-xs text-zinc-400 hover:text-zinc-200">
          <ArrowLeft size={13} /> Clients
        </Link>
        <StateBlock kind="error" title="Client unavailable" detail={error ?? "Unknown error"} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0b0d] p-4 sm:p-6">
      <Link href="/clients" className="mb-4 inline-flex items-center gap-1.5 text-xs text-zinc-400 hover:text-zinc-200">
        <ArrowLeft size={13} /> Clients
      </Link>

      <div className="mb-5 flex flex-wrap items-center gap-3">
        <span className="text-2xl leading-none">{client.emoji ?? "🧩"}</span>
        <h1 className="text-2xl font-semibold tracking-tight text-zinc-100">{client.name}</h1>
        <span className={cn("rounded border px-2 py-0.5 text-[10px] font-medium uppercase", stageBadgeClassName(client.stage))}>
          {stageLabel[client.stage]}
        </span>
      </div>
      {client.status && <p className="mb-1 max-w-3xl text-xs leading-relaxed text-zinc-400">{client.status}</p>}
      {client.memoryPath && <p className="mb-6 font-mono text-[10px] text-zinc-600">{client.memoryPath}</p>}

      <div className="grid gap-5 lg:grid-cols-[1.6fr_0.7fr]">
        {/* Left — work */}
        <div className="space-y-6">
          <section>
            <h2 className="mb-3 text-sm font-semibold text-zinc-100">Open work ({openSignals.length})</h2>
            <div className="overflow-hidden rounded-xl border border-[#20262d] bg-[#0d1014] divide-y divide-[#16191d]">
              {openSignals.length === 0 ? (
                <div className="p-4">
                  <StateBlock kind="empty" title="No open work for this client" />
                </div>
              ) : (
                openSignals.map((signal) => {
                  const busy = updatingId === signal.id;
                  const prompting = proofPromptId === signal.id;
                  return (
                    <div key={signal.id} className={cn("border-l-2 px-4 py-3", priorityRailClassName(signal.priority))}>
                      <div className="flex items-center gap-3">
                        <span className={cn("hidden h-2.5 w-2.5 shrink-0 rounded-full sm:block", statusColor(signal.status), busy && "animate-pulse")} />
                        <button onClick={() => setSelected(signal)} className="min-w-0 flex-1 text-left">
                          <p className="truncate text-sm font-medium text-zinc-100">{signal.title}</p>
                          <p className="mt-0.5 line-clamp-1 text-[11px] text-zinc-600">{signal.context || signal.status}</p>
                        </button>
                        <span className={cn("hidden shrink-0 rounded border px-2 py-0.5 text-[10px] uppercase sm:inline", priorityBadgeClassName(signal.priority))}>
                          {signal.priority ?? "none"}
                        </span>
                        {signal.proofRequired && !prompting && (
                          <span className="hidden shrink-0 items-center gap-1 text-[10px] text-amber-300 sm:flex" title="Proof required to complete">
                            <FileCheck2 size={12} /> proof
                          </span>
                        )}
                        <button
                          type="button"
                          disabled={busy}
                          onClick={() => requestComplete(signal)}
                          className="flex h-8 shrink-0 items-center gap-1.5 rounded-md border border-emerald-500/40 bg-emerald-500/10 px-3 text-[11px] font-medium text-emerald-300 transition-colors hover:bg-emerald-500/20 disabled:opacity-60"
                        >
                          {busy ? <Loader2 size={13} className="animate-spin" /> : <Check size={13} />}
                          Done
                        </button>
                      </div>

                      {prompting && (
                        <div className="mt-3 rounded-md border border-amber-500/30 bg-amber-500/5 p-3">
                          <p className="mb-2 flex items-center gap-1.5 text-[11px] font-medium text-amber-200">
                            <FileCheck2 size={12} /> Evidence required — paste a URL or file path to complete
                          </p>
                          <div className="flex flex-wrap gap-2">
                            <input
                              autoFocus
                              value={proofValue}
                              onChange={(e) => setProofValue(e.target.value)}
                              onKeyDown={(e) => e.key === "Enter" && confirmProofComplete(signal)}
                              placeholder="https://… or memory/clients/…/proof.md"
                              className="min-w-0 flex-1 rounded border border-[#2b333c] bg-[#0f1316] px-2.5 py-1.5 text-xs text-zinc-200 placeholder-zinc-600 focus:border-amber-500/50 focus:outline-none"
                            />
                            <button
                              type="button"
                              disabled={!proofValue.trim() || busy}
                              onClick={() => confirmProofComplete(signal)}
                              className="h-8 rounded-md border border-emerald-500/40 bg-emerald-500/10 px-3 text-[11px] font-medium text-emerald-300 transition-colors hover:bg-emerald-500/20 disabled:cursor-not-allowed disabled:opacity-50"
                            >
                              Complete with proof
                            </button>
                            <button
                              type="button"
                              onClick={() => setProofPromptId(null)}
                              className="h-8 rounded-md border border-[#2b333c] px-3 text-[11px] text-zinc-400 hover:text-zinc-200"
                            >
                              Cancel
                            </button>
                          </div>
                        </div>
                      )}
                    </div>
                  );
                })
              )}
            </div>
          </section>

          <section>
            <h2 className="mb-3 text-sm font-semibold text-zinc-100">Completed this week ({client.completedThisWeek.length})</h2>
            {client.completedThisWeek.length === 0 ? (
              <StateBlock kind="empty" title="Nothing completed in the last 7 days" />
            ) : (
              <div className="overflow-hidden rounded-xl border border-[#20262d] bg-[#0d1014] divide-y divide-[#16191d]">
                {client.completedThisWeek.map((t) => (
                  <CompletedRow key={t._id} task={t} />
                ))}
              </div>
            )}
          </section>

          {client.olderCompletions.length > 0 && (
            <section className="rounded-lg border border-[#20262d] bg-[#0d1014]">
              <button
                type="button"
                onClick={() => setShowOlder((v) => !v)}
                className="flex w-full items-center justify-between gap-3 px-4 py-3 text-left"
              >
                <span className="font-mono text-[11px] uppercase tracking-wider text-zinc-400">
                  Older completions ({client.olderCompletions.length})
                </span>
                {showOlder ? <ChevronDown size={14} className="text-zinc-600" /> : <ChevronRight size={14} className="text-zinc-600" />}
              </button>
              {showOlder && (
                <div className="divide-y divide-[#16191d] border-t border-[#16191d]">
                  {client.olderCompletions.map((t) => (
                    <CompletedRow key={t._id} task={t} />
                  ))}
                </div>
              )}
            </section>
          )}
        </div>

        {/* Right — rails */}
        <div className="space-y-5">
          <section className="rounded-lg border border-[#20262d] bg-[#0d1014] p-4">
            <h3 className="mb-3 text-sm font-semibold text-zinc-100">Money</h3>
            <dl className="space-y-2 text-xs">
              <Row label="Collected to date" value={formatMoney(client.collected)} tone="good" />
              <Row label="Open $" value={client.openDollars > 0 ? formatMoney(client.openDollars) : "—"} />
              <Row label="Next milestone" value={nextMilestone(client)} />
            </dl>
          </section>

          <section className="rounded-lg border border-[#20262d] bg-[#0d1014] p-4">
            <h3 className="mb-3 text-sm font-semibold text-zinc-100">Proof</h3>
            {client.proofAssets.length === 0 ? (
              <StateBlock kind="gap" title="No proof assets on file" detail={`Looked in ${client.memoryPath}/proof-assets/`} />
            ) : (
              <ul className="space-y-1.5">
                {client.proofAssets.slice(0, 12).map((file) => (
                  <li key={file} className="truncate font-mono text-[11px] text-zinc-400">{file}</li>
                ))}
                {client.proofAssets.length > 12 && (
                  <li className="text-[10px] text-zinc-600">+{client.proofAssets.length - 12} more</li>
                )}
              </ul>
            )}
          </section>

          <section className="rounded-lg border border-[#20262d] bg-[#0d1014] p-4">
            <h3 className="mb-2 text-sm font-semibold text-zinc-100">Referral</h3>
            <span
              className={cn(
                "inline-flex rounded border px-2 py-1 text-[11px] font-medium",
                client.referralEligible
                  ? "border-emerald-500/40 bg-emerald-500/10 text-emerald-300"
                  : "border-zinc-700 bg-zinc-900/80 text-zinc-400",
              )}
            >
              {client.referralEligible ? "Referral ask eligible" : "Referral gated"}
            </span>
          </section>
        </div>
      </div>

      <InspectionDrawer
        signal={selected}
        onClose={() => setSelected(null)}
        updating={selected ? updatingId === selected.id : false}
        onStatusChange={(s, status) => updateStatus(s, status)}
        onPriorityChange={(s, priority: SignalPriority) => patchTask(s.id, { priority })}
        onArchive={(s) => patchTask(s.id, { status: "archived" })}
      />
    </div>
  );
}

function CompletedRow({ task }: { task: ClientTask }) {
  return (
    <div className="flex items-center gap-3 px-4 py-2.5">
      <Check size={13} className="shrink-0 text-emerald-400" />
      <p className="min-w-0 flex-1 truncate text-xs text-zinc-300">{task.title}</p>
      <span className="shrink-0 text-[10px] text-zinc-600">{task.updatedAt ? formatRelative(task.updatedAt) : ""}</span>
    </div>
  );
}

function Row({ label, value, tone }: { label: string; value: string; tone?: "good" }) {
  return (
    <div className="flex items-center justify-between gap-3">
      <dt className="text-zinc-500">{label}</dt>
      <dd className={cn("text-right font-medium", tone === "good" ? "text-emerald-300" : "text-zinc-200")}>{value}</dd>
    </div>
  );
}
