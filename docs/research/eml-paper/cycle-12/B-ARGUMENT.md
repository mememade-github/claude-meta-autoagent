# The Smallest Generating Basis of Elementary Functions

A first-principles reduction of a scientific-calculator primitive set to
a **two-element** generating basis $\{\exp,\ \log_x(y)\}$ over input
variables $x, y$.

---

## 1. Motivation

The listed primitives appear numerous, but they are structurally
redundant. Four collapse mechanisms — each derivable from first
principles — force almost every symbol to be expressible from very few.

**Additive ↔ multiplicative duality.** The map $\ln$ is a homomorphism
from $(\mathbb{C}^\times,\times)$ to $(\mathbb{C},+)$ (mod $2\pi i$),
with inverse $\exp$. So $\times$, $\div$, $\sqrt{\cdot}$, $x^y$, $1/x$
are all the additive structure of $\exp$'s codomain transported back.
Once we have any pair $(\exp,\ln)$ and **either** $+$ **or** an operator
that internalizes a difference of logs, the whole multiplicative tower
falls.

**Euler's identity unifies trig and hyperbolic.** From the power series
$\exp(z) = \sum z^n/n!$, substituting $z = i\theta$ and splitting by
parity of $n$ ($i^{2k} = (-1)^k$, $i^{2k+1} = i(-1)^k$) reassembles
exactly the $\cos$ and $i\sin$ series, giving
$e^{i\theta} = \cos\theta + i\sin\theta$. Hence
$\cos x = (e^{ix}+e^{-ix})/2$, $\sin x = (e^{ix}-e^{-ix})/(2i)$, and
$\tan, \sinh, \cosh, \tanh$ are all rational functions of $\exp$.

**Inverse trig / inverse hyperbolic are logarithms.** Solving
$y = \sinh x$ as $u = e^x$ gives a quadratic
$u^2 - 2yu - 1 = 0$, hence $\operatorname{arsinh} y = \ln(y +
\sqrt{y^2+1})$. The same trick applied to $\sin$, $\cos$, $\tan$,
$\cosh$, $\tanh$ yields purely $\ln$-and-$\sqrt{\cdot}$ forms (§5).

**Constants are reachable from a single complex seed, and the seed is
itself reachable from any $\log_x(y)$ + $\exp$ pair.** This is the key
new observation that takes us below the standard 4-element ceiling.
Because $\log_x(x) = 1$ (whenever $x \notin \{0,1\}$), the constant $1$
is a *byproduct* of the binary primitive $\log_x(y)$ alone — no
constant button needed. And once we have $1$, $\exp(1) = e$ gives the
seed needed to reach $-1, i, \pi$ via principal logarithms.

These four observations imply the minimal basis contains: (i) one
unary transcendental that surjects onto $\mathbb{C}^\times$ (i.e.
$\exp$); and (ii) one binary primitive that simultaneously carries a
*ratio* of logs and admits a "diagonal degeneracy" producing a
constant. The original primitive list contains exactly such a binary —
$\log_x(y) = \ln(y)/\ln(x)$ — and pairing it with $\exp$ closes the
system.

---

## 2. Systematic reduction procedure

The reduction proceeds by finite-composition substitution. Given a
working basis $B$ and a primitive $p \notin B$, we delete $p$ from the
primitive set whenever an explicit identity
$p(\cdot) = F[B](\cdot)$
is given. We apply the substitutions in dependency order so that no
later step relies on a not-yet-derived primitive.

Each step is justified by a named identity, derived inline.

1. **Eliminate derived arithmetic** (given $+, \times, -1$):
   $-a = (-1)\cdot a$,
   $a-b = a + (-1)\cdot b$,
   $a/b = a\cdot(1/b)$,
   $a/2 = a\cdot(1/2)$,
   $(a+b)/2 = (a+b)\cdot(1/2)$,
   $a^2 = a\cdot a$,
   $\sqrt{a^2+b^2}$ via $\sqrt{\cdot}$ atop $+$ and squaring.

