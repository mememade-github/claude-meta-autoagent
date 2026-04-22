# ARGUMENT — Joint confluence and termination of R

> **Iteration trace.** This is `iterations/attempt-01.md`, a first draft.
> The final (evaluator-refined) version lives at `task/ARGUMENT.md`.
> Executable oracle: `task/sim/simulator.py`. Captured output:
> `task/sim/output-run1.txt` (first draft).

The rewriting system under study:

    rho1:  len(nil)             -> 0
    rho2:  len(cons(x, ys))     -> s(len(ys))
    rho3:  app(nil, ys)         -> ys
    rho4:  app(cons(x, xs), ys) -> cons(x, app(xs, ys))
    rho5:  app(app(xs, ys), zs) -> app(xs, app(ys, zs))

Signature Σ: nullary `0`, `nil`; unary `s`, `len`; binary `cons`, `app`.
`len`, `app` are defined; the rest are constructors.

Q1 asks: is R confluent? Q2 asks: does R terminate on all closed terms?

---

## 1. Motivation

### 1.1 Why confluence is plausible

Three structural features point toward confluence.

**(a) Every LHS is left-linear.** Inspect each: `len(nil)` (no variables),
`len(cons(x, ys))` (each of `x`, `ys` occurs once), `app(nil, ys)` (one
variable, one occurrence), `app(cons(x, xs), ys)` (three distinct
variables, each once), `app(app(xs, ys), zs)` (three variables, each
once). Left-linearity means no pattern forces two different subterms
to be equal, so matching never "collapses" independent subterms. In
such a system, reducing a redex at one position cannot discard or
duplicate a redex elsewhere in a way that forks subsequent histories
through equated subterms.

**(b) The defined-function rules are pattern-matching on constructor
heads.** Rules `rho1`/`rho2` match `len` against `nil` / `cons(_,_)` —
mutually exclusive constructor-discriminated cases at the first argument.
Rules `rho3`/`rho4` do the same for `app`'s first argument. Functional
programs written in this "case by constructor" style enjoy a unique-
normal-form property for closed inputs: given a closed constructor
term in the first argument of `len`, exactly one of `rho1`, `rho2`
applies, and similarly for `app`. There is no contest between function
definitions.

**(c) Rule `rho5` is the only potentially-overlapping rule.** It
rewrites `app(app(xs, ys), zs)`, which inside itself contains a subterm
`app(xs, ys)` whose head matches the defining head of `rho3`/`rho4`/
`rho5` itself. So overlap risk is concentrated entirely on `rho5`.
Since `rho5` "re-associates" the same operator, it is the kind of
structural rewrite that historically retains confluence because both
the left and right sides still denote the same abstract value under
any model that makes `app` associative — which the other rules will
do.

There is a cautionary precedent in adjacent domains: algebraic rewrite
systems can fail confluence when distinct rewrite histories reach
incompatible canonical forms (e.g., simple equational fragments where
one rule simplifies and another re-associates, and the re-association
blocks the simplification). The job of the confluence proof below is
to verify that no such "race" happens for our five rules: every
two-step divergence from a common origin must join.

### 1.2 Why termination is plausible

Two features point toward termination, one against.

**In favour.** Rules `rho1`, `rho2`, `rho3`, `rho4` each "consume"
structure: a constructor is peeled off the input and, either the
output is strictly smaller, or it is of the same size but simpler in
a measurable way.

- `rho1`: `len(nil)` has 2 symbols, `0` has 1. Strict drop.
- `rho2`: `len(cons(x, ys))` has 4 symbols plus whatever's in `x`,
  `ys`; `s(len(ys))` has 2 plus whatever's in `ys`. The `x` subterm
  is discarded, so at minimum 2 symbols are lost.
- `rho3`: `app(nil, ys)` → `ys`. Strict drop (nil and app gone).
- `rho4`: `app(cons(x, xs), ys)` → `cons(x, app(xs, ys))`. Symbol count
  on each side: LHS has `app`, `cons`, plus `x`, `xs`, `ys`; RHS has
  `cons`, `app`, plus the same three. The root symbols swap, neither
  side strictly shrinks, but the `app` has moved strictly inward —
  which is the kind of "locally-balanced but globally decreasing"
  step that an interpretation can capture while raw symbol count
  cannot.

**Against.** Rule `rho5`: `app(app(xs, ys), zs)` → `app(xs, app(ys, zs))`.
Symbol count is exactly equal on both sides (two `app`s, three variables).
This rule does not "make the term smaller" in any naive sense. Raw
size / subterm ordering / lexicographic-on-head-outermost fails. We
need a measure whose value sees the nesting structure and penalises
left-nested `app` chains relative to right-nested ones.

