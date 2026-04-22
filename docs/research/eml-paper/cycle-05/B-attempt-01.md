# Confluence of the Extended Calculator — Attempt 01

**Task.** Decide whether the 13-rule applicative reduction relation is
confluent. Produce a self-contained first-principles argument.

**Counting conventions (declared up front).**

- A **term** is either a primitive symbol (one of
  `I, K, S, B, C, W, M, Y, T, V, D, Π₁, Π₂`) or an application `(M N)`
  where `M, N` are terms. Lower-case letters denote metavariables over
  arbitrary terms (not part of the object syntax). Application is
  left-associative in display only: `M N O` means `((M N) O)`.
- An **occurrence** (or **position**) in a term is a path in the
  application tree — a finite string over `{L, R}` (go into the left
  or right child). The empty path `ε` is the root.
- A **redex** is a subterm whose head primitive has been applied to at
  least its arity-many arguments; equivalently, a subterm at some
  position whose structural shape matches one of the thirteen left-
  hand-side patterns. We write `red(M)` for the set of redex
  positions in `M`.
- A single-step rewrite `M → N` contracts **one** redex: pick `p ∈
  red(M)`, rewrite the subterm at `p` using the rule determined by
  its head primitive, and replace it in `M`. The many-step relation
  `↠` is the reflexive-transitive closure of `→`.
- **Overlap** between rules `R₁` (LHS `ℓ₁`) and `R₂` (LHS `ℓ₂`) at a
  non-variable position `q` of `ℓ₁`: the subterm `ℓ₁|q` is unifiable
  (syntactically, no binders present) with a renaming of `ℓ₂`. A
  **critical pair** is the pair of terms obtained from the most
  general unifier of such an overlap by applying each rule.
- A **parallel step** `M ⇒ N` will be defined inductively in §2; it
  contracts a (possibly empty) set of redex occurrences of `M`
  *that were already present in `M` before any of them was fired*.
- A **residual** of a redex `r` across a parallel step that does not
  contract `r` is the redex occurrence at the corresponding
  position(s) in the result.

Throughout, I use `≡` for syntactic identity of terms and `=` for
provable equality or equality of substituted instances — never for
reducibility.

---

## §1. Motivation — where confluence is likely to hold

### 1.1 Where confluence comes from in term-rewriting systems

A rewrite relation is confluent iff diverging reductions can always be
re-joined at a common reduct. Informally, the question is: does the
order in which I fire redexes matter for the ultimate outcome? For
many computational models, the answer is "yes, order matters" (think
of effectful imperative programs, or rewrite systems whose rules can
contradict each other). For others, the answer is "no" — and the
reasons for that "no" are well-understood structural reasons:

(a) **Non-interference.** If no two redexes can "fight" for the same
piece of syntax, firing them in any order leaves the same
reachable set. Two redexes fight when their left-hand sides would
contract overlapping portions of the term. In a system where
different rules have structurally distinguishable left-hand sides
and no rule's left-hand side contains, as a sub-pattern, the left-
hand side of any rule, the redexes are structurally separable —
they act on disjoint regions or nested regions, never on
overlapping ones. I will formalize this below as an **overlap-free**
property.

(b) **Variable rigidity.** Even if two redexes are separable in the
source term, firing one can duplicate the other (as `S x y z → x z
(y z)` duplicates `z`, `W x y → x y y` duplicates `y`, and `M x →
x x` duplicates `x`). This is fine as long as: (i) the duplicated
arguments are unaffected by the contraction at the outer site
(which is the case here because contraction replaces the LHS
pattern with an RHS built out of the *same argument terms*, never
inspecting them); and (ii) after duplication, each copy can still
reduce independently, and the resulting reductions can be lifted
to a joint parallel step in a well-behaved manner. Condition (i)
is the usual characterization of "left-linearity" (each variable
in the LHS pattern appears at most once), and condition (ii) is
captured by the standard parallel-reduction construction that
contracts "a set of non-overlapping redex occurrences
simultaneously" (defined formally in §2.2).

(c) **No hidden feedback through termination.** Some confluence
arguments for terminating rewrite systems boil down to "local
confluence + strong normalization implies confluence". That
strategy is unavailable here: `Y f → f (Y f)` and `M (M a) → …` give
immediate non-termination. So the confluence witness must be robust
to infinite reduction paths. The standard way to get that is to
exhibit the **diamond property** (or a weak form of it) directly on
a parallel-reduction relation, without going through normalization.

This motivation predicts: **a system whose LHSs are left-linear, are
distinguishable by the primitive at their head, and pattern-match
only on argument positions (not on internal structure of the
arguments) should be confluent, whether or not it is terminating.**

I now verify that the extended calculator meets exactly these
structural conditions, and use that to build a confluence proof.

### 1.2 Precedents (first-principles) from adjacent domains

Three adjacent domains provide intuition, each reasoned about from
first principles below (no external reference is invoked):

**(P1) Deterministic computation.** For computations on a model where
each configuration has at most one applicable step, confluence is
trivially equivalent to determinism of the step relation. Our
system is non-deterministic at the step level (several redexes may
be present simultaneously), so confluence here is a statement about
the *shape* of the induced lattice of reducts, not about
determinism of step choice. Still, the principle "if all choices
lead somewhere re-joinable, the choice is semantically irrelevant"
is precisely what confluence formalizes.

**(P2) Disjoint-union of deterministic rules.** If we view each of our
13 rules in isolation, each is deterministic: given a redex of
that form, its contraction produces a single, uniquely determined
result. Moreover, the 13 rules act on structurally disjoint
patterns (different head primitives). So each rule is locally
confluent *by itself*; what needs to be shown is that the rules
**compose without introducing new critical pairs**. This is the
classic critical-pair programme, transposed to combinator rewriting.

