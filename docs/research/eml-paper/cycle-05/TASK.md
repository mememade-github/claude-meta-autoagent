# Cycle 05 — TASK definition (ROOT-only)

**Cycle purpose.** Cycle #4 produced the first non-tie delta on the
R10-extended rubric (B 26 vs A 22, Δ = +4) by introducing an
iteration-sensitive axis and picking a domain (combinator
**cardinality** minimization) where the derivation-rigor / iteration-
closure gap surfaced cleanly.  Cycle #5 addresses a different concern
raised at the close of Cycle #4's §5 (comparative notes):

> "R10 will not always separate A and B — on domains where iteration
> is low-value (a first draft already reaches the ceiling on all other
> axes and iteration cannot improve it further), B might iterate
> without producing deltas. … Cycle #5 TASK design should aim at a
> domain where the first-draft's natural ceiling is between band 2 and
> band 3 — low enough that iteration pays, high enough that first
> drafts are worth iterating *from*."

And two system-level additions surfaced as Cycle #4 closed:

1. **Falsifiable evaluation layer.**  Cycle #4's JUDGMENT was
   ROOT-authored and self-contained; there was no independent check
   on ROOT's scoring.  Cycle #5 introduces step 5c (CLAUDE.md §6.7):
   after ROOT's JUDGMENT draft, a `proof-auditor` agent runs
   independently against the same rubric + deliverables and produces
   `rubric-audit.json` with an agreement-matrix.  Arbitration
   triggers on ≥1 axis ±2 bands, ≥3 any-band disagreements, binary
   axis disagreement, or total > 20 % of rubric max.
2. **Oracle catalogue.**  Cycle #4 B's own Python β-reducer
   discharged 10 trace verifications inside its evaluator; that
   reducer was internal to B's container.  Cycle #5 ports an
   equivalent reducer to `scripts/meta/oracles/combinator-reducer.py`
   as a ROOT-side (proof-auditor-accessible) artefact with a built-in
   `--selftest` that is 15/15 green at pre-cycle.  The oracle is
   advisory; the auditor may invoke it for axes where trace
   verification is machine-checkable.

Domain choice for Cycle #5: **confluence of a bounded combinator
reduction system.**  Cycle #4 asked how *small* a primitive basis can
get; Cycle #5 asks whether a given basis's reduction relation is
**confluent** — a different property of the same kind of object.
Confluence is classically one of the three "rigor traps" of rewriting
theory (the others being termination and normalization): first-draft
arguments nearly always reach for local-confluence-by-rule-inspection,
then claim confluence without handling the non-strongly-normalizing
case (where Newman-style local→global inference fails).  The correct
move is to use a parallel-reduction / diamond-property argument — which
takes real work to derive from first principles.  This places the
first-draft ceiling at band 2 on R6 (correct local-confluence check
but missed global argument) and band 2 on R2 (systematic but
incomplete), with R6 = 3 and R2 = 3 reachable by iteration that closes
the disclosed gap.  Expected A-first-draft total: R1=3, R2=2, R3=2,
R4=2 (non-R4 axis for confluence), R5=2, R6=2, R7=2, R8=2, R9=0 or 3
(binary, see §2) → 17–20 ballpark before R10.  Matches the GOAL's
17–22/27 band-2-to-3 ceiling requirement.

---

## 1. Task prompt delivered to A and B

Both sub-agents receive identical text via
`scripts/meta/delegate-sub.sh <key>`.  `scripts/meta/paper-leak-audit.sh`
pattern set is checked on the GOAL before launch.

