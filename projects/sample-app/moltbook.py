#!/usr/bin/env python3
"""Moltbook integration — promote claude-meta-autoagent on AI agent social network."""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

AGENT_NAME = "claude-meta-autoagent"
AGENT_DESC = "2-layer self-evolving agent system for Claude Code"
API_BASE = "https://www.moltbook.com/api/v1"
ENV_PATH = Path(__file__).resolve().parent / ".env" / "moltbook.env"
ACTIVITY_LOG = Path(__file__).resolve().parent / ".moltbook" / "activity.jsonl"

# ---------------------------------------------------------------------------
# Sanitizer — prevent internal information leakage
# ---------------------------------------------------------------------------

# Patterns that must NEVER appear in outbound content
_SENSITIVE_PATTERNS = [
    re.compile(r"(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,}"),  # GitHub PATs
    re.compile(r"sk-[A-Za-z0-9]{20,}"),                          # API keys (OpenAI-style)
    re.compile(r"sk-ant-[A-Za-z0-9\-]{20,}"),                    # Anthropic keys
    re.compile(r"xoxb-[0-9]+-[A-Za-z0-9]+"),                     # Slack bot tokens
    re.compile(r"(?:password|secret|token)\s*[=:]\s*\S+", re.I), # key=value secrets
    re.compile(r"/home/\w+/"),                                     # home directory paths
    re.compile(r"(?:\d{1,3}\.){3}\d{1,3}(?::\d+)?"),             # IP addresses
    re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),  # emails
    re.compile(r"AKIA[0-9A-Z]{16}"),                                 # AWS access key IDs
    re.compile(r"-----BEGIN\s+\w+\s+PRIVATE KEY-----"),              # private key markers
]

# Paths and filenames that indicate internal-only content
_SENSITIVE_PATH_KEYWORDS = [
    ".env", "credentials", "secret", ".ssh", "id_rsa", "id_ed25519",
    ".claude/settings", ".git/config",
]


def sanitize(text):
    """Remove sensitive information from text before posting to Moltbook.

    Returns the sanitized string. Raises ValueError if the text contains
    content that cannot be safely redacted (e.g. the entire body is a secret).
    """
    if not text or not text.strip():
        raise ValueError("Empty content cannot be posted")

    result = text
    for pattern in _SENSITIVE_PATTERNS:
        result = pattern.sub("[REDACTED]", result)

    # Reject if sanitization removed most of the content
    if len(result.strip()) < 10 and len(text.strip()) >= 10:
        raise ValueError("Content too sensitive to post — nearly all content was redacted")

    return result


def is_safe_content(text):
    """Check whether text is safe to post (contains no sensitive patterns)."""
    for pattern in _SENSITIVE_PATTERNS:
        if pattern.search(text):
            return False
    return True


def check_path_safety(path_str):
    """Return True if a file path does not reference sensitive locations."""
    lower = path_str.lower()
    return not any(kw in lower for kw in _SENSITIVE_PATH_KEYWORDS)


# ---------------------------------------------------------------------------
# API Key management
# ---------------------------------------------------------------------------

def load_api_key():
    """Load the Moltbook API key from .env/moltbook.env or environment."""
    # 1. Environment variable takes precedence
    key = os.environ.get("MOLTBOOK_API_KEY", "").strip()
    if key:
        return key

    # 2. Fall back to .env file
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k.strip() == "MOLTBOOK_API_KEY" and v.strip():
                return v.strip()

    return ""


# ---------------------------------------------------------------------------
# Activity logging
# ---------------------------------------------------------------------------

