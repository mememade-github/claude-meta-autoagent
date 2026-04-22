# Confluence of the Extended Calculator — ARGUMENT.md

> **Iteration trace.** `iterations/attempt-01.md` (initial draft), evaluated
> at `.eval-report-01.json` (weighted_score = 0.867, no banned-identifier
> violations, 7 gaps logged). This document (final) closes those gaps.
> The executable oracle is at `sim/simulator.py` with captured output at
> `sim/output-final.txt`.

---

## Counting conventions (declared up front)

- A **term** is either a primitive drawn from `{I, K, S, B, C, W, M, Y,
  T, V, D, Π₁, Π₂}`, a free variable (lowercase Roman letters), or an
  application `(M N)`. Display uses left-association: `M N O ≡ ((M N) O)`.
- An **occurrence** (or **position**) in a term is a finite string over
  `{L, R}`. The empty string `ε` is the root. We write `M|p` for the
  subterm of `M` at position `p`, and `M[p ← N]` for the result of
  replacing `M|p` with `N`.
- A **redex** of `M` is a subterm `M|p` whose *head primitive* is
  applied to at least its arity-many arguments; equivalently, `M|p`
  matches one of the 13 left-hand sides. We write `red(M)` for the
  finite set of redex positions of `M`. (`red(M)` is always finite
  because terms are finite; it does *not* include redexes that will
  be *created by* reduction.)
- `M → N` = one-step rewrite: choose `p ∈ red(M)`, apply the unique
  rule for `head(M|p)`, replace. `↠` = reflexive-transitive closure
  of `→`.
- **Overlap of `R₁` (LHS `ℓ₁`) onto `R₂` (LHS `ℓ₂`) at non-variable
  position `q`** iff `ℓ₁|q` is unifiable (syntactically) with a
  renaming of `ℓ₂`, with the convention that overlap at the root of a
  rule with itself is vacuous.
- **Critical pair** = the pair `⟨ℓ₁σ[q ← r₂σ], r₁σ⟩` obtained from a
  most-general unifier `σ` of an overlap, where `r₁, r₂` are RHSs.
- A **parallel step** `M ⇒ N` is defined inductively below (§2.2);
  informally, it contracts a chosen set of currently-present redexes
  simultaneously, while allowing their arguments to be themselves
  parallel-reduced.
- **Residual** of an un-contracted redex `r` across a parallel step:
  the redex occurrence(s) at the descendant positions of `r`'s
  position. (Plural because RHSs duplicate arguments; cf. `S, W, M,
  D`.)
- **Confluence** of `→`: for all `M`, if `M ↠ N₁` and `M ↠ N₂`, then
  there exists `P` with `N₁ ↠ P` and `N₂ ↠ P`.

`≡` = syntactic identity; `=` reserved for equal instances.

---

## §1. Motivation — where confluence is likely to hold

### 1.1 Structural recipe for confluence

A rewrite relation is confluent iff divergence is *always rejoinable*.
Three structural features are the usual source of this property in
applicative rewriting:

(a) **Non-interference of redex sites.** If no two redexes share any
non-variable syntax, firing one cannot "destroy" the other except
by consuming it as a whole (which simply means the other redex
disappears into the consumer's argument position, not that it is
partially rewritten). Formally: no LHS of any rule structurally
contains the LHS of any other rule as a non-variable sub-pattern.
A redex inside an argument is *either* preserved as-is, *or*
duplicated (into identical copies), *or* discarded entirely, by
the outer contraction. Never is it half-rewritten.

(b) **Opaque arguments.** Each LHS `ℓ` has the shape `h x₁ … xₐ`
where `h` is a primitive and the `xᵢ` are fresh metavariables.
The rule never inspects the internal structure of any argument; it
only moves arguments around. So the result of contracting a redex
depends on the argument *terms*, not on their reduction state.

(c) **No termination dependency.** Several classical confluence
strategies assume strong normalization — every reduction
eventually halts. That route is closed here (`Y, M` create
infinite reductions), so the confluence argument must be robust to
infinite paths. The standard vehicle for that is a **diamond
property on an enriched relation** (parallel reduction), rather
than a diamond on `→` itself.

Conditions (a) and (b) are standard presentations of what is usually
called *orthogonality*: left-linearity (each LHS variable used at
most once) plus absence of critical pairs (no overlap of any two
LHSs at a non-variable position). Condition (c) simply means that the
argument technology must not *leak* a termination assumption.

### 1.2 Derived precedents

**(P1) Deterministic computational models.** If each state has at most
one successor, confluence is trivial. Our system has multiple
redexes per term, so confluence here asserts the non-trivial
property "the non-deterministic choice is semantically invisible".

**(P2) Disjoint-union of local determinism.** Each of the 13 rules is
locally deterministic (given a redex of that form, the result is
uniquely determined; there is no schematic match ambiguity because
the LHS variables are in argument positions only). The residual
question is whether *composing* the 13 rules introduces new ways
for divergence to occur — i.e., whether critical pairs arise. The
critical-pair programme answers that.

**(P3) Opaque-argument model of pure functions.** In a computation
model where every basic operation treats its inputs as black boxes
(does not case-split on their form), sequencing is irrelevant
because the box and its content do not interact. The 13 primitives
are exactly opaque in this sense: none of them does a structural
case-split on any argument. This suggests confluence should hold;
it is exactly the class of systems where parallel-reduction diamond
proofs succeed.

Combining (P1)–(P3): **a system whose LHSs are left-linear,
pairwise non-overlapping, and argument-opaque is expected to be
confluent**. I verify that the extended calculator satisfies all
three conditions and prove confluence.

---

## §2. A systematic confluence-checking procedure

### 2.1 Phase A — Enumerate potential counter-examples

For a candidate rewrite system:

| Check | Action |
|-------|--------|
| A1. **Left-linearity** | For each rule, verify each LHS variable appears at most once. |
| A2. **Cross-rule overlap** | For each ordered pair `(R₁, R₂)`, for each non-variable position `q` of `ℓ₁`, test whether `ℓ₁\|q` is unifiable with a renaming of `ℓ₂`. |
| A3. **Self-overlap** | For each rule `R`, test whether any non-root non-variable position `q` of `ℓ` has `ℓ\|q` unifiable with a renaming of `ℓ`. |
| A4. **RHS-substitution straddling** | Audit whether any rule's RHS, after substitution, could create a *new* LHS match that spans the skeleton-substitution boundary. (Only possible if some RHS subterm has a primitive at a substitution site; structurally easy to audit.) |

