# Confluence, weak normalization, and strong normalization of R

Signature Σ and rules R (restated for reference):

```
Σ  nullary constructors : 0,  nil,  a
Σ  unary  constructor   : s
Σ  binary constructor   : cons
Σ  unary  defined       : len,  f
Σ  binary defined       : c

ρ₁  len(nil)             → 0
ρ₂  len(cons(x, ys))     → s(len(ys))
ρ₃  c(x, y)              → x
ρ₄  c(x, y)              → y
ρ₅  f(x)                 → f(s(x))
ρ₆  f(x)                 → nil
```

**Verdicts committed to:**

| question                        | verdict                         |
|---------------------------------|---------------------------------|
| Q1. Confluence                  | **NOT confluent**               |
| Q2. Weak normalization          | **Weakly normalizing**          |
| Q3. Strong normalization        | **NOT strongly normalizing**    |

A mechanical oracle at `task/sim.py` (transcript `task/sim_output.txt`)
checks every concrete witness below.

---

## 1. Motivation

### 1.1 Q1 — Why confluence is implausible

Two rules share the exact same left-hand side but project it to two
different variables:

```
ρ₃ : c(x, y) → x        ρ₄ : c(x, y) → y
```

Any term of the form `c(t, u)` is simultaneously a ρ₃-redex and a
ρ₄-redex.  Whenever `t` and `u` can be driven to *distinct* normal
forms — e.g. `t = 0, u = nil` — the two projections lead irrevocably
to different answers and the two reductions cannot rejoin.  The
structural intuition: a rule pair of this shape encodes a *non-
deterministic choice primitive*; each firing commits irreversibly to
one branch, and when the two branches carry distinguishable data the
choice is observable.  The analog in process-algebra style reasoning
is exactly the point of a "+" (choice) operator without a merge rule
that identifies `x + y` with both projections.

Nothing else in R can undo such a commitment: there is no rule that
identifies `0` with `nil`, or rebuilds a `c` from its projections.
Joinability is therefore lost at the very first firing.

### 1.2 Q2 — Why weak normalization is plausible

ρ₅ : `f(x) → f(s(x))` is the only rule in R that *grows* its
redex — it is structurally "escape-recursive".  But ρ₅ is not the
only rule whose LHS is `f(x)`: rule ρ₆ matches exactly the same
pattern and escapes to `nil` unconditionally.  Every f-redex in every
term therefore has an *escape hatch*: rather than ρ₅-expanding it,
one can ρ₆-collapse it.

This is the lazy-vs-eager evaluation intuition.  In a functional
program, a definition `f x = f (s x)` is non-terminating under eager
evaluation but harmless under a lazy discipline that avoids firing
it when an alternative definition (ρ₆) can produce a value.
Provided we control redex selection — pick ρ₆ at every f-subterm —
the bad rule is never fired, and the remaining rules are all
structurally simplifying: ρ₁, ρ₂ peel `len` down along list
structure; ρ₃, ρ₄ discard one half of a `c`-redex; ρ₆ discards the
entire f-argument.  Each of these strictly shrinks a weighted term
size.

Because the strategy has a choice at every step and every choice is
either "non-f" (must simplify) or "f, choose ρ₆" (must simplify), a
weighted-size descent argument closes WN.

### 1.3 Q3 — Why strong normalization is implausible

ρ₅ acting alone on `f(t)` produces `f(s(t))`, which is again an
f-redex; a second ρ₅ step produces `f(s(s(t)))`; and so on.  The
sequence `f(t) → f(s(t)) → f(s(s(t))) → …` is a textbook-style
unbounded-recursion trap.  Each step strictly enlarges the term by a
fresh `s`-layer, so no term in the sequence can be repeated (heights
strictly grow), and the sequence is infinite.  Strong normalization
fails.

The parametric intuition: any rule of shape `P(x) → P(g(x))` with a
non-collapsing `g` — no matter what the surrounding system does —
generates an infinite family of reducts.  As long as a strategy
exists that only fires this rule and never any collapsing rule, SN
is impossible.

---

## 2. Method design

Three methods, each used for one question.  Methods may share term-
algebra plumbing (substitution, positions, context-closure) but the
*argument shapes* are distinct and no argument pretends to discharge
more than one question.

### 2.1 Confluence method (§2.1)

**Goal.**  Either show R is confluent (every critical pair joinable,
plus a lifting argument) or exhibit a divergent pair of reductions
ending in distinct normal forms.

**Recipe for non-confluence.**  We seek a *closed* term `t`, two
one-step reductions `t →_ρ u` and `t →_σ v`, and two further
reduction sequences ending in `u', v'` that are simultaneously:

  (N1) normal forms — no rule of R applies at any position;
  (N2) unequal as syntactic terms.

If (N1) and (N2) both hold, `u'` and `v'` cannot join, because a
normal form has no further reducts to travel toward a common
descendant, and they are distinct, so they are not already the same
term.  Hence `t` witnesses non-confluence.

A bare "ρ₃ and ρ₄ disagree" is insufficient because a divergent
*one-step* pair `(x, y)` at the level of a rewrite rule's free
variables does not itself witness non-confluence: one must produce
(i) a ground instance, (ii) reduction to normal form on both sides,
(iii) observable inequality of the normal forms.  §4.1 below
provides all three.

**Named sublemma for §4.1.**

> **SL-1 (non-joinability via distinct NFs).**  If `t ↠ u'`, `t ↠
> v'`, both `u'` and `v'` are normal forms (no rule of R matches at
> any position in either), and `u' ≠ v'` as syntactic terms, then
> R is not confluent.  (Proof: confluence would give some `w` with
> `u' ↠ w` and `v' ↠ w`; normality forces `u' = w = v'`, contradicting
> inequality.)

