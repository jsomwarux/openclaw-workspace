# Relationship / Referral System Audit — 2026-05-13

## Scope
Audited the warm-relationship and referral system across:
- `memory/networking/contacts.md`
- `memory/networking/events.md`
- `HEARTBEAT.md` Monday relationship/event checks
- `memory/clients/proof-pipeline-gates.md`
- Altmark/Yair referral assets
- Aya referral prep and proof gates
- Guyana family-network intro scripts
- Active Mission Control relationship/referral tasks

No external contact was made. No messages were sent or drafted for delivery.

## Before Grade
**B-**

The system had strong referral assets, but the canonical relationship tracker was stale and disconnected from newer proof gates:
- `contacts.md` still marked March contacts as Hot even when last touch was >30 days old.
- Yair/Altmark — the highest-leverage referral path — was missing from the contact tracker.
- Guyana family-network validation was missing from the contact tracker.
- Aya referral prep existed, but the relationship tracker still encouraged a referral ask without the newer proof-safe blocker.
- HEARTBEAT checked warmth decay but did not verify proof/referral gates before surfacing an ask.
- Events file was a loose list, not an event-scoring system with exact date/venue/ICP/proof readiness fields.
- Mission Control had useful tasks, but no explicit blocker to refresh stale relationship state before asking.

## Scorecard

| Gate | Before | After | Notes |
|---|---:|---:|---|
| Contact freshness | C | B+ | Stale March contacts downgraded; Yair/Guyana added; exact latest touches still need human/client-state refresh. |
| Warmth decay | B- | A- | HEARTBEAT now distinguishes Hot decay, stale contacts, and gated asks. |
| Next action clarity | B | A- | Contacts now have owner/gate-based next actions and MC alignment. |
| Referral ask gating | B | A | Cross-client proof gate now requires relationship tracker update before asks. |
| Proof-safe constraints | B+ | A | Altmark/Aya privacy constraints reinforced in contacts and gates. |
| Family/network privacy | B | A | Guyana family ask remains validation-only; no government/favor framing. |
| Event scouting | C+ | B+ | Events file now has scoring/checklist; live event research still pending. |
| MC alignment | B | A- | One blocker task created to prevent stale/premature asks. |
| No stale/premature asks | C+ | A- | Stale asks are now explicitly blocked; final grade waits on refresh completion. |

## Changes Made

### 1. Rebuilt `memory/networking/contacts.md`
Added:
- Canonical contact field checklist.
- Warmth definitions.
- Gate-specific fields: referral gate, privacy/proof constraints, MC alignment.
- Active rows for:
  - Yair / Altmark Group
  - Dad / Guyana family network
  - Gil / Aya
  - Richard Leo / AmCham Guyana
  - Robert Oswald / H.C. Oswald
- Weekly review questions to catch stale/premature asks.

Important corrections:
- Gil/Aya downgraded from Hot to stale in the tracker until March meeting/client outcome is refreshed.
- Richard Leo downgraded from Hot to stale until call outcome is confirmed.
- Robert Oswald downgraded to stale/cold prospecting path, not warm relationship.
- Yair/Altmark referral ask marked blocked until proof/payment/acceptance gates clear.
- Guyana family-network ask marked validation-only, not sales referral.

### 2. Rebuilt `memory/networking/events.md`
Added:
- Event Scouting Checklist.
- Monthly scout rules.
- Buyer/operator prioritization.
- Requirement for exact date/venue/ICP relevance before MC task creation.
- Proof-readiness guardrails for event positioning.

### 3. Hardened `HEARTBEAT.md`
Updated Monday relationship check to:
- Read `memory/networking/contacts.md` and `memory/clients/proof-pipeline-gates.md`.
- Flag Hot contacts untouched in 7+ days.
- Flag stale contacts that still have current high-priority MC tasks.
- Label actions as relationship refresh, validation-only, or referral/proof ask.
- Verify gates before surfacing referral/proof asks.
- Avoid duplicate strategy tasks.

Updated event scout to:
- Read `memory/networking/events.md` first.
- Push HIGH tasks only for exact, actionable events.
- Log “no strong event found” instead of manufacturing urgency.

### 4. Hardened referral/proof docs
Updated `memory/clients/proof-pipeline-gates.md` referral gate:
- Relationship tracker must be current before asks.
- Family/network asks remain validation-only until buyer pain is confirmed.

Updated `memory/consulting/yair-family-office-intro-ask-2026-05-13.md`:
- Added relationship-state update as a pre-send requirement.

Updated `memory/research/guyana/guyana-intro-ask-scripts-2026-05-13.md`:
- Added post-touch logging requirement and guard against turning family names into outreach targets without review.

### 5. Created one Mission Control blocker
Created task: **Relationship system: refresh stale contacts before referral asks**

Purpose: ensure Yair/Altmark, Gil/Aya, and Guyana family-network rows are refreshed with latest real touch outcomes before any ask is sent.

## After Grade
**A-**

The system is now proof-safe and much harder to misuse. It is not A+ yet because the audit could not verify the real-world latest touch outcomes for Gil/Aya, Richard Leo, or Altmark acceptance/payment from direct source-of-truth conversations. Those require either client notes outside the inspected files or JT confirmation.

## Remaining Blockers

1. **Relationship freshness refresh**
   - Need current real-world last-touch outcomes for Yair/Altmark, Gil/Aya, Richard Leo, and Guyana family-network ask status.
   - Tracked by the new MC blocker.

2. **Altmark referral ask remains blocked**
   - Requires PC handoff/access path, insurance workflow acceptance/payment clarity, redacted proof capture, and acceptance wording.

3. **Aya referral ask remains blocked**
   - Requires accepted proof-safe evidence, useful output confirmation, and redaction boundaries in `memory/clients/aya/proof-evidence-checklist.md`.

4. **Event scout not fully live-tested**
   - Events tracker is structured, but no live first-Monday web scout was run during this audit.

## Validation

Validated by:
- Required bootstrap size check: `wc -c AGENTS.md MEMORY.md TOOLS.md HEARTBEAT.md`.
- Direct file inspection of relationship/referral/proof assets.
- Mission Control API read for active relationship/referral tasks.
- Mission Control API POST for blocker creation.
- File content checks after patching.

## Files Changed

- `memory/networking/contacts.md`
- `memory/networking/events.md`
- `HEARTBEAT.md`
- `memory/clients/proof-pipeline-gates.md`
- `memory/consulting/yair-family-office-intro-ask-2026-05-13.md`
- `memory/research/guyana/guyana-intro-ask-scripts-2026-05-13.md`
- `memory/audits/xhigh-systems/2026-05-13-relationship-referral-system.md`

## Task Changed

- Created Mission Control task: `Relationship system: refresh stale contacts before referral asks`.
