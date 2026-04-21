#!/bin/bash
# refinement-gate.sh — Stop hook that blocks stop while /refine loop is active.

GUARD="$ROOT_DIR/.claude/hooks/refinement-gate.sh"

_run_guard() {
  echo '{}' | CLAUDE_PROJECT_DIR="$1" bash "$GUARD"
}

test_allows_stop_without_marker() {
  local tmp=$(mktemp -d)
  (cd "$tmp" && git init -q -b main && git commit --allow-empty -q -m init)
  mkdir -p "$tmp/.claude"
  local ec
  _run_guard "$tmp" >/dev/null 2>&1
  ec=$?
  rm -rf "$tmp"
  assert_eq 0 "$ec" "no refinement marker must allow stop"
}

test_blocks_stop_with_active_low_score() {
  local tmp=$(mktemp -d)
  (cd "$tmp" && git init -q -b main && git commit --allow-empty -q -m init)
  mkdir -p "$tmp/.claude/agent-memory/refinement/attempts"
  jq -n '{task_id:"t1",threshold:"0.85",max_iterations:"5"}' > "$tmp/.claude/.refinement-active"
  echo '{"score":0.4}' > "$tmp/.claude/agent-memory/refinement/attempts/t1.jsonl"
  local out ec
  out=$(_run_guard "$tmp" 2>&1)
  ec=$?
  rm -rf "$tmp"
  assert_eq 0 "$ec" "block decision is returned via JSON, not exit code"
  assert_contains "$out" '"decision": "block"' "must emit block decision"
}

test_allows_stop_when_threshold_reached() {
  local tmp=$(mktemp -d)
  (cd "$tmp" && git init -q -b main && git commit --allow-empty -q -m init)
  mkdir -p "$tmp/.claude/agent-memory/refinement/attempts"
  jq -n '{task_id:"t1",threshold:"0.85",max_iterations:"5"}' > "$tmp/.claude/.refinement-active"
  echo '{"score":0.9}' > "$tmp/.claude/agent-memory/refinement/attempts/t1.jsonl"
  local out ec
  out=$(_run_guard "$tmp" 2>&1)
  ec=$?
  rm -rf "$tmp"
  assert_eq 0 "$ec" "threshold reached must allow stop"
  assert_not_contains "$out" '"decision": "block"' "must not emit block decision"
}

test_allows_stop_when_max_iter_reached() {
  local tmp=$(mktemp -d)
  (cd "$tmp" && git init -q -b main && git commit --allow-empty -q -m init)
  mkdir -p "$tmp/.claude/agent-memory/refinement/attempts"
  jq -n '{task_id:"t1",threshold:"0.85",max_iterations:"3"}' > "$tmp/.claude/.refinement-active"
  printf '%s\n' '{"score":0.3}' '{"score":0.4}' '{"score":0.5}' \
    > "$tmp/.claude/agent-memory/refinement/attempts/t1.jsonl"
  local out ec
  out=$(_run_guard "$tmp" 2>&1)
  ec=$?
  rm -rf "$tmp"
  assert_eq 0 "$ec" "max-iter reached must allow stop"
  assert_not_contains "$out" '"decision": "block"' "must not emit block decision"
}
