# ARGUMENT — Confluence, weak normalization, and strong normalization of R

> Draft trace at `iterations/attempt-01.md`.  Executable oracle at
> `sim/simulator.py`, captured output at `sim/output-final.txt`.  Every
> claim in §3 and §4 is cross-checked by a test in the oracle.

## The system under study

Signature Sigma (as given):

    nullary: 0, e
    unary:   s, neg, t
    binary:  add, mul, q

Rules R:

    alpha1:  add(0, y)        -> y
    alpha2:  add(s(x), y)     -> s(add(x, y))
    alpha3:  mul(0, y)        -> 0
    alpha4:  mul(s(x), y)     -> add(y, mul(x, y))
    alpha5:  q(x, y)          -> x
    alpha6:  q(x, y)          -> y
    alpha7:  t(x)             -> t(s(x))
    alpha8:  neg(neg(x))      -> x

**Positions.**  Positions are tuples of 1-indexed child positions; `()`
is the root.  In displayed overlaps I write `eps` for `()` and `i.j`
for `(i, j)`.

## Verdicts committed to

| Question | Verdict |
|----------|---------|
| Q1 confluence | **NOT confluent** |
| Q2 weak normalization | **NOT weakly normalizing** |
| Q3 strong normalization | **NOT strongly normalizing** |

All three are negative.  Each is witnessed by a concrete closed term
with an explicit per-step rule citation.  The rigor-asymmetry
disclosure (constraint 2) is at the end of §3.

---

## 1. Preliminaries used throughout

### 1.1 Rule LHS heads

The eight LHSs of R have the following heads (a claim checked
mechanically by `test_no_lhs_headed_by` in the oracle):

| Rule | LHS | Head |
|------|-----|------|
| alpha1 | `add(0, y)` | `add` |
| alpha2 | `add(s(x), y)` | `add` |
| alpha3 | `mul(0, y)` | `mul` |
| alpha4 | `mul(s(x), y)` | `mul` |
| alpha5 | `q(x, y)` | `q` |
| alpha6 | `q(x, y)` | `q` |
| alpha7 | `t(x)` | `t` |
| alpha8 | `neg(neg(x))` | `neg` |

The set of LHS heads is `{add, mul, q, t, neg}`.  In particular **no
rule has LHS headed by `0`, `e`, or `s`.**

### 1.2 Immediate NF catalogue

A closed term whose **root head is in `{0, e, s}`** has no redex at
the root: no rule's LHS matches (by §1.1).  If additionally none of
its strict subterms contains a redex, the whole term is a normal
form.  In particular:

- `0` and `e` are nullary; they have no subterms at all.  They are
  NFs.
- `s(t)` is a NF iff `t` is a NF.
- `neg(t)` — the only rule that can fire at its root is `alpha8`,
  requiring the argument `t` to itself be headed by `neg`.  So if
  `t` is not headed by `neg`, no root redex; and `neg(t)` is an NF
  iff `t` is an NF with root head different from `neg`.

These facts are used in §2 and §3.1.

### 1.3 Subterm/closure conventions

Writing `C[u]` for a term with a distinguished occurrence (the
"hole") filled by `u`, the reduction relation satisfies
`u -> u' ==> C[u] -> C[u']` (closure under contexts, as stated in
the task prompt).  I use this without further comment.

---

## 2. Q1 — R is NOT confluent

### 2.1 Witness

    t = q(0, e)

Two derivations:

- **Derivation A.**  `q(0, e) --alpha5@eps--> 0`.
  Rule alpha5: `q(x, y) -> x`; matcher `sigma = {x := 0, y := e}`;
  RHS under sigma is `0`.

- **Derivation B.**  `q(0, e) --alpha6@eps--> e`.
  Rule alpha6: `q(x, y) -> y`; matcher `sigma = {x := 0, y := e}`;
  RHS under sigma is `e`.

Each derivation has length 1, so the `->>` requirement (any number
of steps, including one) is met.