**(P3) Uniqueness of result in evaluated expressions.** In many
functional evaluation models, an expression's value does not depend
on evaluation order provided the model has no side effects and
functions are pure. The extended calculator is closer to this: each
primitive behaves as a pure, total function on its arguments, with
the argument terms treated as opaque black boxes during contraction
(no inspection of their structure). This opacity is what guarantees
that the duplication performed by `S, W, M, D` does not break
confluence: duplicated arguments are independent of each other and
can be reduced (or not) in any order.

Taken together: the structural recipe of this calculator — primitive-
headed, left-linear, non-inspecting — is exactly the recipe under
which confluence is expected. I now *prove* it.

---

## §2. A systematic confluence-checking procedure

I design the procedure in three phases, justified by the motivation
in §1.

### 2.1 Phase A — Identify potential counter-examples

Given a candidate rewrite system, enumerate potential failure modes.
In our setting:

**A1. Rule-vs-rule overlap at a non-root position.** For each ordered
pair of rules `(R₁, R₂)` with LHSs `ℓ₁, ℓ₂`, and each non-variable
position `q` in `ℓ₁` (including root), ask: is `ℓ₁|q` unifiable with
a renaming of `ℓ₂`? If yes, the overlap induces a critical pair
that must be checked for joinability.

**A2. Rule-vs-itself overlap at a non-root position.** Same as A1 but
`R₁ = R₂` and `q ≠ ε` (the root-with-itself case is vacuous).

**A3. Left-linearity.** Verify each variable in each LHS appears at
most once. If violated, the pattern-matching rule for duplicate
occurrences of `x` imposes an extra equational constraint on the
substitution, and the rewrite system becomes non-orthogonal in a
different way (often still confluent, but via a different argument).

**A4. Non-left-linearity on the right.** If a variable `x` appears
multiple times on some RHS (as with `S`, `W`, `M`, `D`), the
parallel-reduction argument must be set up to handle duplicated
residuals coherently. (This is merely a design constraint on the
argument, not a confluence obstruction.)

### 2.2 Phase B — Discharge confluence when no counter-example is found

I define a **parallel-reduction** relation `⇒` and show it has the
diamond property. The construction is the standard one in this type
of analysis; I build it from scratch without naming.

**Definition (parallel reduction, inductive).** `M ⇒ N` iff derivable
from:

- (P-refl)  `a ⇒ a` for any primitive or free variable `a`.
- (P-app)   if `M ⇒ M'` and `N ⇒ N'`, then `(M N) ⇒ (M' N')`.
- (P-rule) for each rule `ℓ[x̄] → r[x̄]` in the system and any
  terms `Tᵢ, T'ᵢ` with `Tᵢ ⇒ T'ᵢ` (one for each metavariable
  `xᵢ` in `ℓ`), if the substituted LHS is `ℓ[x̄ := T̄]` and the
  substituted RHS is `r[x̄ := T̄']`, then
  `ℓ[x̄ := T̄]  ⇒  r[x̄ := T̄']`.

Informally: `M ⇒ N` contracts a set of redex occurrences *present in
M* simultaneously, while allowing the arguments of contracted redexes
to be themselves parallel-reduced (possibly contracting redexes
inside them too).

**Property B1.** `→ ⊆ ⇒`. Any single rewrite step is a parallel step:
use (P-rule) on the contracted redex (with `Tᵢ ⇒ Tᵢ` by reflexivity
and (P-app)) and (P-refl)/(P-app) for the surrounding context.

**Property B2.** `⇒ ⊆ ↠`. Any parallel step decomposes into a finite
sequence of ordinary rewrite steps: fire the contracted redexes one
at a time in any disjoint order, then perform the nested parallel
reductions in the argument terms. Since the argument reductions do
not interfere (they live at strictly nested positions) and there are
finitely many, this is a finite `↠` sequence. (A formal induction on
the derivation of `M ⇒ N` makes this precise; see §2.4.)

**Property B3.** `⇒* = ↠*`. From B1 and B2 plus the reflexive-
transitive closure monotonicity.

**Property B4 (diamond on `⇒`).** If `M ⇒ N₁` and `M ⇒ N₂`, there
exists `P` with `N₁ ⇒ P` and `N₂ ⇒ P`.

Proof of B4 uses the **complete development** construction: given
`M`, define `Φ(M)` = the term obtained from `M` by contracting,
simultaneously, *every* redex occurrence of `M` (and recursively in
each argument). This is well-defined because (by the overlap-free
check of Phase A) the redexes of `M` are either disjoint or strictly
nested, and the contraction of a redex does not inspect its arguments
— it only rearranges them. Then one shows by induction on `M ⇒ N`:

> **Triangle Lemma.** If `M ⇒ N`, then `N ⇒ Φ(M)`.

(Detailed case analysis in §2.4.) From the Triangle Lemma, the
diamond B4 follows immediately: if `M ⇒ N₁` and `M ⇒ N₂`, take
`P = Φ(M)`.

**Property B5 (diamond lifts to `↠`).** Using B3, confluence of `↠`
follows from B4 by a finite tiling argument: given
`M  ↠  N₁  ≡  M ⇒ M₁ ⇒ … ⇒ Mₖ = N₁` and
`M  ↠  N₂  ≡  M ⇒ M'₁ ⇒ … ⇒ M'ₗ = N₂`,
tile a `k × l` grid of parallel-reduction diamonds to reach a common
corner `P`. Since each tile closure exists by B4, and the grid is
finite, `P` exists, with `N₁ ⇒* P` and `N₂ ⇒* P`, hence
`N₁ ↠ P` and `N₂ ↠ P` by B3.

### 2.3 Phase C — Handling the non-terminating case

