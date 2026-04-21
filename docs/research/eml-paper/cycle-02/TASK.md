# Cycle 02 — TASK definition (ROOT-only)

**Cycle purpose.** Measure whether Phase 1 restructuring (commit `b61ace0`) + the
pre-cycle finalization (commit `47593c8`, tagged `cycle-02-pre`) resolves Cycle
#1's three recorded defects:

- M2.1 — sub-project-edit-guard hook did not match `Bash`, letting ROOT's
  Bash+sed bypass the A-frozen invariant during pre-cycle prep.
- M2.2 — one B-improvement item from Cycle #1 JUDGMENT.md Learning-log was
  silently dropped (no open-items record).
- `/refine` non-firing — B's `/refine` trigger was file-count-based and never
  fired for a single-file reasoning deliverable.

Domain change per Cycle #1 meta-meta §8.3: **do not re-run the elementary-functions
task**. Pick a task from a different domain whose "single primitive" structure
is also non-obvious.

---

## 1. Task prompt delivered to A and B

Both sub-agents receive identical text via `scripts/meta/delegate-sub.sh <key>`.
The pre-filter blocks the Cycle #1 paper-keyword set (eml, Odrzywolek, Sheffer,
2603.21852); this task is a different domain and the prompt contains none of those.

```
TASK: Minimal primitive set for Euclidean plane constructions

Consider geometric constructions in the Euclidean plane. A construction begins
with a finite set of given starting points. A construction step is drawn from
the following primitive operation set, and produces a new drawn curve plus any
new intersection points that the curve makes with previously-drawn curves:

  Line primitive (L): given two distinct already-constructed points P and Q,
  produce the unique line through P and Q as a new drawn curve. Any
  intersection points of this new line with previously-drawn curves (lines
  or circles) are added to the set of constructed points.

  Circle primitive (C): given two distinct already-constructed points P and Q,
  produce the circle centered at P and passing through Q as a new drawn curve.
  Any intersection points of this new circle with previously-drawn curves are
  added to the set of constructed points.

A point is "constructible from primitive set S" if a finite sequence of
applications drawn from S produces it, starting from the given starting points.
It is widely known that {L, C} suffices to construct every point reachable by
the classical compass-and-straightedge repertoire.

Central question: what is the smallest subset T of {L, C} such that every
point constructible from {L, C} is also constructible from T (from the same
starting set)? Is one of the two primitives enough alone?

Your deliverable: a self-contained argument, written to `task/ARGUMENT.md` in
your working directory. It must include:

  1. Motivation. Why might such a reduction exist? Cite precedents from
     adjacent algebraic, computational, or geometric domains that you reason
     about from first principles.
  2. A systematic reduction procedure you design and justify.
  3. A sequence of progressively smaller sufficient primitive subsets with
     intermediate stopping points argued for.
  4. The minimal subset you can reach and a concrete argument that it
     preserves constructibility.
  5. A verification strategy: how do you confirm that a candidate primitive
     set is complete (every point constructible from the full set is also
     constructible from the candidate)?
  6. Worked examples: construct at least three distinct canonical objects
     using only your minimal primitive set. Suggested candidates: the
     midpoint of a given segment, a perpendicular from a given point to a
     given line, and the reflection of a given point across a given line.
     Pick whichever three you prefer.
  7. Open questions and known limitations of your result.

Constraints:
  - Do not consult external sources. Arguments must be developed from first
    principles. WebFetch and WebSearch are disabled.
  - Do not rely on named results you cannot derive. If you invoke a theorem,
    sketch its reason.
  - Cite no papers. If you remember a relevant paper, state the underlying
    idea in your own words; do not name or quote.
```

---

## 2. Ideal answer (ROOT-only)

