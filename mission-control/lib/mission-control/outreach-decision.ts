export type OutreachDecisionValue = "approve" | "reject";

export type OutreachDecision = {
  candidateId: string;
  draftSha256: string;
  snapshotSha256: string;
  decision: OutreachDecisionValue;
  decidedBy: "jt";
  decidedAt: number;
};

export type OutreachTask = {
  _id?: string;
  id?: string;
  candidateId?: string;
  cohortId?: string;
  draftSha256?: string;
  status?: string;
  outreachReview?: {
    candidateId: string;
    cohortId?: string;
    draftSha256: string;
    snapshotSha256: string;
    admittedBy: "server";
  };
  outreachDecision?: OutreachDecision;
};

type DecisionInput = {
  candidateId: string;
  draftSha256: string;
  snapshotSha256: string;
  decision: OutreachDecisionValue;
};

const SHA256_PATTERN = /^[a-f0-9]{64}$/;

export function validateOutreachIdentity(candidateId: unknown, draftSha256: unknown): asserts candidateId is string {
  if (typeof candidateId !== "string" || candidateId.trim() === "") throw new Error("candidateId required");
  if (typeof draftSha256 !== "string" || !SHA256_PATTERN.test(draftSha256)) {
    throw new Error("draftSha256 must be 64 lowercase hex characters");
  }
}

export function parseOutreachIdentity(candidateId: unknown, draftSha256: unknown, snapshotSha256?: unknown) {
  validateOutreachIdentity(candidateId, draftSha256);
  if (snapshotSha256 !== undefined && (typeof snapshotSha256 !== "string" || !SHA256_PATTERN.test(snapshotSha256))) {
    throw new Error("snapshotSha256 must be 64 lowercase hex characters");
  }
  return {
    candidateId,
    draftSha256: draftSha256 as string,
    ...(snapshotSha256 === undefined ? {} : { snapshotSha256: snapshotSha256 as string }),
  };
}

function matchesTask(task: OutreachTask, input: Pick<DecisionInput, "candidateId" | "draftSha256" | "snapshotSha256">) {
  return task.candidateId === input.candidateId
    && task.draftSha256 === input.draftSha256
    && task.outreachReview?.candidateId === input.candidateId
    && task.outreachReview?.draftSha256 === input.draftSha256
    && task.outreachReview?.snapshotSha256 === input.snapshotSha256
    && task.outreachReview?.admittedBy === "server";
}

export function resolveOutreachDecision(task: OutreachTask, input: DecisionInput, now: number) {
  parseOutreachIdentity(input.candidateId, input.draftSha256, input.snapshotSha256);
  if (input.decision !== "approve" && input.decision !== "reject") throw new Error("decision must be approve or reject");
  if (!matchesTask(task, input)) {
    if (!task.outreachReview) throw new Error("server-admitted outreach review required");
    throw new Error("outreach decision identity does not match task");
  }

  if (task.outreachDecision) {
    const existing = task.outreachDecision;
    if (
      existing.candidateId === input.candidateId
      && existing.draftSha256 === input.draftSha256
      && existing.snapshotSha256 === input.snapshotSha256
      && existing.decision === input.decision
      && existing.decidedBy === "jt"
    ) return { operation: "existing" as const, decision: existing };
    throw new Error("outreach decision is immutable; create a new versioned task");
  }

  if (task.status !== "todo") throw new Error("active outreach review required");
  return {
    operation: "create" as const,
    decision: {
      candidateId: input.candidateId,
      draftSha256: input.draftSha256,
      snapshotSha256: input.snapshotSha256,
      decision: input.decision,
      decidedBy: "jt" as const,
      decidedAt: now,
    },
    status: "done" as const,
  };
}

export function assertOutreachTaskMutable(task: OutreachTask | null): void {
  if (task?.outreachReview || task?.outreachDecision) {
    throw new Error("outreach review task is immutable; only the specialized decision mutation may append");
  }
}

export function resolveOutreachLookup(
  task: OutreachTask | null, candidateId: string, draftSha256: string, snapshotSha256: string,
) {
  parseOutreachIdentity(candidateId, draftSha256, snapshotSha256);
  if (!task || task.status === "archived" || !matchesTask(task, { candidateId, draftSha256, snapshotSha256 })) {
    return { authorized: false, state: "absent" as const };
  }
  if (!task.outreachDecision) {
    return task.status === "todo"
      ? { authorized: false, state: "pending" as const, taskId: task._id ?? task.id ?? "" }
      : { authorized: false, state: "absent" as const };
  }
  const decision = task.outreachDecision;
  if (
    task.status !== "done"
    || decision.candidateId !== candidateId
    || decision.draftSha256 !== draftSha256
    || decision.snapshotSha256 !== snapshotSha256
    || decision.decidedBy !== "jt"
  ) return { authorized: false, state: "absent" as const };
  const state = decision.decision === "approve" ? "approved" as const : "rejected" as const;
  return { authorized: state === "approved", state, decision, taskId: task._id ?? task.id ?? "" };
}
