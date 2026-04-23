---
status: draft
cycle: 9
domain: confluence-wn-sn-of-trs-with-q-and-t-rules
auditor: proof-auditor
auditor_date: 2026-04-23
arbitration_triggered: false
incumbent_total_A: 23
incumbent_total_B: 25
auditor_total_A: 23
auditor_total_B: 25
agreement: 20_YES_0_CONDITIONAL_0_NO
audit_file: cycle-09/rubric-audit.json
---

# Cycle 09 — JUDGMENT

Grading of `docs/meta-audit/cycle-09/A-ARGUMENT.md` and
`docs/meta-audit/cycle-09/B-ARGUMENT.md` against
`docs/research/eml-paper/judgment-rubric.md` (R1–R10, total 30
points) under the Cycle #9 rubric state — Cycle #7 band-3 tightenings
retained, Cycle #8 R10 M6.3 (c) schema retained, plus the Cycle #9
pre-cycle ports (commit `ba9fb45`):

- **R3 band-3 locus clarification** — deliverable-side tabular
  presentation required for band 3 when the enumeration has finite
  tractable support; oracle-only enumeration maxes at band 2.
- **R8 band-3 labeling clarification** — each disclosure must carry
  an explicit epistemic label (section header, in-text marker, or
  operator-level impossibility framing); dedicated section naming
  not required.
- **R10 M6.3 (c) reproducibility tag** — each band-3 score via
  substitute (c) must record `agent-spontaneous` /
  `scaffolding-assisted` / `not-applicable`.

Front-matter `status` is `draft` at the time of writing; transitions
to `draft` (auditor concurs) / `arbitration-pending` / `arbitrated`
per CLAUDE.md §6.7 step 5c after the proof-auditor pass.

---

## §0. Cycle artefacts (audit record)

Captured at cycle close (2026-04-23 ~13:00 JST).

| Path | mtime (container) | Bytes | sha256 prefix | Role |
|------|-------------------|------:|:-------------:|------|
| `docs/meta-audit/cycle-09/TASK.md` | 12:17 | 8961 | — | Operative TASK prompt (rubric-blind; verified) |
| `docs/meta-audit/cycle-09/A-ARGUMENT.md` | 12:25 | 14086 | 7b06280b00ebccbd | A deliverable (single-shot) |
| `docs/meta-audit/cycle-09/B-ARGUMENT.md` | 12:41 | 16379 | 8a5cd525f66a696b | B deliverable (iteration 2, final) |
| `docs/meta-audit/cycle-09/B-attempt-01.md` | 12:27 | 3286 | 0accac33f05bcc4f | B iteration 1 draft |
| `docs/meta-audit/cycle-09/B-eval-report-01.json` | 12:32 | 11461 | 6e3455a14b2a6410 | B iter-1 evaluator audit (10 gaps G1–G10) |
| `docs/meta-audit/cycle-09/B-eval-report-final.json` | 12:41 | 11950 | 5d9a0582700d421c | B iter-2 evaluator audit (gap_closure per-gap + 2 LOW new-issues) |
| `docs/meta-audit/cycle-09/B-simulator.py` | 12:26 | 13773 | — | B executable oracle |
| `docs/meta-audit/cycle-09/B-sim-output-final.txt` | 12:26 | 3359 | — | B oracle output (all assertions pass) |

**Execution timing (container wall-clock, UTC+09:00).**

- A launched pre-cycle (~12:20 JST); ARGUMENT.md written 12:25
  (single substantive write). No `iterations/` or `attempts/`
  updated this cycle; A's working directory still carries stale
  Cycle #7/#8 files (`sim.py`, `sim_output.txt`, `attempts/`,
  `iterations/` dated Apr 22), untouched. **Single-shot deliverable.**
  No Cycle #9 evaluator report; no iteration trace.
- B launched pre-cycle; `sim/simulator.py` at 12:26:30 (oracle
  built first); `sim/output-final.txt` at 12:26:33 (oracle
  captured); `iterations/attempt-01.md` at 12:27:32 (iteration 1
  draft, 3286 B); `iterations/.eval-report-01.json` at 12:32:08
  (iter-1 evaluator audit, weighted_score 0.7125, 10 gaps G1–G10,
  `ready_for_finalization: false`); `iterations/.eval-report-final.json`
  at 12:41:04 (iter-2 evaluator audit, weighted_score 0.96, per-gap
  `gap_closure.{G1..G10}.status="closed"`, 2 LOW `new_issues`
  [N1, N2], `ready_to_ship: true`); `task/ARGUMENT.md` at 12:41:54
  (iteration 2 final, 16379 B). **Two substantive iterations with
  evaluator reports per iteration.**

B's byte-size delta (`attempt-01 = 3286` B vs `ARGUMENT = 16379` B,
Δ = +13 093 bytes) reflects substantive restructuring: 3-section
scratch flow → 5-section structured argument with §3 split into
eight sub-sections (§3.1–§3.8) plus a §5 rigor-parity disclosure
and five in-line `> Oracle cross-check` blocks.

**Oracle-backed mechanical verification (independent ROOT oracle).**
`/tmp/verify_cycle09.py` implements R's rewrite rules and weight
measures from scratch and probes:

- Q1: `m(c, d) ->_{rho3} c` and `m(c, d) ->_{rho4} d`; both NF;
  distinct. ✓
- Q2: A's weight `w` and B's weight `[·]` each strictly decrease
  under every non-rho6 rule across 500 random closed substitutions
  (3000 assertions per measure, all pass) and strictly increase
  under rho6 across 200 samples (all pass, both measures).
- Q3: `t_n = f^{n+1}(c)` reduces via rho6 at the root to
  `t_{n+1} = f^{n+2}(c)` for `n = 0..7`; sizes 2..10 match both
  A §4 and B §4.

All mechanical claims in both deliverables verified under this
oracle.

---

## §1. Leak audit

Base `scripts/meta/paper-leak-audit.sh` (paper-identifier keyword
set):

- A: `[Paper-leak audit passed] docs/meta-audit/cycle-09/A-ARGUMENT.md`
- B: `[Paper-leak audit passed] docs/meta-audit/cycle-09/B-ARGUMENT.md`

TASK §1 extended banned-identifier grep (34 names total,
enumerated in TASK.md §1 constraints):

- A: no matches.
- B: no matches (confirmed additionally by B's own iter-final audit
  `banned_identifier_hits: []`).

**Both PASS on all leak scans.** Cycles #1–#9 leak streak: **9**.

---

## §2. Agent A score: 23 / 30

### R1 Motivation — 2

A distributes structural / precedent commentary across all three
questions rather than opening with a dedicated motivation section:

- §2 "Structural remark" (Q1): the (rho3, rho4) pair is the source
  of non-confluence because both rules share the LHS `m(x, y)` with
  projection RHSs that cannot be joined once committed; **parametric**
  generalisation: "Any two syntactically distinct closed normal forms
  `n1, n2` plugged in as `m(n1, n2)` would serve as a witness;
  `m(c, d)` is the minimal one." Universally quantified over the
  distinct-NF-pair witness class.
- §3 "Remark on the structure of the argument" (Q2): rho6 is the
  only expansive rule; rho5/rho6 LHS-sharing lets the strategy
  "decline rho6 and use rho5 on the same position" trade divergent
  expansion for convergent contraction — structural reason for why
  WN survives despite rho6.
