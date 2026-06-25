# ClawHub Skill Supply-Chain Audit - 2026-06-24

## Scope
- `/Users/jtsomwaru/.openclaw/workspace/skills`
- `/Users/jtsomwaru/.codex/superpowers/skills`

## Trigger
Mission Control task: `[🔴] OpenClaw ClawHub supply-chain advisory - audit installed skills for marketplace risk`.

Source cited in task: Unit 42 OpenClaw/ClawHub advisory, dated 2026-06-23.

## Command
```bash
rg -n "curl|bash|osascript|security |~/.ssh|~/.config|token|api_key|credential|open https?://|npm install|bun add" \
  /Users/jtsomwaru/.openclaw/workspace/skills \
  /Users/jtsomwaru/.codex/superpowers/skills \
  --glob '!**/node_modules/**'
```

## Result
- No unexpected `~/.ssh`, `osascript`, credential-harvesting, install-on-load, or suspicious external-network execution pattern found in installed skill instructions.
- Expected hits were documentation or known local tooling patterns: X research reads `X_BEARER_TOKEN` from env, job-application documents Google OAuth Drive credentials, runbook documents credential troubleshooting, and consulting/portfolio skills include local preflight scripts or localhost calls.
- Vendored `node_modules` under the brainstorming skill created noisy matches and was excluded from the reviewed result set.

## Disposition
No quarantine or disable action needed. Keep the advisory task closed unless a new ClawHub-sourced skill is installed or a future scan finds unexpected shell/network/credential behavior.
