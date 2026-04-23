# Cycle #9 TASK-draft (L1 reference)

> L1 drafts this as **reference**, not mandate.  L2 ROOT holds TASK
> authorship autonomy (§6.7 cycle pre-cycle).  This draft demonstrates
> the task-prompt-discipline rubric-blind style, extends the Cycle #8
> prohibition list with M8.1/M8.2/M8.3 leak-words, and suggests a
> structurally-similar-but-distinct TRS domain for controlled M8.3
> reproducibility measurement.

## Why this draft exists

Cycle #8 validated M7.1 (clean prompt recovers full rubric
discriminative power: Δ = +6 matching Cycle #6 retrospective).
Cycle #9 tests M8.3: whether the R10 M6.3 (c) closure-artefact
path — first exercised at Cycle #8 via ROOT-authored
`B-gap-closure-check.json` — is reachable **agent-spontaneously**
in Cycle #9 without L1 or L2 scaffolding.

The task domain remains a small TRS with 3 correctness obligations
for continuity with Cycle #8.  The signature and rules differ to
keep the specific answers fresh and to prevent B memoising Cycle #8
artefacts.

## Rubric-blindness check (self-applied to this draft)

Prohibited patterns include Cycle #8 `task-prompt-discipline.md`
set plus the M8.1/M8.2/M8.3 extensions:

```
grep -iE "band[ -]?[0-9]|sublemma separation|named sublemma|tabular enumeration|orthogonal example|parametric impossibility|structural impossibility|cite each trace artifact|gap.?closure.?check|closure.?artefact|open.?questions.? section|enumeration locus|verifier_identity" \
     docs/meta-audit/cycle-09/TASK-draft.md
```

The single match in this file is the grep alternation itself
(inside the fenced block above, which is about the test, not the
prompt); the operative prompt section below contains zero matches.

Additional M8.3-specific prohibition: the TASK must NOT instruct
any iterating agent to produce a closure-verification JSON,
citation-schema artefact, or structured iteration-closure record.
If the agent chooses to produce one, that is agent autonomy —
scaffolding-free.

## Suggested content shape

The actual TASK.md (which L2 commits) should use language like the
following sketch.  **This is a sketch of tone and structure, not a
verbatim template.**  L2 adjusts the rule set and question list.

---

### Sketch: a small TRS with undecided correctness properties

Let T be a term rewriting system over the signature
Σ = { c/2, d/1, e/1, p/0, q/0 } with rewrite rules:

```
S1:  c(x, d(y))    →  d(c(x, y))
S2:  e(c(x, y))    →  c(e(y), e(x))
S3:  d(e(p))       →  e(d(q))
S4:  c(p, q)       →  d(p)
S5:  e(e(x))       →  c(x, d(p))
```

Assume standard left-to-right match semantics.  Positional
conventions and substitution are as in Baader & Nipkow §3 (ref only).
`→*` denotes reflexive-transitive closure of `→`.

**Banned identifiers.**  As recorded in `.refine/banned-identifiers.txt`
at cycle-09 pre-cycle commit.

**Deliverable.**  A single Markdown file named `ARGUMENT.md`
answering the three questions below with justification.

---

### Question 1 — Confluence

Decide whether T is confluent.  If confluent, justify.  If not,
exhibit a concrete divergent pair: find terms s, t₁, t₂ such that
s →* t₁ and s →* t₂ with no common reduct, and provide the
reduction sequences explicitly.

### Question 2 — Weak Normalisation

Decide whether T is weakly normalising.  If yes, provide a strategy
or existence argument ensuring every term has a normal-form
reduction.  If no, exhibit a term with no normal form.

### Question 3 — Strong Normalisation

Decide whether T is strongly normalising.  If yes, justify with a
well-founded measure.  If no, exhibit a concrete infinite reduction
sequence — describe its shape and prove it does not terminate.

### Constraints on the deliverable

- A single file `ARGUMENT.md`.
- Use only terms and concepts defined above or in Baader & Nipkow.
  Banned primitives / identifiers in `.refine/banned-identifiers.txt`
  are excluded.
- If your iteration produces a second draft, record your iteration
  on disk under `attempts/` with the first draft, any evaluator
  reports, and the final deliverable.
- Do not modify `projects/a/` if you are A.
- Push completed work to origin/main at exit.

---

## What this draft deliberately omits

- No mention of how the proof should be structured.
- No mention of whether examples should be tabulated.
- No mention of parametric / structural / "any rule of the form"
  framings as a grading concern.
- No reference to R-axes or bands.
- No mention of JSON artefacts, closure schemas, or iteration-
  evidence record shapes.
- No instruction about iteration count or what evaluator reports
  should contain.

The agent produces whatever shape its architecture yields.  The
rubric is applied to that shape by the grader, not pre-announced.

## L2 ROOT adoption guidance

L2 may:

- Adopt this TASK verbatim.
- Adjust the rule set to produce different specific answers.
- Swap to another non-positive-verdict TRS or small abstract
  rewriting problem, provided it remains rubric-blind.

L2 must NOT:

- Add rubric-shaped instructions to the prompt.
- Instruct agents to produce closure-verification JSONs, tabular
  enumerations, named sublemmas, or structural parametric
  disclosures.
- Mention any rubric axis or band criterion in any form.

## M8.3 experimental protocol (L2 binding)

Cycle #9 measures M6.3 (c) reproducibility per
`procedures/closure-artefact-reproducibility.md`.  L2 ROOT
operational constraints during Cycle #9:

1. L2 ROOT does not author `cycle-09/B-gap-closure-check.json` on
   B's behalf.  If B produces one in its own iteration stream, L2
   ROOT may verify (jsonschema.validate, field checks) it in
   JUDGMENT.md §5c, but must not author it.
2. L2 ROOT does not stage closure-artefact seeds in A or B
   `/tmp/` or working directories.
3. If B does not produce a closure-artefact, R10-B caps at band 2
   (one substantive iteration with gap closure), and the JUDGMENT
   records reproducibility tag `not-applicable` per the procedure
   file.

## Measurement the cycle enables

| Measurement | Interpretation |
|-------------|----------------|
| B produces schema-conformant closure-artefact spontaneously | M6.3 (c) reproducible agent-spontaneously.  R10-B = 3. |
| B does not produce closure-artefact | M6.3 (c) is scaffolding-dependent.  R10-B ≤ 2; future cycles revise expectations. |
| B produces artefact but with ROOT-ish `verifier_identity` | Partial reproducibility; flag as scaffolding-assisted in JUDGMENT. |
| Cycle #9 Δ ≥ +5 under clean TASK | Previous 3-cycle discrimination pattern holds under continued clean prompt. |
| Cycle #9 Δ < +3 | M7.1-clean is not a stable attractor; re-examine for new confound. |

Retrospective cycle-08 Δ under cycle-09 rubric: if the R3 locus and
R8 labeling criteria are ported, the retrospective isolates their
intrinsic effect separately from the M8.3 reproducibility test.

## This draft's status

L1 reference material.  Freezes at cycle-09 pre-cycle commit.  The
actual cycle-09 TASK.md is committed by L2 ROOT (same commit or
subsequent).  Both files stay in the tree — the draft as L1 audit
trail, the TASK as the operative prompt.