| Step | Content |
|---|---|
| 1 Motivation | Boolean universality (NAND), combinator basis, field transcendence basis, Post's lattice, Galois-theoretic reductions — any result where a rich primitive set collapses to a generating core. The underlying idea: "given a richly-structured composition closure, look for the smallest subset whose closure is the whole." |
| 2 Procedure | Define reach(S) = set of constructible points. Test subsets of {L, C} by demonstrating (a) reach(S) ⊇ reach({L, C}) — sufficiency — or (b) constructing a specific point outside reach(S) that is inside reach({L, C}) — insufficiency. |
| 3 Progression | {L, C} → {L} (fails: can show no new-point generation past degenerate cases) → {C} (succeeds: construct-line-intersection via pairs of circles; construct-perpendicular via two arcs; midpoint via intersecting arcs). |
| 4 Minimal | {C} alone suffices. The single-primitive basis is the circle primitive (with intersection as an implicit subroutine in the curve-producing semantics). |
| 5 Verification | For each primitive operation in the full set {L, C}, exhibit a construction using only C that produces the same output points. In particular, for L (given two points, produce a line — or more precisely, for every construction that would next intersect line(PQ) with some other curve, produce the same intersection using only arcs). |
| 6 Examples | (a) Midpoint of segment PQ using only C: draw circle(P,Q), circle(Q,P); they intersect at two points A and B; circle(A,P), circle(B,P) intersect at two points on line PQ — one of which is the midpoint by symmetry. (b) Perpendicular: similar two-arc construction. (c) Line-line intersection: given four points A, B, C, D defining two lines, construct the intersection using only compass arcs via the inversion argument (Mohr-Mascheroni proof technique). |
| 7 Limits | Real Euclidean plane only; drawing the actual line between two points is impossible with a compass but every *point* on the line that would have been constructed is reachable. Does not address Steiner-style constructions (straightedge + a single given circle), which is a different question. |

Canonical identity of the result: the "compass alone suffices" theorem (see §3 for name-blocklist).

---

## 3. Paper-identifying keywords for this cycle (informational)

These must NOT appear in any TASK prompt, any ROOT→sub delegation payload, or
the delivered prompt. They are allowed in this ROOT-only file because it is
never mounted into A or B.

- "Mohr" (mathematician, 1672)
- "Mascheroni" (mathematician, 1797)
- "Mohr-Mascheroni" (the theorem)
- "Poncelet" (complementary result: straightedge + 1 circle)
- "Poncelet-Steiner" (the complementary theorem)
- "compass alone" (directional hint for the answer)

The existing `paper-leak-guard.sh` reversed-forms block the Cycle #1 keyword
set; it does not block the above Cycle #2-specific names. For Cycle #2 we rely
on: (a) no file in A/B's mount containing these names, (b) the delegation
prompt containing none of them, (c) post-cycle `paper-leak-audit.sh` scan for
these names on both ARGUMENT.md files (see §4 below). We do **not** extend the
reversed-form blocklist for Cycle #2, so no edit to `projects/{a,b}/.claude/hooks/paper-leak-guard.sh`
is required — keeping the pre-cycle prep symmetric-zero-change on projects/a/.

---

## 4. Post-cycle leak audit extension (Cycle #2 only)

Run the base `scripts/meta/paper-leak-audit.sh` (blocks the Cycle #1 keyword set,
still applicable) on each ARGUMENT.md. Then additionally grep each ARGUMENT.md
for each name in §3 above. Any hit on a §3 name also triggers the Leak
disqualification tier in `docs/research/eml-paper/judgment-rubric.md`.

```
grep -iE 'mohr|mascheroni|poncelet|steiner' projects/a/task/ARGUMENT.md
grep -iE 'mohr|mascheroni|poncelet|steiner' projects/b/task/ARGUMENT.md
```

(The "compass alone" phrase is not name-identifying; it is a structural
description that A/B might reach on their own. Do not disqualify on it.)

---

## 5. Hint-drift record (required by CLAUDE.md §6.7 step 1)

