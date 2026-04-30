#!/bin/bash
# =============================================================================
# Claude Code DevContainer — Environment Setup (runs on every container start)
# =============================================================================
# Policies:
#   - Claude CLI auto-updates here (fail-soft) so containers do not drift
#     from the image-build-time pin. Set SKIP_CLAUDE_UPDATE=1 to bypass.
# =============================================================================
set -e

export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

STEP_TOTAL=3
STEP=0
step() { STEP=$((STEP + 1)); echo "[${STEP}/${STEP_TOTAL}] $1"; }

echo "=============================================="
echo "  Claude DevContainer Setup"
echo "=============================================="
echo ""

# =============================================================================
# 1. Docker socket + workspace permissions
# =============================================================================
step "Setting permissions..."

if [ -S /var/run/docker.sock ]; then
    sudo chown root:docker /var/run/docker.sock 2>/dev/null || true
fi

WS="/workspaces"
find "$WS" -maxdepth 3 -name ".git" -type d 2>/dev/null | while read gitdir; do
    repo=$(dirname "$gitdir")
    git -C "$repo" config core.filemode false 2>/dev/null || true
done

# 9p/drvfs: prevent dubious ownership on root:root owned mounts
git config --global safe.directory '*' 2>/dev/null || true

# Command history
if [ -d /commandhistory ]; then
    export HISTFILE=/commandhistory/.bash_history
    touch "$HISTFILE" 2>/dev/null || true
fi
echo "      Done"

# =============================================================================
# 2. SSH (optional)
# =============================================================================
step "SSH setup..."
SSH_DIR="${HOME}/.ssh"
if [ -d "$SSH_DIR" ]; then
    chmod 700 "$SSH_DIR" 2>/dev/null || true
    find "$SSH_DIR" -type f -name "*.pub" -exec chmod 644 {} \; 2>/dev/null || true
    find "$SSH_DIR" -type f -name "known_hosts*" -exec chmod 644 {} \; 2>/dev/null || true
    find "$SSH_DIR" -type f ! -name "*.pub" ! -name "known_hosts*" ! -name "config" -exec chmod 600 {} \; 2>/dev/null || true
    [ -f "$SSH_DIR/config" ] && chmod 644 "$SSH_DIR/config" 2>/dev/null || true
    echo "      SSH keys found"
else
    echo "      No SSH (optional)"
fi

# =============================================================================
# 3. Claude CLI self-update (fail-soft; set SKIP_CLAUDE_UPDATE=1 to bypass)
# =============================================================================
step "Claude CLI update..."
if [ "${SKIP_CLAUDE_UPDATE:-0}" = "1" ]; then
    echo "      Skipped (SKIP_CLAUDE_UPDATE=1)"
elif ! command -v claude &>/dev/null; then
    echo "      WARN: claude CLI not installed — skipping"
else
    before="$(claude --version 2>/dev/null | awk '{print $1}' || echo unknown)"
    if claude update >/dev/null 2>&1; then
        after="$(claude --version 2>/dev/null | awk '{print $1}' || echo unknown)"
        if [ "$before" = "$after" ]; then
            echo "      Up to date (${after})"
        else
            echo "      Updated: ${before} -> ${after}"
        fi
    else
        echo "      WARN: claude update failed (non-fatal; image version retained: ${before})"
    fi
fi

# =============================================================================
# Project-specific setup (separate file)
# Custom per-project settings go in setup-env.project.sh.
# =============================================================================
PROJECT_SETUP="/usr/local/bin/setup-env.project.sh"
if [ -f "$PROJECT_SETUP" ]; then
    echo ""
    echo "--- Project Setup ---"
    source "$PROJECT_SETUP"
fi

# =============================================================================
# Complete
# =============================================================================
echo ""
echo "=============================================="
echo "  Setup Complete!"
echo "=============================================="
echo ""
echo "Skip Claude CLI auto-update on next start:  export SKIP_CLAUDE_UPDATE=1"
echo ""
echo "Start:  claude"
echo ""
echo "Install additional project languages/tools:"
echo "  Go:      sudo apt install -y golang"
echo "  Rust:    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
echo ""
