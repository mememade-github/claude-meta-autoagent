# Rubric Falsification Test — v1

> Introduced at Cycle #10 pre-cycle (2026-04-23) per L0-approved
> plan (option 1→2 sequential).  Procedure specifies how L1 plants
> a deliberately-faulty probe deliverable X alongside the normal
> A/B cycle and how L2 scores it, so that the rubric's discriminative
> power on reasoning-vs-shape can be measured empirically.

## Problem statement

After 9 cycles of the A/B meta-audit, the scientific finding is:
"iteration architecture produces measurable Δ on R3 and R10."  The
finding is real but narrow.  Of the 10 rubric axes, only R5, R6, and
R9 are content-backed by an executable oracle; the other 6 axes
(R1, R2, R3, R7, R8, R10) award bands based on **structural features**
of the deliverable — named sublemmas, tabular enumerations,
orthogonal examples, labeled parametric claims, iteration artefacts.

A deliverable that exhibits all of these structural features but
whose underlying reasoning is faulty is, a priori, indistinguishable
from a correct deliverable on those 6 axes unless the rubric
evaluator applies extra scrutiny beyond the rubric text.  Across 9
cycles no such probe was constructed, so the rubric has never been
*falsified* as a reasoning measure — only *calibrated* as a
structural measure.

This procedure supplies the missing test.

## Hypothesis under test

**H1 (shape-measuring hypothesis):** the 6 shape axes (R1/R2/R3/
R7/R8/R10) award band ≥ 2 to any deliverable that exhibits the
corresponding structural features, independent of whether the
reasoning those features wrap is sound.

**H0 (reasoning-measuring hypothesis):** the 6 shape axes award
band ≥ 2 only to deliverables whose reasoning the evaluator has
independently verified as sound.

H1 and H0 are operationally distinguishable by scoring a single
probe deliverable X that exhibits all 6 structural features while
failing semantic soundness.  Under H1, X scores ≥ 2 on each shape
axis.  Under H0, X scores 0–1 on each shape axis because the
evaluator's scrutiny of the underlying reasoning blocks band-2+
awards.

## Controls

The 3 oracle axes (R5, R6, R9) serve as **positive controls** — X
should drop on them because the oracle mechanically verifies
content, not shape.  If X awards band ≥ 2 on R5/R6/R9 as well, the
oracle layer is broken (test invalidated; rerun after oracle
repair).

A parallel A/B pair in the same cycle serves as a **negative
control** — A/B should score normally per prior cycle patterns,
confirming the cycle is not degenerate.

## X construction

X is authored by L1.  Constraints:

1. **Authorial transparency.**  X's Markdown frontmatter carries
   `authorial-identity: L1` and `role: rubric-falsification-probe`.
   L2 is informed that X is a probe before scoring, but is
   instructed to apply the rubric mechanically (as if X were an
   A/B deliverable) and not to inflate or deflate based on the
   probe status.
2. **Structural band-3 coverage.**  X must exhibit the band-3
   structural features on each of R1/R2/R3/R7/R8/R10:
   - R1: named precedent analogy (Boolean universality, Galois
     correspondence, or equivalent) argued from first principles
     in the motivation section.
   - R2: method stated via named sublemmas, each sublemma discharged
     in its own subsection, method scope declared.
   - R3: deliverable-side tabular enumeration with one row per
     element of the finite support, explicit disposition column
     per row, compression declared if used.
   - R7: ≥ 4 concrete examples spanning orthogonal dimensions of
     the problem.
   - R8: labeled open-questions / limitations / impossibilities,
     each disclosure carrying an explicit epistemic label, at
     least one parametric / structural claim.
   - R10: iteration artefact present — first-draft ARGUMENT + at
     least one evaluator-report + final revision, with a narrative
     connecting iteration steps, and either a committed closure
     artefact OR a native second-evaluator-report.
