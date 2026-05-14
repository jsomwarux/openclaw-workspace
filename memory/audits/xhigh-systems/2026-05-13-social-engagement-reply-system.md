# XHigh Audit — Social Engagement / Reply System

**Date:** 2026-05-13  
**Scope:** X reply targets, dynasty X replies, Reddit daily content, Reddit karma reminder, Viral Post Swipe File X Research, ledgers/logs, Mission Control follow-through.  
**External posting:** none. JT still presses send/post.

## Executive grade

- **Before grade:** B-
- **After grade:** B+

The system is directionally strong and much better than a generic content machine: prompts now require fresh targets, direct links, native reply style, anti-repeat checks, subreddit safety, Telegram delivery, and logging. The remaining gap is not copy quality. It is observability/enforcement. A few prompts say the right things, but the historical ledgers are too thin and recent runs prove a repeated dynasty target pack can still appear as `ok`.

## Inventory

### 1) X / general reply targets

- Latest file: `memory/content/reply-targets-2026-05-13.md`
- Freshness: modified ~16h before validation, within the 24h target window.
- Direct links: 5 valid `https://x.com/.../status/...` URLs.
- Quality: replies are short, mostly native, and tied to JT's current lanes: OpenClaw/n8n, property ops, first users, implementation ownership.
- Weakness: several older recent files lack direct links, which makes them poor review artifacts and proves the link rule was added late rather than historically enforced.

### 2) Dynasty X replies

Cron: `8b968751-6e59-42e5-b2ce-09f57d36176c` / `dynasty-replies-gen`

Strengths:
- Enabled, last run `ok`, Telegram delivered.
- Prompt has a real freshness hard stop: final targets must be ≤24h old and cached/old pools must output `BLOCKED`.
- Requires 3 different accounts, at least 2 approved-list targets, ledger read/write, URL/status ID rejection, and native fantasy voice.
- `memory/sports-gm/dynasty-x-targets.md` is a good account universe.

Findings:
- `memory/sports-gm/dynasty-replies-ledger.jsonl` exists and is valid JSONL.
- Ledger is too shallow: 6 rows, all from 2026-05-13. It cannot yet enforce a real 14-day anti-repeat policy.
- Recent cron history shows the latest two dynasty run summaries used identical target URLs before the replacement/correction pack was added to the ledger. That is a real failure mode: duplicate pack can still show as `status=ok`.

### 3) Reddit daily generation

Cron: `bbe49024-458a-4496-9c7c-7a278615810f` / `reddit-daily-gen`

Strengths:
- Enabled, last run `ok`, Telegram delivered.
- Reads `reddit-strategy.md`, `reddit-draft-log.jsonl`, `posted-log.jsonl`, Sports GM skill/report.
- Requires fresh crypto input from ≤48h or `SKIP_SLOT`.
- Has hard anti-repeat bans for stale crypto/fantasy frames.
- Requires Telegram output under 3,500 chars and logging every non-skipped item.

Findings:
- Latest run used a fresh May 13 crypto-agent input and logged Reddit items.
- `memory/content/reddit-draft-log.jsonl` is valid JSON, but despite the `.jsonl` name it is a JSON array. Existing prompts appear compatible because recent runs updated it successfully.
- Log is shallow: 8 entries. Useful, but not yet enough for robust 30-day anti-repeat enforcement.
- Some latest generated Reddit angles are still close to broad crypto mechanism/durability territory, although the newest entries are more concrete than the banned frames.

### 4) Reddit karma daily reminder

Cron: `fe575759-c8b1-4715-ae5a-0dbe034b3c9b` / `reddit-karma-daily-reminder`

Strengths:
- Enabled and last run `ok`.
- Prompt has strong mod-safety: no external links, no CTA, no launch/referral/tool-promo language, no default Nash/Vista mentions, no buy/sell recommendations.
- Requires subreddit activity/rule fit, current effort mapping, anti-repeat reading, and same-run logging.

Concern:
- Cron delivery is `not-requested`, but run summaries claim content was sent to Telegram. This may be from direct message tool use inside the run rather than cron fallback delivery. It should be monitored because delivery truth is less obvious than `deliveryStatus=delivered` jobs.

### 5) Viral Post Swipe File / X Research

Cron: `33b8b0a2-e86c-4f51-aa4f-b8537def3107` / `Viral Post Swipe File — X Research`

Strengths:
- Enabled, last run `ok`.
- Searches are constrained to recent X with `--sort likes --since 7d --limit 12 --json` and retweet/reply exclusions.
- Requires signal thresholds, spam rejection, Notion swipe pushes for usable posts, local report, reply target file, Drive upload, and Telegram summary.
- Latest report: `memory/content/x-research-report-2026-05-13.md` includes query-quality notes, usable posts, timestamps, URLs, and explicit `NO_STRONG_SIGNAL` when thresholds were not met.

Findings:
- Latest X reply target file is good and directly linked.
- Notion swipe push was blocked by missing Notion env in that runtime; report captured the blocker.
- A prior run summary ended mid-process (“search commands completed... proceed to analyze”), which is suspicious because status was still `ok`. Later artifacts appear complete, but this is a monitoring smell.

