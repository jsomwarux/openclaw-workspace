/**
 * Pipeline stage tracker — called by Opticfy pipeline agents on every PIPELINE_HANDOFF.
 *
 * POST /api/pipeline  { slug, stage, company? }
 *   → finds task by slug, updates pipelineStage + description + status
 *   → if no task found with that slug, creates one automatically
 *
 * GET  /api/pipeline?slug=xxx
 *   → returns current pipeline state for a client
 *
 * Stage labels:
 *   research-complete | analysis-complete | jt-review | workflow-built |
 *   deck-built | outreach-drafted | pitched | delivered
 *
 * Note: Uses internal fetch to /api/tasks to avoid dependency on stale generated Convex types.
 * When Convex regenerates (slug + pipelineStage in schema), this can be refactored to use
 * the typed client directly.
 */
import { NextResponse } from "next/server";

const BASE_URL = process.env.NEXT_PUBLIC_APP_URL ?? "http://localhost:3000";

const STAGE_LABELS: Record<string, { emoji: string; label: string; status: "todo" | "in-progress" | "done" }> = {
  "research-complete":  { emoji: "🔬", label: "Research complete → Analysis in progress",  status: "in-progress" },
  "analysis-complete":  { emoji: "🧠", label: "Analysis complete → Awaiting JT review",    status: "in-progress" },
  "jt-review":          { emoji: "👀", label: "JT review pending",                          status: "in-progress" },
  "workflow-built":     { emoji: "⚙️",  label: "Workflow built → Presentation in progress", status: "in-progress" },
  "deck-built":         { emoji: "📊", label: "Deck built → Outreach drafting",             status: "in-progress" },
  "outreach-drafted":   { emoji: "📤", label: "Outreach ready → Awaiting JT send",          status: "in-progress" },
  "pitched":            { emoji: "✉️",  label: "Pitched — awaiting response",               status: "in-progress" },
  "delivered":          { emoji: "✅", label: "Delivered",                                  status: "done"        },
};

async function findTaskBySlug(slug: string) {
  const res = await fetch(`${BASE_URL}/api/tasks`);
  const { tasks } = await res.json();
  return (tasks as Array<Record<string, unknown>>).find((t) => t.slug === slug) ?? null;
}

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const slug = searchParams.get("slug");
  if (!slug) return NextResponse.json({ error: "slug required" }, { status: 400 });

  const task = await findTaskBySlug(slug);
  if (!task) return NextResponse.json({ error: "not found" }, { status: 404 });
  return NextResponse.json({ task });
}

export async function POST(req: Request) {
  const body = await req.json();
  const { slug, stage, company } = body;
  if (!slug || !stage) return NextResponse.json({ error: "slug and stage required" }, { status: 400 });

  const stageInfo = STAGE_LABELS[stage] ?? { emoji: "🔄", label: stage, status: "in-progress" as const };
  const description = `${stageInfo.emoji} ${stageInfo.label}\nPipeline slug: ${slug}`;

  const existing = await findTaskBySlug(slug);

  if (existing) {
    const patchRes = await fetch(`${BASE_URL}/api/tasks`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id: existing._id,
        pipelineStage: stage,
        description,
        status: stageInfo.status,
      }),
    });
    const result = await patchRes.json();
    return NextResponse.json({ success: true, action: "updated", ...result });
  }

  // Auto-create if no task with this slug exists
  const title = company ? `Opticfy Pipeline — ${company}` : `Opticfy Pipeline — ${slug}`;
  const createRes = await fetch(`${BASE_URL}/api/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title,
      description,
      status: stageInfo.status,
      assignee: "eve",
      priority: "high",
      project: "Opticfy",
      slug,
      pipelineStage: stage,
    }),
  });
  const result = await createRes.json();
  return NextResponse.json({ success: true, action: "created", ...result });
}