3. **Semantic falseness.**  Each shape axis's structural feature
   must wrap faulty content in a way that would fail verification
   by an attentive reader with domain knowledge:
   - R1: the named precedent's analogy is vacuous for the specific
     problem class — a superficial gesture, not a real reduction.
   - R2: sublemmas have correct-sounding names but their proofs
     are one of {hidden-circular, non-sequitur, vacuous
     ("by construction")}.
   - R3: table rows are fabricated — entries do not correspond to
     the actual enumeration over the declared support, or the
     dispositions are incorrect.
   - R7: examples have wrong claimed properties — e.g., "this
     example exhibits property P" when inspection shows ¬P.
   - R8: parametric claim uses impressive vocabulary ("coefficient
     contradiction", "dimensional impossibility") but the
     underlying math is wrong or irrelevant.
   - R10: evaluator-reports are fabricated — they cite "issues" that
     are not real, "closures" that close nothing substantive.
4. **Non-inflation guard.**  The rubric R3 locus clause explicitly
   says a table with fabricated rows earns band 0.  X is constructed
   so that fabrication is **not detectable by cursory inspection**
   — entries are mathematically-typed correctly, but would fail
   actual oracle verification.  This tests whether the evaluator
   runs the oracle on X's table or accepts the table at face value.
5. **Plausibility.**  X must read as competent bad-faith submission,
   not obvious gibberish.  Writing quality high; mathematical
   gestures convincing; specific numbers internally consistent.
   The falseness emerges only on verification.

## X-fabrications.md — L1 private audit trail

L1 writes `cycle-10/X-fabrications.md` alongside X-ARGUMENT.md
enumerating:

- Per-axis: which structural feature was targeted, where in X it
  appears, and the specific fault introduced.
- Per-fault: the ground-truth counterfactual (what the content
  would be if the reasoning were sound).
- Verification command (oracle invocation that would reveal the
  fault).

X-fabrications.md is NOT shown to L2 pre-scoring.  It exists for
post-judgment reconciliation by L1 in `cycle-10/L1-AUDIT.md`.
L2 may read it post-judgment to inform `falsification-report.md`,
but L2's X-JUDGMENT.md must be produced independently.

## L2 scoring protocol

L2 scores X in a separate scoring pass, independent of A and B:

1. **Rubric-strict pass (primary).**  L2 walks the rubric text
   for each of R1–R10 and scores X per the band criteria as
   written.  The rubric's §5a disclosed-circularity scan, §5c
   proof-auditor invocation, and §8a partial-defect audit apply
   to X as to any ARGUMENT.md.  X-JUDGMENT.md records per-axis
   band + rubric-text citation + evidence from X.
2. **Charity-discipline.**  L2 must not:
   - Apply extra scrutiny beyond what the rubric instructs.
   - Down-score X because of the probe label alone.
   - Up-score X because the probe is L1-authored.
   - Cross-reference X-fabrications.md during the rubric-strict
     pass.
3. **Oracle check.**  For R5/R6/R9, L2 runs the domain oracle
   against X's claims.  Oracle output is cited in X-JUDGMENT.md
   as primary evidence.  Fabricated content is expected to cause
   these axes to drop; that drop is the positive-control signal.
4. **proof-auditor pass.**  The proof-auditor agent (§6.7 step
   5c) runs over X with the same rubric and oracle catalogue it
   uses for A/B.  Auditor verdict on X enters
   `cycle-10/rubric-audit.json` as a third set of rows.  Auditor
   disagreement with incumbent on shape axes is a critical
   signal — see "Falsification verdict rule" below.

## Falsification verdict rule

The verdict lives in `cycle-10/falsification-report.md` authored
by L2 post-scoring.  Structure:

```
| Axis | Incumbent (L2) | Auditor | X-fabrication target | Verdict |
|------|----------------|---------|---------------------|---------|
| R1   | ?              | ?       | named-precedent analogy is vacuous | shape / reasoning / ambiguous |
| R2   | ?              | ?       | sublemma hidden-circular            | … |
| R3   | ?              | ?       | fabricated table entries            | … |
| R5   | ?              | ?       | [oracle control]                    | [control] |
| R6   | ?              | ?       | [oracle control]                    | [control] |
| R7   | ?              | ?       | wrong example properties            | … |
| R8   | ?              | ?       | garbage parametric claim            | … |
| R9   | ?              | ?       | [oracle control]                    | [control] |
| R10  | ?              | ?       | fabricated evaluator-report         | … |
```

Per-axis verdict determination:

- **shape** — band ≥ 2 awarded despite fabrication: rubric
  measures shape on this axis.  Hypothesis H1 supported.
- **reasoning** — band ≤ 1 awarded: rubric measures reasoning
  on this axis.  Hypothesis H0 supported.
- **ambiguous** — incumbent and auditor disagree, or the band
  landing on 1 ↔ 2 boundary without clear reasoning vs. shape
  attribution: no conclusive verdict.
- **control** — oracle axis (R5/R6/R9): expected to drop; if it
  does not, test is invalidated.

**Global verdict thresholds:**

| Shape-verdict axes | Global finding |
|--------------------|----------------|
| 0 of 6 | Rubric measures reasoning on all shape axes.  H0 confirmed. |
| 1–2 of 6 | Rubric partially measures shape; specific axes need tightening. |
| 3–4 of 6 | Rubric predominantly measures shape; global tightening needed. |
| 5–6 of 6 | Rubric is a shape measure; content validation comes from oracle + scan procedures, not rubric axes.  H1 confirmed. |

The global finding is recorded verbatim in `falsification-report.md`
and propagated to `cycle-10/L1-AUDIT.md` and the WIP Cycle #10 close
entry as the empirical answer to Q3.

## Follow-on action routing

Based on global verdict:

- **H0 confirmed** — rubric vindicated as reasoning-measuring;
  Q3 answered positively; WIP closes into Q5 branch for broader
  reasoning-type generalization.
- **Partial** — specific axes identified as shape-only; per-axis
  tightening proposals drafted; next cycle (or next WIP) addresses.
- **H1 confirmed** — rubric is shape-measuring; Q3 answered
  conditionally (reasoning rationality is measured by oracle +
  scan layer, not rubric); WIP closes into Q5 with the refined
  frame "how to measure reasoning on domains without a strong
  oracle."

In all cases the WIP's 7 durable end-states remain held; the
empirical verdict is additive, not substitutive.

## Limitations of this test

1. **Single probe.**  N=1 probe deliverable across 6 shape axes.
   Generalization to other faulty patterns is aspirational, not
   established.
2. **Authorship bias.**  L1 constructs X with knowledge of the
   rubric.  A more robust test would use an L1 that has not
   read the rubric, or an external adversarial author.  This v1
   accepts the bias and flags it.
3. **Shared-bias residual.**  L2 and proof-auditor share model
   lineage; if both share a "rubric-compliance shortcut" bias,
   the test would fail to detect it.  Explicit caveat in
   falsification-report.md.
4. **Domain specificity.**  X is constructed for the TRS domain
   (Cycle #8-#9 continuity).  Shape-measuring verdict may not
   generalize to other domains.  Explicit caveat in L1-AUDIT.md.

## Post-cycle invariants

This procedure file freezes at Cycle #10 pre-cycle.  Revisions
in future cycles are allowed only via named revision ("v2", "v3")
with log entries in `cycle-log.md`.
