#!/usr/bin/env bash
# ==========================================================================
# Scorer for sample-app — Moltbook integration demo
#
# Tests: Moltbook functionality, security, CLI + project unification.
# Output format (required by /refine):
#   SCORE: 0.XX
#   GAPS: [ID1, ID2, ...]
# ==========================================================================
set -euo pipefail
cd "$(dirname "$0")/.."

PASS=0; TOTAL=0

check() {
    TOTAL=$((TOTAL + 1))
    if eval "$2" >/dev/null 2>&1; then
        PASS=$((PASS + 1))
    else
        GAPS="$GAPS $1"
    fi
}
GAPS=""

# ── F: Functional ──────────────────────────────────────────────
# F1: Module imports without error
check F1 'python3 -c "import moltbook"'

# F2: sanitize removes GitHub PAT
check F2 'python3 -c "
import moltbook
r = moltbook.sanitize(\"tok ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef123456 end\")
assert \"ghp_\" not in r and \"[REDACTED]\" in r
"'

# F3: sanitize removes Anthropic keys
check F3 'python3 -c "
import moltbook
r = moltbook.sanitize(\"key sk-ant-abc123-XYZXYZXYZXYZXYZXYZXYZ here\")
assert \"sk-ant-\" not in r
"'

# F4: sanitize removes emails
check F4 'python3 -c "
import moltbook
r = moltbook.sanitize(\"email user@example.com done\")
assert \"user@example.com\" not in r
"'

# F5: sanitize removes IP addresses
check F5 'python3 -c "
import moltbook
r = moltbook.sanitize(\"host 192.168.1.100:8080 ok\")
assert \"192.168.1.100\" not in r
"'

# F6: sanitize removes password=value
check F6 'python3 -c "
import moltbook
r = moltbook.sanitize(\"config password=secret123 end\")
assert \"secret123\" not in r
"'

# F7: sanitize preserves clean text
check F7 'python3 -c "
import moltbook
t = \"Score improved 0.83 to 0.95\"
assert moltbook.sanitize(t) == t
"'

# F8: is_safe_content detects unsafe
check F8 'python3 -c "
import moltbook
assert moltbook.is_safe_content(\"hello\")
assert not moltbook.is_safe_content(\"password=abc\")
"'

# F9: check_path_safety works
check F9 'python3 -c "
import moltbook
assert moltbook.check_path_safety(\"src/app.py\")
assert not moltbook.check_path_safety(\".env/secrets\")
"'

# F10: compose_refine_post produces safe output
check F10 'python3 -c "
import moltbook
t, b = moltbook.compose_refine_post(0.83, 0.95, [\"G3\"], 2)
assert \"0.83\" in t and \"0.95\" in t
assert moltbook.AGENT_NAME in t
assert moltbook.is_safe_content(b)
"'

# ── E: Error handling ──────────────────────────────────────────
# E1: sanitize rejects empty string
check E1 'python3 -c "
import moltbook
try:
    moltbook.sanitize(\"\")
    exit(1)
except ValueError:
    pass
"'

# E2: post_achievement raises without API key
check E2 'python3 -c "
import os, moltbook
from pathlib import Path
os.environ.pop(\"MOLTBOOK_API_KEY\", None)
moltbook.ENV_PATH = Path(\"/nonexistent\")
try:
    moltbook.post_achievement(\"t\", \"b\")
    exit(1)
except RuntimeError:
    pass
"'

# E3: heartbeat raises without API key
check E3 'python3 -c "
import os, moltbook
from pathlib import Path
os.environ.pop(\"MOLTBOOK_API_KEY\", None)
moltbook.ENV_PATH = Path(\"/nonexistent\")
try:
    moltbook.heartbeat()
    exit(1)
except RuntimeError:
    pass
"'

# ── L: Activity logging ───────────────────────────────────────
# L1: log_activity creates JSONL entries
check L1 'python3 -c "
import json, tempfile, moltbook
from pathlib import Path
d = tempfile.mkdtemp()
moltbook.ACTIVITY_LOG = Path(d) / \"test.jsonl\"
moltbook.log_activity(\"test\", {\"k\": \"v\"})
e = json.loads(open(moltbook.ACTIVITY_LOG).readline())
assert e[\"action\"] == \"test\" and e[\"agent\"] == moltbook.AGENT_NAME
assert e[\"detail\"] == {\"k\": \"v\"} and e[\"success\"] is True
"'

# L2: log_activity records failure
check L2 'python3 -c "
import json, tempfile, moltbook
from pathlib import Path
d = tempfile.mkdtemp()
moltbook.ACTIVITY_LOG = Path(d) / \"test.jsonl\"
moltbook.log_activity(\"fail_action\", success=False)
e = json.loads(open(moltbook.ACTIVITY_LOG).readline())
assert e[\"success\"] is False
"'

# ── C: CLI ─────────────────────────────────────────────────────
# C1: status command works
check C1 'python3 moltbook.py status | grep -q "claude-meta-autoagent"'

# C2: no-args exits 1
check C2 '! python3 moltbook.py'

# C3: unknown command exits 1
check C3 '! python3 moltbook.py badcmd'

# ── S: Security ────────────────────────────────────────────────
# S1: sanitize removes home directory paths
check S1 'python3 -c "
import moltbook
r = moltbook.sanitize(\"path /home/user/secret ok\")
assert \"/home/user/\" not in r
"'

# S2: compose output never contains sensitive patterns
check S2 'python3 -c "
import moltbook
t, b = moltbook.compose_refine_post(0.5, 1.0, [\"A\",\"B\"], 5)
assert moltbook.is_safe_content(t)
assert moltbook.is_safe_content(b)
"'

# ── G: Gap checks (features that should exist) ────────────────
# G1: sanitize removes Slack bot tokens
check G1 'python3 -c "
import moltbook
r = moltbook.sanitize(\"bot xoxb-123456-abcdef token\")
assert \"xoxb-\" not in r
"'

# G2: sanitize handles multiple sensitive items in one string
check G2 'python3 -c "
import moltbook
r = moltbook.sanitize(\"email admin@corp.com host 10.0.0.1 pass password=abc\")
assert \"admin@corp.com\" not in r
assert \"10.0.0.1\" not in r
assert \"password=abc\" not in r
"'

# G3: API key is never sent to non-Moltbook domains
check G3 'python3 -c "
import moltbook
assert \"moltbook.com\" in moltbook.API_BASE
url = moltbook.API_BASE + \"/test\"
assert url.startswith(\"https://www.moltbook.com/\")
"'

# G4: sanitize removes AWS access keys
check G4 'python3 -c "
import moltbook
r = moltbook.sanitize(\"key AKIAIOSFODNN7EXAMPLE here\")
assert \"AKIAIOSFODNN7EXAMPLE\" not in r
"'

# G5: sanitize removes private key markers
check G5 'python3 -c "
import moltbook
r = moltbook.sanitize(\"-----BEGIN RSA PRIVATE KEY----- data here\")
assert \"PRIVATE KEY\" not in r
"'

# G6: post_comment raises without API key
check G6 'python3 -c "
import os, moltbook
from pathlib import Path
os.environ.pop(\"MOLTBOOK_API_KEY\", None)
moltbook.ENV_PATH = Path(\"/nonexistent\")
try:
    moltbook.post_comment(\"123\", \"hello\")
    exit(1)
except RuntimeError:
    pass
"'

# G7: get_feed raises without API key
check G7 'python3 -c "
import os, moltbook
from pathlib import Path
os.environ.pop(\"MOLTBOOK_API_KEY\", None)
moltbook.ENV_PATH = Path(\"/nonexistent\")
try:
    moltbook.get_feed()
    exit(1)
except RuntimeError:
    pass
"'

# G8: sanitize removes secret=value
check G8 'python3 -c "
import moltbook
r = moltbook.sanitize(\"data secret=mysecret123 end\")
assert \"mysecret123\" not in r
"'

# G9: activity log entries have ISO 8601 UTC timestamps
check G9 'python3 -c "
import json, tempfile, re, moltbook
from pathlib import Path
d = tempfile.mkdtemp()
moltbook.ACTIVITY_LOG = Path(d) / \"test.jsonl\"
moltbook.log_activity(\"ts_test\")
e = json.loads(open(moltbook.ACTIVITY_LOG).readline())
assert re.match(r\"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\", e[\"ts\"])
"'

# G10: compose_refine_post handles negative delta (score regression)
check G10 'python3 -c "
import moltbook
t, b = moltbook.compose_refine_post(0.95, 0.80, [], 1)
assert \"0.95\" in t and \"0.80\" in t
"'

# ── T: Test suite ──────────────────────────────────────────────
# T1: test_moltbook.py passes
check T1 'python3 test_moltbook.py'

# ── U: Unification checks (demo consolidation) ────────────────
# U1: mdstat app.py removed (no longer part of demo)
check U1 '! test -f app.py'

# U2: mdstat test_app.py removed
check U2 '! test -f test_app.py'

# U3: score_moltbook.sh merged into score.sh (no duplicate scorer)
check U3 '! test -f .refine/score_moltbook.sh'

# U4: CLAUDE.md references moltbook.py as primary source
check U4 'grep -q "moltbook.py" CLAUDE.md && ! grep -q "app\.py.*Markdown" CLAUDE.md'

# U5: README.md reflects Moltbook as the demo app
check U5 'grep -qi "moltbook" README.md && ! grep -q "python app.py" README.md'

# ── Score ──────────────────────────────────────────────────────
SCORE=$(echo "$PASS $TOTAL" | awk '{printf "%.2f", $1/$2}')
GAPS=$(echo "$GAPS" | xargs)
echo "SCORE: $SCORE"
if [ -n "$GAPS" ]; then
    echo "GAPS: [${GAPS// /, }]"
else
    echo "GAPS: []"
fi