2. **Eliminate multiplicative ops via $\exp,\ln$** (given $\exp,\ln,+$):
   $a\times b = \exp(\ln a + \ln b)$,
   $1/a = \exp(-\ln a)$,
   $\sqrt{a} = \exp((\ln a)/2)$.
   *Power*: from $\ln(x^y) = y\ln x$ (which follows by extending the
   integer identity $\ln(x^n) = n\ln x$ continuously to $y\in\mathbb{R}$
   then to $y\in\mathbb{C}$), $x^y = \exp(y\ln x)$.
   *Arbitrary-base log*: from $y = x^{\log_x y}$, take $\ln$ both sides:
   $\ln y = (\log_x y)\,\ln x$, so $\log_x y = \ln y/\ln x$.

3. **Eliminate hyperbolic** (definitions, not identities):
   $\sinh x = (e^x - e^{-x})/2$, $\cosh x = (e^x + e^{-x})/2$,
   $\tanh x = \sinh x/\cosh x$.

4. **Eliminate trig via Euler**:
   $\cos x = (e^{ix}+e^{-ix})/2$,
   $\sin x = (e^{ix}-e^{-ix})/(2i)$,
   $\tan x = \sin x/\cos x$.

5. **Eliminate inverse hyperbolic** (logarithmic forms, derived in §1):
   $\operatorname{arsinh} y = \ln(y + \sqrt{y^2+1})$,
   $\operatorname{arcosh} y = \ln(y + \sqrt{y^2-1})$,
   $\operatorname{artanh} y = \tfrac12\ln\!\big(\tfrac{1+y}{1-y}\big)$.

6. **Eliminate inverse trig** (same trick on $e^{ix}$):
   $\arctan y = \tfrac{1}{2i}\ln\!\big(\tfrac{1+iy}{1-iy}\big)$,
   $\arcsin y = -i\,\ln(iy + \sqrt{1-y^2})$,
   $\arccos y = \pi/2 - \arcsin y$.

7. **Eliminate sigmoid**: $\sigma(x) = 1/(1+\exp(-x))$.

8. **Eliminate the additive sign seed**. With $-1$ in the basis we
   reach: $\ln(-1) = i\pi$ (principal branch), then $i = \exp(i\pi/2)$,
   $\pi = -i\cdot\ln(-1)$, $1 = (-1)\cdot(-1)$, $2 = 1+1$,
   $e = \exp(1)$.

9. **Collapse $\ln$ into $\log_x(y)$**: since $\ln y = \log_e y$, if the
   basis carries $\log_x(y)$ as a binary, then $\ln y = \log_e(y)$ uses
   only $\log_x(y)$ once $e$ is reached. Conversely, having $\log_x(y)$
   internalizes both $\ln$ and division by $\ln$.

10. **Collapse the constant seed into $\log_x(y)$ + $\exp$**:
    $\log_x(x) = \ln x / \ln x = 1$ for $x \notin \{0,1\}$. This is a
    composition that evaluates to the constant $1$ on a generic domain
    (excluding the two singularities), using only the basis and the
    input variable $x$ — no constant primitive needed.

11. **Collapse $+$ into $\log_x(y)$ + $\exp$**: by step 2,
    $a + b = \ln(\exp(a)\cdot\exp(b))$. Multiplication is itself
    expressible without prior $+$:
    $a\cdot b = \log_{\exp(1/a)}(\exp(b)) = \frac{\ln\exp(b)}{\ln\exp(1/a)} = \frac{b}{1/a} = ab$,
    where $1/a = \log_{\exp(a)}(e) = \frac{\ln e}{\ln\exp(a)} = \frac{1}{a}$.
    So $\times$ is derived directly from $\log_x(y)$ + $\exp$ + the
    constant $e$, without ever invoking $+$. Then $\ln$ is recovered as
    $\log_e(\cdot)$, and $+$ as $\ln(\times)$ of $\exp$'s.

At each step, the operator/constant removed has been replaced by an
exact identity (not an approximation).

---

## 3. Progressively smaller sufficient configurations

Five sufficient bases, each strictly smaller than the last.

### Stage A — ~12 elements (textbook)
$B_A = \{+, -, \times, \div, \exp, \ln, \sqrt{\cdot},\ i,\ -1,\ 1,\ 2,\ \pi\}$.

