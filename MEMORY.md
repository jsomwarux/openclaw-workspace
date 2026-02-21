# MEMORY.md - Long-Term Memory

## JT
- First contact: 2026-02-21 via Telegram
- Named me Eve
- Direct, efficient, low on ceremony — doesn't want hand-holding
- Timezone: America/New_York

## Setup State (as of 2026-02-21)
- **Brave Search** → configured (`tools.web.search.apiKey`)
- **Groq** → configured (`groq:manual` auth profile)
- **QMD skill** → installed (`workspace/skills/qmd/`)
- **qmd binary** → installed via bun, runs from `~/.bun/bin/qmd`
- **~/.bun/bin** → added to PATH in `~/.zshrc`
- **Anthropic/Claude** → primary model (default)

## 🚨 Hard Rules
- **NEVER run gateway commands** (`restart/stop/start/install`) — v2026.2.19-2 bug causes pairing deadlock. Tell JT, let them do it manually.
- **NEVER write arbitrary keys to `~/.openclaw/openclaw.json`** — invalid keys crash the gateway. External API keys go in TOOLS.md.

## Notes
- `qmd` binary was patched to use `bun src/qmd.ts` instead of `node dist/qmd.js` (build wouldn't compile with tsc — missing @types/node)
- Firecrawl API key: stored in TOOLS.md (not openclaw.json)
