# Workflow Protocols — Detailed Reference
> Extracted from AGENTS.md to keep it under bootstrap budget.
> AGENTS.md has pointer lines. Sub-agents: read this file when working on builds/code/n8n/Agentforce.

## Staff Engineer Bar (code quality gate)
Before presenting any code output, implementation, or architecture decision: ask "Would a staff engineer approve this?"
Checklist:
- Is there a simpler way to accomplish the same outcome?
- Are error states handled (not just the happy path)?
- Will this break when inputs are unexpected or empty?
- Is this hardcoded where it should be dynamic?
- Is this duplicating something that already exists in the codebase?
If any answer is unfavorable: fix before delivering. Do not present first drafts as final unless they pass this bar.

## Pre-Execution Plan File Rule
For any coding task or multi-step build: before writing a single line of code, create a `tasks/todo.md` in the project root with a checklist of steps. Format:
```
## Plan — [task name] — [date]
- [ ] Step 1: [specific action]
- [ ] Step 2: [specific action]
```
Check off steps as they complete (`- [x]`). If something breaks mid-task: update the plan, STOP, re-plan.
Exception: one-liner fixes or single-file edits don't need a plan file.

## Running Implementation Notes Rule
For any coding-agent, n8n-agent, Agentforce, app/site build, or non-trivial implementation sub-agent task, require a live `tasks/implementation-notes.html` file alongside `tasks/todo.md`.

Purpose: capture anything JT or the next agent should know about how the implementation diverged from or interpreted the spec. This is the missing audit trail between prompt, code, and final summary.

Canonical prompt block:
```
Implement <SPEC>. As you work, maintain a running `tasks/implementation-notes.html` file that captures anything I should know about how the implementation diverges from or interprets the spec, including:

- Design decisions: choices you made where the spec was ambiguous
- Deviations: places where you intentionally departed from the spec, and why
- Tradeoffs: alternatives you considered and why you picked what you did
- Open questions: anything you'd want me to confirm or revise

Update this file while working; do not reconstruct it only at the end. If there were no meaningful decisions, deviations, tradeoffs, or open questions, write `No material spec interpretation notes` explicitly.
```

HTML file requirements:
- Include a short summary box at top: status, date, task, and top 3 notes.
- Use sections for Design Decisions, Deviations, Tradeoffs, Open Questions, Files Changed, and Verification.
- Keep it readable in a browser: simple inline CSS is fine; no build step or external assets.
- The notes file is for implementation interpretation, not a duplicate changelog. Avoid dumping every file edit unless it matters to the spec.

Final handoff must cite `tasks/implementation-notes.html`, summarize the top 3 notes, and mention any open questions. If the file is missing, the implementation handoff is incomplete.


## Agent-Ready PRD Rule
Before handing off a **non-trivial product/client/app build** to a coding agent, n8n agent, Agentforce agent, or implementation sub-agent, create or fill an agent-ready PRD using `templates/agent-ready-prd-template.md`.

Use this rule when the build has any of:
- multiple screens or user flows
- multiple user roles/personas
- external integrations or data model decisions
- client-facing output
- portfolio/public claims
- unclear success criteria

Skip for:
- one-line fixes
- bugfixes with an obvious failing test/log
- pure config edits
- small copy/content changes
- narrow scripts with a single input/output

Minimum handoff quality:
- user stories exist and each maps to at least one functional requirement
- business/user goals have success metrics or explicit `_TBD_`
- build phases are dependency-ordered, not fake time estimates
- data/integration/privacy constraints are named
- definition of done and verification gate are explicit
- unknowns are marked `_TBD_`, not invented

The PRD can live in the project root as `tasks/prd.md`, in the client folder, or in `memory/drafts/` for early concepts. Link it from `tasks/todo.md` before coding begins.


## Code-Agent Failure Prevention Rules
Use this before and during coding-agent, n8n-agent, Agentforce, or implementation sub-agent work. These are adapted from the Mnilax/Karpathy Claude Code rules and JT/Eve failure history.

