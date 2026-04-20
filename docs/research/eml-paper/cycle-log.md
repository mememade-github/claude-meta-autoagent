# A/B Cycle Log

Running summary of each completed A/B cycle. One entry per cycle, appended in
chronological order. Full deliverables live under `cycle-NN/`.

---

## Cycle 01 — 2026-04-20

**TASK framing.** `cycle-01/TASK.md` — "Minimal generating basis for elementary
functions" over the 34-primitive scientific-calculator set. Structural hint
"does a single binary operator paired with a single constant suffice?" was
intentionally omitted; only the neutral "smallest generating basis" question
was posed. `paper-leak-audit` pattern set passed the GOAL pre-filter.

**Execution.** Both sub-agents launched via `scripts/meta/delegate-sub.sh {a,b}`
with `EFFORT=max`, launched in parallel at 13:32:21 KST.

- A: produced `task/ARGUMENT.md` at 13:43:38 (16362 bytes); process exited
  13:44:37 (~12 min). Single write, no iteration.
- B: first wrote `task/ARGUMENT.md` at 13:42:08 (28224 bytes); iterated in
  place to 35730 bytes; exited 13:58:25 (~26 min). Three writes total. No
  `/refine` invocation (no `.refinement-active` marker, no `attempts/`
  directory); iteration was direct re-editing.

**Leak audit.** Both PASS. No web-access attempts recorded (web-block.sh hook
was deployed; no block events because the agents never tried). No paper-
identifying keyword appears in either ARGUMENT.md. Expanded reversed-form
pattern set (`docs/research`, `eml-paper`, `paper.pdf`, `paper.txt`) verified
functional by unit test on the guard before cycle launch.

**Scores (see `cycle-01/JUDGMENT.md` for per-criterion evidence).**

| Criterion | A | B |
|-----------|---|---|
| R1 Motivation              | 3 | 3 |
| R2 Method design           | 2 | 3 |
| R3 Progressive minimization| 3 | 3 |
| R4 Final basis structure   | 2 | 2 |
| R5 Exact form              | 1 | 1 |
| R6 Verification strategy   | 3 | 3 |
| R7 Constructive examples   | 3 | 3 |
| R8 Open questions          | 3 | 3 |
| R9 Exact answer match      | 0 | 0 |
| **Total**                  | **19/27** | **20/27** |

**Key finding.** Both arguments converge on `{+, exp, ln, i}` as the minimum
basis (4 primitives: 1 binary + 2 unary + 1 constant) and argue that 4 is a
tight lower bound via role-counting / ramification-order / growth-at-∞. Neither
considers fusing `exp` and `ln` into a single binary operator, so both miss
the 1-binary + 1-constant target on R9. A gets closest: §3F considers
`f(x,y) = exp(x) + y` as a hybrid-binary candidate and rejects it for "needing
0 as a separate constant" — this is the exact sub-constraint that `ln(1) = 0`
dissolves when `ln` enters the same binary. The structural doorway was
visible to A; A did not walk through it.

**Comparative delta = +1 for B, on R2 method design** — B's explicit
three-check verification protocol (syntactic closure + functional value at a
non-degenerate point + functional value at 3+ branch-covering points) is
methodologically more rigorous than A's symbolic-only verification. All other
criteria tied.

**/refine did not fire.** B's CLAUDE.md §2 trigger for `/refine` is "changes
affecting 2+ files". A single-file reasoning deliverable does not match. This
is the primary reason the evolvable architecture did not produce more than a
single-point edge this cycle.

**ROOT self-improvements applied (commit `00db913`).** CLAUDE.md §6 now
codifies: (a) step 0 pre-cycle prep as the sole "ROOT edits A" exception,
with `.frozen` remove/restore leaving zero net diff; (b) the
`cycle-NN/TASK.md` hint-drift-record convention; (c) the credentials-bootstrap
requirement before launching sub-agents.

**B improvements applied (commit `e279fd5`).** `projects/b/CLAUDE.md` §2
`/refine` trigger extended to "load-bearing reasoning deliverables" where the
first draft's correctness is not settled by an external oracle. The trigger
now fires on single-file proofs / argument documents, not just multi-file
code changes.

**Drift audits.**
- `git diff cycle-01-pre -- projects/a/` — empty. A untouched. ✓
- `git diff cycle-01-pre -- projects/b/` — only `projects/b/CLAUDE.md`
  (+11 lines), attributable entirely to commit `e279fd5`. No self-edit
  drift from B. ✓

**Commits in this cycle (after `cycle-01-pre`).**
1. `33c678d` docs(cycle-01): JUDGMENT + TASK + A/B ARGUMENT snapshots
2. `00db913` feat(CLAUDE.md §6): codify pre-cycle prep, hint-drift record, auth bootstrap
3. `e279fd5` feat(projects/b CLAUDE.md): extend /refine mandate to reasoning deliverables

**Open for next cycle.**
- Does B's extended `/refine` trigger actually fire on the next reasoning
  task? (Falsifiable expectation: `.refinement-active` marker will appear
  in B's filesystem during cycle-02 execution.)
- Does /refine iteration close the R9 gap? (Falsifiable: R9 changes from 0
  to 3 in the cycle-02 B score, if the convergent blind spot is a
  first-draft artifact rather than an architectural limit.)
- The A-vs-B spread of +1 is too small to distinguish architecture from
  noise. A larger spread, or repeated cycles, is needed before attributing
  causation to any B architectural feature.
