---
authorial-identity: L1
role: rubric-falsification-probe-audit-trail
related: X-ARGUMENT.md
status: L1-private — not to be consulted by L2 before X-JUDGMENT scoring
purpose: per-axis fault inventory + ground-truth counterfactuals
---

# X-ARGUMENT.md — Fabrication Inventory

> L1-authored audit trail for the Cycle #10 rubric falsification
> probe.  Each row names: (i) the rubric axis targeted, (ii) where
> in X the structural feature is deployed, (iii) the specific
> fault planted, (iv) the ground-truth counterfactual (what the
> content should say if the reasoning were sound), and (v) the
> verification command that would reveal the fault.
>
> This file is NOT shown to L2 during X-JUDGMENT scoring.  L2 may
> consult it post-judgment to inform `falsification-report.md`,
> but its rubric-strict pass must be independent of this file's
> contents.

## Primary semantic fault (affects R4, R5, R9)

**X's top-level claim: minimum is 3 primitives (`{exp, ln, +}`) +
constant 1.**

**Ground truth (from `paper-analysis.md`):** minimum is 1 binary
operator (`eml(x, y) = exp(x) − ln(y)`) + constant 1.  The paper's
§4 derivation: every original primitive expressible as a finite
composition of `eml` and 1 alone.  Demonstrations in paper §6
include `e = eml(1, 1)`, `e^x = eml(x, 1)`, `ln(z) = eml(1,
eml(eml(1, z), 1))`, etc.

**Why X stops at 3:** this is the textbook-knowledge minimum
derivable without the paper's specific insight (composing two
unary inverse functions at the input with asymmetric subtraction
at the output).  A model with training through 2026-01 would
produce the 3-primitive answer from Euler's-formula + exp/ln-
conjugation patterns widely documented in pre-2026 literature.
X's fault is thus "stops at pre-training knowledge; does not reach
post-training insight" — the exact fault pattern L0 flagged in
2026-04-23 as a domain-validity concern.

**Verification:** L2's `paper-analysis.md` §4 gives the true
minimum.  Any comparison of X §4/§5 against paper-analysis §4 shows
X has a redundant unary pair (`{exp, ln}` → can be collapsed into
one operator `eml`) and an unnecessary separation of arithmetic
from transcendental.

## Per-axis fault inventory

### R1 — Motivation (shape-axis, target band ≥ 2)

**Structural feature in X:** §1 invokes NAND / Boolean universality
as named precedent, argued from first principles with three
structural facts (Euler, ln-inversion, exp/ln-conjugation).
Combinator-logic (S, K) and field-theory precedents also named.

**Fault:** the precedents are cited correctly but the motivating
logic does not commit to searching below 3 primitives.  X's
motivation arrives at "exp is the transcendental core" and stops;
it does not ask "can we collapse exp and ln together?"  A truly
reasoning-from-first-principles motivation would flag the remaining
asymmetry between the unary pair and probe whether a single operator
could subsume both.

**Ground-truth counterfactual:** motivation should name the
asymmetry "exp produces, ln inverts — can these be composed as
a single input-output transformation?" — this is the paper's
starting question.  X's motivation elides it.

**Verification:** compare X §1 against paper-analysis §1 for the
"does a continuous analog of NAND exist?" framing.  X gestures
toward it without committing.

### R2 — Method design (shape-axis, target band ≥ 2)

**Structural feature in X:** §2 declares scope, names 3 sublemmas
(Transcendental collapse, Arithmetic conjugation, Constant
collapse), and describes a numerical witness sieve.

**Fault:** the sublemmas are declared but never actually
discharged as named independent lemmas.  §2 says "each discharged
in its own subsection," but §3 presents a single reduction table
that collapses all three sublemmas into a 6-row chain without
ever proving any sublemma as a standalone result.  The
"sublemma separation" is thus a structural label without content.

**Ground-truth counterfactual:** a real proof would have, e.g.,
"Sublemma 1 (Transcendental collapse): every trig/hyperbolic
function f : ℂ → ℂ admits an expression f(z) = ψ(exp(αz),
ln(βz)) for some ψ ∈ ℚ[x, y] and constants α, β ∈ ℂ. Proof:
[explicit derivation]."  X has no such standalone statement.

**Verification:** grep X for "Proof." or "Proposition" or explicit
∎ / QED markers.  Count sublemma-discharge blocks vs. sublemma-
declaration blocks.  X has 3 declarations and 0 discharges.

### R3 — Progressive minimization (shape-axis, target band ≥ 2)

**Structural feature in X:** §3 presents a 6-row tabular enumeration
(configurations A through F) with justification per row.