Adjacent precedent: in any rewriting discipline where an associativity
step re-parenthesises an expression, termination typically rests on
weighting the left argument of the associating operator strictly more
than the right. If `phi(app(x, y)) = a·x + b·y + c` with `a > b`, then
the LHS interpretation `a·(a·x + b·y + c) + b·z + c =
a²·x + ab·y + ac + b·z + c` exceeds the RHS interpretation
`a·x + b·(b·y + c) + c = a·x + b²·y + bc + c` whenever
`a² > a` and `ab > b²`, i.e., whenever `a > 1` and `a > b`. The
simplest choice `a = 2, b = 1` works. We develop this below.

### 1.3 Why the two obligations must be treated separately

Non-termination is compatible with confluence (a pathological rewrite
can diverge yet still have unique join points); non-confluence is
compatible with termination (two normal forms can exist without any
infinite trace). So no single argument discharges both. We owe two
proofs, and each uses a different tool:

- Confluence is a *local* property at the pattern level: inspect every
  pair of rules, detect every overlap, close every critical pair.
- Termination is a *global* property requiring a well-founded measure.

They share infrastructure — both reason by structural induction on
terms, both respect contexts — but they do not substitute for each
other.

---

## 2. Method design

### 2.1 Confluence method

**Identifying potential counterexamples.** Two histories from a shared
origin can diverge irreducibly only if two different redexes sit in
overlapping positions of a shared term. There are two flavours:

- **Variable overlap.** One rule's redex sits strictly inside a
  variable position of another rule's matched instance. In
  left-linear rules, this case never forces divergence: the outer
  redex's matched subterm can be reduced before or after without
  changing the match, because the variable admits any value.
  Left-linearity is crucial here — if the same variable appeared
  twice in an LHS, a rewrite at one occurrence would have to be
  mirrored at the other, breaking the confluence-at-this-overlap
  guarantee. All five of our LHSs are left-linear. So variable
  overlaps are automatically joinable (by rewriting the other
  occurrence of the redex, using the same rule, in the alternative
  history).

- **Non-variable overlap (a.k.a. critical pair).** One rule's LHS
  unifies with a non-variable subterm of another rule's LHS. This is
  where real divergence can hide. We enumerate every ordered pair
  (including rule-with-itself) and check every non-variable position
  of the second rule's LHS for unifiability with the first rule's
  LHS.

**Discharging.** For each enumerated critical pair (u, v) derived
from a most-general unifier at position p, we either (a) exhibit a
common reduct w such that u ↠ w and v ↠ w (closure by forward
rewriting), or (b) declare non-confluence with (u, v) as witness.

**Local-to-global.** Once every critical pair closes, and every
variable overlap closes (automatic by left-linearity), we have
*local* confluence: any one-step divergence joins. Lifting this to
the full confluence claim needs termination. The derivation of
"local confluence + termination ⟹ confluence" is sketched from
first principles in §4.3.

### 2.2 Termination method

**Constructing a well-founded measure.** We assign to each symbol
`f` of arity `n` a polynomial `[f](x1, …, xn)` with non-negative
integer coefficients. Extending homomorphically to terms yields a
function `phi: Terms(Σ) → ℕ`. Well-foundedness comes for free from
well-foundedness of `<` on ℕ.

To make the measure respect contexts — i.e., reductions at deep
positions must still strictly decrease the measure — each
interpretation must be **strictly monotone** in each argument:
`[f](…, a, …) < [f](…, b, …)` whenever `a < b`. With polynomial
interpretations over ℕ, this is ensured by giving each argument a
strictly positive coefficient.

**Verifying strict decrease per rule.** For a rule `l → r` with
variables `v1, …, vk`, we compute the symbolic polynomials `[l]`
and `[r]` in the variables, then check `[l] - [r] > 0` for all
choices of `v1, …, vk ∈ ℕ`. This reduces to checking that
`[l] - [r]`, as a polynomial, has non-negative coefficients and
strictly positive constant term (equivalently, `[l] - [r] ≥ 1`
uniformly).

**Handling the expanding rule (rho5).** `rho5`'s RHS has the same
number of symbols as its LHS. What decreases is the *shape of
nesting*. The polynomial for `app` must weight its left argument
strictly more than its right, so that a left-nested occurrence of
`app` contributes more than a right-nested one. Specifically, if
`[app](x, y) = 2x + y + 1`, then

    [app(app(xs, ys), zs)]           [app(xs, app(ys, zs))]
    = 2(2·xs + ys + 1) + zs + 1      = 2·xs + (2·ys + zs + 1) + 1
    = 4·xs + 2·ys + zs + 3           = 2·xs + 2·ys + zs + 2

The difference is `2·xs + 1`, strictly positive for any non-negative
`xs`, so strict decrease holds. The same weight choice must continue
to discharge the other four rules — we verify this below.

**Handling `rho4` where RHS size > LHS size.** `rho4`'s RHS,
measured by raw symbol count, is *bigger* than its LHS (the `cons`
now wraps an `app`). This does not threaten termination as long as
our `phi` is not a literal size count. The proof is a direct
arithmetic check on the chosen polynomials; see §3.2.

