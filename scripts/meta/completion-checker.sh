#!/bin/bash
# =============================================================================
# completion-checker.sh — Pre-Commit Verification
# =============================================================================
# Purpose: Verify code quality, synchronization, and standards before commit.
# Usage:   bash scripts/meta/completion-checker.sh [legacy_pattern]
#
# Checks:
#   1. Repository status    — auto-discovered git repos (uncommitted, unpushed)
#   2. Legacy references    — deprecated symbol grep (optional, pass as $1)
#   3. WIP status           — active wip/task-* directories
#   4. Dead code (vulture)  — Python projects with .vulture-expected config
#   5. Portability (.claude) — hardcoded project values in portable artifacts
#
# Configuration:
#   - Dead code: place .vulture-expected in each Python project root
#     containing the expected false positive count (single integer).
#   - Portability: scripts/meta/portability-check.sh (called as subprocess)
#
# Connects to:
#   - pre-commit-gate.sh reads .claude/.last-verification marker
# =============================================================================

set -e

# --- Root detection (worktree-aware) ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

detect_root() {
    # Priority: CLAUDE_PROJECT_DIR > git common dir (worktree) > git toplevel > script relative
    if [ -n "${CLAUDE_PROJECT_DIR:-}" ] && [ -d "$CLAUDE_PROJECT_DIR" ]; then
        echo "$CLAUDE_PROJECT_DIR"
        return
    fi
    if command -v git &>/dev/null; then
        local git_common
        git_common=$(git -C "$SCRIPT_DIR" rev-parse --git-common-dir 2>/dev/null || true)
        if [ -n "$git_common" ] && [ "$git_common" != ".git" ]; then
            # Worktree detected — git-common-dir may be relative, resolve to absolute
            (cd "$SCRIPT_DIR" && cd "$(dirname "$git_common")" && pwd)
            return
        fi
        local toplevel
        toplevel=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || true)
        if [ -n "$toplevel" ]; then
            echo "$toplevel"
            return
        fi
    fi
    # Fallback: script is at scripts/meta/, root is 2 levels up
    (cd "$SCRIPT_DIR/../.." && pwd)
}

ROOT_DIR="$(detect_root)"
LEGACY_PATTERN="${1:-}"

# --- UI ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

PASS=0; WARN=0; FAIL=0

