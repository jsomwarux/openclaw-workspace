# LinkedIn Content OS Program 0 Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace unreliable LinkedIn publication history with evidence-backed truth, establish a JT-confirmed current focus and exact-text voice corpus, secure one genuinely permissioned positive proof fixture, and locally prove one deduplicated Mission Control check-in contract without creating any live task or automation.

**Architecture:** A Python 3.9-compatible, standard-library-only package reads legacy content files without mutating them and emits canonical, hash-bound Program 0 artifacts. Append-only outcome events own publication/performance facts; a hash-bound read-only Mission Control snapshot owns packet approval/closure facts. A pure projector combines those owners to derive zero or one staged check-in preview without creating a second lifecycle. Mission Control integration, live admission, deployment, recurrence, content generation, image rendering, and publication remain outside this plan.

**Tech Stack:** Python 3.9 standard library, `unittest`, canonical JSON/JSONL, SHA-256, existing Mission Control universal-task and lane-packet contracts.

**Authority boundary:** This plan authorizes local code, fixtures, tests, reports, and exactly four read-only loopback `GET /api/tasks` captures—one before/after pair around each side of the human gate—only after JT separately approves execution. It does **not** authorize a Mission Control write, service restart, deployment, Drive upload, content generation, cron, schedule, provider call, external network call, or LinkedIn action.

**Governing design:** `docs/superpowers/specs/2026-09-28-linkedin-content-os-opus-reconciliation.md`

---

## File map

### New implementation files

- `scripts/linkedin_content_os/__init__.py` — package marker only.
- `scripts/linkedin_content_os/canonical.py` — canonical JSON serialization, SHA-256, strict JSONL reading, atomic writes, and exact-prefix append protection.
- `scripts/linkedin_content_os/contracts.py` — closed Program 0 enums and validators for focus, audit, outcome, corpus, fixture, and check-in records.
- `scripts/linkedin_content_os/mc_snapshot.py` — exact loopback GET capture plus strict hash-bound validation of the read-only Mission Control task snapshot.
- `scripts/linkedin_content_os/historical_audit.py` — read-only migration analysis for legacy LinkedIn rows.
- `scripts/linkedin_content_os/outcomes.py` — append-only content outcome ledger with idempotent replay and conflicting-replay refusal.
- `scripts/linkedin_content_os/recovery.py` — validate JT's bounded focus/history/permission response and convert it into typed append-only events.
- `scripts/linkedin_content_os/focus.py` — current-focus snapshot builder with source hashes and staleness checks.
- `scripts/linkedin_content_os/source_policy.py` — explicit allowed/prohibited source-family policy and owner bindings.
- `scripts/linkedin_content_os/corpus.py` — exact-text gold-set and contrastive-pair builder; never substitutes summaries for final text.
- `scripts/linkedin_content_os/voice_rules.py` — deterministic inventory and retirement checks for legacy voice rules that conflict with the reconciled design.
- `scripts/linkedin_content_os/fixtures.py` — Program 0 positive/negative fixture selection and validation.
- `scripts/linkedin_content_os/checkin.py` — pure zero-or-one check-in projection from unresolved outcome facts.
- `scripts/linkedin_content_os/cli.py` — local Program 0 command surface; no network and no Mission Control writes.
- `scripts/linkedin_content_os/boundaries.py` — before/after read-only boundary snapshots for Mission Control, cron registry, LaunchAgent files, protected inputs, and checkout fingerprints.

### New tests and immutable fixtures

- `scripts/tests/test_linkedin_content_os_canonical.py`
- `scripts/tests/test_linkedin_content_os_historical_audit.py`
- `scripts/tests/test_linkedin_content_os_mc_snapshot.py`
- `scripts/tests/test_linkedin_content_os_outcomes.py`
- `scripts/tests/test_linkedin_content_os_recovery.py`
- `scripts/tests/test_linkedin_content_os_focus.py`
- `scripts/tests/test_linkedin_content_os_source_policy.py`
- `scripts/tests/test_linkedin_content_os_corpus.py`
- `scripts/tests/test_linkedin_content_os_voice_rules.py`
- `scripts/tests/test_linkedin_content_os_fixtures.py`
- `scripts/tests/test_linkedin_content_os_checkin.py`
- `scripts/tests/test_linkedin_content_os_cli.py`
- `scripts/tests/fixtures/linkedin_content_os/legacy-posted-log.jsonl`
- `scripts/tests/fixtures/linkedin_content_os/outcomes.jsonl`
- `scripts/tests/fixtures/linkedin_content_os/focus-sources.json`
- `scripts/tests/fixtures/linkedin_content_os/proof-records.jsonl`

### Generated Program 0 artifacts

- `memory/content/linkedin-content-os/focus-snapshot.v1.json`
- `memory/content/linkedin-content-os/run-context.v1.json`
- `memory/content/linkedin-content-os/run-context.phase-2-authority.v1.json`
- `memory/content/linkedin-content-os/mission-control.snapshot.v1.json`
- `memory/content/linkedin-content-os/historical-audit.v1.json`
- `memory/content/linkedin-content-os/historical-recovery-request.v1.json`
- `memory/content/linkedin-content-os/human-gate-response.v1.json`
- `memory/content/linkedin-content-os/outcomes.v1.jsonl`
- `memory/content/linkedin-content-os/corpus-authority-manifest.v1.json`
- `memory/content/linkedin-content-os/source-policy.v1.json`
- `memory/content/linkedin-content-os/voice-rule-retirements.v1.json`
- `memory/content/linkedin-content-os/voice-gold.v0.jsonl`
- `memory/content/linkedin-content-os/contrastive-pairs.v0.jsonl`
- `memory/content/linkedin-content-os/evaluation-fixtures.v0.jsonl`
- `memory/content/linkedin-content-os/checkin.preview.v1.json`
- `memory/content/linkedin-content-os/boundaries.phase-1.before.v1.json`
- `memory/content/linkedin-content-os/boundaries.phase-1.after.v1.json`
- `memory/content/linkedin-content-os/boundaries.phase-2.before.v1.json`
- `memory/content/linkedin-content-os/boundaries.phase-2.after.v1.json`
- `reports/growth-os/2026-09-28-linkedin-content-os-program-0.md`

### Existing files read but never rewritten by Program 0

- `memory/content/posted-log.jsonl`
- `memory/content/edit-deltas.jsonl`
- `memory/content/current-efforts.md`
- `memory/north-star/active-this-week.md`
- `memory/north-star/revenue-command-center.md`
- `memory/pipeline.jsonl`
- `memory/job-state/job-market-daily-research.md`
- `mission-control/docs/mission-control-lane-packet-contract.md`
- `mission-control/lib/mission-control/lane-packet.ts`
- `mission-control/lib/mission-control/lane-packet-transitions.ts`

