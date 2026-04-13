# Operational Rules
> Source: AGENTS.md — extracted to keep AGENTS.md under bootstrap budget.
> These sections are referenced inline in AGENTS.md with `> Full spec: docs/agents/operational-rules.md`

## Verification (before marking done)
- Run it, test it, check logs, demonstrate correctness
- LARP check: no stubs, no fake data, no hardcoded-pretending-dynamic, no silent error swallowing
- Can't prove it works = not done

## Clarify Before Executing
- Ambiguous task (2+ valid interpretations, different outcomes) → state assumption, ask to confirm before acting
- Multi-file destructive operations → state scope, wait for go-ahead
- Exception: if intent is obvious from context, proceed and note assumption in reply

## Claude-Warden Setup Rule
New project dir created → remind JT to run `/warden-setup` inside it if client-facing, has governance files, or overnight agent will touch it.
Qualifies: client deliverables, jtsomwaru-com, agentforce-agent, consulting demos. Skip: throwaway dirs, one-off scripts.

## Automatic Skill Detection
- Before any task: scan available_skills descriptions. If one clearly matches, read its SKILL.md and follow it.
- If multiple match: pick most specific. Never read more than one skill up front.
- If no skill matches: proceed without reading any SKILL.md.
- **Hard rule: reading the skill file and following the skill file are not the same thing.** After reading, run the skill's pre-output checklist explicitly before generating output. Memory of a skill's rules does not substitute for reading and applying the file. Outreach drafts that bypass the cold-email skill checklist are incomplete work.

## Validated Fix = Apply Immediately Rule
Autoresearch, film review, cron health audit — if the run validates a fix, apply it in the same run.
- Cron payloads → `cron update` (use the cron tool's update action with the jobId and patch)
- Skill files → edit directly
- Creating an MC task for a fix the agent already knows how to make = deferral, not completion

Exception: architectural changes (restructuring a skill's purpose, removing JT-authored sections) → save separately and flag.

**Autoresearch specific:** When autoresearch identifies rule violations in a cron payload and recommends fixes, those fixes must be patched into the cron immediately via `cron update` in the same session. "Logged as recommendations" is not the same as applied. A result file with improvement recommendations that were not applied = incomplete autoresearch run.

## Lessons Auto-Write Rule (mandatory)
Whenever a non-obvious problem is solved, a silent failure mode is discovered, or a pattern is confirmed through operational experience: write the lesson immediately in the same turn. Do not wait for JT to ask.
- n8n/workflow bugs → `~/projects/n8n-agent/tasks/lessons.md`
- Python engine / OpenRouter / ensemble pipeline → `docs/agents/ensemble-build-lessons.md`
- General agent/cron/prompt patterns → `AGENTS.md` Mistakes Log or the relevant skill SKILL.md
- "Would a practitioner be grateful to know this before building?" → yes = write it now.
Never surface "any lessons to add?" as a question. Just add them.

## Project Lessons Rule
Before starting work on ANY project that has a `lessons.md` or `CLAUDE.md` file: read it in full before writing a single line of code or making any changes.
- `~/projects/n8n-agent/tasks/lessons.md` — n8n workflows
- `~/projects/agentforce-agent/CLAUDE.md` — Agentforce builds
- `~/projects/jtsomwaru-com/CLAUDE.md` — portfolio site
- Any project with a lessons file in its root or tasks/ folder
Rule: if a lessons file exists for the project, it must be read. Building without reading = guaranteed repeat of already-solved problems.

## Build & Code Protocols
- **Staff Engineer Bar:** simpler way? error states? hardcoded? duplicated? Fix before presenting.
- **Plan file:** create `tasks/todo.md` before first line of code. Exception: one-liner fixes.
- **n8n:** read `lessons.md` first. Always spawn Claude Code ACP agent. Update lessons.md after every build.
- **Agentforce:** `git pull origin main` before. `git push` after.
- **Site rule:** B2B Account Service Agent permanently banned. Never add unbuilt/untested work to jtsomwaru.com.
