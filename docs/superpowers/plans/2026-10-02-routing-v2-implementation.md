# Routing V2 Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the existing capacity controller with enforceable execution telemetry and a 12/15-minute buyer-copy delivery SLA without changing current capacity thresholds or ownership rules.

**Architecture:** Keep `route_task` as the pure routing engine. Add focused execution-ledger helpers to the same narrow script, using explicit attempt IDs and advisory file locking. The CLI gains additive `complete` and `summary` commands plus optional tracking metadata on `preflight`; policy and state files document the new critical-path contract.

**Tech Stack:** Python 3 standard library (`argparse`, `fcntl`, `json`, `statistics`, `uuid`, `unittest`), Markdown policy/state files, HTML implementation notes.

**Spec:** `docs/superpowers/specs/2026-10-02-routing-v2-design.md`

---

## Pre-implementation checklist

- [x] Create and begin tracking `tasks/todo.md` before production-code edits.
- [x] Obtain fresh approval of `docs/superpowers/specs/2026-10-02-routing-v2-design.md`.
- [ ] Obtain fresh approval of both implementation-plan chunks.

## Chunk 1: Controller behavior and tests

### Task 1: Characterize compatibility and buyer-copy routing

**Files:**
- Modify: `scripts/tests/test_model_capacity_controller.py`
- Modify: `scripts/model_capacity_controller.py`

- [ ] **Step 1: Add failing characterization and buyer-copy tests**

Add tests that assert:

```python
def test_buyer_copy_routes_to_codex(self):
    result = controller.route_task(
        snapshots={"codex": snapshot("codex", 99), "claude": snapshot("claude", 99)},
        task_kind="buyer_copy",
        size="medium",
        estimated_burn=8,
        now=NOW,
    )
    self.assertEqual(result["decision"], "route")
    self.assertEqual(result["provider"], "codex")
```

Also assert that existing `mechanical`, `research`, and `n8n_build` behavior remains unchanged.

- [ ] **Step 2: Run the focused test and confirm RED**

Run:

```bash
python3 -m unittest scripts.tests.test_model_capacity_controller.RoutingTests.test_buyer_copy_routes_to_codex -v
```

Expected: failure because `buyer_copy` is not registered.

- [ ] **Step 3: Add the minimum route registration**

Add:

```python
"buyer_copy": ("codex",),
```

to `TASK_PROVIDERS` without changing other entries.

- [ ] **Step 4: Run all controller tests**

Run:

```bash
python3 -m unittest scripts.tests.test_model_capacity_controller -v
```

Expected: all existing tests plus the new route test pass.

- [ ] **Step 5: Commit the isolated route registration**

```bash
git add scripts/model_capacity_controller.py scripts/tests/test_model_capacity_controller.py
git commit -m "feat: add buyer-copy capacity route"
```

### Task 2: Add versioned, locked execution-ledger primitives

**Files:**
- Modify: `scripts/tests/test_model_capacity_controller.py`
- Modify: `scripts/model_capacity_controller.py`

- [ ] **Step 1: Add failing ledger tests**

Add `ExecutionTrackingTests` with named methods covering:

- a mandatory tracked preflight for `buyer_copy`;
- thresholds at exactly 10 versus above 10;
- stable `routing-execution-v1` fields;
- supplied and generated UUID attempt IDs;
- blocked attempts still being recorded;
- a small legacy preflight not writing execution telemetry;
- two concurrent append workers producing complete, parseable JSONL rows.
- missing `task_id` for a mandatory/forced tracked preflight rejecting before write;
- invalid UUIDs, negative/non-integer batch size, negative/non-finite estimated minutes, and malformed JSONL rejecting without mutation.
- non-finite `estimated_burn` rejecting before any ledger mutation.

- [ ] **Step 2: Run ledger tests and confirm RED**

Run:

```bash
python3 -m unittest scripts.tests.test_model_capacity_controller.ExecutionTrackingTests -v
```

Expected: `AttributeError` for missing `record_preflight` or missing `buyer_copy` tracking behavior, with no unrelated import error.

- [ ] **Step 3: Implement minimum ledger helpers**

Add constants and focused helper signatures:

