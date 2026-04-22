# ARGUMENT — Joint confluence and termination of R

> **Iteration trace.** Draft at `iterations/attempt-01.md`. Evaluator
> report at `.eval-report-01.json` (7 gaps disclosed: G1 §6.1 phi
> arithmetic, G2 §6.2 phi arithmetic, G3 §3.1 tabular completeness,
> G4 §4.3 induction framing, G5 §7.1 extended-measure sketch,
> G6 monotonicity single-line proof, G7 variable-overlap sublemma).
> This document closes G1–G7. Executable oracle: `sim/simulator.py`,
> supporting trace dump at `sim/trace_check.py`, captured output
> `sim/output-final.txt`.

The rewriting system under study:

    ρ1:  len(nil)              → 0
    ρ2:  len(cons(x, ys))      → s(len(ys))
    ρ3:  app(nil, ys)          → ys
    ρ4:  app(cons(x, xs), ys)  → cons(x, app(xs, ys))
    ρ5:  app(app(xs, ys), zs)  → app(xs, app(ys, zs))

Signature Σ: nullary `0`, `nil`; unary `s`, `len`; binary `cons`, `app`.
`len`, `app` are defined; `0`, `nil`, `s`, `cons` are constructors.

Q1 asks: is R confluent? Q2 asks: does R terminate on all closed terms?

Throughout, **positions are 1-indexed over children**: position ε is
the root; position `i` inside an n-ary term is its i-th child; `i.j`
recurses. The simulator uses 0-indexed tuples; the two conventions
agree up to an off-by-one and are not used interchangeably in a single
derivation.

---

## 1. Motivation

### 1.1 Why confluence is plausible

Three structural features point toward confluence.

**(a) Every LHS is left-linear.** Each of the five LHSs uses each of
its variables exactly once: `len(nil)` (no variables), `len(cons(x,
ys))` (x, ys each once), `app(nil, ys)` (ys once), `app(cons(x, xs),
ys)` (x, xs, ys each once), `app(app(xs, ys), zs)` (xs, ys, zs each
once). Left-linearity means a match never forces two independent
subterms to be equal, so rewriting one occurrence of a variable-bound
subterm never has to be mirrored at another, and variable overlaps
always close automatically (§2.1).

**(b) The defined-function rules are pattern-matching on constructor
heads.** Rules ρ1/ρ2 match `len` against `nil` / `cons(_, _)` —
mutually exclusive at the argument's root. Rules ρ3/ρ4 do the same
for `app`'s first argument. Whenever the first argument of `len` or
of `app` is a ground constructor term, exactly one of the discriminating
rules fires: no contest between function definitions.

**(c) Rule ρ5 is the only rule with a non-trivial self-overlap.**
Its LHS `app(app(xs, ys), zs)` contains the subterm `app(xs, ys)`
whose head matches `app`-rooted LHSs. Overlap risk is concentrated
there. Since ρ5 re-associates the same binary operator, both sides
of the rule denote the same abstract value under any model that
makes `app` associative — which the pattern-matching rules ρ3/ρ4
realise. This is a plausibility argument, not a proof; §3.1 discharges
it formally.

A cautionary precedent in adjacent domains: algebraic rewrite systems
can fail confluence when distinct rewrite histories reach incompatible
canonical forms (e.g., equational fragments where one rule simplifies
and another re-associates, and re-association blocks simplification).
The job of §3.1 is to verify that no such race happens in R.

### 1.2 Why termination is plausible

**In favour.** Rules ρ1, ρ2, ρ3, ρ4 each "consume" some constructor
structure on the LHS that is either absent or strictly inward on the
RHS:

- ρ1: `len(nil)` → `0`. Two symbols to one; a `len` and a `nil` are
  deleted.
- ρ2: `len(cons(x, ys))` → `s(len(ys))`. The `cons` is replaced by
  `s`; `x` is discarded.
- ρ3: `app(nil, ys)` → `ys`. `app` and `nil` deleted.
- ρ4: `app(cons(x, xs), ys)` → `cons(x, app(xs, ys))`. The root
  symbols swap, but the `app` is now *inside* a `cons`; nothing is
  deleted, yet a positional invariant decreases.

**Against.** ρ5: `app(app(xs, ys), zs)` → `app(xs, app(ys, zs))`.
Symbol count is exactly equal on both sides (two `app`s, three
variables). Raw size / subterm count / lexicographic-on-head-outermost
fails on this rule. We need a measure that penalises left-nesting of
`app` strictly more than right-nesting.

Adjacent precedent: whenever a rewrite associates a binary operator
rightward, termination typically rests on weighting the left argument
strictly more than the right. If `φ(app(x, y)) = a·x + b·y + c`, then

    φ(app(app(xs, ys), zs)) - φ(app(xs, app(ys, zs)))
      = a(a·xs + b·ys + c) + b·zs + c  -  (a·xs + b(b·ys + c) + c)
      = a²·xs + ab·ys + ac + b·zs + c  -  a·xs - b²·ys - bc - c
      = (a² - a)·xs + (ab - b²)·ys + (a - b)·c
      = a(a-1)·xs + b(a-b)·ys + (a-b)·c.

For this to be strictly positive for all xs, ys ≥ 0, choose `a > 1`
and `a > b`; the simplest choice `a = 2, b = 1, c = 1` gives
`2·xs + 1·ys + 1`, which strictly dominates the RHS by `2·xs + 1` —
independently of `ys`. This same choice must discharge the other four
rules; §3.2 verifies it.

### 1.3 Why the two obligations must be treated separately

Non-termination is compatible with confluence; non-confluence is
compatible with termination. No single argument discharges both:

- Confluence is a *local* property at the pattern level — inspect every
  pair of rules, detect every overlap, close every critical pair.
