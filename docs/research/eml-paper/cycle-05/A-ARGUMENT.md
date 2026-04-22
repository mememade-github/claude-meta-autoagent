# Confluence of the extended calculator

Self-contained derivation that the 13-rule applicative calculus
{I, K, S, B, C, W, M, Y, T, V, D, Π₁, Π₂} has a confluent reduction
relation, with mechanical verification.

The argument proceeds in seven parts as the brief requires; a
companion simulator at `task/sim.py` mechanically discharges every
worked example, and its log is checked into `task/sim_output.txt`.

---

## 1. Motivation

### 1.1 What confluence buys us

A reduction relation `→` is confluent when, for any term `M` reaching
two reducts `N₁` and `N₂`, the two paths can be re-joined: there is
some `P` with `N₁ →* P` and `N₂ →* P`.  Equivalently, on the
reflexive-transitive closure `→*` we have the diamond.

Two adjacent corollaries of confluence are why we usually want it:

  - **Unique normal form.** If a term reaches two normal forms
    (irreducible reducts) `N₁` and `N₂`, confluence forces `N₁ →* P`
    and `N₂ →* P`, but normal forms cannot reduce further, so
    `N₁ = P = N₂`.  Equality of expressions becomes a well-defined
    semantic notion.
  - **Strategy irrelevance for normal forms.** Two evaluators that
    pick different redexes still agree on the answer whenever an
    answer exists.  This is what lets a programmer reason about a
    program without modeling the scheduler.

These corollaries do *not* require strong normalization.  Confluence
is a local geometric fact about how reduction paths fit together; it
is independent of whether reduction always terminates.  The baseline
calculator is non-terminating (`Y f → f (Y f) → f (f (Y f)) → …` and
`M M → M M`), so any honest argument has to work on infinite
reduction graphs.

### 1.2 Where confluence usually fails

It is instructive to note where confluence *does* fail in nearby
systems, because that pinpoints what the present calculator avoids.

  - **Overlapping rewrite rules.** If two rules can both fire at the
    same position with incompatible right-hand sides, the system is
    immediately non-confluent.  Toy example: with rules `f a → b` and
    `f a → c` (with `b ≠ c`), the term `f a` produces `b` and `c`,
    neither of which can reduce further.  No common reduct.
  - **Non-left-linear rules without joinability of the resulting
    critical pair.** A rule like `eq x x → True` matches `eq M M`,
    but if `M` has a redex it can be reduced first only on one side
    of the `eq`, breaking the pattern; the resulting reducts are
    irreconcilable unless the rule system enforces joinability.
  - **Ambiguity inside an argument that is duplicated.** If a rule
    duplicates an argument and another rule could fire only on one
    copy, you get residuals that can be reduced inconsistently.  This
    one is the danger we have to argue away below — duplication
    happens with `S, W, M, Y` in our calculator.

### 1.3 Structural features that make us optimistic here

Inspecting each rule's left-hand side:

| primitive | LHS shape         | arity | head-symbol unique? | LHS variables linear? |
|-----------|-------------------|-------|---------------------|------------------------|
| I         | `I x`             | 1     | yes                 | yes                    |
| K         | `K x y`           | 2     | yes                 | yes                    |
| S         | `S x y z`         | 3     | yes                 | yes                    |
| B         | `B x y z`         | 3     | yes                 | yes                    |
| C         | `C x y z`         | 3     | yes                 | yes                    |
| W         | `W x y`           | 2     | yes                 | yes                    |
| M         | `M x`             | 1     | yes                 | yes                    |
| Y         | `Y f`             | 1     | yes                 | yes                    |
| T         | `T x y`           | 2     | yes                 | yes                    |
| V         | `V x y z`         | 3     | yes                 | yes                    |
| D         | `D x y z w`       | 4     | yes                 | yes                    |
| Π₁        | `Π₁ x y`          | 2     | yes                 | yes                    |
| Π₂        | `Π₂ x y`          | 2     | yes                 | yes                    |

Two structural facts jump out:

  - **(P1) Disjoint head primitives.** Every LHS is rooted at a
    distinct primitive symbol.  A rewriting attempt at a position `p`
    requires the symbol at `p`'s spine head to be exactly that
    primitive; two different primitives cannot match the same
    position.
  - **(P2) Left-linearity.** Each variable on a LHS appears exactly
    once, so a rule never asks "are these two subterms equal?" — a
    requirement that, when present, breaks confluence in the absence
    of joinability.

