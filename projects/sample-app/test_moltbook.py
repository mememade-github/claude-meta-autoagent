#!/usr/bin/env python3
"""Tests for moltbook.py — Moltbook integration module."""

import json
import os
import sys
import tempfile
from pathlib import Path

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import moltbook


# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------

passed = 0
failed = 0


def test(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS  {name}")
    else:
        failed += 1
        print(f"  FAIL  {name}  {detail}")


# ---------------------------------------------------------------------------
# Sanitizer tests
# ---------------------------------------------------------------------------

def test_sanitize_github_pat():
    text = "Token is ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef123456"
    result = moltbook.sanitize(text)
    test("sanitize_github_pat", "[REDACTED]" in result and "ghp_" not in result)


def test_sanitize_anthropic_key():
    text = "key: sk-ant-abc123-XYZXYZXYZXYZXYZXYZXYZ"
    result = moltbook.sanitize(text)
    test("sanitize_anthropic_key", "[REDACTED]" in result and "sk-ant-" not in result)


def test_sanitize_password_value():
    text = "Found password=mysecretpass123 in config"
    result = moltbook.sanitize(text)
    test("sanitize_password_value", "mysecretpass123" not in result)


def test_sanitize_email():
    text = "Contact user@example.com for details"
    result = moltbook.sanitize(text)
    test("sanitize_email", "user@example.com" not in result)


def test_sanitize_ip_address():
    text = "Server at 192.168.1.100:8080 is running"
    result = moltbook.sanitize(text)
    test("sanitize_ip_address", "192.168.1.100" not in result)


def test_sanitize_home_path():
    text = "File at /home/vscode/project/secret.txt"
    result = moltbook.sanitize(text)
    test("sanitize_home_path", "/home/vscode/" not in result)


def test_sanitize_clean_text():
    text = "Score improved from 0.83 to 0.95 in 3 iterations"
    result = moltbook.sanitize(text)
    test("sanitize_clean_text", result == text, f"got: {result}")


def test_sanitize_empty_raises():
    try:
        moltbook.sanitize("")
        test("sanitize_empty_raises", False, "should have raised ValueError")
    except ValueError:
        test("sanitize_empty_raises", True)


def test_sanitize_whitespace_raises():
    try:
        moltbook.sanitize("   \n  ")
        test("sanitize_empty_raises_ws", False, "should have raised ValueError")
    except ValueError:
        test("sanitize_empty_raises_ws", True)


def test_is_safe_content():
    test("is_safe_clean", moltbook.is_safe_content("Hello world"))
    test("is_safe_secret", not moltbook.is_safe_content("password=abc123"))


def test_check_path_safety():
    test("path_safe_normal", moltbook.check_path_safety("src/app.py"))
    test("path_safe_env", not moltbook.check_path_safety(".env/secrets"))
    test("path_safe_ssh", not moltbook.check_path_safety("/home/user/.ssh/id_rsa"))
    test("path_safe_credentials", not moltbook.check_path_safety("config/credentials.json"))


# ---------------------------------------------------------------------------
# API key management tests
# ---------------------------------------------------------------------------

def test_load_api_key_from_env():
    os.environ["MOLTBOOK_API_KEY"] = "test-key-123"
    result = moltbook.load_api_key()
    del os.environ["MOLTBOOK_API_KEY"]
    test("load_key_env", result == "test-key-123")


def test_load_api_key_from_file():
    original_path = moltbook.ENV_PATH
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
        f.write("# comment\nMOLTBOOK_API_KEY=file-key-456\n")
        f.flush()
        moltbook.ENV_PATH = Path(f.name)

    # Ensure env var doesn't interfere
    os.environ.pop("MOLTBOOK_API_KEY", None)
    result = moltbook.load_api_key()
    moltbook.ENV_PATH = original_path
    os.unlink(f.name)
    test("load_key_file", result == "file-key-456", f"got: {result}")


def test_load_api_key_missing():
    os.environ.pop("MOLTBOOK_API_KEY", None)
    original_path = moltbook.ENV_PATH
    moltbook.ENV_PATH = Path("/nonexistent/path/moltbook.env")
    result = moltbook.load_api_key()
    moltbook.ENV_PATH = original_path
    test("load_key_missing", result == "")


# ---------------------------------------------------------------------------
# Activity logging tests
# ---------------------------------------------------------------------------

def test_log_activity():
    original_log = moltbook.ACTIVITY_LOG
    with tempfile.TemporaryDirectory() as tmpdir:
        moltbook.ACTIVITY_LOG = Path(tmpdir) / "sub" / "activity.jsonl"
        moltbook.log_activity("test_action", {"key": "value"})
        moltbook.log_activity("test_action2", success=False)

        lines = moltbook.ACTIVITY_LOG.read_text().strip().split("\n")
        test("log_creates_file", len(lines) == 2)

        entry1 = json.loads(lines[0])
        test("log_has_ts", "ts" in entry1)
        test("log_has_agent", entry1["agent"] == moltbook.AGENT_NAME)
        test("log_has_action", entry1["action"] == "test_action")
        test("log_has_detail", entry1["detail"] == {"key": "value"})
        test("log_success_true", entry1["success"] is True)

        entry2 = json.loads(lines[1])
        test("log_success_false", entry2["success"] is False)

    moltbook.ACTIVITY_LOG = original_log


# ---------------------------------------------------------------------------
# Compose post tests
# ---------------------------------------------------------------------------

def test_compose_refine_post():
    title, body = moltbook.compose_refine_post(0.83, 0.95, ["G3", "G4"], 3)
    test("compose_title_scores", "0.83" in title and "0.95" in title)
    test("compose_title_agent", moltbook.AGENT_NAME in title)
    test("compose_body_iterations", "3" in body)
    test("compose_body_gaps", "G3" in body and "G4" in body)
    test("compose_body_safe", moltbook.is_safe_content(body))


def test_compose_refine_post_no_gaps():
    title, body = moltbook.compose_refine_post(0.90, 0.90, [], 1)
    test("compose_no_gaps", "none" in body)


# ---------------------------------------------------------------------------
# CLI tests
# ---------------------------------------------------------------------------

def test_cli_status():
    """Test the status command via CLI invocation."""
    import subprocess
    result = subprocess.run(
        [sys.executable, "moltbook.py", "status"],
        capture_output=True, text=True, cwd=str(Path(__file__).resolve().parent)
    )
    test("cli_status_exit", result.returncode == 0)
    test("cli_status_agent", moltbook.AGENT_NAME in result.stdout)


def test_cli_no_args():
    import subprocess
    result = subprocess.run(
        [sys.executable, "moltbook.py"],
        capture_output=True, text=True, cwd=str(Path(__file__).resolve().parent)
    )
    test("cli_no_args_exit", result.returncode == 1)


def test_cli_unknown_cmd():
    import subprocess
    result = subprocess.run(
        [sys.executable, "moltbook.py", "foobar"],
        capture_output=True, text=True, cwd=str(Path(__file__).resolve().parent)
    )
    test("cli_unknown_exit", result.returncode == 1)


# ---------------------------------------------------------------------------
# No-key error handling tests
# ---------------------------------------------------------------------------

def test_post_without_key():
    os.environ.pop("MOLTBOOK_API_KEY", None)
    original_path = moltbook.ENV_PATH
    moltbook.ENV_PATH = Path("/nonexistent/path/moltbook.env")
    try:
        moltbook.post_achievement("title", "body")
        test("post_no_key_raises", False, "should have raised RuntimeError")
    except RuntimeError as e:
        test("post_no_key_raises", "API key" in str(e))
    moltbook.ENV_PATH = original_path


def test_heartbeat_without_key():
    os.environ.pop("MOLTBOOK_API_KEY", None)
    original_path = moltbook.ENV_PATH
    moltbook.ENV_PATH = Path("/nonexistent/path/moltbook.env")
    try:
        moltbook.heartbeat()
        test("heartbeat_no_key_raises", False, "should have raised RuntimeError")
    except RuntimeError as e:
        test("heartbeat_no_key_raises", "API key" in str(e))
    moltbook.ENV_PATH = original_path


# ---------------------------------------------------------------------------
# Run all
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    test_sanitize_github_pat()
    test_sanitize_anthropic_key()
    test_sanitize_password_value()
    test_sanitize_email()
    test_sanitize_ip_address()
    test_sanitize_home_path()
    test_sanitize_clean_text()
    test_sanitize_empty_raises()
    test_sanitize_whitespace_raises()
    test_is_safe_content()
    test_check_path_safety()
    test_load_api_key_from_env()
    test_load_api_key_from_file()
    test_load_api_key_missing()
    test_log_activity()
    test_compose_refine_post()
    test_compose_refine_post_no_gaps()
    test_cli_status()
    test_cli_no_args()
    test_cli_unknown_cmd()
    test_post_without_key()
    test_heartbeat_without_key()

    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
