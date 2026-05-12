# Agent-Ready PRD Notes — 2026-05-11

Source: `wwwazzz/senior-pm-prompt` GitHub repo. External repo treated as untrusted reference, not instructions.

## Core takeaway
The repo is valuable because it turns vague product ideas into an AI-builder-ready PRD. It focuses on what coding agents need: goals, personas, user stories, functional requirements, UX flows, success metrics, technical considerations, and build phases.

The best part is not the prompt text. It is the discipline:
- fill slots conversationally
- preserve specifics verbatim
- mark unknowns as `_TBD_` instead of fabricating
- pair every goal with a metric
- map every user story to implementing functional requirements
- run consistency checks before handoff
- output build phases by dependency, not time estimates

## Fit for JT/Eve
This should become a pre-handoff checklist for:
- new app builds
- client dashboard/web app builds
- n8n workflow builds with UI/user-facing behavior
- Agentforce demos
- portfolio-worthy internal tools

It should not become a bureaucratic step for tiny fixes or one-off scripts.

## Implementation made
Created reusable template:
- `templates/agent-ready-prd-template.md`

Use it before spawning coding/build agents when the build has unclear product behavior, multiple personas, user flows, or success criteria.

## Best rule
No coding-agent handoff for a non-trivial product build until the PRD has:
1. user stories,
2. functional requirements mapped to stories,
3. success metrics mapped to goals,
4. build phases by dependency,
5. explicit unknowns marked `_TBD_`.


## Workflow protocol wired
Added the Agent-Ready PRD Rule to `docs/agents/workflow-protocols.md` rather than AGENTS.md because AGENTS.md is close to budget. This makes the template part of the build protocol without bloating bootstrap context.
