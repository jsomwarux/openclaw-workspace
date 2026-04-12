# OpenClaw v2026.4.1 — Research
Date: 2026-04-11
Source: github.com/openclaw/openclaw/releases | releasebot.io

## What's New

**v2026.4.1 — Tasks/Chat Native Task Board**
- Added `/tasks` as a chat-native background task board for the current session
- Shows recent task details and agent-local fallback counts when no linked tasks are visible
- Improves visibility of background task state within conversations

**v2026.4.9-beta.1 — Plugin SDK Auth Cleanup**
- Split command status builders onto lightweight `openclaw/plugin-sdk/command-status` subpath
- Auth-only plugin imports no longer pull status/context warmup into CLI onboarding paths
- Fixes slow startup for auth-only plugins

**v2026.4.x — macOS Gateway Version Parsing Fix**
- Stripped trailing commit metadata from CLI version output before semver parsing
- Mac app now correctly recognizes installed gateway versions like `OpenClaw 2026.4.2 (d74a122)`

**v2026.4.7 — OpenClaw Infer Hub (significant)**
- New `openclaw infer` hub pulls model, media, web, and embedding inference into one first-class CLI surface
- Consolidates inference operations under unified CLI — relevant for AI agent orchestration

## Eve Operational Impact

- `/tasks` task board: no direct impact — Eve uses Mission Control (Convex) for task management
- Plugin SDK auth cleanup: low impact — Eve's plugins are already working
- Infer Hub: worth monitoring — if it can replace separate model calls, could simplify agent orchestration code
- No changes to: cron scheduling, gateway config, LCM, MCP servers, or Agentforce integrations

## Action Items
None. Current setup is unaffected.
