#!/bin/bash
# Consulting Pipeline Preflight — Run before spawning any pipeline agents
# Returns non-zero exit code if critical checks fail
# Usage: bash scripts/preflight.sh [client-slug]

CLIENT_SLUG=${1:-""}
PIPELINE_DIR="$HOME/projects/jt-consulting-pipeline"
N8N_URL="http://localhost:5678"
PASS=0
FAIL=0
WARN=0

check() {
  local label="$1"
  local result="$2"  # "ok" | "fail" | "warn"
  local detail="$3"
  if [ "$result" = "ok" ]; then
    echo "✅ $label"
    PASS=$((PASS + 1))
  elif [ "$result" = "warn" ]; then
    echo "⚠️  $label — $detail"
    WARN=$((WARN + 1))
  else
    echo "❌ $label — $detail"
    FAIL=$((FAIL + 1))
  fi
}

echo "🔍 Consulting Pipeline Preflight"
echo "================================"

# 1. Pipeline directory exists
[ -d "$PIPELINE_DIR" ] && check "Pipeline dir exists" "ok" "" || check "Pipeline dir exists" "fail" "$PIPELINE_DIR not found"

# 2. pipeline.md tracker exists
[ -f "$PIPELINE_DIR/pipeline.md" ] && check "pipeline.md tracker exists" "ok" "" || check "pipeline.md tracker exists" "fail" "pipeline tracker not found"

# 3. n8n is up
N8N_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$N8N_URL/healthz" 2>/dev/null)
if [ "$N8N_STATUS" = "200" ]; then
  check "n8n is running ($N8N_URL)" "ok" ""
else
  check "n8n is running" "fail" "n8n returned HTTP $N8N_STATUS — start n8n or kick the LaunchAgent before proceeding"
fi

# 4. Required agent directories exist
for agent in research-agent analysis-agent n8n-agent presentation-agent outreach-agent; do
  [ -d "$HOME/projects/$agent" ] && check "$agent dir exists" "ok" "" || check "$agent dir exists" "fail" "not found at ~/projects/$agent"
done

# 5. Drive drafts script available
[ -f "$HOME/.openclaw/workspace/scripts/drive_drafts.py" ] && check "drive_drafts.py available" "ok" "" || check "drive_drafts.py available" "fail" "Drive upload script missing"

# 6. If client slug provided, check for existing vs new
if [ -n "$CLIENT_SLUG" ]; then
  CLIENT_DIR="$PIPELINE_DIR/clients/$CLIENT_SLUG"
  if [ -d "$CLIENT_DIR" ]; then
    # Existing client — check what stage they're at
    echo ""
    echo "📁 Client: $CLIENT_SLUG"
    echo "   Existing artifacts:"
    for artifact in research.md analysis.md brief.json workflow.json outreach-draft.md; do
      [ -f "$CLIENT_DIR/$artifact" ] && echo "   ✅ $artifact" || echo "   ⬜ $artifact (not yet created)"
    done
    
    # Pipeline Integrity Guard: Prevent outreach bypass
    if [ ! -f "$CLIENT_DIR/research.md" ]; then
        check "Research complete" "fail" "research.md is MISSING. Never generate outreach on stale/unverified data. Run research stage first."
    fi
    
    # Warn if outreach already drafted — confirm intent
    [ -f "$CLIENT_DIR/outreach-draft.md" ] && echo "   ⚠️  outreach-draft.md exists — already ran pipeline? Confirm intent before re-running."
  else
    echo ""
    echo "📁 New client: $CLIENT_SLUG"
    echo "   No existing artifacts — fresh pipeline run"
    mkdir -p "$CLIENT_DIR"
    echo "   ✅ Client directory created: $CLIENT_DIR"
  fi
fi

# 7. Shortlists directory check (for new prospect discovery)
if [ -z "$CLIENT_SLUG" ]; then
  SHORTLIST_COUNT=$(ls "$PIPELINE_DIR/shortlists/"*.md 2>/dev/null | wc -l | tr -d ' ')
  [ "$SHORTLIST_COUNT" -gt 0 ] && echo "ℹ️  Shortlists available: $SHORTLIST_COUNT files in $PIPELINE_DIR/shortlists/" || echo "⚠️  No shortlist files found — research a prospect first"
fi

echo ""
echo "================================"
echo "Results: $PASS passed, $FAIL failed, $WARN warnings"

if [ "$FAIL" -gt 0 ]; then
  echo "❌ Preflight FAILED — fix errors before spawning agents"
  exit 1
elif [ "$WARN" -gt 0 ]; then
  echo "⚠️  Preflight passed with warnings — review before proceeding"
  exit 0
else
  echo "✅ Preflight PASSED — safe to run pipeline"
  exit 0
fi
