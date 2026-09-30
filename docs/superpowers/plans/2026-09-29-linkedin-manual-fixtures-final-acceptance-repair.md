# LinkedIn Manual Fixtures Final Acceptance Repair Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents are explicitly authorized) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close Claude's five Important findings and the adjacent Minor findings without expanding the external-action boundary, then freeze one new immutable commit for fresh independent acceptance.

**Architecture:** Keep one deterministic normalization/validation path. Governed angle authority is a hash-bound `posted_confirmed` outcome tied to the exact public URL and exact final text; source claims remain exact spans of frozen primary-source excerpts. Builds and validation share symlink-safe resolved-root containment, deterministic render-byte equality, one canonical public-text policy, and a lock/orphan refusal boundary.

**Tech Stack:** Python 3.9, `unittest`, Pillow, canonical JSON/SHA-256, local immutable JSON/PNG artifacts.

---

## Chunk 1: Authority and exploit regressions

### Task 1: Freeze the five Important findings as failing tests

**Files:**
- Modify: `scripts/tests/test_linkedin_content_os_manual_fixtures.py`
- Test: `scripts/tests/test_linkedin_content_os_manual_fixtures.py`

- [x] Add a forged-angle test that replaces the governed outcome with a builder-authored `posted:true` record and expects rejection.
- [x] Add an image-swap test that rehashes a foreign 1080×1350 PNG and expects render-byte mismatch rejection.
- [x] Add parent-directory and packet-directory symlink escape tests for build and validation.
- [x] Add table-driven hard-block tests across post, eyebrow, title, subtitle, stage, footer, and alt text.
- [x] Add a primary-source-permalink/claim-span test that rejects the newsroom index and unbound story-content prose.
- [x] Run each focused test and record the expected RED failure before production edits.

### Task 2: Bind earned angles to governed publication truth

**Files:**
- Modify: `scripts/linkedin_content_os/manual_fixtures.py`
- Modify: `scripts/tests/test_linkedin_content_os_manual_fixtures.py`
- Replace: `memory/content/linkedin-content-os/manual-fixtures/evidence/jt-source-to-decision-posted-confirmation.v1.json`

- [x] Append closed `historical_status: posted_confirmed` and `publication_acknowledged` events to the existing governed outcome ledger with the public LinkedIn URL, exact final text, exact final-text hash, and source pointer.
- [x] Require `_validate_angle` to load the governed ledger beneath the repository root, bind the exact legacy row, verify both event types, source pointer/public URL, exact final text/hash, and the angle excerpt within that text.
- [x] Remove trust in raw `posted:true` or self-authored confirmation prose.
- [x] Run the angle regressions GREEN.

## Chunk 2: Shared deterministic boundary

### Task 3: Add path containment, lock, and orphan refusal

**Files:**
- Modify: `scripts/linkedin_content_os/manual_fixtures.py`
- Modify: `scripts/tests/test_linkedin_content_os_manual_fixtures.py`

- [x] Add one helper that rejects symlinks in every existing path component and proves the resolved target remains below the resolved artifact root before mkdir/read/write.
- [x] Reuse the helper for build paths, validation paths, and earned-angle authority paths.
- [x] Wrap packet creation in an exclusive path lock.
- [x] Refuse an orphan asset or orphan packet instead of overwriting it.
- [x] Run path, replay, and orphan regressions GREEN.

### Task 4: Bind PNG bytes to the visual route and renderer identity

**Files:**
- Modify: `scripts/linkedin_content_os/manual_fixtures.py`
- Modify: `scripts/tests/test_linkedin_content_os_manual_fixtures.py`

- [x] Record deterministic renderer identity, Pillow version, and selected font identities in the packet draft binding.
- [x] Re-render `visualRoute` during validation and require exact PNG byte equality.
- [x] Reject over-wide single words and eyebrow overflow before drawing.
- [x] Increase stage/footer mobile legibility while preserving the 1080×1350 safe area.
- [x] Run swapped-image, overflow, dimensions, replay, and tamper regressions GREEN.

### Task 5: Centralize public-text and attribution policy

**Files:**
- Modify: `scripts/linkedin_content_os/manual_fixtures.py`
- Modify: `scripts/tests/test_linkedin_content_os_manual_fixtures.py`
- Read authority: `docs/agents/content-rules.md`
- Read authority: `scripts/jt_voice_guard.py`

- [x] Encode the complete canonical hard-block vocabulary/patterns once and apply it to all seven public surfaces.
- [x] Reject contractions with `n't`, `not … but`, em dashes, inline colon lists, Eve/internal-automation terms, and the canonical blocked phrases.
- [x] Derive allowed attribution types from source type/publisher instead of trusting claim labels.
- [x] Require `createdAt >= max(source.retrievedAt)`.
- [x] Run one exploit test per pattern/surface plus attribution/timestamp regressions GREEN.

## Chunk 3: Source truth, artifacts, and acceptance

### Task 6: Repair source records and packet lineage

**Files:**
- Modify: `memory/content/linkedin-content-os/manual-fixtures/sources/servicenow-inry-employee-front-door-teardown.v1.json`
- Modify: `memory/content/linkedin-content-os/manual-fixtures/sources/openai-health-summaries-ai-news.v1.json`
- Modify: `scripts/tests/test_linkedin_content_os_manual_fixtures.py`

- [x] Replace the ServiceNow newsroom index with the exact official story permalink and freeze excerpts that support every factual sentence.
- [x] Rewrite or bind the story-content sentence, date claims, footer attribution, and final lines.
- [x] Make attribution typing consistent and add typed evidence pointers for conflict results.
- [x] Start each new revision family at `packetVersion: 1`; do not invent a supersession chain for rejected, never-accepted artifacts.
- [x] Add tracked-artifact build/validate/replay tests.

### Task 7: Regenerate and inspect immutable packets

**Files:**
- Regenerate: `memory/content/linkedin-content-os/manual-fixtures/manual-fixtures/*/packet.v1.json`
- Regenerate: `memory/content/linkedin-content-os/manual-fixtures/manual-fixtures/*/image.v1.png`
- Modify: `memory/content/linkedin-content-os/manual-fixtures/accepted-set.v1.json`
- Modify: `reports/growth-os/2026-09-29-linkedin-manual-fixtures-review-reconciliation.md`

- [x] Build in a real-path temporary directory first and require byte-identical replay.
- [x] Promote only the two complete packet/image pairs into the tracked artifact root.
- [x] Inspect both rendered images at original resolution for hierarchy, overflow, source/JT separation, and stage order.
- [x] Update accepted-set and reconciliation hashes from generated bytes only.

### Task 8: Verify, freeze, and hand off

**Files:**
- Modify: `tasks/todo.md`
- Modify: `tasks/implementation-notes.html`
- Create: `deliverables/claude-reviews/linkedin-manual-fixtures-<new-sha>-prompt.md`

- [x] Run the focused fixture suite, full LinkedIn OS suite with real-path `TMPDIR`, compilation, diff hygiene, voice/distribution guards, replay/tamper probes, and scoped secret scan.
- [ ] Confirm clean worktree after committing and record exact artifact hashes.
- [ ] Prepare a narrow read-only prompt bound only to the new immutable SHA and all governing artifacts.
- [ ] Commission one fresh independent review. Acceptance requires `VERDICT: APPROVED` with zero Critical and zero Important findings.
- [x] Keep posting, Mission Control writes, Drive upload, deployment, scheduling, recurrence, provider actions, applications, and external sends closed.