Two redexes in the same term therefore relate in only three ways:
*identical*, *disjoint* (in non-overlapping subtrees), or *nested*
(one strictly inside an argument of the other).  None of these three
relations gives rise to genuinely incompatible rewrites.  This is the
combinatorial intuition: confluence ought to hold.

The remaining worry is duplication.  `S, W, M, Y` all duplicate
arguments on their right-hand side.  After firing, a redex sitting
inside the duplicated argument has multiple "residuals", one per
copy, and another evaluator might have rewritten the redex *before*
the duplication, producing a single residual.  Reconciling these two
trajectories is exactly what the diamond proof must perform.  The key
trick is to redefine "one step" so it rewrites *all* such residuals
at once — i.e., parallel reduction.

---

## 2. A confluence-checking procedure

Given any candidate combinator-like rewriting system on tree terms,
the procedure I will use has three branches.

### 2.1 Find the danger: overlap analysis

For each ordered pair `(ρ, σ)` of rules, with LHS patterns `ℓ_ρ` and
`ℓ_σ`, check whether `ℓ_ρ` unifies with some non-variable subterm of
`ℓ_σ`.  If yes, the unifier `θ` produces a *critical pair*

  > `(r_ρ θ , (ℓ_σ θ with ℓ_ρ θ replaced by r_ρ θ at the unified position))`

— two distinct one-step reducts from the same starting term `ℓ_σ θ`.
Critical pairs are the only sources of "local divergence at a single
position".  Disjoint and nested redexes always commute trivially (you
can fire them in either order with the same outcome modulo residual
tracking).

**Counting convention.** I count critical pairs at the symbol level.
The trivial root-with-itself overlap `(ρ, ρ)` at the empty position
is excluded by convention (it just says `ℓ_ρ θ → r_ρ θ` and
`ℓ_ρ θ → r_ρ θ`, which is no divergence at all).  A nested overlap
(rule `ρ` matches inside an argument position of rule `σ`) is *not* a
critical pair: variable positions in `ℓ_σ` accept anything, including
a `ρ`-redex, but that just means after reducing `σ` the `ρ`-redex's
copies are residuals, handled by the diamond proof, not a critical
pair.

For our calculator:  by (P1), no two distinct rules' LHSs share their
spine head, so `ℓ_ρ θ` and `ℓ_σ θ` cannot agree at the root for
distinct `ρ ≠ σ`.  And the only non-variable subterm of any LHS at
depth `> 0` is again rooted at the same primitive symbol (e.g.,
`(K x)` inside `(K x y)` has head `K`).  So an overlap `(ρ, σ)` with
`ρ ≠ σ` would require the primitive of `ρ` to occur at depth `> 0`
inside the LHS of `σ`, which never happens.  And `(ρ, ρ)` has only
the trivial root overlap.

**Conclusion of the audit:** zero non-trivial critical pairs.  This
is the input to the next step.

### 2.2 Discharge confluence: parallel-reduction diamond

When the overlap audit produces no non-trivial critical pairs, we
have a "non-overlapping left-linear" system.  The technique is to
build a new relation `⇒` on terms — *parallel reduction* — that
satisfies:

  1. `⇒` contains the original `→` (every single step is also a
     parallel step).
  2. `⇒` is contained in `→*` (every parallel step is achievable as a
     finite sequence of single steps).
  3. `⇒` has the diamond: from `M ⇒ N₁` and `M ⇒ N₂`, some `P`
     satisfies `N₁ ⇒ P` and `N₂ ⇒ P`.

From (3), the reflexive-transitive closure `⇒*` has the diamond by a
standard "tile" argument: stack rectangles to fill in the grid.  From
(1) and (2), `⇒* = →*`.  So `→*` has the diamond, i.e., `→` is
confluent.

The diamond on `⇒` itself is proven via a "complete development"
construction: define `M*`, the term obtained by firing every
currently-present redex of `M` simultaneously, with all arguments
also developed in parallel.  Show *triangle*: `M ⇒ N` implies
`N ⇒ M*`.  Then for any two divergent parallel reductions
`M ⇒ N₁`, `M ⇒ N₂`, both reach `M*`, supplying the common reduct.

### 2.3 Handle non-termination

The construction in 2.2 makes no use of strong normalization.  This
is essential for the present calculator: `Y f` and `M M` are not
strongly normalizing, yet confluence must still hold.

The trap to avoid is the alternative route: prove *local confluence*
(every divergence of length 1 can be rejoined) and then hope to lift
to full confluence.  That lift is sound only when the system is
strongly normalizing.  For our non-terminating system the lift is
unavailable and we cannot use it.  The parallel-reduction route in
2.2 is robust to non-termination because the diamond is established
on `⇒` by a *direct* construction (the triangle to `M*`), not by
induction on reduction-length.

