# Retrospective Re-score Procedure

> ROOT-owned procedure codifying the practice pioneered at Cycle #7
> close: re-score the immediately-prior cycle's A and B deliverables
> under the current cycle's rubric.  Addresses the confounding of
> rubric effect, task-design effect, and prompt-hint-leakage in
> in-cycle measurement.
>
> Ported Cycle #8 pre-cycle from L1-seed
> `docs/meta-audit/cycle-08/L1-seeds/retrospective-rescore-seed.md`.

## Why

In-cycle measurement mixes three effects that must be separated to
credit a capability claim:

1. **Rubric effect** — the tightened rubric's intrinsic discriminative
   power on fixed deliverables.
2. **Task-design effect** — the current cycle's task pushing A toward
   or away from ceiling.
3. **Prompt-hint leakage (M7.1)** — the TASK.md prompt inadvertently
   teaching A band-3 patterns.

Retrospective re-score holds deliverables and task constant (both
come from cycle-(N-1)) while varying only the rubric.  The Δ obtained
is pure rubric effect.

Compare:

- In-cycle cycle-N Δ = rubric_effect(cycle-N) + task_effect(cycle-N)
  + leakage_effect(cycle-N TASK)
- Retrospective cycle-(N-1) under cycle-N rubric Δ
  = rubric_effect(cycle-N) + task_effect(cycle-(N-1))
  + leakage_effect(cycle-(N-1) TASK)

The difference identifies task effect (since leakage is a cycle-
specific artefact, controllable via task-prompt-discipline.md).

## When to run

**Mandatory at every cycle close, starting Cycle #8.**

- If cycle-N's pre-cycle commit modifies any R-axis band text or
  adopts a new band-criterion tightening: re-score cycle-(N-1)
  under the new rubric.
- If cycle-N's rubric is unchanged from cycle-(N-1): re-score
  cycle-(N-1) anyway to confirm zero rubric-effect drift and
  establish the baseline procedure as always-on.

**Skip only** when there is no cycle-(N-1) (i.e., cycle-1); record
the skip in cycle-log with "N/A — first cycle".

## Inputs

- Cycle-(N-1)'s A-ARGUMENT.md (frozen — no edits)
- Cycle-(N-1)'s B-ARGUMENT.md (frozen — no edits)
- Cycle-(N-1)'s JUDGMENT.md (read-only reference for v1 scores)
- `docs/research/eml-paper/judgment-rubric.md` (cycle-N current state)
- Any new rubric-axis tightening seeds ported in cycle-N pre-cycle

Cycle paths: prior cycles (#1–#7) live under
`docs/research/eml-paper/cycle-NN/`; from Cycle #8 onward, primary
artefacts may live under `docs/meta-audit/cycle-NN/` (the
retrospective filing convention adapts to the cycle being rescored).

## Procedure

1. **Freeze deliverables.** Confirm `git log -- <prior-cycle-path>/
   A-ARGUMENT.md` shows no commits after cycle-(N-1)'s close tag.
   If any, this is a protocol violation; halt and investigate.

2. **Apply current rubric.** Score each of the 10 axes for A and
   for B under cycle-N's rubric text.  For each axis, record:
   - v1 score (from cycle-(N-1)/JUDGMENT.md)
   - v2 score (current re-score)
   - Justification when v2 ≠ v1, citing the specific rubric
     clause that moved the score.

3. **Produce JUDGMENT-v2.md.** Commit to
   `docs/meta-audit/cycle-(N-1)/JUDGMENT-v2.md` with frontmatter:

   ```yaml
   ---
   cycle_rescored: cycle-(N-1)
   rescored_under: cycle-N rubric (at commit <sha>)
   original_judgment: <path-to-cycle-(N-1)>/JUDGMENT.md
   rescore_authored_in: cycle-N
   status: retrospective
   ---
   ```

4. **Tabulate per-axis comparison.** Table of shape:

   | Axis | A v1 | A v2 | B v1 | B v2 | Movement | Rubric clause |
   |------|------|------|------|------|----------|----------------|
   | R1 | 3 | 3 | 3 | 3 | — | unchanged |
   | R2 | 3 | 2 | 3 | 3 | A −1 | band-3-tightening §R2 |
   | ... | ... | ... | ... | ... | ... | ... |

5. **Delta comparison.**

   ```
   v1 Δ: B_v1 − A_v1 = ...
   v2 Δ: B_v2 − A_v2 = ...
   Movement: v2 Δ − v1 Δ = ... (pure rubric effect on prior cycle)
   ```

6. **Narrative.** 1-2 paragraphs identifying which axes moved,
   which didn't, and why this matches or diverges from the
   current cycle's in-cycle measurement.

7. **Cross-compare with in-cycle cycle-N.** One table:

   | Measurement | A | B | Δ | Leakage attributable |
   |-------------|---|---|---|----------------------|
   | Cycle-N in-cycle | ... | ... | ... | (compute) |
   | Cycle-(N-1) retrospective under cycle-N rubric | ... | ... | ... | 0 (past TASK did not know cycle-N rubric) |
   | Gap | — | — | — | — |

   The gap (if positive, i.e., retrospective Δ > in-cycle Δ) is
   attributable to prompt-hint leakage in cycle-N's TASK.  The
   task-prompt-discipline forward guardrail should reduce
   this gap in future cycles.

## Storage

`JUDGMENT-v2.md` lives in `docs/meta-audit/cycle-(N-1)/`.  It is
produced by cycle-N's workflow but filed under the cycle it
rescores, because the content is *about* cycle-(N-1)'s deliverables.
For cycles rescored that originally lived under
`docs/research/eml-paper/cycle-NN/`, the v2 file lives under the
parallel `docs/meta-audit/cycle-NN/` to keep the meta-audit layer
visually distinct from the original cycle artefacts.

The cycle-N cycle-log entry must include a one-line summary of the
retrospective result and the path.

## Scientific purpose

Without retrospective re-score, a cycle's Δ is an entangled
measurement.  With retrospective, the entanglement is partially
unwound:

- If retrospective Δ > in-cycle Δ: current TASK is leaky — apply
  task-prompt-discipline tighter.
- If retrospective Δ < in-cycle Δ: current TASK is harder (pushes
  A further below ceiling) — rubric tightening + harder task
  stack synergistically.
- If retrospective Δ ≈ in-cycle Δ: rubric effect is dominant and
  task effect is minimal — measurement is clean.

Across many cycles, the retrospective series itself is informative:
a monotonic increase in retrospective Δ indicates the rubric is
becoming progressively more discriminative (strengthening the
experimental apparatus); a plateau indicates rubric saturation
relative to the deliverables (new tightening ideas needed).

## What retrospective does NOT do

- It does not test new rubric changes' task-interaction (that
  requires next-cycle in-cycle with clean TASK).
- It does not recover cycles whose deliverables were produced
  under leaky TASKs (those cycles' *in-cycle* measurements
  remain entangled; only their retrospective-from-future-cycle
  measurements are clean).
- It does not adjudicate between rubric drift ("the rubric is
  now tighter on everyone") and genuine capability drift ("A has
  slipped").  Cycle-(N-1) deliverables are fixed; only cycle-N
  rubric varies in this comparison.  Longitudinal comparison
  across many retrospectives is needed for capability-drift
  questions.

## Evolution

Edit this procedure when:

- A new confound is identified beyond rubric × task × leakage.
- The three-way comparison table is insufficient to isolate
  some effect observed in later cycles.
- Rubric evolution pauses (no tightening for several cycles) and
  the retrospective procedure becomes ritual; consider demoting
  to "only when rubric changes".
