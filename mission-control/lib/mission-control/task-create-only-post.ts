import { NextResponse } from "next/server";
import { normalizeTaskInput, validateTaskAdmission } from "./task-admission";
import { buildTaskWriteResponse, resolveTaskWriteMode } from "./task-write-mode";

type CreateOnlyMutation = (
  input: Record<string, unknown>,
) => Promise<{ id: string; created: boolean }>;

export function createPostHandler(mutate: CreateOnlyMutation) {
  return async function POST(req: Request) {
    const body = await req.json();
    const rawInput = { status: "todo", assignee: "eve", priority: "medium", ...body };
    try {
      validateTaskAdmission(rawInput);
    } catch (error) {
      return NextResponse.json(
        { error: error instanceof Error ? error.message : String(error) },
        { status: 400 },
      );
    }

    const input = normalizeTaskInput(rawInput);
    if (!input.title) return NextResponse.json({ error: "title required" }, { status: 400 });

    try {
      resolveTaskWriteMode("create-only", Boolean(input.dedupeKey));
    } catch (error) {
      return NextResponse.json(
        { error: error instanceof Error ? error.message : String(error) },
        { status: 400 },
      );
    }

    const result = await mutate(input);
    return NextResponse.json(buildTaskWriteResponse("create-only", result));
  };
}
