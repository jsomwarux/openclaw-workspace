# Dual-Model Capacity Controller Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents are explicitly authorized) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent Codex or Claude subscription exhaustion by routing substantive work from current capacity snapshots, preserving a 25% reserve, and eliminating duplicate model work and unnecessary Drive uploads.

**Architecture:** A deterministic Python CLI owns current snapshots, an append-only usage ledger, and fail-closed task preflight. Canonical policy files define ownership, thresholds, local-first artifacts, and the manual Claude `/status` boundary. Growth OS state consumes the controller without changing providers, schedules, credentials, or external systems.

**Tech Stack:** Python 3 standard library, JSON/JSONL, unittest, Markdown policy/state files.

---

## Task 1: Deterministic capacity controller

**Files:**
- Create: `scripts/model_capacity_controller.py`
- Create: `scripts/tests/test_model_capacity_controller.py`
- Create: `memory/capacity/current.json`
- Create: `memory/capacity/usage-ledger.jsonl`

- [x] Write failing tests for snapshot validation, threshold bands, fit routing, reserve protection, stale/unknown large-lane refusal, deterministic/mechanical routing, and append-only recording.
- [x] Run the focused test and confirm it fails because the controller does not exist.
- [x] Implement the minimal CLI and pure routing functions.
- [x] Run the focused tests and confirm all pass.
- [x] Record the fresh Codex snapshot and an explicit unknown Claude snapshot.

## Task 2: Canonical operating policy

**Files:**
- Create: `docs/agents/model-capacity-routing.md`
- Modify: `AGENTS.md`
- Modify: `TOOLS.md`
- Modify: `MEMORY.md`
- Modify: `/Users/jtsomwaru/.claude/CLAUDE.md`
- Modify: `docs/agents/mistakes-log-recent.md`
- Modify: `docs/agents/regression-checks.md`
- Modify: `memory/2026-10-02.md`

- [x] Define the 60/40/25/15 threshold bands, 25% reserve, telemetry freshness, task ownership, one-builder/one-review rule, and two-cycle repair limit.
- [x] Replace blanket Drive upload policy with local-first policy while preserving explicit client/share/job-application requirements.
- [x] Mark the correction as implemented rather than pending.
- [x] Keep bootstrap files below their byte budgets.

## Task 3: Growth OS and Apollo routing

**Files:**
- Modify: `docs/superpowers/plans/2026-10-01-ai-workflow-growth-os-14-day-throughput-reset.md`
- Modify: `memory/job-state/ai-workflow-growth-os.md`
- Modify: `memory/job-state/ai-workflow-growth-os-restart-handoff.md`

- [x] Route Apollo mechanical validation to scripts first.
- [x] Route bounded evidence research adaptively between Eve and Claude using one row schema and no duplicate full-batch review.
- [x] Assign all n8n implementation to JT's existing Claude Code n8n agent via one paste-ready prompt; Eve owns blueprint, acceptance, state, and final recommendation.
- [x] Preserve every no-send/provider/credential/activation boundary.

## Task 4: Verification and proof

**Files:**
- Modify: `memory/weekly-recaps/current-week.md`
- Modify: `proofs/2026-10-02/actions.jsonl` through `scripts/log-proof.py`

- [x] Run focused unit tests and CLI smoke checks for normal, reserve, hard-stop, unknown, and mechanical cases.
- [x] Run policy consistency checks and `git diff --check` on touched files.
- [x] Run byte-budget checks and the memory recap proof guard.
- [x] Log one same-run proof and update the progress card.

## Scope boundary

This implementation does not change model/provider configuration, cron schedules or payloads, credentials, gateway settings, Apollo, n8n, Google Drive, Mission Control, or any external system. Those remain separate authorization surfaces.