### 2.2 Both reducts are normal forms

`0` is a nullary constant; its head is `0`, which is not the head of
any rule's LHS (§1.1).  It has no subterms.  So no rule applies
anywhere in `0`: it is a NF.

`e` is a nullary constant; by the same argument, it is a NF.

### 2.3 The reducts are distinct

`0` and `e` are syntactically distinct constants of Sigma.  (Sigma
lists them as separate symbols.)  No rule of R rewrites `0` to `e`
or `e` to `0`; in fact — and this is stronger than needed — the
forward-reachable sets are `{0}` and `{e}` respectively (each has
no redex to take any step).

### 2.4 Conclusion for Q1

`q(0, e) ->> 0` and `q(0, e) ->> e` are two reductions ending at
distinct normal forms.  By definition of confluence, if R were
confluent there would be a common reduct `w` with `0 ->> w` and
`e ->> w`; the only reducts of `0` and `e` are themselves, so
`w = 0 = e`, which is impossible since `0 != e`.

Hence **R is not confluent.**

### 2.5 Structural reason (non-essential, for completeness)

The executable oracle enumerates all 104 `(outer rule, inner rule,
non-variable-position)` overlap triples (§`test_q1_cp_enumeration`);
93 are non-unifiable by head mismatch, 11 are unifiable.  Of the 11
unifiable overlaps, the only nontrivial ones are

    (alpha5, alpha6, eps) with reducts <x, y>
    (alpha6, alpha5, eps) with reducts <y, x>   (same overlap, swapped)

and both are **non-joinable** — the reducts are two independent
variables, and no rule of R can transform one variable-projection
into another.  Instantiating `x := 0, y := e` gives the §2.1
witness.  Every other unifiable overlap is either same-rule-at-root
(reducts identical by construction) or has identical RHS-residuals.
This is not required to close Q1 — the §2.1–2.4 argument is
self-contained — but it shows the witness is the *unique*
non-joinable critical pair of R.

---

## 3. Q2 — R is NOT weakly normalizing

A closed term `u` is weakly normalizing iff **some** reduction
sequence from `u` terminates at a normal form.  To show R is not
weakly normalizing, I exhibit a closed term from which **every**
reduction sequence is infinite.

### 3.1 Witness

    t_0 := t(0)

I will show that every term reachable from `t_0` under `->>` has the
form `t(s^n(0))` for some `n >= 0`, has **exactly one** redex
(namely `alpha7` at the root), and so has a unique successor under
`->`.  Hence the reduction graph rooted at `t_0` is a single
infinite chain `t_0 -> t_1 -> t_2 -> ...` with `t_n = t(s^n(0))`,
and no normal form appears in it.

### 3.2 The crux: uniqueness of redex at `t(s^n(0))`

**Lemma 3.2.**  For every `n >= 0`, the term `t(s^n(0))` has
exactly one redex, occurring at position `eps` via rule `alpha7`,
with matcher `sigma_n = {x := s^n(0)}` and reduct `t(s^{n+1}(0))`.

*Proof.*  Let `T_n := t(s^n(0))`.  Every subterm of `T_n` occurs at
exactly one of the positions

    eps,   (1),   (1, 1),   ...,   (1, 1, ..., 1)  (n+1 ones)

with subterm

    eps         -> t(s^n(0))   head: t
    (1)         -> s^n(0)      head: s if n >= 1 else 0
    (1, 1)      -> s^{n-1}(0)  head: s if n >= 2 else 0
    ...
    (1^k)       -> s^{n-k+1}(0) if k <= n, else 0 (and this is k=n+1)
    (1^{n+1})   -> 0            head: 0

So the heads at these positions are, top to bottom: `t`, then
`s` repeated `n` times, then `0` at the deepest position.

Matching rule LHSs (recall §1.1 that the LHS heads are
`{add, mul, q, t, neg}`):

