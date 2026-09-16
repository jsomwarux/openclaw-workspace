import { describe, expect, test } from "bun:test";
import {
  OutreachReviewAuthorityError,
  hashOutreachReviewAuthoritySubmission,
  resolveOutreachReviewAuthorityAdmission,
  resolveOutreachReviewAuthorityLookup,
  validateOutreachReviewAuthoritySubmission,
  type OutreachReviewAuthority,
  type OutreachReviewAuthoritySubmission,
} from "./outreach-review-authority";

const DRAFT_SHA = "a".repeat(64);
const BUNDLE_SHA = "b".repeat(64);
const REPORT_SHA = "c".repeat(64);
const COMMIT_SHA = "d".repeat(40);
const ENTROPY = "1".repeat(20) + "2".repeat(20);

function submission(overrides: Partial<OutreachReviewAuthoritySubmission> = {}): OutreachReviewAuthoritySubmission {
  return {
    candidateId: "candidate-1",
    draftSha256: DRAFT_SHA,
    authorityBundleHash: BUNDLE_SHA,
    verifierReportSha256: REPORT_SHA,
    verifierGitBinding: {
      repository: "owner/repo",
      commitSha: COMMIT_SHA,
      path: "reviews/verifier-report.json",
      blobSha256: REPORT_SHA,
    },
    builderActorId: "builder-1",
    drafterActorId: "drafter-1",
    ...overrides,
  };
}

function errorCode(run: () => unknown): string | undefined {
  try {
    run();
  } catch (error) {
    return error instanceof OutreachReviewAuthorityError ? error.code : undefined;
  }
  return undefined;
}

async function authority(
  input: OutreachReviewAuthoritySubmission = submission(),
  verifierActorId = "verifier-1",
): Promise<OutreachReviewAuthority> {
  const result = await resolveOutreachReviewAuthorityAdmission([], input, verifierActorId, 1_789_452_000_000, ENTROPY);
  if (result.operation !== "create") throw new Error("expected create");
  return result.authority;
}

describe("outreach review authority submission", () => {
  test("accepts only the exact client request shape and excludes server authority fields and prose", () => {
    expect(validateOutreachReviewAuthoritySubmission(submission())).toBe(undefined);
    for (const forbidden of [
      ["verifierActorId", "caller-verifier"],
      ["reviewId", "review_caller"],
      ["observedAt", 1_789_452_000_000],
      ["authorityRevision", "review_authority_" + "f".repeat(20)],
      ["submissionSha256", "f".repeat(64)],
      ["verifierReport", "CONFIRM"],
      ["authorized", true],
      ["sendAuthorized", true],
    ] as const) {
      expect(errorCode(() => validateOutreachReviewAuthoritySubmission({ ...submission(), [forbidden[0]]: forbidden[1] })))
        .toBe("invalid_request");
    }
    expect(errorCode(() => validateOutreachReviewAuthoritySubmission(({ ...submission(), drafterActorId: undefined })))).toBe("invalid_request");
  });

  test("requires lowercase SHA-256 digests and the existing-safe exact Git binding", () => {
    for (const overrides of [
      { draftSha256: "A".repeat(64) },
      { authorityBundleHash: "b".repeat(63) },
      { verifierReportSha256: "z".repeat(64) },
      { verifierGitBinding: { ...submission().verifierGitBinding, repository: "Owner/repo" } },
      { verifierGitBinding: { ...submission().verifierGitBinding, commitSha: "D".repeat(40) } },
      { verifierGitBinding: { ...submission().verifierGitBinding, path: "../report.json" } },
      { verifierGitBinding: { ...submission().verifierGitBinding, blobSha256: "e".repeat(64) } },
      { verifierGitBinding: { ...submission().verifierGitBinding, extra: true } },
    ] as Partial<OutreachReviewAuthoritySubmission>[]) {
      expect(errorCode(() => validateOutreachReviewAuthoritySubmission(submission(overrides)))).toBe("invalid_request");
    }
  });

  test("requires distinct bounded builder, drafter, and server-mapped verifier actors", async () => {
    expect(errorCode(() => validateOutreachReviewAuthoritySubmission(submission({ drafterActorId: "builder-1" })))).toBe("invalid_request");
    expect(errorCode(() => validateOutreachReviewAuthoritySubmission(submission({ builderActorId: "x".repeat(129) })))).toBe("invalid_request");
    for (const verifierActorId of ["builder-1", "drafter-1", "", "Verifier-1"]) {
      expect(await (async () => {
        try {
          await resolveOutreachReviewAuthorityAdmission([], submission(), verifierActorId, 1_789_452_000_000, ENTROPY);
        } catch (error) {
          return error instanceof OutreachReviewAuthorityError ? error.code : undefined;
        }
      })()).toBe("invalid_request");
    }
  });

  test("hashes only the canonical client submission and binds every submitted field", async () => {
    const original = submission();
    const baseline = await hashOutreachReviewAuthoritySubmission(original);
    expect(/^[a-f0-9]{64}$/.test(baseline)).toBe(true);
    const variants = [
      submission({ candidateId: "candidate-2" }),
      submission({ draftSha256: "3".repeat(64) }),
      submission({ authorityBundleHash: "4".repeat(64) }),
      submission({ verifierReportSha256: "5".repeat(64), verifierGitBinding: { ...original.verifierGitBinding, blobSha256: "5".repeat(64) } }),
      submission({ verifierGitBinding: { ...original.verifierGitBinding, path: "reviews/other.json" } }),
      submission({ builderActorId: "builder-2" }),
      submission({ drafterActorId: "drafter-2" }),
    ];
    for (const variant of variants) expect(await hashOutreachReviewAuthoritySubmission(variant)).not.toBe(baseline);
  });
});

