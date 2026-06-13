# Active Cron Audit Proposal - 2026-06-12

Status: proposal only. No cron disable/merge edits executed in this report.

Drive: https://docs.google.com/document/d/1V8z3l2m7eX3F7UDIYbGmZDzu52URdyBLtBY0m1H17zM/edit

Evidence used:
- Active cron list: `openclaw cron list --json` on 2026-06-12 showed 49 enabled jobs.
- Volume guard: `python3 scripts/cron_volume_guard.py` showed 49 enabled jobs, ~198.46 weekly invocations, ~28.35 daily average, ~24.35 agent-turn daily average.
- Cost snapshot: `python3 scripts/cost-tracker.py --snapshot` returned `{"status":"ok","date":"2026-06-12","total_usd":0.5226,"sessions":20}`.
- Per-cron cost caveat: cron run history exposes model/usage summaries, but not reliable per-cron USD. Cost column below is therefore evidence-based where possible and marked UNVERIFIED where per-job USD is unavailable.

## Active Cron Table

| Cron | ID | Schedule | Class | Last useful output date | Cost evidence | Proposal |
|---|---|---|---|---|---|---|
| TikTok App Account Warm-up Reminder (2 PM) | `8033e775-29d2-42f2-83e9-1392352f6493` | `0 14 * * *` | produces-reading | 2026-06-11 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Disable; app marketing warm-up is frozen. |
| Pending Task Processor | `f18cace3-b9e9-4d99-a7a3-625bb121b30c` | `30 10,14,18,22 * * *` | produces-pipeline | 2026-06-12 | System event; likely $0 LLM, per-job USD UNVERIFIED | Keep, but consider 2x/day if pending queue stays quiet. |
| ReelFarm Daily Strategy Intel | `a97df783-31c5-4269-a4f0-3ece75af838d` | `15 17 * * *` | produces-reading | 2026-06-11 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Disable; ReelFarm/app marketing paused. |
| Evening Digest | `evening-digest-001` | `0 19 * * *` | produces-reading | 2026-06-11 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Keep as consolidation layer. |
| Crypto Evening Pulse (9 PM) | `eve-crypto-evening-010` | `30 20 * * *` | produces-reading | 2026-06-11 | GPT-5.5 OAuth latest run plus crypto scripts; per-job USD UNVERIFIED | Merge into one daily crypto digest with hard alert thresholds. |
| Health Check-in (Pattern-Focused) | `6be7f564-5cec-47e7-b67c-9b2fcc3ed8de` | `0 21 * * *` | produces-reading | 2026-06-11 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Keep; health is base layer. |
| Night Autonomy Agent | `f146d8b8-94e0-49ff-8e4a-5050a284e894` | `0 23 * * *` | produces-proof | 2026-06-11 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Keep, but restrict to pipeline/proof/ops lanes. |
| outreach-pipeline | `651fa1da-84d7-44b3-8e10-6a46e1c05cf6` | `0 3 * * *` | produces-pipeline | 2026-06-12 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Keep; core acquisition engine. |
| Job Market Daily Research | `eve-job-market-daily-005` | `15 5 * * *` | produces-reading | 2026-06-12 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Reduce to weekly market-intel memo; exact-fit/inbound only. |
| passive-income-fetch-signals | `f368e18b-1723-47ad-9164-94e95c106902` | `30 5 * * 6` | produces-reading | 2026-06-06 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Disable; new app ideation killed until revenue trigger. |
| Crypto Full Analysis (6 AM) | `eve-crypto-morning-008` | `0 6 * * *` | produces-reading | 2026-06-12 | GPT-5.5 OAuth plus possible X/API/script cost; per-job USD UNVERIFIED | Merge into one daily crypto digest with hard thresholds. |
| Job Application Auto-Builder | `b2357bd5-651d-4151-80df-49e4a928826f` | `15 6 * * *` | produces-pipeline | 2026-06-12 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Disable unless exact-fit $180K+ role is approved. |
| outreach-email-pivot-daily | `9d9b165b-a52f-4dc6-bc02-58f154bcff06` | `45 6 * * *` | produces-pipeline | 2026-06-12 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Merge into outreach-pipeline. |
| Skills & API Researcher - Weekly Synthesis | `05024e45-57fc-4e7c-a236-660e6eb5393f` | `0 7 * * 6` | produces-reading | 2026-06-06 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Keep only as weekly synthesis. |
| Morning Brief | `eve-morning-brief-001` | `30 7 * * *` | produces-reading | 2026-06-12 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Keep. |
| content-reminder | `5e66b4ee-aee3-497d-90ba-7aad670970a3` | `0 8 * * 2,3,4,5,6` | produces-proof | 2026-06-12 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Merge into one case-study derivative content cron. |
| Daily DynastyJig Niche-Growth X Post Pack | `1e614c8a-adb8-4a02-b35f-3031db55b337` | `30 8 * * *` | produces-proof | 2026-06-12 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Disable unless Action Arena gate is approved. |
| critical-files-integrity | `ee357abb-2b58-44b8-8f03-4c152611117d` | `0 9 * * *` | produces-proof | 2026-06-12 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Keep, or move into Weekly Systems Review if daily proof is excessive. |
| dynasty-replies-gen | `8b968751-6e59-42e5-b2ce-09f57d36176c` | `0 11 * * *` | produces-proof | 2026-06-12 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Disable unless Action Arena gate is approved. |
| Skills & API Researcher - Daily Scan | `4c437ff5-02cd-4288-8e6e-6e6fc07203ce` | `30 11 * * 1-6` | produces-reading | 2026-06-12 | GPT-5.5 OAuth latest run; currently error | Disable daily; merge into weekly synthesis. |
| reddit-daily-gen | `bbe49024-458a-4496-9c7c-7a278615810f` | `30 11 * * *` | produces-proof | 2026-06-12 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Disable; no generic app promotion during freeze. |
| Crypto Midday Pulse (12 PM) | `eve-crypto-midday-009` | `0 12 * * *` | produces-reading | 2026-06-12 | GPT-5.5 OAuth plus scripts; per-job USD UNVERIFIED | Merge into one daily crypto digest with hard thresholds. |
| prospect-discovery | `ebb843af-e752-4c65-923d-540d5ff5ad3f` | `0 0 * * 0,3` | produces-pipeline | 2026-06-10 | latest run error/no auth; per-job USD UNVERIFIED | Replace broad cron with property-management lookalike/enrichment cadence. |
| weekly-unemployment-cert | `ac53b979-44c6-481b-b2aa-7cb9203e6476` | `0 7 * * 0` | produces-reading | 2026-06-07 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Keep until unemployment no longer active. |
| Weekly Intelligence Synthesis | `eve-weekly-synthesis-007` | `0 8 * * 0` | produces-reading | 2026-06-07 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Keep, but absorb niche/skills monthly overlap. |
| content-sunday | `d918122d-d58c-4985-a181-126cfd7e6be7` | `0 9 * * 0` | produces-proof | 2026-06-07 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Merge into one case-study derivative content cron. |
| Weekly Health Report | `eve-health-report-004` | `20 9 * * 0` | produces-reading | 2026-06-07 | GPT-5.5 OAuth latest run; latest summary says send failed | Keep but fix/verify delivery. |
| Weekly Systems Review | `b2ca53ab-0c07-4a22-8424-9d39bf988405` | `0 10 * * 0` | produces-proof | 2026-06-07 | GPT-5.5 OAuth latest run; currently error | Keep after fixing error; this is systems maintenance. |
| passive-income-scout | `39435f7a-1102-49f0-8eec-4f7e0c38e7d5` | `0 13 * * 0` | produces-reading | 2026-06-07 | GPT-5.5 OAuth latest run; currently error | Disable; new app ideation killed. |
| passive-income-strategist | `922082ee-da62-4b6e-b9e3-909c3446e381` | `0 15 * * 0` | produces-reading | 2026-06-07 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Disable with Scout. |
| passive-income-strategist-delivery-guard | `e7d45070-1443-4cca-9776-8b016d97e225` | `20 15 * * 0` | produces-reading | 2026-06-07 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Disable if Strategist disabled. |
| ReelFarm Weekly Strategy Synthesis | `bb0819d0-8900-4e2a-99a2-28ab950365ab` | `0 17 * * 0` | produces-reading | 2026-06-07 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Disable; ReelFarm paused. |
| Weekly North Star Command Center | `29772d9b-e007-4f62-9df9-e80b73d0cd21` | `0 18 * * 0` | produces-pipeline | 2026-06-07 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Keep. |
| Weekly Strategic Gut-Check | `d5290646-02a4-4682-9efe-d6577316e8fc` | `30 18 * * 0` | produces-reading | 2026-06-11 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Keep only if merged into North Star weekly review or monthly critic. |
| AI Ops Teardown Weekly Draft | `f96cc24f-55e6-4064-a075-b897156a22f2` | `15 19 * * 0` | produces-proof | 2026-06-07 | GPT-5.5 OAuth latest run; currently error | Reframe to case-study derivatives only or disable. |
| vibe-marketing-generate | `870bf3ff-55c9-49c0-9970-361c81a0920b` | `45 4 * * 1` | produces-proof | 2026-06-08 | GPT-5.5 OAuth latest run; currently error | Disable; marketing crons for Vista/Nash/Glow off. |
| Viral Post Swipe File - X Research | `33b8b0a2-e86c-4f51-aa4f-b8537def3107` | `45 5 * * 1,3,5` | produces-reading | 2026-06-12 | GPT-5.5 OAuth plus possible X/API; per-job USD UNVERIFIED | Reduce to weekly case-study-only sourcing or disable. |
| content-generate-linkedin | `fe984519-ec58-4c6e-a096-9ac425f735a3` | `45 6 * * 1` | produces-proof | 2026-06-08 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Merge with X into one case-study derivative content cron. |
| app-marketing-weekly-scoreboard | `c7033613-feec-456c-b72b-135beaa89fe2` | `0 8 * * 1` | produces-reading | 2026-06-08 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Disable; app marketing crons off. Glow analytics task stays in MC, not cron. |
| content-generate-x | `cb8f29dd-0db1-4abd-b87e-3e7168ca4a97` | `0 9 * * 1` | produces-proof | 2026-06-08 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Merge with LinkedIn into one case-study derivative content cron. |
| Niche Intelligence Monitor | `eve-niche-monitor-006` | `0 9 * * 1-5` | produces-reading | 2026-06-12 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Reduce to weekly synthesis; propagate orange+ ICP changes only. |
| Daily News Hook | `4a70dda4-da77-4437-9e1d-9c3001e9e1f9` | `30 9 * * 1-5` | produces-proof | 2026-06-12 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Disable; generic AI takes lose to proof/case studies. |
| Autoresearch Sweep | `ec9f36d3-3bf8-4bc9-a4b1-06aa886a24ff` | `15 11 * * 1,3,5` | produces-proof | 2026-06-12 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Reduce to weekly or fold into Weekly Systems Review. |
| guyana-economic-opportunity-monitor | `d401b26a-bcde-44ba-9689-4ded28ac2b0e` | `0 12 * * MON` | produces-reading | 2026-06-08 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Disable/hold; Guyana validation-only until named buyer/problem/reply. |
| Sports GM Weekly Market Report | `008a349c-af59-4e6b-88bb-97f65dba61c6` | `0 9 * * 2` | produces-reading | 2026-06-09 | latest run error/no auth; per-job USD UNVERIFIED | Disable unless Action Arena gate approved. |
| Job Application Tracker | `b0b04601-7518-4681-9761-4bbe5054ce9b` | `15 10 * * 2,4` | produces-reading | 2026-06-11 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Reduce to weekly or Morning Brief check. |
| Reminder: YouTube TV midday | `113e3870-13b4-47d3-a325-c9fef056e44d` | `2026-06-25T16:15:00.000Z` | produces-reading | UNVERIFIED/none | one-shot future reminder; per-job USD not applicable | Keep until 2026-06-25 then remove/disable. |
| Monthly Goal-Skills Gap Analysis | `fdc2cf75-50d8-4466-bbb7-5a8683eb6afd` | `0 8 1 * *` | produces-reading | 2026-06-01 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Keep monthly, but tie to KPIs only. |
| Monthly Niche Fitness Review | `1e2cf966-d5d6-4fe4-8ffc-f19ed3a5c094` | `30 9 1 * *` | produces-reading | 2026-06-01 | GPT-5.5 OAuth latest run; per-job USD UNVERIFIED | Merge into Weekly/Monthly Intelligence Synthesis. |

