#!/bin/bash
# =============================================================================
# delegate-sub.sh — ROOT-internal A/B agent launcher with paper-leak pre-filter
# =============================================================================
# ROOT uses this wrapper to start a Level-3a (A) or Level-3b (B) sub-agent
# during a cycle.  In addition to the generic GOAL-not-METHOD check that
# delegate-goal.sh performs, this script rejects any GOAL whose text already
# mentions paper-identifying keywords (rubric disqualification trigger).  A
# and B must reason from first principles; the ROOT prompt itself is the
# last place before the container boundary where a leak could still be
# introduced on purpose or by accident.
#
# Usage:
#   scripts/meta/delegate-sub.sh <a|b> "<GOAL>"
#   EFFORT=high scripts/meta/delegate-sub.sh a "<GOAL>"
#
# Exit codes:
#   0  — launched
#   1  — usage or validation error
#   2  — paper-leak pre-filter tripped
#
# Reference: CLAUDE.md §6 (paper-knowledge isolation),
#            docs/research/eml-paper/judgment-rubric.md (Disqualification).
#
# Literal paper keywords are acceptable in this file because scripts/meta/
# lives on the ROOT filesystem only; it is not mounted into the A or B
# container.
# =============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

die() { echo -e "${RED}ERROR:${NC} $1" >&2; exit 1; }

if [ $# -lt 2 ]; then
  echo "Usage: $0 <a|b> \"<GOAL>\""
  echo ""
  echo "  a — baseline (karpathy-skills only, no .claude/ evolution)"
  echo "  b — evolvable (ROOT-subset, no \u00a76, /refine available)"
  exit 1
fi

SUB_KEY="$1"
GOAL="$2"

case "$SUB_KEY" in
  a|b) ;;
  *)   die "Unknown sub-key '$SUB_KEY'. Must be 'a' or 'b'." ;;
esac

# --- Paper-leak pre-filter on GOAL text --------------------------------------
# Same pattern list as paper-leak-audit.sh.  If the GOAL about to be shipped
# into A or B already contains these words, we refuse to launch.
PATTERNS=(
  'eml'
  'Odrzywolek'
  'Sheffer'
  '2603\.21852'
)

for pat in "${PATTERNS[@]}"; do
  if printf '%s' "$GOAL" | grep -qEi -- "$pat"; then
    echo -e "${RED}BLOCKED:${NC} GOAL contains paper-identifying keyword matching '$pat'." >&2
    echo "" >&2
    echo "The A/B cycle prompt must be derivable-from-first-principles; any keyword leak" >&2
    echo "voids the run per docs/research/eml-paper/judgment-rubric.md." >&2
    exit 2
  fi
done

# --- Delegate to the generic wrapper ----------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GENERIC="$SCRIPT_DIR/delegate-goal.sh"

if [ ! -x "$GENERIC" ] && [ ! -f "$GENERIC" ]; then
  die "delegate-goal.sh not found at $GENERIC"
fi

echo -e "${GREEN}${BOLD}Pre-filter passed${NC} — no paper keywords in GOAL."
echo -e "${YELLOW}Forwarding to delegate-goal.sh${NC} ($SUB_KEY)."

# Forward all behaviour (role-declaration header, effort level, audit log,
# container liveness check, docker exec launch) to delegate-goal.sh.  That
# script already reads EFFORT from the environment.
exec bash "$GENERIC" "$SUB_KEY" "$GOAL"
