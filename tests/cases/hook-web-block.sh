#!/bin/bash
# web-block.sh — PreToolUse hook matched against WebFetch|WebSearch in A/B.

GUARD="$ROOT_DIR/projects/a/.claude/hooks/web-block.sh"

test_blocks_web_fetch() {
  local ec out
  out=$(echo '{"tool_name":"WebFetch","tool_input":{"url":"https://example.com"}}' | bash "$GUARD" 2>&1)
  ec=$?
  assert_eq 2 "$ec" "WebFetch must exit 2"
  assert_contains "$out" "BLOCKED" "must emit BLOCKED message"
}

test_blocks_web_search() {
  local ec
  echo '{"tool_name":"WebSearch","tool_input":{"query":"anything"}}' | bash "$GUARD" >/dev/null 2>&1
  ec=$?
  assert_eq 2 "$ec" "WebSearch must exit 2"
}

test_blocks_unconditionally_when_invoked() {
  # web-block.sh has no tool_name guard — filtering is done by the settings.json
  # matcher (WebFetch|WebSearch). Once invoked, the hook blocks every call.
  local ec
  echo '{"tool_name":"Read","tool_input":{"file_path":"x"}}' | bash "$GUARD" >/dev/null 2>&1
  ec=$?
  assert_eq 2 "$ec" "script blocks regardless of tool_name; matcher does the filtering"
}
