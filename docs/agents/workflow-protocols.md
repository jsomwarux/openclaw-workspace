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
