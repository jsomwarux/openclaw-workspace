/**
 * Read-only view of the priorityAudit trail so the inspection drawer can show
 * who last moved a task's rank inputs, and on what evidence.
 *
 * GET /api/task-audit?taskId=<id>  → audit rows for one task
 * GET /api/task-audit              → 100 most recent rows
 */
import { NextResponse } from "next/server";
import { ConvexHttpClient } from "convex/browser";
import { api } from "@/convex/_generated/api";

const convex = new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const taskId = searchParams.get("taskId") ?? undefined;
  const entries = await convex.query(api.tasks.listAudit, taskId ? { taskId } : {});
  return NextResponse.json({ entries });
}
