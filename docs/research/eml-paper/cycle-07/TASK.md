# Cycle 07 — TASK definition (ROOT-only)

**Cycle purpose.** Cycle #6 JUDGMENT §4 diagnosed that Cycles #5–#6
both ceilinged at R1–R9 = 27/27 on domains where every positive
verdict was individually tractable on first principles.  The R10 axis
was the sole architecture-discriminator at Δ = +2 for two consecutive
cycles.  The Cycle #5 JUDGMENT §5 carry-over
`M5.1-task-ceiling-overshoot`, rebadged in Cycle #6 as
`M6.1-task-ceiling-overshoot-recurrence`, is the primary structural
defect this cycle addresses.

Cycle #7 attacks this on two axes simultaneously:

1. **Rubric tightening on R2 / R3 / R7 / R8** — the band-3 criteria
   for these axes have been ported from the Cycle #6 evidence
   (`band-3-tightening-v1.md`) into `docs/research/eml-paper/judgment-rubric.md`:
   - R2 band-3 now requires **named, separately-discharged sublemmas**
     when the deliverable uses distinct proof tools (conflated proofs
     max at band 2).
   - R3 band-3 now requires **auditable tabular form** when the
     enumeration has finite tractable support (prose enumeration of
     a closeable finite set maxes at band 2).
   - R7 band-3 now requires **≥ 4 examples OR ≥ 3 orthogonal
     failure/success modes** (example counts of 3 with overlapping
     coverage max at band 2).
   - R8 band-3 now requires **at least one structural disclosure**
     (parametric impossibility, coefficient contradiction,
     dimensional argument) rather than single-instance case
     exhibition (all-case-exhibition open-question sections max at
     band 2).
2. **Domain selection with non-positive verdicts** — the cycle's TRS
   contains at least one question whose correct verdict is a
   *negative* claim requiring a *concrete counter-construction*
   (divergent pair, infinite reduction sequence).  Hand-waving
   resistance: "the system is non-confluent because rules ρ_i and
   ρ_j overlap" fails mechanical verification unless the agent
   exhibits a specific ground term `t` and both reduction sequences
   that reach distinct normal forms.

Cycle #7 also applies two rubric-evolution codifications from Cycle
#6 JUDGMENT §7 defect-resolution table, now promoted from CONDITIONAL
to closed band text:

- **M6.2 (R10 band-0/1 second edge).**  A deliverable that emits a
  single ARGUMENT.md draft + a post-hoc audit naming gaps that are
  ALREADY DISCLOSED in the same single-shot draft scores **band 0**,
  not band 1.  Rationale: the audit is a ritual confirmation of
  self-disclosure, not a closure-producing iteration.
- **M6.3 (R10 band-2/3 evaluator-report substitution).**  Band 3
  accepts, in place of a second `.eval-report-*.json`, any one of:
  (a) an independent oracle output that mechanically confirms closure,
  or (b) a committed diff artefact separate from the deliverable
  (e.g., `gap-closure-check.json`) that mechanically shows per-gap
  closure.  Self-attestation inside the deliverable's own front
  matter is **not** sufficient.

Both M6.2 and M6.3 are now part of `judgment-rubric.md` R10's
band-boundary sub-sections.

---

## 1. Task prompt delivered to A and B

Both sub-agents receive identical text via
`scripts/meta/delegate-sub.sh <key>`.  `scripts/meta/paper-leak-audit.sh`
pattern set is checked on the GOAL before launch.