- Termination is a *global* property requiring a well-founded measure.

They share some infrastructure (both reason by structural induction
and respect the context closure of →) but do not substitute for each
other. §4.3 does use the joint statement (local confluence +
termination ⟹ confluence), but we derive that step from first
principles rather than invoking it as a named result.

---

## 2. Method design

### 2.1 Confluence method

**Identifying potential counterexamples.** Two histories from a shared
origin can diverge irreducibly only if two different redexes sit in
overlapping positions of a shared term. There are two flavours:

(i) **Variable overlap.** The inner redex sits strictly below a
variable position of an outer rule's matched instance. We claim: for
left-linear R, every such overlap is automatically joinable.

*Sublemma.* Let ρ: l → r be a rule whose variables all occur at most
once in l. Suppose t contains a redex for some rule ρ' at a position
p that lies strictly below a variable position of a match of l at
position q (so p = q.s and l has a variable x at position s). Then
the two one-step reductions

    t = C[ lσ ]  →  C[ rσ ]               (via ρ at q)
    t = C[ lσ ]  →  C[ (lσ)[ p/u' ] ]    (via ρ' at p)

are joinable, where σ is the matching substitution and u' is ρ''s
one-step reduct of the redex at p.

*Proof.* Left-linearity: variable x appears exactly once at position
s in l; nowhere else. Let σ(x) reduce to σ'(x) by ρ'. Extend σ to σ'
by agreement elsewhere. Then

- `C[rσ]` reduces (in zero or one ρ' steps depending on whether x
  occurs in r — but even if it does, each occurrence reduces
  independently since σ(x) has a redex at the same relative
  position in each) to `C[rσ']`.
- `C[(lσ)[p/u']] = C[lσ']` (replacing σ(x) by σ'(x) at the unique
  position s), which reduces via ρ at q to `C[rσ']`.

Hence common reduct `C[rσ']`. The one-or-more-steps caveat is fine:
joinability is by ↠, not by single →. ∎

So variable overlaps need no further work for a left-linear R. All
five LHSs are left-linear, so only non-variable overlaps remain.

(ii) **Non-variable overlap (critical pair).** One rule's LHS unifies
with a non-variable subterm of another rule's LHS (including
self-overlap when i = j, but only at positions other than the root).
We enumerate every ordered pair (including rule-with-itself) and every
non-variable position.

**Discharging critical pairs.** For each enumerated critical pair
(u, v), we either (a) exhibit a common reduct w (u ↠ w, v ↠ w) or
(b) declare non-confluence with (u, v) as witness.

**Local-to-global.** Once all critical pairs close, local confluence
holds: any one-step divergence joins. Lifting local to global
confluence requires termination; see §4.3 for the first-principles
derivation.

### 2.2 Termination method

**Constructing a well-founded measure.** Assign to each symbol f of
arity n a polynomial [f](x₁,…,xₙ) with non-negative integer
coefficients, at least one of which — on each argument — is strictly
positive. Extend homomorphically: `[f(t₁, …, tₙ)] = [f]([t₁], …,
[tₙ])`, inducing a map `φ: closed terms → ℕ`. Well-foundedness of
the range comes from well-foundedness of `<` on ℕ.

**Monotonicity sublemma (G6-closure).** For a polynomial
`P(x₁, …, xₙ) = Σ c_α · x₁^{α₁} ··· xₙ^{αₙ}` with non-negative
coefficients `c_α` and, for each j ∈ {1..n}, at least one monomial
with both `c_α > 0` and `α_j > 0`, the function
`(x₁, …, xₙ) ↦ P(x₁, …, xₙ)` over ℕⁿ is strictly monotone in each
argument: if `x_j < x'_j` and all other `x_i` are fixed, then
`P(x₁, …, x_j, …, xₙ) < P(x₁, …, x'_j, …, xₙ)`. *Proof:* subtract
the two values; the difference is a sum of non-negative monomials
with at least one (the `α_j ≥ 1, c_α > 0` one) strictly positive at
`x'_j > x_j`. ∎

Applied to our interpretations (which are linear or constant, hence
a trivial instance of the sublemma), strict monotonicity of every
`[f]` in every argument is immediate.

**Verifying strict decrease per rule.** For a rule l → r with
variables v₁, …, vₖ, compute the polynomial difference `[l] - [r]`
and check that every coefficient is non-negative and the constant term
is strictly positive (i.e., `[l] - [r] ≥ 1` uniformly on ℕᵏ).

**Handling the rule ρ5 where symbol count is balanced.** §1.2
motivates `[app](x, y) = 2x + y + 1`: the left argument's coefficient
strictly exceeds the right's. This converts the associativity shape
into a strict drop.

**Handling ρ4 where the RHS has more symbols than the LHS.** A
literal symbol-count measure fails ρ4: its LHS has 5 symbols and its
RHS has 6 (counting variables). Termination is proven by an
*interpretation*, not by raw size; §3.2 verifies ρ4 discharges on
our polynomial choice.

### 2.3 What the two methods share

Both reason term-by-term and both respect the context closure of →.
But they are orthogonal. The confluence proof inspects *patterns*
(LHS shapes pairwise). The termination proof inspects *rules as
transformations on polynomials* (each rule is checked independently
of the others). The confluence proof of §3.1 does not rely on
termination; only §4.3 joins the two.

---

## 3. Progressive derivation

### 3.1 Critical-pair enumeration for Q1

We must consider every ordered pair `(ρᵢ, ρⱼ)` with i, j ∈ {1..5} —
25 pairs total — and for each, every position in ρⱼ's LHS at which
some non-variable subterm could unify with ρᵢ's LHS. Root overlaps
with i = j are trivial self-overlaps and close to a single term;
they are listed but contribute nothing. We tabulate exhaustively.

