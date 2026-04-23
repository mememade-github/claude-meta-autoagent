---
cycle_rescored: cycle-07
rescored_under: cycle-08 rubric (at commit 988e3ed)
original_judgment: docs/research/eml-paper/cycle-07/JUDGMENT.md
rescore_authored_in: cycle-08
status: retrospective
---

# Cycle 07 — JUDGMENT-v2 (retrospective re-score under Cycle #8 rubric)

Per `docs/research/eml-paper/retrospective-rescore.md` (mandatory at
every cycle close from Cycle #8 forward).  Re-applies the rubric in
its Cycle #8 pre-cycle state to the **frozen** Cycle #7 deliverables.
The deliverables themselves are unchanged from
`docs/research/eml-paper/cycle-07/A-ARGUMENT.md` and
`docs/research/eml-paper/cycle-07/B-ARGUMENT.md` (`git log` shows no
commits to either after the Cycle #7 close at `ade4107`).  The
purpose is to isolate the rubric-effect contribution to any Cycle #8
in-cycle Δ.

## §1. Rubric delta between Cycle #7 close and Cycle #8 pre-cycle

The Cycle #8 pre-cycle commit (`988e3ed`) modified the rubric in
exactly one place:

- **R10 M6.3 (band-2/3 evaluator-report-substitution).**  The
  permitted-substitute "(c) committed diff artefact, separate from
  the deliverable" was sharpened by naming
  `docs/research/eml-paper/gap-closure-check.schema.json` as the
  authoritative shape and enumerating its required fields
  (`cycle_id`, `iteration_index`, `prior_iteration_report`,
  `prior_iteration_path`, `current_iteration_path`,
  `closures` (non-empty array with per-entry `gap_id`, `gap_source`,
  `evidence_type`, `evidence_path`, `closure_location`),
  `verifier_identity` from a five-element allow-list excluding
  self-attestation, `non_inflation_check` with `performed: true` +
  result enum).  Schema-conformant equivalents at any path qualify.

This is a *sharpening of evidence requirements*, not a band-text
change.  R10's band-2/3 boundary remains: band 3 requires one of
{(a) subsequent eval report, (b) independent oracle output
mechanically confirming closure, (c) committed diff artefact}.  The
sharpening codifies *what shape* (c) must take to qualify; it does
not alter whether Cycle #7 B's deliverable would have qualified.

R1, R2, R3, R4, R5, R6, R7, R8, R9, and R10 bands 0/1/2 are textually
identical to Cycle #7's reading.  No other axis was modified at the
Cycle #8 pre-cycle commit.

## §2. Per-axis re-score

| Axis | A v1 | A v2 | B v1 | B v2 | Movement | Rubric clause |
|------|-----:|-----:|-----:|-----:|----------|----------------|
| R1 Motivation | 3 | 3 | 3 | 3 | — | unchanged |
| R2 Method design | 3 | 3 | 3 | 3 | — | unchanged (band-3 tightening text from Cycle #7 still applies; both A and B met it) |
| R3 Progressive minimization | 2 | 2 | 3 | 3 | — | unchanged (A's prose self-overlap dispatch still caps at 2; B's 10-row table still meets band 3) |
| R4 Verdict commitment | 3 | 3 | 3 | 3 | — | unchanged (Cycle #7 R4 3-obligation semantic still in force) |
| R5 Exact form | 3 | 3 | 3 | 3 | — | unchanged (mechanical re-verification holds) |
| R6 Verification strategy | 3 | 3 | 3 | 3 | — | unchanged (oracle + no hidden circularity) |
| R7 Constructive examples | 3 | 3 | 3 | 3 | — | unchanged (≥4 examples + coverage table for both) |
| R8 Open questions | 3 | 3 | 3 | 3 | — | unchanged (multiple parametric disclosures in both) |
| R9 Exact answer match | 3 | 3 | 3 | 3 | — | unchanged (both committed all three correctly) |
| R10 Iteration depth | 0 | 0 | 2 | 2 | — | M6.3 sharpening is forward-looking only — Cycle #7 B did not produce any (a)/(b)/(c) substitute; under the sharpened (c) the absence is the same absence; band 2 remains correct |
| **Total** | **26** | **26** | **29** | **29** | — | |

## §3. Delta comparison

```
v1 Δ: B_v1 - A_v1 = 29 - 26 = +3
v2 Δ: B_v2 - A_v2 = 29 - 26 = +3
Movement: v2 Δ - v1 Δ = 0  (zero rubric drift across Cycle #8 pre-cycle)
```

## §4. Narrative

The Cycle #8 pre-cycle commit's rubric change is a **sharpening of
M6.3 evidence shape**, not a band-text change.  R10 M6.3 still admits
the same three substitute kinds; the sharpening fixes the
field-shape of substitute (c) so that future graders can mechanically
audit whether a `gap-closure-check.json`-equivalent qualifies.

For Cycle #7 B's R10 = 2 evaluation, the absence of any of (a), (b),
or (c) is the load-bearing fact, and that absence is invariant under
the sharpening: B did not commit any per-gap closure artefact in any
shape.  Under the sharpened M6.3, the same absence yields the same
band 2.

For all other axes, the Cycle #7 rubric text is identical to the
Cycle #8 pre-cycle text — the band-3 tightenings (R2/R3/R7/R8) and
R10 codifications (M6.2/M6.3) were already in force at Cycle #7
pre-cycle commit `9421996`.  No movement is observed because none is
expected.

This zero-movement retrospective is the **expected outcome** for a
cycle whose pre-cycle commit only sharpens evidence shape rather
than changing band thresholds.  It confirms that the rubric is
stable across this pre-cycle and that the procedure works as a
"control" reading even when its own input variation is null.  Per
the procedure doc §"When to run", this is exactly the case where
"the retrospective confirms zero drift and establishes the baseline
procedure as always-on" — non-trivially valuable, because future
cycles whose pre-cycle commits *do* tighten band text will produce
a non-zero re-score whose isolation depends on the always-on
baseline.

## §5. Cross-comparison with Cycle #7 in-cycle and Cycle #6
retrospective

Three measurements of the rubric / task / leakage decomposition for
the immediately-prior cycles:

| Measurement | A | B | Δ | Leakage component | Rubric component |
|-------------|--:|--:|--:|-------------------|------------------|
| Cycle #7 in-cycle (leaky TASK + Cycle #7 rubric) | 26 | 29 | +3 | + (M7.1 confirmed) | base |
| Cycle #6 retrospective under Cycle #7 rubric (clean TASK + Cycle #7 rubric) | 23 | 29 | +6 | 0 | base + tightening |
| Cycle #7 retrospective under Cycle #8 rubric (this file) | 26 | 29 | +3 | + (Cycle #7 TASK was leaky; not removable retrospectively) | base + tightening + M6.3 sharpening |

The third row's leakage component is **non-removable retrospectively**:
Cycle #7's TASK was leaky and the deliverables were produced under
that leak.  The rubric sharpening at Cycle #8 pre-cycle is
forward-looking and does not re-write history.  The Cycle #7
retrospective therefore inherits Cycle #7's leakage; it measures only
rubric-drift since Cycle #7 close, which is zero.

The Cycle #6 retrospective (Δ=+6) is the cleanest signal of the
tightening's discriminative power: a clean TASK + the tightening
rubric.  If Cycle #8 in-cycle Δ approaches +6, the prompt-hint
discipline forward guardrail is effective.  If Cycle #8 in-cycle
remains near +3, either the Cycle #8 TASK is harder (pushes A below
floor) or some other confound dominates.

## §6. Status disposition

`status: retrospective` — Cycle #7's original close stands as the
authoritative judgment for that cycle.  This v2 file is **additional
evidence** captured at Cycle #8 close to support the cross-cycle Δ
narrative.  No re-tagging of Cycle #7 commits.  No mutation of
Cycle #7 artefacts.
