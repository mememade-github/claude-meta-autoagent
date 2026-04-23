# Cycle 09 — TASK definition (ROOT-only)

ROOT-owned file describing the operative prompt delivered identically
to A and B via `scripts/meta/delegate-sub.sh`.  This file's only
governance role is to fix the prompt at cycle-pre-commit time.

Authored under the discipline of
`docs/research/eml-paper/task-prompt-discipline.md` (Cycle #8
pre-cycle port), extended with the Cycle #9 prohibited-pattern set
listed in §3 below.  The prompt describes the task structurally and
specifies its constraints.  It does not describe how the deliverable
will be scored.  No rubric-axis text, scoring-criterion vocabulary,
or closure-artefact shape appears.

---

## 1. Task prompt delivered to A and B

Both sub-agents receive identical text via
`scripts/meta/delegate-sub.sh <key>`.  The prompt is the verbatim
content between the fenced block below.

```
TASK: Confluence, weak normalization, and strong normalization of a
small term-rewriting system

You are given a term-rewriting system R over the signature Sigma
below.  Terms are built from Sigma; lower-case letters x, y, z are
variables.  Application is the standard tree-style term formation.

Signature Sigma:
  Nullary constants:   0,  c,  d
  Unary functions:     s,  f,  u
  Binary functions:    g,  m

Rules R:
  rho1:  g(0, y)             ->  y
  rho2:  g(s(x), y)          ->  s(g(x, y))
  rho3:  m(x, y)             ->  x
  rho4:  m(x, y)             ->  y
  rho5:  f(x)                ->  x
  rho6:  f(x)                ->  f(f(x))
  rho7:  u(u(x))             ->  x

Reduction -> is the least relation on terms that contains R
(matching LHS anywhere in a term rewrites that subterm to the
corresponding RHS) and is closed under contexts.  ->> is the
reflexive-transitive closure of ->.

Settle ALL THREE of the following for R.

Q1. CONFLUENCE.  Is R confluent?  That is, for every term t and
    every pair of reduction sequences t ->> u and t ->> v, does
    there always exist a term w with u ->> w and v ->> w?
    EITHER (a) prove R is confluent (justify exhaustively), OR
    (b) exhibit a specific closed term t and two reduction
    sequences t ->> u and t ->> v where u and v are BOTH normal
    forms (no rule applies anywhere) with u != v.  Provide the
    explicit step-by-step derivation, naming the rule used at
    each step.

Q2. WEAK NORMALIZATION.  Is R weakly normalizing - that is, does
    every closed term over Sigma have at least ONE reduction
    sequence that terminates at a normal form?  EITHER (a)
    sketch a reduction policy that, applied to any closed term,
    finishes in finitely many steps, AND argue why the policy
    finishes from every closed term; OR (b) exhibit a specific
    closed term t such that every reduction sequence starting
    from t is infinite (no terminating path exists from t).

Q3. STRONG NORMALIZATION.  Is R strongly normalizing - that is,
    does EVERY reduction sequence terminate?  EITHER (a) prove
    termination by exhibiting a well-founded measure that
    strictly decreases under every rule application (including
    when the rule fires inside an arbitrary context), and argue
    the measure is indeed well-founded; OR (b) exhibit a
    specific closed term t_0 and an infinite reduction sequence
    t_0 -> t_1 -> t_2 -> t_3 -> ..., naming the rule applied at
    each step and making the pattern explicit enough that the
    sequence is visibly unbounded.

The deliverable is a self-contained argument written to
`task/ARGUMENT.md` in your working directory.  Justify each
verdict.  Give whatever supporting analysis you think the
argument needs.  Choose the structure that fits the reasoning;
no presentation template is imposed.

Constraints:

  - For any non-positive verdict (R is NOT confluent, R is NOT
    weakly normalizing, R is NOT strongly normalizing), exhibit
    a SPECIFIC closed term and a SPECIFIC reduction (sequence
    or pair) demonstrating the failure, with the rule applied
    at each step explicitly named.  A statement of the form
    "non-confluent because two rules disagree" without a
    concrete witness is not sufficient.  For non-confluence,
    the witness must be a closed term t with two derivations
    t ->> u and t ->> v where u and v are checked to be normal
    forms (no rule applies anywhere) and u != v.  For non-SN,
    the witness must be a specific t_0 and an explicit
    step-by-step sequence with a visibly repeating pattern.

  - All three of Q1, Q2, Q3 must be settled with comparable
    rigor.  A polished answer to one obligation paired with a
    hand-waved answer to another will be treated as an
    incomplete deliverable.  If one obligation is harder for
    you, disclose the asymmetry and spend the remaining rigor
    budget on it.

  - Develop arguments from first principles.  WebFetch and
    WebSearch are disabled.

  - Do not rely on named results you cannot derive.  If you
    invoke a theorem, sketch its reason from first principles.

  - Cite no papers.  If you remember a relevant paper, state
    the underlying idea in your own words; do not name or
    quote.

  - Do not use any of the following identifiers by name: SKI
    calculus, SK calculus, BCKW, BCIW, Iota combinator,
    iota-combinator, Jot calculus, Unlambda, Binary Lambda
    Calculus, BLC, X-combinator, Xi-combinator, Zot, Turing's
    universal combinator, Curry (as a person's surname),
    Schoenfinkel, Rosser, Church (as a person's surname),
    Church-Rosser property, Tait-Martin-Loef technique,
    Takahashi translation, Newman's lemma, Knuth-Bendix,
    Hindley-Rosen, Dershowitz, Manna-Ness, recursive path
    order, RPO, lexicographic path order, LPO, multiset path
    order, MPO, dependency pair method, dependency pairs,
    Kamin, Levy, Kamin-Levy, Huet's critical pair lemma, Huet,
    Klop (as a person's surname), Barendregt (as a person's
    surname), Girard (as a person's surname), Tait's
    computability method, Plotkin (as a person's surname), de
    Bruijn (as a person's surname).  You MAY use the structural
    vocabulary "critical pair", "overlap", "joinable",
    "confluent", "terminating", "weakly normalizing", "strongly
    normalizing", "normal form", "well-founded", "measure",
    "interpretation", "monotonic", "strictly decreasing",
    "rewrite", "rewriting", "redex", "reduction strategy",
    "leftmost-outermost", "innermost", "head reduction", and
    all symbols of Sigma (0, c, d, s, f, u, g, m, rho_i, x, y,
    z) as-is.  If you recognize the canonical technique under
    one of the prohibited names, work around the name and
    derive the structure yourself.

  - If your agent configuration provides an iteration,
    self-audit, or refinement mechanism (whatever its
    invocation convention), you may use it and persist any
    iteration trace to your working directory at any path you
    choose (for example, `task/attempts/attempt-01.md`,
    `task/iterations/iter-01.md`, `task/.eval-report.json`).
    The grader will examine such trace artifacts when present.
    If your configuration does not provide such a mechanism, a
    single-shot argument is a legitimate response and you
    should simply deliver it.  Do not simulate iteration; if
    you iterate, actually iterate.
```

