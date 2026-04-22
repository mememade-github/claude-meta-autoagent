---
status: draft
cycle: 5
domain: confluence-of-applicative-combinator-reduction
auditor: proof-auditor
auditor_date: 2026-04-22
arbitration_triggered: false
incumbent_total_A: 28
incumbent_total_B: 30
auditor_total_A: 28
auditor_total_B: 30
agreement: 19_YES_1_CONDITIONAL_0_NO
audit_file: cycle-05/rubric-audit.json
---

# Cycle 05 — JUDGMENT

Grading of `cycle-05/A-ARGUMENT.md` and `cycle-05/B-ARGUMENT.md`
against `docs/research/eml-paper/judgment-rubric.md` (R1–R10, total 30
points) with the Cycle #5 R4-semantic adjustment from `cycle-05/TASK.md`
§7 (verdict commitment rather than basis cardinality).

Front-matter `status` is `draft` at time of writing; it will be updated
to `draft` / `arbitration-pending` / `arbitrated` per CLAUDE.md §6.7 step
5c after the proof-auditor pass.

---

## §0. Cycle artefacts (audit record)

Captured at cycle close (2026-04-22 14:36 UTC), ported from the A and B
container mounts before any cleanup, with SHA-256 prefixes for
reproducibility.

| Path                                 | Bytes | SHA-256 prefix | mtime (container-local) |
|--------------------------------------|------:|---------------|-------------------------|
| `cycle-05/A-ARGUMENT.md`             | 33962 | `d5c17f60…`   | 14:24:56 |
| `cycle-05/A-iter-01-audit.md`        |  4957 | `98e260b3…`   | 14:26:34 |
| `cycle-05/A-sim.py`                  | 14631 | `057504aa…`   | 14:21:08 |
| `cycle-05/A-sim_output.txt`          |  5857 | —              | 14:21:12 |
| `cycle-05/B-ARGUMENT.md`             | 46444 | `ad6fc70f…`   | 14:33:53 |
| `cycle-05/B-attempt-01.md`           | 45466 | `286ea3d6…`   | 14:26:36 |
| `cycle-05/B-eval-01.json`            |  6601 | `8f108035…`   | 14:28:18 |
| `cycle-05/B-eval-final.json`         |  8185 | `b67a1dd4…`   | 14:36:09 |
| `cycle-05/B-simulator.py`            |  9350 | `ff5f4259…`   | 14:28:49 |
| `cycle-05/B-sim-output-run1.txt`     |  1658 | —              | 14:21:37 |
| `cycle-05/B-sim-output-run2.txt`     |  1664 | —              | 14:28:40 |
| `cycle-05/B-sim-output-final.txt`    |  1670 | —              | 14:28:53 |

**Execution timing.**

- A launched 05:17:44 UTC; first ARGUMENT.md write 14:24:56; self-audit
  write 14:26:34; exited ~14:26 (≈ 9 min wall-clock — A finished
  markedly faster than B, consistent with single-shot + verification
  vs. multi-iteration workflows).
- B launched 05:17:45 UTC; attempt-01 write 14:26:36; eval-01 write
  14:28:18; final ARGUMENT.md write 14:33:53; eval-final write
  14:36:09; exited ~14:36 (≈ 19 min wall-clock, with a clear two-pass
  structure visible in the timestamps).

The byte-size difference between `B-attempt-01.md` (45466) and
`B-ARGUMENT.md` (46444) is ≈ 978 bytes; the SHA-256 prefixes confirm
they are distinct texts.  The `B-eval-01.json` logs 7 gaps;
`B-eval-final.json` records `gap_closure_vs_iteration_1` with all 7
marked `CLOSED` and names the §-locations where each closure lands in
the final draft.

---

## §1. Leak audit

Base `scripts/meta/paper-leak-audit.sh` (eml-paper keyword set):

- A: `[Paper-leak audit passed] cycle-05/A-ARGUMENT.md`
- B: `[Paper-leak audit passed] cycle-05/B-ARGUMENT.md`

Cycle-05 banned-identifier grep (per `cycle-05/TASK.md` §4, scanning
20 cycle-specific names — 14 inherited from Cycle #4 + 6 new):

```
grep -iE 'ski calculus|sk calculus|bckw|bciw|iota combinator|jot|unlambda|
  binary lambda calculus|\bblc\b|x combinator|xi combinator|\bzot\b|
  schönfinkel|schonfinkel|haskell curry|alonzo church|barkley rosser|
  turing.s universal combinator|church.rosser|tait.martin.löf|
  tait.martin-lof|takahashi|newman.s lemma|knuth.bendix|hindley.rosen'
```

- A: no matches
- B: no matches (B's own eval-final.json confirms this with independent
  grep at run-time, banned-identifier-scan field `result: no matches`)

**Both PASS on all leak scans.**

---

## §2. Agent A score: 28 / 30

### R1 Motivation — 3

A §1.1 derives confluence's semantic corollaries (unique normal form,
strategy irrelevance) and explicitly notes their independence from
strong normalization.  §1.2 enumerates three failure modes (overlapping
rules, non-left-linear without joinability, duplication) and §1.3
tables all 13 primitive LHS shapes establishing (P1) disjoint head
primitives and (P2) left-linearity as structural preconditions.  The
three precedents are derived from first principles — failure-mode
analysis, structural rule inspection, combinatorial argument about
how two redexes can relate — without naming any theorem.  The
observation "duplication by S, W, M, Y is the remaining worry" is
explicitly connected to the parallel-reduction fix in §2.

### R2 Method design — 3

