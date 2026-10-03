// Each operator action as ordered backend writes. A retry resumes at the failed step, and a
// retried feedback step first re-reads the card so an entry that already landed is not
// appended twice (GAPS 13 interim rule).
import { ApiError } from "./api";
import type { CockpitApi } from "./api";
import { answerBody, decisionBody } from "./answer";
import { parkPatch } from "./block";
import type { ParkValue } from "./block";
import { deferPatch, deferUndoValue } from "./defer";
import type { RawTask, UndoRecord } from "./types";

export type ActRequest =
  | { action: "start" }
  | { action: "complete" }
  | { action: "saveAnswer"; text: string }
  | { action: "approve"; note: string }
  | { action: "reject"; note: string }
  | { action: "defer"; until: number }
  | { action: "block"; park: ParkValue };

export type WriteAction = ActRequest["action"] | "undo";
export type WriteStep = { kind: "feedback"; body: string } | { kind: "patch"; fields: Record<string, unknown> };

export interface WritePlan {
  action: WriteAction;
  itemId: string;
  steps: WriteStep[];
  undo?: UndoRecord;
}

const DUPLICATE_WINDOW_MS = 60_000;

export function planFor(request: ActRequest, task: RawTask, now: number): WritePlan {
  const base = { action: request.action, itemId: task._id };
  const previousStatus = task.status ?? "todo";
  switch (request.action) {
    case "start":
      return { ...base, steps: [{ kind: "patch", fields: { status: "in-progress" } }], undo: { kind: "start", restore: { status: previousStatus } } };
    case "complete":
      return { ...base, steps: [{ kind: "patch", fields: { status: "done" } }], undo: { kind: "complete", restore: { status: previousStatus } } };
    case "saveAnswer":
      return { ...base, steps: [{ kind: "feedback", body: answerBody(request.text) }] };
    case "approve":
    case "reject":
      return { ...base, steps: [{ kind: "feedback", body: decisionBody(request.action, request.note) }, { kind: "patch", fields: { status: "done" } }] };
    case "defer":
      return {
        ...base,
        steps: [{ kind: "patch", fields: deferPatch(request.until) }],
        undo: { kind: "defer", restore: { snoozedUntil: typeof task.snoozedUntil === "number" ? task.snoozedUntil : null } },
      };
    case "block":
      return { ...base, steps: [{ kind: "patch", fields: parkPatch(request.park, now) }] };
  }
}

/** The write that reverses an earlier one. Defer restores the previous snooze, or now. */
export function undoPlan(itemId: string, undo: UndoRecord, now: number): WritePlan {
  const fields = undo.kind === "defer"
    ? deferPatch(deferUndoValue(typeof undo.restore.snoozedUntil === "number" ? undo.restore.snoozedUntil : undefined, now))
    : { status: undo.restore.status };
  return { action: "undo", itemId, steps: [{ kind: "patch", fields }] };
}

const PHRASES: Record<WriteAction, string> = {
  start: "start this item",
  complete: "mark this item done",
  saveAnswer: "save your answer",
  approve: "record your approval",
  reject: "record the rejection",
  defer: "defer this item",
  block: "park this item",
  undo: "undo that change",
};
export const failurePhrase = (action: WriteAction) => PHRASES[action];

export type PlanResult = { ok: true } | { ok: false; failedStep: number; error: { kind: ApiError["kind"]; status?: number } };

export async function executePlan(
  api: CockpitApi,
  plan: WritePlan,
  options: { fromStep: number; firstAttemptAt: number; retry: boolean },
): Promise<PlanResult> {
  for (let i = options.fromStep; i < plan.steps.length; i += 1) {
    const step = plan.steps[i];
    try {
      if (step.kind === "feedback") {
        if (options.retry && i === options.fromStep && (await alreadyAppended(api, plan.itemId, step.body, options.firstAttemptAt))) continue;
        await api.appendFeedback(plan.itemId, step.body);
      } else {
        await api.patchTask(plan.itemId, step.fields);
      }
    } catch (error) {
      const known = error instanceof ApiError ? error : new ApiError("network");
      return { ok: false, failedStep: i, error: { kind: known.kind, status: known.status } };
    }
  }
  return { ok: true };
}

async function alreadyAppended(api: CockpitApi, id: string, body: string, since: number): Promise<boolean> {
  const task = (await api.listTasks()).find((candidate) => candidate._id === id);
  return Boolean(task?.feedback?.some((entry) => entry.author === "jt" && entry.body === body && entry.createdAt >= since - DUPLICATE_WINDOW_MS));
}
