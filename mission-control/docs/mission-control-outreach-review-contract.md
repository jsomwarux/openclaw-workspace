# Mission Control Outreach Review Owner Contract

This is the integration contract for `jt-ops`. It is inactive until Mission Control is deployed with distinct configured review and decision capabilities. Capability values are never stored in payloads, artifacts, or logs.

## Admit or retry an immutable review snapshot

`POST /api/tasks/outreach-review`

Header: `X-Outreach-Review-Capability`

The JSON body has exactly these fields:

```ts
type GitBinding = {
  repository: string;  // canonical lowercase owner/repo
  commitSha: string;   // 40 lowercase hex
  path: string;        // safe ASCII repository-relative path
  blobSha256: string;  // 64 lowercase hex
};

type OutreachReviewSubmission = {
  candidateId: string;
  cohortId: string;
  draftSha256: string;
  subject: string;             // 1..200 UTF-16 code units
  body: string;                // 1..20,000 UTF-16 code units
  verifierReport: string;      // verbatim, 1..20,000 UTF-16 code units
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

Success is exactly:

```json
{"taskId":"...","created":true,"reviewCycle":1,"snapshotSha256":"..."}
```

An exact retry returns the same `taskId`, cycle, and snapshot hash with `created:false`. Mission Control assigns cycles atomically per `candidateId + cohortId`. A third distinct snapshot returns HTTP 409. The caller cannot provide task display metadata, cycle, admission metadata, or snapshot hash.

The snapshot hash is SHA-256 over UTF-8 deterministic canonical JSON with recursive key sorting:

```json
{"domain":"mission-control/outreach-review-snapshot","snapshot":{...exact submission...},"version":1}
```

It proves content identity only. It is not semantic approval.

## Read the authoritative review budget

`GET /api/tasks/outreach-review?candidateId=...&cohortId=...`

Header: `X-Outreach-Review-Capability`

Success is exactly:

```json
{
  "candidateId":"...",
  "cohortId":"...",
  "reviewCount":1,
  "remainingCycles":1,
  "latest":{
    "taskId":"...",
    "draftSha256":"...",
    "snapshotSha256":"...",
    "reviewCycle":1,
    "decided":false
  }
}
```

`latest` is `null` when absent. No review prose is returned. Malformed authoritative state returns HTTP 409 and never resets the budget.

## Record JT's first immutable decision

`POST /api/tasks/outreach-decision`

This browser/UI route requires the trusted Tailscale JT identity. It does not accept a capability in the body. The JSON body is exactly:

```json
{
  "taskId":"...",
  "candidateId":"...",
  "draftSha256":"...",
  "snapshotSha256":"...",
  "decision":"approve"
}
```

`decision` is `approve` or `reject`. The first decision appends `decidedBy:"jt"` and server time, then closes the task. An identical retry is idempotent. A reversal or identity mismatch returns HTTP 409 and requires a new versioned review task.

## Prepare-send decision lookup

`GET /api/tasks/outreach-decision?candidateId=...&draftSha256=...&snapshotSha256=...`

Header: `X-Outreach-Decision-Capability`

The state is one of `pending`, `approved`, `rejected`, or `absent`. Only an exact, non-archived, server-admitted snapshot can return a state other than `absent`. `approved` is advisory evidence of JT's recorded decision; `jt-ops` must still perform its current live suppression/channel and artifact-hash checks before preparing a send. Missing, rejected, mismatched, corrupt, or archived state fails closed.

## Ownership and immutability

The existing Mission Control task is the only store. Generic task create, POST/PATCH, dedupe upsert, status update, pipeline update, delete, auto-archive, and backfill paths cannot create or mutate an outreach snapshot or decision. The review UI renders the persisted immutable subject, body, verbatim verifier report, actor IDs, cycle, snapshot hash, and all five Git bindings—not caller-controlled generic task text.