- §5 "Consistency check of the three verdicts" (cross-Q): WN vs SN
  relationship; confluence/normalization independence; **bidirectional
  rule-removal analysis**: "Removing rho6 would restore SN ... but
  would not restore confluence. Removing one of rho3, rho4 would
  restore confluence at that source ... but would not restore SN."

Three questions each get structural commentary; at least one
parametric universal quantifier (§2 remark). No opening motivation
section per se. Band 2 — adequate distributed per-question
structural commentary with parametric content; not opening-framed.

### R2 Method design — 3

**Tightened band-3 check (named sublemmas under distinct tools).**
A has four named sublemmas:

- **(NF-1)** in §1 — "A ground term built only from `0`, `c`, `d`,
  `s` is a normal form" + proof by LHS-head inspection.
- **Monotonicity Lemma** in §3.2 — "If `s -> s'` ... and `w(s) >
  w(s')`, then `w(C[s]) > w(C[s'])`" + proof by induction on
  context depth.
- **Strict-Decrease Lemma (non-rho6)** in §3.3 — per-rule symbolic
  difference calculation for rho1..rho7 combined with Monotonicity
  Lemma.
- **Feasibility Lemma** in §3.4 — "Every non-normal-form ground
  term has a non-rho6 redex" + proof by the rho5/rho6 LHS-sharing
  argument.

Each is named, separately proved, and cited downstream by name
(Monotonicity Lemma cited in Strict-Decrease Lemma; Feasibility +
Strict-Decrease cited in "Termination of S"; NF-1 cited in §2
non-confluence argument). Distinct proof tools per question —
Q1: head-mismatch; Q2: weight + monotonicity + feasibility; Q3:
explicit construction. Meets tightened R2. Band 3.

### R3 Progressive minimization — 2

**Tightened band-3 check (deliverable-side tabular enumeration).**
A's per-rule strict-decrease enumeration (§3.3) is **bulleted prose**
with seven bullets (one per rule), each giving the LHS/RHS/difference
calculation in inline arithmetic. The enumeration is present,
complete, and per-rule disposed — but not in markdown-table form.
§1's per-head redex analysis is also bulleted prose (five bullets).
§6 has a 4-row summary table but it summarises witnesses, not the
per-rule enumeration.

Under Cycle #9 R3 locus clarification: deliverable-side tabular
presentation with per-row disposition is required for band 3 when
the support is finite and tractable. A's prose enumeration covers
the support exactly but is not a table. Band 2.

No CP enumeration is presented by A in any form (A does not
enumerate overlaps, since Q1 is dispatched by a single witness at
root; for this cycle's task that is acceptable but leaves R3 only
the per-rule rewrite enumeration as the finite-support candidate,
which is prose).

### R4 Verdict commitment — 3

Per Cycle #7 R4 3-obligation semantic (retained in Cycle #8 and
#9): band 3 = firm commitments on all three obligations AND each
discharged rigorously. A §0 "Verdicts" table commits Q1 NOT
confluent + Q2 IS WN + Q3 NOT SN. Per-obligation discharge:

- Q1 (§2): witness `m(c, d)` + both rho3 and rho4 derivations +
  NF check via (NF-1) + distinctness + "no common reduct"
  argument + conclusion.
- Q2 (§3.1–§3.4): weight `w` definition + Monotonicity Lemma +
  per-rule strict decrease + Strict-Decrease Lemma + Strategy S +
  Feasibility Lemma + Termination argument.
- Q3 (§4): witness `t_0 = f(c)` + explicit infinite sequence
  `t_n -> t_{n+1}` via rho6 at root + per-step rule citation +
  size-count argument for distinctness.

§5 cross-question implication + orthogonality analysis. Band 3.

### R5 Exact form — 3

A's witnesses and reductions are mechanically correct. Verified
by ROOT oracle `/tmp/verify_cycle09.py`:

- Q1: `m(c, d) -> c` via rho3; `m(c, d) -> d` via rho4; both NF;
  distinct. ✓
- Q2: weight `w` decreases under rho1..rho5, rho7 on 3000 random
  samples (0 failures); increases under rho6 on 200 samples
  (200/200 strictly increase). ✓
- Q3: `t_n = f^{n+1}(c)` sizes 2..10 for `n = 0..8`, each reduces
  to `t_{n+1}` via rho6 at root. ✓

Per-rule symbolic calculations in §3.3 (e.g., rho2: `X*Y + X + Y
+ 2 - (X*Y + X + 2) = Y ≥ 1`) are arithmetically correct.
Band 3.

### R6 Verification strategy — 3

A's verification is purely symbolic (no executable oracle).

**Pre-scoring disclosed-circularity scan (CLAUDE.md §6.7 step 5a):**

- (NF-1) — self-contained; proof is by inspection of the LHS-head
  list. No back-edge. ✓
- Monotonicity Lemma — proof is by induction on context depth
  using argument-wise strict monotonicity of `s, u, f, g, m`
  (each proved by differentiating the weight polynomial). No
  back-edge. ✓
- Strict-Decrease Lemma — cites Monotonicity Lemma + the seven
  per-rule symbolic calculations (self-contained arithmetic). No
  back-edge. ✓
- Feasibility Lemma — cites the rho5/rho6 LHS-sharing observation
  (identity of `f(x)` LHS across both rules). Self-contained. ✓
- Termination of S — cites Feasibility + Strict-Decrease + the
  well-foundedness of `N+` (direct statement, not a cited
  theorem). Linear.
- §5 consistency check — trivial cross-question implication, no
  dependency loop.

**Scan found no paragraph-level internal tensions; sections
scanned: §1, §2, §3.1, §3.2, §3.3, §3.4, §4, §5, §6.** Lemma
chain (NF-1) → Monotonicity → Strict-Decrease → Feasibility →
Termination is linear with no back-edge. Under R6 honesty-polarity
(disclosed-gap-2 > hidden-circularity-1): A has no disclosed gap
and no hidden circularity.

R6 band 3 indicator: "numerical sieve combined with algebraic
argument" or "constructive bootstrap with no disclosed gap
remaining". A's trace-argument path has no disclosed gap and no
hidden circularity. Band 3 by trace-argument (path (a)); oracle
is "in addition to" not required for band 3. Band 3.

### R7 Constructive examples — 2

**Tightened band-3 check (≥ 4 examples OR ≥ 3 orthogonal modes).**

A's constructive examples:

- §2: `m(c, d) -> c` via rho3; `m(c, d) -> d` via rho4 (Q1
  divergent-pair witness, 2 derivations on 1 closed term).
- §3.3: 7 per-rule symbolic strict-decrease calculations (one per
  rule) — verification examples, not constructions.
- §4: `t_0 = f(c)` + explicit `t_n -> t_{n+1}` sequence (Q3
  non-SN witness, 1 closed term).

Distinct closed-term witnesses: **2** (`m(c, d)` and `f(c)`).
Orthogonal failure-mode axes: **2** (non-confluence via (rho3,
rho4) projection conflict + non-SN via rho6 expansion).

Q2 is a positive verdict proved by a measure + strategy, not by a
divergent or failing witness, so it does not contribute a third
orthogonal failure-mode axis. The per-rule symbolic decreases in
§3.3 are verification examples, not constructive examples in the
R7 sense.

Generous count: 3 examples (Q1 pair, Q2 strategy demonstration via
rule enumeration, Q3 sequence) — band 2 base. Tightening cap: 2
orthogonal axes < 3-orthogonal threshold and ≠ 4 distinct examples.
Band 2.

### R8 Open questions — 2

**Cycle #9 R8 labeling clarification check** (≥ 3 distinct
disclosures, ≥ 1 structural/parametric, each explicitly labeled).

A's disclosures:

- §2 "Structural remark" — parametric universal statement about
  `m(n1, n2)` witness generation. Content: structural/parametric ✓;
  label: "*Structural remark.*" — a structural-observation label,
  not an open-question / limitation / impossibility label.
- §3 "Remark on the structure of the argument" — structural reason
  rho6 does not threaten WN (rho5/rho6 LHS sharing). Content:
  structural ✓; label: "*Remark on the structure of the argument.*"
  — again structural-observation, not open-question labeled.
- §5 "Consistency check of the three verdicts" — bidirectional
  rule-removal disclosing which rule sources which defect. Content:
  structural ✓; label: "Consistency check" — method-check label,
  not open-question / limitation / impossibility label.

**3 disclosures, ≥ 1 structural/parametric present, but none
carries an explicit epistemic (open-question / limitation /
impossibility) label.** Under the Cycle #9 labeling clarification:
"Band 2 covers structural / parametric content present but
unlabeled (embedded in the proof body or sanity appendix without
epistemic framing)."

A meets band 2 precisely: structural content present across three
questions, but no disclosure carries an open-question or
impossibility label. A does not propose forward-looking open
directions ("what happens if rho6's size-growth is bounded?",
"does relaxing projection rules restore confluence under some
equational theory?", etc.). Band 2.

The Cycle #9 labeling clarification **does not** require a
dedicated "Open Questions" section, but it does require the
disclosure itself to be labeled epistemically; A's structural
remarks are labeled but as structural observations, not as open /
limit / impossibility — hence band 2, not band 3.

### R9 Exact answer match — 3

R9 for Cycle #9 (3-obligation semantic inherited from Cycle #7/#8):
3 iff correct verdicts on **all three** of Q1/Q2/Q3 with rigorous
discharge.

A commits:

- Q1: NOT confluent — witness `m(c, d)`, distinct NF reducts `c`,
  `d`. ✓
- Q2: IS WN — strategy S avoids rho6; weight `w` strictly
  decreases under non-rho6 rules. ✓ (Oracle confirms 3000/3000
  random samples.)
- Q3: NOT SN — witness `f(c)`, rho6-at-root sequence
  `f^{n+1}(c) -> f^{n+2}(c)`. ✓

All three correct; discharge rigorous per R4/R5/R6. Band 3.

### R10 Iteration depth — 0

**A's Cycle #9 on-disk artefacts** (container `claude-meta-autoagent-a`,
mount `/workspaces/task/`, captured 12:25 snapshot):

| Path | mtime | Bytes | Role |
|------|-------|------:|------|
| `task/ARGUMENT.md` | Apr 23 12:25 | 14086 | Single substantive write |
| `task/sim.py` | Apr 22 17:34 | 11024 | **Stale Cycle #7/#8 file**, untouched |
| `task/sim_output.txt` | Apr 22 17:34 | 4765 | **Stale Cycle #7/#8 file**, untouched |
| `task/attempts/` | (Cycle #7 stale only) | — | No Cycle #9 entries |
| `task/iterations/` | (Cycle #6 stale only) | — | No Cycle #9 entries |

A produced no Cycle #9 evaluator report, no Cycle #9 iteration
trace, no disclosed-gap disclosure file, no closure artefact. Pure
single-shot (matches A's Cycle #8 and Cycle #7 pattern; the
architecture has no `/refine`, no evaluator agent).

Against R10 band text:

- Band 0 criterion: "one substantive write of the deliverable with
  no on-disk trace of deliberation between emissions." A's
  Cycle #9 ARGUMENT.md is the single substantive write at 12:25;
  no iteration artefact. **Met.**
- Bands 1–3 require ≥ 1 disclosed gap in an iteration-separate
  artefact; A has none for Cycle #9.
- M6.2 pre-disclosed-gap-audit edge case does not apply (no audit
  artefact exists, not even post-hoc).

R10 = **0**. **Non-inflation check:** no iteration, no new gaps
introduced. Band cap respected.

### A total: 2 + 3 + 2 + 3 + 3 + 3 + 2 + 2 + 3 + 0 = **23 / 30**

---

## §3. Agent B score: 25 / 30

### R1 Motivation — 1

B's motivation apparatus is method-oriented rather than
structural-precedent oriented:

- Opening iteration-trace note (lines 3–7) announces the
  evaluator-audit + gap-closure pattern — this is **method
  announcement**, not motivation.
- Opening oracle note (lines 8–15) announces the simulator's
  role and what it mechanically verifies — also method
  announcement.
- §2 "What we refute" opens with the confluence definition being
  negated — **definition-giving**, not structural motivation.
- §3 opens with "Claim" + "Proof outline" — proof plan, not
  motivation.
- §4 "What we refute" — definition.
- §5 "Rigor parity disclosure" — meta-commentary about method
  parity across Q1/Q2/Q3, not structural motivation.

B does not carry per-question structural-source commentary
comparable to A's §2 structural remark, §3 structural remark, or §5
bidirectional rule-removal. B's deliverable is methodologically
tight (every claim has an oracle cross-check) but has no
"why (rho3, rho4) is the source" or "why rho6 is expansive where
rho5 is not" structural commentary inline. B's §5 parity
disclosure is the closest thing, and it concerns proof-length
structure ("Q2 is longest because universal-statement; Q1/Q3 are
existential") rather than structural precedent.

**Implicit per-question motivation only, and only via definition-
giving intros.** Band 1.

**Delta note.** This reverses the Cycle #8 R1 ordering (R1-A = 1,
R1-B = 2). In Cycle #9, A stepped up its structural commentary
(parametric statements in §2, structural reason in §3 remark,
cross-Q bidirectional analysis in §5) while B flattened its
motivation layer in favour of a method-announcement opening.
Cycle #9 A-R1 > B-R1 is a cycle-specific inversion, not a rubric
drift.

### R2 Method design — 3

**Tightened band-3 check (named sublemmas under distinct tools).**
B has:

- §1 (inside the §3.3 definition block): W totality proved by case
  exhaustion — not a named lemma per se but a cited structural
  statement.
- **Lemma (strict monotonicity of W under each symbol)** in §3.5 —
  full statement + proof sketch by arity-by-arity coefficient
  enumeration. Named lemma.
- §3.5 "Claim" — strict decrease under closed one-hole contexts;
  proved by induction on context structure with base case C = Hole
  and inductive step `C = phi(t_1, ..., C'[-], ..., t_k)`.

B has **one named lemma** explicitly (the monotonicity lemma) + a
named "Claim" + inline "Proof by induction on the structure of
C[-]". Distinct proof tools per question — Q1: head-symbol
equality + confluence-definition refutation; Q2: weight + context
closure induction + well-foundedness + totality-of-S; Q3: explicit
construction with `body_n` recurrence.

A has four named sublemmas where B has one; however B's §3.5 is
genuinely a named sublemma discharged separately, and §3's eight
sub-sections (§3.1–§3.8) each discharge a sub-obligation. The
Cycle #7 R2 tightening requires named sublemma separation; B
satisfies this for the monotonicity lemma and structurally
separates the other obligations by §-numbering with explicit
content-labels.

Both A and B meet the tightened R2. Band 3. (A's four-named-lemma
count is denser than B's one-named-lemma + §-structure; this
difference is visible on R2 scoring but both land at band 3 —
within-band strength asymmetry is not reflected in the 0-3 band.)

### R3 Progressive minimization — 3

**Tightened band-3 check (deliverable-side tabular enumeration
for finite tractable support).**

B's §3.4 "Strict decrease at the top level" presents the per-rule
enumeration as an **explicit markdown table**:

```
| rule    | `[LHS * sigma]`           | `[RHS * sigma]`         | diff          |
|---------|---------------------------|-------------------------|---------------|
| rho1    | `1 + 2*1 + b  = 3 + b`    | `b`                     | `3`           |
| rho2    | `1 + 2*(1+a) + b = 3+2a+b`| `1 + (1+2a+b) = 2+2a+b` | `1`           |
| rho3    | `1 + a + b`               | `a`                     | `1 + b`       |
| rho4    | `1 + a + b`               | `b`                     | `1 + a`       |
| rho5    | `1 + a`                   | `a`                     | `1`           |
| rho6    | `1 + a`                   | `1 + (1+a) = 2 + a`     | `-1`          |
| rho7    | `1 + (1+a) = 2 + a`       | `a`                     | `2`           |
```

Seven rows (one per rule), four columns (rule, [LHS], [RHS], diff
= disposition). Per-row disposition explicit. Supplementary
oracle verification: sim/output-final.txt "500 random closed
substitutions per non-rho6 rule and assert `[LHS] > [RHS]` on each;
all 3000 assertions pass ... 200 random substitutions for rho6
and asserts `[LHS] < [RHS]`; all 200 pass."

Under Cycle #9 R3 locus clarification: "when the enumeration has
finite, tractable support, band 3 requires deliverable-side
tabular presentation — one row per element of the support with an
explicit disposition column, inside the ARGUMENT.md text." B's
§3.4 meets this verbatim. Plus the "combined pattern — deliverable
table + committed oracle output + cross-checkable rows — is the
strongest band-3 shape": B exhibits the deliverable table + oracle
output + row-by-row cross-checkability (each diff sign has a
simulator assertion covering it).

Band 3.

**Delta note.** Cycle #8 B had oracle-only enumeration (§2.5
prose summary of unifiable CPs + simulator holding the full
104-triple enumeration) and was capped at band 2. Cycle #9 B has
lifted the enumeration into the deliverable (§3.4 markdown table
of 7 rules, diff signs + supplementary oracle). The Cycle #9
locus clarification formalised this distinction one cycle after
it surfaced.

