#!/bin/bash
# =============================================================================
# delegate-goal.sh — Role Relativity-enforced Agent Delegation Wrapper
# =============================================================================
# Purpose: Launch a headless Claude agent in a sub-project container with
#          GOAL-not-METHOD validation, role declaration injection, and audit log.
#
# Usage:   scripts/meta/delegate-goal.sh <project-key> "<GOAL>"
#
# The meta-evolution-guard.sh hook blocks direct `docker exec ... claude -p`.
# All delegation MUST use this wrapper.
#
# Reference: CLAUDE.md §6 (Meta-Evolution), Role Relativity, Pre-action gate.
#
# Effort level: Defaults to "medium" (LCD across CLI versions). Override via
# EFFORT env var:  EFFORT=high scripts/meta/delegate-goal.sh sample-app "..."
# Valid values: low, medium, high, max
#
# Opus 4.7+ note: The model follows instructions very literally. GOAL prompts
# must be precise outcome descriptions — vague phrasing may produce narrow
# literal interpretations rather than the intended broad action.
# =============================================================================

set -euo pipefail

# --- Effort level (LCD default: medium) ---
EFFORT_LEVEL="${EFFORT:-medium}"
if ! echo "$EFFORT_LEVEL" | grep -qE '^(low|medium|high|max)$'; then
  echo -e "\033[0;31mERROR:\033[0m Invalid EFFORT='$EFFORT_LEVEL'. Must be: low, medium, high, max" >&2
  exit 1
fi

# --- Project map (extend as needed) ---
# Keys are short identifiers; values are container names.
declare -A PROJECTS=(
  [sample-app]="sample-app"
)

# --- UI ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

die() { echo -e "${RED}ERROR:${NC} $1" >&2; exit 1; }

# --- Args ---
if [ $# -lt 2 ]; then
  echo "Usage: $0 <project-key> \"<GOAL>\""
  echo ""
  echo "Available project keys:"
  for key in "${!PROJECTS[@]}"; do
    echo "  $key  →  ${PROJECTS[$key]}"
  done
  exit 1
fi

PROJECT_KEY="$1"
GOAL="$2"

# --- Pre-action gate: project key ---
CONTAINER="${PROJECTS[$PROJECT_KEY]:-}"
if [ -z "$CONTAINER" ]; then
  die "Unknown project key '$PROJECT_KEY'. Available: ${!PROJECTS[*]}"
fi

# --- Pre-action gate: GOAL-not-METHOD validation ---
# Reject prompts containing slash commands (imperative method injection)
if echo "$GOAL" | grep -qE '(^|[[:space:]])/[a-z]'; then
  die "GOAL contains slash command(s). Role Relativity: provide GOAL, not METHOD.\n  Rejected: $GOAL"
fi

# Reject prompts that are step-by-step recipes (numbered imperative steps)
if echo "$GOAL" | grep -qE '^[[:space:]]*[0-9]+\.[[:space:]]+(Run|Execute|Edit|Create|Delete|Modify|Install|Copy|Move|Push|Pull|Commit)' ; then
  die "GOAL contains imperative step-by-step instructions. Describe the desired OUTCOME, not steps.\n  Rejected: $GOAL"
fi

# Reject empty or trivially short goals
if [ ${#GOAL} -lt 10 ]; then
  die "GOAL too short (${#GOAL} chars). Provide a meaningful outcome description."
fi

# --- Role declaration header (injected into prompt) ---
DECLARATION="You are a sub-project Agent launched by the ROOT Agent.
- Role: Sub-project Agent (${PROJECT_KEY})
- Layer: Execution (owns application code, follows own CLAUDE.md)
- Boundary: Do NOT modify .claude/ portable artifacts or root-level governance files.
- Authority: Full autonomy over METHOD selection within your project scope.

GOAL from ROOT Agent:
"

FULL_PROMPT="${DECLARATION}${GOAL}"

# --- Audit log ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_DIR="$ROOT_DIR/.claude/.delegate-log"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date -u '+%Y%m%d-%H%M%S')
LOG_FILE="$LOG_DIR/${TIMESTAMP}-${PROJECT_KEY}.log"

cat > "$LOG_FILE" <<EOF
timestamp: ${TIMESTAMP}
project_key: ${PROJECT_KEY}
container: ${CONTAINER}
effort: ${EFFORT_LEVEL}
goal: ${GOAL}
status: launching
EOF

echo -e "${GREEN}${BOLD}Delegating to ${PROJECT_KEY}${NC} (container: ${CONTAINER})"
echo -e "  GOAL:   ${GOAL}"
echo -e "  Effort: ${EFFORT_LEVEL}"
echo -e "  Log:    ${LOG_FILE}"

# --- Container liveness check ---
if ! docker inspect "$CONTAINER" --format '{{.State.Running}}' 2>/dev/null | grep -q "true"; then
  echo "status: failed (container not running)" >> "$LOG_FILE"
  die "Container '$CONTAINER' is not running. Start the DevContainer first."
fi

# --- Launch agent (detached) ---
# --effort: LCD default "medium", overridable via EFFORT env var.
# Note: agent.log captures text output only; thinking/reasoning content is
# omitted by the CLI in -p mode (Opus 4.7+ observation constraint).
# Auth: an *empty* ANTHROPIC_API_KEY in the container env forces the CLI onto
# the API-key auth path with an empty secret (→ 401), bypassing the OAuth
# credentials at ~/.claude/.credentials.json. Unset when empty so OAuth wins.
docker exec -d "$CONTAINER" bash -c \
  "[ -z \"\${ANTHROPIC_API_KEY:-}\" ] && unset ANTHROPIC_API_KEY; cd /workspaces && claude --dangerously-skip-permissions --effort $(printf '%q' "$EFFORT_LEVEL") -p $(printf '%q' "$FULL_PROMPT") > /tmp/agent.log 2>&1"

echo "status: launched" >> "$LOG_FILE"
echo -e "${GREEN}Agent launched.${NC} Monitor with:"
echo -e "  docker exec $CONTAINER cat /tmp/agent.log"