## Kill / Merge Proposal To Get Under 15

Target active recurring crons after approval: 14 recurring + 1 temporary one-shot reminder.

Keep:
1. Morning Brief.
2. Evening Digest.
3. Health Check-in.
4. Weekly Health Report after delivery verification.
5. Night Autonomy Agent.
6. Pending Task Processor, reduced to 2x/day if queue remains quiet.
7. outreach-pipeline.
8. one property-management prospect enrichment / lookalike cadence, replacing broad prospect-discovery.
9. Weekly Systems Review after error fix.
10. Weekly North Star Command Center.
11. critical-files-integrity, or fold into Weekly Systems Review if daily check is overkill.
12. one case-study derivative content cron replacing content-reminder, content-sunday, LinkedIn, X, AI Ops Teardown, Viral Swipe, Reddit, and Daily News Hook.
13. one daily crypto digest replacing morning/full, midday, and evening pulses; alert only on hard thresholds.
14. weekly market-intel / job scan replacing daily job market, auto-builder, and job tracker.
15. Weekly Intelligence Synthesis combining skills, niche, monthly niche fitness, and monthly goal-skills gap signals where possible.

Disable immediately after approval:
- TikTok warm-up reminder.
- ReelFarm daily and weekly.
- passive-income-fetch-signals, passive-income-scout, passive-income-strategist, strategist guard.
- vibe-marketing-generate.
- app-marketing-weekly-scoreboard.
- Daily News Hook.
- reddit-daily-gen.
- DynastyJig daily pack, dynasty replies, Sports GM weekly unless Action Arena gate is approved.
- Guyana economic opportunity monitor until named buyer/problem/reply.

Merge after approval:
- Crypto morning/midday/evening -> one daily digest with hard thresholds.
- Vista/Nash/Glow marketing crons -> off; Glow analytics/monitoring remains as Mission Control task only, not marketing cron.
- Content crons -> one case-study derivative generator only; no generic AI takes or app-promo crons.
- Skills daily + niche monitor + monthly niche fitness + monthly goal-skills gap -> one weekly/monthly intelligence review.
- Outreach email pivot -> outreach-pipeline.
- Job market daily + auto-builder + tracker -> weekly exact-fit market memo, with package build only after role clears current criteria.
