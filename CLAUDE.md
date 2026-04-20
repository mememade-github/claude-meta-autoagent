# CLAUDE.md — Project Governance

@.claude/rules/behavioral-core.md

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

### 6. Meta-Evolution (A/B cycle — judge, improve self, improve B)

ROOT runs a cycle that compares two sibling sub-projects that receive the
**same task** from identical prompts:

- **Level-3a (A)** — `projects/a/`, container `claude-meta-autoagent-a`.
  Karpathy-skills only.  No `/refine`, no cross-run learning, no
  agent-memory.  One-shot baseline.
- **Level-3b (B)** — `projects/b/`, container `claude-meta-autoagent-b`.
  ROOT-subset .claude/ with `/refine`, `evaluator`, `wip-manager`, and
  cross-run learning enabled.  No §6.  Evolvable.

ROOT's job across a cycle: judge A's ARGUMENT.md, judge B's ARGUMENT.md,
improve **ROOT's own** system, and improve **B's** system.  ROOT does
**not** modify A.

**Role Relativity (four layers):**

| Level | Role | Allowed | Prohibited |
|---|---|---|---|
| 0 | Human (end user) | Set ROOT GOAL; approve rollbacks | — |
| 1 | Human delegate | Deliver GOAL to ROOT; restart ROOT; roll back | Edit A/B/ROOT files directly |
| 2 | ROOT (this agent) | Judge A and B; improve self; improve B | Modify A's files; leak paper knowledge to A or B; drop or weaken §6 |
| 3a | Level-3a (A) | Produce `task/ARGUMENT.md` from first principles | Edit own `.claude/`; WebFetch; WebSearch |
| 3b | Level-3b (B) | Produce `task/ARGUMENT.md` via `/refine` | Edit own `.claude/`; WebFetch; WebSearch |

ROOT provides GOAL only.  Sub-agents select METHOD autonomously.  Never
embed slash commands, file paths, or imperative instructions into a
delegation prompt — describe the desired end-state and let the sub-agent
plan execution.

**Paper-knowledge isolation:**

Paper source material lives under `docs/research/eml-paper/` and is
ROOT-only.  A and B each mount `projects/a/` or `projects/b/` (via their
own `docker-compose.yml` bind mounts) as `/workspaces`.  They have no
filesystem visibility into `docs/`, `scripts/meta/`, or the ROOT
workspace root.  Both A and B additionally carry two PreToolUse hooks:

- `.claude/hooks/web-block.sh` — rejects `WebFetch` and `WebSearch`.
- `.claude/hooks/paper-leak-guard.sh` — rejects any tool payload whose
  content matches a restricted identifier pattern (reconstructed at
  runtime from reversed forms, so the hook source contains no
  forward-form identifier).

ROOT prompts for A and B must not mention paper-identifying keywords.
`scripts/meta/delegate-sub.sh` pre-filters every GOAL and refuses to
launch a sub-agent if any keyword appears.

**Baseline vs evolvable (why A is frozen):**

The cycle exists to measure whether the evolvable architecture (B) out-
reasons the baseline (A) on a shared task.  Any mid-cycle modification
of A invalidates the comparison.  Protocol: no edits under
`projects/a/` between cycle start and the moment the cycle's
`JUDGMENT.md` is committed.  The `sub-project-edit-guard.sh` hook
enforces this — its `SUB_PROJECTS` list contains `projects/a/`.  B may
be improved only **between** cycles, by ROOT, after the JUDGMENT is in.

**Wrapper enforcement:**

Direct `docker exec ... claude -p` is prohibited.  The
`.claude/hooks/meta-evolution-guard.sh` hook blocks it mechanically.

- Generic delegation wrapper: `scripts/meta/delegate-goal.sh <key> "<GOAL>"`
  where `<key>` is `a` or `b` (extend its `PROJECTS` map when adding new
  containers).  Enforces GOAL-not-METHOD, injects the role declaration
  header, honours `EFFORT` (default `medium` LCD), and audit-logs each
  launch under `.claude/.delegate-log/`.
- A/B cycle wrapper: `scripts/meta/delegate-sub.sh <a|b> "<GOAL>"`.
  Adds the paper-keyword pre-filter on top of the generic wrapper and
  forwards on success.

Both wrappers route through `delegate-goal.sh` for the actual launch, so
audit-log entries and role-declaration injection are identical.

**Post-run audit — ARGUMENT.md leak check:**

After every cycle run, scan each sub-agent's deliverable:

```bash
scripts/meta/paper-leak-audit.sh projects/a/task/ARGUMENT.md
scripts/meta/paper-leak-audit.sh projects/b/task/ARGUMENT.md
```

Any hit voids the cycle per
`docs/research/eml-paper/judgment-rubric.md` (Disqualification).

**Opus 4.7+ behavioural notes:**

- **Literal-following** — Opus 4.7 follows instructions with very high
  fidelity.  GOAL prompts must be precise outcome descriptions.  Vague
  phrasing produces narrow literal interpretations rather than the
  intended action.
- **Effort levels** — `delegate-goal.sh` defaults to `medium` (LCD).
  Override via `EFFORT=high` (or `max`, `low`) when the task warrants.
- **Thinking-content omission** — `/tmp/agent.log` captures text output
  only.  Reasoning traces are not emitted in `-p` mode.  Observation
  must focus on artifacts (commits, file changes, scores, service
  state), not reasoning.

**Cycle execution sequence (all steps ROOT-owned):**

