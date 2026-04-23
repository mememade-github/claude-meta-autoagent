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
   \exp((\ln a)/2)$; $a^b = \exp(b\cdot\ln a) = \exp(b\cdot\ln a)$ (note
   recursion: $\times$ is itself a composition, so $a^b = \exp(\exp(\ln b
   + \ln\ln a))$ on the positive branch). $\log_a b = \ln b / \ln a$.
3. **Eliminate hyperbolic.** By definition (not identity),
   $\cosh x = (e^x + e^{-x})/2$, $\sinh x = (e^x - e^{-x})/2$,
   $\tanh x = \sinh x/\cosh x$. So $\{\cosh, \sinh, \tanh\}$ are
   $\exp$-polynomials.
4. **Eliminate trig via Euler.** From the power-series identity
   $e^{i\theta} = \cos\theta + i\sin\theta$,
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
- **Drop $\ln$:** without $\ln$, the only way to leave $\{-1\}$ is via
  $\exp$ and $+$; but $\exp$ and $+$ starting from $\{-1\}$ generate
  only a recursively enumerable set closed under $\exp$ and $+$,
  containing no $\arctan$-like inverse, no $\log_x$, no square root.
  Inverses of $\exp$ (needed for $\operatorname{pow}$, $\sqrt{\cdot}$,
  inverse trig) are inexpressible.
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

---

## 6. Worked examples

Fully expanded chains in $B^\*$.

**Example 1 — multiplication (algebraic reduction).**
$$x \cdot y \;=\; \exp\big(\ln x + \ln y\big).$$
Syntax tree: $\exp(\ +\ (\ln(x),\ \ln(y)))$. Three basis applications.

**Example 2 — $\cos$ (Euler reduction).** Build $i$ first:
$$i \;=\; \exp\!\Big(\exp\big(\ln(\ln(-1)) + \ln(\exp(-\ln(1+1)))\big)\Big),$$
which is $\exp(\tfrac12 \ln(-1))$ unfolded: $1+1 = 2$, $\exp(-\ln 2) =
1/2$, $\ln(-1)\cdot(1/2) = \exp(\ln(\ln(-1)) + \ln(1/2)) = \tfrac12
\ln(-1)$. Then
$$\cos x \;=\; \tfrac12\big(\exp(i\cdot x) + \exp((-i)\cdot x)\big),$$
expanding the outer $\tfrac12$ and $\cdot$ as $\exp(\ln(\cdot)+\ln(1/2))$
and $\exp(\ln(\cdot)+\ln(\cdot))$ respectively, and $-i = (-1)\cdot i$.
Derivation of Euler form: equate term-by-term
$e^{i\theta} = \sum (i\theta)^n/n! = \cos\theta + i\sin\theta$ by
splitting even and odd $n$; this gives $\cos\theta = (e^{i\theta} +
e^{-i\theta})/2$ by adding $e^{i\theta}$ and $e^{-i\theta}$.

**Example 3 — $\arctan$ (inverse-trig reduction).** Starting from
$y = \tan x = \sin x/\cos x = (e^{ix}-e^{-ix})/(i(e^{ix}+e^{-ix}))$. Let
$u = e^{2ix}$. Then $y = (u-1)/(i(u+1))$, so $iy(u+1) = u-1$, giving
$u(iy - 1) = -1 - iy$, hence $u = (1+iy)/(1-iy)$. Therefore
$2ix = \ln u = \ln\!\big((1+iy)/(1-iy)\big)$, so
$$\arctan y \;=\; \frac{1}{2i}\,\ln\!\Big(\frac{1+iy}{1-iy}\Big).$$
In $B^\*$: $1+iy = 1 + i\cdot y$ uses $+$, $\cdot$ (expanded as
$\exp(\ln i + \ln y)$), and $i$ as constructed. Division is
$\exp(\ln(1+iy) - \ln(1-iy))$. The outer $\tfrac{1}{2i}$ is $(-i/2)$
(since $1/i = -i$), i.e. $(-1)\cdot i\cdot\exp(-\ln 2)$. So the full
chain is
$$\arctan y = (-1)\cdot i\cdot\exp(-\ln 2)\cdot\ln\!\Big(\exp\big(\ln(1+iy)-\ln(1-iy)\big)\Big).$$

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

**Formal lower bound.** The essentiality argument in §4 is a
structural/semantic argument (set-closure considerations), not a
theorem in a fully formalized term algebra. A rigorous lower bound
would fix a term-algebra signature, a composition cost, and a
generation relation, then prove by induction that no 3-element subset
generates the full primitive set. We assert this holds but have not
written the induction.
