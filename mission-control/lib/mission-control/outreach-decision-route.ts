import { NextResponse } from "next/server";
import { parseOutreachIdentity, type OutreachDecisionValue } from "./outreach-decision";
import { assertDistinctServerCapability, authorizeJtIdentity, OutreachAuthError } from "./outreach-auth";

type DecideInput = {
  taskId: string;
  candidateId: string;
  draftSha256: string;
  snapshotSha256: string;
  decision: OutreachDecisionValue;
  capability: string;
};
type IdentityInput = Pick<DecideInput, "candidateId" | "draftSha256" | "snapshotSha256" | "capability">;

type Dependencies = {
  trustedJtLogin: string | undefined;
  serverCapability: string | undefined;
  peerCapability: string | undefined;
  decide: (input: DecideInput) => Promise<unknown>;
  lookup: (input: IdentityInput) => Promise<unknown>;
};

function authError(error: OutreachAuthError) {
  if (error.status === 503) return NextResponse.json({ error: "outreach authority is not configured" }, { status: 503 });
  if (error.status === 403) return NextResponse.json({ error: "JT identity forbidden" }, { status: 403 });
  if (error.message === "JT identity required") return NextResponse.json({ error: "JT identity required" }, { status: 401 });
  return NextResponse.json({ error: "server capability required" }, { status: 401 });
}

function invalidDecision(error: unknown) {
  if (error instanceof OutreachAuthError) return authError(error);
  return NextResponse.json({ error: "invalid outreach decision request" }, { status: 400 });
}

function dependencyError(error: unknown) {
  const code = error instanceof Error ? error.message : "";
  if (code === "OUTREACH_REVIEW_NOT_FOUND") return NextResponse.json({ error: "outreach review not found" }, { status: 404 });
  if (code === "OUTREACH_DECISION_CONFLICT") return NextResponse.json({ error: "outreach decision conflict" }, { status: 409 });
  return NextResponse.json({ error: "outreach decision request failed" }, { status: 500 });
}

export function createOutreachDecisionHandlers(dependencies: Dependencies) {
  async function decisionCapability(provided?: string) {
    return assertDistinctServerCapability(provided, dependencies.serverCapability, dependencies.peerCapability);
  }

  return {
    GET: async (req: Request) => {
      try {
        const capability = await decisionCapability(req.headers.get("X-Outreach-Decision-Capability") ?? undefined);
        const params = new URL(req.url).searchParams;
        const identity = parseOutreachIdentity(params.get("candidateId"), params.get("draftSha256"), params.get("snapshotSha256"));
        if (!("snapshotSha256" in identity)) throw new Error("snapshot required");
        try {
          return NextResponse.json(await dependencies.lookup({ ...identity, capability } as IdentityInput));
        } catch (error) {
          return dependencyError(error);
        }
      } catch (error) {
        return invalidDecision(error);
      }
    },
    POST: async (req: Request) => {
      try {
        authorizeJtIdentity(req.headers, dependencies.trustedJtLogin);
        const capability = await decisionCapability(dependencies.serverCapability);
        const body = await req.json() as Record<string, unknown>;
        const allowed = ["taskId", "candidateId", "draftSha256", "snapshotSha256", "decision"];
        if (Object.keys(body).some((key) => !allowed.includes(key)) || Object.keys(body).length !== allowed.length) {
          throw new Error("invalid fields");
        }
        const taskId = typeof body.taskId === "string" ? body.taskId : "";
        if (!taskId) throw new Error("taskId required");
        const identity = parseOutreachIdentity(body.candidateId, body.draftSha256, body.snapshotSha256);
        if (!("snapshotSha256" in identity)) throw new Error("snapshot required");
        if (body.decision !== "approve" && body.decision !== "reject") throw new Error("invalid decision");
        try {
          return NextResponse.json(await dependencies.decide({ taskId, ...identity, decision: body.decision, capability } as DecideInput));
        } catch (error) {
          return dependencyError(error);
        }
      } catch (error) {
        return invalidDecision(error);
      }
    },
  };
}
