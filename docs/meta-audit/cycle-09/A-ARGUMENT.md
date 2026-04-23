# Confluence, weak normalization, and strong normalization of R

## 0. Setup

Signature Sigma (restated):

```
nullary:   0,  c,  d
unary:     s,  f,  u
binary:    g,  m
```

Rules R:

```
rho1 :  g(0, y)       ->  y
rho2 :  g(s(x), y)    ->  s(g(x, y))
rho3 :  m(x, y)       ->  x
rho4 :  m(x, y)       ->  y
rho5 :  f(x)          ->  x
rho6 :  f(x)          ->  f(f(x))
rho7 :  u(u(x))       ->  x
```

`->` is the closure under arbitrary contexts of "pick a subterm that
matches some LHS under a substitution, replace it by the corresponding
RHS instance"; `->>` is its reflexive-transitive closure.  A *normal
form* is a term no subterm of which matches any LHS.

**Verdicts.**

| question                         | verdict                    |
|----------------------------------|----------------------------|
| Q1.  Confluence                  | **NOT confluent**          |
| Q2.  Weak normalization          | **IS weakly normalizing**  |
| Q3.  Strong normalization        | **NOT strongly normalizing** |

Each negative verdict is witnessed by a specific closed term plus an
explicit derivation.  The positive verdict Q2 is proved by exhibiting
a reduction strategy together with a well-founded monotonic measure
that is strictly decreased by every step the strategy can take.

Sections 2, 3, 4 dispose of Q1, Q2, Q3 respectively.  Section 1 sets
out one preliminary lemma used in the normal-form checks.  Section 5
is a brief consistency check.

---

## 1. Preliminary: which ground terms are normal forms

The LHSs of R have the following head symbols:

 - `g` at rho1, rho2;
 - `m` at rho3, rho4;
 - `f` at rho5, rho6;
 - `u` at rho7.

No rule has head `0`, `c`, `d`, or `s` on its LHS.  So a redex inside a
ground term has head in `{g, m, f, u}`, and moreover:

 - `g(a, b)` is a redex iff `a = 0` (via rho1) or `a = s(a')` for some
   `a'` (via rho2).  Otherwise it is *not* a redex at that root.
 - `m(a, b)` is *always* a redex (rho3 and rho4 impose no shape on
   `a`, `b`).
 - `f(a)` is *always* a redex (rho5 and rho6 impose no shape on `a`).
 - `u(a)` is a redex iff `a = u(a')` for some `a'` (via rho7).
 - `0`, `c`, `d`, `s(a)` never match any LHS at the root.

**(NF-1).**  A ground term built only from `0`, `c`, `d`, `s` is a
normal form: each of its subterms has head in `{0, c, d, s}`, and no
rule LHS has such a head, so no subterm matches any LHS.  In
particular each nullary constant is a normal form.

---

## 2. Q1 — R is not confluent

**Witness term.**  The closed term

```
t  =  m(c, d).
```

**Derivation A** applies rho3 at the root (substitution `x -> c`,
`y -> d`):

```
m(c, d)   ->_{rho3}   c.
```

**Derivation B** applies rho4 at the same root (same substitution):

```
m(c, d)   ->_{rho4}   d.
```

**Both results are normal forms.**  `c` is a nullary constant of
Sigma; it has no proper subterms, and no LHS of R equals `c` or has
head in `{c}`.  Hence `c` contains no redex — cf. (NF-1).  The same
argument applies to `d`.

**The two normal forms differ.**  `c` and `d` are distinct nullary
constants of Sigma, so `c != d` as terms.  Since both are already
normal forms, no further rewriting of either can occur.  In
particular there is no common reduct `w` with `c ->> w` and `d ->> w`:
a normal form reduces only to itself, so any such `w` would force
`c = w = d`, contradicting `c != d`.

Thus `t = m(c, d)` admits two derivations leading to distinct normal
forms `c` and `d`.  R is not confluent.