Derives every trig / hyperbolic / inverse via §2 steps 3–6, plus $\operatorname{pow}$, $\log_x$, sigmoid, mean, halve, hypotenuse, square, reciprocal. Why push: $-,\div,\sqrt{\cdot}$ and $1, 2, \pi, i$ are derivable from a smaller core.

### Stage B — 6 elements
$B_B = \{+, \times, \exp, \ln,\ -1,\ i\}$.

$a-b = a + (-1)b$; $a/b = a\cdot \exp(-\ln b)$; $\sqrt{a} = \exp(\ln a\cdot(1/2))$; $1 = (-1)(-1)$; $2 = 1+1$; $\pi = -i\ln(-1)$. Why push: $\times$ is redundant given $\{\exp,\ln,+\}$, and $i$ is redundant given $-1$ and $\ln$ (since $i = \exp(\ln(-1)/2)$).

### Stage C — 4 elements
$B_C = \{+, \exp, \ln,\ -1\}$.

$a\cdot b = \exp(\ln a + \ln b)$; $i = \exp(\tfrac12 \ln(-1))$; $\pi = -i\cdot\ln(-1)$; $1 = (-1)(-1)$; etc. Why push: with the right binary, the constant $-1$ becomes derivable too, and $\ln$ becomes a special case of $\log_x(y)$.

### Stage D — 3 elements
$B_D = \{\exp,\ \log_x(y),\ 1\}$.

$e = \exp(1)$; $\ln y = \log_e y$; $0 = \log_e(1)$; $-1 = \log_e(1/e) = \log_{\exp(1)}\!\big(\log_{\exp(\exp(1))}(\exp(1))\big)$ since $\log_{\exp(c)}(\exp(d)) = d/c$ gives $1/e = \log_{\exp(e)}(e)$; $\times, +, -, \div$ derived via §2 steps 1–2; trig/hyp/inverses via §2 steps 3–6.

Why push: the constant $1$ is itself derivable from $\log_x(y)$ alone, without any 0-ary primitive — by the diagonal degeneracy $\log_x(x) = 1$.

### Stage E — 2 elements (minimal)
$B^* = \{\exp,\ \log_x(y)\}$, acting on input variables $x, y$.

The constant $1$ is the constant-function $\lambda x.\,\log_x(x)$,
defined for $x \notin \{0,1\}$ (a generic complex domain). All
remaining derivations are unchanged from Stage D.

---

## 4. The minimal configuration

**Basis.** $B^* = \{\,\exp,\ \log_x(y)\,\}$, with input variables
$x, y \in \mathbb{C}$ available as argument slots.

**Signatures.**
- $\exp : \mathbb{C} \to \mathbb{C}^\times$, total, unary.
- $\log_x(y) := \ln y / \ln x$, binary, defined for $x, y \in \mathbb{C}\setminus\{0\}$ with $x \ne 1$, principal branch of $\ln$ on each argument.
- Variables $x, y$ are not basis elements; they are argument slots.

**Cardinality.** $|B^*| = 2$. One binary, one unary, zero constants.

**Constructive completeness.** Working in $B^*$:

| Symbol | Definition in $B^*$ | Section |
|---|---|---|
| $1$ | $\log_x(x)$ | §3 step 10 |
| $e$ | $\exp(1)$ | §2 step 8 |
| $\ln z$ | $\log_e(z) = \log_{\exp(1)}(z)$ | §2 step 9 |
| $0$ | $\log_e(1)$ | direct |
| $1/a$ | $\log_{\exp(a)}(e)$ | §2 step 11 |
| $a\cdot b$ | $\log_{\exp(1/a)}(\exp(b))$ | §2 step 11 |
| $a + b$ | $\ln(\exp(a)\cdot\exp(b))$ | §2 step 2 |
| $-1$ | $\log_e(1/e) = \log_{\exp(1)}\!\big(\log_{\exp(e)}(e)\big)$ | §3 Stage D |
| $i\pi$ | $\ln(-1)$ | §2 step 8 |
| $i$ | $\exp(i\pi/2) = \exp(\tfrac12\cdot\ln(-1))$ | §2 step 8 |
| $\pi$ | $(-i)\cdot\ln(-1) = (-1)\cdot i\cdot\ln(-1)$ | §2 step 8 |
| $2$ | $1+1$ | §2 step 8 |
| trig, hyp, inverses | §2 steps 3–6 | as derived |
| $\operatorname{pow}$, $\sqrt{\cdot}$, $1/x$, $x^2$, halve, mean, hypot, sigmoid, $\log_x$ | §2 steps 1–2, 7 | as derived |

