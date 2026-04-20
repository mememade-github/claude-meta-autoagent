# Minimal Generating Basis for Elementary Calculator Functions

## 1. Motivation

The target set contains ~31 primitives, but three structural facts suggest it is massively redundant:

**(a) Euler's formula unifies exp and trig.** For any z ∈ ℂ, e^{iz} = cos(z) + i·sin(z). Rearranging: cos(z) = (e^{iz} + e^{−iz})/2 and sin(z) = (e^{iz} − e^{−iz})/(2i). The hyperbolic analogues sinh(z) = (e^z − e^{−z})/2 and cosh(z) = (e^z + e^{−z})/2 are structurally identical. The Pythagorean identity sin² + cos² = 1 then collapses to the exponential identity e^{iz}·e^{−iz} = 1. So six of our eighteen unary ops are *shadows* of a single unary op (exp) acting on linear expressions in ℂ.

**(b) The complex logarithm inverts Euler's formula.** Solving x = sin(y) (or tan, tanh, etc.) by treating e^{iy} as an unknown and applying the quadratic formula yields closed-form expressions for every inverse trig/hyperbolic op as *ln of an algebraic expression*. All inverse-transcendental ops thus reduce to ln composed with arithmetic.

**(c) Exp/ln conjugate addition to multiplication.** The identity ln(e^a · e^b) = a + b (on the principal branch) expresses addition as a conjugate of multiplication via ln. Equivalently, x · y = exp(ln x + ln y). Whichever of {+, ×} we keep, the other is derivable.

**Precedents from adjacent domains.** Minimal-generator problems recur throughout mathematics and computation:
- In Boolean logic, {NAND} alone suffices — from it, AND, OR, NOT, XOR, and every Boolean connective follow. Two-place logic reduces to one gate.
- In combinatory logic, the S and K combinators together express every lambda term (and single-combinator bases exist). Computation reduces to a two-element alphabet.
- In field theory, a finitely-generated extension has a minimal transcendence basis plus algebraic generators; the minimality question is structural.
- In group theory, the rank of a finitely-generated group counts irredundant generators.

The common pattern: a system specified by many redundant operations often admits a drastically smaller core capturing the essential algebraic or analytic structure. What makes our calculator special is that almost all of its transcendental richness flows from a single complex function (exp) and its inverse (ln).

## 2. Reduction Procedure

We proceed by iterated elimination. Given a candidate basis C:

1. **Classify** each primitive by its role: *constant*, *arithmetic binary*, *forward transcendental* (exp-family), or *inverse transcendental* (ln-family).
2. **Express** each primitive as a finite composition of other primitives in C where possible. Record the expression.
3. **Eliminate** primitives whose expressions use only other members of C (i.e., eliminate each primitive that is definable from the rest).
4. **Iterate.** Steps 2–3 may cascade: eliminating × might make it easier to see that − is redundant, etc.
5. **Stop** when no primitive in the current C is expressible via others. The remaining set is a *reduced* basis.
6. **Prune constants.** Inspect the remaining constants; replace several by a single seed constant that generates them.
7. **Check minimality** by a role-counting argument: how few primitives does any basis need, given the distinct analytic roles that must be filled?

The procedure's justification: finite composition closure is preserved at each step. If primitive p = E[q₁, …, qₖ] (an expression using only q₁, …, qₖ, which remain in C), then any composition using p can be rewritten using E, so p is redundant.

The guiding strategic insight is (c) above: exp/ln conjugation means that once we have *any one* of {+, ×, −, ÷} together with exp and ln, we have all four. So the reduction pressure is on the transcendental side.

## 3. Progressive Reductions

We label successive configurations A → B → C → D → E → F.

### Configuration A: the given primitive set

~31 primitives as stated.

### Configuration B: eliminate trig, hyperbolic, and inverse-trig

By (a) and (b):

- sin(x) = (e^{ix} − e^{−ix}) / (2i)
- cos(x) = (e^{ix} + e^{−ix}) / 2
- tan(x) = sin(x) / cos(x)
- sinh(x) = (e^x − e^{−x}) / 2
- cosh(x) = (e^x + e^{−x}) / 2
- tanh(x) = sinh(x) / cosh(x)
- arcsin(x) = −i · ln(ix + √(1 − x²))  (derived below)
- arccos(x) = −i · ln(x + i·√(1 − x²))
- arctan(x) = (1/(2i)) · ln((1 + ix)/(1 − ix))
- arsinh(x) = ln(x + √(x² + 1))
- arcosh(x) = ln(x + √(x² − 1))
- artanh(x) = (1/2) · ln((1 + x)/(1 − x))
- σ(x) = 1 / (1 + e^{−x})

