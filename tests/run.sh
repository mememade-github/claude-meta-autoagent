#!/bin/bash
# tests/run.sh — reproducible-execution verification for claude-meta-autoagent
# Discovers every tests/cases/*.sh, sources it, invokes each `test_*` function,
# prints a human summary, and returns 0 iff all assertions passed.
#
# Design (CLAUDE.md §1.2 Simplicity First): no test framework dependency; pure
# bash. Each case file defines functions named test_*; each function:
#   - prints nothing on pass
#   - calls assert_* helpers which emit "FAIL [name] ..." lines on fail
#   - returns 0 regardless (the accumulated FAILED_ASSERTS drives the result)

set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TESTS_DIR="$ROOT_DIR/tests"

# shellcheck source=lib/assert.sh
. "$TESTS_DIR/lib/assert.sh"

mkdir -p "$TESTS_DIR/results"
LOG_FILE="$TESTS_DIR/results/last-run.log"
: > "$LOG_FILE"

export ROOT_DIR

TOTAL=0
PASSED=0
FAILED=0
FAIL_NAMES=()

echo "tests/run.sh — claude-meta-autoagent behaviour suite"
echo "ROOT: $ROOT_DIR"
echo "================================================================"

for case_file in "$TESTS_DIR"/cases/*.sh; do
  [ -f "$case_file" ] || continue
  case_name=$(basename "$case_file" .sh)
  echo ""
  echo "[case] $case_name"
  # shellcheck disable=SC1090
  . "$case_file"
  # Collect test_* functions defined after sourcing.
  mapfile -t fns < <(declare -F | awk '$3 ~ /^test_/ {print $3}')
  for fn in "${fns[@]}"; do
    TOTAL=$((TOTAL + 1))
    CURRENT_TEST="$case_name::$fn"
    BEFORE_FAILS=$FAILED_ASSERTS
    "$fn" >>"$LOG_FILE" 2>&1 || true
    if [ "$FAILED_ASSERTS" -gt "$BEFORE_FAILS" ]; then
      FAILED=$((FAILED + 1))
      FAIL_NAMES+=("$CURRENT_TEST")
      echo "  FAIL  $fn"
    else
      PASSED=$((PASSED + 1))
      echo "  pass  $fn"
    fi
    unset -f "$fn"
  done
done

echo ""
echo "================================================================"
echo "Total: $TOTAL  Pass: $PASSED  Fail: $FAILED"
if [ "$FAILED" -gt 0 ]; then
  echo ""
  echo "Failed tests:"
  for n in "${FAIL_NAMES[@]}"; do echo "  - $n"; done
  echo ""
  echo "Full log: $LOG_FILE"
  exit 1
fi
echo "All green."
exit 0
