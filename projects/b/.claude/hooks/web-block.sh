#!/bin/bash
# PreToolUse hook (matcher: WebFetch|WebSearch): block all network-tool
# invocations in this sandbox.  The task the agent receives is a derive-from-
# first-principles exercise; consulting external sources is disqualifying.
# Exit code 2 with a stderr message is the documented blocking signal.
cat >/dev/null
echo "BLOCKED: WebFetch and WebSearch are disabled in this environment." >&2
echo "Arguments must be developed from first principles only." >&2
exit 2