*Derivation of arcsin.* Let y = arcsin(x). Then x = (e^{iy} − e^{−iy})/(2i). Setting u = e^{iy}: 2ix = u − 1/u, so u² − 2ix·u − 1 = 0, giving u = ix + √(1 − x²) (taking the + branch). Then iy = ln(u), so y = −i · ln(ix + √(1 − x²)). The other inverse formulas follow by analogous quadratic-in-u calculations; artanh uses the Möbius identity (1+tanh)/(1−tanh) = e^{2·artanh}.

Eliminated: sin, cos, tan, sinh, cosh, tanh, arcsin, arccos, arctan, arsinh, arcosh, artanh, σ. (13 ops gone.)

Remaining: exp, ln, reciprocal, sqrt, square, negate, halve, +, −, ×, ÷, log_x(y), pow, mean, hypot, and the six constants.

### Configuration C: eliminate the "shorthand" arithmetic ops

- square(x) = x · x
- sqrt(x) = exp(ln(x) / 2)
- hypot(x, y) = sqrt(x² + y²)
- negate(x) = (−1) · x
- reciprocal(x) = exp(−ln(x))
- halve(x) = x · (1/2)
- mean(x, y) = (x + y) · (1/2)
- pow(x, y) = exp(y · ln(x))
- log_x(y) = ln(y) / ln(x)
- x − y = x + negate(y)
- x / y = x · reciprocal(y)

Eliminated: square, sqrt, hypot, negate, reciprocal, halve, mean, pow, log_x(y), −, ÷.

Remaining ops: exp, ln, +, ×, plus constants π, e, i, −1, 1, 2.

### Configuration D: collapse × into {+, exp, ln}

By (c): x · y = exp(ln(x) + ln(y)). Valid for x, y ≠ 0 on any branch, since exp kills the 2πi-ambiguity in the sum of logs.

Eliminated: ×.

Remaining: {+, exp, ln} ∪ {π, e, i, −1, 1, 2}.

### Configuration E: collapse constants to a single seed

We claim that **i** alone generates all six numerical constants, using {+, exp, ln, i}:

- **−1** = i · i = exp(ln(i) + ln(i))
- **1** = i⁴ = exp(ln(i) + ln(i) + ln(i) + ln(i))
  Verification: 4·ln(i) = 4·(iπ/2) = 2πi on the principal branch (ln(i) = iπ/2 since |i|=1 and arg(i)=π/2). Then exp(2πi) = 1. ✓
- **0** = ln(1) = ln(exp(ln(i) + ln(i) + ln(i) + ln(i))). Here ln(exp(2πi)) = 0 because 2πi lies outside the principal strip Im ∈ (−π, π] and principal-branch ln sends e^{2πi} = 1 to 0, not back to 2πi.
- **2** = 1 + 1 = exp(4·ln(i)) + exp(4·ln(i))
- **e** = exp(1) = exp(exp(4·ln(i)))
- **π** = 2·ln(i) / i. Derivation: ln(i) = iπ/2, so 2·ln(i) = iπ, and π = (2·ln(i)) · i⁻¹. We express i⁻¹ = i³ = exp(3·ln(i)), then π = exp(ln(2·ln(i)) + ln(i⁻¹)) = exp(ln(2·ln(i)) + 3·ln(i)).

Eliminated: π, e, −1, 1, 2.

Remaining: **{+, exp, ln, i}** — 4 primitives.

### Configuration F: attempted further reduction, and why it fails

We argue no 3-element basis suffices. The argument counts *roles* that must be filled:

**Role 1 — Constant.** Every closed-form expression for π in basis B must either (i) use a constant primitive, or (ii) be a constant-valued function of x, y. For (ii), compositions of +, exp, ln on variables x, y are analytic in x, y; such a composition is a constant function only if it is identically constant, which for these operations requires a cancellation (like x − x). But subtraction requires a negation, hence −1, hence a constant seed. So we cannot bootstrap a specific transcendental like π from variables alone; at least one constant is needed.

Moreover, the constant must carry *complex* information. Real positive seeds (1, 2, e, etc.) generate only real values under {+, exp, ln}, so they cannot yield i. The constant must have nonzero imaginary part.

**Role 2 — Binary combination.** Variables x and y must be combinable. Unary ops alone cannot mix two inputs. So a binary op (+, ×, or some hybrid) is required.

