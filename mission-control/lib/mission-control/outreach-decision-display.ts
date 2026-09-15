import type { OutreachDecision } from "./outreach-decision";

type OutreachDecisionSignal = {
  source: string;
  status?: string;
  candidateId?: string;
  draftSha256?: string;
  outreachDecision?: OutreachDecision;
};

const SHA256_PATTERN = /^[a-f0-9]{64}$/;

export function outreachDecisionView(signal: OutreachDecisionSignal) {
  if (
    signal.source !== "task"
    || !signal.candidateId
    || !signal.draftSha256
    || !SHA256_PATTERN.test(signal.draftSha256)
  ) return null;

  if (!signal.outreachDecision) {
    if (signal.status === "done" || signal.status === "archived") return null;
    return { candidateId: signal.candidateId, draftSha256: signal.draftSha256, state: "pending" as const };
  }
  if (
    signal.outreachDecision.candidateId !== signal.candidateId
    || signal.outreachDecision.draftSha256 !== signal.draftSha256
    || signal.outreachDecision.decidedBy !== "jt"
  ) {
    return { candidateId: signal.candidateId, draftSha256: signal.draftSha256, state: "invalid" as const };
  }
  return {
    candidateId: signal.candidateId,
    draftSha256: signal.draftSha256,
    state: signal.outreachDecision.decision === "approve" ? "approved" as const : "rejected" as const,
    decision: signal.outreachDecision,
  };
}
