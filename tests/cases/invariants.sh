#!/bin/bash
# System-level invariants — properties that must hold across the whole repo,
# independent of any single hook/script scenario.

test_no_orphan_rules_files() {
  # Every .claude/rules/*.md that duplicates the Behavioral Foundation must
  # be deleted; it causes split-source-of-truth with CLAUDE.md §1.
  # Scoped to ROOT and projects/b (A has no rules/).
  for bc in "$ROOT_DIR/.claude/rules/behavioral-core.md" \
            "$ROOT_DIR/projects/b/.claude/rules/behavioral-core.md"; do
    assert_file_absent "$bc" "Orphan duplicate of CLAUDE.md §1 Behavioral Foundation"
  done
}

test_claude_md_imports_resolve() {
  # Every `@path` line in CLAUDE.md must point to an existing file.
  local claude_md="$ROOT_DIR/CLAUDE.md"
  assert_file_exists "$claude_md"
  while read -r path; do
    [ -z "$path" ] && continue
    assert_file_exists "$ROOT_DIR/$path" "@import target missing in CLAUDE.md"
  done < <(grep -oE '^@[[:graph:]]+' "$claude_md" | sed 's/^@//')
}

test_settings_json_hook_paths_exist() {
  # Every command path referenced by ROOT settings.json hooks must exist.
  local settings="$ROOT_DIR/.claude/settings.json"
  assert_file_exists "$settings"
  while read -r path; do
    [ -z "$path" ] && continue
    # Settings use $CLAUDE_PROJECT_DIR; substitute ROOT_DIR for resolution.
    local resolved="${path/\$CLAUDE_PROJECT_DIR/$ROOT_DIR}"
    assert_file_exists "$resolved" "settings.json hook path missing"
  done < <(jq -r '[.hooks[][].hooks[]?.command // empty] | .[]' "$settings" \
           | grep -oE '"[^"]*\.sh"|[^ ]*\.sh' | tr -d '"' | sort -u)
}

test_ab_paper_leak_guards_identical() {
  # A and B ship the same paper-leak-guard.sh byte-for-byte. Asymmetry is a
  # security hole — one side could allow a keyword the other rejects.
  local a="$ROOT_DIR/projects/a/.claude/hooks/paper-leak-guard.sh"
  local b="$ROOT_DIR/projects/b/.claude/hooks/paper-leak-guard.sh"
  assert_file_exists "$a"
  assert_file_exists "$b"
  if ! diff -q "$a" "$b" >/dev/null 2>&1; then
    _fail "paper-leak-guard.sh differs between A and B"
  fi
}

test_ab_web_block_guards_identical() {
  local a="$ROOT_DIR/projects/a/.claude/hooks/web-block.sh"
  local b="$ROOT_DIR/projects/b/.claude/hooks/web-block.sh"
  assert_file_exists "$a"
  assert_file_exists "$b"
  if ! diff -q "$a" "$b" >/dev/null 2>&1; then
    _fail "web-block.sh differs between A and B"
  fi
}

test_frozen_markers_present_for_sub_projects() {
  # Both sub-projects are expected to carry .frozen between cycles (per §6.3).
  assert_file_exists "$ROOT_DIR/projects/a/.frozen" "A must remain frozen across cycles"
  assert_file_exists "$ROOT_DIR/projects/b/.frozen" "B expected frozen outside of improvement commits"
}

test_all_hooks_are_executable_shell() {
  # Every hook script must have a shebang line (portable across shells).
  for sh in "$ROOT_DIR/.claude/hooks"/*.sh \
            "$ROOT_DIR/projects/a/.claude/hooks"/*.sh \
            "$ROOT_DIR/projects/b/.claude/hooks"/*.sh; do
    [ -f "$sh" ] || continue
    local first
    first=$(head -1 "$sh")
    assert_contains "$first" "#!/" "Hook missing shebang: $sh"
  done
}
