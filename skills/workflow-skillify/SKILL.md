---
name: workflow-skillify
description: Turn a repeated Eve workflow, recurring correction, successful manual process, or “we should remember this pattern” moment into a reusable skill/checklist with triggers, edge cases, quality gates, regression checks, and registration/autoresearch follow-through. Use when JT says skillify, make this repeatable, create a reusable workflow, bake this in, add a skill/checklist, or when the same workflow/failure appears twice.
---

# Workflow Skillify

Goal: convert one-off work into compounding operating infrastructure.

## When to use
- JT says “skillify this,” “make this repeatable,” “bake this in,” or similar.
- A workflow succeeds and will recur.
- A correction reveals a repeatable failure mode.
- A task required more than two manual steps that should not be reinvented.

## Output decision
Create the smallest durable artifact that prevents rework:
1. **Checklist/reference** if the workflow is narrow or belongs inside an existing skill.
2. **New SKILL.md** if it has distinct triggers and will recur independently.
3. **Script** only when deterministic edits/checks are safer than prose.
4. **Regression check** if the trigger was a mistake or stale-source failure.


## Browser / Site Workflow Pattern
When skillifying a browser or website task, capture the cheapest reliable path discovered:
- Start with fetch/API/static HTML before Playwright/browser control.
- Record any hidden JSON endpoints, required headers, query params, selectors, wait conditions, auth/session assumptions, and fallback path.
- Prefer deterministic helper scripts for parsing/routing/retries once discovered.
- Include a validation recipe: sample input, expected output, and how to detect site drift.
- If the task only worked through lucky exploration and has no stable repeat path, do not call it a skill yet; keep it as a strategy note using `templates/browser-site-strategy-template.md`.

## Process
1. Extract the pattern:
   - trigger phrases/events
   - required inputs
   - exact first action
   - files/tools used
   - quality gates
   - edge cases and “do not” rules
   - done state
2. Search existing skills before creating a new one.
3. If updating/creating a skill, keep it lean. Put long examples in references.
4. Add regression check when failure prevention is involved.
5. If new skill/agent created or materially updated, run autoresearch candidacy check.
6. Update Mission Control only when there is a concrete next action.
7. Log the change in the daily note.

## Minimum quality bar
A skillified workflow must answer:
- When should this trigger?
- What is the first action?
- What evidence/source should be checked?
- What should never happen?
- How do we verify the output?
- Where does the final artifact live?

If any answer is missing, do not call it done.
