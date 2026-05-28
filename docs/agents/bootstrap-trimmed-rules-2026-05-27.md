# Bootstrap-Trimmed Rules — 2026-05-27
> Source: `AGENTS.md`. Extracted to keep bootstrap files near 90% of budget.

## Outreach Send Confirmation Handler
When JT confirms sending outreach (any variant of "sent", "done", "sent it", "just sent"), this is an outreach send confirmation — update status in the SAME TURN, not later.

Detection patterns:
- "sent M1/M2/M3 to [Company]" or "sent to [Company]"
- "sent it to [Company]"
- "[Company] sent" in outreach context
- "sent via LinkedIn/Email"
- Any message within 30 minutes of an outreach review that contains "sent"

Same-turn procedure:
1. Parse from context: prospect name/slug, message number, channel, date.
2. Run:
   `python3 scripts/outreach_update.py --slug [slug] --company "[Company]" --message [M1|M2|M3] --channel [LinkedIn|Email] --date [YYYY-MM-DD]`
3. Confirm updated files/tasks to JT.
4. Log to today's daily note under `## Outreach Sends`.

Slug lookup: company name → `~/projects/jt-consulting-pipeline/clients/[slug]/outreach-draft.md`; if unknown, search client folders. Channel default: LinkedIn if contact has LinkedIn, else Email.

## API Key Exposure Prevention
Root cause of OpenRouter key revocation: API key embedded in workspace files and scanned. Keys live only in approved env/auth files.

Rules:
1. Never embed API keys in code, project files, daily notes, docs, or uploaded content. Approved homes only: `~/.config/env/global.env`, `auth-profiles.json`, `models.json`, and approved `openclaw.json` auth sections.
2. Never modify `auth-profiles.json`, `models.json`, `openclaw.json` auth section, `summaryModel`, or `summaryProvider` without JT approval.
3. Before writing any externally shared/uploaded/pushed file, scan for key patterns (`sk-or-v1`, `sk-ant-`, `Bearer`, long hex/base64) and redact.
4. If a key must be referenced, use `[REDACTED]` or `YOUR_KEY_HERE`.

## Cron Safety Detail
- Never use `deleteAfterRun: true`; it creates scheduler loops.
- LaunchAgents are for zero-LLM automation only. New LaunchAgent requires JT approval.
- Never schedule more than two jobs in the same 15-minute window. On `rate_limit`, wait at least 10 minutes.
- Cron volume guard: `python3 scripts/cron_volume_guard.py` must pass. Current hard caps: <=35 scheduled invocations/day average and <=28 agentTurn/day average; >30/day warns.
- Post-restart drift: crons may fire early. Skip if >2h before scheduled window, log, run `cron list`; do not recreate.
- Timeout sizing: when cron complexity increases, check latest duration and bump timeout before failure if it is near ceiling.
- Telegram delivery guard: crons that save content locally and send Telegram must skip sending empty or "All clear" messages.
