# Ecosystem Landscape: Autonomous Agent Loops (2026)

> Comparative analysis of self-improving agent systems.

## Categories

The autonomous agent loop ecosystem can be divided into five categories:

### 1. Single-Loop Experiment Systems (autoresearch family)
Modify one file → run time-boxed experiment → measure metric → keep/discard → repeat.

### 2. Fresh-Context Coding Loops (Ralph Wiggum family)
Run agent → context fills up → fresh agent starts → git is the memory layer.

### 3. Self-Evolving Agent Frameworks
Agents that improve their own prompts, skills, or workflows through evaluation feedback.

### 4. Meta-Evolution Systems
Agent systems where one layer evolves the agent system itself (not just application code).

### 5. Knowledge Accumulation Systems (LLM Wiki)
LLM incrementally builds and maintains persistent structured knowledge bases.

---

## Comparison Matrix

| Feature | autoresearch | Ralph Loop | EvoAgentX | Hermes Agent | **claude-meta-autoagent** |
|---------|:---:|:---:|:---:|:---:|:---:|
| Keep/discard loop | Yes | No (task completion) | Yes (workflow) | Yes (skills) | **Yes** |
| Cross-run memory | No | No (git only) | Partial | Yes (skills) | **Yes (3-loop)** |
| Scorer evolution | No (fixed metric) | N/A | No | No | **Yes** |
| Meta-evolution | No | No | No | No | **Yes (2-layer)** |
| Multi-agent | No | No | Yes | No | **Yes (ROOT + Sub)** |
| Universal (any project) | No (ML only) | Yes | Yes | Yes | **Yes** |
| Open source | Yes | Yes | Yes | Yes | **Yes** |
| GPU required | Yes | No | No | No | **No** |

---

## Key Projects by Category

### Category 1: autoresearch (Karpathy, 2026-03)

- **Repository**: https://github.com/karpathy/autoresearch
- **Stars**: 21,000+ (as of 2026-03)
- **Core**: Agent edits `train.py`, trains 5min on H100, measures `val_bpb`, keeps/discards
- **Results**: 700 experiments in 2 days, 20 optimizations found, 11% speedup at larger scale
- **Limitation**: Single GPU, single file, fixed metric (val_bpb), no cross-run learning

Notable derivatives (194+ total — see [autoresearch-ecosystem.md](autoresearch-ecosystem.md)):
- **pi-autoresearch**: Generalized loop with dashboard and slash-commands
- **AutoKernel**: GPU kernel optimization
- **n-autoresearch**: Multi-GPU parallelism + adaptive search
- **CORAL**: Multi-agent with branch-isolated workers and skill sharing

### Category 2: Ralph Wiggum Loop (2026-01~)

- **Origin**: Named after the Simpsons character for "naive persistence"
- **Repository**: https://github.com/snarktank/ralph
- **Core**: Infinite loop feeding same prompt to coding agent, progress in git not context
- **Plugin**: Available for Claude Code (`/ralph-loop`), Cursor
- **Strength**: Solves context overflow; simple, works for task-completion goals
- **Limitation**: No evaluation metric, no learning, no keep/discard judgment

