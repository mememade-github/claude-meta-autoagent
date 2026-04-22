# Iteration 1 — self-audit of ARGUMENT.md

Goal of this pass: stress-test the §4 triangle proof against the
trickiest rules (Y, S, M) and verify the simulator's claims agree
with the analytic proof on a worked instance.

## Audit point A — Y with reducible inner argument

Take `M = Y (I g)`.  The inner `I g` is a redex; the outer `Y _` is
also a redex.  Three distinct one-step parallel reductions:

  - D1 (app + I-step inside): `Y (I g) ⇒ Y g`
  - D2 (Y-step with parallel reduction `(I g) ⇒ g`):
    `Y (I g) ⇒ g (Y g)`
  - D3 (Y-step with reflexivity on `I g`):
    `Y (I g) ⇒ (I g) (Y (I g))`

Compute `M* = (Y (I g))* = (I g)* (Y (I g)*) = g (Y g)`.

Verify each Dᵢ-result `Nᵢ ⇒ M*`:

  - N1 = `Y g`.  Apply Y-step with `g ⇒ g`: `Y g ⇒ g (Y g) = M*`.  ✓
  - N2 = `g (Y g)` = M* itself.  ⇒ by reflexivity.  ✓
  - N3 = `(I g) (Y (I g))`.  Apply app rule: need
    `(I g) ⇒ g` (by I-step) and `(Y (I g)) ⇒ (Y g)` (by app rule
    with `Y ⇒ Y` and `(I g) ⇒ g`).  Result `g (Y g) = M*`.  ✓

All three diverging parallel steps reach `M*` in one further parallel
step.  Diamond confirmed on this concrete case, *including* the case
where `Y`'s recursive RHS creates a fresh `Y`-redex that must be
reconciled against an arm that already pre-reduced the inner `I g`.

## Audit point B — S with duplicated argument carrying a redex

Take `M = S a b (I c)`.  Here `z = (I c)` is duplicated by the
S-rule.  Two interesting parallel reductions:

  - D1 (S-step with `(I c) ⇒ c`):  `M ⇒ a c (b c)`.
  - D2 (app-only, fire I inside): `M ⇒ S a b c`.
  - D3 (S-step with `(I c) ⇒ I c` reflexively):
    `M ⇒ a (I c) (b (I c))`.

`M* = (S a b (I c))* = a* c (b* c) = a c (b c)` (assuming a, b atomic).

Triangle:
  - N1 = `a c (b c)` = M*. ✓
  - N2 = `S a b c`.  Apply S-step (with refl on a, b, c):
    `S a b c ⇒ a c (b c) = M*`.  ✓
  - N3 = `a (I c) (b (I c))`.  Need ⇒ to `a c (b c)`.  Apply app
    rules walking down: `(I c) ⇒ c` via I-step, twice (independent
    pointwise applications of ⇒ to the two distinct positions where
    `(I c)` appears).  Result: `a c (b c) = M*`.  ✓

This is the case where left-linearity matters: the two copies of
`(I c)` in N3 are independent positions and we apply ⇒ to each
independently.  No synchronization needed because no rule LHS has a
non-linear pattern.

## Audit point C — M M (the stuck loop)

`M M ⇒ ?`  Only the rule_M applied at root: `M (M) ⇒ M M`.  Or app-
only: `M M ⇒ M M`.  Both give the same result `M M`.  Single one-step
reduct is `M M`.  M* = (M M)* = M (M)* = (after star on the spine)
let's compute carefully.

`M M` has spine head `M` (a primitive symbol), args `[M]`.  M is a
rule-head with arity 1, and we have 1 ≥ 1 args.  So
`(M M)* = r_M[x := M*] = (M*) (M*) = M M`.

So M* = M M.  Diamond closes with `P = M M`.  No paradox.

This is reassuring: a fixed-point under reduction does not violate
confluence; it just means the diamond closes in zero net moves.

## Audit point D — does the proof use anything other than (P1) and (P2)?

Re-reading §4.6: the case analysis uses
  - distinct head primitives (P1) — to argue that at most one
    `rule_c` can apply at a given root position
  - left-linearity (P2) — to argue that the substitution
    `r_c[v_i := v_i*]` is well-defined and that pointwise ⇒ on each
    occurrence of a duplicated variable on the RHS is sound
  - left-linearity *of the LHS* (which is what (P2) means) — to
    argue that the LHS pattern matching is unambiguous and unaffected
    by inner reductions

No additional structural property is needed.  In particular, no use
is made of:
  - confluence of any subset (the proof is direct, not by induction
    on rule count)
  - termination, weak normalization, or normal form existence
  - any specific reduction strategy (the proof is about the relation,
    not how steps are scheduled)

## Audit point E — counting agreement with simulator

§4.2 claims 0 non-trivial critical pairs.
`example_5_overlap_audit` in `sim.py` enumerates all 13 LHS shapes
and confirms each is rooted at a distinct primitive head with arity
∈ {1, 2, 3, 4}.  Manual count of (rule, rule, position) triples
where rule's LHS could unify with a non-variable subterm of another's
LHS: 0.  Agreement.  ✓

§6.2 claims `(Y f)* = f (Y f)`.  Simulator output line 74:
`star(Y f) = f (Y f)`.  Agreement.  ✓

§6.3 claims both leftmost-outermost and rightmost-innermost on
`B (W I) (K a) c` reach `a a`.  Simulator output lines 87, 95.
Agreement.  ✓

## Conclusion of audit

No issues found.  The argument as written discharges all 7 sections
of the brief, agrees with the executable oracle on every checked
instance, and does not depend on any banned named technique (the
proof is built from primitives: parallel reduction, complete
development, triangle, diamond, tile-closure).

No further iteration needed; the deliverable in `task/ARGUMENT.md`
stands.
