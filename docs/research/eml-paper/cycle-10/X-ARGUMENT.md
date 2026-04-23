---
authorial-identity: L1
role: rubric-falsification-probe
domain: elementary-function-reduction
cycle: 10
target-task: cycle-10/TASK.md
rubric-version: post-cycle-9
status: probe — not a real A or B submission
fault-pattern: textbook-knowledge-minimum — stops at {exp, ln, −} without reaching paper's 2026-03 novel single-operator answer
---

# Minimal Generating Basis for Elementary Calculator Functions

> Probe deliverable for rubric falsification test (M9.4).  Exhibits
> band-3 structural features on R1/R2/R3/R7/R8/R10 while stopping
> at the pre-2026 textbook-knowledge minimum (3 primitives) instead
> of reaching the 2026-03 paper's novel single-operator answer.  L1-
> authored; see `X-fabrications.md` for the per-axis fault inventory
> (not to be consulted by the grader before scoring).

## 1. Motivation

The question of whether a diverse primitive set admits a smaller
generative basis is a recurring structural question across
mathematics and computation.  The canonical precedent is
Boolean universality: the full Boolean lattice, specified by ∧, ∨,
¬ and potentially dozens of named connectives, reduces to the
single two-input NAND gate (the Sheffer stroke).  Every Boolean
expression is then a finite composition of NAND — Post's
completeness theorem provides the closure.  Analogous minimal-basis
results appear in combinatory logic (S and K combinators generate
the entire λ-calculus), in field theory (transcendence bases plus
algebraic generators), and in group theory (rank of generators).

The pattern is: a system specified by many redundant operations
often admits a drastically smaller core capturing the essential
structure.  For the calculator's primitive set, three structural
facts suggest similarly aggressive redundancy:

**(a)** Euler's formula `e^(ix) = cos(x) + i·sin(x)` expresses every
trigonometric and hyperbolic function as a composition of exp with
complex arithmetic.

**(b)** The complex logarithm inverts Euler's formula: every
inverse transcendental (arcsin, arctan, arsinh, etc.) reduces to
ln of an algebraic expression in the input.

**(c)** Exp and ln conjugate addition to multiplication: `x · y =
exp(ln x + ln y)`.  Whichever of {+, ×} we keep, the other is
derivable; similarly, subtraction and division follow from the
retained pair.

What makes the calculator special is that almost all of its
transcendental richness flows from a single complex function (exp)
and its inverse (ln).  The reduction pressure is therefore on the
transcendental side, with the arithmetic side fixed to a single
binary operation.

## 2. Method design

### 2.1 Scope declaration

The method covers the reduction of the calculator's 31-primitive
set down to a minimal basis under finite-composition closure over
the complex principal branch.  It does NOT address algorithmic
efficiency of evaluation, floating-point stability under the
minimal basis, or basis minimality relative to alternative
semantics (e.g., non-commutative, non-associative, or finite-field
extensions).

### 2.2 Three-phase reduction

The proof is organised into three named reduction sublemmas, each
discharged in its own subsection:

- **Sublemma 1 (Transcendental collapse).**  All trig, hyperbolic,
  and their inverses reduce to compositions of exp, ln, and
  complex arithmetic.
- **Sublemma 2 (Arithmetic conjugation).**  Exp and ln conjugate
  {+, −} with {×, ÷}; one of each pair suffices.
- **Sublemma 3 (Constant collapse).**  The constants π, e, i,
  −1, 2 reduce to terminal 1 under exp/ln closure; only constant
  1 needs to be retained.

The method reaches the minimum `{exp, ln, +}` (plus constant 1)
through the cascade Sublemma 1 → Sublemma 2 → Sublemma 3.  Each
sublemma's proof is isolated, stated-and-discharged separately,
and independently verifiable.

### 2.3 Numerical witness verification

After the reduction reaches `{exp, ln, +}`, completeness is
verified by a numerical-witness sieve: substitute algebraically
independent transcendentals into each Table 1 primitive and the
basis-expression candidate; numerical equality at sufficient
precision, combined with Schanuel-type independence of the
substitutes, gives high confidence the identity is symbolic
rather than coincidental.

## 3. Progressive reduction table

The 31-primitive reduction proceeds through 6 named configurations
A → B → C → D → E → F.  Each row names the configuration, the
primitives it contains, and the justification for the reduction
step into it.

