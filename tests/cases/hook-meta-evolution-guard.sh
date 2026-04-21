#!/bin/bash
# meta-evolution-guard.sh — blocks direct `docker exec ... claude -p` launches.

GUARD="$ROOT_DIR/.claude/hooks/meta-evolution-guard.sh"

_run_guard() {
  # $1 = command string
  jq -cn --arg c "$1" '{tool_input:{command:$c}}' | bash "$GUARD"
}

test_blocks_direct_docker_exec_claude_p() {
  local out ec
  out=$(_run_guard 'docker exec claude-meta-autoagent-a claude -p "do thing"' 2>&1)
  ec=$?
  assert_eq 2 "$ec" "direct docker exec launching claude -p must exit 2"
  assert_contains "$out" "BLOCKED" "must print BLOCKED message"
}

test_blocks_sudo_docker_exec_claude_p() {
  local ec
  _run_guard 'sudo docker exec ctr claude --effort high -p "x"' >/dev/null 2>&1
  ec=$?
  assert_eq 2 "$ec" "sudo docker exec launching claude -p must also be blocked"
}

test_allows_git_commands_containing_phrase() {
  # A git commit whose message mentions the blocked phrase must still pass —
  # the guard should only inspect commands whose first token is docker/podman.
  local ec
  _run_guard 'git commit -m "document: docker exec ... claude -p is forbidden"' >/dev/null 2>&1
  ec=$?
  assert_eq 0 "$ec" "git commit with docker phrase in message must pass"
}

test_allows_docker_ps() {
  local ec
  _run_guard 'docker ps' >/dev/null 2>&1
  ec=$?
  assert_eq 0 "$ec" "plain docker ps must pass"
}

test_allows_docker_exec_non_claude() {
  local ec
  _run_guard 'docker exec some-ctr ls /tmp' >/dev/null 2>&1
  ec=$?
  assert_eq 0 "$ec" "docker exec that does not run claude -p must pass"
}

test_allows_empty_command() {
  local ec
  echo '{"tool_input":{}}' | bash "$GUARD" >/dev/null 2>&1
  ec=$?
  assert_eq 0 "$ec" "empty tool_input.command must pass"
}
