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

---

## Cycle 02 — 2026-04-21

**TASK framing.** `cycle-02/TASK.md` — "Minimal primitive set for Euclidean
plane constructions" over `{L, C}` (line / circle).  Structural shape hint
"is one of the two primitives enough alone?" was included (parallel to
Cycle #1's "single binary operator + single constant" hint), theorem
names (Mohr, Mascheroni, Poncelet, Steiner), historical dates, and the
inversion / field-extension proof techniques were all omitted.  Domain
swap from continuous analysis (Cycle #1) to discrete geometry — per
Cycle #1 meta-meta §8.3, do not re-run the elementary-functions task.

**Execution.** Both sub-agents launched via `scripts/meta/delegate-sub.sh
{a,b}` with `EFFORT=max`.  Cycle #2's first launch (11:19) hung 2h14m
with empty agent.log and no commits; Level-1 terminated and restarted
ROOT at Phase 3 (pre-existing A/B artefacts reused).

- A: produced `task/ARGUMENT.md` (872 lines, classical operational
  simulation — inversion-based line-line, reflection-based line-circle).
- B: produced `task/ARGUMENT.md` (1398 lines, field-theoretic bypass —
  `K_S^ℂ`-rational-points characterization + compass-only generator
  realization).  `/refine` fired: two evaluator reports present
  (`.eval-report.json` weighted 0.815, 7 priority issues; then
  `.eval-report-final.json` weighted 0.78, 4 priority issues).  Score
  dropped 0.815 → 0.78 but issues dropped 7 → 4 — the refinement traded
  hidden circularity for disclosed gap + internal tension.  See §7.3 of
  `cycle-02/JUDGMENT.md`.

**Leak audit.** Both PASS.  Base `paper-leak-audit.sh` green on both.
Cycle-#2-specific name grep (`mohr|mascheroni|poncelet|steiner`) also
clean on both.  "Compass alone" phrase present in both as a structural
(non-name) description, per TASK.md §4.

**Scores (see `cycle-02/JUDGMENT.md` for per-criterion evidence).**

| Criterion                   | A | B |
|-----------------------------|---|---|
| R1 Motivation               | 3 | 3 |
| R2 Method design            | 3 | 3 |
| R3 Progressive minimization | 3 | 3 |
| R4 Final basis structure    | 3 | 3 |
| R5 Exact form               | 3 | 3 |
| R6 Verification strategy    | 2 | 2 |
| R7 Constructive examples    | 3 | 3 |
| R8 Open questions           | 3 | 3 |
| R9 Exact answer match       | 3 | 3 |
| **Total**                   | **26/27** | **26/27** |

Rubric adaptations for Cycle #2 documented in JUDGMENT.md "Domain
adaptation" table (R3 emphasizes 2→1 reduction quality, not step count;
R4/R5/R9 re-read for the single-primitive-of-`{L, C}` target).

**Key finding.** Both reach `T = {C}` (compass alone).  Both leave a
disclosed gap at the compass-only length-transfer / center-on-line
line-circle intersection — A at §4.9 Case 2b, B at §6.4 Case 2 sub-case
`Q ∉ ℓ`.  A's gap is operational; B's is algebraic-bypass-aware.  The
R6=2 dock on both reflects these disclosed gaps.

**Meta-meta: classical retrieval, not novel contribution.**  Both
arguments are high-quality first-principles re-derivations of the
Mohr–Mascheroni theorem (1797).  Neither cites a name; both use
textbook proof techniques (A: inversion-based; B: field-closure).
Structural leak-resistance is in the "compliant paraphrase" zone:
the syntactic constraint (no names) is honoured, but semantic
retrieval is unavoidable for general-mathematics-literate agents.

**Comparative delta = 0 (tie).**  /refine produced a measurable delta
on *R3 walk-down execution* and *R6 integrity (disclosed > hidden)*,
but neither movement changed the rubric score.  The tie is not a null
result: it indicates that when first-draft quality is high, the
evolvable-architecture premium is small at the rubric level — the
value from B shows up in the refinement trace (scorer-evolution
signal §7.3 of JUDGMENT.md) rather than the score.

**ROOT self-improvements applied this cycle.**
- **M2.1 fix — partial**: forward-coverage tests (three cases:
  `.frozen` toggle allowed, read-only on frozen allowed, outside-frozen
  writes allowed) added to `tests/cases/hook-sub-project-edit-guard.sh`;
  full suite green.  The hook + settings.json edits (Bash
  write-token guard targeting frozen sub-project paths, with `.frozen`
  marker excepted for §6.7 Step 0 compatibility) are fully specified
  but require writes to `.claude/hooks/sub-project-edit-guard.sh` and
  `.claude/settings.json`, both of which the environment's
  sensitive-file policy currently denies non-interactively.  See
  `cycle-02/JUDGMENT.md` §8 and §9 for follow-up instructions.  The
  three complementary blocking Bash test cases (sed -i / rm /
  redirection into frozen must exit 2) are deferred to that same
  follow-up commit.
- **ROOT §4.3 extension (CLAUDE.md)**: ported B's reasoning-deliverable
  `/refine` mandate to ROOT.  Applies to ROOT's own single-file
  judgment deliverables (JUDGMENT.md, design arguments, meta-meta
  rulings).

**B improvements applied this cycle.**  None.  All viable B refinements
either already ported pre-cycle (`/refine` trigger in commit `e279fd5`)
or logged as non-portable / Cycle #3 carry-over (see JUDGMENT.md §7).

**Drift audits.**
- `git diff cycle-02-pre -- projects/a/` — empty. A untouched. ✓
- `git diff cycle-02-pre -- projects/b/` — only
  `projects/b/task/ARGUMENT.md` + `projects/b/task/.eval-report*.json`
  (B-internal deliverables). No self-edit drift from B's `.claude/`. ✓

**Open for next cycle.**
- **Cycle #3 task selection — resolved**: `docs/research/eml-paper/cycle-03/TASK.md`
  drafted. Domain: register-machine instruction-set minimization (discrete
  computation — orthogonal to Cycle #1 analysis and Cycle #2 geometry).
  A1 mitigation: multiple named canonical answers exist (SUBLEQ, Minsky
  machine, Shepherdson–Sturgis, BitBitJump, …), all explicitly banned in
  the delivered prompt; the minimum depends on the agent's declared
  counting convention, forcing engagement with the modelling step rather
  than pure retrieval.
- **Scorer-evolution signal — channelled to Cycle #3 TASK §7**: B's
  0.815 → 0.78 Cycle #2 drop (evaluator treated disclosed-gap
  refinement as G4 regression) is now codified as a G5 integrity axis
  instruction in `cycle-03/TASK.md` §7. B's /refine contract for
  Cycle #3 will include the G5 polarity rule: hidden circularity <
  disclosed gap + named limitation < closed proof. JUDGMENT §7.3's
  prescribed channel ("captured in Cycle #3 TASK preparation as a
  scorer-evolution note for B's next refinement run") is the path
  used; the direct-edit path (write to `projects/b/.claude/agents/evaluator.md`)
  was attempted 2026-04-21 PM and blocked by the sensitive-file
  policy (see Post-cycle ROOT note below).
- **Cycle #2 defect resolution — corrected**: the prior wording here
  ("M2.1 now resolved at the hook level (Bash write-token guard)")
  was incorrect, as `cycle-02/ROOT-DIAGNOSIS.md` §2.3 called out —
  the hook is unchanged this cycle; only forward-coverage tests
  landed. The accurate status: **M2.1 reclassified as Carry-over to
  Cycle #3 under the handle `M2.1-hook-write`** per CLAUDE.md §6.7
  step 8a (partial-defect audit), added in commit `4550cfd` and
  applied retroactively to Cycle #2 in this update. `cycle-02/JUDGMENT.md`
  §8 M2.1 row now states "Carry-over to Cycle #3 (handle:
  M2.1-hook-write)". **M2.2** remains structurally mitigated by
  JUDGMENT.md §7 porting-decision table. **`/refine` non-firing** for
  single-file reasoning — resolved in Cycle #1 post-run and verified
  firing in Cycle #2.

**Post-cycle ROOT note (2026-04-21 PM).**
- The G5 integrity axis for B's evaluator was attempted as a direct
  edit to `projects/b/.claude/agents/evaluator.md` (the natural
  landing site for a standing scorer rule). The edit was blocked by
  the environment's sensitive-file policy, which extends to any
  `.claude/**` path including sub-project `.claude/` trees — broader
  than the `.claude/hooks/**` + `.claude/settings.json` scope
  observed during Cycle #2. Full specification of the evaluator.md
  "Integrity ordering" insert is available in the session transcript
  for out-of-session landing, alongside the M2.1 hook + settings
  edits. The TASK.md §7 channel is the interim delivery path and is
  sufficient for Cycle #3's refinement run per JUDGMENT §7.3's own
  guidance.
- The cycle-03/TASK.md §3 paper-leak-guard pattern extension for
  Cycle #3-specific identifiers (SUBLEQ, Minsky, etc.) is noted as
  bundled into the M2.1-hook-write carry-over: both the M2.1 guard
  rewrite and the pattern extension touch `.claude/hooks/**` and
  are therefore subject to the same sensitive-file policy. The
  post-cycle grep-only audit in `cycle-03/TASK.md` §4 is the
  compensating control until the policy is lifted.
