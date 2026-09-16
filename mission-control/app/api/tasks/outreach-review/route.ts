import { ConvexHttpClient } from "convex/browser";
import type { FunctionArgs } from "convex/server";
import { api } from "@/convex/_generated/api";
import { createOutreachReviewHandlers } from "@/lib/mission-control/outreach-review-route";
import { verifyProtectedSuppressionBinding } from "@/lib/mission-control/outreach-protected-git";

const handlers = createOutreachReviewHandlers({
  enabled: process.env.OUTREACH_SUPPRESSION_OWNER_ENABLED,
  serverCapability: process.env.OUTREACH_REVIEW_CAPABILITY,
  peerCapability: process.env.OUTREACH_DECISION_CAPABILITY,
  readCapability: process.env.OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY,
  authorityWriteCapability: process.env.OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY,
  verifySuppressionBinding: verifyProtectedSuppressionBinding,
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
