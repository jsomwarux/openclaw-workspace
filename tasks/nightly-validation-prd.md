# Nightly Validation Controller PRD

## Product overview

Project title Nightly Validation Controller

Primary user JT Somwaru

Core job Select at most one eligible portfolio lane and up to three bounded validations, then keep weak results out of JT's task list.

## Goals

- Produce one deterministic nightly decision artifact by 7 30 AM when eligible work exists.
- Create no Mission Control task for continue, archive, blocked, or no-qualified-work outcomes.
- Deduplicate records by stable candidate ID and source hash.

## Non-goals

- No Grok integration.
- No builds, external messages, purchases, deployments, applications, client-system changes, or automatic public content.
- No autonomous creation of new recurring jobs beyond the approved controller cron.

## User stories

- US-1 As JT, I want only verified promoted opportunities in Mission Control so that agent activity does not create task churn.
- US-2 As Eve, I want a deterministic queue and state contract so that nightly work is reproducible and auditable.
- US-3 As an operator, I want explicit no-work behavior so that the controller does not invent tasks to stay busy.

## Functional requirements

- FR-1 Read JSONL candidates from `memory/agent-portfolio/validation-queue.jsonl` and validate schema.
- FR-2 Select only pending candidates whose `not_before` has passed and whose source hash has not been processed.
- FR-3 Rank by score, select one lane, and cap the run at three candidates.
- FR-4 Return `NO_QUALIFIED_VALIDATION` when nothing qualifies.
- FR-5 Write run artifacts under `memory/agent-portfolio/runs/YYYY-MM-DD/` without mutating external systems.
- FR-6 Record the last completed run, processed hashes, artifacts, failures, and next run in `memory/job-state/nightly-validation.md`.
- FR-7 Emit a machine-readable promotion file containing only fresh verifier-confirmed `promote` results.
- FR-8 Provide a consumer mode that creates or updates at most one deduplicated Mission Control task from the promotion file.
- FR-9 Fail loud on invalid JSON, stale source, missing verifier confirmation, or unavailable Mission Control.
- FR-10 Support `--dry-run`, `--json`, and an explicit consume mode.

## Data and privacy

Inputs contain public research metadata and local artifact references only. No credentials, client-private data, or private conversation history belong in the queue.

## Technical considerations

Use Python and the standard library where possible. Keep selection, validation, state transitions, and Mission Control payload construction deterministic. The LLM cron may perform research, but the controller script owns admission and routing.

## Failure modes

- Malformed JSONL stops the run with line-level error evidence.
- Missing or stale evidence prevents promotion.
- Duplicate source hashes are skipped.
- Mission Control outage preserves the promotion artifact for retry and reports the failure.
- Partial research never becomes a promoted action.

## Build phases

1. Write failing tests for schema, selection, dedupe, no-work behavior, promotion gating, and task payload.
2. Implement the minimal deterministic controller.
3. Add state and artifact fixtures.
4. Verify tests, dry run, invalid-input behavior, and idempotent consumption.
5. Install the approved 11 15 PM America New York cron only after fresh review.

## Definition of done

- All focused tests pass.
- A clean empty queue returns `NO_QUALIFIED_VALIDATION` and creates no task.
- A mixed fixture selects one lane and at most three candidates.
- Only a fresh verifier-confirmed promote record can produce one task payload.
- A second consume run does not create a duplicate task.
- Current cron volume guard passes after installation.

## Do not touch

- Grok
- OpenClaw auth or model configuration
- Client or production systems
- Existing historical proof and JSONL logs
