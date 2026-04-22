# Iteration 1 — self-audit of ARGUMENT.md

Target of this pass: stress-test both obligations independently and
verify the simulator's mechanical claims agree with the analytic
proof on every claim made.

## Audit point A — completeness of critical-pair enumeration

The §3.1 procedure enumerates overlaps by: for every ordered pair
(ρᵢ, ρⱼ), every non-variable position p of ρᵢ's LHS, attempt
unification of ρᵢ's subterm at p with ρⱼ's LHS (renamed apart),
excluding (ρᵢ, ρᵢ, ε).

Cross-check symbol-by-symbol.  The non-variable subterms of each
LHS and their head symbols (as in §3.1's position table):

  ρ₁: subterm nil at (1) — head nil (nullary constructor)
  ρ₂: subterm cons(x, ys) at (1) — head cons
  ρ₃: subterm nil at (1) — head nil
  ρ₄: subterm cons(x, xs) at (1) — head cons
  ρ₅: subterm app(xs, ys) at (1) — head app

For the outer-rule subterm to unify with an inner-rule LHS, the head
symbols must match.  Rule LHS root heads: ρ₁=len, ρ₂=len, ρ₃=app,
ρ₄=app, ρ₅=app.

  - len-headed inner rules (ρ₁, ρ₂) cannot overlap any subterm
    because no LHS subterm has head len.
  - app-headed inner rules (ρ₃, ρ₄, ρ₅) can only overlap the subterm
    with head app: the subterm at (1) of ρ₅'s LHS.
  - nil-headed and cons-headed positions have no rules with those
    root heads (nil and cons are constructors, not defined symbols).

Therefore overlaps exist only with ρ₅ as the outer rule and ρ₃/ρ₄/ρ₅
as inner rules — exactly 3 critical pairs.  Mechanical enumeration by
`sim.py` produces the same three (see `sim_output.txt` section 1).
Agreement.  ✓

## Audit point B — joinability of each critical pair

CP#1 outer ρ₅ / inner ρ₃.  Common reduct `app(ys, zs)` reached in 0
steps from reduct `app(ys, zs)` and 1 step from reduct `app(nil,
app(ys, zs))` via ρ₃.

CP#2 outer ρ₅ / inner ρ₄.  Common reduct `cons(x, app(xs, app(ys,
zs)))` reached in 1 step from outer-reduct via ρ₄, and in 2 steps
from inner-reduct via ρ₄ then ρ₅.

CP#3 outer ρ₅ / inner ρ₅.  Common reduct `app(xs, app(ys, app(zs,
ws)))` reached in 1 step from outer-reduct via ρ₅, and in 2 steps
from inner-reduct via ρ₅ then ρ₅ (at position (2)).

Mechanical closed-witness verification in `sim.py` section 1
reproduces joinability (same normal form for both reducts in each
case).  Agreement.  ✓

## Audit point C — monotonicity of the interpretation

Claim: every constructor's interpretation is strictly monotone in
each argument.

  [s(x)]       = x + 1                 ∂/∂x = 1   (strict)
  [cons(x,y)]  = x + y + 1             ∂/∂x = 1, ∂/∂y = 1   (strict)
  [len(x)]     = 2x                    ∂/∂x = 2   (strict)
  [app(x,y)]   = 2x + y                ∂/∂x = 2, ∂/∂y = 1   (strict)

All coefficients strictly positive.  Lift to context monotonicity by
structural induction on the context hole's depth.  ✓

## Audit point D — per-rule strict decrease, arithmetic recheck

  ρ₁:  [len(nil)] − [0]
     = 2·1 − 1 = 1.                                strict.
  ρ₂:  [len(cons(x, ys))] − [s(len(ys))]
     = 2(x + ys + 1) − (2ys + 1)
     = 2x + 2ys + 2 − 2ys − 1 = 2x + 1.            strict (x ≥ 1 ⇒ ≥ 3).
  ρ₃:  [app(nil, ys)] − [ys]
     = (2·1 + ys) − ys = 2.                        strict.
  ρ₄:  [app(cons(x, xs), ys)] − [cons(x, app(xs, ys))]
     = 2(x + xs + 1) + ys − (x + 2xs + ys + 1)
     = 2x + 2xs + ys + 2 − x − 2xs − ys − 1 = x + 1. strict (≥ 2).
  ρ₅:  [app(app(xs, ys), zs)] − [app(xs, app(ys, zs))]
     = 2(2xs + ys) + zs − (2xs + 2ys + zs)
     = 4xs + 2ys + zs − 2xs − 2ys − zs = 2xs.       strict (xs ≥ 1 ⇒ ≥ 2).

Every difference is a polynomial in the LHS variables with non-
negative coefficients plus (ρ₁, ρ₃) a positive constant or (ρ₂, ρ₄,
ρ₅) a positive coefficient on a variable that is ≥ 1 under the
positive-integer domain of `[·]`.  Mechanical witness-grid check in
`sim.py` section 2 reports min-difference positive in every row.
Agreement.  ✓

## Audit point E — exhaustive-graph oracle agreement

`sim.py` section 3 runs BFS reachability on 11 closed terms.  For
each, it:
  - verifies every out-edge of every reached state strictly decreases
    `[·]` (termination witness at edge granularity),
  - computes the set of normal forms reached, asserts |NFs| = 1
    (confluence witness).

Every test returns a single normal form and raises no measure
violation.  The largest term tested has 515 distinct reducts; the
longest chain observed is 114 steps, beneath the `[t₀] = 115` bound.
Agreement with the algebraic claims.  ✓

## Audit point F — disclosed gaps and limitations

Gap F1 (disclosed in §7.1).  The polynomial interpretation used does
NOT extend to the augmented system that adds `len(app(xs, ys)) →
add(len(xs), len(ys))`.  With the forced choice `[add(x,y)] = 2x +
y` (from ρ₇'s strict-decrease constraint), the new rule gives
`[LHS] − [RHS] = 0`, failing strict decrease.  A nonlinear or
lexicographic measure is needed for the augmented system.  This is a
concrete limitation of the measure, not of the argument scheme.

Gap F2 (implicit, disclosed here for iteration closure).  The §4.1
case (b) analysis is presented as a three-sub-case exhaustive split,
but relies on the fact that R's RHSs are each linear in their LHS
variables (no LHS variable appears more than once on the RHS).  This
is not part of the brief's "left-linear" assumption — it's an
additional property of R.  A rule with a duplicating RHS (e.g., a
hypothetical `square(x) → times(x, x)`) would turn "at most one
residual of σ" into "two residuals of σ", and the §4.1 case (b)
argument would need to fire σ twice in `u₁` to rejoin.  The argument
still works, but the "at most one residual" convenience is not
general.  Disclosure: the argument as written treats a convenient
subset; a fully general treatment of case (b) needs a per-occurrence
application of σ, which is standard but not reproduced here.

Gap F3 (disclosed in §7.4).  The chosen measure is a linear
polynomial.  Linear polynomials are tight for this R but fragile
under extension.  A multiset or lexicographic measure would be more
robust but over-engineered for R.  The choice is deliberate and its
limitations are disclosed.

## Audit point G — no reliance on banned named results

Spot-check: the ARGUMENT.md text uses only the allowed structural
vocabulary (critical pair, overlap, joinable, confluent, terminating,
well-founded, measure, interpretation, monotonic, strictly
decreasing, rewrite, rewriting).  The "local confluence + termination
⇒ confluence" implication is derived inline in §4.1 by well-founded
induction; it is not invoked by name.  The interpretation-based
termination argument is presented from first principles (polynomial
strict monotonicity + strict decrease per rule ⇒ no infinite chain);
no named ordering technique is invoked.  ✓

## Audit point H — balance between Q1 and Q2

The brief warns against treating one obligation cursorily.  Checking:

  - Q1 occupies §3.1 (CP enumeration with closing sequences), a large
    chunk of §4.1 (case analysis + lifting derivation), plus
    examples in §6.
  - Q2 occupies §3.2 (measure construction + 5-row decrease table),
    §4.2 (termination derivation + step bound), and exercise in §6.3.

Both are developed from first principles; neither is hand-waved.  No
asymmetry to disclose.  ✓

## Conclusion of iteration 1

Three gaps disclosed: F1 (measure fragile under extension), F2
(case-(b) argument assumes RHS-linearity), F3 (linear polynomial
choice).  None invalidates either verdict on R as stated.

Action taken in iteration 1: made all three gaps explicit in the
ARGUMENT.md (F1 and F3 in §7; F2 expanded in §4.1 "case (b)" text and
§7.2).  Verified symbolic and executable channels agree on every
concrete claim (critical pair count, joinability, per-rule decrease,
full-graph reachability for 11 test terms).

No further iteration needed; the deliverable at `task/ARGUMENT.md`
stands.  Iteration closed.
