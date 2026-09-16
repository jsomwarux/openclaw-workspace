"use client";

import { useEffect, useState } from "react";
import type { OutreachDecision, OutreachDecisionValue } from "@/lib/mission-control/outreach-decision";
import { outreachDecisionView } from "@/lib/mission-control/outreach-decision-display";
import type { Signal } from "@/lib/mission-control/types";

export function OutreachDecisionControls({ signal }: { signal: Signal }) {
  const initial = outreachDecisionView(signal);
  const [decision, setDecision] = useState<OutreachDecision | undefined>(initial && "decision" in initial ? initial.decision : undefined);
  const [saving, setSaving] = useState(false);
  const [clearing, setClearing] = useState(false);
  const [cleared, setCleared] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const view = outreachDecisionView(signal);
    setDecision(view && "decision" in view ? view.decision : undefined);
    setCleared(false);
    setError("");
  }, [signal.id, signal.outreachDecision]);

  const view = outreachDecisionView({ ...signal, outreachDecision: decision ?? signal.outreachDecision });
  if (!view) return null;
  const snapshot = view.snapshot;

  async function decide(value: OutreachDecisionValue) {
    setSaving(true);
    setError("");
    try {
      const response = await fetch("/api/tasks/outreach-decision", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          taskId: signal.id,
          candidateId: view!.candidateId,
          draftSha256: view!.draftSha256,
          snapshotSha256: view!.snapshotSha256,
          decision: value,
        }),
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error ?? `Decision request returned ${response.status}`);
      setDecision(body.decision);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : String(caught));
    } finally {
      setSaving(false);
    }
  }

  async function clearSuppressionOwners() {
    setClearing(true);
    setError("");
    try {
      const response = await fetch("/api/tasks/outreach-suppression/clear", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ reviewId: snapshot.reviewAuthorityId }),
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error ?? `Suppression clear returned ${response.status}`);
      setCleared(true);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : String(caught));
    } finally {
      setClearing(false);
    }
  }

  if (view.state === "invalid") {
    return <section className="mt-6 rounded-lg border border-red-900/60 bg-red-950/20 p-3 text-xs text-red-200">Outreach decision identity is invalid. Create a new versioned review task.</section>;
  }

  const decisionPanel = view.state === "approved" || view.state === "rejected" ? (
    <div className="mt-4 border-t border-[#20262d] pt-3">
      <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-500">Outreach decision</p>
      <p className={view.state === "approved" ? "mt-2 text-sm font-semibold text-emerald-300" : "mt-2 text-sm font-semibold text-red-300"}>JT {view.state} this exact draft</p>
      <p className="mt-1 text-[10px] text-zinc-600">Immutable · {new Date(view.decision.decidedAt).toLocaleString()}</p>
    </div>
  ) : (
    <div className="mt-4 border-t border-amber-900/40 pt-3">
      <p className="text-[10px] font-semibold uppercase tracking-wider text-amber-300">JT outreach decision</p>
      <p className="mt-2 text-xs leading-relaxed text-zinc-300">Approve or reject this exact immutable snapshot. The first decision is permanent; any edit requires a new versioned task.</p>
      <div className="mt-3 grid grid-cols-2 gap-2">
        <button type="button" disabled={saving} onClick={() => decide("approve")} className="h-10 rounded-md border border-emerald-500/40 bg-emerald-500/10 text-xs font-semibold text-emerald-200 disabled:opacity-60">Approve exact draft</button>
        <button type="button" disabled={saving} onClick={() => decide("reject")} className="h-10 rounded-md border border-red-500/40 bg-red-500/10 text-xs font-semibold text-red-200 disabled:opacity-60">Reject exact draft</button>
      </div>
    </div>
  );

  return (
    <section className="mt-6 rounded-lg border border-amber-900/50 bg-amber-950/10 p-3">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-[10px] font-semibold uppercase tracking-wider text-amber-300">Immutable outreach review</p>
          <p className="mt-1 text-[10px] text-zinc-500">Cycle {snapshot.reviewCycle} · {snapshot.cohortId} · {snapshot.candidateId}</p>
        </div>
        <span className="font-mono text-[9px] text-zinc-600">{snapshot.snapshotSha256.slice(0, 12)}</span>
      </div>
      <h4 className="mt-4 text-sm font-semibold text-zinc-100">{snapshot.subject}</h4>
      <p className="mt-2 whitespace-pre-wrap text-xs leading-relaxed text-zinc-300">{snapshot.body}</p>
      <div className="mt-4 rounded border border-[#20262d] bg-[#0b0d0f] p-3">
        <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-500">Verifier report · {snapshot.verifierActorId}</p>
        <p className="mt-2 whitespace-pre-wrap text-xs leading-relaxed text-zinc-300">{snapshot.verifierReport}</p>
      </div>
      <div className="mt-4 space-y-1">
        <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-500">Exact Git bindings</p>
        {Object.entries(snapshot.gitBindings).map(([name, binding]) => (
          <p key={name} className="break-all font-mono text-[9px] text-zinc-600">{name}: {binding.repository}@{binding.commitSha}:{binding.path} · {binding.blobSha256}</p>
        ))}
      </div>
      {decisionPanel}
      {view.state === "approved" && snapshot.suppressionBinding && (
        <div className="mt-4 border-t border-[#20262d] pt-3">
          <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-500">Suppression owners</p>
          <p className="mt-2 text-xs leading-relaxed text-zinc-300">Record one retry-stable clear in both owner ledgers for this exact immutable channel binding.</p>
          <button type="button" disabled={clearing || cleared} onClick={clearSuppressionOwners} className="mt-3 h-10 w-full rounded-md border border-emerald-500/40 bg-emerald-500/10 text-xs font-semibold text-emerald-200 disabled:opacity-60">
            {cleared ? "Both owners cleared" : clearing ? "Clearing owners…" : "Clear both suppression owners"}
          </button>
        </div>
      )}
      {error && <p className="mt-2 text-xs text-red-300">{error}</p>}
    </section>
  );
}