A §2 lays out three branches: (2.1) overlap analysis via unification,
(2.2) parallel-reduction diamond technique, (2.3) a branch for
non-terminating systems.  Each branch is defined and justified.
§2's procedure maps directly to the §4 discharge steps.  Verifiable
end-to-end: an overlap found ⇒ fail; no overlap + left-linearity +
no-straddling ⇒ parallel-reduction proof applies.

### R3 Progressive minimization — 3

A §3 walks all 13 primitive additions (I → +K → +S → +B → +C → +W →
+M → +Y → +T → +V → +D → +Π₁ → +Π₂).  At each stage: claim ("adding
Rᵢ preserves confluence"), method (distinct head ⇒ no overlap; triangle
case for the new rule-clause), and disclosed gap ("none" throughout).
The treatment is uniform and each stage is justified via the same
triangle / diamond machinery.  Exceeds R3's "≥ 3 intermediate steps"
at full credit.

### R4 Verdict commitment — 3

A §4 gives an unhedged verdict: **"the full 13-primitive baseline is
confluent"** (§4 opening).  The verdict is then discharged via §4.2
critical-pair audit (no non-trivial overlaps proven structurally),
§4.3 parallel-reduction `⇒` definition, §4.4 complete-development
`M*`, §4.5 `M ⇒ M*` (by induction), §4.6 triangle `M ⇒ N ⟹ N ⇒ M*`
(full case analysis), §4.7 diamond on `⇒`, §4.8 diamond lift `⇒* =
→*`.  Counting conventions declared in §4.9 (critical pair, overlap,
residual, parallel step — all explicitly defined).

Per Cycle #5 R4 semantic (TASK §7): band 3 = "firm commitment on the
full baseline verdict, positive or negative, with a proof or concrete
counterexample."  A commits + discharges.  R4 = 3.

*Observation* (not R4-score-affecting): A does not explicitly address
the central-question sub-clauses "Is there a maximal confluent subset?
A minimal non-confluent extension?"  These are implicitly answered
by A's positive verdict (maximal confluent subset = full baseline by
trivial maximum) but never stated as such.  This is noted here rather
than penalized on R4 because A's positive-verdict branch does not
require discharging the (ii)-branch sub-questions per TASK §1 clause
4.  Relevant contrast with B in §4 below.

### R5 Exact form — 3

A §4 gives explicit definitions of ⇒ (4.3, three clauses refl/app/
rule_c), M* (4.4, recursive), the triangle case analysis (4.6,
discharging refl/app/rule_c cases), the diamond on ⇒ (4.7), and the
tile-closure lift (4.8).  Each clause is stated with inductive
variables explicitly bound.  No hand-waves in the core proof.

### R6 Verification strategy — 3

A §5.1 runs the analytic parallel-reduction triangle + diamond proof
discharged in §4.  A §5.2 runs an **independent executable oracle**
at `task/sim.py` implementing (a) single-step reduction with all redex
positions enumerated, (b) parallel reduction, (c) complete development,
(d) bounded-BFS confluence checker enumerating all reducts of a test
term to depth d and checking pairwise joinability within depth j.  §6
reproduces 3 examples under the oracle with output captured at
`task/sim_output.txt` (147 lines).  §5.3 discusses complementarity:
analytic is exhaustive over rule shapes but only as sound as the
case analysis; oracle is empirical but mechanically checks the actual
rewrite graph.  A bug in §5.1 should cause §5.2 to throw a
counterexample.  No counterexample was observed on the test suite.

Per `judgment-rubric.md` R6 band 3: "constructive bootstrap procedure
… with no disclosed gap remaining.  When the domain admits one, a
working executable oracle … discharges the per-primitive correctness
obligation empirically and counts as a '3' indicator in addition to
the trace-argument path."  A satisfies both legs.  R6 = 3.

### R7 Constructive examples — 3

A §6 gives 3 examples in distinct categories:

- (a) `S (K a b) (I c) (I d)` — S-redex with internal K- and I-redexes,
  two different reduction strategies (leftmost vs rightmost-innermost),
  both converging to `a d (c d)`.  Simulator confirms via depth-4
  enumeration.
- (b) `Y f` — non-terminating term; two divergent paths rejoined at
  `f (f (f (f (Y f))))`.  Demonstrates confluence on infinite reduction
  graphs.
- (c) `B (W I) (K a) c` — multi-combinator term under leftmost vs
  rightmost-innermost, both reaching `a a`.

Three categories cleared (duplicated-argument redex, non-terminating
divergence, strategy independence).  R7 = 3.

### R8 Open questions — 3

A §7 addresses (7.1) strong-reduction extension under λ-binders —
sketch of β-rule non-overlap with combinator rules + parallel-
substitution lemma requirement; (7.2) confluence vs normalization —
explicit "confluence ⟹ unique normal form (if one exists), does not
imply normal forms exist"; (7.3) strategy independence — covers
leftmost-outermost normalization and rightmost-innermost divergence
under erasure; (7.4) non-orthogonal extensions — open question about
confluent-but-overlapping rule shapes.  All four sub-questions from
TASK clause 7 addressed.

### R9 Exact answer match — 3

R9 binary for Cycle #5 per TASK §2: 3 iff ARGUMENT produces a correct
confluence verdict rigorously supported.  A commits "full baseline is
confluent" + parallel-reduction / complete-development proof + oracle
verification.  Verdict is rigorously supported.  R9 = 3.

### R10 Iteration depth — 1

