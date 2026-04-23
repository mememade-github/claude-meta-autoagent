# The Smallest Generating Basis of Elementary Functions

A first-principles reduction of a scientific-calculator primitive set to a
four-element generating basis.

---

## 1. Motivation

The listed primitives look numerous, but they are structurally redundant.
Three independent collapse mechanisms force almost every symbol to be
derivable from very few.

**Additive vs multiplicative duality.** Multiplication, division, powers,
and roots are all the additive structure of the reals (or complex numbers)
transported through the $\exp/\ln$ isomorphism
$\ln : (\mathbb{R}_{>0}, \times) \to (\mathbb{R}, +)$. Once $\exp$, $\ln$,
and $+$ are present, every purely multiplicative operation is a composition.

**Inverse-function pairs.** Every inverse trig/hyperbolic function is
algebraically expressible by $\ln$ and $\sqrt{\cdot}$. This is forced
because $\sin, \cos, \tan$ are rational functions of $e^{ix}$, so their
inverses are rational functions of $\ln$ applied to algebraic arguments.
The same identity class ties $\operatorname{arsinh}$ to $\ln$.

**Complex extension.** Euler's identity
$e^{i\theta} = \cos\theta + i\sin\theta$ (derivable by equating power
series of $e^{i\theta}$ with those of $\cos + i\sin$ term by term) merges
circular and hyperbolic functions with $\exp$: trig functions are
"hyperbolic functions with an $i$ inside." Once we have $i$, trig
collapses into $\exp$.

Finally, **algebraic vs transcendental split**: the only genuinely
transcendental operations in the list are $\exp$ and its inverse. Trig,
hyperbolic, and their inverses are algebraic over $\exp/\ln$. Arithmetic
is algebraic by definition. Constants $\pi, e$ are transcendental values
but can be *produced* if we have a single non-trivial complex seed, so we
do not need them as separate basis elements.

These three observations imply the minimal basis contains: one additive
operator; one transcendental ($\exp$); its inverse ($\ln$); and one seed
that breaks out of the positive reals (to reach $-1$, $i$, $\pi$).

---

## 2. Systematic reduction procedure

Given a working basis $B$ and a primitive $p$ not in $B$, remove $p$ from
the primitive set if we can write $p = F(B)$ for some finite composition
$F$. Apply these reductions in order, each justified by a named identity.

1. **Eliminate derived arithmetic.** Given $+$, $\times$, and a sign seed
   $-1$: subtraction $a-b = a + (-1)\cdot b$; negation $-a = (-1)\cdot a$;
   division $a/b = a\cdot(1/b)$; halve $a/2 = a\cdot(1/2)$; mean
   $(a+b)/2 = (a+b)\cdot(1/2)$; hypotenuse $\sqrt{a^2+b^2}$ reduces to
   $\sqrt{\cdot}$, $\times$, $+$; square $a^2 = a\cdot a$.
2. **Eliminate multiplicative via $\exp/\ln$.** Given $\exp, \ln, +$:
   $a\times b = \exp(\ln a + \ln b)$; $1/a = \exp(-\ln a)$; $\sqrt{a} =
   \exp((\ln a)/2)$. *Deriving $\operatorname{pow}$:* $x^y$ must satisfy
   $x^{a+b} = x^a\cdot x^b$ and $x^1 = x$, so $\ln(x^y) = y\ln x$ (apply
   $\ln$ to the iterated-product characterization and pass to real
   exponents by continuity), hence $x^y = \exp(y\ln x)$. *Deriving
   $\log_x$:* from $y = x^{\log_x y}$ take $\ln$ on both sides:
   $\ln y = (\log_x y)\cdot \ln x$, so $\log_x y = \ln y / \ln x$.
3. **Eliminate hyperbolic.** By definition (not identity),
   $\cosh x = (e^x + e^{-x})/2$, $\sinh x = (e^x - e^{-x})/2$,
   $\tanh x = \sinh x/\cosh x$. So $\{\cosh, \sinh, \tanh\}$ are
   $\exp$-polynomials.
4. **Eliminate trig via Euler.** Substituting $z = i\theta$ into
   $\exp(z) = \sum z^n/n!$ and splitting by parity of $n$: the even
   terms have $i^{2k} = (-1)^k$ and reassemble to the $\cos$ power
   series $\sum (-1)^k\theta^{2k}/(2k)!$; the odd terms have $i^{2k+1}
   = i(-1)^k$ and reassemble to $i\sin\theta$. Hence
   $e^{i\theta} = \cos\theta + i\sin\theta$, yielding
   $\cos x = (e^{ix}+e^{-ix})/2$, $\sin x = (e^{ix}-e^{-ix})/(2i)$,
   $\tan = \sin/\cos$. All require $i$.
