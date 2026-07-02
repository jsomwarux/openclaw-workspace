# Autoresearch Targets Registry
*Managed by Eve. Updated whenever a new skill/agent is enrolled.*
*Autoresearch Sweep reads this file Mon/Wed/Fri 11:15AM ET and runs one high-value pending/active target; overnight/manual runs can also use it on demand.*

## How to enroll a new target
1. Draft checklist (≤6 binary yes/no questions, numbered `1.`–`6.`) → save to `checklists/[skill-slug].md`
2. Append a row to the Active Targets table below
3. Verify the target path and checklist path exist, unless the path is explicitly a cron/payload reference
4. Note enrollment in reply to JT

## Scoring
- Score = fraction of checklist items passing, averaged across all test inputs
- Target score: 90% (0.90)
- Standard loop stops when score hits 90%+ three consecutive rounds, or at max 20 rounds; recurring sweep is bounded to one target, 3 inputs, and max 5 rounds.
- Every run appends `agents/autoresearch/results.tsv` with keep/discard/crash status.
- Estimated cost per recurring sweep: capped at $0.50

---

## Active Targets

| Slug | Skill/Agent Path | Checklist | Status | Last Score | Last Run | Added |
|------|-----------------|-----------|--------|------------|----------|-------|
| cold-email | skills/cold-email/SKILL.md | checklists/cold-email.md | stable | 0.944 | 2026-04-11 | 2026-03-19 |
| t3-cold-hook | agents/t3-cold-hook/AGENT.md | checklists/t3-cold-hook.md | stable | 1.000 | 2026-04-01 | 2026-03-19 |
| content-linkedin | (content-generate-linkedin cron payload) | checklists/content-linkedin.md | stable | 1.000 | 2026-06-03 | 2026-03-19 |
| content-x | (content-generate-x cron payload) | checklists/content-x.md | stable | 1.000 | 2026-06-05 | 2026-03-19 |
| wednesday-linkedin | skills/wednesday-linkedin/SKILL.md | checklists/wednesday-linkedin.md | stable | 1.000 | 2026-06-22 | 2026-03-22 |
| vibe-marketing | agents/vibe-marketing/AGENT.md | checklists/vibe-marketing.md | stable | 0.900 | 2026-03-30 | 2026-03-22 |
| job-application | skills/job-application/SKILL.md | checklists/job-application.md | stable | 1.000 | 2026-03-30 | 2026-03-22 |
| overnight | agents/overnight/ (overnight cron payload) | checklists/overnight.md | stable | 1.000 | 2026-03-31 | 2026-03-29 |
| outreach-email-pivot | scripts/outreach_email_pivot.py + cron payload | agents/autoresearch/checklists/outreach-email-pivot.md | stable | 1.000 | 2026-05-22 | 2026-04-27 |
| runbook | skills/runbook/SKILL.md | checklists/runbook.md | pending | — | — | 2026-04-12 |
| passive-income-scout | agents/passive-income-scout/AGENT.md | checklists/passive-income-scout.md | stable | 1.000 | 2026-07-01 | 2026-04-20 |
| content-scheduler | agents/content-scheduler/AGENT.md | checklists/content-scheduler.md | pending | — | — | 2026-04-20 |
| vibe-post | scripts/vibe-post.py | checklists/vibe-post.md | pending | — | — | 2026-04-20 |
| content-generation | skills/content-generation/SKILL.md | checklists/content-generation.md | pending | — | — | 2026-04-26 |
| google-drive | skills/google-drive/SKILL.md | checklists/google-drive.md | pending | — | — | 2026-04-26 |
| google-slides | skills/google-slides/SKILL.md | checklists/google-slides.md | pending | — | — | 2026-04-26 |
| notion-integration | skills/notion-integration/SKILL.md | checklists/notion-integration.md | pending | — | — | 2026-04-26 |
| system-auditor | skills/system-auditor/SKILL.md | checklists/system-auditor.md | pending | — | — | 2026-04-26 |
| ux-architecture | skills/ux-architecture/SKILL.md | checklists/ux-architecture.md | pending | — | — | 2026-04-26 |
| video-generation | skills/video-generation/SKILL.md | checklists/video-generation.md | pending | — | — | 2026-04-26 |
| sports-gm | skills/sports-gm/SKILL.md | checklists/sports-gm.md | stable | 0.917 | 2026-05-15 | 2026-04-27 |
| portfolio-card | skills/portfolio-card/SKILL.md | checklists/portfolio-card.md | stable | 1.000 | 2026-05-27 | 2026-05-02 |
| app-marketing-product-content | agents/app-marketing/product-content/AGENT.md | agents/autoresearch/checklists/app-marketing-product-content.md | stable | 1.000 | 2026-05-25 | 2026-05-06 |

