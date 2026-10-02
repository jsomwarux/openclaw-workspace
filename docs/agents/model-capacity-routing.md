# Shared Codex / Claude Capacity Routing

## Objective

Treat Codex and Claude as one constrained capacity portfolio. Preserve enough allowance for JT conversations, failures, and scheduled work; never exhaust one service while the other has suitable headroom.

## Source of truth

- Current snapshots: `memory/capacity/current.json`
- Append-only observations: `memory/capacity/usage-ledger.jsonl`
- Append-only task execution events: `memory/capacity/execution-ledger.jsonl`
- Controller: `python3 scripts/model_capacity_controller.py`
- Codex telemetry: current OpenClaw `session_status`, recorded before and after substantive work.
- Claude telemetry: JT's current Claude Code `/status`, recorded before the first Claude lane each day and after a large lane. Eve cannot infer or remotely fetch it.

Snapshots older than 24 hours are stale. Large lanes require fresh, known snapshots for both services. Unknown or stale capacity fails closed; it is never treated as available.

## Thresholds

- **Above 60%:** route by best task fit.
- **40–60%:** shift flexible heavy work toward the service with greater projected headroom.
- **25–40%:** critical work only; remove duplicate review loops.
- **Below 25%:** protected reserve; stop discretionary work.
- **Below 15%:** hard stop except urgent recovery that will remain at or above 15%.

Until observed deltas support better estimates, use 3 percentage points for a small lane, 8 for medium, and 15 for large. Record actual before/after deltas and recalibrate weekly.

## Ownership

- **Codex/Eve:** JT conversation, architecture, prioritization, state, final synthesis, sensitive operations, compact verification.
- **Buyer copy:** Codex drafts already-researched review batches; deterministic scripts validate them. Claude is eligible only through JT's manual Claude Code handoff when fresh telemetry and a documented speed advantage justify the extra handoff.
- **Claude Code:** every n8n implementation, multi-file implementation, repetitive debugging, adversarial review, and bounded research batches. Claude Code is manual-handoff only through one paste-ready prompt that JT runs.
- **Deterministic scripts:** CSV integrity, normalization, dedupe, MX, suppression, hashing, formatting, and report assembly. Mechanical work must not consume a model lane.
- **Flexible research:** run deterministic checks first, split non-overlapping rows according to projected headroom, use one evidence schema, and recheck only ambiguous/high-risk claims. Do not make both models research the same rows unless the first output fails acceptance.

One builder plus one bounded acceptance check is the default. Stop after two repair cycles and revisit the architecture.

## Preflight

Tracked preflight is mandatory when the task kind is `buyer_copy`, the batch contains more than 10 items, or estimated work exceeds 10 minutes. Capacity preflight also remains required for work using more than two model-heavy phases or creating a Claude Code handoff:

```bash
python3 scripts/model_capacity_controller.py status
python3 scripts/model_capacity_controller.py preflight \
  --task-id first-25-m1 \
  --task "bounded task name" \
  --task-kind buyer_copy \
  --size medium \
  --estimated-burn 8 \
  --estimated-minutes 12 \
  --batch-items 25
```

Exit `0` routes the work or selects deterministic tooling. A tracked route returns an `attempt_id`; preserve it through completion. Exit `2` blocks the lane and logs the blocked attempt. A blocked lane must be split, deferred, or rerouted within the task-ownership boundary; n8n builds never reroute away from Claude Code.

## Buyer-copy delivery contract

For already-researched buyer-copy batches, keep the critical path to: governed evidence → tracked preflight → one Codex drafting pass → one deterministic validator → required upload → immediate delivery to JT.

Record completion immediately after delivery:

```bash
python3 scripts/model_capacity_controller.py complete \
  --task-id first-25-m1 \
  --attempt-id <preflight-attempt-id> \
  --tool-calls 8 \
  --provider-delta unknown \
  --avoidable-delay-minutes 0 \
  --delivered
```

The controller computes elapsed time. Delivered buyer copy is `on_target` at 12 minutes or less, `warning` above 12 through 15 minutes, and `breach` above 15 minutes. Stopped or undelivered buyer copy is `missed_delivery`. Proof logging, durable-state synchronization, Mission Control updates, and unrelated repairs happen after delivery unless they affect correctness, authority, privacy, secret exposure, or whether JT can open the artifact.

## Weekly recalibration

```bash
python3 scripts/model_capacity_controller.py summary --days 7
```

Review completions, delivery counts, median elapsed minutes, buyer-copy SLA counts, median tool calls, and total avoidable delay. The summary is evidence only; it never rewrites burn estimates or routing policy automatically.

## Artifact policy

Local canonical artifacts are the default. Upload to Drive only when the artifact is client-facing/shareable, must be used outside the repository, is required by an explicit downstream contract such as job applications, or JT explicitly asks. Internal audits, runbooks, CSVs, proof files, state, logs, and duplicate reports stay local.

## Scheduled work

No cron or provider configuration changes are implied by this policy. New or separately authorized edits to model-dependent automations must add a deterministic capacity preflight and skip noncritical work before the protected reserve. Recovery after a quota incident requires the first natural post-reset run to succeed; do not blind-rerun or silently change providers.
