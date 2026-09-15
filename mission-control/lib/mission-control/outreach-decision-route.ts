import { NextResponse } from "next/server";
import { parseOutreachIdentity, type OutreachDecisionValue } from "./outreach-decision";

type DecideInput = {
  taskId: string;
  candidateId: string;
  draftSha256: string;
  decision: OutreachDecisionValue;
};

type Dependencies = {
  decide: (input: DecideInput) => Promise<unknown>;
  lookup: (input: Omit<DecideInput, "taskId" | "decision">) => Promise<unknown>;
};

function errorResponse(error: unknown, status = 400) {
  return NextResponse.json({ error: error instanceof Error ? error.message : String(error) }, { status });
}

export function createOutreachDecisionHandlers(dependencies: Dependencies) {
  return {
    GET: async (req: Request) => {
      const searchParams = new URL(req.url).searchParams;
      const candidateId = searchParams.get("candidateId");
      const draftSha256 = searchParams.get("draftSha256");
      try {
        return NextResponse.json(await dependencies.lookup(parseOutreachIdentity(candidateId, draftSha256)));
      } catch (error) {
        return errorResponse(error);
      }
    },
    POST: async (req: Request) => {
      try {
        const body = await req.json() as Record<string, unknown>;
        if ("decidedBy" in body || "decidedAt" in body || "outreachDecision" in body) {
          throw new Error("decision authority fields are server-owned");
        }
        const taskId = typeof body.taskId === "string" ? body.taskId : "";
        const candidateId = body.candidateId;
        const draftSha256 = body.draftSha256;
        const decision = body.decision;
        if (!taskId) throw new Error("taskId required");
        const identity = parseOutreachIdentity(candidateId, draftSha256);
        if (decision !== "approve" && decision !== "reject") throw new Error("decision must be approve or reject");
        return NextResponse.json(await dependencies.decide({ taskId, ...identity, decision }));
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        return errorResponse(error, message.includes("immutable") ? 409 : 400);
      }
    },
  };
}