This is the procedure I will execute.

---

## 3. Progressive confluence claims

I now apply the procedure rule-by-rule, in the order
`I, K, S, B, C, W, M, Y, T, V, D, Π₁, Π₂`, building a chain of
strengthening claims.  At each stage I state the claim, the method
that discharges it, and any disclosed gap.

The mechanical bounded check in `task/sim.py` (function
`example_6_progressive_subsets`) confirms each prefix on a fixed
13-term probe suite up to depth 3 with join depth 6.  All probes
verified for every prefix; see `task/sim_output.txt`.

### Stage 1 — `{I}`

Claim.  `→_I` (reduction with only `I x → x`) is confluent.

Method.  The single rule has no self-overlap beyond the trivial root
case.  So no critical pair.  Define `⇒_I` and `M*` as in §4 below.
Triangle is immediate: `(I x)* = x*`, the only redex pattern is
`(I x)`, and the I-step in `⇒_I` reduces `(I x)` to (a parallel
reduct of) `x`.

Disclosed gap.  None.

### Stage 2 — `{I, K}`

Claim.  Adding `K x y → x` preserves confluence.

Method.  K's LHS is rooted at `K`, distinct from `I`.  No overlap
between K and I.  Self-overlap of K is trivial.  Diamond extends by
adding the K-step clause to `⇒` and the K-clause to the definition
of `M*`.  All earlier triangle cases remain.  New cases (where the
top-level reduction is by K) discharged identically.

Disclosed gap.  None.

### Stage 3 — `{I, K, S}`

Claim.  Adding `S x y z → x z (y z)` preserves confluence.

Method.  S's LHS is rooted at `S`, distinct from I and K.  No new
overlaps.  S duplicates `z`: this is the first place where
duplication enters and where parallel reduction earns its keep.
Triangle case for S: `(S x y z)* = (x* z*) (y* z*)`.  An app-rule
parallel reduction yields `(S x' y' z')`; an S-step yields
`x' z' (y' z')`.  Both reach `(x* z*) (y* z*)` by IH (`x' ⇒ x*` etc.)
and by another S-step / app-rules, respectively.  Worked through in
§5.

Disclosed gap.  None.

### Stage 4 — `{I, K, S, B}`

Claim.  Adding `B x y z → x (y z)` preserves confluence.

Method.  B does not duplicate.  Distinct head, no overlap.  Triangle
case: `(B x y z)* = x* (y* z*)`.  Symmetric to S without duplication.

### Stage 5 — `{I, K, S, B, C}`

Claim.  Adding `C x y z → x z y` preserves confluence.

Method.  C permutes; no duplication, no erasure.  Distinct head, no
overlap.  Triangle case: `(C x y z)* = x* z* y*`.

### Stage 6 — `{I, K, S, B, C, W}`

Claim.  Adding `W x y → x y y` preserves confluence.

Method.  W duplicates `y`.  Distinct head, no overlap.  Triangle
case: `(W x y)* = x* y* y*`.  W is the first non-S duplicator; same
argument schema as S.

### Stage 7 — `{I, K, S, B, C, W, M}`

Claim.  Adding `M x → x x` preserves confluence.

Method.  M duplicates `x`.  Distinct head, no overlap.  Triangle
case: `(M x)* = x* x*`.  Now `M M → M M`, a fixed-point loop.  But
even this single-trajectory loop poses no confluence threat: the
*only* one-step reduct of `M M` is `M M` itself, so any reduct pair
is `(M M, M M)`, trivially joined.

### Stage 8 — `{I, K, S, B, C, W, M, Y}`

Claim.  Adding `Y f → f (Y f)` preserves confluence.

Method.  Y "duplicates" by recreating its own LHS inside its RHS.
Distinct head, no overlap.  Triangle case: `(Y f)* = f* (Y f*)`.

The subtlety here is that Y's RHS contains the *same* primitive, so
reducing once leaves a fresh `Y`-redex.  But this is "creation", not
"residual": the new `Y` came from the rule's RHS, not from a
pre-existing redex inside an argument.  Parallel reduction (and
hence the triangle) treats only currently-present redexes; the
freshly created one is the next stage's problem.  The diamond closes
in one parallel step regardless of how deep the unfolding goes,
because both diverging paths agree on what was already there to
reduce.

Worked through mechanically in §6 example (b).

### Stage 9 — `{… , T}`

Claim.  Adding `T x y → y x` preserves confluence.