```python
EXECUTION_SCHEMA = "routing-execution-v1"
DEFAULT_EXECUTION_LEDGER = ROOT / "memory/capacity/execution-ledger.jsonl"

def tracking_required(
    task_kind: str,
    batch_items: Optional[int],
    estimated_minutes: Optional[float],
    forced: bool = False,
) -> bool:
    return bool(
        forced
        or task_kind == "buyer_copy"
        or (batch_items is not None and batch_items > 10)
        or (estimated_minutes is not None and estimated_minutes > 10)
    )

def validate_attempt_id(value: str) -> str:
    return str(uuid.UUID(value))

def read_execution_events(path: Path) -> list[dict[str, Any]]:
    """Read every nonblank JSONL row under a shared adjacent-file lock; fail on malformed rows."""

def append_execution_event(path: Path, event: dict[str, Any]) -> None:
    """Validate and append one newline-terminated JSON object under an exclusive lock."""

def record_preflight(
    *, task_id: str, task: str, attempt_id: Optional[str], task_kind: str,
    size: str, estimated_burn: float, estimated_minutes: Optional[float],
    batch_items: Optional[int], forced: bool, result: dict[str, Any],
    ledger_path: Path, recorded_at: datetime,
) -> Optional[dict[str, Any]]:
    """Return and append a versioned event when tracking is required; otherwise return None."""
```

Use an adjacent `.lock` file with `fcntl.flock`. Hold `LOCK_EX` across one flushed append and `LOCK_SH` across reads. Reject malformed rows.

Implementation order is fixed: validate scalar inputs and UUID first; create the event dict second; acquire the lock third; parse every existing nonblank row fourth; append one `json.dumps(..., sort_keys=True) + "\\n"` write and flush fifth; release the lock in `finally`. Never acquire a second lock from inside a locked helper.

- [ ] **Step 4: Run the new ledger tests, then the full file**

```bash
python3 -m unittest scripts.tests.test_model_capacity_controller.ExecutionTrackingTests -v
python3 -m unittest scripts.tests.test_model_capacity_controller -v
```

Expected: new tests pass; existing routing and snapshot persistence tests remain green.

- [ ] **Step 5: Commit execution-ledger primitives**

```bash
git add scripts/model_capacity_controller.py scripts/tests/test_model_capacity_controller.py
git commit -m "feat: add locked routing execution ledger"
```

### Task 3: Add completion telemetry and SLA verdicts

**Files:**
- Modify: `scripts/tests/test_model_capacity_controller.py`
- Modify: `scripts/model_capacity_controller.py`

- [ ] **Step 1: Add failing completion tests**

Add `CompletionTelemetryTests` with named methods covering:

- missing attempt;
- blocked attempt;
- duplicate completion;
- valid attempt with wrong task ID;
- elapsed time computed from timestamps;
- `on_target` at exactly 12;
- `warning` above 12 through exactly 15;
- `breach` above 15;
- `missed_delivery` for undelivered buyer copy;
- `not_applicable` for tracked non-buyer-copy tasks;
- invalid tool calls, provider delta, delay, and delay greater than elapsed causing no write.
- `nan`, `inf`, and negative numeric values rejecting without mutation;
- `unknown` provider delta becoming JSON `null`.

- [ ] **Step 2: Run completion tests and confirm RED**

Run:

```bash
python3 -m unittest scripts.tests.test_model_capacity_controller.CompletionTelemetryTests -v
```

Expected: `AttributeError` for missing `record_completion`, with no unrelated error.

- [ ] **Step 3: Implement completion helpers**

Add:

```python
def buyer_copy_sla(task_kind: str, delivered: bool, elapsed_minutes: float) -> str:
    if task_kind != "buyer_copy":
        return "not_applicable"
    if not delivered:
        return "missed_delivery"
    if elapsed_minutes <= 12:
        return "on_target"
    if elapsed_minutes <= 15:
        return "warning"
    return "breach"

def parse_provider_delta(value: str) -> Optional[float]:
    """Return None for `unknown`; otherwise require a finite float from 0 through 100."""

def record_completion(
    *, task_id: str, attempt_id: str, tool_calls: int,
    provider_delta: Optional[float], avoidable_delay_minutes: float,
    delivered: bool, ledger_path: Path, recorded_at: datetime,
) -> dict[str, Any]:
    """Atomically find one routed incomplete attempt, compute elapsed, validate, and append completion."""
```

Read and validate the ledger while holding the exclusive lock so attempt lookup and append are atomic. Compute elapsed from UTC timestamps. Do not accept caller-supplied elapsed time.

Inside the one exclusive lock: parse all rows; locate exactly one preflight with matching `task_id` and `attempt_id`; reject missing, blocked, or already-completed attempts; compute `(recorded_at - preflight.recorded_at).total_seconds() / 60`; validate telemetry and delay; build the completion event; append and flush once. All validation errors occur before append.

- [ ] **Step 4: Run completion tests and full controller tests**

