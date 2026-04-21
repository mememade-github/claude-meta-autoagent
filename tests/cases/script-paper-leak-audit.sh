#!/bin/bash
# paper-leak-audit.sh — scans an ARGUMENT.md for paper-identifying keywords.

SCRIPT="$ROOT_DIR/scripts/meta/paper-leak-audit.sh"

test_usage_on_missing_args() {
  local ec out
  out=$(bash "$SCRIPT" 2>&1)
  ec=$?
  assert_eq 2 "$ec" "no args must exit 2"
  assert_contains "$out" "Usage:" "must print usage"
}

test_missing_file_exits_two() {
  local ec
  bash "$SCRIPT" /nonexistent/path >/dev/null 2>&1
  ec=$?
  assert_eq 2 "$ec" "missing file must exit 2"
}

test_clean_file_passes() {
  local tmp=$(mktemp)
  printf 'Ordinary argument about minimal operator sets.\n' > "$tmp"
  local ec
  bash "$SCRIPT" "$tmp" >/dev/null 2>&1
  ec=$?
  rm -f "$tmp"
  assert_eq 0 "$ec" "clean file must pass"
}

test_leaked_file_fails() {
  local tmp=$(mktemp)
  printf 'The eml construction due to Odrzywolek.\n' > "$tmp"
  local ec out
  out=$(bash "$SCRIPT" "$tmp" 2>&1)
  ec=$?
  rm -f "$tmp"
  assert_eq 1 "$ec" "leaked keywords must exit 1"
  assert_contains "$out" "LEAK" "must report LEAK"
}

test_detects_arxiv_id() {
  local tmp=$(mktemp)
  printf 'Reference: arxiv 2603.21852\n' > "$tmp"
  local ec
  bash "$SCRIPT" "$tmp" >/dev/null 2>&1
  ec=$?
  rm -f "$tmp"
  assert_eq 1 "$ec" "arxiv id must be detected"
}