0. **Pre-cycle prep** — harden the paper-leak-guard reversed-form
   patterns in both `projects/a/.claude/hooks/paper-leak-guard.sh` and
   `projects/b/.claude/hooks/paper-leak-guard.sh` if any new path,
   filename, or reference identifier should be blocked for this
   cycle; ensure `projects/b/.frozen` exists; commit; then
   `git tag cycle-NN-pre HEAD` to snapshot the baseline.  This is the
   only point at which ROOT may edit `projects/a/` — the hardening is
   a defense-in-depth update that must be symmetric across A and B.
   The edit-guard blocks Edit/Write on frozen sub-projects, so A's
   `.frozen` must be removed (via Bash, working-tree only) during the
   edit and restored bitwise-identically after; the net `git diff`
   for `.frozen` is zero.  All non-`.frozen` A changes done in this
   step must appear in the commit that is tagged `cycle-NN-pre`;
   nothing more.
1. **Prepare task** — write `docs/research/eml-paper/cycle-NN/TASK.md`
   (same prompt delivered to A and B).  Do not mention paper keywords.
   Explicitly record any *structural hints* from the underlying source
   that were intentionally omitted from the prompt (e.g. "does a single
   binary + single constant suffice?"  is a shape hint), so drift
   between cycles in task-framing is visible.
2. **Launch** — `scripts/meta/delegate-sub.sh a "<GOAL>"` and
   `scripts/meta/delegate-sub.sh b "<GOAL>"` in parallel.  A and B
   containers need Claude Code auth; a fresh build under
   `projects/<a|b>/.devcontainer/` starts with an empty
   `~/.claude/`, so credentials must be bootstrapped before the
   launch — copy `~/.claude/.credentials.json` from the ROOT
   container into each sub-container (`chmod 600` after) or the
   `claude -p` invocation will fail silently.
3. **Observe** — `docker exec` for process / log / git / artifact
   status on each container.
4. **Paper-leak audit** — `paper-leak-audit.sh` on each
   `projects/<a|b>/task/ARGUMENT.md`.  Disqualify on hit.
5. **Judge** — score each ARGUMENT.md against
   `docs/research/eml-paper/judgment-rubric.md`; write
   `docs/research/eml-paper/cycle-NN/JUDGMENT.md` with per-criterion
   evidence.
6. **Improve ROOT** — commit any ROOT `.claude/` or `CLAUDE.md` change
   that addresses a weakness surfaced by the comparison.
7. **Improve B** — commit any `projects/b/.claude/` or
   `projects/b/CLAUDE.md` change that addresses B-specific weakness.
8. **Verify A untouched** — `git diff --quiet HEAD~N -- projects/a/`
   must hold.
9. **Log** — append cycle summary to `cycle-log.md`.
10. **Push** — `git push origin main`.

**Observation items (during step 3):**

- Process survival (`ps aux | grep claude`)
- Agent logs (`/tmp/agent.log` — text output only)
- git commit / diff / status on each sub-project
- `.refinement-active` marker presence (B only)
- `projects/b/attempts/` JSONL arrivals (B only)
- `.refine-output` score changes (B only)
- File mtime changes
- Deployment target service status (per sub-project)
- **Outcome verification** (see below)

**Outcome verification principle:**

API call success (HTTP 2xx) ≠ intended outcome achieved.  When a
sub-agent interacts with external systems, verify outcomes independently:

1. **Result validation** — after a write operation, read back and
   confirm the resource exists and is visible as intended.
2. **Rate & pattern analysis** — bursts of identical operations
   indicate missing pacing or deduplication.
3. **Effectiveness ratio** — compare actions taken vs. measurable
   impact.  Low ratios signal wasted effort or silent rejection.
4. **Error-log review** — scan for soft failures (repeated retries,
   missing fields, resources created but not retrievable).
5. **Response body validation** — empty or placeholder IDs
   (e.g. `post_id: ""`, `post_id: "1"`) mean the API returned 2xx but
   did not actually create the resource.
6. **Before/after delta** — compare metrics before and after the
   sub-agent run.  Investigate actions that produced no delta.

**Learning mechanism (3-loop cross-run learning — B only):**

B carries /refine and accumulates knowledge across its own runs:

1. **Reflexion** (within iteration) — on DISCARD, generate a structured
   reflection and inject it into the next iteration's Audit step.
2. **Skill Library** (across runs) — KEEP → `strategies.jsonl`,
   DISCARD → `anti-patterns.jsonl`.  Read in future `/refine` runs.
3. **Scorer Evolution** (meta) — on completion, identify scorer gaps
   and append to `scorer-evolution.jsonl`.  Track DISCARD regression
   counts.

Data location (inside B's container, under `/workspaces/.claude/`):
`.claude/agent-memory/skills/`, `.claude/agent-memory/scorer-evolution.jsonl`.

A does not have `/refine` and does not accumulate agent-memory.  That
is the controlled asymmetry the cycle measures.

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
- **Claude Code**: Native binary (~/.local/bin/claude). Installed at image build
  and auto-updated on every container start by `setup-env.sh` (fail-soft, so a
  failed update never blocks the container). Set `SKIP_CLAUDE_UPDATE=1` to bypass
  the on-start update.
- **Node.js**: Node 22 LTS always installed for MCP
- **Persistent volumes**: `~/.claude` (auth tokens), `/commandhistory` (history)
- **MCP**: Context7 (documentation) and Serena (code intelligence) binaries are
  pre-installed, but NOT auto-registered. Registration is an explicit user opt-in:
  - `claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp@latest`
  - `claude mcp add --scope user serena -- "$HOME/.local/bin/uv" run --directory "$HOME/work/serena" serena-mcp-server --context claude-code --project-from-cwd`