### Existing owner files updated during Program 0

- `docs/agents/content-rules.md` — remove fixed-day/fixed-shape LinkedIn rules superseded by the reconciled gold-set and gate contract.
- `memory/content-voice.md` — preserve verified voice evidence while retiring fixed weekly format/quota language as generation authority.
- `skills/wednesday-linkedin/SKILL.md` — repair through `skill_workshop`, never by direct file write, to remove the retired 5:1 pronoun ratio and fixed prose/length/day requirements.

## Requirements traceability

| Reconciled Program 0 requirement | Plan owner | Acceptance evidence |
|---|---|---|
| Replace stale current-effort input | Task 5 | Hash-bound proposed focus snapshot and staleness tests |
| Treat legacy `posted:false` as unknown | Tasks 2–3 | Contract + audit tests and status counts |
| Recover possible posts, URLs, and final text | Tasks 3, 7A, 7B, 10 | Bounded recovery request; typed answer ingestion; rebuilt audit/corpus |
| Build exact voice gold and contrastive pairs | Task 6 | Exact-text/hash-only corpus tests and counts |
| Keep corpus authority independently anchored | Tasks 3, 6, 7B, 10 + verifier | Phase-2 authority context digest equals canonical manifest hash and the exact digest consumed by audit and both corpus builders |
| Classify allowed/prohibited source families | Task 8 | Versioned source policy and owner bindings |
| Encode quality/fit diagnosis | Tasks 2, 8, 10 | Closed decline reason, retirement artifact, final report |
| Build positive/negative evaluation evidence | Tasks 7, 7A, 7B | Exact Git/path/SHA-256-bound candidates; permission gap blocks closure |
| Retire conflicting legacy voice rules | Task 8 | Owner-file changes, `skill_workshop` repair, regression tests |
| Derive one check-in without a second lifecycle | Tasks 4, 9 | Read-only MC snapshot + outcome ledger + zero-or-one projector tests |
| No live or external action | Tasks 4, 10 + verifier | Network denial, before/after boundary equality, fresh verifier verdict |

---

## Chunk 1: Canonical truth and historical audit

### Task 1: Create the Program 0 package and canonical file primitives

**Files:**
- Create: `scripts/linkedin_content_os/__init__.py`
- Create: `scripts/linkedin_content_os/canonical.py`
- Create: `scripts/tests/test_linkedin_content_os_canonical.py`
- Modify: `tasks/todo.md`

- [ ] **Step 1: Record the execution checklist before implementation**

Add one Program 0 section to `tasks/todo.md` listing Tasks 1–10 from this plan and the hard stop: `No external network, Mission Control write, deployment, cron, provider call, asset generation, or publication. Exactly four read-only loopback task snapshots are allowed: one before/after pair around each side of the human gate.`

- [ ] **Step 2: Write failing canonicalization tests**

Cover deterministic UTF-8 JSON serialization with sorted keys and compact separators, SHA-256 over exact canonical bytes, strict JSONL refusal on blank/corrupt/non-object rows, atomic whole-file writes, and exact-prefix-preserving JSONL appends.

- [ ] **Step 3: Run the focused tests and verify RED**

Run: `python3 -m unittest scripts.tests.test_linkedin_content_os_canonical -v`

Expected: FAIL because `scripts.linkedin_content_os.canonical` does not exist.

- [ ] **Step 4: Implement the minimal primitives**

Expose only:

```python
canonical_bytes(value: object) -> bytes
sha256_hex(value: bytes) -> str
read_jsonl(path: Path) -> list[dict[str, object]]
write_json_atomic(path: Path, value: object) -> None
append_jsonl_exact_prefix(path: Path, row: dict[str, object]) -> None
```

`append_jsonl_exact_prefix` must re-read the prior bytes after the append and prove they are an exact prefix. On failure it restores the original bytes and raises.

- [ ] **Step 5: Verify GREEN and commit**

Run: `python3 -m unittest scripts.tests.test_linkedin_content_os_canonical -v`

Expected: PASS.

Commit: `git commit -m "feat: add LinkedIn content canonical primitives"`

### Task 2: Define closed Program 0 contracts

**Files:**
- Create: `scripts/linkedin_content_os/contracts.py`
- Create: `scripts/linkedin_content_os/outcomes.py`
- Create: `scripts/tests/test_linkedin_content_os_outcomes.py`
- Create: `scripts/tests/fixtures/linkedin_content_os/outcomes.jsonl`

- [ ] **Step 1: Write failing contract tests**

Require these exact closed values:

```python
HISTORICAL_STATUS = {"posted_confirmed", "not_posted_confirmed", "status_unknown"}
OUTCOME_EVENT = {
    "historical_status", "publication_acknowledged", "publication_deferred",
    "publication_declined", "final_text_captured", "metric_snapshot",
    "qualified_reply", "commercial_outcome", "focus_decision",
    "permission_fixture_accepted", "correction"
}
DECLINE_REASON = {"quality_fit", "stale", "timing", "other"}
CLAIM_ATTRIBUTION = {"public_fact", "vendor_assertion", "jt_verified_fact", "hypothesis"}
```

Every record must include `schemaVersion`, stable ID, `recordedAt`, source pointer, canonical `eventSha256`, and only schema-supported fields. Unknown fields fail closed.

- [ ] **Step 2: Verify RED**

Run: `python3 -m unittest scripts.tests.test_linkedin_content_os_outcomes -v`

Expected: FAIL because validators and the ledger do not exist.

- [ ] **Step 3: Implement strict validators**

Use plain functions and typed dictionaries compatible with Python 3.9. Do not add Pydantic or another dependency. Timestamps must be timezone-aware ISO 8601 strings; hashes must be 64 lowercase hex; URLs must be HTTPS LinkedIn URLs when an event claims publication.

- [ ] **Step 4: Add append-only outcome behavior**

Create `scripts/linkedin_content_os/outcomes.py` with:

```python
append_event(path: Path, event: dict[str, object]) -> Literal["appended", "replayed"]
load_events(path: Path) -> list[dict[str, object]]
```

Exact `outcomeEventId + eventSha256` replay is idempotent. Reusing an ID with different bytes, regressing per-packet timestamps, or changing an earlier prefix fails closed.

- [ ] **Step 5: Verify and commit**

Run: `python3 -m unittest scripts.tests.test_linkedin_content_os_outcomes -v`

Expected: PASS, including replay, conflict, timestamp-order, and prefix-preservation cases.

Commit: `git commit -m "feat: add append-only LinkedIn outcome contracts"`

### Task 3: Audit legacy LinkedIn history without rewriting it

