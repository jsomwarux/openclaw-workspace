import { ConvexHttpClient } from "convex/browser";
import type { FunctionArgs } from "convex/server";
import { api } from "@/convex/_generated/api";
import { createOutreachReviewHandlers } from "@/lib/mission-control/outreach-review-route";

const handlers = createOutreachReviewHandlers({
  serverCapability: process.env.OUTREACH_REVIEW_CAPABILITY,
  peerCapability: process.env.OUTREACH_DECISION_CAPABILITY,
  admit: async (input) => {
    const convex = new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!);
    return await convex.mutation(
      api.tasks.createOutreachReview,
      input as FunctionArgs<typeof api.tasks.createOutreachReview>,
    );
  },
  lookup: async (input) => {
    const convex = new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!);
    return await convex.query(
      api.tasks.getOutreachReviewState,
      input as FunctionArgs<typeof api.tasks.getOutreachReviewState>,
    );
  },
});

export const GET = handlers.GET;
export const POST = handlers.POST;
