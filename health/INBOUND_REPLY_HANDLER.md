# Health Inbound Reply Handler

Deterministic local handler for replies to the 9PM health check-in.

## Trigger
When JT replies in the direct Telegram thread with a health check-in answer and `health/pending-checkin.json` has a matching pending date, run:

```bash
python3 /Users/jtsomwaru/.openclaw/workspace/health/inbound_handler.py --reply "<JT reply>"
```

The handler:
1. Reads `health/pending-checkin.json` for the expected date.
2. Refuses to run if the pending date does not match, unless `--allow-no-pending` is explicitly used.
3. Refuses to overwrite an existing same-date DB row unless `--force` is explicitly used.
4. Parses with `health/parser.py` and writes through the existing `health/db.py` layer.
5. Marks `pending-checkin.json` as `status: logged` with `logged_at` and `handler`.
6. Prints the confirmation text Eve should send back to JT.

## Smoke test without writing

```bash
python3 /Users/jtsomwaru/.openclaw/workspace/health/inbound_handler.py \
  --reply "6, jaw + shoulders, partial, no protocol / 30min walk, 7 woke tense" \
  --date 2099-01-01 \
  --allow-no-pending \
  --dry-run \
  --json
```

## Idempotency
- `health.sqlite` has `checkins.date` unique.
- The handler checks existing rows before writing and exits with `DUPLICATE_CHECKIN` unless `--force` is passed.
- After success, `pending-checkin.json` is marked `logged`, so repeated handling exits with `ALREADY_HANDLED`.

## Current platform boundary
This closes deterministic local consumption of a health reply. Fully automatic inbound routing still depends on the OpenClaw Telegram/direct-message layer invoking this script when a reply belongs to the pending health check-in. Until that routing hook is wired, the main agent must call this script when JT's direct reply is clearly a health check-in.
