---
cycle: 11
test: m9.4 rubric-falsification re-test
procedure: procedures/falsification-retest-v1.md
status: locked (per-axis verdicts from X-JUDGMENT-v2.md + rubric-audit.json v2 rows; post-judgment reconciliation with cycle-10/X-fabrications.md)
v1_reference: cycle-10/falsification-report.md
v1_total_X: 11
v2_total_X: 9
v1_shape_axes_shape: 2_of_6 (R1, R2)
v2_shape_axes_shape: 0_of_6
v2_shape_axes_partial: 2_of_6 (R1, R2) — capped at band 2
v2_shape_axes_reasoning: 4_of_6 (R3, R7, R8, R10)
global_m9_4_closure_verdict: partial-capped (both R1 and R2 capped at band 2; neither closed to reasoning)
---

# Cycle 11 — Falsification Report v2 (post-rubric-tightening)

Empirical verdict on the M9.4 rubric falsification re-test, run on
the unchanged Cycle #10 probe under the **Cycle #11 rubric state**
(Cycle #10 rubric + M10.2 R1 motivation-answer consistency + M10.3
R2 per-sublemma proof locality).

Per `docs/research/eml-paper/procedures/falsification-retest-v1.md`.

**Test apparatus:**

- **Probe X:** same `cycle-10/X-ARGUMENT.md` as in Cycle #10
  falsification test.  Bytes unchanged; content identical; sha256
  unchanged.
- **Rubric v2:** Cycle #10 rubric + M10.2 addendum (R1
  motivation-answer consistency) + M10.3 addendum (R2 per-sublemma
  proof locality).  No other rubric text changed.
- **Scoring protocol:** rubric-strict (same discipline as
  `procedures/falsification-test-v1.md` §L2 scoring protocol).
  `X-fabrications.md` NOT consulted pre-scoring; post-judgment
  reconciliation permitted in §4 below.
- **Scoring output:** `cycle-11/X-JUDGMENT-v2.md`.
- **Auditor:** proof-auditor agent re-audit completed
  2026-04-23.  Output: `cycle-11/rubric-audit.json`.  Agreement
  on X-v2: 10 / 10 axes YES, arbitration_triggered = false,
  total 9 / 30 concurred.

---

## §1. Per-axis shift table (v1 → v2)

| Axis | Axis type | v1 band | v2 band | Δ | Rubric text change | Shift type | Verdict |
|------|-----------|---------|---------|---|---------------------|-----------|---------|
| R1   | shape  | 3 | 2 | −1 | M10.2 motivation-answer consistency addendum | **partial** | capped at 2; not closed to reasoning |
| R2   | shape  | 3 | 2 | −1 | M10.3 per-sublemma proof locality addendum  | **partial** | capped at 2; not closed to reasoning |
| R3   | shape  | 0 | 0 | 0  | none | no shift (control) | reasoning (unchanged from v1) |
| R4   | oracle | 2 | 2 | 0  | none | no shift (control) | control |
| R5   | oracle | 1 | 1 | 0  | none | no shift (control) | control |
| R6   | oracle | 1 | 1 | 0  | none | no shift (control) | control |
| R7   | shape  | 1 | 1 | 0  | none | no shift (control) | reasoning (unchanged from v1) |
| R8   | shape  | 0 | 0 | 0  | none | no shift (control) | reasoning (unchanged from v1) |
| R9   | oracle | 0 | 0 | 0  | none | no shift (control) | control |
| R10  | shape  | 0 | 0 | 0  | none | no shift (control) | reasoning (unchanged from v1) |

**Shape-axis verdict tallies (v2):**

- **reasoning-measuring (band ≤ 1):** 4 of 6 — R3, R7, R8, R10.
- **partial (band 2, capped by tightening):** 2 of 6 — R1, R2.
- **shape-measuring (band ≥ 3):** 0 of 6.

