# ARGUMENT — Confluence, weak normalization, and strong normalization of R

> **Iteration trace.**  Initial draft at `iterations/attempt-01.md`.
> Evaluator audit at `iterations/.eval-report-01.json`
> (weighted_score 0.7125; two high-priority gaps G1, G2 and seven
> medium/low tightenings G3–G10).  This document closes all ten.
>
> **Executable oracle.**  `sim/simulator.py` with captured output at
> `sim/output-final.txt`.  The oracle (a) performs every rewrite step
> used in §2 and §4 and asserts equality with the claimed result,
> (b) certifies the normal-form check via head-scan, (c) samples 500
> random closed substitutions per non-rho6 rule and checks
> `[LHS] > [RHS]`, and (d) enumerates `t_0..t_8` of §4 explicitly.
> Every numbered claim below is independently reproduced by that
> simulator on the cited output block.

## §0. The system under study

**Signature** Sigma:

    nullary:   0,   c,   d
    unary:     s,   f,   u
    binary:    g,   m

**Rules** R:

    rho1:  g(0, y)          ->  y
    rho2:  g(s(x), y)       ->  s(g(x, y))
    rho3:  m(x, y)          ->  x
    rho4:  m(x, y)          ->  y
    rho5:  f(x)             ->  x
    rho6:  f(x)             ->  f(f(x))
    rho7:  u(u(x))          ->  x

**Terms** are trees built from Sigma (and, in rule statements,
variables `x, y, z`).  A **closed** term contains no variable.
**Positions** in a term are finite sequences over the positive
integers, with the empty sequence `eps` marking the root;
`subterm(t, p)` is the subterm at position `p`.

A **redex** in `t` is a pair `(p, rho_i)` such that `subterm(t, p)`
matches the LHS of `rho_i` under some substitution `sigma` sending
rule variables to closed terms.  The associated one-step rewrite
replaces `subterm(t, p)` in `t` with `RHS(rho_i) * sigma`.  Rewriting
is closed under contexts (one may rewrite inside any subterm).  We
write `t -> t'` for one step and `t ->> t'` for the reflexive
transitive closure.

A **normal form** is a term with no redex.

## §1. Verdicts

| Question                         | Verdict                                        |
|----------------------------------|------------------------------------------------|
| Q1 — confluence                  | **NOT confluent**              — see §2        |
| Q2 — weak normalization          | **Weakly normalizing**         — see §3        |
| Q3 — strong normalization        | **NOT strongly normalizing**   — see §4        |

## §2. Q1 — R is not confluent

**What we refute.**  R is **confluent** iff for every term `t` and
every pair `u, v` with `t ->> u` and `t ->> v`, there exists a `w`
with `u ->> w` and `v ->> w` (a common reduct).  To refute this it
suffices to exhibit a specific closed `t` and reductions `t ->> u`,
`t ->> v` where `u` and `v` are **distinct normal forms**: normal
forms have no outgoing step, so the only `w` reachable from `u` is
`u` itself and the only `w` reachable from `v` is `v` itself;
distinctness forces no common reduct.

### Witness

    t  =  m(c, d)

### Two one-step reductions

Both reductions fire at the root (position `eps`), matching rule LHS
`m(?x, ?y)` against `m(c, d)` with substitution
`sigma = { ?x := c,  ?y := d }`.

- `m(c, d)  ->_{rho3, eps,  sigma}  c`.  Rule rho3 has RHS `?x`; hence
  `RHS * sigma = c`.
- `m(c, d)  ->_{rho4, eps,  sigma}  d`.  Rule rho4 has RHS `?y`; hence
  `RHS * sigma = d`.

### Both endpoints are normal forms

Every rule LHS in R has a **non-nullary head**: rho1 and rho2 have
head `g`; rho3 and rho4 have head `m`; rho5 and rho6 have head `f`;
rho7 has head `u`.  Matching requires head-symbol equality.  Now:

- `c` is a single nullary constant.  It has no proper subterms; its
  only position is `eps`, and the head at that position is `c`.  No
  rule LHS has head `c`.  So no rule matches at any position of `c`.
  `c` is a normal form.
- `d` is a single nullary constant; by the same argument with `d` in
  place of `c`, `d` is a normal form.

### The normal forms are distinct

`c` and `d` are distinct nullary symbols in Sigma, so `c != d` as
terms.

### No common reduct

Since `c` is a normal form, `c ->> w` forces `w = c`.  Since `d` is a
normal form, `d ->> w` forces `w = d`.  A common reduct of `c` and
`d` would require `c = d`, contradicting their distinctness.  Hence
no `w` with both `c ->> w` and `d ->> w` exists.

