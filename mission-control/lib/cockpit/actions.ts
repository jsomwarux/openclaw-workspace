// Permitted actions by family and status (DECISIONS 5.7, with override 1 for Defer).
// Only these render; everything else is hidden, not disabled.
import { familyOf, seriesOf } from "./classify";
import { isClosedPacket, isDecidedOutreach, isExpired } from "./eligibility";
import { savedAnswer } from "./answer";
import { validateCard } from "./validity";
import type { DecisionSeries, ItemFamily, RawTask } from "./types";

export type CockpitAction = "start" | "complete" | "saveAnswer" | "approve" | "reject" | "defer" | "block" | "previous" | "next";

export interface ActionContext {
  family: ItemFamily;
  series: DecisionSeries | null;
  status: string;
  valid: boolean;
  paused: boolean;
  expired: boolean;
  closedPacket: boolean;
  approvedCurrent: boolean;
  internal: boolean;
  decided: boolean;
  answerSaved: boolean;
}

export function actionContext(task: RawTask, now: number, options: { paused: boolean }): ActionContext {
  return {
    family: familyOf(task),
    series: seriesOf(task),
    status: task.status ?? "",
    valid: validateCard(task).ok,
    paused: options.paused,
    expired: isExpired(task, now),
    closedPacket: isClosedPacket(task),
    approvedCurrent: task.approvalState === "approved" && typeof task.payloadHash === "string" && task.approvedPayloadHash === task.payloadHash,
    internal: task.doneEvidenceType === "none",
    decided: isDecidedOutreach(task),
    answerSaved: savedAnswer(task.feedback) !== null,
  };
}

const MOVE: CockpitAction[] = ["previous", "next"];
const CLOSED = new Set(["done", "archived"]);
const NOT_STARTED = new Set(["todo", "waiting-external", "snoozed"]);

export function permittedActions(c: ActionContext): CockpitAction[] {
  if (c.paused || !c.valid) return MOVE;
  switch (c.family) {
    case "outreachReview":
      return c.decided || c.status !== "todo" ? MOVE : ["approve", "reject", ...MOVE];
    case "lanePacket": {
      if (c.closedPacket) return MOVE;
      if (c.expired) return ["reject", ...MOVE];
      const list: CockpitAction[] = [];
      if (!c.approvedCurrent) list.push("approve");
      list.push("reject");
      if (c.internal || c.approvedCurrent) list.push("complete");
      list.push("defer", "block");
      if (NOT_STARTED.has(c.status)) list.push("start");
      return [...list, ...MOVE];
    }
    case "decision": {
      if (CLOSED.has(c.status)) return MOVE;
      if (c.series === "P") return ["approve", "reject", "defer", "block", ...MOVE];
      return [c.answerSaved ? "complete" : "saveAnswer", "defer", "block", ...MOVE];
    }
    default: {
      if (CLOSED.has(c.status)) return MOVE;
      if (c.status === "in-progress") return ["complete", "defer", "block", ...MOVE];
      return ["start", "complete", "defer", "block", ...MOVE];
    }
  }
}

/** Slice one renders lane packets and outreach reviews read-only; their actions are slice two. */
export function sliceOneActions(c: ActionContext): CockpitAction[] {
  if (c.family === "lanePacket" || c.family === "outreachReview") return MOVE;
  return permittedActions(c);
}

export const isReadOnlyInSliceOne = (family: ItemFamily) => family === "lanePacket" || family === "outreachReview";
