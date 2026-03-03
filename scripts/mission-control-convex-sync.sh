#!/bin/bash
# mission-control-convex-sync.sh
# Runs the Convex local backend persistently (serves DB on port 3210).
# Called by com.openclaw.mission-control-convex LaunchAgent.
# Category 2: pure automation — zero LLM calls. Approved 2026-02-26.

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
export HOME="/Users/jtsomwaru"

cd /Users/jtsomwaru/.openclaw/workspace/mission-control

exec /opt/homebrew/bin/npx convex dev
