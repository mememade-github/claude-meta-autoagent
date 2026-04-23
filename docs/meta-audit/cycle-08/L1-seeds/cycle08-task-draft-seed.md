# Cycle #8 TASK-draft (L1 reference)

> L1 drafts this as **reference**, not mandate.  L2 ROOT holds TASK
> authorship autonomy (§6.7 cycle pre-cycle).  This draft demonstrates
> the task-prompt-discipline-v1 rubric-blind style and suggests a
> domain continuation for M7.1 controlled measurement.

## Why this draft exists

Cycle #7 TASK.md exposed rubric band-3 criteria to the agents and
produced entangled measurement (M7.1).  Cycle #8 must measure the
same underlying A/B structural gap under a clean (rubric-blind) TASK
to isolate architectural effect from prompt-hint-leakage effect.

Task domain should be **structurally similar** to Cycle #7 (non-
positive-verdict TRS questions) so that task-difficulty is held
approximately constant — the only controlled variable is prompt
discipline.

## Rubric-blindness check (self-applied to this draft)

```
grep -iE "band[ -]?[0-9]|sublemma separation|named sublemmas|tabular enumeration|orthogonal examples|parametric impossibility|structural impossibility|cite each trace artifact" \
     docs/meta-audit/cycle-08/TASK-draft.md
```

Expected: zero matches (this draft itself complies with the
discipline).  The sentence immediately above is a grep test-string;
the grep alternation is about testing, not teaching.

## Suggested content shape

The actual TASK.md (which L2 commits) should use language like the
following sketch.  **This is a sketch of tone and structure, not a
verbatim template.**  L2 adjusts the rule set and question list.

---

### Sketch: a small TRS with undecided properties

Let T be a term rewriting system over the signature
Σ = { f/2, g/1, h/1, a/0, b/0 } with rewrite rules:

```
R1:  f(x, g(y))    →  g(f(x, y))
R2:  h(f(x, y))    →  f(h(y), h(x))
R3:  g(h(a))       →  h(g(b))
R4:  f(a, b)       →  g(a)
```

Assume the standard left-to-right match semantics.  Positional
conventions and substitution are as in Baader & Nipkow §3 (referenced
only; not reproduced here).  `→*` denotes reflexive-transitive
closure of `→`.

**Banned identifiers.**  Do not use the following primitives or
names in your proofs; they are reserved for baseline materials:
(list populated from `.refine/banned-identifiers.txt` at cycle-08
pre-cycle commit).

**Deliverable.**  A single Markdown file named `ARGUMENT.md`
answering the three questions below with justification.

---

### Question 1 — Confluence

Decide whether T is confluent.  If it is confluent, justify.  If it
is not confluent, exhibit a concrete divergent pair: find terms
`s`, `t₁`, `t₂` such that `s →* t₁` and `s →* t₂` but `t₁` and `t₂`
have no common reduct.  Provide the reduction sequences explicitly.

### Question 2 — Weak Normalisation

Decide whether T is weakly normalising.  If yes, provide a strategy
(or existence argument) ensuring every term has a normal-form
reduction.  If no, exhibit a term with no normal form.

### Question 3 — Strong Normalisation

Decide whether T is strongly normalising.  If yes, justify with a
well-founded measure.  If no, exhibit a concrete infinite reduction
sequence — describe its shape and prove it does not terminate.

### Constraints on the deliverable

- A single file `ARGUMENT.md`.
- Use only terms and concepts defined above or in the Baader-Nipkow
  reference.  Banned primitives and identifiers listed in
  `.refine/banned-identifiers.txt` are excluded.
- If you use `/refine` or equivalent iteration affordance and your
  iteration has a second draft, record your iteration on disk
  under `attempts/` with the first draft, any evaluator reports,
  and the final deliverable.
- Do not modify `projects/a/` if you are A.
- Push completed work to origin/main at exit.

---

## What this draft deliberately omits

- No mention of how many sublemmas the proof should have.
- No mention of whether examples should be tabulated.
- No mention of how many examples should be provided.
- No mention of what the grader rewards in open-questions sections.
- No reference to R-axes or bands.
- No instruction to "disclose" anything structural beyond answering
  the three questions.

The agent produces whatever shape its architecture yields.  The
rubric is applied to that shape by the grader, not pre-announced
to the agent.

## L2 ROOT adoption guidance

L2 may:

- Adopt this TASK verbatim.
- Adjust the rule set to produce different specific answers (e.g.,
  change R3 so that T becomes confluent under a different
  argument, or add R5 to produce a different SN witness).
- Swap to a different non-positive-verdict domain entirely (e.g.,
  decidability-of-problem with termination-of-canonical-search
  obligation) provided it remains rubric-blind.

What L2 must NOT do:

- Add rubric-shaped instructions to the prompt.
- Tell the agent to "present in tabular form" or "separate named
  sublemmas".
- Mention band-3 criteria in any form, even obliquely.

## Measurement the cycle enables

Under clean prompt + non-positive-verdict task:

| Measurement | Expected | If actually measured |
|-------------|----------|----------------------|
| In-cycle Cycle #8 Δ | ≥ +5 (close to retrospective +6) | Prompt discipline effective |
| In-cycle Cycle #8 Δ | ≈ +3 (same as Cycle #7 leaky) | Discipline ineffective; re-examine |
| In-cycle Cycle #8 Δ | +1 to +2 | Other confound dominates |

Retrospective cycle-7 Δ under cycle-8 rubric: target ≥ +6.
(If cycle-8 rubric is unchanged from cycle-7, the retrospective
confirms zero drift; if cycle-8 further tightens, retrospective
measures the next step.)

## This draft's status

L1 reference material.  Freezes at cycle-08 pre-cycle commit.  The
actual cycle-08 TASK.md is committed by L2 ROOT (same commit or
subsequent).  Both files stay in the tree — the draft as L1 audit
trail, the TASK as the operative prompt.
