# Cycle #11 TASK-draft (L1 reference)

> L1 drafts this as **reference**, not mandate.  L2 ROOT holds TASK
> authorship autonomy.  Cycle #11 continues the Cycle #10 EML-domain
> restore (no further domain changes for the remainder of this WIP).
> Primary objective: close M9.4 empirical loop via R1/R2 rubric
> tightening + falsification re-test on Cycle #10's X-ARGUMENT.md.
> Secondary: normal in-cycle A/B run to measure post-tightening Δ.

## Why this draft exists

Cycle #10 scored Cycle #10 X at R1=3, R2=3 despite semantic fault
(textbook-minimum answer misses paper's novel single-binary-operator
result).  L2 autonomously identified this as shape-measuring weakness
in R1 and R2 and drafted M10.2 + M10.3 tightening proposals in the
Cycle #10 cycle-log carry-over section.  Cycle #11 operationalizes
those proposals: port the tightening clauses into the rubric and
re-apply to the same X.  If R1 and R2 both drop to ≤ 1, M9.4
empirical loop closes full-H0; if partial, closes partial-reduced.

Cycle #11 additionally runs a fresh A/B on a fresh EML-domain TASK.md
for normal Δ measurement under the post-tightening rubric.  A fresh
TASK is used (not re-using Cycle #10's TASK.md) to keep in-cycle
A/B independent from the re-test — no accidental leakage of
Cycle-#10 experience into Cycle-#11 A/B.

## Rubric-blindness + falsification-blindness + paper-blindness

Cycle #10 prohibition set + M10.2/M10.3/M10.5 extensions:

```
grep -iE "band[ -]?[0-9]|sublemma separation|named sublemma|\
tabular enumeration|orthogonal example|parametric impossibility|\
structural impossibility|cite each trace artifact|\
gap.?closure.?check|closure.?artefact|open.?questions.? section|\
enumeration locus|verifier_identity|\
falsif|planted|probe|X-?ARGUMENT|authorial-identity|\
rubric-falsification|shape-measuring|reasoning-measuring|\
odrzywolek|arXiv.*2603|single operator.*constant|\
eml|sheffer|\
motivation.?answer.?consistency|sublemma.?discharge|\
named.?precedent|answer.?shape|per.?sublemma" \
     docs/meta-audit/cycle-11/TASK-draft.md
```

Prose below produces zero match outside the grep alternation itself.

## Suggested content shape

Same Cycle #1 / Cycle #10 format, different primitive configuration
for task freshness without changing domain.  L2 may pick a different
primitive subset or reframe the central question as a "what is the
smallest basis" question; the domain remains minimal-generating-
basis for elementary calculator functions.

---

### Sketch: Minimal Generating Basis — Cycle #11 variant

Consider the following primitive set:

- **Constants:** π, e, i, −1, 1, 2 (also accept input variables x, y)
- **Unary:** exp, ln, reciprocal, sqrt, square, negate, halve,
  sigmoid, sin, cos, tan, arcsin, arccos, arctan, sinh, cosh, tanh,
  arsinh, arcosh, artanh
- **Binary:** +, −, ×, ÷, log_x(y), pow, mean, hypot

Many of these are redundant.  Central question: *what is the
smallest generating basis from which every primitive above can be
reconstructed as a finite composition?*

**Deliverable:** a self-contained argument at `task/ARGUMENT.md`
covering:

1. Motivation for the reduction, from first principles.
2. A systematic reduction procedure.
3. A sequence of progressively smaller configurations with
   intermediate stopping points.
4. The minimal configuration reached, with exact form.
5. Verification strategy.
6. Worked examples reconstructing ≥ 3 originals.
7. Open questions and limitations.

Constraints unchanged from Cycle #10.

---

## L2 ROOT adoption guidance

L2 may:

- Adopt this TASK verbatim (recommended — continuity with Cycle #10).
- Reframe the primitive set (e.g., drop log_x(y) and hypot) to
  produce a slightly different problem shape.

L2 must NOT:

- Change the domain (EML continuity binding for this WIP).
- Mention any rubric axis or band criterion.
- Hint at X / probe / falsification test.
- Mention paper identity.
- Hint at single-binary-plus-single-constant novel answer.

## M10.x experimental protocol (L2 binding)

1. Pre-cycle commit: ports M10.2 R1 tightening + M10.3 R2 tightening
   into `docs/research/eml-paper/judgment-rubric.md` as band-3
   clarification clauses, following M8.1/M8.2 port pattern.
   `cycle-11-pre` tag applied.
2. Falsification re-test (M10.5): L2 re-scores
   `docs/research/eml-paper/cycle-10/X-ARGUMENT.md` under the
   post-tightening rubric.  Output: `cycle-11/X-JUDGMENT-v2.md`
   with per-axis band + rubric-text citation + evidence-from-X.
   Explicitly flags per axis what changed from Cycle #10 v1.
3. Normal Cycle #11 A/B: L2 runs A and B against Cycle #11 TASK.md
   per §6.7 cycle flow.  `cycle-11/JUDGMENT.md` authored with
   §5a/§5b/§5c steps completed.  proof-auditor covers A, B, and
   the re-test X-row.
4. Retrospective Cycle #10 A/B: L2 re-scores `cycle-10/A-ARGUMENT.md`
   and `cycle-10/B-ARGUMENT.md` under Cycle #11 rubric.  Output:
   `cycle-10/JUDGMENT-v2.md`.
5. Falsification-report-v2: `cycle-11/falsification-report-v2.md`
   records per-axis v1→v2 shift (focused on R1/R2) and global
   closure verdict (Full-H0 / Partial-reduced-1-of-6 / Ineffective)
   per procedure.
6. Cleanup: §6.7 step 9 forensic (6th consecutive cycle).
7. Push to origin/main.

## Measurement the cycle enables

| Measurement | Interpretation |
|-------------|----------------|
| X R1 = ≤ 1 AND R2 = ≤ 1 in v2 | Full-H0 closure; rubric covers all 6 shape axes as reasoning-measuring |
| X R1 = ≤ 1 only | Partial-reduced (1 of 6 shape); R2 tightening needs redesign |
| X R2 = ≤ 1 only | Partial-reduced (1 of 6 shape); R1 tightening needs redesign |
| X R1 = ≥ 2 AND R2 = ≥ 2 in v2 | Ineffective; both tightening ports did not land |
| Cycle #11 A/B Δ ≈ +1 | Post-tightening EML baseline matches Cycle #10 (noise level) |
| Cycle #11 A/B Δ ≫ +1 or ≪ +1 | Domain-side or tightening-side anomaly; investigate |
| Cycle #10 A/B retrospective shift | Separate measurement — any A/B band movement under tightened rubric |

## This draft's status

L1 reference material.  Freezes at cycle-11 pre-cycle commit.  The
actual cycle-11 TASK.md is committed by L2 ROOT.
