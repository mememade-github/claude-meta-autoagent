"""
mdstat — Markdown document statistics CLI tool.

A deliberately simple tool with room for improvement,
designed as a sample project for claude-meta-autoagent /refine.

Usage:
    python app.py <file.md>
    python app.py --json <file.md>
    echo "# Hello" | python app.py -
"""

import sys
import re


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def count_headings(text: str) -> dict:
    """Count headings by level (h1-h6)."""
    counts = {}
    for line in text.splitlines():
        match = re.match(r'^(#{1,6})\s', line)
        if match:
            level = f"h{len(match.group(1))}"
            counts[level] = counts.get(level, 0) + 1
    return counts


def count_code_blocks(text: str) -> int:
    """Count fenced code blocks."""
    return len(re.findall(r'^```', text, re.MULTILINE)) // 2


def count_images(text: str) -> int:
    """Count markdown images ![alt](url)."""
    return len(re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', text))


def count_tables(text: str) -> int:
    """Count markdown tables by detecting separator rows like |---|---|."""
    return len(re.findall(r'^\|[\s\-:|]+\|$', text, re.MULTILINE))


def count_lists(text: str) -> int:
    """Count list blocks (contiguous groups of list items)."""
    blocks = 0
    in_list = False
    for line in text.splitlines():
        is_item = bool(re.match(r'^(\s*[-*]\s|\s*\d+\.\s)', line))
        if is_item and not in_list:
            blocks += 1
            in_list = True
        elif not is_item and line.strip() == "":
            in_list = False
        elif not is_item:
            in_list = False
    return blocks


def count_blockquotes(text: str) -> int:
    """Count blockquote blocks (contiguous groups of > lines)."""
    blocks = 0
    in_block = False
    for line in text.splitlines():
        is_quote = bool(re.match(r'^>\s?', line))
        if is_quote and not in_block:
            blocks += 1
            in_block = True
        elif not is_quote:
            in_block = False
    return blocks


def count_links(text: str) -> int:
    """Count markdown links [text](url), excluding images."""
    return len(re.findall(r'(?<!!)\[([^\]]+)\]\(([^)]+)\)', text))


def analyze(text: str) -> dict:
    """Analyze markdown document and return statistics."""
    lines = text.splitlines()
    return {
        "lines": len(lines),
        "words": count_words(text),
        "characters": len(text),
        "headings": count_headings(text),
        "code_blocks": count_code_blocks(text),
        "links": count_links(text),
        "images": count_images(text),
        "lists": count_lists(text),
        "tables": count_tables(text),
        "blockquotes": count_blockquotes(text),
    }


def format_report(stats: dict) -> str:
    """Format statistics as human-readable report."""
    lines = [
        f"Lines:       {stats['lines']}",
        f"Words:       {stats['words']}",
        f"Characters:  {stats['characters']}",
        f"Code blocks: {stats['code_blocks']}",
        f"Links:       {stats['links']}",
        f"Images:      {stats['images']}",
        f"Lists:       {stats['lists']}",
        f"Tables:      {stats['tables']}",
        f"Blockquotes: {stats['blockquotes']}",
    ]
    if stats["headings"]:
        lines.append("Headings:")
        for level, count in sorted(stats["headings"].items()):
            lines.append(f"  {level}: {count}")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python app.py [--json] <file.md | ->", file=sys.stderr)
        sys.exit(1)

    json_output = False
    filepath = sys.argv[1]

    if filepath == "--json":
        json_output = True
        if len(sys.argv) < 3:
            print("Usage: python app.py --json <file.md | ->", file=sys.stderr)
            sys.exit(1)
        filepath = sys.argv[2]

    if filepath == "-":
        text = sys.stdin.read()
    else:
        with open(filepath) as f:
            text = f.read()

    stats = analyze(text)

    if json_output:
        import json
        print(json.dumps(stats, indent=2))
    else:
        print(format_report(stats))


if __name__ == "__main__":
    main()