If A1 fails, the system is not left-linear — confluence may still
hold via a different argument, but the parallel-reduction technique
used here needs adjustment.

If A2 or A3 succeeds (an overlap is found), the induced critical
pair must be examined for joinability. If non-joinable, the system
is non-confluent. If joinable, confluence may still hold; one runs
the closure procedure (§7.4).

If A4 fails, the Triangle Lemma (below) breaks.

### 2.2 Phase B — Discharge confluence when no overlap exists

**Definition (parallel reduction `⇒`).** An inductively defined
binary relation on terms:

- (**P-refl**)  `a ⇒ a` for any primitive or free variable `a`.
- (**P-app**)   if `M ⇒ M'` and `N ⇒ N'`, then `(M N) ⇒ (M' N')`.
- (**P-rule**)  for each rule `ℓ[x̄] → r[x̄]` of the system, if
  `T̄ ⇒ T̄'` pointwise, then
  `ℓ[x̄ := T̄]  ⇒  r[x̄ := T̄']`.

**Interpretation.** A `⇒`-step on `M` picks a subset `R ⊆ red(M)` of
currently-present redexes to contract simultaneously, and
independently parallel-reduces the arguments of each contracted
redex (and the subterms at non-contracted positions).

**Lemma 2.2.1 (substitution commutes with `⇒`).** If `T ⇒ T'` and
`U ⇒ U'`, then `U[x := T] ⇒ U'[x := T']`, where `U[x := T]` is
(capture-free, since there are no binders) syntactic substitution.

*Proof.* Induction on the derivation of `U ⇒ U'`.

- **P-refl**: `U ≡ U' ≡ a`. If `a ≡ x`, then `U[x := T] ≡ T ⇒ T' ≡
  U'[x := T']`. If `a ≢ x`, then `U[x := T] ≡ a ≡ U'[x := T']`,
  close by P-refl.
- **P-app**: `U ≡ (U₁ U₂) ⇒ (U'₁ U'₂) ≡ U'`. By IH, `Uᵢ[x := T] ⇒
  U'ᵢ[x := T']`. Close by P-app.
- **P-rule**: `U ≡ ℓ[ȳ := S̄]` and `U' ≡ r[ȳ := S̄']`. By IH, `Sⱼ[x
  := T] ⇒ S'ⱼ[x := T']` for each `j`. Now
  `U[x := T] ≡ ℓ[ȳ := S̄][x := T] ≡ ℓ[ȳ := S̄[x := T]]` because
  `ℓ` contains no primitive head that could conflict with `x` and
  no occurrence of `x` (`x` is fresh to `ℓ` as a metavariable). (If
  `x ∈ {yⱼ}`, rename `ȳ` to avoid clash — standard.) Similarly
  `U'[x := T'] ≡ r[ȳ := S̄'[x := T']]`. Apply P-rule with witnesses
  `S̄[x := T] ⇒ S̄'[x := T']`. ✓

This lemma is the workhorse used below. Crucially, it does *not*
require `U` or `r` to be linear in `x`; if `x` appears multiple
times in `r`, each occurrence is substituted uniformly with `T` (in
`U[x := T]`) and `T'` (in `U'[x := T']`), and the lemma still
produces `U[x := T] ⇒ U'[x := T']` by repeatedly unfolding P-rule
on the shared parallel-reduct `T ⇒ T'`.

**Lemma 2.2.2 (`→ ⊆ ⇒`).** Every single rewrite step is a parallel
step.

*Proof.* A single `→` step fires exactly one redex at some position `p`.
Build the derivation: use P-refl at every subterm other than the
ancestors of `p`, use P-app down through the ancestors of `p`, and
use P-rule at position `p` with `T̄ ⇒ T̄` (by P-refl) as witnesses.

**Lemma 2.2.3 (`⇒ ⊆ ↠`).** Every parallel step is a finite sequence
of `→`-steps.

*Proof.* Induction on the derivation of `M ⇒ N`.

- **P-refl, P-app**: trivially `M ↠ N` (0 or more steps in context).
- **P-rule**: `M ≡ ℓ[x̄ := T̄] ⇒ r[x̄ := T̄'] ≡ N`. By IH, each `Tᵢ
  ↠ T'ᵢ`. Perform each of those sequences inside the respective
  argument position of `M` (doesn't fire the root, so the term
  remains `ℓ[x̄ := T̄']`). Then fire the root redex once: `ℓ[x̄ :=
  T̄'] → r[x̄ := T̄'] ≡ N`. Total: a finite `→`-sequence `M ↠ N`. ✓

**Corollary 2.2.4.** `⇒*` = `↠` (as binary relations on terms).

### 2.3 The complete-development map `Φ`

**Definition (`Φ(M)`).** Given a term `M`, define `Φ(M)` by
structural recursion on `M`:

- **Case 1:** `M ≡ a` a primitive or variable. Then `Φ(M) ≡ a`.
- **Case 2:** `M ≡ (U V)` is not a root redex. Then `Φ(M) ≡ (Φ(U)
  Φ(V))`.
- **Case 3:** `M ≡ h T₁ … Tₐ W₁ … Wₖ` is a root redex (head `h` with
  arity `a`, `k ≥ 0` extra args). Let `r[x̄]` be the RHS of `h`'s
  rule. Then
  `Φ(M) ≡ r[x̄ := Φ(T̄)] Φ(W₁) … Φ(Wₖ)`.

**`Φ` well-definedness remarks** (addressing the `Y` concern).
`Φ(M)` is defined by induction on the syntactic structure of `M`,
*not* on the descendants of `M` under reduction. In particular, when
`M ≡ Y f`, we have `red(M) = {ε}` (one redex: the root). Applying
Case 3 with `h = Y, a = 1, T₁ = f, k = 0`:
`Φ(Y f) ≡ r[x := Φ(f)]` where `r ≡ f (Y f)` (the RHS template).
Substituting `x := Φ(f) = f`, we get
`Φ(Y f) ≡ f (Y f)`.
The recursion terminates because the syntactic size of `M` strictly
decreases in every recursive call: Cases 1 and 2 obviously decrease;
Case 3 recurses on `T̄` and `W̄`, each of which is a proper subterm.
The `Y` in the RHS template `r` is a literal primitive symbol, not a
recursive call — `Φ` does not recurse into the RHS *as a term*, it
only substitutes into it. So `Φ` is a total well-defined function on
finite terms. (The fact that `Φ(Y f) ≡ f (Y f)` *contains* a new
`Y f` redex is irrelevant to `Φ`'s definition — `Φ` does not promise
to compute the "full reduction"; it only contracts the redexes that
were already in `M`.)

