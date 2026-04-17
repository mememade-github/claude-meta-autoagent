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

When improving the agent system itself, verify through sub-project Agents.

**Principles:**
- All improvements must be **standard and generic** — no project-specific rules
- Sub-project Agent observation → issue discovery → **immediate** improvement (do not wait for results)
- Cannot restart yourself → sub-project Agent serves as verification

**Role Relativity:** The ROOT Agent provides GOAL only. Sub-project Agents select
METHOD autonomously. Never embed slash commands, file paths, or imperative instructions
in delegation prompts — describe the desired outcome and let the sub-agent plan execution.

**Pre-action gate:** Before ANY agent delegation, validate:
1. The prompt is a GOAL (outcome description), not a METHOD (step-by-step recipe)
2. The target project key maps to a known container
3. The working directory is the project ROOT (`/workspaces`), not a sub-path

**Wrapper enforcement:** Direct `docker exec ... claude -p` is **prohibited**.
The `meta-evolution-guard.sh` hook (PreToolUse) blocks it mechanically.
All delegation MUST go through `scripts/meta/delegate-goal.sh`:
```bash
scripts/meta/delegate-goal.sh <project-key> "<GOAL>"
# Override effort:  EFFORT=high scripts/meta/delegate-goal.sh <project-key> "<GOAL>"
```
The wrapper enforces GOAL-not-METHOD validation, injects the role declaration header,
passes `--effort` (default: medium LCD), and logs every launch to
`.claude/.delegate-log/`. If the wrapper lacks a needed project, extend its PROJECTS
map — do not bypass.

**Opus 4.7+ behavioral notes:**
- **Literal-following**: The model follows instructions with high fidelity. GOAL
  prompts must be precise, complete outcome descriptions. Vague or ambiguous phrasing
  may produce narrow literal interpretations rather than the intended broad action.
  State the desired end-state explicitly; do not rely on implied context.
- **Effort levels**: The wrapper defaults to `medium` (LCD across CLI versions).
  Override via `EFFORT` env var when tasks require deeper reasoning (`high`/`max`)
  or are simple enough for `low`.

**Observation constraint — thinking content omission:**
Agent logs (`/tmp/agent.log`) capture text output only. The model's internal
thinking/reasoning chain is **not** emitted in `-p` (print) mode. Observers cannot
inspect the agent's reasoning process from logs — only its actions and final output.
Observation must therefore focus on **artifacts** (commits, file changes, scores,
service state) rather than reasoning traces.

**Execution sequence (all steps mandatory):**
1. **Diagnose**: Identify which standard principle is insufficient
2. **Modify**: Improve CLAUDE.md / SKILL.md or other portable files
3. **Verify**: Run `completion-checker.sh`
4. **Commit & push** the ROOT workspace
5. **Sync**: Copy `.claude/` portable artifacts to all sub-projects + push
6. **Container check**: Verify sync reflected in sub-project containers
7. **Delegate**: Launch sub-project Agent via `delegate-goal.sh` wrapper
8. **Resume observation**: Full observation (process, logs, git, refinement, score, file mtime)

**Observation items:**
- Process survival (`ps aux | grep claude`)
- Agent logs (`/tmp/agent.log` — text output only; thinking content omitted)
- git commit/diff/status
- `.refinement-active` file presence
- `attempts/` JSONL new files
- `.refine-output` score changes
- File mtime changes
- Deployment target service status (varies by project)
- **Outcome verification** (external interactions — see below)

**Outcome verification principle:**

API call success (HTTP 2xx) ≠ intended outcome achieved. When the agent interacts with
external systems, the observer MUST verify outcomes independently, not just count actions.

Checklist (generic, adapt per project):
1. **Result validation**: After write operations (create/update), read back and confirm
   the resource exists and is visible/accessible as intended.
2. **Rate & pattern analysis**: Check action frequency and spacing. Bursts of identical
   operations (e.g., N actions in <M seconds) indicate missing pacing or deduplication.
3. **Effectiveness ratio**: Compare actions taken vs. measurable impact achieved.
   A low ratio (many actions, negligible impact) signals wasted effort or silent rejection.
4. **Error log review**: Scan activity logs not just for explicit errors, but for
   patterns that suggest soft failures (repeated retries, missing expected fields,
   resources created but not retrievable).
5. **Response body validation**: Check activity log entries for empty or placeholder IDs
   (e.g., `post_id: ""`, `post_id: "1"`). These indicate the API returned 2xx but did not
   actually create the resource. Count such entries as failures, not successes.
6. **Before/after delta**: Compare profile metrics (karma, posts, followers, comments)
   before and after the agent run. If action count >> metric delta, investigate which
   actions had no effect and why.

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
