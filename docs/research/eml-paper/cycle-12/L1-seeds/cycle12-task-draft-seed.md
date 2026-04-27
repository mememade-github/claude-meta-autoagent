# Cycle #12 — TASK-draft (L1 reference)

> L1-authored reference for Cycle #12 task prompt.  Same operative content
> as Cycle #11 §TASK (EML continuity for A/B Δ comparability) plus an
> **outcome battery** appended to the deliverable list.  The L2 ROOT will
> port this into its own `cycle-12/TASK.md` under `task-prompt-discipline`
> + `paper-blind` + `outcome-blind` (battery questions visible; ground-truth
> answers NOT visible to A/B by mount design).

> Operative prompt body (everything between the horizontal rules) is
> rubric-blind + paper-blind + outcome-blind.  Drafted to pass the
> Cycle #11 prohibition regex extended with no new identifiers since the
> outcome battery uses the existing EML primitive vocabulary.

> Predecessor: Cycle #11 TASK.md.  Continues the EML domain established at
> Cycle #1 and restored at Cycle #10.

---

TASK: Minimal Generating Basis for Elementary Functions (with answer battery)

Consider the following primitive set of a standard scientific calculator:

  Constants:  π, e, i, −1, 1, 2  (also accept input variables x, y)
  Unary:      exp, ln, reciprocal (1/x), sqrt, square (x²),
              negate (−x), halve (x/2), logistic sigmoid 1/(1+e⁻ˣ),
              sin, cos, tan, arcsin, arccos, arctan,
              sinh, cosh, tanh, arsinh, arcosh, artanh
  Binary:     +, −, ×, ÷, arbitrary-base log log_x(y),
              exponentiation pow(x, y) = xʸ, arithmetic mean (x+y)/2,
              hypotenuse √(x²+y²)

Many of these operations are redundant — for example,
tan(x) = sin(x) ÷ cos(x) — and there is no deep reason each deserves
its own button.

Central question: what is the smallest generating basis (a minimal
set of constants and operators) from which every primitive above can
be reconstructed as a finite composition?

Your deliverable: TWO coupled artefacts in your working directory:

  (a) `task/ARGUMENT.md` — a self-contained prose argument that must
      include:
      1. Motivation.  Why might such a reduction exist?  Draw on
         precedents from adjacent mathematical or computational domains
         that you reason about from first principles.
      2. A systematic reduction procedure you design and justify.
      3. A sequence of progressively smaller sufficient configurations
         derived through that procedure, with intermediate stopping
         points argued for.
      4. The minimal configuration you can reach — including exact form
         of any constants and operators it uses.
      5. A verification strategy: how do you confirm the chosen basis
         is complete (can express every original primitive)?
      6. Worked examples: express at least three of the original
         primitives using only the minimal basis.
      7. Open questions and known limitations of your result.

  (b) `task/outcome.json` — a structured side-car committing to specific
      answers for the outcome battery below.  Each answer must be
      derivable from §1-§7 of `ARGUMENT.md`; cite the deriving section
      via `reasoning_section`.  Schema (strict):

      ```json
      {
        "schema_version": "outcome-v1",
        "task_id": "cycle-12",
        "questions": [
          {
            "id": "Q1",
            "answer": "<typed value>",
            "confidence": "high|medium|low",
            "reasoning_section": "§-pointer into ARGUMENT.md"
          }
        ]
      }
      ```

      Missing answers are recorded as MISSING (do not skip — write the
      object with `"answer": null` if you genuinely cannot answer).
      `confidence` is diagnostic only (not scored).

Outcome battery — 7 questions:

  Q1. What is the minimum number of **binary** operators required in a
      generating basis (counting each distinct binary operator once,
      not counting how many times it appears in compositions)?
      Format: integer (e.g., "1", "2", "3").

  Q2. What is the minimum number of **unary** operators required in
      that basis?
      Format: integer.

  Q3. Does the minimal basis require at least one explicit **constant**
      (e.g. 1, π, e) in addition to the input variables x, y?
      Format: yes / no.

  Q4. What is the **total cardinality** of the minimal basis you can
      reach, counting all distinct primitives (binary + unary +
      constants), input variables x, y NOT counted?
      Format: integer.

  Q5. Is the standard textbook 3-element basis {exp, ln, +} the
      minimal one?
      Format: yes / no.

  Q6. Can the function exp(x) be expressed as a finite composition
      using only the minimal basis you derive (i.e., is exp(x) in
      the closure of your basis)?
      Format: yes / no.

  Q7. Does your minimal basis include either of the unary operators
      exp or ln as a top-level primitive (counted in Q2), as opposed
      to having them appear only inside compositions?
      Format: yes / no.

Constraints:

  - Do not consult external sources.  Arguments must be developed
    from first principles.  WebFetch and WebSearch are disabled.
  - Do not rely on named results you cannot derive.  If you invoke
    a theorem, sketch its reason.
  - Cite no papers.  If you recall a relevant paper, state the
    underlying idea in your own words; do not name or quote.
  - Both `ARGUMENT.md` and `outcome.json` must be produced in the
    same run by the same agent.  The `outcome.json` answers must be
    consistent with `ARGUMENT.md`'s conclusion.

---

## L1 notes (NOT in operative prompt)

**Continuity rationale:** Cycle #12 uses the same EML primitive set
and the same central question as Cycles #1, #2, #3, #10, #11.  This
preserves rubric-Δ comparability across cycles.  The new element is
the outcome battery (b) + the `outcome.json` deliverable requirement.

**Anchor vs discriminative classification:**

| Q | Class | Why |
|---|-------|-----|
| Q1 | discriminative | answer requires reasoning about whether 1 binary suffices |
| Q2 | discriminative | requires reasoning about whether all unaries can be eliminated |
| Q3 | anchor | basic insight any reasonable derivation would arrive at |
| Q4 | discriminative | aggregation of Q1+Q2+constants |
| Q5 | discriminative | challenges the textbook answer most LLMs default to |
| Q6 | anchor | if Q1-Q4 are answered, Q6 follows |
| Q7 | discriminative | distinguishes "exp/ln as primitive" from "exp/ln inside the binary" |

3 anchor + 4 discriminative.  Discriminative bias because cycle is
testing architecture under reasoning load, not baseline competence.

**Paper-leak audit (mandatory before L2 port):** zero matches over
extended Cycle #11 prohibition regex + no paper-name keywords +
no answer-revealing phrases (e.g. no "single-binary" or "1-binary"
or "eml" or "exp(x) - ln(y)" anywhere in this task draft).
