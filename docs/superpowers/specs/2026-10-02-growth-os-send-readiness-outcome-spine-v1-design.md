# Growth OS Send Readiness + Outcome Spine V1 Design

**Status:** Approved in conversation on 2026-10-02. Local preparation only; no send, campaign activation, provider call, purchase, credential, schedule, or deployment is authorized.

## Goal

Turn the approved 25-message M1 V2 packet into a deterministic, fail-closed send-decision artifact and a prefilled outcome ledger without making any external change.

## Chosen approach

Use one local Python compiler with CSV/JSON inputs and outputs. It joins the canonical first-25 contact file to the approved V2 packet, validates one-to-one identity/copy binding, applies fresh verification and sending-mailbox gates, and emits:

1. a row-level readiness CSV;
2. a compact batch summary JSON;
3. an Instantly import CSV only when every row and assigned sender pass;
4. a prefilled outcome-spine CSV whose initial state is `not_sent`.

This is preferable to a spreadsheet-only checklist because the gates are repeatable and testable, and preferable to a live Instantly/API workflow because the first batch has not yet proven delivery or reply behavior.

## Inputs

- Canonical contacts: `reports/growth-os/data/2026-10-02-first-25-review.csv`
- Approved copy: `reports/growth-os/2026-10-02-first-25-m1-v2-review-packet.md`
- Fresh recipient verification CSV supplied by an authorized verifier or manual operator. Exact fields: `email`, `mailbox_status`, `mailbox_verified_at`, `identity_status`, `identity_checked_at`, `suppression_observed`, `suppression_status`, `suppression_checked_at`. Accepted literals are lowercase: mailbox `valid|invalid|unknown`, identity `verified|mismatch|unknown`, suppression observed `true|false`, and suppression status `clear|blocked|unknown`. `suppression_observed=false` blocks regardless of status.
- Sending-mailbox inventory CSV exported or transcribed from Instantly. Exact fields: `sending_account`, `account_type`, `account_status`, `dns_mx`, `dns_spf`, `dns_dkim`, `dns_dmarc`, `warmup_health_score`, `warmup_days`, `daily_campaign_limit`, `sender_checked_at`. Accepted lowercase enums are account type `prewarmed|standard|airmail`, status `active|paused|error`, and DNS `pass|fail|unknown`. Enums are case-sensitive; surrounding whitespace is rejected.

No credential or API key enters these files.

## Gates

### Recipient gates

- Exact 25-row contact/copy match. Stable row ID is `<batch_id>:<two-digit batch_position>`, where batch ID is `growth-os-first25-m1-v2-2026-10-02`.
- Unique recipient email and company.
- Packet recipient, company, email, and position match the canonical row. Email comparison trims surrounding whitespace and lowercases the domain and local part. Person/company comparisons use Unicode NFC, trim ends, collapse internal whitespace, and casefold. Canonical output preserves the contact CSV values.
- Positions must be exactly 1–25 with no gaps; reordering inputs is allowed because output is sorted by position. Missing, extra, or duplicate rows fail the batch.
- Current identity status equals `verified`; check age is at most seven days.
- Mailbox status equals `valid`; verification age is at most 24 hours.
- Suppression was authoritatively observed, status equals `clear`, and check age is at most 15 minutes.
- Every time uses RFC 3339 UTC with a literal `Z`. The CLI requires `--as-of`; ages are inclusive (`age <= limit`). Naive, offset, malformed, or future timestamps fail closed.

### Sending-mailbox gates

- `jtsomwaru@gmail.com` and any `@jtsomwaru.com` account are rejected.
- Account status is `active`.
- MX, SPF, DKIM, and DMARC all pass.
- Warmup health score is at least 90.
- Non-prewarmed accounts have at least 14 warmup days.
- For this first batch every eligible account is capped at five assigned messages. Platform maximums also apply: prewarmed 25, standard 30, AirMail 20. A configured daily limit above its type maximum rejects the account.
- Allocation is deterministic: recipients sort by batch position; eligible mailboxes sort by normalized sending address; assignments proceed round-robin until each effective capacity `min(daily_campaign_limit, 5)` is exhausted. Duplicate sending accounts reject the inventory.
- Sender attestation age is at most 24 hours, inclusive. `sender_checked_at` follows the same literal-`Z`, fixed-`--as-of`, malformed/future-time refusal rules as recipient timestamps.

