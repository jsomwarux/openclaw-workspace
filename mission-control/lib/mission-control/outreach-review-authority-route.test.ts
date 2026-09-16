import { describe, expect, test } from "bun:test";
import {
  createOutreachReviewAuthorityHandlers,
  type OutreachReviewAuthorityRouteDependencies,
} from "./outreach-review-authority-route";

const WRITE_CAPABILITY = "authority-write-secret";
const READ_CAPABILITY = "authority-read-secret";
const REVIEW_CAPABILITY = "review-secret";
const DECISION_CAPABILITY = "decision-secret";
const DRAFT_SHA = "a".repeat(64);
const BUNDLE_SHA = "b".repeat(64);
const REPORT_SHA = "c".repeat(64);
const COMMIT_SHA = "d".repeat(40);

const verifierGitBinding = {
  repository: "owner/repo",
  commitSha: COMMIT_SHA,
  path: "reviews/verifier-report.json",
  blobSha256: REPORT_SHA,
};

const submission = {
  candidateId: "candidate-1",
  draftSha256: DRAFT_SHA,
  authorityBundleHash: BUNDLE_SHA,
  verifierReportSha256: REPORT_SHA,
  verifierGitBinding,
  builderActorId: "builder-1",
  drafterActorId: "drafter-1",
};

const authority = {
  ...submission,
  verifierActorId: "verifier-1",
  reviewId: "review_" + "1".repeat(20),
  observedAt: 1_789_452_000_000,
  authorityRevision: "review_authority_" + "2".repeat(20),
};

function dependencies(
  overrides: Partial<OutreachReviewAuthorityRouteDependencies> = {},
): OutreachReviewAuthorityRouteDependencies {
  return {
    writeCapability: WRITE_CAPABILITY,
    readCapability: READ_CAPABILITY,
    reviewCapability: REVIEW_CAPABILITY,
    decisionCapability: DECISION_CAPABILITY,
    create: async () => ({ created: true, authority }),
    lookup: async () => ({ authorized: true, authority }),
    ...overrides,
  };
}

function postRequest(payload: unknown = submission, capability?: string) {
  return new Request("http://localhost/api/tasks/outreach-review-authority", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(capability ? { "X-Outreach-Review-Authority-Write-Capability": capability } : {}),
    },
    body: JSON.stringify(payload),
  });
}

function getRequest(
  query: URLSearchParams = new URLSearchParams({
    candidateId: submission.candidateId,
    draftSha256: submission.draftSha256,
    authorityBundleHash: submission.authorityBundleHash,
    verifierReportSha256: submission.verifierReportSha256,
    verifierGitRepository: verifierGitBinding.repository,
    verifierGitCommitSha: verifierGitBinding.commitSha,
    verifierGitPath: verifierGitBinding.path,
    verifierGitBlobSha256: verifierGitBinding.blobSha256,
  }),
  capability?: string,
) {
  return new Request(`http://localhost/api/tasks/outreach-review-authority?${query}`, {
    headers: capability ? { "X-Outreach-Review-Authority-Read-Capability": capability } : {},
  });
}

