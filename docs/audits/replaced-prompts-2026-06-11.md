# Replaced Content Cron Prompts - 2026-06-11

Source backup: /Users/jtsomwaru/.openclaw/cron/jobs.json.backup-phase4-20260611134656

Captured from the pre-Phase-4 cron jobs backup after remediation; these are the payload.message values replaced during Phase 4.

## content-generate-linkedin

- Previous model: `openai/gpt-5.5`
- Prompt bytes: 3201

```text
Generate the weekly LinkedIn queue, but only deliver after local quality guards pass.

MANDATORY PRE-FINAL GUARD:
After writing `memory/content/weekly-[MONDAY-DATE].md` and before Drive/Telegram/Notion finalization, run:
```bash
cd /Users/jtsomwaru/.openclaw/workspace
python3 scripts/content_distribution_guard.py --weekly memory/content/weekly-[MONDAY-DATE].md --require-reference-map linkedin --check-notion-script
```
If the guard fails, do NOT send approved copy and do NOT push Notion entries. Send a concise BLOCKED packet with failing lines and local path.

Task:
1. Read `memory/content-voice.md`, `memory/content/current-efforts.md`, `memory/content/weekly-seeds.md`, Wednesday skill if building Wednesday case study, and platform/niche-filtered Notion swipe references. Do NOT use unfiltered all-platform swipe fetches for generation. Run narrow fetches first, e.g. `python3 scripts/notion-swipe-fetch.py --platform LinkedIn --niche "AI Consulting" --niche "Personal Brand" --limit 8 --since-days 30 --fetch-limit 200`. If fewer than 3 usable current LinkedIn references exist, write `RECENT_SWIPE_GAP` and either use labeled adjacent inspiration or skip weak slots.
2. Generate buyer-facing LinkedIn posts that support JT's consulting/product-builder credibility. Block self-undermining mistake/correction narratives unless explicitly requested.
3. Write `## LinkedIn Reference Mechanics` and the LinkedIn section to `memory/content/weekly-[MONDAY-DATE].md`. Each reference row must include `Source URL`, `Platform`, `Niche`, `Format`, `Hook mechanic`, and `JT translation`. Generic claims like "Notion swipe references checked" do not count.
4. Before running the guard, audit every LinkedIn draft against these six blockers and revise or skip any slot that fails: first line names a buyer-recognizable workday problem instead of a build, product, or feature; zero em dashes; no -ly adverbs or vague declaratives; build-showcase endings state what the build does rather than advising the reader; each post creates a felt reaction; each post includes one concrete number, proper noun, or workflow detail. Log the audit result briefly under the LinkedIn section.
5. Run the guard.
6. If guard passes, upload to Drive and send action-first review packet. If no non-empty content: SKIP THE TELEGRAM SEND.

Hard rules: no em dashes, no placeholders, no `[Source]`, no fake client anecdotes, no public posting. JT presses send.

MANDATORY POSTED-LOG FINALIZATION:
Before announcing success, append one `memory/content/posted-log.jsonl` row for every LinkedIn slot created for the week. Rows must include date, platform=`linkedin`, day, pillar, topic/summary, posted=false, banked=false, scheduled_in_notion=true when pushed to Notion, drive_link, and source_weekly. Then verify with:
```bash
python3 - <<'PY2'
import json
from pathlib import Path
rows=[json.loads(l) for l in Path('memory/content/posted-log.jsonl').read_text().splitlines() if l.strip()]
week='[MONDAY-DATE]'
print([r for r in rows if r.get('platform')=='linkedin' and r.get('source_weekly')==f'memory/content/weekly-{week}.md'])
PY2
```
If zero rows are found, do NOT claim the LinkedIn queue is ready; send a blocker instead.
```

## content-generate-x

- Previous model: `openai/gpt-5.5`
- Prompt bytes: 2947

```text
Generate the weekly X queue, but only deliver a review packet after local quality guards pass.

MANDATORY PRE-FINAL GUARD:
After writing/appending `memory/content/weekly-[MONDAY-DATE].md` and before Telegram/Notion/Drive finalization, run:
```bash
cd /Users/jtsomwaru/.openclaw/workspace
python3 scripts/content_distribution_guard.py --weekly memory/content/weekly-[MONDAY-DATE].md --require-reference-map x --check-notion-script
```
If the guard fails, do NOT push Notion calendar entries and do NOT send approved copy. Send a concise BLOCKED packet with failing lines and local path.

MANDATORY X POST QUALITY AUDIT:
Before running the distribution guard or sending Telegram/Notion/Drive finalization, audit every generated X post against these six checks. Revise the draft until all relevant checks pass; if any check cannot pass, skip that slot and log `X_POST_AUDIT_BLOCKED`.
1. First line opens with the point, with no warmup or preamble.
2. Post body contains no external links.
3. Post contains no hashtags.
4. Thursday hot-take/debate posts make a specific operator claim only someone who runs autonomous agents or consulting work would write; generic AI takes fail.
5. Build-showcase posts end with capability proof: final line says what the build does, not advice for the reader.
6. No em dashes and no banned adverbs from content voice.

Task:
1. Read `memory/content-voice.md`, `memory/content/current-efforts.md`, `memory/content/weekly-seeds.md`, current weekly content file if present, and platform/niche-filtered Notion swipe references. Do NOT use unfiltered all-platform swipe fetches for generation. Run narrow fetches first, e.g. `python3 scripts/notion-swipe-fetch.py --platform X --niche "AI Consulting" --niche "AI Agents" --niche "Personal Brand" --limit 10 --since-days 30 --fetch-limit 200`. For product/crypto slots use `--niche "Nash Satoshi" --niche "Crypto"`; for app/product slots use `--niche "Vista" --niche "App Marketing"`. If fewer than 3 usable current X references exist, write `RECENT_SWIPE_GAP` and either use labeled adjacent inspiration or skip weak slots.
2. Generate platform-native X posts using current proof/current signals. Do not force weak seedless slots.
3. Append/update `## X Reference Mechanics` and only the X section in `memory/content/weekly-[MONDAY-DATE].md`; do not overwrite LinkedIn. Each reference row must include `Source URL`, `Platform`, `Niche`, `Format`, `Hook mechanic`, and `JT translation`. Generic claims like "Notion swipe references checked" do not count.
4. Run the guard above.
5. If guard passes, upload the complete weekly file to Drive, push Notion Calendar entries with `scripts/notion-calendar-push.py`, update posted-log.jsonl, and send action-first Telegram review packet. If no non-empty content: SKIP THE TELEGRAM SEND.

Hard rules: no em dashes, no placeholders, no `[Source]`, no generic AI claims, no fake client anecdotes, no public posting. JT presses send.
```
