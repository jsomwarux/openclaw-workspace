import { NextResponse } from "next/server";
import { ConvexHttpClient } from "convex/browser";
import { api } from "@/convex/_generated/api";
import { Id } from "@/convex/_generated/dataModel";
import { lanePacketDependencyErrorResponse } from "@/lib/mission-control/lane-packet-route";

const convex = new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

export async function PATCH(req: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const body = await req.json();
  try {
    await convex.mutation(api.tasks.update, { id: id as Id<"tasks">, ...body });
  } catch (error) {
    // Lane packets refuse generic Done/archive/reopen; surface that as 409/400, not a bare 500.
    const lanePacketResponse = lanePacketDependencyErrorResponse(error);
    if (lanePacketResponse) return lanePacketResponse;
    throw error;
  }
  return NextResponse.json({ success: true });
}

export async function DELETE(req: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  try {
    await convex.mutation(api.tasks.remove, { id: id as Id<"tasks"> });
  } catch (error) {
    const lanePacketResponse = lanePacketDependencyErrorResponse(error);
    if (lanePacketResponse) return lanePacketResponse;
    throw error;
  }
  return NextResponse.json({ success: true });
}
