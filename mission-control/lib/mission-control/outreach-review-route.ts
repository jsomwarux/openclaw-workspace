import { NextResponse } from "next/server";
import { assertDistinctServerCapability, OutreachAuthError } from "./outreach-auth";
import { parseOutreachIdentity } from "./outreach-decision";
import { normalizeTaskInput, validateTaskAdmission } from "./task-admission";

type Dependencies = {
  serverCapability: string | undefined;
  peerCapability: string | undefined;
  admit: (input: Record<string, unknown>) => Promise<{ id: string; created: boolean }>;
};

const SAFE_REVIEW_ERRORS = new Map<string, number>([
  ["server capability is not a request-body field", 400],
  ["outreach review eligibility requires the specialized endpoint", 400],
  ["outreach decisions require the specialized endpoint", 400],
  ["candidateId required", 400],
  ["draftSha256 must be 64 lowercase hex characters", 400],
  ["title required", 400],
  ["dedupeKey required", 400],
]);

function reviewErrorResponse(error: unknown) {
  if (error instanceof OutreachAuthError) {
    return NextResponse.json({ error: error.message }, { status: error.status });
  }
  const message = error instanceof Error ? error.message : "";
  const safeStatus = SAFE_REVIEW_ERRORS.get(message);
  if (safeStatus) return NextResponse.json({ error: message }, { status: safeStatus });
  return NextResponse.json({ error: "outreach review request failed" }, { status: 500 });
}

function reviewDependencyErrorResponse(error: unknown) {
  if (
    error instanceof Error
    && error.message === "existing task is not the same server-admitted outreach review; create a new versioned task"
  ) {
    return NextResponse.json({ error: "outreach review conflict" }, { status: 409 });
  }
  return NextResponse.json({ error: "outreach review request failed" }, { status: 500 });
}

export function createOutreachReviewPostHandler(dependencies: Dependencies) {
  return async function POST(req: Request) {
    try {
      const callerCapability = req.headers.get("X-Outreach-Review-Capability") ?? undefined;
      const serverCapability = await assertDistinctServerCapability(
        callerCapability,
        dependencies.serverCapability,
        dependencies.peerCapability,
      );

      const body = await req.json() as Record<string, unknown>;
      if ("capability" in body) throw new Error("server capability is not a request-body field");
      validateTaskAdmission(body);
      const identity = parseOutreachIdentity(body.candidateId, body.draftSha256);
      const rawInput = { ...body, status: "todo", assignee: "jt", priority: "high", ...identity };
      const input = normalizeTaskInput(rawInput);
      if (!input.title) throw new Error("title required");
      if (!input.dedupeKey) throw new Error("dedupeKey required");

      let result: { id: string; created: boolean };
      try {
        result = await dependencies.admit({ ...input, capability: serverCapability });
      } catch (error) {
        return reviewDependencyErrorResponse(error);
      }
      return NextResponse.json({ ...result, success: true, writeMode: "create-only", reviewMode: "outreach-review" });
    } catch (error) {
      return reviewErrorResponse(error);
    }
  };
}