```
TASK: Confluence of a bounded applicative-reduction system

Consider the following applicative calculus of tree-shaped terms.
A term is either (i) a primitive symbol drawn from a finite primitive
set P, or (ii) an application (M N), for M and N already terms.
Application is left-associative: (M N O) denotes ((M N) O).

The primitive set below — call it the "extended calculator" — is
equipped with a standard weak-reduction rule for each primitive.  A
single reduction step rewrites a redex (a subterm matching the
left-hand side of some primitive's rule) to its right-hand side;
reduction continues until no redex remains (if it remains).  Lower-
case letters range over arbitrary terms.

  Constants (primitive symbols with reduction rules):
    I   :  I x          → x
    K   :  K x y        → x
    S   :  S x y z      → x z (y z)
    B   :  B x y z      → x (y z)
    C   :  C x y z      → x z y
    W   :  W x y        → x y y
    M   :  M x          → x x
    Y   :  Y f          → f (Y f)
    T   :  T x y        → y x
    V   :  V x y z      → z x y
    D   :  D x y z w    → x y (z w)
    Π₁  :  Π₁ x y       → x
    Π₂  :  Π₂ x y       → y

A reduction relation is **confluent** iff for every term M and every
pair of reduction sequences M ↠ N₁ and M ↠ N₂, there exists a common
reduct P with N₁ ↠ P and N₂ ↠ P.  Equivalently, the reduction relation
has the **diamond property on its reflexive-transitive closure**: no
two diverging reduction paths are unreconcilable.

Confluence is a semantic property of the full calculus, not of a
specific term.  It can hold for a calculus that is non-terminating
(some terms reduce forever) provided the two diverging paths can
always be rejoined.  The baseline above is non-terminating (Y alone
generates divergent reductions; M applied to itself does too), so any
confluence argument here must be robust to non-termination.

Central question: is the reduction relation of the extended calculator
above confluent?  If yes, produce a complete first-principles proof.
If no, exhibit a concrete counter-example — two reductions from a
common starting term that cannot be rejoined — and characterize the
largest subset P′ ⊆ baseline whose reduction relation **is** confluent.
Is there a maximal confluent subset?  A minimal non-confluent extension?
State your claim and discharge it.

Your deliverable: a self-contained argument, written to
`task/ARGUMENT.md` in your working directory.  It must include:

  1. Motivation.  Why might confluence hold for the full baseline, or
     fail on a specific subset?  Cite precedents from adjacent
     algebraic, logical, or computational domains that you reason
     about from first principles — for example, unique-normal-form
     properties of term-rewriting systems, determinism in
     computational models, equivalence-class structure of reduction
     relations.  Explain what structural feature of the baseline rules
     makes you expect confluence to hold (or not).  Derive, do not
     name.

  2. A systematic confluence-checking procedure you design and
     justify.  The procedure should say how, given a candidate
     reduction system, you (a) identify potential counter-examples
     (e.g., critical-pair analysis, overlap detection), (b) discharge
     confluence when no counter-example is found (local-confluence
     arguments, parallel-reduction / diamond arguments, or
     termination-reduction lifts), and (c) handle the non-terminating
     case (where local confluence plus an SN argument is insufficient
     on its own).

  3. A sequence of progressively stronger confluence claims, each
     justified.  For instance: start with a single-rule system (only
     I), establish confluence trivially; add K; verify nothing new is
     broken; add S; analyze; and so on through the 13 baseline
     primitives.  At each stopping point, state (a) the claim (the
     specific subset is confluent), (b) the method used to establish
     it, (c) any disclosed gap.

  4. The confluence verdict on the full baseline.  Either (i) the full
     baseline is confluent with a rigorous proof, or (ii) the full
     baseline is not confluent with a concrete non-confluent pair of
     reductions from a common term, plus a characterization of the
     largest confluent subset.  If the argument requires extending the
     baseline with a newly-invented combinator to exhibit a concrete
     non-confluence (extending, not in the baseline), say so
     explicitly; give the invented combinator's reduction rule.  State
     your counting convention — what exactly counts as a "rule
     overlap" / a "critical pair" / a "residual" / a "parallel step"
     in your chosen technique.

  5. A verification strategy: how do you confirm the confluence claim
     holds?  Representative options: (a) exhibit diamond closure on
     every overlapping rule pair; (b) define a parallel-reduction
     relation ⇒ with the diamond property and prove it generates the
     same reflexive-transitive closure as the original →; (c) reduce
     to a known-confluent system via a translation that preserves
     reduction equivalence; (d) exhibit an executable simulator that
     enumerates reduction paths to a bounded depth for a bounded test
     suite and verifies they converge.  Name your strategy and
     discharge it.  **Worked executable-oracle verification, if
     performed, counts as a R6 = 3 indicator alongside any
     trace-argument path.**

  6. Worked examples: exhibit at least three distinct confluence
     verifications over the baseline or your chosen subset.
     Suggested candidates: (a) a critical pair of the form
     (S x y z) where x is itself a K-redex and y,z are I-redexes — two
     different reduction orders from a single term; (b) a Y-induced
     divergence (Y f reducing in multiple parallel ways) showing
     confluence holds on non-terminating terms; (c) a multi-step
     combinator application exhibiting confluence under leftmost-
     outermost vs rightmost-innermost strategies.  Give the full
     reduction traces and the common reduct.

  7. Open questions and known limitations, including: (a) whether
     your proof technique extends to strong (under-binder) reduction
     if the baseline is extended to λ-terms; (b) the relationship
     between confluence and normalization in your analysis (which
     implies which, under what conditions); (c) whether your proof
     depends on the specific choice of weak-reduction semantics
     (leftmost-outermost) or generalizes to arbitrary reduction
     strategies; (d) whether the combinator set admits a confluent
     extension that is NOT orthogonal (rules with overlapping LHS),
     and if so, what rule shape.

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
    Rosen.  You MAY use "confluence", "confluent", "diamond",
    "parallel reduction", "critical pair", "overlap", "residual",
    "normal form", "strong normalization", "weakly normalizing",
    "rewrite", "rewriting", and the letters S, K, I, B, C, W, M, Y,
    T, V, D as bare symbols.  If you recognize the canonical
    technique under one of the banned names, work around the name
    and derive the structure yourself.

  - Iteration affordance (important).  If your agent configuration
    provides an iteration, self-audit, or refinement mechanism
    (whatever its invocation convention), you are encouraged to use
    it and to persist the iteration trace to your working directory
    at any path you choose (for example, `task/attempts/attempt-01.md`,
    `task/iterations/iter-01.md`, `task/.eval-report.json`, a
    subdirectory under `task/`).  ROOT will cite these paths in
    scoring.  If your configuration does not provide such a
    mechanism, a single-shot argument is a legitimate response and
    you should simply deliver it.  Do not simulate iteration; if you
    iterate, actually iterate.
```

