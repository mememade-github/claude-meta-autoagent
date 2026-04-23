# R3 Enumeration Locus — Deliverable vs Oracle

> ROOT-owned reference for the Cycle #9 R3 clarification.  Codifies
> whether enumeration committed as oracle output (simulator runs,
> schema-conformant JSON, scorer output) counts toward R3 band 3, or
> whether band 3 requires the enumeration to live **inside the
> deliverable text** as an auditable table.

## Evidence anchor — Cycle #8 R3-B CONDITIONAL

Cycle #8 JUDGMENT.md §3 R3 scored B = 2 under the band-3 tightening
("the deliverable to present the enumeration in auditable tabular
form").  Evidence cited:

- B has tabular elements: §1.1 8-row rule LHS table; Appendix A 8-row
  sanity table; `B-simulator.py` + `B-sim-output-final.txt` full 104-
  triple CP enumeration mechanically (93 non-unifiable + 11 unifiable
  + 2 non-joinable).
- B's §2.5 enumerates the 11 unifiable critical pairs in **prose**, not
  as an in-deliverable table.  The full 104-cell enumeration lives in
  the *oracle* (`B-simulator.py::test_q1_cp_enumeration`), not the
  deliverable.

The proof-auditor flagged R3-B as CONDITIONAL on the locus question:
does the oracle-committed enumeration satisfy the tightening, or must
the deliverable itself carry the table?

## Resolution — Cycle #9 R3 band 3 criterion

When the enumeration has a **finite, tractable support** (critical
pairs of a finite TRS, overlaps between a bounded rule set, rules of
a small signature, cases of a bounded classification):

- **Band 3** requires:
  1. **Deliverable-side tabular presentation**: the deliverable text
     contains a table with one row per element of the support and a
     disposition column stating the treatment (joinable / non-joinable
     with reduction trace reference, discharged / counter-example, etc.).
     The table MAY be compressed via symmetry or equivalence classes
     if the compression is declared and justified in the deliverable.
  2. **Reproducible oracle output (when an oracle is used)**: if the
     deliverable cites an executable oracle to mechanically re-verify
     the support enumeration, the oracle output must be committed
     alongside with a reproducible `oracle_command` invocation.

- **Band 2**:
  - Oracle-committed full enumeration (schema-conformant JSON / simulator
    output / scorer output) WITHOUT a deliverable-side tabular
    presentation of the same support — the oracle carries the
    enumeration but the deliverable text only summarizes in prose.
  - OR: deliverable-side table covering only a subset of the support
    (e.g., "the interesting cases") with prose claim for the remainder.

- **Band 1–0**: as in base rubric (1–2 steps without justification,
  or no enumeration at all).

## Rationale

R3 measures *auditability of progressive minimization*.  An oracle
output is mechanically auditable, but an ARGUMENT.md reader cannot
audit the deliverable's reasoning against an external file without
context-switching.  The tightening's purpose was that the reader
should be able to verify the reduction *inline*, not by reading a
separate oracle output.

Oracle output is valuable **supplementary evidence**, earning the
delivery a place at band 3 provided the deliverable itself carries
the inline-auditable table.  Oracle alone is band 2 — the
mechanization is there, but the deliverable's argumentative
structure is incomplete.

## Combined pattern — band 3

The combined pattern that earns band 3 in a finite-support task:

1. Deliverable table listing each element of the support with
   disposition column.
2. Oracle output file committed alongside.
3. Deliverable cites the oracle's `oracle_command` and asserts
   the table is mechanically regenerable.
4. Oracle output file's content matches the deliverable table's
   rows (cross-checkable; if they diverge, the deliverable loses
   its band-3 claim).

This pattern is stronger than either alone: the deliverable is
self-contained for a reader doing paper-only audit, and the oracle
is there for a reader doing mechanical re-verification.

## Domains where this does not apply

- Enumeration with **infinite or intractable support** — inline
  tabular presentation is infeasible; the rubric reverts to "3+
  steps with brief justification" (base band 3).
- **Continuous enumerations** (integration, limit processes) —
  tabular form is not the natural shape; use the base rubric.
- **Enumerations over open classes** (proof tactics, design
  patterns) — tabular form implies closure, which may not hold.

## Cycle #9 pre-cycle port intent

L2 ROOT reads this file during Cycle #9 pre-cycle and ports the
band-2/3 locus boundary into `judgment-rubric.md` R3.  The base
tightening from Cycle #7 `band-3-tightening-v1.md` remains in place;
this file adds the locus clause.

## Non-inflation

A deliverable-side table with **fabricated or unverified rows** does
not earn band 3; it earns band 0 (false enumeration).  The
deliverable-side table's rows must be consistent with (a) the oracle
output if cited, or (b) a reader's ability to verify each row by
hand if no oracle.

## When to evolve this text

Edit this file when:

- A cycle surfaces a case where oracle-alone enumeration is judged
  sufficient for band 3 on domain-specific reasoning (document the
  exception with a named criterion).
- A cycle exhibits the combined pattern (deliverable table + oracle
  + cross-check) and the band-3 claim is unambiguous — promote this
  to a formal pattern description.

Do not edit to weaken the deliverable-side requirement after a
single cycle; ratchet is not bidirectional.
