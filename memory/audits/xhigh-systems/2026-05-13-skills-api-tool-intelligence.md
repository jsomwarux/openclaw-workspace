# XHigh Systems Audit — Skills / API / Tool Intelligence

Date: 2026-05-13
Auditor: subagent `xhigh-audit-skills-api-tool-intelligence`
Scope: `agents/skills-researcher`, Skills & API Researcher daily/weekly crons, Mission Control Skills tasks, autoresearch enrollment, skills registry, `memory/ai-tools.md`, tool/plugin safety rules.

## Executive Score

**Before grade:** B+

Why: the intelligence loop is real and active. The daily and weekly researcher crons exist, run isolated, use failure alerts, avoid runner delivery noise on daily scans, send weekly synthesis to Telegram, and recent runs show correct behavior: 6 X queries, web checks, KB-only routing for low-value findings, no duplicate MC tasks when existing tasks already cover the action, and Telegram only for quality-gated 🔴/🟠 items. Security posture is mostly sound: plugin installs/config changes are already approval-gated in AGENTS/SECURITY rules and the daily cron payload explicitly blocks configuring/installing the risky Brave plugin path.

It was not A-level because:
- `agents/skills-researcher/AGENT.md` had stale internal contradictions: daily protocol said 8 X queries while the actual query set/cron uses 6; weekly protocol said 6 deep queries while the actual weekly set has 4.
- The static installed-skill list was stale and could cause missed update checks.
- The agent registry still described “8 daily queries” and “recommends installations,” which was noisier/riskier than the actual approval-gated behavior.
- Mission Control `Skills` backlog has 58 open tasks, many old tool/release/install/evaluate items. New task quality is strong, but old backlog noise can hide real opportunities.

**After grade:** A-

The main safety/consistency gaps are patched. Remaining reason it is not A+: the old Skills backlog needs a deliberate prune, and I did not bulk-close stale tasks without verifying each one.

## Inventory Findings

### Core researcher files
- `agents/skills-researcher/AGENT.md` — comprehensive X-first + web source protocol, severity gates, MC task quality gates, security rules.
- `agents/skills-researcher/state.json` — valid JSON, tracks OpenClaw release, npm/OpenRouter/Clawhub/Cowork/Nordeim state.
- `agents/skills-researcher/weekly-log.md` — current W20 log includes May 11–13 scans and dedupe/no-task decisions.
- `agents/skills-researcher/scan-cost-log.md` — active history through 2026-05-13.
- `memory/ai-tools.md` — heartbeat AI tooling signal store, current through 2026-05-13.

### Crons
- `4c437ff5-02cd-4288-8e6e-6e6fc07203ce` — **Skills & API Researcher — Daily Scan**
  - Schedule: Mon–Sat 11:30 AM America/New_York
  - Session: isolated
  - Payload model: `openai-codex/gpt-5.5`
  - Timeout: 2400s
  - Delivery: none; direct Telegram only when the agent sends 🔴/🟠 findings
  - Failure alert: enabled after 2 errors, Telegram to JT, 4h cooldown, skipped runs excluded
  - Recent run 2026-05-13: ok, no 🔴/🟠, 0 MC tasks, 0 Telegram, KB’d background findings, updated state/logs.

- `05024e45-57fc-4e7c-a236-660e6eb5393f` — **Skills & API Researcher — Weekly Synthesis**
  - Schedule: Saturdays 7:00 AM America/New_York
  - Session: isolated
  - Payload model: `openai-codex/gpt-5.5`
  - Timeout: 1800s
  - Delivery: Telegram announce, best effort
  - Failure alert: enabled after 1 error, Telegram to JT, 24h cooldown
  - Recent runs delivered successfully.

### Autoresearch / registry
- `agents/autoresearch/targets.md` includes `skills-researcher` as a pending target with checklist `agents/autoresearch/checklists/skills-researcher.md`.
- Checklist exists and is scoreable: usefulness before surfacing, hype vs impact, cost/setup/security, skip/add/watch, independent evaluation before asking JT, task only for worthwhile tools.
- `mission-control/data/agents.json` includes `skills-researcher`; it was stale before patch.

### Mission Control Skills tasks
- Before creating blocker: 58 open `project=Skills` tasks.
- Newer researcher-created tasks are generally actionable: sampled current tasks include `First action`, `Why` / `Why now`, and `Done state` / `Expected outcome`.
- Backlog is still too noisy for A+. Old tool/release tasks require safe triage rather than blind closure.

