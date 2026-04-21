#!/bin/bash
# delegate-goal.sh — GOAL-not-METHOD validation (launch path skipped in tests).
# We exercise only the pre-action gates; they exit before `docker exec`.

SCRIPT="$ROOT_DIR/scripts/meta/delegate-goal.sh"

test_usage_on_missing_args() {
  local out ec
  out=$(bash "$SCRIPT" 2>&1)
  ec=$?
  assert_eq 1 "$ec" "no args must exit 1"
  assert_contains "$out" "Usage:" "must print usage"
}

test_rejects_unknown_project_key() {
  local out ec
  out=$(bash "$SCRIPT" nope "a goal long enough to pass length gate" 2>&1)
  ec=$?
  assert_eq 1 "$ec" "unknown project key must exit 1"
  assert_contains "$out" "Unknown project key" "must explain failure"
}

test_rejects_slash_command_in_goal() {
  local out ec
  out=$(bash "$SCRIPT" a 'run /refine now please please' 2>&1)
  ec=$?
  assert_eq 1 "$ec" "slash command in GOAL must exit 1"
  assert_contains "$out" "slash command" "must explain slash command rejection"
}

test_rejects_imperative_step_list() {
  local out ec
  out=$(bash "$SCRIPT" a '1. Run the build
2. Edit README
3. Commit changes' 2>&1)
  ec=$?
  assert_eq 1 "$ec" "numbered imperative steps must be rejected"
  assert_contains "$out" "imperative" "must explain step-list rejection"
}

test_rejects_short_goal() {
  local out ec
  out=$(bash "$SCRIPT" a 'short' 2>&1)
  ec=$?
  assert_eq 1 "$ec" "goal under 10 chars must exit 1"
  assert_contains "$out" "too short" "must explain length failure"
}

test_rejects_invalid_effort() {
  local out ec
  out=$(EFFORT=wild bash "$SCRIPT" a 'a sufficiently descriptive outcome' 2>&1)
  ec=$?
  assert_eq 1 "$ec" "invalid EFFORT must exit 1"
  assert_contains "$out" "EFFORT" "must name EFFORT"
}
