# Mistakes Log — Recent Entries
> Source: AGENTS.md §Mistakes Log
> Full archive: docs/agents/mistakes-log.md

## Logging Rule
Every entry MUST have all three: (1) specific failure, (2) root cause one level deeper than "I forgot," (3) concrete rule that prevents recurrence. A mistake entry without a rule is incomplete — finish it before moving on.

## Recent Entries (2026-04)

| Date | Mistake | Fix |
|------|---------|-----|
| 2026-04-11 | outreach-pipeline: April 1 batch (7 prospects) all had M1 sent correctly but M2 MC tasks were never created. Pipeline logged M2 due dates but no MC task was created → 6 days of silence on 7 warm prospects. Root cause: process logged the due date but skipped the step of creating the actual Mission Control task for M2. | Rule: **Whenever M1 is sent and logged with an M2 due date, immediately create the M2 MC task on that date. Do not defer. Do not batch. The pipeline must never log a follow-up date without also creating the task to send it.** |
| 2026-04-08 | Telegram delivery failures across multiple crons (niche-monitor, Spanish Weekly Eval, crypto morning) — content generated correctly but empty/minimal messages rejected by Telegram. Root cause: crons send "All clear" or zero-content Telegram messages when no findings exist. Each cron fixed individually. | Rule: **All crons that save content + send Telegram: must skip Telegram send if content is empty or "All clear." Add `If no new [findings]: SKIP THE TELEGRAM SEND` to every Telegram-capable cron payload. Already applied: niche-monitor, Spanish Weekly Eval, crypto morning.** |
| 2026-04-05 | Bootstrap files exceeded safe limits (AGENTS.md 32,311 / MEMORY.md 24,116 / TOOLS.md 19,030). Groq fallback never worked. LCM compaction failing silently. Retry loops burning rate limit. Root cause: no pre-append size check enforced, Groq free tier TPM too low for compaction, fallback model same provider as primary. | Rule: **Check `wc -c` before every append. Use openrouter/gpt-4o-mini as fallback (same provider as primary). LCM summaryModel must be Gemini Flash-Lite via openrouter. Max 3 retries with exponential backoff then stop + alert.** |
| 2026-04-02 | Resume and cover letter generated with em dashes throughout. Root cause: wrote files directly without loading job-application/SKILL.md first. | Rule: **Load job-application/SKILL.md before writing a single word of any application package.** |
| 2026-03-25 | Cover letter uploaded blank — body missing. Root cause: `parse_cover_letter_md()` requires exactly two `---` separators; had only one. | Rule: **Cover letter markdown must have two `---` separators. Always run `parse_cover_letter_md()` verification before uploading.** |