1. **Think before coding:** State assumptions explicitly. If uncertain, ask or surface tradeoffs rather than guessing.
2. **Simplicity first:** Minimum code that solves the problem. No speculative features or abstractions for one-off code.
3. **Surgical changes:** Touch only files required for the task. Clean up only your own mess unless adjacent cleanup blocks correctness.
4. **Goal-driven execution:** Define the exact done state before implementation: command passes, screenshot matches, endpoint returns sample output, cron delivers, or live URL works.
5. **Use models only for judgment calls:** Use LLMs for classification, drafting, summarization, extraction from unstructured text, tradeoff analysis, and ambiguity resolution. Do **not** use LLMs for deterministic routing, retries, status-code handling, schema transforms, date math, file existence checks, or anything plain code can decide reliably.
6. **Token budgets are real:** If a task/session starts looping, repeats the same error, or loses track of prior attempts, stop, summarize state, and start a fresh focused pass. Surfacing context/budget exhaustion beats silently pushing through.
7. **Surface conflicts, do not average them:** If two codebase patterns contradict, pick the newer/more tested/local pattern, explain why, and flag the other for cleanup. Do not blend incompatible styles.
8. **Read before write:** Before adding code, inspect the file exports, immediate caller, and obvious shared utilities. Never generate replacements from memory when the file exists.
9. **Tests verify intent, not just behavior:** Tests/checks should fail if the user-requested business logic is wrong. Passing shallow tests is not proof.
10. **Checkpoint after significant steps:** After plan → scaffold → core → polish → deploy, summarize what changed, what is verified, and what remains. Update `tasks/todo.md`.
11. **Conventions beat novelty:** Match the codebase's existing patterns even if another style seems better. If the convention is harmful, surface it; do not fork silently.
12. **Fail loud:** If data is stale, missing, inaccessible, skipped, or confidence is low, stop and surface the blocker. “Done” is false if anything material was skipped silently.

**Prototype nuance:** For exploratory prototypes, Rule 2 should mean “smallest useful experiment,” not “production-minimal architecture.” Speculative scaffolding is allowed only when the task is explicitly exploratory and clearly labeled as disposable.




## Research Engine Output Rule
For substantive research passes, X/thread analyses, API/tool reviews, or market scans, end with compression into an output. Use `templates/research-engine-output-loop-template.md` when the research is likely to recur or affect strategy.
1. Capture the top source-backed observations.
2. Compress to one pattern, decision, warning, or opportunity.
3. Route it to the right durable surface: memory, consulting wiki, skill/template, Mission Control, content, prospect note, or explicit skip.
4. Prefer action/reusable assets over archives. If research creates no decision, task, draft, or reusable asset, label it non-actionable and do not preserve noise.
5. Record observability: source URLs/file paths, files updated, tasks created/closed, owner, and trigger/review date.
6. Create Mission Control tasks only when there is a concrete owner, first action, and done state. Otherwise route ideas to memory/wiki/future-signals.

## HTML Deliverable Rule
Markdown remains the default for internal notes, memory, skills, checklists, logs, and files JT may edit directly. Use HTML when the output is primarily for reading, sharing, visual scanning, side-by-side comparison, code/design review, or interactive exploration.

Do **not** force a generic `/html` workflow. First decide what the artifact should help JT do: compare options, understand a diff, review a plan, inspect a workflow, share a report, or tune variables. Then choose HTML only if layout/interactivity materially improves review.

Use HTML for:
- client-facing or prospect-facing reports, audits, proposals, and teardown deliverables
- complex specs or plans over ~100 lines that need navigation, visual grouping, tables, diagrams, or decision cards
- exploration packs: multiple design/implementation options laid out side-by-side with tradeoffs
- PR/code-review explainers: rendered diffs, annotations, flowcharts, module maps, severity-coded findings
- dashboards/scorecards/side-by-side comparisons where layout, color, or density improves comprehension
- interactive playgrounds where sliders, toggles, filters, or copyable prompt/config blocks help JT review options
- visual workflow/architecture explanations where markdown would degrade into ASCII diagrams

Do not use HTML for:
- canonical memory files, AGENTS/TOOLS/HEARTBEAT, skills, runbooks, append-only logs, or anything meant to be grep-friendly/editable
- tiny notes or simple drafts
- outputs containing secrets, tokens, private credentials, or unredacted sensitive client data
- places where a maintained markdown source of truth is required

For multi-file HTML explorations, keep a clear final handoff file such as `implementation-plan.html` or `review-index.html` that links the exploration artifacts. Verification agents/subagents should read the relevant HTML artifacts when they define expected behavior or design intent.

Interactive HTML must close the loop back to the agent. If the artifact lets JT tune, sort, annotate, select, compare, or edit something, include an export control such as `copy as JSON`, `copy as prompt`, `copy diff`, `copy markdown`, or `copy config`. The exported text should be paste-ready for a follow-up agent/coding session.

If using HTML, keep a source/audit trail: source URLs/file paths, generation date, owner, and any companion markdown/source file if the HTML is rendered from structured content. For non-trivial HTML deliverables, `templates/html-deliverable-template.html` is optional scaffolding, not a mandatory format.

