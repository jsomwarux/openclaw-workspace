# XHigh Hardening — Social Engagement / Reply System

**Date:** 2026-05-13  
**Scope:** Dynasty X replies, general X reply targets, Reddit daily generation, Reddit karma reminder, Viral Post Swipe File X Research, ledgers, validator wiring, Mission Control blocker.  
**External posting:** none. No replies/posts were sent externally by this task. JT still presses send/post.

## Executive grade

- **Before grade:** B+
- **After grade:** A-

This is no longer just prompt-level hygiene. The daily loops now have a local validator gate, the thin ledgers were backfilled from actual run history, and the known dynasty repeat failure is sealed into the ledger so the same URLs/status IDs are rejected going forward.

Not A+ yet because two warnings are intentionally preserved:
1. older general X reply-target files still lack direct links and should remain treated as non-review artifacts,
2. the latest two inspected dynasty cron runs historically repeated the same pack. The repeated URLs are now ledger-sealed, but the next scheduled run still needs to prove the new guard blocks/replaces repeats in live execution.

## Changes made

### 1) Dynasty replies ledger backfilled

Updated:
- `memory/sports-gm/dynasty-replies-ledger.jsonl`

What changed:
- Added 32 backfilled rows from existing `dynasty-replies-gen` cron run history.
- Ledger went from **6 rows** to **38 rows**.
- Backfill rows are marked with source: `backfill from dynasty cron run history 2026-05-13 hardening`.
- Repeated/cached targets from recent cron history are now in the ledger, including the latest repeated pack and older cached packs.

Impact:
- The 14-day anti-repeat policy now has enough history to enforce against real prior targets.
- The known repeated URLs are explicitly sealed; future runs should reject them before delivery.

### 2) Reddit draft log backfilled

Updated:
- `memory/content/reddit-draft-log.jsonl`

What changed:
- Added 32 entries parsed from `reddit-daily-gen` run history.
- Log went from **8 entries** to **40 entries**.
- Backfill entries include date, subreddit, type, title/look-for, first 120 chars, core angle, body hash, and source.

Impact:
- The Reddit 30-day anti-repeat policy is now enforceable against materially more prior drafts.
- The validator no longer warns that Reddit history is shallow.

### 3) Validator upgraded from audit-only to loop gate

Updated:
- `scripts/social_engagement_audit.py`

What changed:
- Added `--gate` mode:
  - `--gate dynasty` checks dynasty ledger + repeat-pack state.
  - `--gate reddit` checks Reddit draft log validity/depth/duplicates.
  - `--gate x` checks latest reply-target freshness/direct links.
  - `--gate cron` checks cron prompt guard wiring + cron health.
  - default `all` runs the full suite.
- Added cron prompt guard check to ensure all four social crons include pre-send validator instructions.
- Changed the repeated dynasty pack check from hard fail to warning only when the repeated URLs are now present in the ledger. This preserves the historical smell without blocking the hardened system after sealing.

### 4) Social cron prompts patched with pre-send validator gates

Backed up cron config first:
- `~/.openclaw/cron/jobs.json.bak-social-engagement-hardening-20260513`

Updated prompts in:
- `8b968751-6e59-42e5-b2ce-09f57d36176c` — `dynasty-replies-gen`
- `bbe49024-458a-4496-9c7c-7a278615810f` — `reddit-daily-gen`
- `fe575759-c8b1-4715-ae5a-0dbe034b3c9b` — `reddit-karma-daily-reminder`
- `33b8b0a2-e86c-4f51-aa4f-b8537def3107` — `Viral Post Swipe File — X Research`

Prompt guard now requires:
- run the relevant `scripts/social_engagement_audit.py --json --gate ...` before delivery,
- output `BLOCKED: social engagement validator failed — [check name + detail]` on fail,
- write ledgers before sending where applicable,
- rerun the validator after ledger/file writes,
- keep direct X links mandatory,
- never fabricate posted/replied status.

### 5) Mission Control blocker closed

Closed:
- `j57882a7xfd79c2f4gczg522ws86p5wv`
- `Social engagement system: seed ledgers + wire validator into daily loops`

## Validation

### Bootstrap budget check

```text
27013 AGENTS.md
19258 MEMORY.md
14776 TOOLS.md
15578 HEARTBEAT.md
76625 total
```

All were under budget at task start.

### Compile check

```bash
python3 -m py_compile scripts/social_engagement_audit.py
```

Result: pass.

### Full validator after hardening

```bash
python3 scripts/social_engagement_audit.py --json
```

Result:

```json
{
  "ok": true,
  "summary": {"pass": 8, "warn": 2}
}
```

Important checks:
- PASS: latest X reply target file fresh with 5 direct links.
- PASS: dynasty ledger valid with 38 rows.
- PASS: Reddit draft log valid with 40 entries.
- PASS: all social cron prompts include validator gates.
- PASS: all four required crons enabled, `deleteAfterRun=false`, last status ok, failure alerts routed to JT.
- WARN: older recent X reply target files missing direct links.
- WARN: latest two historical dynasty runs repeated, but those repeated URLs are now ledger-sealed.

### Gate-specific checks

```bash
python3 scripts/social_engagement_audit.py --json --gate dynasty
python3 scripts/social_engagement_audit.py --json --gate reddit
python3 scripts/social_engagement_audit.py --json --gate x
python3 scripts/social_engagement_audit.py --json --gate cron
```

Results:
- Dynasty gate: `ok=true`, 1 pass / 1 warn.
- Reddit gate: `ok=true`, 1 pass.
- X gate: `ok=true`, 1 pass / 1 warn.
- Cron gate: `ok=true`, 5 pass.

## Remaining blockers / watch items

1. **Next live dynasty run proof:** the next scheduled run must prove it replaces or blocks ledger-sealed repeated URLs. Current warning is historical, not unsealed.
2. **Historical X target artifacts:** older recent `reply-targets-*` files without direct links should not be treated as usable review artifacts. Latest file and future prompt path enforce direct links.
3. **Notion env for swipe cron:** prior audit noted Notion push missing env in runtime. Not part of reply quality, but still a swipe-file completeness issue.

## Recommendation

Call this **A- now**. Upgrade to **A/A+** after one clean scheduled dynasty run where the validator is invoked and no ledger-sealed target appears in the delivered pack.
