/**
 * HTTP API for tasks. Eve (and any device) can read/write tasks via Next.js routes.
 * This proxies server-side to Convex so mobile devices don't need direct Convex access.
 *
 * GET    /api/tasks           → list all tasks
 * POST   /api/tasks           → create task
 * PATCH  /api/tasks           → update task (pass id + any fields)
 * DELETE /api/tasks?id=<id>   → delete task
 */
import { NextResponse } from "next/server";
import { ConvexHttpClient } from "convex/browser";
import { api } from "@/convex/_generated/api";
import { Id } from "@/convex/_generated/dataModel";
import type { FunctionArgs } from "convex/server";
import { normalizeTaskInput, validateTaskAdmission } from "@/lib/mission-control/task-admission";

const convex = new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const include = searchParams.get("include");
  if (include === "archived") {
    const tasks = await convex.query(api.tasks.listArchived, {});
    return NextResponse.json({ tasks });
  }
  // Default: return only active (non-archived) tasks
  const tasks = await convex.query(api.tasks.listActive, {});
  return NextResponse.json({ tasks });
}

export async function POST(req: Request) {
  const body = await req.json();
  const rawInput = { status: "todo", assignee: "eve", priority: "medium", ...body };
  try {
    validateTaskAdmission(rawInput);
  } catch (error) {
    return NextResponse.json({ error: error instanceof Error ? error.message : String(error) }, { status: 400 });
  }
  const input = normalizeTaskInput(rawInput);
  const { title } = input;
  if (!title) return NextResponse.json({ error: "title required" }, { status: 400 });

  if (input.dedupeKey) {
    const result = await convex.mutation(
      api.tasks.upsertByDedupeKey,
      input as FunctionArgs<typeof api.tasks.upsertByDedupeKey>,
    );
    return NextResponse.json({ ...result, success: true });
  }
  const id = await convex.mutation(api.tasks.create, input as FunctionArgs<typeof api.tasks.create>);
  return NextResponse.json({ id, created: true, success: true });
}

export async function PATCH(req: Request) {
  const body = await req.json();
  const { id, ...rawFields } = body;
  if (!id) return NextResponse.json({ error: "id required" }, { status: 400 });
  try {
    validateTaskAdmission(rawFields);
  } catch (error) {
    return NextResponse.json({ error: error instanceof Error ? error.message : String(error) }, { status: 400 });
  }
  const fields = normalizeTaskInput(rawFields, { includeAudit: true });
  await convex.mutation(
    api.tasks.update,
    { id: id as Id<"tasks">, ...fields } as FunctionArgs<typeof api.tasks.update>,
  );
  return NextResponse.json({ success: true });
}

export async function DELETE(req: Request) {
  const { searchParams } = new URL(req.url);
  const id = searchParams.get("id");
  if (!id) return NextResponse.json({ error: "id required" }, { status: 400 });
  await convex.mutation(api.tasks.remove, { id: id as Id<"tasks"> });
  return NextResponse.json({ success: true });
}