```
TASK: Confluence, weak normalization, and strong normalization of a
small term-rewriting system with choice

You are given a term-rewriting system R over the signature Σ below.
Terms are built from Σ; variables are written xs, ys, x, y, z.
Application is the standard tree-style term formation.

  Signature Σ:
    Nullary constructors:   0,  nil,  a
    Unary constructors:     s
    Unary defined:          len,  f
    Binary constructor:     cons
    Binary defined:         c

  Rules R:
    ρ1:  len(nil)                → 0
    ρ2:  len(cons(x, ys))        → s(len(ys))
    ρ3:  c(x, y)                 → x
    ρ4:  c(x, y)                 → y
    ρ5:  f(x)                    → f(s(x))
    ρ6:  f(x)                    → nil

Reduction → is the least relation on terms that contains R (matching
LHS anywhere in a term rewrites that subterm to the corresponding RHS)
and is closed under contexts.  ↠ is the reflexive-transitive closure
of →.

You must settle ALL THREE of the following for R:

Q1. CONFLUENCE.  Is R confluent?  That is, for every term t and every
    pair of reduction sequences t ↠ u and t ↠ v, does there always
    exist a term w with u ↠ w and v ↠ w?  EITHER (a) prove R is
    confluent by enumerating every critical pair and closing each;
    OR (b) exhibit a specific closed term `t` and two reduction
    sequences `t ↠ u` and `t ↠ v` where `u` and `v` are BOTH normal
    forms (irreducible) with `u ≠ v`.  Provide the explicit
    step-by-step derivation for both reductions, citing the rule used
    at each step.

Q2. WEAK NORMALIZATION.  Is R weakly normalizing — that is, does
    every closed term over Σ have at least ONE reduction sequence
    that terminates at a normal form?  EITHER (a) sketch a reduction
    strategy that, applied to any closed term, terminates in finitely
    many steps, AND argue why your strategy terminates on every
    closed term; OR (b) exhibit a specific closed term `t` such that
    every reduction sequence starting from `t` is infinite (no
    terminating path exists from t).

Q3. STRONG NORMALIZATION.  Is R strongly normalizing — that is, does
    EVERY reduction sequence terminate?  EITHER (a) prove termination
    by exhibiting a well-founded measure that strictly decreases
    under every rule application (including when the rule fires inside
    an arbitrary context), and argue the measure is indeed
    well-founded; OR (b) exhibit a specific closed term `t₀` and an
    infinite reduction sequence `t₀ → t₁ → t₂ → t₃ → …`, citing the
    rule applied at each step and making the pattern explicit enough
    that the sequence is visibly unbounded.

At least two of Q1/Q2/Q3 admit non-positive verdicts on this specific
R; at most one admits a positive verdict.  The deliverable must name
which verdicts it commits to.  Hand-waving a non-positive verdict
("the system is non-confluent because ρ3 and ρ4 disagree") is
explicitly insufficient — the rubric requires a *specific witness*
(a concrete term `t` and the full reduction traces).

Your deliverable: a self-contained argument, written to
`task/ARGUMENT.md` in your working directory.  It must include:

  1. MOTIVATION.  For each of Q1, Q2, Q3, describe structural
     features of R that make each property plausible or implausible.
     Cite precedents from adjacent algebraic, logical, or
     computational domains that you reason about from first
     principles — for example, non-deterministic choice in process
     algebra, lazy-vs-eager evaluation in functional programming,
     unbounded recursion without termination bound.  Derive the
     intuitions; do not name the techniques.

  2. METHOD DESIGN — with THREE sub-sections, one per question:

     §2.1 Confluence method.  Given a candidate TRS, how do you (a)
     identify potential counter-examples via overlap / critical-pair
     analysis, (b) close confluence when no counter-example is found,
     (c) prove non-confluence when a non-joining critical pair is
     found (hint: both reducts must reach distinct normal forms, not
     merely different terms that might later join).

     §2.2 Weak normalization method.  Given a candidate TRS, how do
     you (a) construct a reduction strategy whose termination on
     every closed term you can argue for by structural induction or
     an equivalent well-founded scheme, (b) identify specific terms
     that have no terminating reduction sequence (when WN fails).
     A WN proof may differ from an SN proof because WN only requires
     that SOME reduction terminates; rules that create infinite
     sequences are compatible with WN as long as another rule
     unconditionally provides a path to a normal form.

     §2.3 Strong normalization method.  Given a candidate TRS, how
     do you (a) construct a well-founded measure that strictly
     decreases under every rule application (including context-
     closure via monotonicity), (b) exhibit an infinite reduction
     sequence when SN fails, making the repeating pattern
     structurally visible.

     The three methods may share infrastructure (term-algebra
     reasoning, induction over term size) but must not be conflated.
     Do not claim "WN because SN" without separately proving SN; do
     not claim "not SN" without exhibiting an infinite sequence.  Do
     not claim "non-confluent because WN and SN differ"; the
     implication does not hold for arbitrary TRSs.

     If you use distinct proof tools across the three questions
     (e.g., critical-pair analysis for Q1, reduction-strategy
     argument for Q2, polynomial measure for Q3), each tool should
     be stated as a **named sublemma** in §2 and discharged
     separately; the main arguments in §4 cite the sublemma rather
     than re-proving it inline.

  3. PROGRESSIVE DERIVATION — with three interleaved strands:

     §3.1 Critical-pair enumeration for Q1.  List every pair (ρᵢ,
     ρⱼ) of rules and every non-variable position in ρᵢ's LHS where
     ρⱼ's LHS unifies with ρᵢ's subterm at that position.  For each
     such overlap, write the critical pair as two reducts of the
     most-general overlap term and dispose of it (trivially
     joinable, head-mismatch impossible, non-unifiable, or
     non-joining with distinct normal-form reducts).  When the
     enumeration has a finite, tractable support (six rules × six
     rules × ≤ 2 non-variable positions per rule = a 36–72 cell
     grid), a **tabular presentation** with one row per (ρᵢ, ρⱼ,
     position) triple and a disposition column is preferred — this
     is auditable at a glance whereas a prose enumeration is not.

     §3.2 Reduction-strategy construction for Q2.  Define a
     reduction strategy (e.g., a "prefer ρ6 at every f-subterm"
     rule, or a leftmost-outermost with branch-pruning discipline).
     For each of the 6 rules, argue that your strategy makes
     progress (a step-by-step reduction in some well-founded
     measure visible to the strategy) on every closed term where
     the rule could fire.  If you claim WN fails, exhibit a
     specific term with no terminating reduction and argue
     exhaustively that no rule application reaches a normal form
     from it.

     §3.3 Measure-construction for Q3.  State your chosen measure
     (or exhibit an infinite reduction and argue no measure can
     witness termination).  If you claim SN holds, for each of the
     6 rules verify strict decrease showing the arithmetic; if you
     claim SN fails, exhibit the infinite reduction sequence
     t₀ → t₁ → t₂ → … citing the rule used at each step and
     arguing (by induction on the pattern) that the sequence is
     unbounded.

  4. FINAL VERDICT STRUCTURE.

     §4.1 Q1 answer.  Either "R is confluent" (with the full CP
     closure table as evidence) or "R is NOT confluent" (with the
     concrete divergent pair and its two reduction traces as
     evidence).

     §4.2 Q2 answer.  Either "R is weakly normalizing" (with the
     reduction strategy and its progress argument as evidence) or
     "R is NOT weakly normalizing" (with the concrete term having
     no terminating reduction and the argument that every path from
     it is infinite).

     §4.3 Q3 answer.  Either "R is strongly normalizing" (with the
     measure and strict-decrease proof as evidence) or "R is NOT
     strongly normalizing" (with the concrete infinite reduction
     sequence as evidence).

     §4.4 Cross-question relationships.  Which of the classical
     implications hold on R?  (SN ⇒ WN; confluence + WN ⇒ unique
     NFs when they exist; non-confluence does not imply
     non-termination.)  Derive any implication from first
     principles in the step where you invoke it — do not cite it by
     classical name.

  5. VERIFICATION STRATEGY.  How do you confirm the claims hold?
     Options include: (a) exhaustive critical-pair enumeration
     with each closure traced explicitly; (b) symbolic arithmetic
     per-rule strict decrease for the Q3 measure; (c) **an
     executable simulator** that enumerates reductions from a test
     suite of closed terms, verifies each claimed normal form IS
     a normal form (no rule applies), verifies each non-joining
     critical pair actually produces distinct NFs via different
     reduction sequences, and mechanically re-traces any claimed
     infinite sequence for a bounded number of steps to confirm
     the pattern.  **Worked executable-oracle verification, if
     performed, counts as a R6 = 3 indicator alongside any
     trace-argument path.**  Your oracle should, in particular,
     mechanically verify any non-positive-verdict witness (divergent
     pair and/or infinite reduction sequence) so that hand-waving
     is not possible — the rubric specifically requires concrete
     counter-constructions for non-positive verdicts.

  6. WORKED EXAMPLES — exhibit AT LEAST FOUR distinct reduction
     scenarios.  Each example should stress-test a *different* axis
     of the deliverable's claim; two examples that overlap in
     success / failure mode count as one.  Suggested orthogonal
     categories (adapt as needed):
     (a) a term demonstrating the divergent pair for Q1 (with two
         full reduction traces reaching distinct NFs);
     (b) a term with WN via a specific reduction strategy but
         without SN (both a terminating reduction AND an infinite
         reduction from the same starting term, if applicable);
     (c) a term whose length-reduction terminates deterministically
         (stress-testing the positive portion of Q2, if Q2 is
         positive);
     (d) a term exhibiting the infinite reduction for Q3 with the
         repeating pattern visible.
     Give the full reduction traces for each example and, where
     relevant, any measure value you are tracking.

  7. OPEN QUESTIONS AND KNOWN LIMITATIONS.  At minimum, include:
     (a) Under what rule-removal or rule-modification could R be
         made confluent?  If rule-removal of a specific rule (e.g.,
         ρ4) trivially achieves this, disclose; if you can argue
         parametrically that NO single-rule removal restores
         confluence without changing the system's expressiveness,
         state the structural reason (this is a parametric
         impossibility disclosure, stronger than a case exhibition).
     (b) Whether your WN strategy is unique, or whether multiple
         reduction strategies each succeed.  If you can
         characterize the CLASS of strategies that work
         (parametrically), that is stronger than exhibiting one.
     (c) Whether your SN claim (or non-SN witness) is sensitive to
         the specific measure you chose.  If you can show a
         parametric family of measures that ALL would fail (for
         SN-failing cases), or that all measures in a parametric
         family succeed (for SN-holding cases), that is
         structurally richer than a single-instance measure.
     (d) Whether the relationship between Q1 / Q2 / Q3 for THIS R
         is an instance of a more general pattern (does every TRS
         with a choice rule ρ3/ρ4 fail confluence?  does every TRS
         with an `f(x) → f(s(x))` rule fail SN?  are these claims
         parametric in the rule shape, or contingent on the rest
         of R?).

     Open-question sections that consist entirely of
     single-instance case exhibitions (e.g., "here's another TRS
     that is also non-confluent") are weaker than sections
     including at least one structural / parametric disclosure
     (e.g., "no single-rule removal from R restores confluence
     because ..., therefore ρ3+ρ4 jointly encode an essentially
     non-confluent choice primitive").  The rubric's R8 band-3
     now requires at least one structural disclosure; case-
     exhibition-only sections max at band 2.

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
    surname), Church-Rosser property, Tait-Martin-Löf technique,
    Takahashi translation, Newman's lemma, Knuth-Bendix, Hindley-
    Rosen, Dershowitz, Manna-Ness, recursive path order, RPO,
    lexicographic path order, LPO, multiset path order, MPO,
    dependency pair method, dependency pairs, Kamin, Lévy,
    Kamin-Lévy, Huet's critical pair lemma, Huet, Klop (as a
    person's surname), Barendregt (as a person's surname), Girard
    (as a person's surname), Tait's computability method,
    Plotkin (as a person's surname), de Bruijn (as a person's
    surname).  You MAY use the structural vocabulary "critical
    pair", "overlap", "joinable", "confluent", "terminating",
    "weakly normalizing", "strongly normalizing", "normal form",
    "well-founded", "measure", "interpretation", "monotonic",
    "strictly decreasing", "rewrite", "rewriting", "redex",
    "reduction strategy", "leftmost-outermost", "innermost",
    "head reduction", and all symbol letters (0, s, nil, cons,
    len, c, f, a, xs, ys, x, y, z, ρ₁…ρ₆) as-is.  If you
    recognize the canonical technique under one of the banned
    names, work around the name and derive the structure yourself.

  - Iteration affordance (important).  If your agent configuration
    provides an iteration, self-audit, or refinement mechanism
    (whatever its invocation convention), you are encouraged to use
    it and to persist the iteration trace to your working directory
    at any path you choose (for example, `task/attempts/attempt-01.md`,
    `task/iterations/iter-01.md`, `task/.eval-report.json`).  ROOT
    will cite these paths in scoring.  If your configuration does
    not provide such a mechanism, a single-shot argument is a
    legitimate response and you should simply deliver it.  Do not
    simulate iteration; if you iterate, actually iterate — each
    iteration's evaluator report must name ≥ 1 disclosed gap for
    that iteration to count as closure-producing (per the R10
    band definitions).  NOTE: an audit that names only gaps ALREADY
    DISCLOSED in the deliverable's own open-questions / limitations
    section does not count as disclosure-beyond-the-single-shot;
    the R10 band-0/1 boundary now treats this as band 0.

  - Triple obligation (critical).  All three of Q1, Q2, Q3 must
    receive rigorous treatment.  A brilliant Q1 proof with a
    hand-waved Q2 / Q3 answer, or vice-versa, will score
    materially lower than a balanced treatment.  If one obligation
    is harder for you than the others, disclose the asymmetry and
    spend the remaining rigor budget on closing the hardest gap.

  - Counter-construction rigor (critical).  For any non-positive
    verdict (R is NOT confluent, R is NOT WN, R is NOT SN), the
    argument MUST exhibit a SPECIFIC closed term and a SPECIFIC
    reduction sequence (or pair of sequences) demonstrating the
    failure, with the rule applied at each step explicitly named.
    "Handwave: the system is non-confluent because ρ3 and ρ4
    project differently" is insufficient — you must exhibit a
    term `t`, a reduction `t ↠ u`, a reduction `t ↠ v`, verify
    `u` and `v` are normal forms (no rule of R applies), and
    confirm `u ≠ v`.  The rubric's R9 requires correct verdicts
    with rigorous discharge; non-positive verdicts without
    witnesses are not "correct" for R9 purposes.
```

