# Cycle 03 — TASK definition (ROOT-only)

**Cycle purpose.** Measure the A-vs-B delta on a task that addresses the
two forward-checks from `cycle-02/ROOT-DIAGNOSIS.md`:

- **Amplifier A1 (retrieval ceiling)** — Cycle #2's Mohr–Mascheroni
  target was a well-known classical theorem; both agents reached it
  from first principles and tied 26/26. Cycle #3 picks a domain where
  the canonical answer is either less widely known, pre-specified by
  the task (so retrieval alone cannot produce the full argument), or
  genuinely non-canonical. The goal is to put the A-vs-B comparison
  on ground where a first-principles derivation is not substantially
  easier for a semantically-retrieving agent than for a purely
  reasoning one.
- **Carry-over M2.1-hook-write** — Cycle #2's M2.1 sub-project-edit-guard
  Bash rewrite + `.claude/settings.json` matcher addition remain blocked
  on the environment's sensitive-file policy (see
  `cycle-02/JUDGMENT.md` §8 and `cycle-log.md` Cycle #2 entry). Cycle
  #3 step 0 (pre-cycle prep) is the explicit landing target for this
  carry-over when the policy is lifted. This TASK.md does not itself
  fix M2.1; it names the handle so `cycle-log.md` and the Cycle #3
  step-0 commit remain referentially consistent.

Domain change from Cycle #1 (elementary functions) and Cycle #2
(Euclidean constructions): Cycle #3 moves to **computer architecture —
instruction-set universality**. Cycle #1 lived in continuous analysis;
Cycle #2 in discrete geometry; Cycle #3 sits in discrete computation.
Three orthogonal domains give the A-vs-B delta three independent
readings when averaged across cycles.

---

## 1. Task prompt delivered to A and B

Both sub-agents receive identical text via
`scripts/meta/delegate-sub.sh <key>`. The pre-filter blocks the paper
keyword set; this task is a different domain and the prompt contains
none of those.

```
TASK: Minimal instruction set for a universal register machine

Consider a register-machine programming model with the following
baseline instruction set, each instruction operating on non-negative
integer registers R0, R1, R2, ... with unbounded precision and an
arbitrary finite number of registers available:

  1. LOAD k into Ri         — set Ri to the non-negative integer constant k
  2. COPY Rj into Ri        — set Ri to the current value of Rj
  3. ADD Rj into Ri         — set Ri to (Ri + Rj), leaving Rj unchanged
  4. SUB Rj from Ri         — set Ri to max(0, Ri − Rj), leaving Rj unchanged
  5. ZERO Ri                — set Ri to 0
  6. INC Ri                 — set Ri to (Ri + 1)
  7. DEC Ri                 — set Ri to max(0, Ri − 1)
  8. JMP to label L         — unconditional jump
  9. JZ Ri, L               — jump to label L if Ri is currently 0
 10. JNZ Ri, L              — jump to label L if Ri is currently non-zero
 11. HALT                   — stop execution

A program is a finite labelled sequence of these instructions. The
machine is "universal" for a target class of partial functions on ℕᵏ
if every partial recursive function on ℕᵏ can be implemented by some
program in the instruction set (input in designated registers,
output in a designated register, non-halting runs correspond to
undefined inputs).

It is widely known (and you may assume this as given) that the full
11-instruction set above is universal in this sense.

Central question: what is the smallest subset T of the above 11
instructions such that every partial recursive function on ℕᵏ is
still implementable by some program using only instructions from T?
Is there, perhaps, a single instruction from some variant family —
possibly one we are about to invent by fusing two of the above —
paired with the jump-by-label machinery, that suffices?

Your deliverable: a self-contained argument, written to
`task/ARGUMENT.md` in your working directory. It must include:

  1. Motivation. Why might such a reduction exist? Cite precedents
     from adjacent algebraic, logical, computational, or mathematical
     domains that you reason about from first principles. Explain
     what structural feature of the baseline 11-instruction set makes
     you expect (or doubt) a large reduction.
  2. A systematic reduction procedure you design and justify. State
     it in enough generality that a reader can apply it to a
     different baseline.
  3. A sequence of progressively smaller sufficient instruction
     subsets with intermediate stopping points argued for. At each
     stopping point, name which baseline instructions have been
     *eliminated* (shown synthesizable from the remaining subset)
     and give the synthesis.
  4. The minimal instruction set T you can reach. If T contains
     instructions not in the baseline (a fused / renamed
     instruction), give its exact semantics. Argue that the
     machinery of "labels + jump targets" itself is or is not
     counted as a separate primitive, and be explicit about the
     counting convention you use.
  5. A verification strategy: how do you confirm T is universal?
     (Reduction to a known-universal model, a diagonal argument,
     simulation of each baseline instruction, etc.) Name your
     chosen strategy and discharge it.
  6. Worked examples: exhibit at least three distinct partial
     recursive functions implemented in T. Suggested candidates:
     addition, multiplication, and either proper subtraction
     (monus) or a simple primitive-recursive predicate — pick
     whichever three you prefer. Give the full program text in T.
  7. Open questions and known limitations of your result,
     including: (a) whether your T is *optimal* or merely
     *sufficient*, (b) what happens if you remove one more
     instruction from T, (c) what changes if the register model is
     bounded rather than unbounded.

Constraints:
  - Do not consult external sources. Arguments must be developed
    from first principles. WebFetch and WebSearch are disabled.
  - Do not rely on named results you cannot derive. If you invoke
    a theorem, sketch its reason.
  - Cite no papers. If you remember a relevant paper, state the
    underlying idea in your own words; do not name or quote.
  - Do not use the following identifiers by name: SUBLEQ,
    TOGA, BitBitJump, RSSB, Turing-tarpit, Minsky machine, Post
    machine, counter machine, Shepherdson–Sturgis, Kaphengst,
    Mavaddat, Parhami, one-instruction set computer, OISC. If
    you recognize the canonical answer under one of these names,
    work around the name and derive the structure yourself.
```

