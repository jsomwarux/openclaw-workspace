"use client";

import { useCallback, useEffect, useState } from "react";
import { RefreshCw } from "lucide-react";
import { StateBlock } from "@/components/mission-control/StateBlock";

type Candidate = {
  candidate_id?: string;
  lane?: string;
  score?: number;
  status?: string;
};

type Promotion = {
  candidateId?: string;
  title?: string;
  firstAction?: string;
  whyItMatters?: string;
  doneState?: string;
  verdict?: string;
  verifierConfirmed?: boolean;
  verifiedAt?: string;
  score?: number;
  evidenceScore?: number;
  distributionScore?: number;
  fatalConstraint?: boolean;
  workstream?: string;
};

type Run = {
  runId: string;
  runAt: string;
  status: "admitted" | "reconciled" | "blocked";
  lane: string | null;
  selected: Candidate[];
  promotions: Promotion[];
  promotionArtifact?: string;
  issue?: string;
};

type Snapshot = {
  status: "no-work" | "admitted" | "reconciled" | "blocked";
  queue: Candidate[];
  state: { lastCompletedRun?: string; nextRun?: string; failures: Array<Record<string, unknown>> };
  runs: Run[];
};

export default function OvernightPage() {
  const [snapshot, setSnapshot] = useState<Snapshot | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch("/api/overnight", { cache: "no-store" });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error ?? "Nightly Validation API failed");
      setSnapshot(body);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : String(caught));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { void refresh(); }, [refresh]);

  return (
    <div className="min-h-screen bg-[#0a0b0d] p-4 sm:p-6">
      <div className="mb-6 flex items-start justify-between gap-4">
        <div>
          <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-purple-300">Systems</p>
          <h1 className="mt-1 text-2xl font-semibold tracking-tight text-zinc-100">Nightly Validation</h1>
          <p className="mt-1 max-w-2xl text-xs leading-relaxed text-zinc-500">
            Read-only admission evidence. Only verifier-confirmed promotions can become Mission Control tasks.
          </p>
        </div>
        <button onClick={refresh} className="flex items-center gap-2 rounded-md border border-[#20262d] bg-[#0f1316] px-3 py-2 text-xs text-zinc-300">
          <RefreshCw size={13} className={loading ? "animate-spin" : ""} /> Refresh
        </button>
      </div>

      {error && <StateBlock kind="error" title="Nightly validation unavailable" detail={error} />}
      {loading && !snapshot && <StateBlock kind="loading" title="Loading validation state" detail="Reading local queue and run artifacts." />}

      {snapshot && (
        <div className="space-y-5">
          <StateBlock
            kind={snapshot.status === "blocked" ? "error" : "empty"}
            title={
              snapshot.status === "no-work" ? "No qualified validation"
                : snapshot.status === "admitted" ? "Validation admitted"
                  : snapshot.status === "reconciled" ? "Validation reconciled"
                    : "Validation blocked"
            }
            detail={
              snapshot.status === "no-work" ? "No admission artifact exists. The controller did not invent work."
                : snapshot.status === "admitted" ? "The latest admission is waiting for verifier reconciliation."
                  : snapshot.status === "reconciled" ? "The latest admission has a complete timestamped promotion envelope."
                    : snapshot.runs[0]?.issue ?? "The controller state contains a blocking failure."
            }
          />
          <section className="grid gap-3 sm:grid-cols-3">
            <Metric label="Pending candidates" value={String(snapshot.queue.filter((item) => item.status === "pending").length)} />
            <Metric label="Last completed" value={snapshot.state.lastCompletedRun ?? "No completed run"} />
            <Metric label="Next run" value={snapshot.state.nextRun ?? "Not scheduled in state"} />
          </section>

          <section className="rounded-xl border border-[#20262d] bg-[#0d1014] p-4">
            <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-500">Validation queue</p>
            <div className="mt-3 space-y-2">
              {snapshot.queue.length === 0 ? (
                <StateBlock kind="empty" title="No queued validations" detail="The controller will return NO_QUALIFIED_VALIDATION without inventing work." />
              ) : snapshot.queue.map((candidate) => (
                <div key={candidate.candidate_id} className="flex flex-wrap items-center justify-between gap-3 rounded-lg border border-[#20262d] bg-[#0f1316] p-3">
                  <div>
                    <p className="text-sm text-zinc-200">{candidate.candidate_id ?? "Unnamed candidate"}</p>
                    <p className="mt-1 text-[11px] text-zinc-600">{candidate.lane ?? "No lane"} · {candidate.status ?? "unknown"}</p>
                  </div>
                  <span className="rounded border border-[#2b333c] px-2 py-1 font-mono text-xs text-zinc-300">{candidate.score ?? 0} / 40</span>
                </div>
              ))}
            </div>
          </section>

          <section className="space-y-3">
            <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-500">Run history</p>
            {snapshot.runs.length === 0 ? (
              <StateBlock kind="empty" title="No validation runs yet" detail="Runs will appear after the controller writes a complete decision and promotion pair." />
            ) : snapshot.runs.map((run) => (
              <article key={run.runId} className="rounded-xl border border-[#20262d] bg-[#0d1014] p-4">
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div>
                    <p className="text-sm font-medium text-zinc-100">{run.runId}</p>
                    <p className="mt-1 text-[11px] text-zinc-600">{run.status} · {run.lane ?? "no lane selected"}</p>
                    <p className="mt-1 text-[10px] text-zinc-700">{run.runAt}</p>
                  </div>
                  <div className="text-right text-[11px] text-zinc-500">{run.selected.length} selected · {run.promotions.length} promoted</div>
                </div>
                {run.issue && <p className="mt-3 rounded border border-red-900/50 bg-red-950/20 p-2 text-xs text-red-300">{run.issue}</p>}
                {run.promotions.map((promotion) => (
                  <div key={promotion.candidateId} className="mt-3 rounded-lg border border-emerald-900/40 bg-emerald-950/10 p-3">
                    <div className="flex flex-wrap items-start justify-between gap-2">
                      <p className="text-sm font-medium text-emerald-300">{promotion.title ?? promotion.candidateId}</p>
                      <span className="font-mono text-[10px] text-zinc-500">{promotion.score ?? 0} / 40</span>
                    </div>
                    {promotion.firstAction && <p className="mt-2 text-xs text-zinc-300">{promotion.firstAction}</p>}
                    {promotion.whyItMatters && <p className="mt-1 text-xs text-zinc-500">{promotion.whyItMatters}</p>}
                    <p className="mt-2 text-[10px] text-zinc-600">
                      {promotion.verifierConfirmed ? "Verifier confirmed" : "Verifier unconfirmed"} · evidence {promotion.evidenceScore ?? 0} · distribution {promotion.distributionScore ?? 0}
                    </p>
                  </div>
                ))}
              </article>
            ))}
          </section>
        </div>
      )}
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border border-[#20262d] bg-[#0d1014] p-4">
      <p className="text-[10px] uppercase tracking-wider text-zinc-600">{label}</p>
      <p className="mt-2 break-words text-sm text-zinc-200">{value}</p>
    </div>
  );
}
