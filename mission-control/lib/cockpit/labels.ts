// Plain-language words for stored values. Stored enum names never reach the screen.
import type { DisplayStatus } from "@/docs/design/mission-control-redesign/reference/view-model";

const STATUS_WORDS: Record<string, DisplayStatus> = {
  todo: "Not started",
  "in-progress": "In progress",
  "waiting-external": "Waiting",
  snoozed: "Deferred",
  done: "Done",
  archived: "Done",
};

export function statusWord(status: string | undefined): DisplayStatus {
  return (status && STATUS_WORDS[status]) || "Status not recognized";
}

const PROOF_WORDS: Record<string, string> = {
  "post-url": "post link",
  "message-ref": "message reference",
  "application-ref": "application reference",
  "rsvp-ref": "RSVP reference",
  "profile-edit-ref": "profile edit reference",
  "deploy-ref": "deploy reference",
};

export function proofWord(type: string | undefined): string | null {
  return type && PROOF_WORDS[type] ? PROOF_WORDS[type] : null;
}

const APPROVAL_WORDS: Record<string, string> = { pending: "Approval pending", approved: "Approved", rejected: "Rejected" };
export const approvalWord = (state: string | undefined) => (state && APPROVAL_WORDS[state]) || "Approval state not recognized";
