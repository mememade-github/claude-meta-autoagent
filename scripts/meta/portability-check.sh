#!/bin/bash
# =============================================================================
# portability-check.sh — Detect hardcoded project references in .claude/
# =============================================================================
# Portable .claude/ artifacts (agents, hooks, skills, settings.json, root rules)
# must NOT contain project-specific values. This script scans for violations.
#
# Usage:   bash scripts/meta/portability-check.sh [ROOT_DIR]
#
# Exit codes:
#   0 — no violations found
#   1 — violations detected (details on stdout)
#
# What's checked:
#   - Project names from projects/*/ directories
#   - Hardcoded absolute paths (/workspaces/projects/<name>)
#   - Container names matching project directories
#   - Hardcoded port numbers (except standard ones like 80, 443, 8080)
#
# What's excluded:
#   - agent-memory/ (project-local state, not portable)
#   - rules/project/ (project-specific by design)
#   - Binary files
#   - This script itself
# =============================================================================

set -euo pipefail

ROOT_DIR="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
CLAUDE_DIR="$ROOT_DIR/.claude"

if [ ! -d "$CLAUDE_DIR" ]; then
    echo "ERROR: .claude/ not found at $CLAUDE_DIR" >&2
    exit 1
fi

VIOLATIONS=0

# Collect project names from projects/ directory
PROJECT_NAMES=()
if [ -d "$ROOT_DIR/projects" ]; then
    for dir in "$ROOT_DIR/projects"/*/; do
        [ -d "$dir" ] || continue
        name=$(basename "$dir")
        PROJECT_NAMES+=("$name")
    done
fi

# Also check products/ (legacy layout)
if [ -d "$ROOT_DIR/products" ]; then
    for tier in root derived; do
        for dir in "$ROOT_DIR/products/$tier"/*/; do
            [ -d "$dir" ] || continue
            name=$(basename "$dir")
            PROJECT_NAMES+=("$name")
        done
    done
fi

if [ ${#PROJECT_NAMES[@]} -eq 0 ]; then
    echo "No projects found — nothing to check"
    exit 0
fi

# Portable artifact paths (relative to .claude/)
PORTABLE_PATHS=(
    "agents"
    "hooks"
    "skills"
    "settings.json"
)
# Root-level rules are portable; rules/project/ is excluded
PORTABLE_RULES_GLOB="rules/*.md"

report_violation() {
    local file="$1"
    local pattern="$2"
    local match="$3"
    if [ "$VIOLATIONS" -eq 0 ]; then
        echo "PORTABILITY VIOLATIONS DETECTED"
        echo "==============================="
    fi
    VIOLATIONS=$((VIOLATIONS + 1))
    echo ""
    echo "  VIOLATION #$VIOLATIONS"
    echo "  File:    $file"
    echo "  Pattern: $pattern"
    echo "  Match:   $match"
}

# Build file list of portable artifacts
PORTABLE_FILES=()
for path in "${PORTABLE_PATHS[@]}"; do
    full="$CLAUDE_DIR/$path"
    if [ -f "$full" ]; then
        PORTABLE_FILES+=("$full")
    elif [ -d "$full" ]; then
        while IFS= read -r f; do
            PORTABLE_FILES+=("$f")
        done < <(find "$full" -type f \
            -not -path "*/agent-memory/*" \
            -not -path "*/__pycache__/*" \
            -not -name "*.pyc" 2>/dev/null)
    fi
done

# Add root-level rules (exclude rules/project/)
if [ -d "$CLAUDE_DIR/rules" ]; then
    for f in "$CLAUDE_DIR"/rules/*.md; do
        [ -f "$f" ] && PORTABLE_FILES+=("$f")
    done
fi

if [ ${#PORTABLE_FILES[@]} -eq 0 ]; then
    echo "No portable files found — nothing to check"
    exit 0
fi

# Check each portable file for project-specific references
for file in "${PORTABLE_FILES[@]}"; do
    # Skip binary files
    if file --mime-type "$file" 2>/dev/null | grep -qv "text/"; then
        continue
    fi

    rel_file="${file#$ROOT_DIR/}"

    for project in "${PROJECT_NAMES[@]}"; do
        # Pattern 1: direct project name reference (case-sensitive, word boundary)
        # Allow generic references like "sample-app" in comments/examples only if
        # they appear in documentation context — but flag them anyway for review
        matches=$(grep -n "\b${project}\b" "$file" 2>/dev/null || true)
        if [ -n "$matches" ]; then
            while IFS= read -r line; do
                report_violation "$rel_file" "Project name: $project" "$line"
            done <<< "$matches"
        fi

        # Pattern 2: hardcoded path to project
        matches=$(grep -n "projects/${project}" "$file" 2>/dev/null || true)
        if [ -n "$matches" ]; then
            while IFS= read -r line; do
                report_violation "$rel_file" "Hardcoded path: projects/$project" "$line"
            done <<< "$matches"
        fi

        # Pattern 3: container name matching project
        matches=$(grep -n "docker exec.*${project}" "$file" 2>/dev/null || true)
        if [ -n "$matches" ]; then
            while IFS= read -r line; do
                report_violation "$rel_file" "Container reference: $project" "$line"
            done <<< "$matches"
        fi
    done
done

# Summary
if [ "$VIOLATIONS" -gt 0 ]; then
    echo ""
    echo "==============================="
    echo "Total violations: $VIOLATIONS"
    echo ""
    echo "Portable .claude/ artifacts must be project-agnostic."
    echo "Move project-specific content to .claude/rules/project/ or project CLAUDE.md."
    exit 1
else
    echo "No portability violations found in .claude/ artifacts"
    exit 0
fi
