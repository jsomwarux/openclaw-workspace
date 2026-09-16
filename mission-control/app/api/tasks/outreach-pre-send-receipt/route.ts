import { ConvexHttpClient } from "convex/browser";
import { api } from "@/convex/_generated/api";
import { createOutreachPreSendReceiptHandlers } from "@/lib/mission-control/outreach-pre-send-receipt-route";

const handlers = createOutreachPreSendReceiptHandlers({
  enabled: process.env.OUTREACH_SUPPRESSION_OWNER_ENABLED,
  reviewCapability: process.env.OUTREACH_REVIEW_CAPABILITY,
  readCapability: process.env.OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY,
  decisionCapability: process.env.OUTREACH_DECISION_CAPABILITY,
  authorityWriteCapability: process.env.OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY,
  create: async (input) => new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!).mutation((api.tasks as any).createOutreachPreSendReceipt, input as any),
  lookup: async (input) => new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!).query((api.tasks as any).findOutreachPreSendReceipt, input as any),
});
export const GET = handlers.GET;
export const POST = handlers.POST;
