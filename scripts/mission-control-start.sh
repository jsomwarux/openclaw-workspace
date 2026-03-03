#!/bin/bash
# mission-control-start.sh
# Starts the Mission Control Next.js dashboard.
# Called by com.openclaw.mission-control-next LaunchAgent.
# Category 2: pure automation — zero LLM calls. Approved 2026-02-26.

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
export HOME="/Users/jtsomwaru"

cd /Users/jtsomwaru/.openclaw/workspace/mission-control

exec /opt/homebrew/bin/node node_modules/.bin/next start -H 0.0.0.0