### R4 Verdict commitment — 3

Per Cycle #7 R4 3-obligation semantic. B §1 "Verdicts" table
commits Q1 NOT confluent + Q2 Weakly normalizing + Q3 NOT
strongly normalizing. Per-obligation discharge:

- Q1 (§2): definition + witness `m(c, d)` + both rho3 and rho4
  reductions + head-symbol-equality NF check + distinctness +
  "No common reduct" paragraph + Oracle cross-check + conclusion.
- Q2 (§3.1–§3.8): strategy S + totality lemma + weight W defn +
  per-rule diff table + context closure induction + well-
  foundedness + halting at NFs + assembly + Oracle cross-check.
- Q3 (§4): construction with `body_n = f^n(c)` recurrence +
  per-step rho6 reduction + first 5 concrete steps + size argument
  + Oracle cross-check.

§5 "Rigor parity disclosure" explicitly walks the five shared
structural elements (definitions, witness/strategy, rule
citations, internal verifications, oracle) across all three Qs.
Band 3.

### R5 Exact form — 3

B's witnesses + reductions are mechanically correct. Verified
independently:

- B's own simulator (`B-simulator.py`, 8 assertions, all pass per
  `B-sim-output-final.txt`).
- ROOT's `/tmp/verify_cycle09.py` under both A's and B's weight
  measures (3000 non-rho6 assertions + 200 rho6 assertions + Q3
  chain n=0..7 + Q1 witness), all pass.

