#!/bin/bash
# =============================================================================
# DevContainer Entrypoint
# =============================================================================
# Runs on every container start.
# Both docker compose up -d and VS Code Reopen in Container go through this.
# -> MCP (Context7, Serena) and environment setup are always guaranteed.
#
# VS Code additionally runs postCreateCommand (setup-env.sh),
# but setup-env.sh is idempotent so running twice is safe.
# =============================================================================

# Run MCP and environment setup (non-fatal on error)
if [ -x "/usr/local/bin/setup-env.sh" ]; then
    /usr/local/bin/setup-env.sh 2>&1 || echo "[entrypoint] WARN: setup-env.sh exited with error (non-fatal)"
fi

# Execute the passed command (default: sleep infinity)
exec "$@"
