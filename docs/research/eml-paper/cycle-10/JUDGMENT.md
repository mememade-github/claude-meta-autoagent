---
status: draft
cycle: 10
domain: minimal-generating-basis-for-elementary-calculator-functions
auditor: proof-auditor
auditor_date: 2026-04-23
arbitration_triggered: false
incumbent_total_A: 20
incumbent_total_B: 21
incumbent_total_X: 11
auditor_total_A: 20
auditor_total_B: 21
auditor_total_X: 11
agreement: 30_YES_0_CONDITIONAL_0_NO
audit_file: cycle-10/rubric-audit.json
rubric_version: cycle-10 (identical to cycle-09 rubric state; no R-axis ports at cycle-10 pre-cycle)
falsification_test: m9.4 (procedures/falsification-test-v1.md)
falsification_report: cycle-10/falsification-report.md
---

# Cycle 10 — JUDGMENT

Grading of `docs/research/eml-paper/cycle-10/A-ARGUMENT.md` and
`docs/research/eml-paper/cycle-10/B-ARGUMENT.md` against
`docs/research/eml-paper/judgment-rubric.md` (R1–R10, total 30
points) under the Cycle #10 rubric state — identical to Cycle #9
rubric state (Cycle #10 pre-cycle commit `b2b284e` introduced no
R-axis band-text edits).

This cycle additionally runs the M9.4 rubric falsification test per
`docs/research/eml-paper/procedures/falsification-test-v1.md`.  The
probe deliverable X is scored independently in
`X-JUDGMENT.md`; per-axis and global verdicts are recorded in
`falsification-report.md`.

Front-matter `status` will transition per CLAUDE.md §6.7 step 5c
after the proof-auditor pass.

---

## §0. Cycle artefacts (audit record)

Captured at cycle close (2026-04-23 ~17:56 JST).

| Path | mtime | Bytes | sha256 prefix | Role |
|------|-------|------:|:-------------:|------|
| `docs/research/eml-paper/cycle-10/TASK.md` | 17:27 | 2684 | — | Operative TASK prompt (rubric-blind; verified) |
| `docs/research/eml-paper/cycle-10/A-ARGUMENT.md` | 17:34 | 21594 | d2f68dea7a34e7c8 | A deliverable (single-shot) |
| `docs/research/eml-paper/cycle-10/B-ARGUMENT.md` | 17:51 | 20189 | 7e34be66a9381001 | B deliverable (iteration 1, accepted) |
| `docs/research/eml-paper/cycle-10/B-iter-0-baseline.md` | 17:47 | 16379 | 2aac82a863c822e4 | B iteration 0 baseline |
| `docs/research/eml-paper/cycle-10/B-iter-1-accepted.md` | 17:53 | 20189 | 7e34be66a9381001 | B iteration 1 accepted (== final ARGUMENT.md) |
| `docs/research/eml-paper/cycle-10/B-refine-attempts.jsonl` | 17:53 | 671 | e8765e4f5fcb2be5 | B /refine evaluator trace (2 iteration records) |
| `docs/research/eml-paper/cycle-10/X-ARGUMENT.md` | 17:26 | 13058 | (L1 probe) | X deliverable (L1-authored rubric-falsification probe; scored in X-JUDGMENT.md) |
| `docs/research/eml-paper/cycle-10/X-fabrications.md` | 17:26 | 14689 | (L1 audit trail) | NOT consulted during rubric-strict X scoring |

**Execution timing (UTC+09:00).**

- A launched 17:28:57 via `delegate-sub.sh a`; first launch completed
  normally; A produced single-shot ARGUMENT.md at 17:34 (21594 B)
  and exited.  No Cycle #10 iterations or evaluator reports.  Stale
  Cycle #7/#8/#9 artefacts under `task/attempts/` and `task/iterations/`
  (Apr 22 mtime) remain, untouched.
- B's first launch at 17:29:01 died silently after ~8 min with 0 B
  agent log output (known Cycle #8-style overlaunch/hang remediation
  applicable).  Relaunch at 17:36:49 produced no output; container
  restart at 17:41 (docker restart), credentials re-bootstrapped,
  third launch at 17:41:27 ran to completion.
- B iteration 0 draft at 17:47 (16379 B), iteration 1 candidate at
  17:52 (20189 B), iteration 1 accepted at 17:53 (20189 B), final
  ARGUMENT.md at 17:51 (20189 B).  `/refine` log
  `refine-20260423-174428.jsonl` has two iteration records
  (iter 0 score 0.80 with gaps [R2,R3,R4,R6]; iter 1 score 0.89 with
  gaps [] and `regression: none`).  Exit summary: "Deliverable
  complete. `/refine` loop ran 2 iterations (baseline + 1 keep).
  Score: 0.89 ≥ threshold 0.85, accepted."