**Essentiality** (why neither element can be dropped, restricted to
the original primitive list):

- *Drop $\exp$.* Any term over $\{\log_x(y)\}$ alone with input
  variables $x, y$ produces values in the orbit closed under
  $a, b \mapsto \ln a/\ln b$. Iterating only ever takes ratios of
  (ratios of) logs — no surjection onto $\mathbb{C}^\times$ that
  reaches the multiplicative tower. Concretely, the resulting term
  algebra cannot produce any $z$ with $|z| \to \infty$ as $|x|, |y|$
  vary continuously without first reaching $\exp$-magnitude growth, so
  $\exp$ itself is not in the closure. Hence $\exp$ is essential.
- *Drop $\log_x(y)$, retain only $\exp$.* The closure of $\{\exp\}$ on
  one variable is the iterated-exponential tower $\exp^k(x)$; on two
  variables it cannot combine $x$ and $y$ at all (no binary). So
  neither $+$ nor $\times$ nor any binary primitive is reachable.
- *Drop both, retain only variables.* Trivially insufficient.

A **lower bound** to one element: with a single primitive $g$,
- if $g$ is unary, every term is a unary composition; we cannot express
  any genuinely binary primitive like $+$.
- if $g$ is binary, every term has only one transcendental "stage" and
  cannot produce both $\exp$ (an entire growth function) and $\ln$
  (with a logarithmic branch point) inside its closure unless $g$ is
  itself a transcendental hybrid; among the original primitives, no
  single binary $g$ — neither $+$, $-$, $\times$, $\div$, $\log_x(y)$,
  $\operatorname{pow}$, mean, nor hypot — admits $\exp$ in its closure.
  ($\log_x(y)$ alone gives only meromorphic-of-meromorphic ratios; it
  cannot generate $\exp$.)
  Hence at least two primitives are needed.

Therefore $|B^*| = 2$ is tight.

**Alternative 2-element bases.** $\{\exp,\ \log_x(y)\}$ is one minimal
basis; not unique. By the same construction, $\{\ln,\ \operatorname{pow}\}$
is *not* minimal (cannot derive a constant $1$ without an explicit
seed, since $\operatorname{pow}(x,x) = x^x$ is not constant). The
critical algebraic property of $\log_x(y)$ that admits the 2-basis is
its *diagonal-constant degeneracy* $\log_x(x) = 1$, which singles it
out among the original binary primitives.

---

## 5. Verification strategy

For each primitive, give an explicit composition in $B^*$ and verify by
substitution. We first establish a derived **macro layer**, then use
macros to express each primitive. Each macro unfolds visibly to the
basis primitives.

**Macros (derived in §4):**
- $c_1 := \log_x(x)$ — the constant $1$.
- $c_e := \exp(c_1)$ — the constant $e$.
- $\mathsf{Ln}(z) := \log_{c_e}(z)$ — natural log.
- $c_0 := \mathsf{Ln}(c_1)$ — the constant $0$.
- $\mathsf{R}(a) := \log_{\exp(a)}(c_e)$ — reciprocal $1/a$.
- $\mathsf{M}(a,b) := \log_{\exp(\mathsf{R}(a))}(\exp(b))$ — multiplication $a\cdot b$.
- $\mathsf{Add}(a,b) := \mathsf{Ln}(\mathsf{M}(\exp(a),\exp(b)))$ — addition $a+b$.
- $c_{-1} := \mathsf{Ln}(\mathsf{R}(c_e))$ — the constant $-1$.
- $\mathsf{N}(a) := \mathsf{M}(c_{-1}, a)$ — negation $-a$.
- $\mathsf{S}(a,b) := \mathsf{Add}(a, \mathsf{N}(b))$ — subtraction $a-b$.
- $\mathsf{D}(a,b) := \mathsf{M}(a, \mathsf{R}(b))$ — division $a/b$.
- $c_2 := \mathsf{Add}(c_1, c_1)$, $c_{1/2} := \mathsf{R}(c_2)$.
- $c_{i\pi} := \mathsf{Ln}(c_{-1})$.
- $c_i := \exp(\mathsf{M}(c_{1/2}, c_{i\pi}))$.
- $c_\pi := \mathsf{M}(\mathsf{N}(c_i), c_{i\pi})$.