*Structural remark.*  The pair `(rho3, rho4)` is the source of
non-confluence: both rules share the LHS `m(x, y)`, but their RHSs
`x` and `y` cannot in general be joined — once we have committed
to one coordinate, the other coordinate's contents are lost.  Any
two syntactically distinct closed normal forms `n1, n2` plugged in
as `m(n1, n2)` would serve as a witness; `m(c, d)` is the minimal
one.

---

## 3. Q2 — R is weakly normalizing

We must show: every closed term over Sigma has at least one reduction
sequence that terminates at a normal form.

The plan:

 - Define a weight function `w` from ground terms to positive integers.
 - Show `w` is *monotonic*: replacing a subterm by one of smaller
   weight strictly decreases `w` of the whole term.
 - Show that for every rule rho_i except rho6, every closed instance
   of the LHS has strictly greater `w` than the corresponding instance
   of the RHS.
 - Give a reduction strategy S that never uses rho6.  Argue that
   whenever the current term contains any redex, S can still find a
   non-rho6 redex to apply — so S makes progress until the term is a
   normal form.
 - Since every S-step strictly decreases `w`, and `w` takes values in
   the well-founded set of positive integers, S terminates from every
   starting term.

### 3.1 The weight function

Let `N+ = {1, 2, 3, ...}` be the positive integers.  Define
`w : GroundTerms(Sigma) -> N+` recursively:

```
  w(0)            =  1
  w(c)            =  1
  w(d)            =  1
  w(s(t))         =  w(t) + 1
  w(u(t))         =  w(t) + 1
  w(f(t))         =  2 * w(t)
  w(g(a, b))      =  w(a) * (w(b) + 1) + 1
  w(m(a, b))      =  w(a) + w(b) + 1
```

A straightforward induction on `t` shows `w(t) >= 1` for every ground
`t`: the nullary cases give 1; every recursive case is `>=` the
weights of its children (plus something non-negative), hence `>= 1`.

We extend `w` to terms-with-variables by letting each variable `x`
stand for an arbitrary positive-integer value `X`; the formulas above
then compute a polynomial in those variable weights.  A rule rho_i is
said to *strictly decrease `w`* if, for every assignment of positive
integers to the variables of rho_i, the LHS polynomial strictly
exceeds the RHS polynomial.

### 3.2 Monotonicity

Each recursive clause of `w` is strictly increasing in each argument:

 - `s`, `u`: `w(s(t)) = w(t) + 1` and `w(u(t)) = w(t) + 1` are strictly
   monotone in `w(t)`.
 - `f`: `w(f(t)) = 2 * w(t)` is strictly monotone in `w(t)` (since
   `2 > 0`).
 - `g`: `w(g(a, b)) = w(a)*(w(b)+1) + 1`.  Holding `w(b)` fixed, the
   derivative in `w(a)` is `w(b)+1 >= 2 > 0`.  Holding `w(a)` fixed,
   the derivative in `w(b)` is `w(a) >= 1 > 0`.  Strictly monotone in
   both arguments.
 - `m`: `w(m(a, b)) = w(a) + w(b) + 1` is strictly monotone in both
   arguments.

**Monotonicity Lemma.**  If `s -> s'` is any one-step rewrite at the
root of `s`, and `C[]` is any one-hole context, and
`w(s) > w(s')`, then `w(C[s]) > w(C[s'])`.

*Proof.*  Induction on the depth of the hole in `C`.  At depth 0 the
context is trivial and the inequality is given.  At depth `k+1` the
hole sits under exactly one function symbol `F` which is one of
`s, u, f, g, m`; the inductive hypothesis gives strict decrease at
depth `k`, and the corresponding argument-wise strict monotonicity of
`F` (bullet list above) lifts it through `F`.

### 3.3 Per-rule strict decrease, for every rule except rho6

