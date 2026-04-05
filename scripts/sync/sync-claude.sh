#!/bin/bash
# =============================================================================
# sync-claude.sh — Sync portable .claude/ artifacts from ROOT to a sub-project
# =============================================================================
# Usage:
#   ./scripts/sync/sync-claude.sh projects/sample-app
#   ./scripts/sync/sync-claude.sh /path/to/any/project
#
# What syncs:    agents/, hooks/, skills/, settings.json, rules/*.md (root level)
# What doesn't:  rules/project/, agent-memory/ (project-local)
# =============================================================================

set -euo pipefail

if [ $# -eq 0 ]; then
  echo "Usage: $0 <target-project-path>" >&2
  echo "Example: $0 projects/sample-app" >&2
  exit 1
fi

# Resolve ROOT .claude/
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
ROOT_CLAUDE="$ROOT_DIR/.claude"

# Resolve target
TARGET_PATH="$1"
if [[ ! "$TARGET_PATH" = /* ]]; then
  TARGET_PATH="$ROOT_DIR/$TARGET_PATH"
fi
TARGET_CLAUDE="$TARGET_PATH/.claude"

# Validate
if [ ! -d "$ROOT_CLAUDE" ]; then
  echo "ERROR: ROOT .claude/ not found at $ROOT_CLAUDE" >&2
  exit 1
fi

if [ ! -d "$TARGET_CLAUDE" ]; then
  echo "ERROR: Target .claude/ not found at $TARGET_CLAUDE" >&2
  echo "Create it first: mkdir -p $TARGET_CLAUDE/{agents,hooks,skills,rules}" >&2
  exit 1
fi

echo "Syncing: $ROOT_CLAUDE → $TARGET_CLAUDE"

# Sync portable artifacts
for item in agents hooks skills settings.json; do
  if [ -e "$ROOT_CLAUDE/$item" ]; then
    cp -r "$ROOT_CLAUDE/$item" "$TARGET_CLAUDE/"
    echo "  synced: $item"
  fi
done

# Sync root-level rules only (preserve project-specific rules/project/)
if [ -d "$ROOT_CLAUDE/rules" ]; then
  # Copy only files at root level of rules/ (not subdirectories)
  find "$ROOT_CLAUDE/rules" -maxdepth 1 -name '*.md' -exec cp {} "$TARGET_CLAUDE/rules/" \;
  echo "  synced: rules/*.md (root level)"
fi

# Ensure project-specific directories exist
mkdir -p "$TARGET_CLAUDE/rules/project" 2>/dev/null || true

echo ""
echo "Done. Preserved: rules/project/, agent-memory/"

# Verify sync
echo ""
echo "Verification (portable files should match):"
DIFF_COUNT=0
for item in agents/evaluator.md agents/wip-manager.md settings.json; do
  if [ -f "$ROOT_CLAUDE/$item" ] && [ -f "$TARGET_CLAUDE/$item" ]; then
    if ! diff -q "$ROOT_CLAUDE/$item" "$TARGET_CLAUDE/$item" > /dev/null 2>&1; then
      echo "  DIVERGED: $item"
      DIFF_COUNT=$((DIFF_COUNT + 1))
    fi
  fi
done

if [ "$DIFF_COUNT" -eq 0 ]; then
  echo "  All portable files match."
else
  echo "  WARNING: $DIFF_COUNT file(s) diverged after sync."
fi
