#!/bin/bash
# =============================================================================
# Claude Code DevContainer — Environment Setup (postCreateCommand)
# =============================================================================
set -e

export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

STEP_TOTAL=4
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
# 3. MCP: Context7 (library documentation search)
# =============================================================================
step "MCP: Context7..."
if ! command -v claude &>/dev/null; then
    echo "      WARN: claude CLI not installed — skipping MCP setup"
elif ! command -v npx &>/dev/null; then
    echo "      WARN: npx not installed — skipping Context7"
else
    claude mcp remove context7 --scope user >/dev/null 2>&1 || true
    claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp@latest >/dev/null 2>&1 \
        && echo "      context7: OK" \
        || echo "      WARN: context7 registration failed"
fi

# =============================================================================
# 4. MCP: Serena (code intelligence — pre-installed in Dockerfile)
# =============================================================================
step "MCP: Serena..."
SERENA_DIR="${HOME}/work/serena"
UV_PATH=$(command -v uv 2>/dev/null || echo "${HOME}/.local/bin/uv")

if ! command -v claude &>/dev/null; then
    echo "      WARN: claude CLI not installed — skipping"
elif [ ! -d "$SERENA_DIR" ]; then
    echo "      WARN: Serena not installed ($SERENA_DIR not found)"
elif [ ! -x "$UV_PATH" ]; then
    echo "      WARN: uv not installed"
else
    claude mcp remove serena --scope user >/dev/null 2>&1 || true
    claude mcp add --scope user serena -- "$UV_PATH" run --directory "$SERENA_DIR" serena-mcp-server --context claude-code --project-from-cwd >/dev/null 2>&1 \
        && echo "      serena: OK" \
        || echo "      WARN: serena registration failed"
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
echo "MCP: $(claude mcp list 2>/dev/null | grep -c 'Connected\|Failed' || echo '0') servers"
echo ""
echo "Start:  claude"
echo ""
echo "Install additional project languages/tools:"
echo "  Go:      sudo apt install -y golang"
echo "  Rust:    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
echo ""
