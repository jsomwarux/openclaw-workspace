# Monthly Prompt Rewrite Proposals - 2026-08-02

Source note: `/Users/jtsomwaru/.openclaw/cron/jobs.json` was not present; used same-run `openclaw cron list --json` export at `/tmp/wsr-cron-list-2026-08-02.json`.

No rewrites were installed. JT approval required per prompt.

## Five Longest Live Payloads

1. `Weekly Systems Review` (`b2ca53ab-0c07-4a22-8424-9d39bf988405`) - 1798 words, 13523 chars - proposal: `weekly-systems-review.md`
2. `prospect-discovery` (`ebb843af-e752-4c65-923d-540d5ff5ad3f`) - 1481 words, 11141 chars - proposal: `prospect-discovery.md`
3. `Friday Scoreboard` (`18169759-7450-4e06-8db0-e0d14fbc25fd`) - 445 words, 3343 chars - proposal: `friday-scoreboard.md`
4. `Daily Send Sheet` (`eve-morning-brief-001`) - 440 words, 3138 chars - proposal: `daily-send-sheet.md`
5. `outreach-pipeline` (`651fa1da-84d7-44b3-8e10-6a46e1c05cf6`) - 277 words, 2131 chars - proposal: `outreach-pipeline.md`

## Convex Instance Secret Finding

- Local grep found `scripts/eve_audit_collect.py` already redacts `--instance-secret` in process output.
- Prior local audits recorded that Convex local backend still exposes `--instance-secret` in argv and that no supported bind/host alternative was found.
- Fresh web search found Convex docs/issues about environment variables, but no current evidence that the local backend instance secret can be moved from argv into env/keychain/config without changing the runtime approach.
- Recommendation: keep redaction guard; do not change Convex runtime config without JT approval.