- Head `t` occurs only at `eps`.  The only rule with LHS head `t`
  is `alpha7`, with LHS `t(x)`.  Matching `t(x)` against `T_n`
  succeeds with `x := s^n(0)`.  So `eps` is a redex; it uses rule
  `alpha7`; and the substitution is unique because `alpha7`'s LHS
  is linear (the variable `x` occurs once).
- Head `s` — no rule has LHS headed `s`.  So positions `(1)`
  through `(1^n)` contribute no redex.
- Head `0` — no rule has LHS headed `0`.  So position `(1^{n+1})`
  contributes no redex.

Therefore `T_n` has **exactly one** redex: `alpha7` at position
`eps`.  The matcher is `sigma_n = {x := s^n(0)}`, and the reduct is

    alpha7-rhs under sigma_n  =  t(s(x)) [x := s^n(0)]
                              =  t(s(s^n(0)))
                              =  t(s^{n+1}(0))
                              =  T_{n+1}.          ∎

(The oracle's `test_t_subterm_has_only_alpha7_redex` checks the
claim "`t(s^n(0))` has only one redex, `alpha7@eps`" for `n = 0, 1,
..., 11` mechanically, and `test_q2_not_wn_witness` prints the
redex list at each of the first 10 stages.)

### 3.3 The unique-reduction theorem

**Theorem 3.3.**  Starting from `t_0 = t(0)`, the one-step reduction
relation `->` restricted to the forward-reachable set from `t_0` is
a total function mapping `t_n = t(s^n(0))` to `t_{n+1} =
t(s^{n+1}(0))`.  Hence the only reduction sequence from `t_0` is
the infinite chain

    t(0) -> t(s(0)) -> t(s(s(0))) -> t(s(s(s(0)))) -> ...

with every arrow being `alpha7@eps`.

*Proof.*  By induction on the step index.

*Base.*  `t_0 = t(0) = t(s^0(0))`.  By Lemma 3.2 with `n = 0`, it
has the unique redex `alpha7@eps` with reduct `t_1 = t(s^1(0))`.

*Step.*  Suppose after `n` steps the current term is `t_n =
t(s^n(0))`.  By Lemma 3.2, the unique redex is `alpha7@eps` with
reduct `t_{n+1} = t(s^{n+1}(0))`.  So any reduction sequence from
`t_0` must continue with this step; the `(n+1)`-th term in any
sequence is `t_{n+1}`.

By induction, every reduction sequence from `t_0` has `t_n` at
position `n`, for every `n >= 0`.  Since `t_n` has a redex (Lemma
3.2), no `t_n` is a normal form, and the sequence never terminates.
∎

### 3.4 Explicit first few steps and the general pattern

    t_0 = t(0)
    t_0 --alpha7@eps-->  t(s(0))                  [= t_1]
    t_1 --alpha7@eps-->  t(s(s(0)))               [= t_2]
    t_2 --alpha7@eps-->  t(s(s(s(0))))            [= t_3]
    t_3 --alpha7@eps-->  t(s(s(s(s(0)))))         [= t_4]
    ...
    t_n --alpha7@eps-->  t(s^{n+1}(0))            [= t_{n+1}]

Sizes grow as `|t_n| = n + 2` (one `t`, `n` copies of `s`, one
`0`), so no two terms in the sequence are equal; in particular no
term ever returns to a previously seen one.

### 3.5 Conclusion for Q2

From `t(0)` **every** reduction sequence is the infinite chain of
Theorem 3.3; no NF is reachable.  By the definition of weak
normalization ("some reduction sequence terminates at a NF"), no
such sequence exists for `t(0)`.

Hence **R is not weakly normalizing.**

---

## 4. Q3 — R is NOT strongly normalizing

A TRS is strongly normalizing iff **every** reduction sequence from
every closed term terminates.  Non-SN is witnessed by exhibiting one
closed term with one infinite reduction sequence.

### 4.1 Witness

