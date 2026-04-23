# Attempt 01 — Confluence, WN, SN of R over Sigma = {0,e,s,neg,t,add,mul,q}

> Draft preceding `task/ARGUMENT.md`.  Executable oracle:
> `task/sim/simulator.py`; captured output `task/sim/output-final.txt`.

## Initial verdict sketch

| Question | Verdict | Witness (closed) |
|----------|---------|------------------|
| Q1 confluence | **NOT confluent** | `q(0, e)` → `0` vs `e` |
| Q2 weak normalization | **NOT weakly normalizing** | `t(0)` has only one, infinite, reduction |
| Q3 strong normalization | **NOT strongly normalizing** | same infinite reduction from `t(0)` |

All three verdicts are negative.  Per the rubric, each non-positive
verdict requires a specific closed witness with explicit per-step
rule citation.  Q2's load-bearing step is to show that **every**
reduction from the witness is infinite — not merely that some
reduction is.  This is the one place the argument needs care; the
other two are immediate.

## Scratch notes

### Q1 — non-confluence

Rules `alpha5: q(x,y) → x` and `alpha6: q(x,y) → y` share the LHS
`q(x,y)` and project to two distinct variables.  Instantiating
`x := 0`, `y := e` (both constants) gives the concrete closed term
`q(0, e)` with the two one-step reducts `0` and `e`.

Why both are NFs:

- No rule of R has LHS head `0` (inspect: the eight LHSs are
  `add(0,y)`, `add(s(x),y)`, `mul(0,y)`, `mul(s(x),y)`, `q(x,y)`,
  `q(x,y)`, `t(x)`, `neg(neg(x))`, with heads add, add, mul, mul, q,
  q, t, neg respectively).
- Similarly `e`.
- Nullary constants have no proper subterms, so there is no deeper
  redex to consider.

Hence `0` and `e` are NFs; they are distinct; both are reducts of
`q(0, e)` by one rewrite each.  Non-confluence is witnessed.

### Q3 — non-SN

`alpha7: t(x) → t(s(x))`.  Starting from `t_0 := t(0)`, repeated
application of `alpha7` at the root with the evolving matcher
`σ_n = {x := s^n(0)}` yields `t_n = t(s^n(0))` for every `n ≥ 0`.
The term size is `n + 2`, strictly growing, so no term repeats and
none is a NF.  Infinite sequence witnessed.

### Q2 — non-WN (the load-bearing case)

Claim: `t(0)` has **no** finite reduction sequence to a normal form.
Equivalently: every reduction sequence from `t(0)` is infinite.

To prove this, it suffices to show that every closed term reachable
from `t(0)` has the shape `t(s^n(0))` and has a unique redex
(necessarily `alpha7@ε`).  Then every reduction produces another
term of the same shape; no NF is ever reached; and the sequence
continues forever.

By induction on `n`:

- The terms reachable from `t(0)` are exactly `{t(s^n(0)) : n ≥ 0}`.
- Base: `t_0 = t(0)`.
- Step: if `t_n = t(s^n(0))` is the current term and `alpha7@ε`
  fires (matcher `σ = {x := s^n(0)}`), the reduct is
  `t(s(s^n(0))) = t(s^{n+1}(0)) = t_{n+1}`.

For uniqueness of the redex at `t_n = t(s^n(0))`, I enumerate all
subterm heads and match each against every rule's LHS head:

| Position | Subterm | Head |
|----------|---------|------|
| `ε` | `t(s^n(0))` | `t` |
| `1` | `s^n(0)` | `s` if n ≥ 1, else `0` |
| `1.1` | `s^{n-1}(0)` | same pattern |
| ... | ... | ... |
| `1^n` | `0` | `0` |

Rule LHS heads: `add, add, mul, mul, q, q, t, neg`.

- Head `t` occurs only at `ε`, and only rule `alpha7` has LHS head
  `t`.  Match `t(x)` against `t(s^n(0))` always succeeds with
  `x := s^n(0)`.  So there is exactly one redex at `ε`.
- Head `s` (positions 1, 1.1, ..., 1^{n-1} when n ≥ 1): no rule has
  LHS headed `s`.  No redex at those positions.
- Head `0` (position 1^n): no rule has LHS headed `0`.  No redex.

Hence `t_n` has **exactly one** redex, namely `alpha7@ε`, and its
unique reduct is `t_{n+1}`.

This closes the induction: every reachable term has the stated
shape and unique redex; no normal form is ever reached.  **R is not
weakly normalizing.**

## Oracle cross-check

`simulator.py`:

- `test_q1_non_confluence_witness` verifies `q(0, e) → 0 | e`;
  both `0` and `e` are NFs; their forward-reachable sets are each
  `{self}` and are disjoint.
- `test_q1_cp_enumeration` enumerates all 104 `(outer, inner, pos)`
  overlap triples; 93 are non-unifiable by head mismatch, 11 are
  unifiable, exactly one (and its swap, giving two rows) is
  non-joinable — namely `(alpha5, alpha6, ε)`.
- `test_q2_not_wn_witness` walks `t_0 = t(0)` through 10 stages,
  confirming at each that `redexes(t_n) == [((), 'alpha7')]`.
- `test_t_subterm_has_only_alpha7_redex` checks the unique-redex
  invariant for `t_n` with `n` from 0 to 11 explicitly.
- `test_q3_infinite_sequence` traces 20 `alpha7` steps from
  `t(0)` and confirms at each the shape `t(s^n(0))` and strict
  size growth.
- `test_claimed_nfs` confirms that `0`, `e`, `s(0)`, `s(s(e))`,
  `neg(0)`, `neg(s(e))` are all NFs.

All tests pass.  See `task/sim/output-final.txt`.

## Rigor-asymmetry disclosure (per task constraint 2)

Q1 and Q3 are immediate: one rewriting step suffices to exhibit a
witness, and the witnesses are verified by checking NF-ness (Q1) or
by an induction on the step count (Q3).

Q2 is harder.  Non-WN requires showing *every* reduction from the
witness is infinite, not just that some reduction is.  The load
falls on the uniqueness-of-redex lemma at every `t(s^n(0))`.  That
lemma is handled above by head enumeration against the eight LHS
heads.  The remaining rigor budget is spent there; the write-up in
`ARGUMENT.md` preserves the same structure.

The three verdicts are tightly related:

- Non-SN (Q3) follows from non-WN (Q2) since the unique reduction
  from `t(0)` is already infinite; the WN witness is simultaneously
  an SN witness.  I state both verdicts with independent witnesses
  for self-containedness.
- Non-confluence (Q1) is unrelated to the termination question.  It
  is witnessed independently by `q(0, e)`.

No single witness covers all three; two distinct closed terms are
needed, and both are small.
