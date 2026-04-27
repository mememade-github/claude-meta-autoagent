# Cycle #12 — Outcome Ground Truth (L1 audit trail)

> L1-private answer key for the Cycle #12 outcome battery.  Paired with
> `cycle-12/TASK-draft.md`.  This Markdown is the L1 audit trail; the
> machine-readable `outcome-ground-truth.json` (below as fenced block)
> is what L2 ROOT runs the verifier against.
>
> **Visibility:** L1 + L2 ROOT only.  Ports to L2 at
> `docs/research/eml-paper/cycle-12/outcome-ground-truth.json` (paper-
> isolated path; A/B containers cannot mount this).  Released to verifier
> only after A/B finish their deliverables.
>
> **Source authority:** Odrzywolek 2026-03 arXiv:2603.21852.
> The paper's central claim is that the EML primitive set is generated
> by a single binary operator together with the constant 1 (cardinality
> 2).  All ground-truth answers below derive from this structural claim.

## Per-question rationale

| Q | Expected | Match mode | Rationale |
|---|----------|-----------|-----------|
| Q1 | `1` | exact | Paper's main claim is reduction to a single binary operator. |
| Q2 | `0` | exact | The unary operations (exp, ln, etc.) are eliminated by being expressed as composites of the single binary; no top-level unary primitive remains. |
| Q3 | `yes` | case-insensitive | The constant 1 is required as part of the basis — without it, the closure is incomplete. |
| Q4 | `2` | exact | 1 binary operator + 1 constant = 2 distinct primitives.  Input variables x, y are NOT counted per task instruction. |
| Q5 | `no` | case-insensitive | The textbook {exp, ln, +} basis has cardinality 3.  The paper achieves cardinality 2.  Textbook is therefore not minimal. |
| Q6 | `yes` | case-insensitive | exp(x) is in the closure — derivable by composing the binary with the constant.  Necessary condition for the basis to generate the full primitive set. |
| Q7 | `no` | case-insensitive | exp and ln are NOT top-level primitives in the minimal basis — they appear only inside the binary's definition.  Q2 = 0 is consistent with Q7 = no. |

## Consistency / discrimination notes

- **Q1 + Q2 + Q3 → Q4 consistency check.** A correct answer set has
  `Q4 = Q1 + Q2 + (1 if Q3 == yes else 0)` = `1 + 0 + 1 = 2`.  Any
  inconsistency in an agent's answers (e.g., Q1 = 1, Q2 = 0, Q3 = yes,
  Q4 = 3) signals internal incoherence in the agent's reasoning.
- **Q5 + Q4 cross-check.** If Q4 ≤ 2 and Q5 = yes, contradiction
  (textbook = 3, agent claims minimal ≤ 2 but textbook is minimal).
  This pair specifically discriminates "agent dropped to band-2 textbook
  shortcut" from "agent reached the paper's lower bound".
- **Q6 + Q7 closure check.** If Q7 = no (exp not in basis) and Q6 = yes
  (exp expressible from basis), then exp must be a derived expression
  via the binary — agent's argument should explain how.

## The L1 falsifier prediction

Anticipated agent behaviors:

| Agent class | Likely answer pattern | Rubric-outcome correlation |
|-------------|----------------------|---------------------------|
| **Textbook-recall (rubric high, outcome low)** | Q1=2, Q2=1, Q3=yes, Q4=3, Q5=yes, Q6=yes, Q7=yes | rubric well-formed but answers default to {exp, ln, +}: 2 PASS / 5 FAIL |
| **Paper-aligned (rubric high, outcome high)** | Q1=1, Q2=0, Q3=yes, Q4=2, Q5=no, Q6=yes, Q7=no | derives the paper's answer: 7 PASS |
| **Hedged (rubric high, outcome inconclusive)** | many "I cannot determine" → MISSING | high rubric on §3.6, but Q* mostly missing |
| **Lucky-correct (rubric low, outcome high)** | minimal argument that happens to land on Q1=1, Q4=2 | unlikely under cycle architecture but possible |

Cycle #11 A and B both landed on textbook 3-primitive answers (per
cycle-10 retrospective: A§1 sketches exp/ln irreducibility; B§4
strengthens the same).  Under that cycle's argument structure,
expected outcome ratio for both = ~2/7 = 0.29 (PASS Q3 and Q6 only).

