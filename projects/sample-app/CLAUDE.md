# CLAUDE.md — sample-app

## Identity

- **Project**: sample-app (Moltbook integration demo)
- **Role**: Sub-project (validation target for ROOT agent observation)
- **Environment**: DevContainer (Ubuntu 22.04)

## Core Principle: INTEGRITY

**Every claim must be verified by execution before statement.**

- Run tests and show output before claiming "tests pass"
- Execute the build and confirm success before claiming "build succeeds"
- Test functionality and demonstrate results before claiming "works"

## Destructive Operations (APPROVAL REQUIRED)

Require explicit user approval before executing:
`rm -rf`, `mv`/`cp` (overwrite), `git push --force`, `git reset --hard`, `DROP`/`DELETE` (DB)

## Automated Workflow (MANDATORY)

### 1. Session Start (automated by SessionStart hook)

- Hook injects: current branch, active WIP tasks, environment info
- **If WIP tasks exist**: Immediately read the WIP README.md and resume work.
- **If no WIP**: Report readiness and wait for user instruction.

### 2. Change Evaluation

- **Empirical metric principle**: measurable metrics (tests, build, scorer) take priority over LLM judgment.
- **Meaningful changes**: use `/refine`. Changes affecting 2+ files MUST use `/refine`.
- **Trivial changes** (typo, single config line): direct edit.
- Never self-evaluate. Delegate to **evaluator** agent.
- **Scorer independence**: scorer and product code MUST NOT be modified in the same `/refine` iteration.

### 3. Pre-Commit Gate (automated by pre-commit-gate.sh)

Before ANY `git commit`:
1. Run verification for affected code (auto-detected by file type)
2. All checks MUST pass before commit. No `--no-verify`.

### 4. Multi-Session Tasks

- Tasks likely to span sessions → create WIP via **wip-manager** agent
- WIP location: `wip/task-YYYYMMDD-description/README.md`
- Auto-resume at next session start

### 5. Agent Delegation

| Agent | Invocation |
|-------|-----------|
| evaluator | After code changes (1-pass review); within /refine loop |
| wip-manager | When task spans sessions |

## Coding Rules

1. **Read first** — Read existing code before modifying
2. **Keep it simple** — Minimum code for the task, no over-engineering
3. **Follow patterns** — Match existing codebase style
4. **Protect secrets** — Store credentials in `.env/` (gitignored). Never commit.
5. **Verify** — Build and test before claiming success
6. **Fix root causes** — Diagnose and fix across all system layers
7. **Explicit failure** — Every operation must genuinely succeed or explicitly fail

## Project Info

- **Source**: `moltbook.py` — Moltbook AI social network integration
- **Tests**: `test_moltbook.py`
- **Scorer**: `.refine/score.sh` (Moltbook gap checks G1-G10)
- **Language**: Python 3 (stdlib only, no dependencies)
