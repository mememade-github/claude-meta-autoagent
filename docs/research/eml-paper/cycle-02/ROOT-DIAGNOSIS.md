# Cycle 02 — ROOT structural diagnosis

> Independent ROOT-side diagnosis of the three structural signals that
> Cycle #2's `JUDGMENT.md` surfaced but did not itself resolve.  Written
> after the JUDGMENT was in and pushed (commit `4f3186c`) so the
> diagnostic frame is not load-bearing for the cycle's own scoring.
>
> Scope: CLAUDE.md §4.3 load-bearing reasoning deliverable (ROOT
> structural design argument).  Independently reviewed by the
> `evaluator` agent before commit.

---

## §1 Thesis

Three symptoms from Cycle #2 share one structural root.  Two further
structural amplifiers explain why that root went undetected and will
continue to under-produce an observable A/B signal even after the
root is addressed.

**Symptoms:**

| Symptom | Where it shows up |
|---|---|
| **S1.** A and B tied 26/26 despite one being evolvable | JUDGMENT.md §9 |
| **S2.** B's internal evaluator *dropped* its score (0.815 → 0.78) when `/refine` converted a hidden circularity into a disclosed gap | JUDGMENT.md §7.3 |
| **S3.** Cycle #2 shipped with M2.1 marked **Partial — pending user approval** and with three blocking tests explicitly deferred to a follow-up commit | JUDGMENT.md §8 M2.1 row + §9 |

**Primary root** — one property that the cycle's measurement instrument
(`judgment-rubric.md`) and the cycle's execution protocol (`CLAUDE.md`
§6.7) both share and have inherited from B's own `/refine` stack: **honest
disclosure of a constraint is registered as equivalent to or weaker than
silent non-disclosure.**  Honesty buys deferral; concealment pays no tax.
When the whole stack runs that polarity, evolvable architectures that
*surface* issues look indistinguishable from baseline architectures that
*bury* them — or worse, they score lower.

**Two structural amplifiers** — conditions under which the primary root
stays invisible (see §2.5 for evidence):

