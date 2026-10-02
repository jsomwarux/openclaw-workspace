# Routing V2 Design

**Status:** Approved by JT on 2026-10-02 via `APPROVE ROUTING V2`.

## Objective

Extend the existing Codex/Claude capacity controller so it protects both quota and elapsed delivery time. Already-researched buyer-copy batches should reach JT as a reviewable artifact within 12 minutes, with a 15-minute hard ceiling, while preserving existing authority, verification, and capacity rules.

## Chosen Approach

Add a thin execution-telemetry layer to the existing controller instead of creating a second routing system. The controller remains the sole deterministic authority for provider selection. A new `buyer_copy` task kind routes to Codex, while deterministic scripts handle formatting and validation. Claude is not a default drafting lane; it is eligible only through a separate, manually operated Claude Code handoff with fresh capacity telemetry and a documented speed advantage.

Alternatives rejected:

1. **Policy-only change:** fastest to write, but cannot prove that preflight or completion telemetry happened.
2. **Separate workflow orchestrator:** could enforce every phase, but duplicates routing state and adds more overhead than it removes.

## Components

### 1. Capacity controller

`scripts/model_capacity_controller.py` gains:

- `buyer_copy` as a Codex-owned task kind;
- append-only `preflight` execution events for any task with more than 10 batch items, more than 10 estimated minutes, or task kind `buyer_copy`;
- append-only `complete` execution events containing elapsed minutes, tool-call count, provider delta when known, delivery status, and avoidable-delay minutes;
- a deterministic SLA verdict for delivered buyer-copy work: `on_target` at 12 minutes or less, `warning` above 12 through 15, and `breach` above 15; undelivered buyer-copy work is `missed_delivery`, and other task kinds are `not_applicable`;
- validation that completion events bind to a recorded routed preflight by explicit attempt ID;
- a `summary` command that aggregates completed task telemetry for weekly recalibration without changing estimates automatically.

Execution events live in `memory/capacity/execution-ledger.jsonl`. Capacity snapshots remain in the existing usage ledger. The two ledgers have distinct responsibilities.

The execution ledger uses schema version `routing-execution-v1`. Every event contains `schema_version`, `event_type`, `recorded_at` as UTC ISO 8601, `task_id`, and `attempt_id`. A tracked preflight also records the task label, task kind, batch size, estimated minutes and burn, routing decision, provider, reason, and whether tracking was mandatory. A completion records the explicit attempt link, elapsed minutes, nonnegative integer tool-call count, provider burn delta or `null`, nonnegative avoidable-delay minutes, delivery status (`delivered` or `not_delivered`), and SLA verdict.

Each preflight attempt has an explicit UUID attempt ID. Tests and controlled callers may supply `--attempt-id`; otherwise the CLI generates one. Completion always requires `--attempt-id`. A blocked attempt cannot be completed. A completion is single-use: a second completion for the same attempt fails without writing. Reusing a task ID is allowed because attempts never bind by task ID alone.

JSONL writes are serialized with an adjacent lock file and written as one flushed append while the exclusive lock is held. Readers acquire a shared lock and fail loudly on partial or malformed rows.

### 2. Critical-path contract

For already-researched buyer-copy batches, the delivery path is:

1. reuse the governed evidence artifact;
2. run and log controller preflight;
3. draft once in Codex;
4. run one deterministic validator;
5. upload only when the artifact must be reviewed outside the repository;
6. deliver the review link or file immediately.

Proof logging, memory synchronization, Mission Control updates, and repairs unrelated to artifact safety or correctness occur after delivery. A blocking issue may delay delivery only when it affects copy correctness, authority, privacy, secret exposure, or the ability to open the artifact.

### 3. Policy and operator surfaces

`docs/agents/model-capacity-routing.md`, `TOOLS.md`, and the current Growth OS state describe:

- when preflight is mandatory;
- the buyer-copy routing rule;
- the 12/15-minute target;
- required completion telemetry;
- weekly review using the deterministic summary;
- the distinction between delivery-critical and post-delivery work.

No cron, provider configuration, gateway configuration, or external send is added.

## Interfaces

### Preflight

```bash
python3 scripts/model_capacity_controller.py preflight \
  --task-id first-25-m1 \
  --task "First 25 M1 packet" \
  --task-kind buyer_copy \
  --size medium \
  --estimated-burn 8 \
  --estimated-minutes 12 \
  --batch-items 25
```

