# R1 motivation-answer consistency — v1

> Introduced at Cycle #11 pre-cycle (2026-04-23) to close the M9.4
> falsification R1 shape-verdict (Cycle #10 X probe earned R1 = 3
> via "NAND + S/K + field + group" named-precedent citation while
> stopping at 3-primitive textbook minimum — answer-shape did not
> match any cited precedent's shape).

## Rule

When a deliverable's motivation section invokes a **named structural
precedent** for single-primitive (or single-generator) reduction —
e.g., Boolean universality via NAND / Peirce's arrow, combinators
(S and K), one-instruction computers (OISC / SUBLEQ),
Wolfram's single axiom, interaction combinators, aperiodic monotile,
Rule 110 / FRACTRAN — band 3 additionally requires the deliverable's
final answer to satisfy one of:

- **(a) shape match** — the final basis has the same cardinality
  shape as the precedent.  For a single-primitive precedent, the
  final basis reduces to a single primitive (possibly paired with
  a terminal constant); for a two-primitive precedent, the final
  basis reduces to two primitives; etc.
- **(b) explicit departure justification** — the motivation section
  itself names the specific obstruction that blocks reaching the
  precedent's shape, with at least a sketch argument.  "Reaches
  3 primitives" is not justification for "NAND precedent suggests
  1"; an actual obstruction argument is required (e.g., "unlike
  Boolean, the continuous domain requires both forward and inverse
  transcendentals because X, and these cannot be collapsed because
  Y").

Named-precedent citation without (a) or (b) maxes at **band 2**.

## Evidence anchor

**Cycle #10 X-ARGUMENT.md §1** cited NAND, Sheffer stroke, S/K
combinators, transcendence bases, and group rank — five separate
structural precedents each of single-generator or minimal-generator
shape.  X's final answer (§4): 2 unary + 1 binary + 1 constant = 4
symbols.  X's §1 did not name any obstruction to reaching single-
primitive form; it concluded at "exp is the transcendental core"
without probing further.  Under unmodified Cycle #10 rubric R1 band-
3 text, X earned band 3 because the precedents are real and argued
from first principles.  Under the tightening above, X's R1 earns
band 2 because (a) fails (answer-shape is 3-primitive, precedents
are single-primitive) and (b) fails (no obstruction argument).

## Scope conditions

- **Applies when** R1 cites at least one of the named structural
  precedents above, or a functionally equivalent single-primitive
  / minimal-generator analog.
- **Does not apply when** R1 cites only generic motivation ("reducing
  redundancy is good") or domain-internal motivation without cross-
  domain precedent invocation — in that case, the band text
  unchanged from pre-tightening version applies.

## Non-inflation

Motivations that cite a precedent AND produce a matching answer
shape AND explicitly sketch the analogy (e.g., "our task is to
continuous-domain what NAND is to Boolean, and we achieve this
because X") earn band 3 under both the pre-tightening and
post-tightening versions — the tightening does not demote
correct-and-complete motivations.

## Portability

L2 ROOT ports this clarification into `docs/research/eml-paper/
judgment-rubric.md` as a band-3 tightening addendum to R1, following
the same syntactic pattern used for M8.1 R3 locus and M8.2 R8
locus ports in prior cycles.
