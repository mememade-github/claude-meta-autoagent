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

**Band-3 tightening (ported from `band-3-tightening-v1.md`, Cycle #7 pre-cycle).**
When the deliverable uses **distinct proof tools** (e.g., confluence and
termination argued by different machinery; well-definedness and
decidability argued by different machinery), band 3 additionally
requires that each tool be isolated as a **named sublemma stated and
discharged separately** from the main argument.  Conflated proofs
(distinct machinery argued in intermixed prose) max at band 2.  Band 3
also requires the deliverable to state its **scope**: which axes of
correctness the method covers and which it does not.  Evidence anchor
(Cycle #6 JUDGMENT §4): B §2.1 isolated the variable-overlap handling
as a named sublemma reusable across the CP table; A §2 combined all
reasoning in a single 3-step procedure without a named sublemma.  The
tightening is about structural information content (reusable, citable,
independently-verifiable sublemmas), not prose style.  The tightening
applies **only when** the deliverable's method employs distinct proof
tools; tasks where a single tool discharges the whole obligation remain
unchanged.

### R3 — Progressive minimization (0–3)

Does the argument exhibit a sequence of progressively smaller sufficient configurations,
each justified?

| Score | Evidence |
|---|---|
| 0 | No intermediate configurations. |
| 1 | 1–2 intermediate steps without real justification. |
| 2 | 3+ steps with brief justification. |
| 3 | A coherent reduction sequence with each step motivated — e.g. dropping negation/reciprocal once a non-commutative operator provides inversion; collapsing named constants into functions; moving from lower to higher hyperoperation ranks. |

**Presentation-level grader note (ported from Cycle #5 §6.5).**  When
the axis's discharge requires enumerating a finite set of sub-cases
(e.g., a per-rule overlap audit, a per-primitive synthesis table, a
per-rule residual analysis), a **tabular** presentation is more
auditable than prose and should be preferred.  A tabular format
where each row names the sub-case, the discharge method, and any
disclosed gap is mechanically verifiable; the equivalent prose form
requires the grader to manually track the enumeration.  This is a
scorer-level bias, not a band threshold change: a prose discharge of
≥ 3 sub-cases can still earn band 3, but when the deliverable
presents the enumeration as a table, the grader should lean toward
band 3 on evidence-quality grounds.  Cycle #5 B-ARGUMENT.md §3.1
(13×13 overlap matrix) and §3.2 (per-rule RHS audit table) are
canonical examples; Cycle #5 A-ARGUMENT.md §1.3 (13-row primitive
LHS shape table) is another.  Cycle #6 B-ARGUMENT.md §3.1
(25 ordered-pair × 2 non-variable-position = 50-cell exhaustive
overlap table with disposition per cell) is a third canonical
example, validating that the pattern recurs across at least two
independent rewriting-system domains (combinator confluence +
list-rewriting confluence-plus-termination).

**Band-3 tightening (ported from `band-3-tightening-v1.md`, Cycle #7
pre-cycle).**  The scorer-lean above is promoted to a **band threshold**
in the specific case of enumeration over a finite, tractable support
(critical pairs of a finite TRS, rules of a small signature, overlaps
between a bounded rule set, sub-cases closeable by finite inspection).
In that case, band 3 requires the deliverable to present the
enumeration in **auditable tabular form** — one row per element of
the support, disposition column explicit per row.  Prose enumeration
of a closeable finite set maxes at band 2.  Evidence anchor (Cycle #6
JUDGMENT §4): B §3.1 50-cell overlap table vs A §3 prose enumeration
of the same 25 × 2 support.  Tightening rationale: a tabular format
with per-row disposition is mechanically auditable by the grader and
the proof-auditor's schema; the equivalent prose form requires the
grader to re-project the enumeration into an implicit grid, which is
the subjective-axis shared-bias risk flagged in every cycle's audit
`notes`.  The band-3 lift reduces that risk.  Domains whose
enumeration has genuinely infinite or intractable support are
unchanged (the tightening's precondition — "finite, tractable
support" — is explicit).

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

**Band-3 tightening (ported from `band-3-tightening-v1.md`, Cycle #7
pre-cycle).**  Band 3 additionally requires ≥ 4 examples, OR ≥ 3
examples that span **orthogonal failure / success modes** — each
example stress-tests a distinct axis of the deliverable's claim that
the others do not.  Two examples are orthogonal if removing one does
not reduce the total claim-coverage set; example sets of 3 that
overlap in success / failure mode max at band 2.  Evidence anchor
(Cycle #6 JUDGMENT §4): B had 4 examples where two were deliberately
orthogonal — CP3 ground witness (§6.4) stressed the critical-pair
closure claim; size-grows-but-φ-drops (§6.3) stressed the
measure-decrease-under-growth claim — removing either reduces
coverage of a distinct axis.  A had 3 examples all positive, all
overlapping in their "reduction converges" success mode.  When the
domain makes orthogonality hard to construct (e.g., a pure-existence
question), the ≥ 4 example count path is the available one.

### R8 — Open questions (0–3)

Does the argument end with meaningful limits and open directions?

| Score | Evidence |
|---|---|
| 0 | No discussion of limits or open questions. |
| 1 | Trivial observations only. |
| 2 | Some genuine open directions proposed. |
| 3 | High-quality open problems in the neighborhood of the result — e.g. whether a pure-real-domain Sheffer operator exists; whether a ternary variant can eliminate the distinguished constant entirely; dependence of the result on the specific constant choice; implementation subtleties across branch-cut choices. |

**Band-3 tightening (ported from `band-3-tightening-v1.md`, Cycle #7
pre-cycle).**  Band 3 additionally requires that at least one
disclosure be **structural** — a parametric impossibility, coefficient
contradiction, dimensional argument, or similar move showing *no*
construction in a named family can solve the problem — rather than
case-exhibition of a single failing instance.  All-case-exhibition
open-question sections max at band 2.  Evidence anchor (Cycle #6
JUDGMENT §4): B §7.1 proved "no linear [add] interpretation discharges
ρ6, ρ7, ρ8 simultaneously" by coefficient-intersection-empty
(parametric impossibility); A §7.1 exhibited one specific failing
linear candidate (one data point).  Structural disclosures scale; case
exhibitions do not.  Domains where parametric impossibility is
genuinely unavailable (e.g., purely empirical open questions) may
substitute a well-specified negative conjecture with named candidate
refutation paths, still scaled beyond single-instance exhibition.

### R9 — Exact answer match (0 or 3)

Did the argument reach a correct minimal basis of the form "one binary operator + one
constant" that composes `exp` and `ln`?

| Score | Evidence |
|---|---|
| 0 | Did not reach a single-operator + single-constant basis, or the form is structurally wrong. |
| 3 | Reached `exp(x) − ln(y)` with constant 1, or a formally equivalent variant (`exp(x)/ln(y)` with e; `ln(x) − exp(y)` with −∞). |

Partial credit is not allowed for R9.

### R10 — Iteration depth (0–3)

> **Domain-agnostic generalized form.**  R10 measures whether the
> deliverable was produced by a single-shot generation or by a
> multi-iteration process that made **disclosed, trace-verifiable
> progress** between emissions.  The core criterion is
> **"disclosed-gap closure with on-disk trace"** — applicable to any
> reasoning domain where (a) iterations can be persisted to disk,
> (b) some evaluator (agent or external) can produce gap reports, and
> (c) subsequent iterations can be diffed against prior ones.

#### What it measures

The axis is architecture-sensitive: a configuration with no iteration
affordance cannot score > 0; a configuration that iterates but produces
no reasoning delta cannot score > 1.  The axis rewards iteration that
**closes specific prior gaps** with **on-disk evidence**.

R10 is structurally asymmetric by design in this project: the A baseline
has no iteration affordance (no `/refine` skill, no evaluator agent,
single-shot `claude -p` run terminates after one argument emission).
A can therefore score > 0 on R10 only if its single-shot run happens to
produce multiple time-separated substantive writes to the same
deliverable with reasoning deltas between them, captured by filesystem
mtimes and byte-level diffs — a rare but not impossible pattern.  B
inherits `/refine`, an evaluator agent, and cross-run agent-memory, and
is structurally capable of R10 = 3.

#### Band definitions

| Score | Evidence |
|---|---|
| 0 | **Single-shot *or* vacuous audit.** (a) One substantive write of the deliverable with no on-disk trace of deliberation between emissions; OR (b) an audit / evaluator report exists but names zero disclosed gaps (e.g. "no issues found", empty `hard_constraint_violations`, empty `gaps` array).  A vacuous audit is vacuous iteration: `closure-of-disclosed-gaps` is the load-bearing criterion, and nothing disclosed means nothing to close.  No `attempts/`, no `.eval-report*` with named gaps, no numbered drafts.  mtime-adjacent polish edits (spell-fix, comment-tuning) count as part of the single shot, not as iteration. |
| 1 | **Cosmetic iteration with named gaps.** At least one evaluator / audit report names ≥ 1 disclosed gap (so the case is not vacuous), AND two or more drafts exist on disk, BUT the reasoning delta between drafts is cosmetic (re-wording, re-formatting, reordering) and the named gap is NOT closed by the next draft.  The gap is disclosed but unresolved; iteration happened but closure did not. |
| 2 | **One substantive iteration with gap closure.** Two drafts with at least one evaluator report showing ≥1 disclosed gap in draft-N that draft-(N+1) addresses.  The closure is verifiable by diff between drafts AND the evaluator report confirms the gap no longer appears. |
| 3 | **Two or more substantive iterations with reasoning delta and citable trace.**  Requires ALL of: (a) at least two iterations with on-disk drafts, (b) evaluator reports per iteration with `hard_constraint_violations` or equivalent disclosed gaps, (c) each iteration's deltas close ≥1 prior-iteration gap *without introducing new gaps of the same severity*, (d) the final deliverable reflects the progression, (e) the JUDGMENT can cite each trace artifact by path. |

#### Band boundary: audit-found-nothing vs cosmetic

This boundary was surfaced by Cycle #5's proof-auditor CONDITIONAL on
R10-A (agent produced `A-iter-01-audit.md` with zero gaps named).
Strict reading: band 0 (no closure possible).  Generous reading: band 1
(audit artefact exists).  The grid above resolves this with a single
load-bearing criterion: **band 1 requires ≥ 1 disclosed gap regardless
of closure; band 0 covers every case where no gap was ever disclosed**.
An audit that concludes "no issues found" without naming anything
scores 0, not 1.

Rationale: R10's purpose is to measure whether iteration *closed
disclosed gaps*, not whether the agent *performed the ritual of
auditing*.  A vacuous audit has nothing to close and contributes no
reasoning delta, so it is equivalent to a single-shot for R10's purpose.

#### Band boundary: pre-disclosed-gap audit (M6.2 codification — Cycle #7 pre-cycle port)

Cycle #6 R10-A surfaced a second edge case: A produced a single
ARGUMENT.md draft that already disclosed its own gaps in §7, then
wrote a post-hoc `iter-01-audit.md` naming F1/F2/F3 — where F1/F2/F3
were **already** disclosed in the same single-shot draft's §7.  No
second draft.  Audit concluded "Iteration closed; deliverable stands".

Under the preceding band text this could be read as band 1 ("audit
names ≥ 1 gap, no closure").  Structurally it is a single-shot: the
audit confirms what the deliverable already disclosed, not what a
second draft closed.  No reasoning delta was produced.

**Resolution.**  Band 1 requires the disclosed gap to be named in an
iteration-separate artefact — an evaluator / audit report whose
contents are not already present in the deliverable's own
disclosure section.  If the audit names only gaps already disclosed
in the deliverable itself, no *new* disclosure happened; the
post-hoc audit is a ritual confirmation of self-disclosure, and the
pattern scores **band 0**.

Strict test: *is there any gap named in the audit that is NOT
already named in the deliverable's own open-questions / limitations
section at the time of the audit?*  If no → band 0
(post-hoc confirmation of self-disclosure).  If yes → band 1 or
above depending on closure.

Applied retrospectively: Cycle #6 A-R10 was scored 0 under the
load-bearing closure-count criterion with this edge case flagged as
`M6.2-R10-band-0-1-second-edge-case`.  Under this codification,
Cycle #6 A-R10 = 0 is now closed (not CONDITIONAL): audit-names-only-
pre-disclosed-gaps ≡ band 0.

#### Band boundary: evaluator-report-substitution (M6.3 codification — Cycle #7 pre-cycle port)

Cycle #6 R10-B surfaced a third edge case: B produced iteration 1
(`attempt-01.md` + `.eval-report-01.json` with 7 gaps), iteration 2
(final `ARGUMENT.md` closing all 7), but **no second evaluator
report**.  Closure was verified by ROOT's diff between drafts +
ARGUMENT.md's own front-matter "7 gaps closed at §-locations X,Y,Z"
attestation, not by a `.eval-report-02.json`.

Under strict reading of band 3 ("evaluator reports per iteration" —
plural), B has only one evaluator report and tops at band 2.  Under
generous reading (ROOT diff + self-attested closure substitutes for
a second evaluator report), B reaches band 3.

**Resolution.**  Band 3 requires evaluator-or-equivalent verification
**per iteration beyond the first**, where "equivalent" is one of:

- a subsequent `.eval-report-*.json` or named audit artefact from the
  evaluator, OR
- an independent oracle output (e.g., a simulator run, a type-checker
  pass) that mechanically confirms the closure of each named gap, OR
- a **committed diff artefact, separate from the deliverable, that
  mechanically shows per-gap closure** — for example a
  `gap-closure-check.json` written by ROOT (or by a closure-check
  script reading the prior `.eval-report-01.json` and the final
  ARGUMENT.md).  The verifier (ROOT) must be independent of the
  iterator (B); the attestation must live outside the deliverable.

Self-attestation inside the deliverable's own front matter is **not**
sufficient for band 3 (the attester and the asserter are the same
entity).  ROOT-performed diff verification is sufficient if recorded
as a structured artefact committed alongside (e.g., a
`gap-closure-check.json`), because the verifier (ROOT) is
independent of the iterator (B).

If B produces iteration 2 without any of the three substitutes, the
configuration tops at band 2.

Applied retrospectively: Cycle #6 B-R10 was scored 2 under strict
reading.  Under this codification, if ROOT had additionally
committed a `cycle-06/gap-closure-check.json` (structured
per-gap-per-§-location verification), B-R10 could have reached 3.
It did not, so band 2 remains the correct retrospective score; the
codification is forward-looking.  `M6.3-R10-band-2-3-evaluator-
report-substitution` is closed: the rubric now specifies the three
allowable substitutes.

#### Non-inflation guard

Iteration count alone does NOT elevate the band.  If an iteration
produces no closure (no disclosed gap named in iteration-(N+1)'s
evaluator report is resolved in iteration-(N+2)), that iteration scores
at most the previous band.  R10 and R6 are scored independently, but
an iteration that mechanically re-generates output without resolving
any R6 issue does not earn R10 ≥ 2 even if the file-system trace is
long.

#### Evidence required in JUDGMENT

For any R10 > 0 score, the JUDGMENT MUST include:

1. **Iteration trace table** — one row per on-disk draft / report, with
   path, mtime, byte size, and content-hash (at minimum SHA256 prefix).
2. **Reasoning-delta enumeration** — one entry per disclosed gap
   closed, citing (a) the evaluator-report field where the gap was
   named, and (b) the iteration where the gap was closed (with
   byte-range or §-reference in the new draft).
3. **Non-inflation check** — statement that iterations did NOT
   introduce new gaps of the same severity.  If they did, the band is
   capped.

Citing only ARGUMENT.md line numbers for R10 is insufficient.  If the
trace artefacts are gitignored and will be cleaned up with the next
cycle, the JUDGMENT.md must snapshot the evidence inline (mtimes /
sizes / a representative diff extract) at grading time before the
artefacts disappear.

#### Example bands — Cycle #5 (confluence-proof domain)

| Band | Example |
|------|---------|
| 0 | `task/ARGUMENT.md` written in one pass; no `attempts/` directory; no `.eval-report*.json`.  Also: `task/audit.md` written but naming zero gaps ("no issues found" with empty finding list). |
| 1 | Two `attempts/attempt-0N.md` drafts AND an evaluator report naming ≥ 1 gap, but the named gap is unresolved in the next draft (prose polish only). |
| 2 | One `.eval-report*.json` names a missed critical-pair case in a confluence argument; next iteration's `attempt-02.md` adds that case and the evaluator report confirms it as closed |
| 3 | ≥ 2 `.eval-report*.json` each name proof gaps (e.g., missed critical pair, unchecked reduction order, absent strong-normalization sub-argument); subsequent iterations close each with oracle-verified β-traces; JUDGMENT cites each `attempts/attempt-NN.md` and `.eval-report-NN.json` path |

#### Example bands — Cycle #6 (rewriting-system confluence + termination domain)

| Band | Example |
|------|---------|
| 0 | `task/ARGUMENT.md` written in one pass with no `attempts/` or `.eval-report*`.  Also: agent produces a `self-audit.md` whose "findings" list is empty and deliverable is not revised — vacuous audit, band 0 per the band-boundary rule above. |
| 1 | Two drafts AND an evaluator report naming a gap (e.g., "measure not shown to decrease on rule ρ₃" or "critical pair at ⟨ρ₁, ρ₂⟩ not enumerated"), but the next draft only re-words around the named gap without discharging it. |
| 2 | One `.eval-report*.json` names a specific obligation — a missed critical-pair closure for Q1 (confluence) OR a missed monotonicity check for Q2 (termination) — and the next iteration's draft + re-evaluation confirms the obligation discharged (matrix row added; measure argument extended to cover the missing rule). |
| 3 | ≥ 2 `.eval-report*.json` each naming distinct obligations across both Q1 and Q2 (e.g., iter-1 names "ρ₁/ρ₂ critical pair unchecked" + "ρ₃ decrease of measure not argued"; iter-2 closes both with specific table rows + extended measure proof; iter-3's evaluator confirms closure and introduces no new same-severity gaps); JUDGMENT cites each draft + evaluator path. |

When R10 does NOT apply (no evaluator, or the deliverable is itself an
oracle output with no draft), drop the axis for that cycle.

#### Relation to `/refine` skill

When the executing architecture has `/refine`, an R10 = 3 score should
correspond to a `/refine` run with `contract_score` improving across
iterations and `.claude/agent-memory/refinement/attempts/refine-*.jsonl`
entries reflecting KEEP transitions.  Manual-iteration substitutes
(attempts/ + .eval-report*.json maintained by the executor without
`/refine` firing) still qualify for R10 = 3 provided the non-inflation
guard holds.

#### When to evolve this axis text

Edit this section when a cycle surfaces a gap in band definitions or a
new domain's example-bands row is validated.  Do not edit to
accommodate a specific cycle's peculiar outcome — those belong in that
cycle's JUDGMENT.md.  Changes flow: this file → next cycle's pre-cycle
rubric review.

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