```bash
python3 -m unittest scripts.tests.test_model_capacity_controller.CompletionTelemetryTests -v
python3 -m unittest scripts.tests.test_model_capacity_controller -v
```

Expected: all pass.

- [ ] **Step 5: Commit completion telemetry**

```bash
git add scripts/model_capacity_controller.py scripts/tests/test_model_capacity_controller.py
git commit -m "feat: record routing completion telemetry"
```

### Task 4: Add deterministic weekly summary

**Files:**
- Modify: `scripts/tests/test_model_capacity_controller.py`
- Modify: `scripts/model_capacity_controller.py`

- [ ] **Step 1: Add failing summary tests**

Add `ExecutionSummaryTests` covering empty output, inclusive cutoff/now boundaries, exclusion outside the window, repeated task IDs as distinct attempts, delivered and undelivered counts, median convention, all buyer-copy SLA outcomes, and total avoidable delay.

- [ ] **Step 2: Run summary tests and confirm RED**

```bash
python3 -m unittest scripts.tests.test_model_capacity_controller.ExecutionSummaryTests -v
```

Expected: `AttributeError` for missing `summarize_execution`.

- [ ] **Step 3: Implement `summarize_execution`**

Return stable JSON keys:

```python
{
    "window_days": 7,
    "completion_count": 0,
    "delivered_count": 0,
    "undelivered_count": 0,
    "median_elapsed_minutes": None,
    "median_tool_calls": None,
    "avoidable_delay_minutes": 0.0,
    "buyer_copy_sla": {
        "on_target": 0,
        "warning": 0,
        "breach": 0,
        "missed_delivery": 0,
    },
}
```

- [ ] **Step 4: Run summary and full controller tests**

```bash
python3 -m unittest scripts.tests.test_model_capacity_controller.ExecutionSummaryTests -v
python3 -m unittest scripts.tests.test_model_capacity_controller -v
```

Expected: all pass.

- [ ] **Step 5: Commit summary behavior**

```bash
git add scripts/model_capacity_controller.py scripts/tests/test_model_capacity_controller.py
git commit -m "feat: summarize routing execution telemetry"
```

### Task 5: Wire additive CLI commands

**Files:**
- Modify: `scripts/tests/test_model_capacity_controller.py`
- Modify: `scripts/model_capacity_controller.py`

- [ ] **Step 1: Add failing CLI parser/acceptance tests**

Add `CliCompatibilityTests` and assert:

- legacy preflight still accepts its existing arguments and exit codes;
- tracked preflight prints `tracking_required` and `attempt_id`;
- generated attempt IDs parse as UUIDs;
- `complete` requires exactly one delivery flag and prints SLA JSON;
- `summary --days 7` prints the stable summary contract;
- preflight and completion accept an injected temporary execution-ledger path.
- mandatory tracking without `--task-id` exits 2 before writing.

- [ ] **Step 2: Run CLI tests and confirm RED**

```bash
python3 -m unittest scripts.tests.test_model_capacity_controller.CliCompatibilityTests -v
```

Expected: parser rejection or missing-command failures because the additive CLI is not wired yet.

- [ ] **Step 3: Implement parser and `main` wiring**

Add global `--execution-ledger`, optional preflight flags `--task-id`, `--attempt-id`, `--estimated-minutes`, `--batch-items`, and `--track`, plus `complete` and `summary` subcommands. Preserve existing `record`, `status`, and legacy `preflight` behavior.

- [ ] **Step 4: Run the full focused suite**

```bash
python3 -m unittest scripts.tests.test_model_capacity_controller -v
python3 -m py_compile scripts/model_capacity_controller.py
```

Expected: zero failures and successful compilation.

- [ ] **Step 5: Commit CLI wiring**

```bash
git add scripts/model_capacity_controller.py scripts/tests/test_model_capacity_controller.py
git commit -m "feat: expose routing v2 telemetry CLI"
```

## Chunk 2: Policy, evidence, and acceptance

### Task 6: Update canonical operator surfaces

**Files:**
- Modify: `docs/agents/model-capacity-routing.md`
- Modify: `TOOLS.md`
- Modify: `memory/job-state/ai-workflow-growth-os.md`
- Modify: `memory/job-state/ai-workflow-growth-os-restart-handoff.md`
- Create: `tasks/implementation-notes.html`

- [ ] **Step 1: Update the routing policy**

Document mandatory tracking thresholds, `buyer_copy` ownership, critical path, 12/15-minute SLA, completion telemetry, summary review, and post-delivery housekeeping. State that Claude is eligible for buyer-copy work only through a separate manual Claude Code handoff when fresh telemetry documents a speed advantage. State that weekly summaries never rewrite estimates automatically.

