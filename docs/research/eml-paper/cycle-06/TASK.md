# Cycle 06 — TASK definition (ROOT-only)

**Cycle purpose.** Cycle #5 closed with a Δ = +2 delta driven entirely by
R10 (A: 28/30, B: 30/30) because both agents reached R1–R9 = 27/27 on
Cycle #5's confluence-of-combinators domain.  The first-draft natural
ceiling was too high — the intended "iteration pays on R6 as well"
regime did not activate.  Cycle #6 addresses this directly per Cycle #5
JUDGMENT.md §5 "implication for Cycle #6":

> "Cycle #6 TASK design should aim at a domain where the first-draft's
> natural ceiling is genuinely sub-band-3 on ≥ 3 of R1-R9 axes — e.g.,
> a domain with known wrong-attractor first-draft patterns that
> iteration uncovers, or a domain where subtle counter-examples must
> be found rather than a positive result proved."

Cycle #6 also addresses two rubric-level findings from Cycle #5's
proof-auditor pass:

1. **R10 band-0 / band-1 boundary disambiguation** (auditor CONDITIONAL
   on A-R10 in Cycle #5): the R10 axis text now states explicitly that
   an audit naming zero gaps is a **vacuous audit** and scores band 0,
   not band 1.  The text has been ported into `judgment-rubric.md` for
   Cycle #6 with a Cycle #6-specific "example bands" row.
2. **L2→L3 credential cleanup gap**: `scripts/meta/cleanup-sub.sh` is
   now repo-committed; `scripts/meta/delegate-sub.sh` prints a cleanup
   hint after each launch.  Cycle #6 post-stable forensic verification
   confirms the mechanism works in production (GOAL clause 9).

Domain choice for Cycle #6: **a small term-rewriting system with
simultaneous confluence and termination obligations.**  Confluence
alone (Cycle #5) has a textbook parallel-reduction-diamond proof
technique that first-principles agents reach via structural inspection;
termination requires a distinct tool (a well-founded measure with
strict-decrease closure under contexts) that first drafts routinely
conflate with confluence or hand-wave via "the terms get smaller".
Adding termination as a second obligation forces structural choices in
§2 (method design) and §4 (verdict commitment), and opens ≥ 2 non-R10
axes for band-2 ceiling pressure.

---

## 1. Task prompt delivered to A and B

Both sub-agents receive identical text via
`scripts/meta/delegate-sub.sh <key>`.  `scripts/meta/paper-leak-audit.sh`
pattern set is checked on the GOAL before launch.

```
TASK: Joint confluence + termination of a small list/length rewriting system

You are given a term-rewriting system R over the signature Σ below.
Terms are built from Σ; variables are written xs, ys, zs, ws, x, y.
Application is the standard tree-style term formation.

  Signature Σ:
    Nullary constructors:   0,  nil
    Unary constructors:     s
    Binary constructor:     cons
    Unary defined:          len
    Binary defined:         app

  Rules R:
    ρ1:  len(nil)                → 0
    ρ2:  len(cons(x, ys))        → s(len(ys))
    ρ3:  app(nil, ys)            → ys
    ρ4:  app(cons(x, xs), ys)    → cons(x, app(xs, ys))
    ρ5:  app(app(xs, ys), zs)    → app(xs, app(ys, zs))

Reduction → is the least relation on terms that contains R (matching
LHS anywhere in a term rewrites that subterm to the corresponding RHS)
and is closed under contexts.  ↠ is the reflexive-transitive closure
of →.

You must settle BOTH of the following for R:

Q1. CONFLUENCE.  Is R confluent?  That is, for every term t and every
    pair of reduction sequences t ↠ u and t ↠ v, does there always
    exist a term w such that u ↠ w and v ↠ w?  Either (a) prove R is
    confluent by closing all critical pairs and discharging the
    closure under reduction, or (b) exhibit a concrete divergent pair
    (u, v) from some term t with u ↛* w and v ↛* w for any common w.

Q2. TERMINATION.  Does R terminate on all closed terms?  That is, is
    → well-founded on the set of terms over Σ?  Either (a) prove
    termination by exhibiting a well-founded measure that strictly
    decreases under every rule application (including when the rule
    fires inside an arbitrary context), or (b) exhibit a closed term
    t with an infinite reduction sequence t → t₁ → t₂ → ….

The two obligations are logically independent (a non-terminating
system can still be confluent; a non-confluent system can still be
terminating).  Treat them as separate proof obligations sharing only
the ambient reduction relation.

Your deliverable: a self-contained argument, written to
`task/ARGUMENT.md` in your working directory.  It must include:

  1. Motivation.  Why might confluence hold or fail for R?  Why
     might termination hold or fail?  Cite precedents from adjacent
     algebraic, logical, or computational domains that you reason
     about from first principles — for example, unique-normal-form
     properties of pattern-matching functional programs, structural
     induction as a termination discipline, equivalence-class
     definiteness in quotient systems.  Explain what structural
     feature of each rule makes each property plausible (or
     implausible).  Derive the intuitions; do not name the
     techniques.

  2. Method design — with **two sub-sections** for the two obligations:

     §2.1 Confluence method.  Given a candidate TRS, how do you (a)
     identify potential counter-examples (critical-pair analysis,
     overlap detection, left-linearity check), and (b) discharge
     confluence when no counter-example is found (parallel-reduction
     / diamond arguments, iterative critical-pair closure, or
     translation to a known-confluent system)?

     §2.2 Termination method.  Given a candidate TRS, how do you
     (a) construct a well-founded measure from the rule structure,
     (b) verify that every rule strictly decreases the measure
     (monotonicity under contexts), and (c) handle the case where
     a rule's RHS is structurally larger than its LHS (which does
     not preclude termination — the measure is typically an
     interpretation, not a literal size count).

     The two methods may share infrastructure (both work at the
     term level, both use structural induction) but must not be
     conflated.  Do not claim "confluence because terminating
     plus local-confluence" without a separate argument for local
     confluence that discharges every critical pair; do not claim
     "termination because each rule's RHS is simpler" without a
     named measure that monotonically decreases.

  3. Progressive derivation with two interleaved strands.
     §3.1 Critical-pair enumeration for Q1.  List every pair
     (ρᵢ, ρⱼ) of rules (including self-overlaps) that has a
     non-variable overlap position; for each, write the critical
     pair as a pair of reducts of a single most-general term; then
     either close it (exhibit a common reduct) or exhibit it as a
     counter-example to confluence.
     §3.2 Measure construction and decrease proof for Q2.  State
     your chosen measure (e.g., a polynomial interpretation, a
     structural weight, a composite with lexicographic ordering);
     prove it is well-founded; for each of the 5 rules, verify
     strict decrease, showing the arithmetic / structural
     computation.

  4. Final verdict structure.
     §4.1 Q1 answer.  Either "R is confluent" (with the full
     critical-pair closure table as evidence) or "R is NOT
     confluent" (with the concrete divergent pair as evidence).
     §4.2 Q2 answer.  Either "R terminates" (with the measure and
     its strict-decrease proof as evidence) or "R does NOT
     terminate" (with the concrete infinite reduction as evidence).
     §4.3 Joint implication (if any).  State whether and how the
     two verdicts relate for R.  If you use local-confluence +
     termination ⟹ confluence as an inferential shortcut for Q1,
     you MUST derive that implication from first principles in
     the step where you invoke it (the implication itself is a
     classical result but the derivation must appear, not the
     name).

  5. Verification strategy.  How do you confirm the claims hold?
     Options include: (a) exhaustive critical-pair enumeration
     with each closure traced explicitly, (b) a measure whose
     decrease is verified by symbolic computation for each rule
     instance, (c) an executable simulator that enumerates
     reductions from a test suite of closed terms, reporting
     both confluence (common-reduct convergence) and termination
     (step counts bounded, no reduction exceeds a computed
     bound).  **Worked executable-oracle verification, if
     performed, counts as a R6 = 3 indicator alongside any
     trace-argument path.**

  6. Worked examples: exhibit at least three distinct reduction
     scenarios over R.  Suggested categories: (a) a term
     exercising the associativity rule ρ5 in both reduction
     orders (inner-before-outer vs outer-before-inner), both
     paths converging to a common right-associated reduct;
     (b) a term whose length-reduction and app-reduction
     interleave across a cons-structure; (c) a term
     demonstrating termination on an initially-larger-than-
     RHS rule (ρ4 or ρ5) via the measure you constructed.
     Give the full reduction traces and, where relevant, the
     measure value at each step.

  7. Open questions and known limitations, including:
     (a) whether your proofs extend to R augmented with a
     natural-number addition operator and an add-unfolding rule
     like len(app(xs, ys)) → add(len(xs), len(ys)) — does your
     termination measure still decrease?
     (b) whether your confluence proof relies on R's specific
     left-linearity + non-overlap property or generalizes;
     (c) the relationship in R between termination and
     confluence — for this R specifically, does each property
     imply the other, or are they independent on R?
     (d) whether your measure is a polynomial interpretation
     or a more exotic beast (multiset-of-subterms, structural
     weight, lexicographic composition) and whether the choice
     matters for the termination proof's tightness.

Constraints:
  - Do not consult external sources.  Arguments must be developed
    from first principles.  WebFetch and WebSearch are disabled.
  - Do not rely on named results you cannot derive.  If you invoke
    a theorem, sketch its reason.
  - Cite no papers.  If you remember a relevant paper, state the
    underlying idea in your own words; do not name or quote.
  - Do not use the following identifiers by name: SKI calculus, SK
    calculus, BCKW, BCIW, Iota combinator, ι-combinator, Jot
    calculus, Unlambda, Binary Lambda Calculus, BLC, X-combinator,
    Xi-combinator, Zot, Turing's universal combinator, Curry (as a
    person's surname), Schönfinkel, Rosser, Church (as a person's
    surname), Church-Rosser property, Tait–Martin-Löf technique,
    Takahashi translation, Newman's lemma, Knuth–Bendix, Hindley–
    Rosen, Dershowitz, Manna–Ness, Manna-Ness, recursive path
    order, RPO, lexicographic path order, LPO, multiset path
    order, MPO, dependency pair method, dependency pairs, Kamin,
    Lévy, Kamin-Lévy, Kamin–Lévy, Huet's critical pair lemma,
    Huet.  You MAY use the structural vocabulary "critical pair",
    "overlap", "joinable", "confluent", "terminating", "strongly
    normalizing", "well-founded", "measure", "interpretation",
    "monotonic", "strictly decreasing", "rewrite", "rewriting",
    and all symbol letters (0, s, nil, cons, len, app, xs, ys,
    zs, ws, x, y, ρ₁…ρ₅) as-is.  If you recognize the canonical
    technique under one of the banned names, work around the
    name and derive the structure yourself.

  - Iteration affordance (important).  If your agent configuration
    provides an iteration, self-audit, or refinement mechanism
    (whatever its invocation convention), you are encouraged to use
    it and to persist the iteration trace to your working directory
    at any path you choose (for example, `task/attempts/attempt-01.md`,
    `task/iterations/iter-01.md`, `task/.eval-report.json`, a
    subdirectory under `task/`).  ROOT will cite these paths in
    scoring.  If your configuration does not provide such a
    mechanism, a single-shot argument is a legitimate response and
    you should simply deliver it.  Do not simulate iteration; if
    you iterate, actually iterate — each iteration's evaluator
    report must name ≥ 1 disclosed gap for that iteration to count
    as closure-producing (per the updated R10 band definitions).

  - Double obligation (critical).  Both Q1 and Q2 must receive
    rigorous treatment.  A brilliant Q1 proof with a hand-waved
    Q2 answer, or vice-versa, will score materially lower than
    a balanced treatment.  If one obligation is harder for you
    than the other, disclose the asymmetry and spend the
    remaining rigor budget on closing the hardest gap, not on
    polishing the easier obligation.
```

---

## 2. Ideal answer (ROOT-only)

R **is** confluent AND **is** terminating.  The ideal path from first
principles:

### 2.1 Confluence (Q1)

All 5 rules have distinct head symbols on their LHS (ρ1, ρ2 head `len`;
ρ3, ρ4 head `app` with different first arg patterns — `nil` vs
`cons(x, xs)`; ρ5 head `app` with first arg pattern `app(…)`).  Each
rule is left-linear (no variable repeats in any LHS).

**Critical-pair overlaps** (only non-variable positions count):
- ρ1 vs any rule: ρ1 LHS is `len(nil)`, nullary `nil` has no
  non-variable subterm; no overlap.
- ρ2 vs any rule: ρ2 LHS is `len(cons(x, ys))`; non-variable subterm
  at position 1 is `cons(x, ys)` with head `cons` (constructor, no
  rule has `cons` at LHS head).  No overlap.
- ρ3 vs any rule: ρ3 LHS is `app(nil, ys)`; non-variable subterm at
  position 1 is `nil` (no rule's LHS matches nullary `nil`).  No
  overlap.
- ρ4 vs ρ5: ρ4 LHS is `app(cons(x, xs), ys)`; at position 1 we have
  `cons(x, xs)` with head `cons` (no rule LHS matches `cons(…)`); no
  overlap.  ρ5's LHS is `app(app(xs, ys), zs)`; position 1 is
  `app(xs, ys)` — this can be unified with ρ4's LHS (`app(cons(x,
  xs'), ys')`), forcing xs = cons(x, xs'), ys = ys'.  The induced
  critical pair is at most-general term `app(app(cons(x, xs'), ys'),
  zs)`:
    - outer ρ5 fires → `app(cons(x, xs'), app(ys', zs))`
    - inner ρ4 fires → `app(cons(x, app(xs', ys')), zs)`
  Both reduce further:
    - first path → `cons(x, app(xs', app(ys', zs)))` via ρ4
    - second path → `cons(x, app(app(xs', ys'), zs))` via ρ4 →
      `cons(x, app(xs', app(ys', zs)))` via ρ5
  Common reduct reached.  Joinable.
- ρ5 vs ρ5 (self-overlap): ρ5 LHS `app(app(xs, ys), zs)`; position 1
  is `app(xs, ys)`.  Self-overlap at position 1 unifies
  `app(xs, ys)` with `app(app(xs', ys'), zs')`.  Most-general term:
  `app(app(app(xs', ys'), zs'), zs)`:
    - outer ρ5 → `app(app(xs', ys'), app(zs', zs))` → `app(xs',
      app(ys', app(zs', zs)))` via ρ5
    - inner ρ5 → `app(app(xs', app(ys', zs')), zs)` → `app(xs',
      app(app(ys', zs'), zs))` via ρ5 → `app(xs', app(ys',
      app(zs', zs)))` via ρ5
  Common reduct.  Joinable.
- ρ3 vs ρ5 (non-trivial, often missed): ρ5's position 1 (`app(xs,
  ys)`) can unify with ρ3's LHS (`app(nil, ys'')`), forcing xs = nil.
  Most-general term: `app(app(nil, ys''), zs)`:
    - outer ρ5 → `app(nil, app(ys'', zs))` → `app(ys'', zs)` via ρ3
    - inner ρ3 → `app(ys'', zs)`
  Same term.  Joinable.

So all critical pairs are joinable.  Since R is left-linear and all
critical pairs are joinable, R is confluent — by the standard
parallel-reduction diamond argument (derivable from first principles
without naming the orthogonality theorem).

### 2.2 Termination (Q2)

Polynomial interpretation I : Terms(Σ) → ℕ, extended to terms with
variables by treating variables as ℕ-valued:
- I(0) = 1
- I(s)(x) = x + 1
- I(nil) = 2
- I(cons)(x, y) = x + y + 2
- I(len)(x) = x + 1
- I(app)(x, y) = 2x + y + 1

Monotonicity: each function is strictly increasing in each of its
arguments (positive coefficients), so I is monotonic under arbitrary
contexts.

Strict decrease per rule:
- ρ1: I(len(nil)) = 2 + 1 = 3; I(0) = 1.  3 > 1. ✓
- ρ2: I(len(cons(x, ys))) = (x + ys + 2) + 1 = x + ys + 3.
       I(s(len(ys))) = (ys + 1) + 1 = ys + 2.
       x + 3 > 2 for x ≥ 0. ✓
- ρ3: I(app(nil, ys)) = 2(2) + ys + 1 = ys + 5.
       I(ys) = ys.  5 > 0. ✓
- ρ4: I(app(cons(x, xs), ys)) = 2(x + xs + 2) + ys + 1 = 2x + 2xs +
       ys + 5.
       I(cons(x, app(xs, ys))) = x + (2xs + ys + 1) + 2 = x + 2xs +
       ys + 3.
       (2x + 5) − (x + 3) = x + 2 > 0 for x ≥ 0. ✓
- ρ5: I(app(app(xs, ys), zs)) = 2(2xs + ys + 1) + zs + 1 = 4xs + 2ys
       + zs + 3.
       I(app(xs, app(ys, zs))) = 2xs + (2ys + zs + 1) + 1 = 2xs + 2ys
       + zs + 2.
       (4xs + 3) − (2xs + 2) = 2xs + 1 > 0 for xs ≥ 0. ✓

All rules strictly decrease the interpretation.  Since ℕ is
well-founded under the usual ordering and I is monotonic under
contexts, every reduction sequence must eventually terminate.
Therefore R is terminating.

### 2.3 What can go wrong in first drafts

- **Conflate the two proofs.**  Claim confluence "because the system
  is terminating and locally confluent" without explicitly deriving
  the implication (the classical statement behind the banned name
  "Newman's lemma") or without separately enumerating critical pairs.
- **Miss the ρ5 critical pairs.**  The self-overlap and the ρ3/ρ4
  overlaps via position 1 of ρ5 are easy to miss at first pass.  A
  first draft that only checks "distinct head symbols imply no
  overlap" misses that ρ5 LHS has `app` at position 1 too.
- **Weight coefficient failure on ρ5.**  A naive measure
  I(app)(x, y) = x + y + 1 fails on ρ5 — LHS and RHS interpret to
  the same value, no strict decrease.  The asymmetric coefficient
  I(app)(x, y) = 2x + y + 1 (double-weight on left operand) is the
  key insight — the associativity rule ρ5 moves complexity from the
  left subtree to the right subtree, so the left operand must carry
  extra weight.
- **Claim termination because "terms get smaller"** while RHS of ρ4
  (cons(x, app(xs, ys))) is structurally larger than LHS
  (app(cons(x, xs), ys)) by one cons node — size count alone does
  not work; the polynomial interpretation is required.
- **Hand-wave the monotonicity.**  "The measure decreases on each
  rule" without saying "and the measure is strictly increasing in
  each argument of each operator, so strict decrease propagates
  under contexts" — the context-closure step is where a first draft
  typically skips the careful argument.
- **Ignore the open-question (7a) add-augmented variant.**  Extending
  with `add` and `len(app(xs, ys)) → add(len(xs), len(ys))` requires
  re-checking the measure; a strong ARGUMENT addresses whether the
  current interpretation extends.

**R9 binary shape for this cycle:** R9 = 3 iff the ARGUMENT produces
correct verdicts on **both** Q1 (confluent) and Q2 (terminating)
with rigorous discharge for each.  One correct + one hand-waved is
R9 = 0 (the shape of the answer is "two verdicts with discharge",
not "one verdict with discharge and one hand-wave").  Partial
credit not allowed for R9.

---

## 3. Paper-identifying keywords for this cycle (informational)

These must NOT appear in any TASK prompt, ROOT→sub delegation
payload, or the delivered prompt.  They are allowed in this
ROOT-only file because it is never mounted into A or B.

**Inherited from Cycle #5 (20 entries):**

- "SKI calculus" / "SKI"
- "SK calculus"
- "BCKW" / "BCIW"
- "Iota combinator" / "ι" (the Greek letter in combinator-name context)
- "Jot" / "Jot calculus"
- "Unlambda"
- "Binary Lambda Calculus" / "BLC"
- "X combinator" / "Xi combinator"
- "Zot"
- "Schönfinkel" (person's name)
- "Haskell Curry" (person's name)
- "Alonzo Church" (person's surname)
- "Barkley Rosser" (person's surname)
- "Turing's universal combinator"
- "Church-Rosser" / "Church–Rosser" / "Church-Rosser property"
- "Tait–Martin-Löf" / "Tait-Martin-Löf" / "Tait Martin-Löf technique"
- "Takahashi translation" / "Takahashi parallel reduction"
- "Newman's lemma"
- "Knuth–Bendix" / "Knuth-Bendix" / "Knuth-Bendix completion"
- "Hindley–Rosen" / "Hindley-Rosen lemma"

**Cycle #6 domain-specific additions (7 entries):**

- "Dershowitz" (surname; termination researcher)
- "Manna-Ness" / "Manna–Ness" (surname pair)
- "recursive path order" / "RPO"
- "lexicographic path order" / "LPO"
- "multiset path order" / "MPO"
- "dependency pair method" / "dependency pairs"
- "Kamin-Lévy" / "Kamin–Lévy" / "Kamin" + "Lévy" (surnames)
- "Huet's critical pair lemma" / "Huet" (surname)

Total Cycle #6 banned-identifier list: **28 entries** (20 base + 8
new; counting "Kamin-Lévy" and its surname components as a 2-item
group).

The existing `paper-leak-guard.sh` reversed-form patterns cover the
base paper keyword set; the 28 Cycle #6 names are enforced via
(a) explicit listing in §1's delegation prompt, (b) post-cycle
`paper-leak-audit.sh` base-pattern scan, (c) an extended post-cycle
grep for the 28 Cycle #6 names (§4 below).  No reversed-form
blocklist extension is performed — the cycle's symmetric-zero-change
convention on `projects/a/` applies, and reversed-form hardening is
reserved for new paper-adjacent path / file identifiers, not cycle-
specific technical names.

---

## 4. Post-cycle leak audit extension (Cycle #6 only)

Run the base `scripts/meta/paper-leak-audit.sh` (blocks the eml
paper keyword set, still applicable) on each ARGUMENT.md.  Then
additionally grep each ARGUMENT.md for each name in §3:

```
grep -iE 'ski calculus|sk calculus|bckw|bciw|iota combinator|jot|unlambda|binary lambda calculus|\bblc\b|x combinator|xi combinator|\bzot\b|schönfinkel|schonfinkel|haskell curry|alonzo church|barkley rosser|turing.s universal combinator|church.rosser|tait.martin.löf|tait.martin-lof|takahashi|newman.s lemma|knuth.bendix|hindley.rosen|dershowitz|manna.ness|recursive path order|\brpo\b|lexicographic path order|\blpo\b|multiset path order|\bmpo\b|dependency pair|kamin.lévy|kamin.levy|huet' projects/a/task/ARGUMENT.md
grep -iE 'ski calculus|sk calculus|bckw|bciw|iota combinator|jot|unlambda|binary lambda calculus|\bblc\b|x combinator|xi combinator|\bzot\b|schönfinkel|schonfinkel|haskell curry|alonzo church|barkley rosser|turing.s universal combinator|church.rosser|tait.martin.löf|tait.martin-lof|takahashi|newman.s lemma|knuth.bendix|hindley.rosen|dershowitz|manna.ness|recursive path order|\brpo\b|lexicographic path order|\blpo\b|multiset path order|\bmpo\b|dependency pair|kamin.lévy|kamin.levy|huet' projects/b/task/ARGUMENT.md
```

"Confluence" / "confluent" / "diamond" / "parallel reduction" /
"critical pair" / "overlap" / "residual" / "normal form" /
"well-founded" / "measure" / "polynomial interpretation" /
"strictly decreasing" / "monotonic" / "terminating" / "strongly
normalizing" — generic structural vocabulary, **not** name-
identifying; do not disqualify on these.  Bare letters (Σ, ρ,
variable names xs, ys, …) are symbols from the prompt, permitted.

---

## 5. Hint-drift record (required by CLAUDE.md §6.7 step 1)

| Hint | Decision | Rationale |
|---|---|---|
| "Does R terminate?" + "Is R confluent?" as two separate named obligations | **Included** | Cycle #5's confluence-only prompt ceilinged first-draft R1-R9 at 27/27.  Adding an explicit second obligation of a categorically different kind (confluence = joinability, termination = well-foundedness) forces structural separation in §2 and §4.  First drafts routinely conflate them; R6 and R2 ceiling drops to band 2. |
| Polynomial interpretation as a specific technique name | **Omitted from prompt, allowed in vocabulary** | The task prompt says "well-founded measure that strictly decreases".  "Polynomial interpretation" is the classical instantiation for this TRS; it is allowed as structural vocabulary (not a named theorem) so agents can describe their measure as a polynomial without being forced into a ban-workaround paraphrase.  The specific measure (asymmetric 2x + y + 1 for app) must be derived. |
| Named termination techniques (RPO, LPO, MPO, dependency pairs) | **Omitted and explicitly banned** | These are the canonical first-reach tools for termination.  Banning them forces agents to construct a measure from rule structure — the whole point of the Q2 obligation.  "Dershowitz" (the common surname in the termination literature) is banned alongside the technique names. |
| "Newman's lemma" as inferential shortcut | **Still banned (inherited)** + explicit instruction in clause 4.3 that the agent must derive the implication if invoking it | Newman's lemma is tempting: "local confluence + termination ⟹ confluence" is clean.  Banning the name while allowing the *inference*-if-derived forces a first-principles argument when the agent uses it.  Most first drafts will reach for the shortcut; by structural-derivation requirement, this becomes a band-2 R6 drop, not R6 = 3. |
| "Orthogonality" (left-linearity + non-overlap ⟹ confluence) | **Included as structural vocabulary** (unchanged from Cycle #5) | "Orthogonal term-rewriting system" is a structural property of rules.  The implication "orthogonal ⟹ confluent" is derivable; the *name* of the implication ("orthogonality theorem") is allowed.  Cycle #5 validated this framing. |
| Explicit R10 iteration expectation | **Included at end of §1** with new "each iteration's evaluator report must name ≥ 1 disclosed gap" clarification | Cycle #5 A's one-draft-plus-vacuous-audit pattern produced the R10 band-0/1 CONDITIONAL.  The updated R10 text now classifies vacuous audits as band 0, and the prompt language reinforces this: ritual iteration without named gaps does not cross the band threshold. |
| Executable-oracle verification mention | **Included as "R6 = 3 indicator"** in §1 clause 5 | Cycles #3, #4, #5 established this pattern.  `scripts/meta/oracles/combinator-reducer.py` is NOT directly applicable here (combinator-specific); Cycle #6 agents must build a term-rewriting simulator if they choose this path.  Domain-agnostic oracle pointer is provided in §11 below. |
| Explicit R4/R6 decoupling for Q1 vs Q2 | **Embedded in §1 clause 2** (two sub-sections) and §1 clause 4 (three sub-sections) | Forces the agent to write confluence and termination as two separate proofs with separate discharge, not as a unified narrative.  First drafts that write them as one flowing argument are scoring-capped. |
| Expected A first-draft band-2 axes | (not stated in prompt) | ROOT anticipates first-draft band-2 on R2 (conflated methods), R3 (partial CP enumeration or partial measure check), R6 (hand-waved measure monotonicity under contexts) — at least 2 of these per agent.  Sub-3 ceiling is the design intent. |
| Open-question 7a (augmented system) | **Included** | Forces agent to probe whether its termination argument generalizes.  First drafts rarely re-check; a second iteration catches this as a disclosed gap. |

---

## 6. Task-framing drift vs Cycles #1–#5

| Aspect | Cycle #1 | Cycle #2 | Cycle #3 | Cycle #4 | Cycle #5 | Cycle #6 |
|---|---|---|---|---|---|---|
| Domain | Elementary functions | Euclidean constructions | Register machines | Combinator reduction — cardinality | Combinator reduction — confluence | **List/length TRS — confluence + termination** |
| Domain class | Continuous analysis | Discrete geometry | Discrete sequential computation | Pure syntactic reduction (minimization) | Pure syntactic reduction (semantic property) | **Term rewriting (dual semantic properties)** |
| Primitive family cardinality | ~34 | 2 | 11 | 13 | 13 | **6 symbols + 5 rules** |
| Central-question shape hint | "single binary + single constant?" | "Is one of the two enough alone?" | "single fused instruction?" | "single primitive + application?" | "Is R confluent?" | **"Is R both confluent AND terminating?"** |
| Number of verdict obligations | 1 | 1 | 1 | 1 | 1 (+ sub-questions about subsets) | **2 (Q1 confluence + Q2 termination)** |
| Expected answer form | 1 binary + 1 constant | 1 primitive | 1 fused instruction | 1 combinator | Confluent | **Confluent AND terminating** |
| A1 mitigation strength | Low | Low | Medium-high | Medium-high (14 banned) | High (20 banned) | **High (28 banned)** |
| Rubric max | 27 | 27 | 27 | 30 | 30 | **30** |
| First-draft ceiling | high | high | medium-high | medium (A: 22/30) | high (A: 28/30, both at R1-R9 = 27/27) | **medium (A: 21-25/30 expected; ≥ 2 non-R10 axes at band 2)** |

Cycle #6 is the first cycle with **two independent verdict obligations**.
The design hypothesis: first drafts will treat Q1 and Q2 as variants of
the same proof discipline and conflate them at §2; a second iteration
will separate them cleanly, closing R2 and R6 gaps.  The intended non-R10
delta is +1 to +3 (on at least one of R2, R3, R6).

---

## 7. R4 semantic adjustment for Cycle #6 (ROOT-only scorer note)

The R4 axis in `judgment-rubric.md` is phrased generically.  For Cycle
#6 (two verdict obligations), the band semantics are:

- 0: no verdict committed on either obligation.
- 1: tentative commitment on at most one obligation; the other is
  hedged ("probably terminating but I haven't shown it").
- 2: firm commitment on one obligation (Q1 or Q2) but not the other,
  or firm commitments on both but one is discharged by hand-wave.
- 3: firm commitments on **both** Q1 and Q2 with rigorous discharge of
  each.  The discharges may share infrastructure but must be
  identifiable as separate arguments in §4.

This adjustment is documented here (not ported to `judgment-rubric.md`
yet) because it is Cycle #6-specific.  If Cycle #7 reuses the multi-
obligation framing, it should be generalized in the rubric per ROOT's
cycle-close improvement protocol.

---

## 8. B `/refine` scorer-evolution note (carried forward)

Cycle #3 G5 polarity (hidden circularity < disclosed gap + named
limitation < closed proof) + Cycle #4 R10 iteration-depth internal
analog + Cycle #5 soft-priority gap tracking (seed-12) all remain in
force.  Cycle #6 additions:

- **Vacuous-audit trigger.** The updated R10 band-0 / band-1 boundary
  implies that a B-internal evaluator must name at least one concrete
  gap per iteration for that iteration to count for R10 ≥ 1.  An
  evaluator report with `gaps: []` on a non-trivial deliverable is
  equivalent to no evaluation — R10 caps at 0.  B's `/refine` (or
  its manual substitute) should treat an empty-gaps evaluator output
  as a signal to run a second, harsher pass, not as "ready to ship".
- **Two-obligation gap categorization.**  For Cycle #6 specifically,
  gaps should be tagged Q1 (confluence), Q2 (termination), or Q0
  (shared-infrastructure) so the iteration trace shows which
  obligation each iteration addressed.  Cycle #5 seed-12's priority-
  numbered tracking extends naturally to obligation-tagged tracking.

---

## 9. B `/refine` firing expectation (unchanged)

Per `projects/b/CLAUDE.md` §4.3 (/refine mandatory for reasoning
deliverables without a fixed correctness oracle): Cycle #6 is such a
deliverable.  B must fire `/refine` or an equivalent manual iteration
with on-disk trace for the cycle to count as apples-to-apples.

---

## 10. Cross-cycle persistence seed (Cycle #6 — augmentation expected)

`projects/b/agent-memory-seed/strategies.jsonl` carries 12 KEEP
entries (seed-01 through seed-12 from Cycles #4–#5).  Expected
Cycle #6 augmentation candidates (for post-cycle ROOT harvest):

- **Two-obligation separation strategy:** "When a task has k
  independent verdict obligations, structure §2 method and §4
  verdict as k clearly-separated sub-sections; do not share a single
  narrative flow across obligations."
- **Polynomial-interpretation derivation strategy:** "For a
  termination proof via polynomial interpretation, derive the
  coefficients by forcing strict decrease on each rule (one
  inequality per rule) and solving the resulting coefficient
  constraints; do not guess-and-check."

These will be harvested after B's Cycle #6 run via the same
`docker exec claude-meta-autoagent-b cat .claude/agent-memory/
skills/strategies.jsonl` + dedupe + commit path as Cycles #4–#5.
If Cycle #6 B does not produce novel KEEP entries, the seed stays
at 12.  Forward-check at cycle launch: `docker exec
claude-meta-autoagent-b ls /workspaces/agent-memory-seed/` shows
strategies.jsonl and README.md.

---

## 11. Oracle catalogue pointer (Cycle #6)

Cycle #5's `scripts/meta/oracles/combinator-reducer.py` is NOT
directly applicable to this TRS (different signature).  For Cycle
#6, no new ROOT-side oracle is being added pre-cycle — the signature
is simple enough that both A and B can build their own TRS
simulator (≤ 5 rules, ≤ 6 operators).  Proof-auditor will perform
R6 / R9 trace verification by reading the ARGUMENT.md's own worked
examples and confirming them against the stated rules.

If Cycle #6 JUDGMENT surfaces a post-hoc need for a TRS-oracle
(e.g., several incorrect worked examples slipped through), a
`scripts/meta/oracles/trs-reducer.py` will be added in Cycle #7
pre-cycle.  For now: textual trace verification by the auditor is
the M.O., and the auditor's `method: textual` tag on R6 / R9
signals this transparently.
