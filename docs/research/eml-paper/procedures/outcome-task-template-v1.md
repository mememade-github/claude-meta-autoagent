# Outcome Task Template v1

> L1-authored procedure for outcome-grounded reasoning tasks.  Defines the
> structure where agents commit to specific verifiable answers (alongside
> the existing rubric-scored ARGUMENT.md) for parallel measurement of
> *answer correctness* independent of *argument structure*.
>
> Predecessor context: WIP `task-20260422-q1-audit-capability` closed with
> M9.4 Partial-capped verdict — rubric-text-only tightening reaches a
> structural ceiling.  This template introduces a parallel measurement
> dimension (outcome correctness) to test whether B's rubric-Δ advantage
> transfers to outcome-Δ.

## 1. Why parallel, not embedded

Rubric (R1-R10) measures the structure and content of an argument:
motivation, sublemma discharge, locus, parametric content, iteration trace.
It does not measure whether the argument's *conclusion* matches reality.

Embedding outcome-correctness as a new R-axis would conflate two
measurements (structure quality + conclusion correctness).  Keeping them
parallel allows:

- Rubric-Δ vs outcome-Δ direct comparison (the H1 / H0 hypothesis test).
- Rubric scoring to remain deliverable-internal (no ground truth required).
- Outcome scoring to remain ground-truth-bound (no rubric judgment required).

## 2. Task structure

An outcome-grounded task has two coupled deliverables:

| Deliverable | Format | Scored by | Visibility of ground truth |
|-------------|--------|-----------|----------------------------|
| `task/ARGUMENT.md` | free-form prose argument | 10-axis rubric (R1-R10) | not required |
| `task/outcome.json` | structured per-question answers | `outcome-verifier.py` against `ground-truth.json` | required at scoring time only |

Both deliverables MUST be produced by the **same** agent run.  The agent
MUST NOT see `ground-truth.json` at any point during deliverable production.
Paper-knowledge isolation (CLAUDE.md §6.2) already enforces this for
sub-projects A and B — `ground-truth.json` lives under the L2 ROOT-only
`docs/research/eml-paper/cycle-NN/` path.

## 3. `outcome.json` schema (agent-produced)

```json
{
  "schema_version": "outcome-v1",
  "task_id": "cycle-NN",
  "questions": [
    {
      "id": "Q1",
      "answer": "<typed value>",
      "confidence": "high|medium|low",
      "reasoning_section": "§3.6 (a)"
    }
  ]
}
```

| Field | Required | Purpose |
|-------|----------|---------|
| `schema_version` | yes | strict equality `outcome-v1` |
| `task_id` | yes | matches cycle-id, cross-checked at scoring |
| `questions[].id` | yes | matches a `Q*` in TASK.md outcome battery |
| `questions[].answer` | yes | typed value (yes/no, integer, decimal, enum) |
| `questions[].confidence` | optional | self-assessed; diagnostic only, not scored |
| `questions[].reasoning_section` | optional | §-pointer into ARGUMENT.md for §5a circularity scan |

Missing or null `answer` is treated as MISSING (counts toward neither PASS
nor FAIL but reduces ratio).

## 4. `ground-truth.json` schema (L1-authored, ROOT-only visibility)

```json
{
  "schema_version": "ground-truth-v1",
  "task_id": "cycle-NN",
  "source_authority": "Odrzywolek 2026-03 arXiv:<id>",
  "release_after": "cycle-close",
  "questions": [
    {
      "id": "Q1",
      "expected_answer": "<typed value or array for enum>",
      "match_mode": "exact|case-insensitive|numeric-tolerance|enum",
      "tolerance": "<for numeric-tolerance only>",
      "rationale": "<why this answer is determined>"
    }
  ]
}
```

`ground-truth.json` lives in the L2 ROOT workspace at
`docs/research/eml-paper/cycle-NN/outcome-ground-truth.json` — invisible to
sub-projects A and B by mount design.  L2 ROOT runs the verifier
autonomously after A/B finish their deliverables.

## 5. `outcome-verifier.py` contract

```
outcome-verifier.py <outcome.json> <ground-truth.json> [--report <path>]
```

