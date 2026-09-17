# Cohort-two proof asset — evidence pack

**Status:** APPROVED_SENTENCE_B (was HUMAN_DECISION). Still nothing written to `jt-ops`, no PR opened, no `verified_by: jt` set.
**Date:** 2026-09-16
**Lane:** Claude evidence controller, read-only.
**Question asked:** `Approve this exact proof sentence?`
**JT answered 2026-09-16T17:43:29Z:** `APPROVE B`

**Approved exact sentence** (SHA-256 `d94efb4eaa09380a0ded63846c57228648ae9591bd9f1dcb698becb8db2455d8`):

> I built a workflow that runs on a daily schedule, sends staged certificate-of-insurance reminders automatically, and afterwards sends staff a digest of overdue follow-up, upcoming expirations, data issues, and recorded certificate status.

**What that approval is and is not.** It fixes the canonical wording. It is not the card's `verified_by`/`verified_at` attestation — that asserts JT verified the card against the live system — and it is not authorization to write `evidence/cohort-two.proof-asset.json`, open a PR, merge, activate, schedule, or send. Two things still block any canonical write:

1. **PR #33 is OPEN.** A card citing `514fbac` fails closed at `cohort_two_authority.py:2313` until it merges.
2. **PR #43 is OPEN** and commits the byte-identical *superseded* sentence with `verified_by: jt` already set, against an 11-node backup that does not match PR #33's 12-node live read. Its fate must be decided before a second card exists.

---

## 1. What was done

- Fresh clone of `jsomwarux/jt-ops` at `/Users/jtsomwaru/.cache/claude-evidence-20260916/jt-ops`. No existing worktree touched; clone left clean (`git status` empty).
- Read PR #33 read-only COI runtime evidence, the proof-card schema, the registry/pipeline contracts, the copy/voice/protected-client standards, the drafter prompt, and `scripts/cohort_two_authority.py` on current `origin/main`.
- Ran the repo's own mechanical guards against every candidate sentence.
- Ran one fresh independent adversarial evidence review (separate context, no priors).

## 2. Evidence base — paths, commits, hashes

**PR #33 — `verify/coi-live-runtime`, head `514fbacbfc289434bf8fdbba31df19e1a997741e`, state OPEN (NOT merged into main).**

| Path | Blob OID | SHA-256 |
|---|---|---|
| `reports/coi-live-runtime-verification.md` | `e67abf4fe043dfd8c01e2dce3e018aad4838127b` | `55ea5f21277312819dc4ca819e23a4b2eb662b7556b1936681b448c2b0862949` |
| `reports/evidence/coi-live-topology-redacted.json` | `a3024d57dfd3cdd78344cc044dd344f476cfb97b` | `bb0c5b0f0baf89ccadd90e4636a33337c1bb6d65e7dc40d2f11f505c521281ee` |

Both self-declared hashes **reproduce independently**:
- artifact SHA-256 matches the value the report claims (`bb0c5b0f…`);
- `REPORT_SELF_SHA256` recomputes to `09675a38702d829be0a0d932cd6ddbd5acee38a8514fe55d3a572792bba99ee3`, exactly as claimed.

**`origin/main` at `471e0d8cb0dbf7db8b01a235c8d26d7340328ce1`.**

| Path | Blob OID | SHA-256 |
|---|---|---|
| `schemas/proof_asset_card.schema.json` | `2835b9f64f4d3f2e3542ca689daff5caa3b0f948` | `bc8f9cd0999cf9ec5abc4bd0904e66ab902615acafbe38a0e9022560246bb177` |
| `schemas/registry.json` | `fec7872fc3893d6b62961fed8410c981ad2d6884` | `654e5af40515ddfe300cd10eff0195a8026db3a4ca0cbaaf50a214baede1c70a` |
| `docs/standards/outreach-copy-standard.md` | `b41d7716f6873b705714ba384db527daef29c6fb` | `7c04464214092d734bce9626c63bec4e8fde6daf6fe110af3fd91d03f97d851f` |
| `docs/cohort-two-contract-diff.md` | `c5ef854f07bf90f086d534276e106cc752b9f385` | `e7da88563492983a756182916227aee6875418c7ec51f351271eced722bd1fde` |
| `scripts/cohort_two_authority.py` | `0657852a7d8ac300b7fef8580396f98ccffc1ff3` | `e50753cfd152b3853d9657424eaf35a2efefc71180ad476336d5b87ec4dbdd0f` |