**Files:**
- Create: `scripts/linkedin_content_os/historical_audit.py`
- Create: `scripts/tests/test_linkedin_content_os_historical_audit.py`
- Create: `scripts/tests/fixtures/linkedin_content_os/legacy-posted-log.jsonl`
- Generate later: `memory/content/linkedin-content-os/historical-audit.v1.json`

- [ ] **Step 1: Write failing classification tests**

Fixtures must prove:

- a LinkedIn row with `posted:true` and a valid public URL becomes `posted_confirmed`;
- a LinkedIn row with `posted:true` and explicit JT confirmation but a missing URL remains `posted_confirmed` with `missing:["public_url","final_text"]`;
- every legacy `posted:false` row becomes `status_unknown`, never `not_posted_confirmed`;
- `not_posted_confirmed` requires an explicit governed decline/no-action event;
- X rows are excluded;
- duplicate legacy rows are reported, not silently merged;
- each audit row carries `legacyRowSha256` rather than a mutable line-number identity.

- [ ] **Step 2: Verify RED**

Run: `python3 -m unittest scripts.tests.test_linkedin_content_os_historical_audit -v`

Expected: FAIL because the audit module does not exist.

- [ ] **Step 3: Implement the read-only classifier**

Expose:

```python
audit_legacy_rows(posted_log: Path, outcomes: Optional[Path], generated_at: str, corpus_authority_manifest: Optional[dict[str, object]] = None, expected_manifest_sha256: Optional[str] = None) -> dict[str, object]
```

The output includes source file hash, counts by status, missing-field counts, duplicate groups, raw-posted provenance, and one canonical audit record per LinkedIn row. One shared `expected_recovery_items(records)` algorithm emits `historical-recovery-request.v1.json`, capped to all `posted:true` rows missing URL/final text plus the 20 most recent unique `status_unknown` LinkedIn rows, with exact topic/date/legacy-row-hash and the three allowed answers: `posted` with required URL and optional exact final text, `not_posted`, or `still_unknown`. Pre-gate output includes the fixed explicit empty, run-bound `corpusAuthorityManifest` and permits a missing expected digest only for that empty anchor. After Task 7B, a populated manifest is accepted only when its canonical hash exactly matches the separately supplied `expected_manifest_sha256`; the expected digest may not be derived from the manifest, audit, or outcome ledger. It must not write to `posted-log.jsonl` or infer public status from scheduling, Drive, or Notion fields.

- [ ] **Step 4: Add mutation and reproducibility guards**

Hash `posted-log.jsonl` before and after the run and fail if it changes. Run the audit twice and assert byte-identical canonical output when `generatedAt` is supplied explicitly.

- [ ] **Step 5: Verify and commit**

Run: `python3 -m unittest scripts.tests.test_linkedin_content_os_historical_audit -v`

Expected: PASS.

Commit: `git commit -m "feat: audit LinkedIn publication history"`

---

## Chunk 2: Current focus, voice corpus, and evaluation fixtures

### Task 4: Capture and validate the read-only Mission Control packet snapshot

**Files:**
- Create: `scripts/linkedin_content_os/mc_snapshot.py`
- Create: `scripts/tests/test_linkedin_content_os_mc_snapshot.py`
- Generate later: `memory/content/linkedin-content-os/mission-control.snapshot.v1.json`

- [ ] **Step 1: Write failing snapshot tests**

Mock the transport and require exactly one request: `GET http://127.0.0.1:3000/api/tasks`. Reject redirects, non-loopback hosts, methods other than GET, capability/auth headers, non-JSON responses, duplicate task IDs, and snapshots missing a source SHA-256. Select LinkedIn lane packets only when `packetSchema == "lane-packet-v1"`, `growthLane == "linkedin"`, `approvalState == "approved"`, and `approvedPayloadHash == payloadHash`. Preserve two explicitly typed projections: nonterminal packets eligible for publication acknowledgment, and terminal `completed` packets whose typed closure points to a governed `publication_acknowledged` outcome and may still require the one-time seven-day metrics snapshot. All other terminal packets are excluded.

- [ ] **Step 2: Verify RED**

Run: `python3 -m unittest scripts.tests.test_linkedin_content_os_mc_snapshot -v`

Expected: FAIL because the snapshot module does not exist.

- [ ] **Step 3: Implement exact capture and validation**

Expose:

```python
capture_tasks(url: str = "http://127.0.0.1:3000/api/tasks") -> bytes
validate_snapshot(raw: bytes, run_context: dict[str, object]) -> dict[str, object]
approved_linkedin_packets(snapshot: dict[str, object]) -> list[dict[str, object]]
```

The canonical snapshot wrapper stores `schemaVersion`, `runId`, `capturedAt`, `validUntil`, `sourceUrl`, `rawSha256`, total task count, LinkedIn lane-packet count, and only the minimum filtered LinkedIn projection required by the check-in projector: task ID, status, approval state, packet/payload hashes, content ID, expiry, closure type, and closure outcome pointer. It never stores unrelated task bodies. A snapshot is valid only when its `runId` exactly matches `run-context.v1.json`, `capturedAt` equals that context's `generatedAt`, `validUntil` equals `capturedAt + 2 hours`, and the consuming command runs no later than `validUntil`; any mismatch or later-run reuse fails closed. It is read-only input; Program 0 does not call a PATCH/POST route.

- [ ] **Step 4: Add network-denial regression coverage**

Use a deny-by-default process runner and patch `subprocess.Popen`, `subprocess.run`, `subprocess.call`, `subprocess.check_call`, and `subprocess.check_output` in every test. The only allowed child-process argvs are the read-only Git extraction `git --git-dir <validated-path> show <40-hex-commit>:<validated-relative-path>` for `build-fixtures` and `ingest-human-gate`, plus `openclaw cron list --json` for `capture-boundaries`; no shell, environment override, write command, ref mutation, or alternate argv is accepted. Enforce network denial independently by patching `socket.socket.connect`, `socket.create_connection`, and `urllib.request.urlopen` in every non-capture CLI test. The capture test permits only the mocked exact loopback GET and proves no second request occurs.

- [ ] **Step 5: Verify and commit**

Run: `python3 -m unittest scripts.tests.test_linkedin_content_os_mc_snapshot -v`

Expected: PASS.

Commit: `git commit -m "feat: validate LinkedIn Mission Control snapshot"`

### Task 5: Build a hash-bound current-focus snapshot

**Files:**
- Create: `scripts/linkedin_content_os/focus.py`
- Create: `scripts/tests/test_linkedin_content_os_focus.py`
- Create: `scripts/tests/fixtures/linkedin_content_os/focus-sources.json`
- Generate later: `memory/content/linkedin-content-os/focus-snapshot.v1.json`

- [ ] **Step 1: Write failing focus tests**

The snapshot contract is:

```json
{
  "schemaVersion": "linkedin-focus-snapshot.v1",
  "snapshotId": "sha256:<64 lowercase hex>",
  "generatedAt": "timezone-aware ISO 8601",
  "validUntil": "timezone-aware ISO 8601",
  "targets": [{
    "targetId": "stable slug",
    "kind": "consulting|career|product",
    "label": "human-readable target",
    "desiredOutcome": "bounded outcome",
    "sourceRefs": [{"path":"...","sha256":"..."}]
  }],
  "prohibitedPremises": ["internal_machinery"],
  "status": "proposed"
}
```

Tests must reject zero targets, unsupported kinds, unhashable sources, stale snapshots, duplicate target IDs, `confirmed` without a valid `focus_decision` event, and any status outside `proposed|confirmed`. The pre-gate build is always `proposed`. After response ingestion, `confirmed` is derived only from JT's hash-bound `focus_decision`; a corrected decision deterministically applies the validated correction set and emits a new snapshot ID.

- [ ] **Step 2: Verify RED**

Run: `python3 -m unittest scripts.tests.test_linkedin_content_os_focus -v`

Expected: FAIL because the focus builder does not exist.

- [ ] **Step 3: Implement deterministic focus assembly**

Read only the allowlisted canonical owner files listed in the file map. Each target must cite the exact owner path and file hash. Conflicting owner facts produce a report error; prose is never silently reconciled by a model. Without a `focus_decision` event the output status is `proposed`; with a matching confirmed/corrected event it is deterministically rebuilt as `confirmed` and bound to that event hash.

- [ ] **Step 4: Prove freshness behavior**

`validUntil` is configuration, not a permanent threshold. For Program 0 set it to 30 days from `generatedAt`; stale snapshots block later packet admission and produce one renewal need, not an automatic rewrite.

- [ ] **Step 5: Verify and commit**

Run: `python3 -m unittest scripts.tests.test_linkedin_content_os_focus -v`

Expected: PASS.

Commit: `git commit -m "feat: build LinkedIn focus snapshot"`

### Task 6: Build voice gold only from exact final LinkedIn text

**Files:**
- Create: `scripts/linkedin_content_os/corpus.py`
- Create: `scripts/tests/test_linkedin_content_os_corpus.py`
- Generate later: `memory/content/linkedin-content-os/voice-gold.v0.jsonl`
- Generate later: `memory/content/linkedin-content-os/contrastive-pairs.v0.jsonl`

- [ ] **Step 1: Write failing corpus tests**

Accept a gold example only when a `posted_confirmed` outcome resolves to exact final published text and its SHA-256. Reject summaries, draft text, placeholder URLs, inferred zero edits, duplicate text hashes, and text without provenance. A contrastive pair requires exact draft text, exact JT-final text, both hashes, and a typed edit reason.

- [ ] **Step 2: Verify RED**

Run: `python3 -m unittest scripts.tests.test_linkedin_content_os_corpus -v`

Expected: FAIL because the corpus builder does not exist.

- [ ] **Step 3: Implement corpus derivation**

Expose:

```python
build_voice_gold(audit: dict[str, object], events: list[dict[str, object]], *, expected_manifest_sha256: Optional[str]) -> list[dict[str, object]]
build_contrastive_pairs(events: list[dict[str, object]], audit: Optional[dict[str, object]] = None, *, expected_manifest_sha256: Optional[str]) -> list[dict[str, object]]
```

Empty output is valid and must surface a blocking gap count. Never fall back to `summary`, `memory/content-voice.md`, or an old draft as though it were published text.

Exact text is eligible only through a `corpus_authority_receipt` whose event SHA-256 is listed in the audit's independently supplied, run-bound `corpusAuthorityManifest`. The manifest binds the human-gate authority bytes, exact outcome-ledger prefix and position, sorted receipt allowlist, validation time, and canonical manifest hash. Both corpus builders require a separately supplied expected manifest digest and compare it before trusting the audit manifest. The pre-gate audit contains the fixed explicit empty manifest and uses `None` only for that empty anchor. A text event, matching receipt, and self-hashed manifest cannot self-authorize by mutually agreeing when the external expected digest differs or is missing.

- [ ] **Step 4: Add deterministic origin caps**

Program 0 records at most one copy of a text hash and tags origin as `jt_published`, `jt_authored`, or `jt_edit_pair`. External mechanics prose and model-generated examples are excluded.

- [ ] **Step 5: Verify and commit**

Run: `python3 -m unittest scripts.tests.test_linkedin_content_os_corpus -v`

Expected: PASS.

Commit: `git commit -m "feat: derive LinkedIn voice gold corpus"`

### Task 7: Select Program 0 evaluation fixtures without generating posts

**Files:**
- Create: `scripts/linkedin_content_os/fixtures.py`
- Create: `scripts/tests/test_linkedin_content_os_fixtures.py`
- Create: `scripts/tests/fixtures/linkedin_content_os/proof-records.jsonl`
- Generate later: `memory/content/linkedin-content-os/evaluation-fixtures.v0.jsonl`

- [ ] **Step 1: Write failing fixture tests**

Require:

- one negative internal-machinery fixture bound to the Decagon example;
- one positive build-proof source selected only from `approved-anonymized` or `approved-named` proof with claim-level facts and non-expired permission;
- no generated post copy and no generated image;
- teardown and AI-news placeholders are prohibited; missing evidence is an explicit gap, not a fabricated fixture;
- deterministic selection order: permission sufficiency, claim specificity, freshness, stable proof ID.
- generated evidence may never cite `scripts/tests/fixtures/` as an authoritative source.

- [ ] **Step 2: Verify RED**

Run: `python3 -m unittest scripts.tests.test_linkedin_content_os_fixtures -v`

Expected: FAIL because fixture selection does not exist.

- [ ] **Step 3: Implement source-fixture selection**

Output source/evidence fixtures only. The negative fixture is the exact repository file `mission-control/lib/mission-control/fixtures/jobs/decagon-agent-development-manager.packet.json`, bound to payload hash `cd252d0ca23652adc7a7395ac7dafa97c7e56323dbc92609da3a6eb257644974`. The current positive candidate is the jt-ops Git object at commit `cd3e17f5287a64dbfedc27e1d2153d89250ba02c`, path `evidence/cohort-two.proof-asset.json`, blob `02c53107260317f6eb31b2d8cc742b9b357ccadf`. Because that card lacks an accepted permission record, the initial generated artifact must label it `gap:permission_missing`, not positive. Each record contains `mode`, classification (`positive`, `negative`, or `gap`), immutable source refs, Git object ID, SHA-256 of the exact extracted bytes, permission state, expected gate result, and failure reason where applicable. The SHA-1-sized Git blob ID is provenance only and never substitutes for the content SHA-256.

- [ ] **Step 4: Add fail-closed cases**

