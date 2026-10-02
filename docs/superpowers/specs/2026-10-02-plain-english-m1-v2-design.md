# Plain-English M1 V2 Design

**Approved:** 2026-10-02 via `APPROVE PLAIN-ENGLISH M1 V2`

## Goal

Make contractor cold emails understandable in one skim without making them childish, generic, or gimmicky.

## Copy contract

- Grade 5-7 target; grade 8 warning ceiling.
- 50-85 body words, excluding the signature.
- Average sentence length 8-14 words; no sentence over 20 words.
- One verified company or person signal.
- One plain operational question.
- One plain value sentence.
- One reply-sized CTA.
- Keep the term `COI`; remove consultant abstractions such as `fixed-scope`, `map the workflow`, `handoffs`, `exception ownership`, `control plan`, `escalation rules`, and `tool/build decision`.
- Keep legal and coverage caveats out of M1 unless essential.
- Use a normal email signature. Avoid an abstract title if it adds category confusion.

## System changes

1. Resolve cold-email rule conflicts around email signatures, proof, and body length.
2. Add strong and bad examples for plain construction/COI copy.
3. Add a deterministic validator for length, readability, banned language, CTA size, and batch repetition.
4. Rewrite the COI outreach framework and all 25 M1 drafts from existing verified evidence.
5. Preserve every pre-send gate. This work does not authorize sending.

## Measurement

Use one version for the first 30 delivered emails. Track delivered, positive reply, wrong-person routing, confusion, objection, and CTA response. Do not infer a winner from a 15/15 split.


## Pre-registered fallback (D51)

Recorded before the first send. Wording is exactly as in the batch-10 X-review memo (`jsomwarux/jt-ops:main:reports/growth-os/2026-10-02-x-posts-critical-review-batch-10.md`, section 8 of the cold email offer engine post). The measurement window above ("the first 30 delivered emails") and this rule's 25 sends must be reconciled by JT before the first send (decision card Q7).

> **Conditions:** All 25 sends completed. The standard follow-up cadence is completed. The D22 reply-path test passed. Bounce rate is under the ceiling. Zero complaints.
>
> **If** there are zero positive replies, the next 25 sends change **only** the front end: a free "COI expiry snapshot." List, copy structure, and sender stay the same.
>
> **If** there is at least one positive reply, keep the $1,500 audit and continue the ramp.

A positive reply is `reply_classification = positive` in the outcome spine's `current-outcomes.csv`. The snapshot spec is `jsomwarux/jt-ops:reports/growth-os/drafts/D51-coi-expiry-snapshot-spec.md`. The snapshot runs only if this rule triggers and JT approves it.
