// Answers on Q and AP cards and decisions on P cards (DECISIONS 5.1, 5.2). Both are
// recorded as one append-only feedback entry; the body must fit the 4,000-character limit.
import type { FeedbackEntry } from "./types";

export const FEEDBACK_MAX = 4000;
export const ANSWER_PREFIX = "Answer: ";
export const ANSWER_MAX = FEEDBACK_MAX - ANSWER_PREFIX.length;
const DECISION_PREFIX = { approve: "Decision: Approved.", reject: "Decision: Rejected." } as const;
export const NOTE_MAX = FEEDBACK_MAX - (DECISION_PREFIX.approve.length + 1);

export function answerBody(text: string): string {
  return `${ANSWER_PREFIX}${text.trim()}`;
}

export function validateAnswer(text: string): { ok: true; body: string } | { ok: false; error: string } {
  const trimmed = text.trim();
  if (trimmed.length === 0) return { ok: false, error: "Enter an answer before saving." };
  if (trimmed.length > ANSWER_MAX) {
    return { ok: false, error: `Shorten the answer to ${ANSWER_MAX.toLocaleString("en-US")} characters or fewer.` };
  }
  return { ok: true, body: answerBody(trimmed) };
}

/** The latest answer JT saved on this card, if any. Eve's entries never count. */
export function savedAnswer(feedback: FeedbackEntry[] | undefined): FeedbackEntry | null {
  const answers = (feedback ?? []).filter(
    (entry) => entry.author === "jt" && entry.body.startsWith(ANSWER_PREFIX) && entry.body.slice(ANSWER_PREFIX.length).trim().length > 0,
  );
  return answers.length > 0 ? answers[answers.length - 1] : null;
}

export function decisionBody(kind: "approve" | "reject", note: string): string {
  const trimmed = note.trim();
  return trimmed.length > 0 ? `${DECISION_PREFIX[kind]} ${trimmed}` : DECISION_PREFIX[kind];
}

export function validateDecisionNote(note: string): { ok: true } | { ok: false; error: string } {
  return note.trim().length > NOTE_MAX
    ? { ok: false, error: `Shorten the note to ${NOTE_MAX.toLocaleString("en-US")} characters or fewer.` }
    : { ok: true };
}
