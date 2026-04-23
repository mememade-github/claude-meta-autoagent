---
cycle_rescored: cycle-08
rescored_under: cycle-09 rubric (at commit ba9fb45)
original_judgment: /workspaces/docs/meta-audit/cycle-08/JUDGMENT.md
rescore_authored_in: cycle-09
status: retrospective
---

# Cycle 08 — JUDGMENT (v2, retrospective under Cycle #9 rubric)

Retrospective re-score of Cycle #8 A and B deliverables under the
Cycle #9 rubric state (ba9fb45). Per
`docs/research/eml-paper/retrospective-rescore.md`: holds
deliverables and task constant; varies only the rubric; isolates
pure rubric effect.

## §0. Inputs

- **Cycle #8 A-ARGUMENT.md** —
  `/workspaces/docs/meta-audit/cycle-08/A-ARGUMENT.md` (frozen at
  commit f0d569d, 8757 B).
- **Cycle #8 B-ARGUMENT.md** —
  `/workspaces/docs/meta-audit/cycle-08/B-ARGUMENT.md` (frozen at
  commit f0d569d, 17258 B).
- **Cycle #8 original JUDGMENT.md** — read-only v1 reference
  (A = 20, B = 26).
- **Rubric** —
  `/workspaces/docs/research/eml-paper/judgment-rubric.md` at
  Cycle #9 state (commit ba9fb45), carrying:
  - R3 band-3 **locus clarification** (deliverable-side tabular
    presentation required for band 3 when finite tractable
    support).
  - R8 band-3 **labeling clarification** (each disclosure must
    carry an explicit epistemic label; dedicated section naming
    not required).
  - R10 M6.3 (c) **reproducibility tag** requirement.

## §1. Freeze verification

`git log -- docs/meta-audit/cycle-08/A-ARGUMENT.md
docs/meta-audit/cycle-08/B-ARGUMENT.md` returns only commit
**f0d569d** (Cycle #8 close). No post-close edits. Both
deliverables frozen as required by the retrospective procedure.
✓

## §2. Per-axis re-score

Axes are scored under Cycle #9 rubric text exactly as a Cycle #9
grader would score them on *these* Cycle #8 deliverables.

### R1 Motivation — A: 1 → 1 (unchanged) | B: 2 → 2 (unchanged)

The Cycle #9 rubric text of R1 is unchanged from Cycle #8 (neither
the R3 locus, R8 labeling, nor R10 reproducibility-tag ports touch
R1). A's Q1-only §2-closing commentary still lands at band 1; B's
distributed per-Q structural commentary + parametric §2.5 still
lands at band 2. **No movement.**

### R2 Method design — A: 3 → 3 (unchanged) | B: 3 → 3 (unchanged)

R2 Cycle #7 tightening is unchanged in Cycle #9. A's two named
lemmas (NF-1 + Unique Redex Lemma) and B's preliminary lemmas +
Lemma 3.2 + Theorem 3.3 both meet the tightening. **No movement.**

### R3 Progressive minimization — A: 1 → 1 (unchanged) | B: 2 → 2 (unchanged)

**Cycle #9 locus clarification applied:** deliverable-side tabular
presentation required for band 3 when enumeration has finite
tractable support; oracle-committed enumeration without a
deliverable-side table maxes at band 2.

- **A (v1 = 1):** A presents no critical-pair enumeration at all
  (neither prose nor table); goes directly to single witness
  `q(0, e)`. Band 1 under Cycle #8 text (1–2 intermediate steps
  without enumeration justification). Band 1 under Cycle #9 text
  (locus clarification requires a deliverable-side table for band
  3; A has no enumeration locus at all, so band 1 carries).
  **Unchanged.**

- **B (v1 = 2):** B's deliverable §2.5 gives a *prose summary* of
  unifiable critical pairs; the full 104-triple CP enumeration
  lives in `B-simulator.py` (oracle), not in the ARGUMENT.md text.
  Under Cycle #8 text: borderline 2/3 (tabular elements exist —
  §1.1 8-row LHS heads, Appendix A 8-row per-rule; but the CP
  enumeration itself is prose-only in the deliverable). Cycle #8
  scored 2. **Under Cycle #9 locus clarification explicitly:**
  "oracle-committed enumeration WITHOUT a deliverable-side table
  maxes at band 2" — the clarification retroactively **confirms**
  the Cycle #8 band-2 score as the correct reading. **Unchanged.**

