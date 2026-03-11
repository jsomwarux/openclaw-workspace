#!/bin/bash
# Portfolio Card Preflight — Run before making any changes
# Returns non-zero exit code if any check fails
# Usage: bash scripts/preflight.sh [project-slug]

PROJECT_SLUG=${1:-""}
REPO="$HOME/projects/jtsomwaru-com"
PASS=0
FAIL=0

check() {
  local label="$1"
  local result="$2"  # "ok" or "fail"
  local detail="$3"
  if [ "$result" = "ok" ]; then
    echo "✅ $label"
    PASS=$((PASS + 1))
  else
    echo "❌ $label — $detail"
    FAIL=$((FAIL + 1))
  fi
}

echo "🔍 Portfolio Card Preflight"
echo "================================"

# 1. Repo exists
[ -d "$REPO" ] && check "Repo exists" "ok" "" || check "Repo exists" "fail" "$REPO not found"

# 2. On main branch (warn only)
if [ -d "$REPO" ]; then
  BRANCH=$(cd "$REPO" && git branch --show-current 2>/dev/null)
  [ "$BRANCH" = "main" ] && check "On main branch" "ok" "" || echo "⚠️  On branch '$BRANCH' — ensure this is intentional"
fi

# 3. No uncommitted changes that aren't ours
if [ -d "$REPO" ]; then
  DIRTY=$(cd "$REPO" && git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  [ "$DIRTY" -eq 0 ] && check "Working tree clean" "ok" "" || echo "⚠️  $DIRTY uncommitted changes — this is expected if you just edited projects.ts"
fi

# 4. projects.ts exists and is readable
[ -f "$REPO/src/data/projects.ts" ] && check "projects.ts readable" "ok" "" || check "projects.ts readable" "fail" "file not found"

# 5. ProjectDetail.tsx exists
[ -f "$REPO/src/app/work/[slug]/ProjectDetail.tsx" ] && check "ProjectDetail.tsx readable" "ok" "" || check "ProjectDetail.tsx readable" "fail" "file not found"

# 6. public/images dir exists
[ -d "$REPO/public/images" ] && check "public/images dir exists" "ok" "" || check "public/images dir exists" "fail" "create it first"

# 7. If slug provided, check screenshot folder
if [ -n "$PROJECT_SLUG" ]; then
  IMG_DIR="$REPO/public/images/$PROJECT_SLUG"
  if [ -d "$IMG_DIR" ]; then
    COUNT=$(ls "$IMG_DIR"/*.png "$IMG_DIR"/*.jpg "$IMG_DIR"/*.jpeg 2>/dev/null | wc -l | tr -d ' ')
    [ "$COUNT" -gt 0 ] && check "Screenshots found ($COUNT files) for $PROJECT_SLUG" "ok" "" || check "Screenshots found for $PROJECT_SLUG" "fail" "no image files in $IMG_DIR"
  else
    echo "⚠️  No screenshot folder at $IMG_DIR — create it and add images before running build"
  fi
fi

# 8. Node/npm available
command -v npm >/dev/null 2>&1 && check "npm available" "ok" "" || check "npm available" "fail" "npm not in PATH"

# 9. TypeScript compile check (fast — no emit)
if [ -d "$REPO" ] && command -v npx >/dev/null 2>&1; then
  echo "⏳ Running TypeScript check (no emit)..."
  TS_OUT=$(cd "$REPO" && npx tsc --noEmit 2>&1)
  if [ $? -eq 0 ]; then
    check "TypeScript compiles clean" "ok" ""
  else
    check "TypeScript compiles clean" "fail" "errors found — fix before building"
    echo ""
    echo "TypeScript errors:"
    echo "$TS_OUT" | head -20
  fi
fi

echo ""
echo "================================"
echo "Results: $PASS passed, $FAIL failed"

if [ "$FAIL" -gt 0 ]; then
  echo "❌ Preflight FAILED — fix errors before proceeding"
  exit 1
else
  echo "✅ Preflight PASSED — safe to proceed"
  exit 0
fi