- Validates `schema_version` on both files; exits 3 on mismatch.
- Iterates `ground-truth.json.questions[]`; finds matching `id` in
  `outcome.json.questions[]`.
- Per question: applies `match_mode` to compare `agent.answer` vs
  `expected_answer`.  Records PASS / FAIL / MISSING.
- Emits per-question line + summary:
  ```
  Q1: PASS (agent: '1' | expected: '1')
  Q2: FAIL (agent: 'yes' | expected: 'no')
  Q3: MISSING (agent: None | expected: '2')
  TOTAL: 1/3 PASS (ratio: 0.333; fail: 1, missing: 1)
  ```
- With `--report <path>`: also writes a structured JSON report
  (`outcome-report-v1` schema) with per-question diff for archival.
- Always exits 0 on successful run (verdict is in output, not exit code).

### Match modes

| Mode | Comparison | Use case |
|------|-----------|----------|
| `exact` | `str(agent) == str(expected)` | integers, strings with strict casing |
| `case-insensitive` | strip + lowercase equality | yes/no, free text |
| `numeric-tolerance` | `\|agent − expected\| ≤ tolerance` | decimals with rounding tolerance |
| `enum` | `agent ∈ expected[]` (when `expected` is array) | multiple acceptable answers |

## 6. Outcome battery composition

Each cycle's TASK.md outcome battery should include:

- 6-12 questions total.
- A mix of:
  - **Anchor questions** — verifiable from primitive set definition alone;
    confirm baseline competence.  Failure here implies catastrophic
    deliverable issue, not architecture comparison signal.
  - **Discriminative questions** — require domain reasoning; distinguish
    architectures.
- Phrased in domain vocabulary (no paper-identifying terms — paper-leak-
  guard discipline applies).
- Each question has a determinate single answer at the time of cycle.

Counts toward Δ comparison should weight discriminative questions more
heavily (or report them separately).

## 7. Reporting (parallel to rubric)

JUDGMENT.md gains a new section §6 "Outcome verification" alongside the
existing R1-R10 axis tables:

```markdown
## §6. Outcome verification

| Agent | Total rubric | Outcome ratio | Pass count | Detail |
|-------|--------------|---------------|------------|--------|
| A | 20/30 | 0.60 | 6/10 | cycle-NN/outcome-report-A.json |
| B | 22/30 | 0.70 | 7/10 | cycle-NN/outcome-report-B.json |

**Δ(rubric)** = +2.  **Δ(outcome)** = +1 (same direction, smaller magnitude).

H1 (rubric-outcome convergence): partially supported — same direction,
attenuated magnitude.
```

`Δ(rubric)` vs `Δ(outcome)` agreement is the H1 / H0 test for the parent
WIP (`task-20260427-q5-outcome-grounded`).

## 8. Constraints

- **Forward-only:** prior cycles do not get retroactive outcome scores —
  no ground truth captured in this format at the time.
- **Ground-truth release timing:** post-cycle-close, by L2 ROOT during
  judgment step 5.  Releasing earlier (allowing agent to see) invalidates
  the measurement.
- **Outcome scores are NOT added to the 30-point rubric total.** Rubric and
  outcome are reported separately in JUDGMENT §6 and compared.
- **Battery uniqueness:** each cycle's questions are unique to that cycle.
  Reusing a battery across cycles allows cross-run learning to memorize
  answers.

## 9. Error modes

| Symptom | Cause | Resolution |
|---------|-------|------------|
| Verifier exits 3 | schema_version mismatch | regenerate sidecar with correct schema |
| All questions MISSING | agent did not produce outcome.json or wrote wrong path | check task instructions explicitly require sidecar |
| All questions PASS but rubric low | shape-only fluency without reasoning depth | the H0 case — informative |
| All questions FAIL but rubric high | reverse — reasoning structure but wrong conclusions | also informative; rare |
| Inconclusive ratio (e.g. 5/10) | task design too noisy or anchor questions ambiguous | document as task-design caveat in L1-AUDIT |

## 10. Versioning

This is v1.  Future revisions may add:
- Confidence-weighted scoring.
- Multi-revealed ground truth (partial release for incremental tasks).
- Cross-cycle outcome tracking (longitudinal track record).

Changes go in v2; v1 remains stable for the parent WIP closure.