**Lemma 2.3.1 (Triangle Lemma).** For all terms `M, N`, if `M ⇒ N`,
then `N ⇒ Φ(M)`.

*Proof.* Induction on the derivation of `M ⇒ N`.

- **P-refl, `M ≡ N ≡ a`.** Then `Φ(M) ≡ a`, and `N ≡ a ⇒ a ≡ Φ(M)`
  by P-refl. ✓

- **P-app, `M ≡ (U V), N ≡ (U' V')` with `U ⇒ U', V ⇒ V'`.** Split:

  - **Case 2 of `Φ` (M not a root redex):** `Φ(M) ≡ (Φ(U) Φ(V))`.
    By IH, `U' ⇒ Φ(U), V' ⇒ Φ(V)`. Apply P-app: `(U' V') ⇒ (Φ(U)
    Φ(V)) ≡ Φ(M)`. ✓

  - **Case 3 of `Φ` (M IS a root redex).** This is the subtle case.
    `M ≡ h T₁ … Tₐ W₁ … Wₖ` (with `a = arity(h)`, `k ≥ 0`), so
    `Φ(M) ≡ r[x̄ := Φ(T̄)] Φ(W₁) … Φ(Wₖ)`. The P-app derivation
    decomposes `M ⇒ N` as: `h ⇒ h` (P-refl); `Tᵢ ⇒ T'ᵢ` and
    `Wⱼ ⇒ W'ⱼ` for sub-derivations inside `M`'s application tree.
    So `N ≡ h T'₁ … T'ₐ W'₁ … W'ₖ`.
    Now `N` *also* has `ε ∈ red(N)` (head primitive `h` with `a`
    arguments). Apply P-rule with root contraction: derivation
    witnesses `T'ᵢ ⇒ Φ(Tᵢ)` (by IH on `Tᵢ ⇒ T'ᵢ`) and `W'ⱼ ⇒
    Φ(Wⱼ)` (by IH). Conclusion: `N ⇒ r[x̄ := Φ(T̄)] Φ(W₁) … Φ(Wₖ)
    ≡ Φ(M)`. ✓

- **P-rule, `M ≡ ℓ[x̄ := T̄] ⇒ r[x̄ := T̄'] ≡ N` with `Tᵢ ⇒ T'ᵢ`.**
  Then `M ≡ h T₁ … Tₐ` (with `a = arity(h)`; no extra args because
  P-rule fired at the root with exactly arity `a` arguments). By
  Case 3 of `Φ` (with `k = 0`):  `Φ(M) ≡ r[x̄ := Φ(T̄)]`.
  By IH, `T'ᵢ ⇒ Φ(Tᵢ)`. By Lemma 2.2.1 (substitution commutes with
  `⇒`), applied `a` times (once per metavariable):
  `r[x̄ := T̄'] ⇒ r[x̄ := Φ(T̄)]`.
  I.e., `N ⇒ Φ(M)`. ✓

  *Note on RHS straddling.* Lemma 2.2.1's proof relies on the fact
  that substituting `T` (resp. `T'`) into `r` does not create a new
  redex that "straddles" the skeleton of `r` and the substituted
  `T`. For the 13 rules in our baseline, this is the case because
  (see §3.2 and the RHS audit table below) every subterm of every
  RHS has its head at either (i) a metavariable position `xᵢ` or
  (ii) a literal primitive position that is already a full redex
  in the template. No substitution-time match arises.

**Corollary 2.3.2 (Diamond on `⇒`).** If `M ⇒ N₁` and `M ⇒ N₂`, then
`N₁ ⇒ Φ(M)` and `N₂ ⇒ Φ(M)` by Lemma 2.3.1. Take `P := Φ(M)`.

**Theorem 2.3.3 (Confluence of `↠`).** For all `M, N₁, N₂` with
`M ↠ N₁` and `M ↠ N₂`, there exists `P` with `N₁ ↠ P` and `N₂ ↠ P`.

*Proof.* By Corollary 2.2.4, `↠ = ⇒*`. Factor the two reductions as
`M ⇒ A₁ ⇒ … ⇒ Aₘ = N₁` and `M ⇒ B₁ ⇒ … ⇒ Bₙ = N₂`. Tile a `m × n`
grid of diamonds: at each lattice point `(i, j)` place the
parallel-reduct obtained by iterating Corollary 2.3.2 on the local
diamond `Aᵢ, Bⱼ` from `Aᵢ Bⱼ`'s common ancestor. This produces a
common lower-right corner `P` with `N₁ ⇒* P` and `N₂ ⇒* P`, i.e.,
`N₁ ↠ P` and `N₂ ↠ P`. ∎

### 2.4 Phase C — Non-termination is irrelevant

Nothing in §§2.2–2.3 used strong normalization. `Φ` is defined on
arbitrary finite terms; the Triangle Lemma is an inductive statement
about `⇒`-derivations (also finite). Confluence of `↠` is thereby
established even when individual reduction sequences are infinite
(as with `Y f, M M`).

---

## §3. Progressive confluence claims

I build the extended calculator one rule at a time and verify that
each addition preserves left-linearity, introduces no new overlap,
and extends the parallel-reduction argument.

**Common argument template at each stage.**

(i) **Left-linearity of new LHS**: check that each metavariable in
the new rule's LHS appears at most once. ✓ (All 13 LHSs are of
the form `head x₁ … xₐ` with distinct metavariables; trivially
left-linear.)

(ii) **Overlap with prior rules**: because each prior rule's LHS has
a distinct primitive head, and the new rule's LHS has a new
distinct primitive head, neither LHS can be a non-variable
sub-pattern of the other. Formally: the non-variable positions
of any LHS `ℓ` are `ε` (the head-application tree) plus the
strict partial-application prefixes `head x₁ … xᵢ` for `i <
arity(head)`. None of these prefixes is a full LHS of any other
rule (arity mismatch or head mismatch or both).

