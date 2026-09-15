import { validateOutreachIdentity, type OutreachReview, type OutreachTask } from "./outreach-decision";

type ReviewIdentity = {
  candidateId: string;
  draftSha256: string;
};

export function resolveOutreachReviewCreateOnly<TId, TFields extends Record<string, unknown> & ReviewIdentity>(
  existing: (OutreachTask & { _id: TId }) | null,
  input: TFields,
  now: number,
) {
  validateOutreachIdentity(input.candidateId, input.draftSha256);
  if (existing) {
    if (
      existing.candidateId === input.candidateId
      && existing.draftSha256 === input.draftSha256
      && existing.outreachReview?.candidateId === input.candidateId
      && existing.outreachReview?.draftSha256 === input.draftSha256
      && existing.outreachReview?.admittedBy === "server"
    ) {
      return { operation: "existing" as const, id: existing._id };
    }
    throw new Error("existing task is not the same server-admitted outreach review; create a new versioned task");
  }

  const outreachReview: OutreachReview = {
    candidateId: input.candidateId,
    draftSha256: input.draftSha256,
    admittedBy: "server",
    admittedAt: now,
  };
  return {
    operation: "create" as const,
    fields: { ...input, outreachReview, createdAt: now, updatedAt: now },
  };
}