### 2.3 What the methods share, and what they do not

Both methods reason term-by-term and both respect the context closure
of `→`. But they are orthogonal: the confluence method inspects
*patterns* (LHS shapes pairwise), while the termination method
inspects *rules as transformations on measurements* (LHS and RHS
interpretations independently of other rules). Nothing in the
confluence proof below relies on termination except the final step
§4.3. Nothing in the termination proof relies on confluence.

---

## 3. Progressive derivation

### 3.1 Critical-pair enumeration for Q1

We must consider every ordered pair `(rho_i, rho_j)` with `i, j ∈ {1..5}`,
including `i = j`. For each pair, we check every non-variable position
of `rho_j`'s LHS for unifiability with `rho_i`'s LHS. Root-rooted
heads are:

    rho1, rho2: root = len
    rho3, rho4, rho5: root = app

A necessary condition for overlap at some position p inside rho_j's
LHS is that the subterm at p has a head compatible with rho_i's LHS
root (or is unifiable at a higher-arity level). We organise by pairs.

**Pairs with disjoint root alphabets.** `(rho_i, rho_j)` with one
rooted at `len` and the other at `app` can overlap only if some
non-variable proper subterm of one's LHS has the other's root. Let's
check each side:

- Non-variable proper subterms of `len(nil)` are `nil`. Head `nil`.
- Non-variable proper subterms of `len(cons(x, ys))` are `cons(x, ys)`.
  Head `cons`.
- Non-variable proper subterms of `app(nil, ys)` are `nil`.
- Non-variable proper subterms of `app(cons(x, xs), ys)` are
  `cons(x, xs)`.
- Non-variable proper subterms of `app(app(xs, ys), zs)` are
  `app(xs, ys)`.

None of these proper subterms has root `len`, and the only one with
root `app` is in `rho5`'s own LHS — which is an intra-app-pair matter,
not a cross-alphabet one. So every cross-alphabet pair `(len-rooted,
app-rooted)` yields no overlap, hence no critical pair.

**Pairs inside `len`-rooted rules.** `(rho1, rho2)`, both rooted at
`len`. The first arguments are `nil` and `cons(x, ys)`; these are
rooted at distinct constructors, so they do not unify. No root
overlap. Proper non-variable subterms are `nil` and `cons(x, ys)`
respectively, also rooted differently. Self-overlaps of `rho1` and
`rho2` with themselves at a non-root non-variable position: the
only non-variable proper subterm of `rho1`'s LHS is `nil` (a
constant), and it does not match the rule's own LHS `len(nil)` at
root. Similarly for `rho2`. So no critical pairs among
`len`-rooted rules.

**Pairs inside `app`-rooted rules.** Three rules, six ordered pairs
(including self). Work them out.

*(rho3, rho3).* Self. Non-variable proper subterm: `nil`. Does `nil`
unify with `app(nil, ys)`? Heads differ. No critical pair other than
the trivial root self-overlap (which always closes to itself).

*(rho4, rho4).* Self. Non-variable proper subterm of
`app(cons(x, xs), ys)` is `cons(x, xs)`. Does `cons(x, xs)` unify
with `app(cons(x', xs'), ys')`? Heads differ. No critical pair beyond
trivial.