The argument in Phase B never uses termination. Parallel reduction is
defined irrespective of whether reductions terminate, and the
Triangle Lemma does not require normal forms. Hence the confluence
conclusion holds even when `↠` is infinitary on some terms (`Y f`,
`M M`, etc.).

The alternative "local confluence + strong normalization ⇒
confluence" strategy is explicitly **not** used, because the
baseline fails strong normalization. (That strategy is also strictly
weaker: it would require local-confluence to be shown, which here is
a sub-case of B4 anyway.)

### 2.4 Detailed case analysis for the Triangle Lemma

I prove the Triangle Lemma by induction on the derivation of `M ⇒
N`.

**Case P-refl.** `M ≡ N ≡ a` a primitive or free variable. Then
`red(M) = ∅`, so `Φ(M) = M`. `N ⇒ Φ(M)` is `a ⇒ a`, by P-refl. ✓

**Case P-app.** `M ≡ (M₁ M₂)`, `N ≡ (N₁ N₂)` with `Mᵢ ⇒ Nᵢ`. Two
sub-cases:

- **C1. `M` itself is not a redex.** Then `red(M)` = (redexes lifted
  from `M₁`) ∪ (redexes lifted from `M₂`). So `Φ(M) = (Φ(M₁)
  Φ(M₂))`. By IH, `Nᵢ ⇒ Φ(Mᵢ)`. By P-app, `(N₁ N₂) ⇒ (Φ(M₁)
  Φ(M₂)) ≡ Φ(M)`. ✓

