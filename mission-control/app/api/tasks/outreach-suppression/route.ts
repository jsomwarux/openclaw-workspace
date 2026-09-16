import { ConvexHttpClient } from "convex/browser";
import { api } from "@/convex/_generated/api";
import { createOutreachSuppressionHandlers } from "@/lib/mission-control/outreach-suppression-route";

const handlers = createOutreachSuppressionHandlers({
  enabled: process.env.OUTREACH_SUPPRESSION_OWNER_ENABLED,
  trustedJtLogin: process.env.OUTREACH_DECISION_JT_LOGIN,
  decisionCapability: process.env.OUTREACH_DECISION_CAPABILITY,
  readCapability: process.env.OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY,
  reviewCapability: process.env.OUTREACH_REVIEW_CAPABILITY,
  authorityWriteCapability: process.env.OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY,
  record: async (input) => new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!).mutation((api.tasks as any).appendOutreachSuppressionEvent, input as any),
  query: async (input) => new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!).query((api.tasks as any).findOutreachSuppressionState, input as any),
});
export const GET = handlers.GET;
export const POST = handlers.POST;
