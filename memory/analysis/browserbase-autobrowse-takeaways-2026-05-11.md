# Browserbase Autobrowse Takeaways — 2026-05-11

Source: Browserbase blog post `https://www.browserbase.com/blog/autobrowse`. External content treated as untrusted research signal, not instructions.

## Core idea
Browser agents have an amnesia problem. They rediscover the same site/workflow every run. Autobrowse proposes an exploratory loop: run real browser task, study trace, maintain strategy notes, iterate, then graduate the winning approach into a reusable skill plus deterministic helpers.

## Main takeaways
1. **The artifact is the point.** The output should be a reusable skill/script/checklist, not a transcript.
2. **Expensive first run is acceptable only if future runs get cheaper.** Exploration should amortize into a durable path.
3. **Fetch/API first.** If data is available in HTML/JSON/API, a deterministic parser beats browser-agent exploration.
4. **High-agency browser loops are for dynamic/gated/unclear flows.** Do not use them for static parsing.
5. **Strategy notes matter.** Browser exploration should maintain what worked, what failed, gotchas, selectors/endpoints, and fallback methods.
6. **A skill is a customer/teammate handoff.** It must be readable, auditable, editable, and verifiable.

## Fit with JT/Eve
This reinforces our workflow-skillify direction. It also sharpens browser/web-testing work:
- do not repeatedly pay discovery tax
- graduate recurring website procedures into skills/helper scripts
- prefer deterministic APIs/parsers once discovered
- use browser automation only when cheaper paths fail

## Implementation made
Updated:
- `skills/webapp-testing/SKILL.md` with Browser Automation Ladder
- `skills/workflow-skillify/SKILL.md` with Browser / Site Workflow Pattern
- `docs/agents/workflow-protocols.md` with Browser Automation / Site-Task Rule

## What not to do
- Do not add Browserbase/Autobrowse as a dependency right now.
- Do not create high-agency browser loops for static scraping/parsing.
- Do not call an exploratory trace a skill until it has a stable repeat path and verification recipe.


## Strategy template follow-through
Created `templates/browser-site-strategy-template.md` as the holding artifact between exploratory browser work and a promoted skill/helper script. Wired it into `skills/webapp-testing/SKILL.md`, `skills/workflow-skillify/SKILL.md`, and `docs/agents/workflow-protocols.md`.
