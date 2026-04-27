#!/usr/bin/env python3
"""outcome-verifier.py — compare agent outcome.json to ground-truth.json.

Per docs/meta-audit/procedures/outcome-task-template-v1.md §5 contract.

Usage:
    outcome-verifier.py <outcome.json> <ground-truth.json> [--report <path>]

Exit codes:
    0  success (verdict in stdout; report written if --report given)
    1  argument usage error
    2  input file not found
    3  schema_version mismatch on either input
"""
import json
import sys
from pathlib import Path


def usage() -> None:
    print(
        "Usage: outcome-verifier.py <outcome.json> <ground-truth.json> "
        "[--report <path>]",
        file=sys.stderr,
    )
    sys.exit(1)


def normalize_ci(s) -> str:
    return str(s).strip().lower()


def match_question(agent_answer, gt_question):
    """Return (passed: bool, reason: str)."""
    expected = gt_question["expected_answer"]
    mode = gt_question.get("match_mode", "exact")

    if mode == "exact":
        ok = str(agent_answer) == str(expected)
        return ok, f"exact: '{agent_answer}' vs '{expected}'"

    if mode == "case-insensitive":
        ok = normalize_ci(agent_answer) == normalize_ci(expected)
        return ok, f"ci: '{agent_answer}' vs '{expected}'"

    if mode == "numeric-tolerance":
        try:
            a = float(agent_answer)
            e = float(expected)
            tol = float(gt_question.get("tolerance", 0))
            ok = abs(a - e) <= tol
            return ok, f"|{a} − {e}| = {abs(a - e):.6g} ≤ {tol}"
        except (ValueError, TypeError):
            return False, f"non-numeric: agent='{agent_answer}', expected='{expected}'"

    if mode == "enum":
        if isinstance(expected, list):
            ok = str(agent_answer) in [str(x) for x in expected]
            return ok, f"in {expected}"
        ok = str(agent_answer) == str(expected)
        return ok, f"single-enum: '{agent_answer}' vs '{expected}'"

    return False, f"unknown match_mode: {mode}"


def main() -> None:
    args = sys.argv[1:]
    if len(args) < 2:
        usage()

    outcome_path = Path(args[0])
    ground_path = Path(args[1])
    report_path = None
    if "--report" in args:
        idx = args.index("--report")
        if idx + 1 >= len(args):
            usage()
        report_path = Path(args[idx + 1])

    if not outcome_path.exists():
        print(f"ERROR: outcome.json not found: {outcome_path}", file=sys.stderr)
        sys.exit(2)
    if not ground_path.exists():
        print(f"ERROR: ground-truth.json not found: {ground_path}", file=sys.stderr)
        sys.exit(2)

    outcome = json.loads(outcome_path.read_text())
    ground = json.loads(ground_path.read_text())

    if outcome.get("schema_version") != "outcome-v1":
        print(
            "ERROR: outcome.json must have schema_version: outcome-v1",
            file=sys.stderr,
        )
        sys.exit(3)
    if ground.get("schema_version") != "ground-truth-v1":
        print(
            "ERROR: ground-truth.json must have schema_version: ground-truth-v1",
            file=sys.stderr,
        )
        sys.exit(3)

    agent_by_id = {q["id"]: q for q in outcome.get("questions", [])}

    results = []
    pass_count = 0
    fail_count = 0
    missing_count = 0

    for gt_q in ground["questions"]:
        qid = gt_q["id"]
        if qid not in agent_by_id:
            results.append(
                {
                    "id": qid,
                    "verdict": "MISSING",
                    "agent_answer": None,
                    "expected": gt_q["expected_answer"],
                    "match_mode": gt_q.get("match_mode"),
                    "reason": "no entry in outcome.json",
                }
            )
            missing_count += 1
            continue

        agent_a = agent_by_id[qid].get("answer")
        if agent_a is None:
            results.append(
                {
                    "id": qid,
                    "verdict": "MISSING",
                    "agent_answer": None,
                    "expected": gt_q["expected_answer"],
                    "match_mode": gt_q.get("match_mode"),
                    "reason": "answer is null",
                }
            )
            missing_count += 1
            continue

        passed, reason = match_question(agent_a, gt_q)
        verdict = "PASS" if passed else "FAIL"
        if passed:
            pass_count += 1
        else:
            fail_count += 1
        results.append(
            {
                "id": qid,
                "verdict": verdict,
                "agent_answer": agent_a,
                "expected": gt_q["expected_answer"],
                "match_mode": gt_q.get("match_mode"),
                "reason": reason,
            }
        )

    total = len(ground["questions"])
    ratio = pass_count / total if total > 0 else 0.0

    for r in results:
        print(
            f"{r['id']}: {r['verdict']} (agent: {r['agent_answer']!r} | "
            f"expected: {r['expected']!r})"
        )
    print(
        f"TOTAL: {pass_count}/{total} PASS (ratio: {ratio:.3f}; "
        f"fail: {fail_count}, missing: {missing_count})"
    )

    if report_path:
        report = {
            "schema_version": "outcome-report-v1",
            "task_id": ground.get("task_id"),
            "total": total,
            "pass": pass_count,
            "fail": fail_count,
            "missing": missing_count,
            "ratio": ratio,
            "questions": results,
        }
        report_path.write_text(json.dumps(report, indent=2) + "\n")

    sys.exit(0)


if __name__ == "__main__":
    main()
