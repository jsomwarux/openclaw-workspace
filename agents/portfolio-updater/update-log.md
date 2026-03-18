# Portfolio Updater — Run Log

## 2026-02-27 (initial setup)
- System initialized
- Existing projects seeded into state.json: construction-tracker, streeteasy-scraper, nash-satoshi, vista, glow-index
- Demand scores cached based on current skills-demand-tracker data
- Queue: empty
- Next reorder: will run at next overnight check (2026-02-28 3AM)

## 2026-02-28 (Overnight Run)
- Items in queue processed: 0 (2 new items added to queue tonight)
- Items queued for next run:
  - opticfy-pipeline (score: 8/10, auto-approve) — coding agent needed, deferred (sub-agent limit)
  - conversationfirst-framework (score: 6/10, flagged to JT via overnight log)
- Demand reorder: no (last reorder: 2026-02-27)
- Skills grid updated: no
- Vercel deploy triggered: no
- Note: MC task done-check identified opticfy-pipeline as newly completed, not in addedSlugs; queued.

## 2026-03-02
- Items in queue: 3 (1 opticfy-pipeline unprocessed, 2 ConversationFirst variants already decided)
- Auto-approved: opticfy-pipeline (8/10 — commit 9f2c1c0, live on jtsomwaru.com)
- Flagged to JT: none
- Skipped: ConversationFirst (already marked methodology_added per JT decision 2026-02-28)
- Demand reorder: yes — opticfy-pipeline (46) is now highest-demand project; reorder triggered (opticfy-pipeline → nash-satoshi → construction-tracker → streeteasy-scraper → glow-index → vista)
- Skills grid updated: no (no new tools added that aren't already in About.tsx)
- Vercel deploy triggered: yes (via git push, commit 9f2c1c0 + reorder commit pending)

## 2026-03-06 (Overnight)
- Items in queue: 5 (opticfy-pipeline, conversationfirst, b2b-account-service-agent, pm-operations-agent, support-triage-demo) + 2 new (n8n-insurance-claims, n8n-lead-qual scored tonight)
- Auto-approved: b2b-account-service-agent (8/10) — card added to site (commit b3e553c); n8n-support-triage (8/10) — card added to site (commit b3e553c)
- Already on site (state.json updated): ai-insurance-claims-triage, ai-lead-qualification, wholesale-inventory-reorder, construction-trades-workflow, adversight-ai, pm-operations-agent
- Flagged to JT: none
- Skipped: none
- Demand reorder: no (4 days since last reorder, < 7-day threshold)
- Skills grid updated: no (all tech already in About.tsx)
- Vercel deploy triggered: yes (git push main → auto-deploy)

## 2026-03-10 (Overnight Run)
- Items in queue: 7 total (all previously processed except b2b-account-service-agent)
- Auto-approved: b2b-account-service-agent (scored 8/10 — in queue as pending_build since 2026-03-04)
- Flagged to JT: none
- Skipped: all other queue items already have status=added or methodology_added
- Demand reorder: YES — updated scoring guide (added AgentScript:9, Apex:8, Flow:7), reordered featured projects by score descending: pm-tenant(34) → insurance(34) → b2b(27) → nash-satoshi(20) → ai-claims/wholesale/adversight/support-triage(16) → construction-trades(8)
- Skills grid updated: no
- Vercel deploy triggered: YES — commit bf41a2d pushed to main (Vercel auto-deploys)
- Scoring guide fix: Added AgentScript(9), Apex(8), Flow(7) to AGENT.md — prior guide undervalued Agentforce projects since companion skills weren't scored

## 2026-03-12 (Overnight Run)
- Items in queue: 8 | Unscored: 3 → all resolved (ConversationFirst: already decided; PM Ops Agent + n8n Support Triage: already in addedSlugs)
- Auto-approved tonight: none (no new builds)
- Flagged to JT: none
- Skipped: none
- Demand reorder: no (lastReorderDate 2026-03-10, within 7-day window)
- Skills grid updated: no
- Vercel deploy triggered: no
- Queue housekeeping: marked 3 stale unscored entries as scored/processed

## 2026-03-15 (Overnight Recovery Run — fired 11:13 AM, gateway down overnight)
- Items in queue: 8 | Orphaned pending_build: 2 (n8n-insurance-claims, n8n-lead-qualification) — resolved (both live on site under ai-insurance-claims-triage / ai-lead-qualification, added 2026-03-06)
- Auto-approved: none
- Flagged to JT: none
- Skipped: none
- Demand reorder: no (lastReorderDate 2026-03-10, 5 days ago — under 7-day threshold)
- Skills grid updated: no
- Vercel deploy triggered: no
- Queue housekeeping: 2 stale pending_build entries marked resolved

## 2026-03-16 (3AM Overnight Run)
- **Construction Job Tracker** — score 7/10, auto-approved. Added to queue.jsonl (status: approved_pending_build). MC task pushed: "🌙 Build: Add Construction Job Tracker portfolio card to jtsomwaru.com (7/10 auto-approved)". Slug added to state.json addedSlugs.
- **PM Maintenance Triage** — score 6/10, flagged to JT. Added to queue.jsonl (status: flagged_jt_decision). MC task pushed: "🌙 Portfolio decision: PM Maintenance Triage n8n Template scored 6/10 — add to site?"

## 2026-03-17
- Items in queue: 1 pending (construction-job-tracker, score 7/10, auto-approved)
- Auto-approved: construction-job-tracker
- Flagged to JT: none
- Skipped: none
- Demand reorder: no (lastReorderDate: 2026-03-10, 7 days ago — exactly at threshold, skipping reorder to avoid churn)
- Skills grid updated: no
- Vercel deploy triggered: yes (commit c735b48)
