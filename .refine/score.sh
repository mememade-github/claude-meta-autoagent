#!/bin/bash
# =============================================================================
# claude-meta-autoagent ROOT scorer
#
# Validates the complete 2-layer Meta-Evolution system:
# - Security (no information leaks)
# - Structural completeness (all required files)
# - Sync parity (ROOT .claude/ == sub-project .claude/)
# - Sample functionality (app + scorer work)
# - Documentation (README, docs, quickstart)
# - DevContainer (both ROOT and sub-project)
# =============================================================================

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

PASS=0
TOTAL=0
GAPS=()

# --- DR helpers: doc-vs-reality drift detection ---
# Background: a README advertising 13 agents while only 2 existed went undetected
# for ~50 days. These helpers enumerate the real artifacts under .claude/ and the
# names that CLAUDE.md / README.md claim, so the scorer can flag any mismatch.

_drift_list_agents() {
  find "$PROJECT_DIR/.claude/agents" -maxdepth 1 -name '*.md' -printf '%f\n' 2>/dev/null | sed 's/\.md$//' | sort
}
_drift_list_hooks() {
  find "$PROJECT_DIR/.claude/hooks" -maxdepth 1 -name '*.sh' -printf '%f\n' 2>/dev/null | sed 's/\.sh$//' | sort
}
_drift_list_skills() {
  find "$PROJECT_DIR/.claude/skills" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' 2>/dev/null | sort
}

_drift_all_mentioned() {
  local names="$1" file="$2" n
  [ -f "$file" ] || return 1
  [ -n "$names" ] || return 1
  while IFS= read -r n; do
    [ -z "$n" ] && continue
    grep -qF "$n" "$file" || return 1
  done <<< "$names"
  return 0
}

_drift_agents_in_claude_md() { _drift_all_mentioned "$(_drift_list_agents)" "$PROJECT_DIR/CLAUDE.md"; }
_drift_agents_in_readme()    { _drift_all_mentioned "$(_drift_list_agents)" "$PROJECT_DIR/README.md"; }
_drift_hooks_in_readme()     { _drift_all_mentioned "$(_drift_list_hooks)"  "$PROJECT_DIR/README.md"; }
_drift_skills_in_readme()    { _drift_all_mentioned "$(_drift_list_skills)" "$PROJECT_DIR/README.md"; }

# Reverse direction: every name the doc claims must resolve to an artifact on disk.
_drift_claude_md_agents_exist() {
  local claimed n
  claimed=$(grep -E '^\| [a-z][a-z-]+ \|' "$PROJECT_DIR/CLAUDE.md" \
            | awk -F'|' '{gsub(/^ +| +$/,"",$2); print $2}')
  [ -n "$claimed" ] || return 1
  for n in $claimed; do
    [ -f "$PROJECT_DIR/.claude/agents/$n.md" ] || return 1
  done
  return 0
}

# Extract the name list from a README tree line like "│   ├── hooks/a, b, c"
_drift_readme_tree_names() {
  local kind="$1"
  grep -E "^│[^│]*├──[[:space:]]*${kind}/" "$PROJECT_DIR/README.md" \
    | head -1 | sed -E "s|.*${kind}/||; s/,//g; s/\r//g"
}

_drift_readme_hooks_exist() {
  local claimed n
  claimed=$(_drift_readme_tree_names hooks)
  [ -n "$claimed" ] || return 1
  for n in $claimed; do
    [ -f "$PROJECT_DIR/.claude/hooks/$n.sh" ] || return 1
  done
  return 0
}

_drift_readme_skills_exist() {
  local claimed n
  claimed=$(_drift_readme_tree_names skills)
  [ -n "$claimed" ] || return 1
  for n in $claimed; do
    [ -d "$PROJECT_DIR/.claude/skills/$n" ] || return 1
  done
  return 0
}

_drift_readme_agents_exist() {
  local claimed line n
  # README line 154 format: "│   ├── agents/evaluator.md, wip-manager.md"
  line=$(grep -E "^│[^│]*├──[[:space:]]*agents/" "$PROJECT_DIR/README.md" | head -1)
  [ -n "$line" ] || return 1
  claimed=$(echo "$line" | sed -E 's|.*agents/||; s/,//g; s/\.md//g')
  [ -n "$claimed" ] || return 1
  for n in $claimed; do
    [ -f "$PROJECT_DIR/.claude/agents/$n.md" ] || return 1
  done
  return 0
}

