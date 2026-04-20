#!/bin/bash
# =============================================================================
# paper-leak-audit.sh — scan an ARGUMENT.md for paper-identifying keywords
# =============================================================================
# ROOT-only utility. The sub-agents A and B are asked to solve the cycle task
# from first principles; they must never have acquired the source paper. If
# any paper-identifying keyword appears in the deliverable, we treat the cycle
# as void (per docs/research/eml-paper/judgment-rubric.md — Disqualification).
#
# Usage:
#   scripts/meta/paper-leak-audit.sh <path/to/ARGUMENT.md>
#
# Exit codes:
#   0  — pass (no leak detected)
#   1  — leak detected (details on stdout)
#   2  — usage error (file not found, etc.)
#
# This file lives under scripts/meta/ on the ROOT repo only — it is not
# mounted into the A or B container, so literal keywords are acceptable here.
# The in-container guard that A/B carry is under projects/<x>/.claude/hooks/
# and uses obfuscated patterns to satisfy the "no keyword inside a container
# filesystem" constraint.
# =============================================================================

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <path/to/ARGUMENT.md>" >&2
  exit 2
fi

TARGET="$1"
if [ ! -f "$TARGET" ]; then
  echo "ERROR: file not found: $TARGET" >&2
  exit 2
fi

# Paper-identifying keywords.  Case-insensitive.  These were picked to cover
# the operator nickname, the author's surname, the Sheffer-continuous framing,
# and the arXiv identifier.  The rubric also flags the bare operator body
# "exp(x) - ln(y)" appearing in an argument's motivation section, but that
# check is judgment-based and not mechanical.
PATTERNS=(
  'eml'
  'Odrzywolek'
  'Sheffer'
  '2603\.21852'
)

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

HITS=0
for pat in "${PATTERNS[@]}"; do
  # -w → whole word match; -i → case-insensitive.
  # For regex "2603\.21852", -w is harmless (digits count as word chars) and
  # keeps the match intent clean.
  if matches=$(grep -Iwni -E "$pat" "$TARGET" 2>/dev/null); then
    echo -e "${RED}LEAK${NC}: pattern '$pat' in $TARGET"
    echo "$matches" | sed 's/^/  /'
    HITS=$((HITS + 1))
  fi
done

if [ "$HITS" -gt 0 ]; then
  echo ""
  echo -e "${RED}Paper-leak audit FAILED:${NC} $HITS pattern(s) matched in $TARGET"
  exit 1
fi

echo -e "${GREEN}Paper-leak audit passed${NC}: $TARGET"
exit 0
