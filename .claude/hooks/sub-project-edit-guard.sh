#!/bin/bash
# PreToolUse (Edit|Write): block edits to any sub-project marked frozen.
#
# A sub-project is frozen for the duration of a Meta-Evolution cycle by
# placing a `.frozen` marker file at its root (e.g. `projects/<name>/.frozen`).
# ROOT acts as Human for such sub-projects: it may only deliver STATE + GOAL
# via the delegate-* wrappers, never edit their files directly.
#
# Self-disabling: if the current CLAUDE.md has no §6, this is not a
# Meta-Evolution ROOT layer, so the hook exits 0 unconditionally.  That
# keeps the hook portable via .claude/ sync without affecting downstream
# projects that don't carry §6.
set -euo pipefail

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // ""')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

case "$TOOL_NAME" in
  Edit|Write) ;;
  *) exit 0 ;;
esac

[ -z "$FILE_PATH" ] && exit 0

PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-/workspaces}"
CLAUDE_MD="${PROJECT_ROOT}/CLAUDE.md"
if [ ! -f "$CLAUDE_MD" ] || ! grep -qE '^#+[[:space:]]*6\.?[[:space:]]*Meta-Evolution' "$CLAUDE_MD"; then
  exit 0
fi

case "$FILE_PATH" in
  /*) ;;
  *)  FILE_PATH="${PROJECT_ROOT}/$FILE_PATH" ;;
esac

# Discover frozen sub-projects by scanning PROJECT_ROOT for `.frozen` markers.
SUB_PROJECTS=()
SUBS_PARENT="${PROJECT_ROOT}/projects"
if [ -d "$SUBS_PARENT" ]; then
  for dir in "$SUBS_PARENT"/*/; do
    [ -d "$dir" ] || continue
    dir="${dir%/}"
    [ -f "${dir}/.frozen" ] && SUB_PROJECTS+=("$dir")
  done
fi

for sp in "${SUB_PROJECTS[@]}"; do
  case "$FILE_PATH" in
    "$sp"/*)
      REASON_FILE="${sp}/.frozen"
      REASON=""
      if [ -s "$REASON_FILE" ]; then
        REASON=$(head -1 "$REASON_FILE")
      fi
      cat >&2 <<EOF2
Blocked: $TOOL_NAME on file inside a frozen sub-project.

Target:            $FILE_PATH
Sub-project root:  $sp
Marker:            $REASON_FILE${REASON:+
Marker reason:     $REASON}

Per CLAUDE.md §6 (frozen-sub-project protocol), ROOT must not edit this
sub-project's files.  Deliver STATE + GOAL via the delegate wrapper
instead, or remove the .frozen marker to unfreeze.
EOF2
      exit 2
      ;;
  esac
done

exit 0
