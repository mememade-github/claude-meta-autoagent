#!/bin/bash
# sub-project-edit-guard.sh — blocks Edit/Write targeting frozen sub-projects.

GUARD="$ROOT_DIR/.claude/hooks/sub-project-edit-guard.sh"

_run_guard() {
  # $1 = tool_name, $2 = file_path
  jq -cn --arg t "$1" --arg f "$2" \
    '{tool_name:$t, tool_input:{file_path:$f}}' \
  | CLAUDE_PROJECT_DIR="$ROOT_DIR" bash "$GUARD"
}

test_blocks_edit_inside_frozen_a() {
  local out ec
  out=$(_run_guard Edit "$ROOT_DIR/projects/a/CLAUDE.md" 2>&1)
  ec=$?
  assert_eq 2 "$ec" "Edit on frozen A must exit 2"
  assert_contains "$out" "frozen" "message must mention frozen"
}

test_blocks_write_inside_frozen_b() {
  local ec
  _run_guard Write "$ROOT_DIR/projects/b/README.md" >/dev/null 2>&1
  ec=$?
  assert_eq 2 "$ec" "Write on frozen B must exit 2"
}

test_allows_edit_on_root_claude() {
  local ec
  _run_guard Edit "$ROOT_DIR/.claude/rules/devcontainer-patterns.md" >/dev/null 2>&1
  ec=$?
  assert_eq 0 "$ec" "Edit on ROOT .claude/ must pass (not a frozen sub-project)"
}

test_allows_bash_tool_on_frozen_path() {
  # Bash tool isn't Edit/Write; guard should no-op.
  local ec
  _run_guard Bash "$ROOT_DIR/projects/a/anything" >/dev/null 2>&1
  ec=$?
  assert_eq 0 "$ec" "Bash tool must pass regardless of path"
}

test_allows_edit_outside_projects_tree() {
  local ec
  _run_guard Edit "$ROOT_DIR/CLAUDE.md" >/dev/null 2>&1
  ec=$?
  assert_eq 0 "$ec" "Edit at repo root must pass"
}
