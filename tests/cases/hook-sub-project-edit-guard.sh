#!/bin/bash
# sub-project-edit-guard.sh — blocks Edit/Write/Bash changes to frozen sub-projects.

GUARD="$ROOT_DIR/.claude/hooks/sub-project-edit-guard.sh"

_run_guard() {
  # $1 = tool_name, $2 = file_path
  jq -cn --arg t "$1" --arg f "$2" \
    '{tool_name:$t, tool_input:{file_path:$f}}' \
  | CLAUDE_PROJECT_DIR="$ROOT_DIR" bash "$GUARD"
}

_run_guard_bash() {
  # $1 = bash command string
  jq -cn --arg c "$1" \
    '{tool_name:"Bash", tool_input:{command:$c}}' \
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

test_allows_edit_outside_projects_tree() {
  local ec
  _run_guard Edit "$ROOT_DIR/CLAUDE.md" >/dev/null 2>&1
  ec=$?
  assert_eq 0 "$ec" "Edit at repo root must pass"
}

# --- Bash-mode tests (M2.1 forward coverage) ---
#
# These three tests verify that the guard does NOT over-block legitimate
# Bash operations on frozen sub-projects: touching the .frozen marker
# itself, reading frozen files, and writing outside any frozen
# sub-project.  They pass against both the pre-fix permissive-Bash hook
# (which never blocks Bash) and the post-fix token-aware hook.
#
# The complementary "Bash must BLOCK writes into frozen sub-projects"
# cases — sed -i, rm, redirection — require the post-fix hook.  They
# will be added alongside the `.claude/hooks/sub-project-edit-guard.sh`
# + `.claude/settings.json` edits once those sensitive-file edits are
# approved and committed.  See JUDGMENT.md §8 / cycle-log.md Cycle #2
# for the tracking note.

test_bash_allows_frozen_marker_toggle() {
  local ec
  _run_guard_bash "rm $ROOT_DIR/projects/a/.frozen" >/dev/null 2>&1
  ec=$?
  assert_eq 0 "$ec" "Bash may touch the .frozen marker itself (for unfreeze/refreeze)"
}

test_bash_allows_readonly_on_frozen() {
  local ec
  _run_guard_bash "cat $ROOT_DIR/projects/a/CLAUDE.md | head -5" >/dev/null 2>&1
  ec=$?
  assert_eq 0 "$ec" "Read-only Bash on frozen A must pass"
}

test_bash_allows_write_outside_frozen() {
  local ec
  _run_guard_bash "echo x > $ROOT_DIR/docs/research/eml-paper/cycle-02/JUDGMENT.md" >/dev/null 2>&1
  ec=$?
  assert_eq 0 "$ec" "Bash write outside any frozen sub-project must pass"
}
