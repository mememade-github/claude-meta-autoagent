# Paper Analysis — Argument Chain Summary

> Internal ROOT-only reference. Summarizes Odrzywolek (arXiv:2603.21852) so the ROOT Agent
> can judge A/B argument chains without re-reading the paper each cycle. Keep this file
> inside `docs/research/eml-paper/` — it must never be mounted into A/B containers.

## 1. Motivation

**Core question.** Boolean logic has NAND (the Sheffer stroke) — a single two-input gate
from which every Boolean circuit can be built. Continuous mathematics has had no comparable
primitive: calculators expose many distinct buttons, and classical reductions (logarithm
tables, slide rule, Euler's formula, the exp-log representation) stop at "a few" primitives
without reaching one. The paper asks whether the diversity of elementary functions is
intrinsic, or whether a smaller generative basis exists — ideally, a single binary operator
paired with a single constant.

**Named precedents** (for R1 grading). The paper explicitly invokes these as structural
analogs for a single-primitive universal basis:

- NAND / Peirce Arrow (NOR) — Boolean universality [Sheffer stroke]
- Op-amp — positive/negative feedback processes
- ReLU — modern deep-learning activation
- K, S combinators — combinatory logic
- Interaction Combinators
- Wolfram's single axiom; Rule 110; SUBLEQ (OISC); FRACTRAN
- DNA/RNA — near-universal information carrier in biology
- The "einstein" (ein Stein) aperiodic monotile

A strong R1 answer invokes NAND (or equivalent Boolean universality) as motivation and
frames the search as "does a continuous analog exist?".

## 2. Method

**Iterative ablation** over the 36-primitive scientific-calculator list (Table 1 in the
paper: 8 constants/variables + 20 unary functions + 8 binary operators).

1. Remove one element from the active set.
2. Test whether the remaining set can reconstruct every original primitive.
3. Keep configurations that work; discard those that do not.
4. Repeat until no further removal succeeds.

**Numeric bootstrap verification** (key trick).

- Direct symbolic verification is computationally intractable for expression depths ≥ 7.
- Substitute variables with **algebraically independent transcendental constants** not in the
  exp-log class — e.g. x = γ ≈ 0.577216 (Euler-Mascheroni), y = A ≈ 1.28243 (Glaisher-Kinkelin).
- Evaluate the target numerically; compare against expressions generated from the candidate
  operator set.
- Under **Schanuel's conjecture**, coincidental numerical equality between such expressions
  is vanishingly unlikely → reliable sieve for candidate formulas.
- Candidates passing the sieve are then verified symbolically (Mathematica) and cross-checked
  numerically across four implementations (C, NumPy, PyTorch, mpmath).

**Framing.** The "broken calculator" problem (popular puzzle genre): what can you compute
with a reduced set of keys? The paper treats the endpoint of this process — reduction to a
single binary operator with a single distinguished constant — as the unexplored target.

A strong R2 answer proposes (a) systematic ablation and (b) a numerical witness test with
algebraically independent inputs, or an equivalent verification strategy that can distinguish
true from coincidental identities.

## 3. Progression

Table 2 of the paper records the historical reduction sequence:

| Configuration | Constants | Unary | Binary | Count |
|---|---|---|---|---|
| Base-36 | (Table 1) | (Table 1) | (Table 1) | 36 |
| Wolfram | π, e, i | ln | +, ×, ^ | 7 |
| Calc 3 | none | exp, ln, −x, 1/x | + | 6 |
| Calc 2 | none | exp, ln | − | 4 |
| Calc 1 | e or π | — | x^y, log_x(y) | 4 |
| Calc 0 | none | exp | log_x(y) | 3 |
| EML | 1 | — | eml(x,y) | 3 |

Key transitions:
- **Calc 3 → Calc 2**: dropping negation/reciprocal, using non-commutative subtraction
  (subtraction provides both tree-growth and inversion capability).
- **Calc 2 → Calc 1**: top-down shift to rank-3 hyperoperations (exponentiation and
  arbitrary-base logarithm).
- **Calc 1 → Calc 0**: absorbing e into exp itself.
- **Calc 0 → EML**: combining inverse functions at the input (exp, ln) with asymmetric
  subtraction at the output.

A strong R3 answer names ≥3 intermediate configurations with justification for each step.

## 4. Minimal basis

**The EML operator:**

```
eml(x, y) = exp(x) − ln(y)
```

paired with the constant **1**.

**Why 1 is required.** The logarithmic term must be neutralized via ln(1) = 0; without a
terminal that achieves this, the operator cannot bootstrap arithmetic.

**Why no further reduction is possible.** At least one binary operator and at least one
terminal symbol are required for any non-trivial expression grammar.

**Cousins (near-variants discovered afterwards):**

- `edl(x, y) = exp(x) / ln(y)` with constant e
- `−eml(y, x) = ln(x) − exp(y)` with constant −∞

**Internal domain.** Computations must run over **ℂ** using the principal branch, since
generating constants like i and π requires ln(−1).

A strong R4 answer reaches exactly the structure "one binary operator + one constant." R5
additionally requires the correct form `exp(x) − ln(y)` (or an equivalent cousin) with
constant 1 (or e / −∞ for cousins).

## 5. Verification strategy

**Constructive completeness via bootstrapping:**

1. Start with sets S₀ = {1, eml}, C₀ = every primitive from Table 1.
2. Search for an expression computing some element of C_i using only primitives in S_i.
3. On success, move that element from C_i to S_{i+1}.
4. Repeat until C_i = ∅.

**Independent checks** (Supplementary Information Part II):

- Symbolic simplification of the full discovery chain in Mathematica.
- Numerical cross-validation across four implementations (C, NumPy, PyTorch, mpmath).
- Constructive completeness proof sketch for the Table 1 class.

A strong R6 answer proposes the numeric-substitution sieve (algebraic independence +
Schanuel-style reasoning) and backs it with symbolic cross-checking.

## 6. Worked examples

Canonical identities derived in the paper (abbreviated: E = eml):

- `e = eml(1, 1)` — the constant e emerges from the terminal alone.
- `e^x = eml(x, 1)` — exp is depth-1.
- `ln(z) = eml(1, eml(eml(1, z), 1))` — logarithm is depth-3, RPN code `11xE1EE`.
- `x − y`, `x + y`, `x × y`, `x / y` all expressible; depths range from ~11 to ~27.
- Trigonometric identities derived via Euler's formula over the complex domain.

Depth table (from paper Table 4): identity (depth 9), reciprocal (15), negation (15),
multiplication (19), arbitrary-base log (29).

A strong R7 answer gives ≥3 examples spanning different categories (transcendental,
arithmetic, derived constant).

## 7. Limits and open questions

**Domain constraints.**

- Real-axis evaluation works almost everywhere, except at isolated singular points (zero,
  domain endpoints, branch cuts).
- Internal computations must use the complex principal branch.
- Branch-cut artifacts: `ln(−1) = iπ` via the naive `ln z = eml(1, eml(eml(1, z), 1))`
  picks up a 2πi jump on the negative real axis; EML compiler corrects the i sign manually.

**Implementation quirks.**

- Works in: Mathematica (symbolic), IEEE754 `<math.h>`, NumPy, PyTorch.
- Breaks in: pure Python/Julia (special floats raise errors), Lean 4 (assigns
  Complex.log 0 = 0 as a "junk value" to keep log total).

**Open structural questions flagged by the paper.**

1. A **ternary variant** is mentioned as requiring no distinguished constant at all
   ("tip of the iceberg" note in the abstract).
2. Whether a **pure-real** Sheffer operator exists (i.e. without needing the complex
   principal branch internally) is open.
3. Whether cousins beyond EML / EDL / −EML exist systematically.
4. Whether the 5·2ⁿ − 6 parameter count for the level-n master formula can be reduced
   further.

A strong R8 answer names at least one of these — ternary variant, pure-real Sheffer, or
constant-dependence analysis — in its own terms.

## Application to scoring

When grading an A or B ARGUMENT.md against this analysis:

- **R1–R8** are 0–3 each → 24 points.
- **R9** (exact match to minimal basis): binary operator + single distinguished constant
  in eml / edl / −eml form, or a formally equivalent variant → 0 or 3 (no partial credit).
- Total: 27.

Cross-reference the full rubric in `judgment-rubric.md` (sibling file).

## Source

Odrzywolek, A. *All elementary functions from a single operator.*
arXiv:2603.21852v2 [cs.SC], 4 Apr 2026.
Full text at `./paper.pdf`, OCR at `./paper.txt` (same directory).
