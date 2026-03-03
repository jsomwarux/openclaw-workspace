# TOOLS.md — Base Template
# Agent-specific tool configuration and local setup notes.
# Skills define HOW tools work. This file is YOUR specifics — unique to this agent's setup.

---

## What Goes Here

- SSH hosts and aliases
- API keys for external services (NOT in openclaw.json)
- Camera names, device nicknames, speaker labels
- Preferred voices for TTS
- Environment-specific paths and credentials
- Anything unique to this agent's infrastructure

---

## External API Keys

Store third-party service keys here as reference notes.
Never put them in `openclaw.json` — invalid keys crash the gateway.

```
# Example:
# ServiceName API Key: sk-xxxx...
# Endpoint: https://api.example.com
# Notes: Used for X, rate limit Y req/min
```

---

## SSH / Servers

```
# Example:
# prod-server → 10.0.0.1, user: deploy, key: ~/.ssh/deploy_rsa
# staging     → 10.0.0.2, user: admin
```

---

## Scheduled Jobs

List active cron jobs this agent owns:

| Job ID | Schedule | What it does |
|--------|----------|-------------|
| _(none yet)_ | | |

---

## Notes

<!-- Add agent-specific tool notes, quirks, and setup details below -->