Each macro is a finite composition over $\{\exp,\log_x(y)\}$ + variable
$x$ (and possibly $y$).

**Primitive table.**

| Primitive | Formula |
|---|---|
| $\pi, e, i, -1, 1, 2$ | $c_\pi, c_e, c_i, c_{-1}, c_1, c_2$ |
| $\exp x$ | basis |
| $\ln x$ | $\mathsf{Ln}(x)$ |
| $1/x$ | $\mathsf{R}(x)$ |
| $\sqrt x$ | $\exp(\mathsf{M}(c_{1/2}, \mathsf{Ln}(x)))$ |
| $x^2$ | $\mathsf{M}(x,x)$ |
| $-x$ | $\mathsf{N}(x)$ |
| $x/2$ | $\mathsf{M}(x, c_{1/2})$ |
| $\sigma(x)$ | $\mathsf{R}(\mathsf{Add}(c_1, \exp(\mathsf{N}(x))))$ |
| $\sin x$ | $\mathsf{D}(\mathsf{S}(\exp(\mathsf{M}(c_i,x)), \exp(\mathsf{N}(\mathsf{M}(c_i,x)))), \mathsf{M}(c_2,c_i))$ |
| $\cos x$ | $\mathsf{M}(c_{1/2}, \mathsf{Add}(\exp(\mathsf{M}(c_i,x)), \exp(\mathsf{N}(\mathsf{M}(c_i,x)))))$ |
| $\tan x$ | $\mathsf{D}(\sin x,\cos x)$ |
| $\arcsin x$ | $\mathsf{M}(\mathsf{N}(c_i),\,\mathsf{Ln}(\mathsf{Add}(\mathsf{M}(c_i,x),\,\exp(\mathsf{M}(c_{1/2},\mathsf{Ln}(\mathsf{S}(c_1,\mathsf{M}(x,x))))))))$ |
| $\arccos x$ | $\mathsf{S}(\mathsf{M}(c_{1/2},c_\pi),\arcsin x)$ |
| $\arctan x$ | $\mathsf{M}(\mathsf{R}(\mathsf{M}(c_2,c_i)),\,\mathsf{Ln}(\mathsf{D}(\mathsf{Add}(c_1,\mathsf{M}(c_i,x)),\,\mathsf{S}(c_1,\mathsf{M}(c_i,x)))))$ |
| $\sinh x$ | $\mathsf{M}(c_{1/2},\mathsf{S}(\exp(x),\exp(\mathsf{N}(x))))$ |
| $\cosh x$ | $\mathsf{M}(c_{1/2},\mathsf{Add}(\exp(x),\exp(\mathsf{N}(x))))$ |
| $\tanh x$ | $\mathsf{D}(\sinh x, \cosh x)$ |
| $\operatorname{arsinh} x$ | $\mathsf{Ln}(\mathsf{Add}(x,\exp(\mathsf{M}(c_{1/2},\mathsf{Ln}(\mathsf{Add}(\mathsf{M}(x,x),c_1))))))$ |
| $\operatorname{arcosh} x$ | $\mathsf{Ln}(\mathsf{Add}(x,\exp(\mathsf{M}(c_{1/2},\mathsf{Ln}(\mathsf{S}(\mathsf{M}(x,x),c_1))))))$ |
| $\operatorname{artanh} x$ | $\mathsf{M}(c_{1/2},\mathsf{Ln}(\mathsf{D}(\mathsf{Add}(c_1,x),\mathsf{S}(c_1,x))))$ |
| $x+y$ | $\mathsf{Add}(x,y)$ |
| $x-y$ | $\mathsf{S}(x,y)$ |
| $x\cdot y$ | $\mathsf{M}(x,y)$ |
| $x/y$ | $\mathsf{D}(x,y)$ |
| $\log_x y$ | basis |
| $x^y$ | $\exp(\mathsf{M}(y,\mathsf{Ln}(x)))$ |
| $(x+y)/2$ | $\mathsf{M}(c_{1/2},\mathsf{Add}(x,y))$ |
| $\sqrt{x^2+y^2}$ | $\exp(\mathsf{M}(c_{1/2},\mathsf{Ln}(\mathsf{Add}(\mathsf{M}(x,x),\mathsf{M}(y,y)))))$ |