**v1 → v2 shape-verdict improvement:** 2 axes moved from shape
(band 3) to partial (band 2).  Zero axes moved from shape to
reasoning directly.

**Non-R1/R2 control discipline:** 8 non-R1/R2 axes (R3, R4, R5,
R6, R7, R8, R9, R10) show Δ = 0 across v1→v2, confirming the
retest applied the tightening narrowly to R1/R2 without spillover
onto axes whose text did not change.

---

## §2. Global M9.4 closure verdict

**Verdict: Partial-capped** (per `procedures/falsification-retest-
v1.md` § global verdict table, row "partial + partial").

Quoted from the procedure:

> Partial-capped — both axes cap at band 2; neither closes to
> reasoning.  Tightening discriminates against the specific fault
> pattern but does not close the shape verdict to reasoning;
> further tightening or rubric-redesign would be needed to drop
> to ≤ 1.

### What the tightening accomplished

- **R1:** The probe's "named-precedent without obstruction
  sketch" pattern — which scored band 3 under v1 — now caps at
  band 2.  The rubric now discriminates: X's §1 cites NAND / S/K /
  transcendence bases / group rank (single-primitive /
  minimal-generator precedents) but does not sketch the
  obstruction to reaching the precedent's shape, so under v2 the
  rubric no longer awards "band 3 motivation" to that shape.
- **R2:** The probe's "named sublemma without per-sublemma proof
  block" pattern — which scored band 3 under v1 — now caps at
  band 2.  The rubric now discriminates: X's §2.2 declares three
  sublemmas with statements but no per-sublemma proof blocks
  (discharge is distributed via §3 reduction table), so under v2
  the rubric no longer awards "band 3 method" to that shape.

### What the tightening did not accomplish

- Neither R1 nor R2 closed to band ≤ 1 ("reasoning-measuring").
  The rubric's tightening text lowers the cap by one band but
  does not drop the deliverable into the band-0/1 floor.