---

## 2. Ideal answer (ROOT-only)

R is **NOT confluent**, **IS weakly normalizing**, and **NOT strongly
normalizing**.  The ideal path from first principles:

### 2.1 Confluence (Q1) — Non-confluent

**Critical-pair enumeration** (all 36 ordered pairs × ≤ 2 non-variable
positions = 48 cells total):

- All (ρ_i, ρ_j) pairs with different LHS-head symbols:
  head-mismatch, no CP.
- ρ1 vs ρ2: both head `len`, but position 1 differs (`nil` vs
  `cons(x, ys)`) — not unifiable at position 1, no CP.
- ρ1 vs ρ1, ρ2 vs ρ2: self-overlap, trivially same reduct.
- ρ3 vs ρ4 at root: unifiable trivially (matching variables rename).
  Critical pair: (x, y) with x, y fresh.  This CP does NOT join
  because x and y are distinct free variables; substituting ANY
  closed distinct pair (e.g., x := 0, y := nil) gives distinct
  normal forms.  **NON-JOINING CP.**
- ρ3 vs ρ3, ρ4 vs ρ4: self-overlap, trivially same reduct.
- ρ5 vs ρ6 at root: CP (f(s(x)), nil).  f(s(x)) → nil via ρ6 (fresh
  application of ρ6 at root).  Joinable at `nil`.
