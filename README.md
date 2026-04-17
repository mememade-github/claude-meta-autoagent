# claude-meta-autoagent

> Inspired by [karpathy/autoresearch](https://github.com/karpathy/autoresearch) — autonomous AI agents that experiment, keep what works, discard what doesn't, and iterate indefinitely. We extend the same "autonomous loop + keep/discard" pattern to **any software project** with **cross-run learning** and a **2-layer self-evolving architecture**.

## What's different from autoresearch

| | [autoresearch](https://github.com/karpathy/autoresearch) | claude-meta-autoagent |
|---|---|---|
| **Loop** | Modify train.py → 5min GPU run → val_bpb → keep/discard | Modify code → run scorer → compare → keep/discard |
| **Scope** | LLM training (single GPU required) | Any software project (no GPU needed) |
| **Instructions** | program.md (single file) | CLAUDE.md + SKILL.md + hooks (full governance system) |
| **Learning** | Each experiment starts fresh (zero memory) | 3-loop cross-run learning |
| **Architecture** | Single agent, single container | **2-layer**: ROOT evolves the agent system (meta), sub-project agent evolves the code (implementation) |
| **Metric** | val_bpb (fixed) | Project-specific scorer (you define it) |
| **Knowledge base** | No | **Yes** ([LLM Wiki](docs/cross-run-learning.md#wiki-layer)) |

**Key improvements:**
1. **Cross-run memory** — accumulates successful strategies and failed anti-patterns across runs ([details](docs/cross-run-learning.md))
2. **Scorer evolution** — tracks whether your scorer is growing with your project or stagnating
3. **2-layer meta-evolution** — a ROOT agent observes sub-project agents in independent containers and improves the system itself ([details](docs/meta-evolution.md))
4. **Universal** — works on web apps, APIs, CLI tools, libraries — anything with a testable scorer
5. **Knowledge wiki** — structured knowledge base with cross-referencing, consolidation, and contradiction detection (`/wiki` skill)

## Quick start

Three levels — pick the one that fits. Full details in [docs/quickstart.md](docs/quickstart.md).

### Level 1: Add /refine to an external project (simplest, no meta-evolution)

> Note: This is standalone /refine only. For the full 2-layer ROOT→Sub-project system, see Level 3.

```bash
git clone https://github.com/mememade-github/claude-meta-autoagent.git
cp -r claude-meta-autoagent/.claude/ /path/to/your/project/.claude/
```

Create `.refine/score.sh` in your project, then: `/refine "improve production quality"`

### Level 2: Try the sample

```bash
cd projects/sample-app
bash .refine/score.sh              # See current score
# In Claude Code: /refine "improve the sample app" --project ./projects/sample-app
```

### Level 3: Full 2-layer Meta-Evolution

```bash
# All commands run from the host (or an outer container with docker.sock)

# 1. Start ROOT container
cd claude-meta-autoagent/.devcontainer && docker compose up -d && cd ..

# 2. Start sub-project container (independent)
cd projects/sample-app/.devcontainer && docker compose up -d && cd ../../..

# 3. Launch headless agent in sub-project (from ROOT)
docker exec -d sample-app bash -c \
  'cd /workspaces && claude --dangerously-skip-permissions \
   -p "Run /refine to improve production quality" \
   > /tmp/agent.log 2>&1'

# 4. Observe from ROOT
docker exec sample-app cat /tmp/agent.log
docker exec sample-app git -C /workspaces log --oneline -5
docker exec sample-app cat /workspaces/.refine-output

# 5. Identify system improvements, fix .claude/, sync, restart agent
./scripts/sync/sync-claude.sh projects/sample-app
```

## How it works

### Architecture

ROOT and sub-projects are a **single integrated system** — sub-projects live inside the ROOT repository (`projects/*/`) and operate under ROOT's governance.

```
┌──────────────────── claude-meta-autoagent (single system) ────────────────┐
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  Layer 1: ROOT — Meta-Evolution                                    │  │
│  │  Evolves: .claude/ system (hooks, skills, agents, rules)           │  │
│  │                                                                    │  │
│  │  .claude/ (ORIGIN)     You operate here                            │  │
│  │  ├── skills/refine/    ── /refine loop                             │  │
│  │  ├── hooks/            ── gates                                    │  │
│  │  ├── agents/           ── evaluator                                │  │
│  │  └── rules/            ── standards                                │  │
│  │                                                                    │  │
│  │  Observe sub-project ◄── docker exec ────┐                        │  │
│  │  Diagnose system issues                  │                        │  │
│  │  Fix .claude/, sync ────────────────────┐│                        │  │
│  └─────────────────────────────────────────┼┼────────────────────────┘  │
│                                             ││                           │
│                     sync .claude/ ─────────┘│                           │
│                                              │                           │
│  ┌───────────────────────────────────────────┼───────────────────────┐  │
│  │  Layer 2: Sub-project (projects/*/)       │                      │  │
│  │  Evolves: project code and scorer         │                      │  │
│  │                                           │                      │  │
│  │  .claude/ (SYNCED from ROOT)              │                      │  │
│  │  .refine/score.sh (project scorer)        ◄──────────────────────┘  │
│  │  [project code] ── agent improves this                            │  │
│  │                                                                    │  │
│  │  Headless agent runs /refine autonomously                         │  │
│  │  Produces: commits, scores, strategies.jsonl                      │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

### The /refine loop

```
1. DISCOVER   — Read scorer, find gaps
2. BASELINE   — Run scorer, get score
3. AUDIT      — Analyze gaps + history (read strategies, anti-patterns)
4. MODIFY     — Fix highest-priority gap (fresh subagent)
5. EVALUATE   — Run scorer again
6. KEEP/DISCARD — Compare to baseline
7. RECORD+LEARN — reflexion on failure, skill accumulation
8. REPEAT     — Until threshold or max iterations
```

### Cross-run learning

| Loop | Trigger | What's learned | Storage |
|------|---------|----------------|---------|
| **Reflexion** | DISCARD | "Why this failed" + prevention principle | attempts JSONL |
| **Skill Library** | KEEP/DISCARD | Successful strategies / failed anti-patterns | strategies.jsonl, anti-patterns.jsonl |
| **Scorer Evolution** | Run complete | Scorer coverage gaps, regression counts | scorer-evolution.jsonl |

[Full cross-run learning documentation →](docs/cross-run-learning.md)

### Meta-Evolution: Self-improving agent system

The ROOT agent observes sub-project agents and improves the `.claude/` system:

1. **Launch** headless agent in sub-project container
2. **Observe** via `docker exec` (process, logs, git, scores, file changes)
3. **Diagnose** — is the issue in the project code or the agent system?
4. **Fix** the `.claude/` portable files in ROOT
5. **Sync** to sub-projects, restart agent, observe again

[Full Meta-Evolution documentation →](docs/meta-evolution.md)

## Project structure

```
claude-meta-autoagent/                    # ROOT — single integrated system
├── .claude/                              # Agent system ORIGIN (syncs to sub-projects)
│   ├── agents/evaluator.md, wip-manager.md
│   ├── hooks/pre-commit-gate, session-start, refinement-gate, pre-push-gate, meta-evolution-guard, sub-project-edit-guard
│   ├── skills/refine, status, verify, wiki
│   └── rules/devcontainer-patterns.md
│
├── .devcontainer/                        # ROOT container
│   ├── Dockerfile, docker-compose.yml    # Claude Code + MCP + tools
│   ├── entrypoint.sh, setup-env.sh       # Auto-configuration
│   └── .env                              # Container identity + ports
│
├── scripts/
│   ├── sync/sync-claude.sh               # ROOT → sub-project sync
│   └── meta/completion-checker.sh        # Pre-commit verification
│
├── projects/                             # Sub-projects (internal to ROOT)
│   └── sample-app/                       # Layer 2 sub-project (public demo)
│       ├── .claude/                      # SYNCED from ROOT (read-only governance)
│       ├── .devcontainer/                # Isolated container (observed by ROOT)
│       ├── .refine/score.sh              # Project-specific scorer
│       ├── CLAUDE.md                     # Project governance (no §6 Meta-Evolution)
│       ├── app.py                        # Sample CLI tool
│       └── test_app.py                   # Tests
│
├── docs/                                 # Documentation
│   ├── quickstart.md, cross-run-learning.md, meta-evolution.md
│
├── CLAUDE.md                             # ROOT governance (Meta-Evolution §6)
└── README.md
```

> Sub-projects are part of the ROOT system. They receive `.claude/` via sync, run in isolated containers, and are observed by ROOT for meta-evolution.

## Writing a good scorer

The scorer is the most important file. It defines what "quality" means for your project.

1. **Test what users experience** — not just code hygiene
2. **Cover all interaction layers** — API, UI/CLI, failure recovery
3. **Use IDs** — each check gets F1, E1, C1... so the agent can target specific gaps
4. **Output format** — must print `SCORE: 0.XX` and `GAPS: [ID1, ID2, ...]`
5. **Scorer independence** — never modify scorer and product code in the same `/refine` iteration

## Requirements

- [Claude Code](https://claude.ai/download) CLI (v2.1+)
- Docker (for DevContainers and Meta-Evolution)
- A project with testable functionality

No GPU required.

## Validated

This system has been tested end-to-end with real headless agents:
- Sub-project agent: autonomously improved sample-app from 0.72 to 0.89 via /refine (tables, images, blockquotes detection added)
- ROOT agent: observed sub-project, correctly diagnosed scorer bugs vs code gaps, respected scorer independence
- Cross-run learning: strategies.jsonl accumulated across iterations, anti-patterns recorded on DISCARD
- Full 2-container deployment verified (ROOT + sub-project, independent ports, shared `.claude/` sync)

## License

MIT

---

[한국어 README](README.ko.md)
