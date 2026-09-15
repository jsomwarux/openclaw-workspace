import { NextResponse } from "next/server";
import { assertDistinctServerCapability, OutreachAuthError } from "./outreach-auth";
import { parseOutreachIdentity } from "./outreach-decision";
import { normalizeTaskInput, validateTaskAdmission } from "./task-admission";

type Dependencies = {
  serverCapability: string | undefined;
  peerCapability: string | undefined;
  admit: (input: Record<string, unknown>) => Promise<{ id: string; created: boolean }>;
};

function errorResponse(error: unknown, status = 400) {
  return NextResponse.json({ error: error instanceof Error ? error.message : String(error) }, { status });
}

export function createOutreachReviewPostHandler(dependencies: Dependencies) {
  return async function POST(req: Request) {
    try {
      const callerCapability = req.headers.get("X-Outreach-Review-Capability") ?? undefined;
      const serverCapability = assertDistinctServerCapability(
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

      const result = await dependencies.admit({ ...input, capability: serverCapability });
      return NextResponse.json({ ...result, success: true, writeMode: "create-only", reviewMode: "outreach-review" });
    } catch (error) {
      if (error instanceof OutreachAuthError) return errorResponse(error, error.status);
      const message = error instanceof Error ? error.message : String(error);
      return errorResponse(error, message.includes("existing task") ? 409 : 400);
    }
  };
}
