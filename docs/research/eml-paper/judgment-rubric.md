# Judgment Rubric — A/B ARGUMENT.md Scoring

> Self-contained ROOT-only reference. Use together with `paper-analysis.md` in the same
> directory. This file must never be mounted into A/B containers — it reveals the target
> structure.

## Who uses this

- **Input**: the ARGUMENT.md produced by an A or B agent after a cycle task.
- **Grader**: the ROOT Agent (Level 2). A and B never see this file.
- **Output**: a per-criterion score written to `docs/research/eml-paper/cycle-NN/JUDGMENT.md`.

## Rubric structure

- **R1–R8** each score 0–3 → 24 points possible.
- **R9** is binary: 0 (not reached) or 3 (reached) → 3 points possible.
- **R10** scores 0–3 → 3 points possible.  Added at Cycle #4 pre-cycle to
  surface an iteration-sensitive axis (R1–R9 ceilinged at 27/27 across
  Cycles #2 and #3 while B's iteration activity left no rubric trace).
- **Total**: 30 points.

Missing criteria score 0. Partial credit within 0–3 ranges is allowed for
R1–R8 and R10.

## Criterion definitions

### R1 — Motivation (0–3)

Does the argument explain why a reduction to a single primitive might exist?

| Score | Evidence |
|---|---|
| 0 | No motivation given. |
| 1 | Weak, generic "reducing complexity is good" phrasing. |
| 2 | Adequate analogy or partial precedent (e.g. "polynomial basis"). |
| 3 | Clear structural precedent — Boolean universality via a single two-input gate, or an equivalent named example (combinators, one-instruction computers, Wolfram's single axiom), argued from first principles. |

### R2 — Method design (0–3)

Does the argument propose a systematic, verifiable search/reduction procedure?

| Score | Evidence |
|---|---|
| 0 | Pure guessing; no procedure. |
| 1 | Unsystematic trial and error without a stopping criterion. |
| 2 | Systematic search proposed but the verification step is hand-waved. |
| 3 | Explicit procedure with verification — e.g. iterative ablation combined with a numeric substitution sieve (evaluate candidate and target at algebraically independent transcendental inputs, compare), or an equivalent scheme that can distinguish true identities from coincidence. |

### R3 — Progressive minimization (0–3)

Does the argument exhibit a sequence of progressively smaller sufficient configurations,
each justified?

| Score | Evidence |
|---|---|
| 0 | No intermediate configurations. |
| 1 | 1–2 intermediate steps without real justification. |
| 2 | 3+ steps with brief justification. |
| 3 | A coherent reduction sequence with each step motivated — e.g. dropping negation/reciprocal once a non-commutative operator provides inversion; collapsing named constants into functions; moving from lower to higher hyperoperation ranks. |

### R4 — Final basis structure (0–3)

Does the argument converge on a correctly-shaped minimal basis?

| Score | Evidence |
|---|---|
| 0 | The shape of the answer is not even specified. |
| 1 | Claims multiple binary operators are required. |
| 2 | Reduces to ≤ 2 binary operators, or 1 operator plus several constants. |
| 3 | Exactly one binary operator paired with exactly one distinguished constant (or an equivalent variant that uses a single terminal). |

### R5 — Exact form (0–3)

Does the argument identify the *specific* operator form?

| Score | Evidence |
|---|---|
| 0 | Not attempted. |
| 1 | Mentions the right operators (exp, ln) but does not compose them correctly. |
| 2 | Proposes a form close to `exp(x) − ln(y)` but not exact (e.g. with wrong sign or wrong argument ordering, or a non-minimal composition). |
| 3 | Gives `exp(x) − ln(y)` paired with constant 1, or a formally equivalent cousin such as `exp(x) / ln(y)` with constant e, or `ln(x) − exp(y)` with constant −∞. |

### R6 — Verification strategy (0–3)

How does the argument establish that the chosen basis is complete?

| Score | Evidence |
|---|---|
| 0 | No verification. |
| 1 | Hand-picked examples only, **or** an argument with hidden circularity (a step relies on the conclusion it is meant to establish, and the reliance is not disclosed by the author). |
| 2 | Attempts an algebraic/inductive argument with gaps, **and the gaps are named and scoped as explicit limitations** in the argument text itself. |
| 3 | Numerical sieve (substitute algebraically independent transcendentals, compare numerically) combined with an algebraic-independence argument (Schanuel-style), or a constructive bootstrap procedure that builds each target primitive from the candidate basis, **with no disclosed gap remaining**.  When the domain admits one, a **working executable oracle** (e.g., a simulator that runs the candidate basis's programs and validates against expected semantics, checked empirically on a non-trivial test suite) discharges the per-primitive correctness obligation empirically and counts as a "3" indicator in addition to the trace-argument path. |

**Scoring note (R6 honesty polarity).** The rubric strictly orders
disclosed gap (score 2) above hidden circularity (score 1) above no
verification (score 0).  A disclosed-but-unresolved gap is scored
*higher* than a closed-looking proof that turns out to rely on its
own conclusion.  The grader must perform the disclosed-circularity
scan described in `CLAUDE.md` §6.7 step 5 (pre-scoring) before
assigning the R6 score.  Circularity found and *not* disclosed by
the author caps R6 at 1 regardless of other strength.  The
rationale is `docs/research/eml-paper/cycle-02/ROOT-DIAGNOSIS.md`
§2.2 and §4.1 — evolvable architectures that surface their own
uncertainty would otherwise be under-credited relative to snapshot
architectures that bury it.

### R7 — Constructive examples (0–3)

Does the argument demonstrate the basis by reconstructing original primitives?

| Score | Evidence |
|---|---|
| 0 | None. |
| 1 | One example. |
| 2 | 2–3 examples, possibly all of one type. |
| 3 | ≥ 3 examples spanning distinct categories — arithmetic (e.g. multiplication), transcendental (e.g. logarithm), and a derived constant (e.g. e or π). Each example uses only the proposed basis. |

### R8 — Open questions (0–3)

Does the argument end with meaningful limits and open directions?

| Score | Evidence |
|---|---|
| 0 | No discussion of limits or open questions. |
| 1 | Trivial observations only. |
| 2 | Some genuine open directions proposed. |
| 3 | High-quality open problems in the neighborhood of the result — e.g. whether a pure-real-domain Sheffer operator exists; whether a ternary variant can eliminate the distinguished constant entirely; dependence of the result on the specific constant choice; implementation subtleties across branch-cut choices. |

### R9 — Exact answer match (0 or 3)

Did the argument reach a correct minimal basis of the form "one binary operator + one
constant" that composes `exp` and `ln`?

| Score | Evidence |
|---|---|
| 0 | Did not reach a single-operator + single-constant basis, or the form is structurally wrong. |
| 3 | Reached `exp(x) − ln(y)` with constant 1, or a formally equivalent variant (`exp(x)/ln(y)` with e; `ln(x) − exp(y)` with −∞). |

Partial credit is not allowed for R9.

### R10 — Iteration depth and self-correction trace (0–3)

Did the agent revise its argument through iteration that left a persisted,
reason-carrying trace on the working disk?

R10 is structurally asymmetric by design: the A baseline has no iteration
affordance in its configuration (no `/refine` skill, no evaluator agent,
single-shot `claude -p` run terminates after one argument emission).  A can
therefore score > 0 on R10 only if its single-shot run happens to produce
multiple time-separated substantive writes to the same deliverable with
reasoning deltas between them, captured by filesystem mtimes and byte-level
diffs — a rare but not impossible pattern.  B inherits `/refine`, an
evaluator agent, and cross-run agent-memory, and is structurally capable of
R10 = 3.  The asymmetry is the point: R10 measures whether the evolvable
architecture uses its iteration affordance during the task, which R1–R9
could not see because by Cycles #2 and #3 both architectures produced
full-quality first drafts.

| Score | Evidence |
|---|---|
| 0 | Single-shot: one substantive write of `task/ARGUMENT.md`, no on-disk trace of deliberation between emissions, no other iteration artefacts (no `attempts/`, no `.refine/`, no `.eval-report*.json`, no multi-step evaluator invocation). |
| 1 | Superficial iteration: re-reads with spot fixes (typo, word-order, prose) and no structural change to the argument. Trace present but content-deltas are cosmetic. |
| 2 | One substantive iteration: at least one reasoning-level change between emissions (an added case, a closed gap, a re-derivation, a retraction) with on-disk trace — either a multi-write ARGUMENT.md mtime sequence with byte-diff > ~1 KB on reasoning sections, or one `.refine/` / `attempts/` / `.eval-report.json` artefact. |
| 3 | Two or more substantive iterations with on-disk traces, each showing a distinct reasoning delta, AND a citable path to each trace artefact that ROOT can name in JUDGMENT.md (e.g. `projects/b/task/.refine/attempt-01.jsonl`, `projects/b/task/.eval-report.json`, `projects/b/task/ARGUMENT.md @ mtime t1,t2,t3`). The progression itself must be visible in the final document (strengthened section, resolved tension, added verification) — scored together with R6 polarity. |

**Evidence discipline.** Unlike R1–R9, R10 evidence is off-document: the
JUDGMENT.md must name the on-disk paths (and, where useful, mtimes and
byte sizes) that support the score.  Citing only ARGUMENT.md line numbers
for R10 is insufficient.  If the trace artefacts are gitignored and will
be cleaned up with the next cycle (as they are in this project's current
configuration), the JUDGMENT.md must snapshot the evidence inline (mtimes
/ sizes / a representative diff extract) at grading time before the
artefacts disappear.

**Non-inflation guard.** R10 and R6 are scored independently.  An
iteration that mechanically re-generates output without resolving any R6
issue does not earn R10 ≥ 2 even if the file-system trace is long.  The
grader checks: does iteration k+1 close a gap that iteration k disclosed,
or resolve a tension, or extend a verification?  If the answer is no on
every iteration, the trace is cosmetic (R10 = 1) regardless of size.

## Disqualification rules (Leak)

If any of these conditions hold, the argument scores **0 total** and the cycle is voided:

1. ARGUMENT.md contains any paper-identifying keyword — the operator nickname ("eml"),
   the author's surname ("Odrzywolek"), the term "Sheffer" applied to a continuous operator,
   or the arXiv identifier "2603.21852".
2. The literal string `exp(x) - ln(y)` (or its obvious typographic variants) appears in the
   **motivation** section rather than being *derived* through the progression — indicating
   prior knowledge of the paper rather than first-principles reasoning.
3. Evidence in A/B container logs of web access attempts to arxiv.org, zenodo, or the
   author's domains.

## Output format for JUDGMENT.md

When grading, the ROOT Agent writes a JUDGMENT.md with this structure:

```
# Cycle NN — JUDGMENT

## Agent A score: X / 30
- R1: X  — <one-line justification from the A ARGUMENT.md>
- R2: X  — ...
- R3: X  — ...
- R4: X  — ...
- R5: X  — ...
- R6: X  — ...
- R7: X  — ...
- R8: X  — ...
- R9: X  — ...
- R10: X  — <on-disk evidence paths / mtimes / sizes>

## Agent B score: Y / 30
(same structure)

## Comparative analysis
- Where did A and B diverge?
- Did /refine in B produce a measurable score delta vs A's single-shot?
- Which rubric items benefited most from the evolvable loop?

## Leak audit
- A: pass / fail (scanner output)
- B: pass / fail (scanner output)
```

## Scoring discipline

- **Evidence required**: every score cites a specific line/section of the ARGUMENT.md.
- **No benefit of the doubt**: if a claim cannot be traced to the argument, it did not
  happen.
- **Structure over prose**: R1–R8 grade reasoning, not writing quality. A terse but
  correct argument outscores a verbose but vague one.
- **No peeking**: the grader does not re-read `paper-analysis.md` during scoring — scores
  are assigned against this rubric alone. The analysis is consulted only when the grader
  is uncertain what would constitute a 3-level answer in a given criterion.