describe("server-owned authority resolution", () => {
  test("maps the verifier outside the request and generates formatted immutable server fields", async () => {
    const result = await resolveOutreachReviewAuthorityAdmission([], submission(), "verifier-1", 1_789_452_000_000, ENTROPY);
    expect(result.operation).toBe("create");
    if (result.operation !== "create") throw new Error("expected create");
    expect(result.authority).toEqual({
      ...submission(),
      submissionSha256: await hashOutreachReviewAuthoritySubmission(submission()),
      verifierActorId: "verifier-1",
      reviewId: "review_" + "1".repeat(20),
      observedAt: 1_789_452_000_000,
      authorityRevision: "review_authority_" + "2".repeat(20),
    });
    expect(Object.keys(result.authority).sort()).toEqual([
      "authorityBundleHash", "authorityRevision", "builderActorId", "candidateId", "draftSha256",
      "drafterActorId", "observedAt", "reviewId", "submissionSha256", "verifierActorId",
      "verifierGitBinding", "verifierReportSha256",
    ].sort());
  });

  test("returns an exact retry byte-for-byte unchanged", async () => {
    const original = await authority();
    const result = await resolveOutreachReviewAuthorityAdmission(
      [original], submission(), "verifier-1", 1_999_999_999_999, "3".repeat(40),
    );
    expect(result).toEqual({ operation: "existing", authority: original });
    expect(result.authority).toBe(original);
  });

  test("rejects conflicting same-key submissions and verifier mappings", async () => {
    const original = await authority();
    const changedBinding = submission({ verifierGitBinding: { ...submission().verifierGitBinding, path: "reviews/changed.json" } });
    for (const [input, verifier] of [[changedBinding, "verifier-1"], [submission(), "verifier-2"]] as const) {
      try {
        await resolveOutreachReviewAuthorityAdmission([original], input, verifier, 1_789_452_000_001, "3".repeat(40));
        throw new Error("expected conflict");
      } catch (error) {
        expect(error instanceof OutreachReviewAuthorityError).toBe(true);
        expect((error as OutreachReviewAuthorityError).code).toBe("conflict");
      }
    }
  });

  test("fails closed for duplicate, malformed, and wrong-key stored rows", async () => {
    const original = await authority();
    const corrupt = { ...original, authorityRevision: "caller-revision" };
    const wrongKey = await authority(submission({ candidateId: "candidate-2" }));
    for (const rows of [[original, original], [corrupt], [wrongKey]]) {
      try {
        await resolveOutreachReviewAuthorityAdmission(rows as OutreachReviewAuthority[], submission(), "verifier-1", 1_789_452_000_001, "3".repeat(40));
        throw new Error("expected corrupt authority");
      } catch (error) {
        expect(error instanceof OutreachReviewAuthorityError).toBe(true);
        expect((error as OutreachReviewAuthorityError).code).toBe("corrupt_authority");
      }
    }
  });

  test("supports exact lookup while representing an absent exact binding as null", async () => {
    const original = await authority();
    const lookup = {
      candidateId: original.candidateId,
      draftSha256: original.draftSha256,
      authorityBundleHash: original.authorityBundleHash,
      verifierReportSha256: original.verifierReportSha256,
      verifierGitBinding: original.verifierGitBinding,
    };
    expect(await resolveOutreachReviewAuthorityLookup([original], lookup)).toBe(original);
    expect(await resolveOutreachReviewAuthorityLookup([], lookup)).toBe(null);
    expect(await resolveOutreachReviewAuthorityLookup([original], {
      ...lookup,
      verifierGitBinding: { ...lookup.verifierGitBinding, path: "reviews/changed.json" },
    })).toBe(null);
    for (const rows of [[original, original], [{ ...original, reviewId: "bad" }]]) {
      try {
        await resolveOutreachReviewAuthorityLookup(rows as OutreachReviewAuthority[], lookup);
        throw new Error("expected corrupt authority");
      } catch (error) {
        expect(error instanceof OutreachReviewAuthorityError).toBe(true);
        expect((error as OutreachReviewAuthorityError).code).toBe("corrupt_authority");
      }
    }
  });
});