The same `t_0 = t(0)` and the same infinite sequence from §3.3:

    t(0) --alpha7@eps--> t(s(0))
         --alpha7@eps--> t(s(s(0)))
         --alpha7@eps--> t(s(s(s(0))))
         --alpha7@eps--> t(s(s(s(s(0)))))
         --alpha7@eps--> ...

### 4.2 Verification that each step is a legal rewrite

At stage `n`, the current term is `t_n = t(s^n(0))` (checked in §3
by induction).  Rule `alpha7` has LHS `t(x)` and RHS `t(s(x))`.
Matching `t(x)` against `t_n` gives the matcher `sigma_n = {x :=
s^n(0)}`.  Applying `sigma_n` to the RHS gives
`t(s(s^n(0))) = t(s^{n+1}(0)) = t_{n+1}`.  So `t_n -> t_{n+1}` is
valid, at position `eps`, by rule `alpha7`.  This is legal for
every `n >= 0`.

### 4.3 Pattern made explicit

The shape invariant is

    for all n >= 0:   t_n = t(s^n(0))

The "repeating pattern" requested by constraint 1 of the task: each
successive term appends one more `s`-layer inside the `t(...)`
wrapper; each successive step is `alpha7` at the root.  Size grows
as `n + 2`, so the sequence is visibly unbounded.

(The oracle's `test_q3_infinite_sequence` traces 20 steps and
confirms at every stage that the term equals `t(s^n(0))` and that
`alpha7@eps` applies.)

### 4.4 The general termination impossibility

Any candidate SN proof would require a well-founded measure `Phi`
with `Phi(t) > Phi(t')` whenever `t -> t'`.  Applied to the above
sequence, that would give an infinite descending chain
`Phi(t_0) > Phi(t_1) > Phi(t_2) > ...` in `Phi`'s well-founded
codomain, which is impossible.  So no `Phi` witnesses SN — a
corollary of the concrete counterexample, not a separate argument.

### 4.5 Conclusion for Q3