B's §3.4 per-rule symbolic diffs match the simulator's random-
sample verification. B's §4 `t_n = f(body_n) = f^{n+1}(c)`
recurrence is arithmetically consistent (body_{n+1} = f(body_n),
so f(f(body_n)) = f(body_{n+1}) = t_{n+1}).

Band 3.

### R6 Verification strategy — 3

B has **dual verification channels**:

- **Symbolic / trace-argument**: §0 definitions, §2 head-symbol
  equality argument, §3.1–§3.8 the full WN proof chain, §4 the
  body_n recurrence argument.
- **Executable oracle**: `B-simulator.py` with assertions covering
  Q1 witness (head-scan NF check), per-rule measure decrease
  (500-sample × 6 non-rho6 rules + 200-sample rho6), Q2 strategy
  termination (12 sample closed terms with weight-monotonicity
  assertions), Q3 chain `step(t_n, (), "rho6") == t_{n+1}` for
  n = 0..7.

**Pre-scoring disclosed-circularity scan:**

- §0 definitions — primitive, no back-edge.
- §2 head-symbol equality argument — self-contained.
- §3.3 W totality — case exhaustion over Sigma, no back-edge.
- §3.4 per-rule diff table — arithmetic, each row independent.
- §3.5 monotonicity lemma → §3.5 context closure Claim → §3.6
  well-foundedness → §3.7 halting → §3.8 conclusion — linear
  dependency chain, no back-edge.
- §4 body_n recurrence — primitive definition, no back-edge.

**Scan found no paragraph-level internal tensions; sections
scanned: §0, §1, §2, §3.1–§3.8, §4, §5.** Under R6 honesty
polarity: B has no disclosed gap and no hidden circularity.

R6 band 3 indicator: oracle + trace-argument path with no
disclosed gap. B meets both legs. Band 3.

### R7 Constructive examples — 2

**Tightened band-3 check (≥ 4 examples OR ≥ 3 orthogonal modes).**

B's constructive examples:

- §2: `m(c, d) -> c` via rho3; `m(c, d) -> d` via rho4 (Q1
  divergent pair).
- §3.4: 7-row per-rule diff table + oracle's 3000 random
  substitutions (verification, not construction).
- §4: `t_0 = f(c)` + `t_0..t_8` explicit enumeration with sizes
  2..10 (Q3 non-SN witness + first 9 steps).
- Oracle §3 strategy-samples (12 sample closed terms with
  termination assertions) — verification, not construction.

Distinct closed-term failure-mode witnesses: **2** (`m(c, d)` and
`f(c)`). Orthogonal failure-mode axes: **2** (non-confluence axis
via (rho3, rho4) projection + non-SN axis via rho6 expansion).