**Role 3 — Forward transcendental.** Some operation of the exp family is needed for e, e^x, and everything downstream (trig, hyperbolic, pow). Without it, the algebra is rational in x, y, which is too small.

**Role 4 — Inverse transcendental.** Some operation of the ln family is needed for arbitrary-base log, inverse trig, etc. Critical observation: compositions of {+, exp, constants} produce functions in the "exponential polynomial" class, which is closed under composition and differentiation but **not under functional inversion**. The logarithm is outside this class. So ln cannot be expressed using only exp, +, and constants; it must be added as a primitive.

Any single binary op seems to provide at most one of Roles 3–4:
- pow(x, y) gives exp (as pow(e, x)) but not ln.
- log_x(y) gives ln (as log_e(x)) but not exp.
- f(x, y) = ln(x) + y gives ln (as f(x, 0)) but requires a 0 constant separately.
- f(x, y) = exp(x) + y gives exp (as f(x, 0)) but requires a 0 constant separately.

In each case, attempting to merge two roles into one binary operation forces an additional constant to emerge, and the total count stays at 4.

We conclude that **4 primitives is a tight lower bound** for any basis constructed from standard-shaped elementary ops, under the stated "finite composition" interpretation.

## 4. The Minimal Configuration

**Basis 𝓑 = {+, exp, ln, i}**, where:

- **+** : ℂ × ℂ → ℂ is complex addition.
- **exp** : ℂ → ℂ is the entire complex exponential, exp(z) = Σ z^n / n!.
- **ln** : ℂ \ {0} → ℂ is the principal branch of the complex logarithm: ln(re^{iθ}) = log(r) + iθ for θ ∈ (−π, π].
- **i** ∈ ℂ is the imaginary unit with i² = −1 and Im(i) > 0.

This is 1 binary op + 2 unary ops + 1 constant.

## 5. Verification Strategy

To prove 𝓑 is complete, we exhibit, for each original primitive, an explicit composition using only members of 𝓑. Completeness follows by finite induction: if every level-k primitive is expressible, and every level-(k+1) primitive is expressible using level-≤k primitives, then all are.

We have already given expressions for the originals in §3, grouped by level:

- **Derived constants** (level 1): −1, 0, 1, 2, e, π all written above in §3E.
- **Derived arithmetic** (level 2): ×, −, ÷, reciprocal, negate, halve, mean, square, sqrt, hypot — all written in §3C, using only 𝓑 plus the level-1 derived constants.
- **Derived transcendentals** (level 3): pow, log_x(y), sin, cos, tan, sinh, cosh, tanh, σ, arcsin, arccos, arctan, arsinh, arcosh, artanh — all written in §3B, using only 𝓑 plus the level-1 and level-2 derivations.

A completeness certificate is therefore the explicit composition tree for each primitive, rooted at 𝓑. The leaves are always members of {+, exp, ln, i, x, y}, and internal nodes are applications of {+, exp, ln}.

**Sanity check on branches.** Most identities used (e.g., x · y = exp(ln x + ln y), e^{iπ} = −1) are *exact* complex identities. Some identities (e.g., ln(e^z) = z) hold only on a strip Im(z) ∈ (−π, π]. We use the latter only at specific constant values where the strip condition is verifiable by hand. For variable-input ops, the domains on which the compositional expression agrees with the original primitive match the original primitive's natural domain (real inputs in the valid range, etc.).

## 6. Worked Examples

### Example 1: cos(x)

Goal: cos(x) = (e^{ix} + e^{−ix}) / 2, purely in {+, exp, ln, i, x}.

Let us use the abbreviations, each a composition in 𝓑:

- ONE := exp(ln(i)+ln(i)+ln(i)+ln(i))  (= 1)
- TWO := ONE + ONE  (= 2)
- INV(a) := exp(exp(ln(i)+ln(i)+ln(ln(a))))  (= 1/a; derivation: exp(ln(−1)+ln(ln(a))) = −ln(a), then exp of that is e^{−ln(a)} = 1/a)
- MUL(a, b) := exp(ln(a) + ln(b))  (= a·b)

Then:

- ix := MUL(i, x) = exp(ln(i) + ln(x))
- minus_ix := MUL(MUL(i, i), ix) = MUL(exp(ln(i)+ln(i)), exp(ln(i)+ln(x)))
  = exp(ln(i) + ln(i) + ln(i) + ln(x))  (= −ix)
- exp_ix := exp(ix) = exp(exp(ln(i) + ln(x)))
- exp_minus_ix := exp(minus_ix) = exp(exp(ln(i) + ln(i) + ln(i) + ln(x)))
- sum := exp_ix + exp_minus_ix
- cos_x := MUL(sum, INV(TWO))