- ρ5 vs ρ5, ρ6 vs ρ6: self-overlap, trivially same reduct.
- Inner overlaps at ρ1 position 1 (`nil`): no rule has head `nil`
  in its LHS.  No CP.
- Inner overlaps at ρ2 position 1 (`cons(x, ys)`): no rule has head
  `cons`.  No CP.

**Divergent-pair witness.**  Take `t = c(0, nil)`.
- `t →ρ3 0`.  0 has no outgoing rule (no rule's LHS head is `0`);
  0 is a normal form.
- `t →ρ4 nil`.  nil has no outgoing rule; nil is a normal form.
- `0 ≠ nil` (distinct constructors), so the reductions `t ↠ 0` and
  `t ↠ nil` witness non-confluence.

### 2.2 Weak Normalization (Q2) — WN holds

**Strategy:** at every step, if the term contains an `f(t)` subterm,
rewrite the OUTERMOST `f`-subterm using ρ6 (`f(x) → nil`) at the
outermost applicable position.  Otherwise apply ANY available rule.

**Termination argument.**  Let `|t|_f` = number of `f`-subterm
occurrences in `t`.  Under the strategy, each ρ6 application strictly
decreases `|t|_f` by at least 1 (the rewritten `f`-redex disappears;
ρ6's RHS `nil` contains no `f`).  Within segments with no `f`-subterm,
the only rules that apply are ρ1, ρ2, ρ3, ρ4:
- ρ1 strictly decreases the term size (LHS 2 nodes → RHS 1 node).
- ρ2 keeps size linear in `ys` size (`len(cons(x, ys))` → `s(len(ys))`,
  both "one wrapper + len-subterm").  Applied finitely by structural
  induction on the length of the list `ys`.
- ρ3 and ρ4 strictly decrease size (c(x, y) → x or y, one argument
  disappears).

Composing: the strategy's termination is by lexicographic induction
on (`|t|_f`, term-size), both well-founded on ℕ.  Hence every closed
term reaches a normal form via the strategy.  **WN holds.**

### 2.3 Strong Normalization (Q3) — NOT SN

**Infinite-reduction witness.**  Take `t₀ = f(a)`.  Apply ρ5 at the
root at each step:

- `t₀ = f(a) →ρ5 f(s(a)) = t₁`
- `t₁ = f(s(a)) →ρ5 f(s(s(a))) = t₂`
- `t₂ = f(s(s(a))) →ρ5 f(s(s(s(a)))) = t₃`
- …
- `tₙ = f(sⁿ(a)) →ρ5 f(sⁿ⁺¹(a)) = tₙ₊₁`

Each step applies ρ5 at the root with `x := sⁿ(a)`.  The `s`-depth
strictly increases by 1 per step; since ℕ is unbounded, no tₙ equals
any previous tᵢ, and the sequence is infinite.

Rigorously: `t_n` contains exactly `n` copies of `s` wrapping one
`a` wrapped in one `f`, with no other subterms.  ρ5's applicability
at the root of `f(sⁿ(a))` is immediate (LHS `f(x)` matches with
σ = {x ↦ sⁿ(a)}).  **Not SN.**

### 2.4 Cross-question relationships (ideal §4.4)

- SN ⇒ WN holds for any TRS (if every reduction terminates, then
  some reduction terminates).  Derivable from first principles: if
  every sequence is finite, then in particular some sequence is
  finite; its final term is a normal form.
- WN + confluence ⇒ unique normal form: classical derivation.
  R is WN + non-confluent, so unique NFs DO NOT hold.  Concrete
  example: `c(0, nil)` has two distinct NFs 0 and nil.
- Non-confluence does NOT imply non-SN; R is non-confluent with SN
  failing independently.  Non-SN does NOT imply non-confluence; one
  could have a confluent non-SN system (e.g., a pure increasing-size
  rule `a → s(a)` alone is confluent and non-SN).

### 2.5 What can go wrong in first drafts

- **Missed non-joining CP.**  Agents who enumerate CPs casually
  might miss that ρ3 vs ρ4 at root gives (x, y) — a non-joining CP
  in the symbolic sense because x and y are distinct free variables.
  Instantiated to closed terms, this gives distinct NFs.
- **Hand-wave non-confluence.**  "R is non-confluent because ρ3 and
  ρ4 have the same LHS but different RHSs" is hand-waving; the
  rubric demands a specific closed `t` with two specific NF reducts.
- **Missed the WN argument.**  Agents might conflate WN with SN and
  claim "since SN fails, WN likely also fails" — which is backward
  reasoning; WN asks only for SOME terminating path, which the ρ6
  rule unconditionally provides for any f-term.
- **Miss the SN witness rigor.**  Claiming "f(a) has an infinite
  reduction via ρ5" without spelling out the sequence and the rule
  applied at each step fails R9's rigorous-discharge requirement.
- **Conflate §2 methods.**  Writing Q1/Q2/Q3 as a single unified
  "normalization analysis" prose section, without named sublemmas
  for each question's tool, triggers R2 band-3 tightening cap at 2.
- **Prose CP enumeration.**  With 48 cells of support, a prose
  enumeration triggers R3 band-3 tightening cap at 2.
- **Case-exhibition-only open questions.**  Agents who answer §7(a)
  "the system could be made confluent by removing ρ4" without
  exploring whether ANY single-rule removal suffices parametrically
  trigger R8 band-3 tightening cap at 2.

**R9 binary shape for this cycle:** R9 = 3 iff the ARGUMENT produces
correct verdicts on ALL THREE of Q1 (non-confluent), Q2 (WN), Q3
(NOT SN), with rigorous discharge for each (CP enumeration +
divergent-pair witness for Q1; reduction strategy + well-founded
argument for Q2; infinite-sequence witness for Q3).  Partial credit
is not allowed for R9.

---

## 3. Paper-identifying keywords for this cycle (informational)

These must NOT appear in any TASK prompt, ROOT→sub delegation
payload, or the delivered prompt.  They are allowed in this
ROOT-only file because it is never mounted into A or B.

**Inherited from Cycles #5–#6 (28 entries):**

- "SKI calculus" / "SKI"
- "SK calculus"
- "BCKW" / "BCIW"
- "Iota combinator" / "ι" (in combinator-name context)
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
- "Tait–Martin-Löf" / "Tait-Martin-Löf"
- "Takahashi translation" / "Takahashi parallel reduction"
- "Newman's lemma"
- "Knuth–Bendix" / "Knuth-Bendix" / "Knuth-Bendix completion"
- "Hindley–Rosen" / "Hindley-Rosen lemma"
- "Dershowitz" (surname)
- "Manna-Ness" / "Manna–Ness"
- "recursive path order" / "RPO"
- "lexicographic path order" / "LPO"
- "multiset path order" / "MPO"
- "dependency pair method" / "dependency pairs"
- "Kamin-Lévy" / "Kamin–Lévy"
- "Huet's critical pair lemma" / "Huet" (surname)

**Cycle #7 domain-specific additions (6 entries):**

- "Klop" (surname; classical TRS non-confluence examples author)
- "Barendregt" (surname; lambda calculus / normalization author)
- "Girard" (surname; reducibility-candidates / SN method author)
- "Tait's computability method" / "Tait" (SN by computability,
  surname clash with Tait-Martin-Löf but stands alone)
- "Plotkin" (surname; CBV/CBN + reduction strategies author)
- "de Bruijn" (surname; notation + normalization author)

Total Cycle #7 banned-identifier list: **34 entries** (28 inherited
+ 6 new; "Tait" appears in both the inherited Tait-Martin-Löf pair
and the new standalone "Tait's computability method" — enforcement
covers both by word-level "Tait" grep).

The existing `paper-leak-guard.sh` reversed-form patterns cover the
base paper keyword set; the 34 Cycle #7 names are enforced via
(a) explicit listing in §1's delegation prompt, (b) post-cycle
`paper-leak-audit.sh` base-pattern scan, (c) an extended post-cycle
grep for all 34 names (§4 below).  No reversed-form blocklist
extension is performed — symmetric-zero-change convention on
`projects/a/` applies.

---

## 4. Post-cycle leak audit extension (Cycle #7)

Run the base `scripts/meta/paper-leak-audit.sh` (blocks the eml
paper keyword set, still applicable) on each ARGUMENT.md.  Then
additionally grep each ARGUMENT.md for each name in §3:

```
grep -iE 'ski calculus|sk calculus|bckw|bciw|iota combinator|jot|unlambda|binary lambda calculus|\bblc\b|x combinator|xi combinator|\bzot\b|schönfinkel|schonfinkel|haskell curry|alonzo church|barkley rosser|turing.s universal combinator|church.rosser|tait.martin.löf|tait.martin-lof|takahashi|newman.s lemma|knuth.bendix|hindley.rosen|dershowitz|manna.ness|recursive path order|\brpo\b|lexicographic path order|\blpo\b|multiset path order|\bmpo\b|dependency pair|kamin.lévy|kamin.levy|huet|\bklop\b|barendregt|girard|\btait\b|plotkin|de bruijn' projects/a/task/ARGUMENT.md
grep -iE 'ski calculus|sk calculus|bckw|bciw|iota combinator|jot|unlambda|binary lambda calculus|\bblc\b|x combinator|xi combinator|\bzot\b|schönfinkel|schonfinkel|haskell curry|alonzo church|barkley rosser|turing.s universal combinator|church.rosser|tait.martin.löf|tait.martin-lof|takahashi|newman.s lemma|knuth.bendix|hindley.rosen|dershowitz|manna.ness|recursive path order|\brpo\b|lexicographic path order|\blpo\b|multiset path order|\bmpo\b|dependency pair|kamin.lévy|kamin.levy|huet|\bklop\b|barendregt|girard|\btait\b|plotkin|de bruijn' projects/b/task/ARGUMENT.md
```

"Confluence" / "confluent" / "weakly / strongly normalizing" /
"critical pair" / "overlap" / "joinable" / "reduction strategy" /
"leftmost-outermost" / "innermost" / "head reduction" / "normal
form" / "well-founded" / "measure" / "monotonic" / "strictly
decreasing" — generic structural vocabulary, **not** name-
identifying; do not disqualify on these.  Bare letters (Σ, ρ,
variable names xs, ys, x, y, z) are symbols from the prompt,
permitted.

---

## 5. Hint-drift record (required by CLAUDE.md §6.7 step 1)

| Hint | Decision | Rationale |
|---|---|---|
| 3-question framing (Q1 confluence + Q2 WN + Q3 SN) as three *independent* obligations | **Included** | Cycle #6's two-obligation framing did not force sub-3 R1-R9 axes.  Three obligations with mixed verdicts (non-pos + pos + non-pos) force structural separation at §2 (three sublemma tools), §3 (three enumeration strands), §4 (three verdicts).  Conflation at §2 is the most common first-draft failure mode; the rubric's R2 band-3 tightening penalises exactly this. |
| Non-positive verdicts on Q1 and Q3 requiring concrete counter-construction | **Included and explicitly required** | Cycle #6 JUDGMENT §5 "Implication for Cycle #7" recommended non-positive-verdict domains forcing counter-exhibition.  First drafts often hand-wave "non-confluent because overlap" without providing a specific ground term; the prompt demands the witness.  Mechanically verifiable by simulator: the witness term and both reductions can be re-executed, the NF-ness of the reducts re-checked. |
| Tabular CP enumeration preferred in §3.1 | **Included** | R3 band-3 tightening (Cycle #7 pre-cycle port) promotes tabular to threshold when the enumeration has finite tractable support.  A 36–48 cell CP grid over 6 rules is exactly the target shape. |
| Orthogonal worked examples preferred in §6 | **Included** | R7 band-3 tightening (Cycle #7 pre-cycle port) requires ≥ 4 examples OR ≥ 3 orthogonal.  Prompt suggests 4 orthogonal categories (divergent-pair, WN-but-not-SN, len-termination, non-SN witness) so agents who hit ≥ 4 naturally reach band 3. |
| Structural disclosure in §7 open questions | **Included with explicit invitation** | R8 band-3 tightening requires parametric-impossibility or coefficient-contradiction disclosure.  Prompt §7(a) explicitly invites: "if you can argue parametrically that no single-rule removal restores confluence..." — this is a hook for the structural disclosure pattern. |
| Named sublemmas required for band-3 R2 | **Explicitly invited in §2** | Prompt §2 closing paragraph explicitly says "each tool should be stated as a named sublemma".  Agents who write flowing §2 prose miss this signal and drop to band 2. |
| Counter-construction rigor required for R9 | **Explicitly stated in constraints** | Prompt's final constraint block states: "non-positive verdicts without witnesses are not 'correct' for R9 purposes".  Agents who commit to "non-confluent" without a witness lose R9. |
| "Triple obligation" emphasis | **Explicitly stated** | Ensures agents don't polish Q1 and hand-wave Q2/Q3.  Mirrors Cycle #6's "double obligation" emphasis, adapted. |
| Executable-oracle verification mention | **Included as R6 = 3 indicator** | Same as Cycle #6.  Agents must build their own TRS simulator (6-rule, 8-symbol); small enough to implement.  Oracle must mechanically verify non-positive-verdict witnesses. |
| R10 M6.2/M6.3 codification embedded in the iteration-affordance constraint | **Included as prompt note** | "An audit that names only gaps ALREADY DISCLOSED in the deliverable's own open-questions / limitations section does not count as disclosure-beyond-the-single-shot" — Cycle #6 A-R10 failure mode closed. |
| Banned names list — Cycle #7 specific additions | **Included (Klop, Barendregt, Girard, Tait, Plotkin, de Bruijn)** | These are the canonical first-reach author surnames for classical non-confluence examples, lambda calculus normalization, SN-via-reducibility, SN-by-computability, and reduction strategies.  Banning them forces first-principles reasoning. |
| Expected A first-draft ≥ 2 band-2 axes | (not stated in prompt) | ROOT expects A first-draft to drop on R2 (conflated §2), R3 (prose CP enumeration), R7 (3 overlapping examples), and/or R8 (case-exhibition open questions) — at least 2 of these.  Sub-3 ceiling is the design intent. |

---

## 6. Task-framing drift vs Cycles #1–#6

| Aspect | Cycle #6 | Cycle #7 |
|---|---|---|
| Domain | List/length TRS — confluence + termination | List/length TRS with choice — confluence + WN + SN (3 questions) |
| Domain class | Term rewriting (dual semantic properties, both positive) | Term rewriting (triple semantic properties, mixed positive/negative) |
| Primitive family cardinality | 6 symbols + 5 rules | 8 symbols + 6 rules |
| Number of verdict obligations | 2 (Q1 + Q2) | 3 (Q1 + Q2 + Q3) |
| Number of non-positive-verdict obligations | 0 | 2 (Q1 non-confluent, Q3 not-SN) |
| Rubric tightenings applied pre-cycle | R10 band-0/1 vacuous | R2/R3/R7/R8 band-3 tightened + R10 M6.2/M6.3 closed |
| Expected answer form | Confluent AND terminating | NOT confluent, WN, NOT SN |
| A1 mitigation strength | High (28 banned) | High (34 banned) |
| Rubric max | 30 | 30 |
| First-draft A expected ceiling | 27/30 (observed; ceiling failure) | 21-25/30 (≥ 2 R1-R9 axes drop to band 2 under tightening + mixed-verdict rigor) |

Cycle #7 is the first cycle with **three independent verdict
obligations** AND with **rubric tightening on non-R10 axes**.  Design
hypothesis: the tightening alone (independent of task-domain change)
would raise the Δ baseline; the non-positive-verdict domain forces
concrete counter-construction which A's hand-wave-prone first drafts
often miss.  Intended non-R10 delta: +2 to +5 (on at least two of R2,
R3, R7, R8).

---

## 7. R4 semantic adjustment for Cycle #7 (ROOT-only scorer note)

For Cycle #7 (three verdict obligations), R4 band semantics:

- 0: no verdict committed on any obligation.
- 1: tentative commitment on at most one obligation; others hedged.
- 2: firm commitments on fewer than three obligations, OR firm
  commitments on all three but at least one discharged by hand-wave
  (e.g., "non-confluent because overlap" without a divergent-pair
  witness).
- 3: firm commitments on all three obligations AND each discharged
  rigorously (CP enumeration + divergent-pair witness for Q1; WN
  argument with well-founded measure for Q2; SN measure OR
  non-SN-witness for Q3), identifiable as separate arguments in §4.

This Cycle #7 R4 adjustment generalizes Cycle #6's two-obligation
R4 adjustment (scales linearly with the number of obligations).  If
future cycles reuse multi-obligation framing, this could be ported
into `judgment-rubric.md` proper.

---

## 8. B `/refine` scorer-evolution note (carried forward)

Cycle #6 seed-13 (variable-overlap sublemma) and seed-14 (polynomial-
coefficient derivation) both apply directly: seed-13 for Q1's CP
enumeration (every ρ_i/ρ_j pair with variable positions gets
dispatched by the sublemma); seed-14 in spirit for Q3 if B attempts
an SN measure for the R-minus-ρ5 subsystem.  Cycle #7-specific
additions:

- **Non-positive-verdict gap categorization.**  For Cycle #7
  specifically, gaps should be tagged Q1 (confluence witness), Q2
  (WN strategy + progress), Q3 (SN measure or non-SN witness), or
  Q0 (shared-infrastructure).  Iteration 1's evaluator should check
  specifically whether each non-positive-verdict claim has a
  concrete witness ground term with full reduction traces; absence
  of witness caps R9 at 0 regardless of narrative quality.
- **Tightened-rubric targeting.**  B's iteration evaluator should
  check specifically (1) whether §2 has named sublemmas per tool
  (R2 tightening), (2) whether §3.1 is tabular with per-cell
  disposition (R3 tightening), (3) whether §6 has ≥ 4 examples OR
  ≥ 3 orthogonal (R7 tightening), (4) whether §7 has at least one
  structural / parametric disclosure (R8 tightening).  These four
  should be visible in any iteration's gap list.

---

## 9. B `/refine` firing expectation (unchanged)

Per `projects/b/CLAUDE.md` §4.3 (/refine mandatory for reasoning
deliverables without a fixed correctness oracle): Cycle #7 is such
a deliverable.  B must fire `/refine` or an equivalent manual
iteration with on-disk trace for the cycle to count as
apples-to-apples.

---

## 10. Cross-cycle persistence seed (Cycle #7)

`projects/b/agent-memory-seed/strategies.jsonl` carries 14 KEEP
entries (seed-01 through seed-14 from Cycles #4–#6).  Expected
Cycle #7 augmentation candidates (for post-cycle ROOT harvest):

- **Non-positive-verdict witness construction.**  "When a TRS's
  verdict is non-positive (non-confluent, non-WN, non-SN), the
  argument MUST include a specific closed-term witness.  For
  non-confluence: exhibit a ground term `t` with distinct
  normal-form reducts `u`, `v` (`t ↠ u`, `t ↠ v`) verified
  mechanically.  For non-SN: exhibit an infinite reduction sequence
  `t₀ → t₁ → t₂ → …` with the rule at each step explicit and the
  pattern argued inductively unbounded."
- **Reduction-strategy WN proof.**  "For WN (not SN), construct a
  reduction strategy (e.g., outermost-f-first) and argue its
  progress by lexicographic decrease in a derived measure; each
  rule's contribution to progress is an independent sub-lemma."

These will be harvested after B's Cycle #7 run via the same
`docker exec claude-meta-autoagent-b cat .claude/agent-memory/
skills/strategies.jsonl` + dedupe + commit path as Cycles #4–#6.
If Cycle #7 B does not produce novel KEEP entries, the seed stays
at 14.

---

## 11. Oracle catalogue pointer (Cycle #7)

Cycles #5 and #6 did not add a general TRS-oracle; the auditor
performed textual R6 / R9 trace verification by reading each
ARGUMENT.md's worked examples.  For Cycle #7, the domain is small
enough (6 rules, 8 symbols) that both A and B are expected to build
their own TRS simulator; the auditor will again perform textual
trace verification supplemented with a small ad-hoc TRS reducer
script written at audit time (inline in `/tmp/verify_*.py` style,
matching the Cycle #6 workflow).

If Cycle #7 JUDGMENT surfaces a post-hoc need for a committed
`scripts/meta/oracles/trs-reducer.py`, that can be added in Cycle #8
pre-cycle.  For now: ad-hoc auditor-side verification is the M.O.,
and the auditor's `method: textual` / `method: oracle` tag in
`rubric-audit.json` signals which axes were mechanically checked.

---

## 12. GOAL clause 5 measurement points (for JUDGMENT §4 delta analysis)

Cycle #7 GOAL clause 5 requires one of:
- (a) A's R1-R9 < 27 (≥ 2 R1-R9 axes drop to band 2 under tightening);
- (b) |A − B| ≥ 3 on the 30-point rubric;
- (c) if neither, a "tightening insufficient" root-cause analysis in
  JUDGMENT + Cycle #8 carry-over.

Design intent: A achieves sub-27 on R1-R9 by hitting ≥ 2 of
{R2 conflation, R3 prose CP, R7 non-orthogonal, R8 case-exhibition};
B's iteration catches these and reaches 26–30/30 (depending on
R10 attainment).  Δ ≥ 3 is the more likely clause-satisfaction path.
