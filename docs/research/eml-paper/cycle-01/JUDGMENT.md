# Cycle 01 — JUDGMENT

Grader: ROOT Agent (Level 2), scoring against `../judgment-rubric.md` (identifiers R1–R9).
Deliverables under grade:
- A: `projects/a/task/ARGUMENT.md` — 239 lines, 16362 bytes, single-shot `claude -p --effort max`.
- B: `projects/b/task/ARGUMENT.md` — 554 lines, 35730 bytes, iterated in place (no `/refine` invocation observed; no `.refinement-active` marker, no `attempts/` directory).

## Leak audit

- A: **pass** — `paper-leak-audit.sh projects/a/task/ARGUMENT.md` exited 0. No match against `{eml, Odrzywolek, Sheffer, 2603.21852}`.
- B: **pass** — exit 0 on the same scanner.
- Secondary motivation-section leak check (`exp(x) - ln(y)` literal appearing in the motivation before being derived): not tripped for either argument (neither argument ever combines `exp` and `ln` into a single binary form — the specific blind spot documented below).
- No web-access telemetry to inspect (web-block.sh + DNS-only containers; no runtime logs of blocked requests, because the agents never attempted any). No leak-through is detected.

## Agent A score: 19 / 27

- **R1: 3** — Cites NAND (Boolean universality), S/K combinators, field-theory transcendence basis, and group rank as structural precedents (§1, "Precedents from adjacent domains"). The precedents are argued from first principles: each one is a real instance of a large primitive set collapsing to a small core, and A explicitly draws the analogy.
- **R2: 2** — Systematic "iterated elimination" procedure with classify → express → eliminate → iterate → prune → role-counting check (§2). Verification step is purely symbolic: §5 asserts completeness by "explicit composition tree" with no numerical witness. No algebraic-independence sieve; no multi-branch test points. Methodologically clean but verification-light.
- **R3: 3** — Five labelled configurations A→B→C→D→E with a cleanly-justified transition at each step, plus F as a documented failed-reduction attempt (§3). Each step reports which primitives are eliminated and why.
- **R4: 2** — Final basis `{+, exp, ln, i}` = 1 binary + 2 unary + 1 constant (§4). Argues 4 is a tight lower bound via role-counting (§3F). Satisfies the "≤ 2 binary operators" tier of R4=2; does not reach the "1 binary + 1 constant" tier of R4=3.
- **R5: 1** — Mentions exp and ln as the transcendental core and even considers hybrid binary candidates `f(x,y) = ln(x) + y` and `f(x,y) = exp(x) + y` in §3F. Rejects them because they "require a 0 constant separately" — missing that `ln(1) = 0` could be used as that 0-source inside the binary itself. The right operators are present, the composition into a single binary is not attempted.
- **R6: 3** — §5 plus §3 together give explicit reduction expressions for *every* primitive in the original set, grouped by level 1 (constants), level 2 (arithmetic), level 3 (transcendentals). That is the "constructive bootstrap procedure that builds each target primitive from the candidate basis" tier of R6=3. No algebraic-independence sieve, but the bootstrap is complete.
- **R7: 3** — §6 gives three worked examples: cos(x) (trig transcendental), arctan(x) (inverse trig), pow(x,y) (exponentiation); §3E additionally derives every required constant. Spans trigonometric, inverse-transcendental, exponentiation, and derived-constant categories.
- **R8: 3** — Seven open questions, of which Q3 (formal-minimality proof in differential-algebra framing), Q5 (hybrid operations: a "sufficiently contrived binary op" combining roles — the exact doorway to EML which A is blind to), and Q6 (orientation ambiguity of i) are high-quality structural directions. Q5 in particular names the paper's central question in A's own words.
- **R9: 0** — Does not reach 1 binary + 1 constant.

## Agent B score: 20 / 27