- [ ] **Step 2: Update tool syntax and Growth OS state**

Add exact CLI examples and make Routing V2 the current operating rule for the active outreach lane. Do not add cron, provider, gateway, credential, deployment, or send authority.

- [ ] **Step 3: Maintain implementation notes**

Record design decisions, deviations, tradeoffs, open questions, files changed, and verification. If none exist for a section, say so explicitly.

- [ ] **Step 4: Check budgets and targeted diffs**

```bash
wc -c AGENTS.md MEMORY.md TOOLS.md HEARTBEAT.md
git diff --check -- scripts/model_capacity_controller.py scripts/tests/test_model_capacity_controller.py docs/agents/model-capacity-routing.md TOOLS.md memory/job-state/ai-workflow-growth-os.md memory/job-state/ai-workflow-growth-os-restart-handoff.md tasks/implementation-notes.html
```

Expected: all bootstrap files within limits and no targeted whitespace errors.

- [ ] **Step 5: Commit policy and operator surfaces**

```bash
git add docs/agents/model-capacity-routing.md TOOLS.md memory/job-state/ai-workflow-growth-os.md memory/job-state/ai-workflow-growth-os-restart-handoff.md tasks/implementation-notes.html tasks/todo.md
git commit -m "docs: adopt routing v2 operating contract"
```

### Task 7: Run temporary-ledger acceptance

**Files:**
- Create: `memory/job-state/claims/routing-v2-2026-10-02.md`
- Create: `scripts/routing_v2_acceptance.py`
- Create: `reports/growth-os/2026-10-02-routing-v2-acceptance.json`

- [ ] **Step 1: Write a failing acceptance-harness test**

Add `RoutingV2AcceptanceHarnessTests.test_acceptance_writes_named_report_without_touching_production_ledger` to `scripts/tests/test_model_capacity_controller.py`. It runs the not-yet-existing harness with a temporary report path and asserts exit 0, the acceptance marker, two temporary events, and an unchanged production-ledger checksum or missing state.

Run:

```bash
python3 -m unittest scripts.tests.test_model_capacity_controller.RoutingV2AcceptanceHarnessTests -v
```

Expected: FAIL because `scripts/routing_v2_acceptance.py` does not exist.

- [ ] **Step 2: Implement the deterministic acceptance harness**

The harness uses `tempfile.TemporaryDirectory`, writes a temporary `current.json` containing fresh 99% Codex and Claude snapshots generated at runtime, invokes the controller CLI with fixed task and attempt IDs, parses its temporary JSONL, compares the production execution-ledger checksum or missing state before and after, writes one JSON report to `--report`, prints `ROUTING_V2_ACCEPTANCE_OK events=2 sla=on_target provider_delta=null`, and exits nonzero on any assertion failure.

- [ ] **Step 3: Run the GREEN harness test and full suite**

```bash
python3 -m unittest scripts.tests.test_model_capacity_controller.RoutingV2AcceptanceHarnessTests -v
python3 -m unittest scripts.tests.test_model_capacity_controller -v
```

Expected: both commands pass.

- [ ] **Step 4: Run a fresh named-report acceptance flow**

```bash
python3 scripts/routing_v2_acceptance.py \
  --report reports/growth-os/2026-10-02-routing-v2-acceptance.json
```

Expected final line: `ROUTING_V2_ACCEPTANCE_OK events=2 sla=on_target provider_delta=null` and a named JSON report containing the same result.

- [ ] **Step 5: Prove no production execution event was fabricated**

The acceptance flow uses only the temporary ledger. The before/after checksum or identical absence proves the production execution ledger was not changed. The production ledger begins receiving events only from real routed work after policy adoption.

- [ ] **Step 6: Write the builder claim**

The claim file contains one claim sentence, acceptance criteria, artifact paths including the named acceptance JSON, and exact rerun commands. Do not mark the feature complete elsewhere.

- [ ] **Step 7: Commit the acceptance harness and builder claim**

```bash
git add scripts/routing_v2_acceptance.py scripts/tests/test_model_capacity_controller.py reports/growth-os/2026-10-02-routing-v2-acceptance.json memory/job-state/claims/routing-v2-2026-10-02.md
git commit -m "test: record routing v2 builder claim"
```

### Task 8: Fresh verification and closeout

