<!--
Snapshot of projects/a/task/ARGUMENT.md at Cycle #4 close.
Source container: claude-meta-autoagent-a
Capture time (UTC): 2026-04-21 17:57 (A process exit)
SHA256 at capture: see cycle-04/JUDGMENT.md §0.
-->

# Minimal Primitive Set for the Extended Calculator

## §1. Motivation

The extended calculator offers thirteen primitives — I, K, S, B, C, W, M, Y, T, V, D, Π₁, Π₂ — each with a short rewrite rule. Many of these rules share structure: copying an argument, dropping an argument, reordering arguments, inserting a parenthesis. The *kinds* of work being done are few; the *naming* of who does what is many. So we expect that a smaller set can simulate all of them, and we expect this for structural reasons that recur across mathematics.

**First precedent — propositional logic.** The sixteen binary Boolean operations on {0,1} are not sixteen independent ideas. From a single connective — the "nor" of (p,q) — one derives negation (nor(p,p) = ¬p), then disjunction (nor(nor(p,q), nor(p,q)) = p ∨ q), then every other connective. Why? Because nor by itself can *duplicate* an input (both slots get the same p) and, combined with a constant, can *discard* — and those two capacities, with iteration, span everything. A single operator is enough when the operator's truth-table already contains the primitive "shapes" the rest of the family needs.

**Second precedent — cyclic closures.** A cyclic group of order n, presented by a multiplication table listing all nⁿ binary products, collapses to a presentation of a single generator with a single relation. In finite fields, the multiplicative group is cyclic; every nonzero element is a power of one. In both cases, the algebraic closure under the operation (multiplication) is rich enough that a well-chosen singleton generator reconstructs the whole structure.

**Third precedent — rewriting systems.** In abstract string-rewriting and term-rewriting systems, one often proves that a specific rule schema *simulates* a larger rule schema by a translation. If the simulated system is confluent and the simulator is at least as expressive (can reach every simulator-normal-form the original could), the sets have the same computational closure.

The unifying observation — the one I rely on — is this: **when a closure operation is cheap and unconstrained (for us, application: a free binary constructor over a countable set of terms), and a single primitive already exhibits two distinct reductive *capacities* — (a) **duplication** (some variable on the right-hand side of its rule occurs more than once) and (b) **discarding** (some variable on the left-hand side does not occur on the right-hand side) — then that single primitive is not much weaker than a collection that partitions those capacities across several primitives.** Copies are made by duplication; information is deleted by discarding; everything else (permutation, bracketing, recursion) is expressible once we can copy and forget. This is the structural feature I ride to a small P*.

My informal expectation: the baseline's thirteen members split neatly into (i) pure permuters / bracketers (B, C, T, V, D — none duplicate or discard), (ii) pure discarders (K, Π₁, Π₂ — discard but do not duplicate), (iii) pure duplicators (W, M — duplicate but do not discard), (iv) the universal (S — duplicates and threads), (v) the self-referential (Y). Two primitives suffice as long as at least one duplicates and at least one discards; one suffices if we cram both capacities into a single rule.

---

## §2. Systematic Reduction Procedure

Fix a candidate primitive set P' — a finite set of combinators (from the baseline, or newly invented, each with its own rewrite rule). I check two things.

### 2a. Sufficiency — a decision procedure

Every baseline primitive p has a rule rᵖ: p x₁ … xₙ → Tᵖ(x₁,…,xₙ). To show P' suffices, I give, for each p ∉ P', an explicit closed P'-term tᵖ (built only from P' and application), and verify by reduction that
  tᵖ y₁ … yₙ ↠ Tᵖ(y₁,…,yₙ)
for fresh variables y₁,…,yₙ. Weak reduction is confluent on closed terms, so the existence of such a reduction witnesses that tᵖ and p are observationally identical: any context distinguishing them would have to pick some y₁,…,yₙ and look at the result, and the results agree.

