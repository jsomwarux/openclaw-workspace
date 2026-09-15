"use client";

import { useEffect, useState } from "react";
import type { OutreachDecision, OutreachDecisionValue } from "@/lib/mission-control/outreach-decision";
import { outreachDecisionView } from "@/lib/mission-control/outreach-decision-display";
import type { Signal } from "@/lib/mission-control/types";

export function OutreachDecisionControls({ signal }: { signal: Signal }) {
  const initial = outreachDecisionView(signal);
  const [decision, setDecision] = useState<OutreachDecision | undefined>(initial && "decision" in initial ? initial.decision : undefined);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const view = outreachDecisionView(signal);
    setDecision(view && "decision" in view ? view.decision : undefined);
    setError("");
  }, [signal.id, signal.outreachDecision]);

  const view = outreachDecisionView({ ...signal, outreachDecision: decision ?? signal.outreachDecision });
  if (!view) return null;

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

  if (view.state === "invalid") {
    return (
      <section className="mt-6 rounded-lg border border-red-900/60 bg-red-950/20 p-3 text-xs text-red-200">
        Outreach decision identity is invalid. Create a new versioned review task.
      </section>
    );
  }

  if (view.state === "approved" || view.state === "rejected") {
    return (
      <section className="mt-6 rounded-lg border border-[#20262d] bg-[#0b0d0f] p-3">
        <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-500">Outreach decision</p>
        <p className={view.state === "approved" ? "mt-2 text-sm font-semibold text-emerald-300" : "mt-2 text-sm font-semibold text-red-300"}>
          JT {view.state} this exact draft
        </p>
        <p className="mt-1 text-[10px] text-zinc-600">Immutable · {new Date(view.decision.decidedAt).toLocaleString()}</p>
      </section>
    );
  }

  return (
    <section className="mt-6 rounded-lg border border-amber-900/50 bg-amber-950/10 p-3">
      <p className="text-[10px] font-semibold uppercase tracking-wider text-amber-300">JT outreach decision</p>
      <p className="mt-2 text-xs leading-relaxed text-zinc-300">
        Approve or reject this exact candidate and draft. The first decision is permanent; any edit requires a new versioned task.
      </p>
      <div className="mt-3 grid grid-cols-2 gap-2">
        <button
          type="button"
          disabled={saving}
          onClick={() => decide("approve")}
          className="h-10 rounded-md border border-emerald-500/40 bg-emerald-500/10 text-xs font-semibold text-emerald-200 disabled:opacity-60"
        >
          Approve exact draft
        </button>
        <button
          type="button"
          disabled={saving}
          onClick={() => decide("reject")}
          className="h-10 rounded-md border border-red-500/40 bg-red-500/10 text-xs font-semibold text-red-200 disabled:opacity-60"
        >
          Reject exact draft
        </button>
      </div>
      {error && <p className="mt-2 text-xs text-red-300">{error}</p>}
    </section>
  );
}