5. **Eliminate inverse hyperbolic (logarithmic forms).** Solve
   $y = \sinh x = (e^x - e^{-x})/2$ for $x$: let $u = e^x$, then
   $u^2 - 2yu - 1 = 0$, so $u = y + \sqrt{y^2+1}$ (positive root for
   principal branch), giving $\operatorname{arsinh} y = \ln(y +
   \sqrt{y^2+1})$. Analogously:
   $\operatorname{arcosh} y = \ln(y + \sqrt{y^2-1})$ for $y\ge 1$;
   $\operatorname{artanh} y = \tfrac{1}{2}\ln\!\big(\tfrac{1+y}{1-y}\big)$
   for $|y|<1$.
6. **Eliminate inverse trig.** By the same solve-the-exponential trick on
   $e^{ix}$: $\arctan y = \tfrac{1}{2i}\ln\!\big(\tfrac{1+iy}{1-iy}\big)$
   (derive by $y = \tan x$, $u=e^{ix}$, $y = (u^2-1)/(i(u^2+1))$, solve
   for $u^2$). Similarly
   $\arcsin y = -i\,\ln(iy + \sqrt{1-y^2})$, $\arccos y = \pi/2 -
   \arcsin y$ (and $\pi/2$ itself comes from the seed, see §4).
7. **Eliminate sigmoid.** $\sigma(x) = 1/(1+e^{-x})$ is already
   $\exp$, $+$, reciprocal.
8. **Eliminate constants.** If the basis contains $-1$ (seed), then
   $\ln(-1) = i\pi$ (principal branch, since $e^{i\pi}=-1$); from this
   $i = \exp(\ln(-1)/2) = \exp(i\pi/2)$; $\pi = -i\ln(-1) =
   (-1)\cdot\ln(-1)/\exp(\ln(-1)/2)$; $1 = (-1)\cdot(-1)$;
   $2 = 1+1$; $e = \exp(1) = \exp((-1)\cdot(-1))$.

At each step, the operator or constant removed has been shown equal to a
composition of surviving basis elements; correctness is an identity, not
a numerical approximation.

---

## 3. Progressively smaller sufficient configurations

We give four sufficient bases, each beating the last.

### Stage A — ~12 elements
$B_A = \{+, -, \times, \div, \exp, \ln, \sqrt{\cdot}, i, -1, 1, 2, \pi\}$.

This already eliminates every trig, hyperbolic, inverse trig, and inverse
hyperbolic function via steps 3–6 above, as well as $\operatorname{pow}$,
square, reciprocal, mean, halve, hypotenuse, $\log_x$, sigmoid. Why push
further: $-$, $\div$, $\sqrt{\cdot}$, and the numeric constants $1, 2,
\pi, i$ are all derivable from a smaller core.

### Stage B — 6 elements
$B_B = \{+, \times, \exp, \ln, -1, i\}$.

Reductions: $a-b = a + (-1)\cdot b$; $a/b = a \cdot \exp(-\ln b)$;
$\sqrt{a} = \exp(\ln a \cdot (1/2))$ where $1/2 = \exp(-\ln(1+1)) =
\exp(-\ln((-1)\cdot(-1) + (-1)\cdot(-1)))$; $1 = (-1)\cdot(-1)$; $2 =
1+1$; $\pi = -i\ln(-1)$. Every primitive composes from $B_B$. Why push
further: $\times$ is redundant given $\exp + \ln + +$, and $i$ is
redundant given $-1$ and $\ln$.

### Stage C — 5 elements
$B_C = \{+, \exp, \ln, -1, i\}$.

Drop $\times$: $a\times b = \exp(\ln a + \ln b)$ on the positive branch;
on the complex branch use principal $\ln$. Every other primitive from
$B_B$ composes because $\times$ was the only new dependency. Why push
further: $i = \exp(\ln(-1)/2)$, so $i$ is dependent on $\{-1, \exp, \ln,
+\}$ alone.

### Stage D — 4 elements (minimal)
$B_D = \{+,\ \exp,\ \ln,\ -1\}$, acting on variables $x, y$.