## Score gates

| Gate | Result | Evidence |
|---|---:|---|
| Fresh ≤24h reply targets where required | ✅ / ⚠️ | Latest X reply targets fresh; dynasty prompt requires ≤24h; prior cached-pool behavior was corrected. |
| Direct links | ✅ latest / ⚠️ historical | May 13 target file has 5 links; older target files missing links. |
| Ledger anti-repeat | ⚠️ | Ledger valid but only 6 rows; recent duplicate dynasty pack detected. |
| Subreddit rule compliance | ✅ | `reddit-strategy.md` and prompts enforce no links/CTA/product spam and target-stack rules. |
| No product spam | ✅ | Explicit Nash/Vista/DynastyJig non-promo rules. |
| Native voice | ✅ / ⚠️ | X and dynasty prompts have native style constraints; Reddit still risks polished theory if fresh inputs are weak. |
| Drive/local review paths | ✅ / ⚠️ | X research requires Drive/local files; Reddit is Telegram/log first, no Drive requirement. |
| Mission Control follow-through | ✅ | Created blocker task `j57882a7xfd79c2f4gczg522ws86p5wv`. |
| No stale cached pools | ✅ prompt / ⚠️ observed history | Prompt now blocks cached pools; duplicate recent pack proves validator is needed. |
| Failure alerts | ✅ | All audited crons have failure alert to Telegram `6608544825`. |
| Empty-output guards | ✅ / ⚠️ | Reddit/X prompts prefer SKIP/BLOCKED; no standalone validator existed before this audit. |

## Patches made

### Added read-only validator

Created:
- `scripts/social_engagement_audit.py`

It checks:
- latest X reply target freshness and direct X links
- recent target-file link hygiene
- dynasty replies ledger existence, JSONL validity, duplicate URLs, and minimum history depth
- Reddit draft log JSON validity, required fields, duplicate body hashes, and history depth
- required social crons enabled, non-deleteAfterRun, failure alerts, and last run status
- recent dynasty cron packs for identical target URL repeats

Validation command:

```bash
python3 scripts/social_engagement_audit.py --json
```

Latest validation summary:

```json
{
  "ok": false,
  "summary": {"pass": 5, "warn": 3, "fail": 1}
}
```

Important checks:
- PASS: latest `reply-targets-2026-05-13.md` has 5 direct X links and is fresh.
- PASS: all four audited crons are enabled and have last status `ok`.
- WARN: older recent reply target files missing links.
- WARN: dynasty ledger has only 6 rows.
- WARN: Reddit draft log has only 8 entries.
- FAIL: latest two inspected dynasty cron packs used identical target URLs.

### Added Mission Control blocker

Created task:
- `j57882a7xfd79c2f4gczg522ws86p5wv`
- Title: `Social engagement system: seed ledgers + wire validator into daily loops`
- Priority: high
- Project: Content

First action is to run the validator, then backfill/seal the dynasty and Reddit logs before wiring this as a preflight/weekly guard.

## Files changed

- `scripts/social_engagement_audit.py`
- `memory/audits/xhigh-systems/2026-05-13-social-engagement-reply-system.md`

## Tasks changed

- Created MC blocker: `Social engagement system: seed ledgers + wire validator into daily loops` (`j57882a7xfd79c2f4gczg522ws86p5wv`).

## Validation performed

Commands/checks run:

```bash
wc -c AGENTS.md MEMORY.md TOOLS.md HEARTBEAT.md
openclaw cron list
openclaw cron show <social cron ids> --json
openclaw cron runs --id <social cron ids> --limit 3
python3 -m py_compile scripts/social_engagement_audit.py
python3 scripts/social_engagement_audit.py --json
curl -s http://localhost:3000/api/tasks
```

Bootstrap sizes at start:
- `AGENTS.md`: 27,013 bytes
- `MEMORY.md`: 19,258 bytes
- `TOOLS.md`: 14,776 bytes
- `HEARTBEAT.md`: 15,578 bytes

All are under their hard budgets.

## Remaining blockers

1. **Dynasty duplicate-pack failure** — latest two inspected runs used identical URLs. The replacement ledger rows help future runs, but the system needs a non-prompt guard before A grade.
2. **Ledger depth** — dynasty ledger needs either backfilled rows from recent delivered packs or an explicit “history starts 2026-05-13” note until 14 days accrue.
3. **Reddit anti-repeat depth** — Reddit log only has 8 entries, so the 30-day anti-repeat policy is mostly aspirational until more history/backfill exists.
4. **Historical X reply target links** — latest file is fixed, but older recent files without direct links should not be treated as usable review artifacts.
5. **Notion env visibility for swipe cron** — latest report says Notion push was blocked by missing token in runtime. Not a reply-quality blocker, but a swipe-file completeness blocker.

## Recommendation

Do not call this A+ yet. The content/reply prompts are good enough, but A+ requires the validator to become part of the loop and the ledgers to have enough history to stop repeats without relying on the model remembering.

Next best action: run the MC blocker as a focused hardening task, starting with the dynasty ledger and validator integration. That is the shortest path from B+ to A/A+.