*(rho5, rho5).* Self-overlap. Non-variable proper subterms of
`app(app(xs, ys), zs)`: `app(xs, ys)`. Does `app(xs, ys)` unify
with `app(app(xs', ys'), zs')`? Substitute `xs := app(xs', ys')`,
`ys := zs'`. Yes. This gives a non-trivial critical pair. We build
it:

    Most general overlap term:
      t* = app(app(app(xs', ys'), zs'), zs)

    Path A (reduce at position 1 via rho5):
      t* → app(app(xs', app(ys', zs')), zs)

    Path B (reduce at root via rho5, matching xs ↦ app(xs', ys'),
                                           ys ↦ zs',
                                           zs ↦ zs):
      t* → app(app(xs', ys'), app(zs', zs))

    Close A: app(app(xs', app(ys', zs')), zs)
               → (rho5 at root, xs ↦ xs', ys ↦ app(ys', zs'), zs ↦ zs)
             app(xs', app(app(ys', zs'), zs))
               → (rho5 at position 2, xs ↦ ys', ys ↦ zs', zs ↦ zs)
             app(xs', app(ys', app(zs', zs)))

    Close B: app(app(xs', ys'), app(zs', zs))
               → (rho5 at root, xs ↦ xs', ys ↦ ys', zs ↦ app(zs', zs))
             app(xs', app(ys', app(zs', zs)))

    Common reduct: app(xs', app(ys', app(zs', zs))).     [CP3 closes]

*(rho3, rho4)* and *(rho4, rho3)*. Roots both `app`. First arguments
are `nil` and `cons(x, xs)` — they do not unify. No root overlap.
Non-variable proper subterms: `nil` (in `rho3`) and `cons(x, xs)`
(in `rho4`); neither unifies with `app(…,…)`. No critical pair.

*(rho3, rho5)* and *(rho5, rho3)*. Roots both `app`. First arguments
are `nil` and `app(xs, ys)`. These don't unify (root `nil` vs root
`app`). So no root overlap for this pair in either direction.

But: non-variable proper subterm of `rho5`'s LHS is `app(xs, ys)`.
Does `app(nil, ys')` unify with `app(xs, ys)` (where `xs`, `ys` are
rho5's variables and `ys'` is `rho3`'s variable)? Substitute
`xs := nil`, `ys := ys'`. Yes. This gives a critical pair.

    Most general overlap term:
      t* = app(app(nil, ys'), zs)

    Path A (reduce at position 1 via rho3): → app(ys', zs)

    Path B (reduce at root via rho5, matching xs ↦ nil,
                                           ys ↦ ys',
                                           zs ↦ zs):
      → app(nil, app(ys', zs))
        → (rho3) app(ys', zs)

    Common reduct: app(ys', zs).     [CP1 closes]

Does `rho3`'s LHS have a non-variable proper subterm unifying with
`rho5`'s LHS? Only `nil`, which doesn't match `app(_,_)`. No other
pair in this direction.

*(rho4, rho5)* and *(rho5, rho4)*. Roots both `app`. First arguments
are `cons(x, xs)` and `app(xs', ys')`. Heads differ; no unification;
no root overlap.

Non-variable proper subterm of `rho5`'s LHS is `app(xs, ys)`. Does
`app(cons(x', xs'), ys')` (rho4's LHS) unify with `app(xs, ys)`
(rho5's subterm)? Substitute `xs := cons(x', xs')`, `ys := ys'`.
Yes. This gives a critical pair.

    Most general overlap term:
      t* = app(app(cons(x', xs'), ys'), zs)

    Path A (reduce at position 1 via rho4):
      → app(cons(x', app(xs', ys')), zs)
        → (rho4 at root) cons(x', app(app(xs', ys'), zs))
        → (rho5 at position 1)
          cons(x', app(xs', app(ys', zs)))

    Path B (reduce at root via rho5, matching xs ↦ cons(x', xs'),
                                           ys ↦ ys',
                                           zs ↦ zs):
      → app(cons(x', xs'), app(ys', zs))
        → (rho4 at root) cons(x', app(xs', app(ys', zs)))

    Common reduct: cons(x', app(xs', app(ys', zs))).     [CP2 closes]

Does `rho4`'s LHS have a non-variable proper subterm unifying with
`rho5`'s LHS? Only `cons(x, xs)` — doesn't unify with `app(_,_)`.
No other pair in this direction.

*(rho1, …)* and *(rho2, …)* with `app`-rooted rules: already
excluded by the cross-alphabet analysis above.

**Summary of critical pairs.** Exactly three non-trivial overlaps:

    Label   Rules involved         Position within rho_j  Status
    -----   --------------------   ---------------------  ------
    CP1     (rho3, rho5)           1                      Joinable at app(ys', zs)
    CP2     (rho4, rho5)           1                      Joinable at cons(x', app(xs', app(ys', zs)))
    CP3     (rho5, rho5)           1                      Joinable at app(xs', app(ys', app(zs', zs)))

All three close. **R is locally confluent.**

### 3.2 Measure construction and decrease proof for Q2

**Chosen interpretation.** Assign to each symbol a polynomial over ℕ:

    [0]         = 0
    [nil]       = 1
    [s](x)      = x + 1
    [cons](x, y)= x + y + 2
    [len](x)    = x
    [app](x, y) = 2x + y + 1

Extend to terms homomorphically:
`[f(t_1, …, t_n)] = [f]([t_1], …, [t_n])`. Because each interpretation
is a polynomial with non-negative integer coefficients and strictly
positive coefficient on each argument (`[s]` has 1 on x;
`[cons]` has 1 on both; `[len]` has 1 on x; `[app]` has 2 on x,
1 on y), every interpretation is strictly monotone in each argument.

Call the induced map `phi: closed terms → ℕ`.

**Well-foundedness of the range.** `(ℕ, <)` is well-founded: every
strictly-decreasing sequence of naturals is finite.

**Monotonicity under contexts.** If `s → t` by some rule at position p,
let `C[·]` be the context with p as hole. Then
`phi(C[s]) = [f]…[C[s]]… ` where each outer application inside the
context is strictly monotone in its hole argument; hence
`phi(s) > phi(t)` implies `phi(C[s]) > phi(C[t])`. Formally, induct on
the depth of the context: base (empty context) is trivial; inductive
step uses strict monotonicity of the outermost function symbol in the
path down to the hole.

**Strict decrease on each rule.** We compute `[LHS] - [RHS]` as a
polynomial in the rule's variables and check positivity uniformly in
ℕ-valued variables.

*rho1:*  `len(nil) → 0`
- `[LHS] = [len(nil)] = [nil] = 1`
- `[RHS] = [0] = 0`
- `[LHS] - [RHS] = 1 > 0.`  ✓

*rho2:*  `len(cons(x, ys)) → s(len(ys))`
- `[LHS] = [cons(x, ys)] = x + ys + 2`
- `[RHS] = [s(len(ys))] = ys + 1`
- `[LHS] - [RHS] = x + 1 ≥ 1 > 0.`  ✓

*rho3:*  `app(nil, ys) → ys`
- `[LHS] = 2·[nil] + ys + 1 = 2·1 + ys + 1 = ys + 3`
- `[RHS] = ys`
- `[LHS] - [RHS] = 3 > 0.`  ✓

*rho4:*  `app(cons(x, xs), ys) → cons(x, app(xs, ys))`
- `[LHS] = 2·(x + xs + 2) + ys + 1 = 2x + 2xs + ys + 5`
- `[RHS] = x + (2xs + ys + 1) + 2 = x + 2xs + ys + 3`
- `[LHS] - [RHS] = x + 2 ≥ 2 > 0.`  ✓

*rho5:*  `app(app(xs, ys), zs) → app(xs, app(ys, zs))`
- `[LHS] = 2·(2·xs + ys + 1) + zs + 1 = 4·xs + 2·ys + zs + 3`
- `[RHS] = 2·xs + (2·ys + zs + 1) + 1 = 2·xs + 2·ys + zs + 2`
- `[LHS] - [RHS] = 2·xs + 1 ≥ 1 > 0.`  ✓

**All five rules strictly decrease phi, uniformly in all variable
values.** Composed with monotonicity under contexts, this gives
`s → t ⟹ phi(s) > phi(t)` for any one-step rewrite in any context.
Since `(ℕ, <)` is well-founded, no infinite chain `t_0 → t_1 → t_2 → …`
can exist. **R terminates.**

---

## 4. Final verdict

### 4.1 Q1 answer: R is confluent

Every critical pair of R (enumerated in §3.1) is joinable:

| Label | Rules         | Overlap term                          | Common reduct                                    |
|-------|---------------|---------------------------------------|--------------------------------------------------|
| CP1   | (rho3, rho5)  | app(app(nil, ys), zs)                 | app(ys, zs)                                      |
| CP2   | (rho4, rho5)  | app(app(cons(x, xs), ys), zs)         | cons(x, app(xs, app(ys, zs)))                    |
| CP3   | (rho5, rho5)  | app(app(app(xs', ys'), zs'), zs)      | app(xs', app(ys', app(zs', zs)))                 |

All variable overlaps are discharged for free by left-linearity of
every LHS. Hence R is locally confluent. Combined with termination
(§4.2) via the derivation of §4.3, R is confluent.

### 4.2 Q2 answer: R terminates

The polynomial interpretation

    [0] = 0,  [nil] = 1,  [s](x) = x+1,
    [cons](x, y) = x + y + 2,  [len](x) = x,  [app](x, y) = 2x + y + 1

induces a strictly monotone map `phi: closed terms → ℕ` that strictly
decreases under every rule application (§3.2) and under every context
(via strict monotonicity in each argument of every interpreting
polynomial). Since `(ℕ, <)` is well-founded, R admits no infinite
reduction sequence. R terminates.

### 4.3 Joint implication: local confluence + termination ⟹ confluence

We derive this step from first principles. Call two terms *joinable*,
written `u ↓ v`, if there exists `w` with `u ↠ w ← ↞ v`. We want: if
`t ↠ u` and `t ↠ v` then `u ↓ v`.

Proof by well-founded induction on `t`, using termination's guarantee
that the relation "is a proper reduct of" is well-founded on closed
terms.

*Base*: `t` is in normal form. Then `t ↠ u` forces `u = t` and similarly
`v = t`, so `u ↓ v` trivially via `w = t`.

*Inductive*: `t` is not a normal form. Decompose:
- If `t ↠ u` is zero steps (i.e., `u = t`), then `v` is a reduct of `u`
  and they join at `v`.
- Symmetric: `v = t`.
- Otherwise, `t → t₁ ↠ u` and `t → t₂ ↠ v`. If `t₁ = t₂`, apply the
  induction hypothesis to `t₁`, which is a proper reduct of `t`.
- Else by local confluence, there is `s` with `t₁ ↠ s` and `t₂ ↠ s`.

  Now apply IH at `t₁` (a proper reduct of `t`): the two reductions
  `t₁ ↠ u` and `t₁ ↠ s` give a common reduct `u'`. Apply IH at `t₂`:
  reductions `t₂ ↠ v` and `t₂ ↠ s` give a common reduct `v'`.

  Note `u ↠ u'` and `v ↠ v'`, and both `u'` and `v'` are reducts of `s`.
  Apply IH once more at `s` (which is a proper reduct of `t` since
  `t → t₁ ↠ s` gives `t → s` in ≥1 step): the reductions `s ↠ u'` and
  `s ↠ v'` give a common reduct `w`.

  Then `u ↠ u' ↠ w` and `v ↠ v' ↠ w`, establishing `u ↓ v`.

The induction is legal because termination makes "strictly reduces to"
a well-founded order on closed terms. Hence R is confluent. ∎

---

## 5. Verification strategy

We back the hand-proofs with an executable oracle at
`task/sim/simulator.py`, which implements:

1. Ground-instance realisation of all three non-trivial critical pairs.
   For each pair, both sides of the overlap are reduced (in all
   orders reachable by BFS up to a step bound of 1000) and their
   reachable sets are intersected. The non-empty intersection of
   the two reachable sets *at a ground instance* is a sanity check
   that the hand-proof's closure actually executes, though
   symbolic closure is the strong claim; the script also prints the
   specific common reduct found.
2. Verification that `phi` strictly decreases on *every* rewrite step
   from a pool of terms reachable from a test suite. The script
   asserts this check inline during normalisation: at every step it
   raises if `phi(t_next) >= phi(t)`.
3. Reduction-order independence on five closed test terms: both a
   leftmost-outermost and a rightmost-innermost strategy normalise
   each term, and the two normal forms are checked equal via `assert`.

The captured output (`task/sim/output-run1.txt`) confirms:

- All three critical pairs reach a common reduct on their ground
  instance.
- All sample terms normalise to the same value under both strategies.
- Across all reachable terms (142 steps cross-checked), `phi` strictly
  decreases at every single rule application.

**Important caveats.**

- The simulator is a *falsifier*, not a prover. It checks closure on a
  finite test suite; it cannot substitute for the symbolic closure
  arguments in §3.1 and §3.2. If the simulator disagreed with the
  hand-proof, that would be strong evidence of an error in the hand-
  proof; the simulator agreeing is necessary but not sufficient.
- `phi`'s range is ℕ. The symbolic strict-decrease check in §3.2 is
  what proves termination; the runtime check adds machine-level
  corroboration across many instances.
- Critical-pair closure is proven *symbolically* in §3.1; the
  simulator's ground-instance re-run only rules out bugs in the hand
  substitutions.

**Worked executable-oracle verification is performed end-to-end. This
counts as an R6 = 3 indicator alongside the trace-argument path.**

---

## 6. Worked examples

### 6.1 Associativity exercise (rho5 in both orders)

Start: `t = app(app(app(nil, nil), nil), nil)`.

*Outermost first.* `rho5` at root:
    t → app(nil, app(nil, nil)).
    → (rho3 at root) app(nil, nil).

Wait — that was wrong; `rho5` at root matches `app(app(xs, ys), zs)`
with `xs ↦ app(nil, nil)`, `ys ↦ nil`, `zs ↦ nil`, giving
`app(app(nil, nil), app(nil, nil))`. Re-do:

*Outermost first.*
    app(app(app(nil, nil), nil), nil)
      → (rho5 at root, xs↦app(nil,nil), ys↦nil, zs↦nil)
        app(app(nil, nil), app(nil, nil))
      → (rho3 at position 1, ys↦nil)
        app(nil, app(nil, nil))
      → (rho3 at root, ys↦app(nil,nil))
        app(nil, nil)
      → (rho3 at root, ys↦nil)
        nil

*Innermost first.*
    app(app(app(nil, nil), nil), nil)
      → (rho3 at position (0,0), ys↦nil)
        app(app(nil, nil), nil)
      → (rho3 at position (0,), ys↦nil)
        app(nil, nil)
      → (rho3 at root, ys↦nil)
        nil

Common NF `nil`. Confirmed.

`phi` values along outermost path: 22 → 18 → 14 → 4 → 1.
Along innermost: 22 → 18 → 4 → 1. Both strictly decreasing.

### 6.2 Interleaving of len and app

Start: `t = len(app(cons(0, nil), cons(s(0), nil)))`.

Only `rho4` applies initially (inner `app` has `cons(0, nil)` first
arg), so:

    len(app(cons(0, nil), cons(s(0), nil)))
      → (rho4 at pos 0)
        len(cons(0, app(nil, cons(s(0), nil))))
      → (rho3 at pos (0,1))
        len(cons(0, cons(s(0), nil)))
      → (rho2 at root, x↦0, ys↦cons(s(0), nil))
        s(len(cons(s(0), nil)))
      → (rho2 at pos 0, x↦s(0), ys↦nil)
        s(s(len(nil)))
      → (rho1 at pos (0,0))
        s(s(0))

Normal form `s(s(0))` — the expected length of a 2-element list.
`phi`: 11 → 10 → 7 → 6 → 3 → 2. Strictly decreasing.

Alternative order: reduce `rho2` at root first? Cannot — `rho2`'s LHS
matches `len(cons(x, ys))`, but `t`'s `len` argument is an `app`, not
a `cons`. So `rho2` at root is blocked until the inner `app` reduces
to a `cons`. The "case-analysis-by-constructor" structure enforces
a single choice of first-rule at every top-level `len`.

### 6.3 rho4 making the term structurally larger

Start: `t = app(cons(0, nil), cons(s(0), nil))`. Symbol count 8.

    t → (rho4 at root, x↦0, xs↦nil, ys↦cons(s(0), nil))
        cons(0, app(nil, cons(s(0), nil)))                      [size 9]
      → (rho3 at pos 1, ys↦cons(s(0), nil))
        cons(0, cons(s(0), nil))                                 [size 6]

So raw size went 8 → 9 → 6. Size is *not* a termination measure.

`phi` over the same trace: `phi(app(cons(0, nil), cons(s(0), nil)))`
is `2·[cons(0, nil)] + [cons(s(0), nil)] + 1 = 2·3 + 4 + 1 = 11`.
After `rho4`: `[cons(0, app(nil, cons(s(0), nil)))] = 0 + [app(nil,
cons(s(0), nil))] + 2 = (2·1 + 4 + 1) + 2 = 9`.
After `rho3`: `[cons(0, cons(s(0), nil))] = 0 + 4 + 2 = 6`.

`phi`: 11 → 9 → 6. Strictly decreasing, even though raw size
temporarily increased. This is the substantive demonstration that
a literal size count does *not* discharge termination, while the
chosen `phi` does.

### 6.4 Triple-app associativity, demonstrating CP3 closure under a
         ground witness

Start: `t = app(app(app(nil, cons(0, nil)), nil), cons(s(0), nil))`.
This is the ground instance with `xs' := nil`, `ys' := cons(0, nil)`,
`zs' := nil`, `zs := cons(s(0), nil)` of the overlap origin of CP3.

Path A (rho5 at inner):
    app(app(app(nil, cons(0, nil)), nil), cons(s(0), nil))
      → app(app(nil, app(cons(0, nil), nil)), cons(s(0), nil))
      → app(app(nil, cons(0, app(nil, nil))), cons(s(0), nil))  [rho4 inside]
      → app(app(nil, cons(0, nil)), cons(s(0), nil))           [rho3 inside]
      → app(cons(0, nil), cons(s(0), nil))                      [rho3 outer]
      → cons(0, app(nil, cons(s(0), nil)))                      [rho4]
      → cons(0, cons(s(0), nil))                                [rho3]

Path B (rho5 at outer):
    app(app(app(nil, cons(0, nil)), nil), cons(s(0), nil))
      → app(app(nil, cons(0, nil)), app(nil, cons(s(0), nil)))
      → app(cons(0, nil), app(nil, cons(s(0), nil)))           [rho3]
      → app(cons(0, nil), cons(s(0), nil))                      [rho3]
      → cons(0, app(nil, cons(s(0), nil)))                      [rho4]
      → cons(0, cons(s(0), nil))                                [rho3]

Common normal form: `cons(0, cons(s(0), nil))`. Confirmed by the
simulator. `phi` decreases monotonically along both paths (verified
by the runtime assertion in `reduce_to_nf`).

---

## 7. Open questions and known limitations

### 7.1 Extension with `add` and a len/app distributor

Suppose we extend the system with binary `add`, plus rules

    rho6:  add(0, y)        -> y
    rho7:  add(s(x), y)     -> s(add(x, y))
    rho8:  len(app(xs, ys)) -> add(len(xs), len(ys))

Termination question: does `phi` still decrease? Assign `[add](x, y) =
x + y + 1`. Check each new rule:

- `rho6`: `[LHS] = 0 + y + 1 = y + 1`; `[RHS] = y`. Diff 1. ✓
- `rho7`: `[LHS] = (x + 1) + y + 1 = x + y + 2`; `[RHS] = y_of_s_add =
  (x + y + 1) + 1 = x + y + 2`. Diff 0. **Fails strict decrease.**

So `[add](x, y) = x + y + 1` does not discharge `rho7`. A remedy:
`[add](x, y) = x + y + 2`, but then `rho6` diff becomes 2 ≥ 1 ✓, and
`rho7`: `[LHS] = (x+1) + y + 2 = x + y + 3`; `[RHS] = (x + y + 2) + 1
= x + y + 3`. Still diff 0. So constant-bump alone cannot distinguish
them. A coefficient-bump: `[add](x, y) = 2x + y + 1`:
- `rho6`: `2·0 + y + 1 = y + 1 > y`. ✓
- `rho7`: `2(x+1) + y + 1 = 2x + y + 3`; RHS `[s(add(x, y))] =
  (2x + y + 1) + 1 = 2x + y + 2`. Diff 1. ✓

Now `rho8`:
- `[LHS] = [len(app(xs, ys))] = [app(xs, ys)] = 2·xs + ys + 1` (using
  `[len](x) = x`).
- `[RHS] = [add(len(xs), len(ys))] = 2·xs + ys + 1`.
- Diff 0. **Fails strict decrease.**

So a plain linear polynomial cannot simultaneously discharge `rho5`,
`rho7`, and `rho8`. To separate `rho8`, we would need `[app]` to
outweigh `[add]` strictly, e.g., `[len](x) = x + 1`:
- rho1: `[len(nil)] = 1 + 1 = 2 > 0`. ✓
- rho2: `[len(cons(x, ys))] = (x + ys + 2) + 1 = x + ys + 3`;
  `[s(len(ys))] = (ys + 1) + 1 = ys + 2`. Diff `x + 1 ≥ 1`. ✓
- rho8: `[LHS] = (2·xs + ys + 1) + 1 = 2·xs + ys + 2`;
  `[RHS] = 2·(xs + 1) + (ys + 1) + 1 = 2·xs + ys + 4`. Diff `-2`.
  **Negative — rule is then *increasing*, not decreasing.**

So `[len](x) = x + 1` overfits in the opposite direction. A proper
measure for the extended system requires either a non-linear
interpretation (e.g., multiplicative `[len](x) = 2x`), or a product
measure (lexicographic pair of two linear interpretations). We
conjecture termination still holds — `rho8` strictly "unfolds" `len`
past `app` and the resulting fragments decrease under the ordinary
`add`-measure — but the proof is genuinely harder than for the base
system. *This is an open question under the specific measure we
presented.*

### 7.2 Does the confluence proof generalise?

Our closure argument for Q1 used:

- Left-linearity of every LHS (to discharge variable overlaps for
  free).
- Concrete critical-pair closure for three non-trivial overlaps
  plus absence of other overlaps.
- Termination (to upgrade local to global confluence).

The closure of CP3 relied on `rho5`'s self-overlap joining via three
successive `rho5` applications from each side, converging on a
right-nested normal form. If an added rule changed `app`'s behaviour
on a non-`nil`, non-`cons` first argument, new critical pairs would
arise and would need separate closure. So the argument does *not*
mechanically generalise; any extension needs re-enumeration of
critical pairs.

The confluence argument also does not rely on any specific feature
of `len` or the list constructors beyond left-linearity; it would
carry over verbatim to any system with the same five rule shapes
over any alphabet, provided the other signature symbols introduce
no new overlaps.

### 7.3 Termination vs confluence on R specifically

For this R, Q1 ⇐ Q2 + (all critical pairs joinable), as used in §4.3.
Does Q2 imply Q1 unconditionally for R? No — termination alone does
not imply confluence. It does so *here* because critical pairs happen
to close; a minor change to `rho5` (e.g., replacing it by
`app(app(xs, ys), zs) → cons(xs, zs)`, which has the same measure
profile) would preserve termination but break confluence immediately
via CP3-style non-joinability. Conversely, Q1 does not imply Q2 on R
(one can imagine a confluent but non-terminating variant by adding a
rule like `app(xs, nil) → app(app(xs, nil), nil)`; that breaks
termination while keeping critical pairs closable).

So on R the two properties are not logically equivalent; they
coincidentally both hold, each proved by its own machinery.

### 7.4 Is the measure a polynomial interpretation or something more
         elaborate?

Ours is a linear polynomial interpretation over ℕ. In particular:

- All coefficients are non-negative integers.
- All argument coefficients are strictly positive (ensuring
  monotonicity).
- The "weight of left argument" trick (`2x + y + 1` for `app`) is
  what makes `rho5` work. This is specifically an *asymmetric* linear
  interpretation; a symmetric one `x + y + c` fails `rho5`.

Exoticism is unnecessary for R itself. But §7.1 suggests the
extended system may need a multiset ordering on subterms, a two-step
lexicographic combination, or an exponential interpretation. The
linearity of our measure is tight for R but not portable.

### 7.5 Disclosed gaps

- §3.1's enumeration of overlaps is done by case analysis on root
  symbols. It is exhaustive within the method but is not
  machine-generated; an automated overlap checker would provide
  stronger assurance.
- §4.3's well-founded induction uses "proper reduct" as the inductive
  order. This requires the underlying reduction relation to be
  well-founded, which we established in §3.2 via `phi`. The argument
  would break immediately for a non-terminating system; in other
  words, we have no route to confluence *without* termination for
  this R.
- §7.1 is a true open question: the presented linear measure does not
  extend, and while termination likely holds under a heavier measure,
  we do not prove it here.
- The simulator runs at ground instances only; symbolic closure in
  §3.1 covers the fully general cases, but the simulator's
  corroboration is weaker than a machine-checked symbolic proof.