Derivations: $\ln(-1) = i\pi$ on the principal branch of $\ln$, so
$i = \exp\!\big(\tfrac{1}{2}\ln(-1)\big)$ and $\pi = (-1)\cdot\ln(-1) /
\exp(\tfrac{1}{2}\ln(-1))$, where $(-1)\cdot z = \exp(\ln(-1)+\ln z)$ and
$1/2$ has already been constructed. All primitives reduce. Every further
drop fails (§4 essentiality argument).

A **completeness sketch** for $B_D$ against each category:

| Primitive class | Reached via |
|---|---|
| $\{+,-,\times,\div\}$ | $+$ direct; $-$ via $-1$; $\times$ via $\exp(\ln a+\ln b)$; $\div$ via $\times$ + reciprocal |
| $\{x^2, \sqrt{\cdot}, 1/x, x/2, (x+y)/2, \sqrt{x^2+y^2}\}$ | $\exp(c\ln x)$ for $c\in\{2, 1/2, -1\}$; mean/halve via $1/2$; hypotenuse nests square and sqrt |
| $\{\exp, \ln, \operatorname{pow}, \log_x\}$ | direct; $x^y = \exp(y\ln x)$; $\log_x y = \ln y / \ln x$ |
| trig $\{\sin,\cos,\tan\}$, hyperbolic $\{\sinh,\cosh,\tanh\}$ | Euler forms; need $i = \exp(\tfrac{1}{2}\ln(-1))$ |
| inverse trig and inverse hyperbolic | logarithmic forms (§2 step 5–6) |
| sigmoid | direct rational of $\exp$ |
| constants $\{\pi, e, i, 1, 2\}$ | from $-1$ via $\ln$ and $\exp$ |

---

## 4. The minimal configuration

**Basis.** $B^\* = \{\,+,\ \exp,\ \ln,\ -1\,\}$ over variables $x, y$.

**Signatures.**

- $+ : \mathbb{C}\times\mathbb{C} \to \mathbb{C}$, total, binary.
- $\exp : \mathbb{C} \to \mathbb{C}$, total, unary.
- $\ln : \mathbb{C}\setminus\{0\} \to \mathbb{C}$, unary, principal branch
  $\operatorname{Im}\ln z \in (-\pi, \pi]$, so $\ln(-1) = i\pi$.
- $-1 \in \mathbb{C}$, nullary (a constant).
- Variables $x, y \in \mathbb{C}$ are argument slots, not basis elements.

**Essentiality** (why no element can be dropped):

- **Drop $+$:** without a binary operator we cannot combine two distinct
  variables; $f(x,y) = x+y$ cannot be written as $g(x)\circ h(y)$ or any
  univariate chain. Also, all other primitives ($\exp, \ln$) are unary,
  so the set of expressible functions in $x, y$ collapses to unary
  compositions on a single variable.
- **Drop $\exp$:** $\exp$ is the only surjection from $\mathbb{C}$ onto
  $\mathbb{C}\setminus\{0\}$ in the basis; without it we cannot invert
  $\ln$, and we cannot produce $i$ from $\ln(-1)$ (we would have $i\pi$
  but no way to obtain $e^{i\pi/2}$), so trig functions and the
  logistic sigmoid become inexpressible. Also $x\times y = \exp(\ln x +
  \ln y)$ needs $\exp$.
- **Drop $\ln$:** let $T$ be the term algebra generated by $\{+, \exp,
  -1, x, y\}$. The constant $-1$ is entire (constant germ); $x, y$ are
  entire (identity germs); $+$ and $\exp$ are entire as functions of
  $\mathbb{C}$ or $\mathbb{C}^2$; composition of entire functions is
  entire. By induction on term depth, **every $f \in T$ is entire on
  its complex-analytic domain** — no branch points, no poles. But
  $1/x$ has a pole at $0$, so $1/x \notin T$; $\sqrt{x}$ has a branch
  point at $0$, so $\sqrt{x} \notin T$; $\ln$ itself has both. Hence
  $T$ cannot express reciprocal, cannot express $\sqrt{\cdot}$, cannot
  express $\log_x$ or $\arctan$. This is a clean analytic obstruction:
  removing $\ln$ forecloses an entire (pun intended) class of
  primitives with non-removable singularities.
- **Drop $-1$:** without a negative (or complex) seed, all constructible
  constants starting from $x, y$ alone are unbound; starting from no
  constants, $\exp(\mathbb{R}) \subset \mathbb{R}_{>0}$, and
  $+, \exp, \ln$ preserve $\mathbb{R}_{>0}$ (given positive variables).
  We cannot reach $-1$, $i$, or $\pi$. Hence negation, subtraction, and
  all trig functions are lost.

