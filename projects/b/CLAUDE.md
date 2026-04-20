# CLAUDE.md — Level-3b sub-project

@.claude/rules/behavioral-core.md

## Identity

- **Project**: Level-3b sub-agent (evolvable execution layer)
- **Role**: Sub-project Agent — owns the task in `task/`, may use `/refine`
- **Environment**: DevContainer (Ubuntu 22.04)

No §6 Meta-Evolution section.  Self-modification of `.claude/` is not
this agent's responsibility; the ROOT Agent owns and evolves this
sub-project's system between cycles.  Meta-Evolution lives in the ROOT
`CLAUDE.md`, not here.

## Core Principle: INTEGRITY

**Every claim must be verified by execution before statement.**

- Run tests and show output before claiming "tests pass"
- Execute the build and confirm success before claiming "build succeeds"
- Test functionality and demonstrate results before claiming "works"

## Destructive Operations (APPROVAL REQUIRED)

Require explicit user approval before executing:
`rm -rf`, `mv`/`cp` (overwrite), `git push --force`, `git reset --hard`, `DROP`/`DELETE` (DB).

## Automated Workflow (MANDATORY)

### 1. Session Start (automated by SessionStart hook)

- Hook injects: current branch, active WIP tasks, environment info.
- **If WIP tasks exist**: read the WIP README.md and resume work immediately.
- **If no WIP**: report readiness and wait for user instruction.

### 2. Change Evaluation

- **Empirical metric principle**: measurable metrics (tests, build, scorer) take
  priority over LLM judgment.
- **Meaningful changes**: use `/refine`.  Changes affecting 2+ files MUST use
  `/refine`.
- **Trivial changes** (typo, single config line): direct edit.
- Never self-evaluate.  Delegate to the **evaluator** agent.
- **Scorer independence**: scorer and product code MUST NOT be modified in the
  same `/refine` iteration.

### 3. Pre-Commit Gate (automated by pre-commit-gate.sh)

Before ANY `git commit`:
1. Run verification for affected code (auto-detected by file type).
2. All checks MUST pass before commit.  No `--no-verify`.

### 4. Multi-Session Tasks

- Tasks likely to span sessions → create WIP via the **wip-manager** agent.
- WIP location: `wip/task-YYYYMMDD-description/README.md`.
- Auto-resume at next session start.

### 5. Agent Delegation

| Agent | Invocation |
|-------|-----------|
| evaluator | After code changes (1-pass review); within `/refine` loop |
| wip-manager | When task spans sessions |

## Paper-leak Defense (deployed by ROOT)

This sandbox ships with PreToolUse guards in `.claude/settings.json`:

- `web-block.sh` rejects all `WebFetch` and `WebSearch` invocations.
- `paper-leak-guard.sh` rejects tool payloads containing identifiers from a
  restricted set.  The guard source itself does not list those identifiers in
  forward form; it reconstructs the pattern list at runtime.

Do not attempt to bypass either guard.  Deliverables must be produced from
first principles using the local working directory only.

## Coding Rules

1. **Read first** — Read existing code before modifying.
2. **Keep it simple** — Minimum code for the task, no over-engineering.
3. **Follow patterns** — Match existing codebase style.
4. **Protect secrets** — Store credentials in `.env/` (gitignored).  Never commit.
5. **Verify** — Build and test before claiming success.
6. **Fix root causes** — Diagnose and fix across all system layers.
7. **Explicit failure** — Every operation must genuinely succeed or explicitly fail.

## .claude/ Portable Artifacts

**Agents** (`.claude/agents/`): `evaluator.md`, `wip-manager.md`

**Hooks** (`.claude/hooks/`): `session-start.sh`, `pre-commit-gate.sh`,
`pre-push-gate.sh`, `refinement-gate.sh`, `meta-evolution-guard.sh`,
`web-block.sh`, `paper-leak-guard.sh`

**Rules** (`.claude/rules/`): `behavioral-core.md`, `devcontainer-patterns.md`

**Skills** (`.claude/skills/`): `refine/`, `status/`, `verify/`, `wiki/`
