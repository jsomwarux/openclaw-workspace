import type { OutreachDecision } from "./outreach-decision";
import { validateOutreachReviewSubmission, type OutreachReviewSnapshot } from "./outreach-review";

type OutreachDecisionSignal = {
  source: string;
  status?: string;
  description?: string;
  candidateId?: string;
  cohortId?: string;
  draftSha256?: string;
  outreachReview?: OutreachReviewSnapshot;
  outreachDecision?: OutreachDecision;
};

const SHA256_PATTERN = /^[a-f0-9]{64}$/;

export function outreachDecisionView(signal: OutreachDecisionSignal) {
  const snapshot = signal.outreachReview;
  try {
    if (!snapshot) return null;
    validateOutreachReviewSubmission({
      candidateId: snapshot.candidateId,
      cohortId: snapshot.cohortId,
      draftSha256: snapshot.draftSha256,
      subject: snapshot.subject,
      body: snapshot.body,
      verifierReport: snapshot.verifierReport,
      reviewAuthorityId: snapshot.reviewAuthorityId,
      verifierActorId: snapshot.verifierActorId,
      gitBindings: snapshot.gitBindings,
    });
  } catch {
    return null;
  }
  if (
    signal.source !== "task"
    || !signal.candidateId
    || !signal.draftSha256
    || !SHA256_PATTERN.test(signal.draftSha256)
    || snapshot.candidateId !== signal.candidateId
    || snapshot.draftSha256 !== signal.draftSha256
    || snapshot.admittedBy !== "server"
    || !SHA256_PATTERN.test(snapshot.snapshotSha256)
    || (snapshot.reviewCycle !== 1 && snapshot.reviewCycle !== 2)
    || !Number.isFinite(snapshot.admittedAt)
  ) return null;

  const identity = {
    candidateId: signal.candidateId,
    draftSha256: signal.draftSha256,
    snapshotSha256: snapshot.snapshotSha256,
    snapshot,
  };

  if (signal.status === "archived") return null;

  if (!signal.outreachDecision) {
    if (signal.status !== "todo") return null;
    return { ...identity, state: "pending" as const };
  }
  if (
    signal.outreachDecision.candidateId !== signal.candidateId
    || signal.outreachDecision.draftSha256 !== signal.draftSha256
    || signal.outreachDecision.snapshotSha256 !== snapshot.snapshotSha256
    || signal.outreachDecision.decidedBy !== "jt"
  ) {
    return { ...identity, state: "invalid" as const };
  }
  return {
    ...identity,
    state: signal.outreachDecision.decision === "approve" ? "approved" as const : "rejected" as const,
    decision: signal.outreachDecision,
  };
}
