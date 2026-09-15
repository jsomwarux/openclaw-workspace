export type OutreachDecisionValue = "approve" | "reject";

export type OutreachDecision = {
  candidateId: string;
  draftSha256: string;
  decision: OutreachDecisionValue;
  decidedBy: "jt";
  decidedAt: number;
};

export type OutreachTask = {
  _id?: string;
  id?: string;
  candidateId?: string;
  draftSha256?: string;
  outreachDecision?: OutreachDecision;
};

type DecisionInput = {
  candidateId: string;
  draftSha256: string;
  decision: OutreachDecisionValue;
};

const SHA256_PATTERN = /^[a-f0-9]{64}$/;

export function validateOutreachIdentity(candidateId: unknown, draftSha256: unknown): asserts candidateId is string {
  if (typeof candidateId !== "string" || candidateId.trim() === "") throw new Error("candidateId required");
  if (typeof draftSha256 !== "string" || !SHA256_PATTERN.test(draftSha256)) {
    throw new Error("draftSha256 must be 64 lowercase hex characters");
  }
}

export function parseOutreachIdentity(candidateId: unknown, draftSha256: unknown) {
  validateOutreachIdentity(candidateId, draftSha256);
  return { candidateId, draftSha256: draftSha256 as string };
}

export function resolveOutreachDecision(task: OutreachTask, input: DecisionInput, now: number) {
  validateOutreachIdentity(input.candidateId, input.draftSha256);
  if (input.decision !== "approve" && input.decision !== "reject") {
    throw new Error("decision must be approve or reject");
  }
  if (task.candidateId !== input.candidateId || task.draftSha256 !== input.draftSha256) {
    throw new Error("outreach decision identity does not match task");
  }

  if (task.outreachDecision) {
    const existing = task.outreachDecision;
    if (
      existing.candidateId === input.candidateId
      && existing.draftSha256 === input.draftSha256
      && existing.decision === input.decision
      && existing.decidedBy === "jt"
    ) {
      return { operation: "existing" as const, decision: existing };
    }
    throw new Error("outreach decision is immutable; create a new versioned task");
  }

  return {
    operation: "create" as const,
    decision: {
      candidateId: input.candidateId,
      draftSha256: input.draftSha256,
      decision: input.decision,
      decidedBy: "jt" as const,
      decidedAt: now,
    },
  };
}

export function assertOutreachIdentityMutation(task: OutreachTask, fields: Record<string, unknown>): void {
  if (!task.outreachDecision) return;
  if (
    ("candidateId" in fields && fields.candidateId !== task.candidateId)
    || ("draftSha256" in fields && fields.draftSha256 !== task.draftSha256)
  ) {
    throw new Error("outreach decision identity is immutable");
  }
}

export function assertOutreachTaskRemoval(task: OutreachTask | null): void {
  if (task?.outreachDecision) throw new Error("outreach decision task is immutable");
}

export function resolveOutreachLookup(task: OutreachTask | null, candidateId: string, draftSha256: string) {
  validateOutreachIdentity(candidateId, draftSha256);
  if (
    !task
    || task.candidateId !== candidateId
    || task.draftSha256 !== draftSha256
    || !task.outreachDecision
    || task.outreachDecision.candidateId !== candidateId
    || task.outreachDecision.draftSha256 !== draftSha256
  ) {
    return { authorized: false, state: "absent" as const };
  }

  const state = task.outreachDecision.decision === "approve" ? "approved" as const : "rejected" as const;
  return {
    authorized: state === "approved",
    state,
    decision: task.outreachDecision,
    taskId: task._id ?? task.id ?? "",
  };
}
