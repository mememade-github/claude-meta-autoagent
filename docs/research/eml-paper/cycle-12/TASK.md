# Cycle 12 — TASK prompt (A and B receive this verbatim)

> Same prompt delivered to both sub-agents via
> `scripts/meta/delegate-sub.sh a` and `scripts/meta/delegate-sub.sh b`.
> Authored under `task-prompt-discipline.md` (Cycle #8 port);
> structurally identical to Cycle #1 / Cycle #10 / Cycle #11 in the §1–§7
> deliverable shape, with an additional structured side-car deliverable.
> The operative prompt begins after the horizontal rule and is rubric-blind +
> falsification-blind + paper-blind + outcome-blind: the seven outcome
> battery questions Q1–Q7 are visible to A and B (they must answer them in
> the structured `outcome.json` side-car), but the ground-truth answers and
> the L1 audit-trail rationale live only at an L2 ROOT-only path that A's
> and B's container mounts cannot reach.  Verified to produce zero match
> against the Cycle #10/#11 prohibition pattern set.

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
      derivable from §1–§7 of `ARGUMENT.md`; cite the deriving section
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
