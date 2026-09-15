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
import { buildTaskWriteResponse, resolveTaskWriteMode } from "@/lib/mission-control/task-write-mode";
import { parseTaskFeedbackAppend } from "@/lib/mission-control/task-feedback";

const convex = new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

async function readJsonObject(req: Request): Promise<
  | { ok: true; body: Record<string, unknown> }
  | { ok: false; response: Response }
> {
  try {
    const body: unknown = await req.json();
    if (!body || typeof body !== "object" || Array.isArray(body)) {
      return { ok: false, response: NextResponse.json({ error: "JSON object required" }, { status: 400 }) };
    }
    return { ok: true, body: body as Record<string, unknown> };
  } catch {
    return { ok: false, response: NextResponse.json({ error: "invalid JSON body" }, { status: 400 }) };
  }
}

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
  const parsed = await readJsonObject(req);
  if (!parsed.ok) return parsed.response;
  const body = parsed.body;
  const rawInput = { status: "todo", assignee: "eve", priority: "medium", ...body };
  try {
    validateTaskAdmission(rawInput);
  } catch (error) {
    return NextResponse.json({ error: error instanceof Error ? error.message : String(error) }, { status: 400 });
  }
  const input = normalizeTaskInput(rawInput);
  const { title } = input;
  if (!title) return NextResponse.json({ error: "title required" }, { status: 400 });

  let mode;
  try {
    mode = resolveTaskWriteMode(new URL(req.url).searchParams.get("mode"), Boolean(input.dedupeKey));
  } catch (error) {
    return NextResponse.json({ error: error instanceof Error ? error.message : String(error) }, { status: 400 });
  }

  if (mode === "create-only") {
    const result = await convex.mutation(
      api.tasks.createOnlyByDedupeKey,
      input as FunctionArgs<typeof api.tasks.createOnlyByDedupeKey>,
    );
    return NextResponse.json(buildTaskWriteResponse(mode, result));
  }
  if (mode === "upsert") {
    const result = await convex.mutation(
      api.tasks.upsertByDedupeKey,
      input as FunctionArgs<typeof api.tasks.upsertByDedupeKey>,
    );
    return NextResponse.json(buildTaskWriteResponse(mode, result));
  }
  const id = await convex.mutation(api.tasks.create, input as FunctionArgs<typeof api.tasks.create>);
  return NextResponse.json(buildTaskWriteResponse(mode, { id, created: true }));
}

export async function PATCH(req: Request) {
  const parsed = await readJsonObject(req);
  if (!parsed.ok) return parsed.response;
  const body = parsed.body;
  if (body.action === "append-feedback") {
    let input;
    try {
      input = parseTaskFeedbackAppend(body);
    } catch (error) {
      return NextResponse.json(
        { error: error instanceof Error ? error.message : "invalid feedback" },
        { status: 400 },
      );
    }
    try {
      const feedback = await convex.mutation(api.tasks.appendFeedback, {
        id: input.id as Id<"tasks">,
        body: input.body,
        author: input.author,
      });
      return NextResponse.json({ success: true, feedback });
    } catch {
      return NextResponse.json({ error: "feedback append failed" }, { status: 500 });
    }
  }
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