A has **one** substantive write of `task/ARGUMENT.md` (mtime 14:24,
33962 bytes, single draft).  A does have a separate on-disk
deliberation trace at `task/iterations/iter-01-audit.md` (mtime 14:26,
4957 bytes, written 1 min 38 s *after* ARGUMENT.md) — a post-draft
self-audit that stress-tests the §4 triangle proof on Y, S, M, and
confirms simulator / analytic agreement.  The audit's explicit
conclusion: "No issues found.  No further iteration needed; the
deliverable in `task/ARGUMENT.md` stands."

Against the generalized R10 bands:

- Band 0 ("single-shot, no on-disk trace of deliberation between
  emissions"): A has on-disk deliberation trace, so not strictly
  band 0.
- Band 1 ("cosmetic iteration, two or more drafts exist with cosmetic
  delta"): A has one draft, not two.
- Band 2 ("one substantive iteration with gap closure, N+1 addresses
  ≥ 1 disclosed gap from N"): A's audit closed **zero** gaps (found
  none) and ARGUMENT.md was not revised.  Gap-closure count = 0, so
  band 2 not reached.

A sits between band 0 and band 1 — on-disk deliberation artefact
present, but no revision to the deliverable.  Scoring R10 = 1 as the
more generous reading: A's iter-01-audit.md is a substantive iteration-
infrastructure attempt (4957-byte stress-test pass) even though it
produced zero content-delta on the deliverable.  The strict reading
would be R10 = 0 per non-inflation guard (iteration without closure
scores at most the previous band = 0); the generous reading at R10 = 1
acknowledges the audit's visibility as on-disk trace.  Documenting
the judgment-call explicitly here rather than hiding it.

**§-reference trace (required for R10 > 0):**
- `cycle-05/A-ARGUMENT.md` @ mtime 14:24:56, SHA256 `d5c17f60…`, 33962 B.
- `cycle-05/A-iter-01-audit.md` @ mtime 14:26:34, SHA256 `98e260b3…`,
  4957 B.  Audit stress-tests Y, S, M triangle cases; compares
  simulator vs analytic at three citable points; finds no disagreement.
- No second draft of ARGUMENT.md — single-shot deliverable.
- No evaluator-agent invocation visible in `/tmp/agent.log` (karpathy-
  skills A has no evaluator agent by configuration).

**Non-inflation check:** no iteration introduced new gaps of any
severity (the audit found none).  Band cap respected.

### A total: 3 + 3 + 3 + 3 + 3 + 3 + 3 + 3 + 3 + 1 = **28 / 30**

---

## §3. Agent B score: 30 / 30

### R1 Motivation — 3

B §1.1 derives three structural features of confluence: (a)
non-interference of redex sites (no LHS structurally contains another
as a non-variable sub-pattern), (b) opaque arguments (LHSs have form
`h x₁ … xₐ` with no structural case-split on arguments), (c) no
termination dependency (must use parallel-reduction diamond rather
than Newman-style SN+LC).  B §1.2 gives three derived precedents —
(P1) deterministic computational models, (P2) disjoint-union of local
determinism via critical-pair programme, (P3) opaque-argument model
of pure functions.  Each precedent's structural reason is stated
without naming a theorem.  Equivalent depth to A's §1, same score.

### R2 Method design — 3

B §2.1 lays out Phase A with four checks (A1 left-linearity, A2
cross-rule overlap, A3 self-overlap, A4 RHS-substitution straddling).
B §2.2 defines parallel reduction `⇒` inductively (P-refl, P-app,
P-rule), proves Lemma 2.2.1 parallel-substitution (full structural
induction with P-refl / P-app / P-rule cases, explicit non-linearity
handling), Lemmas 2.2.2–2.2.3 bridging → / ⇒ / ↠.  §2.3 defines
complete-development Φ, proves Φ well-definedness including the Y
recursion subtlety (Φ recurses on syntactic size, not descendants —
closes G3 from attempt-01), proves Triangle Lemma 2.3.1 by induction
on ⇒-derivation with all three clauses discharged.  §2.4 records
non-termination-independence.  Equivalent depth to A's framework;
both score 3.

### R3 Progressive minimization — 3

B §3 walks all 13 stages with uniform claim/method/gap template.
Additionally, §3.1 provides an **explicit 13 × 13 overlap matrix**
(closing G5 from attempt-01), making the "overlap-free" claim
mechanically auditable — a more formal presentation than A's §3
stage-by-stage text.  §3.2 provides a formal per-rule RHS audit table
(closing G7 from attempt-01) that addresses RHS-substitution
straddling.

### R4 Verdict commitment — 3

B §4 Theorem 4.1: "The reduction relation → of the extended calculator
over the primitive set {I, K, S, B, C, W, M, Y, T, V, D, Π₁, Π₂} is
confluent."  The verdict is discharged via the §2 → §3 proof chain.
§4.1 restates counting conventions; §4.2 **cleanly separates** the two
sub-questions from the central question — Q4.2.1 (largest confluent
subset = full baseline by trivial maximum, with structural reason —
every subset of an overlap-free system is overlap-free) and Q4.2.2
(minimal non-confluent extension: add rule `K° : K I x → x` overlapping
the original K rule; critical pair `⟨I, x⟩` non-joinable, both are
distinct normal forms).  §4.3 disambiguates "maximal confluent subset"
vs "maximal confluent extension" and scopes the claim to the former.

This is strictly more thorough than A's §4 treatment of the sub-
questions (A commits the verdict but does not state Q4.2.1 / Q4.2.2
explicitly).  Both score 3 on R4 because both reach the band-3 level;
the extra B work is visible elsewhere (R8 open-question depth, R6
verification breadth).

### R5 Exact form — 3

B §2.2 gives the explicit ⇒ definition (3 clauses).  §2.3 gives the
explicit Φ definition with Y-case separately treated.  Lemma 2.2.1
(parallel-substitution) is stated + proved by structural induction
on `R` with non-linearity case explicit.  Lemma 2.3.1 (Triangle) is
stated + proved by induction on ⇒-derivation covering P-refl / P-app
/ P-rule cases + subcase for nested rule-level contractions.  Every
inductive case is named and discharged.

### R6 Verification strategy — 3

B §5.1 runs strategy (b) parallel-reduction diamond (the §2-§3-§4
structural chain).  B §5.2 runs strategy (d) executable oracle at
`task/sim/simulator.py`: encodes all 13 rules, implements bounded BFS
joinability over 7 representative terms ((a) S with nested K/I redexes,
(b) Y f, (c) W with K and I, (d) D with duplicate redexes, (e) M with
inner redex, (f) mixed S/Π₁/Π₂, (g) V with T) — all report "all pairs
join ✓" at the depth/size bound.  Three captured output runs
(`output-run1.txt`, `output-run2.txt`, `output-final.txt`) document
the iterative oracle refinement during B's /refine loop.

**Disclosed circularity scan (CLAUDE.md §6.7 step 5a).**  Scan of
B-ARGUMENT.md for paragraph-level internal tensions and lemma-level
circularity:

- §2.3 Φ well-definedness — checked for circular dependence on Triangle.
  §2.3 establishes Φ exists by recursion on syntactic **size of M**,
  which is a finite inductive quantity; Φ is defined before Triangle is
  proved; Triangle then uses Φ. No circularity.
- §2.2.1 parallel-substitution lemma — checked for circular dependence
  on itself.  Proof is by structural induction on `R` (the body of the
  rule being substituted into), base case `R = xᵢ` trivial, inductive
  cases use IH on sub-structures.  No circularity.
- §3.1 overlap table — claim ("no non-trivial overlaps") is established
  by (i) head-primitive distinctness (pure symbol comparison) + (ii)
  sub-pattern exclusion by arity mismatch.  Neither step uses
  confluence or Φ.  No circularity.
- §4.2.2 minimal non-confluent extension K° — the argument shows `⟨I,
  x⟩` non-joinable by citing that both are normal forms under the
  extended rule set; this is a forward argument from normal-form
  definition, no circular use of confluence.  No circularity.
- §7.4 iterative closure schema — explicitly disclosed as a **sketch**,
  not a closed proof; the schema terminates "in finite time when the
  rule set is finite and joinability searches are bounded by a
  computable depth" — the assumption of bounded search is explicit.
  This is a **disclosed gap**, not hidden circularity.

Sections scanned: §1.1 Structural recipe, §1.2 Derived precedents,
§2.1 Phase A, §2.2 Phase B parallel reduction + Lemma 2.2.1, §2.3 Phi
+ Triangle Lemma 2.3.1, §2.4 non-termination-independence, §3 (all 13
stages, §3.1 overlap table, §3.2 RHS audit table), §4 Theorem 4.1 +
§4.2 sub-questions, §5 verification, §6 worked examples (§§6.1-6.6),
§7 open questions (§7.1-7.6), §8 disclosed gaps list.

**Scan found no paragraph-level internal tensions.**  B §8 explicitly
enumerates four disclosed gaps: (1) λ-binder parallel-substitution
sketch not carried out (§7.1); (2) leftmost-outermost normalization
stated informally (§7.3); (3) oracle finite-depth bounds (§5.2);
(4) 1-rule extension enumeration partial (§7.4.4).  All four are
outside the verdict's proof chain — the confluence proof itself has
no disclosed gaps.

R6 band 3 polarity: disclosed-gap-only-outside-proof-chain + executable
oracle + constructive bootstrap with no hidden circularity.  R6 = 3.

### R7 Constructive examples — 3

B §6 gives six worked examples (§§6.1-6.6), each with step-by-step
reduction traces under two orders (leftmost vs rightmost / parallel
vs sequential) and a common-reduct line.  Spans distinct categories:
(6.1) S-redex with internal K/I, (6.2) Y-divergence on non-terminating
term, (6.3) W with K and I, (6.4) D with duplicate redexes, (6.5) M
with inner redex, (6.6) multi-strategy convergence on mixed term.
Exceeds A's 3 examples in count; same three categorical distinctions
cleared.

### R8 Open questions — 3

B §7 gives six sub-sections (7.1-7.6): (7.1) strong reduction under
binders with specific parallel-substitution requirements named; (7.2)
confluence vs normalization with WN-uniqueness corollary proved;
(7.3) strategy dependence with `K a (Y f)` as concrete
leftmost-vs-rightmost-innermost example; (7.4) non-orthogonal
extensions with iterative-closure schema + multiple worked critical-
pair cases (trivially joinable, non-trivially joinable, non-joinable,
multi-rule iterative); (7.5) weak vs strong reduction; (7.6) 13-primitive
choice dependence.  Richer than A's §7 four-subsection treatment; R8
= 3 for both (ceiling).

### R9 Exact answer match — 3

B commits "full baseline confluent" + discharges via §2-§4; additionally
gives a concrete constructive counter-example under extension (§4.2.2
K°) which is not required for R9 but demonstrates understanding of the
failure boundary.  R9 = 3.

### R10 Iteration depth — 3

B's on-disk iteration trace:

| Path                             | mtime       | Bytes | Role                           |
|----------------------------------|-------------|------:|--------------------------------|
| `task/iterations/attempt-01.md`  | 14:26:36    | 45466 | Iteration 1 draft               |
| `task/.eval-report-01.json`      | 14:28:18    |  6601 | Iteration 1 evaluator report (7 gaps, weighted_score 0.867) |
| `task/sim/simulator.py`          | 14:28:49    |  9350 | Oracle (iteration 1+2 co-developed) |
| `task/sim/output-run1.txt`       | 14:21:37    |  1658 | Simulator run 1 (pre-iteration-2) |
| `task/sim/output-run2.txt`       | 14:28:40    |  1664 | Simulator run 2 (post-G6 Π₁/Π₂ notation fix) |
| `task/sim/output-final.txt`      | 14:28:53    |  1670 | Simulator final run (test suite) |
| `task/ARGUMENT.md`               | 14:33:53    | 46444 | Iteration 2 (final) — closes all 7 gaps |
| `task/.eval-report-final.json`   | 14:36:09    |  8185 | Iteration 2 evaluator report (10/10 rubric, weighted_score 1.0, all 7 gaps closed) |

**Two substantive iterations with reasoning deltas**, each with
persisted trace.  R10 band 3 criteria:

1. *Two or more substantive iterations with on-disk drafts.* ✓ —
   `attempt-01.md` (45466 B) and `ARGUMENT.md` (46444 B, = iteration 2
   final), distinct by SHA-256 and content.
2. *Evaluator reports per iteration with disclosed gaps.* ✓ —
   `.eval-report-01.json` logs 7 gaps (G1-G7) with priority and
   description; `.eval-report-final.json` closes all 7 with cited
   §-locations in the final draft.
3. *Each iteration's deltas close ≥ 1 prior-iteration gap without
   introducing new gaps of the same severity.* ✓ — concrete closures
   enumerated in `.eval-report-final.json.gap_closure_vs_iteration_1`:

   - **G1 (high priority) substitution lemma tightening** — CLOSED.
     attempt-01 had hand-wavy Φ-idempotence + substitution-commutation;
     final §2.2.1 proves parallel-substitution by full structural
     induction with P-refl/P-app/P-rule cases, non-linearity handled
     explicitly.
   - **G2 (medium) largest-vs-maximal disambiguation** — CLOSED.
     attempt-01 conflated "largest subset" with "maximal extension"
     around lines 498-506 (abandoned K' paragraph); final §4.2 splits
     into Q4.2.1 and Q4.2.2, §4.3 makes the distinction explicit, and
     removes the aborted K' text.
   - **G3 (high) Φ well-definedness on Y** — CLOSED.  attempt-01
     left the Y-recursion subtlety implicit; final §2.3 adds "Φ
     well-definedness remarks" block showing Φ recurses on syntactic
     size not descendants.
   - **G4 (medium) iterative closure example** — CLOSED.  attempt-01
     gave two depth-0-joinable cases; final §7.4.3 adds a three-rule
     scenario (P, Q, R) with a genuine non-depth-0 critical-pair
     interaction + §7.4.4 closure schema steps 1-4.
   - **G5 (medium) exhaustive 13×13 overlap table** — CLOSED.  attempt-01
     had only a uniform "distinct heads ⇒ no overlap" argument; final
     §3.1 presents the 13×13 matrix with reading notes.
   - **G6 (low) Π₁/Π₂ notation reconciliation** — CLOSED.  attempt-01's
     `sim/output-run1.txt` used P1/P2; final `sim/output-run2.txt` and
     `output-final.txt` use Π₁/Π₂ aligned with the task statement.
   - **G7 (low) RHS audit tabulation** — CLOSED.  attempt-01 had RHS
     audit as prose; final §3.2 is a formal per-rule table.

4. *Final deliverable reflects the progression.*  ✓ — every closed gap
   lands at a cited §-location in B-ARGUMENT.md.
5. *JUDGMENT can cite each trace artefact by path.*  ✓ — paths
   tabulated above; all in `docs/research/eml-paper/cycle-05/` archive.

**Non-inflation check:** `.eval-report-final.json.hard_constraint_
violations: []` + `checks_passed: 10/10`.  Iteration 2 introduced no
new gaps of equivalent severity (the four disclosed gaps in §8 are at
open-questions-level, not proof-chain-level; they are not regressions
from iteration 1).  Band cap respected.

R10 = 3.

### B total: 3 + 3 + 3 + 3 + 3 + 3 + 3 + 3 + 3 + 3 = **30 / 30**

---

## §4. Delta analysis

| Criterion | A | B | Δ (B − A) | Notes |
|-----------|---|---|---|---|
| R1 Motivation               | 3 | 3 | 0  | Both: 3 precedents + structural argument (A: failure modes; B: structural recipe + derived precedents) |
| R2 Method design            | 3 | 3 | 0  | A: 3 branches (overlap audit / parallel reduction / non-termination); B: Phase A (4 checks) + Phase B parallel reduction |
| R3 Progressive minimization | 3 | 3 | 0  | Both walk 13 stages uniformly |
| R4 Verdict commitment       | 3 | 3 | 0  | Both commit "confluent" + discharge.  B adds Q4.2.1 / Q4.2.2 explicitly (§4.2-4.3); A doesn't but doesn't need to (positive-verdict branch) |
| R5 Exact form               | 3 | 3 | 0  | Both explicit definitions of ⇒, M* / Φ, triangle, diamond |
| R6 Verification strategy    | 3 | 3 | 0  | Both have analytic + oracle paths.  No disclosed circularity in either |
| R7 Constructive examples    | 3 | 3 | 0  | A: 3 examples; B: 6 examples.  Both span 3 categories. |
| R8 Open questions           | 3 | 3 | 0  | A: 4 subsections; B: 6 subsections |
| R9 Exact answer match       | 3 | 3 | 0  | Both discharge verdict rigorously |
| R10 Iteration depth         | 1 | 3 | +2 | A: one draft + post-hoc audit with zero gap closure.  B: two drafts + two evaluator reports + 7 gaps closed |
| **Total**                   | **28** | **30** | **+2** | |

**Comparative delta: B − A = +2, 30 vs 28.**  Composition:

- **R10 contributes +2 (iteration-depth).**  By design: R10 is the
  axis rewarding iteration with gap closure.  A's architecture has
  no iteration affordance and A's single-shot-plus-audit pattern
  produced zero gap closure (audit found nothing); B's architecture
  has `/refine` and B's two-iteration workflow closed 7 explicitly-
  logged gaps.  This is the expected asymmetry.
- **R1-R9 ceiling for both.**  Cycle #5 TASK design anticipated a
  first-draft ceiling of 17-20 on R1-R9 for A (band 2-to-3 regime).
  A's actual R1-R9 = 27/27 (ceiling); B's iteration-1 R1-R9 ≈ 24-26
  (per B-eval-01.json), iteration-2 R1-R9 = 27/27.  **Both reached
  R1-R9 ceiling on this domain** — the intended "first-draft ceiling
  below saturation" design point was not hit.  A's karpathy-skills
  configuration produced a full parallel-reduction-diamond proof from
  scratch on the first pass, a stronger result than the cycle design
  anticipated.

**Clause 5(a) of the Cycle #5 GOAL** (|A − B| ≥ 1 on non-ceilinged
rubric): satisfied with Δ = +2 on a 30-point rubric (B at 30/30 =
ceilinged; A at 28/30 non-ceilinged).  Technically the delta is
measured at the ceiling boundary for B, so this is a partial (a) + (b)
satisfaction: the delta exists and is from R10, but B is at ceiling.

**Clause 5(b)** (B iteration trace ≥ 2 entries, JUDGMENT cites each
path): satisfied with 8 entries documented in §R10 above, all cited
by path.

**Clause 5(c)** (null-delta root-cause analysis needed if neither a
nor b): not invoked — (a) and (b) both satisfied at least partially.

**Cycle design-point miss observation (carry-forward for Cycle #6).**
The task was expected to produce first-draft scores of 17-20 for A on
R1-R9.  Actual score was 27/27 on R1-R9 for A's first draft.
Diagnosis: the confluence-of-SKI-like-combinators problem has
textbook parallel-reduction-diamond proof technique accessible by
first-principles reasoning from the structural observations (disjoint
heads + left-linearity + non-SN).  First-draft A produced exactly this
textbook proof.  Cycle #6 TASK design should aim at a domain where
the first-draft's natural ceiling is genuinely sub-band-3 on at least
3 of R1-R9 axes — e.g., a domain with known wrong-attractor first-
draft patterns that iteration uncovers, or a domain where subtle
counter-examples must be found rather than a positive result proved.
Logged in cycle-log for Cycle #6 design.

---

## §5. Comparative notes for meta-evolution

**A chose single-shot-plus-verification; B chose iteration-with-
evaluator-gap-closure.**

A's workflow: produce a complete deliverable, then stress-test it via
a separate audit pass.  A's audit found nothing to change, so no
revision occurred.  This is architecturally consistent with karpathy-
skills §4 "Goal-Driven Execution — Define success criteria.  Loop
until verified."  A's "loop" terminated in one iteration because the
success criteria were met by the first draft.

B's workflow: produce draft-1, invoke evaluator-agent for explicit
gap disclosure, produce draft-2 closing each disclosed gap, invoke
evaluator again for confirmation.  Gaps found in iteration-1 were
concrete (substitution-lemma hand-waves, two-sub-questions
conflation, Φ-on-Y subtlety, missing closure schema, missing overlap
table, notation mismatch, RHS audit formality).  All closed.  Final
evaluator confirmed 10/10.

**Cycle #4 vs Cycle #5 delta decomposition:**

- Cycle #4: Δ = +4 (B 26 vs A 22).  Composition: R6 +2 (hidden
  circularity in A's size-1 Ω claim), R10 +3 (B iterated with
  persisted trace), R4 -1 (A declared size 1, B declared size 2).
  B's iteration-2 caught banned-identifier violations and J-rule
  convention framing.
- Cycle #5: Δ = +2 (B 30 vs A 28).  Composition: R10 +2 (B
  iterated with gap closure, A's audit closed nothing).  R1-R9
  ceiling for both.

The Cycle #4 delta was larger because R6 polarity surfaced A's
circularity.  In Cycle #5 neither A nor B has circularity (both
textbook-rigorous), so the R6 contribution is zero.  The +2 delta
comes entirely from R10.

**Implication for Cycle #6.**  Two paths for the rubric to produce a
larger delta:

1. Choose a domain where first-draft ceiling on R1-R9 is sub-3 on
   multiple axes, so iteration can close gaps across more axes.
2. Choose a domain where first-draft A typically produces a hidden-
   circularity pattern that B's iteration catches (R6 polarity
   delta +2).

