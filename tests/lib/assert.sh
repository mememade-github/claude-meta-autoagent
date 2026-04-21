#!/bin/bash
# Assertion primitives for the behaviour suite.
# Each helper returns 0 on pass, 1 on fail, printing a diff-style message on fail.
# Tests accumulate failures into $FAILED_ASSERTS (int) via the runner.

FAILED_ASSERTS=0
CURRENT_TEST=""

_fail() {
  FAILED_ASSERTS=$((FAILED_ASSERTS + 1))
  printf '    FAIL [%s] %s\n' "$CURRENT_TEST" "$1" >&2
}

assert_eq() {
  local expected="$1" actual="$2" msg="${3:-values differ}"
  if [ "$expected" != "$actual" ]; then
    _fail "$msg: expected=<$expected> actual=<$actual>"
    return 1
  fi
  return 0
}

assert_ne() {
  local unexpected="$1" actual="$2" msg="${3:-value should differ}"
  if [ "$unexpected" = "$actual" ]; then
    _fail "$msg: got unexpected value <$actual>"
    return 1
  fi
  return 0
}

assert_contains() {
  local haystack="$1" needle="$2" msg="${3:-substring missing}"
  case "$haystack" in
    *"$needle"*) return 0 ;;
  esac
  _fail "$msg: <$needle> not in <$(printf '%s' "$haystack" | head -c 200)>"
  return 1
}

assert_not_contains() {
  local haystack="$1" needle="$2" msg="${3:-substring should be absent}"
  case "$haystack" in
    *"$needle"*)
      _fail "$msg: <$needle> found in <$(printf '%s' "$haystack" | head -c 200)>"
      return 1
      ;;
  esac
  return 0
}

assert_file_exists() {
  local path="$1" msg="${2:-file missing}"
  if [ ! -e "$path" ]; then
    _fail "$msg: $path"
    return 1
  fi
  return 0
}

assert_file_absent() {
  local path="$1" msg="${2:-file should not exist}"
  if [ -e "$path" ]; then
    _fail "$msg: $path"
    return 1
  fi
  return 0
}