| opticfy-ops | skills/opticfy-ops/SKILL.md | agents/autoresearch/checklists/opticfy-ops.md | stable | 1.000 | 2026-05-18 | 2026-05-03 |
| opticfy-pipeline | skills/opticfy-pipeline/SKILL.md | checklists/opticfy-pipeline.md | stable | 0.944 | 2026-05-13 | 2026-05-03 |
| x-research | skills/x-research/SKILL.md | checklists/x-research.md | stable | 1.000 | 2026-05-20 | 2026-05-03 |
| niche-fitness | agents/niche-fitness/AGENT.md | checklists/niche-fitness.md | pending | — | — | 2026-05-03 |
| passive-income-strategist | agents/passive-income-strategist/AGENT.md | checklists/passive-income-strategist.md | pending | — | — | 2026-05-03 |
| skills-researcher | agents/skills-researcher/AGENT.md | checklists/skills-researcher.md | pending | — | — | 2026-05-03 |
| spanish-daily-lesson | cron:babd905a-1098-49dd-8700-772fef14f817 | checklists/spanish-daily-lesson.md | stable | 1.000 | 2026-06-19 | 2026-05-09 |
| workflow-skillify | skills/workflow-skillify/SKILL.md | checklists/workflow-skillify.md | stable | 1.000 | 2026-05-29 | 2026-05-11 |
| high-stakes-draft-eval | skills/high-stakes-draft-eval/SKILL.md | checklists/high-stakes-draft-eval.md | stable | 1.000 | 2026-06-01 | 2026-05-11 |
| mission-control-priority-auditor | agents/mission-control-priority-auditor/AGENT.md + scripts/mission_control_north_star_audit.py | checklists/mission-control-priority-auditor.md | stable | 1.000 | 2026-05-12 | 2026-05-12 |
| ai-ops-teardown | agents/ai-ops-teardown/AGENT.md + agents/ai-ops-teardown/weekly-prompt.md | checklists/ai-ops-teardown.md | pending | — | — | 2026-05-12 |
| agentguard-positioning | skills/agentguard-positioning/SKILL.md | checklists/agentguard-positioning.md | pending | — | — | 2026-05-13 |
| ai-governance-readiness | skills/ai-governance-readiness/SKILL.md | agents/autoresearch/checklists/ai-governance-readiness.md | pending | — | — | 2026-05-13 |
| reelfarm-intel | agents/reelfarm-intel/daily-prompt.md + agents/reelfarm-intel/weekly-prompt.md | agents/autoresearch/checklists/reelfarm-intel.md | stable | 1.000 | 2026-06-12 | 2026-05-31 |
| linkedin-corpus | skills/linkedin-corpus/SKILL.md | agents/autoresearch/checklists/linkedin-corpus.md | pending | — | — | 2026-05-31 |
| client-proof-capture | skills/client-proof-capture/SKILL.md | agents/autoresearch/checklists/client-proof-capture.md | pending | — | — | 2026-05-31 |
| ai-context-os | skills/ai-context-os/SKILL.md | agents/autoresearch/checklists/ai-context-os.md | stable | 1.000 | 2026-06-29 | 2026-05-31 |
| linkedin-corpus-agent | agents/linkedin-corpus/AGENT.md | agents/autoresearch/checklists/linkedin-corpus-agent.md | pending | — | — | 2026-05-31 |
| client-proof-engine | agents/client-proof-engine/AGENT.md | agents/autoresearch/checklists/client-proof-engine.md | stable | 1.000 | 2026-06-26 | 2026-05-31 |
| plan-review-pack | skills/plan-review-pack/SKILL.md | agents/autoresearch/checklists/plan-review-pack.md | pending | — | — | 2026-06-06 |
| ui-clone | skills/ui-clone/SKILL.md | agents/autoresearch/checklists/ui-clone.md | pending | — | — | 2026-06-07 |
| workflow-strategist | agents/workflow-strategist/AGENT.md | agents/autoresearch/checklists/workflow-strategist.md | stable | 1.000 | 2026-06-24 | 2026-06-07 |
| product-quality-pass | agents/product-quality-pass/AGENT.md | agents/autoresearch/checklists/product-quality-pass.md | stable | 1.000 | 2026-06-08 | 2026-06-07 |
| ai-seo | skills/ai-seo/SKILL.md | agents/autoresearch/checklists/ai-seo.md | stable | 1.000 | 2026-06-15 | 2026-06-14 |

## Status values
- `pending` — checklist written, not yet run
- `active` — has run at least once, loop in progress or complete
- `stable` — scored 90%+ on last run, loop complete, monitor monthly
- `paused` — skill changed significantly, checklist needs re-review before next run

---

## Graduated / Archived

| Slug | Final Score | Rounds | Improvements | Archived |
|------|-------------|--------|--------------|----------|
| jt-consulting-pipeline | — | — | Superseded by `opticfy-pipeline`; old path missing | 2026-05-12 |