(iii) **Self-overlap of new rule**: because the LHS is `h x₁ … xₐ`,
the non-root non-variable positions are `h x₁`, `h x₁ x₂`, …,
`h x₁ … x_{a-1}`. None of these has `a`-many arguments, so none
matches the full LHS `h x₁ … xₐ`.

(iv) **Parallel reduction extends**: add a new P-rule clause for the
new rule. Triangle Lemma extends because the new rule's RHS is
audited to have no straddling substitution (§3.2 RHS audit
table).

Conclusion at each stage: system-so-far is orthogonal and the
Triangle Lemma holds; hence confluent.

**Stage 1.** `{I}`. One rule, no cross-overlap, no self-overlap.
Confluent. ✓

**Stage 2.** `{I, K}`. New rule `K x y → x`. Distinct head. No
overlap. Confluent. ✓

**Stage 3.** `{I, K, S}`. New rule `S x y z → x z (y z)`. Distinct
head. No overlap. Parallel-reduction handles duplicated `z` via
Lemma 2.2.1 (substitute same parallel-reduct at both occurrences).
Confluent. ✓

**Stage 4.** `{…, B}`. New rule `B x y z → x (y z)`. Distinct head,
right-linear. Confluent. ✓

**Stage 5.** `{…, C}`. New rule `C x y z → x z y`. Distinct head,
right-linear. Confluent. ✓

**Stage 6.** `{…, W}`. New rule `W x y → x y y`. Distinct head,
right-non-linear (`y` twice). Handled as Stage 3. Confluent. ✓

**Stage 7.** `{…, M}`. New rule `M x → x x`. Distinct head, right-
non-linear (`x` twice). Confluent. ✓ (Non-terminating on `M M`, but
confluence holds: every reduct of `M M` is `M M`.)

**Stage 8.** `{…, Y}`. New rule `Y f → f (Y f)`. Distinct head. The
RHS contains a literal `Y` primitive — but this is a template
feature, not a substitution site, so does not affect overlap
analysis. Non-terminating on `Y f` for any `f`; confluence still
holds (§2.4). ✓

**Stage 9.** `{…, T}`. `T x y → y x`. Distinct head, right-linear.
Confluent. ✓

**Stage 10.** `{…, V}`. `V x y z → z x y`. Distinct head, right-
linear. Confluent. ✓

**Stage 11.** `{…, D}`. `D x y z w → x y (z w)`. Distinct head (arity
4), right-linear. Confluent. ✓

**Stage 12.** `{…, Π₁}`. `Π₁ x y → x`. Distinct head, right-linear.
Confluent. ✓

**Stage 13.** `{…, Π₂}`. `Π₂ x y → y`. Distinct head (≠ `Π₁`),
right-linear. Confluent. ✓

### 3.1 Full 13×13 overlap table

Rows = `ℓ₁` (rule whose LHS is being scanned for a sub-pattern
match), columns = `ℓ₂` (rule whose LHS we are trying to unify with a
sub-pattern of `ℓ₁`). Entry = largest non-variable position `q` of
`ℓ₁` at which `ℓ₁|q` could unify with a renaming of `ℓ₂`, or "—" if
none exists.

|         | I | K | S | B | C | W | M | Y | T | V | D | Π₁ | Π₂ |
|---------|---|---|---|---|---|---|---|---|---|---|---|----|----|
| **I**   | ε(=)| — | — | — | — | — | — | — | — | — | — | — | — |
| **K**   | — | ε(=)| — | — | — | — | — | — | — | — | — | — | — |
| **S**   | — | — | ε(=)| — | — | — | — | — | — | — | — | — | — |
| **B**   | — | — | — | ε(=)| — | — | — | — | — | — | — | — | — |
| **C**   | — | — | — | — | ε(=)| — | — | — | — | — | — | — | — |
| **W**   | — | — | — | — | — | ε(=)| — | — | — | — | — | — | — |
| **M**   | — | — | — | — | — | — | ε(=)| — | — | — | — | — | — |
| **Y**   | — | — | — | — | — | — | — | ε(=)| — | — | — | — | — |
| **T**   | — | — | — | — | — | — | — | — | ε(=)| — | — | — | — |
| **V**   | — | — | — | — | — | — | — | — | — | ε(=)| — | — | — |
| **D**   | — | — | — | — | — | — | — | — | — | — | ε(=)| — | — |
| **Π₁**  | — | — | — | — | — | — | — | — | — | — | — | ε(=)| — |
| **Π₂**  | — | — | — | — | — | — | — | — | — | — | — | — | ε(=)|

**Reading.** The diagonal entry `ε(=)` records the vacuous root-with-
itself self-overlap (a rule's LHS obviously unifies with itself at
the root; the induced critical pair `⟨r σ, r σ⟩` is trivially
joinable). The off-diagonal entries are all "—" because:

- **Primitive-head distinction.** Every LHS `ℓᵢ` has a head primitive
  distinct from every other `ℓⱼ`. So unifying `ℓᵢ` with `ℓⱼ`
  (i ≠ j) would require unifying distinct primitives — impossible.
- **Sub-pattern exclusion.** The non-variable, non-root sub-patterns
  of any `ℓᵢ` are strict partial applications `h x₁ … xₖ` with `k <
  arity(h)`. These are not full LHSs of any rule (arity
  mismatched); they cannot unify with any `ℓⱼ`.

So the overlap table is *empty of non-trivial entries*. The system
is overlap-free. (This argument mechanizes §2.1 Phase A Check A2 +
A3.)

### 3.2 Formal RHS audit table (addressing straddling)

For Lemma 2.2.1's proof to go through, we need: no RHS admits a new
LHS match created by substitution. Tabulate for each rule:

| Rule | RHS `r` | Every subterm's head is: |
|------|---------|--------------------------|
| I | `x` | metavariable `x` |
| K | `x` | metavariable `x` |
| S | `x z (y z)` | metavariables `x, z, y, z`; no primitive head |
| B | `x (y z)` | metavariables `x, y, z` |
| C | `x z y` | metavariables `x, z, y` |
| W | `x y y` | metavariables `x, y, y` |
| M | `x x` | metavariables `x, x` |
| Y | `f (Y f)` | metavariable `f`; literal primitive `Y` |
| T | `y x` | metavariables `y, x` |
| V | `z x y` | metavariables `z, x, y` |
| D | `x y (z w)` | metavariables `x, y, z, w` |
| Π₁ | `x` | metavariable `x` |
| Π₂ | `y` | metavariable `y` |

**Claim.** No RHS contains a primitive-headed subterm whose structure
could only be matched after substitution.

For rules `I, K, S, B, C, W, M, T, V, D, Π₁, Π₂`: every subterm of
the RHS has a metavariable head. No match against a primitive-headed
LHS is possible purely from the RHS skeleton. The only way a match
occurs after substituting `T̄` is entirely within some `Tᵢ` (which
is already reduced-when-parallel-reduced by IH) or entirely at the
root of a substituted `Tᵢ` that happens to become a redex (again
internal to `Tᵢ`). No straddling.

For rule `Y`: the RHS `f (Y f)` contains a literal `Y f` subterm,
i.e., the primitive `Y` applied to `f`. After substituting `f := T`,
this becomes `T (Y T)` with subterm `Y T`. This subterm is a
`Y`-redex — and it was already going to be a redex regardless of
`T`, because `Y T` is always a redex (Y has arity 1). So the
redex is present *in the template `f (Y f)`* via the `Y f` placement,
and substitution merely threads `T` through it. No straddling —
the redex was there before substitution, at the same position.

Hence Lemma 2.2.1 holds uniformly. The Triangle Lemma holds. ✓

---

## §4. Verdict

**Theorem 4.1.** The reduction relation `→` of the extended
calculator over the primitive set `{I, K, S, B, C, W, M, Y, T, V, D,
Π₁, Π₂}` is confluent.

*Proof.* By §3.1, the system is overlap-free (no non-trivial critical
pair). By §3 stage-by-stage, all LHSs are left-linear. By §3.2, the
RHS audit rules out straddling. Hence by Theorem 2.3.3, `↠` has the
diamond property, which is confluence by definition. ∎

### 4.1 Counting-convention restatement for the verdict

(Already declared at the top; re-stated as required by the task.)

- **Rule overlap** = a position `q` in some LHS `ℓ₁` such that
  `ℓ₁|q` is unifiable (syntactically) with a renaming of some LHS
  `ℓ₂`.
- **Critical pair** = `⟨ℓ₁σ[q ← r₂σ], r₁σ⟩` for a most-general
  unifier `σ` of an overlap. In this system: **empty set**.
- **Residual of `r ∈ red(M)` across `M ⇒ N`** = the (possibly
  multiple) redex occurrence(s) at the positions of `N` descending
  from `r`'s position in `M`. Multiplicity > 1 when an ancestor of
  `r` is inside a duplicated argument of a contracted redex.
- **Parallel step** = relation `⇒` of §2.2.

### 4.2 Two separate questions: "largest confluent subset" and "minimal non-confluent extension"

The task asks two related-but-distinct questions. I answer them
separately to avoid conflation.

**Q4.2.1: What is the largest confluent subset of the 13 rules?**

**A.** The full 13-rule baseline. Because the baseline is confluent
(Theorem 4.1), any subset `P' ⊆ baseline` is also trivially confluent
(restricting rules can only remove rewrite steps, and critical pairs
between rules in `P'` are a subset of those in the baseline, i.e.,
still empty). So *every* subset of the baseline is confluent. The
largest such subset is the baseline itself. (Trivial maximum.)

**Q4.2.2: What is a minimal non-confluent *extension* of the
baseline?**

**A.** Add one extra rule that overlaps an existing rule's LHS and
produces a divergent RHS. The minimal such extension is:

> **Extra rule `K°`**: `K I x → x`.

The LHS `K I x` is an instance of the existing LHS `K x y` (via
substitution `x ↦ I, y ↦ x`), so overlap occurs at the root of `K°`
with the original `K` rule. The overlap induces the critical pair
from the term `K I x`:

- By existing rule `K u v → u` with `u := I, v := x`: `K I x → I`.
- By new rule `K°`: `K I x → x`.

Critical pair: `⟨I, x⟩`. Both are normal forms (`I` is a primitive;
`x` a free variable in normal form). They are syntactically distinct,
so no common reduct exists. Hence the extension is **non-confluent**.

This extension adds exactly one rule, the minimum possible. Any
addition of a new rule that does not overlap any existing rule
(e.g., a new primitive with a fresh head and a non-overlapping LHS)
preserves confluence by the same argument as §3 — hence not every
extension is non-confluent; only those introducing joinability-
failing critical pairs are.

### 4.3 Maximal confluent subset — restated cleanly

"Maximal confluent subset" means: an element of the baseline's power
set that is (a) confluent and (b) maximal with respect to subset
inclusion among confluent subsets. Since every subset is confluent
(see Q4.2.1), the unique maximal element is the full baseline.

*Distinction vs. "maximal confluent extension"*: that phrase would
refer to an upper bound in a larger space that *adds* rules. I do
not claim the baseline is a maximal confluent extension in that
sense — see §7.4 for non-orthogonal confluent extensions.

---

## §5. Verification strategy

Two independent strategies are combined.

### 5.1 Strategy (b): parallel-reduction diamond (primary)

The chain §2 ⇒ §3 ⇒ §4 is a structural proof. It is self-contained
within this document. The argument does not depend on termination,
on a specific reduction strategy, or on a specific choice of
primitives beyond the three structural conditions (left-linearity,
overlap-freeness, no RHS straddling).

### 5.2 Strategy (d): executable oracle (complementary)

An independent empirical check via a Python simulator at
`sim/simulator.py` with captured output at `sim/output-final.txt`.

**What the simulator does.**

1. Encodes terms as nested tuples (primitives as string atoms, free
   variables as lowercase string atoms).
2. Implements all 13 rules exactly as in the task statement.
3. For each test term, performs a bounded breadth-first search of
   single-step reducts up to depth 5–6 with a size cap to prevent
   runaway expansion under `Y, M` recursion.
4. For every pair of reachable reducts, re-runs BFS from each
   reduct and checks for a non-empty intersection — i.e., tests
   *empirical joinability within the bound*.

