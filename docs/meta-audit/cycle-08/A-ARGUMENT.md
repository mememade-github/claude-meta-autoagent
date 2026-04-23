# Confluence, weak normalization, and strong normalization of R

## 0. Setup

Signature Sigma (restated):

```
nullary:   0,  e
unary:     s,  neg,  t
binary:    add,  mul,  q
```

Rules R:

```
alpha1 :  add(0, y)         ->  y
alpha2 :  add(s(x), y)      ->  s(add(x, y))
alpha3 :  mul(0, y)         ->  0
alpha4 :  mul(s(x), y)      ->  add(y, mul(x, y))
alpha5 :  q(x, y)           ->  x
alpha6 :  q(x, y)           ->  y
alpha7 :  t(x)              ->  t(s(x))
alpha8 :  neg(neg(x))       ->  x
```

Reduction `->` is the closure under arbitrary contexts of "pick a subterm
matching some LHS under a substitution and replace it by the corresponding
RHS instance"; `->>` is its reflexive-transitive closure.  A term is a
*normal form* iff it contains no subterm matching any LHS.

**Verdicts.**

| question                    | verdict                    |
|-----------------------------|----------------------------|
| Q1. Confluence              | **NOT confluent**          |
| Q2. Weak normalization      | **NOT weakly normalizing** |
| Q3. Strong normalization    | **NOT strongly normalizing** |

All three are failure verdicts, so each is witnessed by a specific closed
term plus an explicit derivation.

---

## 1. Preliminary: which ground terms are normal forms

We will several times need the following lemma.  A ground (closed) term
*contains a redex* iff some subterm matches an LHS of R.  The LHSs of R
have the following head symbols:

  - `add` at `alpha1, alpha2`
  - `mul` at `alpha3, alpha4`
  - `q`   at `alpha5, alpha6`
  - `t`   at `alpha7`
  - `neg` at `alpha8`

There is **no rule whose LHS has head `0`, `e`, or `s`**.  Therefore:

**(NF-1)** A ground subterm whose tree contains only the symbols `0`, `e`,
and `s` is a normal form.  Proof: every subterm has head in `{0, e, s}`,
so no subterm can match any LHS of R.

In particular, `0` and `e` are normal forms.  `s(0)`, `s(s(e))`,
`s^n(0)` etc. are normal forms.

---

## 2. Q1 — R is not confluent

**Witness term.**  Take the closed term

```
t  =  q(0, e).
```

**Derivation 1.**  One-step reduction applying `alpha5` at the root
(substitution `x -> 0`, `y -> e`):

```
q(0, e)  ->_{alpha5}  0.
```

**Derivation 2.**  One-step reduction applying `alpha6` at the root
(same substitution):

```
q(0, e)  ->_{alpha6}  e.
```

**Both results are normal forms.**  `0` and `e` are constants of Sigma;
they have no proper subterms and themselves match no LHS (no rule LHS
equals `0` or `e`).  Hence neither `0` nor `e` contains any redex — cf.
(NF-1).

**Distinctness.**  `0` and `e` are syntactically distinct constants of
Sigma.  They cannot be joined: since each is already a normal form,
the only candidate for a common reduct `w` would have to satisfy
`0 ->> w` and `e ->> w`, which (as both are normal forms) forces
`w = 0 = e`, a contradiction.

Thus there exists a closed term `t = q(0, e)` with two derivations
leading to distinct normal forms, so R fails confluence.

*Why the rest of R cannot rescue this.*  This is not strictly required
for the witness above, but note that once we are at `0` or at `e`, no
rule can rewrite them, so no "later" rewriting of the two sides can
bring them back together.  The pair `(alpha5, alpha6)` is exactly a
non-deterministic projection operator that commits irrevocably to one
coordinate, and the two coordinates of `q(0, e)` are distinguishable
normal forms.

---

## 3. Q2 — R is not weakly normalizing

**Witness term.**  Take the closed term

```
t_0  =  t(0).
```

**Claim.**  Every reduction sequence starting from `t(0)` is infinite —
there is no normalizing path from `t(0)`.

To prove this, write `s^n(0)` for the term obtained by applying `s` to
`0` exactly `n >= 0` times (so `s^0(0) = 0`, `s^1(0) = s(0)`, etc.).

### 3.1 Structural lemma

**Lemma (Unique Redex).**  For every `n >= 0`, the term `t(s^n(0))` has
*exactly one* redex, namely the whole term, and the one-step reducts of
`t(s^n(0))` are precisely the singleton `{ t(s^{n+1}(0)) }` via
`alpha7`.

*Proof.*  The set of subterms of `t(s^n(0))` is:

```
   {  0,  s(0),  s(s(0)),  ...,  s^n(0),  t(s^n(0))  }.
```

We check each candidate against every LHS of R.

