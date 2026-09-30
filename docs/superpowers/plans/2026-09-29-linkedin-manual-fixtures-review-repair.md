# LinkedIn Manual Fixtures Review Repair Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Repair the two governed LinkedIn manual-fixture packets so a fresh independent Claude review can approve the exact immutable commit with zero Critical and zero Important findings.

**Architecture:** Strengthen the manual-fixture boundary once: source specs are normalized into policy-complete packets, and packet validation re-derives the same contract rather than trusting packet-owned hashes or pass strings. Evidence, relationship-conflict results, claim spans, earned-angle provenance, visual metadata, freshness, and asset paths become closed fields. The stale AI-news fixture is replaced with a fresh primary-source event; no live Mission Control, Drive, publication, provider, deployment, or schedule action is added.

**Tech Stack:** Python 3.9, `unittest`, Pillow, canonical JSON/SHA-256, immutable local fixture artifacts.

---

## Chunk 1: Contract and security boundary

### Task 1: Freeze the reviewed failures as regression tests

**Files:**
- Modify: `scripts/tests/test_linkedin_content_os_manual_fixtures.py`

- [ ] Add one failing test per contract class: expiry bounded by source TTL; validation-time freshness; slug-only IDs; traversal-before-write; symlink asset rejection; exact packet asset path; failed rights/privacy/QA; lane/template mismatch; internal terms across post/visual/alt text; claim excerpt/span binding; earned-angle file hash and exact excerpt; obsolete decision options.
- [ ] Run only the manual-fixture suite and record the expected failures before production edits.

### Task 2: Make normalization and validation share one policy truth

**Files:**
- Modify: `scripts/linkedin_content_os/manual_fixtures.py`
- Test: `scripts/tests/test_linkedin_content_os_manual_fixtures.py`

- [ ] Validate stable IDs before creating paths.
- [ ] Bind `createdAt`, `expiresAt`, reader, objective, winner rationale, lifecycle state, and decision options into the draft hash.
- [ ] Enforce `expiresAt <= earliest source fresh-until` and recompute freshness during packet validation.
- [ ] Re-derive and compare normalized sources, claims, angle, visual, results, and QA instead of accepting internally consistent hashes.
- [ ] Require the exact packet-versioned image path, reject symlinks with `lstat`, and resolve beneath the artifact root.
- [ ] Write a complete candidate packet/image pair under one lock and refuse races/conflicting replay.
- [ ] Keep exact replay byte-identical.
- [ ] Run focused tests after each red/green slice.

## Chunk 2: Evidence and content truth

### Task 3: Add closed evidence and conflict contracts

**Files:**
- Modify: `scripts/linkedin_content_os/manual_fixtures.py`
- Modify: `scripts/tests/test_linkedin_content_os_manual_fixtures.py`
- Modify: `memory/content/linkedin-content-os/source-policy.v1.json`
- Modify: `memory/content/linkedin-content-os/manual-fixtures/sources/appfolio-column-teardown.v1.json`
- Modify: `memory/content/linkedin-content-os/manual-fixtures/sources/<fresh-ai-event>.v1.json`

- [ ] Add exact outbound claim spans and require every material claim text to appear in `postText`.
- [ ] Verify claim excerpt hashes against the frozen source excerpts.
- [ ] Replace free-form earned angles with an allowed source-family record that binds an exact repository file hash, exact excerpt, and JT-confirmation/proof pointer.
- [ ] Add the five required teardown relationship-conflict results and route the AppFolio/Altmark adjacency to an explicit blocked-or-cleared result; no inference from silence.
- [ ] Add AI-event source identity/allowlist and protected-purpose results.
- [ ] Write failing tests first, then implement the smallest closed schemas.

### Task 4: Rewrite the teardown fixture

**Files:**
- Modify: `memory/content/linkedin-content-os/manual-fixtures/sources/appfolio-column-teardown.v1.json`

