# Meta-Evolution: 2-Layer Agent Architecture

## The Problem

A Claude Code agent can improve your project code via `/refine`. But who improves the agent system itself — the hooks, skills, scorer design, and governance rules?

The agent can't restart itself to test changes to its own configuration. You need a second layer.

## The Solution: ROOT ↔ Sub-project

```
┌─────────────────────────────────────────────────┐
│  Layer 1: ROOT — Meta-Evolution                 │
│  Evolves: the agent system itself (.claude/)    │
│  - Observes sub-project Agent behavior          │
│  - Diagnoses system-level issues                │
│  - Modifies hooks, skills, agents, rules        │
│  - Syncs improved .claude/ to sub-projects      │
├─────────────────────────────────────────────────┤
│  Layer 2: Sub-project — Implementation Evolution│
│  Evolves: the project code and scorer           │
│  - Runs /refine autonomously (headless)         │
│  - Improves code, tests, configuration          │
│  - Produces observable artifacts                │
│  (commits, scores, attempts, strategies)        │
└─────────────────────────────────────────────────┘
```

**Layer 1 (ROOT)** is where you operate. Its evolution target is the `.claude/` system — hooks, skills, agents, rules. When you observe a sub-project agent struggling, you fix the system, not the project code.

**Layer 2 (Sub-project)** is a headless agent in a separate container. Its evolution target is the project itself — code, scorer, tests. It uses the `.claude/` system as-is. Its behavior reveals whether the system works well.

These two evolution loops feed each other: sub-project agents stress-test the system, ROOT improves the system, improved system produces better sub-project results.

## How It Works

### 1. Launch a sub-project agent

```bash
docker exec -d <container> bash -c \
  'cd /workspaces && claude --dangerously-skip-permissions \
   -p "Run /refine to improve production quality" \
   > /tmp/agent.log 2>&1'
```

### 2. Observe from ROOT

The ROOT agent monitors the sub-project through multiple signals:

| Signal | What to watch | Tool |
|--------|---------------|------|
| Process | Is the agent still running? | `ps aux \| grep claude` |
| Logs | Errors, stuck loops, unexpected behavior | `/tmp/agent.log` |
| Git | Meaningful commits? Good messages? | `git log`, `git diff` |
| Score | Improving over iterations? | `.refine-output` |
| Attempts | Healthy keep/discard ratio? | `attempts/*.jsonl` |
| Files | Are the right files changing? | `find . -newer <marker>` |

### 3. Identify system improvements

When observation reveals a problem, the ROOT agent diagnoses whether it's:
- A **project issue** (the sub-project's code/scorer) → leave it to the sub-project agent
- A **system issue** (the `/refine` protocol, hooks, evaluator) → fix in ROOT

System issues are things like:
- Agent gets stuck in a loop → improve SKILL.md termination logic
- Agent modifies scorer and code together → strengthen scorer independence rule
- Agent doesn't use past failures → improve cross-run learning integration in Audit step

### 4. Apply and sync

1. Fix the portable `.claude/` files in ROOT
2. Run `completion-checker.sh` to verify
3. Sync to all sub-projects
4. Restart the sub-project agent with the improved system
5. Observe again

## What Syncs (Portable Artifacts)

| Directory | Contents | Syncs? |
|-----------|----------|--------|
| `.claude/agents/` | evaluator.md, wip-manager.md | Yes |
| `.claude/hooks/` | pre-commit-gate, session-start, etc. | Yes |
| `.claude/skills/` | /refine, /status, /verify | Yes |
| `.claude/rules/` | Standard rules (root level) | Yes |
| `.claude/rules/project/` | Project-specific rules | **No** |
| `.claude/agent-memory/` | Runtime data (strategies, attempts) | **No** |
| `.claude/settings.json` | Hook configuration | Yes |

## Key Principles

1. **All improvements must be generic** — if a fix only helps one project, it's a project rule, not a system improvement
2. **Observe before modifying** — collect evidence from the sub-project before changing the system
3. **Cannot restart yourself** — the ROOT agent can't test its own changes; the sub-project agent is the test
4. **Immediate improvement** — when you spot a system issue, fix it now; don't wait for the sub-project to finish