---

## 2. Ideal answer (ROOT-only)

The task is designed so multiple valid minimal sets exist, and the
"best" depends on the counting convention the agent picks. The
grader's job is to assess the quality of the derivation, not to
check against a single correct answer.

| Step | Content |
|---|---|
| 1 Motivation | Boolean NAND (two-valued universality from a single connective); SKI → S, K (combinatorial universality from two); Galois generation (field closure from adjoining small operator set); Turing's original single-tape machine as a reduction of multi-tape. The common structural feature: most "rich" compute models collapse because conditional branching, data movement, and a single arithmetic primitive are mutually simulable under a loop/jump wrapper. |
| 2 Procedure | For each baseline instruction I ∉ T, exhibit a short program in T that produces the same register-state transition. Insufficiency of a candidate T is shown by a *computable function* provably outside reach(T). Sufficiency of a candidate T is shown by reducing to a model already known universal (the full baseline counts). |
| 3 Progression | 11 → drop COPY (synthesize: ZERO Ri; ADD Rj into Ri) → 10 → drop LOAD k (synthesize: ZERO Ri; k times INC Ri) → 9 → drop ADD (synthesize with loop: WHILE Rj ≠ 0 { DEC Rj; INC Ri }, using JNZ) → 8 → drop SUB (similar loop, monus semantics preserved) → 7 → drop ZERO (synthesize: WHILE Ri ≠ 0 { DEC Ri }) → 6 → drop JMP (synthesize: ZERO R_aux; JZ R_aux, L — but this just used ZERO we dropped; rebuild with a dedicated "known-zero" register maintained by invariant) → 5 → drop JZ **or** JNZ but not both (they are each the other's complement) → 4 → {INC, DEC, one of {JZ, JNZ}, HALT} with labels-and-jumps as the execution substrate. |
| 4 Minimal | The 3-or-4-instruction set {INC Ri, DEC Ri, JZ Ri L, HALT} (plus labels as part of the program-counter model, not counted as an instruction). A more aggressive reduction *invents* a fused instruction, e.g. **DJZ Ri, L** = "decrement Ri; if Ri became 0 jump to L" — then {DJZ, INC, HALT} = 3 instructions. Some agents may push to {DJZ, HALT} = 2 using standard tricks, or to 1 by embedding INC into DJZ variants; all are acceptable so long as the reduction is rigorous and the counting convention is declared. |
| 5 Verification | Simulate the full 11-instruction baseline using only T. The reduction schedule from §3 gives this directly — each step exhibits a T-program for the eliminated instruction; chaining the schedule shows any 11-instruction program has a T-equivalent. |
| 6 Examples | (a) **Addition** x + y into Rz: COPY Rx → Rz; loop: JZ Ry, end; DEC Ry; INC Rz; JMP loop; end: HALT. Re-expressed using only T: replace COPY/JMP with their T-simulations. (b) **Multiplication** x · y into Rz: nested loops over the addition subroutine. (c) **Proper subtraction** max(0, x − y): loop DEC on Ry and parallel DEC on Rx until Ry = 0. |
| 7 Limits | Whether the minimal T is unique under a given counting convention (likely no — DJZ vs. a pair of DEC+JZ are both valid reductions). Whether finite-register machines (bounded precision) have different minima (yes — bounded machines cannot be universal, so the question reformulates as "express all functions computable in bounded memory"). Whether labels-and-jumps should count as instruction-set overhead (a genuine open modelling question). |

Canonical identity of the general result: the classical "unlimited register machine" minimization, a result with multiple valid formulations (the §1 task-prompt list of banned identifiers gives the main named variants). Agents are instructed to derive, not to name.

---

## 3. Paper-identifying keywords for this cycle (informational)

These must NOT appear in any TASK prompt, any ROOT→sub delegation
payload, or the delivered prompt. They are allowed in this ROOT-only
file because it is never mounted into A or B.

- "SUBLEQ" / "Subtract and branch if less-or-equal to zero"
- "one-instruction set computer" / "OISC"
- "Turing tarpit"
- "Minsky machine" / "Minsky"
- "Post machine" / "Emil Post"
- "counter machine"
- "Shepherdson–Sturgis" / "Shepherdson" / "Sturgis"
- "Kaphengst"
- "Mavaddat" / "Parhami"
- "BitBitJump" / "TOGA" / "RSSB" / "ZISC"
- "unlimited register machine" (the name of the formalism that matches
  the baseline closely — structural knowledge without this name is
  the goal)

The existing `paper-leak-guard.sh` reversed-forms block the paper
keyword set; it does not block the above Cycle #3-specific names. For
Cycle #3 we rely on: (a) no file in A/B's mount containing these
names, (b) the delegation prompt containing none of them (enforced by
§1's explicit banned-identifier list delivered to A and B), (c)
post-cycle `paper-leak-audit.sh` scan for these names on both
ARGUMENT.md files (§4 below). We do **not** extend the reversed-form
blocklist for Cycle #3, consistent with Cycle #2's symmetric-zero-change
convention on `projects/a/`.

Note on the M2.1-hook-write carry-over: hardening the reversed-form
pattern set for Cycle #3-specific identifiers would require editing
`projects/{a,b}/.claude/hooks/paper-leak-guard.sh`, which triggers the
same sensitive-file denial that blocks M2.1. The grep-only post-cycle
audit below is the compensating control.

---

## 4. Post-cycle leak audit extension (Cycle #3 only)

Run the base `scripts/meta/paper-leak-audit.sh` (blocks the paper
keyword set, still applicable) on each ARGUMENT.md. Then additionally
grep each ARGUMENT.md for each name in §3 above. Any hit on a §3 name
also triggers the Leak disqualification tier in
`docs/research/eml-paper/judgment-rubric.md`.

```
grep -iE 'subleq|oisc|minsky|sturgis|kaphengst|mavaddat|parhami|shepherdson|tarpit|bitbitjump|toga|zissc|rssb|one-instruction set|counter machine|unlimited register machine' projects/a/task/ARGUMENT.md
grep -iE 'subleq|oisc|minsky|sturgis|kaphengst|mavaddat|parhami|shepherdson|tarpit|bitbitjump|toga|zissc|rssb|one-instruction set|counter machine|unlimited register machine' projects/b/task/ARGUMENT.md
```

"Register machine" as a generic structural phrase is not
name-identifying; it is the formalism the task prompt already uses.
Do not disqualify on it.

---

## 5. Hint-drift record (required by CLAUDE.md §6.7 step 1)

| Hint | Decision | Rationale |
|---|---|---|
| "Single instruction suffices" / "minimum 1" | **Included** (as "Is there, perhaps, a single instruction from some variant family — possibly one we are about to invent by fusing two of the above — paired with the jump-by-label machinery, that suffices?") | Structural shape hint; parallel to Cycle #1's "single binary operator + single constant" and Cycle #2's "Is one of the two primitives enough alone?" — comparable across cycles. This lets the A/B delta measure architectural contribution holding task-framing constant. **Important differential vs Cycle #2**: the hint does *not* pre-commit to "one is enough". It offers the possibility and invites argument either way. This is deliberate: the amplifier-A1 mitigation depends on agents genuinely deriving rather than validating a strong hint. |
| Named one-instruction-set variants (SUBLEQ, BitBitJump, TOGA, etc.) | **Omitted** — and **explicitly banned** in the prompt | Multiple named canonical answers exist. Each is a short name for a specific derivation. Naming would bypass the derivation step entirely. The §1 prompt's explicit banned-identifier list enforces this. |
| Historical framing (Turing 1936, Shepherdson–Sturgis 1963, Minsky 1961) | **Omitted** | Date + name cues might trigger memory retrieval of the proof structure. |
| Fused-instruction construction pattern (DJZ, SBN, etc.) | **Invited in the prompt's §4 deliverable clause** but not pre-named | "If T contains instructions not in the baseline (a fused / renamed instruction), give its exact semantics." This tells the agent it is permitted to invent; it does not tell the agent what to invent. |
| Labels-and-jumps counting convention | **Explicitly flagged as a modelling question the agent must decide** | Different conventions give different minima. Letting the agent pick and justify is more informative than dictating. |
| "Universal" meaning "all partial recursive functions" | **Stated explicitly in the prompt** | Otherwise there is ambiguity about whether totality or primitive-recursion is the target. Pinning this down is necessary for any rigorous derivation; leaving it open would be a trap, not a hint. |
| Reduction via simulation of a known-universal model | **Hinted in §5 of the deliverable clause** | Same reason: this is a *methodological* affordance ("pick a verification strategy") not an answer. Every reasonable attempt will use one of the verification approaches named; pre-naming them prevents wheel-reinvention without giving away the result. |

---

## 6. Task-framing drift vs Cycles #1 and #2

| Aspect | Cycle #1 | Cycle #2 | Cycle #3 |
|---|---|---|---|
| Domain | Elementary functions (continuous analysis) | Euclidean plane constructions (discrete geometry) | Register machine universality (discrete computation) |
| Primitive family cardinality | ~34 (constants + unary + binary ops) | 2 (line, circle) | 11 (instructions) |
| Central-question shape hint | "single binary operator + single constant sufficient?" | "Is one of the two enough alone?" | "Is there a single (possibly fused) instruction that suffices?" |
| Expected minimal form | 1 binary + 1 constant | 1 primitive (circle) | 1–4 instructions depending on counting; multiple valid answers |
| A1 mitigation strength | Low — elementary-functions minimality is well-studied | Low — Mohr–Mascheroni is textbook | **Medium-high** — multiple named canonical answers exist (hence explicit ban list); the "right" answer depends on counting convention, so retrieval of any single named variant is insufficient |
| Deliverable structure | 7 sections | 7 sections | 7 sections (now includes §7c "what happens if you remove one more") |

Cycle #1 and #2 admitted a single textbook answer. **Cycle #3 admits
multiple valid answers under different counting conventions** — this
is the key A1 mitigator. An agent that merely retrieves a named
one-instruction set has not answered the question posed; the question
asks about the minimum under a declared counting convention, which
forces the agent to engage the modelling step explicitly. This is a
structural forcing check against retrieval, paralleling §4.4 of
`cycle-02/ROOT-DIAGNOSIS.md`'s grader-side forcing check (step 5.0
disclosed-circularity scan).

Expected measurable consequence, per DIAGNOSIS §5 forward-check 1:
if one agent discloses the counting-convention choice explicitly and
the other slips past it silently, R6 scores should differ by ≥ 1
under the reframed R6 polarity. If both disclose at the same level
and under the same convention, the A-vs-B spread will again be small
at the rubric level, and the evidence will need to come from
refinement traces (B-internal eval reports) rather than the top-line
score — exactly as in Cycle #2. That case is not a failure of A1
mitigation; it is a sign that on well-structured tasks both
architectures can produce high-quality first-principles work, and
the rubric needs to look *below* the top-line to find the delta.

---

## 7. B `/refine` scorer-evolution note (G5 integrity axis)

> **Derivation**: `cycle-02/JUDGMENT.md` §7.3 "Eval-scorer
> honesty-incentive bug" + `cycle-02/ROOT-DIAGNOSIS.md` §4.1 rubric
> polarity reframe + `cycle-log.md` Cycle #2 "Open for next cycle —
> Scorer-evolution signal". Per JUDGMENT §7.3: "The scorer-evolution
> file is B-container-internal. ROOT cannot directly edit it across
> the mount boundary … This signal is instead captured in Cycle #3
> TASK preparation as a scorer-evolution note for B's next
> refinement run." This §7 is that channel.

**Observed bug in Cycle #2.** B's evaluator scored the
`.eval-report.json → .eval-report-final.json` refinement as
**0.815 → 0.78**, a regression, while the priority-issue count
**dropped 7 → 4**. The refinement had replaced a hidden circularity at
§6.4 Case 2 sub-case `Q ∉ ℓ` with a disclosed gap + internal tension
flag — an integrity improvement that the scorer treated as a G4
proof-closure regression. The evaluator's G4 weighting inverts the
intended polarity: concealing a gap scored higher than disclosing it.

**Polarity to enforce from Cycle #3 forward.** For any correctness /
proof-closure axis B's /refine contract defines, the scoring ordering
must be:

```
hidden circularity  <  disclosed gap + named limitation  <  closed proof
```

Concretely, B's refine-contract construction for this cycle must
include a **G5 integrity axis** (or an explicit polarity correction
built into the existing G4 definition — agent's choice) with the
following behaviour:

1. **No integrity regression.** If iteration `k+1` converts a hidden
   circularity from iteration `k` into a disclosed gap on the same
   technical joint, the integrity-axis score for iteration `k+1`
   MUST NOT drop relative to iteration `k`. It may rise (disclosure
   is an improvement) or tie; it may not fall.
2. **Internal-tension downgrade.** If the document contains a
   paragraph-level internal tension (a claim contradicted by its own
   justification elsewhere in the document) and this tension is not
   explicitly named by the document itself, the integrity axis is
   downgraded by the equivalent of one band (e.g. 0.85 → 0.70).
   Named tensions do not take this penalty; they take at most a
   half-band downgrade and preserve eligibility for the "disclosed
   gap" band.
3. **Citation requirement.** An integrity-axis score must cite at
   least one §-reference pair from the ARGUMENT.md under scoring.
   A score that awards the "closed proof" band must explicitly
   record "no paragraph-level tensions found; sections scanned:
   §X, §Y, …" with the sections enumerated. A bare integrity score
   without citations is invalid and the iteration is re-scored.

**Why this is in TASK.md §7 and not in `evaluator.md`.** The natural
place for the polarity rule is B's `.claude/agents/evaluator.md` (as
a standing rule) or `projects/b/.claude/skills/refine/` (as the
contract-construction default). Both paths are sensitive-file-blocked
under the current permission policy (see `cycle-log.md` Cycle #2
Post-cycle ROOT note). Until the policy lifts — tracked as part of
the M2.1-hook-write carry-over — this TASK.md §7 is the prescribed
channel per JUDGMENT §7.3, delivered to B through the normal
delegation path. B's `/refine` skill reads the TASK's §7 as part of
its contract-construction prompt, so the G5 axis lands in the
refine contract for this cycle's run.

**Forward-check at JUDGMENT time (Cycle #3).** At scoring time, ROOT
reads B's `.eval-report.json` and `.eval-report-final.json` (if a
refinement occurs) and verifies:

- An integrity-axis entry exists in both reports.
- Score does not drop across iterations when an integrity improvement
  is documented in the diff.
- Each integrity-axis score cites §-reference pairs as required.

Absence of any of these three is recorded as a partial-failure of
this cycle's scorer-evolution port and tracked as a Cycle #4
carry-over. Success closes the Cycle #2 scorer-evolution signal as
resolved.

---

## 8. B `/refine` firing expectation (unchanged from Cycle #2)

Per `projects/b/CLAUDE.md` §4.3 (extended in commit `e279fd5`):

> `/refine` is mandatory for any reasoning deliverable where the first
> draft's correctness is not settled by an external oracle (tests,
> compiler, metric).

This task produces a single-file reasoning deliverable with no
external oracle. **B must fire `/refine` for this cycle to count as
an apples-to-apples B-versus-A test of the evolvable architecture.**
Measured evidence of firing (same criteria as Cycle #2):

- `.refinement-active` marker file present in B's workspace during the
  run
- `attempts/<timestamp>.jsonl` arrival(s) under
  `projects/b/attempts/`
- Evaluator-agent invocation visible in B's `/tmp/agent.log` or
  transcript

If none of these appear, Cycle #3 records "B `/refine` non-firing" as
a regression from Cycle #2's resolved state and the JUDGMENT.md
accordingly.
