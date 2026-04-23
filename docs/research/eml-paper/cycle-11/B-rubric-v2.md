# Rubric v2 — ARGUMENT.md for "Minimal Generating Basis for Elementary Functions"

Frozen for task_id refine-20260423-104345. Not to be modified during the loop.

Each dimension scored 0..3 (0=absent, 1=weak/gestural, 2=solid, 3=rigorous+explicit).
Weighted average → 0..1 score. Threshold = 0.93.

## Dimensions (with weights)

**R1 Motivation depth (w=1)** — §1 explains *why* a reduction is expected from first principles,
invokes additive/multiplicative duality, inverse-pair structure, complex extension, and
algebraic-vs-transcendental split. No cited named result used opaquely.

**R2 Systematic reduction procedure (w=1)** — §2 gives an ordered elimination procedure with each
step named, justified by an identity, and applicable to a primitive from the list. Does not skip
derivations of pow, log_x, arcsin, arctan.

**R3 Progressive stopping points (w=1)** — §3 exhibits ≥3 strictly decreasing sufficient bases
(e.g. Stage A ~12, Stage B ~6, Stage C ~5, Stage D 4). Each stopping point is independently
defensible with explicit "why push further" justification.

**R4 Minimal configuration (w=1.5)** — §4 states the exact basis (size, symbols, signatures, branch
conventions). Includes an **essentiality argument for each element** using semantic invariants
(entireness, closure under positive reals, arity), not case-exhaustion. Includes an alternate basis
of the same size if one exists.

**R5 Verification strategy (w=1.5)** — §5 supplies a derived-toolkit construction from the minimal
basis and a table mapping every listed primitive to an explicit formula in the basis. Formulas are
syntactically in the basis (no undefined abbreviations).

**R5' Numeric oracle (w=1)** — An executable verification script (e.g. `task/sim/verify.py`) samples
each §5 formula at pseudo-random complex points (fixed seed for reproducibility), compares to a
reference implementation (numpy/cmath), and reports per-formula pass/fail within a numeric
tolerance. Output captured to `task/sim/output.txt`. Absent=0, stub=1, covers ≥10 primitives=2,
covers all §5 primitives with pass=3.

**R6 Worked examples (w=1)** — §6 gives ≥3 worked examples expressed as numbered DAG chains
reducible syntactically to `{+, exp, ln, -1, x, y}` only (via defined macros). At least one example
shows Euler-form trig; at least one shows inverse-trig.

**R7 Counting convention declared (w=0.5)** — Before or at the minimality claim, the artifact names
the convention under which "minimum" is measured (e.g. "one primitive = one constant or one
operation symbol; variables are argument slots, not primitives"). If alternative conventions give
different minima, they are ranked.

**R8 Disclosed gaps (w=0.5)** — §7 disclosures are specific, not vague. Real-vs-complex question
either resolved or sharpened to a crisp obstruction. Branch-cut choices explicit per formula.

**R9 1/2 bootstrap chain clear (w=0.5)** — The construction of the constant 1/2 from the basis
avoids apparent circularity. Dependency order (−1 → 1 → 2 → 1/2 → i → π → e) is stated and each
step uses only prior constants.

**R10 Iteration trace discipline (w=0.5)** — Each iteration persisted to `task/iterations/` with
evaluator report naming closed gaps and cited §-locations.

**Hard constraints (each violation caps weighted_score at 0.85 until cleared):**
- H1 No citation of papers / named theorems used opaquely (Euler OK if derived in-text).
- H2 No web consultation.
- H3 Every formula in §5 and §6 reducible syntactically to `{+, exp, ln, -1}` (or the declared
  alternate basis) after macro expansion.

## Scoring

```
score = (w1·R1 + w2·R2 + w3·R3 + w4·R4 + w5·R5 + w5p·R5' + w6·R6 + w7·R7 + w8·R8 + w9·R9 + w10·R10)
        / (3 · Σw)
```

Σw = 1+1+1+1.5+1.5+1+1+0.5+0.5+0.5+0.5 = 9.5

If any hard constraint is violated, cap score at min(score, 0.85) until cleared.

## Target

- Threshold = 0.93 (stricter than v1's 0.85 since baseline v1 already reached 0.89).
- Max iterations = 4 (this cycle).