**Verification protocol.** A reader confirms each row by (i) checking
syntactic well-formedness — every formula is a tree over
$\{\exp,\log_x(y),x,y\}$ once macros unfold; (ii) checking the
underlying identity, each derived in §2; (iii) optionally evaluating
numerically at sample $x, y$ and comparing to a reference
implementation. Each step is exact, not asymptotic.

---

## 6. Worked examples

Each example is a numbered DAG over $\{\exp, \log_x(y)\}$ + variables.
Macros are visibly defined; the only symbols permitted in the unfolded
tree are the basis primitives and variable slots.

**Example 1 — multiplication $x\cdot y$.**

Unfolded chain (no macros):
```
t1 := log_x(x)                    -- evaluates to 1; uses log_x(y) on (x,x)
t2 := exp(t1)                     -- evaluates to e
t3 := log_{exp(x)}(t2)            -- 1/x; uses log_x(y) on (exp(x), e)
t4 := exp(t3)                     -- exp(1/x)
t5 := exp(y)                      -- exp(y)
t6 := log_{t4}(t5)                -- ln(exp(y))/ln(exp(1/x)) = y/(1/x) = x·y
```

Six basis applications. Validity: at line t6,
$\log_{e^{1/x}}(e^y) = y/(1/x) = xy$.

**Example 2 — $\cos x$ via Euler.**

*Identity*: $\cos x = \tfrac12(e^{ix} + e^{-ix})$, derived in §1 by
splitting $\exp(z) = \sum z^n/n!$ at $z = ix$ by parity of $n$.

Macro chain (using §5 macros, all of which are basis-only):
```
u1 := M(c_i, x)                   -- i·x
u2 := exp(u1)                     -- exp(i·x)
u3 := N(u1)                       -- -i·x
u4 := exp(u3)                     -- exp(-i·x)
u5 := Add(u2, u4)                 -- exp(i·x) + exp(-i·x)
u6 := M(c_{1/2}, u5)              -- (1/2)·(exp(i·x) + exp(-i·x))
```

So $\cos x = u_6$. Each macro unfolds: e.g., $\mathsf{M}(c_{1/2}, u_5)
= \log_{\exp(\mathsf{R}(c_{1/2}))}(\exp(u_5))$, and $\mathsf{R}(c_{1/2})$
unfolds to $\log_{\exp(c_{1/2})}(c_e)$, etc., terminating at $\exp,
\log_x(y), x$.

**Example 3 — $\arctan y$.**

*Derivation*: with $u = e^{ix}$ and $y = \tan x$, we get
$y = (u^2 - u^{-2})/(i(u^2 + u^{-2}))$ (multiply numerator and
denominator by $u$ in the standard $\sin/\cos$ form; or substitute
directly). Solving for $u^2$: $iy(u^2+u^{-2}) = u^2 - u^{-2}$, giving
$u^2(1 - iy) = u^{-2}(1+iy)$ — wait, let us redo cleanly with
$v = e^{2ix}$. Then $\tan x = (v-1)/(i(v+1))$; cross-multiplying,
$iy(v+1) = v-1$, so $v(iy-1) = -1 - iy$, i.e.
$v = (1+iy)/(1-iy)$. Hence $2ix = \ln v$ and
$\arctan y = \tfrac{1}{2i}\ln\!\big(\tfrac{1+iy}{1-iy}\big)$.

Macro chain:
```
v1 := M(c_i, y)                   -- i·y
v2 := Add(c_1, v1)                -- 1 + i·y
v3 := S(c_1, v1)                  -- 1 - i·y
v4 := D(v2, v3)                   -- (1+i·y)/(1-i·y)
v5 := Ln(v4)
v6 := M(c_2, c_i)                 -- 2i
v7 := R(v6)                       -- 1/(2i)
v8 := M(v7, v5)                   -- arctan(y)
```