log_header()  { echo -e "\n${BOLD}${BLUE}═══════════════════════════════════════════════════════════════${NC}"; echo -e "${BOLD}${BLUE}  $1${NC}"; echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════════════════${NC}"; }
log_section() { echo -e "\n${BOLD}─── $1 ───${NC}"; }
log_pass()    { echo -e "${GREEN}[PASS]${NC} $1"; ((PASS++)) || true; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; ((WARN++)) || true; }
log_fail()    { echo -e "${RED}[FAIL]${NC} $1"; ((FAIL++)) || true; }

# =============================================================================
# 1. Repository Status (auto-discovered)
# =============================================================================
check_repo_status() {
    local repo_path="$1"
    local repo_name="$2"

    if [ ! -d "$repo_path/.git" ] && [ ! -f "$repo_path/.git" ]; then
        log_warn "$repo_name: Not a git repository"
        return
    fi

    local status
    status=$(git -C "$repo_path" status --porcelain 2>/dev/null)
    if [ -n "$status" ]; then
        log_warn "$repo_name: Uncommitted changes detected"
        echo "$status" | head -5 | sed 's/^/         /'
    else
        log_pass "$repo_name: Clean working tree"
    fi

    local ahead
    ahead=$(git -C "$repo_path" rev-list --count @{u}..HEAD 2>/dev/null || echo "0")
    if [ "$ahead" -gt 0 ]; then
        log_warn "$repo_name: $ahead commits not pushed"
    fi
}

discover_and_check_repos() {
    log_section "Repository Status"

    # Always check root repo
    check_repo_status "$ROOT_DIR" "Root"

    # Auto-discover git repos under products/
    for tier in root derived; do
        local tier_dir="$ROOT_DIR/products/$tier"
        [ -d "$tier_dir" ] || continue
        for repo_dir in "$tier_dir"/*/; do
            [ -d "$repo_dir" ] || continue
            # Check if it's a git repo (either .git dir or .git file for worktrees)
            if [ -d "$repo_dir/.git" ] || [ -f "$repo_dir/.git" ]; then
                local name
                name=$(basename "$repo_dir")
                check_repo_status "$repo_dir" "$tier/$name"
            fi
        done
    done
}

# =============================================================================
# 2. Legacy References (optional, grep-based)
# =============================================================================
check_legacy_references() {
    if [ -z "$LEGACY_PATTERN" ]; then
        return
    fi

    log_section "Legacy Reference Check (pattern: $LEGACY_PATTERN)"

    local total_found=0
    IFS='|' read -ra SYMBOLS <<< "$LEGACY_PATTERN"

    local search_dirs=()
    [ -d "$ROOT_DIR/products" ] && search_dirs+=("$ROOT_DIR/products/")
    [ -d "$ROOT_DIR/scripts" ] && search_dirs+=("$ROOT_DIR/scripts/")

    if [ ${#search_dirs[@]} -eq 0 ]; then
        log_warn "No products/ or scripts/ directories to search"
        return
    fi

    for symbol in "${SYMBOLS[@]}"; do
        symbol=$(echo "$symbol" | xargs)
        local found
        found=$(grep -rn "$symbol" "${search_dirs[@]}" \
            --include="*.py" --include="*.yaml" --include="*.yml" \
            --include="*.env" --include="*.md" --include="*.sh" --include="*.json" \
            2>/dev/null | grep -v "__pycache__" | grep -v ".venv" || true)

        if [ -n "$found" ]; then
            local count
            count=$(echo "$found" | wc -l)
            log_warn "Found $count match(es) to '$symbol'"
            echo "$found" | head -5 | sed 's/^/         /'
            [ "$count" -gt 5 ] && echo "         ... and $((count - 5)) more"
            total_found=$((total_found + count))
        else
            log_pass "No matches to '$symbol'"
        fi
    done

    [ "$total_found" -gt 0 ] && log_warn "Total legacy references: $total_found (review manually)"
}

# =============================================================================
# 3. WIP Directory
# =============================================================================
check_wip_status() {
    log_section "WIP Directory Check"

    local wip_tasks
    wip_tasks=$(find "$ROOT_DIR/wip" -maxdepth 1 -type d -name "task-*" 2>/dev/null || true)

    if [ -n "$wip_tasks" ]; then
        log_warn "Active WIP tasks found:"
        echo "$wip_tasks" | sed 's/^/         /'
    else
        log_pass "No active WIP tasks"
    fi
}

# =============================================================================
# 4. Dead Code (vulture, config-driven)
#
# Each Python project can place a .vulture-expected file in its root:
#   - Single integer = expected false positive count
#   - Lines starting with # are comments
#   - If file absent, vulture check is skipped for that project
# =============================================================================
check_dead_code() {
    log_section "Dead Code Check (vulture)"

    if ! command -v vulture &>/dev/null; then
        log_warn "vulture not installed — skipping dead code check"
        return
    fi

    local checked=0

    # Scan products/ for Python projects with .vulture-expected
    for tier in root derived; do
        local tier_dir="$ROOT_DIR/products/$tier"
        [ -d "$tier_dir" ] || continue
        for project_dir in "$tier_dir"/*/; do
            [ -d "$project_dir" ] || continue
            local config="$project_dir/.vulture-expected"
            [ -f "$config" ] || continue
            [ -d "$project_dir/src" ] || continue

            local name
            name=$(basename "$project_dir")
            local expected
            expected=$(grep -v '^#' "$config" | grep -v '^$' | head -1 | xargs)

            if ! [[ "$expected" =~ ^[0-9]+$ ]]; then
                log_warn "$name: Invalid .vulture-expected (not an integer: '$expected')"
                continue
            fi

            local output count
            output=$(cd "$project_dir" && vulture src/ --min-confidence 60 --exclude .venv,__pycache__ 2>&1 || true)
            count=0
            if [ -n "$output" ]; then
                count=$(echo "$output" | grep -c "unused" 2>/dev/null || echo "0")
            fi

            if [ "$count" -gt "$expected" ]; then
                local new_count=$((count - expected))
                log_fail "$name: $new_count NEW dead code item(s) (total: $count, expected: $expected)"
                echo "$output" | tail -"$new_count" | sed 's/^/         /'
            elif [ "$count" -lt "$expected" ]; then
                log_pass "$name: $count items (expected: $expected — update .vulture-expected)"
            else
                log_pass "$name: $count items (all verified false positives)"
            fi
            checked=$((checked + 1))
        done
    done

    if [ "$checked" -eq 0 ]; then
        log_pass "No projects with .vulture-expected config — skipped"
    fi
}

# =============================================================================
# 5. Portability (.claude/ artifacts)
# =============================================================================
check_portability() {
    log_section "Portability Check (.claude/)"

    local script="$ROOT_DIR/scripts/meta/portability-check.sh"
    if [ ! -f "$script" ]; then
        log_warn "portability-check.sh not found — skipping"
        return
    fi

    local output
    output=$(bash "$script" "$ROOT_DIR" 2>&1)
    local exit_code=$?

    if [ $exit_code -eq 0 ]; then
        log_pass "No hardcoded project references in portable .claude/ artifacts"
    else
        log_fail "Portability violations in .claude/ artifacts"
        echo "$output" | grep -E "VIOLATION|Pattern:" | sed 's/^/         /'
    fi
}

# =============================================================================
# Verification marker (connects to pre-commit-gate.sh)
# =============================================================================
create_verification_marker() {
    # Resolve actual root for worktree compatibility
    local marker_root="$ROOT_DIR"
    if command -v git &>/dev/null; then
        local git_common
        git_common=$(git -C "$ROOT_DIR" rev-parse --git-common-dir 2>/dev/null || true)
        if [ -n "$git_common" ] && [ "$git_common" != ".git" ]; then
            marker_root=$(dirname "$git_common")
        fi
    fi
    # Append branch name for per-worktree isolation (matches pre-commit-gate.sh)
    local branch
    branch=$(git -C "$ROOT_DIR" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    local branch_safe
    branch_safe=$(echo "$branch" | tr '/' '-')
    local marker="$marker_root/.claude/.last-verification.$branch_safe"
    mkdir -p "$(dirname "$marker")"
    touch "$marker"
    echo -e "  ${GREEN}Verification marker created ($(date))${NC}"
}

# =============================================================================
# Summary
# =============================================================================
show_summary() {
    log_header "Completion Check Summary"

    echo -e "  Root: $ROOT_DIR"
    echo -e "  Timestamp: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
    echo ""
    printf "  ${GREEN}PASS${NC}: %d\n" "$PASS"
    printf "  ${YELLOW}WARN${NC}: %d\n" "$WARN"
    printf "  ${RED}FAIL${NC}: %d\n" "$FAIL"
    echo ""

    if [ "$FAIL" -gt 0 ]; then
        echo -e "  ${RED}${BOLD}Result: NOT READY${NC}"
        echo -e "  ${RED}Fix FAIL items before commit${NC}"
        return 1
    elif [ "$WARN" -gt 0 ]; then
        echo -e "  ${YELLOW}${BOLD}Result: REVIEW WARNINGS${NC}"
        create_verification_marker
        return 0
    else
        echo -e "  ${GREEN}${BOLD}Result: READY${NC}"
        create_verification_marker
        return 0
    fi
}

# =============================================================================
# Main
# =============================================================================
main() {
    log_header "Pre-Commit Verification"
    echo "  Root: $ROOT_DIR"
    echo ""

    discover_and_check_repos
    check_legacy_references
    check_wip_status
    check_dead_code
    check_portability

    show_summary
}

main "$@"