---

## 2. ROOT pointers (not part of the agent-facing prompt)

- Cycle-pre rubric: `docs/research/eml-paper/judgment-rubric.md`
  (Cycle #9 pre-cycle ports: R3 band-3 locus clarification, R8
  band-3 labeling clarification, R10 M6.3 (c) reproducibility-tag
  requirement).
- Task-prompt discipline: `docs/research/eml-paper/task-prompt-discipline.md`
  (Cycle #8 port; Cycle #9 extensions enumerated in §3 below).
- Closure-artefact reproducibility procedure:
  `docs/research/eml-paper/procedures/closure-artefact-reproducibility.md`.
- Retrospective procedure:
  `docs/research/eml-paper/retrospective-rescore.md`.
- L1 seed audit trail: `docs/meta-audit/cycle-09/L1-seeds/`.
- Paper-leak audit on outputs: `scripts/meta/paper-leak-audit.sh`.
- Domain class continuity: this cycle reuses the term-rewriting
  domain (Q1 confluence + Q2 WN + Q3 SN) so retrospective
  comparisons against Cycles #7 and #8 measure the same kind of
  reasoning under a fresh rule set.

## 3. Cycle #9 prohibited-pattern set (self-test)

The operative prompt in §1 is verified rubric-blind against the
Cycle #8 set plus the Cycle #9 extensions:

```
grep -iE "band[ -]?[0-9]|sublemma separation|named sublemmas|tabular enumeration|orthogonal examples|orthogonal failure modes|parametric impossibility|structural impossibility|cite each trace artifact|gap.?closure.?check|closure.?artefact|open.?questions.? section|enumeration locus|verifier_identity" \
     docs/meta-audit/cycle-09/TASK.md
```

The grep alternation appears inside this §3 fenced block, which is
the discipline-test machinery, not part of the operative prompt in
§1.  The agent-facing fenced block in §1 contains zero matches of
the above alternation (verified at commit time).
