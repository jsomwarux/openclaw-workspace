# SECURITY.md - Hard Rules

## 🚨 Gateway Management — HANDS OFF

**Never run gateway commands. Ever.**

Banned commands (operator-only):
- `openclaw gateway restart`
- `openclaw gateway stop`
- `openclaw gateway start`
- `openclaw gateway install`

**Why:** v2026.2.19-2 bug — CLI gateway commands trigger a pairing deadlock that crashes the gateway.

**If a restart seems needed:** Tell JT. They will do it manually from Terminal.

JT will notify when the bug is fixed and this restriction can be lifted.

---

## ⚠️ openclaw.json — No Arbitrary Keys

Never write arbitrary keys to `~/.openclaw/openclaw.json`. Invalid keys crash the gateway on startup. Only documented OpenClaw config keys. Store external API keys (Firecrawl, etc.) in TOOLS.md instead.
