import { NextResponse } from "next/server";
import { OutreachAuthError, secureCapabilityEqual } from "./outreach-auth";
import {
  OUTREACH_REVIEW_AUTHORITY_NOT_CONFIGURED,
  resolveOutreachReviewAuthorityLookup,
  validateOutreachReviewAuthorityLookup,
  validateOutreachReviewAuthoritySubmission,
  type OutreachReviewAuthority,
  type OutreachReviewAuthorityLookup,
  type OutreachReviewAuthoritySubmission,
} from "./outreach-review-authority";

type CreateInput = OutreachReviewAuthoritySubmission & { capability: string };
type LookupInput = OutreachReviewAuthorityLookup & { capability: string };

export type OutreachReviewAuthorityRouteDependencies = {
  writeCapability: string | undefined;
  readCapability: string | undefined;
  reviewCapability: string | undefined;
  decisionCapability: string | undefined;
  create: (input: CreateInput) => Promise<unknown>;
  lookup: (input: LookupInput) => Promise<unknown>;
};

const QUERY_FIELDS = [
  "candidateId",
  "draftSha256",
  "authorityBundleHash",
  "verifierReportSha256",
  "verifierGitRepository",
  "verifierGitCommitSha",
  "verifierGitPath",
  "verifierGitBlobSha256",
] as const;

const AUTHORITY_FIELDS = [
  "candidateId", "draftSha256", "authorityBundleHash", "verifierReportSha256", "verifierGitBinding",
  "builderActorId", "drafterActorId", "verifierActorId", "reviewId", "observedAt", "authorityRevision",
] as const;

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function hasExactKeys(value: Record<string, unknown>, expected: readonly string[]): boolean {
  const actual = Object.keys(value).sort();
  const wanted = [...expected].sort();
  return actual.length === wanted.length && actual.every((key, index) => key === wanted[index]);
}

async function assertCapabilityConfiguration(
  provided: string | undefined,
  expected: "write" | "read",
  dependencies: OutreachReviewAuthorityRouteDependencies,
): Promise<string> {
  const values = [
    dependencies.writeCapability,
    dependencies.readCapability,
    dependencies.reviewCapability,
    dependencies.decisionCapability,
  ];
  if (values.some((value) => !value?.trim())) {
    throw new OutreachAuthError("capability configuration is invalid", 503);
  }
  const configured = values as [string, string, string, string];
  for (let left = 0; left < configured.length; left += 1) {
    for (let right = left + 1; right < configured.length; right += 1) {
      if (await secureCapabilityEqual(configured[left], configured[right])) {
        throw new OutreachAuthError("capability configuration is invalid", 503);
      }
    }
  }
  const required = expected === "write" ? configured[0] : configured[1];
  if (!provided?.trim() || !(await secureCapabilityEqual(provided, required))) {
    throw new OutreachAuthError("server capability required", 401);
  }
  return required;
}

function invalidRequest() {
  return NextResponse.json({ error: "invalid outreach review authority request" }, { status: 400 });
}

function authError(error: OutreachAuthError) {
  if (error.status === 503) {
    return NextResponse.json({ error: "outreach authority is not configured" }, { status: 503 });
  }
  return NextResponse.json({ error: "server capability required" }, { status: 401 });
}

function dependencyError(error: unknown) {
  const message = error instanceof Error ? error.message : "";
  const hasCode = (code: string) => new RegExp(`(?:^|[^A-Z0-9_])${code}(?:$|[^A-Z0-9_])`).test(message);
  if (hasCode(OUTREACH_REVIEW_AUTHORITY_NOT_CONFIGURED)) {
    return NextResponse.json({ error: "outreach authority is not configured" }, { status: 503 });
  }
  if (hasCode("OUTREACH_REVIEW_AUTHORITY_INVALID")) return invalidRequest();
  if (hasCode("OUTREACH_REVIEW_AUTHORITY_CONFLICT")) {
    return NextResponse.json({ error: "outreach review authority conflict" }, { status: 409 });
  }
  if (hasCode("OUTREACH_REVIEW_AUTHORITY_CORRUPT")) {
    return NextResponse.json({ error: "outreach review authority state is corrupt" }, { status: 409 });
  }
  return NextResponse.json({ error: "outreach review authority request failed" }, { status: 500 });
}