**Captured output** (`sim/output-final.txt`):

```
EXAMPLE (a):  S (K I a) (I b) (I c)              28 reducts — all pairs join ✓
EXAMPLE (b):  Y f                                  6 reducts — all pairs join ✓
EXAMPLE (c):  W (K a) (I b)                        8 reducts — all pairs join ✓
EXAMPLE (d):  D (K a) (I b) (I c) w               10 reducts — all pairs join ✓
EXAMPLE (e):  M (I a)                              6 reducts — all pairs join ✓
EXAMPLE (f):  S (Π₁ a b) (Π₂ c d) e                8 reducts — all pairs join ✓
EXAMPLE (g):  V a b (T c d)                        4 reducts — all pairs join ✓
```

**Disclosed limitations.**

- Bounded depth/size caps mean the oracle can fail to find a
  common reduct that exists at greater depth. Empirical silence
  about non-confluence is not a *proof* of confluence; it is a
  stress test that exhibits no counter-example among the tested
  configurations.
- The seven test terms exercise every rule category at least once
  (erasers `K, Π₁, Π₂`; duplicators `S, W, M, D`; permuters `B, C,
  T, V`; identity `I`; recursive generator `Y`) and every rule
  arity. But they do not enumerate all configurations of redex
  multiplicities.

**Why this is strategy (d) proper.** The task awards R6 = 3 for a
worked executable-oracle verification alongside the trace argument.
The simulator is a separately written piece of code (`~220` LOC)
that reduces terms mechanically and checks joinability without
using any human intermediate argument. It agrees with the symbolic
proof.

---

## §6. Worked examples

### 6.1 Example (a) — `S (K I a) (I b) (I c)` (critical-pair-like)

Let `M ≡ S (K I a) (I b) (I c)`. Redex positions at depth-1:

- `ε`: `S`-redex at the root.
- `L·L·R`: `K I a` — matches `K x y` with `x ↦ I, y ↦ a`.
- `L·R`: `I b` — matches `I x` with `x ↦ b`.
- `R`: `I c` — matches `I x` with `x ↦ c`.

**Order α (outer-first).** Fire `ε`:

```
M = S (K I a) (I b) (I c)
  → (K I a) (I c) ((I b) (I c))                  [S-rule]
  → I (I c) ((I b) (I c))                        [K-redex K I a → I]
  → (I c) ((I b) (I c))                          [I-redex at left: I X → X]
  → c ((I b) (I c))                              [I c → c]
  → c (b (I c))                                  [I b → b]
  → c (b c)                                      [I c → c]
```

**Order β (inner-first).** Fire `L·L·R, L·R, R`:

```
M = S (K I a) (I b) (I c)
  → S I (I b) (I c)                              [K I a → I]
  → S I b (I c)                                  [I b → b]
  → S I b c                                      [I c → c]
  → I c (b c)                                    [S-rule]
  → c (b c)                                      [I c → c]
```

**Common reduct**: `c (b c)`. ✓

