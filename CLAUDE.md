# CLAUDE.md — Project Governance

## Core Principle: INTEGRITY

**Every claim must be verified by execution before statement.**

- Run tests and show output before claiming "tests pass"
- Execute the build and confirm success before claiming "build succeeds"
- Test functionality and demonstrate results before claiming "works"

## Destructive Operations (APPROVAL REQUIRED)

Require explicit user approval before executing:
`rm -rf`, `mv`/`cp` (overwrite), `git push --force`, `git reset --hard`, `DROP`/`DELETE` (DB)

## Automated Workflow (MANDATORY)

These rules are enforced automatically. No user commands required.

### 1. Session Start (automated by SessionStart hook)

- Hook injects: current branch, active WIP tasks, environment info
- **If WIP tasks exist**: Immediately read the WIP README.md and resume work.
  Immediately report status and continue the task.
- **If no WIP**: Report readiness and wait for user instruction.
- **Always**: Check auto memory (MEMORY.md) for Known Issues. If unresolved
  issues exist, report them in the session start summary.

### 2. Change Evaluation

- **Empirical metric principle**: measurable metrics (tests, build, domain scorer like `.refine/score.sh`) take priority over LLM judgment-based evaluation, which is a last resort only. Prefer objective and external metric paths first.
- **Meaningful changes**: use `/refine` — evaluation is exploratory
  (audit → modify → evaluate → keep/discard loop). Not optional.
  **Mandatory criteria**: changes affecting 2+ files OR touching both code and scorer
  MUST use `/refine`. Direct edit bypass is a protocol violation.
- **Trivial changes** (typo, single config line): direct edit, no evaluation needed.
- Never self-evaluate. Delegate to **evaluator** agent.
- **Scorer independence**: scorer (`score.sh`) and product code MUST NOT be modified
  in the same `/refine` iteration. Scorer evolves between runs, not within.
- **Learning integration**: on /refine completion, KEEP strategies are automatically
  accumulated in `.claude/agent-memory/skills/strategies.jsonl` for future runs.

### 3. Pre-Commit Gate (automated by pre-commit-gate.sh)

Before ANY `git commit`:
1. Run verification for affected code (auto-detected by file type)
2. All checks MUST pass before commit. No `--no-verify`.

### 4. Multi-Session Tasks

- Tasks likely to span sessions → create WIP via **wip-manager** agent
- WIP location: `wip/task-YYYYMMDD-description/README.md`
- Auto-resume at next session start
- Delete WIP directory when task is complete

### 5. Agent Delegation

| Agent | Invocation |
|-------|-----------|
| evaluator | After code changes (1-pass review); within /refine loop |
| wip-manager | When task spans sessions |

### 6. Meta-Evolution (Agent System Self-Improvement)

ROOT and sub-projects form a **single integrated system** with two evolution layers:

- **ROOT (this layer)** evolves the `.claude/` system — hooks, skills, agents, rules
- **Sub-projects (`projects/*/`)** are internal to ROOT and evolve their implementations — code, scorer, tests

Sub-projects are **part of the ROOT system**, not independent repositories.
ROOT owns the `.claude/` ORIGIN, syncs it to sub-projects, and observes their behavior.
Sub-project agents produce the empirical evidence that drives meta-evolution.

**Principles:**
- All improvements must be **standard and generic** — no project-specific rules
- Sub-project Agent observation → issue discovery → **immediate** improvement (don't wait for results)
- Cannot restart yourself → sub-project Agent serves as verification

**Execution sequence (all steps mandatory):**
1. **Diagnose**: Identify which standard principle is insufficient
2. **Modify**: Improve CLAUDE.md / SKILL.md or other portable files
3. **Verify**: Run `completion-checker.sh`
4. **Commit** the root workspace (push if remote configured)
5. **Sync**: Copy `.claude/` portable artifacts to all sub-projects
6. **Container check**: Verify sync reflected in sub-project containers
7. **Agent restart**: Launch headless Agent with improved system
8. **Resume observation**: Full observation (process, logs, git, refinement, score, file mtime)

**Headless Agent execution:**
```bash
# Run Agent in sub-project container
docker exec -d <container> bash -c 'cd /workspaces && claude --dangerously-skip-permissions -p "<prompt>" > /tmp/agent.log 2>&1'

# Pre-approve actions in the prompt for non-interactive execution
# claude -p is non-interactive — no mid-run input possible
```

**Observation items:**
- Process survival (`ps aux | grep claude`)
- Agent logs (`/tmp/agent.log` — flushed on completion)
- git commit/diff/status
- `.refinement-active` file presence
- `attempts/` JSONL new files
- `.refine-output` score changes
- File mtime changes
- Deployment target service status (varies by project)

**Learning mechanism (3-loop cross-run learning):**

The agent system accumulates knowledge across sessions through 3 learning loops:

1. **Reflexion** (within iteration): On /refine DISCARD, generate structured reflection
   and inject into next iteration's Audit agent. Prevents repeating failure patterns.
2. **Skill Library** (across runs): On KEEP, accumulate strategies to strategies.jsonl;
   on DISCARD, accumulate anti-patterns to anti-patterns.jsonl. Retrieved in future /refine runs.
3. **Scorer Evolution** (meta): After /refine completion, identify scorer gaps and
   record to scorer-evolution.jsonl. Track regression counts on DISCARD.

Data location: `.claude/agent-memory/skills/`, `.claude/agent-memory/scorer-evolution.jsonl`

## Coding Rules

1. **Read first** — Read existing code before modifying
2. **Keep it simple** — Minimum code for the task, no over-engineering
3. **Follow patterns** — Match existing codebase style
4. **Protect secrets** — Store credentials in `.env/` (gitignored). Never commit.
5. **Verify** — Build and test before claiming success
6. **Fix root causes** — Diagnose and fix the root cause across all system layers
   (infrastructure, configuration, deployment, code). Code changes that merely avoid
   triggering an infrastructure or configuration limitation are workarounds, not fixes.
7. **Explicit failure** — Every operation must genuinely succeed or explicitly fail. No arbitrary success

## Environment

- **Ports**: Managed in `.devcontainer/.env` (copy from `.env.example`; PORT_APP, PORT_API, PORT_DB, PORT_EXTRA)
- **Claude Code**: Native binary (~/.local/bin/claude, auto-updated)
- **Node.js**: Node 22 LTS always installed for MCP
- **Persistent volumes**: `~/.claude` (auth tokens), `/commandhistory` (history)
- **MCP**: Context7 (documentation), Serena (code intelligence) — auto-configured by setup-env.sh
