export function resolveTaskCreateOnly<TId, TFields extends Record<string, unknown>>(
  existing: { _id: TId } | null,
  input: TFields,
  now: number,
) {
  if (existing) return { operation: "existing" as const, id: existing._id };
  return { operation: "create" as const, fields: { ...input, createdAt: now, updatedAt: now } };
}