Any missing or stale fact blocks that row or mailbox. `observed:false` is never treated as a suppression clear.

## Outputs and lifecycle

Hash inputs use UTF-8 and LF line endings. Subjects are outer-trimmed. Body text includes the signature, is LF-normalized, strips trailing whitespace from every line, and is outer-trimmed. The outcome spine stores separate `candidate_subject_sha256` and `candidate_body_sha256`; later reconciliation appends separate sent hashes rather than replacing candidate hashes.

Stable derivations and enums:

- The shared schema version for readiness, summary, Instantly row-hash input, outcome seed/projection, reconciliation event, and manifest is `growth-os-send-readiness-v1`.
- Canonical JSON bytes are UTF-8 from `json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)` with no trailing newline. JSON artifact files store those bytes plus one LF; hashes use the no-LF bytes unless explicitly defined as a raw-file hash.
- `prospect_id` is `prospect.` plus the first 20 hex characters of SHA-256 over `b"growth-os-prospect-v1\0" + normalized_email + b"\0" + normalized_company`.
- `email_fingerprint` is SHA-256 over `b"outreach-channel-v1\0direct_email\0" + normalized_email`.
- Instantly `row_hash` is SHA-256 over canonical sorted-key JSON containing `schemaVersion,row_id,email,subject,body,sending_account`.
- `inputHashes` is a sorted-key JSON map with exactly `contactsCsvSha256`, `packetMarkdownSha256`, `recipientVerificationCsvSha256`, and `senderInventoryCsvSha256`. Each present value is SHA-256 of the raw file bytes; an absent optional attestation is JSON null.
- Instantly name splitting first applies Unicode NFC and collapsed internal whitespace. `first_name` is the first whitespace-delimited token; `last_name` is every remaining token joined by one space. A one-token name has a blank `last_name`.
- CSV booleans are lowercase `true|false`. Multiple blocker codes are unique, lexically sorted, and joined by `;`.
- Stable row blockers are `recipient_verification_missing`, `mailbox_invalid`, `mailbox_unknown`, `mailbox_verification_stale`, `identity_mismatch`, `identity_unknown`, `identity_check_stale`, `suppression_not_observed`, `suppression_blocked`, `suppression_unknown`, `suppression_check_stale`, `no_eligible_sending_mailbox`, and `insufficient_sending_capacity`.
- Stable sender-rejection reasons are `prohibited_sender`, `sender_inactive`, `dns_mx_fail`, `dns_mx_unknown`, `dns_spf_fail`, `dns_spf_unknown`, `dns_dkim_fail`, `dns_dkim_unknown`, `dns_dmarc_fail`, `dns_dmarc_unknown`, `health_below_90`, `warmup_incomplete`, `limit_exceeds_policy`, `sender_attestation_missing`, and `sender_attestation_stale`.
- `send_status` is `not_sent|sent`. `delivery_status` is blank until observed, then `delivered|hard_bounce|unknown`. `reply_classification` is blank until observed, then `positive|wrong_person|objection|confused|unsubscribe|no_response|other`; `no_response` requires a later dated observation and is never inferred during compilation.

Exact output contracts:

