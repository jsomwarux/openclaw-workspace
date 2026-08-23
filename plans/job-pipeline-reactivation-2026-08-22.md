# Revised Job Pipeline Reactivation Plan

**Goal:** Reactivate a low-noise employment hedge that surfaces only evidence-backed, realistically competitive roles for JT and builds application packages only after JT approval.

**Approved:** JT approved the revised design on 2026-08-22.

## Scope

- Archive the legacy research, auto-builder, skill-project, consulting-artifact, and market-trend behavior before rewriting anything.
- Rewrite `Job Market Daily Research` for weekday role discovery based on responsibilities and demonstrated evidence, not title similarity.
- Keep `Job Application Auto-Builder` disabled. Application packages remain on-demand after JT selects a role.
- Enable `Job Application Tracker` on its existing Tuesday/Thursday schedule.
- Use `openai/gpt-5.6-sol` through OAuth for application packages by default. Sonnet becomes an explicit comparison/escalation option, not the default.
- Preserve the $150K salary floor, NYC/remote constraint, no-relocation rule, and no developer/ML/Apex/SFDX/pre-sales targeting.

## Acceptance Criteria

- [x] Full legacy cron definitions are stored in a dated archive.
- [x] Research cron runs Monday-Friday at 5:15 AM ET and announces a compact Telegram brief to JT.
- [x] Research prompt contains task context, detailed constraints, immediate task, exact output format, evidence-backed competitiveness gates, live-posting verification, and state/proof requirements.
- [x] Auto-builder remains disabled.
- [x] Tracker is enabled Tuesday/Thursday at 10:15 AM ET.
- [x] Job-application skill and durable instruction surfaces name GPT-5.6 Sol as the default.
- [x] Deterministic guards and live cron inspection pass.
- [x] No application, employer outreach, deploy, or external non-JT message occurs.

## Verification

- Inspect all three jobs with the live cron API.
- Run `python3 scripts/cron_volume_guard.py`.
- Run `python3 scripts/model_routing_guard.py --include-disabled`.
- Validate archive JSON with `jq`.
- Search prompt/model surfaces for stale Sonnet-only application rules.
- Write a claim file and proof record; do not report completion without fresh evidence.
