#!/bin/bash
# delegate-sub.sh — paper-keyword pre-filter on top of delegate-goal.sh.

SCRIPT="$ROOT_DIR/scripts/meta/delegate-sub.sh"

test_usage_on_missing_args() {
  local out ec
  out=$(bash "$SCRIPT" 2>&1)
  ec=$?
  assert_eq 1 "$ec" "no args must exit 1"
  assert_contains "$out" "Usage:" "must print usage"
}

test_rejects_unknown_sub_key() {
  local out ec
  out=$(bash "$SCRIPT" z 'a valid long goal for reduction work' 2>&1)
  ec=$?
  assert_eq 1 "$ec" "unknown sub-key must exit 1"
  assert_contains "$out" "Unknown sub-key" "must name the failure"
}

test_rejects_paper_keyword_eml() {
  local out ec
  out=$(bash "$SCRIPT" a 'derive eml operator from first principles carefully' 2>&1)
  ec=$?
  assert_eq 2 "$ec" "paper keyword must exit 2"
  assert_contains "$out" "BLOCKED" "must print BLOCKED"
}

test_rejects_paper_keyword_odrzywolek() {
  local ec
  bash "$SCRIPT" b 'reproduce the Odrzywolek construction in detail here' >/dev/null 2>&1
  ec=$?
  assert_eq 2 "$ec" "surname keyword must exit 2"
}

test_rejects_arxiv_id() {
  local ec
  bash "$SCRIPT" a 'summarise the argument in arxiv 2603.21852 yourself' >/dev/null 2>&1
  ec=$?
  assert_eq 2 "$ec" "arxiv id must exit 2"
}
