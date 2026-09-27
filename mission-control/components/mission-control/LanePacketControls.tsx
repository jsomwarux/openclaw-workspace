"use client";

import { useEffect, useState } from "react";
import { EVIDENCE_LABELS, isLanePacketSignal, lanePacketActions, lanePacketDetails } from "@/lib/mission-control/lane-packet-display";
import type { Signal } from "@/lib/mission-control/types";

type TransitionBody =
  | { action: "approve" | "reject"; payloadHash: string; note?: string }
  | { action: "complete"; evidence?: { type: string; ref: string } }
  | { action: "skip" | "no-action"; note?: string };

/**
 * Governed actions for a Growth OS lane packet. Every button maps to one
 * server transition on PATCH /api/tasks/lane-packet; the server re-checks the
 * state machine, so this only hides transitions that cannot succeed.
 */
export function LanePacketControls({ signal, onChanged }: { signal: Signal; onChanged?: () => void }) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [evidenceRef, setEvidenceRef] = useState("");
  const [note, setNote] = useState("");

  useEffect(() => {
    setError("");
    setEvidenceRef("");
    setNote("");
  }, [signal.id, signal.payloadHash, signal.approvalState, signal.status]);

  if (!isLanePacketSignal(signal)) return null;
  const details = lanePacketDetails(signal);
  const actions = lanePacketActions(signal, Date.now());
  const evidenceLabel = signal.doneEvidenceType ? EVIDENCE_LABELS[signal.doneEvidenceType] : "Evidence";
  const trimmedNote = note.trim();

  async function send(body: TransitionBody) {
    setBusy(true);
    setError("");
    try {
      const response = await fetch("/api/tasks/lane-packet", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: signal.id, ...body }),
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error ?? `Lane packet request returned ${response.status}`);
      onChanged?.();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : String(caught));
    } finally {
      setBusy(false);
    }
  }

  const withNote = trimmedNote ? { note: trimmedNote } : {};

  return (
    <section className="mt-6 rounded-lg border border-sky-900/50 bg-sky-950/10 p-3">
      <div className="flex items-start justify-between gap-3">
        <p className="text-[10px] font-semibold uppercase tracking-wider text-sky-300">Lane packet</p>
        <span className="font-mono text-[9px] text-zinc-600">{signal.sourceSystem ?? ""}</span>
      </div>
      <dl className="mt-3 grid grid-cols-1 gap-2 sm:grid-cols-2">
        {details.map(([label, value]) => (
          <div key={label} className="min-w-0">
            <dt className="text-[10px] uppercase tracking-wider text-zinc-600">{label}</dt>
            <dd className="mt-0.5 break-words text-xs text-zinc-300">
              {label === "Artifact" && signal.artifactRef?.url?.startsWith("http") ? (
                <a href={signal.artifactRef.url} target="_blank" rel="noreferrer" className="text-emerald-300 hover:underline">{value}</a>
              ) : value}
            </dd>
          </div>
        ))}
      </dl>

      {actions.canApprove && (
        <button
          type="button"
          disabled={busy}
          onClick={() => send({ action: "approve", payloadHash: signal.payloadHash ?? "" })}
          className="mt-4 h-10 w-full rounded-md border border-emerald-500/40 bg-emerald-500/10 text-xs font-semibold text-emerald-200 disabled:opacity-60"
        >Approve</button>
      )}

      {actions.canComplete && actions.needsEvidence && (
        <div className="mt-4 border-t border-[#20262d] pt-3">
          <label className="text-[10px] font-semibold uppercase tracking-wider text-zinc-500" htmlFor={`evidence-${signal.id}`}>{evidenceLabel}</label>
          <input
            id={`evidence-${signal.id}`}
            value={evidenceRef}
            onChange={(event) => setEvidenceRef(event.target.value)}
            placeholder={signal.doneEvidenceType === "post-url" ? "https://…" : "Reference or confirmation ID"}
            maxLength={500}
            className="mt-2 h-9 w-full rounded border border-[#20262d] bg-[#080a0c] px-3 text-xs text-zinc-200 outline-none focus:border-emerald-800"
          />
          <button
            type="button"
            disabled={busy || !evidenceRef.trim()}
            onClick={() => send({ action: "complete", evidence: { type: signal.doneEvidenceType ?? "", ref: evidenceRef.trim() } })}
            className="mt-2 h-9 w-full rounded-md border border-emerald-500/40 bg-emerald-500/10 text-xs font-semibold text-emerald-200 disabled:opacity-50"
          >Record evidence</button>
        </div>
      )}

      {actions.canComplete && !actions.needsEvidence && (
        <button
          type="button"
          disabled={busy}
          onClick={() => send({ action: "complete" })}
          className="mt-4 h-10 w-full rounded-md border border-emerald-500/40 bg-emerald-500/10 text-xs font-semibold text-emerald-200 disabled:opacity-60"
        >Mark done</button>
      )}

      {actions.canClose && (
        <div className="mt-4 border-t border-[#20262d] pt-3">
          <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-500">Close without acting</p>
          <input
            value={note}
            onChange={(event) => setNote(event.target.value)}
            placeholder="Optional note for the closure reason"
            maxLength={1000}
            className="mt-2 h-9 w-full rounded border border-[#20262d] bg-[#080a0c] px-3 text-xs text-zinc-200 outline-none focus:border-zinc-600"
          />
          <div className="mt-2 grid grid-cols-3 gap-2">
            <button type="button" disabled={busy} onClick={() => send({ action: "skip", ...withNote })} className="h-9 rounded-md border border-zinc-700 bg-zinc-900/80 text-xs text-zinc-300 disabled:opacity-60">Skip</button>
            <button type="button" disabled={busy} onClick={() => send({ action: "no-action", ...withNote })} className="h-9 rounded-md border border-zinc-700 bg-zinc-900/80 text-xs text-zinc-300 disabled:opacity-60">No action</button>
            <button type="button" disabled={busy} onClick={() => send({ action: "reject", payloadHash: signal.payloadHash ?? "", ...withNote })} className="h-9 rounded-md border border-red-500/40 bg-red-500/10 text-xs text-red-200 disabled:opacity-60">Reject</button>
          </div>
        </div>
      )}

      {error && <p className="mt-2 text-xs text-red-300">{error}</p>}
    </section>
  );
}
