---
status: draft
cycle: 11
deliverable: cycle-10/X-ARGUMENT.md (unchanged from Cycle #10)
deliverable_path: docs/research/eml-paper/cycle-10/X-ARGUMENT.md
role: rubric-falsification-probe (re-scored under v2 rubric)
authorial_identity: L1
scoring_protocol: rubric-strict (procedures/falsification-retest-v1.md)
rubric_version: cycle-11 (== cycle-10 + M10.2 R1 motivation-answer consistency + M10.3 R2 per-sublemma proof locality)
consulted_X_fabrications_md_pre_scoring: false
incumbent_total_X_v2: 9
auditor_total_X_v2: 9
auditor: proof-auditor
auditor_date: 2026-04-23
arbitration_triggered: false
agreement: 10_YES_0_CONDITIONAL_0_NO
audit_file: cycle-11/rubric-audit.json
v1_reference: cycle-10/X-JUDGMENT.md
v1_total: 11
v2_total: 9
delta: -2
---

# Cycle 11 — X-JUDGMENT-v2

Rubric-strict re-scoring of `docs/research/eml-paper/cycle-10/X-ARGUMENT.md`
(unchanged; same bytes as at cycle-10 close) under the **Cycle #11
rubric state**: Cycle #10 rubric + M10.2 R1 motivation-answer
consistency addendum + M10.3 R2 per-sublemma proof locality
addendum.

Scoring discipline per
`docs/research/eml-paper/procedures/falsification-retest-v1.md`:

1. Walk each rubric axis R1–R10 and apply the band criteria *as
   written under v2*, including every non-inflation clause and
   §5a disclosed-circularity scan.
2. Do not adjust non-R1/R2 axes downward "because the rubric
   improved" — non-R1/R2 rubric text did not change at Cycle #11.
3. Do not consult `X-fabrications.md` during this pass.  (Post-
   judgment reconciliation only, in
   `falsification-report-v2.md` § post-judgment.)
4. Explicitly flag per axis what changed from Cycle #10 v1 and why.

Front-matter `status` will transition per CLAUDE.md §6.7 step 5c
after the proof-auditor pass.

---

## §1. Per-axis re-scoring walk

### R1 Motivation — **2** (v1: 3; Δ = −1)

**v2 rubric text (band 3 + tightening):**

> Base band 3: "Clear structural precedent — Boolean universality
> via a single two-input gate, or an equivalent named example
> (combinators, one-instruction computers, Wolfram's single axiom),
> argued from first principles."
>
> **Band-3 tightening (Cycle #11 port).** When the motivation section
> invokes a named structural precedent for single-primitive or
> single-generator reduction — Boolean universality via NAND /
> Peirce's arrow, combinators (S and K), one-instruction computers
> (OISC / SUBLEQ), Wolfram's single axiom, interaction combinators,
> aperiodic monotile, Rule 110 / FRACTRAN, or a functionally
> equivalent single-generator / minimal-generator analog — band 3
> additionally requires the deliverable's final answer to satisfy
> one of:
>
> (a) Shape match — the final basis has the same cardinality shape
>     as the precedent. ...
> (b) Explicit departure justification — the motivation section
>     itself names the specific obstruction that blocks reaching the
>     precedent's shape, with at least a sketch argument. ...
>
> Named-precedent citation without (a) or (b) maxes at band 2.

**Evidence from X (unchanged content):**

- §1 names five structural precedents of single-primitive /
  single-generator reduction type:
  - "Boolean universality: the full Boolean lattice, specified by
    ∧, ∨, ¬ and potentially dozens of named connectives, reduces
    to the single two-input NAND gate" — single-primitive precedent.
  - "combinatory logic (S and K combinators generate the entire
    λ-calculus)" — named minimal-generator precedent.
  - "field theory (transcendence bases plus algebraic generators)"
    — named minimal-generator analog.
  - "group theory (rank of generators)" — named minimal-generator
    analog.
  - (implicit) Euler's formula as §1(a) — single complex-analysis
    reduction fact.
- §1 closes with: "What makes the calculator special is that almost
  all of its transcendental richness flows from a single complex
  function (exp) and its inverse (ln).  The reduction pressure is
  therefore on the transcendental side, with the arithmetic side
  fixed to a single binary operation."

**Tightening application (per v2):**

- **Trigger.** X cites NAND / Sheffer (single-primitive precedent),
  S/K (minimal-generator), transcendence bases (minimal-generator),
  group rank (minimal-generator).  The tightening's trigger
  condition — "the motivation section invokes a named structural
  precedent for single-primitive or single-generator reduction" —
  holds.
- **(a) Shape match check.** X's final basis (§4): 2 unary + 1 binary
  + 1 terminal constant = 3 function primitives + 1 constant.
  Precedents cited: NAND (1 primitive), S/K (2 primitives), field
  minimal backbone (2 ops + 1 constant).  X's answer shape has
  ≥ 3 function primitives — not a single-primitive shape (vs NAND)
  and not a two-primitive shape (vs S/K or field backbone) either.
  **(a) fails.**
- **(b) Explicit departure justification check.** X's §1 closes by
  *observing* that "the reduction pressure is on the transcendental
  side, with the arithmetic side fixed to a single binary operation"
  — but this is a framing remark, not an argument that reaching the
  precedent's single-primitive shape is obstructed.  No specific
  obstruction (e.g., "unlike Boolean, the continuous domain cannot
  collapse forward and inverse transcendentals into a single primitive
  because Y") appears in §1.  §8 Limitation 2 later asserts a
  rank-deficiency impossibility at the 2-primitive boundary, but that
  disclosure is (i) in §8, not the motivation section, and (ii)
  itself oracle-false per §1 R8/R9 analysis below.  Even charitably
  treating §8 as satisfying "(b) motivation section itself names the
  obstruction" — the rubric text requires "motivation section";
  strict reading excludes §8.  **(b) fails.**
- **Cap:** Named-precedent citation without (a) or (b) → band 2 cap.

**Non-inflation & non-penalization re-check:**

- Cycle #10 X cited precedents that match single-primitive / minimal-
  generator templates — the tightening trigger is squarely on-target
  (not a false positive on an "internal motivation" case).
- X's writing quality is high; the analogical argument from §1(a)–
  (c) is coherent.  Under pre-tightening rubric text, this earned
  band 3.  Under v2, the tightening caps at band 2 because the
  motivation-answer consistency obligation is not met.

**Verdict: R1 v2 = 2.**  Δ from v1: **−1** (3 → 2).  **Shift type:
partial** (per procedure verdict rule: band 2 in v2, v1 was band 3;
not ≤ 1, so not "reasoning"; not unchanged, so not "no shift";
matches "partial shift" — the tightening lowered the cap by one
band without closing to reasoning).

### R2 Method design — **2** (v1: 3; Δ = −1)

**v2 rubric text (band 3 + tightenings):**

> Base band 3: "Explicit procedure with verification ..."
>
> Cycle #7 tightening: "When the deliverable uses distinct proof
> tools, band 3 additionally requires that each tool be isolated as
> a named sublemma stated and discharged separately from the main
> argument. ... Scope declared."
>
> **Cycle #11 locus clarification.** Band 3 requires per-sublemma
> statement-and-proof locality:
> (a) Statement locality — each declared sublemma has its own
>     statement block.
> (b) Proof locality — each declared sublemma has its own proof
>     block immediately following its statement (same subsection
>     OR adjacent subsection), presenting the argument *for that
>     sublemma specifically*, not a multi-sublemma combined
>     argument.
> (c) Non-distributed discharge — the deliverable may additionally
>     reference sublemmas from a downstream reduction table or
>     summary proof, but the table alone cannot substitute for
>     per-sublemma proof blocks.
>
> Declarations with (a) but without (b) — named sublemmas without
> per-sublemma proofs, discharged only via a downstream reduction
> table or collapsed into a multi-sublemma argument — max at
> band 2 regardless of whether the table appears to "use" the
> sublemmas.

**Evidence from X (unchanged content):**

- §2.1 explicit scope declaration — unchanged (still meets scope
  clause).
- §2.2 three **named sublemmas** declared, each in its own labeled
  list item:
  - "Sublemma 1 (Transcendental collapse)."
  - "Sublemma 2 (Arithmetic conjugation)."
  - "Sublemma 3 (Constant collapse)."
  Each has a one-sentence statement beside its name.  **(a)
  Statement locality — met** (each sublemma has its own statement
  in the §2.2 list).
- §2.2 continues with: "The method reaches the minimum `{exp, ln, +}`
  (plus constant 1) through the cascade Sublemma 1 → Sublemma 2 →
  Sublemma 3.  Each sublemma's proof is isolated, stated-and-
  discharged separately, and independently verifiable."
- **X's own claim vs on-page content.** X claims sublemmas are
  "stated-and-discharged separately"; on-page, no §2.2.1/§2.2.2/
  §2.2.3 proof blocks exist.  §2.3 is the numerical-witness sieve
  (a verification step, not a per-sublemma proof block).  §3 is the
  progressive reduction table.  §7 contains worked examples, not
  sublemma proofs.  **No per-sublemma proof block exists in X.**
- §3's reduction table (A→B→C→D→E→F) distributively "uses" the
  sublemmas — the table rows cite Sublemma 2 (Arithmetic
  conjugation) in the E→F justification and implicitly Sublemma 1
  in the B→C justification, but this is downstream reduction-table
  usage, not per-sublemma proof.  Per v2 locus clarification (c):
  "the table alone cannot substitute for per-sublemma proof
  blocks."
- **(b) Proof locality — NOT met.**  §2.2 declares the sublemmas;
  no adjacent subsection (§2.2.1, §2.2.2, §2.2.3, §2.3-as-proofs)
  contains per-sublemma proof blocks.  Discharge is distributed
  via §3's reduction table.

**Tightening application (per v2):**

- **Trigger.** X declares named sublemmas (§2.2).  The Cycle #7
  tightening precondition ("distinct proof tools") arguably
  triggers (Sublemma 1 uses transcendental-identity machinery,
  Sublemma 2 uses exp/ln-conjugation machinery, Sublemma 3 uses
  constant-derivation machinery — three different tools), but
  regardless of whether Cycle #7 triggers, the Cycle #11 locus
  clause's trigger — "the deliverable's method declares named
  sublemmas" — holds.
- **Locus check:** (a) met, (b) not met, (c) X's discharge path is
  via §3 table (distributed).
- **Cap:** Named sublemmas without per-sublemma proofs → band 2
  cap.

**Non-inflation & non-penalization re-check:**

- X's writing quality on §2.2 is good — named sublemmas with clear
  statements.  The Cycle #10 grader read "stated-and-discharged
  separately" as met under Reading B (lenient): sublemmas
  declared, discharged via downstream table.  Under v2 Reading A
  (strict), this pattern caps at band 2.
- Standard lemma-proof-theorem methods (statement per sublemma +
  proof per sublemma + downstream reduction table citing proofs)
  are unaffected — the tightening's non-inflation clause makes
  this explicit.  X does not follow that pattern; A and B in
  Cycle #10 (per JUDGMENT.md) do.

**Verdict: R2 v2 = 2.**  Δ from v1: **−1** (3 → 2).  **Shift type:
partial** (per procedure verdict rule: band 2 in v2, v1 was 3;
matches "partial shift").

### R3 Progressive minimization — **0** (v1: 0; Δ = 0)

**v2 rubric text:** unchanged from v1 (no Cycle #11 ports touch R3).

**Evidence from X:** unchanged.  v1 scored R3 = 0 via the
non-inflation clause ("deliverable-side table with fabricated or
oracle-unverifiable rows earns band 0").  Row E→F's justification
uses operators outside basis F (`×`, `/`, `arg`, `(−1)`, `i`, `π`)
— false enumeration.

**Verdict: R3 v2 = 0.**  Δ from v1: **0**.  **Shift type: no
shift (control)** — non-R1/R2 axis whose rubric text did not
change; v2 band matches v1 band as expected.

### R4 Final basis structure — **2** (v1: 2; Δ = 0)

**v2 rubric text:** unchanged from v1.

**Evidence from X:** unchanged.  X §4: 2 unary + 1 binary + 1
constant = "≤ 2 binary operators" band-2 fit.

**Verdict: R4 v2 = 2.**  Δ from v1: **0**.  **Shift type: no
shift (control — oracle axis).**

### R5 Exact form — **1** (v1: 1; Δ = 0)

**v2 rubric text:** unchanged from v1.

**Evidence from X:** unchanged.  X's basis is three separate
primitives; does not compose into the single-binary form.

**Verdict: R5 v2 = 1.**  Δ from v1: **0**.  **Shift type: no
shift (control — oracle axis).**

### R6 Verification strategy — **1** (v1: 1; Δ = 0)

**v2 rubric text:** unchanged from v1 (R6 honesty-polarity +
§5a scan unchanged).

**Evidence from X:** unchanged.  §5a circularity scan result
(v1): Tension 2 in §7.4 π derivation is hidden circularity (not
disclosed).  R6 polarity caps at band 1.

**v2 §5a re-scan:** same paragraph-level tensions identified in
v1 still present in unchanged X.  No new tensions introduced by
v2 rubric.  Sections scanned: §1, §2.1, §2.2, §2.3, §3, §3.1, §4,
§5, §6, §6.1, §6.2, §7.1, §7.2, §7.3, §7.4, §8, §9, §10.  Tensions
re-confirmed per v1 listing.

**Verdict: R6 v2 = 1.**  Δ from v1: **0**.  **Shift type: no
shift (control — oracle axis).**

### R7 Constructive examples — **1** (v1: 1; Δ = 0)

**v2 rubric text:** unchanged from v1.

**Evidence from X:** unchanged.  3 of 4 examples use operators
outside basis F; only §7.2 is valid.

**Verdict: R7 v2 = 1.**  Δ from v1: **0**.  **Shift type: no
shift (control).**

### R8 Open questions — **0** (v1: 0; Δ = 0)

**v2 rubric text:** unchanged from v1 (R8 non-inflation + labeling
clarification unchanged).

**Evidence from X:** unchanged.  Limitation 2's "2-primitive
impossibility" claim is falsified by R9 oracle (paper establishes
single-binary-plus-constant basis); R8 non-inflation → 0.

**Verdict: R8 v2 = 0.**  Δ from v1: **0**.  **Shift type: no
shift (control).**

### R9 Exact answer match — **0** (v1: 0; Δ = 0)

**v2 rubric text:** unchanged from v1.

**Evidence from X:** unchanged.  X does not reach single-binary +
single-constant form.

**Verdict: R9 v2 = 0.**  Δ from v1: **0**.  **Shift type: no
shift (control — oracle axis).**

### R10 Iteration depth — **0** (v1: 0; Δ = 0)

**v2 rubric text:** unchanged from v1.

**Evidence from X:** unchanged.  §9 narrative claim of iterations;
no on-disk artefacts (`attempts/` directory contents referenced in
§9 do not exist on disk).

**Verdict: R10 v2 = 0.**  Δ from v1: **0**.  **Shift type: no
shift (control).**

---

## §2. X v2 total

**v2 total:** 2 + 2 + 0 + 2 + 1 + 1 + 1 + 0 + 0 + 0 = **9 / 30**

**v1 total (from cycle-10/X-JUDGMENT.md):** 11 / 30

**Δ (v1 → v2):** −2.  Attributed entirely to R1 (−1) and R2 (−1).

Non-R1/R2 axes (R3, R4, R5, R6, R7, R8, R9, R10) produce eight
control observations of zero shift, confirming v1↔v2 rubric
discipline on axes whose text did not change.

---

## §3. Per-axis shift summary

| Axis | Type | v1 band | v2 band | Δ | Shift type |
|------|------|---------|---------|---|-----------|
| R1   | shape  | 3 | 2 | −1 | **partial** (capped at 2, not closed to reasoning) |
| R2   | shape  | 3 | 2 | −1 | **partial** (capped at 2, not closed to reasoning) |
| R3   | shape  | 0 | 0 | 0  | no shift (control) |
| R4   | oracle | 2 | 2 | 0  | no shift (control) |
| R5   | oracle | 1 | 1 | 0  | no shift (control) |
| R6   | oracle | 1 | 1 | 0  | no shift (control) |
| R7   | shape  | 1 | 1 | 0  | no shift (control) |
| R8   | shape  | 0 | 0 | 0  | no shift (control) |
| R9   | oracle | 0 | 0 | 0  | no shift (control) |
| R10  | shape  | 0 | 0 | 0  | no shift (control) |

---

## §4. §5a disclosed-circularity scan (v2 pass)

Re-scan performed against unchanged X under v2 rubric — identical
§5a clause to v1.  Sections scanned: §1, §2.1, §2.2, §2.3, §3,
§3.1, §4, §5, §6, §6.1, §6.2, §7.1, §7.2, §7.3, §7.4, §8, §9,
§10.  Results: **identical to v1** — three paragraph-level
tensions re-confirmed (§3 row F vs §4 basis declaration; §7.4 π
self-reference; §7.4 −1-via-π circular chain).  All three remain
undisclosed in X.  R6 polarity mapping unchanged at band 1.

No new tensions introduced by v2 rubric.

---

## §5. Paper-leak audit

`bash scripts/meta/paper-leak-audit.sh
docs/research/eml-paper/cycle-10/X-ARGUMENT.md`

Result: same as v1 — X carries `authorial-identity: L1`
front-matter; leak audit is informational for probe (see cycle-10
X-JUDGMENT.md §4 for full discussion).  No new leak concerns at
v2.

---

## §6. Proof-auditor hand-off and concurrence

Proof-auditor audit completed 2026-04-23.  X-v2 row-set in
`cycle-11/rubric-audit.json`.

**Auditor total X-v2:** 9 / 30.  **Incumbent total X-v2:** 9 / 30.

**Agreement matrix (X-v2):** 10 YES / 0 CONDITIONAL / 0 NO.

**Auditor per-axis concurrence:**

- R1 = 2: M10.2 trigger fires (X cites 5 single-primitive /
  minimal-generator precedents — NAND/Sheffer, S/K, transcendence
  bases, group rank, Euler).  (a) shape match fails (answer is
  3 primitives + 1 constant, not single-primitive or two-primitive).
  (b) obstruction sketch fails — §1 closes with a strategy
  statement, not an obstruction argument.  Band 2 cap applies.
- R2 = 2: M10.3 locus fires — §2.2 declares three named sublemmas
  (statement locality met) but no per-sublemma proof blocks exist
  anywhere in X; discharge is distributed via §3 reduction table,
  which M10.3 (c) explicitly excludes as substitute.  Band 2 cap
  applies.
- R3, R4, R5, R6, R7, R8, R9, R10: unchanged from v1 (non-R1/R2
  rubric text did not change at Cycle #11).  Control-axis
  confirmation.

**arbitration_triggered = false.**  No axis with
|incumbent − auditor| ≥ 2; zero axes with any band difference;
R9 binary agrees; total diff 0 / 30 (below 6-point threshold).

**Status transition:** `draft` with audit concurrence section
appended.  No arbitration needed.

---

## §7. Post-judgment reconciliation (deferred)

`cycle-10/X-fabrications.md` is NOT consulted during this rubric-
strict pass.  Post-judgment reconciliation — comparing the v2
verdict against L1's pre-declared fabrication inventory — lives
in `cycle-11/falsification-report-v2.md` § post-judgment section.
