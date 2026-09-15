# Outreach Review Snapshot Contract Design

**Status:** Approved for local implementation on 2026-09-15. No deployment, environment configuration, push, or activation is authorized.

## Goal

Make the existing Mission Control task the single immutable record of exactly what JT reviewed, while Mission Control atomically owns the two-cycle review budget and the first approve/reject decision.

## Chosen architecture

Extend the existing embedded `tasks.outreachReview` object. Do not add a table, ledger, or second store. The dedicated outreach-review route accepts one typed decision-context payload. The Convex mutation validates and canonicalizes it, computes a versioned domain-separated SHA-256 snapshot hash, assigns cycle 1 or 2 atomically, derives all displayed task fields, and stamps the server marker. Generic task routes can neither create nor mutate this object.

The client cannot provide task title, description, status, assignee, priority, dedupe key, review cycle, snapshot hash, admission actor, or admission time. This prevents caller-controlled task metadata from diverging from the immutable review payload.

## Canonical request

`POST /api/tasks/outreach-review` requires `X-Outreach-Review-Capability` and accepts exactly:

```ts
type GitBinding = {
  repository: string;
  commitSha: string;     // 40 lowercase hexadecimal characters
  path: string;          // nonblank repository-relative path
  blobSha256: string;    // 64 lowercase hexadecimal characters
};

type OutreachReviewSubmission = {
  candidateId: string;
  cohortId: string;
  draftSha256: string;
  subject: string;
  body: string;
  verifierReport: string;
  reviewAuthorityId: string;
  verifierActorId: string;
  gitBindings: {
    evidence: GitBinding;
    policy: GitBinding;
    gate: GitBinding;
    draft: GitBinding;
    verifier: GitBinding;
  };
};
```

Subject is required and capped at 200 UTF-16 code units. Body and verbatim verifier report are required and each capped at 20,000 UTF-16 code units before hashing or storage. Oversize content returns 413. Unknown or server-owned fields fail closed.

`candidateId`, `cohortId`, `reviewAuthorityId`, and `verifierActorId` are canonical lowercase opaque IDs matching `[a-z0-9][a-z0-9._:-]{0,127}`. Whitespace, uppercase, Unicode, and normalization aliases are rejected rather than normalized. A repository is the lowercase canonical `owner/repo` identifier. A binding path is an ASCII repository-relative path: no leading slash, backslash, NUL, empty segment, `.` segment, or `..` segment. Commit and content hashes are lowercase hexadecimal of their exact required length.

## Canonical hashing

`snapshotSha256` is the lowercase SHA-256 digest of UTF-8 deterministic canonical JSON:

```json
{"domain":"mission-control/outreach-review-snapshot","version":1,"snapshot":{...}}
```

Object keys are recursively sorted by JavaScript code-unit order. Arrays preserve order. Strings are UTF-8 encoded exactly as received with no Unicode normalization; lone UTF-16 surrogates are rejected. Undefined, bigint, functions, symbols, and non-finite numbers are rejected. Server metadata (`reviewCycle`, `admittedBy`, `admittedAt`) is excluded, so an exact retry has the same hash. The hash proves byte-level consistency only, not truth or authorization.

Golden vector: canonical JSON `{"domain":"mission-control/outreach-review-snapshot","snapshot":{"candidateId":"candidate-1"},"version":1}` hashes to SHA-256 `ef5e31cf315c3c5f4d83a6f6ebdbc621a85677e1b884f312f3bd96f3c4f4843e`. Tests also prove object-key order invariance, array-order sensitivity, exact UTF-8 non-ASCII behavior, and that every submitted field changes the digest.

## Atomic cycle ownership

The task table adds `cohortId` and an index on top-level `candidateId + cohortId`. Those top-level values are non-authoritative lookup projections; only an internally consistent embedded server snapshot has authority. The Convex mutation queries that index inside the same transaction.

1. Load every indexed row for the canonical candidate/cohort. Unmarked legacy/generic tasks are ignored.
2. Fully validate the complete server-marked authoritative set. Any malformed identity/hash/cycle, duplicate snapshot hash, duplicate cycle, noncontiguous cycles, or more than two records blocks both admission and count GET as corrupt authoritative state. It never reopens budget.
3. Only after the full set is valid, if exactly one row has the same snapshot hash, return its `taskId`, `reviewCycle`, and hash unchanged (`created: false`).
4. Otherwise count the valid server snapshots. If count is two, reject with the fixed cycle-limit conflict.
5. Otherwise assign `reviewCycle = count + 1`, derive the immutable task display, and insert it atomically. `latest` is always the valid highest-cycle snapshot.

Convex optimistic transaction retry makes concurrent duplicate requests idempotent and concurrent distinct requests consume cycles 1 and 2; a third distinct attempt fails. An in-memory Convex-handler harness invokes the real registered mutation handler through an optimistic fake database: both transactions read the same version, one commits, the second detects its stale read set and reruns before commit. It asserts final task counts for duplicate, distinct, and third-attempt races.

## Stored object and task display

