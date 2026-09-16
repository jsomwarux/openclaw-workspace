import { ConvexHttpClient } from "convex/browser";
import { api } from "@/convex/_generated/api";
import { createOutreachSuppressionClearHandler } from "@/lib/mission-control/outreach-suppression-clear-route";
import { recordConsultingSuppressionClear } from "@/lib/mission-control/consulting-suppression-client";

const handler = createOutreachSuppressionClearHandler({
  enabled: process.env.OUTREACH_SUPPRESSION_OWNER_ENABLED,
  trustedJtLogin: process.env.OUTREACH_DECISION_JT_LOGIN,
  serverCapability: process.env.OUTREACH_DECISION_CAPABILITY,
  reviewCapability: process.env.OUTREACH_REVIEW_CAPABILITY,
  readCapability: process.env.OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY,
  authorityWriteCapability: process.env.OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY,
  loadReview: async (input) => new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!).query((api.tasks as any).findOutreachSuppressionReview, input as any) as any,
  recordConsulting: recordConsultingSuppressionClear as any,
  recordMissionControl: async (input) => new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!).mutation((api.tasks as any).appendOutreachSuppressionEvent, input as any),
});
export const POST = handler;