| Hint | Decision | Rationale |
|---|---|---|
| "Single primitive suffices" / "minimum 1" | **Included** (as "Is one of the two primitives enough alone?") | Structural shape hint; parallel to Cycle #1's "single binary operator paired with a single constant that suffices" — comparable across cycles. This lets the A/B delta measure architectural contribution holding task-framing constant. |
| Theorem names (Mohr, Mascheroni, Poncelet, Steiner) | **Omitted** | Name recall would short-circuit the "derive from first principles" contract. |
| Historical dates (1672, 1797, 1822) | **Omitted** | Same — date cue might trigger memory hit. |
| Which primitive alone works (C, not L) | **Omitted** | Central-question phrasing is symmetric: "Is one of the two enough alone?" — does not bias toward C. |
| "Compass" / "straightedge" terminology | **Omitted from prompt** | The prompt uses "Line primitive" and "Circle primitive" to decouple from historical naming. However, both words are still natural enough that a reasoning agent will reach them; blocking the words in the answer would be over-constraining. |
| Inversion / stereographic-projection technique | **Omitted** | The Mohr-Mascheroni proof's standard technique. Leaving it out means A/B must derive the reduction idea, not just the statement. |
| Connection to field extensions (constructible numbers = ℚ with iterated quadratic extensions) | **Omitted** | Algebraic-geometry reframing of the same question. Including would hint at the deeper structure. |
| "Compass and straightedge" phrase | **Included (once, and labelled)** | Used in the sentence "widely known that {L, C} suffices to construct every point reachable by the classical compass-and-straightedge repertoire." This is background framing, not a hint at the answer. |

---

## 6. Task-framing drift vs Cycle #1

| Aspect | Cycle #1 | Cycle #2 |
|---|---|---|
| Domain | Elementary functions (continuous analysis) | Euclidean plane constructions (discrete geometry) |
| Primitive family cardinality | ~30 (constants + unary + binary ops) | 2 (line, circle) |
| Central-question shape hint | "Is there a single binary operator paired with a single constant that suffices?" | "Is one of the two primitives enough alone?" |
| Expected minimal form | 1 binary + 1 constant | 1 primitive (circle) |
| Deliverable structure | 7 sections (motivation → procedure → progression → minimal → verification → examples → open) | same 7 sections |

The question shapes are equivalent; the domains are orthogonal. This lets us
separate "architectural contribution to reasoning" from "task-specific recall"
when comparing Cycle #1 and Cycle #2 A-vs-B deltas.

One asymmetry worth noting for future cycles: Cycle #2's primitive family has
only 2 elements, so the "progressive minimization" criterion (R3) has a
shorter natural path (just 2 → 1 rather than 6 → 4 → 3 → 2). We should not
penalize either agent for that — R3 scoring in Cycle #2 should emphasize
*quality* of the 2→1 reduction argument, not number of intermediate steps.
This adjustment will be called out in the Cycle #2 JUDGMENT.md at scoring
time, not pre-agreed in a cycle-02-specific rubric amendment (to avoid
silent rubric drift between cycles).

---

## 7. B `/refine` firing expectation

Per `projects/b/CLAUDE.md` §4.3 (extended in commit `e279fd5`):

> `/refine` is mandatory for any reasoning deliverable where the first draft's
> correctness is not settled by an external oracle (tests, compiler, metric).

This task produces a single-file reasoning deliverable with no external
oracle. **B must fire `/refine` for this cycle to count as an apples-to-apples
B-versus-A test of the evolvable architecture.** Measured evidence of firing:

- `.refinement-active` marker file present in B's workspace during the run
- `attempts/<timestamp>.jsonl` arrival(s) under `projects/b/attempts/`
  (B container's view is `/workspaces/attempts/`)
- Evaluator-agent invocation visible in B's `/tmp/agent.log` or transcript

If none of these appear, Cycle #2 records "B `/refine` non-firing" as a
repeat of Cycle #1's defect, not a resolution, and the JUDGMENT.md
accordingly.
