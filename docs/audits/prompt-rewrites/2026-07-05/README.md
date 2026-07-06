# Prompt Rewrite Ritual - 2026-07-05

First Sunday monthly audit. These are proposed rewrites only; none were installed.

## Five Longest Live Cron Prompts
1. `33b8b0a2-e86c-4f51-aa4f-b8537def3107` - Viral Post Swipe File - X Research - 14,990 chars.
2. `eve-job-market-daily-005` - Job Market Daily Research - 14,166 chars.
3. `ebb843af-e752-4c65-923d-540d5ff5ad3f` - prospect-discovery - 11,141 chars.
4. `b2ca53ab-0c07-4a22-8424-9d39bf988405` - Weekly Systems Review - 10,671 chars.
5. `eve-weekly-synthesis-007` - Weekly Intelligence Synthesis - 9,520 chars.

## Convex Instance Secret Finding
`rg` found no live `--instance-secret` argv in Mission Control scripts, LaunchAgents, or app code. Current launch path uses `convex dev` / `npx convex dev`; `scripts/eve_audit_collect.py` only contains a redaction regex for `--instance-secret`.

Status: no runtime config change needed. If Convex later starts passing an instance secret in argv, move investigation to env/keychain/config support before changing LaunchAgents.
