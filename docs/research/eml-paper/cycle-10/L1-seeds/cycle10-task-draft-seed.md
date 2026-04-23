# Cycle #10 TASK-draft (L1 reference)

> L1 drafts this as **reference**, not mandate.  L2 ROOT holds TASK
> authorship autonomy (§6.7 cycle pre-cycle).  This draft **returns
> to the EML-paper domain of Cycles #1-#3** after L0 direction
> 2026-04-23.  Rationale: the A/B meta-audit was designed to measure
> reasoning on post-training-cutoff material; EML paper (Odrzywolek
> arXiv:2603.21852, 2026-03) is post-cutoff for the model.  TRS
> domain (Cycles #4-#9) is classical textbook material with strong
> training-data coverage — confounds reasoning-vs-recall.  Cycle
> #10 restores the novel-domain precondition and runs the M9.4
> rubric falsification test against that cleaner baseline.

## Why this draft exists

Cycle #10 has two jobs:

1. **Restore novel-domain baseline.**  The last three task-domain
   iterations (Cycle #7 non-positive TRS, Cycle #8 confluence/
   termination TRS, Cycle #9 confluence/WN/SN TRS) placed A and B
   on classical material.  The M7.1 prompt-discipline + M8.x locus
   clarifications sharpened the rubric under this confound.
   Returning to EML allows us to retest the sharpened rubric against
   the domain it was originally built for.
2. **Run M9.4 rubric falsification test on the novel domain.**  X
   probe is constructed so its semantic fault is exactly the kind
   of fault pre-training would induce: stopping at the
   textbook-known minimum (`{exp, ln, +}` or `{exp, ln, −}`)
   without reaching the post-training single-operator answer.  The
   rubric is falsifiable iff it distinguishes this fault from a
   correct novel-answer deliverable.

## Rubric-blindness + falsification-blindness + paper-blindness

Cycle #8 prohibition set + Cycle #9 M8.1/M8.2/M8.3 extensions
+ Cycle #10 falsification-specific additions + EML paper-identifying
terms (already in paper-leak-guard):

```
grep -iE "band[ -]?[0-9]|sublemma separation|named sublemma|\
tabular enumeration|orthogonal example|parametric impossibility|\
structural impossibility|cite each trace artifact|\
gap.?closure.?check|closure.?artefact|open.?questions.? section|\
enumeration locus|verifier_identity|\
falsif|planted|probe|X-?ARGUMENT|authorial-identity|\
rubric-falsification|shape-measuring|reasoning-measuring|\
odrzywolek|arXiv.*2603|single operator.*constant|\
eml|sheffer" \
     docs/meta-audit/cycle-10/TASK-draft.md
```

The prose below should produce zero match outside the grep
alternation itself.  paper-leak-guard hook in A/B containers
carries the paper-identifying terms in reversed form and blocks
any tool payload containing them.

## Suggested content shape

The actual TASK.md (which L2 commits) should follow the Cycle #1
format.  **This is a sketch of tone and structure.**  L2 may
adjust the primitive list's surrounding prose but should preserve
the substantive question.

---

### Sketch: Minimal Generating Basis for Elementary Calculator Functions

Consider the following primitive set of a standard scientific
calculator:

- **Constants:** π, e, i, −1, 1, 2 (also accept input variables x, y)
- **Unary:** exp, ln, reciprocal (1/x), sqrt, square (x²),
  negate (−x), halve (x/2), logistic sigmoid 1/(1+e⁻ˣ),
  sin, cos, tan, arcsin, arccos, arctan,
  sinh, cosh, tanh, arsinh, arcosh, artanh
- **Binary:** +, −, ×, ÷, arbitrary-base log log_x(y),
  exponentiation pow(x, y) = xʸ, arithmetic mean (x+y)/2,
  hypotenuse √(x²+y²)

Many of these operations are redundant — for example,
tan(x) = sin(x) ÷ cos(x) — and there is no deep reason each deserves
its own button.

**Central question:** what is the smallest generating basis (a
minimal set of constants and operators) from which every primitive
above can be reconstructed as a finite composition?

**Deliverable:** a self-contained argument, written to `task/
ARGUMENT.md` in your working directory.  It must include:

1. Motivation.  Why might such a reduction exist?  Draw on
   precedents from adjacent mathematical or computational domains
   that you reason about from first principles.
2. A systematic reduction procedure you design and justify.
3. A sequence of progressively smaller sufficient configurations
   derived through that procedure, with intermediate stopping
   points argued for.
4. The minimal configuration you can reach — including exact form
   of any constants and operators it uses.
5. A verification strategy: how do you confirm the chosen basis
   is complete (can express every original primitive)?
6. Worked examples: express at least three of the original
   primitives using only the minimal basis.
7. Open questions and known limitations of your result.

**Constraints:**

- Do not consult external sources.  Arguments must be developed
  from first principles.  WebFetch and WebSearch are disabled.
- Do not rely on named results you cannot derive.  If you invoke
  a theorem, sketch its reason.
- Cite no papers.  If you recall a relevant paper, state the
  underlying idea in your own words; do not name or quote.

**Banned identifiers.**  As recorded in
`.refine/banned-identifiers.txt` at cycle-10 pre-cycle commit.

---

## What this draft deliberately omits

- No hint that the minimum might be 1 binary + 1 constant.
- No mention of how the proof should be structured.
- No mention of whether examples should be tabulated.
- No mention of parametric / structural / "any rule of the form"
  framings as a grading concern.
- No reference to R-axes or bands.
- No mention of JSON artefacts, closure schemas, or iteration-
  evidence record shapes.
- No instruction about iteration count or what evaluator reports
  should contain.
- No mention of any auxiliary, reference, or comparison deliverable
  beyond A and B's own output.

The agent produces whatever shape its architecture yields.  The
rubric is applied to that shape by the grader, not pre-announced.

## L2 ROOT adoption guidance

L2 may:

- Adopt this TASK verbatim (recommended — format continuity with
  Cycle #1-#3).
- Adjust surrounding prose (framing, phrasing of constraints)
  within rubric-blindness + falsification-blindness +
  paper-blindness constraints.

L2 must NOT:

- Change the primitive set in a way that closes or reveals the
  novel answer.
- Add rubric-shaped instructions to the prompt.
- Mention any rubric axis or band criterion in any form.
- Hint at the existence of a third-party deliverable (X) or the
  falsification test.
- Mention the paper or its identity in any form.

## M9.4 experimental protocol (L2 binding)

Cycle #10 runs the rubric falsification test per
`procedures/falsification-test-v1.md` **on the EML domain**.
L2 ROOT operational constraints during Cycle #10:

1. L2 runs A and B normally against the TASK above.  A/B outputs
   scored per §6.7 cycle flow.  The `paper-analysis.md` serves as
   L2's oracle for R4/R5/R9 (the paper's novel answer is the
   ground truth; A/B deliverables are scored against it).
2. After A/B JUDGMENT is drafted, L2 scores the probe deliverable
   X-ARGUMENT.md (present at `docs/research/eml-paper/cycle-10/
   X-ARGUMENT.md` in the L2 workspace, bundled into the delegate-
   goal.sh seed set) against the same rubric.  Scoring uses the
   rubric-strict protocol in `procedures/falsification-test-v1.md`,
   not an adversarial-scrutiny protocol.
3. L2 produces `docs/research/eml-paper/cycle-10/X-JUDGMENT.md`
   with per-axis band + rubric-text citation + evidence from X.
4. proof-auditor runs over A, B, and X with the same invocation
   contract; audit.json carries three sets of rows.
5. L2 produces `docs/research/eml-paper/cycle-10/falsification-
   report.md` with the per-axis shape / reasoning / ambiguous /
   control verdict and a global finding (H0 / H1 / partial) per
   the verdict-threshold table in the procedure file.
6. L2 does NOT let A or B see X-ARGUMENT.md.  A/B containers
   do not mount `docs/research/eml-paper/cycle-10/` except for
   the bare TASK.md produced by L2.
7. paper-leak-guard hooks remain active in A/B containers (they
   always are); Cycle #10 does not relax paper isolation.

## Measurement the cycle enables

| Measurement | Interpretation |
|-------------|----------------|
| X shape-axes all drop to ≤ 1 | Rubric measures reasoning on shape axes.  H0 confirmed on novel domain. |
| X shape-axes mostly stay ≥ 2 | Rubric is shape-measuring.  H1 confirmed — rubric fails to distinguish textbook-stopping-point from novel-reasoning. |
| Mixed — some axes drop, others stay | Partial H1.  Per-axis tightening targets. |
| Incumbent and auditor disagree on X shape axes | Shared-bias decoupling signal. |
| X oracle axes (R5/R6/R9) stay ≥ 2 | Test invalidated.  Oracle layer broken. |
| A/B reach novel answer (1 bin + 1 const) | Architecture demonstrates post-training reasoning.  Strong signal. |
| A/B stop at textbook minimum | Architecture replicates X's fault pattern.  Weak signal for "novel reasoning capability". |

Retrospective cycle-09 Δ under cycle-10 rubric (if rubric ports
occur): per retrospective procedure.  No rubric ports are planned
for Cycle #10 (falsification test is content-neutral to rubric);
retrospective expected to show zero movement.

## This draft's status

L1 reference material.  Freezes at cycle-10 pre-cycle commit.  The
actual cycle-10 TASK.md is committed by L2 ROOT (same commit or
subsequent).  Both files stay in the tree — the draft as L1 audit
trail, the TASK as the operative prompt.
