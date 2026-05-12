#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 1 ]]; then
  echo "Usage: scripts/gbrain-consulting-search.sh \"Company/person/offer query\"" >&2
  exit 2
fi
export PATH="$HOME/.bun/bin:$PATH"
export GBRAIN_HOME="/Users/jtsomwaru/projects/gbrain-pilot-home"
exec gbrain search "$*"