Related:
- **Compound Product** (https://github.com/snarktank/compound-product): Three-phase pipeline (analysis → planning → execution)

### Category 3: Self-Evolving Agent Frameworks

#### EvoAgentX
- **Repository**: https://github.com/EvoAgentX/EvoAgentX
- **Stars**: 2,700+
- **Core**: Automatic workflow construction → evaluation → iterative refinement
- **Components**: WorkFlowGenerator, AgentManager, Evaluation & Evolution Module
- **Strength**: Multi-agent workflow optimization, 20+ built-in tools
- **Limitation**: Evolves workflows, not the agent system itself

#### Hermes Agent (Nous Research)
- **Repository**: https://github.com/NousResearch/hermes-agent
- **Core**: Built-in learning loop — creates skills from experience, improves during use
- **Skills**: Stored in `~/.hermes/skills/`, compatible with agentskills.io standard
- **Backends**: Local, Docker, SSH, Daytona, Singularity, Modal
- **Gateway**: Telegram, Discord, Slack, WhatsApp, Signal
- **Strength**: 40+ tools, multi-platform, persistent user modeling
- **Limitation**: Single-layer only — no meta-evolution

#### Self-Improving Coding Agent (Robeyns)
- **Repository**: https://github.com/MaximeRobeyns/self_improving_coding_agent
- **Core**: Agent works on its own codebase — evaluate → archive → self-modify → iterate
- **Strength**: True recursive self-improvement concept
- **Limitation**: Experimental, minimal tooling

#### EvoSkill
- **Repository**: https://github.com/sentient-agi/EvoSkill
- **Core**: Analyzes failed trajectories → proposes skill changes → keeps better variants
- **Strength**: Failure-driven evolution

### Category 4: Meta-Evolution Systems

#### claude-meta-autoagent (this project)
- **Repository**: https://github.com/mememade-github/claude-meta-autoagent
- **Core**: 2-layer architecture — ROOT evolves `.claude/` system, Sub-project evolves code
- **Unique**: Scorer evolution, 3-loop CAESAR learning, cross-run skill library
- **Positioning**: Only known system with explicit meta-evolution layer

#### autoresearch-autoresearch
- **Repository**: https://github.com/cavit99/autoresearch-autoresearch
- **Core**: Meta-autoresearch maintaining portable canonical loop across domains
- **Relation**: Similar meta-level concept but without the 2-layer separation

#### Bilevel Autoresearch
- **Repository**: https://github.com/EdwardOptimization/Bilevel-Autoresearch
- **Core**: Meta-autoresearch rewriting search mechanisms themselves
- **Relation**: Closest conceptual neighbor — evolves the optimization strategy

### Category 5: Knowledge Accumulation (LLM Wiki)

#### Karpathy LLM Wiki Pattern
- **Source**: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- **Core**: LLM incrementally builds/maintains a persistent wiki from raw sources
- **Three layers**: Raw sources (immutable) → Wiki (LLM-maintained) → Schema (config)
- **Operations**: Ingest (process sources → update pages), Query (search + synthesize), Lint (health-check)
- **Philosophy**: "The human curates sources. The LLM does everything else."

#### karpathy-llm-wiki (Agent Skill)
- **Repository**: https://github.com/Astro-Han/karpathy-llm-wiki
- **Core**: Packages LLM Wiki as installable Agent Skill for Claude Code / Cursor / Codex
- **Install**: `npx add-skill Astro-Han/karpathy-llm-wiki`
- **Metrics**: 94 wiki articles, 99 sources, 87 log entries in 7 days

---

## Architectural Patterns Comparison

| Pattern | Memory Layer | Evaluation | Evolution Target | Scope |
|---------|-------------|-----------|-----------------|-------|
| autoresearch | Git (revert) | Fixed metric | Application code | Single file |
| Ralph Loop | Git (commits) | Tests pass/fail | Task completion | Full repo |
| EvoAgentX | Ephemeral + persistent | Task-specific scoring | Workflows + prompts | Multi-agent |
| Hermes Agent | Skills + sessions | Implicit (use frequency) | Skills | Single agent |
| LLM Wiki | Wiki pages | Lint (consistency) | Knowledge base | Documents |
| **claude-meta-autoagent** | **Git + JSONL skill library** | **Scorer (customizable)** | **Agent system + code** | **2-layer** |

---

## Industry Trends (2026)

1. **Autoresearch explosion**: 194+ implementations across ML, trading, systems optimization, and evaluation — the keep/discard loop is now a standard pattern
2. **Ralph Loop adoption**: Cursor plugin, Claude Code integration — fresh-context loops are mainstream
3. **Skill accumulation**: Hermes, EvoSkill, and autoresearch-engram all converge on persistent skill libraries
4. **Agent-as-infrastructure**: Red Hat OpenShift, SkyPilot, Modal, SageMaker all support autoresearch workloads
5. **Finance dominance**: 15+ trading/finance autoresearch implementations — highest domain-specific adoption
6. **Meta-level gap**: Very few projects (2-3) attempt to evolve the agent system itself — this remains the frontier

---

## Sources

- [karpathy/autoresearch](https://github.com/karpathy/autoresearch)
- [karpathy LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Astro-Han/karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki)
- [EvoAgentX/EvoAgentX](https://github.com/EvoAgentX/EvoAgentX)
- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- [snarktank/ralph](https://github.com/snarktank/ralph)
- [yibie/awesome-autoresearch](https://github.com/yibie/awesome-autoresearch) — 194+ project catalog
- [MaximeRobeyns/self_improving_coding_agent](https://github.com/MaximeRobeyns/self_improving_coding_agent)
- [Addy Osmani — Self-Improving Coding Agents](https://addyosmani.com/blog/self-improving-agents/)
- [Fortune — Karpathy autonomous AI research agent](https://fortune.com/2026/03/17/andrej-karpathy-loop-autonomous-ai-agents-future/)
- [VentureBeat — autoresearch](https://venturebeat.com/technology/andrej-karpathys-new-open-source-autoresearch-lets-you-run-hundreds-of-ai)
- [Anthropic — Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
