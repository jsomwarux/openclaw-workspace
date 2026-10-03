// When a card cannot be acted on (DECISIONS 9), with one plain sentence per failed check.
import { isLanePacket, isOutreachReview } from "./classify";
import type { RawTask } from "./types";

export const KNOWN_STATUSES = ["todo", "in-progress", "waiting-external", "snoozed", "done", "archived"];
const OWNERS = ["jt", "eve", "both"];
const PRIORITIES = ["high", "medium", "low"];

const present = (value: unknown) => typeof value === "string" ? value.length > 0 : value !== undefined && value !== null;

export function validateCard(task: RawTask): { ok: true } | { ok: false; reasons: string[] } {
  const reasons: string[] = [];
  if (typeof task.title !== "string" || task.title.trim().length === 0) reasons.push("No title is recorded.");
  if (!KNOWN_STATUSES.includes(task.status ?? "")) reasons.push("Its status is not one this app recognizes.");
  if (!OWNERS.includes(task.assignee ?? "")) reasons.push("Its owner is not one this app recognizes.");
  if (!PRIORITIES.includes(task.priority ?? "")) reasons.push("Its priority is not one this app recognizes.");
  if (isLanePacket(task) && !(present(task.payloadHash) && present(task.expiresAt) && present(task.doneEvidenceType))) {
    reasons.push("Its approval details are incomplete.");
  }
  if (isOutreachReview(task)) {
    const review = task.outreachReview!;
    const decision = task.outreachDecision;
    const snapshotIncomplete = !(present(review.candidateId) && present(review.draftSha256) && present(review.snapshotSha256));
    const decisionInvalid = decision !== undefined && decision !== null && decision.decision !== "approve" && decision.decision !== "reject";
    if (snapshotIncomplete || decisionInvalid) reasons.push("Its review details are incomplete.");
  }
  return reasons.length === 0 ? { ok: true } : { ok: false, reasons };
}
