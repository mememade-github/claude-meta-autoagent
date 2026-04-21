#!/bin/bash
# pre-push-gate.sh — credential + URL-drift gate on git push.

GUARD="$ROOT_DIR/.claude/hooks/pre-push-gate.sh"

_fresh_repo() {
  local dir="$1" remote_url="$2"
  (cd "$dir" && git init -q -b main && git commit --allow-empty -q -m init)
  git -C "$dir" remote add origin "$remote_url"
  mkdir -p "$dir/.claude"
}

_run_guard() {
  jq -cn --arg c "$1" '{tool_input:{command:$c}}' \
  | CLAUDE_PROJECT_DIR="$2" bash "$GUARD"
}

test_allows_non_push_command() {
  local ec
  _run_guard 'git status' "$ROOT_DIR" >/dev/null 2>&1
  ec=$?
  assert_eq 0 "$ec" "non-push command must pass"
}

test_blocks_push_with_pat_in_url() {
  local tmp=$(mktemp -d)
  _fresh_repo "$tmp" "https://ghp_ABCDEF@github.com/x/y.git"
  local out ec
  out=$(_run_guard 'git push origin main' "$tmp" 2>&1)
  ec=$?
  rm -rf "$tmp"
  assert_eq 2 "$ec" "PAT residue in URL must block"
  assert_contains "$out" "credential" "must mention credential"
}

test_allows_clean_ssh_push() {
  local tmp=$(mktemp -d)
  _fresh_repo "$tmp" "git@github.com:x/y.git"
  local ec
  _run_guard 'git push origin main' "$tmp" >/dev/null 2>&1
  ec=$?
  rm -rf "$tmp"
  assert_eq 0 "$ec" "clean SSH URL must pass"
}

test_warns_on_url_drift() {
  local tmp=$(mktemp -d)
  _fresh_repo "$tmp" "git@github.com:x/y.git"
  echo "git@github.com:OLD/repo.git" > "$tmp/.claude/.last-push-url.origin"
  local out ec
  out=$(_run_guard 'git push origin main' "$tmp" 2>&1)
  ec=$?
  rm -rf "$tmp"
  assert_eq 0 "$ec" "drift warning must not block"
  assert_contains "$out" "changed" "must emit drift warning"
}

test_blocks_on_declaration_mismatch() {
  local tmp=$(mktemp -d)
  _fresh_repo "$tmp" "git@github.com:wrong/place.git"
  printf 'origin=github.com:correct/place.git\n' > "$tmp/.claude/.push-remote"
  local out ec
  out=$(_run_guard 'git push origin main' "$tmp" 2>&1)
  ec=$?
  rm -rf "$tmp"
  assert_eq 2 "$ec" "declaration mismatch must block"
  assert_contains "$out" "declaration" "must mention declaration"
}
