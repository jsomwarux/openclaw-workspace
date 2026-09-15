import { ConvexHttpClient } from "convex/browser";
import type { FunctionArgs } from "convex/server";
import { api } from "@/convex/_generated/api";
import { createOutreachDecisionHandlers } from "@/lib/mission-control/outreach-decision-route";

const convex = new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

const handlers = createOutreachDecisionHandlers({
  decide: async (input) => await convex.mutation(
    api.tasks.decideOutreach,
    input as FunctionArgs<typeof api.tasks.decideOutreach>,
  ),
  lookup: async (input) => await convex.query(
    api.tasks.findOutreachDecision,
    input as FunctionArgs<typeof api.tasks.findOutreachDecision>,
  ),
});

export const GET = handlers.GET;
export const POST = handlers.POST;
