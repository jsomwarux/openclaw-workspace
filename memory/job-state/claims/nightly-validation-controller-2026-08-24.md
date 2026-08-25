# Nightly Validation Controller Builder Claim — 2026-08-24

Status: AWAITING_FRESH_VERIFIER

Claim: The controller now enforces explicit `admit`, `reconcile`, and `consume` phases. Admission selects one lane and at most three candidates without marking hashes processed. Reconciliation requires one complete full-schema result per selected candidate, validates fresh verifier confirmation and evidence integrity, then emits at most one promotion and marks hashes processed. Consumption accepts only an integrity-checked controller promotion artifact, revalidates every gate, and POSTs the full camelCase admission payload to `http://localhost:3000/api/tasks`, whose `dedupeKey` contract performs upsert.

Canonical artifacts: each timestamped run directory contains exactly `admission.json` as the admission contract. Successful reconciliation appends a timestamped `promotions-HHMMSSffffff.json` envelope in that same directory. Mission Control parsers should consume the promotion envelope, not infer a fixed `promotions.json` filename.

Required promotion gates: `verdict=promote`, `verifierConfirmed=true`, fresh `verifiedAt`, score at least 30/40, `evidenceScore>=4`, `distributionScore>=3`, no `fatalConstraint`, current evidence timestamp, matching evidence SHA-256, and evidence paths confined to approved workspace public/local artifact roots.

Failure behavior: invalid, incomplete, stale, tampered, or unavailable-Mission-Control paths exit nonzero, append failure state, do not create a receipt, and preserve the promotion artifact for retry.

Excluded by scope: cron installation or edits, Grok, auth/model configuration, and live Mission Control test writes.

TDD evidence:

- RED: six missing two-phase/gating functions plus two obsolete permissive behavior failures.
- GREEN: replacement contract passed 11 tests.
- RED: post-reconciliation promotion mutation was accepted (`ControllerError not raised`).
- GREEN: artifact hash verification added; final suite `Ran 16 tests in 0.543s`, `OK`.
- RED privacy/type cycle: `score="34"` raised raw `TypeError`; five other wrong types, extra fields, and private-marked evidence were accepted.
- GREEN privacy/type cycle: exact schemas, strict types/allowed values, dedicated public evidence root, secret/private-marker scan, and deterministic field-order diagnostics added; final suite `Ran 19 tests in 0.548s`, `OK`.

CLI matrix evidence:

- Admission selected the `workflow` lane and exactly three candidates; `processed_hashes_json` remained `[]`.
- Reconciliation emitted exactly one promotion; only then were the three source hashes recorded processed.
- Dry consume returned `TASK_PAYLOAD_READY` with camelCase admission and verifier fields.
- Consume against closed local port exited 2, recorded `Mission Control unavailable`, preserved the promotion, and created no receipt.
- Bare invocation exited 2 because `--phase` is mandatory.
- Timestamped admission and promotion files both remained in the isolated run directory.
- Malformed-type CLI reconciliation (`score="34"`) exited 2 with JSON `invalid score: number required`, appended failure state, preserved `admission.json`, and left processed hashes empty.

Fresh verifier must inspect this claim, implementation notes, focused tests, and CLI behavior before cron installation or global completion reporting.