The command prints stable JSON containing the existing routing fields plus `tracking_required` and, when tracked, `attempt_id`. It appends the event when preflight is mandatory. A blocked route exits 2 and is still logged. Legacy callers may ignore the additive JSON fields.

Preflight tracking is mandatory when `batch_items > 10`, `estimated_minutes > 10`, or the task kind is `buyer_copy`. Callers may add `--track` for smaller tasks. Existing preflight calls that omit the new metadata retain their prior routing and exit-code behavior and do not write execution telemetry. Completion telemetry is required only for tracked attempts.

### Completion

```bash
python3 scripts/model_capacity_controller.py complete \
  --task-id first-25-m1 \
  --attempt-id 45e8b559-7695-4bb4-9a39-bf91bb86d225 \
  --tool-calls 8 \
  --provider-delta unknown \
  --avoidable-delay-minutes 0 \
  --delivered
```

The command fails closed if no matching routed preflight exists, the attempt was blocked, or the attempt is already complete. It appends an immutable completion event and prints the SLA verdict. `--delivered` and `--not-delivered` are mutually exclusive and one is required.

Elapsed time is calculated by the controller from the tracked preflight's UTC `recorded_at` through the completion event's UTC `recorded_at`; callers do not supply it. For delivered buyer-copy attempts, completion must be recorded immediately after the artifact is successfully handed to JT. For `not_delivered` attempts, elapsed time ends when the attempt is stopped, and the SLA verdict is `missed_delivery` so failed delivery cannot disappear from weekly reporting.

### Weekly summary

```bash
python3 scripts/model_capacity_controller.py summary --days 7
```

The summary uses UTC and includes events whose `recorded_at` satisfies `cutoff <= recorded_at <= now`. It reports completion count, delivered and undelivered counts, median elapsed minutes, buyer-copy SLA counts across `on_target`, `warning`, `breach`, and `missed_delivery`, median tool calls, and total avoidable-delay minutes. Medians use Python's `statistics.median`; an empty window returns zero counts/totals and `null` medians. It does not silently rewrite routing estimates. Repeated task IDs count as distinct completed attempts.

## Error Handling

- Duplicate task IDs may have multiple attempts; explicit attempt IDs prevent retry or concurrency ambiguity.
- Missing or malformed numeric telemetry fails locally before any ledger write. Numeric values must be finite. Percentages are decimal numbers from 0 through 100; computed elapsed and supplied delay values are nonnegative; avoidable delay may not exceed computed elapsed time; tool calls and batch items are nonnegative integers.
- `provider-delta` accepts a percentage from 0 through 100 or `unknown`; unknown is stored as JSON `null` and is never inferred.
- Ledger parsing fails loudly on invalid JSON rather than skipping rows.
- Ledger writes use advisory file locking and one flushed append so concurrent CLI writers cannot interleave rows.
- Buyer-copy batches over 10 items cannot bypass preflight.
- A buyer-copy SLA breach does not invalidate the artifact; it creates evidence for the next weekly recalibration.

## Testing

Tests will prove:

- `buyer_copy` routes to Codex;
- mandatory preflight events are appended;
- non-mandatory small tasks may route without a ledger write;
- blocked preflights are recorded;
- completion without a routed preflight fails;
- explicit attempt IDs isolate retries, blocked attempts, and duplicate completion commands;
- completion computes all buyer-copy SLA outcomes and `not_applicable` for other task kinds;
- invalid telemetry does not mutate the ledger;
- concurrent writes preserve valid, complete JSONL rows;
- the seven-day summary handles inclusive boundaries, empty windows, repeated attempts, and undelivered completion correctly;
- all existing capacity tests remain green.

## Acceptance Criteria

1. Focused unit tests pass in a fresh process.
2. Python compilation passes.
3. A temporary-ledger CLI acceptance run proves preflight, completion, and summary output.
4. Existing capacity thresholds and n8n ownership behavior remain unchanged.
   Existing `record`, `status`, and legacy `preflight` arguments retain their semantics and exit codes; the new execution telemetry is additive.
5. Canonical policy names the buyer-copy route, delivery critical path, required telemetry, and 12/15-minute SLA.
6. A fresh verifier reads only the claim file and artifacts, reruns acceptance, and returns `CONFIRMED` before completion is reported.