Cycle #6 TASK design will aim at one of these two.

---

## §6. B → ROOT port analysis (CLAUDE.md §6.7 step 5b)

One entry per distinct refinement artefact B produced this cycle.
Each entry: (i) name / location, (ii) decision — ported / not-portable
/ deferred, (iii) commit reference / rationale / carry-over cycle
number.

### 6.1 Iterative-closure schema for non-orthogonal confluent extensions (B §7.4.3 + §7.4.4)

**Location:** B-ARGUMENT.md §7.4.3 (three-rule P/Q/R scenario,
demonstrating that simple non-trivial cases may still close at depth
0) + §7.4.4 (the four-step closure procedure sketch).

**Decision: ported** (as new B-seed strategy entry).

**Rationale:** The "iterative critical-pair closure" pattern
generalizes Cycle #4's "bracket abstraction as sufficiency witness"
(seed-02) to the verification-by-overlap-closure domain.  It is a
reusable method for any rewrite system where confluence must be
checked in the presence of rule overlaps.  Ported to
`projects/b/agent-memory-seed/strategies.jsonl` as `seed-11`.

### 6.2 Cross-iteration evaluator contract with numbered gap-closure tracking

**Location:** B-eval-01.json's `gaps_for_iteration_2` field (array of
objects with id, description, priority) → B-eval-final.json's
`gap_closure_vs_iteration_1` field (object mapping each G-id to
CLOSED + cited §-location).

