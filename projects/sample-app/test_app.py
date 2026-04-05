"""Tests for mdstat app."""

import subprocess
import sys
import os

SAMPLE_DIR = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(SAMPLE_DIR, "app.py")


def run_app(*args, stdin_text=None):
    """Run app.py and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, APP, *args],
        capture_output=True,
        text=True,
        input=stdin_text,
        timeout=10,
    )
    return result.returncode, result.stdout, result.stderr


def test_stdin_input():
    md = "# Title\n\nHello world.\n"
    rc, out, _ = run_app("-", stdin_text=md)
    assert rc == 0
    assert "Words:" in out
    assert "Lines:" in out


def test_json_output():
    md = "# Test\n\nSome text here.\n"
    rc, out, _ = run_app("--json", "-", stdin_text=md)
    assert rc == 0
    import json
    data = json.loads(out)
    assert "words" in data
    assert "headings" in data
    assert data["headings"].get("h1") == 1


def test_no_args():
    rc, _, err = run_app()
    assert rc != 0
    assert "Usage" in err


def test_headings():
    md = "# H1\n## H2\n## H2 again\n### H3\n"
    rc, out, _ = run_app("--json", "-", stdin_text=md)
    assert rc == 0
    import json
    data = json.loads(out)
    assert data["headings"]["h1"] == 1
    assert data["headings"]["h2"] == 2
    assert data["headings"]["h3"] == 1


def test_code_blocks():
    md = "```python\nprint('hi')\n```\n\n```\ncode\n```\n"
    rc, out, _ = run_app("--json", "-", stdin_text=md)
    assert rc == 0
    import json
    data = json.loads(out)
    assert data["code_blocks"] == 2


def test_links():
    md = "[Google](https://google.com) and [GitHub](https://github.com)\n"
    rc, out, _ = run_app("--json", "-", stdin_text=md)
    assert rc == 0
    import json
    data = json.loads(out)
    assert data["links"] == 2


def test_images():
    md = "![logo](logo.png) and ![banner](banner.jpg)\n"
    rc, out, _ = run_app("--json", "-", stdin_text=md)
    assert rc == 0
    import json
    data = json.loads(out)
    assert data["images"] == 2


def test_links_exclude_images():
    md = "[Google](https://google.com) and ![logo](logo.png)\n"
    rc, out, _ = run_app("--json", "-", stdin_text=md)
    assert rc == 0
    import json
    data = json.loads(out)
    assert data["links"] == 1
    assert data["images"] == 1


def test_tables():
    md = "| a | b |\n|---|---|\n| 1 | 2 |\n"
    rc, out, _ = run_app("--json", "-", stdin_text=md)
    assert rc == 0
    import json
    data = json.loads(out)
    assert data["tables"] == 1


def test_tables_none():
    md = "# No tables here\n\nJust text.\n"
    rc, out, _ = run_app("--json", "-", stdin_text=md)
    assert rc == 0
    import json
    data = json.loads(out)
    assert data["tables"] == 0


def test_lists():
    md = "- item 1\n- item 2\n\n1. numbered\n2. second\n"
    rc, out, _ = run_app("--json", "-", stdin_text=md)
    assert rc == 0
    import json
    data = json.loads(out)
    assert data["lists"] == 2


def test_lists_single_block():
    md = "- a\n- b\n- c\n"
    rc, out, _ = run_app("--json", "-", stdin_text=md)
    assert rc == 0
    import json
    data = json.loads(out)
    assert data["lists"] == 1


def test_lists_mixed_no_gap():
    md = "- item 1\n- item 2\n1. numbered\n"
    rc, out, _ = run_app("--json", "-", stdin_text=md)
    assert rc == 0
    import json
    data = json.loads(out)
    assert data["lists"] == 1


if __name__ == "__main__":
    tests = [f for f in dir() if f.startswith("test_")]
    passed = 0
    failed = 0
    for name in sorted(tests):
        try:
            globals()[name]()
            print(f"  PASS  {name}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {name}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