This sublemma is cited once in §4.1 and not re-proved inline.

**Critical-pair enumeration.**  For completeness, §3.1 also
enumerates every critical pair — both to identify the non-joining
overlap precisely and to confirm that no *other* pair contradicts
the verdict once ρ₃/ρ₄ has been pinpointed.

### 2.2 Weak normalization method (§2.2)

**Goal.**  Either exhibit a specific reduction strategy `S` such that
every closed term reduces under `S` to a normal form in finitely
many steps, or exhibit a closed term whose every reduction sequence
is infinite.

**Recipe for a successful WN strategy.**  Choose a redex-selection
discipline `S` that, at every closed non-normal term, picks a single
redex to fire, subject to:

  (W1) *Applicability:*  Whenever `t` is non-normal (some rule
       applies), `S` makes a selection.
  (W2) *Progress under a well-founded measure:*  There is a
       measure `μ : (closed terms) → ℕ` such that every `S`-step
       `t →_S t'` satisfies `μ(t) > μ(t')`.
  (W3) *Termination at a true normal form:*  When `S` halts on `t`
       (produces no selection), `t` is in fact a normal form of R.

Given (W1)+(W2)+(W3), every starting term `t₀` yields an `S`-trace
of length at most `μ(t₀) - 1` (ℕ is well-founded), ending at a real
R-normal form.

For R specifically: S = *leftmost-outermost selection among non-ρ₅
redexes.*  (W1) is immediate once we argue that every f-redex — the
only kind that can match ρ₅ — also matches ρ₆, so choosing ρ₆
bypasses ρ₅ without abandoning the redex.  (W2) is a per-rule check
of strict decrease of μ for ρ₁, ρ₂, ρ₃, ρ₄, ρ₆; ρ₅ is never fired
by S, so its non-decrease is irrelevant.  (W3) is immediate: S only
refuses to fire at terms where no rule matches at all.

**Named sublemma for §4.2.**

> **SL-2 (polynomial measure strictly decreases along S).**  Define
> μ : closed terms → ℕ₊ by the table in §3.3.  For every rule ρ ∈
> {ρ₁, ρ₂, ρ₃, ρ₄, ρ₆} and every ground instantiation θ of ρ's LHS
> variables (each variable assigned a closed term), `μ(LHS·θ) >
> μ(RHS·θ)`.  Further, μ is strictly monotone in every constructor
> argument, so a one-step S-rewrite inside any context strictly
> decreases μ of the enclosing term.

Note the sublemma is deliberately *silent about ρ₅*: SL-2 is
compatible with ρ₅-steps increasing μ, which they do.  The WN
strategy simply avoids them.

### 2.3 Strong normalization method (§2.3)

**Goal.**  Either exhibit a strictly-decreasing well-founded measure
that decreases under *every* single-step rewrite (not just under a
strategy), or exhibit a specific closed term `t₀` with a concrete
infinite reduction sequence whose unbounded pattern is visible by
construction.

**Recipe for non-SN.**  Produce a closed `t₀` and an infinite
sequence

```
t₀ →_ρ(1) t₁ →_ρ(2) t₂ →_ρ(3) …
```

together with an invariant `I(tᵢ)` such that:

  (NSN1) the invariant is preserved: if `I(tᵢ)` then rule ρ_(i+1)
         applies and produces some `t_(i+1)` with `I(t_(i+1))`;
  (NSN2) the invariant carries a strictly increasing parameter
         (e.g. term height or a count of some subterm pattern), so
         no two `tᵢ, tⱼ` with `i ≠ j` are syntactically equal;
  (NSN3) hence the sequence is both infinite and acyclic.

If (NSN1)+(NSN2) hold, the sequence is infinite (no fixpoint, no
cycle), witnessing that some reduction from `t₀` fails to terminate,
which is exactly the negation of SN.

**Named sublemma for §4.3.**

> **SL-3 (ρ₅ generates an unbounded acyclic trajectory).**  For
> every closed term `x`, the sequence `t₀ = f(x)` and `t_(i+1) =
> f(s(tᵢ.arg))` (equivalently, fire ρ₅ at the root of tᵢ) satisfies
> `height(t_(i+1)) = height(tᵢ) + 1`, hence `tᵢ ≠ tⱼ` for `i ≠ j`,
> hence the sequence is infinite and acyclic.

SL-3 is witnessed below by `x = 0`.

### 2.4 What the methods share and where they diverge

All three methods manipulate terms of R on the same term algebra,
and each relies on context-closure monotonicity (a local change of
a subterm shows up as a change of the enclosing term).  Beyond that
shared plumbing:

  - Q1's argument is *existential* — one non-joining CP is enough.
    It does *not* require or produce a measure.
  - Q2's argument is *strategy-scoped* — the measure only has to
    decrease under one chosen strategy, not under all rules.
  - Q3's argument is *universal* — to refute SN it suffices to
    display one infinite chain; a measure would overdischarge.

In particular we do NOT claim "WN because SN" — the opposite is
true: R is WN but not SN, which is already the strong-normalization
textbook counterexample pattern (a rule with a non-simplifying RHS
that is shadowed by a simpler rule with the same LHS).  And we do
NOT infer non-confluence from "WN and SN differ" — non-confluence
has its own witness (§4.1), independent of the other two verdicts.

---

## 3. Progressive derivation

### 3.1 Critical-pair enumeration for Q1

**Non-variable positions of each LHS.**