**Files:**
- Modify: `memory/job-state/claims/routing-v2-2026-10-02.md`
- Modify: `tasks/todo.md`
- Modify: `memory/2026-10-02.md`
- Modify: `memory/weekly-recaps/current-week.md`
- Modify: `MEMORY.md` only after confirming budget headroom or trimming stale content first
- Modify: `/Users/jtsomwaru/.claude/CLAUDE.md`

- [ ] **Step 1: Dispatch a fresh verifier**

The verifier reads only the claim file and referenced artifacts, then runs:

```bash
python3 -m unittest scripts.tests.test_model_capacity_controller -v
python3 -m py_compile scripts/model_capacity_controller.py
python3 scripts/model_capacity_controller.py --help
python3 scripts/model_capacity_controller.py preflight --help
python3 scripts/model_capacity_controller.py complete --help
python3 scripts/model_capacity_controller.py summary --help
python3 scripts/routing_v2_acceptance.py --report /tmp/routing-v2-verifier-acceptance.json
git diff --check -- scripts/model_capacity_controller.py scripts/tests/test_model_capacity_controller.py docs/agents/model-capacity-routing.md TOOLS.md memory/job-state/ai-workflow-growth-os.md memory/job-state/ai-workflow-growth-os-restart-handoff.md tasks/implementation-notes.html
```

Expected: all tests pass, compilation exits 0, all four help commands exit 0, and targeted diff check emits no output. The verifier separately repeats Task 7's temporary-ledger acceptance and returns `CONFIRMED`, `NOT DONE`, or `UNVERIFIABLE` with evidence.

- [ ] **Step 2: If confirmed, append the verifier verdict to the claim**

- [ ] **Step 3: Log same-run proof and update durable state**

Run:

```bash
python3 scripts/log-proof.py --type script_execution \
  --title "Routing V2 execution telemetry verified" \
  --description "Fresh verifier confirmed buyer-copy routing, mandatory tracked preflight, completion telemetry, SLA reporting, and deterministic acceptance." \
  --outcome success \
  --files scripts/model_capacity_controller.py scripts/tests/test_model_capacity_controller.py scripts/routing_v2_acceptance.py docs/agents/model-capacity-routing.md reports/growth-os/2026-10-02-routing-v2-acceptance.json memory/job-state/claims/routing-v2-2026-10-02.md
python3 scripts/memory_recap_proof_guard.py --date 2026-10-02 --json
```

Then update current memory/state and keep all bootstrap files within budget.

- [ ] **Step 4: Update Claude's standing context and verify it**

Add one concise Routing V2 line to `/Users/jtsomwaru/.claude/CLAUDE.md`: buyer-copy batches remain Codex-owned; Claude Code is used only through JT's manual handoff with fresh telemetry and a documented speed advantage. Verify:

```bash
rg -n "Routing V2|buyer-copy" /Users/jtsomwaru/.claude/CLAUDE.md
```

Expected: one current Routing V2 rule, with no contradictory automatic Claude route.

- [ ] **Step 5: Final acceptance**

Rerun focused tests, compilation, temporary CLI acceptance, budget checks, secret scan on externally shareable artifacts if any, and targeted `git diff --check`.

Exact final commands:

```bash
python3 -m unittest scripts.tests.test_model_capacity_controller -v
python3 -m py_compile scripts/model_capacity_controller.py
python3 scripts/routing_v2_acceptance.py --report reports/growth-os/2026-10-02-routing-v2-acceptance.json
wc -c AGENTS.md MEMORY.md TOOLS.md HEARTBEAT.md
python3 scripts/memory_recap_proof_guard.py --date 2026-10-02 --json
git diff --check -- scripts/model_capacity_controller.py scripts/tests/test_model_capacity_controller.py docs/agents/model-capacity-routing.md TOOLS.md memory/job-state/ai-workflow-growth-os.md memory/job-state/ai-workflow-growth-os-restart-handoff.md tasks/implementation-notes.html tasks/todo.md
```

Expected: tests pass, compile exits 0, budgets remain under limits, proof guard returns `"ok": true`, and targeted diff check emits no output.

- [ ] **Step 6: Commit verified closeout state**

```bash
git add memory/job-state/claims/routing-v2-2026-10-02.md tasks/todo.md memory/2026-10-02.md memory/weekly-recaps/current-week.md MEMORY.md
git commit -m "docs: close verified routing v2 rollout"
```

`/Users/jtsomwaru/.claude/CLAUDE.md` is verified separately because it is outside this repository.

- [ ] **Step 7: Report only fresh verified evidence**

Include tests passed, exact policy behavior, acceptance output, file links, implementation-note summary, and any remaining limitation. Do not claim cron or live provider changes.
