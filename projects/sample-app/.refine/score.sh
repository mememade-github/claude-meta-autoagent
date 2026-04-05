#!/bin/bash
# ==========================================================================
# Sample scorer for mdstat — Markdown statistics CLI tool
#
# This scorer demonstrates the /refine scoring pattern.
# It tests functionality, error handling, and edge cases.
#
# Output format (required by /refine):
#   SCORE: 0.XX
#   GAPS: [ID1, ID2, ...]
# ==========================================================================

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

PASS=0
TOTAL=0
GAPS=()

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

# --- F: Functional checks ---

check "F1" "Basic analysis works" \
  'echo "# Hello\n\nWorld" | python3 "$PROJECT_DIR/app.py" -'

check "F2" "JSON output valid" \
  'echo "# Test" | python3 "$PROJECT_DIR/app.py" --json - | python3 -m json.tool'

check "F3" "Word count accurate" \
  'printf "one two three\n" | python3 "$PROJECT_DIR/app.py" --json - | python3 -c "import sys,json; d=json.load(sys.stdin); assert d[\"words\"]==3"'

check "F4" "Heading detection works" \
  'printf "# H1\n## H2\n### H3\n" | python3 "$PROJECT_DIR/app.py" --json - | python3 -c "import sys,json; d=json.load(sys.stdin); assert d[\"headings\"][\"h1\"]==1"'

check "F5" "Code block counting" \
  'printf "\x60\x60\x60\ncode\n\x60\x60\x60\n" | python3 "$PROJECT_DIR/app.py" --json - | python3 -c "import sys,json; d=json.load(sys.stdin); assert d[\"code_blocks\"]==1"'

check "F6" "Link counting" \
  'printf "[a](http://a.com) [b](http://b.com)\n" | python3 "$PROJECT_DIR/app.py" --json - | python3 -c "import sys,json; d=json.load(sys.stdin); assert d[\"links\"]==2"'

check "F7" "Human-readable report format" \
  'printf "# Test\n" | python3 "$PROJECT_DIR/app.py" - | grep -q "Words:"'

# --- E: Error handling checks ---

check "E1" "No args shows usage" \
  'OUT=$(python3 "$PROJECT_DIR/app.py" 2>&1 || true); echo "$OUT" | grep -q -i "usage"'

check "E2" "Exit code non-zero on no args" \
  '! python3 "$PROJECT_DIR/app.py"'

check "E3" "Missing file produces error" \
  '! python3 "$PROJECT_DIR/app.py" /nonexistent/file.md 2>/dev/null'

# --- C: Edge case checks ---

check "C1" "Empty input handled" \
  'echo "" | python3 "$PROJECT_DIR/app.py" --json -'

check "C2" "Large input handled" \
  'python3 -c "print(\"# Title\n\" + \"word \" * 10000)" | python3 "$PROJECT_DIR/app.py" --json -'

# --- G: Gap checks (features the app should have but doesn't yet) ---

check "G1" "Table detection" \
  'printf "| a | b |\n|---|---|\n| 1 | 2 |\n" | python3 "$PROJECT_DIR/app.py" --json - | python3 -c "import sys,json; d=json.load(sys.stdin); assert \"tables\" in d, \"no tables field\""'

check "G2" "Image counting (not confused with links)" \
  'printf "![alt](img.png)\n[text](url)\n" | python3 "$PROJECT_DIR/app.py" --json - | python3 -c "import sys,json; d=json.load(sys.stdin); assert \"images\" in d and d[\"images\"]==1, \"no images field or wrong count\""'

check "G3" "Lists detection" \
  'printf "- item 1\n- item 2\n1. numbered\n" | python3 "$PROJECT_DIR/app.py" --json - | python3 -c "import sys,json; d=json.load(sys.stdin); assert \"lists\" in d, \"no lists field\""'

check "G4" "Blockquote detection" \
  'printf "> quoted text\n> more\n" | python3 "$PROJECT_DIR/app.py" --json - | python3 -c "import sys,json; d=json.load(sys.stdin); assert \"blockquotes\" in d, \"no blockquotes field\""'

check "G5" "Images not counted as links" \
  'printf "![img](pic.png)\n[link](url)\n" | python3 "$PROJECT_DIR/app.py" --json - | python3 -c "import sys,json; d=json.load(sys.stdin); assert d.get(\"links\",0)==1, f\"links should be 1, got {d.get(\"links\")}\""'

# --- T: Test suite checks ---

check "T1" "Unit tests pass" \
  'python3 "$PROJECT_DIR/test_app.py"'

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