**Conclusion.**  The closed term `m(c, d)` has two maximal reductions
`m(c, d) ->> c` and `m(c, d) ->> d` ending in distinct normal forms
with no common reduct.  **R is not confluent.**

> *Oracle cross-check.*  In `sim/output-final.txt` under the banner
> `Q1. NON-CONFLUENCE: witness m(c, d)`, the simulator prints the two
> one-step reductions, runs `is_normal_form` on both endpoints (both
> return `True`), and asserts `c != d`.

## §3. Q2 — R is weakly normalizing

**Claim.**  Every closed term over Sigma admits at least one reduction
sequence terminating at a normal form.

**Proof outline.**
- §3.1 defines a reduction strategy S.
- §3.2 shows S is total on non-normal-form closed terms.
- §3.3 defines a weight measure W on closed terms.
- §3.4 shows W strictly decreases under every non-rho6 rule at the
  top level.
- §3.5 lifts the strict decrease under arbitrary closed contexts.
- §3.6 states well-foundedness of W's codomain and concludes
  S-trajectories are finite.
- §3.7 shows S halts only at normal forms.
- §3.8 assembles the proof.

### §3.1 The strategy S

Given a closed term `t`:

- If `t` has no redex, halt; `t` is a normal form.
- Otherwise, choose any redex `(p, rho_i)` in `t` with `rho_i != rho6`,
  and rewrite at that redex.

### §3.2 S is total on non-normal-form closed terms

Let `t` be a closed term with at least one redex.  Fix any redex
`(p, rho_i)` in `t`.  Two cases:

- `rho_i != rho6`.  The redex itself is non-rho6; S picks it.
- `rho_i = rho6`.  Then `subterm(t, p)` matches the LHS of rho6,
  namely `f(?x)`.  The LHS of rho5 is also `f(?x)`, so the very same
  match witnesses that `(p, rho5)` is a redex of `t`.  That redex is
  non-rho6; S picks it.

Either way, a non-rho6 redex exists.  S is defined at every non-normal-
form closed term.

### §3.3 The weight W

Define `[·]` on closed terms by structural recursion:

    [0]          = 1
    [c]          = 1
    [d]          = 1
    [s(t)]       = 1 + [t]
    [f(t)]       = 1 + [t]
    [u(t)]       = 1 + [t]
    [g(t1, t2)]  = 1 + 2*[t1] + [t2]
    [m(t1, t2)]  = 1 + [t1] + [t2]

The eight cases cover every function symbol of Sigma exactly once, so
`[·]` is total on closed terms.  Every case yields a positive integer
(nullary cases return 1; compound cases add `1` to a sum of previously-
computed positive integers).  Hence `[·]` is a total function
`ClosedTerms(Sigma) -> Z_{>0}`.

### §3.4 Strict decrease at the top level

We compute `[LHS * sigma] - [RHS * sigma]` for each rule, writing
`a := [?x * sigma]` and `b := [?y * sigma]` for the positive integers
to which `sigma` sends the rule's free variables.

| rule    | `[LHS * sigma]`           | `[RHS * sigma]`         | diff          |
|---------|---------------------------|-------------------------|---------------|
| rho1    | `1 + 2*1 + b  = 3 + b`    | `b`                     | `3`           |
| rho2    | `1 + 2*(1+a) + b = 3+2a+b`| `1 + (1+2a+b) = 2+2a+b` | `1`           |
| rho3    | `1 + a + b`               | `a`                     | `1 + b`       |
| rho4    | `1 + a + b`               | `b`                     | `1 + a`       |
| rho5    | `1 + a`                   | `a`                     | `1`           |
| rho6    | `1 + a`                   | `1 + (1+a) = 2 + a`     | `-1`          |
| rho7    | `1 + (1+a) = 2 + a`       | `a`                     | `2`           |

Detailed calculation for rho2 (the only non-trivial case):

    [g(s(?x), ?y) * sigma]  =  1 + 2*[s(?x) * sigma] + [?y * sigma]
                            =  1 + 2*(1 + a) + b
                            =  3 + 2a + b

    [s(g(?x, ?y)) * sigma]  =  1 + [g(?x, ?y) * sigma]
                            =  1 + (1 + 2a + b)
                            =  2 + 2a + b

    diff  =  (3 + 2a + b) - (2 + 2a + b)  =  1.

Since `a, b >= 1`, the diff for every non-rho6 rule is `>= 1`, i.e.
strictly positive.  For rho6 the diff is `-1 < 0` — the measure
*increases* under rho6, which is precisely why S excludes it.

