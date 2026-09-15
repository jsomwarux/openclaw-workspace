import { ConvexHttpClient } from "convex/browser";
import type { FunctionArgs } from "convex/server";
import { api } from "@/convex/_generated/api";
import { createOutreachReviewPostHandler } from "@/lib/mission-control/outreach-review-route";

export const POST = createOutreachReviewPostHandler({
  serverCapability: process.env.OUTREACH_REVIEW_CAPABILITY,
  admit: async (input) => {
    const convex = new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!);
    return await convex.mutation(
      api.tasks.createOutreachReview,
      input as FunctionArgs<typeof api.tasks.createOutreachReview>,
    );
  },
});
