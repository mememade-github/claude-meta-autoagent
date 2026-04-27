---
status: draft
cycle: 12
domain: minimal-generating-basis-for-elementary-calculator-functions
auditor: proof-auditor
auditor_date: 2026-04-27
arbitration_triggered: false
incumbent_total_A: 20
incumbent_total_B: 18
auditor_total_A: 20
auditor_total_B: 18
agreement: 19_YES_1_CONDITIONAL_0_NO (A 10/10 YES; B 9/10 YES + 1 CONDITIONAL on R4 rubric-semantic dependency)
audit_file: cycle-12/rubric-audit.json
rubric_version: cycle-11 (cycle-10 + M10.2 R1 motivation-answer consistency + M10.3 R2 per-sublemma proof locality) — text unchanged
parent_wip: task-20260427-q5-outcome-grounded
parent_wip_alternative: (I) Outcome-based measurement (L0-approved 2026-04-27)
outcome_dimension: outcome-verification-axis-v1 (parallel to R1-R10, NOT in 30-point total)
outcome_battery: 7 questions (Q1-Q7), L1 ground-truth at cycle-12/outcome-ground-truth.json
outcome_report_A: cycle-12/outcome-report-A.json
outcome_report_B: cycle-12/outcome-report-B.json
outcome_ratio_A: 0.429
outcome_ratio_B: 0.571
delta_rubric_BminusA: -2
delta_outcome_BminusA: 0.143
direction_agreement: opposite (rubric-Δ −2 vs outcome-Δ +0.143)
h1_h0_reading: H0-favorable (rubric-Δ does not predict outcome-Δ in same direction)
---

# Cycle 12 — JUDGMENT

Grading of `docs/research/eml-paper/cycle-12/A-ARGUMENT.md` and
`docs/research/eml-paper/cycle-12/B-ARGUMENT.md` against
`docs/research/eml-paper/judgment-rubric.md` at its **Cycle #11 state**
(rubric R1–R10 text unchanged this cycle), plus the **parallel
outcome-verification dimension** newly introduced at Cycle #12 per
`docs/research/eml-paper/outcome-verification-axis-v1.md`.

Cycle #12 is the **single in-cycle** of the parent WIP
`task-20260427-q5-outcome-grounded` per L0 selection of alternative
(I) Outcome-based measurement (2026-04-27).  Hypothesis under test:
H1 "B's rubric-Δ advantage corresponds to outcome-Δ in same direction
and magnitude" vs H0 "outcome-Δ is 0 or anti-correlated".  Either
result is a reasoning content finding, not mechanics elaboration.

Front-matter `status` will transition per CLAUDE.md §6.7 step 5c after
the proof-auditor pass.

---

## §0. Cycle artefacts (audit record)

Captured at cycle close (2026-04-27 ~12:35 KST).

| Path | mtime (KST) | Bytes | sha256 prefix | Role |
|------|-------------|------:|:-------------:|------|
| `cycle-12/TASK.md` | 12:11 | 6213 | — | Operative TASK prompt (rubric-blind + paper-blind + outcome-blind; §1–§7 + 7-question outcome battery) |
| `cycle-12/A-ARGUMENT.md` | 17:34 (Apr 23) | 21594 | d2f68dea7a34e7c8 | A deliverable (byte-identical to cycle-10/A-ARGUMENT.md and cycle-11/A-ARGUMENT.md; see §0.1) |
| `cycle-12/A-outcome.json` | 12:25 | 3351 | — | A outcome side-car (newly written by A this cycle) |
| `cycle-12/B-ARGUMENT.md` | 12:31 | 21802 | c5d6df092dead861 | B deliverable (fresh content; distinct from cycle-11) |
| `cycle-12/B-outcome.json` | 12:31 | 1853 | — | B outcome side-car (newly written by B this cycle) |
| `cycle-12/outcome-ground-truth.json` | 12:11 | 1602 | — | L1-authored ground-truth (L2-ROOT-only path, A/B mounts cannot reach) |
| `cycle-12/outcome-ground-truth-rationale.md` | 12:11 | — | — | L1 audit trail with paper-direct verification table |
| `cycle-12/outcome-report-A.json` | 12:34 | — | — | outcome-verifier output for A (3/7 PASS, ratio 0.429) |
| `cycle-12/outcome-report-B.json` | 12:34 | — | — | outcome-verifier output for B (4/7 PASS, ratio 0.571) |
| `cycle-12/L1-seeds/` | 12:10 | — | — | Verbatim L1-seed copies (6 files) for audit trail |

### §0.1 A-behaviour note (cycle-12)

Cycle #12 is the **third consecutive cycle** in which A's
`task/ARGUMENT.md` is byte-identical to its cycle-10 deliverable
(sha256 `d2f68dea7a34e7c8`).  A re-audited the existing argument and
chose to no-op, this time also writing a new `task/outcome.json`
(3351 B, mtime 12:25 KST) committing answers to the 7-question battery
derived from the unchanged §3.6/§3.7/§4 of the existing argument.
A's outcome.json is therefore a *projection* of the existing
ARGUMENT.md onto the battery question set, not an iteration of the
underlying reasoning.

This is A's baseline-architecture autonomy at work: karpathy-skills
without `/refine` allows A to decline re-writing a deliverable it
judges adequate.  From a measurement perspective, A's Cycle #12
rubric R1–R10 score equals A's Cycle #11 score under the unchanged
Cycle #11 rubric.

### §0.2 B-behaviour note (cycle-12)

