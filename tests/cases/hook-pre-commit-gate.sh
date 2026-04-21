#!/bin/bash
# pre-commit-gate.sh — gates `git commit` on recent verification.

GUARD="$ROOT_DIR/.claude/hooks/pre-commit-gate.sh"

_run_guard() {
  jq -cn --arg c "$1" '{tool_input:{command:$c}}' \
  | CLAUDE_PROJECT_DIR="${2:-$ROOT_DIR}" bash "$GUARD"
}

_init_repo() {
  # Initialise a temp git repo with an identity (required for commits), on
  # branch main (to match the marker file name used by the tests).
  local dir="$1"
  (
    cd "$dir" || exit 1
    git init -q -b main
    git config user.email tests@example.com
    git config user.name tests
    git commit --allow-empty -q -m init
  )
}

test_allows_non_commit_command() {
  local ec
  _run_guard 'git status' >/dev/null 2>&1
  ec=$?
  assert_eq 0 "$ec" "git status must pass through"
}

test_allows_git_add() {
  local ec
  _run_guard 'git add .' >/dev/null 2>&1
  ec=$?
  assert_eq 0 "$ec" "git add must pass through"
}

test_allows_empty_command() {
  local ec
  echo '{"tool_input":{}}' | CLAUDE_PROJECT_DIR="$ROOT_DIR" bash "$GUARD" >/dev/null 2>&1
  ec=$?
  assert_eq 0 "$ec" "empty command must pass"
}

test_commit_with_fresh_marker_passes() {
  local tmp=$(mktemp -d)
  _init_repo "$tmp"
  mkdir -p "$tmp/.claude"
  touch "$tmp/.claude/.last-verification.main"
  local ec
  _run_guard 'git commit -m test' "$tmp" >/dev/null 2>&1
  ec=$?
  rm -rf "$tmp"
  assert_eq 0 "$ec" "commit with fresh marker must pass"
}

test_commit_with_stale_marker_and_no_checker_blocks() {
  local tmp=$(mktemp -d)
  _init_repo "$tmp"
  mkdir -p "$tmp/.claude"
  touch -d '1 hour ago' "$tmp/.claude/.last-verification.main"
  local out ec
  out=$(_run_guard 'git commit -m test' "$tmp" 2>&1)
  ec=$?
  rm -rf "$tmp"
  assert_eq 2 "$ec" "stale marker with no checker must exit 2"
  assert_contains "$out" "Verification" "must prompt for verification"
}
