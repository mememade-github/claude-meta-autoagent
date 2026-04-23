---
status: draft
cycle: 11
domain: minimal-generating-basis-for-elementary-calculator-functions
auditor: proof-auditor
auditor_date: 2026-04-23
arbitration_triggered: false
incumbent_total_A: 20
incumbent_total_B: 22
incumbent_total_X_v2: 9
auditor_total_A: 20
auditor_total_B: 22
auditor_total_X_v2: 9
agreement: 30_YES_0_CONDITIONAL_0_NO (across A + B + X-v2, 10 axes each)
audit_file: cycle-11/rubric-audit.json
rubric_version: cycle-11 (cycle-10 + M10.2 R1 motivation-answer consistency + M10.3 R2 per-sublemma proof locality)
falsification_retest: m9.4 (procedures/falsification-retest-v1.md)
falsification_report: cycle-11/falsification-report-v2.md
retrospective_cycle_10: cycle-10/JUDGMENT-v2.md
---

# Cycle 11 — JUDGMENT

Grading of `docs/research/eml-paper/cycle-11/A-ARGUMENT.md` and
`docs/research/eml-paper/cycle-11/B-ARGUMENT.md` against
`docs/research/eml-paper/judgment-rubric.md` at its **Cycle #11
state** (Cycle #10 rubric + M10.2 + M10.3).

This cycle additionally runs the M9.4 rubric falsification
**re-test** per
`docs/research/eml-paper/procedures/falsification-retest-v1.md`.
The probe X (Cycle #10 `X-ARGUMENT.md`, unchanged) is re-scored
in `cycle-11/X-JUDGMENT-v2.md`; per-axis and global verdicts are
recorded in `cycle-11/falsification-report-v2.md`.  A separate
retrospective re-scoring of Cycle #10 A/B under the Cycle #11
rubric is at `cycle-10/JUDGMENT-v2.md` (non-R1/R2 axes unchanged
by design; no band shifts observed).

Front-matter `status` will transition per CLAUDE.md §6.7 step 5c
after the proof-auditor pass.

Cycle #11 is the **final cycle** of the current WIP per L0
Branch B decision (2026-04-23).

---

## §0. Cycle artefacts (audit record)

Captured at cycle close (2026-04-23 ~19:52 KST).

| Path | mtime (KST) | Bytes | sha256 prefix | Role |
|------|-------------|------:|:-------------:|------|
| `cycle-11/TASK.md` | 19:37 | 2809 | — | Operative TASK prompt (rubric-blind; verified) |
| `cycle-11/A-ARGUMENT.md` | 17:34 | 21594 | d2f68dea7a34e7c8 | A deliverable (byte-identical to cycle-10/A-ARGUMENT.md; see §0.1) |
| `cycle-11/B-ARGUMENT.md` | 19:48 | 20652 | 87a98ac703033bf6 | B deliverable (iter-2 accepted; distinct from cycle-10 B) |
| `cycle-11/B-iter-0-baseline.md` | 17:47 | 16379 | — | B iter 0 baseline (carried from cycle-10) |
| `cycle-11/B-iter-2-accepted.md` | 19:51 | 20652 | 87a98ac703033bf6 | B iter 2 accepted (== final ARGUMENT.md) |
| `cycle-11/B-eval-baseline-v2.json` | 19:45 | 4408 | — | B's internal v2 evaluator, baseline run |
| `cycle-11/B-eval-iter2-v2.json` | 19:50 | 9795 | — | B's internal v2 evaluator, iter-2 (1.0 score, KEEP+ACCEPT) |
| `cycle-11/B-rubric-v2.md` | 19:44 | 4034 | — | B's internal v2 rubric (B-authored, distinct from ROOT rubric) |
| `cycle-11/B-sim-verify.py` | 19:48 | 13042 | — | B's numeric oracle (35 primitives, seed 42, REL_TOL 1e-8) |
| `cycle-11/B-sim-output.txt` | 19:48 | 2414 | — | B's oracle output: **35 / 35 primitives PASS** at ~1e-15 error |
| `cycle-11/X-JUDGMENT-v2.md` | 19:43 | 17423 | — | X v2 re-score (see falsification-report-v2) |
| `cycle-11/falsification-report-v2.md` | 19:48 | 10829 | — | M9.4 closure verdict (Partial-capped) |
| `cycle-10/JUDGMENT-v2.md` | — | — | — | Retrospective cycle-10 A/B re-score (no band shifts) |

### §0.1 A-behaviour note (cycle-11)

Cycle #11 A re-audited its existing `task/ARGUMENT.md` (carried
forward from Cycle #10's run in the same container's workspace)
and reported: "The deliverable at `task/ARGUMENT.md` is already
complete and correct. I audited both the mathematical content and
the structural compliance with the brief. ... No edits needed.
The argument stands as delivered."  The SHA256 of
`cycle-11/A-ARGUMENT.md` is `d2f68dea7a34e7c8`, byte-identical to
`cycle-10/A-ARGUMENT.md`.  This is a single-shot no-op:
A's baseline architecture (karpathy-skills, no `/refine`)
allowed A to decline re-writing a deliverable it judged adequate.
From a measurement perspective, A's Cycle #11 score equals A's
Cycle #10 score under the Cycle #11 rubric (which per the
retrospective at `cycle-10/JUDGMENT-v2.md` is itself equal to A's
Cycle #10 score under the Cycle #10 rubric).

### §0.2 B-behaviour note (cycle-11)

B ran `/refine` with its own internal v2 rubric (committed to
`cycle-11/B-rubric-v2.md`; distinct from ROOT's rubric and not
paper-ground-truth-aware).  B's internal evaluator scored
baseline at 0.9123 with R5' (numeric-oracle) gap, then iterated:
added `task/sim/verify.py` + `task/sim/output.txt` (all 35
primitives PASS) and a §5.1 cross-reference paragraph.  iter-2
scored 1.0 → KEEP+ACCEPT.  Inner evaluator reports live at
`cycle-11/B-eval-{baseline,iter2}-v2.json`.  B's internal rubric
is not the scoring authority — ROOT's rubric (the Cycle #11 state
of `docs/research/eml-paper/judgment-rubric.md`) is.  B's internal
evaluator's R5' "numeric-oracle" dimension maps most closely to
ROOT's R6 (verification strategy) band-3 executable-oracle
indicator; B's self-score of 3 on R5' is plausibly defensible as
R6 band-3 support under the ROOT rubric — see §3 R6 below.

### §0.3 Execution timing (UTC+09:00)

- 2026-04-23 19:39 — `scripts/meta/delegate-sub.sh a` launched A;
  `scripts/meta/delegate-sub.sh b` launched B.  EFFORT=high.
- 2026-04-23 ~19:40 — A completed with no-op (re-audit + keep).
- 2026-04-23 19:44–19:45 — B authored internal rubric-v2.md and
  eval-baseline-v2.json.
- 2026-04-23 19:48 — B's ARGUMENT.md iter-1 write (20652 B);
  task/sim/verify.py + output.txt written.
- 2026-04-23 19:50–19:51 — B's eval-iter2-v2.json (1.0),
  iter-2-accepted.md.
- 2026-04-23 ~19:52 — B exits via KEEP+ACCEPT.

---

## §1. Leak audit

- `bash scripts/meta/paper-leak-audit.sh cycle-11/A-ARGUMENT.md`
  → PASS (no forward-form paper identifiers).
- `bash scripts/meta/paper-leak-audit.sh cycle-11/B-ARGUMENT.md`
  → PASS.

Paper-leak streak extends to **11 / 11** cycles (all cycles #1–#11
have passed paper-leak audit on A and B).

---

## §2. A score per axis (Cycle #11 rubric)

A's deliverable is byte-identical to Cycle #10 A.  Per-axis scoring
follows the Cycle #10 JUDGMENT.md analysis, adjusted for the Cycle
#11 rubric (M10.2 R1 + M10.3 R2 tightenings).  Per the cycle-10
retrospective at `cycle-10/JUDGMENT-v2.md`, no axis shifts under
the Cycle #11 rubric for A — A clears the M10.2 obstruction-sketch
bar (§1(a) argues exp/ln irreducibility; §1(c) sketches
"transcendental layer on top") and meets M10.3 per-sublemma
statement+proof locality (§3.6 four obstructions each discharged
in its own sub-paragraph).

### R1 Motivation — **3** (cycle-10 v2 retrospective: 3; unchanged)

A §1 names three structural precedents:

- §1(a) reduction-under-inversion: "`exp` / `ln` are the only
  genuinely new data; the other 'inverses' are expressible once a
  single complex unit is available" — sketches exp/ln
  irreducibility as an obstruction to further reduction.
- §1(b) real/complex fusion via Euler identity.
- §1(c) field-generation as an equivalent named minimal-basis
  precedent: "Arithmetic of ℂ has a similar minimal backbone;
  everything transcendental lies on top."

**M10.2 tightening check.** A cites minimal-generator precedent
(field generation, 2 binary + 1 constant).  Answer shape: 2 binary
+ 2 unary + 1 constant (strict) or 1 binary + 2 unary + 1 constant
(relaxed).  (a) shape-match: A's answer has 2 additional unary
helpers beyond the precedent's shape — (a) does not hold.  (b)
obstruction sketch: §1(a) argues exp/ln irreducibility; §1(c)
sketches "transcendental lies on top" — combined, A's §1 contains
a sketch argument for why the answer exceeds field-precedent
shape.  **(b) met at sketch level** → R1 stays at band 3.

Distinction from X: X §1 asserts "reduction pressure on
transcendental side" (strategy statement) without arguing exp/ln
irreducibility (obstruction statement).  A argues; X doesn't.

### R2 Method design — **3** (cycle-10 v2 retrospective: 3; unchanged)

A §2 names four reduction rules R1–R4; A §3.6 provides four
named structural obstruction arguments under distinct proof tools
(growth, branch-point, cardinality/2πi-modular, zero-locus).  Each
obstruction in its own sub-paragraph with its own proof.

**M10.3 locus clarification check.** (a) statement locality,
(b) proof locality, (c) non-distributed discharge — all three
met.  R2 stays at band 3.

Distinction from X: X §2.2 declared three sublemmas without
per-sublemma proof blocks — (b) proof locality fails.

### R3 Progressive minimization — **3**

A §3.1–§3.5 has five deliverable-side reduction tables (B₁ 11
rows, B₂ 11 rows, B₃ 2 rows, B₄ 5 rows, B₅ 3 rows), each with
explicit witness column.  Cycle #9 locus clarification met:
deliverable-side tabular enumeration with disposition column.

### R4 Final basis structure — **2**

A §4 strict minimum: 2 binary + 2 unary + 1 constant = 5.  A §3.8
relaxed: 1 binary + 2 unary + 1 constant = 4.  Neither matches
band-3 "exactly one binary + one constant".  Band 2 fits ("≤ 2
binary").

### R5 Exact form — **1**

A does not propose a single binary operator of `exp(x) − ln(y)`
form.  Band 1 fits (right operators mentioned, not composed into
single binary).

### R6 Verification strategy — **2**

A §5 three-stage verification (forward synthesis, numerical
cross-check, strict-minimality audit).  Disclosed gap in §7(2):
"We have not found a way to obtain `×` as a total function from
`{+, exp, ln, constants}` alone, but have not proved it
impossible."  R6 polarity: disclosed gap → band 2.

### R7 Constructive examples — **3**

A §6 has four worked examples spanning inverse-transcendental
(arctan), hyperoperation (pow), composite arithmetic (hypot),
transcendental (sin).  Cycle #7 tightening: ≥ 4 examples path.
Band 3.

### R8 Open questions — **3**

A §7 has six open-question items with explicit epistemic labels
and at least one parametric/structural disclosure (per Cycle
#9 labeling clarification).  Band 3.

### R9 Exact answer match — **0**

A does not reach paper's single-binary + single-constant form.
Band 0 (binary axis).

### R10 Iteration depth — **0**

No on-disk iteration trace in cycle-11/.  A's no-op re-audit
(§0.1) produces zero new on-disk artefacts.  Single-shot from
filesystem-evidence perspective.  Band 0.

### A total: 3 + 3 + 3 + 2 + 1 + 2 + 3 + 3 + 0 + 0 = **20 / 30**

---

## §3. B score per axis (Cycle #11 rubric)

B's Cycle #11 deliverable is distinct from Cycle #10's (sha256
87a98ac7... vs 7e34be66...).  B added §5.1 numeric oracle
reference and task/sim/verify.py closure artefact (35 / 35 PASS).
Elsewhere B's argument structure is preserved from its Cycle
#10 iter-1 baseline.  Per-axis scoring against Cycle #11 rubric:

### R1 Motivation — **2** (cycle-10: 2; unchanged)

B §1 four internal collapse mechanisms (additive/multiplicative
duality via exp/ln isomorphism; inverse-function pairs via Euler;
complex extension via Euler identity; algebraic/transcendental
split).  Per cycle-10 JUDGMENT and M10.2 non-inflation clause: B
does not invoke a cross-domain named structural precedent for
single-primitive / minimal-generator reduction; the M10.2 trigger
does not fire; pre-tightening band text applies.  Band 2 fits
("adequate analogy or partial precedent").

### R2 Method design — **3** (cycle-10: 3; unchanged)

B §2 has 8 ordered reduction steps, each with named identity; B
§4 has four named Drop-X essentiality arguments under distinct
proof tools (arity for Drop +; surjectivity for Drop exp;
analytic entirety for Drop ln; ℝ_{>0} closure for Drop −1), each
discharged in its own sub-paragraph.  M10.3 locus clarification:
(a) statement locality ✓, (b) proof locality ✓, (c) non-distributed
discharge ✓.  Band 3.

### R3 Progressive minimization — **2** (cycle-10: 2; unchanged)

B §3 has four prose stages (A ~12, B 6, C 5, D 4).  Cycle #9 locus
clarification: when enumeration has finite tractable support, band
3 requires deliverable-side tabular presentation.  B's §3 is
prose-per-stage, not a single deliverable-side table with
per-stage disposition column.  Band 2 ("3+ steps with brief
justification").

### R4 Final basis structure — **2** (cycle-10: 2; unchanged)

B §4 commits `B* = {+, exp, ln, −1}` = 1 binary + 2 unary + 1
constant = 4 elements.  Band 3 requires "exactly one binary
operator paired with exactly one distinguished constant" — B has
2 unary helpers beyond that.  Band 2 fits ("≤ 2 binary").

### R5 Exact form — **1** (cycle-10: 1; unchanged)

B §5 derived toolkit composes exp/ln/+ correctly but does not
propose a single binary operator of `exp(x) − ln(y)` form.  Band
1 (right operators mentioned, not composed into single binary).

### R6 Verification strategy — **3** (cycle-10: 2; **+1**)

B's Cycle #11 R6 is strengthened relative to Cycle #10 via two
mechanisms:

**(i) Executable oracle (task/sim/verify.py).**  B's oracle
declares exactly four basis primitives (`BASIS_ADD`,
`BASIS_EXP`, `BASIS_LN`, `BASIS_NEG1`) wrapping numpy primitives,
builds a derived toolkit (NEG, MUL, RECIP, DIV, SUB) using *only*
those basis primitives, then builds each of 35 primitive
implementations (`prim_*`) through the toolkit.  The oracle
evaluates each primitive at 20 complex sample points (fixed seed
42) and compares against numpy reference implementations; numpy's
sin/cos/tan/arcsin/etc. appear **only as reference oracles**,
never in the `prim_*` bodies (per the eval-iter2 evaluator's
grep verification).  Output: **35 / 35 primitives PASS** at
~1e-15 (machine-epsilon) error.  This is the rubric R6 band-3
indicator: "a working executable oracle ... discharges the
per-primitive correctness obligation empirically and counts as a
'3' indicator in addition to the trace-argument path."

**(ii) Essentiality arguments strengthened to rigorous
obstructions.**  Cycle #10's R6 band-2 cap was cited specifically
for: (a) real-vs-complex domain disclosure, and (b) formal-lower-
bound disclosure (essentiality argument admitted to be
"structural/semantic, not a theorem in a fully formalized term
algebra" per cycle-10 §7 "Formal lower bound").  Cycle #11 B §7
"Formal lower bound" now reads: "The per-element essentiality
arguments in §4 are now rigorous obstructions: drop-+ is a
signature/arity argument, drop-exp and drop-ln are analytic
obstructions via entireness/branch structure ..., and drop-(−1)
is a closure argument on ℝ_{>0}.  What *remains* open is a global
cardinality lower bound over arbitrary basis reorganizations —
i.e. a proof that no alternative 3-element basis (not necessarily
a subset of B*) generates the full primitive set."  The cycle-10
gap (per-element essentiality rigor) is discharged; the remaining
open question is about non-subset alternative 3-element bases.

**R6-axis scoping.**  The cycle-11 disclosed residuals — (i) real-
only basis (scope restriction on different domain), (ii) global
lower bound over non-subset alternatives (minimality-of-B* w.r.t.
non-subset alternatives) — are SCOPE and MINIMALITY questions,
not gaps in the B* → primitive *bootstrap completeness* that R6
measures.  The R6 question is "how does the argument establish
the chosen basis is complete?" — B's §5 primitive table + §5.1
numeric oracle + §4 rigorous essentiality discharge that question
with no *completeness* gap disclosed.

**Verdict: R6 v2 = 3.**  Band 3 via executable-oracle indicator +
constructive bootstrap with rigorous essentiality (no disclosed
gap in the completeness path).  This is a genuine +1 over
cycle-10, attributable to (i) the new oracle artefact and (ii)
the strengthened essentiality in §4.

**Non-inflation.** oracle is independently verifiable: (a) output
file at `cycle-11/B-sim-output.txt` shows 35/35 PASS with
per-primitive max errors all < 3.7e-15; (b) the eval-iter2 JSON
records a grep-based audit confirming numpy reference functions
are absent from `prim_*` bodies; (c) the oracle script is
re-runnable on any machine with numpy.  No fabricated rows; no
oracle-unverifiable claims.

### R7 Constructive examples — **3** (cycle-10: 3; unchanged)

B §6 has three worked examples: mult (arithmetic), cos (Euler
complex), arctan (inverse logarithmic).  Orthogonality per cycle-
10 analysis: each example exhibits a distinct reduction pattern.
Band 3 via ≥ 3 orthogonal modes.

### R8 Open questions — **3** (cycle-10: 3; unchanged)

B §7 has seven disclosures with explicit epistemic labels,
including the parametric characterization ("any single complex
seed z_0 ∉ ℝ_{>0} whose principal ln is a rational multiple of
iπ can replace −1") and the Drop-X structural impossibilities.
Cycle #7 tightening met; cycle #9 labeling met.  Band 3.

### R9 Exact answer match — **0** (cycle-10: 0; unchanged)

B's `B* = {+, exp, ln, −1}` is not a single-binary + single-
constant form.  Band 0.

### R10 Iteration depth — **3** (cycle-10: 3; unchanged)

B's on-disk iteration trace for Cycle #11:

| Path | mtime | Bytes | sha256 prefix | Role |
|------|-------|------:|:-------------:|------|
| `cycle-11/B-iter-0-baseline.md` | 17:47 | 16379 | 2aac82a8 | iter 0 baseline (carried from cycle-10) |
| `cycle-11/B-iter-2-accepted.md` | 19:51 | 20652 | 87a98ac7 | iter 2 accepted (== final ARGUMENT.md) |
| `cycle-11/B-eval-baseline-v2.json` | 19:45 | 4408 | — | evaluator baseline (0.9123; R5' gap) |
| `cycle-11/B-eval-iter2-v2.json` | 19:50 | 9795 | — | evaluator iter-2 (1.0; KEEP+ACCEPT) |
| `cycle-11/B-sim-verify.py` | 19:48 | 13042 | — | numeric oracle (35/35 PASS closure artefact) |
| `cycle-11/B-sim-output.txt` | 19:48 | 2414 | — | oracle output |

**Per-iteration evaluator records.**  `B-eval-baseline-v2.json`
identifies G1 (R5' absent), G2 (R7 counting-convention implicit),
G3 (R10 trace discipline unverified).  `B-eval-iter2-v2.json`
records gap closures: G1 closed via new verify.py + output.txt
(covers 35/35 primitives); G2 closed via §7 "Variables as basis
elements" + "Uniqueness" + "Cardinality vs depth minimality"
ranking; G3 noted as low-priority and discussed structurally.

**M6.3 reproducibility tag: `not-applicable`.**  B's pattern is
M6.3 path (a) native — per-iteration evaluator records at
`B-eval-iter2-v2.json` with explicit `gap_closure_vs_baseline`
subtree mapping baseline gaps to closure locations.  Third
consecutive cycle (#9, #10, #11) where B reaches R10 band 3 via
native (a) path.

**Closure artefact (M6.3 (c) analog).**  `B-sim-verify.py` + its
output is a self-contained closure artefact: the numeric oracle
passes 35/35 reproducibly (seed 42), re-runnable without
repo-wide tooling.  This is M6.3 path (c) in spirit (committed
reproducible artefact) combined with R6 band-3 executable-oracle
indicator.  The artefact's contribution to R10 is additive to
the (a) path's iteration record; both are present.

**Verifier identity:** B's `/refine` evaluator (not ROOT, not
Human).  Artefact mtimes fall inside B's active window
(19:39–19:52).  The `rubric-v2.md` and `eval-*-v2.json` files
use B's internal vocabulary (R5' prime for numeric oracle) not
ROOT's vocabulary — no scaffolding leak.

R10 = 3 via M6.3 path (a) + closure-artefact supplement;
reproducibility-tag = `not-applicable` (native path).

### B total: 2 + 3 + 2 + 2 + 1 + 3 + 3 + 3 + 0 + 3 = **22 / 30**

---

## §4. Delta analysis

```
A total = 20
B total = 22
Δ (B − A) = +2
```

**Per-axis breakdown:**

| Axis | A | B | Δ (B−A) | Notes |
|------|---|---|---------|-------|
| R1 | 3 | 2 | **−1** | A cites field-generation minimal-basis precedent + sketches obstruction; B's motivation is internal mechanisms without cross-domain precedent |
| R2 | 3 | 3 | 0 | Both meet M10.3 per-sublemma proof locality (A via §3.6 four distinct tools, B via §4 four Drop-X arguments) |
| R3 | 3 | 2 | **−1** | A has deliverable-side tables per step (cycle-9 locus met); B has prose stages |
| R4 | 2 | 2 | 0 | Both reach ≤ 2 binary but not single-binary form |
| R5 | 1 | 1 | 0 | Both compose exp/ln correctly; neither proposes single binary operator |
| R6 | 2 | 3 | **+1** | B adds executable oracle (35/35 PASS) + rigorous essentiality (cycle-10 R6 gap closed); A still has disclosed ×-reducibility gap |
| R7 | 3 | 3 | 0 | A via ≥ 4 examples; B via ≥ 3 orthogonal modes |
| R8 | 3 | 3 | 0 | Both: dedicated open-question section with ≥ 3 items + parametric/structural disclosure |
| R9 | 0 | 0 | 0 | Neither reaches paper's single-binary + single-constant answer |
| R10 | 0 | 3 | **+3** | A single-shot no-op (see §0.1); B M6.3 (a) native + closure artefact |
| **Total** | 20 | 22 | **+2** | — |

**A-over-B axes:** R1 (−1), R3 (−1).
**B-over-A axes:** R6 (+1), R10 (+3).
**Net delta:** B wins by +2, attributable primarily to R10
(iteration architecture) and R6 (new oracle + strengthened
essentiality this cycle).

### §4.1 Cycle #10 → Cycle #11 A/B Δ shift

- Cycle #10: A = 20, B = 21, Δ = +1.
- Cycle #11: A = 20, B = 22, Δ = +2.

**What changed.**  A unchanged (byte-identical deliverable).  B
improved R6 by 1 band (2→3) via new numeric-oracle closure
artefact + strengthened essentiality arguments.  Net Δ increases
from +1 to +2.

**Interpretation.**  Post-rubric-tightening (Cycle #11 rubric
with M10.2 and M10.3 addenda), the in-cycle EML-domain A/B
comparison shows B retaining its architectural advantage (the /refine
loop + cross-run learning enables B to close a rubric gap that
A's baseline architecture leaves open).  The R1/R2 tightening
did not itself alter A/B bands on either axis (per the
retrospective), confirming the tightening's non-inflation design.
The A/B Δ drift from +1 to +2 reflects B's runtime iteration
behaviour within this cycle, not a rubric-induced shift.

---

## §5. §5a Disclosed-circularity scan (pre-scoring)

Per CLAUDE.md §6.7 step 5a, applied to A and B.

### §5a on A

**Sections scanned:** §1 (with subsections (a) (b) (c)), §2
(R1–R4), §3 (§3.1–§3.8), §4, §5 (Stages A B C), §6 (Examples
1–4), §7 (disclosures 1–6), §8 (summary).

**Paragraph-level tensions detected:** none.

**Lemma dependency check:**

- §3.6 per-primitive essentiality arguments (exp, ln, +, ×) are
  each irreducibility claims that use distinct structural tools
  and do not appeal back to the conclusion being established.
- §6 worked examples use shorthand macros defined in §3.5 / §3.8;
  each macro expands to a finite composition in B₅ without
  self-reference.
- §7 disclosures each name a limitation bounded in scope;
  §7(2) is a disclosed-gap (× reducibility open), not a hidden
  reliance.

**R6 polarity mapping for A:** Disclosed gap in §7(2) → band 2.
No hidden circularity; cleanly disclosed.  R6 scoring at band 2
stands.

### §5a on B

**Sections scanned:** §1 (additive/multiplicative, inverse-pair,
complex extension, algebraic-vs-transcendental), §2 (1–8), §3
(Stages A B C D), §4 (Drop-+, -exp, -ln, -(−1), alternative
basis), §5 (derived toolkit + primitive table + §5.1 oracle),
§6 (Examples 1–3), §7 (branch cuts, domain, pow/log_x,
real-vs-complex, variables, uniqueness, cardinality-vs-depth,
formal-lower-bound).

**Paragraph-level tensions detected:** none.

**Lemma dependency check:**

- §4 Drop-exp: uses inability to get i from ln(−1) without exp —
  a structural forward argument, no self-reference.
- §4 Drop-ln: uses induction on term algebra's closure under
  entireness — a forward structural argument.
- §5 derived toolkit: bootstrap chain (−1) → · → 1 → 2 → 1/2
  → i → π → e.  Each step uses only prior constants (evaluator
  log records this dependency order and verifies no
  circularity).
- §5.1 oracle: the `prim_*` implementations use only basis
  primitives via toolkit macros; numpy references appear only
  in the reference oracle comparison, not in the basis side.
  No self-reference.
- §7 formal-lower-bound: explicitly frames the open question as
  about non-subset alternative 3-element bases; disclosed-as-open,
  not hidden.

**R6 polarity mapping for B:** no disclosed completeness gap; no
hidden circularity.  R6 = 3 (per §3 R6 analysis above).

### §5a on X (re-test; reference X-JUDGMENT-v2.md §4)

Re-scan result identical to cycle-10 X-JUDGMENT.md §3a: three
paragraph-level tensions (§3 row F operators outside basis;
§7.4 π self-reference; §7.4 −1-via-π chain), all undisclosed.
R6 X polarity: hidden circularity → band 1 (unchanged).  See
`cycle-11/X-JUDGMENT-v2.md` §4 for the full re-scan record.

---

## §6. §5b B → ROOT port analysis (post-scoring)

Per CLAUDE.md §6.7 step 5b, each distinct refinement artefact B
produced this cycle is evaluated for portability to ROOT.

### Artefact 1 — B's internal v2 rubric (`B-rubric-v2.md`)

**Location:** `cycle-11/B-rubric-v2.md`.  B authored an 11-
dimension rubric with weights, a 0.93 acceptance threshold, and
hard constraints H1/H2/H3.

**Decision:** **not-portable.**

**Rationale:** B's internal rubric is B's method for /refine
convergence, distinct from ROOT's A/B comparative rubric.  The
two rubrics have different purposes: B's is a self-scorer inside
B's iteration loop (no A↔B comparison, no paper-ground-truth
oracle); ROOT's is the comparative A/B grading authority with
paper-ground-truth via `paper-analysis.md`.  B's rubric's R5'
numeric-oracle dimension is the closest mapping to ROOT's R6
band-3 executable-oracle indicator; R6 already has that
indicator in the ROOT rubric, so no port is needed.

### Artefact 2 — B's numeric oracle pattern (`B-sim-verify.py`)

**Location:** `cycle-11/B-sim-verify.py` + `B-sim-output.txt`.
35-primitive numeric oracle, fixed seed, np-reference comparison,
machine-epsilon tolerance.

**Decision:** **deferred.**

**Rationale:** The oracle pattern is highly valuable in principle
— it's the first time B has produced an executable
domain-specific oracle that discharges R6 band-3.  However,
porting this as a reusable pattern to ROOT would mean either
(a) codifying "oracle expected at task/sim/verify.py" as a
structural expectation in the rubric (band-text edit), or
(b) publishing the pattern as an M-port entry like M6.3 closure-
artefact reproducibility.  Cycle #11 is the final cycle of this
WIP; (a) is out-of-scope (no further cycles to validate the
tightening); (b) is a Q5 candidate for a subsequent WIP where
more domains can test the oracle-pattern's portability.  Logged
as a Q5 carry-over.

**Carry-over handle:** `Q5-M11.1-oracle-pattern-port`.

### Artefact 3 — B's strengthened essentiality argument in §4

**Location:** `cycle-11/B-ARGUMENT.md` §4 Drop-ln and other
Drop-X paragraphs.  Cycle #11 framing: "now rigorous obstructions"
(explicit analytic entirety argument for drop-ln, arity for
drop-+, surjectivity for drop-exp, ℝ_{>0} closure for drop-(−1)).

**Decision:** **not-portable.**

**Rationale:** This is a B-deliverable improvement specific to
the EML domain, not a rubric-structural pattern.  It lands as a
within-cycle R6 improvement (see §3 R6 analysis); no rubric
amendment needed for ROOT to score this correctly (the existing
R6 band-3 text already anticipates "constructive bootstrap with
no disclosed gap remaining" and "oracle as '3' indicator").

### Artefact 4 — B's inner evaluator's gap-closure JSON structure

**Location:** `cycle-11/B-eval-iter2-v2.json` has a
`gap_closure_vs_baseline` subtree mapping each baseline gap to a
closure location + note.

**Decision:** **not-portable.**

**Rationale:** This is a B-internal evaluator trace format; ROOT
already has R10 M6.3 (c) `gap-closure-check.schema.json` for this
role in the ROOT-side schema.  B's iteration record is scored
under R10 via M6.3 path (a) (native per-iteration records), not
path (c) (schema-conformant JSON).  No port needed.

### Summary of §5b decisions

- 4 artefacts inspected.
- 0 ported.
- 3 not-portable (rationale each).
- 1 deferred (Q5 handle: Q5-M11.1-oracle-pattern-port).

No step-6 ROOT commit ports arise from §5b this cycle.

---

## §7. §5c Proof-auditor invocation (post-draft gate)

Per CLAUDE.md §6.7 step 5c, the proof-auditor audits the draft
JUDGMENT.md + its supporting X-JUDGMENT-v2.md + the Cycle #11
A/B deliverables against the Cycle #11 rubric, with oracle
catalogue (paper-analysis.md + scripts/meta/oracles/).  Output:
`cycle-11/rubric-audit.json`.

Status transition logic:

- `draft` → `draft` + "Audit concurrence" appendix if
  `arbitration_triggered = false` on all rows (A, B, X-v2).
- `draft` → `arbitration-pending` if any axis triggers
  arbitration (|incumbent − auditor| ≥ 2 on any axis OR ≥ 3 axes
  with any band difference OR binary-axis disagreement OR total
  score diff > 20% of rubric max).

See §8 below for audit concurrence / arbitration outcome.

---

## §8. Audit concurrence

Proof-auditor audit completed 2026-04-23.  Output:
`cycle-11/rubric-audit.json`.

**Summary:**

- **A:** auditor total 20 / 30, incumbent total 20 / 30.  10 / 10
  axes YES.  `arbitration_triggered = false`.
- **B:** auditor total 22 / 30, incumbent total 22 / 30.  10 / 10
  axes YES.  `arbitration_triggered = false`.
- **X-v2:** auditor total 9 / 30, incumbent total 9 / 30.  10 / 10
  axes YES.  `arbitration_triggered = false`.

**Agreement matrix (combined):** 30 YES / 0 CONDITIONAL / 0 NO.

**Notable auditor-verified claims:**

- A R1=3 clears the M10.2 (b) obstruction-sketch bar via §1(a)
  "exp/ln are the only genuinely new data" (irreducibility sketch)
  + §1(c) "transcendental lies on top" (shape-departure sketch).
- B R6=3 is concurred via structural audit of `B-sim-verify.py`:
  16 `np.{trig/inverse/sqrt/power}` references all appear only as
  `ref_fn` arguments to `run_unary` / `run_binary`; zero appear
  inside `prim_*` bodies (grep-verified by auditor).  Oracle
  output (`B-sim-output.txt`) records 35 / 35 PASS at ~1e-15
  error.  The §7 "Formal lower bound" residual is correctly
  scoped as minimality over non-subset alternative 3-element
  bases, not a completeness gap on B*.
- X-v2 R1=2 and R2=2: M10.2 and M10.3 tightenings fire as
  designed.  R1: X cites 5 single-primitive / minimal-generator
  precedents but answer shape (3 primitives + 1 const) does not
  match (a fails) and §1 closure is a strategy statement not an
  obstruction argument (b fails).  R2: §2.2 declares three named
  sublemmas but has no per-sublemma proof blocks; distributed
  discharge via §3 reduction table is excluded by M10.3 (c).
- 8 control axes for X-v2 (R3, R4, R5, R6, R7, R8, R9, R10)
  show zero v1↔v2 shift as expected — confirms rubric discipline
  on axes whose text did not change.

**Shared-bias disclosure (from audit `notes`):** incumbent and
auditor share the Opus 4.7 model lineage.  Agreement on
subjective axes (A's §1 obstruction-sketch reading, B's R6
completeness-vs-minimality scoping, R7 orthogonality / R8
parametric-disclosure calls) is **not** independent evidence of
correctness — it may reflect shared rubric-compliance bias.
Oracle-backed axes (R3/R4/R5/R8-non-inflation/R9 via
paper-analysis.md; R10 via filesystem + sha256 + mtime; B's R6
via `B-sim-verify.py` structural audit) are the high-confidence
ones.  This caveat carries forward from every cycle's audit
`notes` and is unchanged at Cycle #11.

**Status transition:** `draft` with audit concurrence section
appended, per CLAUDE.md §6.7 step 5c.  `arbitration_triggered =
false` on all three deliverables → no arbitration.  Cycle
proceeds to step 6.

---

## §9. Retrospective and re-test references

- **Cycle #11 in-cycle A/B:** this document (§2, §3, §4).
- **X re-test under v2 rubric:** `cycle-11/X-JUDGMENT-v2.md` +
  `cycle-11/falsification-report-v2.md` → global verdict:
  **Partial-capped** (R1 and R2 both cap at band 2 under v2; no
  axis closes to reasoning).
- **Retrospective cycle-10 A/B under v2 rubric:**
  `cycle-10/JUDGMENT-v2.md` → no band shifts; Δ(B−A) stays at
  +1 under v2.
