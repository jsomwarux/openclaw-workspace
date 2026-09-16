import { NextResponse } from "next/server";
import { assertDistinctServerCapability, OutreachAuthError } from "./outreach-auth";
import {
  OutreachReviewContractError,
  validateOutreachReviewKey,
  validateOutreachReviewSubmission,
  type OutreachReviewSubmission,
} from "./outreach-review";
import { createSuppressionAdmissionAttestation } from "./outreach-suppression-attestation";
import { ProtectedGitBindingMismatchError, ProtectedGitDependencyError } from "./outreach-protected-git";

type AdmissionResult = { taskId: string; created: boolean; reviewCycle: 1 | 2; snapshotSha256: string };
type ReviewState = {
  candidateId: string;
  cohortId: string;
  reviewCount: number;
  remainingCycles: number;
  latest: null | { taskId: string; draftSha256: string; snapshotSha256: string; reviewCycle: 1 | 2; decided: boolean };
};

type Dependencies = {
  serverCapability: string | undefined;
  peerCapability: string | undefined;
  admit: (input: OutreachReviewSubmission & { capability: string; suppressionAttestation?: string }) => Promise<AdmissionResult>;
  lookup: (input: { candidateId: string; cohortId: string; capability: string }) => Promise<ReviewState>;
  verifySuppressionBinding: (input: NonNullable<OutreachReviewSubmission["suppressionBinding"]>) => Promise<void>;
};

function authError(error: OutreachAuthError) {
  if (error.status === 503) return NextResponse.json({ error: "outreach authority is not configured" }, { status: 503 });
  return NextResponse.json({ error: "server capability required" }, { status: 401 });
}

function validationError(error: unknown) {
  if (error instanceof OutreachAuthError) return authError(error);
  if (error instanceof OutreachReviewContractError && error.code === "too_large") {
    return NextResponse.json({ error: "outreach review content too large" }, { status: 413 });
  }
  return NextResponse.json({ error: "invalid outreach review request" }, { status: 400 });
}

function dependencyError(error: unknown) {
  const message = error instanceof Error ? error.message : "";
  const hasCode = (code: string) => new RegExp(`(?:^|[^A-Z0-9_])${code}(?:$|[^A-Z0-9_])`).test(message);
  if (hasCode("OUTREACH_REVIEW_CYCLE_LIMIT")) {
    return NextResponse.json({ error: "outreach review cycle limit reached" }, { status: 409 });
  }
  if (hasCode("OUTREACH_REVIEW_AUTHORITY_CORRUPT")) {
    return NextResponse.json({ error: "outreach review authority state is corrupt" }, { status: 409 });
  }
  return NextResponse.json({ error: "outreach review request failed" }, { status: 500 });
}

export function createOutreachReviewHandlers(dependencies: Dependencies) {
  async function capability(req: Request) {
    return assertDistinctServerCapability(
      req.headers.get("X-Outreach-Review-Capability") ?? undefined,
      dependencies.serverCapability,
      dependencies.peerCapability,
    );
  }

  return {
    POST: async (req: Request) => {
      try {
        const serverCapability = await capability(req);
        const input = await req.json() as unknown;
        validateOutreachReviewSubmission(input);
        let suppressionAttestation: string | undefined;
        if (input.suppressionBinding) {
          try {
            await dependencies.verifySuppressionBinding(input.suppressionBinding);
            suppressionAttestation = await createSuppressionAdmissionAttestation(input, dependencies.peerCapability);
          } catch (error) {
            if (error instanceof ProtectedGitBindingMismatchError) return validationError(error);
            if (error instanceof ProtectedGitDependencyError) return dependencyError(error);
            return dependencyError(error);
          }
        }
        try {
          const result = await dependencies.admit({
            ...input,
            ...(suppressionAttestation ? { suppressionAttestation } : {}),
            capability: serverCapability,
          });
          return NextResponse.json({
            taskId: result.taskId,
            created: result.created,
            reviewCycle: result.reviewCycle,
            snapshotSha256: result.snapshotSha256,
          });
        } catch (error) {
          return dependencyError(error);
        }
      } catch (error) {
        return validationError(error);
      }
    },
    GET: async (req: Request) => {
      try {
        const serverCapability = await capability(req);
        const params = new URL(req.url).searchParams;
        const candidateId = params.get("candidateId");
        const cohortId = params.get("cohortId");
        validateOutreachReviewKey(candidateId, cohortId);
        try {
          const result = await dependencies.lookup({ candidateId, cohortId: cohortId as string, capability: serverCapability });
          return NextResponse.json(result);
        } catch (error) {
          return dependencyError(error);
        }
      } catch (error) {
        return validationError(error);
      }
    },
  };
}
