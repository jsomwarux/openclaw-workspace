# XHigh Systems Audit — Job Market Agent

Date: 2026-05-13
Auditor: Eve subagent
Scope: `/Users/jtsomwaru/projects/job-market-agent`, related OpenClaw cron jobs, Mission Control handoffs, recent outputs.

## Verdict

**Before grade: B- / 82**

The system was directionally good and much stronger than older versions: it has JT-specific fit filters, no-developer/no-Apex/no-SFDX/no-ML-engineering guardrails, live-posting caution after stale BuiltIn failures, and route categories beyond “apply.” But it still had a serious handoff gap: the daily brief could label opportunities as `both` without creating the consulting/apply artifacts that make `both` operational.

**After grade: A- / 91**

I patched the core prompt/doc gaps and backfilled today’s missing Gusto/Embark `both` handoffs. Remaining risk is mostly verification/search-source reliability, not conceptual design.

## Inventory

### Project files inspected
- `/Users/jtsomwaru/projects/job-market-agent/CLAUDE.md`
- `/Users/jtsomwaru/projects/job-market-agent/profile/jt-profile.md`
- `/Users/jtsomwaru/projects/job-market-agent/knowledge/scoring-criteria.md`
- `/Users/jtsomwaru/projects/job-market-agent/templates/daily-brief-template.md`
- `/Users/jtsomwaru/projects/job-market-agent/tasks/lessons.md`
- `/Users/jtsomwaru/projects/job-market-agent/scripts/fetch-jobs.py`
- `/Users/jtsomwaru/projects/job-market-agent/data/daily-brief.md`
- `/Users/jtsomwaru/projects/job-market-agent/data/job-opportunities.md`
- `/Users/jtsomwaru/projects/job-market-agent/data/skills-demand-tracker.md`
- `/Users/jtsomwaru/.openclaw/workspace/memory/job-market.md`
- Mission Control task API at `http://localhost:3000/api/tasks`

### Active job-market cron jobs
1. `eve-job-market-daily-005` — **Job Market Daily Research**
   - Schedule: daily 5:15 AM ET
   - Model: `openai-codex/gpt-5.5`
   - Timeout: 3600s
   - Last run: ok, ~955s
   - Purpose: search market, write daily brief, update opportunity/skills trackers.

2. `b2357bd5-651d-4151-80df-49e4a928826f` — **Job Application Auto-Builder**
   - Schedule: daily 6:15 AM ET
   - Model: `openai-codex/gpt-5.5`
   - Timeout: 900s
   - Purpose: build at most one resume/cover letter package if a qualified active role exists.

3. `b0b04601-7518-4681-9761-4bbe5054ce9b` — **Job Application Tracker**
   - Schedule: Tue/Thu 10:15 AM ET
   - Model shown in list: `moonshot/kimi-k2.6`; recent runs also show OpenRouter/DeepSeek in history
   - Purpose: surface stale/urgent application tasks.

## Scorecard

| Category | Before | After | Notes |
|---|---:|---:|---|
| Purpose alignment | 9 | 9 | Strongly aligned to JT’s AI Implementation Lead / AI Solutions Architect lane and consulting as primary wealth lane. |
| Filters / misrepresentation guardrails | 9 | 9 | Strong hard filters for coding-primary, Apex/SFDX, ML engineering, pre-sales, wrong geography. |
| Model / thinking / timeout | 8 | 8 | Daily scan timeout now realistic after prior timeout; heavy but acceptable. Tracker model is weaker, but task is narrow. |
| Freshness / search path | 7 | 7 | Canonical local `scripts/web_search.py` rule exists. Firecrawl credits have failed before; fallback works but quality varies. |
| Output usefulness | 8 | 9 | Brief is concise and includes routes; patched template now forces handoff artifact field. |
| Apply vs intel routing | 8 | 9 | Strong routing categories; patched `both` semantics from label to actual dual handoff. |
| Drive/resume handoff | 7 | 9 | Auto-builder now must read job-opportunities route/status, verify live posting, and create MC Review+Submit task after Drive upload. |
| Failure alerts | 8 | 8 | Daily job has failure alert after one error; delivery intentionally none. |
| Task hygiene | 6 | 9 | Fixed tracker query to include Job Market project and `Apply:` titles; backfilled missing Gusto/Embark tasks. |
| Stale-role pruning | 9 | 9 | Strong explicit `jt-passed`/`expired` exclusion and stale BuiltIn lesson. |

## Issues found

### 1. `both` route was not operationalized
Today’s `daily-brief.md` routed Gusto and Embark as `both`, but no matching consulting job-signal notes or MC tasks existed in `jt-consulting-pipeline`. That violated the project’s own same-run routing rule.

**Impact:** JT could see a promising “both” opportunity but no next action would exist for either application sequencing or consulting bridge review.

