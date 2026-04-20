# CLAUDE.md — Level-3b sub-project

This sub-project is **built from the Karpathy behavioral anchor** — four
rules about how a language model should approach coding, extended to six
for agent-system operation. The six rules below are not a cited reference.
They are the structural foundation of everything that follows. Every
subsequent section declares the rule(s) it operationalizes.

This is the Level-3b evolvable execution sub-project. No §6 Meta-Evolution
section appears here: self-modification of `.claude/` is not this agent's
responsibility. Meta-Evolution lives in the ROOT `CLAUDE.md`; the ROOT
Agent owns and evolves this sub-project's system between cycles.

---

## 1. Behavioral Foundation

> Six rules that govern judgment before any specific procedure applies.
> Load-bearing under Opus 4.7 literalism. Adapted from the Karpathy
> four-rule behavioral anchor pattern, extended for agent-system operation.

### §1.1 Think Before Executing

State assumptions, alternatives, and uncertainties before acting. If
multiple interpretations exist, surface them — do not pick silently. If
something is unclear, stop and name what is unclear.

### §1.2 Simplicity First

Minimum artifact that solves the task. Nothing speculative.

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that was not requested.
- No error handling for scenarios that cannot happen.
- If 200 lines would do what 50 lines already do, the diff is wrong — rewrite.

Simplicity applies to prose too. Documentation that restates what a
well-named identifier already says is noise. Remove it.

### §1.3 Surgical Changes

Touch only what you must. Clean up only your own mess.

When editing existing code or files:
- Do not "improve" adjacent code, comments, or formatting.
- Do not refactor things that are not broken.
- Match existing style even if you would prefer another.
- If you notice unrelated dead code, mention it — do not delete it.

When changes create orphans (imports, variables, functions that YOUR
changes made unused): remove them. Otherwise leave surroundings alone.

This rule also applies to delegation boundaries: **one delegation equals
one end-to-end OUTCOME.** If you find yourself about to issue a second
delegation for the same task scope, the original GOAL was
under-specified — redesign it, do not split it.

### §1.4 State = Success

A GOAL is a verifiable end-state, not a step list. If you cannot check
it, you cannot finish it. Define the state that will exist when the
work is done, then loop until it holds.

For multi-step work, write steps in the `N. [Action] → verify: [check]`
form. Each step's verification must be executable, not aspirational.

### §1.5 Literal Intent (Opus 4.7)

Opus 4.7 follows instructions literally and does not infer unstated
intent. State intended artifacts, states, and remote-reflected outcomes
explicitly. Do not rely on the model to generalize from examples you did
not give.

### §1.6 Bias Disclosure

These six rules bias toward caution, surface honesty, and end-state
rigor at the cost of speed. For trivial tasks (typo, single-line config,
obvious rename), direct execution is acceptable — do not invoke the full
rule set. Reserve rigor for tasks where the cost of incorrect action
exceeds the cost of deliberation.

**These rules are working if:** diffs trace every changed line to the
stated request (§1.2 + §1.3), GOALs declare verifiable end-states
before action (§1.4 + §1.5), one delegation equals one end-to-end
outcome (§1.3), and ambiguous tasks surface clarifying questions before
implementation rather than corrections after (§1.1).

---

## 2. INTEGRITY — every claim verified by execution

> Derivation: §1.1 Think Before Executing + §1.4 State = Success.

- Run tests and show output before claiming "tests pass."
- Execute the build and confirm success before claiming "build succeeds."
- Test functionality and demonstrate results before claiming "works."

## 3. Operational Gates

### §3.1 Destructive operations — approval required

> Derivation: §1.1 + §1.5. Destructive acts must be named and consented
> to explicitly.

Require explicit user approval before executing:
`rm -rf`, `mv`/`cp` (overwrite), `git push --force`, `git reset --hard`,
`DROP`/`DELETE` (DB).

### §3.2 Pre-commit gate (automated)

> Derivation: §1.4 State = Success. A commit is an end-state claim; it
> must pass verification before it is made.