def log_activity(action, detail=None, success=True):
    """Append an activity entry to .moltbook/activity.jsonl."""
    ACTIVITY_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "agent": AGENT_NAME,
        "action": action,
        "success": success,
    }
    if detail:
        entry["detail"] = detail
    with open(ACTIVITY_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


# ---------------------------------------------------------------------------
# API client
# ---------------------------------------------------------------------------

def _api_request(method, endpoint, data=None, api_key=None):
    """Low-level Moltbook API request. Returns parsed JSON or raises."""
    url = f"{API_BASE}/{endpoint.lstrip('/')}"
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        raise RuntimeError(f"Moltbook API error {e.code}: {error_body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Moltbook API connection error: {e.reason}") from e


def register_agent():
    """Register the agent on Moltbook and return the API key + claim URL."""
    result = _api_request("POST", "/agents/register", {
        "name": AGENT_NAME,
        "description": AGENT_DESC,
    })
    api_key = result.get("api_key", "")
    if api_key:
        # Persist the key
        ENV_PATH.parent.mkdir(parents=True, exist_ok=True)
        ENV_PATH.write_text(f"# Auto-registered {time.strftime('%Y-%m-%d')}\nMOLTBOOK_API_KEY={api_key}\n")
    log_activity("register", {"claim_url": result.get("claim_url", "")})
    return result


def post_achievement(title, body, community="ai_agents"):
    """Post a project achievement to Moltbook.

    Content is sanitized before posting. Raises ValueError if content
    is unsafe even after sanitization.
    """
    api_key = load_api_key()
    if not api_key:
        raise RuntimeError("No Moltbook API key configured. Run register_agent() first or set MOLTBOOK_API_KEY.")

    safe_title = sanitize(title)
    safe_body = sanitize(body)

    result = _api_request("POST", "/posts", {
        "title": safe_title,
        "content": safe_body,
        "submolt_name": community,
        "type": "text",
    }, api_key=api_key)

    log_activity("post", {"title": safe_title, "post_id": result.get("id", "")})
    return result


def heartbeat():
    """Send a heartbeat to keep the agent account active."""
    api_key = load_api_key()
    if not api_key:
        raise RuntimeError("No Moltbook API key configured.")
    result = _api_request("POST", "/agents/heartbeat", api_key=api_key)
    log_activity("heartbeat")
    return result


def post_comment(post_id, body):
    """Comment on an existing Moltbook post."""
    api_key = load_api_key()
    if not api_key:
        raise RuntimeError("No Moltbook API key configured.")

    safe_body = sanitize(body)
    result = _api_request("POST", f"/posts/{post_id}/comments", {
        "content": safe_body,
    }, api_key=api_key)
    log_activity("comment", {"post_id": post_id})
    return result


def get_feed(sort="hot", limit=10):
    """Fetch the agent's feed from Moltbook."""
    api_key = load_api_key()
    if not api_key:
        raise RuntimeError("No Moltbook API key configured.")
    return _api_request("GET", f"/feed?sort={sort}&limit={limit}", api_key=api_key)


# ---------------------------------------------------------------------------
# Convenience: compose achievement post from refine results
# ---------------------------------------------------------------------------

def compose_refine_post(score_before, score_after, gaps_fixed, iteration_count):
    """Build a Moltbook post body from /refine results.

    All numeric values are validated. Internal file paths and sensitive
    details are excluded by design.
    """
    score_before = float(score_before)
    score_after = float(score_after)
    delta = score_after - score_before

    title = f"[{AGENT_NAME}] Score improved {score_before:.2f} -> {score_after:.2f} (+{delta:.2f})"

    lines = [
        f"**{AGENT_DESC}**",
        "",
        f"Completed a /refine cycle:",
        f"- Iterations: {int(iteration_count)}",
        f"- Score: {score_before:.2f} -> {score_after:.2f} (delta: +{delta:.2f})",
        f"- Gaps fixed: {', '.join(gaps_fixed) if gaps_fixed else 'none'}",
        "",
        "The self-evolving agent autonomously discovered and resolved quality gaps",
        "using evidence-based scoring with context-isolated evaluation.",
    ]
    body = "\n".join(lines)
    return title, body


# ---------------------------------------------------------------------------
# CLI interface
# ---------------------------------------------------------------------------

def main():
    """CLI entry point for moltbook integration."""
    if len(sys.argv) < 2:
        print("Usage: python moltbook.py <command> [args...]")
        print("Commands: register, post, heartbeat, status")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "register":
        result = register_agent()
        print(f"Registered! Claim URL: {result.get('claim_url', 'N/A')}")
        print("API key saved to .env/moltbook.env")

    elif cmd == "post":
        if len(sys.argv) < 4:
            print("Usage: python moltbook.py post <title> <body>")
            sys.exit(1)
        result = post_achievement(sys.argv[2], sys.argv[3])
        print(f"Posted! ID: {result.get('id', 'N/A')}")

    elif cmd == "heartbeat":
        heartbeat()
        print("Heartbeat sent.")

    elif cmd == "status":
        key = load_api_key()
        log_exists = ACTIVITY_LOG.exists()
        entry_count = 0
        if log_exists:
            entry_count = sum(1 for _ in open(ACTIVITY_LOG))
        print(f"Agent: {AGENT_NAME}")
        print(f"API Key: {'configured' if key else 'NOT configured'}")
        print(f"Activity log: {entry_count} entries")

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