The embedded snapshot stores every submission field plus `snapshotSha256`, `reviewCycle`, `admittedBy: "server"`, and `admittedAt`. The mutation derives:

- title from cohort, candidate, and cycle;
- description as a bounded server-derived summary containing cohort, candidate, cycle, and snapshot hash only;
- status `todo`, assignee `jt`, priority `high`;
- a server-derived dedupe key containing cohort, candidate, and snapshot hash.

The full subject, body, verifier report, actors, and Git bindings exist once in `outreachReview`. The UI displays only that persisted embedded snapshot. It never reconstructs review content from generic task fields, description, or caller payloads.

## API responses

Successful POST response is exactly:

```json
{"taskId":"...","created":true,"reviewCycle":1,"snapshotSha256":"..."}
```

`GET /api/tasks/outreach-review?candidateId=...&cohortId=...` requires the review capability and returns exactly the owner count/state:

```json
{
  "candidateId":"...",
  "cohortId":"...",
  "reviewCount":1,
  "remainingCycles":1,
  "latest":{"taskId":"...","draftSha256":"...","snapshotSha256":"...","reviewCycle":1,"decided":false}
}
```

`latest` is `null` when absent and otherwise the highest cycle. It never returns subject, body, verifier report, or capabilities. Corrupt authoritative state returns a fixed 409 response.

## Decision binding

Decision POST requires `taskId + candidateId + draftSha256 + snapshotSha256 + decision`. For a first decision, the specialized mutation authorizes only a server-admitted `todo` snapshot whose complete identity matches; it atomically appends the immutable decision and closes the task as `done`. An exact same-value retry is checked before the active-status gate and returns the original decision even after closure; a reversal fails. Decision GET requires the decision capability and the same candidate/draft/snapshot triple. Its state union is `pending | approved | rejected | absent`: pending is an active exact snapshot without a decision; approved/rejected include `taskId` and the exact decision (candidate/draft/snapshot, value, `decidedBy: "jt"`, `decidedAt`); absent contains neither task nor decision and covers archived, missing, or mismatched records. A done task with its valid persisted decision remains approved/rejected.

## Security and errors

Review admission and JT decisions keep separate nonblank, unequal raw opaque capabilities. For comparison, each UTF-8 capability is imported as a nonextractable Web Crypto HMAC-SHA-256 key; the left key signs the fixed UTF-8 domain string `mission-control/outreach-capability/v1`, and `subtle.verify` checks that fixed 32-byte authenticator with the right key. No signature encoding crosses an API boundary. Missing/blank pairs return 503, equal configured pairs return 503, wrong/swapped caller values return 401, and values are never logged or returned. Review GET/POST require only the review capability; decision GET/POST require only the decision capability, and decision POST additionally requires the configured trusted Tailscale JT identity. Every public Convex outreach mutation and query independently accepts and validates the appropriate capability against both protected Convex environment values before any database read or write. Direct Convex calls without, with wrong, or with swapped authority fail closed. Tailscale identity remains the HTTP ingress identity proof for decision POST.

Routes may emit only this public error vocabulary; downstream/Convex exception text never crosses the route:

| Condition | Status | Exact JSON |
|---|---:|---|
| malformed/unknown/server-owned request field | 400 | `{"error":"invalid outreach review request"}` or `{"error":"invalid outreach decision request"}` |
| body/report/subject exceeds cap | 413 | `{"error":"outreach review content too large"}` |
| missing capability or wrong/swapped capability | 401 | `{"error":"server capability required"}` |
| missing Tailscale JT identity | 401 | `{"error":"JT identity required"}` |
| mismatched Tailscale identity | 403 | `{"error":"JT identity forbidden"}` |
| missing/blank/equal capability config or missing JT config | 503 | `{"error":"outreach authority is not configured"}` |
| decision task missing | 404 | `{"error":"outreach review not found"}` |
| cycle limit | 409 | `{"error":"outreach review cycle limit reached"}` |
| corrupt authoritative set | 409 | `{"error":"outreach review authority state is corrupt"}` |
| immutable reversal/identity conflict | 409 | `{"error":"outreach decision conflict"}` |
| unknown dependency failure | 500 | `{"error":"outreach review request failed"}` or `{"error":"outreach decision request failed"}` |

## Acceptance boundaries

- dropped/unknown/server-owned fields fail before mutation;
- altered display fields cannot be submitted or patched;
- caller cannot set/reset/decrement cycle;
- exact retries are idempotent;
- two distinct snapshots consume the two cycles; a concurrent third fails;
- malformed/oversized content fails before hashing/storage;
- generic routes cannot forge or mutate the snapshot;
- decision identity includes the exact snapshot hash;
- GET/UI read the same persisted snapshot;
- existing create-only task behavior remains unchanged.
- update, status move, archive, remove/delete, pipeline-stage update, dedupe upsert, auto-archive, client backfill, and every bulk task mutation reject or skip server snapshots and legacy outreach decisions.
- direct public Convex review/decision mutation/query calls with missing, wrong, or swapped capabilities perform zero reads and zero writes.
