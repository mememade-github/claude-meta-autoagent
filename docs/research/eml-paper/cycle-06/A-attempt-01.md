# Attempt 01 — derivation trace

Task: joint confluence + termination for the 5-rule list/length TRS
(ρ₁..ρ₅ over Σ = {0, nil, s, cons, len, app}).

## Steps taken

1. Read brief.  Identified two obligations Q1 (confluence) and Q2
   (termination) to be settled independently.

2. Inspected ruleset for structural features:
   - All 5 rules left-linear.
   - RHSs linear in LHS variables (incidental bonus).
   - ρ₂, ρ₄, ρ₅ have RHS of same or greater node count than LHS.
   - Only ρ₅ has head `app` in its LHS subterm at position (1).

3. Enumerated candidate overlaps.  Head-matching constraint reduces
   the search to (ρ₅ outer × ρ₃/ρ₄/ρ₅ inner at position (1)).  Three
   critical pairs.

4. Closed each critical pair by hand, exhibiting explicit joining
   reduction sequences.

5. Constructed a polynomial interpretation.  Tried `[app(x,y)] = 2x +
   y` (motivated by the need to penalize the left operand of app, so
   ρ₅'s "move material from left to right" shift strictly decreases
   the measure).  Verified this, together with `[len(x)] = 2x` and
   obvious choices for constructors, strictly decreases on all 5
   rules.

6. Wrote `sim.py` to:
   - enumerate critical pairs mechanically by first-order unification,
   - verify interpretation strictly decreases per rule via a witness
     grid,
   - BFS-exhaust the reduction graph of 11 closed test terms and
     check unique normal forms + monotone decrease on every edge,
   - trace leftmost-outermost vs rightmost-innermost reductions with
     the measure annotated at each step.

7. Ran simulator.  All three CPs found and closed; all 5 rules strict
   per witness grid; all 11 test terms confluent and terminating
   under the measure; both trace strategies in three worked examples
   converge to identical normal forms.

8. Wrote ARGUMENT.md with all 7 required sections:
   §1 motivation (why confluence/termination plausible), §2 method
   design (2.1 confluence procedure, 2.2 termination procedure, 2.3
   non-conflation), §3 progressive derivation (3.1 CP list with
   closings, 3.2 measure + per-rule decrease arithmetic), §4 verdicts
   (4.1 Q1=confluent with local-confluence + well-founded-induction
   lifting derived from first principles, 4.2 Q2=terminates with
   step bound, 4.3 joint implication), §5 verification (symbolic
   channel + executable oracle), §6 worked examples (associativity in
   two orders, len/app interleave, rho5-dominated termination), §7
   open questions (4.1 augmented system with add, 4.2 left-linearity
   dependence, 4.3 independence of verdicts for R, 4.4 nature of
   measure).

9. Self-audit in `iterations/iter-01-audit.md` with three disclosed
   gaps (measure fragility under §7.1 extension; case-(b) reliance
   on RHS-linearity; linear-polynomial choice).

## Verdict

Q1: R is confluent.
Q2: R terminates.

Both verdicts independently established; joint implication (Q2 ⇒
local-confluence-lift-to-Q1) derived from first principles in §4.1.
