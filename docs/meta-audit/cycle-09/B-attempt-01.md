# Attempt 01 — first-draft argument

> Initial draft.  Will be audited by the evaluator agent and revised into
> the final `ARGUMENT.md`.

## Verdicts

| Question | Verdict |
|----------|---------|
| Q1 confluence          | **NOT confluent**        |
| Q2 weak normalization  | **Weakly normalizing**   |
| Q3 strong normalization| **NOT strongly normalizing** |

## Q1 — R is not confluent

Witness: the closed term `t = m(c, d)`.

Two reductions of `t`:
- `t = m(c, d)  ->_{rho3}  c`   (rho3 at the root, matching `x := c, y := d`)
- `t = m(c, d)  ->_{rho4}  d`   (rho4 at the root, matching `x := c, y := d`)

`c` and `d` are nullary constants.  No rule LHS is a nullary constant, so
no rule can fire at a term that is just `c` or just `d`.  Hence `c` and
`d` are distinct normal forms.  So R is not confluent.

## Q2 — R is weakly normalizing

I give a strategy `S` that produces a normal form from every closed
term in finitely many steps, plus a polynomial measure `W` that strictly
decreases under every step of `S`.

### Strategy S

At a term `t`:
- If `t` has no redex, halt: `t` is a normal form.
- Otherwise pick any redex whose rule is NOT `rho6`, and apply that
  rule.  This is always possible because rho5 shares its LHS `f(x)` with
  rho6: whenever rho6 can fire at a position, rho5 can too.

### Measure W

Define `W` recursively:

    [0] = [c] = [d] = 1
    [s(t)] = 1 + [t]
    [f(t)] = 1 + [t]
    [u(t)] = 1 + [t]
    [g(t1, t2)] = 1 + 2*[t1] + [t2]
    [m(t1, t2)] = 1 + [t1] + [t2]

`W` takes values in positive integers.  For every symbol and every
argument, the coefficient is strictly positive, so `W` is strictly
monotone in each argument — i.e. replacing one child with a smaller
child (under `<`) strictly decreases the whole.

Check each rule (LHS minus RHS, under an arbitrary substitution):
- rho1: `[g(0,y)] - [y] = 1 + 2*1 + [y] - [y] = 3`.
- rho2: `[g(s(x),y)] - [s(g(x,y))] = (3 + 2*[x] + [y]) - (2 + 2*[x] + [y]) = 1`.
- rho3: `[m(x,y)] - [x] = 1 + [y]`.
- rho4: `[m(x,y)] - [y] = 1 + [x]`.
- rho5: `[f(x)] - [x] = 1`.
- rho7: `[u(u(x))] - [x] = 2`.

Every non-rho6 rule strictly decreases `W`.  Because `W` is strictly
monotone under every function symbol, the strict decrease is preserved
under contexts: any S-step sends `C[LHS σ]` to `C[RHS σ]` with `W(C[LHS σ]) > W(C[RHS σ])`.

Finally rho6 increases `W` by 1 — which is exactly why S excludes it.

### Termination

S-reductions produce a strictly decreasing sequence of positive
integers, so every S-reduction terminates.  S halts only at a term with
no redex.  Hence every closed term reaches a normal form under S.
R is weakly normalizing.

## Q3 — R is not strongly normalizing

Witness: `t_0 = f(c)`.  Apply rho6 at the root at every step.

    t_0 = f(c)
    t_0 ->_{rho6}  f(f(c))           = t_1     (match x := c, root)
    t_1 ->_{rho6}  f(f(f(c)))        = t_2     (match x := f(c), root)
    t_2 ->_{rho6}  f(f(f(f(c))))     = t_3     (match x := f(f(c)), root)
    ...
    t_n ->_{rho6}  f(f(t_n))         = t_{n+1} (match x := the body of t_n at the root)

At step `n`, `t_n = f^{n+1}(c)`, i.e. `n+1` nested `f`s over `c`.  The
size of `t_n` is `n + 2`, strictly increasing.  The sequence does not
repeat and does not terminate.  R is not strongly normalizing.