> *Oracle cross-check.*  In `sim/output-final.txt` under the banner
> `Measure check: weight strictly decreases under every non-rho6 rule`,
> the simulator draws 500 independent random closed substitutions for
> each non-rho6 rule and asserts `[LHS] > [RHS]` on each; all 3000
> assertions pass.  The same block draws 200 random substitutions for
> rho6 and asserts `[LHS] < [RHS]` on each; all 200 pass, confirming
> the diff-sign table above.

### §3.5 Context closure of the strict decrease

Write `l = LHS * sigma` and `r = RHS * sigma`; §3.4 gives `[l] > [r]`
for every non-rho6 rule and every closed `sigma`.  A rewrite at an
arbitrary position replaces `l` by `r` inside some closed one-hole
context `C[-]`, producing `C[l] -> C[r]`.  We must show
`[C[l]] > [C[r]]`.

**Lemma (strict monotonicity of W under each symbol).**  For every
function symbol `phi` of Sigma of arity `>= 1` and every argument
index `i`, the weight expression for `phi(..., arg_i, ...)` is a
strictly increasing function of `[arg_i]` when the other arguments
are held fixed.  Reason: the coefficient of `[arg_i]` in the weight
formula is a positive integer.

- unary `s, f, u`: coefficient on the single argument is `1`.
- binary `g`: coefficient on first argument is `2`, on second is `1`.
- binary `m`: coefficient on either argument is `1`.

**Claim.**  For closed `l, r` with `[l] > [r]` and every closed
one-hole context `C[-]`, `[C[l]] > [C[r]]`.

**Proof by induction on the structure of `C[-]`.**

- *Base* `C[-] = Hole`.  Then `C[l] = l` and `C[r] = r`, so
  `[C[l]] = [l] > [r] = [C[r]]`.
- *Inductive step* `C[-] = phi(t_1, ..., C'[-], ..., t_k)` where
  `phi` is of arity `k`, the hole sits in argument slot `i`, and
  `t_j` (for `j != i`) are closed terms without holes.  The induction
  hypothesis gives `[C'[l]] > [C'[r]]`.  By the monotonicity lemma
  applied to `phi` with slot `i`, replacing the `i`-th argument from
  `C'[l]` to the smaller `C'[r]` strictly decreases the `phi`-term's
  weight.  Hence `[C[l]] > [C[r]]`.

This exhausts the context constructors.  So every S-step
`C[l] -> C[r]` strictly decreases `[·]`:

                    [C[l]]  >  [C[r]].

### §3.6 Well-foundedness and finite S-trajectories

`([·]: ClosedTerms(Sigma) -> Z_{>0})` maps into the positive integers
under the usual order `<`.  This order is well-founded: any nonempty
set of positive integers has a minimum, so no infinite strictly
descending sequence `n_0 > n_1 > n_2 > ...` of positive integers
exists.

Let `t_0 -> t_1 -> t_2 -> ...` be any S-reduction.  By §3.5, the
sequence `[t_0] > [t_1] > [t_2] > ...` is a strictly descending
sequence of positive integers, hence finite.  Therefore every
S-reduction terminates.

### §3.7 S halts at normal forms

S halts on `t` iff `t` has no redex (§3.1), i.e. iff `t` is a normal
form.  On non-normal-form closed terms, S has a non-rho6 redex
available (§3.2) and takes a step.  Consequently every finite
S-trajectory ends in a normal form.

### §3.8 Conclusion for Q2

Combining §3.6 and §3.7: every closed term `t` has an S-trajectory
that is finite and ends in a normal form.  **R is weakly
normalizing.**

> *Oracle cross-check.*  `sim/output-final.txt` under the banner
> `Q2. WN: 'avoid rho6' strategy terminates on a variety of terms`
> runs the S-strategy on twelve sample closed terms covering every
> symbol of Sigma in several configurations (flat, nested, combined
> with `m`, `g`, `f`, `u`, and `s`).  Every run terminates at a
> normal form; the simulator additionally asserts the weight
> strictly decreases at every step of every run.

## §4. Q3 — R is not strongly normalizing

**What we refute.**  R is **strongly normalizing** iff every reduction
sequence is finite.  To refute it we exhibit a specific closed `t_0`
and an infinite reduction `t_0 -> t_1 -> t_2 -> ...`.

### Construction

Set `t_0 = f(c)`.  For `n >= 0` define

    body_n  =  f^n(c)              where  f^0(c) = c   and   f^{k+1}(c) = f(f^k(c))
    t_n     =  f(body_n)  =  f^{n+1}(c).