Reject client facts with `internal-only` permission, expired permission, missing claim bindings, active prospect/employer conflict, or a protected internal premise.

- [ ] **Step 5: Verify and commit**

Run: `python3 -m unittest scripts.tests.test_linkedin_content_os_fixtures -v`

Expected: PASS.

Commit: `git commit -m "feat: add LinkedIn evaluation source fixtures"`

---

### Task 7A: Stop at the explicit JT human gate

**Files:**
- Generate: `memory/content/linkedin-content-os/human-gate-response.v1.json` (JT-supplied structured response; never inferred)
- Modify: `tasks/todo.md`

- [ ] **Step 1: Produce the decision packet and stop**

Present the proposed focus snapshot, every bounded historical-recovery row, and the permission-gap record to JT. Do not mark Program 0 complete and do not proceed to the final verifier. The required response contract is:

```json
{
  "schemaVersion": "linkedin-human-gate-response.v1",
  "recoveryRequestSha256": "<64 lowercase hex>",
  "focusSnapshotSha256": "<64 lowercase hex>",
  "fixtureGapSha256": "<64 lowercase hex>",
  "focusDecision": {"decision": "confirmed"},
  "historyAnswers": ["answer-specific closed objects described below"],
  "permissionedFixture": {
    "proofId": "stable proof ID",
    "gitDir": "validated absolute .git path",
    "commit": "40 lowercase hex",
    "path": "validated repository-relative path",
    "contentSha256": "64 lowercase hex of extracted bytes",
    "permissionEvidenceRef": "immutable reference",
    "permissionEvidenceSha256": "64 lowercase hex",
    "permissionStatus": "approved-anonymized|approved-named"
  },
  "confirmedAt": "timezone-aware ISO 8601"
}
```

`focusDecision` is also a closed, null-free union. Confirmation is exactly `{"decision":"confirmed"}`. Correction is `{"decision":"corrected","correctedTargets":[...]}` where `correctedTargets` is a complete replacement list using the Task 5 target schema; every `sourceRefs` path must be on the existing allowlist and its SHA-256 must match current bytes. Partial patch operations, free-form fields, unbound sources, and empty target lists fail closed. Every recovery row must receive exactly one answer using one closed, null-free shape: `{"legacyRowSha256":"…","answer":"posted","publicUrl":"https://www.linkedin.com/…"}` with optional `finalText` omitted when unavailable; `{"legacyRowSha256":"…","answer":"not_posted","declineReason":"quality_fit|stale|timing|other"}`; or `{"legacyRowSha256":"…","answer":"still_unknown"}`. A posted answer without final text creates `posted_confirmed` plus `missing:["final_text"]`; edit distance stays `unknown`. Empty or partial response files fail closed. The permissioned fixture must resolve by the exact read-only Git command to bytes matching `contentSha256`; `permissionEvidenceRef` is a JSON Pointer inside those same immutable bytes, and the canonical pointed value must match `permissionEvidenceSha256` and show non-expired permission. The existing `gap:permission_missing` candidate is not acceptable. If no such proof already exists, Program 0 remains paused; authoring new jt-ops permission evidence is a separately reviewed and authorized write, not hidden inside this plan.

- [ ] **Step 2: Record the pause**

Update `tasks/todo.md` with the exact response path and blocked conditions. No Mission Control task is created by Program 0.

### Task 7B: Ingest JT's response, rebuild truth, and prove the human gate closed

**Files:**
- Create: `scripts/linkedin_content_os/recovery.py`
- Create: `scripts/tests/test_linkedin_content_os_recovery.py`
- Append: `memory/content/linkedin-content-os/outcomes.v1.jsonl`
- Generate: `memory/content/linkedin-content-os/corpus-authority-manifest.v1.json`
- Generate: `memory/content/linkedin-content-os/run-context.phase-2-authority.v1.json`
- Regenerate: focus, audit, corpus, and fixture artifacts

- [ ] **Step 1: Write failing response-ingestion tests**

Prove complete coverage, exact request/focus/fixture-gap hash matching, focus correction validation, required URL with optional exact final text, typed decline reasons, null/unknown-field refusal, idempotent exact replay, conflicting-replay refusal, non-expired permission evidence, and exact-prefix-preserving ledger append.

- [ ] **Step 2: Implement and run ingestion**

Expose `ingest_human_gate(response, request, focus, fixture_gap, ledger)`. Append `historical_status` events carrying `posted_confirmed`, `not_posted_confirmed`, or `status_unknown`; one `focus_decision` event carrying `confirmed` or `corrected`; one `permission_fixture_accepted` event; and exact-text authority receipts where complete publication text is supplied. Independently emit `corpus-authority-manifest.v1.json` from the validated human-gate boundary, never by projecting the outcome ledger. It must bind the run ID, human-gate response receipt SHA-256, exact appended-ledger prefix SHA-256/position, sorted authority-receipt event hashes, validation timestamp, and canonical manifest SHA-256. At that same authority boundary, emit an immutable phase-2 authority run context derived from the input run context and carrying `corpusAuthorityManifestSha256`; later audit/corpus commands read the expected digest only from this context and never derive it from the audit, manifest, receipts, or events. Bind the accepted proof fixture to exact repository/commit/path, extracted-byte SHA-256, immutable permission evidence hash, and permission expiry. Never mutate the legacy posted log.

- [ ] **Step 3: Rebuild and assert closure prerequisites**

Re-run audit with the independently emitted manifest and the expected digest from `run-context.phase-2-authority.v1.json`, then pass that same independently supplied expected digest to both voice-gold and contrastive-pair builders. Rebuild focus, corpus, and fixtures from the updated ledger. Program 0 closure prerequisites at this point are: no unanswered bounded recovery rows; a JT-confirmed focus snapshot; one `positive` permissioned fixture and one `negative` fixture; and all remaining unknowns explicitly labeled, never coerced to zero or false. Task 10 builds and verifies the check-in preview after Task 9 creates the projector.

- [ ] **Step 4: Verify and commit**

Run: `python3 -m unittest scripts.tests.test_linkedin_content_os_recovery -v`

Expected: PASS, including idempotent replay and fail-closed permission cases.

Commit: `git commit -m "feat: ingest LinkedIn Program 0 human gate"`

---

### Task 8: Encode source-family policy and retire conflicting legacy voice rules

**Files:**
- Create: `scripts/linkedin_content_os/source_policy.py`
- Create: `scripts/linkedin_content_os/voice_rules.py`
- Create: `scripts/tests/test_linkedin_content_os_source_policy.py`
- Create: `scripts/tests/test_linkedin_content_os_voice_rules.py`
- Modify: `docs/agents/content-rules.md`
- Modify: `memory/content-voice.md`
- Repair through `skill_workshop`: `skills/wednesday-linkedin/SKILL.md`
- Generate later: `memory/content/linkedin-content-os/source-policy.v1.json`
- Generate later: `memory/content/linkedin-content-os/voice-rule-retirements.v1.json`

