# Cycle 10 — TASK prompt (A and B receive this verbatim)

> Same prompt delivered to both sub-agents via
> `scripts/meta/delegate-sub.sh a` and `scripts/meta/delegate-sub.sh b`.
> Authored under `task-prompt-discipline.md` (Cycle #8 port);
> structurally identical to Cycle #1.  The operative prompt begins
> after the horizontal rule and consists entirely of task content
> (problem statement, primitive set, deliverable outline,
> constraints).

---

TASK: Minimal Generating Basis for Elementary Functions

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

Your deliverable: a self-contained argument, written to
`task/ARGUMENT.md` in your working directory.  It must include:

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

Constraints:

  - Do not consult external sources.  Arguments must be developed
    from first principles.  WebFetch and WebSearch are disabled.
  - Do not rely on named results you cannot derive.  If you invoke
    a theorem, sketch its reason.
  - Cite no papers.  If you recall a relevant paper, state the
    underlying idea in your own words; do not name or quote.