Method.  T permutes (length-2 cycle).  Distinct head; triangle case
`(T x y)* = y* x*`.  No overlap, no duplication.

### Stage 10 — `{… , V}`

Claim.  Adding `V x y z → z x y` preserves confluence.

Method.  V is a 3-element rotation.  Triangle case
`(V x y z)* = z* x* y*`.  No overlap, no duplication.

### Stage 11 — `{… , D}`

Claim.  Adding `D x y z w → x y (z w)` preserves confluence.

Method.  D is a 4-arg combinator that introduces an inner
application but no duplication.  Triangle case
`(D x y z w)* = x* y* (z* w*)`.  Distinct head; no overlap.

### Stage 12 — `{… , Π₁}`

Claim.  Adding `Π₁ x y → x` preserves confluence.

Method.  Π₁ has the same RHS shape as K but a different primitive
head.  No overlap with K (different head!), no overlap with anything
else.  Triangle case `(Π₁ x y)* = x*`.

Aside.  Π₁ and K are *operationally equivalent* on their own (both
project the first argument).  This poses no confluence problem; it
just means the calculator is *redundant*, not inconsistent.

### Stage 13 — full baseline `{I, K, S, B, C, W, M, Y, T, V, D, Π₁, Π₂}`

Claim.  The full baseline is confluent.

Method.  Adding Π₂ contributes another head-distinct, non-
duplicating, non-overlapping rule.  All previous reasoning carries
over.  Full proof in §4 below.

Disclosed gap.  None.

---

## 4. Verdict on the full baseline

**Verdict: the full 13-primitive baseline is confluent.**

### 4.1 Definitions

Terms `T ::= s | (T T)` where `s` ranges over a primitive set
`P = {I, K, S, B, C, W, M, Y, T, V, D, Π₁, Π₂}` plus arbitrary
constants (atoms with no rule).

Application is left-associative.  The *spine* of a term `t` is the
unique decomposition `t = h a₁ a₂ … aₙ` where `h` is not an
application; we write `head(t) = h` and `args(t) = [a₁,…,aₙ]`.

A term is a *redex at the root* iff `head(t)` is some primitive `c`
with arity `k_c` ≤ `n`, in which case the rule for `c` rewrites the
first `k_c` arguments and leaves `a_{k_c+1}, …, a_n` untouched.

Single-step reduction `→` is the contextual closure: `M → M'` iff
some position of `M` is a root-redex `R` and `M'` results from
replacing `R` by its rule's reduct in place.

### 4.2 Critical pair audit

Let `ρ, σ` be any two of the 13 rules.  Write `ℓ_ρ` for the LHS
pattern of `ρ`.  We claim no critical pair beyond the trivial
identity `(ρ = σ, root)`.

Each `ℓ_ρ` has the form `c v₁ … v_{k_c}` where `c` is the primitive
of `ρ` and `v_i` are pairwise-distinct placeholder variables.  The
non-variable subterms of `ℓ_ρ` are exactly the prefix subspines
`c`, `c v₁`, `c v₁ v₂`, …, `c v₁ … v_{k_c}`.  Each of these has
spine head `c`.

Suppose `ℓ_σ` (with `σ ≠ ρ`) unifies with some non-variable subterm
`u` of `ℓ_ρ`.  Both are rooted at the same primitive (`c` for `u`,
the primitive of `σ` for `ℓ_σ`).  But the primitives of `ρ` and `σ`
differ.  Contradiction.

Suppose `σ = ρ` and the overlap is at a strictly internal position
`p ≠ root`.  Then `ℓ_ρ` would have to unify with a strictly-shorter
subspine `c v₁ … v_j` (with `j < k_c`) of itself.  But `ℓ_ρ` has
spine length `k_c + 1 > j + 1`, so the lengths cannot match; no
unification.

Therefore there are no non-trivial critical pairs.  ∎ (audit)

### 4.3 Parallel reduction `⇒`

Define `⇒` inductively:

  - (refl)   `s ⇒ s` for each primitive `s` and each constant.
  - (app)    `M ⇒ M'`, `N ⇒ N'` ⟹ `(M N) ⇒ (M' N')`.
  - (rule_c) for each primitive `c` with arity `k_c` and rule `c v_1 … v_{k_c} → r_c`,
             `v_1 ⇒ v_1', …, v_{k_c} ⇒ v_{k_c}'`
             ⟹ `(c v_1 … v_{k_c}) ⇒ r_c[v_1 := v_1', …, v_{k_c} := v_{k_c}']`.