For brevity write `X = w(x)`, `Y = w(y)` for positive-integer variable
weights.  We compute LHS minus RHS for each rule.

 - **rho1** `g(0, y) -> y`.
   LHS `w(g(0, y)) = 1 * (Y + 1) + 1 = Y + 2`.
   RHS `w(y)       = Y`.
   Difference `Y + 2 - Y = 2 > 0`.  Strict decrease.

 - **rho2** `g(s(x), y) -> s(g(x, y))`.
   LHS `w(g(s(x), y)) = w(s(x))*(Y + 1) + 1 = (X + 1)(Y + 1) + 1
                      = X*Y + X + Y + 2`.
   RHS `w(s(g(x, y))) = w(g(x, y)) + 1
                      = X*(Y + 1) + 1 + 1
                      = X*Y + X + 2`.
   Difference `LHS - RHS = Y >= 1 > 0`.  Strict decrease.

 - **rho3** `m(x, y) -> x`.
   LHS `w(m(x, y)) = X + Y + 1`.  RHS `w(x) = X`.
   Difference `Y + 1 >= 2 > 0`.  Strict decrease.

 - **rho4** `m(x, y) -> y`.
   LHS `w(m(x, y)) = X + Y + 1`.  RHS `w(y) = Y`.
   Difference `X + 1 >= 2 > 0`.  Strict decrease.

 - **rho5** `f(x) -> x`.
   LHS `w(f(x)) = 2*X`.  RHS `w(x) = X`.
   Difference `X >= 1 > 0`.  Strict decrease.

 - **rho6** `f(x) -> f(f(x))`.
   LHS `w(f(x))      = 2*X`.
   RHS `w(f(f(x)))   = 2 * w(f(x)) = 4*X`.
   Difference `LHS - RHS = -2*X < 0`.  rho6 *increases* weight.  This
   is exactly the rule our strategy will refuse to apply.

 - **rho7** `u(u(x)) -> x`.
   LHS `w(u(u(x))) = w(u(x)) + 1 = X + 2`.  RHS `w(x) = X`.
   Difference `2 > 0`.  Strict decrease.

Combined with the Monotonicity Lemma, this gives:

**Strict-Decrease Lemma (non-rho6).**  If `s -> s'` by one application
of some rule `rho_i != rho6` at any position of `s`, then
`w(s) > w(s')`.

### 3.4 The reduction strategy S

Strategy `S`: while the current term `t` is not a normal form, pick
*any* non-rho6 redex in `t` and apply the corresponding non-rho6 rule;
stop when `t` is a normal form.

**Feasibility Lemma.**  Every non-normal-form ground term has a
non-rho6 redex.

*Proof.*  Let `t` be a ground term that is not a normal form.  By
definition some subterm `r` of `t` matches the LHS of some rule
rho_i, so `(r, rho_i)` is a redex of `t`.  If `rho_i != rho6` we are
done: that redex is itself a non-rho6 redex.  Otherwise `rho_i =
rho6`, so `r` matches the LHS `f(x)` of rho6.  But rho5 has the same
LHS `f(x)`, so `r` also matches the LHS of rho5.  Hence `(r, rho5)`
is a non-rho6 redex at the same position.  Either way, a non-rho6
redex exists.

**Termination of S.**  By Feasibility, S can always take a step until
it halts at a normal form.  By the Strict-Decrease Lemma, each step
strictly decreases `w(t)`.  But `w(t) >= 1` always, and `w` takes
values in the well-founded set `N+`, so no infinite strictly
decreasing chain exists.  Therefore S halts after finitely many
steps, necessarily at a normal form.

Thus every closed term has at least one terminating reduction
sequence — the one produced by S.  R is weakly normalizing.

*Remark on the structure of the argument.*  The rule rho6 is the only
expansive rule in R.  Because rho5 and rho6 share the identical LHS
`f(x)`, every occurrence of an rho6-redex is simultaneously an
rho5-redex; the strategy "decline rho6 and use rho5 on the same
position" trades divergent expansion for convergent contraction
without ever having to reach around an unwanted redex.  This is why
the rule `f(x) -> f(f(x))` does *not* threaten weak normalization even
though it threatens (and, per Q3, defeats) strong normalization.

---

## 4. Q3 — R is not strongly normalizing

**Witness term.**

```
t_0  =  f(c).
```

