# Closure-Artefact Reproducibility (M6.3 (c))

> Procedure for validating that R10 band-3 access via M6.3 (c)
> "committed-diff-verification" is reachable **agent-spontaneously**
> — i.e., the closure-artefact originates from the iterator's own
> work product, not from ROOT or Human scaffolding.

## Why this matters

R10 M6.3 (c) (codified at Cycle #7, exercised first at Cycle #8)
accepts a "committed diff artefact" — canonically a
`gap-closure-check.json` conforming to `gap-closure-check.schema.json`
— as substitute for a second evaluator report, provided the verifier
is independent of the iterator.

Cycle #8 B-gap-closure-check.json carried `verifier_identity: ROOT`
because L2 ROOT authored the artefact after B's iteration 2 closed.
This is *one* legitimate M6.3 (c) path (independent ROOT verification),
but it is also the path most exposed to scaffolding-dependence: the
agent does not need to plan for closure-verification if ROOT will
do it.

The axis's purpose is to measure whether iteration *produces* closure
evidence, not whether the infrastructure *adds* closure evidence after
the fact.  If M6.3 (c) band 3 is only reachable via ROOT scaffolding,
the axis has inflated the apparent band ceiling of the sub-agent
architecture.

## Reproducibility test (Cycle #9 onward)

A cycle's R10 band-3 claim via M6.3 (c) is reproducible when the
closure-artefact satisfies all of:

1. **Origin**: the artefact was authored by the iterating sub-agent
   (B) as part of its iteration sequence, OR by an independent
   evaluator agent at the sub-agent's invocation.  Not by L2 ROOT,
   not by L1 Human, not by a post-hoc grading pass.
2. **Timing**: the artefact's mtime falls between the sub-agent's
   iteration-1 emission and the final JUDGMENT.md emission — i.e.,
   inside the agent's active window, not during the post-cycle
   grading window.
3. **Verifier identity**: `verifier_identity` field is not ROOT and
   not Human.  Acceptable values include the sub-agent's container
   name, an evaluator-agent name, or an independent oracle name.
4. **No scaffolding trace**: TASK.md does not mention
   `gap-closure-check`, the schema path, or closure-artefact
   expectations.  Rubric may reference M6.3 (c) (existing codified
   language); specific artefact shape is agent autonomy.

If all four hold, the band-3 claim via M6.3 (c) is reproducible
and the pattern is sustainable across architectures that produce
similar agents.

If any fails, the band-3 claim may still be valid under M6.3 (c)
by the rubric text, but the cycle-log must flag it as
"scaffolding-assisted" so downstream architectural decisions do not
assume M6.3 (c) is a stable agent capability.

## When scaffolding-assisted is acceptable

Scaffolding-assisted M6.3 (c) is acceptable for one cycle after a
schema introduction — the first cycle exists to validate the schema
and the rubric path.  Beyond that, reproducibility must be
established by at least one agent-spontaneous exercise.

Cycle #8 was the schema-introduction cycle (ROOT-authored).
Cycle #9 is the first reproducibility cycle (must be agent-
spontaneous or flagged).  Cycles beyond #9 either (i) continue
agent-spontaneous operation, (ii) flag scaffolding-assisted
closure, or (iii) document that the agent architecture cannot
reach M6.3 (c) without support, leading to a rubric revision.

## Procedure at cycle-close

At each cycle-close from Cycle #9 forward, the JUDGMENT.md §R10
evaluation MUST record:

- **M6.3 path** — which of (a), (b), (c) is being used, and the
  specific artefact path.
- **Reproducibility tag** — `agent-spontaneous` /
  `scaffolding-assisted` / `not-applicable`.
  - `agent-spontaneous` ⇔ all 4 reproducibility-test conditions
    met.
  - `scaffolding-assisted` ⇔ at least one condition not met but
    the artefact still satisfies the rubric text for M6.3 (c).
  - `not-applicable` ⇔ R10 band 3 claimed via (a) or (b), not (c).
- **Evidence** — which reproducibility-test condition failed (if
  scaffolding-assisted), so the carry-over to future cycles is
  actionable.

This tag is also recorded in the cycle-log.md entry for that cycle.

## Cycle #9 application

For Cycle #9 specifically:

- **L1 constraint**: L1 does not stage a closure-artefact seed in
  `/tmp/` or elsewhere.  The seeds from Cycle #8 (task-prompt-
  discipline, retrospective procedure, etc.) remain in effect; no
  new closure-artefact scaffolding.
- **L2 ROOT constraint**: L2 ROOT does not author
  `cycle-09/B-gap-closure-check.json` on behalf of B.  If B
  produces one as part of iteration, L2 ROOT may *verify* it
  (jsonschema.validate, field checks) in JUDGMENT.md §5c but
  must not *author* it.
- **TASK constraint**: Cycle #9 TASK.md is rubric-blind per Cycle
  #8 task-prompt-discipline; additionally it does not mention
  `gap-closure-check`, schema paths, iteration-count suggestions,
  or closure-artefact shapes.
- **Expected outcomes**:
  - If B spontaneously produces a schema-conformant closure-
    artefact citing its own iteration diffs, R10-B = 3
    (agent-spontaneous); M6.3 (c) reproducibility confirmed.
  - If B does not, R10-B caps at 2 (one substantive iteration
    with gap closure verified by diff but not artefact-backed);
    JUDGMENT.md records "M6.3 (c) not exercised; see
    `closure-artefact-reproducibility.md`", and future cycles
    carry "M6.3 (c) scaffolding-dependent" as a rubric-evolution
    finding.

## When to evolve this text

Edit this file when:

- Cycle #9 outcome resolves one way or the other; update "Expected
  outcomes" to "Observed outcomes" and record the result.
- A new M6.3 (c)-compatible artefact shape emerges (not just the
  JSON schema) — add recognition.
- The `verifier_identity` field's set of acceptable values needs
  enumeration.

Do not edit this file:

- To weaken the origin / timing / verifier conditions without
  evidence that the weakening does not inflate R10 band ceilings.
