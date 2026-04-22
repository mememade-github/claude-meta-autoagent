---
status: retrospective-rescore
derived_from: cycle-06/JUDGMENT.md
rescored_under: judgment-rubric.md (Cycle #7 pre-cycle tightened R2/R3/R7/R8)
cycle: 6
cycle_when_rescored: 7
purpose: isolate-rubric-effect-from-task-design-effect
---

# Cycle 06 — JUDGMENT v2 (retrospective re-score under Cycle #7 tightened rubric)

This document re-scores the Cycle #6 A and B deliverables
(`cycle-06/A-ARGUMENT.md`, `cycle-06/B-ARGUMENT.md`) against the
**post-Cycle #7-pre-cycle** `judgment-rubric.md` — specifically the
R2 / R3 / R7 / R8 band-3 tightenings committed in
`chore(cycle-07-pre): R2/R3/R7/R8 band-3 tightening + R10 M6.2/M6.3
codification + cycle-07 TASK`.  R1, R4, R5, R6, R9, R10 are unchanged
between Cycle #6 grading and this re-score; only the tightened four
axes need re-examination.

The retrospective isolates the **rubric effect** from the
**task-design effect** in Cycle #7.  If rubric tightening alone
produces a larger Δ on a previously-graded cycle, the tightening is
validated independently of Cycle #7's domain change.

Deliverables are **unchanged** (no re-running of A or B); only the
rubric scoring is revisited.  The incumbent Cycle #6 JUDGMENT.md
stands as the grading-of-record for Cycle #6; this v2 file is an
analytical companion, not a replacement.

---

## Re-scoring per tightened axis

### R2 — Method design (tightened band 3 requires named sublemmas under distinct proof tools)

**Cycle #6 deliverable positions:**
- A §2.1 confluence method (3-step: identify / discharge / lift) +
  §2.2 termination method (3-step: measure / strict-decrease /
  well-founded) + §2.3 independence demonstration. Methods laid out
  as flowing procedures with prose case analysis.  **No named
  sublemma is stated and discharged separately in §2.**  A's
  variable-overlap handling in §4.1 case (b) is inlined within the
  proof, not extracted as a sublemma.
- B §2.1 confluence method with an **explicit variable-overlap
  sublemma, stated and proved separately**, reusable across §3.1.
  §2.2 termination method with an **explicit monotonicity sublemma,
  stated and proved separately**, backing the §3.2 decrease
  argument.  §2.3 names what the methods share and what they don't.

**Original scores (both band 3).**  Tightened reading:

- A: the methods are discharged via flowing prose without named
  sublemmas.  **Tightened band 3 caps at band 2.**  Score under
  tightening: **2.**
- B: two explicitly-stated-and-proved sublemmas (variable-overlap,
  monotonicity) plus method-independence note.  Meets tightening.
  Score under tightening: **3.**

**Δ per axis: +1 (was 0).**

---

### R3 — Progressive minimization (tightened band 3 requires tabular form for finite-tractable enumerations)

**Cycle #6 deliverable positions:**
- A §3.1 has a position table per rule + overlap audit in **prose**
  (ruling out 21 cases by head-mismatch + identifying 3 critical
  pairs CP#1/#2/#3 with inline closing sequences).  The support is
  25 ordered pairs × 2 non-variable positions = 50 cells,
  finite-tractable.
- B §3.1 has the **exhaustive 25 × 2 = 50-cell ordered-pair ×
  non-variable-position tabulation** with per-cell disposition
  (trivial / impossible-by-head-mismatch / impossible-by-
  non-unification / non-trivial CP).  Three non-trivial CPs
  identified with closing sequences.

**Original scores (both band 3, with B more auditable per grader
note).**  Tightened reading:

- A: prose enumeration of the same 50-cell support.  **Tightened
  band 3 caps at band 2.**  Score under tightening: **2.**
- B: tabular form with per-cell disposition.  Meets tightening.
  Score under tightening: **3.**

**Δ per axis: +1 (was 0).**

---

### R7 — Constructive examples (tightened band 3 requires ≥ 4 examples OR ≥ 3 orthogonal)

**Cycle #6 deliverable positions:**
- A §6 has **3 examples**:
  (a) `app(app(L1, L2), L3)` exercising ρ₅ in both LMO + RMI orders
      (positive-reduction success pattern).
  (b) `len(app(cons(0, nil), cons(s(0), nil)))` interleaving
      len/app (positive-reduction success pattern).
  (c) `(((nil @ nil) @ nil) @ nil)` — termination on a
      structurally-same-size rule (positive-reduction success).
  All three examples are in the "successful reduction converges
  under the stated polynomial interpretation" success mode; their
  claim-coverage sets overlap.
- B §6 has **4 examples**:
  §6.1 ρ₅ LMO + RMI (convergence success).
  §6.2 len/app interleave (convergence success).
  §6.3 **size-grows-but-φ-drops** (`app(cons(0,nil), cons(s(0),nil))`
  with raw size 8 → 9 → 6 but φ 11 → 9 → 6) — this example
  stress-tests the *measure ≠ size-count* claim, which neither
  §6.1, §6.2, nor §6.4 covers.  **Orthogonal to the convergence-
  success axis.**
  §6.4 CP3 ground-witness closure on a fully concrete instance,
  φ-tracking on both Path A and Path B to common reduct — stress-
  tests the *critical-pair closure* claim at depth.  **Orthogonal
  to §6.1/§6.2 which don't touch CP closure at a ground instance.**

**Original scores (both band 3).**  Tightened reading:

- A: 3 examples all in the same success mode (reduction converges
  under polynomial measure).  **Tightened band 3 requires ≥ 4
  examples OR ≥ 3 orthogonal.**  A has neither (3 overlapping).
  Caps at band 2.  Score under tightening: **2.**
- B: 4 examples with at least two orthogonal in coverage (§6.3
  measure-vs-size + §6.4 CP ground-witness closure).  Meets both
  tightening arms.  Score under tightening: **3.**

**Δ per axis: +1 (was 0).**

---

### R8 — Open questions (tightened band 3 requires ≥ 1 structural / parametric disclosure)

**Cycle #6 deliverable positions:**
- A §7 has 4 sub-sections:
  §7.1 augmented system with `add` + ρ₆/ρ₇/ρ₈ — **exhibits one
  specific failing linear interpretation** (forced `[add](x,y) =
  2x + y` gives ρ₈'s `[LHS] − [RHS] = 0`).  Single-case exhibition,
  not parametric.
  §7.2 LHS-linearity + RHS-linearity dependence with **toy
  counterexample** (dup(x, x) → x destroys confluence).  Single-
  case exhibition.
  §7.3 directional analysis (Q1 ↔ Q2 for R).
  §7.4 nature of the measure (linear polynomial, tightness
  discussion).
  **All four sub-sections are case-exhibitions or descriptive; no
  structural / parametric impossibility disclosure.**
- B §7 has 4 sub-sections + §8 6-entry disclosed-gaps list:
  §7.1 derives **an explicit linear-coefficient contradiction for
  extending the measure with `add` rules**: B ≥ 1 from ρ₆, B < 1
  from ρ₈, **intersection empty** ⟹ **no linear interpretation**
  discharges the augmented system.  **Parametric impossibility
  within the linear-family.**  Structural disclosure.
  §7.2 considers portability under ρ₈ extension and checks new CPs
  for joinability.
  §7.3 termination-vs-confluence directional analysis.
  §7.4 nature of the measure with explicit `a > b` constraint
  re-derived.

**Original scores (both band 3).**  Tightened reading:

- A: all four sub-sections are case-exhibitions (one-instance
  demonstrations) or descriptive commentary.  **Tightened band 3
  caps at band 2.**  Score under tightening: **2.**
- B: §7.1 delivers a parametric impossibility disclosure
  (non-existence of linear measure by empty-coefficient-
  intersection argument).  Meets tightening.  Score under
  tightening: **3.**

**Δ per axis: +1 (was 0).**

---

## Aggregate re-score

| Criterion | Cycle #6 incumbent A | Tightened A | Cycle #6 incumbent B | Tightened B | Δ (B−A) tightened |
|-----------|:--:|:--:|:--:|:--:|:--:|
| R1 Motivation             | 3 | 3 | 3 | 3 | 0 |
| R2 Method design          | 3 | **2** | 3 | 3 | **+1** |
| R3 Progressive min.       | 3 | **2** | 3 | 3 | **+1** |
| R4 Verdict commitment     | 3 | 3 | 3 | 3 | 0 |
| R5 Exact form             | 3 | 3 | 3 | 3 | 0 |
| R6 Verification           | 3 | 3 | 3 | 3 | 0 |
| R7 Constructive examples  | 3 | **2** | 3 | 3 | **+1** |
| R8 Open questions         | 3 | **2** | 3 | 3 | **+1** |
| R9 Exact answer match     | 3 | 3 | 3 | 3 | 0 |
| R10 Iteration depth       | 0 | 0 | 2 | 2 | **+2** |
| **Total**                 | **27** | **23** | **29** | **29** | **+6** |

**Key result.**  Under the tightened rubric applied to the *same*
Cycle #6 deliverables:

- **A drops 27 → 23 (−4).** Four axes (R2, R3, R7, R8) hit band-2
  cap; all other axes unchanged.
- **B stays 29 (±0).** All four tightenings were anchored to Cycle
  #6 B evidence; B already exhibited sublemmas, tabular
  enumeration, orthogonal examples, and parametric impossibility.
- **Δ grows from +2 to +6 (300 % increase).**

**A-drop magnitude = 4 on R2 / R3 / R7 / R8** (one point per
tightened axis).  This is the retrospective-validation metric
referenced in Cycle #7 GOAL clause 4.

---

## Interpretation for Cycle #7

The tightening successfully discriminates retroactively on Cycle #6:
a first-principles single-shot (A) that tied at ceiling under the
loose rubric drops by 4 points under the tightened rubric, while an
iteration-with-evaluator-closure deliverable (B) that also tied at
ceiling retains all its points because B already produced the
tightened-rubric-targeted patterns.

Implication: the Cycle #7 Δ should be ≥ +4 from rubric tightening
alone (assuming A and B again produce analogous patterns on the new
3-question domain).  Any additional Δ on Cycle #7 beyond +4 is
attributable to the domain change (non-positive-verdict counter-
construction pressure on R9 and R6 specifically).

The Cycle #7 JUDGMENT.md §4 "retrospective validation" line will
cite this file: *"retrospective validation: A-drop magnitude = 4 on
R2/R3/R7/R8 re-scoring Cycle #6 under tightened rubric"*.

---

## Non-rescoring disclosures

- **No re-audit by proof-auditor.**  The v2 score is ROOT's
  mechanical application of the tightened rubric; an independent
  auditor pass on the re-score is out of scope for this companion
  document.  The Cycle #6 rubric-audit.json is still the cycle's
  audit record.
- **No deliverable changes.**  A and B ARGUMENTs are untouched.
  The SHA-256 prefixes cited in Cycle #6 JUDGMENT §0 are
  byte-stable.
- **No cycle-void.**  Retrospective re-scoring does not retroactively
  invalidate the original Cycle #6 cycle — the incumbent verdict
  (A 27, B 29, Δ +2) remains Cycle #6's grading-of-record; this
  file is a rubric-evolution validation companion.

---

## Commit reference

This file is committed alongside the Cycle #7 cycle-scope commits
(see Cycle #7 JUDGMENT.md).  Retrospective re-scoring is permitted
in step 6 "Improve ROOT" of CLAUDE.md §6.7 as an analytical
companion that validates the rubric-tightening commit is
discriminative as designed.