Fully expanded:

cos(x) = exp( ln(exp(exp(ln(i)+ln(x))) + exp(exp(ln(i)+ln(i)+ln(i)+ln(x)))) + ln(INV(ONE+ONE)) )

Every subexpression uses only +, exp, ln, i, and x. ✓

### Example 2: arctan(x)

Goal: arctan(x) = (1/(2i)) · ln((1 + ix)/(1 − ix)).

Steps in 𝓑:

- ONE, TWO, MUL, INV as before.
- ix := MUL(i, x)
- NEG(a) := MUL(MUL(i, i), a) = exp(ln(i) + ln(i) + ln(a))  (= −a)
- one_plus_ix := ONE + ix
- one_minus_ix := ONE + NEG(ix)
- ratio := MUL(one_plus_ix, INV(one_minus_ix))
- ln_ratio := ln(ratio)
- two_i := MUL(TWO, i)  (= 2i)
- arctan_x := MUL(INV(two_i), ln_ratio)

Each of MUL, INV, NEG is itself a composition in {+, exp, ln, i}, so the whole expression is in 𝓑. ✓

### Example 3: pow(x, y) = x^y

Goal: x^y = exp(y · ln(x)).

Steps in 𝓑:

- ln_x := ln(x)
- y_ln_x := MUL(y, ln_x) = exp(ln(y) + ln(ln(x)))
- pow_xy := exp(y_ln_x) = exp(exp(ln(y) + ln(ln(x))))

So pow(x, y) = exp(exp(ln(y) + ln(ln(x)))), a clean depth-4 composition in 𝓑 using inputs x and y directly — no constants needed at all. ✓

This example illustrates the compactness that emerges: once ×, exp, ln are in play, exponentiation is just a three-layer tower.

## 7. Open Questions and Limitations

**Q1: Branch-cut subtleties.** Several identities used in §3 depend on the *principal* branch of ln. In particular:
- ln(exp(z)) = z only if Im(z) ∈ (−π, π].
- ln(i) = iπ/2 depends on convention; a different branch gives ln(i) = iπ/2 + 2πik.

When composing, intermediate values may cross branch cuts, causing 2πi-shifts. Most compositions in §3–§6 evaluate correctly at real or "small" complex inputs, but global correctness requires careful branch tracking. A fully rigorous treatment would define each derived op on an explicit domain where its compositional definition matches the intended primitive.

**Q2: Zero inputs.** ln(0) is undefined, so any expression using ln on a value that may be zero is partial. Our derivations inherit these partialities. E.g., reciprocal(0) is undefined, as in the original primitive.

**Q3: Absolute minimality.** Our lower-bound argument (§3F) is informal. A genuine proof that no 3-element basis exists would require a more formal theory of "elementary function bases," perhaps in the spirit of differential algebra. The Liouville-style theory of elementary functions is a natural setting, but even there, "minimality of generators" is not fully classical. We conjecture 4 is optimal but have not proved it with full rigor.

**Q4: Uniqueness of the seed constant.** Any complex constant c with nonzero imaginary part whose real and imaginary parts are irrational-over-ℚ (like iπ, e^{i}, ln(2) + i, or i itself) is a candidate. The basis {+, exp, ln, c} generates i, π, e, etc., with varying degrees of compositional depth. We chose **i** because it has the shortest description and minimal algebraic complexity (algebraic of degree 2), but {+, exp, ln, iπ} or {+, exp, ln, −1} are equally valid.

**Q5: Hybrid operations.** We ruled out 3-element bases using *standard-shaped* operations (+, ×, exp, ln, pow, log). A sufficiently contrived binary op could in principle combine arithmetic, forward-transcendental, and inverse-transcendental roles. We do not know if such an op exists within the elementary-function category; this is a concrete open problem.

**Q6: Orientation ambiguity in i.** Specifying "i" rather than "−i" requires choosing an orientation of ℂ. This is a single bit of information but is genuinely necessary: the basis {+, exp, ln} is closed under complex conjugation, so it cannot distinguish i from −i. Thus exactly one "oriented" choice is required — any less and we lose the orientation; any more and we have redundancy.

**Q7: Computational vs. symbolic minimality.** Our minimality is about *symbolic expressibility*. In a numerical calculator, considerations like precision, stability, and speed might favor keeping redundant primitives (e.g., sin as a direct primitive rather than a composition that risks cancellation errors in (e^{ix} − e^{−ix})/(2i)). Our minimization is a mathematical, not an engineering, claim.