## Goal-Mode / Long-Running Agent Rule
Use goal-style execution only for one durable objective with a verifiable stop condition. This applies to Codex `/goal` if available, OpenClaw TaskFlow, or any long-running autonomous/background agent loop.

Do not use goal mode for vague research, broad backlog cleanup, ordinary content drafting, outreach writing, crypto/financial decisions, or tasks without objective evidence of completion.

Before starting, fill or mentally apply `templates/goal-mode-spec-template.md`:
- one objective
- allowed/forbidden scope
- required files/docs to read first
- done state/stopping condition
- validation commands/evidence
- checkpoint cadence
- budget/stop rules
- completion audit

If Codex `/goal` becomes available, treat it as experimental and require explicit JT approval before enabling/installing or changing OpenClaw config. Prefer current OpenClaw TaskFlow/cron/subagent patterns unless `/goal` clearly beats them for one code-heavy, long-running, verifiable objective.

## Agent-Native CLI / Tool Design Rule
When a workflow repeats across APIs, browser steps, local files, or crons, prefer an agent-native CLI/helper before adding raw tool sprawl.
1. Check existing OpenClaw tools, skills, scripts, and CLIs first; prefer improving/wrapping what exists over creating another tool.
2. Identify the service's “secret identity” for JT: what job does it actually help an agent do?
3. Design the magic compound command first, not endpoint-by-endpoint wrappers.
4. Use local SQLite/cache mirrors when repeated cross-record queries, history, diff, drift, or joins matter.
5. Include agent-readable output modes such as `--json`, `--compact`, and `--agent`/`--llm` when useful.
6. Keep deterministic transforms in code; use LLMs only for judgment, summarization, or unstructured extraction.
7. Add auth/secrets handling, write-action safety gates, rate-limit behavior, and audit/log path before relying on it in crons or client work.
8. Pair the CLI with a small skill/docs handoff and eval questions.
Use `templates/agent-native-cli-template.md` for non-trivial tool builds.

## Browser Automation / Site-Task Rule
For browser/site tasks, avoid repeated high-agency exploration.
1. Probe with fetch/API/static HTML first.
2. Use deterministic parsers/scripts when data is present in responses.
3. Escalate to Playwright/browser reconnaissance only for JS/auth/dynamic flows.
4. If exploration discovers a repeatable path, graduate it into a skill/checklist/helper script with endpoints/selectors/gotchas/verification.
5. If no stable path exists, save a strategy note using `templates/browser-site-strategy-template.md`, not a claimed reusable skill.

## n8n Build Rule
**Before** ANY n8n workflow build: read `~/projects/n8n-agent/tasks/lessons.md` in full. No exceptions.

**How to build:** Always spawn the Claude Code ACP agent (`sessions_spawn` runtime="acp", workdir=`~/projects/n8n-agent`). Do NOT build n8n workflows via exec/Python scripts directly — the ACP agent reads CLAUDE.md (which enforces lessons.md read at session start). If Eve must build directly for any reason, she must read lessons.md herself before writing a single node.

**Task prompt when spawning:** must include `"Read tasks/lessons.md in full before starting. Apply all relevant lessons."`

After EVERY n8n workflow build, update `~/projects/n8n-agent/tasks/lessons.md` with lessons learned before the session ends. Format: `[client-name/workflow-name]: lesson`. Then `git add tasks/lessons.md && git commit -m "Update lessons.md — [workflow-name]"`. No exceptions — a build without a lessons update is incomplete.

## n8n Demo Close-Out Checklist
Not done until: (1) workflow JSON saved (2) git commit + push (3) lessons.md updated (4) MC task done (5) daily note updated (6) portfolio queue entry added (7) JT manual steps → 🌙 HIGH MC task.

## Agentforce Build Rules
- Sync is live: `jsomwarux/agentforce-agent` → `~/projects/agentforce-agent`
- Before ANY Agentforce work: `cd ~/projects/agentforce-agent && git pull origin main`
- After ANY Agentforce work: `git add . && git commit -m "..." && git push origin main`
- Overnight builds are allowed — pull first, push after, every time

## Agentforce Site Rules (still enforced)
- B2B Account Service Agent: permanently banned from jtsomwaru.com. Do not add it under any circumstances.
- NEVER add anything to jtsomwaru.com that is not fully built, fully tested, and explicitly approved by JT. Adding unbuilt/untested work misrepresents JT's capabilities. This is a trust violation.