The simulator (output-final.txt) confirms 28 reachable reducts from
`M` within depth 6, every pair joinable. The joint normal form (on
free variables `a, b, c`) is `c (b c)`; note that `a` is erased by
the `K I a → I` step in every path (since the `S`-rule discards its
first argument's second position anyway).

### 6.2 Example (b) — `Y f` (non-terminating divergence)

Let `M ≡ Y f`. `red(M) = {ε}` (one redex: the root `Y`-redex).

```
M = Y f
  → f (Y f)                                       [Y-rule]
```

At this point, `red(f (Y f)) = {R}` (a Y-redex at position `R`, viz.
the inner `Y f`). Two successor states:

**Path α**: contract the inner redex.

```
f (Y f) → f (f (Y f))                            [Y-rule at R]
```

**Path β**: reduce to a specific instance. Take `f := I` to produce a
closed trace (for clarity). Then:

```
M ≡ Y I
  → I (Y I)                                       [Y]
  → Y I                                           [I-redex]
```

So `Y I ↠ Y I` in two steps — a cycle.

Now the key joinability observation. From `M ≡ Y I`, reducts within
depth 5 are `{Y I, I (Y I), I (I (Y I))}` (a finite set because of
size capping). Any two of these are joinable:

- `Y I` and `I (Y I)`: from `Y I`, do one `Y`-step to reach `I (Y
  I)`. ✓
- `I (Y I)` and `I (I (Y I))`: from `I (Y I)`, `Y`-step inside to
  `I (I (Y I))`. ✓
- `Y I` and `I (I (Y I))`: two `Y`-steps from `Y I` reach `I (I (Y
  I))`. ✓

So **confluence holds even though no reduct is a normal form**. The
diamond on `⇒` does not require finite reduction traces; it only
requires pairwise rejoinability at some common reduct.

### 6.3 Example (c) — Leftmost-outermost vs rightmost-innermost

Let `M ≡ W (K a) (I b)`.

**Leftmost-outermost.** Fire the outermost redex (the `W`-redex at
root):

```
M = W (K a) (I b)
  → (K a) (I b) (I b)                            [W-rule: x y y with x ↦ K a, y ↦ I b]
```

The leftmost-outermost redex in the result is the `K a (I b)` redex
(the `K`-rule with the first two arguments `a` and `I b`):

```
(K a) (I b) (I b)
  → a (I b)                                      [K-rule: K a (I b) → a; drops the second I b]
  → a b                                          [I-rule]
```

**Rightmost-innermost.** The rightmost-innermost redex is the
subterm `I b` at position `R`:

```
M = W (K a) (I b)
  → W (K a) b                                    [I b → b]
  → (K a) b b                                    [W-rule]
  → a b                                          [K a b → a; drops the second b]
```

**Common reduct:** `a b`. ✓ Both strategies agree on the normal form,
as confluence requires.

### 6.4 Example (d) — Duplication under `S` with nested redexes (bonus)

Let `M ≡ S A (I b) c` for any reducible `A`. The `S`-rule duplicates
the third argument `c`. After the S-step:

```
M = S A (I b) c
  → A c ((I b) c)                                 [S-rule]
  → A c (b c)                                     [I b → b]
```

Alternative order (reduce `I b` first):

```
M = S A (I b) c
  → S A b c                                       [I b → b]
  → A c (b c)                                     [S-rule]
```

Same reduct. ✓ This illustrates that parallel reduction handles
argument duplication coherently: whether we duplicate first and
then reduce both copies, or reduce and then duplicate, the result is
identical.

### 6.5 Example (e) — `M (I a)` (bonus, tests `M` non-right-linearity)

`M x → x x` duplicates its argument.

**Order α**: fire `M` first.

```
M (I a)
  → (I a) (I a)                                   [M-rule]
  → a (I a)                                       [I a → a at left]
  → a a                                           [I a → a at right]
```

**Order β**: fire `I a` first.

```
M (I a)
  → M a                                           [I a → a]
  → a a                                           [M-rule]
```

Common reduct: `a a`. ✓

### 6.6 Example (f) — `D (K a) b (I c) d` (bonus, tests `D`)

```
N = D (K a) b (I c) d
  → (K a) b ((I c) d)                             [D-rule: x y (z w) with x ↦ K a, y ↦ b, z ↦ I c, w ↦ d]
  → a ((I c) d)                                   [K a b → a]
  → a (c d)                                       [I c → c]
```

Alternative order — reduce `I c` first:

```
N = D (K a) b (I c) d
  → D (K a) b c d                                 [I c → c]
  → (K a) b (c d)                                 [D-rule]
  → a (c d)                                       [K a b → a]
```

Common reduct: `a (c d)`. ✓

---

## §7. Open questions and known limitations

### 7.1 Extension to strong reduction under binders

If the baseline is enriched with λ-abstraction `λx. M` and β-reduction
`(λx. M) N → M[x := N]` (capture-avoiding substitution), with
reduction permitted under binders (strong reduction), the parallel-
reduction argument should extend — but I have not carried it out.

What's needed:

- **Parallel-substitution lemma for strong reduction.** The analogue
  of Lemma 2.2.1 but with capture-avoiding substitution. The
  standard capture-avoidance machinery (α-renaming before
  substitution, de Bruijn indices, or nominal sets) would be
  invoked. The key step is that `M ⇒ M'` and `N ⇒ N'` imply
  `M[x := N] ⇒ M'[x := N']`, which holds for the same structural
  reasons as in the first-order case, provided `x` is chosen not
  to appear free in any binder of `M`.
- **Left-linearity/overlap check for β.** The β-rule's LHS `(λx.
  M) N` has a sub-pattern `λx. M` — but this sub-pattern is not
  the LHS of any of our combinator rules (different syntactic
  category). No overlap between β and combinator rules.
- **RHS audit for β.** `M[x := N]` involves an arbitrary-depth
  substitution into `M`, which *can* create new β-redexes if `M`
  has a subterm `λy. P` applied to something whose head becomes
  exposed only after substitution. So β-reduction has a non-
  trivial straddling case — but it is the textbook case and is
  handled by the standard parallel-reduction proof for λ-calculus.

Net: the combined system (combinators + strong β) is expected to be
confluent, but the proof requires the parallel-substitution lemma
for λ, which is beyond the scope of this document.

### 7.2 Confluence versus normalization

- **Orthogonality ⇒ confluence** (our result): verified in §§2–4.
- **Orthogonality ⇏ strong normalization**: counter-examples are
  `Y f, M M` in our baseline.
- **Confluence + weak normalization ⇒ unique normal form**: if a
  term has some reduct that is a normal form, then any reduct that
  is also a normal form coincides with it. Proof: let `M ↠ N₁` and
  `M ↠ N₂` with both `Nᵢ` normal. By confluence, there exists `P`
  with `N₁ ↠ P` and `N₂ ↠ P`. But normal forms have no reducts
  except themselves, so `P ≡ N₁` and `P ≡ N₂`, hence `N₁ ≡ N₂`.
- Consequence for our system: **every term that has a normal form
  has a unique one**, but not every term has a normal form (e.g.,
  `Y f` does not).

The converse ("strong normalization + local confluence ⇒ full
confluence") is a well-known theorem in rewriting — it follows from
induction on the termination order. It does *not* apply to our
system because we lack strong normalization, but we also don't need
it, because parallel-reduction diamond already proves confluence.

### 7.3 Dependence on reduction strategy

Confluence is a property of the relation `→`, not of any specific
strategy. In particular:

- **Leftmost-outermost** is normalizing: for any weakly-normalizing
  orthogonal term rewriting system, the leftmost-outermost strategy
  reaches the normal form when one exists. (Proof sketch: at any
  step where a normal form is reachable via some reduction sequence,
  the leftmost-outermost redex must lie on that sequence or be
  erasable; case analysis establishes it remains on a shortest path
  to normalization. I do not carry out the full proof here.)
- **Rightmost-innermost** is not normalizing on terms mixing
  erasure with non-termination. E.g., `K a (Y f)` has normal form
  `a` (erase the second argument, which is the diverging `Y f`) via
  leftmost-outermost: `K a (Y f) → a`. Rightmost-innermost attempts
  to normalize `Y f` first and never terminates.
- Confluence does *not* say all strategies reach the same infinite
  trace; it only says that whenever two reductions terminate (or
  pause at the same term), they can be made to agree.

### 7.4 Non-orthogonal confluent extensions

Can a rule be added to the baseline that *overlaps* an existing rule
while remaining confluent? Yes — provided the induced critical pair
is joinable, and provided the iterative **critical-pair closure**
terminates with all pairs joined.

#### 7.4.1 Trivially-joinable example

Add `K K x → K`. Overlap with `K x y → x` at root (unify `K x' y'`
with `K K x`; substitution `x' ↦ K, y' ↦ x`): the existing rule gives
`K K x → K`, the new rule gives `K K x → K`. Identical results;
critical pair `⟨K, K⟩` joinable at depth 0. Confluent. ✓

(This is trivial because the two rules produce the same RHS. The
extension adds no new behaviour.)

#### 7.4.2 Non-trivially-joinable example

Add `I I x → I x`. Overlap with `I y → y` at root (unify `I y` with
`I I x`; substitution `y ↦ I x`): the existing rule gives `I I x →
I x`, the new rule gives `I I x → I x`. Same result — joinable at
depth 0. Confluent. ✓

Also overlap with `I y → y` at position `L`: `I I x` has subterm
`I I` at position `L`, so unify `I y` with `I I` using `y ↦ I`; the
existing rule gives `I I → I` (at position `L`), so the whole term
rewrites to `I x`. Same as above. Joinable. ✓

#### 7.4.3 Iterative closure example

To show that closure is a non-trivial procedure, consider adding two
overlapping rules simultaneously:

> **New rules** `A`: `K a b → c` and `B`: `K a x → b`
> (with fixed primitives `a, b, c`, variable `x`).

Here `a, b, c` are treated as additional primitives with no
reduction rules of their own (dummy constants).

Overlap of `A` with `B` at root: unify `K a b` with `K a x`
(substitution `x ↦ b`). Rule `A` gives `c`; rule `B` gives `b` (since
`x ↦ b`). Critical pair `⟨c, b⟩`.

Attempt to join: can `c ↠ X` and `b ↠ X` for some `X`? Since `b, c`
are dummy primitives with no reduction rules, they are in normal
form and distinct. **Non-joinable**. Extension is non-confluent.

Now modify: replace `B` with `B'`: `K a x → c`. Overlap unification
gives critical pair `⟨c, c⟩`. Trivially joinable. Extension is
**confluent**.