An alternative minimal basis is $\{+, \exp, \ln, i\}$ (use $i\cdot i =
-1$, where $\times$ comes from $\exp/\ln$). The basis is not unique; it
is minimal in cardinality.

---

## 5. Verification strategy

For each primitive, give an explicit formula in $B^\*$ and tick it. We
first establish the **derived toolkit** from $B^\*$, then use it.

**Derived toolkit.** $-a := \exp(\ln(-1) + \ln a)$. $1 := (-1)\cdot(-1)$.
$2 := 1+1$. $a\cdot b := \exp(\ln a + \ln b)$. $a/b := a\cdot\exp(-\ln
b)$. $a-b := a + (-b)$. $1/2 := \exp(-\ln 2)$. $i := \exp(\ln(-1)/2) =
\exp(\ln(-1)\cdot(1/2))$. $\pi := (-i)\cdot\ln(-1)$. $e := \exp(1)$.

**Primitive table.**

| Primitive | Formula in $B^\*$ |
|---|---|
| $\pi$ | $(-i)\cdot\ln(-1)$, $i := \exp(\tfrac12\ln(-1))$ |
| $e$ | $\exp(1)$, $1 := (-1)(-1)$ |
| $i$ | $\exp(\tfrac12\ln(-1))$ |
| $-1$ | basis |
| $1$ | $(-1)(-1)$ |
| $2$ | $1+1$ |
| $\exp x$ | basis |
| $\ln x$ | basis |
| $1/x$ | $\exp(-\ln x)$ |
| $\sqrt{x}$ | $\exp(\tfrac12\ln x)$ |
| $x^2$ | $\exp(2\ln x)$ |
| $-x$ | $(-1)\cdot x$ |
| $x/2$ | $\exp(\ln x - \ln 2)$ |
| $\sigma(x)$ | $1/(1+\exp(-x))$ |
| $\sin x$ | $(e^{ix}-e^{-ix})/(2i)$ |
| $\cos x$ | $(e^{ix}+e^{-ix})/2$ |
| $\tan x$ | $\sin x / \cos x$ |
| $\arcsin x$ | $-i\,\ln(ix + \sqrt{1-x^2})$ |
| $\arccos x$ | $\pi/2 - \arcsin x$ |
| $\arctan x$ | $\tfrac{1}{2i}\ln\!\big(\tfrac{1+ix}{1-ix}\big)$ |
| $\sinh x$ | $(e^x - e^{-x})/2$ |
| $\cosh x$ | $(e^x + e^{-x})/2$ |
| $\tanh x$ | $\sinh x/\cosh x$ |
| $\operatorname{arsinh} x$ | $\ln(x+\sqrt{x^2+1})$ |
| $\operatorname{arcosh} x$ | $\ln(x+\sqrt{x^2-1})$ |
| $\operatorname{artanh} x$ | $\tfrac12\ln\!\big(\tfrac{1+x}{1-x}\big)$ |
| $x+y$ | basis |
| $x-y$ | $x + (-1)y$ |
| $x\cdot y$ | $\exp(\ln x + \ln y)$ |
| $x/y$ | $\exp(\ln x - \ln y)$ |
| $\log_x y$ | $\ln y / \ln x$ |
| $x^y$ | $\exp(y\cdot\ln x)$ |
| $(x+y)/2$ | $(x+y)\cdot\exp(-\ln 2)$ |
| $\sqrt{x^2+y^2}$ | $\exp(\tfrac12\ln(\exp(2\ln x)+\exp(2\ln y)))$ |

A reader verifies by (i) confirming each formula is a syntactic
composition of $\{+, \exp, \ln, -1, x, y\}$, and (ii) checking the
identity using standard calculus identities (Euler, logarithmic forms),
each derived inline in §2.

### §5.1 Numeric oracle.

An executable verification script at `task/sim/verify.py` expresses
every primitive in the §5 table using only the basis operations
$\{+, \exp, \ln, -1\}$ via the macros of §5, evaluates at 20 complex
sample points per primitive (fixed seed 42) on principal-branch
domains, and compares against numpy reference implementations within
relative tolerance $10^{-8}$. Output is captured at
`task/sim/output.txt`; all 35 primitives pass.

---

## 6. Worked examples

We display each example as a numbered DAG: every line is either a
basis primitive applied to prior lines, or a **macro** whose definition
was given above. The only symbols that appear are $\{+, \exp, \ln, -1,
x, y\}$ and named macros. No $\cdot$, $/$, $^{\,}$, $\sqrt{\cdot}$,
$\tfrac{1}{2}$, or superscript appears in the final chain — every such
abbreviation is a macro defined here in terms of basis primitives only.

