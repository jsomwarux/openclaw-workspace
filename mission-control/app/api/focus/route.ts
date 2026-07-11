/**
 * Read-only HTTP API for the weekly focus row. The cockpit needs it client-side
 * to build the scoring context (focus projects + the $10K gate).
 *
 * GET /api/focus?weekOf=YYYY-MM-DD → { focus: FocusRow | null }
 */
import { NextResponse } from "next/server";
import { ConvexHttpClient } from "convex/browser";
import { api } from "@/convex/_generated/api";

const convex = new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const weekOf = searchParams.get("weekOf");
  if (!weekOf) return NextResponse.json({ error: "weekOf required" }, { status: 400 });

  const focus = await convex.query(api.tasks.getFocus, { weekOf });
  return NextResponse.json({ focus: focus ?? null });
}
