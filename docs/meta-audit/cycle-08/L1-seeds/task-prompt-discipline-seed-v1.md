# TASK-Prompt Discipline — v1

> ROOT-owned reference addressing **M7.1 (prompt-hint-leakage)** surfaced
> at Cycle #7 close.  When the agent-facing TASK.md describes the rubric
> criteria it will be graded on, the agent can target those patterns
> directly, bypassing the architectural property under test.
> Result: in-cycle Δ underestimates the rubric's true discriminative
> power.

## The leak pattern (Cycle #7 evidence)

Cycle #7 TASK.md exposed Cycle #7 rubric's tightened band-3 criteria
(named sublemma separation, tabular auditability, ≥4 orthogonal
examples, structural/parametric impossibility disclosure).  Both A
(single-shot) and B (evolvable) read the TASK and produced deliverables
targeting those patterns.  A compensated by producing 3 named sublemmas
+ 4 examples with a coverage table + structural open questions despite
the A architecture having no iteration affordance.

Measurement:

| Measure | Δ |
|---------|---|
| In-cycle Cycle #7 (leaky TASK) | +3 |
| Retrospective Cycle #6 (same rubric, TASK-unchanged, no leak) | +6 |

Gap = +3 attributable to prompt-hint leakage.  A under clean prompt
scored 23 / 30 (Cycle #6 retrospective); A under leaky prompt scored
26 / 30 (Cycle #7 in-cycle).

## Principle

A TASK.md prompt describes **what to reason about** — the rule set,
the questions, the constraint list, the notational conventions.  It
does NOT describe **how the reasoning will be graded** — the rubric
axes, the band criteria, the scoring patterns.

The agent is evaluated *on* the rubric, not *by* the rubric.  The
rubric is the grader's tool, not the subject's tool.  Exposing the
rubric short-circuits the capability under test.

## Prohibited patterns in TASK.md

The following strings (case-insensitive) and their close paraphrases
MUST NOT appear in a TASK.md prompt intended for A/B agent execution:

| Prohibited string / pattern | Reason |
|-----------------------------|--------|
| `band 3`, `band-3`, `band N` | Names the rubric banding directly. |
| `sublemma separation`, `named sublemmas`, `separate sublemmas` | R2 band-3 criterion paraphrase. |
| `tabular enumeration`, `tabulate your`, `present as a table` | R3 band-3 criterion. |
| `orthogonal examples`, `orthogonal failure modes`, `≥ N examples` | R7 band-3 criterion. |
| `parametric impossibility`, `structural impossibility`, `coefficient contradiction` | R8 band-3 criterion. |
| `cite each trace artifact`, `iteration-N closure` | R10 band-3 criterion. |
| Any direct phrasing of a rubric-axis band threshold | Equivalent leakage. |

Domain-inherent terminology is acceptable even when it overlaps
superficially.  Example: a TRS task may ask "find a divergent
reduction pair" — this describes the mathematical object, not a
rubric criterion, and is permitted.  Whereas "separate your proof
into named sublemmas per tool" imposes a proof-presentation structure
that mirrors R2 band 3 and is prohibited.

## Test before committing TASK.md

```bash
grep -iE "band[ -]?[0-9]|sublemma separation|named sublemmas|tabular enumeration|orthogonal examples|parametric impossibility|structural impossibility|cite each trace artifact" \
     docs/meta-audit/cycle-NN/TASK.md
```

Expected: zero matches.  If any match appears, rewrite the TASK
prompt in structural-only language.

## What the TASK may legitimately include

- The **rule set** (TRS rewrite rules, axiom schema, primitive
  definitions).
- The **question list** (Q1, Q2, Q3 with precise verdict forms
  requested: "decide confluent / non-confluent with witness",
  "decide SN / WN / NOT SN with witness").
- The **convention declarations** (notation, term representation,
  evaluation strategy assumed, banned identifier list).
- The **constraint list** (paper-leak exclusion, oracle-output
  format if any, trace persistence affordance).
- Domain-inherent success criteria ("provide a ground divergent
  pair for non-confluence").

## What the TASK may NOT include

- Any sentence describing the rubric axes or their bands.
- Any sentence prescribing proof structure, presentation format,
  or deliverable shape that mirrors a band-3 criterion.
- Any sentence telling the agent what the grader will count.
- Any reference to R-axis numbers (R1–R10) by identifier.

## Relationship to agent autonomy

This discipline constrains the **TASK prompt author** (L2 ROOT at
cycle-N pre-cycle commit time), not the agent.  The agent remains
free to produce whatever structure its architecture naturally
yields.  B (evolvable) will often produce rubric-aligned structure
spontaneously because its architecture encodes the reasoning
patterns the rubric rewards — this is the *capability under test*.
A (frozen Karpathy baseline) will produce whatever structure a
single-shot run yields — this is the *baseline under comparison*.

The delta between A and B should reflect the architectural
difference, not the prompt's inadvertent teaching.

## Relationship to R10

R10 (iteration depth) measures architectural iteration affordance.
Prompt leakage is a separate phenomenon: even without iteration
leakage, a single-shot agent can be taught to mimic band-3 patterns
if the prompt describes those patterns.  M7.1 is about *all* axes,
R10 included.  The R10-specific M6.3 codification (evaluator-report
substitution) does not address prompt leakage; it addresses a
different closure-evidence question.

## Evolution

Edit this file when:

- A new cycle surfaces a leakage pattern not covered above
  (e.g., an R-axis tightened in the future with a vocabulary not
  listed in the prohibited table).
- A prohibited pattern turns out to be essential domain terminology
  for a specific cycle (document the exception and its mitigation).

Do not edit this file to loosen the discipline for a specific cycle.
If a cycle's design requires rubric-shaped prompt language, use
retrospective-rescore instead to isolate rubric effect.

## Relation to retrospective re-score

Retrospective re-score (`docs/meta-audit/procedures/retrospective-
rescore.md`) is the second tool addressing the same problem from
the opposite direction: prompt discipline keeps in-cycle
measurement clean going forward; retrospective re-score recovers
clean measurement from past cycles where prompt discipline was not
in effect.  Both are needed; both are complementary.
