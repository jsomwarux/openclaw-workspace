# LinkedIn Manual Fixtures Authority Repair Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a new immutable repair commit that closes Claude review findings I-1 through I-3, preserves Program 0 verification, and receives an independent acceptance verdict with zero Critical and zero Important findings.

**Architecture:** Make the canonical outcome ledger and Program 0 latest-wins derivation the only earned-angle publication authority. Regenerate every Program 0 artifact and receipt that legitimately derives from the extended ledger through the governed CLI. Replace the hand-maintained public-copy subset with one policy module consumed by fixture validation and table-driven tests, while also closing lock-file and ledger-read filesystem gaps at the same boundary.

**Tech Stack:** Python 3.9, `unittest`, canonical JSON/SHA-256, Program 0 CLI, Pillow, Git.

**Execution status (2026-09-30):** Chunks 1-3 and Task 8 completed as written. Task 6 deviated: Program 0 `audit-history` rejects the `c4aefea` ledger events (`empty authority allowlist requires all status_unknown human-gate answers`) because JT's 2026-09-28 gate answer for legacy row `fabf927a…` is `still_unknown`; JT chose to restore the approved ledger (`e27dc5bb…`) and hold both fixtures, and Program 0 was regenerated through the canonical CLI with byte-identical outputs. Task 7 therefore records both fixtures as blocked candidates instead of regenerating tracked packets. Task 9's independent review was excluded from this run by JT.

---

## Chunk 1: Freeze the rejected review as executable evidence

### Task 1: Add RED authority and policy regressions

**Files:**
- Modify: `scripts/tests/test_linkedin_content_os_manual_fixtures.py`
- Modify or create only if a shared policy test boundary is needed: `scripts/tests/test_linkedin_content_os_content_policy.py`

- [x] Add a forged-ledger test proving a caller-selected JSONL cannot establish `posted_confirmed` authority.
- [x] Run the forged-ledger test and confirm it fails because the current validator accepts it.
- [x] Add a later-retraction test proving latest-wins governed status must reject an earlier `posted_confirmed` event.
- [x] Run the retraction test and confirm it fails because the current validator ignores the later status.
- [x] Add table-driven tests for every canonical banned hook, forbidden word, statement-colon/list shape, and exclamation point across post, title, subtitle, stages, footer, alt text, and attribution surfaces.
- [x] Run the policy matrix and record the expected failures before implementation.
- [x] Add lock-symlink and noncanonical-ledger-path regressions; confirm both fail for the reviewed reasons.

### Task 2: Record the root-cause contract

**Files:**
- Modify: `tasks/implementation-notes.html`
- Modify: `reports/growth-os/2026-09-29-linkedin-manual-fixtures-review-reconciliation.md`

- [x] Record that caller-selected evidence paths, duplicated policy subsets, and unpropagated governed-ledger mutations are the three root causes.
- [x] Record the exact rejected target `c4aefeaba5847d3c0ad703489f6aa2234b6c1365` and the 0 Critical/3 Important/7 Minor verdict.

## Chunk 2: Repair the authority and filesystem boundaries

### Task 3: Canonicalize earned-angle authority

**Files:**
- Modify: `scripts/linkedin_content_os/manual_fixtures.py`
- Modify: `scripts/tests/test_linkedin_content_os_manual_fixtures.py`
- Modify: `memory/content/linkedin-content-os/manual-fixtures/sources/servicenow-inry-employee-front-door-teardown.v1.json`
- Modify: `memory/content/linkedin-content-os/manual-fixtures/sources/openai-health-summaries-ai-news.v1.json`

- [x] Remove `confirmationPath` from the trusted source-spec and packet contract.
- [x] Resolve only `memory/content/linkedin-content-os/outcomes.v1.jsonl` as the canonical ledger.
- [x] Reuse Program 0's governed latest-wins derivation rather than duplicating event-selection semantics.
- [x] Require the row's derived status to be `posted_confirmed` and bind the exact latest publication event, final text hash, public URL, and source row.
- [x] Bind the relevant ledger prefix/position rather than the mutable whole-file hash so unrelated later events do not invalidate accepted fixtures.
- [x] Run the focused authority tests after each RED/GREEN slice.

### Task 4: Close adjacent filesystem gaps

**Files:**
- Modify: `scripts/linkedin_content_os/canonical.py`
- Modify: `scripts/linkedin_content_os/manual_fixtures.py`
- Modify: `scripts/tests/test_linkedin_content_os_manual_fixtures.py`

- [x] Open artifact lock files without following symlinks and prove an existing lock symlink cannot create or modify an external target.
- [x] Read the canonical outcome ledger through strict JSONL parsing and repository containment.
- [x] Keep exact replay, orphan refusal, ancestor-symlink rejection, and byte-identical image binding green.

## Chunk 3: Centralize the full public-copy policy

### Task 5: Create one deterministic policy authority

