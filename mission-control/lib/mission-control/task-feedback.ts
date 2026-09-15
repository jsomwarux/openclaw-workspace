import type { TaskFeedbackEntry } from "./types";

const MAX_FEEDBACK_LENGTH = 4_000;

export function parseTaskFeedbackAppend(input: Record<string, unknown>): {
  id: string;
  body: string;
  author: "jt" | "eve";
} {
  if (input.action !== "append-feedback") throw new Error("append-feedback action required");
  if (typeof input.id !== "string" || !input.id) throw new Error("id required");
  if (typeof input.body !== "string") throw new Error("feedback body required");
  if (input.author !== "jt" && input.author !== "eve") throw new Error("feedback author invalid");
  return { id: input.id, body: input.body, author: input.author };
}

export function appendTaskFeedback(
  existing: TaskFeedbackEntry[] | undefined,
  input: { body: string; author: "jt" | "eve" },
  now: number,
): TaskFeedbackEntry[] {
  const body = typeof input.body === "string" ? input.body.trim() : "";
  if (!body) throw new Error("feedback body required");
  if (body.length > MAX_FEEDBACK_LENGTH) throw new Error("feedback body too long");
  if (input.author !== "jt" && input.author !== "eve") throw new Error("feedback author invalid");
  const feedback = existing ?? [];
  return [...feedback, { id: `${now}-${feedback.length + 1}`, body, author: input.author, createdAt: now }];
}