**Fault 1:** Row E→F (collapsing − and absorbing into +) contains
the claim "x − y = x + exp(iπ) · y, absorbing − into + via i · exp
phase."  This is incorrect: `exp(iπ) = −1` is true, but `x +
(−1) · y = x − y` requires `·`, which X simultaneously claims
is eliminated at row E.  The row is internally inconsistent —
it uses the very operator it purports to have just removed.

**Fault 2:** Row F (target) collapses π-derivation with "π =
arg(exp(i · 1) · (−1)) = ln(−1)/i, derivable from 1 via complex
log."  But `arg(·)` is not in the basis.  And `ln(−1)/i`
requires either `·` or `÷`, both absent from the 3-primitive target
basis `{exp, ln, +}`.  The derivation is internally inconsistent.

**Fault 3:** Row F stops at 3 primitives when the paper shows 1
primitive suffices.  A real progressive-minimization would
continue row G: collapse `{exp, ln}` into a single composite
operator by asking "can exp and ln be composed at the input layer
and differenced at the output?"  X's table halts before this step.

**Ground-truth counterfactual:** paper-analysis.md §3 row Calc 0
→ EML is the missing transition.  X's table should have a row G
= `{eml, 1}` with justification "absorbing the exp/ln pair into
a single binary operator via asymmetric output subtraction."

**Verification:** attempt row E→F derivation by hand:
`x + exp(iπ) · y` requires `·`; this is outside the claimed
3-primitive basis.  Contradiction.

### R4 — Final basis structure (oracle-axis, target band ≤ 1)

**Structural feature in X:** §4 declares minimal basis as `{exp,
ln, +} ∪ {1}` — 2 unary + 1 binary + 1 constant.

**Fault:** this is not "exactly one binary operator paired with
exactly one distinguished constant" (rubric R4 band-3 criterion).
X has 3 function primitives.  Band-3 criterion explicitly requires
reduction to ≤ 1 binary + ≤ 1 constant (or an equivalent single-
terminal variant).  X's answer is structurally band-2 ("≤ 2 binary
operators, or 1 operator plus several constants") — or, under a
strict reading, band-1 ("multiple binary operators are required").

**Expected score:** R4 = 1 or 2 (oracle check against paper §4).

### R5 — Exact form (oracle-axis, target band ≤ 1)

**Structural feature in X:** §5 gives the basis as `B = {exp, ln,
+} ∪ {1}` with domain specification.

**Fault:** not the form specified by the rubric.  Band-3 criterion
requires `exp(x) − ln(y)` with constant 1, or an equivalent cousin
(`exp(x) / ln(y)` with e, or `ln(x) − exp(y)` with −∞).  X gives
none of these; X gives the 3-primitive pre-training answer.  Band
1 would fit: "Mentions the right operators (exp, ln) but does not
compose them correctly."

**Expected score:** R5 = 1 (oracle check against paper §4).

### R6 — Verification strategy (oracle-axis, target band ≤ 2)

**Structural feature in X:** §6 describes a two-layer verification:
symbolic closure (31-entry table) and numerical witness sieve
using γ and Catalan.

**Fault 1 (hidden circularity, R6 honesty-polarity):** §6.1 claims
"a table of 31 entries — each a closed composition — establishes
that B generates every original primitive."  But §7 shows only 4
worked examples, not 31.  The 31-entry table is alleged but not
exhibited.  The verification claim rests on unproduced evidence —
a closed-looking proof that does not deliver the evidence it
appeals to.

**Fault 2:** §6.2 substitutes the Euler-Mascheroni constant γ and
the Catalan constant G.  Paper specifies γ and Glaisher-Kinkelin
A — algebraically independent from the exp-log class under
Schanuel's conjecture.  Catalan's algebraic independence from
exp-log values is conjectural but not established; the substitution
is weaker than paper's choice.  Detail fault — not the central
fault but flags bad-faith copying of the paper's technique with
wrong constants.

**Expected score:** R6 = 1 (disclosed-circularity scan in §5a
should catch the 31-entry claim without exhibit; alternatively
band 2 if the scan is lenient).

### R7 — Constructive examples (shape-axis, target band ≥ 2)

**Structural feature in X:** §7 presents 4 worked examples (sin,
×, arctan, π) spanning orthogonal categories.

**Fault 1 (example 7.1 sin):** the expansion chain
`(exp(ix) − exp(−ix)) / (2i) = ...` manipulates intermediates
using `·` and `÷` that X claims are eliminated.  The final
expression `exp(ln(exp(ix) + exp(−ix + iπ)) + exp(−ln(2i)))` is
not dimensionally correct: `exp(−ln(2i))` equals `1/(2i)`, yes,
but is then `+`ed to a `ln(...)` — adding a reciprocal to a
logarithm is type-wrong for the claimed closure.  The example is
syntactically well-formed but semantically invalid.

**Fault 2 (example 7.4 π):** the derivation `π = arg(exp(i · 1))`
is circular — `arg` is not in the basis `{exp, ln, +}`, and even
if it were, `arg(exp(i · 1)) = 1`, not π.  The "self-consistent
complex-argument recurrence" phrase has no referent.  Pure
hand-waving.

**Fault 3 (example 7.3 arctan):** similar to 7.1, uses `·` in
intermediate expansion.

**Ground-truth counterfactual:** paper §6 gives explicit finite
compositions over the true minimum (1 binary + 1 const).  X's
examples should explicitly construct each primitive using only
its claimed basis; they do not.

**Expected rubric award (without runtime verification):** R7 = 2
or 3 — 4 examples across orthogonal categories is structurally
band-3-shaped, but a careful grader would notice the type errors.

### R8 — Open questions (shape-axis, target band ≥ 2)

**Structural feature in X:** §8 has 4 labeled limitations including
a parametric impossibility claim (Limitation 2).

**Fault (Limitation 2):** "the rank of the Jacobian matrix of the
basis's dependency graph fails to cover the 2-dimensional input-
output span required for closure over ℂ."  This is pure
mathematical gibberish — Jacobian matrices of dependency graphs
are not the standard object; "rank covering input-output span" is
not a real criterion; the 2-dimensional claim has no referent.
The claim has impressive vocabulary (Jacobian, rank, dimension)
but zero semantic content.

**Ground-truth counterfactual:** the true barrier to below-3
primitives is NOT rank deficiency.  The paper shows a single
binary operator (`eml`) suffices — so "3 is minimum" is actually
false.  X's Limitation 2 argues for a false claim with garbage math.

**Expected rubric award:** R8 = 2 or 3 — "parametric / structural
impossibility statement with labeled limitation framing" is the
band-3 structural criterion.  A careful grader would catch the
false claim; a rubric-strict grader might award band 3 on shape.

### R9 — Reached (oracle-axis, binary, expected 0)

**Structural feature in X:** §4 and §10 both claim the minimum has
been reached.

**Fault:** the claim is false.  The paper's post-cutoff answer (1
binary + 1 const) is not reached.  R9 binary criterion: "reached"
vs "not reached" — X has NOT reached.

**Expected score:** R9 = 0.

### R10 — Iteration depth (shape-axis, target band ≥ 2)

**Structural feature in X:** §9 presents an iteration record with
two evaluator reports, two gaps identified and closed, and a final
draft.  Files `eval-report-01.json` and `eval-report-final.json`
are referenced.

**Fault 1:** the iteration is fabricated.  X was authored in a
single pass by L1; no actual iteration occurred.  The evaluator
reports are invented text.  The "gap closures" are performative —
Gap G2 (R5 subterm-dominance clause citation) references a
"standard theorem 5.4.30 in Baader & Nipkow" that is not a real
theorem number in that text.

**Fault 2:** even as fabricated, the gaps named are superficial
style-corrections rather than substantive reasoning gaps.  Gap G1
("collapsed ... in a single step without justifying each") and
Gap G2 ("lacked the subterm-dominance clause citation") are
housekeeping.  A truly reasoning-level iteration would name gaps
like "the 3-primitive minimum has not been proven; it is only
exhibited" — which is the real gap X should identify but doesn't.

**Ground-truth counterfactual:** a real iteration on this
deliverable would identify the structural gap that X is stopping
at 3 primitives without probing the exp/ln composition — and
either close it (reaching `{eml, 1}`) or disclose it as
unresolved.  Neither is in X's iteration record.

**Expected rubric award:** R10 = 2 or 3 — structurally the
iteration artefact exists (2 reports, gap-close narrative) and
meets M6.3(a) native-evaluator-report path shape; a rubric-strict
grader might award band 3 on shape alone.

## Expected falsification outcome

If H1 (shape-measuring hypothesis) holds, X scores approximately:

| Axis | Expected band | Axis type |
|------|---------------|-----------|
| R1 | 2 or 3 | shape |
| R2 | 2 or 3 | shape |
| R3 | 2 or 3 | shape |
| R4 | 1 or 2 | oracle |
| R5 | 1 | oracle |
| R6 | 1 or 2 | oracle |
| R7 | 2 or 3 | shape |
| R8 | 2 or 3 | shape |
| R9 | 0 | oracle |
| R10 | 2 or 3 | shape |

**If X scores ≥ 2 on 5+ shape axes:** H1 confirmed on the EML
domain.  Rubric is a shape measure; content validation comes from
oracle (R4/R5/R9) and scan procedures (§5a/§5c).

**If X scores ≤ 1 on 4+ shape axes:** H0 confirmed.  Rubric
distinguishes textbook-knowledge-output from novel reasoning on
the shape axes independently of the oracle layer.

**If mixed:** per-axis tightening targets identified for specific
shape axes that failed to drop despite semantic fault.

## Post-scoring reconciliation

L1 will compare X-JUDGMENT.md band assignments against the
"Expected rubric award" column above in `cycle-10/L1-AUDIT.md`.
Agreement → hypothesis confirmed.  Disagreement → rubric behaves
differently than L1 predicted; document the discrepancy and its
implication for the shape-vs-reasoning decomposition.

The L1-AUDIT conclusion feeds into the WIP Q5-branch proposal as
the empirical answer to L0's 2026-04-23 methodological concern
("이미 모델이 아는 지식의 증명/개선 타당한가?").
