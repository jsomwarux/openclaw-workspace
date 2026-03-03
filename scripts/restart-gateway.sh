#!/bin/bash
# restart-gateway.sh
# Safe gateway restart. Sends a Telegram notification via direct API call
# BEFORE cutting the connection — no cron jobs, no deleteAfterRun, nothing scheduled.
#
# Usage: bash restart-gateway.sh [message]
# Example: bash restart-gateway.sh "Restart complete. Compaction buffer updated."

set -e

TELEGRAM_TARGET="6608544825"
CUSTOM_MSG="${1:-Gateway restarted and back online. ✅}"

# Load bot token from env config
if [ -f "$HOME/.config/env/global.env" ]; then
  source "$HOME/.config/env/global.env"
fi

# Send direct Telegram notification BEFORE restart (fire-and-forget)
if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
  echo "📨 Sending pre-restart Telegram notification..."
  curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -d "chat_id=${TELEGRAM_TARGET}" \
    -d "text=🔄 Gateway restarting now. Will be back online in ~30 seconds." \
    > /dev/null 2>&1 || true
fi

echo "🔄 Restarting gateway..."
launchctl unload ~/Library/LaunchAgents/ai.openclaw.gateway.plist
sleep 3
launchctl load ~/Library/LaunchAgents/ai.openclaw.gateway.plist
echo "✅ Gateway restarted."

# NOTE: Do NOT create any cron jobs here — not one-shot, not deleteAfterRun, nothing.
# When the gateway comes back online, the main session will send a message directly.
# NEVER use deleteAfterRun:true jobs for post-restart notifications. See AGENTS.md.