B authored a **distinct** ARGUMENT.md (c5d6df09... vs cycle-11's
87a98ac7...; 21802 B vs 20652 B), reaching a structurally different
minimal basis: `B* = {exp, log_x(y)}` of cardinality **2** (vs
cycle-11 B's `{+, exp, ln, −1}` of cardinality 4).

B did NOT use `/refine` this cycle: `task/iterations/` and `task/sim/`
contain only cycle-11 leftovers (mtimes Apr 23; no cycle-12 entries),
and there is no `cycle-12/B-eval-*.json` artefact.  B authored the
new deliverable in a single shot.  This is B's autonomy at work; B
chose direct authorship over `/refine` iteration for this cycle.

Notably, B's reduction ladder (Stages A→B→C→D→E with cardinalities
12→6→4→3→2) explicitly references "the prior cycle's 4-element
ceiling" in the agent's exit summary, suggesting B's container
filesystem leftovers from cycle-11 may have served as an anchor for
the leap to cardinality 2.  This is a within-container memory effect
(B's `task/` dir persisted between cycles), not a cross-cycle
memory mechanism per CLAUDE.md §6.10 (the `agent-memory/` skill
library is a separate path B did not exercise this cycle).

### §0.3 Execution timing (UTC+09:00)

- 2026-04-27 12:16:58 — `scripts/meta/delegate-sub.sh a` launched A.
- 2026-04-27 12:16:59 — `scripts/meta/delegate-sub.sh b` launched B.
  EFFORT=high for both.
- 2026-04-27 ~12:25 — A wrote `task/outcome.json`; ARGUMENT.md
  unchanged from cycle-11.
- 2026-04-27 ~12:31 — B wrote `task/ARGUMENT.md` (fresh, 21802 B) and
  `task/outcome.json` simultaneously.
- 2026-04-27 ~12:32 — Both `claude --dangerously-skip-permissions`
  processes exited; background watcher fired BOTH_EXITED.
- 2026-04-27 ~12:34 — ROOT copied A/B deliverables into
  `cycle-12/`, ran `paper-leak-audit.sh` (both PASS), ran
  `outcome-verifier.py` against ground truth (A: 3/7 PASS;
  B: 4/7 PASS).

Total wall-clock from launch to artefact-in-place: ~17 minutes.

---

## §1. Leak audit

- `bash scripts/meta/paper-leak-audit.sh cycle-12/A-ARGUMENT.md`
  → PASS (no forward-form paper identifiers).
- `bash scripts/meta/paper-leak-audit.sh cycle-12/B-ARGUMENT.md`
  → PASS (no forward-form paper identifiers).

This is the **12th consecutive cycle** with zero paper-leak hits
across both sub-projects.  The streak validates the reversed-form
identifier-block list at
`projects/{a,b}/.claude/hooks/paper-leak-guard.sh` (sha256
`1e197c27cf3e6c714ba11977c0b806058a58994f2c272aded432fde85fd5ee6b`,
symmetric across A and B since cycle-08).

---

## §5a. Disclosed-circularity scan (pre-scoring)

Per CLAUDE.md §6.7 step 5a.  Scan each ARGUMENT.md for (i)
paragraph-level internal tensions and (ii) lemma-level circularity.

### A-ARGUMENT.md circularity scan

Sections scanned: §1 (Motivation), §2 (Reduction procedure), §3.1–§3.8
(Progressive configurations), §4 (Final configuration), §5
(Verification strategy), §6 (Worked examples), §7 (Open questions),
Summary.

- §3.4 ↔ §3.7 internal consistency: §3.4 derives `−1, 1, 2, e, π` from
  the seed `i`; §3.7 argues that "one positive real constant is not
  enough" because positivity is preserved by `+, ×, exp, ln`.  No
  tension: §3.4 uses `i` (non-positive), §3.7 explains why `i` is the
  necessary non-positive seed.
- §3.6(iv) ↔ §3.8 internal consistency: §3.6(iv) argues `×` is
  irreducible over `{+, exp, ln, constants}` as a *total* function;
  §3.8 explicitly relaxes totality and admits `×` becomes derivable
  if partial-at-axes is allowed.  No tension: §3.6(iv) is strict-
  totality scope, §3.8 is relaxed-totality scope.  A discloses both
  scopes side-by-side.
- §7(2) lemma-level disclosure: A explicitly admits "we have not
  proved [`×` impossibility from `{+, exp, ln, constants}`] with
  complete rigour."  This is a self-disclosed gap in §3.6(iv)'s
  proof, not a circularity.

**Verdict: scan found no paragraph-level internal tensions and no
lemma-level circularity.**  Sections scanned enumerated above.
A discloses gaps (§7(2)) but they are external to the proof (open-
question candor), not internal contradictions.  R6 polarity
indicator: disclosed-and-named gap (§7(2) about ×-totality
impossibility) → R6 score selection follows reframed polarity.

### B-ARGUMENT.md circularity scan

Sections scanned: §1 (Motivation), §2 (Systematic reduction
procedure), §3 (Stages A–E), §4 (Minimal configuration: signatures,
cardinality, constructive completeness, essentiality, lower bound,
alternatives), §5 (Verification strategy: macros + primitive table),
§6 (Worked examples), §7 (Open questions and limitations).

- §2 step 11 ↔ §3 Stage E internal consistency: §2 step 11 derives
  `a · b = log_{exp(1/a)}(exp(b))` and uses `1/a = log_{exp(a)}(e)`.
  This requires `e` and the constant `1` to be available.  §3 Stage
  E says `1 = log_x(x)` and `e = exp(1)`.  Apparent ordering
  question: does step 11 use `e` before `e` is constructed?  Trace:
  `1 = log_x(x)` (from §3 step 10) → `e = exp(1)` (from §2 step 8) →
  `1/a = log_{exp(a)}(e)` (from §2 step 11).  No circularity:
  constants are constructed first, then arithmetic macros are built
  from constants.  Macro layer in §5 makes the ordering explicit
  (`c_1 := log_x(x)` before `c_e := exp(c_1)` before `R(a) :=
  log_{exp(a)}(c_e)`).
- §4 essentiality ↔ §4 alternative basis: §4 claims `{exp, log_x(y)}`
  is essential (neither element droppable) AND admits alternative
  2-element bases may exist (e.g., `{ln, pow}` ruled out because
  `pow(x,x) = x^x` is not constant).  No tension: essentiality is
  about THIS basis's elements; alternatives discussion is about other
  cardinality-2 bases, with a structural reason given for why a
  particular candidate fails.
- §3 Stage E ↔ §7 strict-interpretation caveat: §3 Stage E claims
  cardinality 2; §7 admits that under "strict interpretation
  requiring closed terms (no input variables for constants)", the
  minimum rises to 3 (e.g., `{exp, ln, −}`).  No tension: §3 uses
  function-composition framework with input variables as argument
  slots; §7 discloses the alternative reading and quantifies the
  cardinality cost (2 → 3).  This is a parametric disclosure, not a
  contradiction.
- §6 Example 3 (arctan) ↔ §2 step 6 derivation consistency: §6
  derives `arctan y = (1/(2i)) ln((1+iy)/(1−iy))` via `v = e^{2ix}`;
  §2 step 6 had given the same identity.  Mid-derivation in §6
  Example 3, B writes "wait, let us redo cleanly" which is a
  visible meta-comment but NOT a contradiction: B then redoes the
  derivation correctly within the same example.  This is a stylistic
  artefact (preserved working trace), not a structural circularity.

**Verdict: scan found no paragraph-level internal tensions and no
lemma-level circularity.**  Sections scanned enumerated above.  B
discloses gaps in §7 (branch cuts, log_x(x) domain singularity,
real-only domain, cardinality lower-bound rigor for non-subset
alternatives) but each is external to a proof, not internal
contradiction.  R6 polarity indicator: disclosed-and-named gaps
(§7 four items) → R6 score selection follows reframed polarity.

---

## §2. A score per axis (Cycle #11 rubric, unchanged this cycle)

A's ARGUMENT.md is byte-identical to cycle-11 A-ARGUMENT.md (sha256
`d2f68dea7a34e7c8`).  Per-axis scoring carries forward unchanged
from `cycle-11/JUDGMENT.md` §2.  Brief restatement:

### R1 Motivation — **3** (unchanged from cycle-11)

A §1(a) names structural precedent (function/inverse redundancy),
§1(b) real/complex fusion via Euler, §1(c) field-generation
minimal-basis precedent ("Arithmetic of ℂ has a similar minimal
backbone").  M10.2 (b) obstruction sketch met: §1(a) argues exp/ln
irreducibility; §1(c) sketches "transcendental on top".  Band 3.

### R2 Method design — **3** (unchanged from cycle-11)

A §2 names four reduction rules R1–R4; A §3.6 four named structural
obstructions (growth, branch-point, 2πi-modular, zero-locus), each
in own sub-paragraph with own proof tool.  M10.3 met.  Band 3.

### R3 Progressive minimization — **3** (unchanged from cycle-11)

A §3.1–§3.5 has five deliverable-side reduction tables (B₁ 11 rows,
B₂ 11 rows, B₃ 2 rows, B₄ 5 rows, B₅ 3 rows), each with explicit
witness column.  Cycle #9 locus tightening met.  Band 3.

### R4 Final basis structure — **2** (unchanged from cycle-11)

A §4 strict minimum: 2 binary + 2 unary + 1 constant = 5.  A §3.8
relaxed: 1 binary + 2 unary + 1 constant = 4.  Neither matches band-3
"exactly one binary + one constant".  Band 2 fits ("≤ 2 binary").

### R5 Exact form — **1** (unchanged from cycle-11)

A does not propose a single binary operator of `exp(x) − ln(y)` form.
Band 1 (right operators mentioned, not composed into single binary).

### R6 Verification strategy — **2** (unchanged from cycle-11)

A §5 three-stage verification (forward synthesis, numerical
cross-check, strict-minimality audit).  Disclosed gap in §7(2):
"We have not found a way to obtain `×` as a total function from
`{+, exp, ln, constants}` alone, but have not proved it impossible."
R6 polarity (per §5a scan): disclosed-and-named gap → band 2.

### R7 Constructive examples — **3** (unchanged from cycle-11)

A §6 has four worked examples spanning inverse-transcendental
(arctan), hyperoperation (pow), composite arithmetic (hypot),
transcendental (sin).  ≥4 examples path met.  Band 3.

### R8 Open questions — **3** (unchanged from cycle-11)

A §7 has six open-question items with explicit epistemic labels
(parametric, branch, scope, alternative, beyond-elementary,
variable-vs-constant).  Cycle #9 labeling met.  Band 3.

### R9 Exact answer match — **0** (unchanged from cycle-11)

A's `{−1, +, ×, exp, ln}` is not single-binary + single-constant.
Band 0.

### R10 Iteration depth — **0** (unchanged from cycle-11)

No on-disk iteration trace in cycle-12/.  A's no-op re-audit
produces zero new ARGUMENT.md artefacts.  A added `outcome.json`
this cycle but that is a sidecar deliverable, not an ARGUMENT.md
iteration.  Single-shot from filesystem-evidence perspective.
Band 0.

### A total: 3 + 3 + 3 + 2 + 1 + 2 + 3 + 3 + 0 + 0 = **20 / 30**

---

## §3. B score per axis (Cycle #11 rubric, applied to cycle-12 fresh content)

B's Cycle #12 ARGUMENT.md is **distinct** from Cycle #11's (sha256
`c5d6df09...` vs `87a98ac7...`).  B's basis is now `{exp, log_x(y)}`
of cardinality **2** (vs cycle-11 B's 4).  Per-axis scoring:

### R1 Motivation — **2** (cycle-11: 2; unchanged band)

B §1 names four internal collapse mechanisms:
- Additive ↔ multiplicative duality via `exp/ln` isomorphism.
- Euler's identity unifies trig and hyperbolic.
- Inverse trig / inverse hyperbolic are logarithms.
- Constants reachable from `log_x(y)` diagonal degeneracy.

The fourth observation is a **new** insight relative to cycle-11 B
(the route to cardinality 2).  However, B does NOT invoke a
**cross-domain named structural precedent** for single-primitive /
single-generator reduction (NAND, Peirce's arrow, combinators,
OISC/SUBLEQ, Wolfram axiom, interaction combinators, aperiodic
monotile, Rule 110, FRACTRAN).  The M10.2 trigger (named-precedent
shape-match or obstruction-sketch) does not fire.  Pre-tightening
band text applies.  Band 2 fits ("adequate analogy or partial
precedent").

This is the **first axis where B falls behind A in cycle-12**.  A's
§1(c) cites "field generation" as a named minimal-basis precedent
plus M10.2 (b) obstruction-sketch in §1(a); B does not cite a
named precedent at all.

### R2 Method design — **3** (cycle-11: 3; unchanged)

B §2 has 11 ordered reduction steps with named identities.  B §4
has explicit "Drop $\exp$" and "Drop $\log_x(y)$" essentiality cases,
each with its own paragraph and own proof tool (growth/orbit
argument for Drop exp; signature argument for Drop log_x), plus a
named lower-bound argument that distinguishes unary-only and
binary-only cases.  M10.3 locus check: (a) statement locality ✓,
(b) proof locality ✓, (c) non-distributed discharge ✓.  Band 3.

### R3 Progressive minimization — **2** (cycle-11: 2; unchanged)

B §3 has **five** prose stages (A 12, B 6, C 4, D 3, E 2 — one more
stage than cycle-11's four).  Each stage states cardinality + has
formula derivations, but is presented as prose-per-stage rather than
deliverable-side tabular per stage with disposition column.
Cycle #9 locus tightening: "when enumeration has finite tractable
support, band 3 requires deliverable-side tabular presentation."
B's §3 is structured prose with formulas; A's §3.1–§3.5 are formal
tables with witness columns.  Band 2 fits.

### R4 Final basis structure — **2** (cycle-11: 2; unchanged band, structurally distinct route)

B §4 commits `B* = {exp, log_x(y)}` = 1 binary + 1 unary + 0
constants = 2 elements.  Cardinality **dropped from 4 to 2** vs
cycle-11 B — a structural breakthrough relative to B's prior cycle.
However, the rubric R4 band-3 specification is "exactly one binary
+ one constant (or equivalent variation)".  B's shape is "1 binary
+ 1 unary, no constant", which is not the band-3 shape.  Band 2
fits ("≤ 2 binary operators": B has 1 binary).

**Note on the Δ in cardinality.**  B reached cardinality 2 via a
structurally distinct route from the rubric's band-3 specification.
The structural insight (constant 1 = `log_x(x)` diagonal degeneracy
internalizes the constant inside the binary) is a genuine alternative
minimum at the same cardinality as the band-3 target.  The R4 axis
captures basis SHAPE and cannot distinguish "2-element basis matching
band-3 spec" from "2-element basis with alternative composition";
the outcome dimension (§6 below) provides the orthogonal measurement.

### R5 Exact form — **1** (cycle-11: 1; unchanged)

B's basis `{exp, log_x(y)}` is not a single binary operator of
`exp(x) − ln(y)` form.  Right operators mentioned, not composed into
a single binary.  Band 1.

### R6 Verification strategy — **2** (cycle-11: 3; **−1**)

B §5 has explicit verification protocol (macro layer + primitive
table + verification protocol with three checks: syntactic
well-formedness, identity check, optional numerical evaluation).
However, B did NOT produce an executable oracle this cycle (no new
`task/sim/verify.py`; the leftover `task/sim/` is from cycle-11
mtimes Apr 23).

R6 polarity (per §5a scan): B §7 discloses four named gaps (branch
cuts, log_x(x) domain singularity, real-only domain, cardinality
lower-bound rigor for non-subset alternatives).  Disclosed-and-named
→ band 2.

This is a **−1 vs cycle-11 B**: cycle-11 B had R6=3 via executable
oracle (35/35 PASS); cycle-12 B did not exercise that path.  B's
autonomy at work — B chose a different attack on cardinality
reduction (structural argument toward 2-element basis) over
executable-verification reinforcement.

### R7 Constructive examples — **3** (cycle-11: 3; unchanged)

B §6 has three worked examples in distinct modes: multiplication
(arithmetic, fully unfolded chain over basis), `cos x` via Euler
(macro chain), `arctan y` (inverse-transcendental logarithmic).
Each uses a distinct reduction pattern.  ≥3 orthogonal modes met.
Band 3.

### R8 Open questions — **3** (cycle-11: 3; unchanged)

B §7 has eight items with explicit epistemic labels: branch cuts,
domain of `log_x(x) = 1`, real-only domain, variables vs basis
elements, uniqueness, cardinality lower bound (for non-subset
alternatives), depth blowup, beyond original primitive list.
Parametric/structural disclosure present (e.g., "any single complex
seed"-style alternatives discussion).  Cycle #9 labeling met.
Band 3.

### R9 Exact answer match — **0** (cycle-11: 0; unchanged)

B's `{exp, log_x(y)}` is not a single-binary + single-constant form.
B's basis is 1 binary + 1 unary, structurally distinct from the
band-3 / R9 target shape.  Band 0.

### R10 Iteration depth — **0** (cycle-11: 3; **−3**)

B did NOT use `/refine` this cycle.  `task/iterations/` and
`task/sim/` contain only cycle-11 leftovers (mtimes Apr 23).  No
`cycle-12/B-eval-*.json`, no `cycle-12/B-iter-*.md`, no
`cycle-12/B-sim-*` artefacts.  B authored both `ARGUMENT.md` and
`outcome.json` in a single shot.  Single-shot from filesystem-
evidence perspective.  Band 0.

This is a **−3 vs cycle-11 B**.  B's autonomy at work — B chose
direct authorship over iterated `/refine` for this cycle.  The
content quality (cardinality 2 vs cycle-11's 4) is real evidence of
deeper reasoning, but the rubric R10 axis measures iteration TRACE
on disk, not content quality.  This is one of the axes where the
rubric framework and the underlying reasoning quality diverge — see
§6 below.

### B total: 2 + 3 + 2 + 2 + 1 + 2 + 3 + 3 + 0 + 0 = **18 / 30**

---

## §4. Δ analysis (rubric)

```
A total = 20
B total = 18
Δ (B − A, rubric) = −2
```

Per-axis breakdown:

| Axis | A | B | Δ (B−A) | Notes |
|------|---|---|---------|-------|
| R1 | 3 | 2 | **−1** | A names field-generation precedent + M10.2 (b) obstruction; B uses internal collapse mechanisms only, no cross-domain precedent |
| R2 | 3 | 3 | 0 | Both meet M10.3 per-sublemma proof locality |
| R3 | 3 | 2 | **−1** | A has deliverable-side tables per stage (cycle-9 locus met); B has prose-per-stage |
| R4 | 2 | 2 | 0 | Both reach ≤ 2 binary; A=5 elements (binary+constant shape), B=2 elements (binary+unary shape, structurally distinct from band-3 spec) |
| R5 | 1 | 1 | 0 | Both compose exp/ln correctly; neither proposes single binary operator |
| R6 | 2 | 2 | 0 | Both disclose gaps; B regressed from cycle-11's R6=3 (no executable oracle this cycle) |
| R7 | 3 | 3 | 0 | A via ≥4 examples; B via ≥3 orthogonal modes |
| R8 | 3 | 3 | 0 | Both have dedicated open-question section with parametric/structural disclosure |
| R9 | 0 | 0 | 0 | Neither reaches paper's single-binary + single-constant answer |
| R10 | 0 | 0 | 0 | A single-shot byte-identical no-op; B single-shot fresh content (no `/refine` trace this cycle) |
| **Total** | 20 | 18 | **−2** | — |

**A-over-B axes:** R1 (−1), R3 (−1).
**B-over-A axes:** none.
**Net delta:** A wins by +2 on rubric.  **Direction reversal vs
Cycle #11** (where B led by +2).  Driving factors:
- B's R6 dropped 3→2 (no executable oracle this cycle).
- B's R10 dropped 3→0 (no `/refine` trace this cycle).
- A's all 10 axes unchanged (byte-identical deliverable).

### §4.1 Cycle #10 → #11 → #12 A/B Δ shift

| Cycle | A | B | Δ (B−A) |
|-------|---|---|---------|
| #10 | 20 | 21 | +1 |
| #11 | 20 | 22 | +2 |
| #12 | 20 | 18 | **−2** |

What changed in cycle-12: A unchanged (3rd byte-identical no-op).
B replaced cycle-11's R6=3 + R10=3 (oracle + iteration trace) with
fresh content that pushed cardinality 4→2 but did so single-shot
without /refine and without executable oracle.  Net rubric Δ swung
from +2 to −2 (a 4-point swing on a 30-point scale).

**Interpretation.**  Within the rubric framework, B's cycle-12 work
appears worse than cycle-11 B's by 4 points.  Within the underlying
content, B's cycle-12 answer is structurally closer to the paper's
cardinality target (2 vs 4).  This divergence between rubric scoring
and content quality is precisely the H1/H0 question Cycle #12 was
designed to surface — see §6.

---

## §5a. Disclosed-circularity scan results summary

A: scan found no paragraph-level internal tensions; one disclosed
gap in §7(2) (×-impossibility under strict totality not fully
proven).  R6 polarity → band 2.

B: scan found no paragraph-level internal tensions; four disclosed
gaps in §7 (branch cuts, `log_x(x)` domain, real-only domain,
non-subset cardinality lower bound).  R6 polarity → band 2.

(Detailed scan in §5a above.)

---

## §5b. B → ROOT port analysis (post-scoring)

Per CLAUDE.md §6.7 step 5b, one entry per distinct refinement
artefact B produced this cycle (a `/refine` diff, a new documentation
pattern, a scorer signal, an internal evaluator finding).

### Cycle #12 finding: B produced ZERO new B-side refinement artefacts

B did not exercise `/refine` this cycle (per §0.2 + §3 R10).  No new
B-internal evaluator findings, no new scorer signals from B, no new
B-authored procedures.  B authored a fresh ARGUMENT.md + outcome.json
single-shot, then exited.

**Decision:** no B-side refinement artefact to port to ROOT this
cycle.  This is a **valid empty B → ROOT port row** — the §5b gate
requires "one entry per distinct refinement artefact B produced",
and the count this cycle is zero.

### Cycle #12 indirect signal: rubric-vs-content divergence

While not a B-authored artefact, Cycle #12's empirical result —
B's rubric score dropped 4 points while B's basis cardinality
dropped from 4 to 2 — is a **scorer signal originating from the
cycle architecture itself** (the introduction of the parallel
outcome dimension forced this measurement).  The signal is:

> The current rubric R1–R10 framework awards B for `/refine`
> iteration architecture (R10) and executable oracles (R6 band-3
> path), but does not award B for reaching a strictly smaller
> cardinality basis when the basis structure differs from the
> band-3-specified shape (R4 axis caps at band 2 for `1 binary +
> 1 unary` even when total cardinality matches the target).

This is a **rubric-coverage finding**, not a B-authored finding.
Decision: **deferred** to a post-cycle ROOT improvement iteration
(see §7 below).  Not actioned in this cycle's commits — the H1/H0
verdict is the headline finding; rubric-coverage refinement is a
follow-on if L0/L1 chooses to extend the WIP beyond Cycle #12.

---

## §6. Outcome verification (parallel measurement dimension)

Per `outcome-verification-axis-v1.md`, reported parallel to R1–R10,
NOT included in the 30-point rubric total.

### §6.1 Per-agent outcome ratios

| Agent | Total rubric | Outcome ratio | Pass / Fail / Missing | Detail |
|-------|--------------|---------------|------------------------|--------|
| A | 20/30 | 0.429 | 3 / 4 / 0 | `cycle-12/outcome-report-A.json` |
| B | 18/30 | 0.571 | 4 / 3 / 0 | `cycle-12/outcome-report-B.json` |

### §6.2 Per-question detail (anchor + discriminative breakdown)

| Q | Class | Expected | A answer | A | B answer | B |
|---|-------|----------|----------|---|----------|---|
| Q1 | discriminative (binary count) | `1` | `2` | FAIL | `1` | **PASS** |
| Q2 | discriminative (unary count) | `0` | `2` | FAIL | `1` | FAIL |
| Q3 | anchor (constant required?) | `yes` | `yes` | PASS | `no` | FAIL |
| Q4 | discriminative (total cardinality) | `2` | `5` | FAIL | `2` | **PASS** |
| Q5 | discriminative (textbook 3 minimal?) | `no` | `no` | PASS | `no` | PASS |
| Q6 | anchor (exp expressible?) | `yes` | `yes` | PASS | `yes` | PASS |
| Q7 | discriminative (exp/ln top-level?) | `no` | `yes` | FAIL | `yes` | FAIL |

### §6.3 Δ(rubric) vs Δ(outcome) reading

```
Δ(rubric, B − A)  = −2     (B behind on rubric structure)
Δ(outcome, B − A) = +0.143 (B ahead on outcome correctness)
                  = +1 PASS / 7 questions
```

**Direction:** OPPOSITE.  Rubric and outcome point in opposite
directions for Cycle #12's A vs B comparison.

### §6.4 Anchor question scrutiny

| Anchor | A | B | Note |
|--------|---|---|------|
| Q3 (constant required?) | PASS | FAIL | Anchor question — basic insight any reasonable derivation should arrive at.  A passed by including `−1` as constant; B FAILED by deriving the constant from `log_x(x)` (B's framework treats this as "no explicit constant required") |
| Q6 (exp in closure?) | PASS | PASS | Both pass; necessary for any complete basis |

B's Q3 FAIL is **NOT a catastrophic deliverable issue**.  B's answer
is internally consistent with B's framework (where the constant 1 is
derived as `log_x(x)`, so no "explicit constant in addition to
input variables" is required).  B's framework treats variable-input
realizations of constants as not requiring an explicit constant
seed.  The ground-truth answer ("yes") reflects the paper's
framework where constant 1 IS an explicit basis primitive.  This is
a **framework-disagreement FAIL**, not a content-error FAIL — B's
reasoning is coherent within B's framework; it just doesn't match
the paper's framework.

This nuance is captured by the `outcome-verifier.py` mechanism but
not surfaced in the bare ratio.  See §6.6 below.

### §6.5 Discriminative question reading

B passed Q1 (binary=1) and Q4 (total=2) — the two questions that
specifically discriminate "agent reached cardinality 2" from
"agent stuck at textbook 3+ or higher".  B reached the lower bound.
A failed Q1 (binary=2) and Q4 (total=5) — A is firmly in the
textbook-cardinality regime (or above).

B's discriminative-axis advantage is real and matches the structural
reading of B's ARGUMENT.md (cardinality 4 → 2 leap).

B failed Q2 (unary=1 instead of 0) and Q7 (exp/ln top-level: yes
instead of no) — these are **structural-route disagreements**, not
content errors.  B's basis has `exp` as a top-level primitive
(unary count = 1, exp top-level = yes); the paper's basis has `eml`
as a single binary that internalizes both `exp` and `ln`, so unary
count = 0 and exp/ln top-level = no.  Both routes reach cardinality
2; they make different structural choices about what to expose at
top level.

### §6.6 Framework-disagreement vs content-error: a verifier limitation

The outcome verifier mechanically compares agent answer to
ground-truth answer per `match_mode`.  It cannot distinguish:
- **content-error FAIL**: agent's framework matches GT framework,
  but agent reasoned to wrong answer.
- **framework-disagreement FAIL**: agent's framework differs from
  GT framework, and agent reasoned correctly within its own
  framework to an answer that differs from GT.

B's Q2/Q3/Q7 FAILs are all **framework-disagreement** type:
- Q2 (unary=1 vs 0): B's basis has `exp` top-level; paper's basis
  has 0 top-level unary because `eml` internalizes everything.
- Q3 (no vs yes): B derives constant 1 from `log_x(x)`; paper has
  constant 1 as basis primitive.
- Q7 (yes vs no): B has `exp` top-level; paper has no top-level
  unary at all.

A's Q1/Q2/Q4/Q7 FAILs are mixed:
- Q1 (2 vs 1): A's basis has 2 binary operators; paper has 1.
  Could be framework-disagreement (A's strict-totality reading
  forces 2 binary) or content-error (A did not consider
  alternative 1-binary route).  A's §7(2) self-disclosure
  ("we have not proved [×-impossibility from {+, exp, ln, c}]")
  suggests A is aware its lower bound is conditional → leans
  framework-disagreement.
- Q4 (5 vs 2): A's strict-totality basis is 5 elements; paper's
  is 2.  Same as Q1 — A's strict-totality framing is the gap.
- Q7 (yes vs no): A's basis has both exp and ln top-level.
  Framework-disagreement (A includes them; paper doesn't).

**Implication:** the bare outcome ratio under-counts B's
"framework-coherent but framework-different" answers as content
errors.  A more sophisticated outcome scoring would distinguish
these classes.  This is a **v1 verifier limitation** captured by
`outcome-verification-axis-v1.md` §"Limitations" item 1
("lucky-correctness vs reasoned-correctness").

For the H1/H0 reading, we report the bare ratio as primary evidence
and note framework-disagreement as a contextual qualifier.

### §6.7 H1 / H0 reading for Cycle #12

**H1**: B's rubric-Δ advantage corresponds to outcome-Δ in same
direction and magnitude.

**H0**: outcome-Δ is 0 or anti-correlated with rubric-Δ.

**Cycle #12 evidence:**

```
Δ(rubric, B − A) = −2     (B behind by 2 points on 30-point scale)
Δ(outcome, B − A) = +1/7  (B ahead by 1 PASS on 7-question battery)
                  = +0.143 in ratio terms
```

The two Δ values point in **opposite directions**.  Within Cycle
#12, the rubric framework rates A higher; the outcome framework
rates B higher.

**Interpretation:** H1 is **NOT supported** by Cycle #12 evidence.
H0 is **supported** by Cycle #12 evidence — the rubric's positive-
direction prediction (cycle-11 +2 should map to outcome-positive)
not only fails in magnitude but also flips sign on rubric while
outcome shows B ahead by a small but positive margin.

**Magnitude interpretation:**
- Rubric Δ = −2/30 = −0.067 normalized.
- Outcome Δ = +1/7 = +0.143 normalized.
- |Outcome Δ| > |Rubric Δ| (in normalized ratio terms), but
  opposite sign.

**Caveats acknowledged:**
1. **n = 1 cycle.**  Single-cycle outcome data; no longitudinal
   replication.  Could be high-variance noise rather than systematic
   H0 confirmation.
2. **Framework-disagreement masking** (§6.6).  3 of B's 4 FAILs are
   framework-disagreement, not content-error.  If we re-classified
   those as PASS-with-caveat, B's outcome ratio would rise from
   4/7 = 0.571 toward 7/7 = 1.0 (extreme).  Even partial reclass
   would amplify Δ(outcome) further in B's favor.
3. **A's framework-disagreement count:** 4 FAILs are mixed; A's
   §7(2) suggests at least Q1/Q4 are framework-disagreement.
   Reclass would lift A toward the 0.6-0.7 range.  Net Δ direction
   unchanged but magnitude reduces.
4. **Rubric R10 + R6 vulnerability.**  B's rubric score dropped 4
   points relative to cycle-11 specifically because B did not
   exercise `/refine` (R10) and did not produce executable oracle
   (R6).  These axes reward iteration ARCHITECTURE, not content
   QUALITY.  An architecture-rewarding rubric will score a
   single-shot quality leap below an iterated quality plateau.

**WIP closure:** the parent WIP `task-20260427-q5-outcome-grounded`
selected alternative (I) Outcome-based measurement to test whether
rubric-Δ and outcome-Δ correspond.  Cycle #12 evidence: they do
not correspond in direction within this cycle.  The WIP closes on
this **H0-favorable verdict** for the single-cycle outcome
hypothesis test.  Either result was acceptable per the WIP charter;
the empirical finding is H0.

### §6.8 Schema validity + ground-truth integrity

- `cycle-12/A-outcome.json` schema: `outcome-v1`, task_id `cycle-12`,
  7 questions Q1-Q7 present.  Schema-valid.
- `cycle-12/B-outcome.json` schema: `outcome-v1`, task_id `cycle-12`,
  7 questions Q1-Q7 present.  Schema-valid.
- `cycle-12/outcome-ground-truth.json` schema: `ground-truth-v1`,
  task_id `cycle-12`, 7 questions Q1-Q7, source authority chain
  recorded.  Schema-valid.
- `cycle-12/outcome-report-A.json`: schema `outcome-report-v1`,
  pass=3, fail=4, missing=0, ratio=0.429.  Numbers match this §6.
- `cycle-12/outcome-report-B.json`: schema `outcome-report-v1`,
  pass=4, fail=3, missing=0, ratio=0.571.  Numbers match this §6.

**Integrity verified.**

---

## §7. Defect resolution table (for §8a partial-defect audit)

This cycle's defect-resolution status table.  All entries are
**closed** in this cycle's commits or **not applicable** (no defect
of this kind surfaced).

| ID | Description | Status |
|----|-------------|--------|
| C12-D1 | Cycle #12 outcome-dimension introduction (parallel measurement) | Closed (cycle-12-pre commit + this JUDGMENT §6) |
| C12-D2 | Outcome ground-truth port to L2-only path (paper-isolated) | Closed (cycle-12-pre commit) |
| C12-D3 | Outcome verifier executable + schema-validated | Closed (cycle-12-pre commit, sanity-tested 7/7 PASS on synthetic input) |
| C12-D4 | A/B outcome.json sidecar deliverable produced this cycle | Closed (both A and B produced schema-valid outcome.json) |
| C12-D5 | Paper-leak audit on A and B (12th consecutive cycle) | Closed (both PASS) |
| C12-D6 | H1/H0 verdict produced regardless of magnitude (per WIP charter) | Closed (§6.7 verdict: H0-favorable) |

**Carry-over candidates (NOT defects this cycle, flagged for
post-WIP iteration if L0/L1 extends):**

- **C12-CO1: Rubric-coverage gap on cardinality vs structural-shape.**
  R4 axis caps at band 2 when basis is `1 binary + 1 unary` (B's
  cycle-12 route) even though total cardinality (2) matches the
  band-3 target.  Either rubric R4 needs a "structural-equivalent
  variation" elaboration OR rubric needs a separate "cardinality
  axis" parallel to R4's "shape axis".
- **C12-CO2: Outcome-verifier framework-disagreement-vs-content-error
  distinction.**  The bare outcome ratio under-counts framework-
  coherent-but-framework-different answers as content errors (§6.6).
  Future v2 verifier could reflect this.
- **C12-CO3: R10 single-shot-quality-leap reward gap.**  R10 measures
  iteration TRACE on disk.  A single-shot quality leap (cycle-12 B:
  cardinality 4 → 2 in one shot) earns R10=0 even though it
  represents deeper reasoning than an iterated plateau.  Either R10
  needs an alternative path for single-shot leaps OR a separate
  "content-leap axis" parallel to R10's "iteration axis".

Carry-overs are NOT defects in Cycle #12; they are observations
surfaced by Cycle #12's empirical result and are appropriate
material for any future WIP that builds on this one.  Per §8a, no
"Partial" rows in this cycle's defect table.

(The "Partial-capped" verdict text from cycle-11 falsification-
report-v2.md is a **verdict-class label**, not a defect-resolution
status — it does not appear in any defect-resolution table in
Cycle #12.)

---

## §8. Audit concurrence (post-proof-auditor section)

Per CLAUDE.md §6.7 step 5c, an independent `proof-auditor` audit
ran on the cycle-12 deliverables + this JUDGMENT.md draft +
`docs/research/eml-paper/judgment-rubric.md` (Cycle #11 state) +
the oracle catalogue (`outcome-verifier.py` already-executed
reports as authoritative; `combinator-reducer.py` not applicable
to continuous-elementary-functions domain; `paper-analysis.md` as
EML-domain ground truth).

### §8.1 Auditor totals

| Agent | Incumbent | Auditor | Δ |
|-------|-----------|---------|---|
| A | 20/30 | 20/30 | 0 |
| B | 18/30 | 18/30 | 0 |

Both totals match byte-for-byte.

### §8.2 Agreement matrix summary

- **A: 10/10 YES** (zero disagreements, zero conditionals).
- **B: 9/10 YES + 1 CONDITIONAL on R4** (zero disagreements).

Total: **19 YES + 1 CONDITIONAL + 0 NO** across A + B.

### §8.3 Arbitration trigger checks (CLAUDE.md §6.7 step 5c)

| Trigger | Threshold | Cycle #12 result |
|---------|-----------|------------------|
| ≥1 axis with \|incumbent − auditor\| ≥ 2 | one axis | none |
| ≥3 axes with any band difference | three axes | 0 axes have any difference |
| Any binary axis (R9) disagreement | R9 mismatch | A R9=0, B R9=0 — concur |
| Total score difference > 20% rubric max (>6 pts) | >6 pts | A diff = 0, B diff = 0 |

→ `arbitration_triggered: false`.  JUDGMENT proceeds with
`status: draft` per CLAUDE.md §6.7 step 5c.

### §8.4 The single CONDITIONAL (B-R4)

Auditor concurred with the incumbent's B-R4 = 2 score under the
**strict reading** of the band-3 specification ("exactly one
binary + one constant or equivalent variation"), where "equivalent
variation" admits other choices of the *terminal constant* (`−1`
vs `i` vs another non-positive seed) but does NOT admit replacing
the constant with a unary primitive.

Under a **generous reading** where "equivalent variation"
admits any 2-element basis at the same cardinality regardless of
the binary/unary/constant decomposition, B-R4 could lift to band 3.

The auditor flags this as a **rubric-semantic dependency**, not
an arbitration trigger.  The locus is exactly the same as
JUDGMENT §7 carry-over **C12-CO1** (Rubric-coverage gap on
cardinality vs structural-shape).  The CONDITIONAL is consistent
with the §6 H0-favorable outcome verdict — the rubric R4 axis
cannot distinguish B's cardinality-equivalent alternative shape
from the band-3-specified shape, which is one of the structural
reasons rubric-Δ and outcome-Δ point in opposite directions in
this cycle.

### §8.5 Outcome dimension auditor verification (mandatory)

Per `outcome-verification-axis-v1.md` §"Auditor coverage", the
auditor verified:

- **(i) outcome.json schema validity:** A-outcome.json and
  B-outcome.json both have `schema_version: "outcome-v1"`,
  `task_id: "cycle-12"`, 7 questions Q1-Q7 present.  **VALID.**
- **(ii) ground-truth.json integrity:** `schema_version:
  "ground-truth-v1"`, `task_id: "cycle-12"`, 7 questions, source
  authority chain recorded (Odrzywolek 2026-03 arXiv:2603.21852).
  No tampering indicators.  **INTACT.**
- **(iii) JUDGMENT §6 numbers cross-check:** §6.1 ratios
  (A=0.429, B=0.571) match `outcome-report-A.json` (0.4286) and
  `outcome-report-B.json` (0.5714).  §6.2 per-question PASS/FAIL
  labels match every cell of both verifier reports.  **ALL MATCH.**

### §8.6 Auditor shared-bias disclosure

Per the auditor's own self-bias disclosure, strongest auditor-
confidence axes are R10 (filesystem oracle: sha256 + ls) and the
outcome dimension (mechanical verifier).  Weakest auditor-
confidence axes are R1 (M10.2 (b) "obstruction-sketch" judgment
for A; "no cross-domain precedent" judgment for B), R3 (prose-
vs-tabular discrimination for B is interpretive), R4 (the
CONDITIONAL above).

Audit JSON: `cycle-12/rubric-audit.json`.  Per-axis evidence,
oracle outputs, and per-axis agreement records are inside that
file.

---

## §9. Cycle close summary

- **Rubric verdict:** A 20 vs B 18, Δ = **−2** (A ahead on rubric).
- **Outcome verdict:** A 3/7 vs B 4/7, Δ = **+0.143** ratio
  (B ahead on outcome).
- **Direction agreement:** **opposite** (rubric and outcome
  disagree on the within-cycle A/B comparison).
- **H1/H0:** **H0-favorable** for this single-cycle test.
- **Paper-leak audit:** both PASS — **12th consecutive cycle**
  with zero paper-identifier hits.
- **A no-op streak:** 3 consecutive cycles (Cycles #10, #11, #12)
  byte-identical A-ARGUMENT.md.
- **B autonomy variation:** B exercised single-shot direct
  authorship this cycle (no `/refine`); content quality leapt
  cardinality 4 → 2 but rubric R6 + R10 dropped 4 points.
- **Parent WIP:** `task-20260427-q5-outcome-grounded` closes on
  H0-favorable verdict.  Empirical evidence: rubric-Δ and outcome-Δ
  point in opposite directions within Cycle #12 (n = 1).
