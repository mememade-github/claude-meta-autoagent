---
cycle: 10
test: m9.4 rubric-falsification-v1
procedure: procedures/falsification-test-v1.md
status: locked (per-axis verdicts from X-JUDGMENT.md + rubric-audit.json; post-judgment reconciliation with X-fabrications.md)
global_finding: partial
shape_verdict_count: 2_of_6
reasoning_verdict_count: 4_of_6
---

# Cycle 10 — Rubric Falsification Report

Empirical verdict on the M9.4 rubric falsification test, run on the
EML-paper domain (Cycle #10).  Per the procedure at
`docs/research/eml-paper/procedures/falsification-test-v1.md`.

**Test apparatus:**

- **Probe X:** L1-authored `X-ARGUMENT.md` constructed to exhibit
  band-3 structural features on R1/R2/R3/R7/R8/R10 while stopping
  at the pre-2026 textbook-knowledge minimum (3 primitives `{exp,
  ln, +}` + constant 1) instead of the paper's 2026-03 novel single-
  binary-operator answer (`eml(x, y) = exp(x) − ln(y)` + constant 1).
- **Scoring protocol:** L2 (ROOT) scored X rubric-strict in
  `X-JUDGMENT.md` without consulting `X-fabrications.md` pre-scoring.
- **Second reader:** proof-auditor agent independently scored X at
  `rubric-audit.json`; 30 / 30 YES agreement with L2 incumbent.
- **Global finding threshold:** per the procedure's verdict table.

---

## §1. Per-axis verdict table (rubric-strict scoring, post-auditor)

| Axis | Axis type | X band (L2 incumbent) | X band (auditor) | L1 fault-target | Verdict |
|------|-----------|-----------------------|------------------|-----------------|---------|
| R1   | shape     | 3                     | 3                | named-precedent analogy (NAND + S/K + field + group) surface-matches; answer-shape mismatch not caught | **shape** |
| R2   | shape     | 3                     | 3                | named sublemmas declared in §2.2 but not discharged as separate lemma proofs; rubric tightening text not triggered by structure-without-discharge | **shape** |
| R3   | shape     | 0                     | 0                | fabricated row E→F (uses ×, /, arg, (−1), i, π outside target basis F); non-inflation clause caught | **reasoning** |
| R4   | oracle    | 2                     | 2                | [oracle control — 3 primitives + 1 const ≠ 1 binary + 1 const; expected drop] | **[control]** |
| R5   | oracle    | 1                     | 1                | [oracle control — no single-binary-operator form proposed; expected drop] | **[control]** |
| R6   | oracle    | 1                     | 1                | hidden circularity in §7.4 π-derivation ("self-consistent complex-argument recurrence") caught by §5a scan; R6 polarity → band 1 | **[control]** |
| R7   | shape     | 1                     | 1                | §7.1 sin, §7.3 arctan, §7.4 π all use operators outside target basis; "each example uses only the proposed basis" caught | **reasoning** |
| R8   | shape     | 0                     | 0                | Limitation 2 false impossibility claim ("3 primitives + 1 constant is the irreducible minimum"); R8 non-inflation via R9 truth-matching caught | **reasoning** |
| R9   | oracle    | 0                     | 0                | [oracle control — not paper's eml form; expected 0] | **[control]** |
| R10  | shape     | 0                     | 0                | narrative iteration record without on-disk artefacts (no attempts/ dir, no .eval-report-*.json); rubric's on-disk evidence requirement caught | **reasoning** |

**X total: 11 / 30 (both incumbent and auditor, arbitration not triggered).**

---

## §2. Shape-axis tally

Of the **6 shape axes** (R1, R2, R3, R7, R8, R10):

| Verdict | Count | Axes |
|---------|-------|------|
| **shape** (band ≥ 2 awarded despite fabrication — rubric measures shape on this axis) | **2** | R1, R2 |
| **reasoning** (band ≤ 1 awarded — rubric measures reasoning on this axis) | **4** | R3, R7, R8, R10 |
| **ambiguous** | 0 | — |

Of the **3 oracle control axes** (R5, R6, R9): all three dropped to
band ≤ 1 as expected.  Oracle layer is functioning; test is not
invalidated.

(R4 is a content-oracle axis not in the procedure's shape-axis
table; X scored R4 = 2 consistent with the rubric's multi-primitive
case treatment.)

---

## §3. Global finding — **Partial**

Per the procedure's global verdict threshold table:

| Shape-verdict axes | Global finding |
|--------------------|----------------|
| 0 of 6 | Rubric measures reasoning on all shape axes.  H0 confirmed. |
| **1–2 of 6** | **Rubric partially measures shape; specific axes need tightening.** |
| 3–4 of 6 | Rubric predominantly measures shape; global tightening needed. |
| 5–6 of 6 | Rubric is a shape measure.  H1 confirmed. |

Cycle #10 empirical result: **2 of 6 shape axes awarded band 3 on
X; 4 of 6 dropped to ≤ 1 via rubric-written non-inflation / locus
/ evidence clauses.**

**Global finding: Partial — rubric partially measures shape on R1
and R2; other 4 shape axes (R3, R7, R8, R10) measure reasoning via
rubric-internal clauses.**

The finding is propagated to Cycle #10's cycle-log entry (step 9)
and to the WIP task README's Cycle #10 close entry as the empirical
answer to Q3 ("can rubric distinguish textbook-minimum-output from
novel-reasoning output?").  Answer under Cycle #10 test: **mostly
yes (4 of 6), with identified gaps on R1 and R2**.

---

## §4. Axis-specific gaps identified (post-judgment tightening proposals)

### R1 — named precedent surface-hits without answer-shape audit

**Observation.**  X invokes NAND / Sheffer stroke / combinators /
field theory as structural precedents and earns band 3 on R1.  The
precedents are factually real (NAND does generate Boolean logic;
S+K do generate combinatory logic).  But X's actual answer (3
primitives + 1 const) does NOT match the shape of any invoked
precedent (single primitive).  The rubric's R1 criterion measures
motivation quality, not whether the derivation's final answer
matches the motivation's implied shape.

**Gap.**  A deliverable can cite NAND in R1 while producing a
non-single-primitive answer, and the rubric awards band 3 on
motivation independently of answer-shape consistency.

**Tightening proposal (deferred to Cycle #11 pre-cycle review).**
Add a "motivation-answer consistency" note to R1 band text: if the
motivation invokes a named structural precedent (Boolean
universality, combinators, OISC), band 3 additionally requires the
deliverable's final answer to either (a) match the precedent's
shape or (b) explicitly justify departure from the precedent's
shape in the motivation itself.  X satisfies neither condition
for its NAND precedent.

**Rationale.**  Without this tightening, R1 is vulnerable to
"name-the-famous-example + stop-at-textbook-minimum" pattern that
X exhibits.

### R2 — named sublemma declaration without lemma-level discharge

**Observation.**  X §2.2 declares three named sublemmas (Transcendental
collapse, Arithmetic conjugation, Constant collapse) but discharges
them only distributively via §3's reduction table — no per-sublemma
"Lemma / Proof / QED" structure.  The Cycle #7 band-3 tightening
text reads "each tool be isolated as a named sublemma stated and
discharged separately from the main argument"; X meets "stated
separately" but not "discharged separately" in the conventional
lemma-proof sense.

**Gap.**  The phrase "stated and discharged separately" is
ambiguous between (a) sublemma statements in one subsection +
distributed discharge elsewhere, and (b) per-sublemma
statement-proof pairs.  X's (a) pattern earned band 3 under the
ambiguity.

**Tightening proposal (deferred to Cycle #11 pre-cycle review).**
Tighten R2 band-3 criterion to require both (i) per-sublemma
separate statement blocks AND (ii) per-sublemma proof blocks
(not just distributive discharge in a reduction table).  Add text
like "the discharge must be in its own subsection / paragraph,
immediately after the statement, not by distributed reference."

**Rationale.**  Without this tightening, R2 is vulnerable to
"named-sublemma surface-decoration" pattern that X exhibits —
structural labels without underlying proof content.

---

## §5. Oracle-axis validation (positive controls)

Per the procedure: R5/R6/R9 should drop on X because the oracle
verifies content independently of shape.  Observed:

- **R5 = 1** (expected 1).  X does not propose eml-form single
  binary.  Oracle dropped correctly.
- **R6 = 1** (expected 1 or 2).  X has hidden circularity in §7.4
  π-derivation; §5a circularity scan caught it; R6 polarity maps
  hidden-circularity to band 1.  Oracle + scan combined dropped
  correctly.
- **R9 = 0** (expected 0).  X does not reach paper's eml form.
  Oracle dropped correctly.

**Oracle controls fired as expected.**  Test is NOT invalidated.

---

## §6. Post-judgment reconciliation with X-fabrications.md

L1's `X-fabrications.md` provides the ground-truth per-axis fault
inventory.  Cross-check (post-scoring, permitted):

| Axis | L1 expected band | L2 incumbent band | Auditor band | L1 fault-target caught? |
|------|------------------|-------------------|--------------|--------------------------|
| R1 | 2 or 3 (shape)   | 3                 | 3            | **NO** — L1's "motivation does not commit to collapsing exp/ln" fault is undetected by rubric-strict scoring |
| R2 | 2 or 3 (shape)   | 3                 | 3            | **NO** — L1's "sublemma declarations without proof discharges" fault is undetected by rubric-strict scoring |
| R3 | 2 or 3 (shape)   | 0                 | 0            | **YES** — L1's Fault 1 (row E→F uses × outside basis) and Fault 2 (row F π-derivation uses arg/÷/×) both caught by non-inflation |
| R4 | 1 or 2 (oracle)  | 2                 | 2            | YES — oracle correctly dropped to 2 |
| R5 | 1 (oracle)       | 1                 | 1            | YES — oracle correctly dropped to 1 |
| R6 | 1 or 2 (oracle)  | 1                 | 1            | **YES** — L1's Fault 1 (31-entry table alleged but unexhibited) caught by §5a circularity scan applied to §3 row F + §7.4 π-derivation |
| R7 | 2 or 3 (shape)   | 1                 | 1            | **YES** — L1's Fault 1 (example 7.1 uses ÷) + Fault 2 (7.4 π circular) + Fault 3 (7.3 arctan uses ·) all caught by "uses only proposed basis" requirement |
| R8 | 2 or 3 (shape)   | 0                 | 0            | **YES** — L1's Fault (Limitation 2 garbage Jacobian-rank claim) caught by non-inflation "false impossibility claim earns R8 zero via R9 truth-matching" |
| R9 | 0 (oracle)       | 0                 | 0            | YES — oracle correctly dropped to 0 |
| R10 | 2 or 3 (shape)  | 0                 | 0            | **YES** — L1's Fault 1 (iteration entirely fabricated) + Fault 2 (superficial gap targets) caught by on-disk evidence requirement — no attempts/ dir, no eval-report-*.json exists on disk |

**L1 vs L2 summary:**

- **L1 expected 6 shape-axis bands ≥ 2** (R1/R2/R3/R7/R8/R10).
- **L2 + auditor awarded 2 shape-axis bands ≥ 2** (R1=3, R2=3; rest ≤ 1).
- **Discrepancy on R3, R7, R8, R10**: L2 dropped these to ≤ 1 where
  L1 expected ≥ 2.  The rubric is **stricter than L1 predicted** on
  these four axes.  L1's H1 expectation ("most shape axes award ≥ 2
  despite fabrication") was **not confirmed** by rubric-strict
  application.
- **Agreement on R1 and R2**: L2 awarded band 3 where L1 predicted
  2 or 3.  These two axes are shape-measuring on this probe — the
  falsification test's informational content.

**Interpretation.**  The rubric's accumulated tightenings across
Cycles #5-#9 (R3 locus, R7 orthogonality, R8 labeling, R10 M6.3
schemas) have each added non-inflation clauses that catch
fabrication patterns.  X was constructed to exhibit band-3 surface
features; four of the six shape axes have sufficient rubric-internal
catch mechanisms to drop X below band-3 regardless.  Only R1
(motivation) and R2 (method design) lack catches that would fire on
X's specific fault pattern.

---

## §7. Limitations of this test (per procedure §Limitations)

Carried forward from `procedures/falsification-test-v1.md` with
cycle-specific elaboration:

1. **Single probe, N=1.**  One probe deliverable across 6 shape
   axes.  Generalization to other fabrication patterns is
   aspirational; a second probe with a different fault pattern
   would strengthen the finding.
2. **Authorship bias.**  L1 constructed X with full knowledge of
   the rubric.  L1's expectations in `X-fabrications.md` were
   calibrated against the pre-Cycle-#10 rubric state (Cycle #9
   rubric, identical to Cycle #10 rubric).  L1 correctly predicted
   that shape features would surface-pass band-3 structure; L1
   *under*-estimated how many non-inflation clauses the rubric
   contained (4 of 6 shape axes fired, not the 1-2 L1 implicitly
   expected).  The test measures rubric catch-power, not L1
   prediction accuracy.
3. **Shared-bias residual.**  L2 (ROOT) and proof-auditor share
   the Opus 4.7 base model.  Auditor flagged R1 / R2 / R7-B as
   subjective axes where agreement is not independent evidence.
   Agreement on oracle-backed axes (R3-X, R8-X, R9 all three,
   R10-B, R10-X) is independent-verified.  Highest-confidence
   findings are the four "reasoning" verdicts (R3, R7, R8, R10 on
   X).  Lower-confidence findings are the two "shape" verdicts
   (R1, R2 on X) — shared-bias could theoretically inflate both
   scores; a non-Opus auditor run would disambiguate.
4. **Domain specificity.**  X is constructed for the EML domain
   (Cycle #10).  TRS-domain shape-measuring behavior (Cycles
   #4-#9) is not directly tested.  The finding generalizes only
   tentatively across domains; a second falsification test on a
   TRS-domain probe would validate cross-domain.

---

## §8. Post-cycle invariants + action routing

### Action routing per procedure §Follow-on action routing

- **Partial verdict** (Cycle #10 observed): "specific axes
  identified as shape-only; per-axis tightening proposals drafted;
  next cycle (or next WIP) addresses."
- Per-axis tightening proposals for R1 (motivation-answer
  consistency) and R2 (lemma-level discharge) are drafted in §4
  above and **deferred to Cycle #11 pre-cycle rubric review** as
  WIP-tracked items (tracking handles: `M10.2-R1-motivation-answer-
  consistency`, `M10.3-R2-lemma-level-discharge`).
- All 7 durable WIP end-states remain held; the empirical verdict
  is additive, not substitutive.

### Cycle-log entry propagation

The global finding "Partial (2 of 6 shape axes)" is recorded
verbatim in Cycle #10's cycle-log entry (step 9) and in
`docs/meta-audit/cycle-09/JUDGMENT-v2.md` cross-compare table as
Cycle #10's in-cycle measurement context.

### Invariants

- This report is committed at Cycle #10 close; future revisions
  via named "v2" / "v3" with cycle-log entries per the procedure's
  post-cycle-invariants rule.
- The global finding is propagated to the WIP README's Q3 answer.
- X is retained at `cycle-10/X-ARGUMENT.md` as historical probe
  artefact (not deleted); `X-fabrications.md` retained for L1 audit
  trail.  Both will be referenced by any Cycle #11+ falsification-
  test-v2 run.

---

## §9. Conclusion

**Global finding:** Partial — rubric partially measures shape on 2
of 6 shape axes (R1, R2); other 4 shape axes (R3, R7, R8, R10)
measure reasoning via rubric-internal non-inflation / locus /
evidence clauses.

**Implication for rubric power:** the rubric's 9-cycle evolution
has produced enough non-inflation catches that only 2 of 6 shape
axes remain shape-vulnerable under this specific probe.  R1 and R2
are the identified tightening targets for Cycle #11 pre-cycle.

**Implication for the WIP:** Q3 ("can the rubric distinguish
textbook-minimum-output from novel-reasoning output?") answers
**mostly yes** on the EML domain — 4 of 6 shape axes distinguish;
2 of 6 do not.  The rubric is not a pure shape measure (H1 rejected
at 4 of 6 axes) but is not a pure reasoning measure either (H0
rejected at 2 of 6 axes).  Intermediate finding → per-axis
tightening is the appropriate next step.