`t(0)` admits the infinite reduction sequence above.  By the
definition of strong normalization ("every reduction sequence
terminates"), that single infinite sequence suffices to refute SN.

Hence **R is not strongly normalizing.**

---

## 5. Rigor-asymmetry disclosure (per constraint 2)

Q1 and Q3 are immediate from the witnesses: Q1 requires checking
that `0` and `e` are NFs (four-line argument from LHS-head analysis,
§2.2) and are distinct (syntactic, §2.3); Q3 requires exhibiting
one infinite sequence and verifying each step by a substitution
check (§4.2).

Q2 is harder.  Non-WN is a universal claim — *every* reduction
sequence from the witness must be infinite — not merely that
one is.  The load falls on Lemma 3.2, which establishes that each
term `t(s^n(0))` has **exactly one** redex.  The Lemma is proved by
enumerating the positions of `t(s^n(0))`, reading off the head at
each, and checking each head against the list of rule LHS heads
(§1.1).  The enumeration is finite for each `n` (exactly `n + 2`
positions), and the head-set at those positions is `{t, s, ..., s,
0}` independent of `n` (up to `s`-multiplicity), so the lemma
generalizes cleanly by induction.  The remaining rigor budget has
been spent on that step.

The three verdicts are tightly related:

- Q3's witness is literally a subsequence of Q2's unique-reduction
  chain.  Non-SN follows trivially from non-WN; I give Q3 its own
  write-up only to make the Q3 answer self-contained.  If Q2 failed
  to establish non-WN — i.e., if some *other* reduction sequence
  from `t(0)` terminated — the infinite sequence of §4 would still
  exist, and Q3 would still conclude non-SN.  So Q3 is strictly
  weaker than Q2.
- Q1's witness `q(0, e)` is independent of Q2's/Q3's witness
  `t(0)`.  The non-confluence of R traces to `alpha5/alpha6`; the
  non-WN/non-SN of R traces to `alpha7`.  Removing `q` (rules
  `alpha5`, `alpha6`) would make R confluent but leave non-WN
  intact.  Removing `t` (rule `alpha7`) would kill non-WN/non-SN
  but leave non-confluence via `q` intact.  No single closed term
  can witness all three failures; two are needed (or one somewhat
  larger term combining both, e.g., `q(t(0), e)`, which has no
  NF on one projection and has NF `e` on the other — but this adds
  nothing over the two small witnesses and is not presented).

No external named theorem is invoked.  All reasoning is by direct
case analysis on the eight rules and the subterm structure of the
witnesses, together with the definitions of NF, WN, SN, and
confluence as stated in the task prompt.

---

## 6. Oracle verification summary

`sim/simulator.py` runs eight tests, captured in
`sim/output-final.txt`:

1. `test_no_lhs_headed_by` — confirms §1.1: LHS heads are exactly
   `{add, mul, q, t, neg}`, none of `0`, `e`, `s`.
2. `test_claimed_nfs` — confirms §1.2: `0`, `e`, `s(0)`, `s(s(e))`,
   `neg(0)`, `neg(s(e))` all have zero redexes.
3. `test_per_rule_size_delta` — shows per-rule size changes on
   representative instances; confirms `alpha7` is the only
   size-growing rule whose growth has no size-shrinking compensation
   at its own redex position (alpha4 grows size on the instance
   shown but also leaves a smaller mul-redex behind).  Not used in
   the argument; included for orientation.
4. `test_q1_non_confluence_witness` — confirms §2: `q(0, e)` reduces
   to `0` via alpha5 and to `e` via alpha6; both are NFs; their
   forward-reachable sets are `{0}` and `{e}`; disjoint.
5. `test_q1_cp_enumeration` — confirms §2.5: of 104 overlap
   triples, 93 are non-unifiable; 11 unifiable; the only
   non-joinable overlaps are `(alpha5, alpha6, eps)` and its swap.
6. `test_q2_not_wn_witness` — confirms §3.2 at stages 0..9:
   `redexes(t_n) == [((), 'alpha7')]`.
7. `test_t_subterm_has_only_alpha7_redex` — confirms the same
   property for `t(s^n(0))` with `n = 0..11` directly (not relying
   on the reduction chain).
8. `test_q3_infinite_sequence` — traces 20 `alpha7` steps from
   `t(0)`, confirming at each the shape `t(s^n(0))` and strict
   size growth.

All tests pass on the captured run.

---

## Appendix A — Sanity table of per-rule behaviour

For reference (not load-bearing in the argument):

| Rule | Size-monotone? | Creates new redexes? | Comment |
|------|----------------|---------------------|---------|
| alpha1 | strictly shrinks | no | clears `add(0, _)` |
| alpha2 | preserves (on closed) | yes (inner `add`) | recursive `add` descent |
| alpha3 | strictly shrinks | no | collapses `mul(0, _)` |
| alpha4 | strictly grows | yes (new `add` and `mul`) | unfolds one `mul` step |
| alpha5 | strictly shrinks | no | left projection of `q` |
| alpha6 | strictly shrinks | no | right projection of `q` |
| alpha7 | strictly grows | yes (same `t(...)` shape) | the WN/SN-destroying rule |
| alpha8 | strictly shrinks | no | cancels double `neg` |

alpha7 is the source of non-WN/non-SN: a rule whose RHS recreates
the LHS pattern with a strictly larger argument, and whose
redex-pattern is created by no other rule — so there is no
"alternative" that could avoid alpha7 when the term is `t(...)`.
This contrasts with alpha4 (which also grows size) — alpha4 applied
to `mul(s(x), y)` produces `add(y, mul(x, y))` whose inner `mul`
argument `x` is strictly smaller than the original `s(x)`, so
repeated alpha4 applications terminate (alpha4 is innermost-
well-founded on `x`).

alpha5 and alpha6 jointly are the source of non-confluence: they
share the LHS `q(x, y)` and project to distinct variables; no
rule can reconcile two independent variable projections.
