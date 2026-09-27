import { assertOutreachTaskMutable, type OutreachTask } from "./outreach-decision";
import { LanePacketError, isLanePacket } from "./lane-packet";

export function resolveTaskUpsert<TId, TFields extends Record<string, unknown>>(
  existing: { _id: TId; createdAt: number; updatedAt: number } | null,
  input: TFields,
  now: number,
) {
  if (!existing) {
    return { operation: "create" as const, fields: { ...input, createdAt: now, updatedAt: now } };
  }
  assertOutreachTaskMutable(existing as unknown as OutreachTask);
  if (isLanePacket(existing)) {
    throw new LanePacketError("transition_required", "lane packets are create-only; use the lane-packet route");
  }
  return { operation: "update" as const, id: existing._id, fields: { ...input, updatedAt: now } };
}
