import { NextResponse } from "next/server";
import { parseOutreachIdentity, type OutreachDecisionValue } from "./outreach-decision";
import { assertDistinctServerCapability, authorizeJtIdentity, OutreachAuthError } from "./outreach-auth";

type DecideInput = {
  taskId: string;
  candidateId: string;
  draftSha256: string;
  decision: OutreachDecisionValue;
  capability: string;
};

type IdentityInput = Pick<DecideInput, "candidateId" | "draftSha256">;

type Dependencies = {
  trustedJtLogin: string | undefined;
  serverCapability: string | undefined;
  peerCapability: string | undefined;
  decide: (input: DecideInput) => Promise<unknown>;
  lookup: (input: IdentityInput) => Promise<unknown>;
};

const SAFE_DECISION_ERRORS = new Map<string, number>([
  ["decision authority fields are server-owned", 400],
  ["taskId required", 400],
  ["candidateId required", 400],
  ["draftSha256 must be 64 lowercase hex characters", 400],
  ["decision must be approve or reject", 400],
]);

function decisionErrorResponse(error: unknown) {
  if (error instanceof OutreachAuthError) {
    return NextResponse.json({ error: error.message }, { status: error.status });
  }
  const message = error instanceof Error ? error.message : "";
  const safeStatus = SAFE_DECISION_ERRORS.get(message);
  if (safeStatus) return NextResponse.json({ error: message }, { status: safeStatus });
  return NextResponse.json({ error: "outreach decision request failed" }, { status: 500 });
}

function decisionDependencyErrorResponse(error: unknown) {
  if (
    error instanceof Error
    && error.message === "outreach decision is immutable; create a new versioned task"
  ) {
    return NextResponse.json({ error: "outreach decision conflict" }, { status: 409 });
  }
  return NextResponse.json({ error: "outreach decision request failed" }, { status: 500 });
}

export function createOutreachDecisionHandlers(dependencies: Dependencies) {
  return {
    GET: async (req: Request) => {
      const searchParams = new URL(req.url).searchParams;
      const candidateId = searchParams.get("candidateId");
      const draftSha256 = searchParams.get("draftSha256");
      try {
        const identity = parseOutreachIdentity(candidateId, draftSha256);
        try {
          return NextResponse.json(await dependencies.lookup(identity));
        } catch (error) {
          return decisionDependencyErrorResponse(error);
        }
      } catch (error) {
        return decisionErrorResponse(error);
      }
    },
    POST: async (req: Request) => {
      try {
        authorizeJtIdentity(req.headers, dependencies.trustedJtLogin);
        const serverCapability = await assertDistinctServerCapability(
          dependencies.serverCapability,
          dependencies.serverCapability,
          dependencies.peerCapability,
        );
        const body = await req.json() as Record<string, unknown>;
        if ("decidedBy" in body || "decidedAt" in body || "outreachDecision" in body || "capability" in body) {
          throw new Error("decision authority fields are server-owned");
        }
        const taskId = typeof body.taskId === "string" ? body.taskId : "";
        const candidateId = body.candidateId;
        const draftSha256 = body.draftSha256;
        const decision = body.decision;
        if (!taskId) throw new Error("taskId required");
        const identity = parseOutreachIdentity(candidateId, draftSha256);
        if (decision !== "approve" && decision !== "reject") throw new Error("decision must be approve or reject");
        try {
          return NextResponse.json(await dependencies.decide({
            taskId,
            ...identity,
            decision,
            capability: serverCapability,
          }));
        } catch (error) {
          return decisionDependencyErrorResponse(error);
        }
      } catch (error) {
        return decisionErrorResponse(error);
      }
    },
  };
}