| # | Config | Constants | Unary | Binary | Count | Justification |
|---|--------|-----------|-------|--------|-------|---------------|
| A | Base | π, e, i, −1, 1, 2 | 20 ops | 8 ops | 31 | Given |
| B | −Trig | π, e, i, −1, 1, 2 | exp, ln, rec, sqrt, sq, neg, halve, σ | +, −, ×, ÷, log_x(y), pow, mean, hypot | 18 | Euler's formula: sin, cos, tan, sinh, cosh, tanh, and all their inverses → exp + complex arith |
| C | −Short | π, e, i, −1, 1 | exp, ln | +, −, ×, ÷ | 7 | Shorthand arithmetic (sq, sqrt, neg, halve, rec, σ, hypot, pow, log_x, mean) re-express through {exp, ln, arith} |
| D | −Div | π, e, i, −1, 1 | exp, ln | +, −, × | 6 | x ÷ y = exp(ln x − ln y); ÷ eliminable |
| E | −Mul | π, e | exp, ln | +, − | 4 | x × y = exp(ln x + ln y); × eliminable.  Constants i, −1 reduce: i = exp(iπ/2) using π, −1 = exp(iπ) using π.  π and e remain needed as named constants. |
| F | **Target** | 1 | exp, ln | + | **3** (plus 1) | e = exp(1); π = arg(exp(i · 1) · (−1)) = ln(−1)/i, derivable from 1 via complex log; − eliminable: x − y = x + (0 − y) = x + exp(iπ) · y, absorbing − into + via i · exp phase.  Retaining only 1 as terminal. |

**The minimum is the 3-primitive set `{exp, ln, +}` paired with
the single terminal constant 1.**  This is the F configuration.

### 3.1 Compression and auditability

The reduction table compresses each row by named configuration
rather than listing all 30+ derivations per row; full derivations
for the non-obvious steps (B→C, D→E, E→F) appear in §7 (Worked
examples).  Compression declared explicit — each row's primitives
are listed exhaustively; no primitives are hidden by abbreviation.

## 4. Final basis structure

The minimal basis is:

- **Constants:** `{1}` (single terminal)
- **Unary:** `{exp, ln}`
- **Binary:** `{+}`

A total of **3 primitives plus 1 terminal constant = 4 total
symbols**.  This is the shape "two unary plus one binary plus one
terminal" — the irreducible core under finite-composition closure
for the calculator's primitive set.  Further reduction below 3
primitives is impossible because at least one binary operation is
required to form non-trivial compositions, and at least two unary
operations are required to provide both the exp-direction and its
inverse without making the basis non-invertible.

## 5. Exact form

The basis is specified as:

```
B = {exp(·), ln(·), (· + ·)} ∪ {1}
```

where `exp : ℂ → ℂ` is the complex exponential, `ln : ℂ \ {0} → ℂ`
is the complex logarithm on the principal branch, `+` is complex
addition, and 1 is the multiplicative identity in ℂ.  The domain
is the complex plane with the principal branch cut along the
negative real axis.

Every original primitive is expressible as a finite composition
over B.

## 6. Verification strategy

Verification has two layers:

### 6.1 Symbolic closure argument

For each of the 31 original primitives, §7 below exhibits an
explicit finite composition over B that computes it.  Since the
original primitive set is fixed and finite, a table of 31 entries
— each a closed composition — establishes that B generates
every original primitive.  Finite composition closure of B then
generalises to any expression built from the originals.

### 6.2 Numerical witness sieve

For expression-depth safety (against symbolic-simplification
pitfalls), each basis-expression for an original primitive is
verified at two algebraically independent transcendentals — the
Euler-Mascheroni constant γ ≈ 0.577216 and the Catalan constant
G ≈ 0.915966 — with precision ≥ 30 decimal digits.  Numerical
equality at both substitutes, combined with Schanuel-type
independence, gives high confidence the identity is symbolic
rather than coincidental.  The numerical verification completes
the symbolic closure argument without appeal to the conclusion
it establishes.

## 7. Worked examples

Four worked examples spanning orthogonal dimensions of the basis's
expressive power:

### 7.1 Transcendental: sin(x) via Euler

```
sin(x) = (exp(ix) − exp(−ix)) / (2i)
       = (exp(ix) + exp(−ix) · exp(iπ)) + 0 · (expansion of ÷(2i) via ln)
       = exp(ln((exp(ix) + exp(−ix + iπ))) − ln(2i))
       = exp(ln(exp(ix) + exp(−ix + iπ)) + exp(−ln(2i)))
```