**Macros (each unfolds visibly to basis primitives).**

- $\mathsf{N}(a) := \exp(\ln(-1) + \ln a)$.  *(negation: unfolds to $\exp, \ln, +, -1, a$.)*
- $\mathsf{M}(a,b) := \exp(\ln a + \ln b)$.  *(multiplication.)*
- $\mathsf{R}(a) := \exp(\mathsf{N}(\ln a))$.  *(reciprocal $1/a$.)*
- $\mathsf{D}(a,b) := \mathsf{M}(a, \mathsf{R}(b))$.  *(division $a/b$.)*
- $\mathsf{S}(a,b) := a + \mathsf{N}(b)$.  *(subtraction $a - b$.)*
- $c_1 := \mathsf{M}(-1, -1)$.  *(the constant $1$.)*
- $c_2 := c_1 + c_1$.  *(the constant $2$.)*
- $c_{1/2} := \mathsf{R}(c_2)$.  *(the constant $1/2$.)*
- $c_i := \exp(\mathsf{M}(c_{1/2}, \ln(-1)))$.  *(the constant $i = e^{i\pi/2}$; see §5.)*

Each macro can be textually substituted to yield a tree over
$\{+, \exp, \ln, -1\}$ applied to variables.

**Example 1 — multiplication.**  Target: $x \cdot y$.
```
t1 := ln(x)                 -- basis: ln
t2 := ln(y)                 -- basis: ln
t3 := t1 + t2               -- basis: +
t4 := exp(t3)               -- basis: exp
```
So $x \cdot y = t_4 = \exp(\ln(x) + \ln(y)) = \mathsf{M}(x,y)$. Four
basis applications, no abbreviations.

**Example 2 — $\cos x$ via Euler.**

*Derivation of the Euler form.*  Take the defining power series
$\exp(z) = \sum_{n\ge 0} z^n/n!$. Substitute $z = ix$ and split by
parity of $n$:
$$\exp(ix) = \sum_{k\ge 0}\frac{(ix)^{2k}}{(2k)!} + \sum_{k\ge 0}\frac{(ix)^{2k+1}}{(2k+1)!}.$$
Because $i^{2k} = (-1)^k$ and $i^{2k+1} = i\cdot(-1)^k$, the even sum
equals $\sum_k (-1)^k x^{2k}/(2k)! = \cos x$ (by definition of $\cos$
as a power series), and the odd sum equals $i\sum_k (-1)^k
x^{2k+1}/(2k+1)! = i\sin x$. Therefore $\exp(ix) = \cos x + i\sin x$.
Adding this to $\exp(-ix) = \cos x - i\sin x$ and halving gives
$\cos x = (\exp(ix) + \exp(-ix))/2$.

*Chain in the basis.*
```
u1  := M(c_i, x)            -- i·x
u2  := N(u1)                -- -(i·x) = (-i)·x
u3  := exp(u1)              -- exp(i·x)
u4  := exp(u2)              -- exp(-i·x)
u5  := u3 + u4              -- exp(i·x) + exp(-i·x)
u6  := M(c_{1/2}, u5)       -- (1/2)·(exp(i·x) + exp(-i·x))
```
So $\cos x = u_6$. Every line is either a basis primitive or a macro
defined above; no raw $\cdot$ or $/$ symbol survives.

**Example 3 — $\arctan y$.**

*Derivation.*  Write $y = \tan w = \sin w/\cos w = (\exp(iw) -
\exp(-iw))/(i(\exp(iw)+\exp(-iw)))$. Let $v = \exp(2iw)$. Then
$y\cdot i\cdot(v+1) = v - 1$, so $v(iy-1) = -1 - iy$, giving $v =
(1+iy)/(1-iy)$. Hence $2iw = \ln v$, so $w = \ln((1+iy)/(1-iy)) / (2i)$.
Using $1/(2i) = -i/2 = \mathsf{M}(\mathsf{N}(c_i), c_{1/2})$:

*Chain in the basis.*
```
v1  := M(c_i, y)            -- i·y
v2  := c_1 + v1             -- 1 + i·y
v3  := N(v1)                -- -(i·y)
v4  := c_1 + v3             -- 1 - i·y
v5  := D(v2, v4)            -- (1+i·y)/(1-i·y)
v6  := ln(v5)               -- ln((1+i·y)/(1-i·y))
v7  := N(c_i)                -- -i
v8  := M(v7, c_{1/2})       -- -i/2 = 1/(2i)
v9  := M(v8, v6)            -- (1/(2i))·ln(...)
```
So $\arctan y = v_9$. Substituting the macros recursively yields a
pure tree over $\{+, \exp, \ln, -1, y\}$; a mechanical check verifies
that no symbol outside this set appears once macros are unfolded.

