import { NextResponse } from "next/server";
import { secureCapabilityEqual } from "./outreach-auth";
import { validatePreSendReceiptSubmission } from "./outreach-suppression-binding";

type Dependencies = {
  enabled: string | undefined;
  reviewCapability: string | undefined;
  readCapability: string | undefined;
  decisionCapability: string | undefined;
  authorityWriteCapability: string | undefined;
  create: (input: Record<string, unknown>) => Promise<unknown>;
  lookup: (input: Record<string, unknown>) => Promise<unknown>;
};
const ID = /^pre_send_[a-f0-9]{20}$/;
function disabled() { return NextResponse.json({ error: "outreach suppression owner is not configured" }, { status: 503 }); }
async function capability(provided: string | undefined, kind: "write" | "read", dependencies: Dependencies) {
  const values = [dependencies.reviewCapability, dependencies.readCapability, dependencies.decisionCapability, dependencies.authorityWriteCapability];
  if (values.some((value) => !value?.trim())) throw new Error("disabled");
  const configured = values as string[];
  for (let left = 0; left < configured.length; left++) for (let right = left + 1; right < configured.length; right++) if (await secureCapabilityEqual(configured[left], configured[right])) throw new Error("disabled");
  const expected = kind === "write" ? configured[0] : configured[1];
  if (!provided?.trim() || !(await secureCapabilityEqual(provided, expected))) throw new Error("unauthorized");
  return expected;
}
function failed(error: unknown) {
  const message = error instanceof Error ? error.message : "";
  if (message === "disabled") return disabled();
  if (message === "unauthorized") return NextResponse.json({ error: "server capability required" }, { status: 401 });
  if (message.includes("CONFLICT")) return NextResponse.json({ error: "pre-send receipt conflict" }, { status: 409 });
  return NextResponse.json({ error: "pre-send receipt request failed" }, { status: 500 });
}

export function createOutreachPreSendReceiptHandlers(dependencies: Dependencies) {
  return {
    POST: async (req: Request) => {
      if (dependencies.enabled !== "true") return disabled();
      try {
        const cap = await capability(req.headers.get("X-Outreach-Review-Capability") ?? undefined, "write", dependencies);
        let input: unknown;
        try { input = await req.json(); validatePreSendReceiptSubmission(input); } catch { return NextResponse.json({ error: "invalid pre-send receipt request" }, { status: 400 }); }
        return NextResponse.json(await dependencies.create({ ...input, capability: cap }));
      } catch (error) { return failed(error); }
    },
    GET: async (req: Request) => {
      if (dependencies.enabled !== "true") return disabled();
      try {
        const cap = await capability(req.headers.get("X-Outreach-Review-Authority-Read-Capability") ?? undefined, "read", dependencies);
        const params = new URL(req.url).searchParams;
        if ([...params.keys()].length !== 1 || !ID.test(params.get("preSendReceiptId") ?? "")) return NextResponse.json({ error: "invalid pre-send receipt request" }, { status: 400 });
        return NextResponse.json(await dependencies.lookup({ preSendReceiptId: params.get("preSendReceiptId")!, capability: cap }));
      } catch (error) { return failed(error); }
    },
  };
}