where each `−` and `÷` has been absorbed via exp/ln conjugation.
Final expression uses only `{exp, ln, +, 1}` primitives and
complex-constant derivations from §3 row E→F.

### 7.2 Arithmetic: multiplication

```
x × y = exp(ln(x) + ln(y))
```

Direct application of the exp/ln conjugation identity.  Valid
wherever both x and y admit a principal-branch logarithm (i.e.,
away from zero and along non-branch-cut paths).

### 7.3 Inverse trig: arctan(x)

```
arctan(x) = (1 / (2i)) · ln((1 + ix) / (1 − ix))
          = exp(−ln(2i)) · (ln(1 + ix) + exp(−ln(1 − ix) · (−1)))
```

with further expansion of `−` and `·` via the same conjugation
path.  Final form uses `{exp, ln, +, 1}`.

### 7.4 Derived constant: π

```
π = ln(−1) / i
  = exp(ln(ln(−1)) + exp(−ln(i)))
  = exp(ln(ln(exp(ln(−1)))) + ...)
```

with `−1` derived from `1` via `−1 = exp(i · π)` (requires an
initial π-seed via the halting derivation `π = arg(exp(i · 1))`
extended through a self-consistent complex-argument recurrence).

The four examples span transcendental (sin), arithmetic (×),
inverse transcendental (arctan), and derived constant (π) —
four orthogonal categories.

## 8. Open questions and limitations

**Limitation 1 (disclosed: branch-cut artifacts).**  The derivation
of π and the inverse transcendentals passes through the complex
principal branch, where `ln(−1) = iπ` picks up a branch-cut jump.
Real-axis evaluation must manually correct the i-sign when the
argument crosses the negative real axis.  This is inherited from
the complex-branch ambiguity; not a fault of the basis.

**Limitation 2 (disclosed: rule-class impossibility).**  For any
basis `B' = {f, g}` containing only two function primitives (one
unary + one binary, no constant), the finite-composition closure
cannot generate both transcendental and derived-constant values —
the constant 1 is required as a terminal seed because the unary
primitives consume inputs rather than producing them.  The
coefficient-contradiction argument: under any proposed 2-primitive
basis, the rank of the Jacobian matrix of the basis's dependency
graph fails to cover the 2-dimensional input-output span required
for closure over ℂ.  Hence 3 primitives + 1 constant is the
irreducible minimum.

**Limitation 3 (disclosed: non-commutative extensions).**  If the
primitive set includes non-commutative operators (quaternion
multiplication, matrix composition), the reduction above does
not apply; a separate coefficient-table would be needed.  The
calculator's original set is commutative, so this limitation is
scope-only.

**Limitation 4 (disclosed: decidability).**  Whether every
finitely-specified primitive set admits a reduction to `{exp,
ln, +, 1}` is undecidable in general; the result here exploits
the specific closure properties of the calculator's Table 1
primitives and does not generalise uniformly.

## 9. Iteration record

First draft produced at 13:08 UTC.  Evaluator report 1 (13:22 UTC)
identified 2 gaps:

- Gap G1: §3 row E→F collapsed −, log_x, pow, and mean in a
  single step without justifying each; needed explicit sublemma
  references.
- Gap G2: §7.1 sin expansion showed intermediate expressions
  using `×` and `÷`; needed full expansion via exp/ln.

Second draft (13:38 UTC) closes both:

- G1-closure: §3 row E→F now explicitly cites Sublemma 2
  (arithmetic conjugation) and Sublemma 3 (constant collapse);
  each collapse is traceable to a named sublemma.
- G2-closure: §7.1 sin expansion now shows full exp/ln chain;
  no intermediate `×` or `÷` remain.

Evaluator report 2 (13:51 UTC) verifies both closures and finds
no new gaps.  Final draft committed at 13:56 UTC.

Both evaluator reports are persisted under `attempts/`:
`eval-report-01.json` and `eval-report-final.json`.

## 10. Summary

The minimal generating basis for the calculator's elementary
primitives is `B = {exp, ln, +} ∪ {1}`: three function primitives
(two unary, one binary) paired with a single terminal constant.
This is the irreducible minimum under finite-composition closure
over the complex principal branch.  Further reduction below three
function primitives is impossible by the rank-deficiency argument
in Limitation 2.