**Retroactive validation:** Cycle #9 locus clarification does not
reverse any Cycle #8 R3 score; it sharpens the future-cycle
discrimination. Cycle #8 R3 Δ unchanged.

### R4 Verdict commitment — A: 3 → 3 (unchanged) | B: 3 → 3 (unchanged)

R4 Cycle #7 3-obligation semantic unchanged in Cycle #9. Both A
and B meet the tightening. **No movement.**

### R5 Exact form — A: 3 → 3 (unchanged) | B: 3 → 3 (unchanged)

R5 unchanged. Both mechanically correct per Cycle #8 grading +
ROOT oracle. **No movement.**

### R6 Verification strategy — A: 3 → 3 (unchanged) | B: 3 → 3 (unchanged)

R6 honesty-polarity ordering + circularity-scan rules unchanged
in Cycle #9. Both A and B discharged at band 3 in Cycle #8 with
no hidden circularity. **No movement.**

### R7 Constructive examples — A: 2 → 2 (unchanged) | B: 2 → 2 (unchanged)

R7 Cycle #7 tightening (≥ 4 examples OR ≥ 3 orthogonal modes) is
unchanged in Cycle #9. Both A and B had 2 witnesses + 2
orthogonal axes in Cycle #8; both still cap at band 2 under
Cycle #9. **No movement.**

### R8 Open questions — A: 1 → 1 (unchanged) | B: 2 → 2 (unchanged)

**Cycle #9 labeling clarification applied:** band 3 requires (i)
≥ 3 distinct disclosures, (ii) ≥ 1 structural/parametric, (iii)
each disclosure explicitly labeled as open question / limitation /
impossibility / equivalent epistemic marker. Sufficient labels
include dedicated section headers, in-text markers, or
operator-level impossibility framings. Dedicated section naming
is NOT required.

