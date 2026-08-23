# Subscription-Limit Cron Recovery Map — 2026-08-22

Internal control note. No cron/provider/config changes or external sends were performed.

## Live blocker

Four enabled agent-turn jobs are red on the same Codex subscription rate limit, with reset stated as 2026-08-27 00:13 ET:

- Nightly Claude Delta Packet Reminder
- outreach-pipeline
- Daily Send Sheet
- Friday Scoreboard

## Safe deterministic recovery surface

| Job | Deterministic/local recovery available | Current status | Boundary |
|---|---|---|---|
| outreach-pipeline | `python3 scripts/outreach_pipeline_runner.py --json` plus `python3 scripts/north_star_pipeline.py queue --limit 4 --write` | Recovered at 11:22; report written and send queue refreshed | No outreach send; no LLM copy unless preflight returns eligible review items |
| Daily Send Sheet | Current `memory/send-queue.md`, Mission Control APIs, local pipeline/payment evidence | Inputs are locally available, but no replacement delivery was sent from this heartbeat | Do not duplicate user notifications or claim delivery without an artifact |
| Nightly Claude Delta Packet Reminder | Reminder text is deterministic | No replacement cron run or delivery attempted | Do not change provider/model or duplicate reminders without a current delivery decision |
| Friday Scoreboard | Local evidence sources exist, but the job requires multi-source synthesis and repeat-offender digest | Not autonomously reconstructed in this heartbeat | Do not fabricate cash/sends/claims; cite evidence or report unknown |

## Decision

Keep the failed jobs unchanged until reset or explicit routing authority. Continue deterministic preflight/reconciliation only where the job contract already defines it, and keep delivery claims separate from locally recovered artifacts.
