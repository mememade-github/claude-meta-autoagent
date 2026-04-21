#!/bin/bash
# paper-leak-guard.sh — PreToolUse hook mounted into A and B. Rejects any tool
# payload whose text carries a restricted identifier (reconstructed at runtime
# from reversed forms). A and B ship identical copies (invariants.sh enforces).

GUARD="$ROOT_DIR/projects/a/.claude/hooks/paper-leak-guard.sh"

_run_guard() {
  # $1 = json payload
  printf '%s' "$1" | bash "$GUARD"
}

test_blocks_forbidden_keyword_in_content() {
  local payload
  payload=$(jq -cn '{tool_input:{content:"The eml operator solves this."}}')
  local out ec
  out=$(_run_guard "$payload" 2>&1)
  ec=$?
  assert_eq 2 "$ec" "restricted keyword in content must block"
  assert_contains "$out" "BLOCKED" "must print BLOCKED"
}

test_blocks_forbidden_surname_in_new_string() {
  local payload
  payload=$(jq -cn '{tool_input:{new_string:"As Odrzywolek showed, ..."}}')
  local ec
  _run_guard "$payload" >/dev/null 2>&1
  ec=$?
  assert_eq 2 "$ec" "restricted surname in new_string must block"
}

test_blocks_arxiv_id() {
  local payload
  payload=$(jq -cn '{tool_input:{command:"curl arxiv.org/abs/2603.21852"}}')
  local ec
  _run_guard "$payload" >/dev/null 2>&1
  ec=$?
  assert_eq 2 "$ec" "arxiv id must block"
}

test_blocks_restricted_path_token() {
  local payload
  payload=$(jq -cn '{tool_input:{file_path:"/workspaces/docs/research/hint.md"}}')
  local ec
  _run_guard "$payload" >/dev/null 2>&1
  ec=$?
  assert_eq 2 "$ec" "restricted path token docs/research must block"
}

test_blocks_sheffer() {
  local payload
  payload=$(jq -cn '{tool_input:{content:"A Sheffer-style reduction ..."}}')
  local ec
  _run_guard "$payload" >/dev/null 2>&1
  ec=$?
  assert_eq 2 "$ec" "Sheffer keyword must block"
}

test_allows_benign_payload() {
  local payload
  payload=$(jq -cn '{tool_input:{content:"Ordinary mathematical argument about functions."}}')
  local ec
  _run_guard "$payload" >/dev/null 2>&1
  ec=$?
  assert_eq 0 "$ec" "benign content must pass"
}

test_allows_empty_payload() {
  local ec
  echo '{"tool_input":{}}' | bash "$GUARD" >/dev/null 2>&1
  ec=$?
  assert_eq 0 "$ec" "empty payload must pass"
}
