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

PASS=0; TOTAL=0; SKIP=0

check() {
    TOTAL=$((TOTAL + 1))
    if eval "$2" >/dev/null 2>&1; then
        PASS=$((PASS + 1))
    else
        GAPS="$GAPS $1"
    fi
}
GAPS=""

skip() {
    SKIP=$((SKIP + 1))
}

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

# ── D: Delta display correctness ──────────────────────────────
# D1: compose_refine_post negative delta must NOT show "+-" (should show "-")
check D1 'python3 -c "
import moltbook
t, b = moltbook.compose_refine_post(0.95, 0.80, [], 1)
assert \"+-\" not in t, f\"Title has +-: {t}\"
assert \"-0.15\" in t or \"−0.15\" in t
"'

# D2: compose_refine_post positive delta shows "+" correctly
check D2 'python3 -c "
import moltbook
t, b = moltbook.compose_refine_post(0.80, 0.95, [], 1)
assert \"+0.15\" in t
assert \"+-\" not in t
"'

# ── V: Input validation ──────────────────────────────────────
# V1: get_feed validates sort parameter (only allowed values)
check V1 'python3 -c "
import moltbook
# Monkey-patch to avoid real API call — just check validation
original = moltbook._api_request
called_with = []
def mock_req(method, endpoint, data=None, api_key=None):
    called_with.append(endpoint)
    return []
