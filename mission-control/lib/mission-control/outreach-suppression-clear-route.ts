import { NextResponse } from "next/server";
import { authorizeJtIdentity, secureCapabilityEqual } from "./outreach-auth";
import { deriveSuppressionClearInputs, type SuppressionBinding } from "./outreach-suppression-binding";

type Dependencies = {
  enabled: string | undefined;
  trustedJtLogin: string | undefined;
  serverCapability: string | undefined;
  reviewCapability: string | undefined;
  readCapability: string | undefined;
  authorityWriteCapability: string | undefined;
  loadReview: (input: { reviewId: string; capability: string }) => Promise<{ suppressionBinding: SuppressionBinding }>;
  derive?: typeof deriveSuppressionClearInputs;
  recordConsulting: (input: Record<string, unknown>) => Promise<unknown>;
  recordMissionControl: (input: Record<string, unknown>) => Promise<unknown>;
};

const REVIEW = /^review_[a-f0-9]{20}$/;
const EVENT = /^suppression_event_[a-f0-9]{20}$/;
const DIGEST = /^[a-f0-9]{64}$/;
const UTC = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$/;
function disabled() { return NextResponse.json({ error: "outreach suppression owner is not configured" }, { status: 503 }); }
function record(value: unknown): value is Record<string, unknown> { return Boolean(value) && typeof value === "object" && !Array.isArray(value); }
function ownerMetadata(value: unknown, missionControl = false) {
  if (!record(value) || typeof value.created !== "boolean" || !DIGEST.test(String(value.ownerRevision ?? ""))) throw new Error("invalid owner response");
  const source = missionControl ? value.event : value;
  if (!record(source) || !EVENT.test(String(source.eventId ?? "")) || !UTC.test(String(source.observedAt ?? "")) || !Number.isFinite(Date.parse(String(source.observedAt)))) throw new Error("invalid owner response");
  return { eventId: source.eventId as string, ownerRevision: value.ownerRevision as string, observedAt: source.observedAt as string };
}

export function createOutreachSuppressionClearHandler(dependencies: Dependencies) {
  return async (req: Request) => {
    if (dependencies.enabled !== "true") return disabled();
    try {
      authorizeJtIdentity(req.headers, dependencies.trustedJtLogin);
      const configured = [dependencies.serverCapability, dependencies.reviewCapability, dependencies.readCapability, dependencies.authorityWriteCapability];
      if (configured.some((value) => !value?.trim())) return disabled();
      const values = configured as string[];
      const decisionCapability = values[0];
      for (let left = 0; left < values.length; left++) for (let right = left + 1; right < values.length; right++) if (await secureCapabilityEqual(values[left], values[right])) return disabled();
      let body: unknown;
      try { body = await req.json(); } catch { return NextResponse.json({ error: "invalid outreach suppression clear request" }, { status: 400 }); }
      if (!body || typeof body !== "object" || Array.isArray(body) || Object.keys(body).length !== 1 || !REVIEW.test(String((body as Record<string, unknown>).reviewId ?? ""))) throw new Error("invalid");
      const reviewId = (body as { reviewId: string }).reviewId;
      const review = await dependencies.loadReview({ reviewId, capability: decisionCapability });
      const inputs = await (dependencies.derive ?? deriveSuppressionClearInputs)(reviewId, review.suppressionBinding);
      const consulting = await dependencies.recordConsulting({ ...inputs.consulting, actorId: "jt:mission-control-clear" });
      const missionControl = await dependencies.recordMissionControl({ ...inputs.missionControl, capability: decisionCapability });
      return NextResponse.json({ consulting: ownerMetadata(consulting), missionControl: ownerMetadata(missionControl, true) });
    } catch (error) {
      const message = error instanceof Error ? error.message : "";
      if (message.includes("forbidden")) return NextResponse.json({ error: "JT identity forbidden" }, { status: 403 });
      if (message.includes("identity")) return NextResponse.json({ error: "JT identity required" }, { status: 401 });
      if (message === "invalid") return NextResponse.json({ error: "invalid outreach suppression clear request" }, { status: 400 });
      return NextResponse.json({ error: "outreach suppression clear failed" }, { status: 500 });
    }
  };
}
