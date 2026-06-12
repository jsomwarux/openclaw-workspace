#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "usage: run_content_guard.sh <linkedin|x> <YYYY-MM-DD>" >&2
  exit 2
fi

platform="$1"
monday="$2"
workspace="/Users/jtsomwaru/.openclaw/workspace"
weekly="$workspace/memory/content/weekly-$monday.md"

case "$platform" in
  linkedin|x) ;;
  *)
    echo "platform must be linkedin or x" >&2
    exit 2
    ;;
esac

exec python3 "$workspace/scripts/content_distribution_guard.py" --weekly "$weekly" --require-reference-map "$platform" --check-notion-script
