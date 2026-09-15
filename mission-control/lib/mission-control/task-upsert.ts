import { assertOutreachIdentityMutation, type OutreachTask } from "./outreach-decision";

export function resolveTaskUpsert<TId, TFields extends Record<string, unknown>>(
  existing: { _id: TId; createdAt: number; updatedAt: number } | null,
  input: TFields,
  now: number,
) {
  if (!existing) {
    return { operation: "create" as const, fields: { ...input, createdAt: now, updatedAt: now } };
  }
  assertOutreachIdentityMutation(existing as unknown as OutreachTask, input);
  return { operation: "update" as const, id: existing._id, fields: { ...input, updatedAt: now } };
}
