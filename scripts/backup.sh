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
  log "  ⚠ Cost snapshot failed (non-fatal)"
fi

# ── Summary ───────────────────────────────────────────────────────────────────
size=$(du -sh "$DEST" 2>/dev/null | cut -f1)
remaining=$(ls -d "$BACKUP_ROOT"/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] 2>/dev/null | wc -l | tr -d ' ')
log "=== Backup complete — $size at $DEST (${remaining} backup(s) retained) ==="