moltbook._api_request = mock_req
import os; os.environ[\"MOLTBOOK_API_KEY\"] = \"test\"
try:
    moltbook.get_feed(sort=\"hot&admin=true\")
    exit(1)  # Should reject injection attempt
except (ValueError, RuntimeError):
    pass
finally:
    moltbook._api_request = original
    del os.environ[\"MOLTBOOK_API_KEY\"]
"'

# V2: get_feed validates limit parameter (must be positive integer)
check V2 'python3 -c "
import moltbook, os
original = moltbook._api_request
def mock_req(method, endpoint, data=None, api_key=None):
    return []
moltbook._api_request = mock_req
os.environ[\"MOLTBOOK_API_KEY\"] = \"test\"
try:
    moltbook.get_feed(limit=-1)
    exit(1)
except (ValueError, TypeError):
    pass
finally:
    moltbook._api_request = original
    del os.environ[\"MOLTBOOK_API_KEY\"]
"'

# ── K: CLI completeness ──────────────────────────────────────
# K1: CLI help text lists comment command
check K1 'OUT=$(python3 moltbook.py 2>&1 || true); echo "$OUT" | grep -q "comment"'

# K2: CLI help text lists feed command
check K2 'OUT=$(python3 moltbook.py 2>&1 || true); echo "$OUT" | grep -q "feed"'

# ── N: New API function coverage ──────────────────────────────
# N1: All new API functions exist as callables
check N1 'python3 -c "
import moltbook
fns = [\"verify_challenge\", \"upvote_post\", \"downvote_post\", \"upvote_comment\",
       \"follow_agent\", \"unfollow_agent\", \"update_profile\", \"search\",
       \"get_dashboard\", \"get_comments\", \"get_post\", \"subscribe_submolt\",
       \"unsubscribe_submolt\", \"list_submolts\", \"get_notifications\",
       \"get_profile\", \"post_link\"]
for fn in fns:
    assert callable(getattr(moltbook, fn)), f\"{fn} not callable\"
"'

# N2: New API functions raise RuntimeError without API key (representative sample)
check N2 'python3 -c "
import os, moltbook
from pathlib import Path
os.environ.pop(\"MOLTBOOK_API_KEY\", None)
moltbook.ENV_PATH = Path(\"/nonexistent\")
fns = [
    lambda: moltbook.verify_challenge(\"code\", 1.0),
    lambda: moltbook.upvote_post(\"123\"),
    lambda: moltbook.downvote_post(\"123\"),
    lambda: moltbook.upvote_comment(\"123\"),
    lambda: moltbook.follow_agent(\"x\"),
    lambda: moltbook.unfollow_agent(\"x\"),
    lambda: moltbook.update_profile(description=\"x\"),
    lambda: moltbook.search(\"q\"),
    lambda: moltbook.get_dashboard(),
    lambda: moltbook.get_comments(\"123\"),
    lambda: moltbook.get_post(\"123\"),
    lambda: moltbook.subscribe_submolt(\"x\"),
    lambda: moltbook.unsubscribe_submolt(\"x\"),
    lambda: moltbook.list_submolts(),
    lambda: moltbook.get_notifications(),
    lambda: moltbook.get_profile(),
    lambda: moltbook.post_link(\"t\", \"http://x\"),
]
for fn in fns:
    try:
        fn()
        exit(1)
    except RuntimeError:
        pass
"'

# N3: search validates search_type parameter
check N3 'python3 -c "
import os, moltbook
os.environ[\"MOLTBOOK_API_KEY\"] = \"test\"
moltbook._api_request = lambda *a, **kw: []
try:
    moltbook.search(\"q\", search_type=\"invalid\")
    exit(1)
except ValueError:
    pass
finally:
    del os.environ[\"MOLTBOOK_API_KEY\"]
"'

# N4: search validates limit parameter
check N4 'python3 -c "
import os, moltbook
os.environ[\"MOLTBOOK_API_KEY\"] = \"test\"
moltbook._api_request = lambda *a, **kw: []
try:
    moltbook.search(\"q\", limit=-5)
    exit(1)
except ValueError:
    pass
finally:
    del os.environ[\"MOLTBOOK_API_KEY\"]
"'

# N5: get_comments validates sort parameter
check N5 'python3 -c "
import os, moltbook
os.environ[\"MOLTBOOK_API_KEY\"] = \"test\"
moltbook._api_request = lambda *a, **kw: []
try:
    moltbook.get_comments(\"123\", sort=\"evil&admin=1\")
    exit(1)
except ValueError:
    pass
finally:
    del os.environ[\"MOLTBOOK_API_KEY\"]
"'

# N6: update_profile sanitizes description before sending
check N6 'python3 -c "
import os, moltbook
os.environ[\"MOLTBOOK_API_KEY\"] = \"test\"
sent_data = {}
def mock_req(method, endpoint, data=None, api_key=None):
    sent_data.update(data or {})
    return {}
moltbook._api_request = mock_req
moltbook.update_profile(description=\"my ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef1234567 secret\")
assert \"ghp_\" not in sent_data[\"description\"]
assert \"[REDACTED]\" in sent_data[\"description\"]
del os.environ[\"MOLTBOOK_API_KEY\"]
"'

# N7: post_link sanitizes title before sending
check N7 'python3 -c "
import os, moltbook
os.environ[\"MOLTBOOK_API_KEY\"] = \"test\"
sent_data = {}
def mock_req(method, endpoint, data=None, api_key=None):
    sent_data.update(data or {})
    return {\"id\": \"1\"}
moltbook._api_request = mock_req
moltbook.post_link(\"check password=secret123 link\", \"http://example.com\")
assert \"secret123\" not in sent_data[\"title\"]
del os.environ[\"MOLTBOOK_API_KEY\"]
"'

# N8: verify_challenge formats answer to 2 decimal places
check N8 'python3 -c "
import os, moltbook
os.environ[\"MOLTBOOK_API_KEY\"] = \"test\"
sent_data = {}
def mock_req(method, endpoint, data=None, api_key=None):
    sent_data.update(data or {})
    return {}
moltbook._api_request = mock_req
moltbook.verify_challenge(\"code1\", 3.14159)
assert sent_data[\"answer\"] == \"3.14\", f\"got {sent_data['answer']}\"
del os.environ[\"MOLTBOOK_API_KEY\"]
"'

# N9: CLI help lists new commands (verify, search, subscribe, notifications)
check N9 'OUT=$(python3 moltbook.py 2>&1 || true); echo "$OUT" | grep -q "verify" && echo "$OUT" | grep -q "search" && echo "$OUT" | grep -q "subscribe" && echo "$OUT" | grep -q "notifications"'

# ── P: Pacing quality (burst detection in activity.jsonl) ─────
# Skipped when activity.jsonl is absent (file is gitignored runtime data)
if [ -f ".moltbook/activity.jsonl" ]; then
# P1: No burst of >=4 identical actions within a 5-second window
check P1 'python3 -c "
import json
from datetime import datetime
LOG = \".moltbook/activity.jsonl\"
entries = [json.loads(l) for l in open(LOG)]
def parse_ts(s): return datetime.strptime(s, \"%Y-%m-%dT%H:%M:%SZ\")
# Sliding window: for each entry, count same-action entries within 5s forward
for i, e in enumerate(entries):
    t0 = parse_ts(e[\"ts\"])
    count = 1
    for j in range(i+1, len(entries)):
        if entries[j][\"action\"] != e[\"action\"]:
            continue
        dt = (parse_ts(entries[j][\"ts\"]) - t0).total_seconds()
        if dt > 5:
            break
        count += 1
    assert count < 4, f\"Burst: {count}x {e['action']} in 5s at {e['ts']}\"
"'

# P2: Median inter-action gap >= 2 seconds (not machine-gunning)
check P2 'python3 -c "
import json, statistics
from datetime import datetime
LOG = \".moltbook/activity.jsonl\"
entries = [json.loads(l) for l in open(LOG)]
def parse_ts(s): return datetime.strptime(s, \"%Y-%m-%dT%H:%M:%SZ\")
gaps = []
for i in range(1, len(entries)):
    dt = (parse_ts(entries[i][\"ts\"]) - parse_ts(entries[i-1][\"ts\"])).total_seconds()
    gaps.append(dt)
med = statistics.median(gaps)
assert med >= 2, f\"Median gap {med:.1f}s < 2s\"
"'

# P3: No 60-second window contains more than 15 actions
check P3 'python3 -c "
import json
from datetime import datetime
LOG = \".moltbook/activity.jsonl\"
entries = [json.loads(l) for l in open(LOG)]
def parse_ts(s): return datetime.strptime(s, \"%Y-%m-%dT%H:%M:%SZ\")
times = [parse_ts(e[\"ts\"]) for e in entries]
for i in range(len(times)):
    count = sum(1 for t in times[i:] if (t - times[i]).total_seconds() <= 60)
    assert count <= 15, f\"{count} actions in 60s window starting {entries[i]['ts']}\"
"'
else
    skip P1; skip P2; skip P3
fi

# ── A: API utilization coverage ──────────────────────────────
# Skipped when activity.jsonl is absent
if [ -f ".moltbook/activity.jsonl" ]; then
# A1: At least 8 distinct action types in activity log
check A1 'python3 -c "
import json
LOG = \".moltbook/activity.jsonl\"
actions = {json.loads(l)[\"action\"] for l in open(LOG)}
assert len(actions) >= 8, f\"Only {len(actions)} distinct actions, need >= 8\"
"'

# A2: At least 50% of logging API functions appear in activity log
check A2 'python3 -c "
import json
LOG = \".moltbook/activity.jsonl\"
# All action names that moltbook.py log_activity() can produce
ALL_LOGGED = {\"register\", \"post\", \"comment\", \"heartbeat\", \"verify\",
    \"upvote_post\", \"downvote_post\", \"upvote_comment\", \"follow\",
    \"unfollow\", \"update_profile\", \"subscribe\", \"unsubscribe\",
    \"post_link\", \"engagement_round\"}
used = {json.loads(l)[\"action\"] for l in open(LOG)}
coverage = len(used & ALL_LOGGED) / len(ALL_LOGGED)
assert coverage >= 0.50, f\"API coverage {coverage:.0%} < 50%\"
"'
else
    skip A1; skip A2
fi

# ── Q: Engagement diversity ──────────────────────────────────
# Skipped when activity.jsonl is absent
if [ -f ".moltbook/activity.jsonl" ]; then
# Q1: No single action type exceeds 40% of all entries
check Q1 'python3 -c "
import json
from collections import Counter
LOG = \".moltbook/activity.jsonl\"
actions = [json.loads(l)[\"action\"] for l in open(LOG)]
counts = Counter(actions)
total = len(actions)
for action, n in counts.items():
    pct = n / total
    assert pct <= 0.40, f\"{action} is {pct:.0%} of entries (>{40}%)\"
"'

# Q2: Shannon entropy of action distribution >= 1.8 bits (natural log)
check Q2 'python3 -c "
import json, math
from collections import Counter
LOG = \".moltbook/activity.jsonl\"
actions = [json.loads(l)[\"action\"] for l in open(LOG)]
counts = Counter(actions)
total = len(actions)
entropy = -sum((n/total) * math.log(n/total) for n in counts.values())
assert entropy >= 1.8, f\"Entropy {entropy:.2f} < 1.8\"
"'

# Q3: At least 3 action categories used (content, social, admin)
check Q3 'python3 -c "
import json
LOG = \".moltbook/activity.jsonl\"
actions = {json.loads(l)[\"action\"] for l in open(LOG)}
CONTENT = {\"post\", \"post_link\", \"comment\"}
SOCIAL = {\"upvote_post\", \"downvote_post\", \"upvote_comment\", \"follow\", \"unfollow\"}
ADMIN = {\"register\", \"update_profile\", \"subscribe\", \"unsubscribe\", \"heartbeat\", \"verify\"}
cats = sum([bool(actions & CONTENT), bool(actions & SOCIAL), bool(actions & ADMIN)])
assert cats >= 3, f\"Only {cats} action categories used, need >= 3\"
"'
else
    skip Q1; skip Q2; skip Q3
fi

# ── M: Moltbook API external metrics ─────────────────────────
# Skipped when MOLTBOOK_API_KEY is not set
if [ -n "${MOLTBOOK_API_KEY:-}" ]; then
# M1: profile command returns data with karma field
check M1 'python3 moltbook.py profile 2>&1 | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())
assert \"karma\" in data, \"karma field missing from profile\"
"'

# M2: notifications command returns valid response structure
check M2 'python3 moltbook.py notifications 2>&1 | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())
assert isinstance(data, (list, dict)), \"notifications response is not list or dict\"
"'
else
    skip M1; skip M2
fi

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
if [ "$SKIP" -gt 0 ]; then
    echo "SKIPPED: $SKIP"
fi