- Subterms `0, s(0), ..., s^n(0)` consist only of symbols `0` and `s`.
  By (NF-1) none of them contains any redex.  In particular none of
  them *is* a redex, because no LHS of R has head `0` or `s`.

- The whole term `t(s^n(0))` has head `t`.  The unique rule with head
  `t` on the LHS is `alpha7 : t(x) -> t(s(x))`.  Pattern-matching
  `t(x)` against `t(s^n(0))` succeeds with substitution `x -> s^n(0)`,
  producing reduct `t(s(s^n(0))) = t(s^{n+1}(0))`.  No other rule
  applies at the root.

So the whole term is the unique redex, and rewriting it via `alpha7`
yields exactly `t(s^{n+1}(0))`.  There is no other redex position, so
no other one-step reduct exists.  End of proof of the lemma.

### 3.2 No normalizing path

We now show that no reduction sequence starting at `t(0)` ever reaches a
normal form.

Induction on the length `k` of a reduction sequence
`t(0) = u_0 -> u_1 -> ... -> u_k`:

- Base case `k = 0`:  `u_0 = t(0) = t(s^0(0))`.  By the Unique Redex
  Lemma, `u_0` contains a redex, so `u_0` is not a normal form, and
  the sequence can (in fact, must) be extended.
- Induction step: assume `u_k = t(s^n(0))` for some `n >= 0` (this
  holds for `k = 0` with `n = 0`).  The Unique Redex Lemma forces the
  only continuation to be `u_{k+1} = t(s^{n+1}(0))`, which is again of
  the form `t(s^{m}(0))` with `m = n + 1`.

By induction, every one-step reduct of `t(0)`, and every multi-step
reduct, has the form `t(s^m(0))` for some `m >= 0`.  Every such term
contains a redex (its root), so it is not a normal form.

Therefore no reduction sequence from `t(0)` can ever stop at a normal
form.  In particular, *every* reduction sequence from `t(0)` is
infinite.  This is the strongest possible failure of weak
normalization for this starting term: not only does some reduction
sequence fail to terminate, but *every* one does.

Consequently R is not weakly normalizing.

---

## 4. Q3 — R is not strongly normalizing

**Witness term.**  Same as Q2: `t_0 = t(0)`.

**Explicit infinite reduction sequence.**  Applying `alpha7` at the root
repeatedly:

```
t(0)                    ->_{alpha7}  t(s(0))
t(s(0))                 ->_{alpha7}  t(s(s(0)))
t(s(s(0)))              ->_{alpha7}  t(s(s(s(0))))
t(s(s(s(0))))           ->_{alpha7}  t(s(s(s(s(0)))))
                        ...
t(s^n(0))               ->_{alpha7}  t(s^{n+1}(0))
                        ...
```

At step `n` (starting from `n = 0`) the redex is the whole term
`t(s^n(0))`; we match LHS `t(x)` of `alpha7` with substitution
`x -> s^n(0)`, and rewrite to RHS instance `t(s(x)) = t(s(s^n(0)))
= t(s^{n+1}(0))`.  The pattern is visibly unbounded: at each step the
`s`-height strictly increases by one, so no term ever repeats and the
sequence has no terminal element.

This is a specific, named-at-every-step infinite reduction
`t_0 -> t_1 -> t_2 -> ...` with `t_n = t(s^n(0))`, witnessing that R is
not strongly normalizing.

(Trivially, non-weak-normalization implies non-strong-normalization —
any closed term from which no terminating reduction exists must itself
admit an infinite reduction, since at each stage some one-step reduct
exists and no finite path can terminate.  But the task asks for a
specific infinite sequence, which we have given.)

---

## 5. Consistency check of the three verdicts

The three verdicts are mutually consistent:

- Strong normalization implies weak normalization, so "not WN" implies
  "not SN"; our Q2 and Q3 agree.
- Confluence and normalization are logically independent properties;
  both can fail and they do here, via independent witnesses: Q1 uses
  the `q`-projection pair `(alpha5, alpha6)`, Q2/Q3 use the expansive
  rule `alpha7`.  Removing `alpha7` from R would not restore
  confluence (Q1's witness survives); removing `alpha5` and `alpha6`
  would not restore normalization (Q2/Q3's witness survives).  The
  two defects are orthogonal.

## 6. Summary table of witnesses

| obligation     | closed witness term | rule(s) that fire                 | outcome                                           |
|----------------|---------------------|-----------------------------------|---------------------------------------------------|
| Q1 not CR      | `q(0, e)`           | `alpha5` on one side, `alpha6` on the other | two distinct normal forms `0` and `e`   |
| Q2 not WN      | `t(0)`              | `alpha7` is the only applicable rule at every stage | every reduction sequence is infinite |
| Q3 not SN      | `t(0)`              | `alpha7` repeatedly                | explicit infinite sequence `t(s^n(0)) -> t(s^{n+1}(0))` for all `n >= 0` |
