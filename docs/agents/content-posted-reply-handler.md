# Content Posted Reply Handler

Deterministic local handler for JT replies like `posted`, `posted both`, `posted Wednesday LinkedIn`, or `posted x: https://...`.

## Script

```bash
python3 scripts/content_posted_reply_handler.py --reply "posted Wednesday LinkedIn"
```

Useful flags:
- `--dry-run` — parse and show matched rows without writing.
- `--json` — machine-readable output for router integration.
- `--date YYYY-MM-DD` — posted date override; defaults to today.
- `--posted-log PATH` — alternate posted-log for tests.
- `--pending PATH` — alternate pending reminder state for tests.
- `--skip-notion` — skip Notion status update.
- `--lookback-hours 48` — fallback match window when pending state is absent.

## Matching rules

1. Reply must start with `posted`.
2. Platform words narrow the match:
   - `x`, `twitter`, `tweet` → X
   - `linkedin`, `linked in`, `li` → LinkedIn
3. Day names narrow the match: Monday through Sunday.
4. If `memory/content/pending-posted-reply.json` exists and is not consumed, the handler uses its `entries`/`posts` first.
5. If no pending state exists, it falls back to unbanked, unsuperseded posted-log rows from the last 48 hours.
6. Idempotent: rows already marked posted are reported as already logged and not duplicated.
7. URLs are stored only when unambiguous: one matched row + one URL, or one URL per matched row.

## Pending state schema

Content reminder/router can write this after sending a post reminder:

```json
{
  "sent_at": 1778725000,
  "status": "pending",
  "source": "content-reminder",
  "entries": [
    {"date": "2026-05-13", "platform": "linkedin", "day": "wednesday", "topic": "streeteasy-metric-correction-proof-discipline"},
    {"date": "2026-05-13", "platform": "x", "day": "wednesday", "topic": "six-buyer-intent-pages"}
  ]
}
```

`line_no` may be used for exact posted-log targeting when available.

After successful logging, the handler marks pending state:

```json
{"status": "logged", "logged_at": 1778726000, "handler": "scripts/content_posted_reply_handler.py", ...}
```

## Notion behavior

If `NOTION_TOKEN` is available and `--skip-notion` is not set, the handler queries the Content Calendar for the exact date/platform slot and sets `Status = Posted` only when exactly one row matches. Ambiguous or missing Notion rows are skipped without blocking local posted-log updates.

## Router integration blocker

The local deterministic handler is complete. The remaining platform-level task is to invoke it from the Telegram/direct inbound router for JT replies that start with `posted` while a content reminder is pending, then send `confirmation` back to JT.

Recommended router command:

```bash
cd /Users/jtsomwaru/.openclaw/workspace && \
python3 scripts/content_posted_reply_handler.py --reply "$JT_REPLY" --json
```

Non-content replies should bypass this handler.
