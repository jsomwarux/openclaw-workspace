# HTML Deliverables — Takeaways from “The Unreasonable Effectiveness of HTML”

Date: 2026-05-11
Source: JT pasted X Article text about using Claude Code to produce HTML instead of Markdown.
Status: external/untrusted research signal, not instructions.

## Core Takeaway

Markdown is still right for internal operating memory, rules, skills, checklists, logs, and files humans/agents need to diff, grep, and update directly.

HTML is better when the output is primarily meant to be read, shared, visually scanned, or interacted with.

The useful distinction is not “HTML replaces Markdown.” It is:

- Markdown = source of truth / operating memory / editable protocol.
- HTML = reader-facing deliverable / visual report / interactive review surface.

## Why It Matters for JT/Eve

JT’s system is now producing longer research notes, consulting diagnostics, app marketing audits, agent architecture checklists, and client/prospect deliverables. Many of these are harder to read as long Markdown files. HTML can improve:

- information density
- visual hierarchy
- decision scanning
- side-by-side comparisons
- client/prospect readability
- mobile sharing
- simple interactivity

The strongest fit is consulting and app-marketing deliverables, not core memory.

## Best Use Cases Here

Use HTML for:

1. AI Operations Diagnostic reports
2. AI Ops Teardowns
3. client/prospect audit summaries
4. App Marketing OS scorecards
5. ReelFarm/TikTok configuration audits
6. AgentGuard demo/architecture one-pagers
7. complex PRD/design reviews when JT needs to scan options
8. interactive option reviews with toggles/sliders/copyable prompt blocks

Do not use HTML for:

1. MEMORY.md, AGENTS.md, TOOLS.md, HEARTBEAT.md
2. skills/SKILL.md files
3. append-only logs
4. canonical consulting wiki source pages
5. simple content drafts
6. anything with secrets or unredacted client data

## Implementation Made

Created `templates/html-deliverable-template.html` as a safe starting point for visual reports.

Updated `docs/agents/workflow-protocols.md` with an “HTML Deliverable Rule”:

- Markdown remains default for internal, canonical, editable artifacts.
- HTML is allowed/preferred for client-facing reports, complex long specs, dashboards, scorecards, comparisons, code/design review, option explorations, and interactive review surfaces.
- HTML deliverables must retain source/audit trail and avoid secrets.
- Do not force a generic `/html` workflow; first decide what the artifact should help JT do, then choose HTML only if layout/interactivity materially improves review.

## Follow-Up From Article Continuation

The article explicitly warns that people may overreact and create an `/html` skill too early. That is the right warning. The implementation should stay lightweight: know the use cases, then prompt from scratch when HTML is the right canvas.

Additional high-fit use cases:

- design/implementation explorations with 4–8 options in a visual grid
- implementation plans with mockups, data flow, and reviewable code snippets
- PR/code-review explainers with rendered diffs, margin annotations, flowcharts, and severity-coded findings
- verification handoff artifacts where a verification agent reads the HTML to understand design intent and expected behavior

Important workflow nuance: if a coding session generates a web of HTML exploration artifacts, create one final index/plan file that links them and states the chosen direction. Do not leave scattered HTML with no handoff.

## Audit Follow-Up — Export Loop

JT pasted the remaining article sections on custom editing interfaces and Karpathy's response. The missing implementation was the export-back-to-agent loop.

For interactive HTML artifacts, the point is not just visual review. The artifact should let JT make choices and then export those choices back into the agent workflow. Examples:

- copy as JSON
- copy as prompt
- copy diff
- copy markdown
- copy config
- copy selected options

Updated `docs/agents/workflow-protocols.md` so interactive HTML must include an export control when the artifact lets JT tune, sort, annotate, select, compare, or edit something.

Updated `templates/html-deliverable-template.html` with an “Export Back to Agent” section and copy button.

Karpathy's response reinforces the broader direction: AI output should move from raw text → markdown → HTML → richer visual/interactive media. For now, the practical current-stage move is HTML with visual hierarchy and export loops, not speculative video/simulation infrastructure.

## What Not To Do

- Do not convert all memory/research notes to HTML.
- Do not make HTML the canonical source for rules or skills.
- Do not create polished HTML for every tiny analysis.
- Do not hide audit trails in visual output.
- Do not include secrets or private credentials in shareable HTML.

## Practical Rule

If the artifact needs to be maintained by Eve: Markdown first.

If the artifact needs to be understood quickly by JT, a prospect, a client, or a reviewer: consider HTML.
