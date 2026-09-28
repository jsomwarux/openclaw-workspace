import { ConvexHttpClient } from "convex/browser";
import { api } from "@/convex/_generated/api";
import type { Id } from "@/convex/_generated/dataModel";
import { createLanePacketHandlers } from "@/lib/mission-control/lane-packet-route";

const handlers = createLanePacketHandlers({
  producerCapability: process.env.LANE_PACKET_CAPABILITY,
  decisionCapability: process.env.LANE_PACKET_DECISION_CAPABILITY,
  trustedJtLogin: process.env.LANE_PACKET_JT_LOGIN,
  admit: async (input) => {
    const convex = new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!);
    return await convex.mutation(api.tasks.admitLanePacket, input);
  },
  transition: async ({ id, transition, actor, capability }) => {
    const convex = new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!);
    return await convex.mutation(api.tasks.transitionLanePacket, { id: id as Id<"tasks">, transition, actor, capability });
  },
});

export const POST = handlers.POST;
export const PATCH = handlers.PATCH;
