# Self-Evolving Agent Frameworks (2026)

> Agent systems that improve their own capabilities through feedback loops.

## Overview

Self-evolving agents go beyond single-loop experimentation (autoresearch) by maintaining
persistent capabilities (skills, workflows, prompts) that improve across sessions.

---

## Major Frameworks

### EvoAgentX

- **Repository**: https://github.com/EvoAgentX/EvoAgentX
- **By**: EvoAgentX team (research paper published July 2025)
- **Stars**: 2,700+
- **License**: Open source

**Architecture**:
```
Natural language goal
    → WorkFlowGenerator (auto-assemble multi-agent workflow)
    → AgentManager (instantiate agents with roles)
    → WorkFlow Execution Engine (orchestrate)
    → Evaluation & Evolution Module (score → refine → repeat)
```

**Evolution mechanism**:
1. Agents execute tasks
2. Evaluators score performance with task-specific metrics
3. Low-performing workflows get targeted improvement suggestions
4. Prompts, tool assignments, and agent roles adjust
5. Repeat until convergence

**Built-in tools** (20+): Python/Docker execution, Wikipedia/Google/arXiv search,
MongoDB/PostgreSQL/FAISS, browser automation, DALL-E/Flux image generation

**Differentiation**: Evolves workflows (not just code). HITL checkpoints.
Multi-LLM support via LiteLLM/OpenRouter.

**Limitation**: No meta-evolution. No cross-run skill accumulation.

---

### Hermes Agent (Nous Research)

- **Repository**: https://github.com/NousResearch/hermes-agent
- **By**: Nous Research
- **License**: Open source

**Architecture**:
```
agent/     — Primary agent loop
gateway/   — Multi-platform messaging (Telegram, Discord, Slack, WhatsApp, Signal)
hermes_cli/ — TUI with slash-commands
skills/    — Skill library (agentskills.io compatible)
cron/      — Scheduled automation
tools/     — 40+ integrated tools
```

**Self-improving loop**:
1. **Skill generation**: Creates new skills after complex tasks
2. **Skill refinement**: Improvements during active use
3. **Memory persistence**: Agent-curated memory with periodic nudges
4. **Session search**: FTS5 + LLM summarization for cross-session recall
5. **User modeling**: Honcho dialectic framework for personal profiles

**Execution backends**: Local, Docker, SSH, Daytona, Singularity, Modal

**Notable features**:
- Runs on $5 VPS with near-zero idle costs
- Cross-platform conversation continuity (CLI ↔ Telegram ↔ Discord)
- Batch trajectory generation for training tool-calling models
- Atropos RL environment support
- Autoresearch skill requested ([#4832](https://github.com/NousResearch/hermes-agent/issues/4832), [#5114](https://github.com/NousResearch/hermes-agent/issues/5114))

**Differentiation**: Most complete single-agent platform. Skill persistence + multi-platform gateway.

**Limitation**: Single-layer. No scorer-driven evolution. No meta-evolution.

---

### Self-Improving Coding Agent (Robeyns)

- **Repository**: https://github.com/MaximeRobeyns/self_improving_coding_agent
- **Status**: Experimental

**Self-improvement loop**:
```
Evaluate current agent → Archive results → Self-modify own codebase → Iterate
```

**Key idea**: The agent works on its own source code. Performance data directly
informs code enhancements. Docker-based isolation prevents unintended damage.

**Differentiation**: True recursive self-improvement (agent modifies itself).

**Limitation**: Minimal tooling. Base agent deliberately lacks advanced capabilities,
positioning itself as a bootstrapping framework.

---

### EvoSkill (Sentient AGI)

- **Repository**: https://github.com/sentient-agi/EvoSkill

**Mechanism**:
1. Analyze failed agent trajectories
2. Propose skill changes
3. Test variants
4. Keep better-performing skills

**Differentiation**: Failure-driven skill evolution. Learns from what went wrong.

---

### OpenSpace (HKUDS)

- **Repository**: https://github.com/HKUDS/OpenSpace

**Key concept**: Skills as living entities with full lifecycle management —
discovery → application → monitoring → analysis → evolution — without human intervention.

**Differentiation**: Automatic skill lifecycle. No human trigger needed.

---

## Comparison with claude-meta-autoagent

| Capability | EvoAgentX | Hermes | Self-Improving | EvoSkill | **claude-meta-autoagent** |
|-----------|:---------:|:------:|:--------------:|:--------:|:------------------------:|
| Skill persistence | No | Yes | No | Yes | **Yes (JSONL)** |
| Scorer-driven | Task-specific | Implicit | Benchmarks | Trajectory | **Custom scorer** |
| Cross-run learning | No | Yes (skills) | No | Yes | **Yes (3-loop CAESAR)** |
| Meta-evolution | No | No | Partial (self) | No | **Yes (2-layer)** |
| Failure learning | No | No | No | Yes | **Yes (anti-patterns.jsonl)** |
| Scorer evolution | No | No | No | No | **Yes** |
| Universal (any project) | Yes | Yes | No (self only) | Yes | **Yes** |

**Key gap in the ecosystem**: No other framework combines all three of:
1. Explicit scorer-driven keep/discard loop
2. Cross-run skill/anti-pattern accumulation
3. Meta-layer that evolves the agent system itself

---

## Survey & Catalogs

- [Awesome Self-Evolving Agents](https://github.com/EvoAgentX/Awesome-Self-Evolving-Agents) — Comprehensive survey paper + resource list
- [awesome-ai-agents-2026](https://github.com/caramaschiHG/awesome-ai-agents-2026) — 300+ AI agents across 20+ categories
- [e2b-dev/awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents) — Curated list of autonomous agents
- [OpenAI Self-Evolving Agents Cookbook](https://developers.openai.com/cookbook/examples/partners/self_evolving_agents/autonomous_agent_retraining) — Cookbook for autonomous agent retraining