function parseLookup(req: Request): OutreachReviewAuthorityLookup {
  const params = new URL(req.url).searchParams;
  const keys = [...params.keys()].sort();
  const expected = [...QUERY_FIELDS].sort();
  if (keys.length !== expected.length || keys.some((key, index) => key !== expected[index])) {
    throw new Error("invalid query");
  }
  const lookup = {
    candidateId: params.get("candidateId"),
    draftSha256: params.get("draftSha256"),
    authorityBundleHash: params.get("authorityBundleHash"),
    verifierReportSha256: params.get("verifierReportSha256"),
    verifierGitBinding: {
      repository: params.get("verifierGitRepository"),
      commitSha: params.get("verifierGitCommitSha"),
      path: params.get("verifierGitPath"),
      blobSha256: params.get("verifierGitBlobSha256"),
    },
  };
  validateOutreachReviewAuthorityLookup(lookup);
  return lookup;
}

async function validateAuthority(value: unknown, lookup: OutreachReviewAuthorityLookup): Promise<OutreachReviewAuthority> {
  if (!isRecord(value) || !hasExactKeys(value, AUTHORITY_FIELDS)) throw new Error("invalid authority response");
  const authority = await resolveOutreachReviewAuthorityLookup([value as OutreachReviewAuthority], lookup);
  if (!authority) throw new Error("invalid authority response");
  return authority;
}

async function projectCreateResult(value: unknown, input: OutreachReviewAuthoritySubmission) {
  if (!isRecord(value) || !hasExactKeys(value, ["created", "authority"]) || typeof value.created !== "boolean") {
    throw new Error("invalid create response");
  }
  const lookup: OutreachReviewAuthorityLookup = {
    candidateId: input.candidateId,
    draftSha256: input.draftSha256,
    authorityBundleHash: input.authorityBundleHash,
    verifierReportSha256: input.verifierReportSha256,
    verifierGitBinding: input.verifierGitBinding,
  };
  const authority = await validateAuthority(value.authority, lookup);
  if (authority.builderActorId !== input.builderActorId || authority.drafterActorId !== input.drafterActorId) {
    throw new Error("invalid create response");
  }
  return { created: value.created, authority };
}

async function projectLookupResult(value: unknown, lookup: OutreachReviewAuthorityLookup) {
  if (!isRecord(value) || typeof value.authorized !== "boolean") throw new Error("invalid lookup response");
  if (value.authorized === false) {
    if (!hasExactKeys(value, ["authorized"])) throw new Error("invalid lookup response");
    return { authorized: false } as const;
  }
  if (!hasExactKeys(value, ["authorized", "authority"])) throw new Error("invalid lookup response");
  return { authorized: true as const, authority: await validateAuthority(value.authority, lookup) };
}

export function createOutreachReviewAuthorityHandlers(dependencies: OutreachReviewAuthorityRouteDependencies) {
  return {
    POST: async (req: Request) => {
      let capability: string;
      try {
        capability = await assertCapabilityConfiguration(
          req.headers.get("X-Outreach-Review-Authority-Write-Capability") ?? undefined,
          "write",
          dependencies,
        );
      } catch (error) {
        return error instanceof OutreachAuthError ? authError(error) : dependencyError(error);
      }
      let input: unknown;
      try {
        input = await req.json();
        validateOutreachReviewAuthoritySubmission(input);
      } catch {
        return invalidRequest();
      }
      try {
        return NextResponse.json(await projectCreateResult(
          await dependencies.create({ ...input, capability }),
          input,
        ));
      } catch (error) {
        return dependencyError(error);
      }
    },
    GET: async (req: Request) => {
      let capability: string;
      try {
        capability = await assertCapabilityConfiguration(
          req.headers.get("X-Outreach-Review-Authority-Read-Capability") ?? undefined,
          "read",
          dependencies,
        );
      } catch (error) {
        return error instanceof OutreachAuthError ? authError(error) : dependencyError(error);
      }
      let lookup: OutreachReviewAuthorityLookup;
      try {
        lookup = parseLookup(req);
      } catch {
        return invalidRequest();
      }
      try {
        return NextResponse.json(await projectLookupResult(
          await dependencies.lookup({ ...lookup, capability }),
          lookup,
        ));
      } catch (error) {
        return dependencyError(error);
      }
    },
  };
}
