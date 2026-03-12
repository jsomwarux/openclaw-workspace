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
  const { title, description, status = "todo", assignee = "eve", priority = "medium", project, slug, pipelineStage, sortOrder } = body;
  if (!title) return NextResponse.json({ error: "title required" }, { status: 400 });

  const id = await convex.mutation(api.tasks.create, {
    title, description, status, assignee, priority, project, slug, pipelineStage, sortOrder,
  });
  return NextResponse.json({ id, success: true });
}

export async function PATCH(req: Request) {
  const body = await req.json();
  const { id, ...fields } = body;
  if (!id) return NextResponse.json({ error: "id required" }, { status: 400 });
  await convex.mutation(api.tasks.update, { id: id as Id<"tasks">, ...fields });
  return NextResponse.json({ success: true });
}

export async function DELETE(req: Request) {
  const { searchParams } = new URL(req.url);
  const id = searchParams.get("id");
  if (!id) return NextResponse.json({ error: "id required" }, { status: 400 });
  await convex.mutation(api.tasks.remove, { id: id as Id<"tasks"> });
  return NextResponse.json({ success: true });
}
