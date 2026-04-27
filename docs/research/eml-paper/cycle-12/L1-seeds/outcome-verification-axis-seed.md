# Outcome Verification Axis v1

> Defines the **parallel measurement dimension** for outcome correctness,
> reported alongside (not inside) the existing R1-R10 rubric.
>
> Companion document: `procedures/outcome-task-template-v1.md` (full
> procedure including schema and verifier contract).

## Axis definition

| Property | Value |
|----------|-------|
| Name | Outcome verification |
| Dimension | Parallel to R1-R10 (NOT a new R-axis) |
| Score | per-question PASS / FAIL / MISSING + ratio (0.0 to 1.0) |
| Range | not on the 30-point rubric scale; reported as ratio + count |
| Source of truth | L2-ROOT-only `ground-truth.json` (see procedure §4) |
| Verifier | `scripts/meta/oracles/outcome-verifier.py` |
| Reporting locus | JUDGMENT.md §6 "Outcome verification" |

## Why parallel, not embedded as R11

Adding an outcome axis to R1-R10 would conflate two distinct measurements:
- **Rubric (R1-R10):** how well-structured is the argument.
- **Outcome:** does the conclusion match reality.

A deliverable can score high on rubric (well-organized, motivated,
disclosed circularity) and FAIL outcome (wrong conclusions reasoned
correctly from wrong premises).  It can score low on rubric (sketchy,
under-explained) and PASS outcome (right answer for unclear reasons).
These four quadrants are independently informative; collapsing them into
one number loses the signal.

| Rubric \ Outcome | Outcome PASS | Outcome FAIL |
|------------------|--------------|--------------|
| Rubric high | rigorous reasoning + correct (ideal) | rigorous reasoning to wrong conclusion (informative — premise error or structural blind spot) |
| Rubric low | shape-poor + correct (lucky / shortcut) | shape-poor + wrong (catastrophic) |

## Scoring

For each question in the cycle's outcome battery:

```
PASS  if agent.answer matches ground-truth.expected_answer per match_mode
FAIL  if agent.answer differs (and not missing)
MISSING  if outcome.json lacks an entry for the question id, or .answer is null
```

Aggregate:
- `pass_count`, `fail_count`, `missing_count`, `total`
- `ratio = pass_count / total`

`MISSING` is reported separately from `FAIL` so that "agent didn't try" is
distinguishable from "agent got it wrong".

## Δ definition

For Cycle #N with sub-projects A and B:

```
Δ(rubric, B − A) = total_rubric_B − total_rubric_A    (in points, range −30 to +30)
Δ(outcome, B − A) = ratio_B − ratio_A                  (in [-1, +1])
```

Both reported in JUDGMENT §6.  Sign agreement and magnitude correlation
across cycles is the longitudinal H1 / H0 evidence.

## Reporting requirements

JUDGMENT.md §6 MUST include:

1. Per-agent total rubric score (existing).
2. Per-agent outcome ratio + pass/fail/missing counts.
3. Per-agent link to `cycle-NN/outcome-report-<a|b>.json`.
4. `Δ(rubric)` and `Δ(outcome)` explicit values + same-direction / opposite-
   direction note.
5. Per-question table or summary identifying any **anchor question failures**
   (catastrophic deliverable issue).
6. H1 / H0 reading for this single cycle (the parent WIP closes on the H1 /
   H0 verdict aggregated across the cycle's data).

## Auditor coverage

`proof-auditor` is OPTIONAL on the outcome dimension because the verifier
is mechanical (no model judgment).  The auditor should still verify:
- `outcome.json` schema validity.
- Ground-truth file integrity (no tampering).
- That JUDGMENT §6 numbers match `outcome-report-*.json` outputs.

If a future Q5.x branch introduces semantic outcome questions (free-text
answers requiring judgment), the auditor's role expands.

## Limitations (named at v1)

1. **Lucky correctness vs reasoned correctness** — outcome ratio cannot
   distinguish "agent guessed correctly" from "agent reasoned to the
   answer".  Pairing with rubric helps (rubric measures reasoning shape)
   but does not eliminate.
2. **Question selection bias** — L1 author of ground-truth selects which
   structural facts to query.  Selection can favor architectures that
   excel on certain question types.  Mitigation: 50%+ anchor questions
   (any architecture should pass these) + diverse discriminative.
3. **Single source authority** — ground truth is L1-derived from one
   paper.  Multi-source ground truth (cross-paper consensus) would be a
   v2 extension.
4. **Forward-only** — cannot retroactively score Cycles #1-#11 because
   outcome batteries did not exist then.

## v1 stability

This v1 stays in force for the duration of the parent WIP
(`task-20260427-q5-outcome-grounded`).  Closure of that WIP triggers
either v1 freeze (if WIP closes successfully) or v2 redesign (if WIP
discards).
