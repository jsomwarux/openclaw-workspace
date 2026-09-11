# Checkpoint 1B Readiness — 2026-09-10

Status: read-only implementation brief. No code, schema, schedule, deployment, or production data change is authorized by this document.

## Decision

Build a thin `jt-ops` → Mission Control adapter after JT confirms P1 sent. Do not implement the full v3.7 contract list as new schemas. Existing owner surfaces already cover most of it.

## Evidence inspected

- `jsomwarux/jt-ops` `main`: `pipelines.json`; `schemas/run_receipt.schema.json`; `schemas/outcome.schema.json`; `schemas/proof.schema.json`; `schemas/signal.schema.json`; `runs/spine-heartbeat/2026-09-10.json`.
- Local Mission Control: `convex/schema.ts`; `convex/tasks.ts`; `lib/mission-control/types.ts`; `lib/mission-control/adapters.ts`; `lib/mission-control/task-admission.ts`; `app/api/tasks/route.ts`; `CLAUDE.md` Today contract.

## Reuse, do not rebuild

### `jt-ops` remains authoritative for

- Pipeline registry and cadence.
- Run receipts, including empty/degraded/failed state.
- Proof records and permission state.
- Deferred signals and wake conditions.
- Outcome records.

### Mission Control remains authoritative for

- Human task status and assignee.
- First action, why it matters, and done state.
- Due/review dates, waiting-on state, effort, lane, evidence links, dedupe key, and ranking inputs.
- Human decision queue and rendered Today state.

## Minimum missing bridge

1. **Stateless sync command**: translate one validated `jt-ops` artifact or receipt into the existing Mission Control task fields. Reuse `sourceSystem`, `sourceHash`, `evidenceLinks`, `dedupeKey`, `verdict`, `verifierConfirmed`, and `verifiedAt`. Reuse the existing `POST /api/tasks` keyed-upsert path; do not add another manifest or upsert mechanism.
2. **Append-only feedback entry**: card/task ID, lane, artifact ID, verbatim JT note, and timestamp. Raw feedback cannot modify a canonical skill or lessons file. Add this only after the field-level diff confirms no existing feedback owner covers it.
3. **Payload-hash invalidation**: if the approved external-action payload changes, its task returns to pending review. Add a dedicated field only if `sourceHash` cannot safely represent the exact actionable payload; document that distinction before implementation.
4. **Outcome write-through**: confirmed external results append to the existing `jt-ops` `outcome` schema. Mission Control keeps only its task status and an evidence link to that outcome; do not create an outcome-pointer schema or second outcome ledger.
5. **Approval state stays in Mission Control task truth** until a real persistent decision entity exists. Do not invent a `decision_id` or duplicate decision/time/expiry in `jt-ops`. For v1, a changed payload hash returns the task to `todo`; JT's actual external action is captured through the existing outcome ledger after confirmation.

## Weekly heartbeat

The existing `spine-heartbeat` pipeline is already registered daily and already writes receipts. Do not create a second health pipeline.

After explicit JT approval for a recurring schedule, add one weekly consumer that reads the latest heartbeat and lane receipts and emits exactly one of:

- a no-decision health receipt/card confirming the system ran and naming the next check; or
- a decision card for a real failure, stale consumer, or missing output.

The weekly card must separate worker execution, artifact validity, delivery, human decision, external action, and commercial outcome. Absence of decision cards is not accepted as evidence that the system ran.

## Build sequence after `P1 sent`

1. Create an isolated worktree from current `jt-ops` `origin/main`; do not use the dirty shared Mission Control checkout.
2. Diff existing schemas and code before adding fields.
3. Preserve the existing keyed-upsert tests. Write only missing failing tests for payload-hash invalidation, feedback append, outcome write-through to the existing schema, and weekly no-decision heartbeat.
4. Implement the smallest stateless adapter and test double for Mission Control; no production writes during tests.
5. Run full `jt-ops` tests and Mission Control adapter tests in their intended runtimes.
6. Produce a review artifact and PR. Do not merge or deploy.
7. Send the exact diff and artifacts to a fresh-context verifier that did not build them. Report its verdict verbatim, including failures.
8. Present JT with one approval card for merge/deployment/schedule decisions.

## Explicit non-goals

- No second task board.
- No copy of Mission Control task truth in `jt-ops`.
- No copy of `jt-ops` proof/run truth in Convex.
- No new outreach infrastructure.
- No automatic send, post, application, RSVP, purchase, deployment, merge, or schedule activation.
- No daily heartbeat card; the human-facing heartbeat is weekly.

## Start gate

Implementation starts only after JT confirms that P1 reached the buyer-facing mailbox. Read-only preparation may happen before that gate; code work may not.