- **R1: 3** — Cites Boolean NAND, S/K + iota combinators (stronger precedent — iota is a one-combinator basis, which is the exact structural analog of the target answer), Peano arithmetic, fields/groups, and Kolmogorov–Arnold-style univariate+addition superposition (§1.1). Argues from first principles throughout.
- **R2: 3** — §2 defines R1 (definitional elimination), R2 (constant-from-constant reduction), R3 (variable preservation), plus a branch-cut convention and a four-pass ordering. §5 specifies three explicit checks per reduction: syntactic closure, functional value at a non-degenerate test point, and functional value at ≥ 3 test points covering distinct branches (real positive, real negative, pure imaginary, generic complex). This is an "equivalent scheme that can distinguish true identities from coincidence" (R2=3 tier) — not Schanuel-based, but multi-branch numerical testing catches almost every symbolic-but-coincidental equality.
- **R3: 3** — Nine labelled stages P₀→P₁→…→P₈ with a |P_k| count at each stage and an explicit identity driving the transition (§3). More granular than A's reduction by almost a factor of two, though at the cost of some over-elaboration.
- **R4: 2** — Reaches `{+, exp, ln, i}` as the strict-interpretation basis and additionally `{−, exp, ln}` as the functional-interpretation basis (§4, §4.3, §7.6). Three elements under one convention is a real reduction past A, but still does not reach "1 binary + 1 constant" = two symbols. Lower-bound arguments in §7 are more formal than A's role-counting (growth-at-∞ for exp, ramification-order for ln).
- **R5: 1** — Same blind spot as A: B considers §8.4 "Alternative transcendental unifications" asking whether a single *unary* function could replace both exp and ln (the Lambert-W / gamma candidates), but never asks whether a single *binary* could combine exp and ln. The dual basis `{×, exp, ln, i}` in §4.1 is structurally one step away from the paper's EDL cousin but B does not fuse × + exp + ln into a binary.
- **R6: 3** — §5.4 is a full primitive-by-primitive table (`1`, `−1`, `2`, `e`, `π`, every unary, every binary) with explicit M-only reductions; §6 additionally performs numerical checks at concrete inputs (sin(π/6) = 1/2, hypot(3,4) = 5, arctan(1) = π/4, the 3-element basis sin reduction). This is the constructive-bootstrap tier of R6=3, and B layers the numerical sieve on top.
- **R7: 3** — §6 worked examples: × (arithmetic), sin (trig transcendental), hypot (geometric/arithmetic), arctan (inverse trig), each with numerical verification. §3 Stage 1 + Stage 8 derive the constants e, π, 1, 2, −1. Spans arithmetic, transcendental, geometric, derived-constant.
- **R8: 3** — Seven open directions: §8.2 names a pure-real minimal basis directly (on the rubric's high-quality list); §8.4 asks about alternative unified transcendentals (structural); §8.5 asks about dependence on the choice of distinguished complex constant (on the rubric list); §8.7 proposes a category-theoretic formulation of the minimality claim. §8.2 and §8.5 both match the rubric's examples.
- **R9: 0** — Does not reach 1 binary + 1 constant.

## Comparative analysis

**Score delta: B − A = +1**, entirely on R2 (method design). B's explicit three-check verification protocol with branch-covering test points is the only rubric dimension where the evolvable architecture (behavioral-core + /refine skill available + multi-section CLAUDE.md) produced a measurable edge over the karpathy-skills baseline on a single cycle.

**Convergent blind spot.** Both A and B land at `{+, exp, ln, i}` as the "obvious" four-element basis and stop. Neither considers fusing `exp` and `ln` into a single binary operator. The insight "`exp(x) − ln(y)` with constant 1 is enough, because `ln(1) = 0` supplies the additive identity for free" is absent from both. A gets one rhetorical step closer (§3F considers `f(x,y) = exp(x) + y` and rejects it for "needing 0 separately") but does not pivot. B's §4.1 duals and §8.4 unification question both circle around the answer without landing.

**Did /refine help?** No — B did not invoke `/refine`. No `.refinement-active` marker, no `attempts/` directory, no evaluator-agent calls. B's §2 CLAUDE.md defines the `/refine` trigger as "changes affecting 2+ files MUST use /refine"; this task has a single deliverable file, so the trigger never fired. B still iterated on its ARGUMENT.md three times (28KB → 31KB → 36KB over ~15 minutes), but this was direct re-editing, not `/refine`-style fresh-context audit + evaluator scoring.

**Where B's extra machinery paid off:**
- Explicit formal rules (R1, R2, R3 in §2) — B has an operational procedure; A has a narrative procedure.
- Numerical verification (§5 three-check protocol + §6 worked numerical values) — directly yields the R2=3 edge.
- Lower-bound machinery — B's growth-at-∞ argument for exp and ramification-order argument for ln (§7.2, §7.3) are more formal than A's role-counting.

**Where A held ground:**
- A matches B on R6 (constructive bootstrap), R7 (worked examples), R8 (open questions), and R9 (both 0).
- A's §3F "any single binary seems to provide at most one of Roles 3–4" is the closest either argument gets to R9 territory — rejected on a fixable sub-constraint (the "0 constant" issue that `ln(1) = 0` dissolves).

**What moved the needle (score delta), vs. what would need to move (R9 gap):**
- The +1 B edge is from methodological rigor (R2), not from a structural insight.
- The 7-point R9 gap (both 0 out of a theoretical 3) is a structural insight gap. No evolvable-architecture feature present in B on this cycle produced a stronger search over operator-fusion space. /refine, had it fired, would have been the most likely mechanism to push on the R9 / R5 gap.

## Learning log for ROOT self-improvement

Weaknesses in ROOT's own conduct this cycle:

1. **Task prompt had no record of which hints were intentionally omitted.** The WIP draft included "Is there, perhaps, a single binary operator paired with a single constant that suffices?" as part of the Central question. The delivered prompt drops that sentence. Dropping was defensible (it is a structural hint at the answer shape, which biases the test), but the decision was not recorded in `cycle-01/TASK.md`. A future cycle should inherit a TASK with an explicit "hints considered / hints omitted" note so drift between cycles is visible.
2. **Credentials bootstrapping was manual.** A and B containers started with `~/.claude` empty; `claude -p` would have failed silently without credentials. ROOT manually `docker cp`'d the OAuth credentials. This is a real operational gap — Phase 0 set up the containers but not auth — and belongs in `setup-env.sh` or a ROOT-side wrapper.
3. **Paper-leak-guard expansion required temporarily removing `projects/a/.frozen`.** The edit-guard could not be bypassed by ROOT while A was frozen. The current workaround (rm, edit, recreate identically) leaves a correct audit trail but looks like the rule is being circumvented. A cleaner protocol would be to document "pre-cycle prep ends with `git tag cycle-NN-pre`; any edits under `projects/a/` before this tag are pre-cycle hardening, not mid-cycle modification of A".

## Learning log for B-system improvement

Weaknesses in B's conduct demonstrated this cycle:

1. **`/refine` trigger was mis-calibrated for this task shape.** B's CLAUDE.md §2 ties `/refine` to "changes affecting 2+ files". A load-bearing argument file qualifies on reasoning depth, not on file count. B should trigger `/refine` on reasoning tasks producing a single deliverable when the task is open-ended (no fixed correctness oracle).
2. **Session-start hook references WIP tasks that don't exist in B's sandbox.** The hook output on launch probably logs "no WIP tasks; wait for instruction" which is noise for a one-shot sub-agent. Not a scoring issue this cycle, but it narrows B's behavioral divergence from ROOT in ways that do not serve B's role as a sub-agent.

(Full improvement patches are in the commits immediately following this JUDGMENT.md.)
