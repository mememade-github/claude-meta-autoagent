# R8 Parametric Content Locus — Section-named vs Labeled-anywhere

> ROOT-owned reference for the Cycle #9 R8 clarification.  Codifies
> whether band-3 parametric / structural disclosure must appear in a
> dedicated "Open Questions" or "Limitations" section, or whether
> labeled structural content anywhere in the deliverable qualifies.

## Evidence anchor — Cycle #8 R8-B CONDITIONAL

Cycle #8 JUDGMENT.md §3 R8 scored B = 2 under the band-3 tightening
("≥ 1 structural / parametric disclosure").  Evidence cited:

B had multiple structural / parametric disclosures distributed across
§2.5, §5, and Appendix A:

- §2.5 **parametric statement**: "Any pair of rules with shape
  g(v_1, ..., v_n) -> v_i and g(v_1, ..., v_n) -> v_j with i != j
  produces a non-joining critical pair (v_i, v_j) at the root".
  Universally quantified.
- §5 **bidirectional rule-removal analysis**: "Removing q would make
  R confluent but leave non-WN intact.  Removing t would kill non-
  WN/non-SN but leave non-confluence intact."
- Appendix A **structural contrast**: alpha7 vs alpha4 size-growth
  distinction.

**Tightening threshold met** by content.  But the band-3 claim was
denied on a presentation-level ground: B had **no dedicated open-
questions section**.  The structural commentary lives in §5 (rigor
disclosure framing) and Appendix A (sanity reference framing), not
in a "what remains open / what could be different" framing.

The proof-auditor flagged R8-B as CONDITIONAL on the section-naming
question: does parametric content meeting the tightening criterion
qualify for band 3 when positioned outside an open-questions section?

## Resolution — Cycle #9 R8 band 3 criterion

R8 measures disclosure of **meaningful limits and open directions**
of the deliverable's argument.  The axis's purpose is to reward
epistemic honesty about what the argument does NOT close, not to
enforce a specific section layout.

- **Band 3** requires:
  1. **3+ distinct open questions / limitations / structural
     impossibilities** disclosed in the deliverable.
  2. **≥ 1 disclosure is structural / parametric** — a coefficient
     contradiction, dimensional argument, rule-class impossibility,
     or universally quantified statement showing *no* construction
     in a named family discharges the problem.
  3. **Each disclosure is labeled** explicitly as an open question,
     limitation, impossibility, or equivalent epistemic marker.
     Examples of sufficient labels:
     - "Open Questions" section header.
     - "Limitations" section header.
     - In-text label: "this remains open", "this is a limitation",
       "no linear interpretation of the form [...] satisfies [...]"
       stated as a parametric impossibility claim, "no rule in the
       class [...] closes [...]" stated as a class-level impossibility.
  4. Dedicated section naming ("Open Questions", "Limitations") is
     NOT required.  A deliverable may surface limitations inline in
     its §5 rigor-disclosure or Appendix structural-contrast, as
     long as each disclosure carries an explicit label.

- **Band 2**: structural / parametric content present, but:
  - No explicit labels marking the content as open-question /
    limitation / impossibility (the parametric statement is embedded
    in the main proof or a sanity appendix without framing as a
    limit); OR
  - Fewer than 3 distinct disclosures.

- **Band 1**: case-exhibition disclosures only (single failing
  instances) without structural generalization; or single
  disclosure at most.

- **Band 0**: no disclosure of open directions / limits.

## Rationale

Requiring a specific section-naming convention conflates
presentation with content.  A deliverable that carries its
limitation analysis in §5 as "rigor disclosure" is doing the
epistemic work the axis measures; denying band 3 on the basis of
section title would penalize authors who integrate their
limitations into structural discussion rather than segregating them.

What matters for R8 is:
1. The content is present (parametric / structural disclosure).
2. The reader can recognize it as open / limit / impossibility
   (explicit labeling).

The "explicit label" requirement is what prevents silent burial —
structural content must be *visible as a limit* to the reader, not
buried in the proof body without framing.

## Distinguishing labeled-anywhere from buried

The label requirement is satisfied when a reader reading only the
labeled sentence (without context from the surrounding §) can
identify the sentence as a disclosure of a limit / open question /
impossibility.  Example:

- ✓ Labeled: "No linear interpretation of the form a*|x| + b
  satisfies both ρ6 and ρ7 simultaneously (coefficient intersection
  empty)."  ← reader sees "No ... satisfies ..." as an impossibility
  claim immediately.
- ✓ Labeled: "Any pair of rules of shape g(v_1,...,v_n) -> v_i and
  g(v_1,...,v_n) -> v_j with i ≠ j produces a non-joining critical
  pair."  ← "Any pair ..." marks universal quantification; "produces
  a non-joining critical pair" labels the consequence.
- ✗ Buried: "We note that the reduction works because the
  coefficient set {1, 2, 3} contains no element c with ..." — reader
  reads this as an in-proof observation, not as a disclosure of
  impossibility unless framed.
- ✗ Buried: "The size-grows-but-φ-drops pattern is instructive."
  ← interesting observation but not framed as an impossibility or
  limit.

## Cycle #9 pre-cycle port intent

L2 ROOT reads this file during Cycle #9 pre-cycle and ports the
labeled-anywhere criterion into `judgment-rubric.md` R8.  The base
tightening from Cycle #7 `band-3-tightening-v1.md` (structural /
parametric over case-exhibition) remains in place; this file adds
the locus / labeling clause.

## Non-inflation

Fabricated parametric statements without justification earn band 0
on the fabrication axis (via R9 truth-matching); the R8 band-3
claim requires the disclosure to be *true* as well as *structural*.
A false impossibility claim does not earn R8 credit.

## When to evolve this text

Edit this file when:

- A cycle surfaces a legitimate open-question framing outside the
  examples above (document the new pattern).
- The "explicit label" criterion is shown to be gameable (tighten
  the recognition test).

Do not edit to re-require dedicated section naming without at least
2 cycles of evidence that labeled-anywhere content is gaming the
axis.