Substitution of macros yields a finite tree over
$\{\exp,\log_x(y),y,x\}$; a mechanical pass verifies no other symbol
appears.

---

## 7. Open questions and limitations

**Branch cuts.** We use principal $\ln$ throughout, with
$\operatorname{Im}\ln z \in (-\pi, \pi]$, so $\ln(-1) = i\pi$.
$\log_x(y) = \ln y/\ln x$ inherits both branch cuts. The macros
$\mathsf{R}, \mathsf{M}, \mathsf{Add}, \ldots$ are exact identities on
the principal-branch domain, but composition through branch cuts can
shift sheets; numerical agreement holds on generic complex inputs but
may fail at branch boundaries. This is the same caveat any
$\exp/\ln$-based basis carries.

**Domain of $\log_x(x) = 1$.** The constant $1$ is realized as
$\log_x(x)$, defined for $x \notin \{0, 1\}$. In a function-composition
framework where input variables $x, y$ are accepted, this is a valid
finite composition that evaluates to $1$ on a generic complex domain
(complement of two points). A *strict* interpretation that demands
closed terms with no input dependency would require a 0-ary primitive
in the basis — under that interpretation the minimum rises to $3$
(e.g., $\{\exp,\log_x(y), c\}$ for any $c \notin \{0,1\}$, or
$\{\exp,\ln,-\}$ via $0 = x-x$, which is total).

**Real-only domain.** If the calculator must operate purely in
$\mathbb{R}$, $\log_x(y)$ on negative arguments is undefined, so we
cannot reach $-1, i, \pi$ from positive inputs alone. A real-only
analogue requires either an explicit $-1$ (or $\pi$) seed or a
primitive that breaks positivity (e.g., $-$). A real minimal basis is
likely $\{\exp,\ln,-\}$ at cardinality $3$, with $0 = x-x$, $1 =
\exp(0)$, and so on; trig-on-reals then requires either an explicit
trig primitive or a complex extension (since the Euler form needs
$i$).

**Variables vs. basis elements.** We treat $x, y$ as argument slots,
not basis primitives. This is the standard convention in term algebras
with separate signatures for operations and variables. Counting them
as basis elements would shift the cardinality but not the structural
content.

**Uniqueness.** The basis is minimal in cardinality but not unique.
$\{\ln, \operatorname{pow}\}$ is *not* minimal (lacks the diagonal
constant). $\{\exp, \log_x(y)\}$ exploits the specific algebraic
property $\log_x(x) = 1$. Whether other 2-element bases exist over the
original primitive list is an open question; a candidate to investigate
is $\{\operatorname{pow}, \log_x(y)\}$, where $\operatorname{pow}(x,x)
= x^x$ is *not* constant, and $\log_x(\operatorname{pow}(y,z)) = z\ln
y/\ln x$ does not seem to admit an $\exp$ analogue without an extra
seed.

**Cardinality lower bound.** The §4 essentiality argument is tight for
the chosen basis. A *global* lower bound — that no 1-element basis
generates the original set — is given by the unary/binary signature
argument and the inability of any single original binary to produce
$\exp$ in its closure. The §4 obstruction for *unary-only* bases is a
trivial signature obstruction; the obstruction for *binary-only* bases
is that no single original binary admits $\exp$ in its
finite-composition closure (each preserves either degree-1 polynomial
structure, or rational structure, or log-of-rational structure, none
of which generates an entire transcendental of arbitrary growth).

**Depth blowup.** Cardinality minimization is orthogonal to *depth*
minimization. In $B^*$, $\cos x$ has macro-unfolded depth on the order
of $20$ in basis primitives, vs. depth $1$ in the original set. Depth
optimality has not been pursued.

**Beyond the original primitive list.** If the basis is allowed to
contain any "natural" elementary primitive (not restricted to the
original list), more compact bases may exist — e.g., a single binary
$F(x,y) = \ln y / \ln x$ combined with a unary that internalizes both
$\exp$ and a constant (e.g., $g(x) = e^x - 1$ pairs with $+$ to give
$\exp$ via $g(x) + 1$, but recovering $\ln$ requires an inverse which
is not a finite composition of $g$). We have not fully explored this
larger search space; the result $|B^*| = 2$ is over the *given*
primitive list.