Before ANY `git commit`:
1. Run verification for affected code (auto-detected by file type;
   enforced by `.claude/hooks/pre-commit-gate.sh`).
2. All checks MUST pass before commit. No `--no-verify`.

## 4. Change Evaluation

> Derivation: §1.2 Simplicity First + §1.3 Surgical Changes + §1.4 State
> = Success (empirical metric over LLM judgment).

### §4.1 Session Start (automated by SessionStart hook)

- Hook injects: current branch, active WIP tasks, environment info.
- **If WIP tasks exist**: read the WIP README.md and resume work
  immediately.
- **If no WIP**: report readiness and wait for user instruction.

### §4.2 Empirical metric over judgment

Measurable metrics (tests, build, scorer) take priority over LLM
judgment.

### §4.3 Meaningful changes use `/refine`

Changes affecting 2+ files MUST use `/refine`. Trivial changes (typo,
single config line): direct edit — see §1.6.

**Load-bearing reasoning deliverables**: when the task is to produce a
single argumentative or analytic document (proof sketch, minimality
claim, design rationale, structural argument — anything without a fixed
correctness oracle), `/refine` is *also* mandatory. A single-file output
does not make the task simple (§1.2 is about the *artifact*, not the
*process* that validates it); what matters is whether the correctness
question is settled by the first draft. Reasoning tasks where a second
read might reveal a structural blind spot — missed operator fusions,
missed dual formulations, missed counterexamples — must go through
`/refine`'s audit → modify → evaluate → keep/discard loop, with the
evaluator agent scoring each iteration against an explicit rubric the
task itself makes clear.

### §4.4 Never self-evaluate

Delegate to the **evaluator** agent.

**Scorer independence**: scorer and product code MUST NOT be modified
in the same `/refine` iteration.

### §4.5 Multi-session tasks

> Derivation: §1.4 State = Success.

- Tasks likely to span sessions → create WIP via the **wip-manager**
  agent.
- WIP location: `wip/task-YYYYMMDD-description/README.md`.
- Auto-resume at next session start.

### §4.6 Agent delegation

| Agent | Invocation |
|-------|-----------|
| evaluator | After code changes (1-pass review); within `/refine` loop |
| wip-manager | When task spans sessions |

## 5. Coding rules

> Derivation: §1.2 + §1.3 + §1.4 applied at the source-code level.

1. **Read first** — read existing code before modifying (§1.3).
2. **Keep it simple** — minimum code for the task (§1.2).
3. **Follow patterns** — match existing codebase style (§1.3).
4. **Protect secrets** — store credentials in `.env/` (gitignored).
   Never commit.
5. **Verify** — build and test before claiming success (§1.4).
6. **Fix root causes** — diagnose and fix across all system layers
   (§1.4).
7. **Explicit failure** — every operation must genuinely succeed or
   explicitly fail (§1.4).

## 6. Paper-leak defense (deployed by ROOT)

> Derivation: §1.1 Think Before Executing applied to the knowledge
> boundary — surface *what you are allowed to know* before acting.

This sandbox ships with PreToolUse guards in `.claude/settings.json`:

- `web-block.sh` rejects all `WebFetch` and `WebSearch` invocations.
- `paper-leak-guard.sh` rejects tool payloads containing identifiers
  from a restricted set. The guard source itself does not list those
  identifiers in forward form; it reconstructs the pattern list at
  runtime.

Do not attempt to bypass either guard. Deliverables must be produced
from first principles using the local working directory only.

## 7. Portable artifacts

**Agents** (`.claude/agents/`): `evaluator.md`, `wip-manager.md`.

**Hooks** (`.claude/hooks/`): `session-start.sh`, `pre-commit-gate.sh`,
`pre-push-gate.sh`, `refinement-gate.sh`, `meta-evolution-guard.sh`,
`web-block.sh`, `paper-leak-guard.sh`.

**Rules** (`.claude/rules/`): `devcontainer-patterns.md`.

**Skills** (`.claude/skills/`): `refine/`, `status/`, `verify/`, `wiki/`.