- The residual band-2 award means X is still scored "adequate"
  rather than "weak" on R1 and R2 under v2.  A rubric that wanted
  to score X as "weak" on R1/R2 would need:
  - A tightening that caps at band 1 (not band 2) when (a)/(b)
    fail — more aggressive than the current M10.2 text.
  - Or a pre-scoring scrutiny step that verifies the precedent's
    analogical pressure matches the answer shape *before* band 2
    is awarded (shifting the analysis from "named sublemma
    present" to "named sublemma's proof is correct").
  - Or an oracle layer (like R5/R6/R9 have) that can verify
    motivation-answer consistency and per-sublemma proof
    correctness mechanically.

### Implication for the WIP's Q3

- Cycle #10 answered Q3 as "Partial — 2 of 6 shape axes (R1, R2)
  award band ≥ 2 to shape-only content".
- Cycle #11 refines the answer: after the tightening,
  **0 of 6 shape axes award band ≥ 3 to shape-only content; 2 of 6
  still award band = 2 to shape-only content**.  The rubric's
  reasoning-measurement coverage increased on R1 and R2, but not
  to the "reasoning" floor.
- M9.4 empirical loop closure status: **Partial-capped** — the
  WIP closes with a documented residual: rubric-text-based
  tightening alone reduces but does not eliminate the shape-
  measuring verdict on R1 and R2.  A Q5 branch would investigate
  stronger mechanisms (oracle-backed verification, multi-
  reviewer discipline) if further closure is desired.

---

## §3. Distinction from cycle-10 A/B retrospective

`cycle-10/JUDGMENT-v2.md` (authored alongside this report) shows
that cycle-10 A and B are **unaffected** by the v2 tightening —
both retain their v1 bands on all 10 axes; Δ(B−A) stays at +1.
This confirms the tightening's **non-inflation design**:
deliverables that supply motivation-answer consistency (A §1) and
per-sublemma proof locality (A §3.6, B §4) are not penalized.
The tightening discriminates *against* the specific fault pattern
X exhibits, not against structurally-sound arguments.

The separate-measurement discipline is upheld: cycle-10 A/B
retrospective (sound deliverables, no shift) + cycle-11 X re-test
(faulty probe, R1/R2 drop by one band each).

---

## §4. Post-judgment reconciliation (X-fabrications.md)

Per the procedure, `cycle-10/X-fabrications.md` may now be
consulted after the rubric-strict pass.

X-fabrications.md declared (excerpts, summarized):

- **R1 fault target:** "named-precedent analogy vacuous for the
  specific problem class — NAND/S/K don't reduce to single-
  primitive answer here; the precedent is cited without
  obstruction explanation."
- **R2 fault target:** "sublemmas declared without per-sublemma
  proofs; discharge distributed via reduction table; rubric's
  'separate discharge' text satisfied under lenient reading
  despite shape-only compliance."
- **R4/R5/R9 fault targets:** "answer is textbook-minimum
  3-primitive basis, not paper's single-binary answer."

**Reconciliation under v2:**

- R1 and R2 targets are now explicitly addressed by the rubric
  text.  The v2 score (R1=2, R2=2) reflects the rubric's
  discrimination against these exact fault patterns.
- The residual "R1=2, R2=2" state rather than "R1≤1, R2≤1"
  indicates that L1's fault targets were construction-intent
  choices compatible with "adequate but not strong" under the
  v2 rubric; the rubric does not classify them as "weak or
  absent".
- R4/R5/R9 targets were already addressed by the oracle layer at
  cycle-10 (R4=2, R5=1, R9=0); no reconciliation gap on those
  axes.

**Empirical finding:** the v2 rubric's closure of R1/R2 shape
verdicts is *partial and asymmetric* — the tightening lowers the
awardable band on exactly the fault patterns X exhibits, but
does not collapse them to the reasoning floor.  L1's probe
design anticipated a "partial closure" outcome at seed-authoring
time (the seed seed-text predicted "band 2 cap" explicitly under
the tightening).  The empirical result matches the seed's
prediction.

---

## §5. Limitations of this re-test

1. **Same probe reuse.** The re-test reuses the Cycle #10 X
   unchanged.  The tightening's effect on *other* fault patterns
   not instantiated in this X is not measured.
2. **N=1 probe.** Single-probe generalization caveat carried
   forward from Cycle #10's `falsification-report.md` § limitations.
3. **Rubric-text-only intervention.** This re-test measures the
   rubric *text* tightening, not potential alternative mechanisms
   (oracle, multi-reviewer, pre-scoring scrutiny).  A Q5 branch
   would explore these.
4. **Authorship bias carried forward.** L1 authored X with
   knowledge of the rubric.  L1 also authored the M10.2/M10.3
   tightening seeds with knowledge of X's specific fault pattern.
   This creates a closed loop where L1 knows both the probe and
   the fix; a stronger test would use independent probe and fix
   designers.
5. **Shared-bias residual.** L2 and proof-auditor share model
   lineage.  If both share a "rubric-compliance shortcut" bias on
   the post-tightening text, the test could miss edge cases.

---

## §6. Post-cycle invariants

- Cycle #11 is the final cycle of the current WIP (Branch B
  decision 2026-04-23).  This report's verdict propagates to
  the cycle-log.md entry and to the parent WIP's closure
  narrative.
- WIP closure narrative per the verdict rule:
  > **Partial-capped** — WIP closes with documented finding that
  > rubric tightening of the type attempted (named-precedent
  > shape-match, per-sublemma proof locality) lowers the
  > max-awardable band by one but does not close to ≤1 under
  > the rubric-text-only approach.  A Q5 branch would investigate
  > stronger tightening mechanisms (oracle-backed checks,
  > multi-reviewer discipline).
- All 7 durable end-states of the WIP remain held; the empirical
  Q3 answer is additive, not substitutive.