**Remediation history (Cycle #8-#9 pattern applied):** B's silent-exit
on first-two-launches was resolved by docker restart + credential
re-bootstrap.  Single-launch failure is consistent with the
Cycle #8/#9 remediation pattern.  Third launch succeeded and
produced native M6.3 (a) iteration artefacts.

**Oracle-backed mechanical verification (paper-analysis.md).**
`docs/research/eml-paper/paper-analysis.md` is ROOT's oracle for
R4/R5/R9 in the EML domain: paper's minimum is `eml(x, y) = exp(x)
− ln(y)` with constant `1` (or cousin variants `edl` / `−eml`).  A
reaches `{−1, +, ×, exp, ln}` (5 primitives) or `{i, +, exp, ln}`
(4 primitives relaxed); B reaches `{+, exp, ln, −1}` (4 primitives).
Neither reaches the paper's 1-binary + 1-constant form.

---

## §1. Leak audit

```
bash scripts/meta/paper-leak-audit.sh
     docs/research/eml-paper/cycle-10/A-ARGUMENT.md
bash scripts/meta/paper-leak-audit.sh
     docs/research/eml-paper/cycle-10/B-ARGUMENT.md
```

Result: both pass (`Paper-leak audit passed` for each).  Neither
A nor B contains the paper-identifying keywords (`eml`, `Odrzywolek`,
`Sheffer`, `2603.21852`) or the derived-from-paper motivation form
`exp(x) - ln(y)` in the motivation section.  No disqualification.

Cycle #10 **leak streak 10**: Cycles #1–#10 all clean across the
restricted keyword set.

---

## §2. Agent A score: 20 / 30

### R1 Motivation — **3**

A §1 names three structural precedents argued from first principles:

- **§1(a) Duplicated inverses.**  "A calculator ships `sin` with
  `arcsin`, `exp` with `ln`, `square` with `sqrt`, `×` with `÷`,
  `pow` with `log_x(y)`.  Every such pair is a function and its
  local inverse.  ... `exp` / `ln` are the only genuinely new
  data; the other 'inverses' are expressible once a single complex
  unit is available."  — reduction-under-inversion precedent.
- **§1(b) Real vs complex.**  "Over ℂ they are the same object:
  the identity `e^{ix} = cos x + i sin x` splits the exponential
  on the imaginary axis into its real and imaginary parts.  Admitting
  i collapses a whole tower of primitives onto one." — named
  structural identity.
- **§1(c) Algebraic minimality of fields.**  "A field is generated
  by two operations, `+` and `×`, plus one constant that is not a
  root of its prime subfield.  Arithmetic of ℂ has a similar
  minimal backbone; everything transcendental lies on top." —
  **field-generation structural precedent**, an "equivalent named
  example" per the band-3 rubric clause (analogous to
  combinators / OISC / Boolean universality as minimal-basis
  precedents in other domains).

Band 3 text: "Clear structural precedent — Boolean universality via
a single two-input gate, or an equivalent named example ..., argued
from first principles."  A's §1(c) is an equivalent named
minimal-basis precedent (field generation) argued from first
principles; §1(a) and §1(b) supplement with derivation-under-
inversion and real/complex-fusion structural facts.

### R2 Method design — **3**

A §2 names four explicit reduction rules:

- **R1 (Algebraic elimination).** Remove f if f equals an expression
  over remaining basis.
- **R2 (Inverse via exp/ln).**  Given {+, ×, exp, ln, i}, inverse
  transcendentals unfold into logarithmic formulas.
- **R3 (Constant consolidation).**  Remove c if c is in closure of
  remaining basis applied to empty variable list.
- **R4 (Operation consolidation).**  Strict vs relaxed distinction
  made explicit.

Scope declared via R4's strict-vs-relaxed convention.  A §3.6
additionally provides four **named structural obstruction
arguments** under distinct proof tools:

- **(i) exp is irreducible over {+, ×, ln, constants}** — growth
  argument (algebraic-logarithmic expressions can't match `exp`'s
  super-polynomial growth).
- **(ii) ln is irreducible over {+, ×, exp, constants}** —
  branch-point argument (entire-function compositions can't match
  `ln`'s essential singularity-type at 0).
- **(iii) + is irreducible over {×, exp, ln, constants}** —
  cardinality / 2πi-modular argument.
- **(iv) × is irreducible over {+, exp, ln, constants} as a total
  function** — zero-locus argument.

Each obstruction is discharged in its own sub-paragraph with a
distinct structural tool.  Cycle #7 band-3 tightening (named
sublemma separation under distinct tools) met.  Scope declared
via R4 strict-vs-relaxed distinction.

Verification via §5 three-stage (forward synthesis, numerical
cross-check, strict-minimality audit).

### R3 Progressive minimization — **3**

A §3 presents **six** progressively-smaller configurations
B₁ → B₂ → B₃ → B₄ → B₅ → B₆, each **with a deliverable-side
reduction table** (disposition column = witness):

- §3.1 B₁ (11 rows): each removal paired with explicit witness.
  E.g. "`log_x(y) | ln(y) ÷ ln(x)`", "`pow(x,y) | exp(y · ln(x))`".
- §3.2 B₂ (11 rows): Euler collapse; each trig / hyp / inverse with
  its explicit exp/ln formula.
- §3.3 B₃ (2 rows): `−` and `÷` reduced.
- §3.4 B₄ (5 rows): constants `−1, 1, 2, e, π` derived from `i`.
- §3.5 B₅ (3+ rows): constants derived from `−1`.
- §3.8 B₆ (relaxed, §3.8 prose + basis listing).

Non-inflation check: spot-verified rows across §3.1–§3.5.  All
witnesses are correct standard identities (e.g., §3.4 "π =
(i·i·i) · ln(i·i)" verifies since `i·i·i = −i` and `ln(i·i) = ln(−1)
= iπ`, so `(−i)·(iπ) = π`).  No fabricated rows; no oracle-
unverifiable rows.  Cycle #9 locus clarification satisfied:
deliverable-side tabular enumeration with disposition column, one
row per element of the finite support (primitives / constants).

### R4 Final basis structure — **2**

A §4 commits to the **strict recommended minimum**:

> "constant: −1; binary: +, ×; unary: exp, ln — five primitives:
> one constant, two binary operations, two unary operations."

§3.8 reports the **relaxed minimum**: `B₆ = { i, +, exp, ln }` —
four primitives (1 binary, 2 unary, 1 constant), at the cost of
making multiplication partial at the coordinate axes.

Paper's answer (oracle: `paper-analysis.md`): `eml(x, y) = exp(x) − ln(y)`
with constant 1 — **one binary operator + one constant** (2 symbols).

A has 2 binary (strict) or 1 binary + 2 unary (relaxed), plus
unary helpers.  Band 3 requires "exactly one binary operator paired
with exactly one distinguished constant" — A has additional unary
primitives.  Band 2 fits: "Reduces to ≤ 2 binary operators" (strict
has 2; relaxed has 1).  Band 1 does not fit (A does not claim
multiple binary operators are required — relaxed achieves 1).

### R5 Exact form — **1**

A's basis uses `{+, ×, exp, ln, −1}` (or `{+, exp, ln, i}` relaxed)
— four or five **separate primitives**.  A composes exp and ln
correctly in expressions (`exp(ln x + ln y) = x · y` in §3.8,
`exp((−1)·ln(y)) = 1/y`) but does not propose a **single binary
operator** of the form `exp(x) − ln(y)` (or a cousin variant
`edl`, `−eml`) paired with a single constant.

Band 1 text: "Mentions the right operators (exp, ln) but does not
compose them correctly."  A mentions and composes them correctly
in multi-primitive form; the band-1 text is the closest fit
because A does not reach the single-binary-operator form that
band 2/3 contemplate.  Band 2 ("a form close to `exp(x) − ln(y)`
but not exact") requires a proposed **single binary** form; A has
none.

### R6 Verification strategy — **2**

A §5 has three stages:

- **Stage A forward synthesis.**  Mechanical substitution: replace
  each primitive by its witness, repeatedly, until only B₅ symbols
  remain.  Termination argued by occurrence-count decrease.
- **Stage B numerical cross-check.**  Generic inputs {x_k} ⊂ ℂ
  avoiding branch cuts / singularities, evaluate f(x_k) and T_f(x_k)
  with independent `{exp, ln, +, ×}` implementations, compare up
  to floating-point tolerance.  Equality on Zariski-dense set
  extends to full common domain via meromorphy.
- **Stage C strict-minimality audit.**  §3.6 + §3.7 obstruction
  arguments bound the minimum from below.

§5a disclosed-circularity scan (A) — see §5a below — no hidden
circularity detected.

**§7(2) disclosed gap.**  "We have not found a way to obtain `×`
as a total function from `{+, exp, ln, constants}` alone, but have
not proved it impossible with complete rigour either: the argument
in Section 3.6(iv) rules out the natural exp/ln trick and
continuous extensions thereof, but a more elaborate composition
using cancellations has not been formally excluded."

**R6 polarity mapping.**  Disclosed gap (§7(2)) → band 2 (per
rubric R6 honesty-polarity).  No numerical-sieve with algebraic-
independence (Schanuel) argument explicitly; verification is
symbolic + numerical cross-check + structural.  Band 3 requires
"numerical sieve with algebraic-independence argument ... with no
disclosed gap remaining"; A has a disclosed gap in §7(2).

### R7 Constructive examples — **3**

A §6 has **four worked examples**, each using only basis B₅ after
shorthand expansion:

- **Example 1 arctan.** `arctan(x) = ln((1+i·x)/(1−i·x)) / (2i)`
  expanded to `ln( (1+i·x) · exp((−1)·ln(1−i·x)) ) · exp((−1)·ln(2·i))`.
  Uses exp, ln, +, ×, (−1), with i derived via §3.5.  Inverse-
  transcendental category.
- **Example 2 pow.** `pow(x, y) = exp(y · ln(x))`.  Uses exp, ln, ×.
  Hyperoperation category.
- **Example 3 hypot.** `hypot(x,y) = exp(ln((x·x)+(y·y)) ·
  exp((−1)·ln(1+1)))`.  Uses exp, ln, +, ×, (−1).  Composite
  arithmetic category.
- **Example 4 sin.** `sin(x) = (exp(i·x) + (−1)·exp((−1)·(i·x))) ·
  exp((−1)·ln(i+i))`.  Uses exp, ln, +, ×, (−1), i.  Transcendental
  category.

Cycle #7 tightening: ≥ 4 examples OR ≥ 3 orthogonal.  A has 4,
spanning inverse-transcendental, hyperoperation, composite-
arithmetic, transcendental — orthogonal categories.  Each example
uses only the proposed basis (per A's shorthand expansion note at
§6 opening).  Band 3 met by the ≥4 path.

### R8 Open questions — **3**

A §7 (dedicated section header "Open questions and limitations") has
**six** numbered disclosures:

1. **Branch choices.** "The minimal basis *depends on the branch
   choice*." — domain-limit disclosure.
2. **Zero and the partial-vs-total distinction.** — disclosed-gap
   ("not proved with complete rigour either") about × totality.
3. **Uniqueness of the minimum.** "Every non-real-non-positive seed
   `c ∈ ℂ ∖ ℝ_{≥0}` works: the general form is
   `{c, +, ×, exp, ln}`." — **parametric characterization** of
   valid seeds.
4. **Alternative operation pairs.** — scope disclosure about
   swapping exp/ln for trig/arctrig pairs.
5. **Beyond elementary functions.** — scope disclosure about
   non-elementary enlargements.
6. **Variables and constants on the same footing.** — convention
   disclosure about whether variables-as-inputs count.

Cycle #7 tightening: ≥ 3 distinct disclosures + ≥ 1 structural /
parametric.  §7(3) parametric characterization "every non-real-
non-positive seed" qualifies; §7(2) is a disclosed impossibility-
status about × totality.

Cycle #9 labeling clarification: dedicated section header
"Open questions and limitations" + individual numbered items with
descriptive labels.  Label test passes.

Non-inflation: no false impossibility claim.  §7(2) is honest
about its own incompleteness.

### R9 Exact answer match — **0**

Rubric is binary: 0 if not "one binary + one constant" in
eml / edl / −eml form; 3 if so.

A's strict basis is `{−1, +, ×, exp, ln}` (5 primitives); relaxed
is `{i, +, exp, ln}` (4 primitives).  Neither is a
single-binary-operator + single-constant form.

Oracle (paper-analysis.md): paper's answer is `eml(x, y) = exp(x)
− ln(y)` with constant 1 (or cousins).  A does not reach this
form.  R9 = 0 (no partial credit).

### R10 Iteration depth — **0**

A's `task/` on disk at cycle-close:

- `task/ARGUMENT.md` — 21594 B, mtime 17:34:23 (single substantive
  write during A's Cycle #10 window 17:28–17:34).
- `task/attempts/`, `task/iterations/` — stale Cycle #7/#8 files
  (Apr 22 mtime), untouched.
- `task/sim.py`, `task/sim_output.txt` — stale Apr 22 mtime.
- No Cycle #10 `.eval-report-*.json`; no Cycle #10 iteration-
  separate evaluator artefact.

**Band 0: single-shot write with no on-disk trace of deliberation
between emissions.**  Bands 1–3 all require ≥ 1 disclosed gap in
an iteration-separate artefact.  A's architecture has no
iteration affordance (baseline Karpathy-skills-only, no `/refine`,
no evaluator agent).

R10 = 0 by architectural design for A.  Non-inflation: no
iteration, no new gaps.

### A total: 3 + 3 + 3 + 2 + 1 + 2 + 3 + 3 + 0 + 0 = **20 / 30**

---

## §3. Agent B score: 21 / 30

### R1 Motivation — **2**

B §1 opens with three **collapse mechanisms** plus a fourth
"algebraic vs transcendental split":

- **Additive vs multiplicative duality.** "Multiplication, division,
  powers, and roots are all the additive structure of the reals
  (or complex numbers) transported through the `exp/ln`
  isomorphism `ln : (ℝ_{>0}, ×) → (ℝ, +)`."  — named structural
  isomorphism.
- **Inverse-function pairs.** "Every inverse trig/hyperbolic
  function is algebraically expressible by `ln` and `sqrt(·)`...
  because `sin, cos, tan` are rational functions of `e^{ix}`." —
  structural mechanism (Euler-via-series).
- **Complex extension.** "Euler's identity `e^{iθ} = cos θ + i sin θ`
  ... merges circular and hyperbolic functions with `exp`." —
  named identity.
- **Algebraic vs transcendental split.** — structural dichotomy.

The mechanisms are substantively correct and structurally
motivated.  **However, none is a named external structural-
minimality precedent** of the band-3 exemplar type ("Boolean
universality via a single two-input gate, or an equivalent named
example: combinators, one-instruction computers, Wolfram's single
axiom").  B's mechanisms are **internal structural facts about
the calculator's primitives** (exp/ln isomorphism, Euler, alg-vs-
transcendental) — these function as "adequate analogies or partial
precedents" (band 2), not as a "clear structural precedent"
(band 3).

Comparison to A: A §1(c) invoked field-generation as an
equivalent named minimal-basis precedent (two operations + one
constant minimal backbone for fields).  B lacks an equivalent
named external minimal-basis precedent.

Band 2 fits: "Adequate analogy or partial precedent (e.g.
'polynomial basis')."  B's exp/ln-isomorphism named structural
fact is adequate.

### R2 Method design — **3**

B §2 has **eight numbered reduction steps**, each stating the
identity used:

1. Eliminate derived arithmetic (−, ÷, halve, mean, hypotenuse,
   square via +, ×, sign seed).
2. Eliminate multiplicative via exp/ln (×, 1/a, √a, pow, log_x).
3. Eliminate hyperbolic (cosh, sinh, tanh).
4. Eliminate trig via Euler (cos, sin, tan with i).
5. Eliminate inverse hyperbolic (logarithmic forms).
6. Eliminate inverse trig (logarithmic forms from Euler).
7. Eliminate sigmoid (rational of exp).
8. Eliminate constants (seed `−1` → all constants).

B §4 "Essentiality" discharges four **named structural
impossibility arguments** under distinct tools:

- **Drop +.** Arity argument: "all other primitives (exp, ln) are
  unary, so the set of expressible functions in x, y collapses to
  unary compositions on a single variable."
- **Drop exp.** Surjectivity / inverse-of-ln argument.
- **Drop ln.** **Analytic entirety argument** (Cycle #10 B-specific
  closure): "let `T` be the term algebra generated by
  `{+, exp, −1, x, y}`.  ... every `f ∈ T` is entire on its
  complex-analytic domain — no branch points, no poles.  But
  `1/x` has a pole at 0, so `1/x ∉ T`; `sqrt(x)` has a branch point
  at 0, so `sqrt(x) ∉ T`; `ln` itself has both.  This is a clean
  analytic obstruction: removing ln forecloses an entire class of
  required primitives."
- **Drop −1.** ℝ_{>0} closure argument: "exp(ℝ) ⊂ ℝ_{>0}, and +,
  exp, ln preserve ℝ_{>0} (given positive variables).  We cannot
  reach −1, i, or π."

Four distinct proof tools — arity, surjectivity, analytic entirety,
ℝ_{>0} closure — each named and discharged in its own sub-paragraph.

Cycle #7 band-3 tightening: named sublemma separation under distinct
tools.  §4's four Drop-X arguments qualify.  Scope declared via §4
signatures + §7 real-vs-complex domain discussion.

### R3 Progressive minimization — **2**

B §3 has **four progressive stages**: Stage A ~12 elements, Stage B
6, Stage C 5, Stage D 4 (minimal).  Each stage described in
**prose + embedded reductions**, not in tabular form.  Stage D
§3 closing includes a completeness-sketch table (6 rows:
primitive-class / reached-via), but this is §3's concluding
coverage check, not the progression enumeration.

Cycle #9 R3 locus clarification: "when the enumeration has finite,
tractable support, band 3 requires **deliverable-side** tabular
presentation — one row per element of the support with an explicit
disposition column, inside the ARGUMENT.md text."

The "support" for R3 is the progression sequence
(Stage A → B → C → D).  B presents these in prose subsections, not
as a deliverable-side table with per-row disposition column.  This
is the A-prose-vs-B-table boundary that Cycle #9 clarified.  Cycle
#10 B is on the *prose* side; Cycle #10 A is on the *table* side
(A §3.1–§3.5 has per-step tables).

Band 2 text: "3+ steps with brief justification."  B has 4 stages
with brief per-stage justification.  Band 2 fits.  Band 3 requires
tabular presentation per locus clarification; B's §3 is prose.

Comparison to A: A has five per-step reduction tables (§3.1 B₁
11 rows, §3.2 B₂ 11 rows, §3.3 B₃ 2 rows, §3.4 B₄ 5 rows, §3.5 B₅
3+ rows).  A R3 = 3; B R3 = 2.

### R4 Final basis structure — **2**

B §4 commits: `B* = {+, exp, ln, −1}` — four elements (1 binary +
2 unary + 1 constant).  Alternative: `{+, exp, ln, i}`.

Paper's answer (oracle): 1 binary + 1 constant (eml / cousin form).
B's basis has **additional unary helpers** (exp, ln).  Band 3
requires "exactly one binary operator paired with exactly one
distinguished constant" — B has 2 unary helpers beyond that.

Band 2 fits: "≤ 2 binary operators" (B has 1 binary).

Same score as A under strict reading (both have 1 binary + unary
helpers + 1 constant in the relaxed form).

### R5 Exact form — **1**

B §5 provides a "derived toolkit" composing exp, ln, + into
`−a := exp(ln(−1) + ln a)`, `a·b := exp(ln a + ln b)`,
`a/b := a · exp(−ln b)`, etc.  These are correct compositional
definitions but **do not form a single binary operator** of the
eml form `exp(x) − ln(y)`.

B mentions the right operators (exp, ln) and composes them
correctly (band 1+).  B does not propose a single-binary-operator
form (band 2/3 blocked).

Band 1 fits, same as A.

### R6 Verification strategy — **2**

B §5 verification strategy:

> "A reader verifies by (i) confirming each formula is a syntactic
> composition of `{+, exp, ln, −1, x, y}`, and (ii) checking the
> identity using standard calculus identities (Euler, logarithmic
> forms), each derived inline in §2."

No numerical sieve; no algebraic-independence argument.  Pure
symbolic verification via §2 identity derivations + §5 primitive
table.

§5a disclosed-circularity scan (B) — see §5a below — no hidden
circularity detected.

**Disclosed gaps in §7.**

- **§7 "Real-vs-complex domain."** "no closed real formula recovers
  `sin` from `{+, exp, ln, −1, π}` by finite composition without
  power series, so the real-only analogue may require an additional
  trig primitive.  This is an **open question**."
- **§7 "Formal lower bound."** "The essentiality argument in §4 is
  a structural/semantic argument (set-closure considerations), not
  a theorem in a fully formalized term algebra.  A rigorous lower
  bound would fix a term-algebra signature, a composition cost,
  and a generation relation, then prove by induction that no
  3-element subset generates the full primitive set.  **We assert
  this holds but have not written the induction.**"

Two disclosed gaps.  R6 polarity: disclosed gap → band 2 (not
band 1 hidden circularity, not band 3 no-gap-remaining).

Same score as A (both band 2 via disclosed gap).

### R7 Constructive examples — **3**

B §6 has **three worked examples**:

- **Example 1 multiplication.** `x · y = exp(ln x + ln y)`.
  Syntax tree: `exp( + ( ln(x), ln(y) ))`.  Arithmetic-via-
  logarithmic category.
- **Example 2 cos.** Build `i = exp((1/2) ln(−1))` first.  Then
  `cos x = (1/2)(exp(i x) + exp((−i) x))` fully expanded using
  `−i = (−1) · i`, `1/2 = exp(−ln 2)`, `·` = `exp(ln · + ln ·)`.
  Euler-in-complex category.
- **Example 3 arctan.** Full derivation from
  `y = tan x = (u²−1)/(i(u²+1))` to
  `arctan y = (1/(2i)) ln((1+iy)/(1−iy))`, then expanded to
  `(−1)·i·exp(−ln 2)·ln(exp(ln(1+iy) − ln(1−iy)))`.  Inverse-via-
  logarithmic category.

Each example uses only B* = {+, exp, ln, −1, x, y} after shorthand
expansion (the "derived toolkit" in §5 is the expansion table).

Cycle #7 tightening: ≥ 4 examples OR ≥ 3 that span orthogonal
failure / success modes.  B has 3 examples spanning:

- mult: `exp(ln + ln)` arithmetic pattern.
- cos: Euler complex-exponential pattern.
- arctan: inverse-via-logarithmic pattern.

**Orthogonality check.**  Removing mult: no exhibition of
`exp(ln + ln) = ·`.  Removing cos: no exhibition of Euler complex.
Removing arctan: no exhibition of inverse logarithmic form.  Each
example exhibits a distinct reduction pattern that the other two
do not.  Band 3 via ≥ 3 orthogonal modes.

### R8 Open questions — **3**

B §7 (dedicated section header "Open questions and limitations") has
**seven** distinct disclosures:

1. **Branch cuts.** — domain-limit disclosure.
2. **Domain restrictions.** — scope-limit disclosure.
3. **Real-vs-complex domain.** — **open question** about real-only
   basis insufficiency.
4. **Variables as basis elements.** — convention disclosure.
5. **Uniqueness of the basis.** — **parametric characterization**
   of equivalent seeds: "any single complex seed `z_0 ∉ ℝ_{>0}`
   whose principal ln is a rational multiple of iπ can replace
   −1."
6. **Cardinality vs depth minimality.** — methodological disclosure.
7. **Formal lower bound.** — **disclosed incompleteness** of the
   impossibility proof.

Cycle #7 tightening: ≥ 3 distinct + ≥ 1 structural / parametric.
§7(5) parametric-seed characterization qualifies.  §7(3) and §7(7)
add named open questions about the impossibility class.

Cycle #9 labeling clarification: dedicated section header + bold
descriptive labels per item.  Label test passes.

Non-inflation: no false impossibility claim.  §7(7) is explicit
about the formal lower bound being open.

### R9 Exact answer match — **0**

B's `B* = {+, exp, ln, −1}` is not a single-binary + single-constant
form.  Oracle (paper-analysis.md): paper's answer is `eml(x, y) =
exp(x) − ln(y)` with constant 1 (or cousins).  B does not reach
this form.  R9 = 0.

Same score as A.

### R10 Iteration depth — **3**

B's on-disk iteration trace:

| Path | mtime | Bytes | sha256 prefix | Role |
|------|-------|------:|:-------------:|------|
| `cycle-10/B-iter-0-baseline.md` | 17:47:XX | 16379 | 2aac82a8 | iter 0 baseline draft |
| `cycle-10/B-iter-1-accepted.md` | 17:53:XX | 20189 | 7e34be66 | iter 1 accepted (== final ARGUMENT.md) |
| `cycle-10/B-ARGUMENT.md` | 17:51:44 | 20189 | 7e34be66 | final deliverable |
| `cycle-10/B-refine-attempts.jsonl` | 17:53:XX | 671 | e8765e4f | /refine evaluator trace (2 iter records) |

**Per-iteration evaluator records** (from `B-refine-attempts.jsonl`):

```json
{"iter":0,"score":0.80,"gaps":["R2","R3","R4","R6"],"result":"BASELINE",
 "feedback":"Fully expand Examples 2 and 3 into literal {+, exp, ln, −1, x, y}
 syntax trees with zero abbreviations, and give a rigorous per-element
 essentiality argument for ln"}
{"iter":1,"score":0.89,"gaps":[],"result":"KEEP+ACCEPT",
 "feedback":"iter1 closed R2/R3/R4/R6 via entireness essentiality argument,
 expanded Euler/pow/log_x derivations, DAG-form worked examples, pow/log_x
 branch notes","regression":"none"}
```

**Reasoning-delta enumeration** (per rubric R10 evidence requirement):

- **Gap G1 (named in iter-0 evaluator report as axis R2/R3/R4/R6
  feedback "rigorous per-element essentiality argument for ln"):**
  closed in iter-1 via the **analytic entirety argument** in §4
  Drop-ln (the term algebra over `{+, exp, −1, x, y}` is entire;
  reciprocal/sqrt/arctan are not entire).  Byte-range: §4
  "Drop ln" paragraph grew from 6 lines (iter-0) to 12 lines
  (iter-1, detailed analytic argument).
- **Gap G2 (iter-0 feedback: "Fully expand Examples 2 and 3 into
  literal ... zero abbreviations"):** closed in iter-1 via
  DAG-form Example 2 (cos) and Example 3 (arctan) in §6.
  Byte-range: §6 grew from ~40 lines (iter-0) to ~60 lines
  (iter-1).
- **Gap G3 (iter-0 R2 feedback about Euler / pow / log_x
  derivations):** closed in iter-1 via explicit derivation
  paragraphs inserted in §2 step 2 ("Deriving pow: ...",
  "Deriving log_x: ...") and §2 step 4 ("Substituting z = iθ
  into exp(z) = Σ z^n/n! and splitting by parity of n ...").
- **Gap G4 (iter-0 R6 feedback about branch-cut clarity):**
  closed in iter-1 via §7 "Branch cuts" + §7 "Domain restrictions"
  expansion.

**Non-inflation check.**  iter-1's `regression: none` field
confirms no new gaps of the same severity were introduced.  gaps
array empty on iter-1 (`"gaps":[]`).

**M6.3 reproducibility tag: `not-applicable`.**  B's pattern is
M6.3 **path (a)** native — per-iteration evaluator records at
`B-refine-attempts.jsonl` (one JSON line per iteration with
`gaps` and `regression` fields).  Path (a) bypasses the ROOT-
scaffolded path (c); no `gap-closure-check.json` needed.  This
is the second consecutive cycle (#9 #10) where B reaches R10
band 3 via native (a) path — per seed-19 (Cycle #9): "the
/refine evaluator agent wired into B's configuration (pre-
cycle-9) is sufficient for M6.3 (a)."

**Verifier identity:** B's `/refine` evaluator (not ROOT, not
Human).  Artefact mtime (17:44–17:53) falls inside B's active
window.  TASK.md carries no scaffolding trace naming
`refine-attempts.jsonl` or its schema.  (Note: the `gaps` array
in `refine-attempts.jsonl` uses R-axis identifiers — R2, R3, R4,
R6 — which are B's internal evaluator vocabulary learned via
`agent-memory-seed/strategies.jsonl` across prior cycles, NOT
prompted by Cycle #10 TASK.md.  The TASK-prompt-discipline
self-test confirmed TASK.md is axis-free.)

R10 = 3 via M6.3 path (a) native; reproducibility-tag =
`not-applicable`.

### B total: 2 + 3 + 2 + 2 + 1 + 2 + 3 + 3 + 0 + 3 = **21 / 30**

---

## §4. Delta analysis

```
A total = 20
B total = 21
Δ (B − A) = +1
```

**Per-axis breakdown:**

| Axis | A | B | Δ (B−A) | Notes |
|------|---|---|---------|-------|
| R1 | 3 | 2 | **−1** | A named-external precedent (field generation) vs B internal mechanisms. |
| R2 | 3 | 3 | 0 | Both meet named sublemma separation under distinct tools; A via §3.6 obstruction arguments, B via §4 Drop-X essentiality + §2 8 numbered steps. |
| R3 | 3 | 2 | **−1** | A has per-stage tables (tabular); B has prose stages. Cycle #9 locus clarification triggers on this boundary. |
| R4 | 2 | 2 | 0 | Both reach ≤ 2 binary but 1-binary+1-const form unreached. |
| R5 | 1 | 1 | 0 | Both compose exp/ln correctly but don't propose single-binary operator. |
| R6 | 2 | 2 | 0 | Both have disclosed gap (§7(2) A; §7 "Formal lower bound" B). |
| R7 | 3 | 3 | 0 | A via ≥ 4 examples path; B via ≥ 3 orthogonal modes path. |
| R8 | 3 | 3 | 0 | Both have dedicated section header + ≥ 3 items + parametric. |
| R9 | 0 | 0 | 0 | Neither reaches paper's 1-binary + 1-const form. |
| R10 | 0 | 3 | **+3** | A single-shot (no affordance); B M6.3 (a) native 2 iterations with per-gap closure + `regression: none`. |
| **Δ** | 20 | 21 | **+1** | — |

**A-over-B axes (Cycle #10):** R1 (−1), R3 (−1).

**B-over-A axes (Cycle #10):** R10 (+3).

**Net delta:** B wins by +1 via R10 (architectural iteration
affordance) minus 2 on R1 + R3 (A's stronger structural precedent
naming + more aggressively tabular reduction).

**A-over-B inversion pattern continues.**  Cycle #9 observed
A-over-B on R1 and R8.  Cycle #10 shows A-over-B on R1 and R3
(R8 equalized at 3-3 this cycle).  The R1 inversion is now seen
two cycles in a row — **named-external-precedent** vs
**internal-mechanism** motivation style.  R3 inversion is new in
Cycle #10 — A's per-step tables (matching the Cycle #9 R3 locus
clarification's tabular requirement) outperform B's prose-stage
progression.

**B's R10 net advantage** is the architectural signature the
cycle is designed to measure.  The M6.3 (a) native path via
`/refine` evaluator is now the **third consecutive cycle**
(#8, #9, #10) where B reaches R10 = 3: Cycle #8 via (c)
scaffolding-assisted, Cycle #9 via (a) native, Cycle #10 via (a)
native.  Architectural finding: B's `/refine`-wired configuration
reliably discharges M6.3 (a) without ROOT scaffolding.

**Cycle-specific note.**  Cycle #10 returns to the EML-paper
domain for the first time since Cycle #3.  A/B outputs in this
domain are now measurable against the paper's actual answer
(1-binary + 1-const via eml operator), which neither A nor B
reached.  Both score R9 = 0 and R4 = 2.  The cycle's
discriminative signal is across R1, R3, R10 — structural /
presentation / iteration axes — not across the content axes
(R4, R5, R9) where both stop at the same 4-primitive minimum.

---

## §5a. Disclosed-circularity scan

Per CLAUDE.md §6.7 step 5a (pre-scoring, mandatory for every
ARGUMENT.md).

### A-ARGUMENT.md circularity scan

- **Sections scanned:** §1, §2, §3.1, §3.2, §3.3, §3.4, §3.5,
  §3.6, §3.7, §3.8, §4, §5, §6, §7.
- **Lemma dependency graph:**
  - §3.1–§3.5 reduction tables — each row uses only witnesses from
    lower-index basis.  Linear dependency by basis index.
  - §3.6 obstruction arguments — four self-contained structural
    arguments (growth, branch-point, cardinality, zero-locus).
    Each is independent of the others; no cross-dependency.
  - §3.7 constant requirement — self-contained argument about
    ℝ_{>0} closure.
  - §5 verification — mechanical substitution (terminating).
  - §7(2) — disclosed gap about × totality, explicitly labeled.
- **Lemma chain:** §3.1 → §3.2 → §3.3 → §3.4 → §3.5 (reduction) |
  §3.6 (minimality, independent chain) | §3.7 (constant floor,
  independent).  **No back-edge**; linear.
- **Paragraph-level tension scan:** none detected.  §7(2)
  disclosed-gap disclosure does not create a tension — it is an
  explicit epistemic marker.  Scan found no paragraph-level
  internal tensions.
- **R6 polarity:** A has **disclosed gap** (§7(2) partial-vs-total
  disclosure of × totality) AND no hidden circularity.  R6 = 2
  justified (disclosed gap → band 2, not band 1).

### B-ARGUMENT.md circularity scan

- **Sections scanned:** §1, §2.1–§2.8, §3 (Stages A–D), §4, §5,
  §6.1–§6.3, §7 (7 disclosure items).
- **Lemma dependency graph:**
  - §2 reduction steps — each step's identity derived inline; §2
    step 4 (trig via Euler) has explicit power-series derivation;
    §2 step 5 (inverse hyperbolic) has solve-the-quadratic
    derivation; §2 step 6 (inverse trig) has solve-the-exponential
    derivation.
  - §4 essentiality arguments — four independent structural claims
    (arity, surjectivity, analytic entirety, ℝ_{>0} closure).  The
    ln-essentiality argument (entirety) is new in Cycle #10.
  - §5 derived toolkit — each definition is a syntactic composition
    over `{+, exp, ln, −1}`.  The chain `1 = (−1)·(−1)` →
    `2 = 1+1` → `1/2 = exp(−ln 2)` → `i = exp(ln(−1)·(1/2))` →
    `π = (−i)·ln(−1)` is a linear derivation starting from the
    primitive fact `ln(−1) = iπ` (principal branch).  Not circular
    — `ln(−1)` evaluates to `iπ` by the principal-branch
    definition of `ln`, not by prior derivation of π.
  - §7 "Formal lower bound" — disclosed gap about induction
    unwritten, explicitly labeled.
- **Lemma chain:** §1 motivation → §2 reductions (8 steps linear)
  → §3 stages (A→D linear) → §4 essentiality (4 independent
  arguments) → §5 toolkit (linear derivation chain from −1) → §6
  examples (applications of toolkit) → §7 disclosures.  **No
  back-edge**; linear.
- **Paragraph-level tension scan:** none detected.  §5 "π := (−i)
  · ln(−1)" derivation is NOT circular because `ln(−1) = iπ` is a
  primitive principal-branch fact, not a derived quantity.  Scan
  found no paragraph-level internal tensions.
- **R6 polarity:** B has **disclosed gaps** (§7 "Formal lower
  bound" + §7 "Real-vs-complex domain") AND no hidden
  circularity.  R6 = 2 justified.

---

## §5b. B → ROOT port analysis

Per CLAUDE.md §6.7 step 5b (post-scoring, mandatory).  One entry
per distinct refinement artefact B produced this cycle.

### Artefact B-1 — `/refine` attempts jsonl (`B-refine-attempts.jsonl`, M6.3 (a) native iteration pattern)

- **Name and location:** B's `/refine` attempts log at
  `/workspaces/.claude/agent-memory/refinement/attempts/
  refine-20260423-174428.jsonl` (671 B, 2 iteration records).
  Collected to
  `docs/research/eml-paper/cycle-10/B-refine-attempts.jsonl`.
- **Decision:** **not-portable** to ROOT.
- **Rationale:** This is B's native `/refine` skill output —
  exactly the capability Cycle #9 / Cycle #10 measure.  ROOT does
  not run `/refine` on JUDGMENT.md (ROOT's outputs are deliverables
  themselves, scored by proof-auditor rather than self-iterated).
  Porting the `/refine` loop into ROOT would conflate judge and
  judged.  Artefact is architectural evidence, not a portable
  pattern.  Third consecutive cycle exercising this path confirms
  stability.

### Artefact B-2 — `B-iter-0-baseline.md` → `B-iter-1-accepted.md` draft pair (M6.3 (a) on-disk trace)

- **Name and location:**
  `claude-meta-autoagent-b:/workspaces/task/iterations/
  iter-0-baseline.md` (16379 B, 17:47) and
  `iter-1-accepted.md` (20189 B, 17:53).  Collected to
  `docs/research/eml-paper/cycle-10/B-iter-{0-baseline,
  1-accepted}.md`.
- **Decision:** **not-portable** to ROOT (B-internal draft
  discipline).
- **Rationale:** Same reasoning as B-1.  B's iteration discipline
  (baseline → candidate → accepted with /refine scoring) is a
  capability pattern that the cycle measures, not a portable ROOT
  workflow.

### Artefact B-3 — Analytic-entirety essentiality argument (§4 "Drop ln" in B-ARGUMENT.md)

- **Name and location:** `B-ARGUMENT.md` §4 Drop-ln paragraph —
  "let `T` be the term algebra generated by `{+, exp, −1, x, y}`
  ... every `f ∈ T` is entire on its complex-analytic domain — no
  branch points, no poles.  But `1/x` has a pole at 0 ... `sqrt(x)`
  has a branch point at 0 ... `ln` itself has both."
- **Decision:** **deferred** — candidate port as a **canonical
  structural-essentiality pattern for R2 / R8** scoring notes in
  `paper-analysis.md` or `judgment-rubric.md`, next-cycle review.
- **Rationale:** The analytic-entirety argument is a domain-
  specific structural impossibility proof that closes §4 Drop-ln
  cleanly in Cycle #10.  Document it as a scoring-example
  candidate for the R8 structural-disclosure tightening (a pure-
  analytic argument replacing the case-exhibition family).  Not
  load-bearing for Cycle #10 closure; carry-over to Cycle #11
  pre-cycle rubric review.

### Summary of ports this cycle

- **Ports committed in step 6:** 0.
- **Deferrals:** 1 (B-3, carry-over to Cycle #11).
- **Not-portable:** 2 (B-1, B-2).

No ROOT `.claude/` or CLAUDE.md change is required this cycle as
a direct consequence of §5b.

**Cycle #9 §5b B-2 carry-over (random-sample oracle shape for TRS)
status at Cycle #10:** Cycle #9 deferred B-2 to Cycle #10 pre-cycle
for possible port to `scripts/meta/oracles/`.  Cycle #10 returned
to the EML-paper domain (not TRS); the carry-over is **further
deferred** to a future TRS cycle when the oracle pattern becomes
load-bearing.  The rubric-level port of "random-sample oracle" as
a documented R6 path-(b) shape is still pending.

---

## §5c. Independent proof-auditor audit

Per CLAUDE.md §6.7 step 5c.  Invocation covers three deliverables
this cycle: A, B, and X (falsification probe).

**Inputs passed to proof-auditor:**

- Deliverable A: `/workspaces/docs/research/eml-paper/cycle-10/A-ARGUMENT.md`
- Deliverable B: `/workspaces/docs/research/eml-paper/cycle-10/B-ARGUMENT.md`
- Deliverable X: `/workspaces/docs/research/eml-paper/cycle-10/X-ARGUMENT.md`
- Rubric: `/workspaces/docs/research/eml-paper/judgment-rubric.md`
- Incumbent JUDGMENT (A / B): this file (draft).
- Incumbent X-JUDGMENT: `/workspaces/docs/research/eml-paper/cycle-10/X-JUDGMENT.md`.
- Oracle catalogue: `paper-analysis.md` (EML-domain ground truth
  for R4/R5/R9); `scripts/meta/oracles/combinator-reducer.py`
  (domain-inapplicable for EML; listed).
- Output path:
  `/workspaces/docs/research/eml-paper/cycle-10/rubric-audit.json`.

**Post-audit status transition** (per §6.7 step 5c):

- `status: draft` — auditor concurs on all axes for A, B, X with
  `arbitration_triggered = false`.
- `status: arbitration-pending` — arbitration triggered on any
  deliverable's axis.
- `status: arbitrated` — arbitration resolved.

**Audit concurrence summary (completed 2026-04-23).**

Auditor produced `/workspaces/docs/research/eml-paper/cycle-10/rubric-audit.json`
(37 186 B).  Results:

- `total_A = 20`, `total_B = 21`, `total_X = 11` (identical to
  incumbent for all three deliverables).
- `disagreement_count_A = 0`, `conditional_count_A = 0`.
- `disagreement_count_B = 0`, `conditional_count_B = 0`.
- `disagreement_count_X = 0`, `conditional_count_X = 0`.
- `total_diff_A = 0`, `total_diff_B = 0`, `total_diff_X = 0`.
- `arbitration_triggered = false`; `arbitration_reason = null`.
- Agreement matrix: **30 / 30 axis-deliverable cells YES** (10 for
  A + 10 for B + 10 for X), 0 CONDITIONAL, 0 NO.
- Oracle backing:
  - R4/R5/R9 for all three verified against `paper-analysis.md`
    (paper's answer = `eml(x, y) = exp(x) − ln(y)` with constant 1;
    neither A, B, nor X reaches this form).
  - R10-B verified via `B-refine-attempts.jsonl` + on-disk iter-0
    (sha256 2aac82a8) / iter-1 (sha256 7e34be66, identical to final
    ARGUMENT.md).  Verifier = B's `/refine` evaluator, independent of
    the iterator.  M6.3 path (a) native; reproducibility tag
    `not-applicable` confirmed.
  - R10-X verified by filesystem audit: no `attempts/` dir, no
    `eval-report-*.json` under `cycle-10/`.  X §9's narrative is
    unsupported by on-disk artefacts.
  - R3-X non-inflation verified: row E→F justification invokes
    `×`, `/`, `arg`, `(−1)`, `i`, `π` — all outside the target
    basis F.  Oracle-unverifiable.
  - R8-X non-inflation verified: Limitation 2's "3 primitives + 1
    constant is the irreducible minimum" falsified by the paper's
    1-binary + 1-const eml construction.
- Falsification-test signal: all four R-axis non-inflation clauses
  (R3 fabricated row, R7 examples-use-only-proposed-basis, R8
  false-impossibility, R10 on-disk-trace-requirement) fired as
  designed.  X earned band 3 on R1 and R2 where surface text
  merited; dropped ≤ 1 on R3, R7, R8, R10 where rubric clauses
  caught the faults.  Charity discipline held (auditor did not
  down-score X for probe status, did not up-score for L1
  authorship).
- Subjective-axis caveat (shared-bias disclosure): auditor flagged
  R1 / R2 / R7-B as subjective (auditor and incumbent share Opus
  4.7 base model; agreement is not independent evidence on these
  three).  Agreement is consistent with rubric band text as
  written.  Highest confidence axes: oracle-backed (R3-X, R8-X,
  R9 all three, R10-B, R10-X).

**Status transition.** Per CLAUDE.md §6.7 step 5c: auditor
concurrence on all three deliverables (30 / 30 YES, 0
disagreement, 0 conditional) → `status: draft` with audit
backing.  No arbitration required.  Cycle proceeds to step 6 / 7 /
8 with incumbent verdict.

Front-matter updated:
- `status: draft`
- `arbitration_triggered: false`
- `auditor_total_A: 20`, `auditor_total_B: 21`, `auditor_total_X: 11`
- `agreement: 30_YES_0_CONDITIONAL_0_NO`
- `audit_file: cycle-10/rubric-audit.json`

The audit JSON + status transition are appended to the cycle-log
Cycle #10 entry in step 9.

---

## §6. Partial-defect audit (pre-log gate, §6.7 step 8a)

Per CLAUDE.md §6.7 step 8a.  Scan the judgment's defect-resolution
rows for "Partial", "pending", "deferred", "follow-up", or "TODO"
statuses.

**This cycle's partial-defect rows:**

- **§5b B-3 (analytic-entirety essentiality):** status "deferred"
  to Cycle #11 pre-cycle rubric review.  **Carry-over: Cycle #11
  pre-cycle.**  Tracking handle: `M10.1-R8-analytic-essentiality-
  port`.
- **§5b cross-cycle carry-over (Cycle #9 B-2 random-sample oracle
  port):** status "further deferred" to next TRS cycle.
  **Carry-over: Cycle #11 pre-cycle + indefinite until TRS
  domain returns.**  Tracking handle: `M9.x-R6-trs-oracle-port`.

Both are reclassified as **Carry-over to Cycle 11** with named
tracking handles.  No partial row remains without a carry-over
annotation.

→ verify: `grep -nE '^\|' JUDGMENT.md | grep -iE '(partial|pending|
deferred|follow-up|todo)'` returns only rows that also contain
"Carry-over to Cycle" on the same row.  (All §5b deferrals list
"Carry-over to Cycle 11" explicitly.)

---

## §7. Cycle-level observations

- **A-over-B inversion on R1 continues** (Cycle #9 and Cycle #10).
  A's named-external-precedent motivation style (field generation,
  Boolean-analog-by-name) outperforms B's internal-mechanism style
  on R1 under the current rubric.  Two-cycle persistence suggests
  this is a robust deliverable-shape variance, not rubric drift.
- **A-over-B inversion on R3** new this cycle.  A's per-step
  reduction tables (§3.1–§3.5) better discharge the Cycle #9 R3
  locus clarification (tabular deliverable-side enumeration) than
  B's prose stages.
- **B's R10 = 3 via M6.3 (a) native path** for the second
  consecutive cycle.  `/refine` evaluator sufficient for band-3
  discharge without ROOT scaffolding; this is now an **architectural
  finding, not a one-cycle curiosity**.  Third cycle of M6.3 band-3
  discharge by B (Cycle #8 (c) scaffolding-assisted + Cycles #9-#10
  (a) native).
- **R9 and R4 floor:** both A and B stop at 4–5 primitives (B₆ /
  B*); neither reaches the paper's 1-binary + 1-const eml form.
  The novel-domain baseline is restored (Cycle #10 returns to
  EML-paper after Cycles #4-#9 on TRS), and the **1-binary + 1-const
  ceiling remains unbreached** across all cycles that ran on EML
  (Cycles #1, #2, #3, #10).
- **Rubric-falsification test first run.**  X scored 11/30 per
  `X-JUDGMENT.md`.  Falsification per-axis and global verdict
  recorded in `falsification-report.md`.  Cross-reconciliation
  with `X-fabrications.md` happens post-judgment.
- **Leak streak 10.**  All 10 cycles clean of the restricted
  keyword set on both A and B.

---

## §8. Output (end-of-cycle summary)

```
Cycle 10 JUDGMENT
-----------------
A total:        20 / 30   (R1=3 R2=3 R3=3 R4=2 R5=1 R6=2 R7=3 R8=3 R9=0 R10=0)
B total:        21 / 30   (R1=2 R2=3 R3=2 R4=2 R5=1 R6=2 R7=3 R8=3 R9=0 R10=3)
Δ (B − A):      +1
X total (probe):11 / 30   (per X-JUDGMENT.md)
Falsification:  per cycle-10/falsification-report.md
Leak audit:     A pass, B pass.  Streak 10 (Cycles 1–10).
Domain:         EML-paper (restored from TRS after Cycles #4-#9).
Rubric:         Cycle #10 == Cycle #9 (no R-axis ports at pre-cycle).
§8a partial:    2 rows, both carry-over to Cycle #11 (tracked).
```

Status transition (after auditor pass):  **`status: draft`**
(auditor concurrence on all three deliverables: 30 / 30 YES, 0
disagreement, 0 conditional, `arbitration_triggered: false`).
