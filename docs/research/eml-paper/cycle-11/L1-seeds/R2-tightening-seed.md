# R2 sublemma discharge locus — v1

> Introduced at Cycle #11 pre-cycle (2026-04-23) to close the M9.4
> falsification R2 shape-verdict (Cycle #10 X probe declared 3
> named sublemmas then discharged them distributively via a
> downstream reduction table without per-sublemma proof blocks —
> earned R2 = 3 via surface-decoration pattern).

## Background

Cycle #7 introduced R2 band-3 tightening requiring distinct proof
tools to be "isolated as a named sublemma stated and discharged
separately from the main argument" when the deliverable uses
distinct proof tools.  The text was ambiguous about *where* the
discharge must happen:

- **Reading A (strict, now adopted):** each sublemma carries its
  own statement-proof pair.  Statement block followed immediately
  by proof block, either in the same subsection or adjacent
  subsections.
- **Reading B (lenient, now excluded):** sublemmas are declared in
  one subsection and discharged distributively elsewhere (e.g.,
  via a later reduction table that collapses multiple sublemmas
  without per-sublemma lemma-proof structure).

The falsification probe exploited Reading B: X §2.2 listed three
named sublemmas and §3 presented a 6-row reduction table that
collapsed all three sublemmas without any per-sublemma proof.

## Rule

Band 3 requires **per-sublemma statement-and-proof locality**:

- **(a) Statement locality** — each declared sublemma has its own
  statement block (a distinct named paragraph or subsection that
  exhibits the sublemma's claim).
- **(b) Proof locality** — each declared sublemma has its own
  proof block immediately following its statement (same subsection
  OR the adjacent subsection), presenting the argument for that
  sublemma specifically, not a multi-sublemma combined argument.
- **(c) Non-distributed discharge** — the deliverable may additionally
  reference sublemmas from a downstream reduction table or summary
  proof, but the table alone cannot substitute for per-sublemma
  proof blocks.

Declarations with (a) but without (b) — named sublemmas without
per-sublemma proofs — max at **band 2** regardless of whether a
downstream reduction table appears to "use" the sublemmas.

## Evidence anchor

**Cycle #10 X-ARGUMENT.md §2.2** named three sublemmas (Transcendental
collapse, Arithmetic conjugation, Constant collapse).  **§3** then
presented a 6-row reduction table (A → B → C → D → E → F) whose
row-by-row justifications sometimes cited a sublemma by name but
never presented a per-sublemma proof block.  The sublemmas were
surface-decoration labels without proof content.  Under unmodified
Cycle #10 rubric R2 band-3 text, X earned band 3 because "stated
and discharged separately" was satisfied under Reading B.  Under
the tightening above, X's R2 earns band 2 because (b) Proof
locality fails — no per-sublemma proof block exists anywhere in X.

## Scope conditions

- **Applies when** the deliverable's method declares named
  sublemmas (regardless of whether the tightening of Cycle #7
  "distinct proof tools" clause triggers).
- **Does not apply when** the method uses a single unified
  argument without declaring sublemmas — pre-tightening band
  text still applies.

## Non-inflation

Methods with (i) one statement per sublemma + (ii) one proof per
sublemma in adjacent location + (iii) downstream reduction table
that references the proofs — the standard lemma-proof-theorem
pattern — earn band 3 under both pre-tightening and post-tightening
versions.  The tightening does not penalize deliverables that do
follow the lemma-proof pattern.

## Interaction with Cycle #7 tightening

The Cycle #7 tightening requires "distinct proof tools as named
sublemmas".  This Cycle #11 tightening is additive — a deliverable
that meets Cycle #7 (distinct tools → named sublemmas) but fails
this tightening (sublemmas declared but not discharged per-sublemma)
earns band 2.  A deliverable that uses one unified tool does not
need named sublemmas and is evaluated against pre-tightening band
text.

## Portability

L2 ROOT ports this clarification into `docs/research/eml-paper/
judgment-rubric.md` as a band-3 locus clause on R2, following the
same port pattern used for M8.1 R3 locus and M8.2 R8 locus in
prior cycles.