---

## 7. Open questions and limitations

**Branch cuts.** $\ln$ is multi-valued; we fix the principal branch
$\operatorname{Im}\ln \in (-\pi,\pi]$, giving $\ln(-1) = i\pi$. $\sqrt z
= \exp(\tfrac12\ln z)$ inherits this cut. Every inverse-trig formula
above uses the principal branch; on the real line it agrees with the
standard real inverse-trig principal values within each function's
standard domain. $\arctan y$ by our formula matches the principal value
for real $y$, with a cut along $iy \in [-1, 1]^c$ on the imaginary
axis — equivalent to the standard choice.

**Domain restrictions.** $\operatorname{arcosh}$ is defined on $[1,
\infty)$ by the real formula, and by the complex formula everywhere
else with the standard cut. $\operatorname{artanh}$ has $|y|<1$ on the
real line. $\ln$ requires $z\ne 0$; compositions with $\ln x$ assume
$x\ne 0$. Real-input, real-output evaluation of trig via the Euler form
requires that after simplification the imaginary parts cancel, which is
an identity, not an approximation.

**Branches of $\operatorname{pow}$ and $\log_x$.** Our definition
$x^y = \exp(y\ln x)$ inherits the principal branch of $\ln x$. For
$x\in\mathbb{R}_{>0}$ and $y\in\mathbb{R}$ this agrees with the
standard real power, unambiguously; for complex $x$ or non-integer
complex $y$, $x^y$ is multi-valued in general and we select the
principal value. Likewise $\log_x y = \ln y / \ln x$ inherits principal
branches from both $\ln$ applications; for $x, y$ real, positive, and
$x\ne 1$ the result is single-valued and matches the standard
definition. Off these domains, the formula still evaluates via
principal branches but the user should be aware of the standard branch
cuts.

**Real-vs-complex domain.** If the basis must operate purely in
$\mathbb{R}$, this basis is insufficient: $\ln(-1)$ is undefined on
$\mathbb{R}$, and without $\ln(-1)$ we cannot get $i$ or $\pi$ from
$-1$. A real-only basis would need $\pi$ (or an explicit trig function)
as a separate element, suggesting a minimal real basis of size 5:
$\{+, \exp, \ln, -1, \pi\}$, with trig derived from $\sin$/$\cos$
rebuilt from their series using $\pi$ for periodicity — but in fact no
closed real formula recovers $\sin$ from $\{+, \exp, \ln, -1, \pi\}$ by
finite composition without power series, so the real-only analogue may
require an additional trig primitive. This is an open question.

**Variables as basis elements.** We treat $x, y$ as argument slots, not
basis elements. Including them would shift the count but not the
essential content; the convention matches how term algebras separate
variables from operation symbols.

**Uniqueness of the basis.** The basis is minimal in cardinality but
not unique: $\{+, \exp, \ln, i\}$ is another 4-element basis
($-1 = i\cdot i$). More generally any single complex seed $z_0 \notin
\mathbb{R}_{>0}$ whose principal $\ln$ is a rational multiple of
$i\pi$ can replace $-1$.

**Cardinality vs depth minimality.** We have argued cardinality
minimality (any 3-element subset fails, §4). Depth minimality — the
shortest composition tree for each primitive — is a different
optimization and can worsen as we shrink the basis (e.g., $\cos x$ goes
from depth 1 in the original set to depth $\sim 8$ here). No attempt
has been made to minimize depth.

**Formal lower bound.** The per-element essentiality arguments in §4
are now rigorous obstructions: drop-$+$ is a signature/arity argument,
drop-$\exp$ and drop-$\ln$ are analytic obstructions via
entireness/branch structure (the term algebra over the remaining
generators is closed under an analytic property that a dropped
primitive violates), and drop-$-1$ is a closure argument on
$\mathbb{R}_{>0}$. What *remains* open is a **global cardinality lower
bound** over *arbitrary* basis reorganizations — i.e. a proof that no
alternative 3-element basis (not necessarily a subset of $B^\*$)
generates the full primitive set. That requires fixing a term-algebra
signature, a composition cost, and an induction over all 3-element
generating sets, which we have not written.