- [ ] **Step 1: Write failing policy and retirement tests**

Require the exact allowed families `client_delivery`, `field_lesson`, `engineering_recipe`, `teardown_trigger`, and `ai_event`; prohibit `internal_machinery`. Bind each family to its canonical owner and evidence rules. Regression tests must fail while any owner still enforces the retired 5:1 pronoun ratio, mandatory Wednesday publication/case-study shape, universal 150–250-word prose-only format, or fixed weekly LinkedIn quota.

- [ ] **Step 2: Verify RED**

Run: `python3 -m unittest scripts.tests.test_linkedin_content_os_source_policy scripts.tests.test_linkedin_content_os_voice_rules -v`

Expected: FAIL because policy modules do not exist and legacy conflicting rules remain.

- [ ] **Step 3: Implement source-family ownership**

Each family record includes `family`, `status`, `owner`, required evidence, conflict checks, permission rule, and source freshness rule. The exact owners are:

- `client_delivery` -> immutable jt-ops proof-asset Git object plus its permission evidence;
- `field_lesson` -> JT-confirmed field-note or append-only outcome event;
- `engineering_recipe` -> accepted verifier claim plus execution artifact, after protected-purpose removal;
- `teardown_trigger` -> primary public source plus consulting suppression/client/prospect and job/employer conflict owners;
- `ai_event` -> X Intelligence Router when proven, otherwise a JT-supplied or approved primary public source plus one bound JT artifact;
- `internal_machinery` -> prohibited, with no owner able to override it implicitly.

`engineering_recipe` never makes `internal_machinery` publishable.

- [ ] **Step 4: Retire conflicting voice rules at their owner surfaces**

Update `docs/agents/content-rules.md` and `memory/content-voice.md` so exact JT-final LinkedIn text, evidence safety, and the reconciled gates outrank fixed-day/format mechanics. Use `skill_workshop` to read and patch `wednesday-linkedin`; do not edit its file directly. Preserve useful buyer-confidence, factuality, and proof-specificity rules.

The retirement artifact records old rule, owner surface, replacement rule, reason, regression test, and effective date. It also records the durable diagnosis `historicalBottleneck:"quality_fit"` and `legacyPostedFalseAuthority:"status_unknown"`.

- [ ] **Step 5: Verify and commit**

Run: `python3 -m unittest scripts.tests.test_linkedin_content_os_source_policy scripts.tests.test_linkedin_content_os_voice_rules -v`

Expected: PASS. No generated source-policy or fixture record may cite `scripts/tests/fixtures/` as authoritative evidence.

Commit: `git commit -m "docs: reconcile LinkedIn source and voice rules"`

---

## Chunk 3: One check-in projection and Program 0 proof

### Task 9: Locally prove the single deduplicated check-in contract

**Files:**
- Create: `scripts/linkedin_content_os/checkin.py`
- Create: `scripts/tests/test_linkedin_content_os_checkin.py`
- Generate later: `memory/content/linkedin-content-os/checkin.preview.v1.json`

- [ ] **Step 1: Write failing projection tests**

The pure projector must return zero or one universal-task preview with stable dedupe key `linkedin-checkin:v1`. Cover:

1. no unresolved items -> no task;
2. approval exists only in the hash-bound Mission Control snapshot; an outcome event alone cannot create an approved packet;
3. one or many approved packets without outcomes -> one aggregated publication acknowledgment task;
4. `not_yet` -> same task identity and next eligible self due date, no new packet;
5. `posted` -> requires a LinkedIn HTTPS URL and links the event to the original packet;
6. `wont_post` -> requires a closed decline reason and maps to governed `no-action` semantics;
7. seven days after posting -> the same task requests one bounded metrics snapshot;
8. no 24-hour metrics prompt;
9. missing performance -> `metrics_unknown`, never zero;
10. mixed publication and metrics gaps -> one task with ordered exact steps;
11. repeat projection -> byte-identical preview with no duplicate reminder row;
12. snapshot hash mismatch, changed approved payload, stale snapshot, or terminal packet without a matching typed publication closure -> fail closed or exclude the packet with a receipt;
13. a terminal completed packet with a matching hash-bound `publication_acknowledged` closure remains eligible only for its one-time seven-day metrics request and can never re-enter the publication-acknowledgment path.

- [ ] **Step 2: Verify RED**

Run: `python3 -m unittest scripts.tests.test_linkedin_content_os_checkin -v`

Expected: FAIL because the projector does not exist.

- [ ] **Step 3: Implement the pure projection**

Expose:

```python
project_checkin(
    mc_snapshot: dict[str, object],
    events: list[dict[str, object]],
    now: datetime,
) -> dict[str, object] | None
```

The preview uses the existing seven-field universal-card shape: `title`, `whyItMatters`, `exactSteps`, optional `pasteReadyPrompt`, optional `pasteDestination`, `doneState`, and append-only `feedback` excluded from producer input. It includes the source snapshot hash, `dueDate`, `dueDateSource:"self"`, project `LinkedIn Content OS`, assignee `jt`, and no lane-packet approval fields.

- [ ] **Step 4: Prove authority separation**

Tests must show the preview cannot mutate outcome state, cannot mark a packet posted, cannot complete a lane packet, and contains no capability, credential, or request command. Add an explicit `liveWriteAuthorized:false` field to the preview wrapper; this wrapper is not submitted to Mission Control.

- [ ] **Step 5: Verify and commit**

Run: `python3 -m unittest scripts.tests.test_linkedin_content_os_checkin -v`

Expected: PASS.

Commit: `git commit -m "feat: project LinkedIn outcome check-in"`

### Task 10: Add one local CLI and generate Program 0 artifacts

**Files:**
- Create: `scripts/linkedin_content_os/cli.py`
- Create: `scripts/linkedin_content_os/boundaries.py`
- Create: `scripts/tests/test_linkedin_content_os_cli.py`
- Generate: all Program 0 artifacts listed in the file map
- Create: `reports/growth-os/2026-09-28-linkedin-content-os-program-0.md`
- Modify: `tasks/todo.md`

- [ ] **Step 1: Write failing CLI tests**

Require exact subcommands:

```text
init-run
capture-boundaries
audit-history
ingest-human-gate
build-focus
build-corpus
build-fixtures
build-source-policy
audit-voice-rules
preview-checkin
verify
```

`init-run --generated-at now` captures one timestamp into `run-context.v1.json` and atomically creates an empty `outcomes.v1.jsonl` when absent; an existing ledger is preserved byte-for-byte. Every other artifact command requires that context and never calls the clock. All commands emit JSON to stdout. Each `capture-boundaries` invocation permits one exact read-only loopback GET. All other subcommands run under a socket deny guard and refuse external network or write-capable Mission Control URLs.