# Count parity: README enumeration length must equal actual artifact count.
_drift_hooks_count_parity() {
  local claimed claimed_n actual_n
  claimed=$(_drift_readme_tree_names hooks)
  [ -n "$claimed" ] || return 1
  claimed_n=$(echo $claimed | wc -w)
  actual_n=$(find "$PROJECT_DIR/.claude/hooks" -maxdepth 1 -name '*.sh' 2>/dev/null | wc -l)
  [ "$claimed_n" -eq "$actual_n" ]
}

_drift_skills_count_parity() {
  local claimed claimed_n actual_n
  claimed=$(_drift_readme_tree_names skills)
  [ -n "$claimed" ] || return 1
  claimed_n=$(echo $claimed | wc -w)
  actual_n=$(find "$PROJECT_DIR/.claude/skills" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
  [ "$claimed_n" -eq "$actual_n" ]
}

_drift_agents_count_parity() {
  local claimed claimed_n actual_n line
  line=$(grep -E "^│[^│]*├──[[:space:]]*agents/" "$PROJECT_DIR/README.md" | head -1)
  [ -n "$line" ] || return 1
  claimed=$(echo "$line" | sed -E 's|.*agents/||; s/,//g; s/\.md//g')
  claimed_n=$(echo $claimed | wc -w)
  actual_n=$(find "$PROJECT_DIR/.claude/agents" -maxdepth 1 -name '*.md' 2>/dev/null | wc -l)
  [ "$claimed_n" -eq "$actual_n" ]
}

check() {
  local id="$1"
  local desc="$2"
  shift 2
  TOTAL=$((TOTAL + 1))

  if eval "$@" > /dev/null 2>&1; then
    PASS=$((PASS + 1))
  else
    GAPS+=("$id")
  fi
}

# --- S: Security checks (no information leaks) ---

check "S1" "No MEMEMADE references (except LICENSE, GitHub URL, research)" \
  '! grep -ri "mememade" "$PROJECT_DIR" --include="*" -l 2>/dev/null | grep -v ".git/\|score\.sh\|LICENSE\|README.*\.md\|quickstart\.md\|\.last-push-url\|docs/research/"'

check "S2" "No poc-rag references" \
  '! grep -ri "poc-rag" "$PROJECT_DIR" --include="*" -l 2>/dev/null | grep -v ".git/\|score\.sh\|docs/research/"'

check "S3" "No internal IP addresses" \
  '! grep -ri "1\.234\.53\|172\.10\.100" "$PROJECT_DIR" --include="*" -l 2>/dev/null | grep -v ".git/\|score\.sh"'

check "S4" "No internal hostnames" \
  '! grep -ri "cp001\|50022\|mememade-github" "$PROJECT_DIR" --include="*" -l 2>/dev/null | grep -v ".git/\|score\.sh\|README.*\.md\|quickstart\.md\|\.last-push-url\|docs/research/"'

check "S5" "No DAX references" \
  '! grep -ri "DAX_ROOT\|DAX_LEAF" "$PROJECT_DIR" --include="*" -l 2>/dev/null | grep -v ".git/\|score\.sh"'

check "S6" "No credential files" \
  '[ ! -d "$PROJECT_DIR/.env" ] && [ ! -f "$PROJECT_DIR/.env/git.env" ]'

# --- R: ROOT structure checks ---

check "R1" "ROOT CLAUDE.md exists" \
  '[ -f "$PROJECT_DIR/CLAUDE.md" ]'

check "R2" "ROOT .claude/settings.json" \
  '[ -f "$PROJECT_DIR/.claude/settings.json" ]'

check "R3" "ROOT evaluator agent" \
  '[ -f "$PROJECT_DIR/.claude/agents/evaluator.md" ]'

check "R4" "ROOT wip-manager agent" \
  '[ -f "$PROJECT_DIR/.claude/agents/wip-manager.md" ]'

check "R5" "ROOT /refine skill" \
  '[ -f "$PROJECT_DIR/.claude/skills/refine/SKILL.md" ]'

check "R6" "ROOT pre-commit hook" \
  '[ -f "$PROJECT_DIR/.claude/hooks/pre-commit-gate.sh" ]'

check "R7" "ROOT session-start hook" \
  '[ -f "$PROJECT_DIR/.claude/hooks/session-start.sh" ]'

check "R8" "ROOT Dockerfile" \
  '[ -f "$PROJECT_DIR/.devcontainer/Dockerfile" ]'

check "R9" "ROOT docker-compose.yml" \
  '[ -f "$PROJECT_DIR/.devcontainer/docker-compose.yml" ]'

check "R10" "ROOT entrypoint.sh" \
  '[ -f "$PROJECT_DIR/.devcontainer/entrypoint.sh" ]'

check "R11" "Sync script exists" \
  '[ -f "$PROJECT_DIR/scripts/sync/sync-claude.sh" ]'

check "R12" "Sync script executable" \
  '[ -x "$PROJECT_DIR/scripts/sync/sync-claude.sh" ] || bash "$PROJECT_DIR/scripts/sync/sync-claude.sh" 2>&1 | grep -q "Usage"'

# --- P: Sub-project structure checks ---

check "P1" "Sub-project exists" \
  '[ -d "$PROJECT_DIR/projects/sample-app" ]'

check "P2" "Sub-project CLAUDE.md" \
  '[ -f "$PROJECT_DIR/projects/sample-app/CLAUDE.md" ]'

check "P3" "Sub-project .claude/ exists" \
  '[ -d "$PROJECT_DIR/projects/sample-app/.claude" ]'

check "P4" "Sub-project Dockerfile" \
  '[ -f "$PROJECT_DIR/projects/sample-app/.devcontainer/Dockerfile" ]'

check "P5" "Sub-project docker-compose.yml" \
  '[ -f "$PROJECT_DIR/projects/sample-app/.devcontainer/docker-compose.yml" ]'

check "P6" "Sub-project .env.example" \
  '[ -f "$PROJECT_DIR/projects/sample-app/.devcontainer/.env.example" ]'

check "P7" "Sub-project container name is sample-app" \
  'grep -q "CONTAINER_NAME=sample-app" "$PROJECT_DIR/projects/sample-app/.devcontainer/.env.example"'

check "P8" "Sub-project ports differ from ROOT" \
  'grep -q "PORT_APP=4000" "$PROJECT_DIR/projects/sample-app/.devcontainer/.env.example"'

check "P9" "Sub-project scorer exists" \
  '[ -f "$PROJECT_DIR/projects/sample-app/.refine/score.sh" ]'

check "P10" "Sub-project app exists" \
  '[ -f "$PROJECT_DIR/projects/sample-app/moltbook.py" ]'

# --- Y: Sync parity checks ---

check "Y1" "Sync: evaluator.md matches" \
  'diff -q "$PROJECT_DIR/.claude/agents/evaluator.md" "$PROJECT_DIR/projects/sample-app/.claude/agents/evaluator.md"'

check "Y2" "Sync: settings.json matches" \
  'diff -q "$PROJECT_DIR/.claude/settings.json" "$PROJECT_DIR/projects/sample-app/.claude/settings.json"'

check "Y3" "Sync: refine SKILL.md matches" \
  'diff -q "$PROJECT_DIR/.claude/skills/refine/SKILL.md" "$PROJECT_DIR/projects/sample-app/.claude/skills/refine/SKILL.md"'

check "Y4" "Sync: pre-commit-gate matches" \
  'diff -q "$PROJECT_DIR/.claude/hooks/pre-commit-gate.sh" "$PROJECT_DIR/projects/sample-app/.claude/hooks/pre-commit-gate.sh"'

check "Y5" "Sync: all hooks match" \
  'diff -rq "$PROJECT_DIR/.claude/hooks/" "$PROJECT_DIR/projects/sample-app/.claude/hooks/"'

# --- F: Functional checks ---

check "F1" "Sample app runs" \
  'python3 "$PROJECT_DIR/projects/sample-app/moltbook.py" status'

check "F2" "Sample tests pass" \
  'python3 "$PROJECT_DIR/projects/sample-app/test_moltbook.py"'

check "F3" "Sample scorer runs" \
  'bash "$PROJECT_DIR/projects/sample-app/.refine/score.sh" 2>&1 | grep -q "SCORE:"'

# --- D: Documentation checks ---

check "D1" "README.md exists" \
  '[ -f "$PROJECT_DIR/README.md" ]'

check "D2" "README mentions autoresearch" \
  'grep -q "autoresearch" "$PROJECT_DIR/README.md"'

check "D3" "README has quick start" \
  'grep -qi "quick start" "$PROJECT_DIR/README.md"'

check "D4" "README has 2-layer architecture" \
  'grep -q "2-layer\|2-Layer\|ROOT.*Sub-project\|Meta-Evolution" "$PROJECT_DIR/README.md"'

check "D5" "docs/cross-run-learning.md exists" \
  '[ -f "$PROJECT_DIR/docs/cross-run-learning.md" ]'

check "D6" "docs/meta-evolution.md exists" \
  '[ -f "$PROJECT_DIR/docs/meta-evolution.md" ]'

check "D7" "docs/quickstart.md exists" \
  '[ -f "$PROJECT_DIR/docs/quickstart.md" ]'

check "D8" "LICENSE exists" \
  '[ -f "$PROJECT_DIR/LICENSE" ]'

# --- Q: Content quality checks ---

check "Q1" "README has comparison table with autoresearch" \
  'grep -q "autoresearch.*claude-meta-autoagent\|claude-meta-autoagent.*autoresearch" "$PROJECT_DIR/README.md"'

check "Q2" "README Level 3 shows docker exec command" \
  'grep -q "docker exec.*sample-app" "$PROJECT_DIR/README.md"'

check "Q3" "README shows sync command" \
  'grep -q "sync-claude" "$PROJECT_DIR/README.md"'

check "Q4" "CLAUDE.md has Meta-Evolution section" \
  'grep -q "Meta-Evolution" "$PROJECT_DIR/CLAUDE.md"'

check "Q5" "CLAUDE.md has learning mechanism section" \
  'grep -q "cross-run learning\|3-loop" "$PROJECT_DIR/CLAUDE.md"'

check "Q6" "Sub-project CLAUDE.md does NOT have Meta-Evolution" \
  '! grep -q "Meta-Evolution" "$PROJECT_DIR/projects/sample-app/CLAUDE.md"'

check "Q7" "quickstart.md has Level 1/2/3 scenarios" \
  'grep -q "Level 1" "$PROJECT_DIR/docs/quickstart.md" && grep -q "Level 2" "$PROJECT_DIR/docs/quickstart.md" && grep -q "Level 3" "$PROJECT_DIR/docs/quickstart.md"'

check "Q8" "cross-run-learning.md explains all 3 loops" \
  'grep -q "Reflexion" "$PROJECT_DIR/docs/cross-run-learning.md" && grep -q "Skill Library" "$PROJECT_DIR/docs/cross-run-learning.md" && grep -q "Scorer Evolution" "$PROJECT_DIR/docs/cross-run-learning.md"'

check "Q9" "meta-evolution.md has ROOT and Sub-project" \
  'grep -q "ROOT" "$PROJECT_DIR/docs/meta-evolution.md" && grep -q "Sub-project" "$PROJECT_DIR/docs/meta-evolution.md"'

check "Q10" "Sync script validates source and target" \
  'grep -q "ERROR.*ROOT.*not found" "$PROJECT_DIR/scripts/sync/sync-claude.sh" && grep -q "ERROR.*Target.*not found" "$PROJECT_DIR/scripts/sync/sync-claude.sh"'

check "Q11" "Sync script produces verification output" \
  'bash "$PROJECT_DIR/scripts/sync/sync-claude.sh" "$PROJECT_DIR/projects/sample-app" 2>&1 | grep -q "All portable files match"'

check "Q12" "ROOT Dockerfile installs Claude Code" \
  'grep -q "claude.ai/install.sh" "$PROJECT_DIR/.devcontainer/Dockerfile"'

check "Q13" "ROOT Dockerfile installs Serena MCP" \
  'grep -q "serena" "$PROJECT_DIR/.devcontainer/Dockerfile"'

check "Q14" "Sub-project Dockerfile same as ROOT" \
  'diff -q "$PROJECT_DIR/.devcontainer/Dockerfile" "$PROJECT_DIR/projects/sample-app/.devcontainer/Dockerfile"'

check "Q15" "Sample scorer has functional checks" \
  'grep -q "Functional\|functional\|F[0-9]" "$PROJECT_DIR/projects/sample-app/.refine/score.sh"'

check "Q16" "Sample scorer has error handling checks" \
  'grep -q "Error\|error\|E[0-9]" "$PROJECT_DIR/projects/sample-app/.refine/score.sh"'

check "Q17" "README has requirements section" \
  'grep -qi "requirements\|Requirements" "$PROJECT_DIR/README.md"'

check "Q18" "README mentions Claude Code CLI requirement" \
  'grep -q "Claude Code" "$PROJECT_DIR/README.md"'

# --- W: Wiki capability checks ---

check "W1" "Wiki skill exists" \
  '[ -f "$PROJECT_DIR/.claude/skills/wiki/SKILL.md" ]'

check "W2" "Wiki skill defines init operation" \
  'grep -q "/wiki init" "$PROJECT_DIR/.claude/skills/wiki/SKILL.md"'

check "W3" "Wiki skill defines ingest operation" \
  'grep -q "/wiki ingest" "$PROJECT_DIR/.claude/skills/wiki/SKILL.md"'

check "W4" "Wiki skill defines query operation" \
  'grep -q "/wiki query" "$PROJECT_DIR/.claude/skills/wiki/SKILL.md"'

check "W5" "Wiki skill defines lint operation" \
  'grep -q "/wiki lint" "$PROJECT_DIR/.claude/skills/wiki/SKILL.md"'

check "Y6" "Sync: wiki SKILL.md matches" \
  'diff -q "$PROJECT_DIR/.claude/skills/wiki/SKILL.md" "$PROJECT_DIR/projects/sample-app/.claude/skills/wiki/SKILL.md"'

# --- DR: Drift detection (CLAUDE.md/README.md claims vs .claude/ reality) ---
# Fails whenever an artifact under .claude/ is not documented, or any documented
# name has no corresponding file. Catches the stale-advertisement drift that
# otherwise accumulates silently between sync/edit cycles.

check "DR1" "Every .claude/agents/*.md is mentioned in CLAUDE.md" \
  '_drift_agents_in_claude_md'

check "DR2" "Every .claude/agents/*.md is mentioned in README.md" \
  '_drift_agents_in_readme'

check "DR3" "Every .claude/hooks/*.sh is mentioned in README.md" \
  '_drift_hooks_in_readme'

check "DR4" "Every .claude/skills/*/ is mentioned in README.md" \
  '_drift_skills_in_readme'

check "DR5" "Every agent in CLAUDE.md §5 table exists as .md file" \
  '_drift_claude_md_agents_exist'

check "DR6" "Every agent listed in README tree exists as .md file" \
  '_drift_readme_agents_exist'

check "DR7" "Every hook listed in README tree exists as .sh file" \
  '_drift_readme_hooks_exist'

check "DR8" "Every skill listed in README tree exists as dir" \
  '_drift_readme_skills_exist'

check "DR9" "README agents enumeration count == actual .md count" \
  '_drift_agents_count_parity'

check "DR10" "README hooks enumeration count == actual .sh count" \
  '_drift_hooks_count_parity'

check "DR11" "README skills enumeration count == actual dir count" \
  '_drift_skills_count_parity'

# --- Output ---

if [ "$TOTAL" -eq 0 ]; then
  echo "SCORE: 0.00"
  echo "GAPS: [NO_CHECKS]"
  exit 1
fi

SCORE=$(echo "$PASS $TOTAL" | awk '{printf "%.2f", $1/$2}')
if [ ${#GAPS[@]} -eq 0 ]; then
  echo "SCORE: $SCORE"
  echo "GAPS: []"
else
  GAP_STR=$(printf ", %s" "${GAPS[@]}")
  echo "SCORE: $SCORE"
  echo "GAPS: [${GAP_STR:2}]"
fi
