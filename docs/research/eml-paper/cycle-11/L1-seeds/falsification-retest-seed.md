# Rubric Falsification Re-Test — v1

> Introduced at Cycle #11 pre-cycle (2026-04-23) to close the M9.4
> empirical loop.  Cycle #10's falsification test found Partial
> verdict (2 of 6 shape axes — R1 and R2 — awarded band ≥ 2 to
> the L1 probe despite semantic fault).  This procedure specifies
> how Cycle #11 re-scores the same probe under the R1/R2 tightening
> ports (M10.2 + M10.3) and reports the verdict shift.

## Purpose

Measure the pure rubric-tightening effect on R1 and R2 shape-verdict
by re-applying the rubric to an unchanged probe.  Any change in the
per-axis band between Cycle #10 (pre-tightening) and Cycle #11
(post-tightening) is attributable to the tightening text alone,
isolating it from:

- X-authorship drift (probe is reused verbatim)
- A/B performance drift (separate from X re-score)
- Domain drift (EML continuity with Cycle #10)
- Auditor drift (same proof-auditor invocation contract)

## Procedure

### Re-score setup

- **Probe:** Cycle #10's `cycle-10/X-ARGUMENT.md`, unchanged.
- **Rubric:** `judgment-rubric.md` at Cycle #11 state (post-
  M10.2/M10.3 port).  Cycle #11 pre-cycle commit lands the two
  rubric-axis clarifications following the same port pattern used
  for M8.1/M8.2.
- **Scoring output:** `cycle-11/X-JUDGMENT-v2.md`.  Per-axis band
  with rubric-text citation per axis and evidence-from-X per axis,
  in the same format as `cycle-10/X-JUDGMENT.md`.  L2 explicitly
  flags per axis which bands shifted from Cycle #10 v1 and why.
- **Auditor:** proof-auditor invocation with same contract.  X
  row in `cycle-11/rubric-audit.json` reflects post-tightening
  verdict.
- **Charity discipline:** same rubric-strict protocol from
  `falsification-test-v1.md`.  L2 must not adjust non-R1/R2 axes
  downward "because the rubric improved" — bands on R3/R7/R8/R10
  and oracle axes should remain identical unless the rubric-text
  on those axes also changed (it did not at Cycle #11).

### Per-axis shift table

`cycle-11/falsification-report-v2.md` contains a comparison:

```
| Axis | Axis type | Cycle #10 band (v1) | Cycle #11 band (v2) | Δ | Verdict shift |
|------|-----------|---------------------|---------------------|---|---------------|
| R1   | shape     | 3                   | ?                   | ? | shape→reasoning OR no shift |
| R2   | shape     | 3                   | ?                   | ? | shape→reasoning OR no shift |
| R3   | shape     | 0                   | 0                   | 0 | unchanged (control) |
| R4   | oracle    | 2                   | 2                   | 0 | unchanged (control) |
| R5   | oracle    | 1                   | 1                   | 0 | unchanged (control) |
| R6   | oracle    | 1                   | 1                   | 0 | unchanged (control) |
| R7   | shape     | 1                   | 1                   | 0 | unchanged (control) |
| R8   | shape     | 0                   | 0                   | 0 | unchanged (control) |
| R9   | oracle    | 0                   | 0                   | 0 | unchanged (control) |
| R10  | shape     | 0                   | 0                   | 0 | unchanged (control) |
```

Non-R1/R2 axes serve as within-probe controls.  They should
not move in v2.

### Retrospective A/B re-scoring

In addition to the X re-test, `cycle-10/JUDGMENT-v2.md` is authored
re-scoring Cycle #10 A-ARGUMENT.md and B-ARGUMENT.md under the
Cycle #11 tightened rubric per the standardized retrospective
procedure.  Expected per-axis shifts on A/B are recorded separately
from the X re-test (different deliverables, different tightening
triggers).

### Cycle #11 in-cycle A/B run

Cycle #11 also runs a fresh A/B on a fresh EML-domain TASK.md for
a new Δ measurement under the tightened rubric.  This is the normal
cycle flow — independent of the re-test.  The re-test and the
in-cycle A/B are logically separate measurements.

## Verdict rules

### Per-axis (R1 and R2)

- **shape → reasoning shift** if Cycle #11 v2 band ≤ 1 on that
  axis despite identical X content.  The tightening closed the
  shape-verdict on that axis.
- **no shift** if Cycle #11 v2 band ≥ 2 on that axis.  The
  tightening did not close the shape-verdict; further tightening
  or a redesigned rubric clause is needed.

### Global M9.4 closure verdict

| Cycle #11 R1 verdict | Cycle #11 R2 verdict | M9.4 closure |
|----------------------|----------------------|--------------|
| reasoning | reasoning | **Full-H0** — all 6 shape axes now measure reasoning.  M9.4 loop closed. |
| reasoning | shape | **Partial-reduced (1 of 6)** — R1 closed, R2 still needs work.  M9.4 loop partially closed. |
| shape | reasoning | **Partial-reduced (1 of 6)** — R2 closed, R1 still needs work.  M9.4 loop partially closed. |
| shape | shape | **Ineffective** — tightening did not land.  M9.4 loop not closed; seed redesign needed. |

The verdict is recorded in `cycle-11/falsification-report-v2.md`
and propagated to `cycle-11/L1-AUDIT.md` as the final empirical
answer for the WIP's Q3.

## Post-cycle invariants

- Cycle #11 is the final cycle of the current WIP per L0-approved
  Branch B (2026-04-23).  After L1-AUDIT sign-off, WIP closes.
- If the closure verdict is **Full-H0**, WIP closes cleanly —
  rubric's reasoning-measurement coverage is 6 of 6 shape axes.
- If the closure verdict is **Partial-reduced**, WIP closes with
  documented residual gap on the uncovered axis; a Q5 branch may
  carry it forward.
- If the closure verdict is **Ineffective**, WIP closes with
  documented failure — the R1 or R2 tightening did not land as
  expected; the Q5 branch must investigate why rubric-text-based
  tightening is insufficient for these axes.

The re-test's outcome determines WIP-closure framing but does
not extend WIP — this is the final cycle in all cases.

## L2 execution notes

1. The re-test is a separate scoring pass, not part of the main
   Cycle #11 A/B JUDGMENT flow.  Order of operations: (i) pre-
   cycle port M10.2/M10.3 into judgment-rubric.md, (ii) commit
   + tag cycle-11-pre, (iii) re-score X-ARGUMENT.md from Cycle #10
   location, (iv) launch normal A/B Cycle #11 flow, (v) retrospective
   A/B re-score, (vi) cycle close.
2. The re-test may happen before or after the in-cycle A/B
   launch — L2 choice.  The report file (`falsification-report-
   v2.md`) and the re-scored JUDGMENT (`X-JUDGMENT-v2.md`) can be
   committed separately or with the close commit.
3. The re-test scorer must NOT consult `X-fabrications.md` during
   the rubric-strict pass, matching the Cycle #10 protocol.  Post-
   judgment reconciliation in `falsification-report-v2.md` §
   post-judgment section is permitted.