Q2 positive verdict + its measure + 12 sample runs are verification
examples (of the strategy's termination), not constructions of new
failure modes. Oracle tests are also verification, not construction.

Band-3 threshold (≥ 4 distinct examples or ≥ 3 orthogonal axes)
not met. Generous count: 3 (Q1 pair, Q2 table+samples, Q3 chain) —
band 2 base; tightening cap at 2 orthogonal axes. Band 2.

B's oracle adds richer verification than A has, but R7 measures
deliverable constructions, not oracle assertions. R7-B = R7-A = 2,
same as Cycle #8.

### R8 Open questions — 1

**Cycle #9 R8 labeling clarification check.**

B's only labeled disclosure-like sentence is in §5 "Rigor parity
disclosure":

> "Q2 contains the longest argument because it must settle a
> universal statement (every closed term, some reduction to normal
> form), whereas Q1 and Q3 settle existential claims ... That is an
> irreducible structural asymmetry — not an asymmetry in effort."

This is **one labeled observation** — "irreducible structural
asymmetry" is an impossibility-labeled phrase, qualifying under
the Cycle #9 labeling rules — but:

- it concerns method / proof-length parity, not the underlying
  TRS's reasoning structure;
- it is a single disclosure (< 3 required for band 3);
- it is not an "open question" in the forward-looking sense.

B has no other labeled disclosure. B does **not** carry:

- a parametric-impossibility statement about the rule class (A's §2
  remark for Q1 witnesses is closer to this);
- a structural-source analysis per question (A's §3 and §5 are
  closer);
- a forward-looking open-direction section.

Under Cycle #9 R8 labeling clarification: band 1 covers "trivial
observations only." B's §5 asymmetry remark is a single,
methodologically-scoped disclosure — not trivial in content but
methodological rather than substantive. Compared to A's unlabeled
structural content (which maps to band 2 under Cycle #9 labeling
rules), B's single labeled methodological observation is band 1.

Band 1.

**Delta note.** This reverses the Cycle #8 R8 ordering (R8-A = 1,
R8-B = 2). In Cycle #8, B had distributed unlabeled structural
content (§2.5 parametric + §5 bidirectional + Appendix A
structural contrast) that was counted at band 2 under the
pre-clarification R8 text. In Cycle #9, B's deliverable flattened
out this structural-commentary layer — most of B's writing went
into the rigor / oracle / WN-proof chain, leaving R8 essentially
unserviced. A meanwhile retained distributed structural commentary.
The inversion R8-A > R8-B is a cycle-specific deliverable-shape
fact, not a rubric drift.

### R9 Exact answer match — 3

Q1: NOT confluent — `m(c, d)` witness ✓; Q2: WN — S + W proof ✓
(oracle + ROOT oracle confirm); Q3: NOT SN — `f(c)` chain ✓. All
three correct with rigorous discharge. Band 3.

### R10 Iteration depth — 3

**B's on-disk iteration trace** (container `claude-meta-autoagent-b`,
mount `/workspaces/task/`):

| Path | mtime | Bytes | sha256 prefix | Role |
|------|-------|------:|:-------------:|------|
| `task/sim/simulator.py` | Apr 23 12:26:30 | 13773 | — | Oracle (built pre-iter-1) |
| `task/sim/output-final.txt` | Apr 23 12:26:33 | 3359 | — | Oracle output (built pre-iter-1) |
| `task/iterations/attempt-01.md` | Apr 23 12:27:32 | 3286 | 0accac33f05bcc4f | Iteration 1 draft |
| `task/iterations/.eval-report-01.json` | Apr 23 12:32:08 | 11461 | 6e3455a14b2a6410 | Evaluator audit of iter-1 (10 gaps G1–G10) |
| `task/iterations/.eval-report-final.json` | Apr 23 12:41:04 | 11950 | 5d9a0582700d421c | Evaluator audit of iter-2 (gap_closure + 2 LOW new_issues) |
| `task/ARGUMENT.md` | Apr 23 12:41:54 | 16379 | 8a5cd525f66a696b | Iteration 2 (final) |

**Two substantive iterations** (attempt-01.md = 3286 B → ARGUMENT.md
= 16379 B; Δ = +13 093 bytes; ~5× expansion). Structural
restructuring: 3-section scratch → 5-section with §3 split into
eight sub-sections + §5 rigor-parity + five in-line oracle cross-
check blocks.

**Per-gap closure verification by evaluator reports (M6.3 (a) native
path):**

`B-eval-report-01.json` names 10 gaps (2 HIGH, 5 MEDIUM, 3 LOW):

- **HIGH: G1** — Q3 recurrence bug: `t_n -> f(f(t_n)) = t_{n+1}`
  arithmetically wrong (actually `f(f(t_n)) = f^{n+3}(c) = t_{n+2}`,
  not `t_{n+1}`). Oracle-verified by simulator.
- **HIGH: G2** — Oracle-silence: zero simulator references in
  attempt-01.md.
- **MEDIUM: G3** — Context closure of W's strict decrease asserted
  but not inductively proved.
- **MEDIUM: G4** — Well-foundedness of `(Z_{>0}, <)` implicit only.
- **MEDIUM: G5** — Pathological-case rho5/rho6 LHS-sharing
  argument too compact.
- **MEDIUM: G6** — NF argument imprecise ("nullary constant"
  phrasing).
- **MEDIUM: G7** — Confluence definition not stated before
  refutation.
- **LOW: G8** — W domain ClosedTerms(Sigma) -> Z_{>0} not
  explicitly typed.
- **LOW: G9** — Q3 simulator citation missing.
- **LOW: G10** — Rigor-parity paragraph absent.

`B-eval-report-final.json` gap_closure block verifies each of
G1–G10 as `"status": "closed"` with specific § references:

- G1 → §4 `body_n = f^n(c)` framing replaces the wrong
  `f(f(t_n)) = t_{n+1}` with the correct
  `f(f(body_n)) = f(body_{n+1}) = t_{n+1}`.
- G2 → header oracle declaration + 5 in-line `> Oracle cross-check`
  blocks (§2, §3.4, §3.8-oracle-cross-ref, §4, §5 parity).
- G3 → §3.5 monotonicity lemma + structural induction on one-hole
  contexts.
- G4 → §3.6 explicit "any nonempty set of positive integers has a
  minimum, so no infinite strictly descending sequence exists."
- G5 → §3.2 two-case totality argument with explicit rho5-rho6
  LHS-sharing.
- G6 → §2 head-symbol equality argument.
- G7 → §2 "What we refute" confluence definition + "No common
  reduct" paragraph.
- G8 → §3.3 "total function ClosedTerms(Sigma) -> Z_{>0}" typing.
- G9 → §4 `> Oracle cross-check` block citing `Q3. NON-SN` banner
  with `step(t_n, (), "rho6") == t_{n+1}` for `n = 0..7` and
  `size(t_n) = n + 2` printed sizes 2..10.
- G10 → §5 "Rigor parity disclosure" dedicated section.

**New issues in final audit:**

