#!/usr/bin/env bash
# Eve's Workspace Backup Script
# Runs daily at 2:00 AM EST via system crontab
# Backs up ~/.openclaw/workspace/ → ~/.openclaw/backups/YYYY-MM-DD/
# Retains last 7 daily backups, deletes older ones

set -euo pipefail

WORKSPACE="$HOME/.openclaw/workspace"
BACKUP_ROOT="$HOME/.openclaw/backups"
DATE=$(date +%Y-%m-%d)
DEST="$BACKUP_ROOT/$DATE"
LOG="$BACKUP_ROOT/backup.log"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG"
}

FAILURES=()
record_failure() {
  FAILURES+=("$*")
  log "  ⚠ $*"
}

backup_git_repo() {
  local repo="$1"
  local branch="$2"
  local label="$3"
  local preflight

  log "Pushing $label to GitHub..."
  if ! preflight=$(python3 "$WORKSPACE/scripts/git_backup_preflight.py" \
      --repo "$repo" --branch "$branch" --json 2>&1); then
    record_failure "$label GitHub push skipped by preflight: $preflight"
    return 0
  fi

  cd "$repo"
  if git diff --quiet && git diff --cached --quiet; then
    log "  ✓ No changes to commit"
  else
    git add -A
    if git commit -m "Nightly backup — $(date +%Y-%m-%d)" >> "$LOG" 2>&1; then
      log "  ✓ Committed $label changes"
    else
      record_failure "$label commit failed"
      return 0
    fi
  fi
  if git push origin "$branch" >> "$LOG" 2>&1; then
    log "  ✓ Pushed $label"
  else
    record_failure "$label GitHub push failed"
  fi
}

log "=== Backup started → $DEST ==="

# Create destination
mkdir -p "$DEST"

# ── Markdown files at workspace root ──────────────────────────────────────────
log "Backing up workspace root .md files..."
for f in SOUL.md SECURITY.md USER.md IDENTITY.md TOOLS.md MEMORY.md AGENTS.md HEARTBEAT.md SKILLS.md BOOTSTRAP.md; do
  src="$WORKSPACE/$f"
  if [ -f "$src" ]; then
    cp "$src" "$DEST/$f"
    log "  ✓ $f"
  fi
done

# ── Directories to back up ────────────────────────────────────────────────────
log "Backing up directories..."
for dir in memory knowledge plans proofs tasks; do
  src="$WORKSPACE/$dir"
  if [ -d "$src" ]; then
    rsync -a \
      --exclude='node_modules/' \
      --exclude='__pycache__/' \
      --exclude='.git/' \
      --exclude='*.pyc' \
      "$src/" "$DEST/$dir/"
    log "  ✓ $dir/"
  fi
done

# ── interventions.jsonl ───────────────────────────────────────────────────────
if [ -f "$WORKSPACE/interventions.jsonl" ]; then
  cp "$WORKSPACE/interventions.jsonl" "$DEST/interventions.jsonl"
  log "  ✓ interventions.jsonl"
fi

# ── Sacred files: global.env (never overwrite — back up for recovery only) ────
GLOBAL_ENV="$HOME/.config/env/global.env"
if [ -f "$GLOBAL_ENV" ]; then
  cp "$GLOBAL_ENV" "$DEST/global.env.bak"
  log "  ✓ global.env.bak"
fi

# ── Cleanup: keep last 7 backups ──────────────────────────────────────────────
log "Pruning old backups (keeping last 7)..."
cd "$BACKUP_ROOT"
# List dirs sorted by name (date-based, so alphabetical = chronological)
dirs=($(ls -d [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] 2>/dev/null | sort))
total=${#dirs[@]}
keep=7

if [ "$total" -gt "$keep" ]; then
  to_delete=$(( total - keep ))
  for i in $(seq 0 $(( to_delete - 1 ))); do
    old="${dirs[$i]}"
    rm -rf "$BACKUP_ROOT/$old"
    log "  🗑 Deleted old backup: $old"
  done
fi

# ── Cost snapshot ────────────────────────────────────────────────────────────
log "Capturing daily API cost snapshot..."
if python3 "$WORKSPACE/scripts/cost-tracker.py" --snapshot >> "$LOG" 2>&1; then
  log "  ✓ Cost snapshot saved to memory/costs/$(date +%Y-%m-%d).json"
else
  record_failure "Cost snapshot failed"
fi

# ── GitHub push ───────────────────────────────────────────────────────────────
# Fetch and inspect each remote before staging or committing. Remote-ahead or
# diverged repositories are preserved for deliberate reconciliation instead of
# accumulating commits behind a push that cannot succeed.
backup_git_repo "$WORKSPACE" master "jsomwarux/openclaw-workspace"
backup_git_repo "$HOME/projects/jt-consulting-pipeline" master "jsomwarux/jt-consulting-pipeline"
backup_git_repo "$HOME/projects/n8n-agent" main "jsomwarux/n8n-agent"

# ── Google Drive OAuth token proactive refresh ────────────────────────────────
# Runs on the 1st of each month. Refreshes the token before Google expires it.
# (Published-app tokens are long-lived but proactive refresh prevents silent failures)
DAY_OF_MONTH=$(date +%-d)
if [ "$DAY_OF_MONTH" = "1" ]; then
  log "Monthly Drive token refresh..."
  TOKEN_PATH="$HOME/.openclaw/workspace/config/google-oauth-token.json"
  if [ -f "$TOKEN_PATH" ]; then
    python3 -c "
import json, os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
TOKEN_PATH = os.path.expanduser('~/.openclaw/workspace/config/google-oauth-token.json')
with open(TOKEN_PATH) as f:
    td = json.load(f)
creds = Credentials(
    token=td.get('token'),
    refresh_token=td.get('refresh_token'),
    token_uri=td.get('token_uri'),
    client_id=td.get('client_id'),
    client_secret=td.get('client_secret'),
)
creds.refresh(Request())
td['token'] = creds.token
with open(TOKEN_PATH, 'w') as f:
    json.dump(td, f)
print('Token refreshed OK')
" >> "$LOG" 2>&1 && log "  ✓ Drive token refreshed" || record_failure "Drive token refresh failed — re-auth may be needed"
  else
    record_failure "Drive token file not found at $TOKEN_PATH"
  fi
fi

# ── Failure escalation artifact ──────────────────────────────────────────────
if [ "${#FAILURES[@]}" -gt 0 ]; then
  ALERT_DIR="$WORKSPACE/reports/backup-alerts"
  mkdir -p "$ALERT_DIR"
  ALERT_FILE="$ALERT_DIR/$DATE.md"
  {
    echo "# Backup Alert — $DATE"
    echo
    echo "Local backup completed at: $DEST"
    echo
    echo "## Nonfatal failures requiring follow-up"
    for failure in "${FAILURES[@]}"; do
      echo "- $failure"
    done
    echo
    echo "Log: $LOG"
  } > "$ALERT_FILE"
  log "  ⚠ Backup completed with ${#FAILURES[@]} nonfatal failure(s); alert written to $ALERT_FILE"
fi

# ── Summary ───────────────────────────────────────────────────────────────────
size=$(du -sh "$DEST" 2>/dev/null | cut -f1)
remaining=$(ls -d "$BACKUP_ROOT"/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] 2>/dev/null | wc -l | tr -d ' ')
log "=== Backup complete — $size at $DEST (${remaining} backup(s) retained) ==="
if [ "${#FAILURES[@]}" -gt 0 ]; then
  exit 2
fi