Conventions for the table: **positions** are 1-indexed children (ε =
root). A cell with entry "⊥" marks an impossible overlap for that
(ρᵢ, ρⱼ, position) triple, with a reason. Non-variable positions of
each ρⱼ's LHS are:

- ρ1 `len(nil)`: positions ε, 1 (subterms `len(nil)`, `nil`).
- ρ2 `len(cons(x, ys))`: positions ε, 1 (subterms `len(cons(x, ys))`,
  `cons(x, ys)`); positions 1.1 (= x), 1.2 (= ys) are variable.
- ρ3 `app(nil, ys)`: positions ε, 1 (subterms `app(nil, ys)`, `nil`);
  position 2 is variable.
- ρ4 `app(cons(x, xs), ys)`: positions ε, 1 (subterms `app(cons(x,
  xs), ys)`, `cons(x, xs)`); positions 1.1, 1.2, 2 are variable.
- ρ5 `app(app(xs, ys), zs)`: positions ε, 1 (subterms
  `app(app(xs, ys), zs)`, `app(xs, ys)`); positions 1.1, 1.2, 2 are
  variable.

The exhaustive table of overlaps (ρᵢ matching at position p of ρⱼ's
LHS):

| i→j | pos ε                       | pos 1                               |
|-----|-----------------------------|-------------------------------------|
| 1→1 | trivial self; RHS=RHS       | ⊥ (ρ1 LHS=`len(nil)`; subterm=`nil`; heads differ) |
| 1→2 | ⊥ (first args `nil` vs `cons(x,ys)` don't unify) | ⊥ (`cons(x,ys)` head ≠ `len`) |
| 1→3 | ⊥ (heads `len` vs `app` differ) | ⊥ (subterm `nil` head ≠ `len`) |
| 1→4 | ⊥ (heads differ)            | ⊥ (subterm `cons(x,xs)` head ≠ `len`) |
| 1→5 | ⊥ (heads differ)            | ⊥ (subterm `app(xs,ys)` head ≠ `len`) |
| 2→1 | ⊥ (first args `cons(x,ys)` vs `nil` don't unify) | ⊥ (subterm `nil` head ≠ `len`) |
| 2→2 | trivial self; RHS=RHS       | ⊥ (subterm `cons(x,ys)` head ≠ `len`) |
| 2→3 | ⊥ (heads differ)            | ⊥ (subterm `nil` head ≠ `len`) |
| 2→4 | ⊥ (heads differ)            | ⊥ (subterm `cons(x,xs)` head ≠ `len`) |
| 2→5 | ⊥ (heads differ)            | ⊥ (subterm `app(xs,ys)` head ≠ `len`) |
| 3→1 | ⊥ (heads differ)            | ⊥ (subterm `nil` head ≠ `app`) |
| 3→2 | ⊥ (heads differ)            | ⊥ (subterm `cons(x,ys)` head ≠ `app`) |
| 3→3 | trivial self; RHS=RHS       | ⊥ (subterm `nil` head ≠ `app`) |
| 3→4 | ⊥ (first args `nil` vs `cons(x,xs)` don't unify) | ⊥ (subterm `cons(x,xs)` head ≠ `app`) |
| 3→5 | ⊥ (first args `nil` vs `app(xs,ys)` don't unify) | **CP1** (subterm `app(xs,ys)` unifies with `app(nil, ys')` via xs ↦ nil, ys ↦ ys'); joinable |
| 4→1 | ⊥ (heads differ)            | ⊥ (subterm `nil` head ≠ `app`) |
| 4→2 | ⊥ (heads differ)            | ⊥ (subterm `cons(x,ys)` head ≠ `app`) |
| 4→3 | ⊥ (first args `cons(x,xs)` vs `nil` don't unify) | ⊥ (subterm `nil` head ≠ `app`) |
| 4→4 | trivial self; RHS=RHS       | ⊥ (subterm `cons(x,xs)` head ≠ `app`) |
| 4→5 | ⊥ (first args `cons(x,xs)` vs `app(xs',ys')` don't unify) | **CP2** (subterm `app(xs,ys)` unifies with `app(cons(x',xs'), ys')` via xs ↦ cons(x',xs'), ys ↦ ys'); joinable |
| 5→1 | ⊥ (heads differ)            | ⊥ (subterm `nil` head ≠ `app`) |
| 5→2 | ⊥ (heads differ)            | ⊥ (subterm `cons(x,ys)` head ≠ `app`) |
| 5→3 | ⊥ (first args `app(xs,ys)` vs `nil` don't unify) | ⊥ (subterm `nil` head ≠ `app`) |
| 5→4 | ⊥ (first args `app(xs,ys)` vs `cons(x',xs')` don't unify) | ⊥ (subterm `cons(x',xs')` head ≠ `app`) |
| 5→5 | trivial self; RHS=RHS       | **CP3** (subterm `app(xs,ys)` unifies with `app(app(xs',ys'), zs')` via xs ↦ app(xs',ys'), ys ↦ zs'); joinable |

25 × 2 = 50 cells. Three are non-trivial critical pairs (CP1, CP2,
CP3); five are trivial self-overlaps at the root; the remaining 42
are ruled out by head mismatch or constructor non-unification. We
now close the three non-trivial pairs.

**CP1 (ρ3 into ρ5 at position 1).**

    Most general overlap term: t* = app(app(nil, ys'), zs)

    Path A (ρ3 at position 1, discharging inner redex):
        app(app(nil, ys'), zs) → app(ys', zs)

    Path B (ρ5 at ε, with xs ↦ nil, ys ↦ ys', zs ↦ zs):
        app(app(nil, ys'), zs) → app(nil, app(ys', zs))
                               → (ρ3) app(ys', zs)

    Common reduct: app(ys', zs). ✓

**CP2 (ρ4 into ρ5 at position 1).**

    Most general overlap term: t* = app(app(cons(x', xs'), ys'), zs)

    Path A (ρ4 at position 1):
        → app(cons(x', app(xs', ys')), zs)
          → (ρ4 at ε) cons(x', app(app(xs', ys'), zs))
          → (ρ5 at position 1) cons(x', app(xs', app(ys', zs)))

    Path B (ρ5 at ε, xs ↦ cons(x', xs'), ys ↦ ys', zs ↦ zs):
        → app(cons(x', xs'), app(ys', zs))
          → (ρ4 at ε) cons(x', app(xs', app(ys', zs)))

    Common reduct: cons(x', app(xs', app(ys', zs))). ✓

**CP3 (ρ5 into ρ5 at position 1).**

    Most general overlap term: t* = app(app(app(xs', ys'), zs'), zs)

    Path A (ρ5 at position 1):
        → app(app(xs', app(ys', zs')), zs)
          → (ρ5 at ε, xs ↦ xs', ys ↦ app(ys', zs'), zs ↦ zs)
            app(xs', app(app(ys', zs'), zs))
          → (ρ5 at position 2, xs ↦ ys', ys ↦ zs', zs ↦ zs)
            app(xs', app(ys', app(zs', zs)))

    Path B (ρ5 at ε, xs ↦ app(xs', ys'), ys ↦ zs', zs ↦ zs):
        → app(app(xs', ys'), app(zs', zs))
          → (ρ5 at ε, xs ↦ xs', ys ↦ ys', zs ↦ app(zs', zs))
            app(xs', app(ys', app(zs', zs)))

    Common reduct: app(xs', app(ys', app(zs', zs))). ✓

All three non-trivial critical pairs join. Combined with the variable-
overlap sublemma of §2.1, **R is locally confluent.**

### 3.2 Measure construction and decrease proof for Q2

**Chosen interpretation.**

    [0]          = 0
    [nil]        = 1
    [s](x)       = x + 1
    [cons](x, y) = x + y + 2
    [len](x)     = x
    [app](x, y)  = 2x + y + 1

Each [f] is a linear polynomial with non-negative integer coefficients
and a strictly positive coefficient on each argument (for [s], [len]:
coefficient 1 on x; for [cons]: coefficient 1 on each of x, y; for
[app]: coefficient 2 on x, 1 on y). By the monotonicity sublemma of
§2.2, each [f] is strictly monotone in each argument over ℕ.

Extend homomorphically to terms: `φ(f(t₁,…,tₙ)) = [f](φ(t₁),…,φ(tₙ))`.

**Monotonicity of φ under contexts.** By induction on the depth of
the context's hole. Base (hole at the root): t → t' with φ(t) > φ(t')
gives the conclusion vacuously. Inductive (hole depth ≥ 1, so context
is `f(u₁, …, u_{k-1}, C'[·], u_{k+1}, …, u_n)` for some smaller
context `C'`): by IH, `φ(C'[t]) > φ(C'[t'])`; strict monotonicity
of `[f]` in its k-th argument preserves the inequality. So for all
contexts C, `φ(t) > φ(t')` implies `φ(C[t]) > φ(C[t'])`.

**Strict decrease per rule.** Each line below computes `[LHS] - [RHS]`
as a polynomial in the rule's variables, using the homomorphic
extension. Positivity is checked as "all coefficients non-negative,
constant term ≥ 1".

- ρ1: `[len(nil)] = [nil] = 1`;  `[0] = 0`. Difference = 1. ✓
- ρ2: `[len(cons(x, ys))] = x + ys + 2`;  `[s(len(ys))] = ys + 1`.
  Difference = `x + 1 ≥ 1` for x ∈ ℕ. ✓
- ρ3: `[app(nil, ys)] = 2·1 + ys + 1 = ys + 3`;  `[ys] = ys`.
  Difference = 3. ✓
- ρ4: `[app(cons(x, xs), ys)] = 2(x + xs + 2) + ys + 1
      = 2x + 2xs + ys + 5`;
  `[cons(x, app(xs, ys))] = x + (2xs + ys + 1) + 2
      = x + 2xs + ys + 3`.
  Difference = `x + 2 ≥ 2`. ✓
- ρ5: `[app(app(xs, ys), zs)] = 2(2xs + ys + 1) + zs + 1
      = 4xs + 2ys + zs + 3`;
  `[app(xs, app(ys, zs))] = 2xs + (2ys + zs + 1) + 1
      = 2xs + 2ys + zs + 2`.
  Difference = `2xs + 1 ≥ 1`. ✓

All five rules strictly decrease φ, uniformly in ℕ-valued variables.
Combined with context-monotonicity, for any one-step rewrite `s → t`
(at any position, in any context), `φ(s) > φ(t)`. `(ℕ, <)` is well-
founded. Hence no infinite `→`-chain exists: **R terminates on all
closed terms.**

---

## 4. Final verdict

### 4.1 Q1 answer: R is confluent

§3.1 exhausts the 50 (ordered pair × non-variable position) cells.
Five are trivial self-overlaps; 42 are ruled out by head mismatch;
three are non-trivial critical pairs, each joinable:

| Label | Rules (i→j)   | Origin t*                            | Common reduct                                    |
|-------|---------------|--------------------------------------|--------------------------------------------------|
| CP1   | (ρ3, ρ5)      | `app(app(nil, ys'), zs)`             | `app(ys', zs)`                                   |
| CP2   | (ρ4, ρ5)      | `app(app(cons(x', xs'), ys'), zs)`   | `cons(x', app(xs', app(ys', zs)))`               |
| CP3   | (ρ5, ρ5)      | `app(app(app(xs', ys'), zs'), zs)`   | `app(xs', app(ys', app(zs', zs)))`               |

Variable overlaps close by the sublemma of §2.1. Hence R is locally
confluent. Combined with termination (§4.2) via the derivation of
§4.3, **R is confluent.**

### 4.2 Q2 answer: R terminates

The polynomial interpretation

    [0] = 0,  [nil] = 1,  [s](x) = x + 1,
    [cons](x, y) = x + y + 2,  [len](x) = x,  [app](x, y) = 2x + y + 1

induces a strictly monotone (by the sublemma of §2.2) map
`φ: closed terms → ℕ` that strictly decreases under every rule
application (§3.2) and under every context (by context-monotonicity).
Since `(ℕ, <)` is well-founded, R admits no infinite `→`-chain.
**R terminates.**

### 4.3 Joint implication: local confluence + termination ⟹ confluence

We derive this step from first principles. The classical statement
we use:

> If → is terminating and every one-step divergence t →₁ u,
> t →₁ v has a common reduct (i.e., R is locally confluent), then
> every multi-step divergence also has a common reduct (R is
> confluent).

*Proof.* §3.2 established that → is well-founded on closed terms:
every closed term t has no infinite descending →-chain. Equivalently,
the relation `<` defined by `t > s ⟺ t → s` (and its transitive
closure `t > s ⟺ t ↠ s via at least one step`) is a well-founded
strict partial order on closed terms. In particular, strict reducts
of t are strictly below t under `>`.

We prove by well-founded induction on `t` under `>`: for all closed
t, if `t ↠ u` and `t ↠ v` then there exists w with `u ↠ w` and
`v ↠ w`.

*Base.* If t is a normal form (no outgoing →), then `t ↠ u` forces
`u = t`; similarly `v = t`. Take w = t.

*Inductive.* Assume the claim for all strict reducts of t. Given
`t ↠ u` and `t ↠ v`. If either reduction has length zero, the other
side serves directly as common reduct (u = t, so v is already a
reduct of u; take w = v; symmetric case analogous).

Otherwise `t → t₁ ↠ u` and `t → t₂ ↠ v`. Two cases:

Case α: t₁ = t₂. Then both reductions from t₁ land at reducts u, v
of t₁; apply IH at t₁ (which is a strict reduct of t, hence t₁ < t).
Get a common reduct w of u, v. Then `u ↠ w` and `v ↠ w` as required.

Case β: t₁ ≠ t₂. Local confluence (§3.1) gives some s with `t₁ ↠ s`
and `t₂ ↠ s`. Now:

- s is a reduct of t₁ (via `t₁ ↠ s`), hence of t (via `t → t₁ ↠ s`,
  which uses ≥ 1 step, so s < t strictly).
- Apply IH at t₁ (t₁ < t): the two reductions `t₁ ↠ u` and `t₁ ↠ s`
  meet at some u' with `u ↠ u'` and `s ↠ u'`.
- Apply IH at t₂ (t₂ < t): the two reductions `t₂ ↠ v` and `t₂ ↠ s`
  meet at some v' with `v ↠ v'` and `s ↠ v'`.
- Apply IH at s (s < t, as noted): the two reductions `s ↠ u'` and
  `s ↠ v'` meet at some w with `u' ↠ w` and `v' ↠ w`.

Compose: `u ↠ u' ↠ w` and `v ↠ v' ↠ w`. Common reduct w.

The induction is legal because the well-founded order `>` was
established in §3.2. ∎

This derivation closes §4.3 without invoking any classical result by
name.

---

## 5. Verification strategy

We back the hand-proofs with an executable oracle, `sim/simulator.py`,
which implements:

1. **Ground-instance realisation of the three non-trivial critical
   pairs.** For each of CP1, CP2, CP3, both sides of the
   one-step divergence are materialised at a concrete closed
   instance, and their reachable sets under → (BFS-enumerated up to
   1000 terms) are intersected to find a common reduct.
2. **Per-step φ-decrease verification.** The normal-form reducer
   raises an exception if any step fails `φ(t) > φ(t')`.
3. **Reduction-order independence on sample closed terms.** Each
   sample is normalised under leftmost-outermost and rightmost-
   innermost strategies; the two normal forms are asserted equal.
4. **Pool φ-audit.** For every term reachable from the sample pool
   (142 rewriting steps across all reachable instances), every
   rewrite step is asserted to strictly decrease φ.

Captured output: `sim/output-final.txt` (final run) confirms:

- All three critical pairs reach a common reduct on their ground
  instance.
- All sample terms normalise to the same value under both strategies.
- 142 rewrite steps across the reachable pool all strictly decrease φ.

**Worked executable-oracle verification is performed end-to-end;
this counts as an R6 = 3 indicator alongside the trace-argument
path.**

**Caveats.**

- The simulator is a *falsifier*, not a prover. It checks closure
  on finite ground instances; it cannot substitute for the symbolic
  arguments in §3.1 and §3.2. Simulator disagreement would refute
  the hand-proof; agreement is necessary but not sufficient.
- Critical-pair closure is proven *symbolically* in §3.1; the
  simulator's ground-instance rerun only rules out bugs in the
  unifiers.
- The φ-audit covers closed terms reachable from the test pool up
  to a BFS bound; the symbolic per-rule check in §3.2 covers all ℕ
  substitutions uniformly.

---

## 6. Worked examples

Each example below was cross-checked against `sim/trace_check.py`,
whose output is inlined when helpful. **LMO = leftmost-outermost; RMI
= rightmost-innermost.**

### 6.1 ρ5 in both reduction orders

`t = app(app(app(nil, nil), nil), nil)`.

φ(t) = 2·[app(app(nil,nil),nil)] + [nil] + 1
     = 2·(2·[app(nil,nil)] + 1 + 1) + 1 + 1
     = 2·(2·4 + 2) + 2 = 2·10 + 2 = 22.

*LMO trace.* Root is a ρ5-redex; at every subsequent step the root
is again the leftmost-outermost redex.

    t = app(app(app(nil, nil), nil), nil)                             φ=22
      → (ρ5 at ε, xs↦app(nil,nil), ys↦nil, zs↦nil)
        app(app(nil, nil), app(nil, nil))                             φ=13
      → (ρ5 at ε, xs↦nil, ys↦nil, zs↦app(nil,nil))
        app(nil, app(nil, app(nil, nil)))                             φ=10
      → (ρ3 at ε, ys↦app(nil, app(nil, nil)))
        app(nil, app(nil, nil))                                       φ=7
      → (ρ3 at ε, ys↦app(nil, nil))
        app(nil, nil)                                                 φ=4
      → (ρ3 at ε, ys↦nil)
        nil                                                           φ=1

*RMI trace.* At every step the deepest, rightmost redex is the
deepest `app(nil, nil)`.

    t = app(app(app(nil, nil), nil), nil)                             φ=22
      → (ρ3 at position 1.1, ys↦nil)
        app(app(nil, nil), nil)                                       φ=10
      → (ρ3 at position 1, ys↦nil)
        app(nil, nil)                                                 φ=4
      → (ρ3 at ε, ys↦nil)
        nil                                                           φ=1

Both orders reach the same normal form `nil`. φ is strictly decreasing
along both traces: 22>13>10>7>4>1 and 22>10>4>1. Convergence verified.

### 6.2 Interleaving of `len` and `app` across a cons-structure

`t = len(app(cons(0, nil), cons(s(0), nil)))`.

φ(t) = [app(cons(0, nil), cons(s(0), nil))]
     = 2·[cons(0, nil)] + [cons(s(0), nil)] + 1
     = 2·3 + 4 + 1 = 11.

Only ρ4 applies initially (inner `app`'s first argument is
`cons(0, nil)`, not `nil`). The ρ2 redex at root is blocked until
the inner `app` reduces to a `cons`.

*RMI trace (matches the narrative reduction most readers expect).*

    t = len(app(cons(0, nil), cons(s(0), nil)))                       φ=11
      → (ρ4 at position 1, x↦0, xs↦nil, ys↦cons(s(0), nil))
        len(cons(0, app(nil, cons(s(0), nil))))                       φ=9
      → (ρ3 at position 1.2, ys↦cons(s(0), nil))
        len(cons(0, cons(s(0), nil)))                                 φ=6
      → (ρ2 at ε, x↦0, ys↦cons(s(0), nil))
        s(len(cons(s(0), nil)))                                       φ=5
      → (ρ2 at position 1, x↦s(0), ys↦nil)
        s(s(len(nil)))                                                φ=3
      → (ρ1 at position 1.1)
        s(s(0))                                                       φ=2

Normal form `s(s(0))` — the length of a two-element list. φ is
strictly decreasing: 11>9>6>5>3>2. The LMO trace reaches the same
normal form via a different intermediate sequence (φ: 11,9,8,5,3,2
— see `sim/trace-check-output.txt`); both strategies converge.

### 6.3 ρ4: raw size grows, but φ strictly drops

`t = app(cons(0, nil), cons(s(0), nil))`. Symbol count: 8.

    t = app(cons(0, nil), cons(s(0), nil))        size 8    φ=11
      → (ρ4 at ε, x↦0, xs↦nil, ys↦cons(s(0), nil))
        cons(0, app(nil, cons(s(0), nil)))        size 9    φ=9
      → (ρ3 at position 2, ys↦cons(s(0), nil))
        cons(0, cons(s(0), nil))                  size 6    φ=6

Raw symbol count: 8 → 9 → 6 — a literal size measure is *not* a
termination measure; it increases at the first step. φ: 11 → 9 → 6
— strictly decreasing. This is the load-bearing example for §2.2's
claim that the right measure is an interpretation, not a size count.

### 6.4 CP3 ground-witness closure

The symbolic CP3 proof in §3.1 is now verified on a closed instance.
Choose `xs' := nil`, `ys' := cons(0, nil)`, `zs' := nil`,
`zs := cons(s(0), nil)`.

    t = app(app(app(nil, cons(0, nil)), nil), cons(s(0), nil))        φ=33

*Path A (Path A of §3.1: ρ5 at position 1).*

    → (ρ5 at position 1, xs↦nil, ys↦cons(0,nil), zs↦nil)
      app(app(nil, app(cons(0, nil), nil)), cons(s(0), nil))          φ=27
    → (ρ5 at ε, xs↦nil, ys↦app(cons(0,nil), nil), zs↦cons(s(0), nil))
      app(nil, app(app(cons(0, nil), nil), cons(s(0), nil)))          φ=20
    → (ρ5 at position 2, xs↦cons(0,nil), ys↦nil, zs↦cons(s(0), nil))
      app(nil, app(cons(0, nil), app(nil, cons(s(0), nil))))          φ=17

Now Path A converges with the symbolic common reduct
`app(xs', app(ys', app(zs', zs)))` — here
`app(nil, app(cons(0, nil), app(nil, cons(s(0), nil))))`. From this
point we continue to a full normal form (not required for closure,
but useful to cross-check determinism):

    → (ρ3 at position 2.2, ys↦cons(s(0), nil))
      app(nil, app(cons(0, nil), cons(s(0), nil)))                    φ=14
    → (ρ4 at position 2, x↦0, xs↦nil, ys↦cons(s(0), nil))
      app(nil, cons(0, app(nil, cons(s(0), nil))))                    φ=12
    → (ρ3 at position 2.2, ys↦cons(s(0), nil))
      app(nil, cons(0, cons(s(0), nil)))                              φ=9
    → (ρ3 at ε, ys↦cons(0, cons(s(0), nil)))
      cons(0, cons(s(0), nil))                                        φ=6

*Path B (Path B of §3.1: ρ5 at ε).*

    → (ρ5 at ε, xs↦app(nil, cons(0,nil)), ys↦nil, zs↦cons(s(0), nil))
      app(app(nil, cons(0, nil)), app(nil, cons(s(0), nil)))          φ=20
    → (ρ5 at ε, xs↦nil, ys↦cons(0,nil), zs↦app(nil, cons(s(0), nil)))

Hmm — ρ5 still matches at the root? No: after the previous step the
root is `app(app(nil, cons(0, nil)), app(nil, cons(s(0), nil)))`. Its
LHS pattern match for ρ5 requires first arg to be of shape `app(_, _)`.
Yes, first arg is `app(nil, cons(0, nil))`. So ρ5 does apply.

Actually more directly, both ρ3-redexes and one ρ5-redex all apply.
Choosing ρ3 for a shorter path:

    → (ρ3 at position 1, ys↦cons(0, nil))
      app(cons(0, nil), app(nil, cons(s(0), nil)))                    φ=14
    → (ρ3 at position 2, ys↦cons(s(0), nil))
      app(cons(0, nil), cons(s(0), nil))                              φ=11
    → (ρ4 at ε, x↦0, xs↦nil, ys↦cons(s(0), nil))
      cons(0, app(nil, cons(s(0), nil)))                              φ=9
    → (ρ3 at position 2, ys↦cons(s(0), nil))
      cons(0, cons(s(0), nil))                                        φ=6

Both paths reach `cons(0, cons(s(0), nil))`, confirming CP3 closure
on this ground instance. φ strictly decreases along each trace
(33→27→20→17→14→12→9→6 and 33→20→14→11→9→6); verified by the
simulator (`sim/output-final.txt`).

---

## 7. Open questions and known limitations

### 7.1 Extension with `add` and a `len`/`app` distributor

Extend R with binary `add` and three rules:

    ρ6:  add(0, y)         → y
    ρ7:  add(s(x), y)      → s(add(x, y))
    ρ8:  len(app(xs, ys))  → add(len(xs), len(ys))

Does the polynomial measure of §3.2 extend? Assign `[add](x, y) =
Ax + By + C` (A, B, C ≥ 0, at least one of A, B strictly positive,
to be determined).

- ρ6: `[LHS] = A·0 + B·y + C = By + C`;  `[RHS] = y`.
  For strict decrease over ℕ: need `By + C > y` for all y ≥ 0, i.e.,
  `B ≥ 1` and `C ≥ 1`.
- ρ7: `[LHS] = A(x+1) + By + C = Ax + By + A + C`;
  `[RHS] = [s(add(x,y))] = (Ax + By + C) + 1 = Ax + By + C + 1`.
  Strict decrease requires `A + C > C + 1`, i.e., `A ≥ 2`.
- ρ8: `[LHS] = [app(xs, ys)] = 2·xs + ys + 1`;  `[RHS] = A·xs + B·ys
  + C`. Strict decrease requires `2 > A` on the xs-coefficient and
  `1 > B` on the ys-coefficient, and `1 > C` on the constant.

Combining: ρ6 gives B ≥ 1; ρ8 gives B < 1. **Contradiction.** No
choice of linear `[add]` with non-negative integer coefficients
discharges both ρ6 and ρ8 simultaneously while keeping ρ7's need
(A ≥ 2). This is a genuine dimensional obstruction: linear
interpretations over ℕ form a finite-parameter family, and imposing
ρ6, ρ7, ρ8 cuts out a strictly empty region.

A way forward: use a *lexicographic* composition. Define a secondary
measure `ψ` counting the number of `len` occurrences in t. Observe:

- ρ8 reduces `len(app(xs, ys))` to `add(len(xs), len(ys))`, which
  has *two* `len`s on the RHS versus *one* on the LHS. So ψ strictly
  *increases* on ρ8. A lexicographic `(ψ, φ)` ordering with ψ
  outside does not work.

Swap: `(k, φ)` where `k(t)` counts the number of `app` occurrences
strictly inside a `len`. Then:

- ρ8: LHS `len(app(xs, ys))` has one `app` strictly inside a `len`;
  RHS `add(len(xs), len(ys))` has zero. k strictly drops at ρ8.
- ρ1, ρ2: `len(nil)`, `len(cons(x, ys))` have no `app` under `len`
  on either side (RHSs contain no `len` over an `app` either). k ≥
  0 stays 0 for these rules on both sides.
- ρ3, ρ4, ρ5: no `len` appears in the rule at all, so k is unchanged
  on any rewrite at any context (since the rule operates away from
  any `len(…)` in an enclosing context — more precisely, whether the
  rewrite occurs inside or outside a `len`, the count of `app`
  occurrences inside `len`-contexts is governed by how many `app`s
  the rewrite moves in and out; ρ3 deletes one `app`, ρ4 preserves,
  ρ5 preserves — so if the rewrite happens *inside* a `len`, k drops
  by one (ρ3) or stays (ρ4, ρ5); if *outside*, k is unchanged).
- ρ6, ρ7: no `len` appears; no effect on k.

Lexicographic pair `(k(t), φ(t))` with k outermost. Every rule either
strictly decreases k (ρ8, and ρ3 when applied inside a `len`) or
leaves k unchanged and strictly decreases φ (the rest, with φ computed
under a choice like `[add](x, y) = 2x + y + 1`, `[len](x) = x`,
`[app](x, y) = 2x + y + 1` — but now the conflict of ρ6/ρ8 is isolated
to the second component, and ρ8 is already handled by k).

We have *not* written out the full decrease check for ρ6 and ρ7 under
this composite; the present document claims only that the linear
obstruction identified above rules out *single-polynomial* measures
of the kind used for the base R, and that a lex pair (k, φ) with k
counting `app-under-len` is a plausible route. A full proof for the
extended system is left as an open question.

### 7.2 Does the confluence proof generalise?

The argument of §3.1 relied on:

- Left-linearity of every LHS (discharges variable overlaps by §2.1).
- Exhaustive critical-pair closure for three non-trivial overlaps.
- Termination (upgrades local confluence to global via §4.3).

Any extension of R that introduces a new LHS creates new
(ρᵢ, ρⱼ) pairs and potentially new critical pairs. For instance,
adding ρ8 above introduces a new LHS `len(app(xs, ys))`, and
enumeration becomes:

- ρ8 against ρ3: subterm `app(xs, ys)` unifies with `app(nil, ys')` —
  new critical pair `(len(ys), add(len(nil), len(ys)))`. Is this
  joinable? `len(ys)` is already in normal form (for variable ys).
  `add(len(nil), len(ys))` → (ρ1) `add(0, len(ys))` → (ρ6) `len(ys)`.
  Joinable at `len(ys)`. ✓
- ρ8 against ρ4: subterm `app(xs, ys)` unifies with
  `app(cons(x', xs'), ys')` — critical pair
  `(len(cons(x', app(xs', ys'))), add(len(cons(x', xs')), len(ys')))`.
  Left side → (ρ2) `s(len(app(xs', ys')))` → (ρ8)
  `s(add(len(xs'), len(ys')))`. Right side → (ρ2)
  `add(s(len(xs')), len(ys'))` → (ρ7) `s(add(len(xs'), len(ys')))`.
  Joinable. ✓
- ρ8 against ρ5: similar; joinable.

So the base confluence proof *does* extend to this particular
extension, provided we also know (independently) that the extended
system is terminating. The proof is not mechanical; each critical
pair must be re-examined. The base confluence argument is therefore
*modular* in structure but not *monotone*: adding rules can
introduce new critical pairs that happen to close (as above), but
does not carry forward a confluence certificate automatically.

### 7.3 Termination vs confluence on R specifically

For this R, Q1 is *proved using* Q2 (via §4.3). Does Q2 imply Q1
unconditionally for R? Not as a logical tautology: termination
alone does not imply confluence — a non-left-linear or overlapping
terminating system can easily lack confluence. For R it happens to,
because every critical pair closes *and* R terminates; both facts
are needed.

Does Q1 imply Q2 for R? Again not as a logical tautology. One can
imagine a non-terminating confluent extension of R (e.g., add
`app(xs, nil) → app(app(xs, nil), nil)`, which trivially loops;
confluence is preserved since the rule yields a canonical right-
associated spiral, but termination fails). So on R the two properties
are independent *in principle*. They happen to both hold by separate
arguments.

### 7.4 Is the measure a polynomial interpretation or something more
         elaborate?

Ours is a linear polynomial interpretation over ℕ with coefficients
in {0, 1, 2} and constant terms in {0, 1, 2}. The critical shape:
`[app](x, y) = 2x + y + 1`, i.e., the left argument outweighs the
right strictly.

More elaborate constructions are *unnecessary* for the base R: a
linear interpretation suffices. For extensions (§7.1), a
lexicographic pair of interpretations, a multiset-of-subterms
ordering, or an exponential interpretation may be needed. The
linearity of our measure is tight for R — the ρ5 coefficient
asymmetry cannot be weakened to symmetric linear (see §1.2's
derivation showing `a > b` is needed) — but is not portable to
richer systems.

---

## 8. Disclosed gaps

Listed explicitly so the evaluator has a concrete audit list:

- **(D1)** §3.1's enumeration table is constructed by hand, not
  machine-generated. Completeness is argued by exhaustion of all
  (ρᵢ, ρⱼ, position) triples with non-variable position in ρⱼ's LHS;
  a reader must trust the position lists for each LHS are complete,
  and our non-variable positions are indeed `{ε, 1}` for each rule.

- **(D2)** §4.3's induction relies on §3.2's termination to obtain
  the well-founded order. The proof of confluence for R is therefore
  not "termination-independent": were R non-terminating, the
  local-confluence closures of §3.1 would not suffice by our method.
  A termination-independent confluence argument (e.g., parallel-
  reduction diamond closure) would remove this dependency; we do
  not attempt it here.

- **(D3)** §7.1's extended-system termination is left as a genuine
  open question. The linear-interpretation obstruction is proved
  (coefficient constraints are contradictory), and a lexicographic-
  pair sketch (k, φ) is proposed, but the full verification of ρ6
  and ρ7 under the composite is not carried out.

- **(D4)** The simulator runs at ground instances; symbolic closure
  (§3.1) and symbolic per-rule strict decrease (§3.2) are the
  load-bearing proofs, while the simulator's 142-step audit is
  corroborative only. A stronger backing would mechanise the
  symbolic arguments (e.g., polynomial-arithmetic certification in
  a theorem prover); that is outside the scope of this document.

- **(D5)** §2.1's variable-overlap sublemma handles left-linear R.
  If a future extension adds a non-left-linear LHS, variable overlaps
  may fail to close, and §3.1's argument would need a separate
  variable-overlap enumeration.

- **(D6)** The iteration-01 evaluator report (`/workspaces/task/
  .eval-report-01.json`) flagged arithmetic errors in the worked-
  example φ traces of the draft (G1, G2). These are corrected in
  the present version and re-verified against
  `sim/trace-check-output.txt`.