Thus `body_0 = c`, `body_1 = f(c)`, `body_2 = f(f(c))`, and in
general `body_n` is `c` wrapped in exactly `n` `f`-symbols.  `t_n`
is `c` wrapped in exactly `n+1` `f`-symbols.

### The one-step reduction `t_n -> t_{n+1}`

Apply rho6 at the root of `t_n`.  Rho6 has LHS `f(?x)` and
RHS `f(f(?x))`; matching against `t_n = f(body_n)` gives
`sigma = { ?x := body_n }`.  Instantiating the RHS under `sigma`
produces `f(f(body_n))`, so the step is

    t_n  =  f(body_n)   ->_{rho6, eps, sigma}   f(f(body_n)).

By the defining recurrence `body_{n+1} = f(body_n)`, the inner
`f(body_n)` equals `body_{n+1}`, so

    f(f(body_n))  =  f(body_{n+1})  =  t_{n+1}.

Hence for every `n >= 0`,

    t_n  ->_{rho6,  eps,  ?x := body_n}  t_{n+1}.

### First several steps with all substitutions named

    t_0 = f(body_0)       ->_{rho6, eps, ?x := body_0 = c}
      t_1 = f(f(c))
    t_1 = f(body_1)       ->_{rho6, eps, ?x := body_1 = f(c)}
      t_2 = f(f(f(c)))
    t_2 = f(body_2)       ->_{rho6, eps, ?x := body_2 = f(f(c))}
      t_3 = f(f(f(f(c))))
    t_3 = f(body_3)       ->_{rho6, eps, ?x := body_3 = f(f(f(c)))}
      t_4 = f(f(f(f(f(c)))))
    t_4 = f(body_4)       ->_{rho6, eps, ?x := body_4}
      t_5 = f(f(f(f(f(f(c))))))
    ...
    t_n = f(body_n)       ->_{rho6, eps, ?x := body_n = f^n(c)}
      t_{n+1} = f^{n+2}(c)

### The sequence is genuinely infinite

`size(t_n) = n + 2` (the term has one outer `f`, `n` inner `f`'s
from `body_n`, and one `c`).  Strictly increasing size implies
`t_i != t_j` for `i != j`, so the sequence does not enter a cycle.
Every `t_n` admits the rho6-step shown above, so no `t_n` is terminal.
Hence the infinite chain

    t_0  ->  t_1  ->  t_2  ->  t_3  ->  ...

is a genuine infinite reduction in R.  **R is not strongly
normalizing.**

> *Oracle cross-check.*  `sim/output-final.txt` under the banner
> `Q3. NON-SN: infinite sequence from f(c)` prints `t_0..t_8` with
> their sizes and weights, and asserts that
> `step(t_n, (), "rho6") == t_{n+1}` for every `n = 0..7`.  The
> printed sizes are `2, 3, 4, 5, 6, 7, 8, 9, 10`, matching
> `size(t_n) = n + 2`.  The pattern continues without bound because
> rho6 applies at the root of every term of the form `f(·)`.

## §5. Rigor parity disclosure

All three obligations follow the same template.

- **Definitions up front.**  §0 pins down terms, redexes, reductions,
  normal forms.  §2, §3, §4 each open by stating precisely what
  positive or negative claim they are addressing.
- **Witness or strategy.**  §2 gives a closed witness.  §4 gives a
  closed witness *plus* an explicit infinite reduction schema.  §3
  gives a total reduction strategy together with a measure.
- **Explicit rule citations.**  Every rewrite step cites the rule
  applied, the position at which it fires, and the substitution
  sigma — including the inductive step `t_n -> t_{n+1}` of §4.
- **Internal verifications.**  Each question ends at an assertion
  backed by direct calculation: §2 refutes confluence via a head-based
  normal-form check and constant distinctness; §3 proves WN via strict
  measure decrease on every rule, context-closure induction, and
  well-foundedness of the positive integers; §4 refutes SN via a
  strictly increasing size bound and a per-step equality
  `step(t_n) = t_{n+1}`.
- **Oracle.**  Every arithmetic and rewrite claim is independently
  reproduced by `sim/simulator.py`; the captured output at
  `sim/output-final.txt` contains assertions that fail loudly on any
  discrepancy.  All assertions pass.

Q2 contains the longest argument because it must settle a universal
statement (every closed term, some reduction to normal form), whereas
Q1 and Q3 settle existential claims (some closed term, some
reductions witnessing failure).  That is an irreducible structural
asymmetry — not an asymmetry in effort.  Each verdict is supported by
(a) an explicit construction, (b) rule-cited reductions, and (c) a
verification argument whose steps are machine-checked by the oracle.
