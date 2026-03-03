# SKILLS.md — Base Template
# Tracks installed skills for this agent.
# Only install skills this agent actually needs — every skill adds context and attack surface.

---

## Skill Discipline

**Install only what's needed for this agent's domain.**

Bad: installing coding-agent skill on a research-only agent
Good: installing only the weather skill on a home-automation agent

Each skill adds:
- Token cost (skill files loaded into context)
- Attack surface (more capabilities = more abuse potential)
- Maintenance burden (skills need updating)

When in doubt, don't install it. Add it only when a specific task demands it.

---

## Installed Skills

| Skill | Location | Purpose | Date Installed |
|-------|----------|---------|---------------|
| _(none yet)_ | | | |

---

## Finding Skills

```bash
# Browse installed skills
ls /opt/homebrew/lib/node_modules/openclaw/skills/

# Browse community skills
# https://clawhub.com

# Install a skill
openclaw skills install <skill-name>
```

---

## Skill Usage Protocol

Before using a skill:
1. Check if it's listed above — if not, don't assume it's installed
2. Read its `SKILL.md` before running any commands from it
3. After installing a new skill, add it to the table above

---

## Agent-Specific Notes

<!-- Add notes about skill usage patterns, known issues, or customizations -->
