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
