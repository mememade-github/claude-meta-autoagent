# Cycle 04 — TASK definition (ROOT-only)

**Cycle purpose.** The three prior cycles produced a collapsing delta on
the R1–R9 rubric: **19 vs 20** (Cycle #1, +1 B on R2), **26 vs 26**
(Cycle #2, tie), **27 vs 27** (Cycle #3, tie).  R1–R9 ceilinged across
Cycles #2 and #3 while B's iteration activity (fire in Cycle #2,
architecturally blocked in Cycle #3) left no rubric trace.  The tie
pattern is not evidence that the evolvable architecture adds nothing —
it is evidence that **the measurement instrument has no iteration-
sensitive axis.**  Cycle #4 addresses this at three layers:

1. **Rubric layer** — `docs/research/eml-paper/judgment-rubric.md` now
   carries **R10 iteration-depth and self-correction trace** (0–3),
   extending total from 27 to 30.  R10 is structurally asymmetric: A
   baseline is single-shot by configuration and scores 0 unless its
   run happens to produce a multi-write mtime trace with reasoning
   deltas; B has `/refine`, evaluator, and agent-memory affordances
   and can reach R10 = 3.  The asymmetry is the point of R10 — it
   measures whether the evolvable architecture **uses** its iteration
   affordance during the task.
2. **Task layer** — this prompt names the persisted-trace deliverable
   explicitly.  Agents whose configuration does not support iteration
   produce a single-shot argument (legitimate response; scores 0 on
   R10).  Agents with iteration affordances are free to persist
   iteration trace at any disk path under their working directory.
   ROOT will cite those paths in scoring.
3. **Persistence layer** — `projects/b/.claude/agent-memory-seed/` is
   introduced as a committed path (un-gitignored) that the B container
   mount exposes as `/workspaces/.claude/agent-memory-seed/`.  Between
   cycles this path survives (it is tracked), so Cycle #5's B startup
   reads Cycle #4's seed.  This addresses clause 5 of the Cycle #4
   GOAL (between-cycle learning persistence) and is the first step
   toward actual cross-run learning on the B side (CLAUDE.md §6.10).

Domain change from prior cycles: Cycle #1 continuous analysis, Cycle
#2 discrete geometry, Cycle #3 discrete computation (register
machine).  Cycle #4 moves to **pure syntactic reduction — combinator
minimization**.  No state, no sequential execution, no numeric values
— only application of symbols to symbols under substitution.
Orthogonal to all three prior domains (though related to Cycle #3
through the Church–Turing identification, the *operational* texture
is completely different: Cycle #3 agents reasoned about labelled
jumps and register invariants; Cycle #4 agents will reason about
reduction rules on binary trees of applications).

---

## 1. Task prompt delivered to A and B

Both sub-agents receive identical text via
`scripts/meta/delegate-sub.sh <key>`.  The `scripts/meta/paper-leak-audit.sh`
pattern set is checked on the GOAL before launch.

```
TASK: Minimal primitive set for applicative combinator reduction

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
    T   :  T x y        → y x                      (thrush / reverse-apply)
    V   :  V x y z      → z x y                    (pair / Vireo)
    D   :  D x y z w    → x y (z w)
    Π₁  :  Π₁ x y       → x                        (first-of-pair)
    Π₂  :  Π₂ x y       → y                        (second-of-pair)

  Additional primitives you MAY treat as derivable during the argument
  (not further baseline):
    the Church numerals c₀, c₁, c₂, …
    Boolean True = K, Boolean False = K I
    the pairing operator cons = λxyz.z x y
    the fixed-point (via Y)

It is widely known (you may assume this as given) that the extended
calculator above is Turing-complete under substitution: every computable
function of natural numbers can be encoded as a term built by
application from this primitive set.  Many of the listed primitives
are redundant — for example, I can be rewritten as ((S K) K), so
strictly I is not irreducibly needed.

Central question: what is the smallest primitive set P*, drawn from
combinators of your choosing, such that every term in the extended
calculator's reduction behaviour is still reachable?  In particular,
is there, perhaps, a single primitive symbol (one constant) paired
with application as the only binary form, that suffices?  You are
free to invent new primitive combinators — define them by their
reduction rules in terms of abstract variables, the same way the
baseline is defined — if that leads to a smaller P*.

Your deliverable: a self-contained argument, written to
`task/ARGUMENT.md` in your working directory.  It must include:

  1. Motivation. Why might such a reduction exist? Cite precedents
     from adjacent algebraic, logical, or computational domains that
     you reason about from first principles — for example, the
     existence of functionally-complete single connectives in Boolean
     logic, or the existence of single generators in other algebraic
     closures.  Explain what structural feature of the baseline
     makes you expect a large reduction.  Derive, do not name.

  2. A systematic reduction procedure you design and justify.  The
     procedure should say how, given a candidate P′, you (a) check
     sufficiency — every primitive outside P′ can be synthesized as
     a term over P′, and (b) check insufficiency — for P′ too small,
     exhibit a primitive outside P′ provably not synthesizable.

  3. A sequence of progressively smaller sufficient primitive sets,
     with intermediate stopping points argued for.  At each stopping
     point, name which primitives have been eliminated and give the
     synthesis (e.g., "I = S K K" if you reach S-and-K).  Reach at
     least 3 intermediate sizes before your final P*.

  4. The minimal primitive set P* you can reach.  If P* contains one
     or more primitives not in the baseline (a newly-invented
     combinator with its own reduction rule), give each such
     primitive's exact reduction rule.  State explicitly the
     counting convention you use — whether "application" counts as
     a primitive, whether a newly-invented combinator counts as one
     primitive or as its defining term's worth, and so on.  Different
     conventions give different minima; yours must be declared.

  5. A verification strategy: how do you confirm P* is complete for
     the extended calculator?  Reduction to a known-complete basis,
     explicit synthesis of every baseline primitive, a diagonal
     argument that smaller bases cannot work, or some combination.
     Name your strategy and discharge it.

  6. Worked examples: exhibit at least three distinct computations
     reduced in P*.  Suggested candidates: identity composition
     I = ? over P*; a simple arithmetic operation on Church
     numerals (successor, addition, multiplication — pick one); a
     fixed-point combinator (or at least a divergent term)
     expressed over P*.  Give the full term text over P*.

  7. Open questions and known limitations, including: (a) whether
     your P* is optimal or merely sufficient (can one more
     combinator be removed?); (b) what changes if the reduction
     semantics is strengthened to strong (under-binder) reduction
     rather than weak; (c) whether your P* depends on the
     particular counting convention you chose in §4 and how a
     different convention would rank your answer against
     alternative minimal sets.

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
    Xi-combinator, Zot, Turing's universal combinator, Curry
    (as a person's surname), Schönfinkel, Rosser,
    Church (as a person's surname).  You MAY use "lambda", "lambda
    calculus", "combinator", "combinatory", "application",
    "reduction", "normal form", and the letters S, K, I, B, C, W, M,
    Y, T, V, D as bare symbols in the symbol-table sense.  If you
    recognize the canonical answer under one of the banned names,
    work around the name and derive the structure yourself.

  - Iteration affordance (important).  If your agent configuration
    provides an iteration / self-audit / /refine mechanism, you are
    encouraged to use it and to persist the iteration trace to your
    working directory at any path you choose (for example,
    `task/attempts/attempt-01.md`, `task/.refine/`,
    `task/iterations/iter-01.md`, `task/.eval-report.json`).  ROOT
    will cite these paths in scoring.  If your configuration does
    not provide such a mechanism, a single-shot argument is a
    legitimate response and you should simply deliver it.  Do not
    simulate iteration; if you iterate, actually iterate.
```

---

## 2. Ideal answer (ROOT-only)

The task admits multiple valid minimal primitive sets, and the "best"
depends on the counting convention the agent picks.  The grader's job
is to assess the quality of the derivation, not to check against a
single answer.

| Step | Content |
|---|---|
| 1 Motivation | Boolean universality via a single connective (NAND / NOR); field generation by adjoining small root sets; Galois closure; Turing's universal machine as a single reduction of multi-tape; the pattern "rich computational model → small generator + fixed wrapper".  Structural clue: application is already a single binary operation; what remains is whether the *constants* can collapse to one, and whether that one can encode the substitution behaviour of every removed constant. |
| 2 Procedure | For each baseline primitive p ∉ P′, exhibit a term T_p over P′ whose reduction behaviour matches p's rule on abstract variables.  Insufficiency: pick a semantic invariant preserved by all P′-reductions but violated by some term outside P′.  E.g., if P′ = {K}, every closed term over {K} with no free variables reduces only to K-headed normal forms — cannot express S's three-variable rewrite.  A reduction count / normal-form-shape argument sustains insufficiency. |
| 3 Progression | 13 primitives → drop derived Booleans / numerals / pair-accessors (already stated as derivable) → core 11 → drop M (= W I = SII) → 10 → drop T, V, D, Π₁, Π₂ (all expressible in S, K) → 6 → drop W, C, B, Y (SKI derivations) → {S, K, I} → drop I (= S K K) → {S, K} → at this point, fuse S and K into a **single combinator** with its own reduction rule.  Multiple valid fusions exist: one that reduces to SK-pair behaviour (requires one application-and-project gadget), a different one that matches SK with three arguments, etc.  Ending at a single primitive whose reduction rule is a 4-argument or 5-argument rewrite. |
| 4 Minimal | Candidate P*: a single combinator *X* with rule *X f → f K S K S K* or the dual *X f → f S K* (depending on the fusion the agent invents).  Counting convention: application is a syntactic operation (not a primitive); the combinator is the sole primitive.  Alternatively, an agent may fuse two layers into one 2-argument combinator and end at one primitive with a 2-argument rule.  All three shapes are valid so long as the reduction is argued through.  The strongest form reaches **P\* = {X}** where X alone + application = universal. |
| 5 Verification | Express S and K in terms of X (or the chosen single combinator) via a short term; conclude that any SK-term has an X-term with identical reduction behaviour; cite the SK-completeness result as already discharged in §3.  Numerically: apply X to a non-trivial closed term and trace the reduction; confirm it matches the expected SK-trace. |
| 6 Examples | (a) I over P* = a short term like X (X X) X or similar; (b) Church successor succ n f x = f (n f x) — write succ as a SK-term, then translate to X-term; (c) Y-combinator Y = SSK(S(K(SS(S(SSK))))K) or a known SK-form, then translate. |
| 7 Limits | Whether P* is unique — no (multiple valid fusions); whether under strong reduction the minimum differs — yes, strong reduction restricts admissible reduction orders and some SK-equivalences fail (e.g., certain non-normalizing terms become stratified); whether counting application as a separate primitive changes the answer — yes, then the minimum is 1 combinator + 1 binary primitive ("application"), which is structurally identical to Cycle #1's "single binary + single constant" shape. |

The canonical identity of the result is the single-combinator reduction
known under the banned names above.  Single-combinator bases have
been independently rediscovered multiple times; the derivation is not
hidden behind one name.

---

## 3. Paper-identifying keywords for this cycle (informational)

These must NOT appear in any TASK prompt, any ROOT→sub delegation
payload, or the delivered prompt.  They are allowed in this ROOT-only
file because it is never mounted into A or B.

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
- "Moses Schönfinkel"
- "Haskell Curry" (person's name)
- "Church" (Alonzo Church, as a person's surname)
- "Rosser" (Barkley Rosser, as a person's surname)
- "Turing's universal combinator"

The existing `paper-leak-guard.sh` reversed-forms block the paper
keyword set for the eml paper ("eml", "Odrzywolek", "Sheffer",
"2603.21852").  It does not block the above Cycle #4-specific names.
For Cycle #4 we rely on: (a) no file in A/B's mount containing these
names, (b) the delegation prompt containing none of them (enforced by
§1's explicit banned-identifier list delivered to A and B),
(c) post-cycle `paper-leak-audit.sh` scan for these names on both
ARGUMENT.md files (§4 below).  We do **not** extend the reversed-form
blocklist for Cycle #4, consistent with the Cycle #2 and #3
symmetric-zero-change convention on `projects/a/`.

Note on the paper keyword "Sheffer".  In combinatory logic literature
a "Sheffer function" / "Sheffer stroke" sometimes describes a single
connective that is functionally complete.  If an agent uses this
phrasing, the base `paper-leak-audit.sh` will flag it and the cycle
will void.  The §1 banned-identifier list explicitly does *not* invite
this phrasing — agents are told to derive, not to name — but if an
agent independently coins "Sheffer-style combinator" they will trip
the audit.  This is acceptable: it is the exact control the paper-
keyword set is designed to enforce.  A clean derivation does not need
to name the pattern.

---

## 4. Post-cycle leak audit extension (Cycle #4 only)

Run the base `scripts/meta/paper-leak-audit.sh` (blocks the eml paper
keyword set, still applicable) on each ARGUMENT.md.  Then additionally
grep each ARGUMENT.md for each name in §3 above.  Any hit on a §3 name
also triggers the Leak disqualification tier in
`docs/research/eml-paper/judgment-rubric.md`.

```
grep -iE 'ski calculus|sk calculus|bckw|bciw|iota combinator|jot|unlambda|binary lambda calculus|\bblc\b|x combinator|xi combinator|\bzot\b|schönfinkel|schonfinkel|haskell curry|alonzo church|barkley rosser|turing.s universal combinator' projects/a/task/ARGUMENT.md
grep -iE 'ski calculus|sk calculus|bckw|bciw|iota combinator|jot|unlambda|binary lambda calculus|\bblc\b|x combinator|xi combinator|\bzot\b|schönfinkel|schonfinkel|haskell curry|alonzo church|barkley rosser|turing.s universal combinator' projects/b/task/ARGUMENT.md
```

"Combinator" / "combinatory" / "lambda" / "application" / "reduction"
as generic structural vocabulary are not name-identifying; they are
the formalism the task prompt itself uses.  Do not disqualify on them.
Bare letters (S, K, I, B, C, W, M, Y, T, V, D) as symbols in the
symbol-table sense are not names — they are variable-like tokens from
the prompt and are permitted.

---

## 5. Hint-drift record (required by CLAUDE.md §6.7 step 1)

| Hint | Decision | Rationale |
|---|---|---|
| "Is there a single primitive symbol (one constant) paired with application as the only binary form, that suffices?" | **Included** | Structural shape hint; parallel to Cycle #1's "single binary operator + single constant", Cycle #2's "Is one of the two primitives enough alone?", and Cycle #3's "Is there a single instruction from some variant family that suffices?".  Keeping the hint comparable across cycles lets the A/B delta measure architectural contribution holding task-framing constant.  The phrasing does not pre-commit to "one is enough" — it invites argument either way. |
| Named single-combinator answers (Iota, Jot, X, Unlambda, BLC) | **Omitted and explicitly banned** in the prompt | Multiple named canonical answers exist.  Each is a short name for a specific reduction.  Naming would bypass the derivation step entirely. |
| Historical framing (Schönfinkel 1924, Curry 1930, Church 1932–36) | **Omitted** | Date + name cues might trigger memory retrieval of the proof structure. |
| Fused-combinator construction pattern (e.g. "define X such that X f = f S K") | **Invited in §4 of the deliverable clause** but not pre-named | "If P* contains one or more primitives not in the baseline (a newly-invented combinator with its own reduction rule), give each such primitive's exact reduction rule."  This tells the agent it is permitted to invent; it does not tell the agent what to invent. |
| Application-as-primitive counting convention | **Explicitly flagged as a modelling question the agent must decide** | Different conventions give different minima.  Letting the agent pick and justify is more informative than dictating. |
| "Turing-complete under substitution" is given | **Stated explicitly in the prompt** | Otherwise the agent might spend effort on the Turing-completeness question itself, which is not what this task measures.  Completeness of the baseline is a premise; the minimization is the task. |
| Explicit R10 iteration expectation | **Included at end of §1 ("Iteration affordance") — not as an instruction but as an invitation** | Rubric R10 requires on-disk trace evidence.  The agent must know that iteration trace will be inspected, or a well-iterating agent might iterate in-memory only (no R10 credit).  The phrasing is invitational (not imperative) so A's single-shot configuration is not disadvantaged by non-compliance — A legitimately produces single-shot.  Method-freedom is preserved per §6.1. |

---

## 6. Task-framing drift vs Cycles #1, #2, #3

| Aspect | Cycle #1 | Cycle #2 | Cycle #3 | Cycle #4 |
|---|---|---|---|---|
| Domain | Elementary functions | Euclidean constructions | Register machines | Combinator reduction |
| Domain class | Continuous analysis | Discrete geometry | Discrete sequential computation | Pure syntactic reduction |
| Primitive family cardinality | ~34 | 2 | 11 | 13 (baseline) |
| Central-question shape hint | "single binary + single constant sufficient?" | "Is one of the two enough alone?" | "Is there a single fused instruction that suffices?" | "Is there a single primitive symbol (one constant) paired with application that suffices?" |
| Expected minimal form | 1 binary + 1 constant | 1 primitive (circle) | 1–4 instructions under counting convention | 1 combinator + application-as-wrapper |
| A1 mitigation strength | Low | Low | Medium-high (multi-convention counting, banned list) | **Medium-high** (multi-shape fusions, large banned list including 14 names) |
| Rubric max | 27 | 27 | 27 | **30 (R10 added)** |
| Deliverable structure | 7 sections | 7 sections | 7 sections (+ removal-of-one question) | 7 sections (+ strong-vs-weak reduction + counting-convention dependence in §7) |

Cycle #4 is the first cycle under the **R10-extended** rubric.  The
expectation is that R1–R9 may again ceiling to a tie (the three-cycle
trend is strong) — and that the A vs B delta comes from R10 and
R6-polarity-under-iteration.  If R1–R9 also separates, that is
additional evidence; if R1–R9 ties but R10 separates, the measurable
delta called for by Cycle #4 GOAL clause 2 is still achieved.

---

## 7. B `/refine` scorer-evolution note (carried forward from Cycle #3 TASK §7)

The Cycle #3 G5 integrity-axis polarity rule (hidden circularity <
disclosed gap + named limitation < closed proof) is preserved
verbatim for Cycle #4's B refinement run.  See
`cycle-03/TASK.md` §7 for the full three-rule enforcement list.  This
§7 is the continuing channel through which ROOT codifies scorer-
evolution for B's /refine contract, pending the sensitive-file policy
lift that would let the rule land permanently in B's
`.claude/agents/evaluator.md`.

Additionally for Cycle #4: the **R10 iteration-depth axis** should be
reflected in B's own internal evaluator scoring if B runs /refine.
Concretely:

- An iteration that closes a gap disclosed in a prior iteration scores
  strictly higher on integrity than the prior iteration — same
  direction as G5, different surface expression (integrity discloses;
  R10 resolves).
- An iteration that merely re-reads without resolving any disclosed
  gap or tension scores at most 1 on the internal R10 analogue.
- Final iteration must leave an identifiable on-disk artefact (attempt
  JSONL, eval-report, timestamped markdown file) whose path can be
  cited in ROOT's JUDGMENT.md.  If B runs /refine but leaves no
  persisted trace (as happened in Cycle #3), R10 scores at most 1
  regardless of what /refine did in-memory.

Forward-check at JUDGMENT time: ROOT reads B's task directory
contents and itemizes every iteration artefact found, citing mtimes
and byte sizes.  Absence of any persisted trace caps R10 at 1 for B,
independent of refinement claims in ARGUMENT.md prose.

---

## 8. B `/refine` firing expectation (unchanged from Cycle #2 and #3)

Per `projects/b/CLAUDE.md` §4.3:

> `/refine` is mandatory for any reasoning deliverable where the first
> draft's correctness is not settled by an external oracle.

Cycle #4 is such a deliverable.  B must fire `/refine` (or, if the
Cycle #3 M3.1 architectural blockage persists, fire a manual
equivalent — fresh-context evaluator agent with persisted trace) for
this cycle to count as apples-to-apples.  Measured evidence of firing:

- `.refinement-active` marker file present in B's workspace during the
  run, OR a functionally equivalent marker in a different path.
- `attempts/<timestamp>.jsonl` arrival(s) OR equivalently-located
  iteration artefacts.
- Evaluator-agent invocation visible in B's `/tmp/agent.log` or
  transcript.

If none of these appear AND no alternative on-disk trace exists,
Cycle #4 records "B `/refine` non-firing with no substitute" as a
regression from Cycle #2 (and from Cycle #3's manual-substitute
compliance).  M3.1-refine-architectural-blockage status re-evaluated
at that point.

---

## 9. Cross-cycle persistence seed (Cycle #4 new)

`projects/b/.claude/agent-memory-seed/` is the tracked, un-gitignored
path introduced in Cycle #4 pre-cycle commits.  The B container mount
exposes this as `/workspaces/.claude/agent-memory-seed/`.  Contents at
Cycle #4 launch time: `strategies.jsonl` with pre-seeded patterns
derived from Cycles #1–#3 KEEP-class observations (what tends to work
for first-principles minimization derivations).

This is an *opt-in* seed: B is free to consult it (read-only during
the task; writes to `.claude/agent-memory/` during /refine accumulate
there as usual and remain gitignored).  B's `refine` skill on
completion writes KEEP strategies to `.claude/agent-memory/skills/
strategies.jsonl` per CLAUDE.md §4.4; that gitignored path does not
survive across cycles, but the seed does.

**Ingress path for next cycle.**  At Cycle #5 pre-cycle prep, ROOT
harvests the current cycle's `.claude/agent-memory/skills/
strategies.jsonl` contents from the B container via
`docker exec claude-meta-autoagent-b cat`, deduplicates against the
seed, and commits any new KEEP-class entries to
`projects/b/.claude/agent-memory-seed/strategies.jsonl` before the
next launch.  The seed accumulates across cycles; the runtime
agent-memory is reset each cycle (gitignore clears the volume).  This
asymmetry is intentional: runtime pollution from noisy intermediate
iterations does not leak to the seed; only post-/refine KEEP-class
survivals are promoted.

See `cycle-log.md` Cycle #4 entry for the initial seed contents and
the forward-check that confirms B reads the seed on launch.