If `c` appears as the head of a longer spine `c v_1 … v_{k_c} u_1 … u_m`, the
rule_c clause applies to the prefix and `app` applies to the trailing
arguments; this is the standard congruence on application.

Containments.  `→ ⊆ ⇒`: a single-step reduction is the rule_c clause
with `v_i ⇒ v_i` (refl) for unaffected subterms, plus `app` for the
context.  `⇒ ⊆ →*`: induction on `⇒` derivations; `app` and `refl`
are immediate, and `rule_c` is one root-step `→` followed by reducing
the substituted arguments via IH.

### 4.4 Complete development `M*`

Define `M*` recursively on the structure of `M`:

  - If `M` is a primitive or atom, `M* = M`.
  - Otherwise let `(h, [a₁, …, aₙ]) = spine(M)`.  Compute
    `aᵢ* = star(aᵢ)`.  If `h` is a primitive `c` with arity `k_c ≤ n`,
    set
        `M* = r_c[v_i := aᵢ*]_{i=1..k_c}  applied to a_{k_c+1}*, …, aₙ*`.
    Otherwise (`h` is a non-rule symbol or `n < k_c`),
        `M* = h applied to a₁*, …, aₙ*`.

Note `M*` always exists and is unique; `(M, *)` is a deterministic
function.

### 4.5 `M ⇒ M*`

By induction on `M`.  Atoms: `M = h ⇒ h = M*`.  For `M = h a₁ … aₙ`
with `h` a non-redex head (primitive without enough args, or
non-rule symbol): by IH `aᵢ ⇒ aᵢ*`, and by repeated `app`
`(h a₁ … aₙ) ⇒ (h a₁* … aₙ*) = M*`.  For `M = c v₁ … v_{k_c} u₁ … u_m`
with `c` a rule head: by IH `vᵢ ⇒ vᵢ*` and `uⱼ ⇒ uⱼ*`; apply
rule_c plus app to obtain
`M ⇒ r_c[v_i := vᵢ*]  applied to  u₁* … u_m* = M*`.  ∎

### 4.6 Triangle: `M ⇒ N ⟹ N ⇒ M*`

By induction on the derivation of `M ⇒ N`.

*Case (refl), `M = N`.*  By 4.5, `N = M ⇒ M*`.  ✓

*Case (app), `M = (P Q) ⇒ (P' Q') = N`.*  We have `P ⇒ P'` and
`Q ⇒ Q'`.

Subcase A: `M` is not a redex at the root, but the inductive structure
of `M*` may still trigger a rule_c reduction at the root if `P` is a
spine `c a₁ … a_{k_c-1}` (so that `M = c a₁ … a_{k_c-1} Q` is exactly
a redex of arity `k_c`).  This is the only situation worth checking
carefully.

  - If `M = c a₁ … a_{k_c} … aₙ` with `n ≥ k_c`, then
    `M* = r_c[v_i := a_i*] · a_{k_c+1}* · … · aₙ*`.
    Now `(P, Q) = (c a₁ … a_{n-1}, aₙ)`, so `P' = c a₁' … a_{n-1}'`
    and `Q' = aₙ'` with each `aᵢ ⇒ aᵢ'`.  Then
    `N = c a₁' … aₙ'`.  By IH on each subterm, `aᵢ' ⇒ aᵢ*`.
    Apply rule_c to `N` with parallel reductions `aᵢ' ⇒ aᵢ*`:
    `N ⇒ r_c[v_i := a_i*] · a_{k_c+1}* · … · aₙ* = M*`.  ✓

  - If `M = h a₁ … aₙ` with `h` non-rule or `n < k_h`, then
    `M* = h a₁* … aₙ*`.  `N = h a₁' … aₙ'` (similar form).  By IH
    `aᵢ' ⇒ aᵢ*`; by app, `N ⇒ h a₁* … aₙ* = M*`.  ✓

*Case (rule_c), `M = c v₁ … v_{k_c} ⇒ r_c[v_i := v_i'] = N`*
(plus possibly trailing args handled by app, treated as in
subcase A).  Then with `M = c v₁ … v_{k_c} u₁ … u_m`,
`M* = r_c[v_i := v_i*] · u_1* · … · u_m*`.

