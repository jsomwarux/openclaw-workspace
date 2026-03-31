# Autoresearch Rules — Full Detail
> Referenced from AGENTS.md. Read this file when creating new skills or agents.

## Autoresearch Candidacy Rule (mandatory at skill/agent creation)
When any new skill (SKILL.md) or agent (AGENT.md) is created, evaluate it for autoresearch enrollment in the same session. Three candidacy questions:
1. Does it run repeatedly (not a one-off build)?
2. Is the output scoreable with yes/no questions (not purely subjective)?
3. Is there a clear failure mode worth fixing automatically?

All three yes → ENROLL:
- Draft a 6-question yes/no checklist (≤6 — overfitting risk above this) based on the skill's stated rules and known failure modes
- Save to `~/.openclaw/workspace/agents/autoresearch/checklists/[skill-slug].md`
- Append entry to `~/.openclaw/workspace/agents/autoresearch/targets.md`:
  `| [skill-slug] | [skill path] | [checklist path] | pending | — | [DATE added] |`
- Note the enrollment in the reply to JT: "Enrolled in autoresearch — checklist at [path]. Review before first loop runs."

Any no → skip silently. Do not force enrollment on subjective or one-off skills.