- N1 (LOW): §4 line 312 has a "`* sigma-result`" notational remnant
  (non-mathematical; the following line clarifies "The substituted
  RHS is f(f(body_n)).").
- N2 (LOW): §2 "c's only position is eps" is terse; a reader-aid
  clause about `c` having no proper subterms would help.

**Non-inflation check.** Original gaps: 2 HIGH, 5 MEDIUM, 3 LOW.
New issues introduced by iteration 2: 2 LOW, 0 MEDIUM, 0 HIGH.
**No new gaps of the same severity as the highest original
severity (HIGH) were introduced; and no new MEDIUM gaps were
introduced.** Non-inflation holds strictly.

**Band determination under Cycle #9 rubric:**

- Band 3 criteria (all of a–e):
  - (a) ≥ 2 iterations with on-disk drafts ✓ (attempt-01.md +
    ARGUMENT.md).
  - (b) evaluator reports per iteration with `hard_constraint_violations`
    or equivalent disclosed gaps ✓ (eval-report-01 names 10 gaps;
    eval-report-final confirms gap_closure + names 2 new_issues).
  - (c) each iteration's deltas close ≥ 1 prior-iteration gap
    *without introducing new gaps of the same severity* ✓ (10/10
    gaps closed; 2 LOW new_issues ≪ 2 HIGH / 5 MEDIUM closed).
  - (d) the final deliverable reflects the progression ✓ (§4
    `body_n` framing directly replaces the bugged recurrence;
    oracle-silence replaced with 5 cross-check blocks; §3.5, §3.6,
    §3.7 new sub-sections explicitly add G3/G4/G5 closures).
  - (e) the JUDGMENT can cite each trace artifact by path ✓ (all
    paths cited above).

R10 = **3** via the M6.3 (a) native evaluator-report path.

**Reproducibility tag (Cycle #9 pre-cycle port).** R10 band 3
was achieved via M6.3 substitute **(a)** "a subsequent
`.eval-report-*.json` or named audit artefact from the evaluator"
— B produced two evaluator reports (iter-1 and iter-final), both
authored by the evaluator agent, both in B's container inside B's
active window (12:26:30 – 12:41:54). The M6.3 (c) committed-diff-
verification substitute was NOT used (no `cycle-09/B-gap-closure-
check.json` exists or was authored).

**The reproducibility-tag requirement applies specifically to band
3 via M6.3 (c). Since B's Cycle #9 R10 = 3 via (a), not (c), the
tag is `not-applicable`** with note: "B chose the M6.3 (a) native
evaluator-report path; the reproducibility-tag field only governs
(c) committed-diff-verification artefacts."

This is the M8.3 reproducibility-test outcome (CLAUDE.md clause 6
of the cycle GOAL): B's Cycle #9 architecture reached band 3
without ROOT scaffolding. In Cycle #8, B reached band 3 via (c)
with ROOT authoring the closure-check (`scaffolding-assisted`); in
Cycle #9, B reached band 3 via (a) with the evaluator agent
producing a subsequent `.eval-report-final.json` (no ROOT
scaffolding). **Architectural finding: Cycle #9 B can reach M6.3
band 3 through its own evaluator agent; the Cycle #8 ROOT-
scaffolding path is confirmed as an alternative, not a requirement.**

### B total: 1 + 3 + 3 + 3 + 3 + 3 + 2 + 1 + 3 + 3 = **25 / 30**

---

## §4. Delta analysis

| Criterion                         | A | B | Δ (B−A) | Notes |
|-----------------------------------|---|---|--------|-------|
| R1 Motivation                     | 2 | 1 | **−1** | A has distributed per-Q structural commentary including parametric (§2 remark) + structural (§3 remark) + cross-Q rule-removal (§5). B's opening is method-announcement + definition-giving; §5 rigor-parity is methodological not structural. **Cycle-specific inversion vs Cycle #8 (R1-A=1, R1-B=2).** |
| R2 Method design                  | 3 | 3 |  0  | Both: distinct-tool named sublemmas (A: 4 lemmas NF-1/Monotonicity/Strict-Decrease/Feasibility; B: monotonicity lemma + §3 sub-section structure). Both meet Cycle #7 tightening. |
| R3 Progressive minimization       | 2 | 3 | **+1** | **Cycle #9 R3 locus clarification activated.** B's §3.4 explicit 7-row × 4-column markdown table (rule / [LHS] / [RHS] / diff) is deliverable-side tabular per-rule enumeration with per-row disposition + oracle verification. A's §3.3 enumeration is bulleted prose of the same 7 rules, no table. |
| R4 Verdict commitment             | 3 | 3 |  0  | Both commit all three with per-Q discharge + cross-Q analysis. |
| R5 Exact form                     | 3 | 3 |  0  | Both mechanically correct; ROOT oracle `/tmp/verify_cycle09.py` confirms 3000+ sample assertions across both weight measures + Q1 witness + Q3 chain. B additionally has its own simulator (8 assertion tests, all pass). |
| R6 Verification strategy          | 3 | 3 |  0  | A: trace-argument with no hidden circularity, named lemmas, no disclosed gap. B: trace-argument + oracle, no hidden circularity, no disclosed gap. Both meet band 3 under R6 honesty-polarity. |
| R7 Constructive examples          | 2 | 2 |  0  | Same 2 distinct closed-term witnesses (`m(c, d)` + `f(c)`) and same 2 orthogonal axes (non-conf + non-SN); Q2 positive doesn't contribute a third axis; oracle tests are verification not construction. Tightening caps both at band 2. |
| R8 Open questions                 | 2 | 1 | **−1** | **Cycle #9 R8 labeling clarification activated.** A has 3 unlabeled structural disclosures (§2 remark + §3 remark + §5 consistency) — content-present-unlabeled maps to band 2. B has 1 labeled disclosure (§5 "irreducible structural asymmetry" — methodological scope) and no other substantive open-question/limitation content — maps to band 1. **Cycle-specific inversion vs Cycle #8 (R8-A=1, R8-B=2).** |
| R9 Exact answer match             | 3 | 3 |  0  | Both: all three verdicts correct under ROOT oracle. |
| R10 Iteration depth               | 0 | 3 | **+3** | A: pure single-shot, no Cycle #9 iteration trace (matches Cycle #7/#8 A pattern). B: 2 substantive iterations with evaluator reports per iteration (M6.3 (a) native path); 10 gaps → 10 closed; 2 LOW new-issues (non-inflation strict); reproducibility-tag = `not-applicable` (b chose (a) not (c)). **M8.3 outcome: B reached band 3 without ROOT scaffolding.** |
| **Total**                         | **23** | **25** | **+2** | |

**Comparative delta: B − A = +2, 25 vs 23.** Composition:

- +1 from R3 (Cycle #9 locus clarification activated this axis).
- +3 from R10 (architectural asymmetry; M6.3 (a) path).
- −1 from R1 (cycle-specific inversion: A stepped up structural
  commentary, B leaned on method-announcement opening).
- −1 from R8 (cycle-specific inversion: A's distributed unlabeled
  structural content vs B's single methodological asymmetry
  remark).

The +4 gross gain (R3 + R10) is partially offset by −2 gross loss
(R1 + R8); net +2.

**Comparison to Cycle #8 (Δ = +6):** Cycle #9 Δ = +2 is a 4-point
compression driven by A's cycle-specific stepup on R1 and R8
structural commentary and B's cycle-specific regression on those
same axes. R3 Cycle #9 locus clarification lifted B by +1 (Cycle
#8 B had been capped at band 2 under the same conditions). R10
parity remained at +3 both cycles. The compression is not a
rubric-effect measurement artefact — retrospective re-score of
Cycle #8 under Cycle #9 rubric (see JUDGMENT-v2.md, filed at
`docs/meta-audit/cycle-08/JUDGMENT-v2.md`) preserves Cycle #8 Δ
at +6, identifying the compression as a deliverable-effect of
Cycle #9's specific A and B outputs.

---

## §5a. Disclosed-circularity scan

Per CLAUDE.md §6.7 step 5a (pre-scoring, mandatory for every
ARGUMENT.md).

### A-ARGUMENT.md circularity scan

- **Sections scanned:** §0, §1, §2, §3.1, §3.2, §3.3, §3.4, §4, §5,
  §6.
- **Lemma dependency graph:**
  - (NF-1) [§1] — self-contained; proof by LHS-head enumeration.
  - Monotonicity Lemma [§3.2] — self-contained; proof by induction
    on context depth + argument-wise coefficient positivity.
  - Strict-Decrease Lemma (non-rho6) [§3.3] — depends on
    Monotonicity Lemma + per-rule arithmetic; linear.
  - Feasibility Lemma [§3.4] — self-contained; rho5/rho6 LHS-
    sharing.
  - Termination of S [§3.4] — depends on Feasibility + Strict-
    Decrease + well-foundedness of `N+`; linear.
  - §5 consistency check — trivial cross-Q implication; no
    dependency loop.
- **Lemma chain:** NF-1 → Monotonicity → Strict-Decrease →
  Feasibility → Termination. **Linear; no back-edge.**
- **Paragraph-level tension scan:** none detected. Scan found no
  paragraph-level internal tensions.
- **R6 polarity:** A has no disclosed gap AND no hidden
  circularity. R6 score 3 justified.

### B-ARGUMENT.md circularity scan

- **Sections scanned:** §0, §1, §2, §3.1, §3.2, §3.3, §3.4, §3.5,
  §3.6, §3.7, §3.8, §4, §5.
- **Lemma dependency graph:**
  - §0 definitions — primitives.
  - §2 head-symbol equality NF argument — self-contained.
  - §3.3 W totality — case exhaustion over Sigma; self-contained.
  - §3.4 per-rule diff table — arithmetic; each row independent.
  - §3.5 strict monotonicity lemma — self-contained; argument-
    wise coefficient positivity.
  - §3.5 context-closure Claim — depends on §3.5 monotonicity
    lemma; linear.
  - §3.6 well-foundedness — self-contained (primitive statement
    about `Z_{>0}`).
  - §3.7 halting — depends on §3.1 (S halts at NF by construction)
    + §3.6 (finite trajectory length); linear.
  - §3.8 conclusion — assembles §3.6 + §3.7; linear.
  - §4 body_n recurrence — self-contained; primitive definition.
- **Lemma chain:** §0 → §2 (independent); §3.1 → §3.3 → §3.4 →
  §3.5 monotonicity → §3.5 Claim → §3.6 → §3.7 → §3.8. **Linear;
  no back-edge.**
- **Paragraph-level tension scan:** none detected. Scan found no
  paragraph-level internal tensions.
- **R6 polarity:** B has no disclosed gap AND no hidden
  circularity. R6 score 3 justified.

---

## §5b. B → ROOT port analysis

Per CLAUDE.md §6.7 step 5b (post-scoring, mandatory). One entry
per distinct refinement artefact B produced this cycle.

### Artefact B-1 — `iterations/attempt-01.md` + two `.eval-report-*.json` pair (M6.3 (a) native iteration pattern)

- **Name and location:** B's iteration-1 draft (12:27:32) + iter-1
  evaluator report (12:32:08) + iter-final evaluator report
  (12:41:04) + iter-2 deliverable (12:41:54). Live at
  `claude-meta-autoagent-b:/workspaces/task/iterations/` +
  `task/ARGUMENT.md`. Collected to
  `docs/meta-audit/cycle-09/B-*.{md,json}`.
- **Decision:** **not-portable** to ROOT.
- **Rationale:** This is B's native `/refine` + evaluator agent
  behaviour — exactly the capability the cycle measures. ROOT
  does not iterate on its own artefacts (ROOT's outputs are the
  JUDGMENT.md + rubric-audit.json pair, not iterated). Porting
  evaluator-per-iteration discipline into ROOT would conflate the
  judge and the judged. The artefact is load-bearing for R10 band
  3 via M6.3 (a) native path; ROOT records it as architectural
  evidence, not as a portable pattern.

### Artefact B-2 — `sim/simulator.py` with 500-sample-per-rule random verification (R6 oracle path (b))

- **Name and location:**
  `claude-meta-autoagent-b:/workspaces/task/sim/simulator.py`
  (13773 B, 8 assertion tests covering Q1 witness, per-rule
  measure decrease × 500 random samples × 6 non-rho6 rules,
  per-rule measure increase × 200 random samples × rho6, Q2
  strategy termination × 12 sample terms, Q3 chain `step(t_n)
  == t_{n+1}` for n = 0..7). Captured output
  `sim/output-final.txt` (3359 B).
- **Decision:** **deferred** — candidate port to the rubric as a
  documented "band-3 oracle shape for TRS domains", carry-over to
  Cycle #10 pre-cycle review.
- **Rationale:** B's oracle pattern (random-sample verification +
  8 assertion tests + captured output) is domain-portable across
  TRS cycles. A rubric update documenting this pattern as a
  canonical R6 path-(b) shape would scale the oracle-catalogue
  approach. Deferring to Cycle #10 pre-cycle prevents conflating
  Cycle #9 rubric effect (retrospective vs in-cycle Δ
  disentanglement) with new rubric additions. No mechanical port
  needed this cycle; the `scripts/meta/oracles/` directory
  already exists and the TRS pattern can be added there next
  cycle.