Live-system revision token (n8n's own change token for the published graph):
`042759ce-d4f4-4ee9-906e-cb34d9de28b7`. Workflow `AOQgsFtNHaNeaHPy`, `active: true`, 12 nodes, 11 directed edges.

## 3. The sentence proposed for test

> I built a workflow that sends certificate reminders on a daily schedule and gives staff a daily digest of overdue follow-up, upcoming expirations, data issues, and certificate status.

## 4. Clause-to-proof mapping

| # | Clause | Committed evidence | Support |
|---|---|---|---|
| C1 | "I built" | Not in PR #33 — that report is a read-only inspection and names no builder ("a human *configured* the templates…"). Repo-internal only: five cohort-1 briefs on main (`reports/cohort-1-briefs/*.md:57`) call it "built for a NYC property-operations client" as JT's proof point. | **Self-assertion, not corroborated.** `verified_by: jt` is a verification identity, not an authorship attestation. |
| C2 | "a workflow" | Workflow identity table; `active: true`, `isArchived: false`, 12 nodes, draft == published version. | **Exact** |
| C3 | "sends certificate reminders" | `Send Tenant Email` (Gmail v2.2), no `resource`/`operation` override → `message:send`; `DRY_RUN=false`, `ALLOW_PRODUCTION_CC=true` hardcoded in live code. | **Supported.** Two shadings: stage 1 is `initial_request`, not literally a reminder; recipient (external tenant) is omitted, which can leave a reader thinking no external party is contacted. |
| C4 | "on a daily schedule" | `Daily 7AM ET` `scheduleTrigger` v1.3, `triggerAtHour: 7`; 14 retained executions, every day 2026-08-28 → 2026-09-10, all `mode: trigger`, all `success`. | **True of the run, misleading about the tenant.** The escalation gates prove the opposite of daily contact: ≥14 days initial→followup, ≥7 days followup→final, at most one stage per run, hard stop after the third message. |
| C5 | "gives staff a daily digest" | `Send Daily Summary` → **four internal staff addresses**, "internal staff only. No external recipient." | **Supported, two caveats.** "Daily" is inferred from the daily trigger + 14/14 successful runs (execution payloads deliberately not fetched). "Gives" asserts receipt; delivery is an explicit non-capability (no bounce handling, no read receipt, no confirmation). |
| C6 | "overdue follow-up" | Digest contents: "overdue tenants needing personal outreach." | **Supported (paraphrase).** |
| C7 | "upcoming expirations" | Digest contents: "certificates expiring within 30 days." | **Supported; correctly vaguer** — "30" would be an unlicensed number. |
| C8 | "data issues" | Digest contents: "data issues (missing address, invalid date, per-row processing errors)"; classifier outcomes `skip_no_email`, `skip_bad_date`, `workflow_error`. | **Exact** |
| C9 | "certificate status" | Digest contents: "a certificate status breakdown table with percentages." | **Section exists; capability overstated.** Every value is human-typed spreadsheet content — the workflow never receives, opens, OCRs, parses or validates a certificate, and never detects replies. |

**Omissions are honest.** The digest has six items; the sentence lists four. The two dropped are "emails sent today" and "currently-expired counts". Neither omission overstates.

**The documented accuracy caveat is correctly avoided.** The report is emphatic that the digest's "Emails Sent Today" list is computed from classifier *intent*, not Gmail responses, so a send that fails after 3 retries still shows as sent — "Do not describe the digest as a record of confirmed sends." The proposed sentence never enumerates sends, counts, or delivery. **Clean on this point.**

## 5. Permission-safe wording

Copy standard (`docs/standards/outreach-copy-standard.md`) permits: *configured reminders send automatically*, *staff are copied concurrently*, *staff may receive a later digest*. It forbids any claim of pre-send human review, approval, release or sign-off.

**All mechanical guards pass** (run against the repo's own `scripts/cohort_two_authority.py`):

| Guard | Result |
|---|---|
| `PROHIBITED_CLAIMS` | no hit |
| `NUMBER_RE` | **zero digit tokens** → `claim_values: []` correct |
| `URL_RE` / `ATTACHMENT_RE` | no hit |
| `@` after NFKC normalisation / `MAIL_OBFUSCATION_RE` | no hit |
| `\bclient\b` | no hit |
| protected names (`Altmark`, `Marketsmith`, `MSI`, `SoberLife Coach`, `Aya`) | no hit |

**No leak** of client identity, private detail, or invented metric.

**Structural caveat that matters:** none of those guards actually runs on `outbound_text`. `cohort_two_authority.py:474` checks only that approved proof text is a non-empty string; `guard_draft` operates on the drafted subject+body. Per the contract diff: *"Schemas and hashes prove shape and byte identity. They do not prove truth or grant permission."* **Passing the guards is evidence of nothing about this sentence's honesty. That burden is entirely JT's.**

**Clause order is safe and deliberate** — send stated first, digest second. Reversing them would imply the digest precedes the send. Topology confirms the digest is a sibling off `Classify Tenants` output 0 position 1, with no edge into `IF send_email` or `Send Tenant Email`; `human_approval_nodes_on_either_path: 0`, `wait_nodes: 0`, `approval_or_form_nodes: 0`, `gmail_sendAndWait_operation_used: false`, `if_false_output_connected: false`.

**Connotation risk is real.** "Gives staff a … digest of overdue follow-up" describes a work queue, and the sentence drops the word "automatically" that the standard explicitly licenses. Cohort one shipped exactly this misread: five briefs on main say the system *"surfaces exceptions for human review, and keeps the approval on a person rather than the system."* PR #33 rules on that directly: **`# VERIFIED NO`**. This is a documented, shipped error, not a hypothetical.

## 6. Material conflict JT must resolve first — PR #43

**`eve/cohort-two-proof-asset`, head `cd3e17f5287a64dbfedc27e1d2153d89250ba02c`, OPEN, created 2026-09-16, adds `evidence/cohort-two.proof-asset.json` (blob `02c53107260317f6eb31b2d8cc742b9b357ccadf`, SHA-256 `4cca9c69d5430e0d08a16ff9d5ae7141fa2f277ce85196ed4aeb502658c99961`).**

It carries **byte-identical** `outbound_text` to the sentence under test, and **already sets `verified_by: "jt"` and `verified_at: "2026-09-16T00:00:00Z"`** — the exact attestation this lane is forbidden to make. Its PR body states "JT's wording, approved verbatim."

Four concrete discrepancies between PR #43 and PR #33's live evidence:

1. **Node count.** PR #43 says it verified against a workflow with **11 nodes**. PR #33's live read shows **12 nodes** (11 directed *edges*). The artifact PR #43 checked is not demonstrably the deployed graph.
2. **Verified against a backup, not the live system.** PR #43 says "read from a local byte-exact backup." The replan contract (`docs/plans/2026-09-14-cohort-two-simplified-replan.md:19`) requires a "canonical proof-asset card JT verified **against the live system**."
3. **`system_revision` is not the live token.** PR #43 uses `altmark-coi-expiration-tracking-final-2@AOQgsFtNHaNeaHPy/20260609T180228Z`. The report names the n8n change token as the active version id `042759ce-d4f4-4ee9-906e-cb34d9de28b7`; the embedded timestamp (18:02:28Z) also differs from the published version's creation time (18:03:18.056Z).
4. **Protected client name committed.** `Altmark` is in `outreach-protected-clients.json`. It never reaches buyer-facing copy (`system_revision` is not in `_draft_request`), and the name already appears in internal repo docs, so this is a **consistency note, not a mechanical violation** — but it runs against PR #33's own redaction discipline, which withheld the workflow name precisely because it contains a client name.
5. **Freshness.** The lane enforces `MAX_SOURCE_AGE = 30 days` on `proof.verified_at` (`cohort_two_authority.py:388`), not the 90-day window PR #43's body cites.

Git author on PR #43 is `JT Somwaru <jsomwarux@yahoo.com>` — the standard local git identity agents also use. **That is not proof JT personally attested.**

## 7. Fresh independent evidence review

**Verdict: `TIGHTEN_REQUIRED`.** No prohibited claim, no leak, no unlicensed number, no guard trip — but three wordings are substantive, not stylistic: "I built" is unevidenced, "on a daily schedule" supports a reader inference the escalation gates affirmatively disprove, and dropping "automatically" reopens the exact oversight misread that burned cohort one.

Three load-bearing structural claims from that review were independently re-verified here:
- `cohort_two_authority.py:2313` raises `LaneFinding("authority commit is not reachable from origin/main")` — **confirmed**. A card citing `514fbac` fails closed until PR #33 merges.
- `data/proof/` on main contains only `.gitkeep` — **confirmed**; no canonical card exists on main today.
- The cohort-1 "approval on a person" language — **confirmed** in five briefs at line 57.

One reviewer point is softened here: it treated "I built" as having no committed basis at all. Five cohort-1 briefs on main do assert the build as JT's proof point. That is repo-internal self-assertion, not independent corroboration — it lowers the novelty of the claim without closing the evidence gap.

## 8. Controller recommendation

The evidence does **not** support the starting sentence exactly, so per lane rules it is tightened rather than passed through. Every change below is bound to committed evidence; **no metric or claim is added**.

**Option A — as proposed (unchanged).** Guards clean. Accepts risks 2, 3, 4 and 5 below.

**Option B — tightened single sentence (recommended):**

> I built a workflow that runs on a daily schedule, sends staged certificate-of-insurance reminders automatically, and afterwards sends staff a digest of overdue follow-up, upcoming expirations, data issues, and recorded certificate status.

- "runs on a daily schedule" — moves cadence onto the run (`triggerAtHour: 7`; 14 consecutive daily executions), killing the per-tenant-daily misread.
- "staged" — the four-stage cascade, "at most one stage advances per run."
- "automatically" — explicitly licensed by the copy standard; restores the cohort-one inoculation.
- "afterwards" — the standard's own "later digest"; sibling-branch topology under `executionOrder: v1`, "the digest describes sends already made."
- "sends staff" not "gives" — delivery is an explicit non-capability.
- "recorded certificate status" — bounds the claim to the spreadsheet values the workflow actually reads.

Guards re-run: 238 chars, 32 words, zero digit tokens, no prohibited phrase, no `@`, no URL, no attachment token, no `\bclient\b`, no protected name. Sentence SHA-256 `d94efb4eaa09380a0ded63846c57228648ae9591bd9f1dcb698becb8db2455d8`.

**Option C — split into two facts** (same `concept_id`/`sentence_id`, distinct `fact_id`s; the schema permits it), so the weaker digest claim can stand or fall separately:

> Fact A: I built a workflow that runs on a daily schedule and sends staged certificate-of-insurance reminders automatically.
> Fact B: The same workflow afterwards sends staff a digest of overdue follow-up, upcoming expirations, data issues, and recorded certificate status.

Both guard-clean.

## 9. Risks JT must weigh before approving

1. **Authorship is JT's word.** No committed artifact independently names a builder; `verified_by: jt` verifies, it does not attest authorship.
2. **Per-tenant daily misread.** Gates prove ≥14/≥7-day spacing and a hard three-message cap.
3. **"Automatically" is absent** from the proposed sentence though the standard licenses it — the cheapest guard against repeating the cohort-one "approval on a person" error.
4. **"Gives" claims receipt**; delivery is unverified by design.
5. **"Certificate status" implies verified compliance**; every value is human-typed.
6. **"Daily" digest is inferred, not measured** — execution payloads deliberately not fetched.
7. **The card is unbindable today.** PR #33 is open; a card citing `514fbac` fails closed at `cohort_two_authority.py:2313` until it merges.
8. **`system_revision` should be `042759ce-d4f4-4ee9-906e-cb34d9de28b7`**, the live n8n change token — not an export label or backup path.
9. **Silent v1 redefinition.** `sentence_id` is pinned to the single enum value `coi-reminder-routing-v1`. Materially rewriting the sentence under that ID changes what "v1" means with no version bump.
10. **No machine check guards the card sentence itself.** Truth is human-owned here.
11. **PR #43 already asserts `verified_by: jt` for this exact sentence** — JT must confirm whether that attestation is genuinely his, and reconcile its 11-vs-12-node and `system_revision` discrepancies, before either PR merges.

## 10. Lane boundary honoured

No push, merge, deploy, activation, scheduling, or send. No canonical evidence file written. No PR opened. `verified_by` deliberately **absent** from the handoff payload — which is why it fails schema validation on `verified_by`/`verified_at` by design. Only JT can supply those two fields. The `cohort-two-authority` pipeline remains `paused`.
