# Growth OS Send Readiness + Outcome Spine V1 Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a deterministic, fail-closed readiness decision and prefilled outcome spine for the approved first-25 M1 V2 batch.

**Architecture:** A focused Python compiler parses the canonical contact CSV and approved Markdown packet, joins optional recipient and sender attestations, applies freshness and sender-safety gates, and atomically writes bounded CSV/JSON outputs. It has no network, credential, provider, campaign, or send capability.

**Tech Stack:** Python 3.9+, standard library only, `unittest`, CSV/JSON/Markdown artifacts.

---

### Task 1: Lock schemas and packet binding

**Files:**
- Create: `scripts/tests/test_growth_os_send_readiness.py`
- Create: `scripts/growth_os_send_readiness.py`

- [ ] Write failing tests for 1–25 positions, 24/26-row inputs, missing/extra packet rows, reordered input, normalized comparisons, duplicate positions/emails, company/person drift, stable row IDs, and known-answer copy hashes.
- [ ] Run the focused suite and confirm RED for the missing module.
- [ ] Implement the minimum parser and binding logic.
- [ ] Run the focused suite and confirm GREEN.

### Task 2: Implement recipient and sender gates

**Files:**
- Modify: `scripts/tests/test_growth_os_send_readiness.py`
- Modify: `scripts/growth_os_send_readiness.py`

- [ ] Write failing tests for exact recipient schema/enums, missing/stale checks, missing/false suppression observation, malformed booleans, unknown values, inclusive 24-hour/seven-day/15-minute boundaries, and future/naive/offset timestamps.
- [ ] Write failing tests for exact sender schema/enums, prohibited and duplicate senders, DNS/health/warmup gates, malformed numbers, per-type platform maximums, deterministic round-robin mixed-capacity allocation, insufficient capacity, and missing/exact-boundary/stale/future sender attestations.
- [ ] Run the focused suite and confirm the expected failures.
- [ ] Implement the minimum gate and allocation logic.
- [ ] Run the focused suite and confirm GREEN.

### Task 3: Emit controlled artifacts

**Files:**
- Modify: `scripts/tests/test_growth_os_send_readiness.py`
- Modify: `scripts/growth_os_send_readiness.py`
- Create: `reports/growth-os/send-readiness/growth-os-first25-m1-v2-2026-10-02/current.json`
- Create: `reports/growth-os/send-readiness/growth-os-first25-m1-v2-2026-10-02/bundles/<bundle_id>/readiness.csv`
- Create: `reports/growth-os/send-readiness/growth-os-first25-m1-v2-2026-10-02/bundles/<bundle_id>/outcome-spine.csv`
- Create: `reports/growth-os/send-readiness/growth-os-first25-m1-v2-2026-10-02/bundles/<bundle_id>/summary.json`
- Create only when ready: `reports/growth-os/send-readiness/growth-os-first25-m1-v2-2026-10-02/bundles/<bundle_id>/instantly-import.csv`

- [ ] Write failing known-answer tests for the exact shared schema version, canonical JSON bytes/hashes, exact headers, raw-file `inputHashes` including null optional inputs, buyer-name splitting, stable prospect/fingerprint/row-hash derivations, enum encoding, lexical multi-blocker ordering, count invariants, ordering, deterministic bundle IDs/payloads/manifests, identical-bundle reuse, same-ID/content-mismatch refusal, run-bundle atomicity, import withholding, `not_sent` outcome initialization, and ready-run → blocked-rerun current-manifest invalidation.
- [ ] Run the focused suite and confirm the expected failures.
- [ ] Implement output generation and CLI.
- [ ] Run the focused suite and confirm GREEN.
- [ ] Run the CLI twice with a fixed `--as-of` on the real first-25 inputs with no fabricated attestations; require 25 readiness rows, 25 `not_sent` outcome rows, zero ready/assigned rows, reconciled counts, byte-equivalent bundle payloads, and no current Instantly import.

### Task 4: Implement append-only sent-copy reconciliation

**Files:**
- Modify: `scripts/tests/test_growth_os_send_readiness.py`
- Modify: `scripts/growth_os_send_readiness.py`
- Create on first reconciliation: `reports/growth-os/send-readiness/growth-os-first25-m1-v2-2026-10-02/reconciliation-events.jsonl`
- Create/update atomically: `reports/growth-os/send-readiness/growth-os-first25-m1-v2-2026-10-02/current-outcomes.csv`

- [ ] Write failing tests for exact reconciliation-event schema rejection, exact projection header, exact-copy send, JT-edited final copy, replay idempotency, conflicting replay, concurrent duplicate/conflict attempts, missing timestamp/vendor/evidence refusal, symlink/hard-link aliases, malformed existing ledger, interrupted-write recovery, and an authoritative post-reconciliation projection showing `sent` while candidate hashes remain unchanged.
- [ ] Run the focused suite and confirm the expected failures.
- [ ] Implement the minimal append-only reconciliation event writer; preserve candidate hashes.
- [ ] Run the focused suite and confirm GREEN.

### Task 5: Verify and reconcile state

**Files:**
- Modify: `memory/job-state/ai-workflow-growth-os.md`
- Modify: `memory/job-state/ai-workflow-growth-os-restart-handoff.md`
- Modify: `memory/2026-10-02.md`
- Modify: `memory/weekly-recaps/current-week.md`

- [ ] Run unit tests in normal and optimized Python.
- [ ] Run `py_compile`, targeted `git diff --check`, secret-pattern scans, and a static no-network-import check.
- [ ] Have a fresh verifier inspect the implementation and artifacts.
- [ ] Record only evidenced current blockers: mailbox inventory/health, recipient mailbox verification, and fresh suppression clear.
- [ ] Update current state and handoff without authorizing sends.