---

## 2. Ideal answer (ROOT-only)

The full baseline **is** confluent; the rules are left-linear and
non-overlapping (no LHS of one rule can match a subterm of another's
LHS as a whole, though each rule's LHS can match inside a reduct of
another — that is residual structure, not critical-pair overlap).
An orthogonal (left-linear, non-overlapping) term-rewriting system is
confluent — this is a classical result with a standard proof via
parallel reduction.

The ideal path from first principles:

| Step | Content |
|---|---|
| 1 Motivation | Precedents: determinism of functional programs (Church's thesis analog for functional computation); unique normal forms under β-equivalence; equivalence-class well-definedness in quotient algebras; the observation that "the order of evaluation doesn't matter for the result" is exactly confluence; field axioms giving unique results; the categorical view of rewriting as diagrams. Structural clue: every baseline rule has a distinct **head constant** and distinct arity, so no two rules ever fire at the same position — local confluence by structural non-overlap. |
| 2 Procedure | (a) enumerate rule pairs, check for critical-pair overlap. All 13 rules have distinct head constants → no overlap → local confluence holds trivially. (b) Since baseline is non-SN (Y and SII(SII) diverge), Newman-style LC→C via SN does NOT apply. Must use parallel reduction. Define M ⇒ N: (i) M = N (reflexivity); (ii) if M₁ ⇒ N₁ and M₂ ⇒ N₂, then (M₁ M₂) ⇒ (N₁ N₂) (congruence); (iii) for each primitive rule, closure under substitution. Show ⇒ has diamond property. Show →* = ⇒*. Done. (c) For non-terminating case: parallel reduction's diamond doesn't require SN. |
| 3 Progression | {I}: 1 rule, trivially confluent (deterministic). {I, K}: 2 rules, distinct heads, parallel-reduction diamond trivial. {I, K, S}: first non-trivial case — S-rule duplicates its third argument, so parallel reduction must handle the case where one ⇒-step reduces an S-redex and another ⇒-step reduces inside its third argument (both before and after duplication). Classical "residual argument": x z (y z) after S-reduction with z ⇒ z' gives x z' (y z'); if instead z was reduced first to z' and then S fires, same result. Diamond closes. {I, K, S, B, C, W, M}: add non-linear (W, M) and linear (B, C); W duplicates like S; same argument. {…, Y}: Y's rule Y f → f (Y f) is self-referential; parallel-step diamond on Y treats Y f ⇒ f (Y f) as a one-step parallel-reduction. Handle. Full baseline: orthogonal, so the orthogonality theorem's argument carries. |
| 4 Verdict | Full baseline is confluent. All 13 rules orthogonal. Proof method: parallel-reduction diamond. Counting convention: "rule overlap" = critical pair at the position LHS₁ overlaps LHS₂ in a term where both could fire simultaneously; left-linear rules (no duplicated variable on LHS) + non-overlapping LHSes = orthogonal; orthogonal ⇒ confluent. Each of the 13 rules is left-linear (variables I_v, K_(x,y), S_(x,y,z), etc. all distinct); no rule's LHS is a subterm of another's → non-overlapping. |
| 5 Verification | Exhibit diamond closure on at least 3 critical-pair-free rule combinations (since there are no critical pairs in the strict sense, the combinations are parallel applications at different positions). Representative example: S(K a)(K b) c — reduces via S first to (K a) c ((K b) c) → a b; reduces via inner K first to S a (K b) c → a c ((K b) c) → a c b [different! — wait, check rule: S x y z → x z (y z), so S a (K b) c → a c ((K b) c) → a c b]. Verify these are the **same** result? **No** — first path gives `a b`, second gives `a c b`. **Critical check**: S(K a)(K b) c — is (K a) a free variable or a subterm? S has rule S x y z → x z (y z), so with x = (K a), y = (K b), z = c, the reduct is (K a) c ((K b) c). Reducing (K a) c → a, and (K b) c → b, so the final normal form is a b. Alternative path: first reduce the inner (K a) and (K b) in place before S fires? But (K a) is not a redex — K is a 2-argument combinator, (K a) is an un-applied K — not reducible. So the alternative path doesn't exist: S(K a)(K b) c has only one reduction path. The example was mis-conceived. A better critical example: M(M x) = (M M) x — M applied to M and then to x — wait, M is unary, so M x → x x. M (M x) → (M x) (M x) → (x x)(M x) → (x x)(x x). Two ⇒-steps give the same result; one-step diamond closure. Verify via combinator-reducer.py. |
| 6 Examples | (a) The parallel-redex example M(M x) → (M x)(M x) with two different parallel orderings closing at (x x)(x x). (b) Y-induced divergence: (Y f) → f (Y f) → f (f (Y f)) → ... all reductions up to k steps match when paralleled. (c) Mixed K-reduction plus S-duplication: S K K x — either (K x)(K x) → x x [but K has arity 2, applied to only x is un-redex] — hmm, S K K x with x = x: S x y z rule gives K x (K x), which is just (K x)(K x), neither reducible. Wait — S K K x means apply S to K, K, x: by rule S f g z → f z (g z) with f=K, g=K, z=x → K x (K x) — K has arity 2; K x is un-applied, K x (K x) is application of unapplied K x to (K x), i.e., (K x) (K x). Under K's rule K a b → a, this is K applied to x, then applied to (K x), so it's of shape K x (K x) = (K x) (K x) as function application. K x is the partial K-application; applying (K x) to (K x) means evaluating K x (K x), and K's rule fires: K x (K x) → x. Final: x. So S K K x → K x (K x) → x. Verify: oracle reports `(S K K x)` → `x` in 2 steps (confirmed in combinator-reducer.py --selftest). This is the identity-from-S-K example — reductions converge to x. |
| 7 Limits | (a) Strong reduction (under λ-binders) requires extending parallel reduction to handle β-redexes inside abstractions; same technique works but proof is longer. (b) Confluence does not imply normalization: Y (which has no normal form) coexists with confluence. (c) Non-orthogonal extensions: adding a rule like `L x → x x` (= M) alongside M is a duplicate rule with identical LHS — creates a "trivial" critical pair that resolves by rule equivalence. A non-orthogonal *non-trivial* extension: `N x y → x` (= K up to arity-pattern) is distinct from K but LHS is overlappable at head position — this creates a critical pair that does not close with strong local confluence but does close with the diamond closure under parallel reduction. (d) Weak vs strong confluence: the baseline is strongly confluent (one-step diamond holds) because each rule is deterministic on its position. |

**What can go wrong in first drafts:**
- Claim confluence from local confluence alone without addressing non-termination (invokes Newman-style reasoning which requires SN that doesn't hold here).
- Claim "all rules non-overlapping therefore confluent" without the parallel-reduction machinery (the orthogonality theorem *is* the combination, but needs the diamond argument).
- Miss the left-linearity requirement (SII(SII) has nested duplication; the argument must cover it).
- Confuse critical pair with residual / descendant structure.
- Exhibit a "counter-example" that is actually confluent on closer inspection (misidentify non-reducible subterms as redexes).

**R9 binary shape for this cycle:** R9 = 3 iff the ARGUMENT produces
a correct confluence verdict (either "baseline is confluent, proof
discharged" or "baseline is not confluent at rules X vs Y, counter-
example C") where the verdict is **rigorously** supported.  R9 = 0
otherwise.  "The baseline looks confluent / I think it's confluent"
without a discharge is R9 = 0.  Partial credit not allowed for R9.

The canonical identity of the result is what classical combinatory-
logic texts call the "orthogonality confluence theorem" (Klop, Klop &
de Vrijer, Barendregt) — a standard result; the derivation is not
hidden behind one name.

---

## 3. Paper-identifying keywords for this cycle (informational)

These must NOT appear in any TASK prompt, any ROOT→sub delegation
payload, or the delivered prompt.  They are allowed in this ROOT-only
file because it is never mounted into A or B.

**Inherited from Cycle #4 (14 entries):**

- "SKI calculus" / "SKI"
- "SK calculus"
- "BCKW" / "BCIW"
- "Iota combinator" / "ι" (the Greek letter in combinator name context)
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

**Cycle #5 domain-specific additions (6 entries):**

- "Church-Rosser" / "Church–Rosser" / "Church-Rosser property"
- "Tait–Martin-Löf" / "Tait-Martin-Löf" / "Tait Martin-Löf technique"
- "Takahashi translation" / "Takahashi parallel reduction"
- "Newman's lemma"
- "Knuth–Bendix" / "Knuth-Bendix" / "Knuth-Bendix completion"
- "Hindley–Rosen" / "Hindley-Rosen lemma"

Total Cycle #5 banned-identifier list: **20 entries** (14 base + 6
new).

The existing `paper-leak-guard.sh` reversed-forms block the paper
keyword set for the eml paper ("eml", "Odrzywolek", "Sheffer",
"2603.21852", plus path-style additions from Cycle #1: "docs/research",
"eml-paper", "paper.pdf", "paper.txt").  Cycle #5's 20 banned names
are enforced via (a) explicit listing in §1's delegation prompt,
(b) post-cycle `paper-leak-audit.sh` base-pattern scan, and
(c) an extended post-cycle grep for the 20 Cycle #5 names (§4 below).
Consistent with Cycle #4, we do **not** extend the reversed-form
blocklist in `paper-leak-guard.sh` for these 20 — the cycle's
symmetric-zero-change convention on `projects/a/` means reversed-form
hardening is only done when a **new** paper-adjacent path/file
identifier is introduced, not for cycle-specific technical names.

---

## 4. Post-cycle leak audit extension (Cycle #5 only)

Run the base `scripts/meta/paper-leak-audit.sh` (blocks the eml paper
keyword set, still applicable) on each ARGUMENT.md.  Then
additionally grep each ARGUMENT.md for each name in §3 above:

```
grep -iE 'ski calculus|sk calculus|bckw|bciw|iota combinator|jot|unlambda|binary lambda calculus|\bblc\b|x combinator|xi combinator|\bzot\b|schönfinkel|schonfinkel|haskell curry|alonzo church|barkley rosser|turing.s universal combinator|church.rosser|tait.martin.löf|tait.martin-lof|takahashi|newman.s lemma|knuth.bendix|hindley.rosen' projects/a/task/ARGUMENT.md
grep -iE 'ski calculus|sk calculus|bckw|bciw|iota combinator|jot|unlambda|binary lambda calculus|\bblc\b|x combinator|xi combinator|\bzot\b|schönfinkel|schonfinkel|haskell curry|alonzo church|barkley rosser|turing.s universal combinator|church.rosser|tait.martin.löf|tait.martin-lof|takahashi|newman.s lemma|knuth.bendix|hindley.rosen' projects/b/task/ARGUMENT.md
```

"Confluence" / "confluent" / "diamond" / "parallel reduction" /
"critical pair" / "overlap" / "residual" / "normal form" / "rewrite"
as generic structural vocabulary are **not** name-identifying; they
are the formalism the task prompt itself uses.  Do not disqualify on
them.  Bare letters (S, K, I, B, C, W, M, Y, T, V, D) as symbols in
the symbol-table sense are not names — they are variable-like tokens
from the prompt and are permitted.

---

## 5. Hint-drift record (required by CLAUDE.md §6.7 step 1)

| Hint | Decision | Rationale |
|---|---|---|
| "Is the full baseline's reduction relation confluent?  If not, where is the largest confluent subset, and is there a minimal non-confluent extension?" | **Included** | Shape hint analogous to Cycle #1's "single binary + single constant" and Cycle #4's "single primitive symbol + application".  For Cycle #5 the shape hint invites the agent to commit to a verdict (yes / no / subset) and forbids the non-committal "possibly confluent" response.  The phrasing does not pre-commit to "yes" — it invites argument either way. |
| Parallel-reduction / diamond technique by name | **Omitted and explicitly banned** (via Tait–Martin-Löf, Takahashi entries in §3) | Canonical proof names would bypass the derivation step entirely.  The agent must reinvent the parallel-reduction idea from the structural observation that local confluence + SN insufficient → needs a "parallel step that closes in one hop". |
| Newman's lemma by name | **Omitted and explicitly banned** | Newman's lemma is often the first "named tool" agents reach for; its non-applicability here (no SN) is a key discovery point the agent must make themselves. |
| Critical-pair analysis by name | **Included in prompt vocabulary** | "Critical pair" and "overlap" are technical terminology from rewriting-systems formalism; they appear in the prompt (§1 clause 2, clause 5 option (a)) because the task definition itself requires them.  Knuth–Bendix (the critical-pair completion algorithm) is banned by name; the concept of a critical pair itself is allowed. |
| Orthogonality (left-linearity + non-overlap) by name | **Included in prompt** as structural criterion | "Orthogonal term-rewriting system" is specific terminology but describes a *structural* property of rules, not an invented technique.  Allowed.  The canonical "orthogonality ⇒ confluence" theorem is what the ideal answer discharges via parallel reduction — the **theorem** is derivable; only the proof *technique name* is banned. |
| Turing-completeness of baseline | **Stated explicitly** (as in Cycle #4) | The same premise as Cycle #4; carrying it across cycles keeps baselines comparable. |
| Explicit R10 iteration expectation | **Included at end of §1** ("Iteration affordance") as invitation (same format as Cycle #4) | Rubric R10 requires on-disk trace evidence.  The invitation format preserves A's legitimate single-shot response. |
| Executable-oracle verification mention | **Included as "R6 = 3 indicator"** in §1 clause 5 | Cycle #4 established this as a per-primitive correctness validator.  For Cycle #5, the oracle mention is in the deliverable clause (not the motivation) to avoid priming the agent — only relevant if the agent chooses to build a simulator.  `/workspaces/scripts/meta/oracles/combinator-reducer.py` is ROOT-side, NOT mounted into A or B; the A and B containers must build their own simulators if they choose this path, same as Cycle #4 B did. |
| Arbitration / proof-auditor step | **Not mentioned in the prompt** | This is a grading-layer concern (CLAUDE.md §6.7 step 5c), not an agent-side concern.  The agent produces ARGUMENT.md; ROOT grades; proof-auditor independently audits.  The agent does not need to know. |

---

## 6. Task-framing drift vs Cycles #1, #2, #3, #4

| Aspect | Cycle #1 | Cycle #2 | Cycle #3 | Cycle #4 | Cycle #5 |
|---|---|---|---|---|---|
| Domain | Elementary functions | Euclidean constructions | Register machines | Combinator reduction — cardinality | **Combinator reduction — confluence** |
| Domain class | Continuous analysis | Discrete geometry | Discrete sequential computation | Pure syntactic reduction (minimization) | **Pure syntactic reduction (semantic property)** |
| Primitive family cardinality | ~34 | 2 | 11 | 13 (baseline) | **13 (same as Cycle #4)** |
| Central-question shape hint | "single binary + single constant sufficient?" | "Is one of the two enough alone?" | "Is there a single fused instruction that suffices?" | "Is there a single primitive symbol + application that suffices?" | **"Is the full baseline's reduction relation confluent?"** |
| Expected answer form | 1 binary + 1 constant | 1 primitive (circle) | 1–4 instructions under convention | 1 combinator + application-wrapper | **Yes, full baseline confluent via orthogonality + parallel-reduction diamond** |
| A1 mitigation strength | Low | Low | Medium-high | Medium-high (14 banned names) | **High (20 banned names, including technique-specific)** |
| Rubric max | 27 | 27 | 27 | 30 (R10 added) | **30 (R10 kept; R4 band semantics adjusted per §7)** |
| First-draft ceiling | high | high | medium-high | medium (Cycle #4 A: 22/30) | **medium-low (17–20/30 expected A-first-draft)** |

Cycle #5 is the first cycle where the **first-draft ceiling is
deliberately below the R1–R9 saturation line**.  Cycles #2, #3 ceilinged
at 27/27; Cycle #4 A at 22/30.  Cycle #5 expected A-first-draft is
17–20/30 — this is the band-2-to-band-3 "iteration pays" regime the
Cycle #4 close asked for.

---

## 7. R4 semantic adjustment for Cycle #5 (ROOT-only scorer note)

The R4 axis in `judgment-rubric.md` is phrased in terms of "basis
cardinality" — the shape of Cycle #4's minimization question.  For
Cycle #5 (confluence), the analog is **"verdict commitment"** — did
the agent stake a definite confluence claim (yes / no / subset)?

Score mapping for R4 this cycle:
- 0: no commitment; argument is "it seems confluent, maybe, under
  some conditions".
- 1: tentative commitment but hedged beyond rubric reading
  ("probably confluent but cannot prove").
- 2: firm commitment to a partial answer ("confluent on subset P′
  but I cannot establish full-baseline confluence").
- 3: firm commitment on the full baseline verdict, whether positive
  or negative, with a proof or concrete counterexample.

This adjustment is documented here (not ported to `judgment-rubric.md`
yet) because it is Cycle #5-specific.  If Cycle #6 reuses this
framing, it should be generalized in the rubric per ROOT's cycle-close
improvement protocol.

---

## 8. B `/refine` scorer-evolution note (carried forward)

Cycle #3 G5 integrity-axis polarity (hidden circularity < disclosed
gap + named limitation < closed proof) + Cycle #4 R10 iteration-depth
internal analog remain in force for Cycle #5.  Additional Cycle #5
guidance:

- **Oracle invocation.** If B builds a Python β-reducer as in Cycle #4,
  that reducer may also be used to check specific confluence claims
  (enumerate reduction paths for a small term, check for common
  reduct).  The `.eval-report*.json` for Cycle #5 should include an
  `oracle_verifications` field if any were performed, citing the
  reducer invocation and the claim it discharged.
- **Banned-identifier hard-constraint violations** (Cycle #4's
  seed-09 strategy) apply to the 20-entry Cycle #5 list.  The
  evaluator should treat any match on the 20-name list as a hard
  constraint that must be cleared before `release_readiness`.

---

## 9. B `/refine` firing expectation (unchanged)

Per `projects/b/CLAUDE.md` §4.3 (/refine mandatory for reasoning
deliverables without a fixed correctness oracle): Cycle #5 is such a
deliverable.  B must fire `/refine` or an equivalent manual
iteration with on-disk trace for the cycle to count as apples-to-
apples.  Same measurable-firing evidence as Cycle #4 (attempts/,
.eval-report*.json, evaluator invocation in /tmp/agent.log).

---

## 10. Cross-cycle persistence seed (Cycle #5 — augmentation expected)

`projects/b/agent-memory-seed/strategies.jsonl` carries 10 Cycle #4
KEEP entries (seed-01 through seed-10).  Expected Cycle #5
augmentation candidates (for post-cycle ROOT harvest):

- **Confluence-specific strategy:** "Default to parallel-reduction
  diamond when local confluence + SN is insufficient (non-SN
  systems)" — derivable from Cycle #5 ideal path step 2.
- **Technique-renaming workaround:** "When a canonical proof
  technique's name is banned, describe the technique by its
  *mechanism* (one-step parallel closure) rather than by name" —
  analogous to Cycle #4 seed-08 banned-identifier workaround.

These will be harvested after B's Cycle #5 run via the same
`docker exec claude-meta-autoagent-b cat .claude/agent-memory/skills/
strategies.jsonl` + dedupe + commit path as Cycle #4.  If Cycle #5 B
does not produce novel KEEP entries, the seed stays at 10.  The
lifecycle-validation in the cycle-log entry confirms the seed path
remained mounted into B's container (forward-check: `docker exec
claude-meta-autoagent-b ls /workspaces/agent-memory-seed/` shows
strategies.jsonl and README.md at cycle launch).

---

## 11. Oracle catalogue pointer (Cycle #5 new)

`scripts/meta/oracles/combinator-reducer.py` is the ROOT-side
executable β-reducer (weak-head, leftmost-outermost) with `--selftest`
(15/15 passing as of pre-cycle).  It is NOT mounted into A or B's
container — the agents must build their own simulator if they choose
the executable-oracle path.  Its role at Cycle #5 is:

- **Proof-auditor accessible** — during CLAUDE.md §6.7 step 5c,
  proof-auditor may invoke the reducer to verify R6 / R9
  trace-level claims the incumbent JUDGMENT makes.
- **Not leak-relevant** — the reducer implements standard combinator
  reduction rules already present in §1's prompt; it contains no
  paper-identifying content.  It is allowed in ROOT filesystem.

Future cycles may add domain-specific oracles (type-checkers for typed
calculi, rewriting-system simulators for tag-systems, etc.) to the
same directory.