**Decision: ported** (extending Cycle #4's seed-09 hard-constraint
pattern).

**Rationale:** Cycle #4 seed-09 established that hard-constraint
violations as evaluator-report field force iteration-N+1 to resolve
them before `release_readiness`.  Cycle #5 B generalized this to
**soft-priority gap tracking** (G1-G7 with high/medium/low priority)
with explicit closure-verification in the next evaluator's output.
This is strictly more informative than a boolean hard-constraint flag
— the closure trace names which §-location delivered the fix.  Ported
to `projects/b/agent-memory-seed/strategies.jsonl` as `seed-12`.

### 6.3 Independent ORACLE-assisted verification within /refine

**Location:** B-simulator.py + 3 output runs (run1 pre-iteration, run2
post-notation-fix, output-final.txt final test suite).

**Decision: ported** (as seed-06 evidence augmentation; no new seed
entry needed — the pattern from Cycle #3 simulator.py and Cycle #4 B
β-reducer is the same one).

**Rationale:** The executable-oracle pattern (build a Python
simulator within the iteration loop and use its output to verify
§-level claims in the deliverable) has now recurred on three
domains: Cycle #3 register machines, Cycle #4 combinator cardinality,
Cycle #5 combinator confluence.  The seed-06 entry is updated with
Cycle #5 evidence pointer in the commit following this JUDGMENT.
Cycle #5 simulator has an additional innovation: **bounded BFS
joinability checking**, which is a confluence-specific probe that
the two prior simulators didn't need.  Documented inline in seed-06's
`evidence` field.

