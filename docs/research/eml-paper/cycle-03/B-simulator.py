"""Simulator for the single-instruction register machine defined in ARGUMENT.md.

The only instruction is STEP with semantics:

    STEP Ri, Rj, L1, L2:
        if Ri > 0: Ri := Ri - 1; goto L1
        else    : Rj := Rj + 1; goto L2

Halts on arriving at a label with no instruction attached (convention of §4.1).
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional


@dataclass
class StepIns:
    label: str
    Ri: str
    Rj: str
    L1: str
    L2: str


def parse_program(text: str) -> Tuple[List[StepIns], List[str]]:
    """Parse a STEP program. Each non-empty non-comment line is either

        <Label>: STEP <Ri>, <Rj>, <L1>, <L2>

    or a bare terminal label

        <Label>:

    Terminal labels are returned separately; STEP instructions carry their own
    labels in program order.
    """
    instructions: List[StepIns] = []
    terminal_labels: List[str] = []
    for raw in text.splitlines():
        line = raw.split("#")[0].strip()
        if not line:
            continue
        if ":" not in line:
            raise ValueError(f"line lacks label: {raw!r}")
        label, rest = line.split(":", 1)
        label = label.strip()
        rest = rest.strip().rstrip(",")
        if rest == "":
            terminal_labels.append(label)
            continue
        tok = rest.replace(",", " ").split()
        if tok[0] != "STEP" or len(tok) != 5:
            raise ValueError(f"bad instruction: {raw!r}")
        instructions.append(StepIns(label, tok[1], tok[2], tok[3], tok[4]))
    return instructions, terminal_labels


def simulate(
    program: List[StepIns],
    terminal_labels: List[str],
    initial: Dict[str, int],
    *,
    max_steps: int = 1_000_000,
) -> Tuple[Dict[str, int], int, Optional[str]]:
    """Run the program from the first instruction; return (regs, steps, halt_reason)."""
    if not program:
        return dict(initial), 0, "empty"
    regs: Dict[str, int] = defaultdict(int)
    for k, v in initial.items():
        regs[k] = v
    label_to_index = {ins.label: i for i, ins in enumerate(program)}
    for lbl in terminal_labels:
        label_to_index[lbl] = len(program)
    pc = 0
    for step in range(max_steps):
        if pc >= len(program):
            return dict(regs), step, "halted"
        ins = program[pc]
        if regs[ins.Ri] > 0:
            regs[ins.Ri] -= 1
            target = ins.L1
        else:
            regs[ins.Rj] += 1
            target = ins.L2
        if target not in label_to_index:
            raise RuntimeError(f"jump to undefined label {target!r} at step {step}")
        pc = label_to_index[target]
    return dict(regs), max_steps, "timeout"


# -----------------------------------------------------------------------------
# Programs transcribed from ARGUMENT.md
# -----------------------------------------------------------------------------

ADDITION = """
L0:    STEP R1, Rg, Linc1, L1
Linc1: STEP Rz, Rout, L0, L0
L1:    STEP R2, Rg, Linc2, Lhalt
Linc2: STEP Rz, Rout, L1, L1
Lhalt:
"""

MULTIPLICATION = """
Louter: STEP R1, Rg, Lcopy, Lhalt
Lcopy:  STEP R2, Rg, LincR, Lback
LincR:  STEP Rz, Rout, LincT, LincT
LincT:  STEP Rz, T,    Lcopy, Lcopy
Lback:  STEP T,  Rg,   LincB, Lnext
LincB:  STEP Rz, R2,   Lback, Lback
Lnext:  STEP Rz, Rg,   Louter, Louter
Lhalt:
"""

MONUS = """
Lmov:  STEP R1, Rg, LincO, Lsub
LincO: STEP Rz, Rout, Lmov, Lmov
Lsub:  STEP R2, Rg, Ldec, Lhalt
Ldec:  STEP Rout, Rg, Lsub, Lsub
Lhalt:
"""


def run_case(program_text: str, inputs: Dict[str, int], out_reg: str) -> int:
    program, terminals = parse_program(program_text)
    regs, steps, reason = simulate(program, terminals, inputs)
    if reason != "halted":
        raise RuntimeError(f"did not halt: reason={reason}, steps={steps}")
    return regs[out_reg]


def check_addition():
    cases = [(0, 0), (0, 3), (3, 0), (3, 5), (1, 1), (7, 11), (0, 20), (20, 0)]
    for a, b in cases:
        got = run_case(ADDITION, {"R1": a, "R2": b, "Rout": 0}, "Rout")
        want = a + b
        ok = got == want
        print(f"  add({a}, {b}) = {got}  (expected {want})  {'OK' if ok else 'FAIL'}")
        if not ok:
            return False
    return True


def check_multiplication():
    cases = [(0, 0), (0, 5), (5, 0), (1, 7), (7, 1), (3, 4), (4, 3), (6, 6), (2, 10)]
    for a, b in cases:
        got = run_case(MULTIPLICATION, {"R1": a, "R2": b, "Rout": 0, "T": 0}, "Rout")
        want = a * b
        ok = got == want
        print(f"  mul({a}, {b}) = {got}  (expected {want})  {'OK' if ok else 'FAIL'}")
        if not ok:
            return False
    return True


def check_monus():
    cases = [(0, 0), (5, 0), (0, 5), (5, 3), (3, 5), (5, 5), (10, 2), (2, 10), (7, 7)]
    for a, b in cases:
        got = run_case(MONUS, {"R1": a, "R2": b, "Rout": 0}, "Rout")
        want = max(0, a - b)
        ok = got == want
        print(f"  monus({a}, {b}) = {got}  (expected {want})  {'OK' if ok else 'FAIL'}")
        if not ok:
            return False
    return True


if __name__ == "__main__":
    print("== addition ==")
    a_ok = check_addition()
    print("== multiplication ==")
    m_ok = check_multiplication()
    print("== monus ==")
    s_ok = check_monus()
    print()
    if a_ok and m_ok and s_ok:
        print("ALL PASSED")
        raise SystemExit(0)
    print("SOME FAILED")
    raise SystemExit(1)
