# XHigh Systems Audit — Content Calendar / Posting / Follow-through

Date: 2026-05-13 22:15 ET
Scope: weekly content generation, daily reminders, Sunday flow, Notion calendar, Drive drafts, posted-log, content guard, stale/duplicate prevention, current-effort alignment.

## Before grade
B / B+

The system generated useful drafts and reminders, but had two follow-through failures:
1. X weekly generation ran twice on 2026-05-11/13, creating duplicate X entries in both `memory/content/posted-log.jsonl` and Notion Content Calendar.
2. The first X Notion batch had no Drive links, so reviewability depended on the later corrected batch.

## After grade
A-

Local generation/reminder guardrails now pass, duplicate local log entries are marked superseded, stale unlinked Notion X rows were archived, and a repeatable audit script now detects this class of drift.

Not A+ because automatic inbound `posted` reply consumption is still prompt/process based, not a deterministic router. There is no evidence to mark posts posted, so no post status was fabricated.

## Inventory findings

### Weekly content file
- Current weekly file: `memory/content/weekly-2026-05-11.md`.
- Contains current-effort grounding, constraint log, hook mappings, Wednesday advisory board, X section, and one explicit Sunday `SKIP_SLOT` with `Do not send` language.
- `scripts/content_distribution_guard.py --weekly memory/content/weekly-2026-05-11.md --check-notion-script` passes.

### Cron flows
- `content-generate-linkedin`: enabled, delivered, creates weekly file, uploads Drive, pushes Notion, logs scheduled entries.
- `content-generate-x`: enabled, runner delivery is `none` but prompt sends Telegram itself; recent run did send, upload Drive, push Notion, and log.
- `content-reminder`: enabled, delivered daily Tue-Sat, runs guard before sending scheduled copy.
- `content-sunday`: enabled, delivered Sunday, includes learn-in-public placeholder block and performance feedback prompt.

### Notion calendar
- Before cleanup: 20 rows for 2026-05-11 through 2026-05-17: 6 LinkedIn + 14 X.
- Problem: every X date had two rows. The older seven X rows had no Drive Link.
- Fixed: archived the older unlinked X rows. Remaining Notion audit for week passes: no duplicate date/platform slots and all rows have Drive links.

### Drive drafts
- LinkedIn weekly Drive link from cron: `https://docs.google.com/document/d/18pvrbIAorW4q4QekGNvX9Ulq3p2TtsSK_HsxJOt6R2k/edit`.
- X completed weekly Drive link from cron: `https://docs.google.com/document/d/1oqRLF6y1zoRpSyLHbp6XzPCuYY63XsHlc0uAn7g4kcY/edit`.
- Remaining Notion rows all have Drive links.

### Posted log
- Before cleanup: duplicate scheduled X slots for 2026-05-11 through 2026-05-17.
- Fixed: older X entries were marked `superseded: true`, `superseded_by: content-generate-x rerun 2026-05-13`, and `banked: true` so scheduled-slot duplicate checks pass without deleting history.
- No `posted: true` status was added because no post URL/evidence was found.

### Reminder / feedback loop
- Reminder crons ask JT to reply `posted` after posting.
- Sunday flow asks which post performed best and prompts for vibe-marketing metrics.
- Deterministic inbound posted-reply handler still appears missing; this is the main remaining A+ blocker.

## Patches made
1. Added `scripts/content_calendar_audit.py`:
   - Checks weekly file/guard.
   - Checks posted-log JSON and duplicate scheduled slots.
   - Checks content cron prompt markers.
   - Optional `--with-notion` checks for duplicate date/platform rows and missing Drive links.
2. Patched `scripts/notion-calendar-push.py`:
   - Added existing Notion date/platform slot guard.
   - Default behavior now skips creating duplicate rows unless `--replace` is explicitly passed.
   - Keeps `--dry-run` behavior.
3. Patched `scripts/content_distribution_guard.py`:
   - Now checks that Notion push script has an existing-slot guard.
4. Patched `docs/agents/content-rules.md`:
   - Added Content Calendar Follow-through Audit procedure.
5. Patched `memory/content/posted-log.jsonl`:
   - Marked older duplicate X entries for 2026-05-11 through 2026-05-17 as superseded/banked.
6. Archived stale Notion X rows without Drive links for 2026-05-11 through 2026-05-17.

## Validation
```bash
python3 -m py_compile scripts/content_calendar_audit.py scripts/content_distribution_guard.py scripts/notion-calendar-push.py
python3 scripts/content_distribution_guard.py --weekly memory/content/weekly-2026-05-11.md --check-notion-script
python3 scripts/content_calendar_audit.py --week 2026-05-11
set -a; source ~/.config/env/global.env; set +a; python3 scripts/content_calendar_audit.py --week 2026-05-11 --with-notion
```

Results:
- `CONTENT_DISTRIBUTION_GUARD_PASS`
- `weekly: PASS`
- `posted_log: PASS`
- `crons: PASS`
- `notion: PASS`

Additional live checks:
- `openclaw cron runs` showed recent content reminder, Sunday, LinkedIn generation, and X generation all finished `ok`.
- `scripts/notion-calendar-push.py --dry-run` passes.
- Duplicate push test skipped existing Notion slot instead of creating a new duplicate.

## Score gates
| Gate | Status | Notes |
|---|---:|---|
| Calendar entries created | PASS | Current week has LinkedIn + X rows. |
| Drive links saved | PASS | Remaining Notion rows have Drive links. |
| Reminders delivered | PASS | Recent reminder and Sunday runs delivered. |
| Posted replies logged | PARTIAL | Process exists, deterministic inbound handler not found for content. |
| Guard before delivery | PASS | Reminder and generation prompts include guard; guard script passes. |
| Stale/placeholder blocking | PASS | Sunday SKIP_SLOT is explicit and blocked. |
| Performance feedback loop | PARTIAL | Sunday prompt exists; no evidence of deterministic metrics ingestion for all content. |
| No duplicate/repeat posts | PASS after fix | Local and Notion duplicates cleaned/guarded. |
| Current effort alignment | PASS | `current-efforts.md` is used; weekly file aligns to consulting/property/diagnostic. |
| Telegram length guard | PASS | Cron prompts include summary-style delivery; no >3500 char issue found in recent summaries. |

## Remaining blocker
Create one deterministic content posted-reply handler, analogous to the new health inbound handler.

First action: inspect OpenClaw Telegram/direct inbound routing hooks for `agent:main:telegram:direct:6608544825`, then route replies matching `posted`, `posted both`, `posted LinkedIn`, or `posted X` within 48 hours of a content-reminder/content-sunday send into a local script that updates `memory/content/posted-log.jsonl` with `posted: true`, `posted_date`, and URL when provided.

Why it matters: drafts currently become reviewable/postable, but the final posted state depends on Eve interpreting chat context correctly. That is the last fragile handoff.

Done state: simulated Telegram replies update only the intended latest content entries, platform-specific replies mark only that platform, duplicates are idempotent, non-content replies bypass, and a confirmation is sent back to JT.

## Report path
`memory/audits/xhigh-systems/2026-05-13-content-calendar-followthrough.md`