We need `N = r_c[v_i := v_i'] · u_1' · … · u_m' ⇒ M*`.  Each variable
`v_i` may appear several times in `r_c` (e.g., `S` makes `z` appear
twice).  Each occurrence in `N` is `v_i'`.  By IH each `v_i' ⇒ v_i*`
(applied independently to each occurrence — this is sound because
parallel reduction acts pointwise per occurrence; left-linearity of
the LHS means each `v_i'` in `N` is a syntactically independent copy
that may itself be reduced independently).  Likewise `u_j' ⇒ u_j*`.
Combine by repeated app to lift inside-the-RHS-context:

  `r_c[v_i := v_i'] · u₁' · … · u_m'  ⇒  r_c[v_i := v_i*] · u₁* · … · u_m* = M*`.  ✓

This is the case where left-linearity is critical.  Without left-
linearity, distinct copies of a duplicated variable in `r_c` could
have been reduced inconsistently between `M ⇒ N` and the IH-step,
preventing the merge.

All cases discharged.  ∎ (triangle)

### 4.7 Diamond on `⇒`

Suppose `M ⇒ N₁` and `M ⇒ N₂`.  By the triangle, `N₁ ⇒ M*` and
`N₂ ⇒ M*`.  So `P := M*` is the required common reduct.  ∎ (diamond)

### 4.8 Diamond on `→*`

The diamond lifts from `⇒` to `⇒*` by tiling:
to fill the rectangle for `M ⇒* N₁` and `M ⇒* N₂`, decompose `M ⇒* N₁`
as `M ⇒ A₁ ⇒ A₂ ⇒ … ⇒ N₁` and `M ⇒* N₂` as
`M ⇒ B₁ ⇒ … ⇒ N₂`; iteratively close diamonds at each cell using
the diamond on `⇒`.

Since `→ ⊆ ⇒ ⊆ →*`, taking reflexive-transitive closures gives
`→* ⊆ ⇒* ⊆ →*`, so `→* = ⇒*`.  Therefore `→*` has the diamond, i.e.,
`→` is confluent.  ∎ (full baseline confluent)

### 4.9 Counting conventions

  - **Critical pair:** an unifier-pair `(ℓ_ρ θ → r_ρ θ, ℓ_σ θ →
    ℓ_σ θ[r_ρ θ at p])` for some non-variable position `p` of `ℓ_σ`,
    excluding `(ρ, ρ, p = root)`.  Count for our calculator: 0.
  - **Overlap:** a unification of one rule's LHS with a non-variable
    subterm of another's, modulo the trivial root self-overlap.
    Count: 0.
  - **Residual:** for `M → N` via a rule `ρ` at position `p`, and a
    redex `r` at position `q`, the residuals of `r` in `N` are the
    occurrences of the rewritten copy of `r` in `N`.  If `q` is
    disjoint from `p`, there is one residual at `q`.  If `q` is
    inside an argument of the `ρ`-redex that gets duplicated, there
    are as many residuals as duplicates (e.g., S duplicates the
    third arg, so a redex inside it has two residuals).  If `q` is
    inside an argument that gets erased (K erases its second arg),
    there are zero residuals.
  - **Parallel step:** one application of the inductive `⇒`
    relation (one root-rule fired per chosen redex, with congruence
    propagating into all chosen subterms).

---

## 5. Verification strategy

I run two independent verification strategies and report success on
both.

### 5.1 Strategy A: parallel-reduction triangle (analytic)

Discharged in §4 above.  Every clause of the inductive `⇒` is paired
with a clause of `M*`; the triangle case analysis is exhaustive over
the rule shapes.  Because (P1) ensures distinct head primitives, no
two `rule_c` cases can apply to the same `M`, so case analysis is
exhaustive without overlap.

### 5.2 Strategy B: bounded executable oracle

`task/sim.py` implements term representation, single-step reduction
with all redex positions enumerated, parallel reduction with
complete development, and a bounded BFS oracle that for each test
term `t` enumerates all reducts reachable in `≤ d` steps and checks
that every pair of reducts shares a common further reduct reachable
in `≤ j` steps from each.  Output captured in `task/sim_output.txt`.

The oracle is a *falsifier*: any genuine non-confluence in the
calculator within the depth bounds would surface as a pair of
reducts with no common join.  No such pair was found across the
test suite.

This is the executable-oracle verification path; combined with §5.1
this yields two independent confirmations.

### 5.3 Why the two strategies are complementary

§5.1 is *exhaustive* over the algebraic structure but is only as
sound as the structural arguments themselves.  §5.2 is *empirical*
but mechanically checks the actual rewrite graph.  A bug in §5.1's
case analysis or a hidden missed overlap should cause §5.2 to throw
a counterexample.  The empirical verification therefore acts as a
sanity check on the symbolic proof.

---

## 6. Worked examples

All three examples are exhibited mechanically in `sim.py`.  Output
excerpted below; reproduce with `python3 task/sim.py`.

