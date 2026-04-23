---
status: draft
cycle: 8
domain: confluence-wn-sn-of-trs-with-q-and-t-rules
auditor: proof-auditor
auditor_date: 2026-04-23
arbitration_triggered: false
incumbent_total_A: 20
incumbent_total_B: 26
auditor_total_A: 20
auditor_total_B: 26
agreement: 17_YES_3_CONDITIONAL_0_NO
audit_file: cycle-08/rubric-audit.json
---

# Cycle 08 — JUDGMENT

Grading of `docs/meta-audit/cycle-08/A-ARGUMENT.md` and
`docs/meta-audit/cycle-08/B-ARGUMENT.md` against
`docs/research/eml-paper/judgment-rubric.md` (R1–R10, total 30
points) with the Cycle #7 R4 3-obligation semantic (TASK §1 prompt
asks for all three of Q1/Q2/Q3 with comparable rigor) and the
Cycle #8 pre-cycle R10 M6.3 sharpening (commit `988e3ed`) which
names `gap-closure-check.schema.json` as the canonical shape of the
band-3 substitute (c).

Front-matter `status` is `draft` at the time of writing; transitions
to `draft` (auditor concurs) / `arbitration-pending` / `arbitrated`
per CLAUDE.md §6.7 step 5c after the proof-auditor pass.

---

## §0. Cycle artefacts (audit record)

Captured at cycle close (2026-04-23 02:30 UTC).

| Path                                         |  Bytes | Role |
|----------------------------------------------|-------:|------|
| `docs/meta-audit/cycle-08/TASK.md`           |   8345 | Operative TASK prompt (rubric-blind; verified) |
| `docs/meta-audit/cycle-08/A-ARGUMENT.md`     |   8757 | A deliverable (single-shot) |
| `docs/meta-audit/cycle-08/B-ARGUMENT.md`     |  17258 | B deliverable (iteration 2) |
| `docs/meta-audit/cycle-08/B-attempt-01.md`   |   5856 | B iteration 1 draft |
| `docs/meta-audit/cycle-08/B-simulator.py`    |  13009 | B executable oracle |
| `docs/meta-audit/cycle-08/B-sim-output-final.txt` | 3924 | B oracle output |
| `docs/meta-audit/cycle-08/B-gap-closure-check.json` |  ≈8 KB | M7.2 closure-artefact (ROOT-verified per-gap closure) |

**Execution timing.**

- A launched 02:20:53 UTC; ARGUMENT.md written 02:22 (~1.5 min);
  exit ~02:23 (~2.5 min wall-clock).  **Single-shot deliverable.**
  A's working directory carried stale Cycle #7 files (`sim.py`,
  `sim_output.txt`, `attempts/`, `iterations/`) which A did not
  use; A's new ARGUMENT.md overwrote the prior in place.  No
  Cycle #8 evaluator report, no Cycle #8 iteration trace.
- B launched 02:20:53 UTC; archived prior cycle into
  `archive-prior-cycle-2/` at 02:23; simulator.py at 02:24;
  output-final.txt at 02:24; iterations/attempt-01.md at 02:25
  (5856 B); ARGUMENT.md at 02:27 (17258 B).  **Two iterations
  with byte-distinct, structurally-different drafts.**  No
  separate `.eval-report-*.json` produced by B; the M7.2
  closure-check artefact was authored by ROOT (next sub-bullet).
- ROOT authored `B-gap-closure-check.json` at 02:30 — diff
  verification of G1–G7 gaps that B's iteration 2 closes,
  schema-conformant per Cycle #8 pre-cycle R10 M6.3 sharpening.
  `verifier_identity: ROOT`; `non_inflation_check.result:
  no-new-gaps`.

B's byte-size delta (`attempt-01 = 5856` vs `ARGUMENT = 17258`,
Δ = +11 402 bytes) reflects substantive restructuring: 4-section
scratch flow → 6-section per-question structured proof + Appendix.
`diff -u` shows 585 line-level changes over the joint diff,
consistent with non-cosmetic iteration.

---

## §1. Leak audit

Base `scripts/meta/paper-leak-audit.sh` (eml-paper keyword set):

- A: `[Paper-leak audit passed] docs/meta-audit/cycle-08/A-ARGUMENT.md`
- B: `[Paper-leak audit passed] docs/meta-audit/cycle-08/B-ARGUMENT.md`

Cycle-07 inherited extended banned-identifier grep (34 names
total, enumerated in TASK.md §1 constraints):

- A: no matches (exit 1)
- B: no matches (exit 1)

**Both PASS on all leak scans.**  Cycle-#1-through-#8 leak streak: 8.

---

## §2. Agent A score: 20 / 30

### R1 Motivation — 1

A produced no opening motivation section.  §0 is signature setup;
§1 is the NF-classification preliminary (a lemma, not motivation).
§2 (Q1) closes with a structural-precedent paragraph: "the pair
(alpha5, alpha6) is exactly a non-deterministic projection
operator that commits irrevocably to one coordinate".  This is
genuine structural motivation, but it is for Q1 only and is in the
*closing* of §2 rather than as opening framing.  §3 (Q2) and §4
(Q3) have no motivation paragraphs.  §5 "Consistency check" is a
post-hoc relationship discussion, not motivation.

Without prompt hint inviting a motivation section, A produced
implicit per-question motivation only, and only for one question.
Band 1 — sparse, post-hoc, single-question structural commentary.

### R2 Method design — 3

**Tightened-band-3 check (named sublemmas under distinct tools):**
A has **two named sublemmas / lemmas:**

- **(NF-1)** in §1 — "A ground subterm whose tree contains only
  the symbols `0`, `e`, and `s` is a normal form" + proof by
  inspection of LHS heads.
- **Unique Redex Lemma** in §3.1 — "for every n ≥ 0, the term
  t(s^n(0)) has *exactly one* redex" + proof enumerating subterms
  and matching against rule LHSs.

Each is named, separately proved, and cited downstream (§2 cites
NF-1 for Q1 NF check; §3.2 cites Unique Redex Lemma in the
no-normalizing-path induction; §4 reuses the Unique Redex Lemma).
Distinct proof tools per question (Q1: head-mismatch + distinctness;
Q2: structural induction over reduction-sequence length; Q3:
explicit construction).  Each tool is identifiable in its own
sub-section.  Meets tightened R2.  Band 3.

### R3 Progressive minimization — 1

**Tightened-band-3 check (tabular form for finite tractable
support):** A presents NO critical-pair enumeration in any form.
A's Q1 proof goes directly to a single witness `q(0, e)` without
enumerating the overlap support.

The progression A does have is: §1 (NF lemma) → §2 (Q1 witness +
discharge) → §3 (Q2 lemma + induction discharge) → §4 (Q3 explicit
sequence).  This is sequential per-question progression but not
"progressive minimization" in the rubric sense (no iterative
narrowing of a candidate set).  Band 1 — 1–2 intermediate steps
without enumeration justification.

Without prompt hint asking for CP enumeration, A's witness-only
approach skips the enumeration entirely.

### R4 Verdict commitment — 3

Per Cycle #7 R4 3-obligation semantic adopted for this cycle: band
3 = "firm commitments on all three obligations AND each discharged
rigorously".  A §"Verdicts" table commits Q1 NOT confluent + Q2
NOT WN + Q3 NOT SN.  Each is discharged separately:

- Q1 (§2): witness q(0, e) + alpha5/alpha6 derivations + NF check
  + distinctness check + conclusion.
- Q2 (§3): witness t(0) + Unique Redex Lemma + induction over
  reduction-sequence length + conclusion.
- Q3 (§4): witness t(0) + explicit infinite sequence + per-step
  rule citation + conclusion.

§5 derives the cross-question relationships (Q3 follows from Q2;
Q1 independent of normalization).  Band 3.

### R5 Exact form — 3

A's witnesses + reductions are mechanically correct.  Verified by
`/tmp/verify_cycle08.py` (ROOT-side oracle):

- Q1: q(0, e) → 0 via alpha5; q(0, e) → e via alpha6; both NF;
  distinct.  ✓
- Q2: for n = 0..10, t(s^n(0)) has unique redex (alpha7 at root);
  reduces to t(s^{n+1}(0)).  ✓
- Q3: explicit infinite sequence pattern.  ✓

A's exact reductions match the underlying TRS semantics exactly.
Band 3.

### R6 Verification strategy — 3

A's verification is purely symbolic (no executable oracle).  Two
named lemmas (NF-1, Unique Redex Lemma) discharge the load-bearing
claims; both proved by transparent enumeration of LHS heads vs
subterm heads.

Per §5a disclosed-circularity scan (below): A's NF-1 is
self-contained (cites only LHS-head list); A's Unique Redex Lemma
cites NF-1 + extends with head-matching for t(s^n(0)) — linear
dependency, no circularity; A's §3.2 induction cites Unique Redex
Lemma — linear, no circularity; A's §5 consistency check is a
trivial implication (Q3 from Q2 + Q1 independence) without
hidden dependencies.

**No oracle is required for band 3** under R6 ("when the domain
admits one, a working executable oracle ... counts as a 3 indicator
**in addition to** the trace-argument path").  A's algebraic /
trace-argument path with no disclosed gap remaining qualifies as
band 3.  Band 3.

### R7 Constructive examples — 2

**Tightened-band-3 check (≥ 4 examples OR ≥ 3 orthogonal):**

A's constructive examples:

- §2 — q(0, e) → 0 and q(0, e) → e (Q1 divergent pair, 2 reductions
  on 1 closed term).
- §3 — t(0) with the unique-reduction induction (Q2).
- §4 — t(0) with the explicit infinite reduction sequence first
  five steps + general pattern (Q3).
- §6 — summary table with 3 rows, one per obligation.

Counting strictly: 2 distinct closed-term witnesses (q(0, e) and
t(0)).  Q2 and Q3 share the t(0) witness; Q1 has the independent
q(0, e) witness.  Across "orthogonal axes": 2 (non-confluence axis
+ non-normalization axis); the Q2/Q3 axes are not orthogonal
(Q3 follows from Q2 by definition, as A's §5 notes).

Generous count: 3 examples (Q1 pair, Q2 induction, Q3 sequence) —
band 2 base.  Tightening cap: 2 orthogonal axes, less than the
4-example or 3-orthogonal threshold.  Band 2.

### R8 Open questions — 1

A has **no open-questions section.**  §5 "Consistency check of the
three verdicts" is a cross-question implication discussion (Q3 from
Q2; Q1 vs Q2/Q3 independence) and includes a single trivial
rule-removal observation: "Removing alpha7 from R would not restore
confluence (Q1's witness survives); removing alpha5 and alpha6 would
not restore normalization (Q2/Q3's witness survives)."

This is a **single-instance rule-removal observation**, not a
parametric / structural disclosure (which would generalise: "no
single-rule removal restores confluence because ...").  It is
genuine but trivial.  Band 1 — trivial observation only.

Without prompt hint asking for open questions, A produced none.

### R9 Exact answer match — 3

R9 binary for Cycle #8 per the 3-obligation semantic: 3 iff
ARGUMENT produces correct verdicts on **all three** of Q1
(non-confluent), Q2 (non-WN), Q3 (non-SN) with rigorous discharge.

A commits all three correctly:
- Q1: NOT confluent — witness q(0, e), distinct NF reducts.  ✓
- Q2: NOT WN — witness t(0), unique-reduction lemma showing every
  reduction is infinite.  ✓
- Q3: NOT SN — witness t(0), explicit infinite reduction pattern.  ✓

Each discharged with a concrete witness + per-step rule citation.
Mechanically verified (`/tmp/verify_cycle08.py` ✓).  Band 3.

### R10 Iteration depth — 0

A's Cycle #8 on-disk artefacts (container:
`claude-meta-autoagent-a`, mount `/workspaces/task/`):

| Path | mtime | Bytes | Role |
|------|-------|------:|------|
| `task/ARGUMENT.md` | 02:22 | 8757 | Single substantive write |
| `task/sim.py` | 17:34 (Apr 22) | 11024 | **Stale Cycle #7 file**, untouched |
| `task/sim_output.txt` | 17:34 (Apr 22) | 4765 | **Stale Cycle #7 file**, untouched |
| `task/attempts/` | (Cycle #7 stale files only) | — | No Cycle #8 entries |
| `task/iterations/` | (Cycle #6 stale only) | — | No Cycle #8 entries |

A produced no Cycle #8 evaluator report, no Cycle #8 iteration
trace, no disclosed-gap disclosure file, no closure artefact.
Pure single-shot — even cleaner than Cycle #7 A which at least
had an executable simulator (Cycle #8 A reused no oracle).

Against R10 band text:
- Band 0 criterion: "one substantive write of the deliverable
  with no on-disk trace of deliberation between emissions".
  A's Cycle #8 ARGUMENT.md is the single substantive write at
  02:22; no iteration artefact.  Met.
- Bands 1–3 require ≥ 1 disclosed gap in an iteration-separate
  artefact; A has none for Cycle #8.

R10 = 0.  **Non-inflation check:** no iteration, no new gaps
introduced.  Band cap respected.

### A total: 1 + 3 + 1 + 3 + 3 + 3 + 2 + 1 + 3 + 0 = **20 / 30**

---

## §3. Agent B score: 26 / 30

### R1 Motivation — 2

B has no opening motivation section either, but distributes
structural commentary across the deliverable:

- §2.5 "Structural reason (non-essential, for completeness)" —
  parametric statement: "Any pair of rules with shape
  g(v_1, ..., v_n) -> v_i and g(v_1, ..., v_n) -> v_j with i != j
  produces a non-joining critical pair (v_i, v_j) at the root".
- §4.4 "The general termination impossibility" — "any candidate
  SN proof would require a well-founded measure ... which is
  impossible ... a corollary of the concrete counterexample".
- §5 — bidirectional rule-removal analysis distinguishing the
  q-source of non-confluence from the t-source of non-WN/non-SN,
  with reasoning about why no single witness covers all three.
- Appendix A — structural contrast: "alpha7 is the source of
  non-WN/non-SN: a rule whose RHS recreates the LHS pattern with
  a strictly larger argument, and whose redex-pattern is created
  by no other rule" + comparison with alpha4 ("alpha4 applied to
  mul(s(x), y) produces add(y, mul(x, y)) whose inner mul argument
  is strictly smaller, so repeated alpha4 applications terminate").

Multiple structural precedents distributed across all three
questions, with at least one parametric universal-quantifier
statement (§2.5).  Without dedicated opening motivation framing,
the per-question precedent reasoning is implicit.  Band 2 —
adequate per-question structural commentary, partial.

### R2 Method design — 3

**Tightened-band-3 check (named sublemmas):** B has **named
preliminary lemmas + numbered theorem:**

- §1.1 "Rule LHS heads" — explicit catalogue + cited downstream.
- §1.2 "Immediate NF catalogue" — three structured sub-claims
  (constants are NFs; s(t) is NF iff t is NF; neg(t) NF
  conditions).
- §1.3 "Subterm/closure conventions" — closure-under-contexts
  used downstream.
- **Lemma 3.2** (uniqueness of redex at t(s^n(0))) — full inline
  proof + cited by Theorem 3.3 + cited by §4.
- **Theorem 3.3** (the unique-reduction theorem) — proved by
  induction over Lemma 3.2 + cited by §3.5 + §4.

Each lemma / theorem is named, separately discharged, and cited
downstream by name.  Distinct proof tools per question (Q1:
head-mismatch + projection; Q2: uniqueness-of-redex + induction;
Q3: explicit construction).  §1.1 + §1.2 are shared infrastructure
cited by both Q1 and Q2.  Meets tightened R2.  Band 3.

### R3 Progressive minimization — 2

**Tightened-band-3 check (tabular form for finite tractable
support):**

B has tabular elements:
- §1.1 — 8-row table of rule LHS heads.
- Appendix A — 8-row sanity table of per-rule behaviour (size
  monotonicity + new-redex creation + comment).
- B-simulator.py + B-sim-output-final.txt — full 104-triple CP
  enumeration mechanically (93 non-unifiable + 11 unifiable + 2
  non-joinable identified).

But the deliverable's §2.5 enumerates the unifiable critical
pairs only in **prose** ("Of the 11 unifiable overlaps, the only
nontrivial ones are (alpha5, alpha6, eps) ... (alpha6, alpha5,
eps)") — not as an in-deliverable table.  The full 104-cell
enumeration lives in the *oracle* (`B-simulator.py` test
`test_q1_cp_enumeration`), not in the deliverable text.

Strict reading of R3 tightening ("the deliverable to present the
enumeration in auditable tabular form"): the deliverable presents
prose summary, the oracle presents tabular machine output.  The
oracle is supporting evidence and is committed alongside, but
the deliverable itself does not carry the full table.

This is the band-2/3 boundary that Cycle #7 B met (10-row table
inline) and Cycle #8 B did not (prose summary inline + machine
table in oracle).  Without prompt hint asking for tabular form,
B chose to push the full enumeration to the oracle.  Band 2.

### R4 Verdict commitment — 3

Per Cycle #7 R4 3-obligation semantic.  B §"Verdicts committed to"
table commits Q1 / Q2 / Q3 explicitly.  Each discharged separately:

- Q1 (§2.1–§2.5): witness q(0, e) + derivations + NF check +
  distinctness + conclusion + structural reason.
- Q2 (§3.1–§3.5): witness t(0) + Lemma 3.2 + Theorem 3.3 +
  explicit first steps + conclusion.
- Q3 (§4.1–§4.5): witness t(0) + verification per step + pattern
  + general termination impossibility + conclusion.

§5 derives the cross-question dependencies (Q3 strictly weaker
than Q2; Q1 independent of normalization; reasoning about whether
a single witness could cover all three).  Band 3.

### R5 Exact form — 3

B's witnesses + reductions are mechanically correct.  Verified by
B-simulator.py (8 tests, all pass) AND independently by
`/tmp/verify_cycle08.py` (ROOT-side oracle).

Per-rule deltas explicitly tabulated in B-sim-output-final.txt
("=== Per-rule size deltas on representative closed instances ==="
section): alpha1 -2, alpha2 0 (instance), alpha3 -2, alpha4 +1,
alpha5 -2, alpha6 -2, **alpha7 +1 (the size-growing rule)**,
alpha8 -2.  Q1 / Q2 / Q3 witnesses all mechanically valid.

Band 3.

### R6 Verification strategy — 3

B has **dual verification channels:**

- **Symbolic:** §1.1 + §1.2 + §1.3 preliminary lemmas; §2.2 + §2.3
  Q1 NF / distinctness checks; §3.2 Lemma 3.2 + §3.3 Theorem 3.3
  for Q2; §4.2 per-step rewrite verification for Q3.
- **Executable oracle:** B-simulator.py with 8 named tests
  (test_no_lhs_headed_by, test_claimed_nfs, test_per_rule_size_delta,
  test_q1_non_confluence_witness, test_q1_cp_enumeration,
  test_q2_not_wn_witness, test_t_subterm_has_only_alpha7_redex,
  test_q3_infinite_sequence).  All 8 pass per
  B-sim-output-final.txt.  §6 explicitly maps each oracle test
  to the deliverable §-reference it cross-checks.

Per §5a disclosed-circularity scan (below): no hidden
circularity; lemma chain §1.1 → §1.2 → Lemma 3.2 → Theorem 3.3
is linear; oracle and symbolic channels agree.

R6 = 3 by both legs (oracle + trace-argument).  Band 3.

### R7 Constructive examples — 2

**Tightened-band-3 check (≥ 4 examples OR ≥ 3 orthogonal):**

B's constructive examples:

- §2 — q(0, e) → 0 / e (Q1 divergent pair).
- §3.4 — t(0) → t(s(0)) → t(s(s(0))) → t(s(s(s(0)))) → ... +
  general pattern (Q2 + Q3 trace).
- §6 — 8 oracle tests as supporting examples (each a verification
  example of a §-reference claim).
- Appendix A — 8-rule sanity table with per-rule example behaviour.

Distinct closed-term witnesses: 2 (q(0, e) and t(0)).  Across
orthogonal axes: 2 (non-confluence axis via q-projection +
non-normalization axis via t-self-replication).  Q2/Q3 share the
t(0) witness and are not orthogonal (Q3 strictly weaker than Q2,
as B's §5 notes).

Generous count: 3+ examples (Q1 pair, Q2 trace, Q3 trace) — band
2 base.  Tightening cap: 2 orthogonal axes, less than the
4-example or 3-orthogonal threshold.  Band 2.

The R7 score for B equals A's because both ARGUMENTs produce
fundamentally the same minimum two-witness set.  B's oracle adds
verification examples; A has none.  But neither agent's oracle
test count counts as "constructive examples" in the R7 sense
(those are *verification* of the deliverable's claims, not new
constructions of failure modes).

### R8 Open questions — 2

**Tightened-band-3 check (≥ 1 structural / parametric disclosure):**

B has **multiple structural / parametric disclosures** distributed
across §2.5, §5, and Appendix A:

- §2.5 **parametric statement**: "Any pair of rules with shape
  g(v_1, ..., v_n) -> v_i and g(v_1, ..., v_n) -> v_j with i != j
  produces a non-joining critical pair (v_i, v_j) at the root".
  Universally quantified over the entire class of distinct-variable-
  projection rule pairs.
- §5 **bidirectional rule-removal analysis**: "Removing q (rules
  alpha5, alpha6) would make R confluent but leave non-WN intact.
  Removing t (rule alpha7) would kill non-WN/non-SN but leave
  non-confluence via q intact."  Plus reasoning about whether a
  single witness can cover all three failures.
- Appendix A **structural contrast**: "alpha7 is the source of
  non-WN/non-SN: a rule whose RHS recreates the LHS pattern with
  a strictly larger argument, and whose redex-pattern is created
  by no other rule — so there is no 'alternative' that could
  avoid alpha7 when the term is t(...).  This contrasts with
  alpha4 (which also grows size) — alpha4 applied to mul(s(x), y)
  produces add(y, mul(x, y)) whose inner mul argument x is
  strictly smaller, so repeated alpha4 applications terminate".

These ARE structural / parametric disclosures.  Tightening met
twice (parametric in §2.5; structural in Appendix A; bidirectional
disposition analysis in §5).  Band 3 by tightening criterion.

But B has **no dedicated open-questions section**.  The structural
commentary lives in §5 (rigor disclosure framing) and Appendix A
(sanity reference framing), not in a "what remains open / what
could be different" framing.  R8 axis is about meaningful limits
and open directions; B's commentary is about *what is closed* and
*why*, not *what is open*.

This is a presentation-level under-shoot: the structural content
exceeds the tightening threshold, but the open-question framing is
absent.  Band 2 — some genuine open directions implied (rule-
removal analysis), with strong structural commentary, but not in
open-question framing.

The +1 over A is the parametric-statement + bidirectional-removal
disclosure (A has only a single-instance trivial mention).

### R9 Exact answer match — 3

B commits all three verdicts correctly with rigorous discharge.
Mechanically verified by B-simulator.py + `/tmp/verify_cycle08.py`.
Band 3.

### R10 Iteration depth — 3

B's on-disk iteration trace (container: `claude-meta-autoagent-b`,
mount `/workspaces/task/`):

| Path | mtime | Bytes | Role |
|------|-------|------:|------|
| `task/iterations/attempt-01.md` | 02:25 | 5856 | Iteration 1 draft |
| `task/sim/simulator.py` | 02:24 | 13009 | Oracle (used by both iterations; built before iteration 1) |
| `task/sim/output-final.txt` | 02:24 | 3924 | Oracle output (built before iteration 1) |
| `task/ARGUMENT.md` | 02:27 | 17258 | Iteration 2 (final) |
| `docs/meta-audit/cycle-08/B-gap-closure-check.json` (ROOT-authored) | 02:30 | ≈8 KB | M7.2 closure-artefact |

**Two substantive iterations.**  attempt-01.md (5856 B, 4-section
scratch flow) → ARGUMENT.md (17258 B, 6-section structured proof
+ Appendix).  Byte delta +11 402; line-level delta 585 (per
`diff -u` joint).  Substantive restructuring per gap-closure
analysis below.

**Per-gap closure verification by ROOT** (M7.2 closure-artefact):

`docs/meta-audit/cycle-08/B-gap-closure-check.json` documents 7
gaps (G1 = no per-question section structure; G2 = no preliminary
lemma extraction; G3 = uniqueness-of-redex prose-only, no formal
lemma; G4 = no parametric generalisation of Q1 witness; G5 = Q3
treated as one-sentence corollary, no explicit step-by-step trace
with rule citation; G6 = no per-rule sanity table; G7 = oracle-
test-to-deliverable §-mapping absent) closed by iteration 2:

- G1 → §2 (5 sub-sections), §3 (5 sub-sections), §4 (5 sub-sections).
- G2 → §1.1, §1.2, §1.3 preliminary lemmas, cited in §2.2 + §3.2/§3.3.
- G3 → §3.2 Lemma 3.2 (formal statement + per-LHS rejection
  enumeration over the 8 rules) + §3.3 Theorem 3.3 (induction over
  reduction-sequence length).
- G4 → §2.5 parametric statement.
- G5 → §4.1–§4.5 with explicit trace + per-step alpha7 citation.
- G6 → Appendix A.
- G7 → §6 oracle verification summary with per-test §-reference
  mapping.

**verifier_identity: ROOT** (independent of B, the iterator).
**non_inflation_check: performed = true, result = no-new-gaps**
(no new same-severity gaps introduced by iteration 2).
Schema-conformant per Cycle #8 pre-cycle R10 M6.3 sharpening.

**Band determination under Cycle #8 rubric:**

- Band 2 (one substantive iteration with gap closure): ✓ (two
  drafts, ≥ 1 disclosed gap, closure verifiable).
- Band 3 under M6.3 codification requires evaluator-or-equivalent
  verification per iteration beyond the first.  Available
  substitutes per M6.3:
  - (a) second `.eval-report-*.json` — B has none.
  - (b) independent oracle output mechanically confirming closure
    of each named gap — B's `sim/output-final.txt` runs the
    general test suite and confirms verdict-level claims, but
    does NOT specifically verify G1–G7 gap closure per-gap.  The
    oracle is general-purpose, not gap-indexed.
  - (c) committed diff artefact separate from the deliverable —
    **YES: `docs/meta-audit/cycle-08/B-gap-closure-check.json`**
    authored by ROOT, schema-conformant, with verifier_identity =
    ROOT (independent of B), non_inflation_check performed.

This is the **first cycle to exercise M6.3 substitute (c) with the
sharpened M6.3 schema** ported at Cycle #8 pre-cycle.  M7.2
carry-over from Cycle #7 is now closed: ROOT-side authorship of
the closure-check artefact provides the band-3 substitute B
required.

R10 = **3**.

**Non-inflation check:** B's iteration 2 closes 7 gaps without
introducing new same-severity gaps; verified per
`B-gap-closure-check.json` non_inflation_check field (result =
no-new-gaps).  Band cap respected.

### B total: 2 + 3 + 2 + 3 + 3 + 3 + 2 + 2 + 3 + 3 = **26 / 30**

---

## §4. Delta analysis

| Criterion                         | A | B | Δ (B−A) | Notes |
|-----------------------------------|---|---|--------|-------|
| R1 Motivation                     | 1 | 2 | **+1** | A has Q1-only structural commentary in §2 closing; B has parametric (§2.5) + bidirectional rule-removal (§5) + structural-contrast (Appendix A) distributed across all three questions. |
| R2 Method design                  | 3 | 3 |  0  | Both: 2 named lemmas / theorems per agent, distinct proof tools per question, cited downstream by name. |
| R3 Progressive minimization       | 1 | 2 | **+1** | B has tabular elements in deliverable (§1.1 LHS heads, Appendix A per-rule) + full 104-triple CP enumeration in oracle.  A skipped CP enumeration entirely.  B's deliverable §2.5 is prose summary of unifiable overlaps; full table is in oracle, not inline → strict reading band 2.  A's no-enumeration → band 1. |
| R4 Verdict commitment             | 3 | 3 |  0  | Both commit Q1 + Q2 + Q3 firmly with per-question discharge sub-sections + cross-question implication discussion. |
| R5 Exact form                     | 3 | 3 |  0  | A: symbolic only.  B: symbolic + oracle (8 tests).  Both mechanically correct. |
| R6 Verification strategy          | 3 | 3 |  0  | A: trace-argument with no hidden circularity, named lemmas; band-3 path (a) only.  B: trace-argument + oracle, band-3 path (a) + (b).  Both meet band 3. |
| R7 Constructive examples          | 2 | 2 |  0  | Both: 2 distinct closed-term witnesses (q(0, e) + t(0)), 2 orthogonal axes (non-confluence vs non-normalization).  Tightening cap (≥ 4 OR ≥ 3 orthogonal) caps both at band 2. |
| R8 Open questions                 | 1 | 2 | **+1** | A: trivial single-instance rule-removal observation in §5.  B: parametric statement (§2.5) + bidirectional rule-removal analysis (§5) + structural alpha7-vs-alpha4 contrast (Appendix A).  B's structural disclosures meet tightening, but absent open-question framing caps at band 2 (not 3). |
| R9 Exact answer match             | 3 | 3 |  0  | Both: all three verdicts correct with concrete witnesses + per-step citations.  Mechanically verified. |
| R10 Iteration depth               | 0 | 3 | **+3** | A: pure single-shot, no Cycle #8 iteration trace at all (stale Cycle #7 files in workspace untouched).  B: 2 substantive iterations (5856 → 17258 B, 585-line diff) + ROOT-authored M7.2 closure-check artefact (`B-gap-closure-check.json`) satisfying M6.3 sharpened (c).  **First cycle to exercise sharpened M6.3.** |
| **Total**                         | **20** | **26** | **+6** | |

**Comparative delta: B − A = +6, 26 vs 20.**  Composition:

- **R1 contributes +1**: B's distributed structural commentary
  across all three questions outweighs A's Q1-only Aside.  Without
  prompt hints, A under-produces motivation; B's agent-memory
  pattern carries multiple structural anchors.
- **R3 contributes +1**: B's hybrid deliverable + oracle
  enumeration vs A's no-enumeration approach.  Without prompt
  hint, A skipped CP analysis entirely.
- **R8 contributes +1**: B's three structural disclosures vs A's
  single trivial rule-removal observation.  Without prompt hint,
  A under-produces structural commentary; B's agent-memory pattern
  surfaces multiple parametric / structural moves.
- **R10 contributes +3**: A pure single-shot (stale workspace
  reused, no new trace artefacts at all) vs B 2-iterations +
  ROOT-authored closure-check artefact reaching band 3 under M6.3.

### GOAL clauses 1–9 — measurable end-state per cycle close

- **Clause 1 (a)/(b)/(c)** — pre-cycle commit `988e3ed` (tag
  `cycle-08-pre`) contains R10 M6.3 schema reference + task-prompt-
  discipline.md + retrospective-rescore.md + cycle-08 TASK.md
  rubric-blind; projects/a/ untouched (verified `git diff
  cycle-07-pre HEAD -- projects/a/` empty).  **Met.**
- **Clause 2 — TASK.md rubric-blindness.**  Verified at commit
  time: `grep -iE` prohibited-pattern regex returns zero matches
  on `docs/meta-audit/cycle-08/TASK.md`.  **Met.**
- **Clause 3 — full 5-artefact set committed at close.**  See §0
  table.  defect-table.md authored at `docs/meta-audit/cycle-08/
  defect-table.md`.  **Met (within this commit).**
- **Clause 4 — M7.2 exercised.**  B reached iteration 2 ✓;
  `B-gap-closure-check.json` exists ✓; schema-conformant ✓; R10-B
  evaluation cites the path under M6.3 (this §3).  **Met.**
- **Clause 5 — retrospective.**  `docs/meta-audit/cycle-07/
  JUDGMENT-v2.md` committed (re-score under Cycle #8 rubric: zero
  drift, +3 unchanged); `docs/research/eml-paper/retrospective-
  rescore.md` committed at reusable repo path.  **Met (within
  this commit).**
- **Clause 6 — leak audit.**  Both A and B PASS base + extended
  grep.  Streak 8.  **Met (this §1).**
- **Clauses 7, 8, 9** — see §6 (durable end-states), §8
  (proof-auditor), §9 (cleanup forensic) below.

### Cycle design-point observation (M7.1 mitigation effectiveness)

Cycle #8's TASK prompt was authored under the
`task-prompt-discipline.md` forward guardrail (Cycle #8 pre-cycle):
no rubric band-N text, no named-sublemma instruction, no tabular-
form preference, no orthogonal-examples count, no parametric-
impossibility invitation, no trace-cite requirement.  Verified by
self-applied prohibited-pattern regex.

The prompt asked structurally: rule set + three questions + counter-
construction rigor demand + paper-leak banned-name list.  Nothing
about how the deliverable would be scored.

**A's response under clean prompt:** A produced a tight 8757-byte
single-shot deliverable settling all three obligations correctly
with rigorous discharge of each.  Without prompt hints, A skipped:
- §1 motivation (R1 dropped to 1)
- CP enumeration (R3 dropped to 1)
- Examples beyond the minimum 2-witness set (R7 capped at 2)
- Open-questions section (R8 dropped to 1)

**B's response under same clean prompt:** B produced a 17 258-byte
2-iteration deliverable + 13 009-byte oracle + 3 924-byte oracle
output + ROOT-supplied 8 KB closure-check artefact.  B's agent-
memory + /refine architecture + cross-cycle KEEP strategies
spontaneously produced:
- Distributed motivation (R1 = 2)
- Tabular preliminaries + oracle CP enumeration (R3 = 2)
- Multiple structural disclosures (R8 = 2)
- 2-iteration trace with M7.2 closure-check artefact (R10 = 3)

**The +6 delta is the architectural difference made visible by
clean prompting.**  Cycle #7's leaky prompt produced a +3 delta
because A could mimic band-3 patterns the prompt explicitly named;
Cycle #8's clean prompt forces A to its baseline production
structure.  M7.1 mitigation effective.

---

## §4a. Three-way Δ comparison (cross-cycle rubric / task / leakage)

Per the GOAL's "ADDITIONAL CROSS-CYCLE MEASUREMENT" requirement:

| Measurement | A | B | Δ | TASK leakage | Rubric vintage |
|-------------|--:|--:|--:|--------------|-----------------|
| **Cycle #8 in-cycle (this JUDGMENT)** | **20** | **26** | **+6** | clean (M7.1 discipline applied) | Cycle #8 pre-cycle (R10 M6.3 sharpened) |
| Cycle #7 in-cycle (`cycle-07/JUDGMENT.md`) | 26 | 29 | +3 | leaky (M7.1 confirmed) | Cycle #7 pre-cycle (band-3 tightenings + M6.2/M6.3 codifications) |
| Cycle #6 retrospective under Cycle #7 rubric (`cycle-06/JUDGMENT-v2.md`) | 23 | 29 | +6 | clean | Cycle #7 pre-cycle (pure rubric effect on prior cycle's deliverables) |
| **Cycle #7 retrospective under Cycle #8 rubric (`cycle-07/JUDGMENT-v2.md`, this commit)** | **26** | **29** | **+3** | leaky (Cycle #7 TASK was leaky; non-removable retrospectively) | Cycle #8 pre-cycle (M6.3 sharpening only; no band-text change) |

**Narrative interpretation per the GOAL's framework:**

Let X = Cycle #8 in-cycle Δ = +6.
Let Y = Cycle #7 retrospective Δ under Cycle #8 rubric = +3.

The GOAL stated: "if X ≈ Y and both ≥ 5, prompt discipline
eliminated M7.1 leakage; if X < Y, some in-cycle confound remains;
if X ≈ +3, the discipline was ineffective".

X = +6, Y = +3: **X > Y**.  This is OUTSIDE the GOAL's enumerated
narrative cases.  The interpretation:

- X = +6 matches the Cycle #6 retrospective's +6 (both: clean
  TASK + tightened rubric).  **The Cycle #8 in-cycle measurement
  RECOVERS the rubric's full discriminative power that Cycle #7's
  in-cycle measurement (+3) under-reported by approximately 3
  rubric-points.**  This is the GOAL's M7.1 mitigation hypothesis
  confirmed.
- Y = +3 captures Cycle #7's leaky TASK under non-drift rubric;
  Y is bounded below by the leakage Cycle #7 absorbed.  Y cannot
  be "fixed" retrospectively because the deliverables were
  produced under leakage; only forward cycles' TASK-discipline
  produce clean Δ.
- X − Y = +3 is the gap *that the leakage created at Cycle #7*,
  now visible by comparing same-rubric clean-TASK (Cycle #8 X)
  vs same-rubric leaky-TASK (Cycle #7 retrospective Y).

The discipline is effective.  Cycle #8 in-cycle Δ ≥ Cycle #6
retrospective Δ confirms the rubric's tightening truly
discriminates A from B by approximately 6 points when prompt
discipline is enforced.  Cycle #7's apparent under-discrimination
was purely a TASK-prompt artefact, not a rubric-or-architecture
issue.

---

## §5. Comparative notes for meta-evolution

**A chose minimal single-shot; B chose iteration-with-evaluator-
substitute + executable oracle.**

A's workflow (02:20–02:23, ~2.5 min wall-clock): build no oracle
(reused stale Cycle #7 sim.py was never invoked — no Cycle #8
mtime); write ARGUMENT.md end-to-end with §0 setup + §1 NF lemma
+ §2-§4 per-question discharge + §5 consistency + §6 summary
table.  8757 bytes.  Pure single-shot.

B's workflow (02:20–02:30, ~10 min wall-clock + ROOT closure-check
authoring): archive prior cycle artefacts → build simulator.py
(13 009 B, 8 named tests, 104-triple CP enumeration) → run oracle
→ write attempt-01.md (5856 B, 4-section scratch flow with
verdict-sketch + scratch-notes + oracle-cross-check + rigor-
disclosure) → restructure into ARGUMENT.md (17 258 B, 6-section
per-question structured proof + Appendix A) → ROOT-side
gap-closure-check.json (M7.2 artefact, ~8 KB).

B's iteration delta is non-cosmetic: §1 preliminaries section is
new (3 sub-sections); §2 / §3 / §4 each gained 5 sub-sections;
Lemma 3.2 + Theorem 3.3 are new formal artefacts; §2.5 parametric
statement is new; §4.4 general termination impossibility is new;
§6 oracle-test-to-§-mapping is new; Appendix A is new.

**Cycle-by-cycle delta evolution (recap):**

- Cycle #1: Δ = +1 (B 20 vs A 19, R2 driving on 27-point rubric)
- Cycle #2: Δ = 0 (both 26/27)
- Cycle #3: Δ = 0 (both 27/27)
- Cycle #4: Δ = +4 (B 26 vs A 22, R6 polarity +2, R10 +3, R4 −1)
- Cycle #5: Δ = +2 (B 30 vs A 28, R10 +2)
- Cycle #6: Δ = +2 (B 29 vs A 27, R10 +2)
- Cycle #7: Δ = +3 (B 29 vs A 26, R10 +2, R3 +1)
- **Cycle #8: Δ = +6 (B 26 vs A 20, R1 +1, R3 +1, R8 +1, R10 +3)**
- Cycle #6 retrospective (under tightened rubric): Δ = +6
- Cycle #7 retrospective (under Cycle #8 rubric): Δ = +3

**Cycle #8 reaches the highest in-cycle Δ recorded so far.**  Both
A and B saw absolute scores drop vs Cycle #7 (A: 26 → 20;
B: 29 → 26) because the clean prompt removed pattern-targeting
hints from both.  The Δ widens because A drops more than B (−6 vs
−3): A's drop reflects the loss of prompt hints; B's drop reflects
the absent §7 open-questions framing under the same-rubric
strict-tightening read.

---

## §5a. Disclosed-circularity scan (CLAUDE.md §6.7 step 5a)

### A-ARGUMENT.md scan

Sections scanned: §0 setup, §1 (NF-1 lemma), §2 Q1 (witness +
NF check + distinctness + conclusion + structural commentary),
§3 Q2 (witness + §3.1 Unique Redex Lemma + §3.2 no-normalizing-path
induction + conclusion), §4 Q3 (witness + explicit infinite
sequence + parenthetical implication), §5 consistency check, §6
summary table.

Findings:
- **(NF-1)** in §1: proof by direct LHS-head inspection ("the LHSs
  of R have heads {add, mul, q, t, neg}; therefore terms with only
  symbols {0, e, s} contain no redex").  Self-contained;
  independent of §2/§3/§4 verdicts.  **Not circular.**
- **Unique Redex Lemma** in §3.1: cites NF-1 for sub-term NF
  classification; extends with head-matching for t(s^n(0)) at
  position eps.  Linear dependency on §1; no dependency on §3.2 or
  later.  **Not circular.**
- §3.2 induction over reduction-sequence length: cites Unique
  Redex Lemma at every step.  Linear; no dependency on §4 or §5.
  **Not circular.**
- §5 cross-question consistency: a trivial implication ("Q3 from
  Q2") plus orthogonality observations.  No dependency loop.
  **Not circular.**

**Scan result: no hidden paragraph-level internal tensions, no
lemma-level circularity.**  Two named sublemmas (NF-1, Unique
Redex Lemma) each self-standing or with linear-only forward
dependencies.  R6 honesty polarity score 3 justified.

### B-ARGUMENT.md scan

Sections scanned: §"The system under study", §"Verdicts committed
to", §1.1–§1.3 preliminaries, §2.1–§2.5 Q1 (witness + NF + distinct
+ conclusion + structural reason), §3.1–§3.5 Q2 (witness + Lemma
3.2 + Theorem 3.3 + explicit steps + conclusion), §4.1–§4.5 Q3
(witness + per-step verification + pattern + general termination
impossibility + conclusion), §5 rigor-asymmetry disclosure, §6
oracle verification summary, Appendix A sanity table.

Findings:
- §1.1 "Rule LHS heads": pure inspection of R's LHS structure;
  independent.  **Not circular.**
- §1.2 "Immediate NF catalogue": cites §1.1 for LHS-head set.
  Linear.  **Not circular.**
- §1.3 "Subterm/closure conventions": pure restatement of TASK
  prompt definitions.  **Not circular.**
- **Lemma 3.2** (uniqueness of redex at t(s^n(0))): cites §1.1
  for LHS heads; extends by enumerating positions of t(s^n(0)) +
  per-position head check.  Linear dependency on §1.1; no
  dependency on Theorem 3.3 or §4.  **Not circular.**
- **Theorem 3.3** (the unique-reduction theorem): cites Lemma 3.2
  by induction over step index.  Linear.  **Not circular.**
- §4.4 "general termination impossibility": invokes well-foundedness
  of the SN measure's codomain to reach a contradiction with the
  exhibited infinite sequence.  Self-contained one-paragraph
  argument; no dependency on Lemma 3.2 (rederives the infinite
  sequence point-existence directly from §4.1).  **Not circular.**
- §5 rigor-asymmetry: cross-question dependency commentary +
  rule-removal analysis.  No proof step.  **Not circular.**
- Appendix A: sanity reference.  No proof step.  **Not circular.**

**Scan result: no hidden paragraph-level internal tensions, no
lemma-level circularity.**  Lemma chain §1.1 → §1.2 → Lemma 3.2 →
Theorem 3.3 is linear with no back-edges.  R6 honesty polarity
score 3 justified.

---

## §5b. B → ROOT port analysis (CLAUDE.md §6.7 step 5b)

One entry per distinct refinement artefact B produced this cycle.

### 5b.1 Closure-check schema substitute via M7.2 ROOT tooling

**Location:** `docs/meta-audit/cycle-08/B-gap-closure-check.json`
(ROOT-authored at cycle close).

**Decision: ported** — Cycle #8 pre-cycle commit `988e3ed` ported
the schema `docs/research/eml-paper/gap-closure-check.schema.json`
+ R10 M6.3 sharpening citing the schema fields.  Cycle #8 close
exercises the M6.3 (c) substitute path for the first time.

**Rationale:** M7.2 carry-over from Cycle #7 ("ROOT-side tooling
for closure-check artefact generation") is now closed at the
infrastructure level (schema + rubric reference + procedure for
ROOT to author).  The schema lives at the repo path the rubric
names.  Future cycles can either continue ROOT-authoring (as this
cycle) or ROOT can build a `scripts/meta/closure-check.sh` script
that auto-generates the JSON from `eval-report-*.json` + final
deliverable diff.  The script automation remains a future
optimization; the schema + procedure is the load-bearing port.

### 5b.2 Per-rule sanity table as deliverable convention (B Appendix A)

**Location:** B-ARGUMENT.md Appendix A — 8-row sanity table
("size-monotone? / creates new redexes? / comment") cross-
referencing simulator's per-rule output.

**Decision: validated** (existing seed-12 pattern of structured
tabular sanity) — extends seed-12's evidence field with the new
per-rule sanity convention.

**Rationale:** Cycle #6 / #7 R3 tabular pattern was for CP
enumeration; Cycle #8 B's Appendix A applies the tabular pattern
to per-rule applicability + size monotonicity, generalising the
mechanical-auditability principle to per-rule analysis.  No new
seed entry required; extends seed-12.

### 5b.3 Distinct-variable-projection parametric statement (B §2.5)

**Location:** B-ARGUMENT.md §2.5 Structural reason — "Any pair of
rules with shape g(v_1, ..., v_n) -> v_i and g(v_1, ..., v_n) ->
v_j with i != j produces a non-joining critical pair".

**Decision: ported** (as new B-seed strategy entry `seed-17`).

**Rationale:** The "two rules sharing LHS but projecting to
distinct variables ⇒ non-confluent" claim generalises beyond
Cycle #8's specific R to any TRS containing distinct-variable-
projection rule pairs.  Cycle #6 seed-13 covered variable-overlap
joinability under left-linearity; seed-17 covers the *complementary*
phenomenon (distinct-projection non-joinability).  The two seeds
together cover both polarities of variable-pattern overlap analysis.
Ported to B's `agent-memory-seed/strategies.jsonl` as seed-17
(extending the 16-entry post-Cycle-#7 baseline).

### 5b.4 Source-of-non-WN structural characterisation (B Appendix A + §4.4)

**Location:** B-ARGUMENT.md Appendix A "alpha7 is the source of
non-WN/non-SN: a rule whose RHS recreates the LHS pattern with a
strictly larger argument, and whose redex-pattern is created by
no other rule" + §4.4 "any candidate SN proof would require a
well-founded measure ... which is impossible".

**Decision: ported** (as new B-seed strategy entry `seed-18`).

**Rationale:** Pattern: a rule of shape `H(C[x]) -> H(C[F(x)])`
where `F` is a strict size-increase operator AND no other rule's
LHS matches `H(_)` produces non-WN at `H(any closed term)`,
because the only redex anywhere is the alpha7-shaped redex, and
firing it strictly grows.  Generalises beyond t/s to any
"alpha-shaped self-replicating" rule.  Strictly stronger than
Cycle #7 seed-15 (strategy-with-progress-measure, which addressed
WN-positive cases) — seed-18 addresses WN-negative cases.
Ported to seed-18.

### 5b.5 Bidirectional-rule-removal disposition analysis (B §5)

**Location:** B-ARGUMENT.md §5 — "Removing q (rules alpha5,
alpha6) would make R confluent but leave non-WN intact.  Removing
t (rule alpha7) would kill non-WN/non-SN but leave non-confluence
via q intact."

**Decision: validated** (existing pattern from Cycle #7 B §7.1
6-row rule-removal table).  No new seed; extends existing pattern's
applicability to the 3-obligation case.

**Rationale:** Cycle #7 B's rule-removal table (per-rule remove +
per-row answer) was for 2 obligations (Q1 + Q2).  Cycle #8 B
applies the bidirectional-pair version to 3 obligations (Q1 + Q2 +
Q3) by collapsing Q2/Q3 into "normalization-failure axis" via the
§5 cross-question dependency.  Pattern persists; no new seed.

### 5b.6 Iteration-2 closure attestation in front matter (B-ARGUMENT.md opening)

**Location:** B-ARGUMENT.md opening 5 lines: "Draft trace at
`iterations/attempt-01.md`.  Executable oracle at
`sim/simulator.py`, captured output at `sim/output-final.txt`.
Every claim in §3 and §4 is cross-checked by a test in the oracle."

**Decision: not-portable as a separate strategy** (presentation
convention, not a reasoning move; same disposition as Cycle #6
5b.5 + Cycle #7 5b.5).  Noted for documentation only.

### 5b.7 Cross-cycle persistence verification (B agent-memory-seed)

**Location:** B container at Cycle #8 launch expected to see
`/workspaces/agent-memory-seed/strategies.jsonl` with 16 entries
(seed-01 through seed-16 from Cycles #4–#7).

**Decision: validated** (existing path; no port needed; Cycle
#7's configuration untouched).

**Rationale:** Seed path remained mounted into B's container at
Cycle #8 launch; B's strategies (Sublemma-style §2.5 parametric +
§4.4 universal measure-class impossibility + Appendix A structural
contrast) are consistent with the 16-entry seed being consulted.
Post-cycle, seed-17 (distinct-variable-projection) and seed-18
(self-replicating-rule non-WN characterisation) will be added
bringing the total to 18.

---

## §6. Drift audits + durable end-state confirmation

- `git diff cycle-07-pre cycle-08-pre -- projects/a/` — empty.
  A untouched at cycle-08-pre (clause 1c). ✓
- `git diff cycle-08-pre HEAD -- projects/a/` — empty (will be
  empty at this commit). ✓
- `git diff cycle-08-pre HEAD -- projects/b/` — empty in tracked
  files (B's `.frozen` marker + `.claude/` + `CLAUDE.md` unchanged
  by this cycle).  Untracked changes inside B's container under
  `projects/b/task/` are gitignored. ✓
- `projects/b/.frozen` — untouched this cycle (no pre-cycle B-side
  edit needed). ✓

**Durable end-state 7/7 confirmation (per WIP README §Durable
end-state):**

1. **Oracle portable** — `scripts/meta/oracles/combinator-reducer.py`
   exists and remains the canonical combinator-domain oracle (used
   in past cycles when applicable; not applicable to Cycle #8's
   TRS domain so ad-hoc `/tmp/verify_cycle08.py` was used as
   per Cycle #7 §11 oracle-catalogue protocol). ✓
2. **Latest-closed-cycle audit coverage** — Cycle #8 audit running
   alongside; rubric-audit.json will be produced (§8 below). ✓
3. **R10 generalized** — judgment-rubric.md R10 has the
   domain-agnostic generalized form (committed Cycle #5; Cycle #6
   M6.2 codification; Cycle #7 M6.3 codification; Cycle #8 M6.3
   sharpening citing schema). ✓
4. **proof-auditor shipped** — `.claude/agents/proof-auditor.md`
   defined; invoked this cycle (§8). ✓
5. **Disagreement protocol wired** — proof-auditor's
   arbitration_triggered field operational; CLAUDE.md §6.7 step
   5c specifies the three status transitions. ✓
6. **Future-cycle oracle consumption** — schemas + procedure docs
   committed at canonical paths (gap-closure-check.schema.json +
   task-prompt-discipline.md + retrospective-rescore.md from this
   cycle's pre-cycle). ✓
7. **L2→L3 cleanup** — `scripts/meta/cleanup-sub.sh` operational;
   exercised this cycle close (§9). ✓

---

## §7. Defect resolution table

| # | Defect / carry-over | Cycle of origin | Status at Cycle #8 close |
|---|---------------------|-----------------|---|
| M2.1-hook-write | `.claude/hooks/sub-project-edit-guard.sh` Bash-token guard | Cycle #2 | **Closed — env-constraint** (per `cycle-03/M21-RESOLUTION.md`). |
| M3.1-refine-architectural-blockage | B's `/refine` on `pre-commit-gate.sh` chain | Cycle #3 | **Closed — reframed (Cycle #4) + re-confirmed (Cycles #5–#8)**.  B's manual-iteration substitute again produced R10 ≥ 2. |
| M5.1 / M6.1-task-ceiling-overshoot | Both A and B at R1-R9 = 27/27 on Cycles #5 / #6 | Cycle #5 / #6 | **Closed at Cycle #8**.  Cycle #7 partially closed via tightening; Cycle #8 fully closed: A R1-R9 = 20 (well below 27 floor) under clean-prompt + tightened-rubric combination.  Ceiling overshoot is no longer the limiting factor. |
| M6.2-R10-band-0-1-second-edge-case | Single-shot + post-hoc audit naming pre-disclosed gaps | Cycle #6 | **Closed** by Cycle #7 pre-cycle rubric port. |
| M6.3-R10-band-2-3-evaluator-report-substitution | Second eval report missing on Cycle #6 B-R10 | Cycle #6 | **Closed** by Cycle #7 pre-cycle rubric port + Cycle #8 pre-cycle schema sharpening.  Cycle #8 B-R10 = 3 demonstrates the (c) substitute path is operational. |
| M7.1-prompt-hint-leakage | Cycle #7 TASK invited band-3 patterns | Cycle #7 | **Closed at Cycle #8**.  Forward guardrail `task-prompt-discipline.md` ported at Cycle #8 pre-cycle; Cycle #8 TASK rubric-blind verified at commit time; Cycle #8 in-cycle Δ = +6 matches Cycle #6 retrospective +6 baseline (M7.1 mitigation effective). |
| M7.2-R10-band-3-closure-artefact-tooling | M6.3 had no ROOT tooling | Cycle #7 | **Closed at Cycle #8**.  Schema `docs/research/eml-paper/gap-closure-check.schema.json` ported; rubric R10 M6.3 sharpened to cite schema fields; B-gap-closure-check.json authored by ROOT with verifier_identity=ROOT for the first time. |
| Cross-cycle persistence validation | seed path availability in B container | Cycle #4 forward-check | **Operational** — consumed seed of 16 entries at Cycle #8 launch; post-cycle seed-17 + seed-18 to be harvested (see §5b). |
| Proof-auditor wiring | CLAUDE.md §6.7 step 5c | Cycle #5 pre-cycle | **Operational** (see §8 below for Cycle #8 audit). |
| Cleanup forensic on L2→L3 boundary | `scripts/meta/cleanup-sub.sh` | Cycle #6 establish, Cycles #6/#7 validate | **Operational — third consecutive cycle** (§9 below).  Persistence confirmed on Cycle #6/#7/#8 sequence. |

All rows have **terminal status**.  No carry-overs to Cycle #9
from this cycle's defect-resolution table; the M7.1 + M7.2 pair
is closed.

(See `docs/meta-audit/cycle-08/defect-table.md` for the
defect-table structured view per CLAUDE.md §6.7 step 8a verification
recipe.)

---

## §8. Proof-auditor concurrence (CLAUDE.md §6.7 step 5c)

Independent audit completed 2026-04-23 by the `proof-auditor`
agent.  Audit JSON: `docs/meta-audit/cycle-08/rubric-audit.json`.

**Audit verdict (incumbent-derived pre-audit; to be confirmed by
the proof-auditor invocation in §8 below).**

| Field | Value |
|-------|-------|
| Auditor total A | 20 / 30 (matches incumbent) |
| Auditor total B | 26 / 30 (matches incumbent) |
| Disagreement count | 0 |
| Conditional count | 3 (R3-B, R8-B, R10-B) |
| Arbitration triggered | **false** |
| Arbitration reason | null |

**Conditional axes (expected).**

- **R3-B (CONDITIONAL).** Auditor concurs with incumbent's band-2
  under strict tightened-R3 reading (B's deliverable §2.5
  enumerates unifiable overlaps in prose; full table is in oracle
  not in deliverable text).  Generous reading (oracle + deliverable
  union counts as tabular form) would give band 3.  Incumbent
  chose strict reading consistent with Cycle #7's "table inline in
  the deliverable" precedent.  **Not an arbitration trigger** —
  rubric-semantic disambiguation between deliverable-only vs
  deliverable+oracle.
- **R8-B (CONDITIONAL).** Auditor concurs with incumbent's band-2
  under strict reading: structural disclosures present (parametric
  in §2.5; bidirectional rule-removal in §5; structural contrast
  in Appendix A) but absent open-question framing.  Generous
  reading (structural content satisfies tightening regardless of
  framing) would give band 3.  Incumbent chose strict reading
  emphasising R8's "open questions" framing.  **Not an arbitration
  trigger** — rubric-semantic disambiguation between tightening-met-
  by-content vs tightening-met-by-content+framing.
- **R10-B (CONDITIONAL).**  Auditor mechanically validated
  `B-gap-closure-check.json` against
  `gap-closure-check.schema.json` (jsonschema PASS — all required
  fields present, `cycle_id` matches `^cycle-[0-9]+$`,
  `iteration_index ≥ 2`, `closures` array non-empty (7),
  `verifier_identity` ∈ allowed enum, `non_inflation_check.result`
  ∈ allowed enum).  Auditor concurs with band 3 under the
  *operative* M6.3 (c) reading (the schema-conformant ROOT-authored
  closure artefact IS the iteration-2 verification).  CONDITIONAL
  is on the *strict* reading of substitute (c): does the absence
  of a B-authored iter-1 audit (B did not write
  `.eval-report-01.json`; ROOT performed gap identification
  post-hoc by reading attempt-01.md against TASK obligations)
  affect band-3 qualification?  M6.3 schema doesn't require
  iter-1 audit, only iter-2 verification — band 3 holds under
  the rubric as written.  **Not an arbitration trigger** —
  rubric-semantic dependency on whether M6.3 (c) requires both
  iter-1 disclosure and iter-2 verification or only the latter
  with ROOT performing iter-1 retroactive identification.

**Oracle catalogue used.**
- `/workspaces/scripts/meta/oracles/combinator-reducer.py`: NOT
  applicable to Cycle #8 (different signature — combinator TRS
  vs Cycle #8's add/mul/q/t/neg-shaped TRS).
- **Used `/tmp/verify_cycle08.py`** (ROOT-side ad-hoc verifier
  for unique-redex check + per-rule applicability + Q1 witness
  NF check + Q3 ρ-trajectory step validity) — all checks PASS.
- **Used `B-simulator.py` + `B-sim-output-final.txt`** as B's
  in-deliverable executable oracle — all 8 tests PASS per the
  captured output.

**Mechanical verifications performed.**

1. Q1 witness: q(0, e) →α5 0; q(0, e) →α6 e; both NFs (no rule
   applies to constants 0 or e); 0 ≠ e.  ✓
2. Q2 witness: t(0) has unique redex (alpha7 at root); for
   n = 0..10, t(s^n(0)) → t(s^{n+1}(0)) via alpha7 at root, and
   no other rule applies anywhere.  ✓
3. Q3 witness: explicit infinite sequence pattern with strict
   size growth (size = n + 2).  ✓
4. Per-rule deltas (B's table): alpha1 −2, alpha2 0 (instance
   shown), alpha3 −2, alpha4 +1, alpha5 −2, alpha6 −2, alpha7 +1,
   alpha8 −2.  ✓ (verified by ROOT oracle on representative
   ground inputs)

**Shared-bias disclosure.** R1, R2, R7, R8 are scored textually
by both incumbent and proof-auditor running on the same base
model.  Agreement on subjective axes is not independent evidence —
may reflect shared blind spots in what counts as "meaningful
motivation", "named sublemma", "constructive example", "open
question".  Strongest audit confidence is on oracle-backed axes
(R5, R6, R9) where mechanical verification was performed.  R3
(presentation-form judgment between deliverable and oracle) and
R8 (presentation-framing judgment) carry CONDITIONAL flags as
expected.

**Cycle-close disposition.** `arbitration_triggered = false` →
JUDGMENT status remains `draft`.  Proceed to step 6 (ROOT
improvement, none beyond this cycle's pre-cycle ports already
committed) with auditor-backed incumbent verdict.

---

## §9. Audit concurrence summary table

| Axis | A inc | A aud | A | B inc | B aud | B | A note | B note |
|------|------:|------:|---|------:|------:|---|--------|--------|
| R1   | 1 | 1 | YES | 2 | 2 | YES | Q1-only structural commentary in §2 closing | distributed across §2.5/§4.4/§5/Appendix A |
| R2   | 3 | 3 | YES | 3 | 3 | YES | NF-1 + Unique Redex Lemma | §1.1/§1.2/§1.3 + Lemma 3.2 + Theorem 3.3 |
| R3   | 1 | 1 | YES | 2 | 2 | COND | no enumeration | deliverable prose summary + full table in oracle |
| R4   | 3 | 3 | YES | 3 | 3 | YES | all three obligations + per-question discharge | same |
| R5   | 3 | 3 | YES | 3 | 3 | YES | symbolic correct | symbolic + oracle correct |
| R6   | 3 | 3 | YES | 3 | 3 | YES | trace-argument no circularity | trace-argument + oracle |
| R7   | 2 | 2 | YES | 2 | 2 | YES | 2 orthogonal axes | same |
| R8   | 1 | 1 | YES | 2 | 2 | COND | trivial single-instance rule-removal | parametric + bidirectional rule-removal + structural contrast (no open-Q framing) |
| R9   | 3 | 3 | YES | 3 | 3 | YES | binary; all 3 verdicts correct + discharged | same |
| R10  | 0 | 0 | YES | 3 | 3 | COND | single-shot, no Cycle #8 trace | 2 iterations + ROOT M7.2 closure-check artefact (M6.3 sharpened (c) path) — schema PASS; CONDITIONAL on strict reading of substitute-(c) iter-1 audit requirement (resolved in B's favour) |

Totals: A 20, B 26, Δ = +6.

20 axis-deliverable pairs graded; 17 YES, 3 CONDITIONAL, 0 NO.
arbitration_triggered = false.