**Files:**
- Create: `scripts/linkedin_content_os/content_policy.py`
- Modify: `scripts/linkedin_content_os/manual_fixtures.py`
- Modify: `scripts/tests/test_linkedin_content_os_manual_fixtures.py`
- Test: `scripts/tests/test_linkedin_content_os_content_policy.py`

- [x] Encode the complete governed hard bans from `docs/agents/content-rules.md` and `memory/content-voice.md` as explicit deterministic constants and regex rules.
- [x] Reject forbidden words as word/phrase boundaries, all hard-banned hooks/shapes, statement-colon/list reveals, and exclamation points.
- [x] Apply the same function to every public surface: post, title, subtitle, eyebrow, stages, footer, alt text, and attribution.
- [x] Keep non-public evidence text out of this voice policy unless a separate privacy/internal-machinery rule governs it.
- [x] Run the table-driven surface matrix until green, then run the focused manual-fixture suite.

## Chunk 4: Reconcile Program 0 and regenerate immutable fixtures

### Task 6: Regenerate Program 0 governed derivatives

**Files:**
- Regenerate: `memory/content/linkedin-content-os/historical-audit.v1.json`
- Regenerate: `memory/content/linkedin-content-os/historical-recovery-request.v1.json`
- Regenerate: `memory/content/linkedin-content-os/voice-gold.v0.jsonl`
- Regenerate: `memory/content/linkedin-content-os/contrastive-pairs.v0.jsonl`
- Regenerate: `memory/content/linkedin-content-os/authority-consumption.phase-2-audit.v1.json`
- Regenerate: `memory/content/linkedin-content-os/authority-consumption.phase-2-corpus.v1.json`
- Regenerate: `reports/growth-os/2026-09-28-linkedin-content-os-program-0.md`

- [x] Run only the governed `audit-history` and `build-corpus` CLI commands from the canonical Program 0 plan. Deviation: run against the restored approved ledger, because the extended ledger violates the existing authority context; outputs are byte-identical to the approved artifacts.
- [x] Run the canonical Program 0 `verify` command and require PASS with all receipt and byte hashes recomputed.
- [ ] Confirm the formerly stale historical row now derives `posted_confirmed` and the audit/corpus counts reconcile. Not achievable without a governed human-gate answer; the row correctly derives `status_unknown` and counts reconcile at 101 `status_unknown`.
- [x] Do not perform network calls, new boundary captures, Mission Control writes, or human-gate re-ingestion.

### Task 7: Regenerate and inspect the two fixture packets

**Files:**
- Regenerate: `memory/content/linkedin-content-os/manual-fixtures/linkedin-teardown-servicenow-inry-2026-09-29-v1/packet.v1.json`
- Regenerate: `memory/content/linkedin-content-os/manual-fixtures/linkedin-teardown-servicenow-inry-2026-09-29-v1/image.v1.png`
- Regenerate: `memory/content/linkedin-content-os/manual-fixtures/linkedin-ai-news-openai-health-2026-09-29-v1/packet.v1.json`
- Regenerate: `memory/content/linkedin-content-os/manual-fixtures/linkedin-ai-news-openai-health-2026-09-29-v1/image.v1.png`
- Modify: `memory/content/linkedin-content-os/manual-fixtures/accepted-set.v1.json`

- [ ] Regenerate with a resolved real-path `TMPDIR` and a valid in-window timestamp; if the AI-news fixture has expired, replace it rather than extending stale evidence. Blocked: both specs fail the governed earned-angle gate; they build only under synthetic governed confirmation in isolation.
- [x] Confirm exact replay is byte-identical and conflicting replay is refused (isolated governed copy and regression tests).
- [x] Inspect both 1080×1350 images at original resolution (isolated renders; byte-identical to the `c4aefea`-reviewed images).
- [x] Re-run voice and distribution guards on both final posts.

## Chunk 5: Immutable verification and independent acceptance

### Task 8: Run complete builder verification

**Files:**
- Modify: `tasks/todo.md`
- Modify: `tasks/implementation-notes.html`
- Modify: `memory/job-state/claims/linkedin-manual-fixtures-repair-2026-09-29.md`

- [x] Run focused manual-fixture and policy tests.
- [x] Run the full `test_linkedin_content_os_*.py` suite with a resolved real-path `TMPDIR`.
- [x] Run Program 0 verify, Python compilation, voice guards, distribution guards, replay/tamper probes, secret scan, `git diff --check`, and clean-status check.
- [x] Record exact counts, hashes, files changed, deviations, and remaining questions in the implementation notes and builder claim.

### Task 9: Freeze and independently review the new commit

**Files:**
- Create: `deliverables/claude-reviews/linkedin-manual-fixtures-<new-sha>-prompt.md`

- [ ] Commit the complete repair locally without amending `c4aefea…`.
- [ ] Verify the new HEAD and clean worktree.
- [ ] Run one fresh read-only Claude Code review from JT's Anthropic-direct subscription session against the new exact SHA.
- [ ] Accept only `VERDICT: APPROVED` with zero Critical and zero Important findings.
- [ ] Keep publication, Mission Control writes, Drive uploads, deployment, scheduling, recurrence, applications, provider changes, and external sends closed.