### Artefact B-3 — Iteration-trace header announcement + inline `> Oracle cross-check` blocks (deliverable discipline)

- **Name and location:** Lines 3–15 of
  `docs/meta-audit/cycle-09/B-ARGUMENT.md` (iteration trace + oracle
  announcement); 5 inline oracle cross-check blocks at §2, §3.4,
  §3.8, §4, §5.
- **Decision:** **not-portable** to ROOT (B-internal deliverable
  discipline); **potentially portable** to `task-prompt-discipline.md`
  as a "self-documenting deliverable" pattern if surfaced in a
  later cycle's prompt-hint audit.
- **Rationale:** This is a B-specific deliverable-shape pattern
  that arose under B's /refine loop. Porting it to ROOT's TASK.md
  would constitute prompt-hint leakage (M7.1 risk: B would recognize
  its own output pattern described in a TASK prompt, inflating
  R10/R7). The pattern stays inside B's deliverable discipline;
  ROOT does not port it.

### Summary of ports this cycle

- **Ports committed in step 6:** 0.
- **Deferrals:** 1 (B-2, carry-over to Cycle #10 pre-cycle).
- **Not-portable:** 2 (B-1, B-3).

No ROOT .claude/ or CLAUDE.md change is required this cycle as a
direct consequence of §5b.

---

## §5c. Independent proof-auditor audit

Per CLAUDE.md §6.7 step 5c. Invocation to follow after this
draft is complete.

**Inputs passed to proof-auditor:**

- A-ARGUMENT.md: `/workspaces/docs/meta-audit/cycle-09/A-ARGUMENT.md`
- B-ARGUMENT.md: `/workspaces/docs/meta-audit/cycle-09/B-ARGUMENT.md`
- Rubric: `/workspaces/docs/research/eml-paper/judgment-rubric.md`
- Incumbent JUDGMENT: this file (draft)
- Oracle catalogue: `/workspaces/scripts/meta/oracles/` — no
  TRS-specific oracle is committed yet; `combinator-reducer.py`
  is domain-inapplicable to Cycle #9's TRS. The ROOT oracle
  `/tmp/verify_cycle09.py` is session-scoped and is referenced
  in §0 artefact table but not committed. Auditor may run it
  inline if needed for R5/R9 verification.
- Output path:
  `/workspaces/docs/meta-audit/cycle-09/rubric-audit.json`.

**Post-audit status transition** (Per §6.7 step 5c):

- `status: draft` — auditor concurs on all axes with
  `arbitration_triggered = false`. Cycle proceeds with incumbent
  verdict.
- `status: arbitration-pending` — ≥ 1 axis `|incumbent − auditor| ≥ 2`
  OR ≥ 3 axes with any band difference OR binary R9 disagreement
  OR total difference > 20% (6/30) of rubric max. Cycle freezes.
- `status: arbitrated` — arbitration resolved; per-axis
  arbitrated bands recorded.

The audit JSON + status transition are appended to cycle-log.md
Cycle #9 entry in step 9.

**Audit concurrence summary (completed 2026-04-23).**

Auditor produced `/workspaces/docs/meta-audit/cycle-09/rubric-audit.json`
(25 898 B). Results:

- `total_A = 23`, `total_B = 25` (identical to incumbent).
- `disagreement_count_A = 0`, `conditional_count_A = 0`.
- `disagreement_count_B = 0`, `conditional_count_B = 0`.
- `total_diff_A = 0`, `total_diff_B = 0`.
- `arbitration_triggered = false`; `arbitration_reason = null`.
- Agreement matrix: **20/20 axis-pairs YES** (10 for A + 10 for B),
  0 CONDITIONAL, 0 NO.
- Oracle backing: R5/R9 for both A and B verified via
  `/tmp/verify_cycle09.py` (Q1 witness + 3000 non-rho6 + 200
  rho6 samples per measure + Q3 chain n = 0..7, all pass); R3-B
  and R6-B oracle leg additionally cross-checked via B's own
  `B-simulator.py` + `B-sim-output-final.txt`.
- Rubric-port activation: auditor confirms Cycle #9 R3 locus
  clarification activated exactly on the A-prose-vs-B-table
  boundary (R3 A=2, R3 B=3); Cycle #9 R8 labeling clarification
  activated exactly on the A-unlabeled-structural-content vs
  B-single-labeled-methodological-observation boundary (R8 A=2,
  R8 B=1); Cycle #9 R10 reproducibility-tag port activated
  correctly with B's `not-applicable` tag (path (a) used, not (c)).

**Status transition.** Per CLAUDE.md §6.7 step 5c: auditor
concurrence triggers `status: draft` (front-matter transitions to
`draft` with audit backing). No arbitration required. Cycle
proceeds to step 6 / 7 / 8 with incumbent verdict.

Front-matter state updated:
- `status: draft`
- `arbitration_triggered: false`
- `auditor_total_A: 23`, `auditor_total_B: 25`
- `agreement: 20_YES_0_CONDITIONAL_0_NO`
- `audit_file: cycle-09/rubric-audit.json`

---

## §6. Partial-defect audit (pre-log gate, §6.7 step 8a)

No table rows with "Partial", "pending", "deferred", "follow-up",
or "TODO" status in the above scoring table.

**B-2 deferred port** in §5b is tracked as a Cycle #10 pre-cycle
carry-over, not a cycle-close partial-defect.

All defects this cycle: 0 closed-mid-cycle; 0 reclassified as
carry-over; 0 partial-pending at cycle close.

---

## §7. Cycle-level observations

1. **R3 locus clarification first activation.** Cycle #9 R3 locus
   clarification (ported from `cycle-09/L1-seeds/R3-enumeration-
   locus-seed.md`) first activated here. B's §3.4 markdown table
   is the canonical band-3 shape under the clarification. A's
   prose enumeration hit the band-2 cap under the clarification.
   Retrospective re-score of Cycle #8 (JUDGMENT-v2.md) tests
   whether the clarification retroactively preserves Cycle #8
   scoring; outcome: preserved (A = 20, B = 26 unchanged), so
   the clarification sharpens future discrimination without
   destabilising past scoring.

2. **R8 labeling clarification first activation.** Cycle #9 R8
   labeling clarification (ported from `cycle-09/L1-seeds/R8-
   parametric-content-locus-seed.md`) first activated here. A's
   unlabeled-but-structural content stays at band 2; B's single
   labeled methodological observation stays at band 1. Both
   outcomes match the clarification's intent (labeling matters
   for R8 epistemic discipline).

