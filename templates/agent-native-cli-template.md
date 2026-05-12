# Agent-Native CLI / Tool Design Template

Use before building or refactoring a repeated API/data workflow into a script, CLI, MCP server, or OpenClaw skill.

## Existing tool check
Before building anything new, check existing tools/skills/scripts:
- Existing OpenClaw tool/skill/script:
- Why it is insufficient:
- Could this be a wrapper or improvement instead of a new tool?

## Workflow identity
- **Service / data source:**
- **Human product label:**
- **Agent-native identity:** What is this secretly useful for? Example: issue tracker → blocker intelligence, CRM → relationship graph.
- **Primary user:** Eve / JT / client / coding agent / cron
- **Read-only or write-capable:**
- **Auth/secrets location:** env/auth profile only, never hardcoded
- **External/shareable output risk:** what must be redacted?

## Magic command
One command that should solve the recurring job:
```bash
[command] [natural or compact args]
```
Expected output:

## Compound workflow
What multi-step API/browser/manual workflow does this collapse?
1.
2.
3.

## Data strategy
Choose the cheapest reliable option:
- direct API call
- local SQLite/cache mirror
- file snapshot
- browser/site strategy
- hybrid

If local mirror/cache:
- DB path:
- Sync command:
- Freshness rule:
- Drift/backfill strategy:

## Agent output modes
Required where useful:
- `--json` for structured downstream use
- `--compact` for Telegram/briefs
- `--agent` or `--llm` for terse agent-readable output
- `--explain` for human review/debugging

## Tool shape
- Core commands:
- Compound commands:
- Safety gates for writes/destructive actions:
- Pagination/filtering:
- Error messages that suggest next action:

## Safety / permissions
- Read-only by default?
- Write/destructive actions require explicit confirmation?
- Secrets redaction check:
- Rate-limit/backoff behavior:
- Audit/log path for actions:

## Skill / docs handoff
- OpenClaw skill path, if needed:
- CLI help examples:
- Common gotchas:
- Verification command:

## Eval
Create 5-10 real questions/jobs this CLI should answer. Include expected outputs or verification checks.
1.
2.
3.

## Promotion decision
- Keep as script / promote to CLI / expose as MCP / create OpenClaw skill
- Why:
- Next action:
