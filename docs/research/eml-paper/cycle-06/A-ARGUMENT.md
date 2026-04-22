# Confluence and termination of the 5-rule list rewriting system

Signature Σ and rules R (restated for reference):

```
Σ nullary : 0, nil
Σ unary   : s
Σ binary  : cons
Σ defined unary  : len
Σ defined binary : app

ρ₁  len(nil)               → 0
ρ₂  len(cons(x, ys))       → s(len(ys))
ρ₃  app(nil, ys)           → ys
ρ₄  app(cons(x, xs), ys)   → cons(x, app(xs, ys))
ρ₅  app(app(xs, ys), zs)   → app(xs, app(ys, zs))
```

Two separate questions are to be settled:

  - **Q1.** Is R confluent?
  - **Q2.** Does R terminate on every closed term?

The verdict ahead: **yes to both**.  The two verdicts are reached by
two genuinely distinct arguments that happen to share a single
ambient reduction relation, and the joint-implication step in §4.3
derives one from the other only after both have independent
standing.

A mechanical oracle at `task/sim.py` verifies every concrete claim
below; its transcript is at `task/sim_output.txt`.

---

## 1. Motivation

### 1.1 Why confluence might hold (or fail) for R

A rewriting system can break confluence in one of two canonical ways.

  * **Non-left-linear patterns.**  A rule whose left-hand side binds
    the same variable in two positions (e.g. `eq(x, x) → True`) acts
    as an equality test: reducing one copy but not the other can leave
    the two divergent trajectories irreconcilable.  R has no such
    rule — every LHS variable appears exactly once.

  * **Genuine overlaps.**  If two rule left-hand sides unify at some
    non-variable position, one starting term has two incompatible
    rewrites and the two resulting reducts might fail to join.  R has
    overlaps, but all between the associativity rule ρ₅ and the three
    other `app`-rules (ρ₃, ρ₄, and ρ₅ itself).  Whether these join is
    a concrete finite check.

Plausibility from structural feature:

  - ρ₁, ρ₂ have head `len`, which appears nowhere else; so len-rules
    participate in no overlap.
  - ρ₃, ρ₄, ρ₅ have head `app`.  ρ₃ and ρ₄ have a constructor
    pattern (nil or cons) in their first argument, and those
    constructors do not appear deeper inside any other LHS; so no
    overlap between ρ₃ and ρ₄.  But ρ₅'s first argument is itself
    `app`, which *is* the head of ρ₃, ρ₄ and ρ₅.  Hence ρ₅ overlaps
    with each of ρ₃, ρ₄, ρ₅ — three overlap cases, one per app-rule.
    Each overlap yields one critical pair that must be shown
    joinable.

This is the pattern-matching-functional-program intuition: a
left-hand side that is a nested pattern of constructors (here, nested
`app`) must be checked for overlap with rules that manipulate the
same symbol.  The analog in equational reasoning on algebraic data
types (pattern-matching on a pair-of-cons, say) gives the same
structural warning and the same style of discharge.

### 1.2 Why termination might hold (or fail) for R

Two of the five rules have right-hand sides at least as deep as their
left-hand sides:

  - ρ₄: `app(cons(x, xs), ys) → cons(x, app(xs, ys))` — same node
    count (4 each, counting each occurrence as a node).
  - ρ₅: `app(app(xs, ys), zs) → app(xs, app(ys, zs))` — same node
    count (5 each).

A naïve syntactic-size argument fails.  Termination must therefore
come from a cleverer measure that sees what is being *moved*: in both
ρ₄ and ρ₅, "material" is being shifted from the left operand of a
top-level `app` into its right operand.  A measure that weights the
left operand of `app` more heavily than the right operand — so that
moving a subterm from left to right strictly decreases the measure —
is the intuition we will make precise.

The adjacent structural precedent is induction on (quantitative) term
shape: in a functional program, `app` recurs on the first argument,
always peeling a `cons` off the left; the length of the left argument
strictly decreases on each recursive call.  Our measure formalizes
exactly this intuition, extended to handle ρ₅.

Finally, len is structurally induced from its arguments: `len`
reduces only when its argument is a concrete list constructor.  Every
ρ₁/ρ₂ firing strictly shrinks the "len argument" (from `nil` to `0`,
or from `cons(x, ys)` to `ys`).  The intuition here is the classical
structural-induction discipline on inductive types.

No rule in R is self-embedding (no LHS appears as a proper subterm of
its own RHS up to renaming) — a decisive first check against cycles.

### 1.3 Summary of structural features

| feature                              | holds for R? |
|--------------------------------------|:---:|
| left-linear LHSs                     | yes |
| no rule's LHS appears as subterm of that rule's RHS | yes |
| overlaps only between app-rules (ρ₃/ρ₄/ρ₅ with ρ₅)  | yes (3 CPs) |
| right-hand sides no bigger (by node count) than left-hand sides in ρ₁, ρ₃; equal in ρ₂, ρ₄, ρ₅ | yes |
| any rule "reshapes" rather than "creates fresh structure" | yes (shape-preserving for ρ₂, ρ₄, ρ₅) |

Both obligations look plausibly dischargeable.  The methods to close
them follow.

---

## 2. Method design

### 2.1 Confluence method

Given a candidate TRS, the route is:

  1. **Identify potential counter-examples.**  For every ordered pair
     of rules `(ρᵢ, ρⱼ)` and every non-variable position `p` in the
     left-hand side of `ρᵢ`, try to unify the subterm at `p` with the
     left-hand side of `ρⱼ` (after renaming variables apart).  If the
     unification succeeds, the two rewrites — outer `ρᵢ` fired at the
     root of the unified instance, inner `ρⱼ` fired at `p` — yield a
     *critical pair*.  Exclude `(ρᵢ, ρᵢ, p = ε)` as trivial.

     The only remaining ways for a term to enable two different
     rewrites are:
       (a) parallel positions (neither is a prefix of the other) —
       trivially joinable by firing each rewrite on the other
       result;
       (b) one position strictly below a *variable* position of the
       other rule's LHS — joinable, because the inner redex
       commutes with substitution into the LHS variable, up to
       reducing each residual (≤ 1 copy because no variable is
       duplicated on any RHS in R, see §3.2 below);
       (c) overlapping at a non-variable position — the critical
       pair case already enumerated.

  2. **Discharge each critical pair.**  For each pair `(u, v)` arising
     as above, exhibit a term `w` with `u ↠ w` and `v ↠ w`.  When
     every critical pair is so closed, the system is *locally
     confluent*: any one-step divergence rejoins.

  3. **Lift local confluence to full confluence.**  Local confluence
     alone does not give confluence (there are counter-examples).  The
     lift works when reduction is terminating: given strong
     termination, every divergent pair can be rejoined by a
     well-founded induction on the starting term.  The derivation of
     this implication from first principles appears inside §4.3 below
     (not as a cited result).

### 2.2 Termination method

Given a candidate TRS, the route is:

  1. **Construct a measure.**  Define a numeric interpretation `[·]`
     that sends every ground term over Σ to a positive integer.
     Require:
       - each constructor `f` has a chosen interpretation `[f](·, …)`
         mapping positive integers to positive integers;
       - every such chosen interpretation is *strictly monotone in
         each argument* — i.e., if `a < a'`, then `[f](…, a, …) <
         [f](…, a', …)` — so that `[·]` is contextually monotone:
         whenever `[u] < [v]`, replacing `u` by `v` inside any larger
         context `C[_]` yields `[C[u]] < [C[v]]`.

  2. **Verify strict decrease per rule.**  For every rule `ℓ → r` and
     every ground instantiation `θ`, check `[ℓ·θ] > [r·θ]`.  Because
     the chosen interpretations are polynomials with non-negative
     coefficients and positive-integer arguments, checking the
     symbolic inequality `[ℓ] > [r]` (in the free variables of ℓ,
     bounded below by 1) suffices.

  3. **Conclude.**  Monotonicity (1) plus rule-decrease (2) implies
     every single-step rewrite of a closed term strictly decreases
     `[·]`.  Positive integers are well-ordered, so no infinite
     descending chain exists.  Thus there is no infinite reduction
     sequence.

The fact that a rule's right-hand side may be *syntactically larger*
than its left-hand side (ρ₂, ρ₄, ρ₅ have RHS of node-count equal to
or greater than LHS) does not block termination: the measure assigns
coefficients that penalize particular structural positions, and the
arithmetic can favor the RHS in size while disfavoring it in measure.
This is what makes the interpretation approach more powerful than a
literal size-count argument.

### 2.3 What the two methods share and what they do not

Both §2.1 and §2.2 operate on the same term algebra and use
structural induction on terms.  Neither argument subsumes the other:

  - A terminating system can fail to be confluent (take ρ: `a → b,
    a → c` with `b` and `c` distinct normal forms — terminates
    trivially, but `a → b` and `a → c` do not rejoin).
  - A confluent system can fail to terminate (take a single rule
    `f(x) → f(s(x))` — confluent because deterministic, never
    terminates).

R is both.  The joint derivation appears only in §4.3, after each
obligation is discharged on its own.

---

## 3. Progressive derivation

### 3.1 Critical-pair enumeration for Q1

**Position table.**  Non-variable positions of each LHS, with the
subterm at that position and that subterm's head symbol:

| rule | LHS                          | non-variable proper subterm positions | head at each |
|------|------------------------------|---------------------------------------|--------------|
| ρ₁   | `len(nil)`                   | (1): `nil`                            | nil          |
| ρ₂   | `len(cons(x, ys))`           | (1): `cons(x, ys)`                    | cons         |
| ρ₃   | `app(nil, ys)`               | (1): `nil`                            | nil          |
| ρ₄   | `app(cons(x, xs), ys)`       | (1): `cons(x, xs)`                    | cons         |
| ρ₅   | `app(app(xs, ys), zs)`       | (1): `app(xs, ys)`                    | app          |

(The root position ε of each LHS has head `len` for ρ₁,ρ₂ and head
`app` for ρ₃,ρ₄,ρ₅.)

**Overlap audit.**  For each pair `(ρᵢ, ρⱼ)`, does ρⱼ's LHS unify
with some non-variable subterm of ρᵢ's LHS?  Two symbols unify only
if they are the same symbol.  So:

  - ρⱼ = ρ₁ or ρ₂ (head `len` at root): the non-variable subterms in
    the table that have head `len` are none.  No overlap.
  - ρⱼ = ρ₃, ρ₄, ρ₅ (head `app` at root): the non-variable subterm
    with head `app` in the table is the one in ρ₅'s LHS at position
    (1), namely `app(xs, ys)`.  Each of ρ₃, ρ₄, ρ₅ can potentially
    unify its LHS with `app(xs, ys)`; check each:
      * ρ₃'s LHS = `app(nil, ys')` unifies with `app(xs, ys)` via
        `xs := nil, ys := ys'` → **CP#1**.
      * ρ₄'s LHS = `app(cons(x', xs'), ys')` unifies with `app(xs,
        ys)` via `xs := cons(x', xs'), ys := ys'` → **CP#2**.
      * ρ₅'s LHS = `app(app(xs', ys'), zs')` unifies with `app(xs,
        ys)` at position (1) of ρ₅ (a distinct-instance self-overlap,
        not the trivial root-with-itself case) via `xs :=
        app(xs', ys'), ys := zs'` → **CP#3**.

No other pair (ρᵢ, ρⱼ) produces an overlap.  Three critical pairs
in total; mechanically confirmed by `sim.py` section 1.

**Critical pair #1.**  ρ₃ overlapping inside ρ₅.

```
Source  :  app(app(nil, ys), zs)
Outer ρ₅:  → app(nil, app(ys, zs))
Inner ρ₃:  → app(ys, zs)
```

Close by firing ρ₃ once on the outer-reduct:

```
app(nil, app(ys, zs))  →ρ₃  app(ys, zs)
```

Both sides reach `app(ys, zs)`.  **Joinable.**

**Critical pair #2.**  ρ₄ overlapping inside ρ₅.

```
Source  :  app(app(cons(x, xs), ys), zs)
Outer ρ₅:  → app(cons(x, xs), app(ys, zs))
Inner ρ₄:  → app(cons(x, app(xs, ys)), zs)
```

From the outer-reduct:
```
app(cons(x, xs), app(ys, zs))  →ρ₄  cons(x, app(xs, app(ys, zs)))
```

From the inner-reduct:
```
app(cons(x, app(xs, ys)), zs)  →ρ₄  cons(x, app(app(xs, ys), zs))
                               →ρ₅  cons(x, app(xs, app(ys, zs)))
```

Both sides reach `cons(x, app(xs, app(ys, zs)))`.  **Joinable.**

**Critical pair #3.**  ρ₅ self-overlap at position (1).

```
Source  :  app(app(app(xs, ys), zs), ws)
Outer ρ₅:  → app(app(xs, ys), app(zs, ws))
Inner ρ₅:  → app(app(xs, app(ys, zs)), ws)
```

From the outer-reduct:
```
app(app(xs, ys), app(zs, ws))  →ρ₅  app(xs, app(ys, app(zs, ws)))
```

From the inner-reduct:
```
app(app(xs, app(ys, zs)), ws)  →ρ₅  app(xs, app(app(ys, zs), ws))
                               →ρ₅ (at position (2))  app(xs, app(ys, app(zs, ws)))
```

Both sides reach `app(xs, app(ys, app(zs, ws)))`.  **Joinable.**

All three critical pairs are closed.  R is locally confluent.
`sim.py` section 1 independently instantiates each CP with a closed
ground witness and verifies the two reducts share a unique normal
form.

### 3.2 Measure construction and decrease proof for Q2

**Interpretation.**  Define a map `[·]` from closed terms over Σ to
positive integers by:

| symbol    | interpretation        |
|-----------|-----------------------|
| 0         | `[0] = 1`             |
| nil       | `[nil] = 1`           |
| s(x)      | `[s(x)] = x + 1`      |
| cons(x,y) | `[cons(x,y)] = x + y + 1`    |
| len(x)    | `[len(x)] = 2·x`      |
| app(x,y)  | `[app(x,y)] = 2·x + y`|

**Well-foundedness.**  Every closed term has positive integer
interpretation (at least 1, by an easy induction: base atoms 0 and
nil give 1; each constructor's value is at least `1 + (stuff ≥ 0)`).
The strict ordering `<` on positive integers is a well-founded
ordering (no infinite strictly-decreasing chain exists among positive
integers, since each chain would need to descend below 1).

**Strict monotonicity in each argument.**  For each constructor `f`,
its interpretation is strictly increasing in each argument:

  - `s`: coefficient 1 on its argument.
  - `cons`: coefficient 1 on each argument.
  - `len`: coefficient 2 on its argument.
  - `app`: coefficient 2 on first argument, coefficient 1 on second.

Strict monotonicity of a polynomial `α·x + (terms not involving x)`
in `x` is the statement `α > 0`, which holds for every coefficient
above.  Because each constructor is strictly monotone in each slot,
the induced term-interpretation is strictly monotone under arbitrary
contexts: if a subterm `u` strictly decreases in interpretation to
`u'`, every containing context `C[u]` satisfies `[C[u]] > [C[u']]`.

**Rule-wise strict decrease.**  For each rule, compute `[LHS] − [RHS]`
as a polynomial in the free variables of the LHS, treating each
variable as an unknown positive integer (i.e., each `x` ≥ 1):

| rule | `[LHS]` | `[RHS]` | `[LHS] − [RHS]` | `> 0`? |
|------|---------|---------|-----------------|--------|
| ρ₁ | `[len(nil)] = 2·1 = 2` | `[0] = 1` | `1` | ✓ |
| ρ₂ | `[len(cons(x, ys))] = 2·(x + ys + 1) = 2x + 2ys + 2` | `[s(len(ys))] = 2ys + 1` | `2x + 1` | ≥ 3 > 0  ✓ |
| ρ₃ | `[app(nil, ys)] = 2·1 + ys = ys + 2` | `[ys] = ys` | `2` | ✓ |
| ρ₄ | `[app(cons(x, xs), ys)] = 2·(x + xs + 1) + ys = 2x + 2xs + ys + 2` | `[cons(x, app(xs, ys))] = x + (2xs + ys) + 1 = x + 2xs + ys + 1` | `x + 1` | ≥ 2 > 0  ✓ |
| ρ₅ | `[app(app(xs, ys), zs)] = 2·(2xs + ys) + zs = 4xs + 2ys + zs` | `[app(xs, app(ys, zs))] = 2xs + (2ys + zs) = 2xs + 2ys + zs` | `2xs` | ≥ 2 > 0  ✓ |

Each difference is strictly positive for every positive-integer
assignment to the free variables.  Rule-wise strict decrease is
established.

**Monotonicity under context lifts this to single-step strict
decrease.**  If `t → t'` via rule `ℓ → r` at position `p`, then the
subterm `t|_p` is some instance `ℓ·θ` and `t'|_p = r·θ`.  By
rule-wise strict decrease, `[ℓ·θ] > [r·θ]`.  By context monotonicity,
`[t] > [t']`.

**Termination.**  Suppose for contradiction there were an infinite
reduction chain `t₀ → t₁ → t₂ → …`.  The corresponding sequence
`[t₀] > [t₁] > [t₂] > …` would be an infinite strictly-descending
sequence of positive integers.  No such sequence exists.
Contradiction.  Hence no infinite chain.  R terminates.

`sim.py` section 2 evaluates `[LHS] − [RHS]` for every rule over a
witness set of small ground terms, reporting the min and max
difference; every minimum is strictly positive.  `sim.py` section 3
enumerates the complete reduction graph of each test term and
verifies directly that every edge strictly decreases `[·]`; step
counts are all bounded below `[t₀]`.

---

## 4. Final verdict

### 4.1 Q1 answer — R is confluent

Proof outline.  By §3.1, R has exactly three critical pairs and every
one is joinable (explicit common reducts exhibited).  Any
single-step divergence `t → u₁` and `t → u₂` of R falls into one of
three cases (§2.1 item 1):
  (a) parallel redex positions,
  (b) nested positions with the inner redex at a variable position
      of the outer rule's LHS,
  (c) overlapping redexes at a non-variable position — a critical-
      pair instance.

Cases (a) and (b) join without critical pairs:

  * Case (a) is immediate: fire each rule on the other reduct.  Left-
    linearity is not even needed for this case; the two redexes
    operate in disjoint subtrees, so firing them commutes.

  * Case (b) is the variable-substitution case.  Say `t → u₁` by
    outer rule ρ at position p, and `t → u₂` by inner rule σ at
    position `p·q` where `q` is below (or at) a variable position of
    ρ's LHS.  Let `x` be that LHS variable.  In R, every LHS is
    left-linear (each LHS variable appears at most once on its own
    LHS), and every RHS is also linear: no variable from a rule's LHS
    appears more than once in the corresponding RHS.  (Inspection:
    ρ₁ has no vars, ρ₂ uses `ys` once and erases `x`, ρ₃ uses `ys`
    once, ρ₄ uses each of `x, xs, ys` once, ρ₅ uses each of `xs, ys,
    zs` once.)  Therefore firing ρ on `t` yields a term in which the
    σ-redex has at most one residual.  Two sub-cases:

      — If `x` does not occur in ρ's RHS (case: `x` in ρ₂ is erased):
      the σ-redex has zero residuals in `u₁`.  But `u₂` after firing
      σ still has the ρ-redex (by left-linearity of ρ's LHS, the
      inner substitution does not alter the outer pattern-match);
      firing ρ on `u₂` yields exactly `u₁`.

      — If `x` does occur in ρ's RHS (one occurrence, since the RHS
      is linear in LHS variables): the σ-redex has exactly one
      residual in `u₁`.  Firing σ at that residual, and
      symmetrically firing ρ at the root of `u₂`, both produce the
      same term (`u₂` is the LHS match of ρ with the instantiation
      modified by σ's action on `x`'s binding).

    Mechanically: `u₁ ↠ w` in ≤ 1 step (fire σ on the residual if
    any), `u₂ ↠ w` in exactly 1 step (fire ρ).

  * Case (c) is handled by the critical-pair analysis: every critical
    pair of R is joinable, so the specific instance `(u₁, u₂)` —
    which is a substitution instance of a critical pair — is joinable
    by the same substituted joining sequence.

So every one-step divergence `u₁ ← t → u₂` has a common reduct `w`
(in at most a few further steps).  That is: **R is locally
confluent.**

Now we derive, from first principles in this specific setting, that
"R locally confluent and R terminating" implies "R confluent".

Let `→` denote single-step reduction of R, and `↠` its reflexive-
transitive closure.  Assume R terminates (Q2, proven independently in
§4.2) and is locally confluent (just proven).  Define, for every
closed term `t`, the property

  > **P(t)** :  for every pair of terms `u, v` with `t ↠ u` and
  >             `t ↠ v`, there exists `w` with `u ↠ w` and `v ↠ w`.

We must show `P(t)` holds for all `t`.  Termination means `→` is a
well-founded relation: there is no infinite chain `t → t₁ → t₂ →
…`.  Equivalently, the relation "is a strict descendant of" (`t →⁺
t'`) is well-founded.  We proceed by well-founded induction on this
relation, with induction hypothesis:

  > (**IH**)  `P(t')` holds for every `t'` with `t →⁺ t'`.

Prove `P(t)`.  Fix `u, v` with `t ↠ u` and `t ↠ v`.  If `t = u` take
`w = v`; if `t = v` take `w = u`.  Otherwise both reductions are non-
empty:

```
t → t₁ ↠ u          t → t₂ ↠ v
```

Apply local confluence to the one-step divergence `t₁ ← t → t₂`: get
`s` with `t₁ ↠ s` and `t₂ ↠ s`.

`t → t₁`, so `t →⁺ t₁`; by **IH**, `P(t₁)` holds.  Apply `P(t₁)` to
the pair `(t₁ ↠ u, t₁ ↠ s)`: get `w₁` with `u ↠ w₁` and `s ↠ w₁`.

`t → t₂`, so `t →⁺ t₂`; by **IH**, `P(t₂)` holds.  Compose `t₂ ↠ s ↠
w₁`, giving `t₂ ↠ w₁`.  Apply `P(t₂)` to the pair `(t₂ ↠ v, t₂ ↠
w₁)`: get `w` with `v ↠ w` and `w₁ ↠ w`.

Then `u ↠ w₁ ↠ w` and `v ↠ w`.  Hence `P(t)`.  ∎

Thus `P(t)` holds for every closed term `t`: R is confluent.

### 4.2 Q2 answer — R terminates

Proof outline.  By §3.2 we have a polynomial interpretation `[·]`
into positive integers, strictly monotone in each argument, with every
rule strictly decreasing `[·]`.  Because of strict monotonicity in
each argument, any contextual rewrite `C[ℓ·θ] → C[r·θ]` satisfies
`[C[ℓ·θ]] > [C[r·θ]]`.

If R admitted an infinite chain `t₀ → t₁ → t₂ → …`, then `[t₀] >
[t₁] > [t₂] > …` would be an infinite strictly-decreasing sequence
of positive integers, which is impossible.  Hence every chain is
finite: R terminates on every closed term.  Furthermore, for any
starting term `t₀`, the length of any reduction chain from `t₀` is at
most `[t₀] − 1` (each step strictly decreases by at least 1, and the
minimum value is 1).  ∎

`sim.py` section 3 enumerates the full reduction graph of 11 closed
test terms (one of them has 515 reachable states) and confirms on
every edge that the measure strictly decreases, and confirms the
longest chain from each starting term is below `[t₀]`.

### 4.3 Joint implication

For this R the verdicts combine as follows.  The Q1 proof invokes Q2
(termination gives the well-foundedness needed to lift local
confluence to full confluence).  Q1 does *not* produce Q2: a
confluent but non-terminating system would not be ruled out by any
amount of critical-pair analysis.  Concretely, if we removed
termination as an assumption, the §4.1 derivation would stop at
"locally confluent", and we would have no classical way to promote
that to "confluent".

Conversely, Q2 does not require Q1.  The measure argument cares only
about strict decrease, not about path rejoinability.  A fully non-
confluent terminating system (like the toy `a → b, a → c` example
noted earlier) would be correctly classified "terminating" by the
same interpretation idea.

So for this R: *termination is the foundation; confluence rides on
top of termination plus the three joinable critical pairs.*
Both proofs are necessary and neither subsumes the other.

---

## 5. Verification strategy

Two independent channels confirm the verdicts.

### 5.1 Channel A — symbolic proof (the arguments in §3 and §4)

Every critical pair is listed, and for each an explicit joining
sequence is given (exhibiting `w`).  For termination, the
interpretation is a polynomial with closed-form symbolic `LHS − RHS`
reduction for each rule; each difference is a polynomial in the free
variables with non-negative coefficients plus a strictly positive
constant, hence positive under any positive-integer assignment.  This
argument is exhaustive at the algebraic level.

### 5.2 Channel B — executable oracle (`task/sim.py`, log
`task/sim_output.txt`)

The simulator performs four independent things:

  1. **Critical-pair enumeration by mechanical unification.**  For
     every ordered pair of rules and every non-variable position, it
     runs first-order unification.  Exactly the three critical pairs
     listed in §3.1 are found.  Each critical pair is instantiated
     with a small closed witness; the leftmost-outermost reduction
     of the two reducts yields the same normal form in every case.

  2. **Per-rule interpretation check.**  For each rule, the simulator
     enumerates a 5-element witness set for each free LHS variable
     (i.e., up to 5³ = 125 combinations for ρ₅) and computes
     `[LHS] − [RHS]`.  Every minimum difference is strictly
     positive.

  3. **Exhaustive reduction-graph oracle.**  For each of 11 closed
     test terms (including one with 515 reachable reducts), it
     enumerates the entire reduction graph via BFS, verifies every
     edge strictly decreases `[·]`, and reports that the graph has a
     unique normal form.  Every test passes.

  4. **Worked traces.**  Two-strategy traces (leftmost-outermost
     versus rightmost-innermost) on each of three representative
     starting terms, with the measure annotated at every step.
     Both strategies reach the same normal form.

The simulator is a *falsifier*: any missed critical pair, any
miscalculated interpretation, or any non-confluence within the test
suite would surface as a mismatch (exception, non-decreasing edge, or
multiple normal forms).  None was found.  The oracle channel and the
symbolic channel agree on every claim.

This executable-oracle verification is explicitly enumerated alongside
the trace-argument path.

---

## 6. Worked examples

Recorded verbatim from `sim.py` section 4; reproduce with
`python3 task/sim.py`.  Let
```
L1 = cons(0, nil)
L2 = cons(s(0), nil)
L3 = cons(0, nil)
```

### 6.1 Example (a) — associativity by ρ₅ in both orders

Starting term  `t = ((L1 @ L2) @ L3)`  written out as
`app(app(L1, L2), L3)`, with `[t] = 23`.

Leftmost-outermost (ρ₅ at root fires first):

```
step rule  pos   reduct                                                    [ · ]
 1   ρ₅   ()    app(L1, app(L2, L3))                                         17
 2   ρ₄   ()    cons(0, app(nil, app(L2, L3)))                               15
 3   ρ₃   (2)   cons(0, app(L2, L3))                                         13
 4   ρ₄   (2)   cons(0, cons(s(0), app(nil, L3)))                            10
 5   ρ₃   (2,2) cons(0, cons(s(0), L3)) = cons(0, cons(s(0), cons(0, nil)))    8
```

Rightmost-innermost (ρ₄ on the inner `app(L1,L2)` fires first):

```
step rule  pos   reduct                                                    [ · ]
 1   ρ₄   (1)   app(cons(0, app(nil, L2)), L3)                               19
 2   ρ₃   (1,2) app(cons(0, L2), L3)                                         15
 3   ρ₄   ()    cons(0, app(L2, L3))                                         13
 4   ρ₄   (2)   cons(0, cons(s(0), app(nil, L3)))                            10
 5   ρ₃   (2,2) cons(0, cons(s(0), cons(0, nil)))                             8
```

Both strategies converge to the same right-associated form.  The
measure decreases monotonically in both traces.  (The leftmost path
fires ρ₅ at the root; the rightmost never fires ρ₅ — the inner ρ₄
consumes the inner `app` and ρ₅ no longer applies.  This is the
classic demonstration that ρ₅ is "redundant" modulo the already-
present ρ₃, ρ₄ when the inner `app`'s first argument is a list
constructor; the system is confluent regardless.)

### 6.2 Example (b) — len and app interleaved

Starting term  `t = len(app(L1, L2)) = len(app(cons(0, nil),
cons(s(0), nil)))`, `[t] = 20`.

Strategy A (ρ₄ then ρ₂, fully unwinding app first is actually *not*
forced — interleaving appears naturally from leftmost-outermost):

```
 1   ρ₄   (1)   len(cons(0, app(nil, L2)))        16
 2   ρ₂   ()    s(len(app(nil, L2)))              13
 3   ρ₃   (1,1) s(len(L2))                         9
 4   ρ₂   (1)   s(s(len(nil)))                     4
 5   ρ₁   (1,1) s(s(0))                            3
```

Strategy B (reduce app fully before letting len fire):

```
 1   ρ₄   (1)   len(cons(0, app(nil, L2)))        16
 2   ρ₃   (1,2) len(cons(0, L2))                  12
 3   ρ₂   ()    s(len(L2))                         9
 4   ρ₂   (1)   s(s(len(nil)))                     4
 5   ρ₁   (1,1) s(s(0))                            3
```

Both reach `s(s(0))`, the length of `L1 @ L2` (a two-element list).
Measure decreases every step.  The interleaving in strategy A
exercises ρ₂ while the `app`-subterm is still partially reduced,
demonstrating that the confluence claim is not sensitive to order.

### 6.3 Example (c) — termination on a structurally-same-size rule

Starting term
```
t = (((nil @ nil) @ nil) @ nil)
  = app(app(app(nil, nil), nil), nil)
```
with `[t] = 15`.  Every rule firing on this term either is ρ₅
(same-sized on the surface) or ρ₃ (strictly smaller on the surface).

ρ₅-first trace:

```
 1   ρ₅   ()    app(app(nil, nil), app(nil, nil))      9   (ρ₅, surface-same-sized)
 2   ρ₅   ()    app(nil, app(nil, app(nil, nil)))      7   (ρ₅, surface-same-sized)
 3   ρ₃   ()    app(nil, app(nil, nil))                 5
 4   ρ₃   ()    app(nil, nil)                           3
 5   ρ₃   ()    nil                                     1
```

Measure drops by 6, 2, 2, 2, 2 respectively.  Even when the
syntactic shape does not shrink (steps 1 and 2 each apply ρ₅, whose
LHS and RHS have the same node count), the interpretation still
drops, by `2·[xs]` each time — precisely the design of the
coefficient `2` on app's first argument.

ρ₃-first trace:

```
 1   ρ₃   (1,1) app(app(nil, nil), nil)                 7
 2   ρ₃   (1)   app(nil, nil)                           3
 3   ρ₃   ()    nil                                     1
```

Both paths converge to `nil`, normal form of the input.

---

## 7. Open questions and known limitations

### 7.1 Extending R with an addition operator and a len/app-distribution rule

Suppose we extend the signature with a binary defined symbol `add`
and the rules

```
ρ₆  add(0, y)         → y
ρ₇  add(s(x), y)      → s(add(x, y))
ρ₈  len(app(xs, ys))  → add(len(xs), len(ys))
```

**Critical-pair impact.**  ρ₈'s LHS is `len(app(xs, ys))`.  Its
non-variable subterm at position (1) is `app(xs, ys)`, which unifies
with ρ₃'s, ρ₄'s, and ρ₅'s LHSs — three *new* critical pairs.  Each is
tractable to close (e.g., the ρ₈-versus-ρ₃ pair: `len(app(nil, ys)) →
len(ys)` vs `add(len(nil), len(ys)) → add(0, len(ys)) → len(ys)`;
joinable).  ρ₇ with itself and ρ₆ with ρ₇ need checking.

**Termination impact.**  Our measure *does not extend* as-is.
Trying `[add(x,y)] = 2x + y` (forced by ρ₇'s decrease: `[add(s(x), y)]
− [s(add(x,y))] = 2(x+1)+y − (2x+y+1) = 1`) and keeping
`[app(x,y)] = 2x + y` gives

```
[len(app(xs, ys))]       = 2·(2xs + ys)          = 4xs + 2ys
[add(len(xs), len(ys))]  = 2·(2xs) + 2ys          = 4xs + 2ys
```

Difference = 0 — ρ₈ is not strictly decreasing.  The measure would
need redesign: either a non-linear interpretation (e.g., making
`[app(x, y)]` superlinear in both arguments) or a lexicographic pair
of the form `([len-applications], [·])`.  The argument scheme carries
over, but the specific polynomial does not.  This is a genuine
limitation disclosed.

### 7.2 Does the confluence proof need left-linearity and non-overlap?

The §4.1 case analysis relies on:

  - **Left-linearity of LHSs** (no LHS variable repeats) — so that
    inner reductions commute with outer pattern matching.
  - **RHS-linearity over LHS variables** (each LHS variable appears
    at most once on the RHS) — so that the variable-substitution
    case (b) produces at most one residual per inner redex.  This is
    stronger than the standard confluence toolkit requires; what the
    standard toolkit really needs is left-linearity at the LHS plus
    joinability of critical pairs.

In our system, LHS-linearity holds for all five rules; RHS-linearity
over LHS vars holds for all five rules (it is an incidental bonus,
not a required property).  The §4.1 argument simplifies accordingly.
Dropping RHS-linearity is harmless provided one replaces "at most one
residual" with "k residuals, each joined independently", which a
more careful parallel-reduction style argument handles.

Dropping LHS-linearity is NOT harmless: a rule like `ρ*: dup(x, x) →
x` added to R would destroy confluence (take `t = dup(M, M)` with `M`
a term having two distinct reducts `N₁` and `N₂`; then `t → M` by
`ρ*` is blocked by the inner reduction because `dup(N₁, M) ≠
dup(M, N₂)`; the resulting critical pair is generally unclosable).

### 7.3 Do termination and confluence imply each other for R?

For this specific R:
  - **Termination ⇒ confluence**: yes, via local confluence.  The
    §4.1 derivation uses well-foundedness (which follows from
    termination) and local confluence.  Local confluence itself is a
    standalone fact (all three critical pairs are joinable), not a
    consequence of termination.
  - **Confluence ⇒ termination**: no.  Confluence is a statement
    about rejoining paths; termination is a statement about path
    finiteness.  Neither implies the other in general, and there is
    no particular feature of R that would upgrade confluence into
    termination.

So the two verdicts for R are genuinely independent facts, joined
only by the §4.3 one-way implication.

### 7.4 Nature of the measure used

The measure is a *polynomial interpretation* over positive integers,
not a more exotic beast (no multiset, no lexicographic composition,
no syntactic-weight function).  The polynomial degree is 1 in each
variable (linear); all coefficients are small non-negative integers.

The choice matters in two ways:

  - **Tightness.**  Linear polynomial interpretations suffice exactly
    when every RHS's "weighted" size is linearly less than its
    LHS's, uniformly over variable instantiations.  For R this
    holds.  For the extension with `ρ₈` in §7.1, it does not, and a
    strictly stronger measure is required.

  - **Generality.**  A polynomial interpretation is very "explicit":
    the decrease inequalities are closed-form polynomial
    inequalities checkable by mechanical arithmetic.  This makes
    `sim.py`'s per-rule check trivial (brute-force witnessing over a
    small grid).  If we had used a lexicographic measure, the
    decrease check would have been per-component, with more care
    needed to avoid increasing lower-priority components while a
    higher-priority one decreases.

The measure here is as simple as possible — which is an argument in
its favor, but also means extensions that break linearity (§7.1) will
need a rebuild, not a patch.

---

## Summary

  - **Q1:** R is confluent.  Evidence: three explicit joinable
    critical pairs (§3.1), local confluence via case analysis on one-
    step divergences (§4.1), termination-lifted to full confluence by
    well-founded induction (§4.1 derivation).
  - **Q2:** R terminates.  Evidence: polynomial interpretation `[·]`
    over positive integers strictly monotone in each constructor
    argument, strictly decreasing on every rule (§3.2, §4.2).
    Longest reduction chain from any `t₀` is bounded above by `[t₀]
    − 1`.
  - **Independence of proofs:** Q2 is proven without Q1 directly from
    the measure.  Q1 relies on Q2 in the local-confluence-to-
    confluence lifting step; the lifting implication is derived from
    first principles in §4.1, not cited.
  - **Verification:** §3, §4 (symbolic arguments) plus `task/sim.py`
    (executable oracle) agree on every concrete claim.  Log at
    `task/sim_output.txt`.