| rule | LHS                     | non-variable positions | head symbol at each           |
|------|-------------------------|------------------------|-------------------------------|
| ρ₁   | `len(nil)`              | ε, (1)                 | len at ε, nil at (1)          |
| ρ₂   | `len(cons(x, ys))`      | ε, (1)                 | len at ε, cons at (1)         |
| ρ₃   | `c(x, y)`               | ε                      | c at ε                        |
| ρ₄   | `c(x, y)`               | ε                      | c at ε                        |
| ρ₅   | `f(x)`                  | ε                      | f at ε                        |
| ρ₆   | `f(x)`                  | ε                      | f at ε                        |

**Overlap audit.**  At any non-variable position of ρᵢ's LHS, ρⱼ's
LHS must head-match.  Heads of LHSs: len (ρ₁, ρ₂), c (ρ₃, ρ₄), f
(ρ₅, ρ₆).  Heads at the non-root non-variable positions: `nil` (only
in ρ₁'s LHS), `cons` (only in ρ₂'s LHS).  No rule in R has its LHS
head `nil` or `cons`, so no rule unifies at those non-root positions.
Hence every critical pair in R lives at the *root* position and
arises from two rules sharing a head.

**The six nontrivial root overlaps.**  Excluding trivial self-
overlaps `(ρᵢ, ρᵢ, ε)` — these produce the identical CP `⟨RHS, RHS⟩`
on both sides and are joinable by zero further steps — the root-
overlap matrix is:

| (outer ρᵢ, inner ρⱼ) | source               | ρᵢ-reduct (outer at ε) | ρⱼ-reduct (inner at ε) | joinable? |
|---------------------|----------------------|------------------------|------------------------|-----------|
| (ρ₁, ρ₂)            | — (nil vs cons don't unify) | —               | —                      | n/a       |
| (ρ₂, ρ₁)            | — (cons vs nil don't unify) | —               | —                      | n/a       |
| (ρ₃, ρ₄)            | `c(x, y)`            | `x`                    | `y`                    | **NO — distinct NFs under ground witness**     |
| (ρ₄, ρ₃)            | `c(x, y)`            | `y`                    | `x`                    | **NO — symmetric to above**                    |
| (ρ₅, ρ₆)            | `f(x)`               | `f(s(x))`              | `nil`                  | YES (join at `nil` via ρ₆ on left reduct)     |
| (ρ₆, ρ₅)            | `f(x)`               | `nil`                  | `f(s(x))`              | YES (symmetric)                                |

Disposition in detail:

  - **(ρ₃, ρ₄) and (ρ₄, ρ₃) — non-joinable.**  The critical pair
    contains two distinct LHS-variables as its reducts.  With
    ground substitution `x := 0, y := nil` we get two distinct
    reducts `0` and `nil` that are each normal forms (§4.1 verifies
    no rule matches at any position of `0` or `nil`).  SL-1 applies.

  - **(ρ₅, ρ₆) — joinable.**  From `f(x) →_ρ₅ f(s(x))` and `f(x)
    →_ρ₆ nil`: apply ρ₆ to `f(s(x))`, producing `nil`.  Both sides
    reach `nil`.

  - **(ρ₆, ρ₅) — joinable.**  Symmetric: apply ρ₆ to the right-hand
    reduct.

  - **Trivial self-overlaps (ρᵢ, ρᵢ, ε) for ρᵢ ∈ {ρ₁, …, ρ₆}.**
    Both sides of the CP are the same RHS — joinable trivially.

Conclusion: there is a non-joinable critical pair at (ρ₃, ρ₄, ε).
Per SL-1, together with the ground witness of §4.1, R is non-
confluent.  `sim.py` section A mechanically finds all four non-
trivially-equal CP instances — `(rho3, rho4)`, `(rho4, rho3)`,
`(rho5, rho6)`, `(rho6, rho5)` — and section B produces the ground
non-confluence witness.

### 3.2 Reduction-strategy construction for Q2

**Strategy S.**  On a closed term `t`:

  1. Compute the set `R(t) = {(p, ρ) : ρ applies at position p of t}`.
  2. Filter out the ρ₅ entries:  `R'(t) = {(p, ρ) ∈ R(t) : ρ ≠ ρ₅}`.
  3. If `R'(t)` is empty, halt.
  4. Otherwise choose `(p, ρ)` from `R'(t)` minimizing `(len(p), p)`
     in lexicographic order — i.e., leftmost-outermost — and fire.

(The leftmost-outermost tie-break is for definiteness; any tie-break
works.)

**Progress (applicability).**  Claim: at any closed non-normal term
`t`, `R'(t)` is nonempty.

Proof.  `t` non-normal means `R(t)` is nonempty.  Fix any `(p, ρ) ∈
R(t)`.  Inspect the rule heads:

  - If ρ ∈ {ρ₁, ρ₂}, the LHS head is `len`, so `t|_p` has head
    `len`.  No other rule in R has LHS head `len`.  So in fact at
    position `p` exactly one of ρ₁, ρ₂ applies (depending on whether
    `t|_p = len(nil)` or `t|_p = len(cons(a, b))`).  Either is in
    `R'(t)`.
  - If ρ ∈ {ρ₃, ρ₄}, the LHS head is `c`, and both ρ₃ and ρ₄ apply
    at position `p`.  Both are in `R'(t)`.
  - If ρ ∈ {ρ₅, ρ₆}, the LHS head is `f` and `t|_p = f(u)` for some
    closed `u`.  Both ρ₅ and ρ₆ have LHS `f(x)` and each matches
    `f(u)` with `x := u`.  So `(p, ρ₆) ∈ R(t)` as well, and `(p,
    ρ₆) ∈ R'(t)`.

In every case `R'(t) ≠ ∅`.  So S halts only at terms where even
`R(t) = ∅`, i.e. true R-normal forms.  ✓

**Polynomial measure μ.**  Define μ : closed terms → ℕ₊ by:

| symbol        | μ-interpretation         |
|---------------|--------------------------|
| `0`           | μ(0) = 1                 |
| `nil`         | μ(nil) = 1               |
| `a`           | μ(a) = 1                 |
| `s(x)`        | μ(s(x)) = μ(x) + 1       |
| `cons(x, y)`  | μ(cons(x, y)) = μ(x) + μ(y) + 1 |
| `len(x)`      | μ(len(x)) = 2·μ(x) + 1   |
| `c(x, y)`     | μ(c(x, y)) = μ(x) + μ(y) + 2 |
| `f(x)`        | μ(f(x)) = 2·μ(x) + 1     |

By induction every closed term has μ ≥ 1 (each base atom gives 1,
and every constructor's formula is at least `1 + (non-negative
stuff)`).

**Strict monotonicity of μ in each argument of each constructor.**
For each constructor `g` the μ-formula is a polynomial `α₁·x₁ + … +
αₖ·xₖ + β` with each `αᵢ ≥ 1`:  `s` has (1; +1), `cons` has (1, 1;
+1), `len` has (2; +1), `c` has (1, 1; +2), `f` has (2; +1).
Strict monotonicity in `xᵢ` is equivalent to `αᵢ > 0`, which holds
for every coefficient listed.  Hence if a subterm strictly decreases
in μ, every enclosing context strictly decreases in μ.

**Per-rule strict decrease of μ for non-ρ₅ rules.**  Each difference
`μ(LHS) − μ(RHS)` below is computed treating LHS variables as
positive-integer unknowns (each ≥ 1, since ground terms have μ ≥ 1):

| rule | μ(LHS)                                  | μ(RHS)               | μ(LHS) − μ(RHS)    | > 0 for all ground θ? |
|------|------------------------------------------|----------------------|--------------------|-----------------------|
| ρ₁   | μ(len(nil)) = 2·1 + 1 = 3                | μ(0) = 1             | 2                  | ✓ (constant)          |
| ρ₂   | μ(len(cons(x, ys))) = 2(μx + μys + 1) + 1 = 2μx + 2μys + 3 | μ(s(len(ys))) = (2μys + 1) + 1 = 2μys + 2 | 2μx + 1 | ≥ 3          |
| ρ₃   | μ(c(x, y)) = μx + μy + 2                 | μ(x) = μx            | μy + 2             | ≥ 3                   |
| ρ₄   | μ(c(x, y)) = μx + μy + 2                 | μ(y) = μy            | μx + 2             | ≥ 3                   |
| ρ₅   | μ(f(x)) = 2μx + 1                        | μ(f(s(x))) = 2(μx + 1) + 1 = 2μx + 3 | −2 | **< 0 — μ INCREASES**  |
| ρ₆   | μ(f(x)) = 2μx + 1                        | μ(nil) = 1           | 2μx                | ≥ 2                   |

Every rule except ρ₅ strictly decreases μ.  Rule ρ₅ strictly
*increases* μ by 2 — which is why it is excluded from strategy S.

`sim.py` section D verifies these differences over a 5- to 49-sample
grid of ground instantiations; every minimum is strictly positive
for ρ₁, ρ₂, ρ₃, ρ₄, ρ₆ and strictly negative for ρ₅.

**Single-step strict decrease under S.**  If S selects `(p, ρ)` with
ρ ≠ ρ₅, then `t|_p = LHS·θ` reduces to `RHS·θ` in the subterm, and
by per-rule decrease `μ(LHS·θ) > μ(RHS·θ)`.  By context monotonicity,
`μ(t) > μ(t[p ← RHS·θ])`.  Hence every S-step strictly decreases μ.

**Termination of S.**  An S-trace `t₀ → t₁ → t₂ → …` would give `μ(t₀)
> μ(t₁) > μ(t₂) > …`, an infinite strictly-descending sequence of
positive integers.  No such sequence exists.  Hence S halts in at
most `μ(t₀) − 1` steps from any `t₀`, and §4.2 item (W3) gives that
the halting point is a real normal form of R.

### 3.3 Infinite-reduction construction for Q3

Take `t₀ = f(0)` and for each `i ≥ 0` fire ρ₅ at the root:

```
t₀ = f(0)
t_(i+1) = (reduce t_i at root by ρ₅) = f(s(k_i))    where k_i is t_i's argument
```

Equivalently, `tᵢ = f(sⁱ(0))` where `sⁱ` denotes `i`-fold application
of `s` and `s⁰(0) = 0`.

**ρ₅ applies at the root of every tᵢ.**  `tᵢ = f(sⁱ(0))` matches LHS
`f(x)` with `x := sⁱ(0)`.  The ρ₅-reduct is `f(s(sⁱ(0))) = f(s^(i+1)(0)) =
t_(i+1)`.  ✓

**Height strictly grows.**  Define `height(0) = height(nil) =
height(a) = 1`, `height(g(t₁, …, tₖ)) = 1 + max(height(tᵢ))`.  Then
`height(sⁱ(0)) = i + 1` and `height(tᵢ) = height(f(sⁱ(0))) = i + 2`.
In particular `height(tᵢ) ≠ height(tⱼ)` for `i ≠ j`, so tᵢ ≠ tⱼ as
syntactic terms — the sequence has no repeats.

**The sequence is infinite and acyclic.**  Infinite: the recursion
defines `t_(i+1)` from `tᵢ` for every `i`, and each defining step is
a valid ρ₅-rewrite.  Acyclic: a cycle would require `tᵢ = tⱼ` for
some `i ≠ j`, contradicting height growth.

This directly witnesses failure of SN.  `sim.py` section C traces
steps 0 through 10 explicitly.

---

## 4. Final verdict

### 4.1 Q1 answer — R is NOT confluent

**Witness.**  `t = c(0, nil)`.

**Reduction 1.**
```
c(0, nil)  →_ρ₃  0
```
(by ρ₃ with substitution `x := 0, y := nil`).

**Reduction 2.**
```
c(0, nil)  →_ρ₄  nil
```
(by ρ₄ with the same substitution).

**u = 0 is a normal form.**  Positions of `0`: only ε.  At ε, `0`
has head `0`, but no rule in R has LHS head `0`.  No rule matches.
Hence `0` is normal.

**v = nil is a normal form.**  Positions of `nil`: only ε.  At ε,
`nil` has head `nil`, but no rule in R has LHS head `nil` (ρ₁'s LHS
is `len(nil)`, head `len`).  No rule matches.  Hence `nil` is normal.

**u ≠ v.**  `0` and `nil` are distinct nullary constructors and
hence syntactically distinct terms.

Apply SL-1 (§2.1): distinct-NFs from a shared source → not
confluent.

Hence **R is not confluent**, witnessed by `t = c(0, nil) ↠ 0` and
`t = c(0, nil) ↠ nil`.  `sim.py` section B mechanically confirms the
two reducts, checks normality of each by exhaustive redex
enumeration, and confirms inequality.

### 4.2 Q2 answer — R is weakly normalizing

**Claim.**  Every closed term `t₀` has a reduction sequence
terminating at a normal form.

**Proof.**  Let S be the strategy of §3.2.  By §3.2 *progress*, at
every closed non-normal term S selects a redex (applying one of ρ₁,
ρ₂, ρ₃, ρ₄, ρ₆).  By SL-2 (cited from §3.2), every S-step strictly
decreases μ.  The ordinary "<" on ℕ₊ admits no infinite strictly-
descending sequence, so S produces at most `μ(t₀) − 1` steps and
halts.  By §3.2 construction, S halts only at terms where no R-rule
applies anywhere — i.e., at R-normal forms.  Hence the finite S-
trace starting from `t₀` is a reduction sequence of R that
terminates at a normal form.  ∎

This is WN: we exhibited, for every closed `t₀`, a specific
terminating reduction.  SN is a *different* statement (every
reduction terminates), and SL-2's silence on ρ₅ does not close SN
because ρ₅-sequences can still exist and can still be infinite.

`sim.py` section E runs S on a suite of six seed closed terms and
confirms every run terminates in at most 4 S-steps with μ strictly
decreasing along every step and a real normal form at the end.

### 4.3 Q3 answer — R is NOT strongly normalizing

**Witness.**  `t₀ = f(0)`.

**Infinite reduction sequence.**

```
t₀ = f(0)
 →_ρ₅ at ε        f(s(0))                        = t₁
 →_ρ₅ at ε        f(s(s(0)))                     = t₂
 →_ρ₅ at ε        f(s(s(s(0))))                  = t₃
 →_ρ₅ at ε        f(s(s(s(s(0)))))               = t₄
 →_ρ₅ at ε        f(s(s(s(s(s(0))))))            = t₅
     ⋮                              ⋮
 →_ρ₅ at ε        tᵢ  ↦  f(sⁱ⁺¹(0)) = t_(i+1)     for every i ≥ 0
     ⋮                              ⋮
```

At every step, ρ₅ matches the entire term `tᵢ = f(sⁱ(0))` with the
substitution `x := sⁱ(0)` and produces `f(s(sⁱ(0))) = f(s^(i+1)(0)) =
t_(i+1)`.

**Sequence is genuinely infinite and acyclic.**  Apply SL-3 (§2.3):
height(tᵢ) = i + 2 strictly grows in `i`, so no two `tᵢ, tⱼ` are
syntactically equal when `i ≠ j`, so the sequence contains no cycle
and the definition `t_(i+1)` is valid at every `i`.

Hence **R is not strongly normalizing**, witnessed by `t₀ = f(0)`
and the ρ₅-trajectory above.  `sim.py` section C mechanically
executes the first 10 steps and confirms the height-growth invariant.

### 4.4 Cross-question relationships

Four classical implications could be in play.  Only one is invoked
below, and it is derived from first principles rather than cited.

**(a) "SN implies WN."**  This would say: if every reduction from
`t₀` terminates, then some reduction from `t₀` terminates.  Trivially
true by pointing at any reduction.  But SN *fails* for R, so this
implication is not available as a Q2 proof for R; we proved Q2
directly via SL-2.

**(b) "Non-SN implies non-WN."**  False in general: the existence of
one infinite reduction does not preclude the existence of another
terminating one.  For R this is exactly the situation: ρ₅-only
reductions are infinite (Q3), but ρ₆-preferring reductions terminate
(Q2).  R sits in the region "WN but not SN", which is precisely
allowed when a diverging rule is shadowed by a converging one at
the same redex position.

**(c) "Non-confluence implies non-WN (or non-SN)."**  False in
general, and false for R.  A terminating non-confluent system with
multiple distinct normal forms (e.g., a → b, a → c with b, c both
normal) is non-confluent yet strongly normalizing.  For R, Q2 holds
despite Q1 failing.

**(d) "Confluence + WN implies unique normal forms (when they
exist)."**  Derivation from first principles for this session: if
R were confluent and weakly normalizing, take any `t₀` and any two
reductions to normal forms `t₀ ↠ u` and `t₀ ↠ v`; confluence gives
`w` with `u ↠ w` and `v ↠ w`; normality of `u` and `v` forces `u =
w = v`.  Contrapositively, *two distinct normal-form reducts of the
same source witness non-confluence* — this is SL-1 again.  Our
Q1 witness (`c(0, nil)` with NFs `0` and `nil`) is a concrete
instance.

So the cross-question picture for R is:

```
 Q1: NOT confluent         \  witnessed by c(0, nil)
 Q2: WN                     \  via strategy S (never-ρ₅)
 Q3: NOT SN                 \  witnessed by f(0) →_ρ₅ f(s(0)) → …

Q2 holds *despite* Q3 failing — the textbook "shadowed diverging rule" pattern.
Q1 fails *independently* of Q2 and Q3 — its failure is carried entirely by
ρ₃/ρ₄'s shared LHS with distinct projections.
```

No verdict here was inferred from another by an abstract implication
we did not check; each was witnessed directly.

---

## 5. Verification strategy

Two channels.

### 5.1 Channel A — symbolic / hand argument (this document)

  - **Q1:** explicit ground witness `c(0, nil)`; explicit reduction
    to `0` (ρ₃) and to `nil` (ρ₄); explicit normality check by
    position enumeration (`0` and `nil` have only position ε and no
    rule's LHS has those heads); explicit inequality of syntactic
    terms.  SL-1 closes the verdict.
  - **Q2:** explicit strategy S with leftmost-outermost redex
    selection on the set of non-ρ₅ redexes; explicit per-rule
    polynomial difference `μ(LHS) − μ(RHS)` computed as a polynomial
    in the free variables; each is shown strictly positive under
    positive-integer substitutions by algebraic inspection (§3.2
    table).  Applicability of S shown by case-split on the head
    symbol at a redex position (three cases: len, c, f).
  - **Q3:** explicit term `f(0)`, explicit recurrence `t_(i+1) =
    f(s(tᵢ.arg))`, explicit height invariant `height(tᵢ) = i + 2`,
    explicit conclusion of acyclicity and infinitude.

### 5.2 Channel B — executable oracle (`task/sim.py`)

Five mechanical checks, all of which pass (log at
`task/sim_output.txt`):

  1. **Critical-pair enumeration by unification** (sim.py §A).  For
     every ordered pair of rules and every non-variable position of
     the outer rule's LHS, first-order unification determines
     whether an overlap exists.  The oracle finds four
     non-trivially-equal CP instances, matching §3.1: two for the
     (ρ₃, ρ₄) root overlap (in both directions), two for the
     (ρ₅, ρ₆) root overlap.

  2. **Q1 witness** (sim.py §B).  The term `c(0, nil)` is built,
     reduced via ρ₃ to `0` and via ρ₄ to `nil`, each reduct is
     mechanically verified to have no applicable rule at any
     position, and the two reducts are checked unequal.  All checks
     pass.

  3. **Q3 witness** (sim.py §C).  Starting from `f(0)`, ten ρ₅-steps
     are fired explicitly, confirming the reduction is valid at
     every step and the s-stack depth strictly grows.

  4. **Q2 per-rule μ-inequalities** (sim.py §D).  For each rule, the
     difference `μ(LHS) − μ(RHS)` is evaluated over a sample grid
     of ground instantiations (1 to 49 samples depending on the
     rule's variable count).  Every sample's δ for ρ₁, ρ₂, ρ₃, ρ₄,
     ρ₆ is strictly positive; every sample's δ for ρ₅ is strictly
     negative (−2).  This confirms that ρ₅ must be excluded from
     the strategy, consistent with §3.2.

  5. **Q2 strategy-S simulation** (sim.py §E).  For each of six
     seed closed terms, S is executed step by step, μ is tracked,
     and after halting the final term is checked for normality by
     exhaustive redex enumeration.  All six seeds reduce to a real
     normal form with strictly decreasing μ at every step.

The oracle is designed as a *falsifier*: any missing CP, any
mis-specified rule, any non-decreasing edge under S, or any seed
reaching a "normal form" that in fact has an applicable rule would
surface as a Python assertion failure or as output discrepancy with
§3/§4.  None arise.

---

## 6. Worked examples

Four reduction scenarios, each stress-testing a distinct axis of the
verdict.

### 6.1 Example (a) — Q1 divergent pair, both sides normal

`t = c(0, nil)`.

```
trace 1 (via ρ₃):    c(0, nil)  →_ρ₃ at ε   0        mu: 4 → 1  — normal form
trace 2 (via ρ₄):    c(0, nil)  →_ρ₄ at ε   nil      mu: 4 → 1  — normal form
```

Both reducts are normal forms, and `0 ≠ nil`.  This is the
non-confluence witness of §4.1.

### 6.2 Example (b) — WN terminates, SN fails, from the same term

`t = f(0)`.

Terminating reduction (strategy S selects ρ₆):

```
 f(0)   →_ρ₆ at ε   nil                        mu: 3 → 1
```

One step, normal form.

Infinite reduction (adversarial selection fires ρ₅ indefinitely):

```
 f(0)
  →_ρ₅ at ε   f(s(0))                          mu: 3 → 5     (mu grows)
  →_ρ₅ at ε   f(s(s(0)))                       mu: 5 → 7
  →_ρ₅ at ε   f(s(s(s(0))))                    mu: 7 → 9
  →_ρ₅ at ε   f(s(s(s(s(0)))))                 mu: 9 → 11
     ⋮
```

From the same starting term we display both a terminating reduction
(witnessing Q2) and an infinite reduction (witnessing Q3).  This is
the structural signature of "WN but not SN": a shadowed diverging
rule.

### 6.3 Example (c) — deterministic len reduction on a 2-element list

`t = len(cons(a, cons(0, nil)))`.  μ(t) = 11.

```
 len(cons(a, cons(0, nil)))             mu = 11
  →_ρ₂ at ε           s(len(cons(0, nil)))            mu = 8
  →_ρ₂ at (1)         s(s(len(nil)))                  mu = 5
  →_ρ₁ at (1, 1)      s(s(0))                         mu = 3
```

The reduction uses only ρ₁ and ρ₂; no choices (no ρ₃, ρ₄, or f-
redexes arise).  μ strictly decreases at each step.  Final term
`s(s(0))` has no redex (no rule matches `0` or `s(·)` patterns) —
normal form.  This exercises the "deterministic inductive part" of
R, establishing that list-length computation terminates cleanly
independent of the choice / f-machinery.

### 6.4 Example (d) — interleaved c / f / len

`t = c(f(0), len(cons(s(0), cons(a, nil))))`.  μ(t) = 18.

Strategy S:
```
 c(f(0), len(cons(s(0), cons(a, nil))))                mu = 18
  →_ρ₃ at ε         f(0)                               mu =  3
  →_ρ₆ at ε         nil                                mu =  1
```

Two steps, normal form `nil`, μ drops 18 → 3 → 1.

Alternative strategy (reduce the len-subterm first):
```
 c(f(0), len(cons(s(0), cons(a, nil))))                mu = 18
  →_ρ₂ at (2)       c(f(0), s(len(cons(a, nil))))      mu = 15
  →_ρ₂ at (2, 1)    c(f(0), s(s(len(nil))))            mu = 12
  →_ρ₁ at (2,1,1)   c(f(0), s(s(0)))                   mu = 10
  →_ρ₃ at ε         f(0)                               mu =  3
  →_ρ₆ at ε         nil                                mu =  1
```

Different trace, same normal form `nil`.  This illustrates that in
closed terms not involving `c(·,·)` ambiguity at the surface, S is
insensitive to where it starts reducing; all non-ρ₅ reductions
converge here.

A *third* trace that fires ρ₄ instead of ρ₃:
```
 c(f(0), len(cons(s(0), cons(a, nil))))                mu = 18
  →_ρ₄ at ε         len(cons(s(0), cons(a, nil)))      mu = 13
  →_ρ₂ at ε         s(len(cons(a, nil)))               mu =  8
  →_ρ₂ at (1)       s(s(len(nil)))                     mu =  5
  →_ρ₁ at (1,1)     s(s(0))                            mu =  3
```

Normal form `s(s(0))` — **different from the first trace's `nil`**.
This is another manifestation of Q1 non-confluence: the same closed
starting term admits two reductions to two distinct normal forms.
The Q2 strategy S (which prefers ρ₃) picks one branch; a different
strategy preferring ρ₄ picks the other; both are valid WN-
terminating reductions, but they commit to incomparable normal
forms.

### 6.5 Table of example coverage

| example | axis stressed                                     |
|---------|---------------------------------------------------|
| 6.1     | Q1 divergent pair (both reducts normal, unequal)  |
| 6.2     | same seed, WN-terminating vs non-SN infinite      |
| 6.3     | deterministic len-only subsystem terminates       |
| 6.4     | interleaved c / f / len; multiple NFs per seed (also re-confirms Q1) |

---

## 7. Open questions and known limitations

### 7.1 Parametric disclosure: no single-rule removal from R restores confluence without also disabling the shared-LHS choice primitive

The non-confluence of R is carried entirely by the pair (ρ₃, ρ₄)
sharing the exact LHS `c(x, y)` and projecting to the two distinct
variables.  Remove ρ₃ alone: ρ₄ remains and the `c(·,·)` symbol
reduces deterministically to its second argument — confluence is
restored but the choice primitive is gone.  Remove ρ₄ alone:
symmetric.  Remove both: `c(·,·)` becomes a constructor with no
reduction rule — again confluent (no redex), again the choice
primitive is gone.

What about removing rules *other than* ρ₃ or ρ₄?

  - Remove ρ₁: the ground witness `c(0, nil)` is unaffected (ρ₁ is
    not used in the Q1 derivation).  Still non-confluent.
  - Remove ρ₂: same.  Still non-confluent.
  - Remove ρ₅: f-behavior becomes "f(x) → nil" unconditionally, but
    ρ₃/ρ₄ still project `c(0, nil)` to distinct NFs.  Still non-
    confluent.
  - Remove ρ₆: ρ₅ becomes the only f-rule, but ρ₃/ρ₄ on `c(0, nil)`
    are still divergent.  Still non-confluent.

**Parametric statement.**  Every single-rule removal from R that
leaves both ρ₃ and ρ₄ in place leaves `c(0, nil)` as a non-
confluence witness; every single-rule removal that eliminates ρ₃ or
ρ₄ also eliminates the shared-LHS choice structure (the only rule
pair in R with unifying LHSs projecting to distinct variables).
Hence R's non-confluence is structurally pinned to the choice
primitive ρ₃/ρ₄; no purely local editing short of losing that
primitive restores confluence.  The same parametric reasoning applies
to *any* TRS that contains two rules `g(v̄) → x_i` and `g(v̄) → x_j`
for distinct LHS variables `x_i, x_j`; such a pair is an essentially
non-confluent choice primitive.

### 7.2 Parametric characterization of WN-successful strategies

The specific S we built is "leftmost-outermost over non-ρ₅
redexes".  A wider parametric family works:

  - *Strategies within the family:* any redex-selection discipline
    that (i) is applicable at every non-normal closed term and (ii)
    never fires ρ₅.  Applicability was discharged by showing every
    closed non-normal term has a non-ρ₅ redex.  Hence *any* tie-
    breaking (innermost, rightmost, random, etc.) over the set of
    non-ρ₅ redexes still terminates in `≤ μ(t₀) − 1` steps under
    the same μ.

  - *Strategies outside the family that still succeed:* mixed
    strategies may fire ρ₅ *finitely many* times, as long as they
    eventually halt.  The μ-drop argument does not cover such
    strategies (ρ₅ raises μ), but other arguments could — e.g.,
    bound ρ₅-firings by a fresh counter and fire ρ₆ at least once
    per ρ₅.

  - *Strategies guaranteed to fail:* firing only ρ₅ at some
    f-subterm (never ρ₆ there) produces the §4.3 infinite chain and
    never halts.  In particular, "always fire the first applicable
    rule in numeric order" would loop on any f-redex.

So the family "never fire ρ₅" is *sufficient* but not *necessary*
for WN.  The characterization of the exact success boundary is open
— it is at least as hard as distinguishing terms where ρ₅ is safe
(the residual f-subterm will be collapsed later by a ρ₆-step
elsewhere) from terms where it is fatal.

### 7.3 Sensitivity of the SN-failure witness to the chosen measure

The non-SN verdict is witness-based (concrete infinite reduction),
so it does not depend on a measure choice.  But one could ask: is
the *form* of the measure we *would need* to witness SN (if SN
held) structurally obstructed?

Parametric claim: **no polynomial interpretation over ℕ₊ that is
strictly monotone in every argument can make ρ₅ strictly decrease.**

Proof sketch.  Suppose `μ(f(x)) = P(x)` for some polynomial `P` that
is strictly monotone increasing (coefficient of `x` is at least 1 at
every occurrence of `x` in `P`, with the natural extension to higher
degrees).  Then `μ(f(s(x))) = P(s(x)) = P(μ(s(x)))`.  With `s`
strictly increasing in its argument, `μ(s(x)) > μ(x)`, and because
`P` is strictly monotone, `P(μ(s(x))) > P(μ(x))`.  Hence `μ(f(s(x)))
> μ(f(x))`, i.e., ρ₅ strictly *increases* μ.  Identical reasoning
fails for any measure of this class: *strict monotonicity plus
strict `s`-growth plus "P is increasing" forces ρ₅ to go up*.

So the non-SN verdict is robust under the entire family of
strictly-monotone polynomial measures; to witness SN (were it true,
which it isn't here) one would need either a measure that is
*non*-monotone in some constructor — breaking context-closure — or
a multiset / lexicographic / ordinal-rank measure that escapes the
strictly-monotone polynomial family entirely.  The parametric
obstruction aligns with our verdict: no measure of this class could
prove SN for R, because SN is false.

### 7.4 Generalizations of the pattern

Three structural claims, each derived from first principles for
this specific R and visibly generalizable:

  (i) **Every TRS containing a pair of rules `g(v̄) → x_i` and
      `g(v̄) → x_j` with `i ≠ j` fails confluence.**  The two
      projections applied to `g(t₁, …, tₖ)` with `t_i` and `t_j`
      having distinct normal forms (always constructible when the
      TRS has at least two distinct ground normal forms) give two
      non-joinable reducts.

  (ii) **Every TRS containing a rule `f(x) → f(h(x))` with `h`
      structure-preserving (height-increasing on closed terms) fails
      SN.**  Apply the rule indefinitely at the root; height grows;
      the sequence is infinite and acyclic.  Our ρ₅ with `h = s`
      instantiates this.

  (iii) **WN can coexist with failure of SN when a rule of shape
      `f(x) → f(h(x))` is shadowed by another rule `f(x) → c` with
      `c` a ground normal form.**  Choose the second rule at every
      f-redex.  This is exactly the ρ₅ / ρ₆ dynamic.  The
      parametric statement: this shadow pattern is a complete
      recipe for building WN-but-not-SN systems; it is the same
      structural idea as lazy evaluation preferring a constant
      alternative over a recursive one.

These three claims together explain why R's (Q1, Q2, Q3) =
(NO, YES, NO) verdict is not a coincidence specific to R but a
structural consequence of the rule shapes it contains.

### 7.5 Limitations of this writeup

  - The confluence analysis discharges the non-confluence verdict
    rigorously, but does *not* attempt to characterize *which*
    closed terms of R have unique normal forms.  That question —
    "given `t`, decide whether all reductions of `t` terminate at
    the same normal form" — is open here; clearly the f-free,
    c-free fragment does (strategy-independent), but mixed terms
    can inherit the ρ₃/ρ₄ divergence (see Example 6.4's third
    trace).

  - The WN strategy S is one family; we have not ruled out that a
    simpler measure suffices or that a strategy firing ρ₅ finitely
    often might also succeed.  See §7.2.

  - The non-SN witness is a root-only ρ₅-trajectory.  Non-SN
    reductions buried inside larger contexts (where ρ₅ fires at a
    non-root f-subterm) are possible and are handled symmetrically
    by context-closure, but are not individually enumerated.

---

## Summary

  - **Q1 — R is NOT confluent.**  Witness: `c(0, nil) →_ρ₃ 0` and
    `c(0, nil) →_ρ₄ nil`; both reducts are normal forms; `0 ≠ nil`.
    Full CP enumeration (§3.1) confirms this is the one non-joinable
    overlap; all others (self-overlaps, (ρ₅, ρ₆) and its mirror) are
    joinable.

  - **Q2 — R IS weakly normalizing.**  Strategy S (leftmost-
    outermost among non-ρ₅ redexes) reduces every closed term to a
    normal form in at most `μ(t₀) − 1` steps, where μ is the
    polynomial interpretation of §3.2.  Applicability holds because
    every f-redex admits ρ₆ as an alternative to ρ₅.  Every S-step
    strictly decreases μ.

  - **Q3 — R is NOT strongly normalizing.**  Witness: `t₀ = f(0)`,
    `t_(i+1) = reduce tᵢ at root by ρ₅ = f(sⁱ⁺¹(0))`.  Each tᵢ has
    height `i + 2`, so the sequence has no cycle and is infinite.

  - **Verification:** §3 / §4 (symbolic) plus `task/sim.py`
    (executable) agree on every concrete claim.  Log at
    `task/sim_output.txt`.
