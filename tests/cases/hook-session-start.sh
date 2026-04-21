#!/bin/bash
# session-start.sh — emits additionalContext JSON consumed by Claude at start.

GUARD="$ROOT_DIR/.claude/hooks/session-start.sh"

_run_guard() {
  echo '{"source":"startup"}' | CLAUDE_PROJECT_DIR="$1" bash "$GUARD"
}

test_outputs_valid_json() {
  local out
  out=$(_run_guard "$ROOT_DIR" 2>/dev/null)
  if ! echo "$out" | jq -e '.hookSpecificOutput.additionalContext' >/dev/null 2>&1; then
    _fail "hook output is not the expected JSON shape"
    return 1
  fi
  return 0
}

test_reports_git_branch() {
  local ctx
  ctx=$(_run_guard "$ROOT_DIR" 2>/dev/null | jq -r '.hookSpecificOutput.additionalContext')
  assert_contains "$ctx" "Git branch:" "must include git branch line"
}

test_auto_resume_on_wip_presence() {
  local tmp=$(mktemp -d)
  (cd "$tmp" && git init -q -b main && git commit --allow-empty -q -m init)
  mkdir -p "$tmp/wip/task-20260420-demo"
  printf '# Demo WIP\n' > "$tmp/wip/task-20260420-demo/README.md"
  local ctx
  ctx=$(_run_guard "$tmp" 2>/dev/null | jq -r '.hookSpecificOutput.additionalContext')
  rm -rf "$tmp"
  assert_contains "$ctx" "Active WIP tasks" "must detect WIP directory"
  assert_contains "$ctx" "AUTO_RESUME" "must emit AUTO_RESUME directive"
  assert_contains "$ctx" "task-20260420-demo" "must list the WIP task"
}

test_env_issue_on_missing_env_dir() {
  local tmp=$(mktemp -d)
  (cd "$tmp" && git init -q -b main && git commit --allow-empty -q -m init)
  local ctx
  ctx=$(_run_guard "$tmp" 2>/dev/null | jq -r '.hookSpecificOutput.additionalContext')
  rm -rf "$tmp"
  assert_contains "$ctx" ".env/ directory missing" "must flag missing .env/"
}

test_stale_marker_is_cleaned_up() {
  local tmp=$(mktemp -d)
  (cd "$tmp" && git init -q -b main && git commit --allow-empty -q -m init)
  mkdir -p "$tmp/.claude"
  touch "$tmp/.claude/.last-verification.nonexistent-branch"
  _run_guard "$tmp" >/dev/null 2>&1
  local stale_still_there=0
  [ -f "$tmp/.claude/.last-verification.nonexistent-branch" ] && stale_still_there=1
  rm -rf "$tmp"
  assert_eq 0 "$stale_still_there" "stale marker for deleted branch must be cleaned up"
}