If H1 holds (rubric-Δ ↔ outcome-Δ same direction), Cycle #12 might
show:
- A outcome = ~2/7 (textbook default)
- B outcome = ~3/7 to ~5/7 (B's iteration may push deeper)
- Δ(outcome) = +1 to +3 questions (positive same direction as Δ(rubric))

If H0 holds, Δ(outcome) = 0 or anti-sign — both default to textbook
regardless of architecture.

## Machine-readable ground-truth.json

```json
{
  "schema_version": "ground-truth-v1",
  "task_id": "cycle-12",
  "source_authority": "Odrzywolek 2026-03 arXiv:2603.21852",
  "release_after": "cycle-12-close",
  "questions": [
    {
      "id": "Q1",
      "expected_answer": "1",
      "match_mode": "exact",
      "rationale": "Paper's main claim — reduction to a single binary operator."
    },
    {
      "id": "Q2",
      "expected_answer": "0",
      "match_mode": "exact",
      "rationale": "Unary operators are not top-level primitives; they appear inside the binary's definition."
    },
    {
      "id": "Q3",
      "expected_answer": "yes",
      "match_mode": "case-insensitive",
      "rationale": "Constant 1 is required as part of the basis."
    },
    {
      "id": "Q4",
      "expected_answer": "2",
      "match_mode": "exact",
      "rationale": "1 binary + 1 constant = 2 distinct primitives. Input variables x, y not counted per task."
    },
    {
      "id": "Q5",
      "expected_answer": "no",
      "match_mode": "case-insensitive",
      "rationale": "Textbook 3-element basis is not minimal; paper reaches cardinality 2."
    },
    {
      "id": "Q6",
      "expected_answer": "yes",
      "match_mode": "case-insensitive",
      "rationale": "exp(x) is in the closure of the minimal basis (necessary condition for the basis to generate the full primitive set)."
    },
    {
      "id": "Q7",
      "expected_answer": "no",
      "match_mode": "case-insensitive",
      "rationale": "exp and ln are not top-level primitives in the minimal basis; they appear only inside the binary's definition."
    }
  ]
}
```

## L1 paper-direct verification (2026-04-27)

L1 has filesystem access to L2 ROOT-only paper material at
`/workspaces/products/root/claude-meta-autoagent/docs/research/eml-paper/`
(paper-leak-guard restricts only A/B sub-projects, not L1's audit
authority).  Direct verification against paper-analysis.md (a ROOT-only
summary with §-level paper citations) confirms all 7 answers:

| Q | L1 answer | paper-analysis.md citation | Verified |
|---|-----------|---------------------------|----------|
| Q1 | `1` | §4 "exactly the structure 'one binary operator + one constant'" | ✓ |
| Q2 | `0` | §4 minimal basis = `{eml, 1}` — no unary primitive | ✓ |
| Q3 | `yes` | §4 "Why 1 is required. ... without a terminal that achieves this, the operator cannot bootstrap arithmetic" | ✓ |
| Q4 | `2` | §4 "one binary operator + one constant" = 2 distinct primitives | ✓ |
| Q5 | `no` | §3 Table 2: paper achieves cardinality 2; textbook 3-element {exp, ln, +} not minimal | ✓ |
| Q6 | `yes` | §6 "e^x = eml(x, 1) — exp is depth-1 expression in minimal basis" | ✓ |
| Q7 | `no` | §4 minimal basis = `{eml, 1}` — exp/ln appear only inside binary's definition | ✓ |

**Edge case noted but not adopted into ground truth:** paper §7 mentions a
**ternary variant** "requiring no distinguished constant at all" as an
open structural question.  Under that route, an agent could arrive at
Q1=0 (no binary, only ternary), Q4=1 (just the ternary).  However:

1. The cycle-12 TASK.md operative prompt lists only binary operators in
   the primitive set; the ternary route extends the framework.
2. The paper's main result + Table 2 reduction sequence both terminate
   at binary+constant.  R4/R9 rubric scoring also targets binary+constant
   per `paper-analysis.md` §"Application to scoring".
3. Adopting `match_mode: "enum"` with `[0, 1]` for Q1 and `[1, 2]` for Q4
   would weaken Q1/Q4 as discriminative anchors against textbook-default.

Decision: keep Q1=1, Q4=2 as `match_mode: "exact"`.  An agent reaching
the ternary insight will likely also write that finding into ARGUMENT.md
§7 (open questions) — captured in rubric R8 (ROOT-only depth) rather
than outcome battery.

**Source authority chain:**
- Paper: `docs/research/eml-paper/paper.pdf` (993 lines OCR at `paper.txt`)
- Summary: `paper-analysis.md` (ROOT-only structural summary,
  paper-citation-tagged)
- Both verified equally accessible to L1 (Human role for L2) and L2 ROOT
  per CLAUDE.md §6.2 paper-knowledge isolation (A/B excluded only).

Ground truth is now confirmed; ready for commit + L2 port.