- **A (v1 = 1):** A's §5 single-instance rule-removal observation
  ("Removing alpha7 from R would not restore confluence...
  Removing alpha5 and alpha6 would not restore normalization").
  One unlabeled observation; trivial in content. Band 1 under
  Cycle #8 text. Under Cycle #9 labeling clarification: same
  content, still unlabeled, still < 3 distinct disclosures; band
  1 carries. **Unchanged.**

- **B (v1 = 2):** B's §2.5 parametric statement ("Any pair of
  rules with shape `g(v_1, ..., v_n) -> v_i` and
  `g(v_1, ..., v_n) -> v_j` with `i != j` produces a non-joining
  critical pair at the root") IS an operator-level impossibility
  framing — under Cycle #9 labeling clarification, this is a
  qualifying epistemic label. §5 bidirectional rule-removal is
  unlabeled structural content. Appendix A structural contrast
  is a "sanity reference" label, not open-question / limitation /
  impossibility.

  Count under Cycle #9 labeling clarification:
  - 1 labeled disclosure (§2.5 parametric impossibility framing) ✓
  - 2 unlabeled structural disclosures (§5, Appendix A)

  **< 3 labeled disclosures, < 3 epistemically-labeled.** Under
  Cycle #9 band-3 criterion: NOT met. Band 2: "structural /
  parametric content present but unlabeled (embedded in the
  proof body or sanity appendix without epistemic framing), or
  fewer than 3 distinct disclosures." B has content present with
  1-of-3 labeled; band 2 still fits. Cycle #8 scored 2 for "strong
  structural commentary, but not in open-question framing" — the
  Cycle #9 labeling clarification gives a sharper reason for the
  same score (1 labeled disclosure is < 3 required). **Unchanged.**

**Retroactive validation:** Cycle #9 labeling clarification does
not reverse any Cycle #8 R8 score; it sharpens the *reason* for
B's band 2. Cycle #8 R8 Δ unchanged.

### R9 Exact answer match — A: 3 → 3 (unchanged) | B: 3 → 3 (unchanged)

R9 3-obligation semantic unchanged. Both A and B correct on all
three. **No movement.**

### R10 Iteration depth — A: 0 → 0 (unchanged) | B: 3 → 3 (unchanged)

**Cycle #9 reproducibility-tag port applied:** each R10 band 3
score via M6.3 (c) MUST record `agent-spontaneous` /
`scaffolding-assisted` / `not-applicable`.

- **A (v1 = 0):** A had no Cycle #8 iteration trace. Band 0
  under both rubrics. **Unchanged.**

- **B (v1 = 3):** B reached band 3 in Cycle #8 via M6.3
  substitute (c) — ROOT-authored `B-gap-closure-check.json`.
  Under Cycle #9 reproducibility-tag port: this was a
  **`scaffolding-assisted`** closure-artefact (ROOT authored it
  on B's behalf to verify per-gap closure, since B did not
  produce its own second-iteration evaluator report). Per the
  port: "A `scaffolding-assisted` tag is acceptable for exactly
  one cycle after schema introduction (Cycle #8 exercised this
  path)." The tag is applied retrospectively and is recorded
  here for the historical record:

  **Cycle #8 R10-B reproducibility tag: `scaffolding-assisted`**

  This tag is within the per-port allowance ("acceptable for
  exactly one cycle after schema introduction"); Cycle #8 IS
  that one cycle. Band 3 stands. If Cycle #9 or later also
  showed `scaffolding-assisted` via (c), the accumulation would
  signal an architectural finding. Cycle #9 did NOT repeat the
  pattern (Cycle #9 B reached band 3 via native M6.3 (a) path;
  see Cycle #9 JUDGMENT.md §R10). **Architectural
  reassurance.**

  Band 3 **unchanged**; tag newly recorded for historical
  record.

## §3. Per-axis comparison table

| Axis | A v1 | A v2 | B v1 | B v2 | Movement | Rubric clause |
|------|------|------|------|------|----------|----------------|
| R1   | 1 | 1 | 2 | 2 | — | unchanged (R1 text unchanged in Cycle #9) |
| R2   | 3 | 3 | 3 | 3 | — | unchanged (Cycle #7 tightening retained) |
| R3   | 1 | 1 | 2 | 2 | — | Cycle #9 locus clarification **retroactively confirms** Cycle #8 scoring |
| R4   | 3 | 3 | 3 | 3 | — | unchanged (3-obligation semantic retained) |
| R5   | 3 | 3 | 3 | 3 | — | unchanged |
| R6   | 3 | 3 | 3 | 3 | — | unchanged (honesty-polarity retained) |
| R7   | 2 | 2 | 2 | 2 | — | unchanged (Cycle #7 tightening retained) |
| R8   | 1 | 1 | 2 | 2 | — | Cycle #9 labeling clarification **retroactively confirms** B's band 2 via explicit label count |
| R9   | 3 | 3 | 3 | 3 | — | unchanged |
| R10  | 0 | 0 | 3 | 3 | — | Cycle #9 reproducibility-tag port **retroactively attaches** `scaffolding-assisted` tag to Cycle #8 R10-B |
| **Total** | **20** | **20** | **26** | **26** | **— (0 / 0)** | |

## §4. Delta comparison

```
v1 Δ (Cycle #8 in-cycle under Cycle #8 rubric):
  B_v1 − A_v1 = 26 − 20 = +6

v2 Δ (Cycle #8 deliverables under Cycle #9 rubric):
  B_v2 − A_v2 = 26 − 20 = +6

Movement: v2 Δ − v1 Δ = 0
  → pure rubric effect on prior cycle: 0 points.
```

## §5. Narrative

**Zero movement on every axis.** The Cycle #9 pre-cycle ports
(R3 locus clarification, R8 labeling clarification, R10
reproducibility-tag requirement) are **all formalizations of
decisions implicit in Cycle #8's scoring**, not new criteria
that rescore prior deliverables. Specifically:

- **R3 locus clarification (`cycle-09/L1-seeds/R3-enumeration-
  locus-seed.md`)** was motivated by Cycle #8 R3-B's CONDITIONAL
  between "oracle-committed enumeration = band 3" and "deliverable-
  only table = band 3". Cycle #8 scored 2 (oracle path without
  deliverable table). Cycle #9's clarification codifies that
  Cycle #8 reading — it does not revise it. Retrospective R3-B =
  2 confirms the formalization is **backward-compatible**.

- **R8 labeling clarification (`cycle-09/L1-seeds/R8-parametric-
  content-locus-seed.md`)** was motivated by Cycle #8 R8-B's
  CONDITIONAL on whether a "dedicated section" is required or
  labeling anywhere suffices. Cycle #9 ruled: labeling anywhere
  suffices, but each disclosure must carry an explicit epistemic
  label. Cycle #8 B had 1 labeled (§2.5 parametric) + 2 unlabeled
  (§5, Appendix A) — < 3 labeled, band 2 under Cycle #9 criterion.
  Cycle #8 scored 2. Retrospective R8-B = 2. **Backward-compatible.**

- **R10 reproducibility-tag port (`procedures/closure-artefact-
  reproducibility.md`)** was motivated by Cycle #8's first
  exercise of M6.3 (c) via ROOT authorship. The port requires
  per-cycle tags (`agent-spontaneous` / `scaffolding-assisted` /
  `not-applicable`) and permits exactly one cycle of
  `scaffolding-assisted` post-schema-introduction. Cycle #8
  occupies that one cycle. Retrospective R10-B = 3 with tag
  `scaffolding-assisted` **matches the port's explicit allowance**.
  Band 3 unchanged; tag attached retrospectively. **Backward-
  compatible.**

**Retrospective scientific outcome:** the Cycle #9 rubric ports
are purely forward-looking sharpenings that formalize Cycle #8
grading decisions without overturning them. The clean zero-movement
result validates the port design — if any port had shifted Cycle
#8 scores, it would have indicated the port was not merely a
clarification but a silent re-criterion. All three ports pass
this test.

## §6. Cross-compare with Cycle #9 in-cycle

| Measurement | A | B | Δ | Leakage attributable |
|-------------|---|---|---|----------------------|
| Cycle #9 in-cycle under Cycle #9 rubric | 23 | 25 | **+2** | (in-cycle TASK) |
| Cycle #8 retrospective under Cycle #9 rubric | 20 | 26 | **+6** | 0 (Cycle #8 TASK did not know Cycle #9 rubric) |
| **Gap** | — | — | **−4** | — |

**Interpretation.** Cycle #9 in-cycle Δ = +2 is **smaller than**
the Cycle #8 retrospective Δ = +6. The −4 gap is NOT attributable
to prompt-hint leakage (Cycle #9 TASK was authored rubric-blind
per `task-prompt-discipline.md`, verified at pre-cycle commit).

The −4 gap is attributable to **Cycle #9's deliverable-shape
differences** between A and B:

- **A stepped up:** Cycle #9 A has distributed per-Q structural
  commentary (§2 parametric remark + §3 structural remark + §5
  bidirectional rule-removal) where Cycle #8 A had Q1-only
  closing paragraph. R1 +1, R8 +1 (under Cycle #9's content-
  unlabeled = band 2 rule).

- **B stepped sideways / down:** Cycle #9 B has method-focused
  opening (iteration-trace header + oracle announcement) rather
  than structural-source commentary. R1 −1 (from 2 to 1).
  Cycle #9 B has fewer labeled open-question disclosures than
  Cycle #8 B (single §5 "irreducible structural asymmetry" is
  methodological not substantive). R8 −1 (from 2 to 1).

- **B lifted +1 on R3** thanks to Cycle #9 locus clarification
  + Cycle #9 B's explicit §3.4 markdown table — this is the
  single Cycle #9 axis where the deliverable and the rubric port
  cooperated to lift B above Cycle #8.

Net: Cycle #9 A +2 total (from 20 → 23 in Cycle-#9-A-like-
Cycle-#8-A-except-better-R1-and-R8); Cycle #9 B −1 total
(from 26 → 25: R1 −1, R8 −1, R3 +1).

The gap reflects **real deliverable variance**, not rubric or
prompt-hint effects. This is the experimental apparatus
functioning as intended — the retrospective isolates rubric
effect (=0), confirming the −4 is deliverable-shape variance.

## §7. Port-backward-compatibility verdict

All three Cycle #9 pre-cycle rubric ports pass the retrospective
backward-compatibility test (0 movement on prior deliverables).
The ports may be considered **structural sharpenings**, not
re-criteria. Future cycles may rely on them without destabilising
prior historical scoring.

## §8. Storage

- Filed at `/workspaces/docs/meta-audit/cycle-08/JUDGMENT-v2.md`
  per `retrospective-rescore.md` §Storage (retrospective lives
  under the cycle being rescored, authored during the cycle
  doing the rescoring).
- Cycle #9 `cycle-log.md` entry references this file with a
  one-line summary ("Retrospective: Cycle #8 under Cycle #9
  rubric, 0 movement on all 10 axes, v1 Δ = +6 retained").
