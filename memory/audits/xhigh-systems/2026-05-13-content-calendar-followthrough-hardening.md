# XHigh Hardening — Content Calendar / Posting / Follow-through

Date: 2026-05-13 22:16 ET
Scope: close the A+ blocker from `memory/audits/xhigh-systems/2026-05-13-content-calendar-followthrough.md`: deterministic inbound `posted` reply handling.

## Before grade
A-

The content system had calendar generation, Drive links, duplicate guards, local posted-log hygiene, and reminders. The weak handoff was final posting confirmation: JT's `posted` replies depended on Eve/manual context interpretation instead of a deterministic local handler.

## After grade
A

Local deterministic content posted-reply consumption now exists, is documented, and is covered by the content calendar audit. The remaining A+ blocker is platform-level Telegram routing into the local handler, not posted-log mutation logic.

## Files changed
- `scripts/content_posted_reply_handler.py` — new deterministic handler for inbound `posted` replies.
- `docs/agents/content-posted-reply-handler.md` — usage, schema, matching rules, Notion behavior, router handoff.
- `docs/agents/content-rules.md` — replaced manual/context-only posted logging instructions with the handler command and rules.
- `scripts/content_calendar_audit.py` — now verifies the posted-reply handler and docs exist and include required markers.
- `memory/audits/xhigh-systems/2026-05-13-content-calendar-followthrough-hardening.md` — this report.

No real `memory/content/posted-log.jsonl` rows were marked posted. No external posts were made.

## Handler behavior

Command:
```bash
cd /Users/jtsomwaru/.openclaw/workspace
python3 scripts/content_posted_reply_handler.py --reply "posted Wednesday LinkedIn"
```

Supported replies:
- `posted`
- `posted both`
- `posted LinkedIn`
- `posted X`
- `posted Wednesday LinkedIn`
- `posted x: https://...`

Safety rules implemented:
- Requires reply to start with `posted`.
- Narrows by platform aliases: X/Twitter/tweet and LinkedIn/LI.
- Narrows by weekday when present.
- Uses `memory/content/pending-posted-reply.json` first if present and unconsumed.
- Falls back to recent unbanked, unsuperseded scheduled posted-log rows within `--lookback-hours`.
- Does not mutate banked/superseded rows through fallback matching.
- Idempotent: duplicate replies return already-logged instead of appending/duplicating.
- URL storage only when unambiguous: one matched row + one URL, or one URL per row.
- Optional Notion update: if `NOTION_TOKEN` exists, set Content Calendar `Status = Posted` only when exactly one date/platform row matches. Missing/ambiguous Notion rows do not block local logging.
- `--dry-run`, `--json`, alternate posted-log/pending paths for safe tests.

## Pending state contract

A reminder/router can create:
```json
{
  "sent_at": 1778725000,
  "status": "pending",
  "source": "content-reminder",
  "entries": [
    {"date": "2026-05-13", "platform": "linkedin", "day": "wednesday", "topic": "streeteasy-metric-correction-proof-discipline"}
  ]
}
```

After successful logging the handler writes `status: logged`, `logged_at`, handler path, raw reply, and matched rows.

## Tasks changed

Updated Mission Control task:
- `Content posting: deterministic posted-reply handler` → renamed to `Content posting: wire Telegram posted replies to local handler`.
- Status remains `todo` because platform-level Telegram/direct routing is still not wired.
- Description now states local handler is complete and gives the exact router command:
  ```bash
  cd /Users/jtsomwaru/.openclaw/workspace && python3 scripts/content_posted_reply_handler.py --reply "$JT_REPLY" --json
  ```

## Validation

Commands run:
```bash
python3 -m py_compile scripts/content_posted_reply_handler.py scripts/content_calendar_audit.py scripts/notion-calendar-push.py

# temp-copy posted-log + temp pending file dry run
python3 scripts/content_posted_reply_handler.py \
  --reply "posted Wednesday LinkedIn: https://www.linkedin.com/feed/update/test" \
  --date 2026-05-13 \
  --posted-log "$TMPDIR/posted-log.jsonl" \
  --pending "$TMPDIR/pending.json" \
  --dry-run --skip-notion --json

# temp write + idempotency
python3 scripts/content_posted_reply_handler.py --reply "posted Wednesday LinkedIn: https://www.linkedin.com/feed/update/test" --date 2026-05-13 --posted-log "$TMPDIR/posted-log.jsonl" --pending "$TMPDIR/pending.json" --skip-notion --json
python3 scripts/content_posted_reply_handler.py --reply "posted Wednesday LinkedIn: https://www.linkedin.com/feed/update/test" --date 2026-05-13 --posted-log "$TMPDIR/posted-log.jsonl" --pending "$TMPDIR/pending.json" --skip-notion --json

python3 scripts/content_calendar_audit.py --week 2026-05-11
```

Results:
- `py_compile` passed.
- Dry-run matched only the intended 2026-05-13 LinkedIn row.
- Temp write set `posted: true`, `posted_date: 2026-05-13`, and URL on the copied log only.
- Temp pending state was consumed with `status: logged`.
- Duplicate temp reply returned `Already logged ✅`.
- Local content audit passed:
  - `weekly: PASS`
  - `posted_log: PASS`
  - `crons: PASS`

## Remaining blockers

1. **Telegram/direct inbound router wiring** — platform-level work still needed. Route JT content replies beginning with `posted` into `scripts/content_posted_reply_handler.py --reply "$JT_REPLY" --json`, then send `confirmation` back to JT.
2. **Reminder pending-state creation** — best final form is for `content-reminder` / `content-sunday` delivery flow to write `memory/content/pending-posted-reply.json` with exact entries sent. Handler already supports this. Without pending state, it safely falls back to recent scheduled rows, but pending state is cleaner.

## Report path
`memory/audits/xhigh-systems/2026-05-13-content-calendar-followthrough-hardening.md`