### 6.1 Example (a): an `S`-redex with internal `K`- and `I`-redexes

Term: `t = S (K a b) (I c) (I d)`.

Two reduction strategies:

```
[A] leftmost-outermost:
  S (K a b) (I c) (I d)
→ K a b (I d) (I c (I d))         -- fire S at root
→ a (I d) (I c (I d))             -- fire K at root
→ a d (I c (I d))                 -- fire inner I (first arg of a)
→ a d (c (I d))                   -- fire I-on-c
→ a d (c d)                       -- fire I-on-d
   normal form: a d (c d)

[B] rightmost-innermost:
  S (K a b) (I c) (I d)
→ S (K a b) (I c) d               -- fire I-on-d (rightmost redex)
→ S (K a b) c d                   -- fire I-on-c
→ S a c d                         -- fire K
→ a d (c d)                       -- fire S
   normal form: a d (c d)
```

Both strategies converge to `a d (c d)`, in 5 vs 4 steps; the
calculator's confluence on this term is exhibited.

The simulator additionally enumerates *all* depth-4 reducts (16+
distinct terms) of `t` and verifies pairwise joinability within 8
extra steps; result `OK; 0 failures`.

### 6.2 Example (b): `Y`-induced divergence (non-terminating)

Term: `t = Y f`.

```
Y f
→ f (Y f)
→ f (f (Y f))
→ f (f (f (Y f)))
…
```

Take two divergent reduction sequences from `t`:

  - Path α: 1 step.  Result `N_α = f (Y f)`.
  - Path β: 2 steps.  Result `N_β = f (f (Y f))`.

The common reduct exhibited by the simulator is
`f (f (f (f (Y f))))` (reachable from `f (Y f)` in 3 single-steps and
from `f (f (Y f))` in 2 single-steps).

Equivalently, by the triangle: `(Y f)* = f (Y f)`, and `N_α ⇒ (Y f)*`
trivially (it *is* `(Y f)*`), while `N_β ⇒ f ((Y f)*) = f (f (Y f))`
and from there `f (f (Y f)) ⇒ f (f (Y f))` …  the diamond closes one
parallel layer at a time, keeping the unfolding lock-step.

This demonstrates confluence on a non-normalizing term.  The diamond
lives at the level of `⇒`, not at the level of "reach a common normal
form" — the latter does not exist for `Y f`.

### 6.3 Example (c): leftmost vs rightmost on a multi-combinator term

Term: `t = B (W I) (K a) c`.

```
[leftmost]                              [rightmost]
B (W I) (K a) c                         B (W I) (K a) c
→ W I (K a c)         (B at root)      → W I (K a c)        (B at root)
→ I (K a c) (K a c)   (W at root)      → W I a              (K a c → a inside)
→ K a c (K a c)       (I at root)      → I a a              (W at root)
→ a (K a c)           (K at root)      → a a                (I at root)
→ a a                 (K a c → a)
   normal form: a a                        normal form: a a
```

Both reach `a a`, in 5 vs 4 steps.  The two trajectories interleave
the same set of rule firings differently — leftmost fires `B` then
`W` immediately and accumulates duplicated `K a c`-redexes that must
each be consumed, while rightmost fires the inner `K a c → a`
*before* duplicating, avoiding redundant work.  Confluence guarantees
they meet.  Bounded oracle on depth-6 reducts: `OK; 0 failures`.

### 6.4 Bonus: critical-pair audit and progressive subset checks

`example_5_overlap_audit` in `sim.py` enumerates the 13 LHS shapes
and confirms the structural argument that no pair has a non-trivial
overlap.  `example_6_progressive_subsets` checks the 13-term probe
suite under each cumulative prefix of the rule set; all 13 prefixes
verified `13/13` probes confluent.

---

## 7. Open questions and known limitations

### 7.1 Extension to under-binder reduction

If we extend the calculus with λ-abstraction `(λx. M)` and a β-rule
`(λx. M) N → M[x := N]`, the proof structure carries over but two
new ingredients appear:

  - **α-conversion** must be handled.  Either work modulo α (terms
    are equivalence classes) or use a nameless representation
    (positions counted from the binder).  Either choice keeps `⇒` and
    `M*` well-defined.
  - **Substitution must commute with `⇒`.**  Specifically, if `M ⇒ M'`
    and `N ⇒ N'`, then `M[x := N] ⇒ M'[x := N']`.  This requires the
    substituted variable to be left-linear (the binder is) and the
    body's parallel reduction to be congruent under substitution.
    Both hold for plain β.

