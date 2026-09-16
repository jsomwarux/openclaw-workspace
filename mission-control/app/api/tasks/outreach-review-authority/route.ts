import { ConvexHttpClient } from "convex/browser";
import type { FunctionArgs } from "convex/server";
import { api } from "@/convex/_generated/api";
import { createOutreachReviewAuthorityHandlers } from "@/lib/mission-control/outreach-review-authority-route";

const handlers = createOutreachReviewAuthorityHandlers({
  writeCapability: process.env.OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY,
  readCapability: process.env.OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY,
  reviewCapability: process.env.OUTREACH_REVIEW_CAPABILITY,
  decisionCapability: process.env.OUTREACH_DECISION_CAPABILITY,
  create: async (input) => {
    const convex = new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!);
    return await convex.mutation(
      api.tasks.createOutreachReviewAuthority,
      input as FunctionArgs<typeof api.tasks.createOutreachReviewAuthority>,
    );
  },
  lookup: async (input) => {
    const convex = new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!);
    return await convex.query(
      api.tasks.findOutreachReviewAuthority,
      input as FunctionArgs<typeof api.tasks.findOutreachReviewAuthority>,
    );
  },
});

export const GET = handlers.GET;
export const POST = handlers.POST;