- **C2. `M` is a redex at root** (applied to some head primitive `h`
  with enough arguments). Then `M ≡ h T₁ … Tₐ W₁ … Wₖ` where `a =
  arity(h)` and the `Wⱼ` are "extra" arguments beyond the root
  redex pattern. Since P-app was the outermost constructor of the
  derivation `M ⇒ N`, the root redex was **not** contracted in this
  step; it must have been decomposed into the (P-app) case all the
  way down. Its head primitive `h` parallel-reduces to itself (by
  P-refl), each `Tᵢ ⇒ T'ᵢ`, and the `Wⱼ` parallel-reduce to some
  `W'ⱼ`. So `N ≡ h T'₁ … T'ₐ W'₁ … W'ₖ`. Now `Φ(M)` fires the root
  redex **and** recurses into the arguments: `Φ(M) ≡ (Φ(r[x̄ :=
  T̄]))` with the `W̄` appended and Φ-reduced — concretely, `Φ(M)
  = Φ(r[x̄ := T̄] W₁ … Wₖ)`.
  **But wait:** parallel reduction allows us to fire the root redex
  from `N` in one parallel step. Namely, `N ⇒ r[x̄ := Φ(T̄)] Φ(W̄)`
  using (P-rule) for the root with sub-derivations `T'ᵢ ⇒ Φ(T'ᵢ)
  ⇒ Φ(Tᵢ)` (by IH) plus (P-app) chaining. Since `Φ(Tᵢ) = Φ(T'ᵢ)`
  whenever `T'ᵢ ⇒ Φ(Tᵢ)` and `Φ` is idempotent on the reachable
  set, we get `N ⇒ Φ(M)`. ✓
  (Sub-case C2 is the case that could in principle fail for a
  rewrite system with critical pairs — it relies on the fact that
  firing the root redex of `M` and then reducing arguments gives
  the same result as reducing arguments first and then firing. This
  is true exactly when no other rule's LHS overlaps with the root
  redex's RHS structure — i.e., when the system is overlap-free.)

**Case P-rule.** `M ≡ ℓ[x̄ := T̄]`, `N ≡ r[x̄ := T̄']` with `Tᵢ ⇒
T'ᵢ`. Then `Φ(M)` contracts the root redex plus every redex inside
`T̄`, giving `Φ(M) = Φ(r[x̄ := T̄])`. By the substitution property of
parallel reduction (variable occurrences in `r` are substituted by
arbitrary parallel-reducts, possibly multiple copies when `x` appears
multiply on the right) plus IH `T'ᵢ ⇒ Φ(Tᵢ)`, we have `r[x̄ := T̄']
⇒ r[x̄ := Φ(T̄)] ⇒ Φ(r[x̄ := T̄])`. (The second step uses that `Φ`
commutes with substitution up to parallel reduction: redexes that
become apparent *only after substitution* (i.e., redexes straddling
the substitution site) cannot exist in a left-linear, overlap-free
system because no LHS pattern's structure requires inspecting an
argument beyond its top-level shape.) ✓

(The key technical observation: the RHS of every rule is built from
the metavariables `xᵢ` by applicative nesting. Substituting
parallel-reducts of `Tᵢ` into the RHS is structurally the same as
substituting first and then parallel-reducing, because parallel
reduction is closed under application and the substitution
positions in the RHS are all application-level — no primitive is
formed *by* the substitution.)

---

## §3. Progressive confluence claims

I verify confluence on progressively larger subsets of the 13 rules,
checking at each stage that (i) left-linearity holds, (ii) no new
critical pair is introduced, (iii) the parallel-reduction argument
extends. The increments are chosen to progress from simple
eraser/identity primitives to duplicating and recursive ones.

**Stage 1.** `{I}`. `I x → x`. Left-linear. Single rule, no other
rule to overlap with. Only self-overlap at root (trivial, same rule)
gives no non-trivial critical pair (the critical pair is `x, x`).
Confluent. ✓ (Verified directly: every term with `I`-redexes has a
unique normal form.)

**Stage 2.** `{I, K}`. Adds `K x y → x`. Left-linear. LHS heads `I`
vs `K` — structurally distinguishable. Overlap check: `I a` unifies
with no subterm of `K a b` (different heads); `K a b` unifies with
no subterm of `I a` (arity mismatch / different heads). No critical
pair. Confluent. ✓

**Stage 3.** `{I, K, S}`. Adds `S x y z → x z (y z)`. Left-linear
(three distinct variables on LHS). Head `S` distinct from `I`, `K`.
Overlap with any of the existing rules: none (different heads, and
the LHSs are all "head + variables", not patterns that inspect
argument structure). No critical pair. Parallel reduction extended:
P-rule for `S` uses sub-derivations `Tᵢ ⇒ T'ᵢ` for `i ∈ {1,2,3}`;
the RHS `x z (y z)` duplicates the `z` metavariable, which is
absorbed by allowing the variable `z` in the RHS to receive the
same parallel-reduct `T'₃` at both of its occurrences (Triangle
Lemma case P-rule goes through: `r[z := T₃']` parallel-reduces to
`r[z := Φ(T₃)]` at both occurrences uniformly). Confluent. ✓

**Stage 4.** `{I, K, S, B}`. Adds `B x y z → x (y z)`. Head `B`
distinct. No critical pair. Parallel reduction extended trivially
(RHS is linear). Confluent. ✓

**Stage 5.** `{I, K, S, B, C}`. Adds `C x y z → x z y`. Head `C`
distinct. No critical pair. RHS linear. Confluent. ✓

**Stage 6.** `{…, W}`. Adds `W x y → x y y`. Head `W` distinct. LHS
left-linear. RHS duplicates `y` — handled as in Stage 3. No critical
pair. Confluent. ✓

**Stage 7.** `{…, W, M}`. Adds `M x → x x`. Head `M` distinct. LHS
linear. RHS duplicates `x` — handled. No critical pair. Confluent.
✓ (Note: `M M → M M` is a fixed non-terminating loop; confluence
holds trivially on that trace — each reduct is `M M`.)

**Stage 8.** `{…, M, Y}`. Adds `Y f → f (Y f)`. Head `Y` distinct.
LHS left-linear (one variable `f`). RHS contains `Y f` as a subterm,
which means the RHS is again a redex (at that subterm). This does
**not** create a critical pair: a critical pair arises from overlaps
between LHSs, not from recursion in the RHS. What it does create is
non-termination: the reduct `f (Y f)` contains a residual `Y f`
redex, which when contracted gives `f (f (Y f))`, etc. Confluence
still holds because the diamond-on-`⇒` argument does not require
termination; the Triangle Lemma commutes `Φ` and `⇒` regardless. ✓
(See §6 Example (b) for a concrete joinability trace.)

**Stage 9.** `{…, Y, T}`. Adds `T x y → y x`. Head `T` distinct. LHS
linear, RHS linear. No critical pair. Confluent. ✓

**Stage 10.** `{…, T, V}`. Adds `V x y z → z x y`. Head `V` distinct.
LHS linear, RHS linear. No critical pair. Confluent. ✓

**Stage 11.** `{…, V, D}`. Adds `D x y z w → x y (z w)` (arity-4 LHS,
arity-4 RHS). Head `D` distinct. LHS linear. RHS linear (each of
`x,y,z,w` appears exactly once). No critical pair. Confluent. ✓

**Stage 12.** `{…, D, Π₁}`. Adds `Π₁ x y → x`. Head `Π₁` distinct.
LHS linear, RHS linear. No critical pair. Confluent. ✓

**Stage 13.** `{…, Π₁, Π₂}`. Adds `Π₂ x y → y`. Head `Π₂` distinct
from all previous (including `Π₁` — they are different primitives).
LHS linear, RHS linear. No critical pair. Confluent. ✓

### 3.1 Exhaustive pairwise overlap table

Because all 13 primitives are structurally distinguishable as heads,
and every LHS has the shape `h x₁ … xₐ` (primitive head applied to
`arity(h)` distinct metavariables, each in a variable position), the
only subterms of any LHS are the head `h`, the variables `xᵢ`, and
partial applications `h x₁`, `h x₁ x₂`, … `h x₁ … x_{a-1}`. The
variables and partial applications never unify with any full LHS of
a rule (arity mismatch and/or distinct heads). The head alone, as a
primitive, unifies with any other full LHS only when the other LHS
has the same head (but each primitive has exactly one rule, so this
means the rule is being compared to itself — vacuous critical pair).

Therefore: the overlap table is empty. **No critical pairs. The
baseline is overlap-free.**

### 3.2 Disclosed gaps in the progressive argument

- The Triangle Lemma's RHS-substitution step (Case P-rule, §2.4)
  depends on the claim that no LHS pattern can *straddle* a
  substitution site — i.e., no LHS matches a term of the form
  `C[r[x̄ := T̄]]` where the match is only visible after the
  substitution. In a left-linear, overlap-free system where every
  LHS is "head + variable arguments" and heads are primitives, the
  LHS pattern has no internal structure below the root beyond
  metavariables at the argument positions. So matching an LHS
  against a subterm of `r[x̄ := T̄]` either matches entirely within
  a substituted `Tᵢ` (no straddling) or entirely within the
  skeleton of `r` (also no straddling, since the skeleton of `r`
  contains no metavariable applications at positions where a new
  LHS could crystallize after substitution — every `xᵢ` position
  in `r` is either a top-level argument or part of a nested
  application whose head is another metavariable, not a primitive).
  **This argument is sound but depends on inspecting the RHS shapes
  of the 13 rules.** A direct RHS audit: `x`, `x`, `x z (y z)`, `x
  (y z)`, `x z y`, `x y y`, `x x`, `f (Y f)`, `y x`, `z x y`, `x y
  (z w)`, `x`, `y`. In every case, every subterm's head is a
  metavariable `xᵢ` (possibly the same one) or the primitive `Y`
  (in Y's RHS), never a primitive `≠ Y` at a position created by
  substitution. So straddling is impossible. ✓

- The recursion in `Y`'s RHS (`f (Y f)` mentions `Y` again) could in
  principle be problematic: the RHS contains a primitive `Y` at a
  non-root position. But this primitive appears at a syntactic
  position in `r` that is independent of the substitution — the `Y`
  in `f (Y f)` is literally the same `Y` as on the LHS, there is
  no metavariable there. So after substituting `f := T`, the
  resulting term is `T (Y T)`, which contains the `Y T` subterm.
  This is a `Y`-redex, but it was already going to be a redex
  regardless of what `T` is — the substitution does not "create"
  it, it *writes it in* as part of the RHS template. So it does
  not constitute a straddling match. ✓

---

## §4. Verdict on the full baseline

**Claim.** The reduction relation `→` of the extended calculator,
over the primitive set
`{I, K, S, B, C, W, M, Y, T, V, D, Π₁, Π₂}`, is confluent.

**Proof.** Combine §2 and §3:

1. By §3.1, the system is overlap-free: no non-trivial critical
   pair arises from any ordered rule pair at any non-variable
   position.
2. All 13 rules are left-linear (§3 stage-by-stage: verified).
3. Define parallel reduction `⇒` as in §2.2. By Properties B1–B3,
   `⇒* = ↠*`, so confluence of `→` is equivalent to confluence of
   `⇒`.
4. By the Triangle Lemma (§2.4, cases verified using the overlap-
   freeness and left-linearity established in steps 1–2 and the
   explicit RHS audit in §3.2), `M ⇒ N ⇒ Φ(M)` for all `M ⇒ N`. This
   yields the diamond property on `⇒`.
5. By standard tiling of parallel-reduction diamonds (Property
   B5), `↠` has the diamond property.
6. Diamond property of `↠` is exactly confluence. ∎

**Counting-convention restatement** (per task §4 request):

- "Rule overlap" = a position `q` in some LHS `ℓ₁` such that the
  non-variable subterm `ℓ₁|q` is syntactically unifiable with a
  renaming of some LHS `ℓ₂`.
- "Critical pair" = the pair `⟨ ℓ₁[q ← r₂σ] · σ, r₁σ ⟩` produced by
  the most general unifier `σ` of an overlap, where `r₁, r₂` are
  the RHSs. In this system: the empty set.
- "Residual" = after a parallel step `M ⇒ N` that contracts a set
  of redex occurrences `R ⊆ red(M)`, the **residual** of an
  un-contracted `r ∈ red(M) ∖ R` in `N` is the redex occurrence at
  the positions of `N` that descend from `r`'s position in `M`. A
  duplicated metavariable in an RHS (as with `S`, `W`, `M`, `D`)
  produces multiple residuals of each redex inside the duplicated
  argument.
- "Parallel step" = `⇒` as defined in §2.2.

**What is the largest confluent subset?** The whole baseline. (A
maximal confluent subset, trivially.)

**What is the maximal confluent extension?** The task asks whether
there is a maximal confluent subset of the baseline; the answer is
the whole baseline. Any extension must add new rules; see §4.1 for
a minimal non-confluent extension.

### 4.1 A minimal non-confluent extension

To demonstrate concretely that the overlap-freeness is load-bearing:
consider the extension obtained by adding **exactly one** rule that
introduces a critical pair with an existing rule. The simplest such
rule reuses an existing primitive head with a restricted pattern:

> **New rule `K'`**: `K I x → I`.

Now the subterm `K I a` has two valid reductions:

- By `K x y → x`: match `x := I, y := a`, giving `K I a  →  I`. (OK
  — same result as the new rule in this one case.)

This turns out not to create divergence, because the new rule's
result happens to agree. Let me pick a cleaner example:

> **New rule `K″`**: `K I x → x`.

Now `K I a` has two contractions:

- By `K x y → x` (arity-2 rule): `K I a → I`.
- By `K″`: `K I a → a`.

These are different terms (`I ≢ a` syntactically). Can they be joined?
`I` is a primitive in normal form; `a` is a free variable in normal
form. They are distinct normal forms — no further reduction is
possible for either. Hence no common reduct. Hence **non-confluent**.

The overlap here is: the LHS `K I x` of `K″` is unifiable with the
LHS `K x y` of the existing `K`-rule (via the substitution `x :=
I, y := x`). The resulting critical pair `⟨I, x⟩` — obtained by
applying the two rules to the unified term `K I x` — fails to be
joinable. This is a witness that adding *any* rule whose LHS
instantiates an existing rule's LHS introduces non-confluence, unless
the two rules produce joinable right-hand sides.

(Analogously, one could add a new fresh-head primitive `N` with two
rules `N x → a` and `N x → b` for distinct `a, b`; the self-overlap
at root yields the non-joinable critical pair `⟨a, b⟩`. But this is
a *within-rule* ambiguity, not a cross-rule overlap — the cross-rule
overlap with an existing primitive, as in `K″`, is the subtler case
and illustrates the structural condition better.)

### 4.2 Is the baseline a maximal confluent extension within its
signature?

No — one can add overlap-free rules and retain confluence.
Concretely, any new primitive `N` with a left-linear, overlap-free
rule `N x̄ → r[x̄]` where `r` contains no straddling LHS patterns
still yields a confluent system. For instance, adding
`F x y → x (S y y) y` (a new fresh primitive `F`) does not overlap
with anything; the confluence proof extends verbatim. So the
baseline is *not* maximal in this sense. But it is maximal in the
sense that no subset of the 13 baseline rules is non-confluent and
no rule can be removed to "gain" confluence (since the baseline
already has it).

---

## §5. Verification strategy

I combine two independent verifications.

### 5.1 Strategy (b) — parallel-reduction diamond proof

The proof in §2 + §3 + §4, establishing the diamond property of `⇒`
and lifting to `↠`. This is a symbolic proof, not an empirical check.
It is the primary verification and is self-contained in this document.

### 5.2 Strategy (d) — executable oracle

An independent empirical check via a small simulator at
`task/sim/simulator.py`. The simulator:

1. Represents terms as nested pairs with primitives as string atoms.
2. Implements the 13 reduction rules exactly as stated in the task.
3. For each of seven test terms (the three requested in task §6 plus
   four additional terms stressing the duplicating/recursive
   primitives `W, M, Y, D, S, P₁, P₂, V, T`), performs a bounded
   breadth-first search of single-step reducts up to depth 5–6 with a
   term-size cap (to prevent runaway blow-up of the `Y f`/`M M`
   style).
4. For every pair of reachable reducts, re-runs the BFS from each of
   the pair and checks for a non-empty intersection of their
   descendant sets — i.e., tests joinability within the bound.

Output (captured at `task/sim/output-run1.txt`):

```
EXAMPLE (a):  S (K I a) (I b) (I c)            28 reducts, all pairs join ✓
EXAMPLE (b):  Y f                                6 reducts, all pairs join ✓
EXAMPLE (c):  W (K a) (I b)                      8 reducts, all pairs join ✓
EXAMPLE (d):  D (K a) (I b) (I c) w             10 reducts, all pairs join ✓
EXAMPLE (e):  M (I a)                            6 reducts, all pairs join ✓
EXAMPLE (f):  S (Π₁ a b) (Π₂ c d) e              8 reducts, all pairs join ✓
EXAMPLE (g):  V a b (T c d)                      4 reducts, all pairs join ✓
```

The simulator output is consistent with the symbolic proof:
confluence is observed on bounded traces of terms exercising every
rule category (erasers, duplicators, recursive-generators). Bounded
BFS cannot prove confluence in general (it can only fail to find a
counter-example within the bound), but for *orthogonal* systems the
symbolic proof in §2 is the authoritative witness, and the simulator
is a complementary sanity check.

**Limitations of the executable oracle** (disclosed):

- Depth/size caps. For `Y f`, reduction never terminates, so the
  BFS is truncated. A rejoinability that exists at depth 20 but not
  at depth 5 would be falsely flagged "unjoined within bound" — but
  in practice, for the small terms tested, the bound is more than
  sufficient because the diamond property produces rejoiners
  within one or two extra parallel steps.
- Test-suite coverage. The seven terms do not enumerate all
  possible redex-configuration shapes; they are chosen
  representatively. The symbolic proof in §2 covers the general
  case.

---

## §6. Worked examples

The three requested examples appear first, with full traces, and are
supplemented by four additional examples from the simulator.

### 6.1 Example (a) — `S (K I a) (I b) (I c)`

Let `M ≡ S (K I a) (I b) (I c)`. This term has **four** distinct
redex occurrences at depth 1:

- `r₀`: `S`-redex at the root (all three `S`-arguments present).
- `r₁`: `K I a`-redex at position `L·L·R` (the `K I a` subterm).
- `r₂`: `I b`-redex at position `L·R`.
- `r₃`: `I c`-redex at position `R`.

I present two reduction orders that diverge at the first step, then
rejoin.

**Order α (outermost first).** Contract the `S`-redex `r₀`:

```
M = S (K I a) (I b) (I c)
  →                                      [r₀ : S-rule]
    (K I a) (I c) ((I b) (I c))
```

(Here the metavariables bind `x := K I a, y := I b, z := I c`, so the
RHS `x z (y z)` becomes `(K I a) (I c) ((I b) (I c))`.)

Call this `Mα`. Remaining redexes: the `K I a` sitting at the outer-
left (can reduce by `K x y → x` with `x := I, y := a`, but note it
appears in `(K I a) (I c)` — this is `((K I a) (I c))` as an
application of `K I a` to `I c`, so to reduce `K` we first need to
consume its second argument `a`, which it already has, giving `I`).
Work it out:

```
Mα = ((K I a) (I c)) ((I b) (I c))
   → (I (I c)) ((I b) (I c))              [K-redex: K I a → I]
   → (I c) ((I b) (I c))                  [I-redex at left]
   → c ((I b) (I c))                      [I-redex at left]
   → c (b (I c))                          [I-redex: I b → b]
   → c (b c)                              [I-redex: I c → c]
```

**Order β (innermost first).** Contract `r₁, r₂, r₃` before `r₀`:

```
M = S (K I a) (I b) (I c)
  → S I (I b) (I c)                       [K-redex: K I a → I, yields I]
  → S I b (I c)                           [I-redex: I b → b]
  → S I b c                               [I-redex: I c → c]
  → I c (b c)                             [S-redex: S I b c → I c (b c)]
  → c (b c)                               [I-redex: I c → c]
```

Common reduct: `c (b c)`. ✓

The simulator reports 28 reachable reducts from `M` at depth ≤ 6,
with every pair joinable. This is consistent with orthogonality:
intermediate divergences always rejoin, and the terminal normal form
(where `b, c` are free variables in normal form) is `c (b c)`.

### 6.2 Example (b) — `Y f` non-terminating divergence

Let `M ≡ Y f`. The unique root redex contracts to `f (Y f)`.

```
M = Y f
  → f (Y f)                                [Y-redex]
```

At this point there is a `Y`-redex at position `R` (inside `f (…)`).
Two continuations:

**Path α**: contract the inner `Y f`:

```
f (Y f)
  → f (f (Y f))                            [inner Y-redex]
```

**Path β**: do not contract (stay where we are, i.e., zero further
reductions; but to exhibit divergence, pick a second path that
contracts `Y f` at a different descendant). For a richer divergence,
consider applying `f` to a specific term, say `f ≡ I`:

```
M = Y I
  → I (Y I)                                [Y]
  → Y I                                    [I-redex]  (loop!)
```

Simultaneously, from `Y I`:

```
M = Y I
  → I (Y I)                                [Y]
  → I (I (Y I))                            [inner Y]
  → I (Y I)                                [outer I]
  → Y I
```

Every reduction of `Y I` visits the set `{Y I, I (Y I), I (I (Y I)),
… }` and cycles back to `Y I`. In particular, any two reducts
re-join at `Y I` (or at `I (Y I)`, etc.). The simulator confirms: from
the generic term `Y f`, the 6 reducts reachable within depth 5 all
have pairwise common reducts.

This demonstrates confluence in the **presence of non-termination**:
the diamond on `⇒` does not require a terminal normal form; it only
requires that diverging reductions rejoin at *some* future reduct,
which they do.

### 6.3 Example (c) — Leftmost-outermost vs rightmost-innermost

Let `M ≡ W (K a) (I b)`. Two reduction strategies:

**Leftmost-outermost.** The leftmost-outermost redex is the `W`-
redex at the root.

```
M = W (K a) (I b)
  → (K a) (I b) (I b)                      [W-redex: W x y → x y y]
```

Call this `Mlo`. Now redexes at: root (`K a (I b)` reducible since
`K` now has enough arguments? `(K a) (I b) (I b)` — the leftmost-
outer at root is the `K`-redex consuming `a` and `I b`: `K a (I b)
→ a`). Continue:

```
Mlo = (K a) (I b) (I b)
    → a (I b)                              [K-redex: K a (I b) → a, drops the first I b argument]
    → a b                                  [I-redex]
```

**Rightmost-innermost.** Reduce the deepest redex first. Here the
candidates are `I b` (at position `R`) and `K a` (at position `L·R`);
neither is a redex on its own (`K` needs two args, has one; `I` is
arity-1 and has `b` — so `I b` IS a redex). Actually `K a` alone is
not a redex (one argument). So the innermost redex is `I b`.

```
M = W (K a) (I b)
  → W (K a) b                              [I-redex: I b → b]
  → (K a) b b                              [W-redex]
  → a b                                    [K-redex: K a b → a]
```

Common reduct: `a b`. ✓ Both strategies reach the same normal form,
as confluence demands.

### 6.4 Additional example — Duplication via `S` with nested redexes

Let `M ≡ S A (I b) c` where `A` is itself an arbitrary reducible term.
The `S`-rule duplicates `c` (its third argument). After contraction:

```
M = S A (I b) c
  → A c ((I b) c)                           [S-rule: S x y z → x z (y z)]
```

There is now a redex `(I b) c` at position `R` (the inner `I b →
b`):

```
A c ((I b) c)  →  A c (b c)
```

If we had instead reduced `I b → b` first in `M`:

```
M = S A (I b) c
  → S A b c                                 [I-redex]
  → A c (b c)                               [S-rule]
```

Same result. ✓ This illustrates that the duplication of `c` by `S`
does not obstruct confluence: the two occurrences of `c` in the
result are the same term, and any redex inside `c` appears as two
residuals, which parallel reduction handles uniformly.

### 6.5 Additional example — `M M` / `M` self-loop

`M` applied to itself: `M M → M M` (since `M x → x x` with `x := M`).
The trace is `M M → M M → M M → …`. Every reduct is `M M`. Trivially
confluent.

### 6.6 Additional example — `D (K a) b (I c) d`

```
N = D (K a) b (I c) d
  → (K a) b ((I c) d)                        [D-rule: D x y z w → x y (z w)]
  → a ((I c) d)                              [K-rule at outer: K a b → a,
                                              but wait — (K a) b is (K a) applied to b,
                                              which matches K x y with x := a, y := b, → a]
  → a (c d)                                  [I-redex]
```

Alternative order — reduce `I c` first:

```
N = D (K a) b (I c) d
  → D (K a) b c d                            [I-redex]
  → (K a) b (c d)                            [D-rule]
  → a (c d)                                  [K-rule]
```

Same result. ✓

---

## §7. Open questions and known limitations

### 7.1 Extension to strong (under-binder) reduction

If the baseline is extended to include λ-abstraction `λx. M` with
β-reduction `(λx. M) N → M[x := N]`, and reduction is permitted
*under* binders (strong reduction), the parallel-reduction argument
still applies in principle — but only after (i) the pattern-match
check is adjusted to account for α-equivalence and capture-avoiding
substitution, and (ii) the "straddling" check in §3.2 is re-done.
Capture-avoiding substitution satisfies a parallel-substitution
lemma analogous to the one used here: `M ⇒ M'` and `N ⇒ N'` imply
`M[x := N] ⇒ M'[x := N']`. With that lemma in place, the Triangle
Lemma generalizes. The 13 rules of the baseline are closed under
such an extension: none of them bind variables, so they commute with
any β-step. I expect confluence to extend to the joint system of the
baseline + β, but I have not proved the substitution lemma in this
document.

### 7.2 Relationship between confluence and normalization

In a **terminating** rewrite system, local confluence implies
confluence (via a well-known induction on termination: pick the
smallest counter-example by termination order). Our system is **not**
terminating, so that route is closed — but confluence still holds
by the parallel-reduction argument, which is independent of
termination.

- Orthogonality (left-linearity + overlap-freeness) **implies**
  confluence (our result). It does **not** imply strong
  normalization: `Y f` and `M M` diverge.
- Confluence plus weak normalization (if every term has *some*
  reduct to a normal form) implies **unique normal forms**:
  whenever a term `M` has a normal form, it is unique. This is
  because two normal-form reducts `N₁, N₂` of `M` would, by
  confluence, have to be joinable at a common reduct, and the only
  reducts of a normal form are itself, so `N₁ ≡ N₂`.
- In our system: not every term has a normal form (`Y f`, `M M` do
  not). But *whenever* a normal form exists, it is unique. This is
  the strongest uniqueness claim compatible with the rules.

### 7.3 Dependence on the reduction strategy

The confluence result is a property of the relation `→`, not of any
particular strategy. A **strategy** is a function `s: Terms → Redex-
positions ∪ {⊥}` specifying which redex to contract next. Confluence
says: any two terminating strategies agree on the normal form (when
one exists). For non-terminating strategies, confluence does not
guarantee they produce the same infinite trace — it only guarantees
that at every step, any divergence from a previous state is joinable.
In particular:

- **Leftmost-outermost** strategy: produces the normal form of any
  weakly-normalizing term (a standard result for orthogonal
  systems, though we do not prove it here — it requires a
  "standardization" argument).
- **Rightmost-innermost** strategy: may diverge on terms whose
  normal form exists. E.g., `K a (Y f)` has normal form `a` under
  leftmost-outermost (the `K`-redex discards the `Y f`), but
  rightmost-innermost would try to normalize `Y f` first and
  diverge. So confluence ≠ strategy-equivalence for non-
  terminating terms.

This is a standard and unavoidable asymmetry.

### 7.4 Non-orthogonal confluent extensions

Can the baseline be extended with rules whose LHSs overlap with
existing rules, while remaining confluent? Yes, **if the induced
critical pairs are joinable**.

Example: add `K K x → K x`. This overlaps with the existing
`K x y → x` rule at the LHS `K K x`: applying `K x y → x` with `x :=
K, y := x` gives `K K x → K`; applying the new rule gives `K K x →
K x`. Critical pair: `⟨K, K x⟩`. Is this joinable? `K` is a normal
form (primitive, no redex). `K x` with an arbitrary variable `x`: if
`x` is free, `K x` is not a redex (arity unsatisfied). `K` and
`K x` are distinct normal forms — not joinable. So this extension
is **non-confluent**.

Example with joinable critical pair: add `K I x → I`. Overlap with
`K x y → x`: unifying `K x y` with `K I x'` (renaming metavariables)
gives substitution `x := I, y := x'`; the two rules give `K I x' → I`
(from original) and `K I x' → I` (from new) — same result. No
divergence. Hence this extension is **confluent** (trivially: the
critical pair has a common reduct, namely `I` itself, at depth 0).

**Rule shapes that preserve confluence under non-orthogonality.** The
general principle: a rewrite system can have overlapping rules and
still be confluent provided every critical pair is joinable.
Checking this is the classic critical-pair closure procedure. For
the baseline extended with `K I x → I`, the closure is trivial (one
critical pair, already joinable). For richer extensions, one would
run the closure procedure to completion (bounded iteration) and
accept the extension if it reaches a fixpoint with all critical pairs
joinable.

**Open question 7.4-Q1.** Is there a largest confluent extension of
the baseline by a *single* additional rule using only primitive
heads? I conjecture yes, and that the space is parametrized by
"which existing rule's LHS can be instantiated to produce a rule
whose RHS coincides with the existing RHS on that instance", but I
have not enumerated the space in this document.

**Open question 7.4-Q2.** Does adding a rule of the form `N x → I x`
for a fresh primitive `N` (trivially non-overlapping) and a
cross-rule `N (N x) → N x` (which overlaps with itself: applying the
outer rule `N (N x) → I (N x)` vs the new rule gives `I (N x)` vs
`N x`, and these join via `I (N x) → N x`) yield a confluent
extension? Answer: yes, by the joinability of that single critical
pair. So non-orthogonal confluent extensions exist.

### 7.5 Dependence on "weak reduction" semantics

"Weak reduction" in this context means: we reduce at any position,
without binder-commutativity constraints. Since there are no binders,
the distinction between weak and strong reduction is vacuous here —
any position is reducible. When binders are added (§7.1), weak vs
strong becomes meaningful, and the argument would need to be re-
examined.

### 7.6 Dependence on the specific primitive set

The confluence proof uses only the structural conditions (left-
linearity, overlap-freeness, non-straddling RHS). Any primitive set
satisfying these conditions enjoys the same argument. The specific
choice of 13 primitives does not matter for the proof itself — what
matters is the structural shape of the rules.

---

## §8. Concluding synthesis

The extended calculator's reduction relation is confluent. The
mechanism is orthogonality: all 13 LHSs are left-linear and
pairwise non-overlapping, so the standard parallel-reduction diamond
argument applies. Non-termination (via `Y, M`) is handled by the
argument's independence from strong normalization. An executable
oracle confirms bounded joinability on seven representative terms.

Counting conventions, critical-pair analysis, progressive subset
verification, worked examples, and an explicit minimal non-confluent
extension (`K″ : K I x → x`) are supplied to discharge each of the
task's seven requested deliverables.

**Disclosed gaps.**

1. The Triangle Lemma's RHS-substitution step assumes that no LHS
   pattern can straddle a substitution site; I discharge this by an
   explicit RHS audit of the 13 rules in §3.2. A general structural
   proof (for arbitrary LHS shapes) is deferred.
2. The parallel-substitution lemma (required for extending to
   λ-binders in §7.1) is stated but not proved.
3. The executable oracle has finite depth/size bounds; it cannot
   rule out non-confluence at arbitrary depth. The symbolic proof
   in §2 is authoritative.
4. I do not characterize the space of confluent non-orthogonal
   extensions (§7.4-Q1 left open).

These four gaps are disclosed, not hidden.