---

## Addendum A — Program 0 supplemental human-gate correction (approved 2026-09-30)

**Why:** JT answered legacy row `fabf927a2f54fa40a8d4cc48948f32393259c842d7ada3bbd5bfae84f2f69ccf` as posted on 2026-09-30 (`confirmedAt` 2026-09-30T09:01:38-04:00; URL `https://www.linkedin.com/feed/update/urn:li:activity:7490053069380964353/`; final text 1,083 bytes, SHA-256 `fb2d82be18e796fdf3eb32dbb4c109792460aa2e90d86ea2fdbfa6b806b4bdea`). `ingest-human-gate` is a one-shot boundary: it refuses the answer (`phase-two run context predates confirmedAt`; `human-gate replay conflicts with the existing event block`). It stays unchanged.

**Design (smallest canonical path):**

- New closed CLI command `ingest-history-correction`, backed by `derive_history_supplement` / `ingest_history_supplement_files` in `recovery.py`. It is separate from `ingest-human-gate`.
- Input `human-gate-supplement-1.v1.json` (`linkedin-human-gate-supplement.v1`): `supplementId`, `baseResponseSha256`, `baseManifestSha256`, `corrections[]` (each `legacyRowSha256`, `targetOutcomeEventId`, `targetEventSha256`, plus the base answer shapes `posted`/`not_posted`/`still_unknown`), and `confirmedAt`. Closed, null-free, strict JSON.
- Append-only events; prior bytes are never edited and the 2026-09-28 `history:<row>` event is preserved:
  - `history-supplement-1:<row>` is the replacement `historical_status`.
  - When the answer is posted, `publication-supplement-1:<row>` and, if final text is supplied, the exact-text receipt `authority-supplement-1:<row>` are added. Both use the existing receipt derivation (response hash, fresh run ID, ledger prefix/position, and validation time).
  - `correction-supplement-1:<row>` targets `history:<row>` with the replacement hash. Its `recordedAt` is the fresh run context time, strictly later than both.
- Transactional outputs:
  - `corpus-authority-manifest.supplement-1.v1.json` uses the existing manifest v1 schema, bound to the supplement response hash, fresh run ID, receipt allowlist, and ledger prefix/position through the supplement block.
  - `run-context.supplement-1-authority.v1.json`.
  - The base manifest, base authority context, and focus receipt and anchor stay byte-identical.
- Fails closed on:
  - a run context that is not later than `confirmedAt`
  - a `confirmedAt` not later than the base authority
  - base response, base manifest, or target hash mismatch
  - a wrong packet or event type
  - a target that is no longer the row's latest status, or is already corrected (chains/cycles)
  - a no-op correction
  - unknown, null, or partial fields
  - a base ledger that already carries corpus authority receipts (manifest v1 binds one authority)
  - symlink, escape, or alias paths
  - partial or conflicting outputs

  Exact replay writes nothing.
- Boundaries: a fresh `init-run` context `run-context.supplement-1.v1.json`, with new phases `supplement-before` and `supplement-after` captured by the existing read-only `capture-boundaries`.
- `verify`:
  - New all-or-none arguments: `--supplement`, `--supplement-run-context`, `--supplement-authority-run-context`, `--supplement-manifest`, `--supplement-before`, `--supplement-after`.
  - Base checks keep the base manifest and context.
  - With a supplement, verify re-derives the ledger block, manifest, and authority context byte-exactly, requires an equal `supplement-before/after` pair bound to the supplement run context, and requires phase-2 receipts to consume the supplement authority.
  - Without supplement arguments, any `historical_status`, `correction`, or `corpus_authority_receipt` after the base ledger position fails closed.
- Regeneration:
  - `audit-history` and `build-corpus` run under the supplement authority at the canonical phase-2 paths; prior hashes are recorded in the reconciliation report.
  - `build-focus`, phase-2 `build-fixtures`, and `preview-checkin` are rerun to prove they are byte-identical.
  - The verification report, both fixture packet/image pairs, and the accepted set are regenerated.
- The 2 likes / 2 comments snapshot is intentionally omitted: `metric_snapshot` requires an observed `windowDays`, which is unknown.

### Task A1: RED regressions
- [ ] Recovery: supplement derivation, ingestion, replay, and every fail-closed case above.
- [ ] CLI: the command set includes `ingest-history-correction`; boundary phases accept `supplement-before/after`; verify passes only with the equal, run-bound supplement pair and rejects missing, partial, or tampered supplement proof.

### Task A2: Implement minimally until GREEN

### Task A3: Governed run
- [ ] `init-run` for the supplement, then `supplement-before` capture.
- [ ] `ingest-history-correction`, `audit-history`, and `build-corpus`.
- [ ] Byte-identical focus, fixture, and check-in reruns.
- [ ] `supplement-after` capture, then `verify`.

### Task A4: Regenerate fixtures, packets, images, and the accepted set

### Task A5: Full verification

### Task A6: One immutable child commit of `d4c3bcd…`; no push, no independent review
