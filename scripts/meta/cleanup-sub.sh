#!/bin/bash
# =============================================================================
# cleanup-sub.sh — L2→L3 session-scoped cleanup (A or B sub-project container)
# =============================================================================
# Removes session-scoped artefacts relayed by delegate-sub.sh into a Level-3a
# (A) or Level-3b (B) sub-project container:
#   - ~/.claude/.credentials.json  (OAuth credentials relayed at launch)
#   - /tmp/agent-YYYYMMDD-*.log    (today's agent logs only)
#   - Orphaned 'claude doctor' / 'claude update' processes
#
# Boundary: mirrors the L1→L2 cleanup pattern down one layer.  ROOT runs this
# after each Cycle-NN run to enforce that relayed credentials do not persist
# inside the A/B containers.
#
# Usage:
#   scripts/meta/cleanup-sub.sh <a|b> [--stop]
#
# Exit codes:
#   0  — clean run (or container not running)
#   1  — usage / invalid sub-key
# =============================================================================

set -euo pipefail

usage() {
  cat >&2 <<EOF
Usage: $0 <a|b> [--stop]

Removes session-scoped artefacts from the A or B sub-project container:
  - ~/.claude/.credentials.json  (OAuth file relayed by delegate-sub.sh)
  - /tmp/agent-YYYYMMDD-*.log    (today's agent logs only)
  - Orphaned 'claude doctor' / 'claude update' processes

Optional:
  --stop   docker stop the container after cleanup (lifecycle close-out)

Subkey 'a' → container claude-meta-autoagent-a
Subkey 'b' → container claude-meta-autoagent-b
EOF
}

if [ $# -lt 1 ]; then
  usage
  exit 1
fi

SUB_KEY="$1"
STOP_AFTER=0
if [ "${2:-}" = "--stop" ]; then
  STOP_AFTER=1
fi

# Sub map — keep in sync with delegate-sub.sh
declare -A SUBS=(
  ["a"]="claude-meta-autoagent-a"
  ["b"]="claude-meta-autoagent-b"
)

if [ -z "${SUBS[$SUB_KEY]:-}" ]; then
  echo "Error: unknown sub key '$SUB_KEY' (expected 'a' or 'b')" >&2
  usage
  exit 1
fi

CONTAINER="${SUBS[$SUB_KEY]}"

if ! docker ps --filter "name=^${CONTAINER}$" --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
  echo "Container '${CONTAINER}' is not running. Nothing to clean inside."
  if [ "$STOP_AFTER" = "1" ]; then
    echo "(--stop is moot; container already stopped)"
  fi
  exit 0
fi

TODAY=$(date +%Y%m%d)
echo "Cleanup target: ${CONTAINER} (today=${TODAY})"

# Heredoc-over-stdin pattern: avoids pgrep self-match that occurs when the
# pattern string lands in the docker-exec cmdline as a literal argv slot.
docker exec -i "$CONTAINER" env CLEANUP_TODAY="$TODAY" bash -s <<'INNER_CLEANUP'
set -e
removed=()

if [ -f /home/vscode/.claude/.credentials.json ]; then
  rm -f /home/vscode/.claude/.credentials.json
  removed+=('credentials.json')
fi

for f in /tmp/agent-${CLEANUP_TODAY}-*.log; do
  if [ -f "$f" ]; then
    rm -f "$f"
    removed+=("$(basename "$f")")
  fi
done

for pid in $(pgrep -f 'claude doctor|claude update' 2>/dev/null || true); do
  if kill -TERM "$pid" 2>/dev/null; then
    removed+=("pid:$pid")
  fi
done

if [ ${#removed[@]} -eq 0 ]; then
  echo 'removed: (nothing — already clean)'
else
  echo "removed: ${removed[*]}"
fi
INNER_CLEANUP

if [ "$STOP_AFTER" = "1" ]; then
  echo "Stopping container ${CONTAINER}..."
  docker stop "$CONTAINER" >/dev/null
  echo "stopped."
fi