- [ ] **Step 2: Verify RED**

Run: `python3 -m unittest scripts.tests.test_linkedin_content_os_cli -v`

Expected: FAIL because the CLI does not exist.

- [ ] **Step 3: Implement the CLI and generate artifacts**

From the worktree root, run these exact commands in order:

```bash
python3 -m scripts.linkedin_content_os.cli init-run \
  --generated-at now \
  --outcomes memory/content/linkedin-content-os/outcomes.v1.jsonl \
  --output memory/content/linkedin-content-os/run-context.v1.json
python3 -m scripts.linkedin_content_os.cli capture-boundaries \
  --phase phase-1-before \
  --run-context memory/content/linkedin-content-os/run-context.v1.json \
  --output memory/content/linkedin-content-os/boundaries.phase-1.before.v1.json
python3 -m scripts.linkedin_content_os.cli audit-history \
  --posted-log memory/content/posted-log.jsonl \
  --outcomes memory/content/linkedin-content-os/outcomes.v1.jsonl \
  --run-context memory/content/linkedin-content-os/run-context.v1.json \
  --output memory/content/linkedin-content-os/historical-audit.v1.json \
  --recovery-output memory/content/linkedin-content-os/historical-recovery-request.v1.json
python3 -m scripts.linkedin_content_os.cli build-focus \
  --workspace-root . \
  --run-context memory/content/linkedin-content-os/run-context.v1.json \
  --output memory/content/linkedin-content-os/focus-snapshot.v1.json
python3 -m scripts.linkedin_content_os.cli build-corpus \
  --audit memory/content/linkedin-content-os/historical-audit.v1.json \
  --outcomes memory/content/linkedin-content-os/outcomes.v1.jsonl \
  --run-context memory/content/linkedin-content-os/run-context.v1.json \
  --gold-output memory/content/linkedin-content-os/voice-gold.v0.jsonl \
  --pairs-output memory/content/linkedin-content-os/contrastive-pairs.v0.jsonl
python3 -m scripts.linkedin_content_os.cli build-fixtures \
  --decagon-packet mission-control/lib/mission-control/fixtures/jobs/decagon-agent-development-manager.packet.json \
  --jt-ops-git-dir /Users/jtsomwaru/.openclaw/workspace/.worktrees/jt-ops-proof-asset/.git \
  --jt-ops-commit cd3e17f5287a64dbfedc27e1d2153d89250ba02c \
  --jt-ops-path evidence/cohort-two.proof-asset.json \
  --output memory/content/linkedin-content-os/evaluation-fixtures.v0.jsonl
python3 -m scripts.linkedin_content_os.cli capture-boundaries \
  --phase phase-1-after \
  --run-context memory/content/linkedin-content-os/run-context.v1.json \
  --output memory/content/linkedin-content-os/boundaries.phase-1.after.v1.json
```

The phase-1 `build-corpus` command must validate the base run context and the audit's fixed empty pre-gate authority manifest. Its tests and receipt must prove that the empty allowlist, zero authority/prefix hashes, zero ledger position, and canonical empty-manifest hash match the run ID; any populated manifest or non-empty authority field fails without a separately anchored expected digest.

**Stop here for Task 7A.** Send JT the focus snapshot, historical recovery request, and fixture-gap record. Resume only after `human-gate-response.v1.json` satisfies the contract. Then run:

```bash
python3 -m scripts.linkedin_content_os.cli init-run \
  --generated-at now \
  --outcomes memory/content/linkedin-content-os/outcomes.v1.jsonl \
  --output memory/content/linkedin-content-os/run-context.v1.json
python3 -m scripts.linkedin_content_os.cli capture-boundaries \
  --phase phase-2-before \
  --run-context memory/content/linkedin-content-os/run-context.v1.json \
  --mc-output memory/content/linkedin-content-os/mission-control.snapshot.v1.json \
  --output memory/content/linkedin-content-os/boundaries.phase-2.before.v1.json
python3 -m scripts.linkedin_content_os.cli ingest-human-gate \
  --response memory/content/linkedin-content-os/human-gate-response.v1.json \
  --recovery-request memory/content/linkedin-content-os/historical-recovery-request.v1.json \
  --focus memory/content/linkedin-content-os/focus-snapshot.v1.json \
  --fixtures memory/content/linkedin-content-os/evaluation-fixtures.v0.jsonl \
  --outcomes memory/content/linkedin-content-os/outcomes.v1.jsonl \
  --corpus-authority-manifest-output memory/content/linkedin-content-os/corpus-authority-manifest.v1.json \
  --authority-run-context-output memory/content/linkedin-content-os/run-context.phase-2-authority.v1.json \
  --run-context memory/content/linkedin-content-os/run-context.v1.json
python3 -m scripts.linkedin_content_os.cli audit-history \
  --posted-log memory/content/posted-log.jsonl \
  --outcomes memory/content/linkedin-content-os/outcomes.v1.jsonl \
  --corpus-authority-manifest memory/content/linkedin-content-os/corpus-authority-manifest.v1.json \
  --run-context memory/content/linkedin-content-os/run-context.phase-2-authority.v1.json \
  --output memory/content/linkedin-content-os/historical-audit.v1.json \
  --recovery-output memory/content/linkedin-content-os/historical-recovery-request.v1.json
python3 -m scripts.linkedin_content_os.cli build-focus \
  --workspace-root . \
  --outcomes memory/content/linkedin-content-os/outcomes.v1.jsonl \
  --run-context memory/content/linkedin-content-os/run-context.v1.json \
  --output memory/content/linkedin-content-os/focus-snapshot.v1.json
python3 -m scripts.linkedin_content_os.cli build-corpus \
  --audit memory/content/linkedin-content-os/historical-audit.v1.json \
  --outcomes memory/content/linkedin-content-os/outcomes.v1.jsonl \
  --run-context memory/content/linkedin-content-os/run-context.phase-2-authority.v1.json \
  --gold-output memory/content/linkedin-content-os/voice-gold.v0.jsonl \
  --pairs-output memory/content/linkedin-content-os/contrastive-pairs.v0.jsonl
python3 -m scripts.linkedin_content_os.cli build-fixtures \
  --decagon-packet mission-control/lib/mission-control/fixtures/jobs/decagon-agent-development-manager.packet.json \
  --human-gate-response memory/content/linkedin-content-os/human-gate-response.v1.json \
  --output memory/content/linkedin-content-os/evaluation-fixtures.v0.jsonl
python3 -m scripts.linkedin_content_os.cli build-source-policy \
  --run-context memory/content/linkedin-content-os/run-context.v1.json \
  --output memory/content/linkedin-content-os/source-policy.v1.json
python3 -m scripts.linkedin_content_os.cli audit-voice-rules \
  --run-context memory/content/linkedin-content-os/run-context.v1.json \
  --output memory/content/linkedin-content-os/voice-rule-retirements.v1.json
python3 -m scripts.linkedin_content_os.cli preview-checkin \
  --mc-snapshot memory/content/linkedin-content-os/mission-control.snapshot.v1.json \
  --outcomes memory/content/linkedin-content-os/outcomes.v1.jsonl \
  --run-context memory/content/linkedin-content-os/run-context.v1.json \
  --output memory/content/linkedin-content-os/checkin.preview.v1.json
python3 -m scripts.linkedin_content_os.cli capture-boundaries \
  --phase phase-2-after \
  --run-context memory/content/linkedin-content-os/run-context.v1.json \
  --output memory/content/linkedin-content-os/boundaries.phase-2.after.v1.json
python3 -m scripts.linkedin_content_os.cli verify \
  --workspace-root . \
  --run-context memory/content/linkedin-content-os/run-context.phase-2-authority.v1.json \
  --corpus-authority-manifest memory/content/linkedin-content-os/corpus-authority-manifest.v1.json \
  --phase-1-before memory/content/linkedin-content-os/boundaries.phase-1.before.v1.json \
  --phase-1-after memory/content/linkedin-content-os/boundaries.phase-1.after.v1.json \
  --phase-2-before memory/content/linkedin-content-os/boundaries.phase-2.before.v1.json \
  --phase-2-after memory/content/linkedin-content-os/boundaries.phase-2.after.v1.json \
  --report reports/growth-os/2026-09-28-linkedin-content-os-program-0.md
```

