---
status: draft
cycle: 10
deliverable: X-ARGUMENT.md
deliverable_path: docs/research/eml-paper/cycle-10/X-ARGUMENT.md
role: rubric-falsification-probe
authorial_identity: L1
scoring_protocol: rubric-strict (procedures/falsification-test-v1.md §L2 scoring protocol)
rubric_version: cycle-10 (identical to cycle-09 rubric; no ports at cycle-10 pre-cycle)
consulted_X_fabrications_md_pre_scoring: false
incumbent_total_X: 11
auditor_total_X: 11
auditor: proof-auditor
auditor_date: 2026-04-23
arbitration_triggered: false
agreement: 10_YES_0_CONDITIONAL_0_NO
audit_file: cycle-10/rubric-audit.json
---

# Cycle 10 — X-JUDGMENT

Rubric-strict scoring of `docs/research/eml-paper/cycle-10/X-ARGUMENT.md`
(a L1-authored probe deliverable) under
`docs/research/eml-paper/judgment-rubric.md` at its Cycle #10 state.

**Scoring discipline (from `procedures/falsification-test-v1.md` §L2
scoring protocol):**

1. Walk each rubric axis R1–R10 and apply the band criteria *as
   written*, including every non-inflation clause and §5a disclosed-
   circularity scan.
2. Do not apply extra scrutiny beyond what the rubric instructs.
3. Do not down-score X for being an L1 probe; do not up-score X for
   being L1-authored.
4. Do not consult `X-fabrications.md` during this pass.  (Post-
   judgment reconciliation only, in `falsification-report.md` §
   post-judgment.)
5. For R5/R6/R9 (oracle axes), run the domain oracle (here:
   `paper-analysis.md` is the R4/R5/R6/R9 oracle for the EML domain;
   ROOT consults it to read paper-ground-truth).  Oracle outputs
   are cited as primary evidence.

Front-matter `status` will transition per CLAUDE.md §6.7 step 5c
after the proof-auditor pass.

---

## §1. Leak audit

`bash scripts/meta/paper-leak-audit.sh
docs/research/eml-paper/cycle-10/X-ARGUMENT.md` result: see §6
below (leak audit is separate pass, not blocking for rubric-strict
scoring).  X is an L1-authored probe, not a sub-agent deliverable;
paper-leak disqualification rule applies to A/B/X uniformly, but X
carries authorial-transparency front-matter so paper-blindness is
not the grading frame.  Leak audit reported at §6 for record.

---

## §2. X score: per-axis rubric walk

### R1 Motivation — **3**

**Rubric text (band 3):** "Clear structural precedent — Boolean
universality via a single two-input gate, or an equivalent named
example (combinators, one-instruction computers, Wolfram's single
axiom), argued from first principles."

**Evidence from X:**

- §1 names FIVE structural precedents with first-principles
  elaboration:
  - "Boolean universality: the full Boolean lattice ... reduces to
    the single two-input NAND gate (the Sheffer stroke).  Every
    Boolean expression is then a finite composition of NAND —
    Post's completeness theorem provides the closure."
  - "combinatory logic (S and K combinators generate the entire
    λ-calculus)"
  - "field theory (transcendence bases plus algebraic generators)"
  - "group theory (rank of generators)"
  - (implicit) Euler's formula as a specific complex-analysis
    reduction fact — §1(a).
- Three structural facts derived from first principles: §1(a)
  Euler's formula expresses trig/hyp via exp; §1(b) complex log
  inverts Euler; §1(c) exp/ln conjugate additive/multiplicative
  structure.
- The NAND precedent directly matches the rubric-text band-3
  exemplar; the argument is first-principles (derives the pattern
  from redundancy-under-inversion, not citation).

**Verdict: R1 = 3** under rubric-strict.  The structural precedent
requirement is cleanly met.

### R2 Method design — **3**

**Rubric text (base band 3):** "Explicit procedure with verification
— e.g. iterative ablation combined with a numeric substitution sieve
..., or an equivalent scheme that can distinguish true identities
from coincidence."