- Readiness CSV: `schema_version,batch_id,row_id,batch_position,company,buyer_name,email,copy_subject_sha256,copy_body_sha256,sending_account,ready,blocker_codes`.
- Summary JSON: `schemaVersion,batchId,asOf,generatedAt,inputHashes,rowCount,readyCount,blockedCount,eligibleSenderCount,assignedCount,blockerCounts,ready,currentBundle`. `generatedAt` equals the fixed `asOf`.
- Instantly CSV: `email,first_name,last_name,company_name,subject,body,sending_account,row_id,row_hash`; emitted only for a fully ready current bundle.
- Outcome CSV: `schema_version,batch_id,row_id,batch_position,prospect_id,company,email_fingerprint,candidate_subject_sha256,candidate_body_sha256,sending_account,send_status,sent_at,vendor_message_id,sent_subject_sha256,sent_body_sha256,delivery_status,delivery_observed_at,reply_classification,reply_observed_at,outcome_evidence_id,next_action,next_action_due_at`. Initial send status is `not_sent`; delivery status and reply classification are independent.
- Reconciliation event JSONL exact fields are `schemaVersion,eventId,batchId,rowId,vendorMessageId,evidenceId,sentAt,finalSubject,finalBody,sentSubjectSha256,sentBodySha256,eventObservedAt`. `eventId` is SHA-256 over canonical JSON of every field except `eventId`. Events are keyed for idempotency by `batchId + rowId + vendorMessageId`, preserve candidate hashes through projection, and record exact sent hashes. Both vendor and evidence IDs are mandatory in V1; evidence-only/manual-Gmail reconciliation is unsupported. Exact replay is idempotent; conflicting replay fails. No transition to `sent` occurs without both IDs, a literal-`Z` sent timestamp, final subject/body, valid hashes, and a literal-`Z` event observation timestamp. One exclusive lock covers existing-ledger validation, idempotency/conflict lookup, append, flush, and fsync. Symlink and hard-link aliases are rejected, malformed existing rows fail closed with a controlled error, and incomplete trailing bytes are never accepted as an event.
- `reconciliation-events.jsonl` is authoritative for sent state. Immutable bundle `outcome-spine.csv` is a seed snapshot only. A deterministic projector validates the seed plus full event ledger and atomically writes root `current-outcomes.csv` using the exact Outcome CSV header above; consumers read that projection for current `send_status`, sent hashes, timestamps, and vendor/evidence IDs. Projection overlays only valid events, preserves candidate hashes, sorts by batch position, and fails closed on conflicts or malformed history.

All CSV output is ordered by numeric batch position. JSON keys are canonical/sorted. Counts must reconcile exactly.

## Failure behavior

- Schema mismatch, duplicate identity, packet/contact mismatch, invalid timestamps, future timestamps, stale checks, unsafe sender, or insufficient sender capacity returns a controlled error or a blocked result.
- The compiler never silently drops rows.
- Instantly import output is withheld unless all 25 rows are ready.
- Output root is `reports/growth-os/send-readiness/growth-os-first25-m1-v2-2026-10-02/`. Immutable bundles live at `bundles/<bundle_id>/` and contain `readiness.csv`, `outcome-spine.csv`, `summary.json`, and optional `instantly-import.csv`. Root `current.json` is the only readiness authority and contains `schemaVersion,batchId,bundleId,ready,summaryPath,readinessPath,outcomePath,instantlyImportPath`; the import path is JSON null when blocked. Reconciliation events live at root `reconciliation-events.jsonl`; the authoritative projection is root `current-outcomes.csv`.
- `bundle_id` is SHA-256 over canonical sorted-key JSON containing `schemaVersion,batchId,asOf,inputHashes`. Identical inputs plus `--as-of` yield the same bundle ID. Outputs are assembled in a temporary directory and fsynced. If the destination bundle is absent, the directory is renamed into place. If it exists, every expected filename and byte hash must match the staged bundle; exact matches reuse it and any mismatch fails closed. Immutable bundles are never overwritten. The chosen bundle is selected by one atomically replaced and fsynced `current.json`. A blocked rerun points `current.json` to a bundle with no Instantly import; an older ready import is historical and invalid unless its bundle ID and path match the current manifest. Interrupted runs cannot replace the prior complete manifest.

## Testing

Unit tests cover exact schemas/enums, malformed booleans/numbers, recipient and sender timestamp boundaries plus future/naive times, suppression observation, prohibited/duplicate senders, deterministic mixed-capacity allocation, packet/contact drift, stable row IDs, known-answer hashes, bundle atomicity, ready-to-blocked invalidation, and crash-safe append-only reconciliation conflicts. Acceptance uses fixed `--as-of` against the real files with no fabricated attestations and must produce exactly 25 blocked readiness rows, 25 `not_sent` outcome rows, zero sender assignments, reconciled summary counts, no current Instantly import, byte-identical bundle payloads and current manifest across reruns, and no network access.

## Parallel lane

Claude Code may build the already-scoped inactive Apollo-to-n8n fixture proof in `/Users/jtsomwaru/projects/n8n-agent/clients/apollo-coi-sourcing/`. That lane must not touch the readiness compiler, provider credentials, live n8n, Instantly, or send state.