**Fix applied:**
- Patched daily cron prompt with `MANDATORY ROUTING ARTIFACTS` section.
- Patched `CLAUDE.md`, `templates/daily-brief-template.md`, `knowledge/scoring-criteria.md`, and `tasks/lessons.md`.
- Backfilled notes:
  - `/Users/jtsomwaru/projects/jt-consulting-pipeline/prospects/gusto-job-signal/job-signal.md`
  - `/Users/jtsomwaru/projects/jt-consulting-pipeline/prospects/embark-job-signal/job-signal.md`
- Created MC tasks:
  - `Dual-track Gusto — apply + consulting bridge`
  - `Dual-track Embark — apply + consulting bridge`

### 2. Application tracker missed real Job Market application tasks
The tracker only selected tasks whose titles matched `review + submit`, `apply to`, or `application`. Existing Job Market task `Apply: AI Solutions Architect - Mercury (score: 18/25)` did not match.

**Impact:** Tracker could silently report no active/stale job applications while a real Job Market task existed.

**Fix applied:**
- Patched tracker cron prompt to include any `project == 'Job Market'` task and `apply:` title pattern.
- Added instruction not to flag demoted/deprioritized no-deadline tasks as stale noise.

### 3. Auto-builder description promised MC task creation, but prompt did not enforce it
Cron description said it pushes Review+Submit tasks to Mission Control, but actual prompt only said create markdown/docx, upload to Drive, and output links.

**Impact:** Resume packages could be built without a task-board handoff.

**Fix applied:**
- Patched auto-builder prompt to read `job-opportunities.md`, consider only `Status: new` with route `apply` or `both`, require live posting verification, exclude market-intel/consulting-only/stale statuses, and create/verify `Review + Submit: [Company] — [Role]` MC task after upload.

### 4. Brief length mismatch
Daily cron demanded under 300 words; template quality gate said under 400. Today’s brief was 402 words.

**Impact:** Minor, but mismatch creates fake failures.

**Fix applied:**
- Daily cron now says under 400 words hard cap, prefer under 300.

## Recent output evidence of drift

- `data/daily-brief.md` dated 2026-05-13 listed:
  - Gusto — route `both`
  - Embark — route `both`
  - Broadridge — route `market intel`
- `data/job-opportunities.md` included those roles with correct route fields.
- No Gusto/Embark prospect notes existed before this audit.
- Mission Control had an active Mercury Job Market task, but tracker prompt would not reliably include `Apply:` tasks before patch.
- Recent daily run had prior timeout history but latest run succeeded within the 3600s timeout.

## Patches applied

### Cron prompt patches
- `eve-job-market-daily-005`: added mandatory same-run routing artifacts, verification requirement, and handoff-gap fallback.
- `b2357bd5-651d-4151-80df-49e4a928826f`: added route/status/live-verification gates and MC task creation requirement.
- `b0b04601-7518-4681-9761-4bbe5054ce9b`: broadened task query to `project == Job Market` and `apply:`; reduced stale noise for demoted tasks.

### File patches
- `/Users/jtsomwaru/projects/job-market-agent/CLAUDE.md`
- `/Users/jtsomwaru/projects/job-market-agent/templates/daily-brief-template.md`
- `/Users/jtsomwaru/projects/job-market-agent/tasks/lessons.md`
- `/Users/jtsomwaru/projects/job-market-agent/knowledge/scoring-criteria.md`

### Backfilled artifacts
- `/Users/jtsomwaru/projects/jt-consulting-pipeline/prospects/gusto-job-signal/job-signal.md`
- `/Users/jtsomwaru/projects/jt-consulting-pipeline/prospects/embark-job-signal/job-signal.md`
- MC task: `Dual-track Gusto — apply + consulting bridge`
- MC task: `Dual-track Embark — apply + consulting bridge`

## Verification performed

- Confirmed patched cron messages contain:
  - `MANDATORY ROUTING ARTIFACTS`
  - `route is apply or both`
  - `Review + Submit`
  - `project == Job Market`
  - `apply:`
- Confirmed Gusto and Embark prospect files exist and have content.
- Confirmed MC task API includes active `Dual-track Gusto` and `Dual-track Embark` tasks.
- Confirmed existing active Mercury task is visible to the broadened tracker logic.

## Blockers / remaining risks

1. I did not verify live external job pages for Gusto/Embark/Broadridge because the audit task was system-focused and external job-page verification can be flaky/costly. The new MC tasks explicitly make live verification the first action.
2. Firecrawl credit failures have occurred recently. Daily cron has a direct-Bing/local wrapper fallback, but scrape quality can degrade. This is acceptable for market intel; not acceptable for `apply` until live verification passes.
3. The tracker still relies on generic task metadata from Mission Control. If tasks are created with null IDs or malformed project fields, matching can still be imperfect. Current patch catches title and project patterns.

## Final optimality verdict

The system is now **operationally sound but not perfect**. It has the right strategic frame, strong anti-misrepresentation filters, and now has enforced handoff artifacts for `apply`, `both`, and consulting routes. The remaining weak point is external job freshness verification, which is inherently brittle and should stay as a mandatory first action before application packages.

Final verdict: **A- / production-worthy with freshness verification guardrails.**