- [ ] Attribute vendor assertions explicitly.
- [ ] Rewrite around a concrete property-finance input scene without the blocked `exception layer`, disconnected-risk, colon-list, or semantic-repeat shapes.
- [ ] Keep every material claim bound to exact source text and label the workflow as a public-evidence hypothesis.
- [ ] Reorder the workflow, image stages, and alt text so validation precedes posting/movement and all three agree.
- [ ] If the Altmark adjacency cannot be safely cleared from canonical evidence, return `SKIP` for this candidate and select a different fresh teardown trigger rather than asking JT to resolve an avoidable content candidate.

### Task 5: Replace the stale AI-news fixture

**Files:**
- Create: `memory/content/linkedin-content-os/manual-fixtures/sources/<fresh-ai-event>.v1.json`
- Remove through versioned replacement, not history rewrite: the stale OpenAI fixture from the accepted candidate set

- [ ] Select one primary public AI event still inside the five-day window with enough life remaining for review.
- [ ] Freeze compliant excerpts and hashes locally.
- [ ] Bind a public-safe JT artifact or confirmed field lesson that is not internal machinery.
- [ ] Separate vendor/public facts from JT's operating model in both copy and image.
- [ ] Map 100% of material claims to exact post spans and excerpts.
- [ ] Avoid banned contrast and colon-list shapes.

## Chunk 3: Visual and deterministic QA

### Task 6: Harden the renderer and visual validator

**Files:**
- Modify: `scripts/linkedin_content_os/manual_fixtures.py`
- Modify: `scripts/tests/test_linkedin_content_os_manual_fixtures.py`

- [ ] Add deterministic minimum font sizes, bounding-box overflow checks, safe-area checks, and centered numeral rendering.
- [ ] Raise disclosure/footer and stage-label sizes to mobile-readable values.
- [ ] Scan title, subtitle, stages, footer, and alt text for prohibited internal terms and voice hard-fails.
- [ ] Record font identity and Pillow version in the packet or make rendering fail closed when the pinned host font is unavailable.
- [ ] Ensure the AI-news card paraphrases the source and visibly separates JT interpretation from source attribution.

### Task 7: Regenerate immutable packets and review artifacts

**Files:**
- Regenerate: `memory/content/linkedin-content-os/manual-fixtures/<packet-id>/packet.v1.json`
- Regenerate: `memory/content/linkedin-content-os/manual-fixtures/<packet-id>/image.v1.png`
- Modify: `reports/growth-os/2026-09-28-linkedin-manual-fixtures-next-wave.md`
- Create: `reports/growth-os/2026-09-29-linkedin-manual-fixtures-review-reconciliation.md`

- [ ] Build both fixtures using the real current timestamp and a real-path temporary directory.
- [ ] Inspect both images at original resolution and 390px mobile width.
- [ ] Record exact source, draft, payload, and image hashes plus every adjudicated Claude finding.
- [ ] Keep all external and live-system gates closed.

## Chunk 4: Verification and model-efficient handoff

### Task 8: Local verification

**Files:**
- Test: `scripts/tests/test_linkedin_content_os_manual_fixtures.py`
- Test: `scripts/tests/test_linkedin_content_os_*.py`

- [ ] Run focused manual-fixture tests.
- [ ] Run the full LinkedIn Content OS suite with `TMPDIR` resolved to a nonsymlink real path.
- [ ] Run Python compilation and `git diff --check`.
- [ ] Run voice and distribution guards on post text and all visual text/alt text.
- [ ] Run exact replay and hostile tamper probes.
- [ ] Run credential, privacy, and boundary scans.

### Task 9: Immutable claim and one final Claude review

**Files:**
- Create: `memory/job-state/claims/linkedin-manual-fixtures-repair-2026-09-29.md`
- Create: `deliverables/claude-reviews/linkedin-manual-fixtures-<repair-sha>-prompt.md`

- [ ] Commit the exact repair bundle locally.
- [ ] Write the builder claim with commands, observed counts, hashes, and all gates still closed.
- [ ] Prepare one narrow read-only Claude prompt against base `75d5058...` and the repair SHA.
- [ ] Do not ask Claude to rebuild; it verifies the immutable diff and reports only Critical/Important residuals plus verification evidence.
- [ ] Acceptance requires a fresh non-builder `VERDICT: APPROVED` before reporting the fixtures accepted.
