import { NextResponse } from "next/server";
import { authorizeJtIdentity, secureCapabilityEqual } from "./outreach-auth";
import { SUPPRESSION_NOT_CONFIGURED, validateMissionControlSuppressionSubmission, validateSuppressionTuple } from "./outreach-suppression";

type Dependencies = {
  enabled: string | undefined;
  trustedJtLogin: string | undefined;
  decisionCapability: string | undefined;
  readCapability: string | undefined;
  reviewCapability: string | undefined;
  authorityWriteCapability: string | undefined;
  record: (input: Record<string, unknown>) => Promise<unknown>;
  query: (input: Record<string, unknown>) => Promise<unknown>;
};

async function requireCapability(provided: string | undefined, kind: "write" | "read", dependencies: Dependencies) {
  const values = [dependencies.decisionCapability, dependencies.readCapability, dependencies.reviewCapability, dependencies.authorityWriteCapability];
  if (values.some((value) => !value?.trim())) throw new Error(SUPPRESSION_NOT_CONFIGURED);
  const configured = values as string[];
  for (let left = 0; left < configured.length; left++) for (let right = left + 1; right < configured.length; right++) {
    if (await secureCapabilityEqual(configured[left], configured[right])) throw new Error(SUPPRESSION_NOT_CONFIGURED);
  }
  const expected = kind === "write" ? configured[0] : configured[1];
  if (!provided?.trim() || !(await secureCapabilityEqual(provided, expected))) throw new Error("unauthorized");
  return expected;
}

function disabled() { return NextResponse.json({ error: "outreach suppression owner is not configured" }, { status: 503 }); }
function invalid() { return NextResponse.json({ error: "invalid outreach suppression request" }, { status: 400 }); }
function dependencyError(error: unknown) {
  const message = error instanceof Error ? error.message : "";
  if (message.includes(SUPPRESSION_NOT_CONFIGURED)) return disabled();
  if (message.includes("CONFLICT")) return NextResponse.json({ error: "outreach suppression conflict" }, { status: 409 });
  return NextResponse.json({ error: "outreach suppression request failed" }, { status: 500 });
}

export function createOutreachSuppressionHandlers(dependencies: Dependencies) {
  return {
    POST: async (req: Request) => {
      if (dependencies.enabled !== "true") return disabled();
      let capability: string;
      try {
        authorizeJtIdentity(req.headers, dependencies.trustedJtLogin);
        capability = await requireCapability(req.headers.get("X-Outreach-Decision-Capability") ?? undefined, "write", dependencies);
      } catch (error) {
        const message = error instanceof Error ? error.message : "";
        if (message.includes(SUPPRESSION_NOT_CONFIGURED)) return disabled();
        if (message.includes("forbidden")) return NextResponse.json({ error: "JT identity forbidden" }, { status: 403 });
        return NextResponse.json({ error: message.includes("identity") ? "JT identity required" : "server capability required" }, { status: 401 });
      }
      let input: unknown;
      try { input = await req.json(); validateMissionControlSuppressionSubmission(input); } catch { return invalid(); }
      try { return NextResponse.json(await dependencies.record({ ...input, capability })); } catch (error) { return dependencyError(error); }
    },
    GET: async (req: Request) => {
      if (dependencies.enabled !== "true") return disabled();
      let capability: string;
      try { capability = await requireCapability(req.headers.get("X-Outreach-Review-Authority-Read-Capability") ?? undefined, "read", dependencies); }
      catch (error) { return error instanceof Error && error.message.includes(SUPPRESSION_NOT_CONFIGURED) ? disabled() : NextResponse.json({ error: "server capability required" }, { status: 401 }); }
      try {
        const params = new URL(req.url).searchParams;
        const keys = [...params.keys()].sort();
        const expected = ["channelFingerprint", "organizationFactId", "prospectId"];
        if (keys.length !== expected.length || keys.some((key, index) => key !== expected[index])) throw new Error("invalid");
        const tuple = { prospectId: params.get("prospectId"), organizationFactId: params.get("organizationFactId"), channelFingerprint: params.get("channelFingerprint") };
        validateSuppressionTuple(tuple);
        return NextResponse.json(await dependencies.query({ ...tuple, capability }));
      } catch (error) {
        if (error instanceof Error && (error.message.includes("invalid suppression") || error.message === "invalid")) return invalid();
        return dependencyError(error);
      }
    },
  };
}