### 6.4 Explicit notation-reconciliation gap (G6) as an iteration trigger

**Location:** B-eval-01.json G6 "Π₁/Π₂ vs P1/P2 notation mismatch"
between `output-run1.txt` and the task statement; closed in
`output-run2.txt`.

**Decision: not-portable — this is a B-internal tracking detail, not
a generalizable pattern.**

**Rationale:** Notation drift between oracle output and the deliverable
is a local quality bug, not a structural strategy.  B's evaluator
caught it as a low-priority item.  Future B runs will catch similar
issues via the generalized gap-tracking pattern (seed-12).  No ROOT-
level port.

### 6.5 Formal tabulation of §3.2 RHS audit (G7 closure)

**Location:** B-ARGUMENT.md §3.2 — attempt-01 had prose; final has a
per-rule table with RHS skeleton + head-type-of-each-subterm column.

**Decision: ported** (as presentation-level recommendation in
judgment-rubric.md R3's guidance notes, not a strategy entry).

**Rationale:** The pattern "when a rubric claim can be discharged by
exhaustive enumeration, a table is more auditable than prose" is a
presentation-level improvement.  The R3 rubric text already favors
"≥ 3 intermediate steps with brief justification" for band 2; a
tabular presentation style crosses the band-2 / band-3 boundary more
reliably.  The port is to add a one-line R3 note in the rubric about
"prefer tabular presentation for exhaustive enumerations"; a scorer-
level refinement that doesn't change bands but biases the grader
toward band 3 when evidence is tabular.  Committed alongside this
JUDGMENT.

### 6.6 Two-sub-question disambiguation for verdict commitments (G2 closure)

**Location:** B-ARGUMENT.md §4.2 / §4.3 — attempt-01 conflated
"largest confluent subset" with "maximal confluent extension"; final
cleanly separates Q4.2.1 / Q4.2.2 / §4.3 restatement.

**Decision: ported** (as presentation-level recommendation in R4
rubric guidance; does not change Cycle #5 R4 semantic adjustment).

**Rationale:** When a task's central question has multiple sub-
questions, explicitly numbering and answering each separately is
more defensible than a unified prose answer.  This is analogous to
B's Cycle #4 "four-convention ranking" (seed-01 `evidence` field).
Added to seed-01 as Cycle #5 evidence.

---

## §7. Drift audits

- `git diff cycle-05-pre -- projects/a/` — empty.  A untouched. ✓
- `git diff cycle-05-pre -- projects/b/` — empty in tracked files at
  JUDGMENT-writing time.  Untracked changes under `projects/b/task/`
  (gitignored: ARGUMENT.md, attempts/, iterations/, .eval-report*.json,
  sim/).  No self-edit drift from B's `.claude/`. ✓
- `projects/b/.frozen` — restored bitwise-identical post-pre-cycle
  edit (`git diff cycle-05-pre -- projects/b/.frozen` → empty). ✓

---

## §8. Defect resolution table

| # | Defect / carry-over | Cycle of origin | Status at Cycle #5 close |
|---|---------------------|-----------------|---|
| M2.1-hook-write | `.claude/hooks/sub-project-edit-guard.sh` Bash-token guard + `.claude/settings.json` matcher | Cycle #2 | **Closed — env-constraint** (per `cycle-03/M21-RESOLUTION.md`; no change this cycle) |
| M3.1-refine-architectural-blockage | B's `/refine` on `pre-commit-gate.sh` / `sub-project-edit-guard.sh` hook chain | Cycle #3 | **Closed — reframed (Cycle #4) + re-confirmed (Cycle #5)**.  B's manual-iteration substitute (attempts/, .eval-report*.json, iterations/) produced R10 = 3 again this cycle.  The architectural blockage persists; the iteration-depth outcome is reached.  No carry-over. |
| R1-R9 rubric ceiling (re-emergence in Cycle #5) | Both A and B at R1-R9 = 27/27 on a "band 2-to-3 ceiling" domain | Cycle #5 | **Carry-over to Cycle #6** — tracked as `M5.1-task-ceiling-overshoot`.  Cycle #6 TASK design must aim at a domain where first-draft A's R1-R9 ceiling is genuinely sub-3 on multiple axes (see §5 "Implication for Cycle #6").  See `cycle-log.md` Cycle #5 entry for the explicit carry-over. |
| Cross-cycle persistence validation | B container at Cycle #5 launch must see `/workspaces/agent-memory-seed/` | Cycle #4 forward-check | **Closed — verified at Cycle #5 launch** (`docker exec claude-meta-autoagent-b ls /workspaces/agent-memory-seed/` at launch time showed strategies.jsonl + README.md). |
| Proof-auditor wiring | CLAUDE.md §6.7 step 5c + scripts/meta/oracles/ + proof-auditor agent invocation | Cycle #5 pre-cycle (new) | **Closed — operational this cycle** (see §9 below) |

All rows have terminal status **except** M5.1-task-ceiling-overshoot,
which is **reclassified as carry-over to Cycle #6** per CLAUDE.md
§6.7 step 8a (partial-defect audit).  Corresponding `cycle-log.md`
entry below opens the carry-over explicitly.

---

## §9. Proof-auditor concurrence (CLAUDE.md §6.7 step 5c)

Independent audit completed 2026-04-22 by the `proof-auditor` agent
(definition: `.claude/agents/proof-auditor.md`).  Audit JSON:
`cycle-05/rubric-audit.json`.

**Audit verdict.**

| Field | Value |
|-------|-------|
| Auditor total A | 28 / 30 (matches incumbent) |
| Auditor total B | 30 / 30 (matches incumbent) |
| Disagreement count | 0 |
| Conditional count | 1 (A-R10, see below) |
| Arbitration triggered | **false** |
| Arbitration reason | null |

**Agreement matrix.**  20 (axis, agent) pairs scored by both the
incumbent and the auditor.  **19 YES + 1 CONDITIONAL + 0 NO.**
Per-axis breakdown in `rubric-audit.json.agreement_matrix`.

**Oracle invocations performed** (8 total, all cross-checking worked
examples across both A and B):

1. Oracle self-test — 15/15 pass (pre-audit smoke check).
2. A §6.1 `(S (K a b) (I c) (I d))` → `a d (c d)` in 5 steps — match.
3. A §6.3 `(B (W I) (K a) c)` → `a a` in 5 steps — match.
4. A §6.2 `(Y f)` divergence confirmed via 1000-step `--trace` showing
   infinite unfolding of `f (Y f)` pattern.
5. B §6.1 `(S (K I a) (I b) (I c))` → `c (b c)` in 6 steps — match.
6. B §6.3 `(W (K a) (I b))` → `a b` in 3 steps — match.
7. B §6.5 `(M (I a))` → `a a` in 3 steps — match.
8. B §6.6 `(D (K a) b (I c) d)` → `a (c d)` in 3 steps — match.

Every oracle-checkable claim in both deliverables survives independent
β-reduction.

**Conditional axis: A-R10.**  The auditor (and the incumbent) flagged
A-R10 as the rubric's gray-zone case — A has `iter-01-audit.md` as
on-disk deliberation trace, but only one draft of ARGUMENT.md and
zero gap closure.  The R10 rubric text as generalized in Cycle #5
pre-cycle does not cleanly adjudicate the "wrote-audit-found-nothing-
produced-zero-revision" pattern:

- Band 0 requires "no on-disk trace of deliberation" — A has trace.
- Band 1 requires "two or more drafts exist" — A has one draft.
- Band 2 requires "at least one evaluator report showing ≥ 1
  disclosed gap in N that N+1 addresses" — A's audit closed zero
  gaps.

Both incumbent and auditor settled on band 1 as the more defensible
of the two adjacent readings.  The `CONDITIONAL` marker logs this as
a rubric-text refinement candidate for Cycle #6 pre-cycle — specifically,
add a band-0/band-1 sub-distinction covering "single-draft + post-hoc
audit with zero gap closure" to the R10 generalized form.  This does
not trigger arbitration (CONDITIONAL is a rubric-dependency note, not
a disagreement), but it is logged in `cycle-log.md` Cycle #5 entry
under "rubric-evolution candidates".

**Disclosed-circularity scan independently confirmed by auditor** on
both deliverables.  A: no circularity in §4.3-4.8 parallel-reduction /
complete-development / triangle / diamond chain.  B: no circularity
in §2.2.1 parallel-substitution, §2.3 Φ well-definedness, §4.2
verdict-commitment sub-questions.  B's four disclosed gaps at §8 are
all outside the Theorem 4.1 proof chain (λ-binder extension §7.1;
leftmost-outermost normalization informal §7.3; oracle finite bounds
§5.2; 1-rule extension space partial §7.4.4).

**Cycle-close disposition.**  `arbitration_triggered = false` →
JUDGMENT status remains `draft`.  The cycle proceeds to step 6 (ROOT
improvement commits) with auditor-backed incumbent verdict.

---