- **A1. Task-design retrieval ceiling.**  When the cycle task reaches
  a well-known classical result (Cycle #2: Mohr–Mascheroni), both A
  and B default to high-quality retrieval.  Neither has incentive to
  conceal a circularity because both have one available — so the
  polarity fix cannot split scores that retrieval flattens.
- **A2. Grader mono-culture.**  B's internal evaluator, B's refinement
  evaluator, and ROOT's JUDGMENT.md grader are all single-pass
  `evaluator`-agent invocations against the same rubric text.  The
  honesty inversion in S2 went undetected *inside* B because no
  second pass disagreed with the first.  The §4.1 rubric reframe
  alone is necessary but not sufficient: the same single-pass grader
  can still apply the reframed text in the same biased direction
  without a forcing check.

The rest of this document names the three symptom sites and the two
amplifiers, then prescribes the minimum set of ROOT-owned edits that
reverses the polarity *and* forces a check the grader cannot skip.

---

## §2 Symptom analysis

### §2.1 S1 — the 26/26 tie is a measurement-paradigm artefact

The JUDGMENT.md §9 tie is *not* an indictment of B as an architecture.
The refinement trace is real: `/refine` moved B's §3.1 from narrative
to a 4-row walk-down table (directly addressing C3 from the first eval
report) and moved §6.4 Case 2 sub-case `Q ∉ ℓ` from hidden circularity
into a disclosed, named gap with an internal tension openly flagged
(JUDGMENT.md §7.3, last paragraph).  Both are real architectural
improvements.

The rubric did not see them.  R1–R9 are **snapshot criteria**: they
evaluate the final deliverable against a fixed target structure and
award points for reaching it.  They have no axis for "the process that
produced this deliverable handled its own uncertainty well."  An agent
that concealed a circularity and an agent that disclosed it at the same
R6 partial-credit bucket are treated identically by R1–R8 and only
weakly distinguished at R6 (both pick up a 2 as "attempts an
algebraic/inductive argument but leaves gaps").

This is not a cycle-#2 accident.  It is the rubric's design: R6 score 2
definition reads "leaves gaps" with no polarity between *acknowledged*
and *silent* — the same two letters at the same numeric value.  For
single-shot tasks on well-known classical results this is tolerable
(the target is the answer, retrieval is expected per §6 Meta-meta).
For distinguishing snapshot-only architectures from process-carrying
architectures it is structurally blind.

### §2.2 S2 — the honesty inversion is the same polarity, surfaced at the scorer

B's own internal evaluator showed the inversion directly: the
`.eval-report.json → .eval-report-final.json` transition was
0.815 → 0.78 while the priority-issue count *dropped* 7 → 4.  The
refinement *reduced* the number of open concerns by disclosing rather
than routing around `§6.4 Case 2 sub-case Q ∉ ℓ`, and the scorer
penalized the disclosure.  JUDGMENT.md §7.3 names this correctly as a
scorer weighting bug (G4 proof-closure weighting rewards concealment
over admission).

ROOT's `judgment-rubric.md` then *inherited* the same polarity by
independently docking both A and B to R6=2 for the same kind of
disclosed gap (see JUDGMENT.md §8 M2.1 row; also R6 reasoning for A
and for B in the main body).  The rubric's R6 definition does not
express a strict order between "attempts an argument, leaves gaps,
declares them" and "attempts an argument, leaves gaps, hides them" —
so the grader has no hook to credit B's refinement over its own
pre-refinement draft.

### §2.3 S3 — the partial ship is the same polarity, surfaced at the execution protocol

CLAUDE.md §6.7 step 9 (`Log — append cycle summary to cycle-log.md`)
and step 10 (`Push — git push origin main`) are gated by no
integrity check at all on the JUDGMENT.md's own defect-resolution
table.  Cycle #2's §8 declared M2.1 **Partial — pending user
approval** with three blocking tests *explicitly deferred*, then
proceeded to steps 9 and 10.  The cycle shipped in precisely the
mode the rubric and scorer reward: admit the limitation, defer,
proceed.

This is internally consistent with the rubric polarity: a disclosed
unresolved item is no worse than an undisclosed one, so there is no
incentive in the protocol to hold the cycle on disclosed deferrals.
M2.1 became a multi-cycle carry-over that the execution protocol
treated as closure (see cycle-log.md Cycle #2 block, line
"M2.1 now resolved at the hook level" — which is *false*, M2.1 is
not resolved at the hook level this cycle, the hook is unchanged, as
JUDGMENT.md §8 states in its own evidence column).  The cycle's
own log contradicts its own JUDGMENT on the same defect.  This is
the cost of shipping partial: downstream artefacts drift apart.

### §2.4 Cross-symptom diagnosis

S1, S2, S3 are three projections of one property:

> The rubric, the internal scorer, and the execution protocol all
> treat disclosed gaps as *at-or-below* undisclosed gaps.  Honesty
> has a neutral-or-negative slope against concealment across the
> whole stack.

Any one of the three symptoms in isolation could be a local bug.  The
three together are a systemic under-crediting of honest constraint
disclosure.

### §2.5 Why the polarity went undetected

**A1 — task-design retrieval ceiling.**  Cycle #2's own meta-meta
section (JUDGMENT.md §6) concluded: "classical retrieval
(Mohr–Mascheroni, 1797), not novel contribution, for both A and B.
… Structural leak-resistance is in the 'compliant paraphrase' zone."
Both agents produced textbook treatments of a known theorem.  Under
those conditions the polarity's observable effect on the A-vs-B
delta is near-zero — not because the polarity doesn't exist but
because the task did not require either agent to handle an
unresolved technical joint *asymmetrically*.  Both agents disclosed
the same gap at the same joint; the rubric then scored them
identically at R6=2 and the polarity left no fingerprint.  This is
why a cycle-log reading on Cycle #2 *alone* cannot diagnose the
polarity — the diagnosis requires looking at B's internal eval
delta (§7.3), which is one layer below the JUDGMENT.

**A2 — grader mono-culture.**  B's first eval gave 0.815; B's
second eval gave 0.78; same evaluator pattern, different iteration.
The scorer inversion went unsurfaced inside B's own /refine because
there was no second grader to disagree.  ROOT then produced its
JUDGMENT.md with the same single-pass evaluator-agent pattern (one
grader, one rubric read, one score per criterion per agent), and
naturally aligned with B's internal eval on R6=2.  The rubric
polarity is therefore *stable under mono-culture grading*: a
grader with the current rubric will reproduce the bias whether it
runs once or a hundred times, because the bias is in the rubric
text the grader reads.  Fixing the rubric alone is not enough; the
protocol must also force the grader to do a thing the rubric text
does not ask for (§4.4 below).

---

## §3 What the diagnosis is *not* saying

Three boundaries, stated up front so the prescription in §4 stays
scoped (§1.3 surgical changes):

1. **Not "tie is wrong"**.  A and B both reached `T = {C}` with
   high-quality first-principles reasoning.  The 26/26 numeric tie is
   defensible at the per-criterion level.  What the diagnosis objects
   to is the *absence* of a criterion that would have resolved the
   tie toward B's refinement trace.

2. **Not "B is the correct architecture"**.  The cycle's purpose is
   to *measure* A vs B, not to declare a winner a priori.  The
   diagnosis prescribes measurement fixes, not outcome predictions.

3. **Not "Cycle #2 should be voided"**.  The JUDGMENT is committed
   and the leak audits pass.  The diagnosis is *forward*-facing —
   what Cycle #3 onward needs — not retrospective invalidation.

---

## §4 Prescribed self-improvement

Four ROOT-owned edits, bundled as one commit.  Three reverse the
honesty polarity at the three symptom sites (§4.1 for S2, §4.2 for
S3, §4.3 for the port-analysis gap M2.2 mitigated without
codifying).  The fourth (§4.4) addresses amplifier A2 so the
rubric reframe (§4.1) cannot be silently no-op'd by a mono-culture
grader.

### §4.1 `judgment-rubric.md` — R6 honesty ordering

Rewrite R6's score-level definitions so the ordering is:

```
0 < hidden circularity < disclosed-but-unresolved gap < closed proof
  =        1              =        2                  =    3
```

Concretely, R6 currently reads:

> 1 — A couple of hand-picked examples only.
> 2 — Attempts an algebraic/inductive argument but leaves gaps.
> 3 — Numerical sieve … or a constructive bootstrap procedure that
>     builds each target primitive from the candidate basis.

Replace with:

> 1 — Hand-picked examples only, **or** an argument with hidden
>     circularity (a step relies on the conclusion it is meant to
>     establish, and the reliance is not disclosed).
> 2 — Attempts an algebraic/inductive argument with gaps, **and the
>     gaps are named and scoped as explicit limitations**.
> 3 — Numerical sieve … or a constructive bootstrap procedure that
>     builds each target primitive from the candidate basis **with
>     no disclosed gap remaining**.

Plus a "Scoring note" paragraph stating explicitly: disclosed gap at
R6=2 outranks hidden circularity at R6=1.  Grader must scan for
circularity at the §-reference level and downgrade accordingly.

This reverses S2 (the inversion).  It also turns S1 (the tie) into a
resolvable signal: if a future cycle sees one agent disclose and the
other conceal on the same technical joint, R6 will split them 2 vs 1
instead of 2 vs 2.

### §4.2 CLAUDE.md §6.7 — no-partial-ship gate

Insert between §6.7 step 8 (Verify A untouched) and step 9 (Log) a
new step 8a.  The gate is scoped to the JUDGMENT.md's
defect-resolution *table* (not free prose) so "pending" or "TODO"
appearing in descriptive paragraphs does not false-match:

> 8a. **Partial-defect audit** — identify each defect-resolution
>     table row in the cycle's JUDGMENT.md whose Status column
>     contains "Partial", "pending", "deferred", "follow-up", or
>     "TODO".  Each such row must be either (i) **resolved** in a
>     subsequent commit *before this step completes*, with the
>     JUDGMENT.md row updated to a closure status, or (ii)
>     **reclassified as a carry-over defect** — the row in this
>     cycle's JUDGMENT.md must be edited to state "Carry-over to
>     Cycle N+1" with a named new-cycle tracking handle, and a
>     corresponding `cycle-log.md` entry must open the carry-over
>     explicitly.  "Partial" is not a terminal state for cycle
>     closure.  → verify: grep the markdown table rows only
>     (`grep -nE '^\|' docs/research/eml-paper/cycle-NN/JUDGMENT.md
>     | grep -iE '(partial|pending|deferred|follow-up|todo)'`)
>     returns only rows that match clause (ii), verified by a
>     "Carry-over to Cycle" string on the same row.

This addresses S3 directly.  It also enforces the diagnosis's own
§1.3 rule on future ROOT work: if this diagnosis itself prescribes
four edits, step 8a ensures the cycle's next run either lands all
four or re-scopes them explicitly.

### §4.3 CLAUDE.md §6.7 step 5 — B → ROOT port-analysis requirement

Cycle #2's JUDGMENT §7 introduced port-decision analysis ad-hoc.
Port analysis is an artefact written *into* the JUDGMENT.md itself,
so it belongs under step 5 (Judge — write JUDGMENT.md), not step 6
(Improve ROOT — commit changes).  Add as step 5a:

> 5a. **B → ROOT port analysis** — the JUDGMENT.md written in step
>     5 must carry a "B → ROOT port analysis" section with one
>     entry per distinct refinement artefact B produced this cycle
>     (a `/refine` diff, a new documentation pattern, a scorer
>     signal, an internal evaluator finding): (i) name and
>     location, (ii) decision — ported / not-portable / deferred,
>     (iii) if ported — commit reference; if not-portable —
>     rationale; if deferred — carry-over cycle number.  Step 6
>     (Improve ROOT) then operationalises each "ported" decision
>     as an actual commit.

This addresses the M2.2-class failure mode that Cycle #1 exhibited
and Cycle #2 structurally mitigated (per JUDGMENT.md §8 M2.2) but
did not codify.  It also gives the rubric the cross-run observability
it lacks: B's process wins become first-class cycle artefacts.

### §4.4 CLAUDE.md §6.7 step 5 — disclosed-circularity scan (grader forcing check)

To address amplifier A2 (grader mono-culture), add a pre-scoring
sub-step that the grader cannot satisfy by reading the rubric text
alone — the scan must be performed against the ARGUMENT.md itself
before the R6 score is written.  As step 5.0 (prepended to step 5
body, before the per-criterion scoring begins):

> 5.0. **Disclosed-circularity scan** (pre-scoring) — for each
>      ARGUMENT.md under grading, scan for (i) paragraph-level
>      internal tensions (a claim whose justification elsewhere in
>      the document contradicts it, e.g. a §X step that invokes a
>      result whose own derivation at §Y relies on §X), and (ii)
>      lemma-level circularity (a sub-proof whose ingredient is
>      the theorem itself).  Each finding must be cited by
>      §-reference pair in the JUDGMENT.md's R6 score
>      justification.  R6 score selection then uses the reframed
>      polarity from §4.1: disclosed & named → 2; hidden or
>      undisclosed → 1; closed → 3.  Mandatory for every
>      ARGUMENT.md, whether or not the ARGUMENT author declares
>      gaps — a self-declared "no gaps" document is a case where
>      the grader must *independently* verify the absence.

The "independently" clause is what breaks grader mono-culture: the
grader must produce paragraph-level citations that a single rubric
read would not produce.  The citations become audit-trail evidence
that the R6 scoring engaged the forcing check, so later readers
can verify the grader did not skip.

### §4.5 What this commit does *not* try to do

Explicitly out of scope, named to resist mission creep (§1.3):

- **Not touching M2.1 hook + settings edits**.  Those require
  `.claude/hooks/sub-project-edit-guard.sh` and
  `.claude/settings.json` writes, which the environment's
  sensitive-file policy denies non-interactively.  The
  `no-partial-ship gate` (§4.2) promotes M2.1 to explicit
  carry-over instead of leaving it as "Partial" — which is the
  right closure under the new polarity.  The hook fix itself is the
  first Cycle-#3 action, under the new protocol.
- **Not touching B's `.claude/`**.  This is a ROOT-self-improvement
  diagnosis (GOAL clause 3).  B improvements are a separate
  cycle-level concern.
- **Not rewriting R1–R5 or R7–R9**.  Only R6 carries the inversion;
  the other axes are snapshot-correct and should not be disturbed
  (§1.3 surgical changes).
- **Not adding a new R10 axis**.  Minimum viable fix is a polarity
  correction inside R6.  Inflating to a 28-point rubric without a
  forcing reason violates §1.2.

---

## §5 How we would know these edits worked

Four forward-checks, to be executed at Cycle #3's JUDGMENT time:

1. **R6 polarity check** — if Cycle #3's A and B differ in whether
   they disclose their hardest unresolved step, R6 scores differ by
   ≥ 1.  (If they still tie at R6=2 despite one concealing and one
   disclosing, the reframe failed and the rubric text is still
   ambiguous.)
   **Caveat (amplifier A1):** this check can only fire if Cycle #3's
   task does not reduce to pure classical retrieval.  If the next
   task is another shape-hinted well-known theorem — as Cycle #2
   was — A and B will again disclose the same joint at the same
   level and the check will be vacuous.  Cycle #3 task selection
   must therefore prefer (a) obscure classical results, (b) results
   with a canonical answer a first-principles derivation would
   diverge from, or (c) results with no classical answer.  This is
   a task-design companion to §4.1, not a separate rubric fix.
2. **Partial-defect-audit check** — Cycle #3's `cycle-log.md` entry
   either contains no "Partial" rows in the defect-resolution table,
   or every such row is matched by a "Carry-over to Cycle #4" line
   with a named tracking handle.
3. **Port-analysis check** — Cycle #3's JUDGMENT.md carries a "B →
   ROOT port analysis" section with at least one entry per
   `/refine` artefact B produced, each carrying a decision label.
4. **Grader-forcing-check audit** — Cycle #3's JUDGMENT.md R6
   score justifications each cite at least one §-reference pair
   from the ARGUMENT.md under grading, produced by the
   disclosed-circularity scan (step 5.0).  A score-3 R6 requires
   the justification to explicitly state "scan found no
   paragraph-level internal tensions" with the sections scanned
   enumerated.  If an R6 justification is a single bullet with no
   §-refs, the scan was skipped — repeat step 5.0 before step 9.

If Cycle #3 misses any of the four, the corresponding §4 edit is
under-specified and needs a second iteration — recorded as a
Cycle-#3 defect under the new polarity (explicitly, not as
"Partial").

---

## §6 Relationship to the six-rule Behavioral Foundation

The diagnosis is an application of §1.1 (Think Before Executing:
surface assumptions the rubric didn't surface) + §1.4 (State =
Success: "cycle shipped" is not an end-state if declared defects
remain partial).  The prescription is an application of §1.3
(Surgical Changes: exactly the four edits that address the
polarity and its grader-mono-culture amplifier, nothing more) +
§1.5 (Literal Intent: writing the no-partial-ship gate as a
verifiable grep rather than a "try to resolve partial items"
exhortation).

The self-improvement commit this diagnosis feeds into satisfies
GOAL clause 3 (ROOT self-improvement ≥ 1 commit) by modifying the
rubric (§4.1) and three parts of the execution protocol (§4.2,
§4.3, §4.4) together in one unit — all four edits are load-bearing
for each other and splitting them would violate §1.3 (one
delegation = one OUTCOME).  §4.1 alone is insufficient without
§4.4's grader forcing check (amplifier A2); §4.2 depends on §4.3's
port-analysis section existing as a structured JUDGMENT.md
artefact; §4.4 depends on §4.1's reframed R6 for its scoring
branch.
