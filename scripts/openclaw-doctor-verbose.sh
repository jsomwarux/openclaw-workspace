#!/usr/bin/env bash
set -u

DIAG="$HOME/.openclaw/workspace/scripts/gateway-diagnose.py"
PREFLIGHT="$HOME/.openclaw/workspace/scripts/gateway-preflight.sh"
PORT="${OPENCLAW_GATEWAY_PORT:-18789}"
PLIST="$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist"

echo "== OpenClaw Gateway Doctor =="
date

echo "\n== launchctl =="
launchctl print "gui/$(id -u)/ai.openclaw.gateway" 2>&1 \
  | sed -E 's/(KEY|TOKEN|SECRET|PASSWORD)( => | = )[^[:space:]]+/\1\2[REDACTED]/g; s/(sk-[A-Za-z0-9_-]{8})[A-Za-z0-9_-]+/\1[REDACTED]/g' \
  | tail -40 || true

echo "\n== gateway process =="
pgrep -af "/opt/homebrew/lib/node_modules/openclaw/dist/index.js gateway" || echo "not running"

echo "\n== port $PORT =="
lsof -nP -iTCP:"$PORT" -sTCP:LISTEN 2>/dev/null || echo "no listener"

echo "\n== preflight =="
"$PREFLIGHT" check || true

echo "\n== structured diagnosis =="
python3 "$DIAG" json || true

echo "\n== env presence (redacted) =="
python3 - <<'PY'
import os
keys=['OPENAI_API_KEY','ANTHROPIC_API_KEY','OPENROUTER_API_KEY','TELEGRAM_BOT_TOKEN','FIRECRAWL_API_KEY','NOTION_TOKEN']
for k in keys:
    print(f'{k}: {"present" if os.environ.get(k) else "missing"}')
PY

echo "\n== recommended dependency repair commands (manual approval only) =="
echo "brew update"
echo "brew reinstall simdjson"
echo "brew reinstall node@22"
echo "launchctl unload ~/Library/LaunchAgents/ai.openclaw.gateway.plist"
echo "launchctl load ~/Library/LaunchAgents/ai.openclaw.gateway.plist"