## Patches Applied

1. `agents/skills-researcher/AGENT.md`
   - Fixed daily protocol from “8 daily queries” to 6, matching the actual query set and cron payload.
   - Fixed weekly protocol from “6 weekly X queries” to 4, matching the actual weekly deep-scan set.
   - Replaced stale installed-skill list with a dynamic inventory rule: inspect `skills/*/SKILL.md` and session available-skills registry at run time.
   - Clarified 🔴/🟠 routing: content/MC/Telegram actions only after quality/noise gate passes.
   - Fixed duplicated `c.` step to `d.` for Telegram.
   - Updated model/timeout docs to describe current cron payload values without implying model config should be edited from the doc.
   - Strengthened security rule: never install/activate skill/plugin, run plugin-install commands, edit auth/model config, or enable new external integrations without JT approval.

2. `mission-control/data/agents.json`
   - Updated `skills-researcher` domain from “8 daily queries” to 6.
   - Reframed “recommends installations” as approval-gated evaluations.
   - Clarified that only quality-gated 🔴/🟠 findings go to Telegram/MC and no plugin/config changes happen without JT approval.

3. Mission Control task created
   - `Skills/API intelligence: prune stale tool backlog`
   - ID: `j579v94mtzbafr767qgyt9ey0n86q762`
   - Priority: medium, Project: Skills, sortOrder: 55
   - First action: review 58 open Skills tasks oldest-first; close superseded release/install items, merge duplicates, keep only tasks with current first action/why/done state.
   - Done state: Skills project ≤15 open tasks; remaining tasks actionable and approval-gated where needed.

## Validation

- Bootstrap budget preflight:
  - `AGENTS.md`: 27,013 bytes (<28,000)
  - `MEMORY.md`: 19,258 bytes (<20,000, near ceiling)
  - `TOOLS.md`: 13,947 bytes (<16,000)
  - `HEARTBEAT.md`: 15,578 bytes (<16,000, near ceiling)
- `agents/skills-researcher/state.json` validates with `python3 -m json.tool`.
- `mission-control/data/agents.json` validates with `python3 -m json.tool`.
- Cron inventory confirmed exactly one daily and one weekly Skills & API Researcher job, both enabled and with failure alerts.
- Recent daily runs show correct no-noise behavior: no Telegram when no 🔴/🟠 passes gate; KB/state/log updates still happen.
- AGENT.md consistency grep/checks passed:
  - No stale “all 8 daily”/`x_queries: 8` remains.
  - Daily 6-query language present.
  - Weekly 4-query language present.
  - Approval-gated install/plugin/config rule present.
  - Dynamic skill inventory rule present.
- Mission Control API accepted the backlog-prune blocker and open Skills task count moved from 58 to 59 by design.

## Gate Scores

| Gate | Before | After | Notes |
|---|---:|---:|---|
| Safe research sources | A- | A | X-first + vetted web/API sources; canonical web wrapper rule avoids risky Brave plugin path. |
| Alert severity filtering | A- | A- | Recent runs prove no-message behavior for low-value findings; older backlog still noisy. |
| No plugin/config risk | A- | A | Security language tightened in researcher doc + registry. |
| MC task quality | B | A- | New tasks are actionable; old backlog remains the main weakness. |
| Autoresearch candidacy | A- | A- | Enrolled, checklist exists; still pending execution. |
| Skill registry consistency | B | A- | Registry patched; future dynamic inventory reduces drift. |
| Duplicate task prevention | A- | A- | Recent run skipped duplicates; backlog still needs prune. |
| Weekly synthesis | A- | A- | Runs and delivers; protocol query-count drift fixed. |
| Memory/tool signal updates | A- | A- | `memory/ai-tools.md`, KB, logs active. |
| Failure alerts | A | A | Daily and weekly have Telegram failure alerts. |

## Remaining Blockers

1. **Open Skills backlog is too large.**
   - 59 open Skills tasks after adding the blocker.
   - This is the only meaningful non-A+ blocker.
   - Created MC task: `Skills/API intelligence: prune stale tool backlog`.

2. **Autoresearch target still pending.**
   - `skills-researcher` is enrolled but not yet stable.
   - Let the normal autoresearch sweep handle it; no urgent intervention needed.

## Recommendation

Keep the system running. Do not add more discovery sources until the Skills backlog is pruned. The discovery engine is good enough; the bottleneck is now task hygiene.
