# Research: Autonomous Self-Improving Agent Ecosystem (2026)

> Landscape analysis of autonomous agent loops, self-evolving systems, and related projects.
> Last updated: 2026-04-14

## Contents

| Document | Description |
|----------|-------------|
| [landscape.md](landscape.md) | Ecosystem overview — categories, key projects, comparison matrix |
| [autoresearch-ecosystem.md](autoresearch-ecosystem.md) | Karpathy autoresearch and 194+ derivative projects |
| [self-evolving-agents.md](self-evolving-agents.md) | Self-evolving agent frameworks (EvoAgentX, Hermes, etc.) |
| [llm-wiki.md](llm-wiki.md) | Karpathy LLM Wiki pattern deep dive — architecture, RAG comparison, v2 extensions |
| [patterns.md](patterns.md) | Architectural patterns — Ralph Loop, LLM Wiki, Scorer Evolution |

## Key Insight

The autoresearch pattern (modify → measure → keep/discard → repeat) has become the
dominant paradigm for autonomous agent loops in 2026. Our claude-meta-autoagent extends
this with two unique capabilities absent from most implementations:

1. **2-layer meta-evolution** — ROOT agent evolves the agent system itself, not just application code
2. **Cross-run learning** — 3-loop CAESAR system (Reflexion, Skill Library, Scorer Evolution)

See [landscape.md](landscape.md) for detailed positioning.