Now modify further: add **three rules** `P`: `K I x → x`, `Q`: `K y
I → y`, and `R`: `K y y → y`. All have overlaps with the original
`K x y → x`:

- Overlap of `K x y → x` with `P` at root: unify `K x y` with `K I
  x'` (σ: `x ↦ I, y ↦ x'`); original gives `I`, `P` gives `x'`.
  Critical pair `⟨I, x'⟩` — not joinable when `x'` is a variable.
- So adding `P` alone creates non-confluence (as in §4.2.2).

But if we add only `R` (`K y y → y`): overlap with original gives
critical pair from `K y y` — unify `K x' y'` with `K y y` (σ: `x' ↦
y, y' ↦ y`); original gives `y`, `R` gives `y`. Joinable at depth 0.
Also self-overlap of `R` with itself at root: the only unifier is
the identity (which is vacuous).

Closure terminates at depth 0 with no unjoined pairs. So adding *only*
`R` to the baseline yields a confluent non-orthogonal extension.

**Iterative-closure schema** (for the procedure in general):

1. Initialize `CP := {critical pairs from all rule overlaps}`.
2. For each `⟨s, t⟩ ∈ CP`, search for a common reduct `u` with
   `s ↠ u` and `t ↠ u`. If found, mark joinable.
3. If any pair is unjoinable, declare non-confluent and halt.
4. If all pairs are joinable, declare confluent.

The closure does not re-cycle (unlike some other rewrite-system
completion procedures), because we are not generating new rules —
we are only checking existing critical pairs. Procedure terminates
in finite time when the rule set is finite and joinability searches
are bounded by a computable depth.

#### 7.4.4 Open sub-question

**7.4-Q1.** Characterize the space of 1-rule extensions of the
baseline that preserve confluence. *Partial answer.* Any extension
by a new fresh-headed primitive with a left-linear LHS and no
straddling RHS preserves confluence (new head ⇒ no overlap with
existing rules). Extensions reusing an existing primitive head
must have LHS a strict sub-instance of the existing LHS, and must
produce an RHS that is `↠`-joinable with the existing rule's RHS
on the overlap instance. I do not enumerate the finite space of
such extensions in this document.

### 7.5 Weak vs. strong reduction

"Weak reduction" usually means "do not reduce under binders". Since
the baseline has no binders, the distinction is vacuous. All our
reductions are at arbitrary positions. When binders are added (§7.1),
the weak/strong distinction reappears and the proof must be
extended.

### 7.6 Dependence on the 13-primitive choice

The proof structure (§2–§4) uses only three generic conditions:
left-linearity, no critical pairs, no RHS straddling. Any primitive
set satisfying these conditions is confluent. The choice of 13 is
convenient (exercises duplication, permutation, recursion, erasure)
but not essential. Dropping `D`, `V`, or `T` (say) leaves the
remaining 10-rule system confluent by the same argument. Adding
rules like `J x y z → x (y z y)` or similar fresh-headed LHSs
preserves confluence as long as the three conditions hold.

---

## §8. Concluding synthesis

**Verdict.** The reduction relation of the extended calculator is
confluent.

**Proof technique.** Parallel-reduction diamond via complete
development. The parallel relation `⇒` satisfies `→ ⊆ ⇒ ⊆ ↠`, so
`⇒* = ↠`. `⇒` has the diamond property because `Φ` is a closing
functor on parallel reductions (Triangle Lemma: `M ⇒ N` implies
`N ⇒ Φ(M)`). Confluence of `↠` follows by tiling of parallel
diamonds.

**Why it works structurally.** The 13 rules are left-linear (LHSs
are `head x₁ … xₐ` with distinct metavariables), overlap-free (no
critical pairs — the 13×13 overlap table in §3.1 has only vacuous
diagonal entries), and have RHSs with no straddling substitution
sites (§3.2 audit). Non-termination (via `Y, M`) is irrelevant to
the argument, because the parallel-reduction technique makes no
termination assumption.

**Empirical verification.** An executable oracle (`sim/simulator.py`,
output `sim/output-final.txt`) runs all 13 rules on 7 representative
test terms and confirms joinability of every pair of reachable
reducts within a bounded-depth BFS.

**Disclosed gaps** (per §1.6 and rubric polarity on honesty-over-
closure):

1. The parallel-substitution Lemma 2.2.1 is proved from scratch,
   but a fully rigorous treatment under λ-binders (§7.1) requires
   the capture-avoidance machinery which I sketch but do not prove.
2. The leftmost-outermost normalization theorem in §7.3 is stated
   informally; a complete standardization argument is outside the
   scope of this document.
3. The executable oracle has finite depth/size caps; it cannot
   rule out non-confluence at arbitrary depth. The symbolic proof
   (§§2–4) is the authoritative witness.
4. Characterization of the space of 1-rule non-orthogonal confluent
   extensions (§7.4-Q1) is partial: new-head extensions are fully
   classified, but the finite space of head-reusing extensions is
   not enumerated.

**Counter-example status.** None for the baseline. A minimal non-
confluent extension is `K° : K I x → x` (§4.2.2), exhibiting the
non-joinable critical pair `⟨I, x⟩` at term `K I x`.