For each `n >= 0` write `f^n(c)` for the term obtained by applying
`f` to `c` exactly `n` times: `f^0(c) = c`, `f^1(c) = f(c)`,
`f^{n+1}(c) = f(f^n(c))`.  So `t_0 = f^1(c)`.

**Explicit infinite reduction sequence.**  Set `t_n = f^{n+1}(c)` for
all `n >= 0`.  We verify that `t_n ->_{rho6} t_{n+1}` at every step.

For the step `t_n -> t_{n+1}`: the whole term `t_n = f(f^n(c))` has
head `f`; rho6's LHS `f(x)` matches `t_n` at the root with
substitution `x -> f^n(c)`.  The corresponding RHS instance is
`f(f(x)) = f(f(f^n(c))) = f^{n+2}(c) = t_{n+1}`.  Rule rho6 fires,
and we have indeed `t_n ->_{rho6} t_{n+1}`.

Spelling out the first few steps explicitly:

```
t_0  =  f(c)
     ->_{rho6}  f(f(c))                                         =  t_1
     ->_{rho6}  f(f(f(c)))                                      =  t_2
     ->_{rho6}  f(f(f(f(c))))                                   =  t_3
     ->_{rho6}  f(f(f(f(f(c)))))                                =  t_4
                    ...
     ->_{rho6}  f^{n+1}(c)                                      =  t_n
     ->_{rho6}  f^{n+2}(c)                                      =  t_{n+1}
                    ...
```

At each step the applied rule is rho6, the redex is the whole term,
and the rewrite increases the count of `f`'s by exactly one.

**The sequence is infinite and unbounded.**  For every `n >= 0` the
term `t_n = f^{n+1}(c)` contains exactly `n + 1` occurrences of the
symbol `f`; the `f`-count is a function of the term and it is
different for different `n`.  So the terms `t_0, t_1, t_2, ...` are
pairwise distinct, and in particular no `t_n` is the final term of
the sequence.  The infinite chain

```
t_0  ->_{rho6}  t_1  ->_{rho6}  t_2  ->_{rho6}  t_3  ->_{rho6}  ...
```

has no termination.  This is an infinite reduction sequence in R
starting from the specific closed term `f(c)`.

Therefore R is not strongly normalizing.

---

## 5. Consistency check of the three verdicts

The three verdicts `(not confluent, WN, not SN)` are mutually
consistent:

 - WN is strictly weaker than SN; `WN and not SN` is a standard
   combination (some reduction paths terminate, some do not).  Our
   proofs match: Q2's strategy S never applies rho6, producing a
   terminating path; Q3's chain applies rho6 exclusively, producing
   an infinite path; both paths coexist starting from `f(c)`.
 - Confluence is logically independent of normalization.  Q1's
   non-confluence witness `m(c, d)` does not involve `f`, `rho5`,
   `rho6` at all, so it is unaffected by Q2's or Q3's considerations.
 - The two defects are orthogonal and each is localised to a distinct
   pair of rules: non-confluence comes from `(rho3, rho4)` sharing the
   LHS `m(x, y)` with incompatible RHSs, while non-strong-
   normalization comes from `rho6` being expansive in `f`.  Removing
   `rho6` would restore SN (our weight `w` certifies termination of
   the remaining six rules) but would not restore confluence
   (`m(c, d)` still splits).  Removing one of `rho3`, `rho4` would
   restore confluence at that source (the `m` LHSs would no longer
   overlap with incompatible RHSs) but would not restore SN
   (`f(c) ->_{rho6} ...` still diverges).

---

## 6. Summary table of witnesses

| obligation | verdict | witness term | rule(s) applied | outcome |
|------------|---------|--------------|-----------------|---------|
| Q1 confluence | NOT | `m(c, d)` | `rho3` on one branch, `rho4` on the other | two distinct normal forms `c != d` |
| Q2 weak normalization | IS | every closed term | any non-`rho6` rule under strategy S; weight `w` strictly decreases | some terminating path exists from every starting term |
| Q3 strong normalization | NOT | `f(c)` | `rho6` at the root, repeatedly | infinite chain `f^{n+1}(c) ->_{rho6} f^{n+2}(c)` |
