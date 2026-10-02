# Plain-English M1 V2 Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace abstract first-touch COI copy with a validated plain-English system and a rewritten 25-message review packet.

**Architecture:** Keep judgment rules in the cold-email skill and offer framework. Put mechanical checks in one Python validator with unit tests. Treat the review packet as immutable input evidence plus regenerated copy, while preserving all send gates.

**Tech Stack:** Markdown, Python 3 standard library, unittest.

---

### Task 1: Lock the approved contract

**Files:**
- Create: `docs/superpowers/specs/2026-10-02-plain-english-m1-v2-design.md`
- Create: `docs/superpowers/plans/2026-10-02-plain-english-m1-v2.md`

- [x] Record the approved copy limits, banned abstractions, testing plan, and non-send boundary.

### Task 2: Build the deterministic validator with TDD

**Files:**
- Create: `scripts/plain_english_m1_validator.py`
- Create: `scripts/tests/test_plain_english_m1_validator.py`

- [x] Write failing tests for word count, grade ceiling, sentence limits, banned phrases, CTA size, and batch repetition.
- [x] Run the tests and confirm RED failures.
- [x] Implement the smallest validator that passes.
- [x] Run focused tests and confirm GREEN.

### Task 3: Repair the copy rules

**Files:**
- Modify: `skills/cold-email/SKILL.md`
- Modify: `skills/cold-email/examples/bad/anti-patterns.md`
- Create: `skills/cold-email/examples/good/plain-coi-m1.md`
- Modify: `/Users/jtsomwaru/projects/jt-consulting-pipeline/offers/coi-reliability-workflow-audit/outreach-framework.md`

- [x] Replace the 75-150-word email floor with the approved M1 contract.
- [x] Resolve the email-signature contradiction.
- [x] Add abstraction-stack and legal-caveat anti-patterns.
- [x] Add a plain construction/COI example.
- [x] Rewrite the offer framework in buyer language.

### Task 4: Rewrite and validate the first 25

**Files:**
- Create: `reports/growth-os/2026-10-02-first-25-m1-v2-review-packet.md`
- Create: `reports/growth-os/2026-10-02-first-25-m1-v2-evaluation.json`

- [x] Preserve recipients, verified evidence, source status, personalization notes, and pre-send gates.
- [x] Rewrite all 25 bodies to the approved contract.
- [x] Run the validator and repair every hard failure.
- [x] Run a one-read comprehension review across the batch.

### Task 5: Verify and close

- [x] Run focused unit tests and validator acceptance.
- [x] Run `git diff --check` on touched files.
- [x] Scan externally shareable artifacts for secret patterns.
- [x] Record the changed decision in durable state and provide the review artifact.
- [x] Record Routing V2 completion telemetry. The run breached the 15-minute ceiling at 16.97 minutes; baseline comparison and delivery-order regression guards were added before closeout.
