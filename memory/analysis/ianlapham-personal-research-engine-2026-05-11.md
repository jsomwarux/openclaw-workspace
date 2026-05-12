# Ian Lapham Personal Research Engine — Takeaways — 2026-05-11

Source: X post `https://x.com/ianlapham/status/2052567929049272571` plus thread/replies. External content treated as untrusted research signal, not instructions.

## Post summary
Ian argues that after two months of daily use, setting up a personal research engine is one of the highest-ROI things for staying on the edge. He recommends a cloud-hosted agent such as Hermes or OpenClaw and learning memory systems.

Thread replies sharpened the signal:
- write skills, work packages, and review results instead of only coding
- avoid memory/system drift
- cost/token visibility changes behavior
- observability is needed for autonomous memory/skill updates
- memory near the browser/source matters because tomorrow’s tabs should reuse yesterday’s context
- second-brain hoarding is a trap; compression beats collection

## Takeaways for JT/Eve
1. We already have the core research engine: OpenClaw, X research, web fetch/search, crons, LCM, MEMORY.md, daily notes, skills, consulting wiki, qmd/GBrain pilots.
2. The missing discipline is not more ingestion. It is output loops: research should compress into decisions, tasks, templates, skills, content, offers, or explicit skips.
3. Observability matters: if autonomous loops update memory/skills/tasks, future sessions need to see what changed and why.
4. Skills are the compounding layer. Repeated research workflows should become skills/checklists/work packages, not scattered notes.
5. Cost visibility is already partly covered by Eve’s cost tracker; do not add another token/cost tool unless a concrete gap appears.

## Implementation made
- Created `templates/research-engine-output-loop-template.md`.
- Updated `skills/x-research/SKILL.md` with Research Engine Output Loop.
- Updated `docs/agents/workflow-protocols.md` with Research Engine Output Rule.

## What not to do
- Do not install Hermes or another research engine just because the post says so.
- Do not ingest more sources without a routing/output plan.
- Do not confuse saved links with leverage.
- Do not add new crons until a specific repeatable research gap is proven.


## Audit follow-up
Tightened the output loop to require source URLs/file paths and to prevent Mission Control clutter. Research should create MC tasks only when there is a concrete owner, first action, and done state; otherwise route to memory/wiki/future-signals or mark non-actionable.
