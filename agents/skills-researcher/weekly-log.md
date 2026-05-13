# Weekly Log — Skills & API Researcher

## Week: 2026-W20 (May 11 - May 17, 2026)

<!-- Daily scans append below -->

## 2026-05-09 Daily Scan

### 🔴 OpenClaw v2026.5.9-beta.1 — Codex harness + model identity/runtime fixes
- Source: https://github.com/openclaw/openclaw/releases/tag/v2026.5.9-beta.1
- Relevance: JT actively runs OpenClaw and has a same-day reminder to reevaluate the Codex plugin / embedded Codex harness. Release updates @openai/codex 0.130.0, Codex harness model snapshot, current provider/model identity injection, `oc-path`, active-memory toolsAllow, Telegram throttling/reasoning defaults, secret redaction, task ledger RPC, and Gemini 3.1 ID normalization.
- Cost: free beta; install/update risk because prerelease.
- Fits: Eve/OpenClaw ops.
- First action: open release notes and run a non-config-changing smoke check against current install before touching gateway/model config.
- MC quality gate: PASS — directly relevant to active OpenClaw/Codex harness decision within 48h.

### 🟠 OpenRouter new model options — Gemini 3.1 Flash Lite + Ring-2.6-1T free
- Source: https://openrouter.ai/api/v1/models
- Relevance: OpenRouter is active, crons/cost tracking are active, and Gemini 3.1 Flash Lite/Ring-2.6-1T may lower costs for high-volume scan/summarization tasks if smoke-tested safely.
- Cost: Gemini 3.1 Flash Lite low-cost; Ring-2.6-1T free.
- Fits: Eve/cost tracker/model routing.
- First action: run a one-off model smoke test for structured summary + tool-call compatibility, without changing defaults.
- MC quality gate: PASS — specific immediate experiment with potential cost impact.
[2026-05-11] daily scan — no critical findings. KB'd: OpenClaw v2026.5.10-beta.3 beta notes; OpenRouter free/cheap models; n8n-mcp reminder; property-management AI signals; MCP security/monitoring signals.

[2026-05-12] 🔴 OpenClaw v2026.5.10-beta.5 — active-stack release with agent policy controls, secret redaction, symlinked memory path rejection, process/session fixes, localService model startup, and Control UI recovery panel. Source: https://github.com/openclaw/openclaw/releases/tag/v2026.5.10-beta.5 | Relevance: Eve/OpenClaw runtime | First action: run `openclaw update --version v2026.5.10-beta.5`, restart gateway if prompted, then run `openclaw gateway status` and one Telegram self-test.
