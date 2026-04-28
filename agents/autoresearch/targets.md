# Autoresearch Targets Registry
*Managed by Eve. Updated whenever a new skill/agent is enrolled.*
*Overnight agent reads this file and runs enrolled targets monthly (or on-demand).*

## How to enroll a new target
1. Draft checklist (≤6 yes/no questions) → save to `checklists/[skill-slug].md`
2. Append a row to the Active Targets table below
3. Note enrollment in reply to JT

## Scoring
- Score = fraction of checklist items passing, averaged across all test inputs
- Target score: 90% (0.90)
- Loop stops when score hits 90%+ three consecutive rounds, or at max 20 rounds
- Estimated cost per run: $0.10–0.20

---

## Active Targets

| Slug | Skill/Agent Path | Checklist | Status | Last Score | Last Run | Added |
|------|-----------------|-----------|--------|------------|----------|-------|
| cold-email | skills/cold-email/SKILL.md | checklists/cold-email.md | stable | 0.944 | 2026-04-11 | 2026-03-19 |
| t3-cold-hook | agents/t3-cold-hook/AGENT.md | checklists/t3-cold-hook.md | stable | 1.000 | 2026-04-01 | 2026-03-19 |
| content-linkedin | (content-generate-linkedin cron payload) | checklists/content-linkedin.md | active | 0.833 | 2026-03-31 | 2026-03-19 |
| content-x | (content-generate-x cron payload) | checklists/content-x.md | active | 0.900 | 2026-03-20 | 2026-03-19 |
| wednesday-linkedin | skills/wednesday-linkedin/SKILL.md | checklists/wednesday-linkedin.md | active | 0.920 | 2026-03-24 | 2026-03-22 |
| vibe-marketing | agents/vibe-marketing/AGENT.md | checklists/vibe-marketing.md | stable | 0.900 | 2026-03-30 | 2026-03-22 |
| job-application | skills/job-application/SKILL.md | checklists/job-application.md | stable | 1.000 | 2026-03-30 | 2026-03-22 |
| overnight | agents/overnight/ (overnight cron payload) | checklists/overnight.md | stable | 1.000 | 2026-03-31 | 2026-03-29 |
| outreach-email-pivot | scripts/outreach_email_pivot.py + cron payload | checklists/outreach-email-pivot.md | pending | — | — | 2026-04-27 |
| runbook | skills/runbook/SKILL.md | checklists/runbook.md | pending | — | — | 2026-04-12 |
| opticfy-pipeline | skills/opticfy-pipeline/SKILL.md | checklists/opticfy-pipeline.md | pending | — | — | 2026-04-20 |
| passive-income-scout | agents/passive-income-scout/AGENT.md | checklists/passive-income-scout.md | pending | — | — | 2026-04-20 |
| content-scheduler | agents/content-scheduler/AGENT.md | checklists/content-scheduler.md | pending | — | — | 2026-04-20 |
| vibe-post | scripts/vibe-post.py | checklists/vibe-post.md | pending | — | — | 2026-04-20 |
| content-generation | skills/content-generation/SKILL.md | checklists/content-generation.md | pending | — | — | 2026-04-26 |
| google-drive | skills/google-drive/SKILL.md | checklists/google-drive.md | pending | — | — | 2026-04-26 |
| google-slides | skills/google-slides/SKILL.md | checklists/google-slides.md | pending | — | — | 2026-04-26 |
| notion-integration | skills/notion-integration/SKILL.md | checklists/notion-integration.md | pending | — | — | 2026-04-26 |
| system-auditor | skills/system-auditor/SKILL.md | checklists/system-auditor.md | pending | — | — | 2026-04-26 |
| ux-architecture | skills/ux-architecture/SKILL.md | checklists/ux-architecture.md | pending | — | — | 2026-04-26 |
| video-generation | skills/video-generation/SKILL.md | checklists/video-generation.md | pending | — | — | 2026-04-26 |
| sports-gm | skills/sports-gm/SKILL.md | checklists/sports-gm.md | pending | — | — | 2026-04-27 |

## Status values
- `pending` — checklist written, not yet run
- `active` — has run at least once, loop in progress or complete
- `stable` — scored 90%+ on last run, loop complete, monitor monthly
- `paused` — skill changed significantly, checklist needs re-review before next run

---

## Graduated / Archived

| Slug | Final Score | Rounds | Improvements | Archived |
|------|-------------|--------|--------------|----------|
| — | — | — | — | — |
