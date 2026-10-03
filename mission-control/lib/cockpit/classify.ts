// Card families (state map Part A) and decision-card detection (DECISIONS 1.4).
import type { DecisionSeries, ItemFamily, RawTask } from "./types";

export const DECISION_TITLE = /^(?:.*?\s)?(AP|Q|P)(\d{1,3}):/;

export function decisionCode(title: unknown): { series: DecisionSeries; number: number } | null {
  if (typeof title !== "string") return null;
  const match = DECISION_TITLE.exec(title);
  if (!match) return null;
  return { series: match[1] as DecisionSeries, number: Number(match[2]) };
}

export function isLanePacket(task: RawTask): boolean {
  return task.packetSchema === "lane-packet-v1";
}

export function isOutreachReview(task: RawTask): boolean {
  return typeof task.outreachReview === "object" && task.outreachReview !== null;
}

/** One card belongs to exactly one family. A decision card is a generic task with a title code. */
export function familyOf(task: RawTask): ItemFamily {
  if (isLanePacket(task)) return "lanePacket";
  if (isOutreachReview(task)) return "outreachReview";
  if (decisionCode(task.title)) return "decision";
  return "generic";
}

export function seriesOf(task: RawTask): DecisionSeries | null {
  return familyOf(task) === "decision" ? decisionCode(task.title)!.series : null;
}