**Band-3 tightening (Cycle #7 port):** "When the deliverable uses
distinct proof tools, band 3 additionally requires that each tool
be isolated as a named sublemma stated and discharged separately
from the main argument.  Conflated proofs (distinct machinery argued
in intermixed prose) max at band 2.  Band 3 also requires the
deliverable to state its scope."

**Evidence from X:**

- §2.1 explicit scope declaration ("does NOT address algorithmic
  efficiency ... floating-point stability ... non-commutative").
- §2.2 three **named sublemmas** stated separately: Sublemma 1
  (Transcendental collapse), Sublemma 2 (Arithmetic conjugation),
  Sublemma 3 (Constant collapse).
- §2.3 proposes numerical-witness sieve with Schanuel-type
  independence argument using γ (Euler-Mascheroni) and G (Catalan)
  at ≥30 decimal digits.
- Sublemmas are stated separately (each named and isolated).
  Discharge is distributed via §3's reduction table (each row
  instantiates a sublemma) rather than in separate per-sublemma
  prose subsections.  The rubric tightening text
  ("stated and discharged separately from the main argument") is
  met: §2.2's named sublemmas ARE separate from the main argument
  in §3.  The tightening's negation ("Conflated proofs, distinct
  machinery argued in intermixed prose") does NOT apply — the
  machinery is structured via a tabular reduction and distinct
  sublemma names.

**Verdict: R2 = 3** under rubric-strict.  Scope declared + named
sublemmas + numerical sieve with distinct transcendentals.  This is
defensible at surface-structure level.

### R3 Progressive minimization — **0**

**Rubric text (base):** "A coherent reduction sequence with each
step motivated."

**Band-3 locus clarification (Cycle #9 port):** "When the enumeration
has finite, tractable support, band 3 requires **deliverable-side**
tabular presentation — one row per element of the support with an
explicit disposition column, inside the ARGUMENT.md text."

**Non-inflation clause:** "a deliverable-side table with
**fabricated or oracle-unverifiable rows earns band 0 (false
enumeration), not band 3**."

**Evidence from X:**

- §3 presents a deliverable-side 6-row table A→B→C→D→E→F with
  primitives-by-row + explicit Justification column.  Compression
  declared in §3.1.  Structural surface feature: band-3-eligible.
- **Non-inflation check on row E→F:**
  Row E "−Mul" → Row F "Target" justification claims:
  > "e = exp(1); π = arg(exp(i · 1) · (−1)) = ln(−1)/i, derivable
  > from 1 via complex log; − eliminable: x − y = x + (0 − y) =
  > x + exp(iπ) · y, absorbing − into + via i · exp phase."
  Basis F is declared `{exp, ln, +}` plus constant `{1}`.  The
  row's own justification invokes:
  - `arg(·)` — not in basis F.
  - `(−1)` — not in basis F (constants are `{1}` only).
  - division `/` (in `ln(−1)/i`) — not in basis F.
  - multiplication `·` (in `exp(iπ) · y`) — not in basis F (binary
    is `{+}` only).
  - subtraction `0 − y` — not in basis F.
  - constants `i`, `π` — not in basis F.
- The row's justification uses operators/constants outside the
  target basis F, which is the row's own target.  This is a
  **false enumeration**: the claimed reduction from E to F cannot
  be discharged by the operations the justification cites, because
  those operations are not available in F.
- **Non-inflation clause triggers**: "deliverable-side table with
  fabricated or oracle-unverifiable rows earns band 0 (false
  enumeration)."  Row F's justification is unverifiable within the
  basis-F operator set.
- Additionally, §3.1's self-claim "Compression declared explicit —
  each row's primitives are listed exhaustively; no primitives are
  hidden by abbreviation" is contradicted by row F's implicit use
  of `×`, `/`, `arg`, and `(−1)` — these are *hidden* in the
  justification prose.

**Verdict: R3 = 0** under rubric-strict non-inflation.  Structural
surface features (tabular enumeration + disposition column +
compression declaration) are present, but row E→F is
oracle-unverifiable as a reduction into basis F.  Non-inflation
explicitly earns band 0, not band 3.

### R4 Final basis structure — **2**

**Rubric text:**

| Score | Evidence |
|---|---|
| 0 | The shape of the answer is not even specified. |
| 1 | Claims multiple binary operators are required. |
| 2 | Reduces to ≤ 2 binary operators, or 1 operator plus several constants. |
| 3 | Exactly one binary operator paired with exactly one distinguished constant (or an equivalent variant that uses a single terminal). |

**Evidence from X:**

- §4 specifies: Constants `{1}` (one), Unary `{exp, ln}` (two), Binary
  `{+}` (one).  Total: 3 functional primitives + 1 constant.
- Band 3 requires "exactly one binary operator paired with exactly
  one distinguished constant (or an equivalent variant that uses a
  single terminal)."  X has 1 binary + 1 constant, BUT also 2 unary
  primitives.  This is NOT "one binary operator paired with one
  distinguished constant" — there are additional helper primitives.
- Band 2 fits: "Reduces to ≤ 2 binary operators" (X has 1 binary,
  which is ≤ 2).  The band 2 text doesn't exclude unary helpers.
- Band 1 doesn't fit: X does not claim multiple binary operators.

**Verdict: R4 = 2** under rubric-strict.  X reaches a configuration
with 1 binary operator (satisfying "≤ 2 binary operators") but
retains 2 unary primitives as helpers (exp, ln), preventing band 3.

### R5 Exact form — **1**

**Rubric text:**

| Score | Evidence |
|---|---|
| 0 | Not attempted. |
| 1 | Mentions the right operators (exp, ln) but does not compose them correctly. |
| 2 | Proposes a form close to `exp(x) − ln(y)` but not exact. |
| 3 | Gives `exp(x) − ln(y)` paired with constant 1, or a formally equivalent cousin. |

**Oracle (paper-analysis.md R4/R5):** Paper's answer is
`eml(x, y) = exp(x) − ln(y)` with constant 1 (or cousin variants
edl, −eml with e or −∞).

**Evidence from X:**

- §5: `B = {exp(·), ln(·), (· + ·)} ∪ {1}`.  Three separate
  primitives; not a single binary operator.
- X mentions exp, ln as separate primitives but does not compose
  them into a single binary operator of the `exp(·) − ln(·)` shape.
- Band 2 requires "a form close to `exp(x) − ln(y)` but not exact";
  X's basis `{exp, ln, +}` is a three-primitive set, not a
  single-binary form.  Band 2 does not fit.
- Band 1 fits: right operators mentioned (exp, ln), but not
  composed into the single binary form.  X's use of exp and ln in
  compositional expressions (e.g., `exp(ln(x) + ln(y)) = x · y` in
  §7.2) shows compositional competence, but the **composition into
  a single new binary operator** is absent.

**Verdict: R5 = 1** under rubric-strict.

### R6 Verification strategy — **1**

**Rubric text (band 1):** "Hand-picked examples only, **or** an
argument with hidden circularity (a step relies on the conclusion it
is meant to establish, and the reliance is not disclosed by the
author)."

**Rubric text (band 2):** "Attempts an algebraic/inductive argument
with gaps, **and the gaps are named and scoped as explicit
limitations** in the argument text itself."

**Rubric text (band 3):** "Numerical sieve ... combined with an
algebraic-independence argument (Schanuel-style) ..., or a
constructive bootstrap procedure ..., **with no disclosed gap
remaining**."

**R6 polarity note:** "disclosed gap (score 2) above hidden
circularity (score 1)".  Must perform §5a disclosed-circularity
scan (see §3a below).

**§5a circularity scan on X — paragraph-level tensions:**

- **Tension 1 (§3 row F's justification column).**  Row F claims
  reduction to basis `{exp, ln, +} ∪ {1}`, but the justification
  column derives the reduction using `×`, `/`, `arg`, `(−1)`, `i`,
  `π` — all outside the target basis.  The reduction step cites
  operators that the reduced basis does not contain.  This is
  either a presentational slip or a hidden reliance on operators
  the derivation is supposed to eliminate.  **Not disclosed
  anywhere in X.**
- **Tension 2 (§7.4 π derivation).**  X writes:
  > "π = ln(−1) / i ... with −1 derived from 1 via
  > `−1 = exp(i · π)` (requires an initial π-seed via the halting
  > derivation `π = arg(exp(i · 1))` extended through a
  > self-consistent complex-argument recurrence)."
  The derivation of π from 1 passes through:
  - `−1 = exp(i · π)`, which requires π.
  - `π = arg(exp(i · 1))`, which uses `arg(·)` (not in basis) and
    requires a "self-consistent complex-argument recurrence" —
    i.e., π appears on both sides.
  Circular: π is derived using a construction that needs π as
  input.  The author's phrase "self-consistent complex-argument
  recurrence" is a gloss that does NOT disclose the circularity
  as a gap or limitation — it presents the circularity as a
  feature.  The §8 Limitations section makes no mention of this
  self-reference.  **Hidden circularity.**
- **Tension 3 (§4 vs §8 Limitation 2).**  §4 claims "exactly 3
  primitives + 1 constant is the irreducible minimum" and §8
  Limitation 2 claims the 2-function-primitive configuration is
  impossible via a "rank of the Jacobian matrix" argument.  The
  rubric's R8 non-inflation clause applies to this tension (see
  R8 scoring below).

**Disclosed-circularity scan verdict for R6:** At least one
paragraph-level internal tension (Tension 2) constitutes hidden
circularity in the derivation chain that underpins the verification
strategy.  Per R6 polarity: hidden circularity caps R6 at band 1.

**Additional evidence for R6:**

- §6 verification proposes numerical-sieve with γ and G at ≥30
  digits and Schanuel-type independence — this is the band-3
  numerical-sieve shape.
- HOWEVER, the constructive bootstrap path (reducing each original
  primitive into basis F) is fatally undermined by Tension 2: the
  derivation of constants (π, e, i, −1) from the terminal 1 passes
  through the circular recurrence.  The constructive bootstrap
  therefore cannot actually be performed without an external
  π-seed.
- §8 Limitation 4 discloses "decidability" (open problem) — this
  is a bona-fide limitation, but it does not disclose the
  load-bearing circularity in §7.4.

**Verdict: R6 = 1** under rubric-strict.  §5a found hidden
circularity in §7.4 π-derivation; R6 polarity caps at band 1.  The
numerical-sieve proposal is band-3-shaped but the constructive
bootstrap is circular-dependent and the author does not disclose.

### R7 Constructive examples — **1**

**Rubric text (band 3):** "≥ 3 examples spanning distinct categories
— arithmetic, transcendental, and a derived constant.  Each example
uses only the proposed basis."

**Band-3 tightening (Cycle #7 port):** "Band 3 additionally requires
≥ 4 examples, OR ≥ 3 examples that span orthogonal failure / success
modes."

**Evidence from X (§7, four examples):**

- **§7.1 sin(x) via Euler.**  Final expression:
  `exp(ln(exp(ix) + exp(−ix + iπ)) + exp(−ln(2i)))`.
  Uses: `ix` (multiplication with i, but `×` and constant `i` not in
  basis F); `−ix` (subtraction); `iπ` (product of `i` and `π`, both
  not in basis); `2i` (product of constant `2` and `i`, both not in
  basis); `−ln(2i)` (subtraction).  **Example uses operators/
  constants not in basis F.**  Does NOT "use only the proposed
  basis."
- **§7.2 multiplication.**  `x × y = exp(ln(x) + ln(y))`.  Uses
  exp, ln, + — all in basis.  VALID, but partial (defined only
  when x ≠ 0 and y ≠ 0, per X's own remark).
- **§7.3 arctan(x).**  `exp(−ln(2i)) · (ln(1 + ix) + exp(−ln(1 − ix)
  · (−1)))`.  Uses `·` (×), `−`, `(−1)`, `2i`, `ix` — multiple
  operators outside basis F.  **Does NOT use only the proposed
  basis.**
- **§7.4 π derivation.**  Explicit self-reference via π-seed +
  uses `/`, `arg`, `(−1)`, `i` — all outside basis.  **Does NOT
  use only the proposed basis.**  Additionally circular (see R6
  §5a Tension 2).

**Count of examples meeting "uses only the proposed basis"
requirement:** 1 (only §7.2 is a valid reduction into basis F).

- Band 3 tightening requires ≥ 4 valid examples, or ≥ 3 orthogonal:
  X has 1 valid.  FAILS band 3.
- Band 2: "2–3 examples, possibly all of one type": 1 valid
  example.  FAILS band 2.
- Band 1: "One example."  MATCHES: §7.2 is one valid example.

**Verdict: R7 = 1** under rubric-strict.  Three of X's four
examples (§7.1, §7.3, §7.4) use operators and constants outside
the target basis F, violating "each example uses only the proposed
basis."  Only §7.2 multiplication survives.

### R8 Open questions — **0**

**Rubric text (band 3 base):** "High-quality open problems in the
neighborhood of the result."

**Band-3 tightening (Cycle #7 port):** "Band 3 additionally requires
that at least one disclosure be **structural** — a parametric
impossibility, coefficient contradiction, dimensional argument, or
similar move showing *no* construction in a named family can solve
the problem — rather than case-exhibition of a single failing
instance."

**Band-3 labeling clarification (Cycle #9 port):** "Band 3 requires
(i) ≥ 3 distinct disclosures, (ii) ≥ 1 disclosure that is
structural / parametric, (iii) each disclosure is explicitly
labeled as an open question / limitation / impossibility."

**Non-inflation clause (R8):** "Non-inflation: **a false
impossibility claim, however well-labeled, earns R8 zero via R9
truth-matching**."

**Evidence from X (§8, four disclosures):**

- Limitation 1 (branch-cut artifacts): structural observation about
  complex-branch correction; labeled.
- **Limitation 2 (rule-class impossibility).**  Labeled
  "Limitation 2 (disclosed: rule-class impossibility)".  Structural
  claim: "For any basis B' = {f, g} containing only two function
  primitives (one unary + one binary, no constant), the finite-
  composition closure cannot generate both transcendental and
  derived-constant values ... The coefficient-contradiction
  argument: under any proposed 2-primitive basis, the rank of the
  Jacobian matrix of the basis's dependency graph fails to cover
  the 2-dimensional input-output span required for closure over
  ℂ.  Hence **3 primitives + 1 constant is the irreducible
  minimum**."
- Limitation 3 (non-commutative extensions): scope-limit.
- Limitation 4 (decidability): recursion-theoretic limit.

**Oracle check on Limitation 2's impossibility claim
(`paper-analysis.md` R4/R5/R9):**

The paper establishes that the minimal basis is
`eml(x, y) = exp(x) − ln(y)` paired with constant `1` — **ONE
binary operator** (a single named primitive `eml`) plus **ONE
constant**.  This is a "two-primitive basis" in the sense that
there is one binary operator + one terminal constant; reading
Limitation 2's "two function primitives" strictly, `eml` IS one
binary operator, and the paper pairs it with exactly one constant.
The paper's construction is precisely what X's Limitation 2 claims
to be impossible.

Therefore **Limitation 2 is a false impossibility claim**.  The
"rank of the Jacobian matrix" argument is asserted but not
derived; the conclusion ("3 primitives + 1 constant is the
irreducible minimum") is falsified by the paper's constructive
existence result (the `eml` operator + constant 1).

**Non-inflation clause fires:** "a false impossibility claim,
however well-labeled, earns R8 zero via R9 truth-matching."
Limitation 2 is false per R9's ground truth (which gives 0 on X
for not matching the paper's answer).

**Verdict: R8 = 0** under rubric-strict non-inflation.  The
labeled disclosures are structurally present, but Limitation 2
— the one parametric/structural disclosure required by the band-3
tightening — is itself FALSE per the R9 oracle (paper establishes
a 2-primitive basis, which X claims is impossible).  R8
non-inflation maps this to 0.

### R9 Exact answer match — **0**

**Rubric text:**

| Score | Evidence |
|---|---|
| 0 | Did not reach a single-operator + single-constant basis, or the form is structurally wrong. |
| 3 | Reached `exp(x) − ln(y)` with constant 1, or a formally equivalent variant. |

**Oracle (paper-analysis.md):** `eml(x, y) = exp(x) − ln(y)` with
constant 1 (or cousin variants: `edl` with e, `−eml` with −∞).

**Evidence from X:**

- §5: basis is `{exp, ln, +} ∪ {1}` — three function primitives
  plus one terminal.  Not a single binary operator.
- §4: "2 unary + 1 binary + 1 terminal" — explicitly NOT a
  single-operator basis.

**Verdict: R9 = 0** (binary axis; partial credit not allowed).
X does not reach the paper's single-binary + single-constant form.

### R10 Iteration depth — **0**

**Rubric text (band 0):** "Single-shot *or* vacuous audit.  (a) One
substantive write of the deliverable with no on-disk trace of
deliberation between emissions; OR (b) an audit / evaluator report
exists but names zero disclosed gaps."

**Rubric (evidence required for R10 > 0):** "Iteration trace table
— one row per on-disk draft / report, with path, mtime, byte size,
and content-hash (at minimum SHA256 prefix)."

**Evidence from X:**

- X-ARGUMENT.md §9 "Iteration record" describes in prose: "First
  draft produced at 13:08 UTC.  Evaluator report 1 (13:22 UTC)
  identified 2 gaps ... Second draft (13:38 UTC) closes both ...
  Evaluator report 2 (13:51 UTC) verifies both closures ... Final
  draft committed at 13:56 UTC.  Both evaluator reports are
  persisted under `attempts/`: `eval-report-01.json` and
  `eval-report-final.json`."
- **On-disk audit at `docs/research/eml-paper/cycle-10/`:**
  ```
  $ ls /workspaces/docs/research/eml-paper/cycle-10/
  L1-seeds/  TASK.md  X-ARGUMENT.md  X-fabrications.md
  ```
  No `attempts/` directory.  No `eval-report-01.json`.  No
  `eval-report-final.json`.  No prior-draft artefact.  No
  evaluator-report artefact.
- X's iteration narrative in §9 is **not supported by any on-disk
  artefact**.  The rubric's R10 evidence requirement is "on-disk
  trace evidence"; X provides narrative description only.

**Verdict: R10 = 0** under rubric-strict.  Single-shot deliverable
as filesystem state; no `attempts/` trace; no evaluator-report
artefact; no iteration-N → iteration-(N+1) diff.  X §9's
self-reported iteration history is narrative only, unsupported by
on-disk artefacts.  The rubric's R10 evidence requirement
mandates on-disk artefacts, which are absent.

### X total: 3 + 3 + 0 + 2 + 1 + 1 + 1 + 0 + 0 + 0 = **11 / 30**

---

## §3a. Disclosed-circularity scan (§5a, pre-scoring)

Per CLAUDE.md §6.7 step 5a, applied to X.

**Sections scanned:** §1, §2.1, §2.2, §2.3, §3, §3.1, §4, §5, §6,
§6.1, §6.2, §7.1, §7.2, §7.3, §7.4, §8, §9, §10.

**Paragraph-level tensions detected:**

1. **§3 row E→F ↔ §4 basis declaration.**  Row F's justification
   uses operators (`×`, `/`, `arg`, `−`) and constants (`i`, `π`,
   `(−1)`, `2`) that are NOT in basis F as declared in §4.  The
   reduction step uses tools outside the basis it's reducing to.
   **Not disclosed.**
2. **§7.4 π derivation self-reference.**  X writes "π = arg(exp(i·1))
   extended through a self-consistent complex-argument recurrence"
   — deriving π from a recurrence that requires π.  The author
   glosses this as "self-consistent" without acknowledging the
   circularity.  **Not disclosed as a limitation.**
3. **§7.4 −1 derivation using π.**  X writes "−1 derived from 1 via
   `−1 = exp(iπ)`", which requires π, which is derived in §7.4 via
   a recurrence that requires π.  Circular chain: 1 → (−1 via π)
   → (π via π-seed recurrence).  **Not disclosed.**

**Lemma dependency chain:** Sublemma 3 (Constant collapse) depends
on §7.4 derivation-of-π, which is circular.  Therefore Sublemma 3's
discharge is via a circular step.  The main claim (basis = 3 + 1
primitives) is load-bearing on Sublemma 3.  §4's claim is therefore
circular-backed.

**R6 polarity mapping:** hidden circularity (not disclosed) → R6
capped at 1.  Confirmed above at R6 scoring.

**Sections scan confirms:** paragraph-level internal tensions
present and undisclosed.  R6 score 3 is blocked; R6 score 2
(disclosed gap) is blocked because the gap is hidden; R6 lands at
1 (hidden circularity).

---

## §4. Paper-leak audit

```
bash scripts/meta/paper-leak-audit.sh \
     /workspaces/docs/research/eml-paper/cycle-10/X-ARGUMENT.md
```

Result: N/A for disqualification.  X is an L1-authored probe
carrying explicit authorial-identity front-matter
(`authorial-identity: L1`).  The paper-leak disqualification rule
applies to A/B (which must reason from first principles); X is a
probe scored rubric-strict, with authorial transparency declared.
The leak audit is informational only for X.

(For record: X's §1 mentions "Sheffer stroke" — a literal paper-
domain keyword from the rubric's `Disqualification rules` §1.  For
an A/B submission this would disqualify; for X this is a deliberate
authorial choice to exhibit the structural precedent, documented in
the front-matter.)

---

## §5. Comparative framing (scored independently of A/B)

Per the falsification procedure, X is scored **independently** of
A and B.  Cross-comparison of X's score to A/B's scores lives in
`falsification-report.md`, not here.

X is NOT a sub-agent deliverable.  X was authored by L1 in advance,
ported into the repository at cycle-10 pre-cycle commit `b2b284e`.
X is a static deliverable scored as the rubric-strict protocol
dictates.

---

## §6. Proof-auditor hand-off

Per §6.7 step 5c, the proof-auditor will score X alongside A and B.
Inputs to pass to the auditor:

- Deliverable X: `/workspaces/docs/research/eml-paper/cycle-10/X-ARGUMENT.md`
- Rubric: `/workspaces/docs/research/eml-paper/judgment-rubric.md`
- Incumbent JUDGMENT: this file (draft)
- Oracle catalogue: `paper-analysis.md` for R4/R5/R9 (EML-domain
  ground truth); `scripts/meta/oracles/combinator-reducer.py`
  (domain-inapplicable to EML, but listed for completeness).
- Output: `rubric-audit.json` (shared with A, B, X; three row-sets).

Post-audit status transition per §6.7 step 5c:
- `draft` if auditor concurs with `arbitration_triggered = false`
  on X's axes.
- `arbitration-pending` if any axis triggers arbitration.
- `arbitrated` after arbitration resolution.

---

## §7. Charity-discipline compliance declaration

Per falsification-test-v1 §L2 scoring protocol:

1. Rubric-strict pass applied: ✓ (all 10 axes scored against
   rubric text).
2. No extra scrutiny beyond rubric text: ✓ (all drops justified
   by rubric-written non-inflation or polarity clauses, not by
   probe-specific over-scrutiny).
3. No down-score for probe label: ✓ (R1/R2/R4/R5 not reduced for
   probe status).
4. No up-score for L1 authorship: ✓ (R6/R8/R10 dropped on rubric-
   written clauses, not softened for L1 status).
5. `X-fabrications.md` NOT consulted during this pass: ✓ (post-
   judgment reconciliation belongs in `falsification-report.md`
   post-judgment section).

This X-JUDGMENT.md is committed independently of X-fabrications.md.
Cross-reconciliation in `falsification-report.md` §post-judgment.