`capture-boundaries` records Mission Control task IDs/counts/lane-row hashes from the validated minimal snapshot, normalized cron-definition hash, LaunchAgent plist path/hash pairs, protected input hashes, and the primary-checkout fingerprint. Cron normalization retains only stable configuration fields (job ID, name, enabled state, schedule/timezone, session target, wake mode, payload/config hash, delivery mode/target) and excludes last/next-run timestamps, runtime state, durations, counters, and errors. It refuses secret-bearing values and records no raw environment or argv. The after command takes a fresh exact loopback GET and a fresh cron listing, normalizes it identically, then compares governed external configuration to the before artifact.

Preserve before/after SHA-256 values for every legacy input. Generate the report with:

- exact counts of `posted_confirmed`, `not_posted_confirmed`, and `status_unknown`;
- missing URL/final-text counts;
- current focus targets and source hashes;
- voice-gold and contrastive-pair counts;
- accepted/rejected/gap fixture counts;
- zero-or-one check-in preview result;
- human-gate resolution status; the final report must show zero unanswered bounded recovery rows, confirmed focus, and one permissioned positive fixture or refuse completion;
- explicit statement that no live or external action occurred.

The phase-2 CLI and final verifier must fail closed unless `run-context.phase-2-authority.v1.json.corpusAuthorityManifestSha256` equals the canonical `manifestSha256` recomputed from `corpus-authority-manifest.v1.json` and equals the exact `expected_manifest_sha256` supplied to the phase-2 audit, `build_voice_gold`, and `build_contrastive_pairs` calls. No command may derive that expected digest from the audit, manifest, receipts, or outcome ledger during corpus construction. The final report records the authority-context digest and recomputed canonical manifest hash as separate named fields plus the audit/gold/pairs consumption receipts that prove all four values are identical.

- [ ] **Step 4: Run the complete Program 0 verification matrix**

Run:

```bash
python3 -m unittest \
  scripts.tests.test_linkedin_content_os_canonical \
  scripts.tests.test_linkedin_content_os_outcomes \
  scripts.tests.test_linkedin_content_os_recovery \
  scripts.tests.test_linkedin_content_os_historical_audit \
  scripts.tests.test_linkedin_content_os_mc_snapshot \
  scripts.tests.test_linkedin_content_os_focus \
  scripts.tests.test_linkedin_content_os_source_policy \
  scripts.tests.test_linkedin_content_os_corpus \
  scripts.tests.test_linkedin_content_os_voice_rules \
  scripts.tests.test_linkedin_content_os_fixtures \
  scripts.tests.test_linkedin_content_os_checkin \
  scripts.tests.test_linkedin_content_os_cli -v
python3 -m unittest discover -s scripts/tests -v
git diff --check
```

Expected: all focused tests pass; the full script suite passes with no regression; `git diff --check` prints nothing.

- [ ] **Step 5: Prove no forbidden action and commit**

Verify from both phase-specific before/after boundary pairs, test output, and the Program 0 report:

- Mission Control task IDs/count and lane-packet row hashes are unchanged;
- the only HTTP requests were the four exact read-only loopback snapshots—one before/after pair per phase; external socket attempts fail in tests;
- normalized stable cron-definition hash and LaunchAgent path/hash inventory are unchanged;
- no Drive, Notion, provider, or LinkedIn write occurred;
- `memory/content/posted-log.jsonl` and `memory/content/edit-deltas.jsonl` hashes are unchanged;
- primary checkout fingerprint is unchanged if implementation uses an isolated worktree.

Mark the Program 0 checklist complete and commit:

`git commit -m "feat: complete LinkedIn Content OS Program 0"`

---

## Final independent verification gate

After Task 10, a fresh verifier must inspect the exact implementation commit and independently confirm:

1. legacy `posted:false` is never treated as confirmed non-publication;
2. the outcome ledger is append-only, idempotent, and conflict-safe;
3. gold text comes only from exact final LinkedIn text;
4. focus and fixtures are source-hash bound;
5. JT's human-gate response was completely ingested, the focus is confirmed, and a genuinely permissioned positive fixture exists alongside the negative fixture;
6. check-in projection emits at most one staged task and owns no content lifecycle;
7. no live Mission Control task, deployment, schedule, provider call, asset, or publication occurred;
8. all tests and diff checks pass from a clean checkout.
9. the phase-2 authority-context digest, recomputed canonical corpus-manifest hash, and exact expected digest consumed by the audit and both corpus builders are identical and independently traceable.

The verifier writes `memory/job-state/claims/linkedin-content-os-program-0-<implementation-commit>.md` with: implementation commit, inspected artifact hashes, every verification command and exit code, all four phase-boundary hashes, the separately named authority-context manifest digest and recomputed canonical manifest hash, the phase-2 audit/gold/pairs consumption-receipt hashes, findings, and an exact final verdict line `VERDICT: CONFIRM` or `VERDICT: REJECT`. Only `CONFIRM` closes Program 0. Program 1 planning then remains a separate gate for templates and the governed Mission Control delivery/check-in rail.
