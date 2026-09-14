export type TaskWriteMode = "create" | "upsert" | "create-only";

export function resolveTaskWriteMode(mode: string | null, hasDedupeKey: boolean): TaskWriteMode {
  if (mode === null || mode === "") return hasDedupeKey ? "upsert" : "create";
  if (mode !== "create-only") throw new Error(`unsupported task write mode: ${mode}`);
  if (!hasDedupeKey) throw new Error("dedupeKey required for create-only mode");
  return "create-only";
}

export function buildTaskWriteResponse<T extends Record<string, unknown>>(mode: TaskWriteMode, result: T) {
  if (mode === "create-only") {
    return { ...result, success: true, writeMode: "create-only" as const };
  }
  return { ...result, success: true };
}