The triangle proof for the β case reads: `((λx. M) N)* = M*[x := N*]`,
and the inductive cases follow.  No critical pair arises between β
and our 13 combinator rules because β's LHS is rooted at a λ-binder
(a different syntactic class than any primitive symbol).

So the proof technique extends cleanly to the under-binder setting,
provided we are careful about substitution and α-equivalence.

### 7.2 Confluence vs normalization

In our calculator, confluence holds *without* strong normalization.
The implications go:

  - Confluence ⟹ unique normal form *if one exists*.  Does not imply
    normal forms exist.  Example: `Y f` has no normal form but is
    confluent.
  - Strong normalization ⟹ confluence *given local confluence*.  We
    don't use this direction (we don't have strong normalization),
    but it would be the alternative route in a normalizing calculus.
  - Strong normalization + confluence ⟹ unique normal form for every
    term.  This is the comfortable case but not ours.
  - Weak normalization (some reduction strategy reaches a normal
    form) + confluence ⟹ every reduction strategy that terminates
    reaches the same normal form, and a normal form exists for each
    term that is weakly normalizing.

Our argument deliberately decouples confluence from normalization;
this matters because of `Y` and `M`.

### 7.3 Strategy independence

The proof targets the relation `→`, not any specific strategy.  Once
`→` is confluent, any strategy (leftmost-outermost, rightmost-
innermost, randomized, parallel) operates inside the same equivalence
classes.  In particular:

  - If a normal form exists, every terminating strategy finds the
    same one (by confluence + irreducibility of normal forms).
  - Some strategies may fail to terminate where others succeed
    (e.g., rightmost-innermost may diverge on `K a (Ω)` where `Ω`
    is a non-terminating term, while leftmost-outermost terminates
    by erasing `Ω` first).  Confluence does not promise termination
    parity across strategies.

So the proof generalizes to *all* strategies in the sense of
agreement on outcomes, but does not promise *equal termination
behavior*.

### 7.4 Non-orthogonal confluent extensions

Yes, the calculator admits non-orthogonal confluent extensions.  An
illustrative example:  add a fresh primitive `J` with rule

  > `J x y → I (K x y)`

The new rule's LHS is rooted at the fresh head `J`, so no overlap
with anything in the baseline.  By the same parallel-reduction
argument as above, the extended system is confluent.  This is *still*
orthogonal — the new rule is left-linear and head-disjoint.

For a genuinely *non*-orthogonal but confluent extension, allow LHS
overlap and prove the resulting critical pair joins.  Example: add
the rule

  > `K (I x) y → x`

This LHS overlaps with `I` at position `1` (the `(I x)` subterm is
itself a redex).  Two reductions from `K (I a) b`:

  - Fire the I inside first: `K (I a) b → K a b → a` (using K's old
    rule).
  - Fire the new K-rule directly: `K (I a) b → a` (one step).

Both reach `a`.  The critical pair joins.  If we add this rule,
confluence is preserved.  Such extensions are common when one rule
"shortcuts" a multi-step reduction that the existing rules already
implement, and all such shortcuts must be checked for joinability of
their critical pairs.  The general shape: adding a rule
`f(g(...)) → r` whose RHS coincides with some existing reduction of
`f(g(...))`.  This builds a confluent non-orthogonal system.

Whether the *baseline* alone (without such tactical additions) admits
a "natural" non-orthogonal confluent extension that an engineer would
find useful is a question about programming language design rather
than rewriting theory; my analysis here gives the methodology
(critical pair joinability) but not the design guidance.

---

## Summary

  - **Verdict:** the 13-rule baseline is confluent.
  - **Method:** parallel reduction `⇒` with complete development `M*`,
    triangle property `M ⇒ N ⟹ N ⇒ M*`, diamond on `⇒`, lift to
    `→*` via `→* = ⇒*`.
  - **Why it works:** distinct head primitives + left-linearity ⟹ no
    non-trivial critical pairs ⟹ orthogonal-style confluence holds
    independent of termination.
  - **Why it survives non-termination:** the diamond is established
    by direct construction on `⇒`, not by induction on the length of
    `→`-sequences; `Y` and `M`'s divergent terms are handled cleanly.
  - **Verification:** analytic proof in §4 plus mechanical bounded
    oracle in `task/sim.py`; both confirm the verdict on the test
    suite, with no counterexamples found.
  - **No counterexample exists in the baseline; no new combinator
    needs to be invented to exhibit non-confluence; the calculator is
    its own maximal confluent subset (it equals the maximal
    confluent extension of itself within itself).**