3. **R10 M6.3 (a) native path activation.** Cycle #9 B reached R10
   = 3 via the `.eval-report-*.json`-per-iteration substitute (a),
   contrasting with Cycle #8 B which reached R10 = 3 via the
   ROOT-authored committed-diff substitute (c). The Cycle #9
   pre-cycle reproducibility-tag port gates (c) against
   scaffolding-assist; (a) is native and requires no tag. M8.3
   reproducibility-test outcome: **agent-spontaneous not required
   for (a); not-applicable (c did not fire)**. The Cycle #8 (c)
   path remains a valid substitute when (a) is not available, but
   Cycle #9 demonstrates that B's architecture can achieve band 3
   without ROOT scaffolding through the evaluator-native path.

4. **Cycle-specific A-over-B inversions on R1 and R8.** For the
   first time since Cycle #4 (the proof-auditor-concurred cycle),
   A outscores B on a rubric axis (R1 and R8). This is not rubric
   drift — the per-axis reasoning traces above cite the
   deliverable content directly. It is a cycle-specific outcome
   of A's distributed structural commentary and B's flatter
   motivation layer. Retrospective re-score confirms that Cycle
   #8's opposite ordering (B > A on R1 and R8) was not an
   artefact of pre-clarification rubric text: under Cycle #9's
   clarifications, Cycle #8 A remains R1 = 1 / R8 = 1 and Cycle
   #8 B remains R1 = 2 / R8 = 2 (see JUDGMENT-v2.md). The
   inversion is a deliverable-shape difference between Cycle #8
   B and Cycle #9 B, not a rubric effect.

5. **Leak streak.** All 9 cycles clean of paper-identifier
   keywords in A or B deliverables. Hardening streak unbroken.

6. **Scientific result line (for cycle-log).** Cycle #9 JUDGMENT
   Δ = +2 (A = 23, B = 25); R3 locus + R8 labeling clarifications
   first activated (A stayed at band 2 on R3, B lifted to band 3;
   A at band 2 on R8, B at band 1); R10 band 3 reached via M6.3
   (a) native evaluator-report path without ROOT scaffolding
   (reproducibility tag: not-applicable); auditor concurrence
   pending.

---

## §8. Output

- `docs/meta-audit/cycle-09/A-ARGUMENT.md` — frozen (14086 B,
  sha256 7b06280b00ebccbd...).
- `docs/meta-audit/cycle-09/B-ARGUMENT.md` — frozen (16379 B,
  sha256 8a5cd525f66a696b...).
- `docs/meta-audit/cycle-09/B-attempt-01.md` — iteration 1 draft.
- `docs/meta-audit/cycle-09/B-eval-report-01.json` — iter-1 audit.
- `docs/meta-audit/cycle-09/B-eval-report-final.json` — iter-final
  audit.
- `docs/meta-audit/cycle-09/B-simulator.py` — B oracle source.
- `docs/meta-audit/cycle-09/B-sim-output-final.txt` — B oracle
  output.
- `docs/meta-audit/cycle-09/JUDGMENT.md` — this file.
- `docs/meta-audit/cycle-09/rubric-audit.json` — proof-auditor
  verdict (produced post-draft).
- `docs/meta-audit/cycle-08/JUDGMENT-v2.md` — retrospective re-
  score of Cycle #8 under Cycle #9 rubric (per
  `retrospective-rescore.md` discipline).
- `docs/research/eml-paper/cycle-log.md` — Cycle #9 entry
  appended at step 9.

**Final verdict.** Cycle #9 A = 23/30, B = 25/30, Δ = +2. Audit
concurrence pending. Cycle status = draft until rubric-audit.json
is produced and status transitions to `draft` (auditor concurs) /
`arbitration-pending` / `arbitrated`.