describe("outreach review authority owner API", () => {
  test("POST accepts only the client authority submission and forwards no verifier identity", async () => {
    let received: unknown;
    const handlers = createOutreachReviewAuthorityHandlers(dependencies({
      create: async (input) => {
        received = input;
        return { created: true, authority };
      },
    }));

    const response = await handlers.POST(postRequest(submission, WRITE_CAPABILITY));

    expect(response.status).toBe(200);
    expect(received).toEqual({ ...submission, capability: WRITE_CAPABILITY });
    expect(await response.json()).toEqual({ created: true, authority });
  });

  test("POST rejects dropped, unknown, verifier-owned, and server-owned fields before Convex", async () => {
    let calls = 0;
    const handlers = createOutreachReviewAuthorityHandlers(dependencies({
      create: async () => {
        calls += 1;
        return { created: true, authority };
      },
    }));
    const { drafterActorId: _dropped, ...dropped } = submission;
    for (const payload of [
      dropped,
      { ...submission, unknown: true },
      { ...submission, verifierActorId: "caller-verifier" },
      { ...submission, reviewId: "review_" + "9".repeat(20) },
      { ...submission, observedAt: 1 },
      { ...submission, authorityRevision: "review_authority_" + "9".repeat(20) },
      { ...submission, capability: WRITE_CAPABILITY },
      { ...submission, authorized: true },
    ]) {
      const response = await handlers.POST(postRequest(payload, WRITE_CAPABILITY));
      expect(response.status).toBe(400);
      expect(await response.json()).toEqual({ error: "invalid outreach review authority request" });
    }
    expect(calls).toBe(0);
  });

  test("GET requires the complete exact lookup key and rejects aliases or unknown query fields before Convex", async () => {
    let calls = 0;
    const handlers = createOutreachReviewAuthorityHandlers(dependencies({
      lookup: async () => {
        calls += 1;
        return { authorized: false };
      },
    }));
    const complete = new URL(getRequest(undefined, READ_CAPABILITY).url).searchParams;
    const malformed = [
      new URLSearchParams([...complete].filter(([key]) => key !== "verifierGitPath")),
      new URLSearchParams([...complete, ["unknown", "value"]]),
      new URLSearchParams([...complete, ["candidateId", "candidate-2"]]),
      new URLSearchParams({
        candidateId: submission.candidateId,
        draftSha256: submission.draftSha256,
        authorityBundleHash: submission.authorityBundleHash,
        verifierReportSha256: submission.verifierReportSha256,
        repository: verifierGitBinding.repository,
        commitSha: verifierGitBinding.commitSha,
        path: verifierGitBinding.path,
        blobSha256: verifierGitBinding.blobSha256,
      }),
    ];
    for (const query of malformed) {
      const response = await handlers.GET(getRequest(query, READ_CAPABILITY));
      expect(response.status).toBe(400);
      expect(await response.json()).toEqual({ error: "invalid outreach review authority request" });
    }
    expect(calls).toBe(0);
  });

  test("GET passes the full nested Git-bound lookup and projects present and absent responses exactly", async () => {
    let received: unknown;
    const present = createOutreachReviewAuthorityHandlers(dependencies({
      lookup: async (input) => {
        received = input;
        return { authorized: true, authority };
      },
    }));
    const presentResponse = await present.GET(getRequest(undefined, READ_CAPABILITY));
    expect(presentResponse.status).toBe(200);
    expect(received).toEqual({
      candidateId: submission.candidateId,
      draftSha256: submission.draftSha256,
      authorityBundleHash: submission.authorityBundleHash,
      verifierReportSha256: submission.verifierReportSha256,
      verifierGitBinding,
      capability: READ_CAPABILITY,
    });
    expect(await presentResponse.json()).toEqual({ authorized: true, authority });

    const absent = createOutreachReviewAuthorityHandlers(dependencies({
      lookup: async () => ({ authorized: false }),
    }));
    const absentResponse = await absent.GET(getRequest(undefined, READ_CAPABILITY));
    expect(absentResponse.status).toBe(200);
    expect(await absentResponse.json()).toEqual({ authorized: false });
  });

  test("POST and GET require their least-privilege capability and never call Convex on failure", async () => {
    let calls = 0;
    const handlers = createOutreachReviewAuthorityHandlers(dependencies({
      create: async () => { calls += 1; return { created: true, authority }; },
      lookup: async () => { calls += 1; return { authorized: true, authority }; },
    }));
    for (const response of [
      await handlers.POST(postRequest()),
      await handlers.POST(postRequest(submission, READ_CAPABILITY)),
      await handlers.POST(postRequest(submission, REVIEW_CAPABILITY)),
      await handlers.GET(getRequest()),
      await handlers.GET(getRequest(undefined, WRITE_CAPABILITY)),
      await handlers.GET(getRequest(undefined, DECISION_CAPABILITY)),
    ]) {
      expect(response.status).toBe(401);
      expect(await response.json()).toEqual({ error: "server capability required" });
    }
    expect(calls).toBe(0);
  });

  test("all four Next capabilities must be nonblank and pairwise unequal before dependencies", async () => {
    for (const overrides of [
      { writeCapability: undefined },
      { readCapability: "   " },
      { reviewCapability: undefined },
      { decisionCapability: "" },
      { readCapability: WRITE_CAPABILITY },
      { reviewCapability: WRITE_CAPABILITY },
      { decisionCapability: WRITE_CAPABILITY },
      { reviewCapability: READ_CAPABILITY },
      { decisionCapability: READ_CAPABILITY },
      { decisionCapability: REVIEW_CAPABILITY },
    ] satisfies Partial<OutreachReviewAuthorityRouteDependencies>[]) {
      let calls = 0;
      const handlers = createOutreachReviewAuthorityHandlers(dependencies({
        ...overrides,
        create: async () => { calls += 1; return { created: true, authority }; },
        lookup: async () => { calls += 1; return { authorized: true, authority }; },
      }));
      for (const response of [
        await handlers.POST(postRequest(submission, WRITE_CAPABILITY)),
        await handlers.GET(getRequest(undefined, READ_CAPABILITY)),
      ]) {
        expect(response.status).toBe(503);
        expect(await response.json()).toEqual({ error: "outreach authority is not configured" });
      }
      expect(calls).toBe(0);
    }
  });

  test("rejects malformed dependency successes instead of publishing invented authority state", async () => {
    for (const [method, handlers] of [
      ["POST", createOutreachReviewAuthorityHandlers(dependencies({ create: async () => ({ created: true } as never) }))],
      ["GET", createOutreachReviewAuthorityHandlers(dependencies({ lookup: async () => ({ authorized: true } as never) }))],
      ["GET", createOutreachReviewAuthorityHandlers(dependencies({ lookup: async () => ({ authorized: "yes" } as never) }))],
      ["POST", createOutreachReviewAuthorityHandlers(dependencies({ create: async () => ({ created: true, authority, extra: true } as never) }))],
      ["GET", createOutreachReviewAuthorityHandlers(dependencies({ lookup: async () => ({ authorized: false, state: "absent" } as never) }))],
    ] as const) {
      const response = method === "POST"
        ? await handlers.POST(postRequest(submission, WRITE_CAPABILITY))
        : await handlers.GET(getRequest(undefined, READ_CAPABILITY));
      expect(response.status).toBe(500);
      expect(await response.json()).toEqual({ error: "outreach review authority request failed" });
    }
  });

  test("maps stable malformed and conflict failures while sanitizing arbitrary dependency errors", async () => {
    for (const [code, status, body] of [
      ["OUTREACH_REVIEW_AUTHORITY_INVALID", 400, { error: "invalid outreach review authority request" }],
      ["OUTREACH_REVIEW_AUTHORITY_CONFLICT", 409, { error: "outreach review authority conflict" }],
      ["OUTREACH_REVIEW_AUTHORITY_CORRUPT", 409, { error: "outreach review authority state is corrupt" }],
    ] as const) {
      const handlers = createOutreachReviewAuthorityHandlers(dependencies({
        create: async () => { throw new Error(`[CONVEX] ${code}`); },
        lookup: async () => { throw new Error(`[CONVEX] ${code}`); },
      }));
      for (const response of [
        await handlers.POST(postRequest(submission, WRITE_CAPABILITY)),
        await handlers.GET(getRequest(undefined, READ_CAPABILITY)),
      ]) {
        expect(response.status).toBe(status);
        expect(await response.json()).toEqual(body);
      }
    }

    const secret = "dependency-secret-must-not-leak";
    const leaking = createOutreachReviewAuthorityHandlers(dependencies({
      create: async () => { throw new Error(secret); },
      lookup: async () => { throw new Error(secret); },
    }));
    for (const response of [
      await leaking.POST(postRequest(submission, WRITE_CAPABILITY)),
      await leaking.GET(getRequest(undefined, READ_CAPABILITY)),
    ]) {
      const text = await response.text();
      expect(response.status).toBe(500);
      expect(JSON.parse(text)).toEqual({ error: "outreach review authority request failed" });
      expect(text).not.toContain(secret);
    }
  });
});