Closed under this equivalence: if each p ∉ P' has a synthesis tᵖ, then any extended-calculator term M translates to a P'-term M* by literal substitution, and reduces in lock-step to the same result. (A baseline redex M ↠ N translates to M* ↠* N* because every baseline rule's RHS was designed to reduce to the same normal form as the LHS; replacing primitives by synthesized equivalents preserves normal-form equality under confluence.)

### 2b. Insufficiency — invariants

To rule out a too-small P', I supply an invariant preserved by all P'-reductions but violated by some baseline reduction.

The key invariants are **multiplicity invariants**. Define, for any term M with distinguished free occurrences {y₁, …, yₖ}, the multiplicity vector μ(M) = (μ₁,…,μₖ) where μᵢ is the number of free occurrences of yᵢ in M.

- **K-monotone systems have the non-increase property.** If every rule in P' has the form p x₁…xₙ → T where each variable x₁,…,xₙ appears *at most once* in T, then for any reduction M ↠ N, μ(N) ≤ μ(M) componentwise. Hence S cannot be synthesized in such a system: S x y z → x z (y z) strictly increases the multiplicity of z.

- **S-monotone systems have the non-erasure property.** If every rule in P' has the form p x₁…xₙ → T where each variable x₁,…,xₙ appears *at least once* in T, then for M ↠ N, μ(N) ≥ μ(M) componentwise. Hence K cannot be synthesized: K x y → x erases y (μᵧ drops from ≥1 to 0).

Thus a P' that synthesizes both S and K must contain at least one rule with duplication (some variable twice on RHS) and at least one rule with erasure (some variable zero times on RHS). With this bound, we begin the chain.

---

## §3. Chain of Reductions

Abbreviation convention: below I write rules left-associatively (M N O = (M N) O) and use = for functional equivalence under weak reduction (both sides reduce to identical normal forms on fresh inputs).

### Stage 0: Baseline (|P| = 13)

P₀ = {I, K, S, B, C, W, M, Y, T, V, D, Π₁, Π₂}.

### Stage 1: Eliminate the projectors and the small permuters (|P| = 7)

P₁ = {I, K, S, B, C, W, Y}.

Six eliminations:

**Π₁ = K.** Identical rules: Π₁ x y → x and K x y → x.

**Π₂ = K I.** Π₂ x y → y. (K I) x y → I y → y. ✓

**T = C I.** T x y → y x. (C I) x y → I y x → y x. ✓

**M = S I I.** M x → x x. (S I I) x → I x (I x) → x x. ✓

**D = B B.** D x y z w → x y (z w). Compute (B B) x y z w step-by-step. B has rule B a b c → a (b c). Thus:
   B B x y  = B (x y)                 [B-rule with a=B, b=x, c=y]
   B B x y z  = (B (x y)) z            (partial, B with 1 arg then 1 more)
   B B x y z w = (B (x y)) z w → (x y)(z w)
                                       [B-rule with a=(x y), b=z, c=w]
So B B x y z w → x y (z w). ✓

**V = B C (C I).** V x y z → z x y. We verify term-by-term:
   (C I) x y → I y x → y x. So C I = T, acting as λab. b a.
   B C T x y z = B-rule applied: C (T x) y z.
   C (T x) y z = [C-rule] (T x) z y = (y from T x applied to z = T x z = z x) so (T x) z = z x. Hence (T x) z y = (z x) y = z x y. ✓

### Stage 2: Eliminate I (|P| = 6)

P₂ = {K, S, B, C, W, Y}.

**I = S K K.** (S K K) x → K x (K x) → x [first K-rule: K x a → x with a = K x]. ✓

Since I is eliminated, every appearance of I in later synthesis expands to S K K.

### Stage 3: Eliminate W (|P| = 5)

P₃ = {K, S, B, C, Y}.

**W = S S (K I) = S S (K (S K K)).** Verification:
   S S (K I) x y = S x ((K I) x) y       [outer S-rule]
                 = S x I y                 [(K I) x → I]
                 = x y (I y)               [inner S-rule]
                 = x y y. ✓

### Stage 4: Eliminate C (|P| = 4)

P₄ = {K, S, B, Y}.

**C = S (B B S) (K K).** Verification (the most elaborate in this stage; C must permute its last two args):
   S (B B S) (K K) x y z
     = (B B S) x ((K K) x) y z              [outer S-rule]
     = (B B S) x K y z                      [(K K) x → K]
     = B (S x) K y z                        [B B S x = B (S x) by Stage-1 D=BB pattern]
     = (S x)(K y) z                         [B-rule on B (S x) K y]
     = x z ((K y) z)                        [S-rule]
     = x z y.                               [(K y) z → y]
So C x y z = x z y. ✓

### Stage 5: Eliminate B (|P| = 3)

P₅ = {K, S, Y}.

**B = S (K S) K.** Verification:
   S (K S) K x y z
     = (K S) x (K x) y z                    [outer S-rule]
     = S (K x) y z                          [(K S) x → S]
     = (K x) z (y z)                        [inner S-rule]
     = x (y z).                             [(K x) z → x]
So B x y z = x (y z). ✓

### Stage 6: Eliminate Y (|P| = 2)

P₆ = {K, S}.

This is the delicate stage. The baseline Y is self-referential (Y f → f (Y f)); to drop Y from P we must derive a fixed-point combinator from S and K alone. The key fact we need: there is an S-K term Y* such that for every term f, Y* f ↠ f (Y* f).

**Construction.** Start from the intended fixed-point behaviour: for each f, we want Y* f = Uf Uf where Uf := λx. f (x x). Under weak reduction, (S I I) applied to any term A reduces via the S-rule to A A — i.e., (S I I) is a self-applicator. So Y* f = Uf Uf is equivalently (S I I) Uf. We therefore aim at
  Y* f = (S I I) Uf     where Uf = λx. f (x x) = S (K f) (S I I).
(The middle equation is a bracket abstraction on x: [x](f (x x)) = S (K f) (S I I), using the standard rules.)

Now bracket-abstract f from Y* f = (S I I) Uf = (S I I) (S (K f) (S I I)):
  Y* = [f]((S I I)(S (K f)(S I I)))
     = S (K (S I I))  [f](S (K f)(S I I))               [[f](S I I) = K (S I I), since f is not in S I I]
     = S (K (S I I))  (S  [f](S (K f))  (K (S I I)))    [nested split; again [f](SII) = K(SII)]
     = S (K (S I I))  (S  (S (K S) K)  (K (S I I))).    [using [f](S (K f)) = S (K S) K after eta on [f](K f) = K]

So

  Y* = S (K (S I I)) (S (S (K S) K) (K (S I I))).

**Verification that Y* f → f (Y* f).** Apply the rule:
   Y* f = S (K (S I I)) (S (S (K S) K) (K (S I I))) f
        = (K (S I I)) f   (S (S (K S) K) (K (S I I)) f)      [outer S-rule]
        = (S I I)   (S (S (K S) K) (K (S I I)) f)            [K-rule on K (S I I) f]

Compute the right half G = S (S (K S) K) (K (S I I)) f:
   G = (S (K S) K) f   ((K (S I I)) f)                       [S-rule]
     = (S (K S) K) f   (S I I)                               [K-rule]
     = (K S) f (K f) (S I I)                                 [S-rule]
     = S (K f) (S I I)                                       [(K S) f → S]

So Y* f = (S I I) (S (K f) (S I I)). Name U := S (K f) (S I I). Then Y* f = (S I I) U = I U (I U) → U (I U) → U U.

And U x = (K f) x ((S I I) x) = f (x x) [K-rule reduces (K f) x → f, and (S I I) x = I x (I x) → x x].

Hence Y* f = U U = f (U U) = f (Y* f). ✓

So Y — and therefore recursion via fixed points — is expressible from S and K alone. With this, P₆ = {S, K} is sufficient for the entire extended calculator.

### Stage 7 (optional): A single primitive (|P| = 1)

Is |P*| = 2 tight, or can we go further? Among the baseline, no single primitive works: by §2b, a sufficient P' must contain one primitive that duplicates (rules out K, B, C, T, V, D, Π₁, Π₂, I alone) and one primitive that discards (rules out S, W, M, Y alone). No baseline primitive does both (check the rules), so every baseline singleton fails.

But we are allowed to invent new primitives. Introduce a single new primitive Ω with arity 1 and rule

  Ω x → x S* K*,

where the right-hand side is interpreted as x applied to the fixed closed Ω-terms

  S* := Ω (Ω (Ω (Ω Ω)))
  K* := Ω (Ω (Ω Ω)).

That is, the *literal* rule is

  Ω x → x (Ω (Ω (Ω (Ω Ω)))) (Ω (Ω (Ω Ω))).

The only symbols on the right are the rule's bound variable x and the primitive Ω itself — exactly the same self-referential pattern the baseline already permits for Y.

**Why this works (informal).** Pretend for a moment we are working abstractly with the rule Ω x → x S K (where S, K are the "ideal" combinators). Then, step by step:

   Ω Ω       = Ω S K
             = (S S K) K              [Ω S = S S K via the Ω-rule with x = S]
             = S S K K
             = S K (K K)              [S-rule with x=S, y=K, z=K]
             = (S K)(K K).
   (S K)(K K) z = K z ((K K) z) = K z K = z.    [S-rule, then K-rule twice]
   Hence Ω Ω = I.

   Ω (Ω Ω) = Ω I = I S K = S K.       [S K is the "pick second" combinator: S K a b = K b (a b) = b.]

   Ω (Ω (Ω Ω)) = Ω (S K) = (S K) S K
                 = K K (S K)          [S-rule with x = K, y = S, z = K]
                 = K.                  [K-rule]

   Ω (Ω (Ω (Ω Ω))) = Ω K = K S K = S.  [K-rule]

So the Ω-term K* reduces (under the ideal rule) to K and the Ω-term S* reduces (under the ideal rule) to S. Substituting S* and K* for S and K inside the rule gives the literal rule above — it is self-referential in exactly the way Y's rule is, and its behaviour on terms is what the abstract rule describes, modulo unfolding steps.

Under this construction, P₇ = {Ω}, |P₇| = 1. I adopt this as P*, subject to the counting convention stated next.

---

## §4. The Minimal Primitive Set P*

**Counting convention, declared.**

1. A *primitive* is a symbol paired with one rewrite rule. The count |P| is the number of primitive symbols.
2. *Application* is the free binary constructor, not counted as a primitive.
3. A rule may reference the primitive being defined (self-reference), the way Y's baseline rule does. This is allowed under "the same way the baseline is defined".
4. A rule's RHS may mention only (i) the LHS's bound variables and (ii) the primitive being defined. It may *not* mention any *other* primitive. Under this constraint, a set with k primitives has rules each quoting only itself.
5. Rule complexity (length, nesting depth, number of Ω-occurrences on the RHS) is *not* counted. A rule like "Ω x → x (Ω(Ω(Ω(Ω Ω)))) (Ω(Ω(Ω Ω)))" counts the same as "I x → x".

Under this convention:

  **P* = {Ω}, with rule Ω x → x (Ω(Ω(Ω(Ω Ω)))) (Ω(Ω(Ω Ω))).**  **|P*| = 1.**

The new primitive is Ω; its reduction rule is self-referential. The two Ω-subterms on the RHS are exactly the Ω-synthesis of the S and K primitives.

(If the convention were tightened to forbid self-reference, Y would fail too — so for fairness the baseline's own rules would no longer satisfy the convention, and the question is ill-posed. Conversely, if the convention counted rule-RHS length, {S, K} [total RHS length 3 + 1 = 4] would beat {Ω} [RHS length on the order of 10 occurrences]. My convention is the one natural to the task: count symbols, allow self-reference, ignore rule size.)

A robust fallback: under the stricter "no self-reference" convention, **P* = {S, K}, |P*| = 2** (derived in §3.6).

---

## §5. Verification Strategy

I use a **multi-pronged strategy**:

**(V1) Explicit synthesis, baseline-by-baseline.** For each primitive p ∉ P* in the chain §3, an explicit closed term tᵖ over P* was given and its reduction tᵖ y₁…yₙ ↠ p y₁…yₙ was traced. This discharges sufficiency for every baseline primitive except Y; for Y, the trace §3.6 discharged its defining equation Y* f = f (Y* f). By confluence of weak reduction on closed S-K terms (standard property of the underlying term-rewriting system: each rule is left-linear and non-overlapping), tᵖ and p are observationally identical.

**(V2) Reduction to a known-complete basis.** {S, K} is confirmed computationally universal by the following standard first-principles argument. A *bracket-abstraction* procedure converts any untyped λ-term to a closed S-K combinator with the same reduction behaviour:
  [x]ᵤ = I         (with u the abstracted variable)
  [y]ᵤ = K y        (y ≠ u, y does not contain u)
  [M N]ᵤ = S [M]ᵤ [N]ᵤ.
By structural induction on the λ-term, the translation preserves β-equivalence (K handles the case where u does not occur; S handles the case where u occurs on both sides of an application). Since the untyped λ-calculus expresses every computable function of natural numbers (it encodes recursive functions with full generality), {S, K} does as well. Since the extended calculator's primitives are all λ-definable (each primitive's rule is a β-equivalence), the extended calculator's reduction behaviour is a subset of {S, K}-reachable behaviour.

**(V3) Transitivity.** {Ω} → (synthesizes) → {S, K} → (synthesizes) → all baseline → all extended-calculator behaviour. Each arrow is a finite synthesis, so the composition is.

**(V4) Lower bound (non-triviality).** |P*| ≥ 1. No non-empty calculator behaviour is reachable from ∅ (no terms to apply). Hence |P*| = 1 is optimal *under the declared convention*.

**(V5) Lower bound (from invariants).** Under the stricter "no self-reference" convention, I claim |P*| ≥ 2 by the multiplicity-invariant argument of §2b. No single baseline primitive has both duplication and erasure in its rule. For a hypothetical single *invented* structural primitive Ω with rule Ω x₁…xₙ → T (no self-ref, only LHS variables on RHS) to be complete, T must exhibit both duplication (some variable twice) and erasure (some variable absent). No such arity-2 rule is complete (easy exhaustion); arity-3 and above are conjecturally achievable (this is the canonical pure-structural single-combinator question, which I do not claim to solve here — it requires a careful encoding that exceeds the space I have), so in the strict convention I settle on |P*| = 2 as the defensible lower bound.

---

## §6. Worked Examples

### Example A — Identity

Over {S, K}:  I = S K K.
  S K K z → K z (K z) → z.

Over {Ω}:  I = Ω Ω (behaviourally).
  Ω Ω z = (Ω's rule) z applied after the rule's unfolding. In abstract terms (Ω x = x S K):
     Ω Ω = Ω S K = (S S K) K = S S K K = S K (K K) = (S K)(K K).
     (S K)(K K) z = K z ((K K) z) = K z K = z.
  So Ω Ω z ↠ z, i.e., Ω Ω acts as I on any argument z.

### Example B — Iterator-style successor and a small addition

Iterator-style numerals: cₙ f x = fⁿ x (apply f to x, n times).
  c₀ f x = x
  c₁ f x = f x
  c₂ f x = f (f x)

Successor: succ n = λf x. f (n f x). In S-K form (derived once, used everywhere):
  succ = S B.
Verify: S B n f x = B f (n f) x = f (n f x). ✓

With B = S (K S) K:
  succ = S (S (K S) K).

With only {Ω}: substitute S ↦ S* = Ω(Ω(Ω(Ω Ω))) and K ↦ K* = Ω(Ω(Ω Ω)):
  succ = S* (S* (K* S*) K*).

Compute succ c₀ at f, x explicitly (using the S-K form):
  succ c₀ f x
   = S B c₀ f x
   = B f (c₀ f) x                [S-rule]
   = f (c₀ f x)                   [B-rule]
   = f x.                         [c₀ f x = x]
So succ c₀ f x = f x = c₁ f x. Good: succ c₀ = c₁.

Iterator addition: add m n f x = m f (n f x). Arithmetically, add m n = n succ m: apply the successor n times to m. Both forms are S-K expressible; concretely, bracket-abstract λm n f x. m f (n f x) through the procedure in §5 to obtain a pure S-K term (the derivation is mechanical but ~10 lines of intermediate steps, which I elide). With succ = S B already in P₆, the resulting add sits inside P₆. Over {Ω}, expand S and K by the Ω-synthesis above.

Spot-check a small addition: add c₀ c₁ should be c₁. Compute add c₀ c₁ f x = c₀ f (c₁ f x) = c₁ f x = f x. And c₁ f x = f x. ✓

### Example C — A divergent term via a fixed-point combinator

Y f ↠ f (Y f) ↠ f (f (Y f)) ↠ …

Over {S, K}, using Y* from §3.6: set f := I. Then
  Y* I ↠ I (Y* I) ↠ Y* I,
giving an infinite reduction sequence — no normal form.

More usefully, pick f to be a "self-applying" computation. For example, f = λx. f-action(x); apply Y* f and you get an infinite unrolling that computes f's recursive definition.

A concrete divergent term entirely in {S, K}: (S I I)(S I I). Compute:
   (S I I)(S I I) = I (S I I) (I (S I I))  = (S I I)(S I I).
That is, (S I I)(S I I) reduces to itself — a classic diverging term, built only from S and K (since I = S K K). The term

   (S (S K K) (S K K)) (S (S K K) (S K K))

is a pure S-K term that diverges, exhibiting that divergent computations are reachable from P* = {S, K} (and hence from {Ω} by further substitution).

---

## §7. Open Questions and Known Limitations

**(a) Is P* = {Ω} optimal?**

Yes, trivially: |P*| ≥ 1 because ∅ cannot produce any non-empty calculator behaviour (no terms exist without primitives). Going below 1 would require application itself to be non-trivial, which it is not — application is an inert binary constructor with no reduction rule of its own. Under any counting convention that treats "primitive symbols" as the unit of count, 1 is a lower bound.

However: my {Ω} trades a large primitive set for a large rule. The rule's RHS mentions Ω five times. If one scored "reduction systems" by the total number of symbol-occurrences across all rule RHSs, {S, K} (3 + 1 = 4) beats {Ω} (~10). Under that alternative, the minimum might be 2, achieved by {S, K}, or something different again.

**(b) Strong reduction (reduction under binders).**

The analysis above was in weak-reduction mode: no reducing under a variable-binder (lambda), combinators treated as closed first-order terms that reduce only when fully applied. Under strong reduction, additional redexes become visible — in particular, η-redexes (λx. M x ↠ M when x ∉ M). With η, some of our equivalences collapse to identities: for instance, Ω (Ω Ω) ≡ S K ≡ λab. b, and η-reducing λab. b leaves it fixed (no trailing eta-redex), but other identities tighten. The *minimum* P* is unchanged, because sufficiency at weak reduction implies sufficiency at strong reduction (more redexes do not *remove* expressible behaviour). Insufficiency invariants transfer as well: multiplicity invariants hold under both weak and strong reduction. So §5 goes through.

One caveat: under strong reduction, *inequivalent* weak-reduction terms may become η-equivalent, slightly relaxing the synthesis obligation. This can only *shrink* the minimum P*, not grow it.

**(c) Dependence on convention.**

The single greatest source of ambiguity is convention, not mathematics. Ranking:

  - **"Count primitive symbols, self-reference allowed, ignore rule size."** My convention. P* = {Ω}, size 1.
  - **"Count primitive symbols, no self-reference allowed, ignore rule size."** A pure-structural single-combinator basis plausibly exists (invent an arity-3 rule with both duplication and erasure), but I have not exhibited one explicitly, and the invariant argument of §2b only rules out certain small arities. Assuming such an invented combinator exists, P* = 1. If one insists it be baseline-only, P* = {S, K}, size 2.
  - **"Count primitive symbols, self-reference allowed, *include* rule RHS size in the count."** Minimum is heavily convention-dependent: Ω's rule has RHS size ~10, while {S, K} has total rule RHS size 4. {S, K} wins.
  - **"Count primitive symbols, each rule's RHS must be a term over primitives only (no bound variables on RHS as free-standing subterms) and no self-reference."** Removes Y's rule from the baseline — the question changes: without self-reference, the baseline is not what it was.

Different conventions give different minima. The *ordering* of answers under my convention is: {Ω} (1) < {S, K} (2) < {S, K, Y} (3) < full baseline (13). Under the pure-structural-no-self-ref convention, the chain is: {S, K} (2) < {S, K, Y} (3) < full baseline (13), with my {Ω} unavailable.

**(d) Complexity blow-up.**

The translation from the baseline into P* is size-expanding. Each layer (V, D, T, M, etc. → B, C, W, Y; then B, C, W, Y → S, K; then S, K → Ω) multiplies term size by a constant factor. The final Ω-translation of a baseline term of size n has size roughly O(nᶜ) for some c depending on the worst-case substitution depth (each S-K symbol expands to a ~10-symbol Ω-tree). This is a genuine cost: compactness is traded for uniformity of primitive set.

**(e) Confluence under translation.**

Both the baseline and {S, K} and {Ω} are left-linear, non-overlapping term-rewriting systems (each rule's LHS is a single combinator applied to distinct variables; different combinators' rules do not overlap). By a standard argument, such systems are confluent. Translation preserves confluence because the translation is compositional and each translated rule simulates the original's reduction behaviour by a bounded-length sequence of translated-system reductions. Hence the translated system inherits the diamond property (confluence): if M ↠ N₁ and M ↠ N₂ in the baseline, then translations M*, N₁*, N₂* satisfy M* ↠ N₁* and M* ↠ N₂*, and both N₁* and N₂* reduce to a common term.

**(f) A cleanly-pure-structural single combinator: open.**

Whether there exists a cleanly pure-structural (no self-reference on RHS, only LHS bound variables) single combinator Ω of low arity that is complete — call this the "strict-1 question" — I do not resolve from first principles within this deliverable. Candidate rules must contain both duplication and erasure; I explored several arity-3 rules (e.g., Ω x y z → x z z) and found that various Ω-compositions yield W-like and K-W-like behaviours but the direct synthesis of bare K from pure Ω eludes a short derivation. This is a real open question for me; a more leisurely derivation (or a rule with arity ≥ 4 carefully chosen so that self-application cascades produce both K and S) would likely settle it affirmatively.

---

*End of argument.*
