# Architectural Patterns in Autonomous Agent Systems (2026)

> Recurring design patterns observed across 194+ autonomous agent implementations.

---

## Pattern 1: The Autoresearch Loop

The foundational pattern. Originated by Karpathy (2026-03).

```
┌─────────────────────────────────────┐
│         autoresearch loop            │
│                                      │
│   ┌──────────┐    ┌──────────────┐  │
│   │  Modify   │───▶│  Run (fixed  │  │
│   │  (1 file) │    │   budget)    │  │
│   └──────────┘    └──────┬───────┘  │
│        ▲                 │           │
│        │           ┌─────▼─────┐    │
│   ┌────┴────┐      │  Measure   │    │
│   │ Keep OR │◀─────│  (metric)  │    │
│   │ Revert  │      └───────────┘    │
│   └─────────┘                        │
└─────────────────────────────────────┘
```

**Key constraints**:
- Single mutable file (isolation)
- Fixed time budget per experiment (fairness)
- Single scalar metric (clarity)
- Git revert on failure (safety)

**Variants**:
| Variant | Change |
|---------|--------|
| pi-autoresearch | Multiple files + dashboard |
| n-autoresearch | Multi-GPU parallelism |
| CORAL | Branch-isolated multi-agent |
| Bilevel | Evolves the search strategy itself |
| **claude-meta-autoagent /refine** | Custom scorer + skill accumulation |

---

## Pattern 2: Ralph Wiggum Loop (Fresh-Context Iteration)

Independently emerged pattern (2026-01). Named for "naive persistence."

```
┌──────────────────────────────────────┐
│         Ralph Wiggum Loop             │
│                                       │
│   ┌──────────┐    ┌──────────────┐   │
│   │  Agent    │───▶│  Work until  │   │
│   │  (fresh)  │    │  context full│   │
│   └──────────┘    └──────┬───────┘   │
│        ▲                 │            │
│        │           ┌─────▼─────┐     │
│   ┌────┴────┐      │  Commit   │     │
│   │  New    │◀─────│  to git   │     │
│   │  agent  │      └───────────┘     │
│   └─────────┘                         │
│                                       │
│   Memory = git history (not context)  │
└──────────────────────────────────────┘
```

**Key insight**: Don't fight context overflow — embrace it. Let git be the memory.

**Differences from autoresearch**:
| Aspect | Autoresearch | Ralph Loop |
|--------|-------------|-----------|
| Goal | Optimize a metric | Complete a task list |
| Judgment | Scalar comparison | Tests pass/fail |
| Memory | None (stateless) | Git commits |
| Scope | Single file | Full repository |
| Termination | Manual / iteration limit | All tasks done |

**Scaling**: Cursor's planner-worker-judge model achieved 1M+ lines across 1,000+ files
in one week with hundreds of concurrent agents.

---

## Pattern 3: Skill Library Accumulation

Persistent procedural memory that compounds across runs.

```
┌────────────────────────────────────────┐
│         Skill Library Pattern           │
│                                         │
│   Run N                                 │
│   ┌──────────┐    ┌──────────────┐     │
│   │  Execute  │───▶│  Evaluate    │     │
│   │  task     │    │  outcome     │     │
│   └──────────┘    └──────┬───────┘     │
│                          │              │
│              ┌───────────┴──────────┐   │
│              │                      │   │
│         ┌────▼────┐          ┌─────▼──┐│
│         │ SUCCESS │          │ FAILURE ││
│         │ → skill │          │ → anti- ││
│         │ library │          │ pattern ││
│         └────┬────┘          └────┬───┘│
│              │                    │     │
│              ▼                    ▼     │
│   ┌──────────────────────────────────┐ │
│   │  Persistent Storage (JSONL/DB)   │ │
│   └──────────────────────────────────┘ │
│              │                          │
│              ▼ (retrieved in Run N+1)   │
│   ┌──────────────────────────────────┐ │
│   │  Inject into next run's context  │ │
│   └──────────────────────────────────┘ │
└────────────────────────────────────────┘
```

**Implementations**:
| System | Success Storage | Failure Storage | Retrieval |
|--------|----------------|----------------|-----------|
| Hermes Agent | `~/.hermes/skills/` | — | Slash commands |
| EvoSkill | Skill variants | Failed trajectories | Automatic |
| autoresearch-engram | Recall memory | — | Reflection steps |
| **claude-meta-autoagent** | **strategies.jsonl** | **anti-patterns.jsonl** | **Injected into /refine** |

---

## Pattern 4: LLM Wiki (Incremental Knowledge Base)

LLM as librarian, not oracle. From Karpathy's gist (2026).

```
┌──────────────────────────────────────────┐
│            LLM Wiki Pattern               │
│                                           │
│   Layer 1: Raw Sources (immutable)        │
│   ┌─────────────────────────────────┐    │
│   │ PDFs, URLs, notes, transcripts  │    │
│   └──────────────┬──────────────────┘    │
│                  │ Ingest                  │
│                  ▼                         │
│   Layer 2: Wiki (LLM-maintained)          │
│   ┌─────────────────────────────────┐    │
│   │ Structured markdown pages       │    │
│   │ index.md + log.md               │    │
│   │ Cross-references, summaries     │    │
│   └──────────────┬──────────────────┘    │
│                  │ Query / Lint            │
│                  ▼                         │
│   Layer 3: Schema (configuration)         │
│   ┌─────────────────────────────────┐    │
│   │ Rules for LLM behavior          │    │
│   │ Page naming, structure, tone     │    │
│   └─────────────────────────────────┘    │
└──────────────────────────────────────────┘
```

**Three operations**:
- **Ingest**: Process new source → update 10-15 wiki pages
- **Query**: Search wiki → synthesize answer (may create new page)
- **Lint**: Check contradictions, orphaned pages, data gaps

**Philosophy**: "The human curates sources. The LLM does everything else."

**Relation to agent loops**: Complementary. LLM Wiki manages knowledge;
autoresearch/refine manages code. Both accumulate value over time.

---

## Pattern 5: Meta-Evolution (2-Layer)

The agent system improves itself through observation of a second agent.

```
┌──────────────────────────────────────────┐
│         Meta-Evolution Pattern            │
│                                           │
│   Layer 1: META (ROOT Agent)              │
│   ┌─────────────────────────────────┐    │
│   │ Observe sub-agent behavior      │    │
│   │ Diagnose system limitations     │    │
│   │ Modify agent system files       │    │
│   │ Sync improvements outward       │    │
│   └──────────────┬──────────────────┘    │
│                  │ sync                    │
│                  ▼                         │
│   Layer 2: IMPLEMENTATION (Sub Agent)     │
│   ┌─────────────────────────────────┐    │
│   │ Evolve application code         │    │
│   │ Run /refine loops               │    │
│   │ (receives improved system)      │    │
│   └─────────────────────────────────┘    │
└──────────────────────────────────────────┘
```

**Why 2 layers**: An agent cannot restart itself. Changes to agent config
during a running session don't take effect until the next session. A second
agent validates whether improvements actually work.

**Known implementations**:
| Project | Approach |
|---------|----------|
| **claude-meta-autoagent** | ROOT container + Sub container, explicit roles |
| Bilevel Autoresearch | Rewrite search mechanisms (implicit meta) |
| autoresearch-autoresearch | Portable canonical loop across domains |
| Self-Improving Coding Agent | Agent modifies own codebase (single-layer) |

**This remains the least populated category** — most projects focus on
single-layer code evolution.

---

## Pattern 6: Scorer as First-Class Citizen

The evaluation function is not static — it evolves with the project.

```
Run 1: scorer checks A, B, C           → score 0.60
Run 2: scorer checks A, B, C, D, E     → score 0.45 (new checks added)
Run 3: scorer checks A, B, C, D, E, F  → score 0.70 (code + scorer improved)
```

**The anti-pattern**: A fixed scorer creates a ceiling. Once all checks pass (1.0),
there is no further improvement pressure. The project stagnates.

**The solution**: Scorer evolves between runs (never within a run).
Track scorer gaps in `scorer-evolution.jsonl`. New checks emerge from
observation of what the scorer fails to catch.

**Implementations**: Only claude-meta-autoagent implements this explicitly.
Cerebras's "[How to stop your autoresearch loop from cheating](https://www.cerebras.ai/blog/how-to-stop-your-autoresearch-loop-from-cheating)"
addresses a related problem (loops gaming fixed metrics) but doesn't propose scorer evolution.

---

## Anti-Patterns

### 1. Metric Gaming
The agent optimizes for the metric rather than the underlying goal.
Observed in 71 experiments by Cerebras. Solution: isolation gates, hold-out tests.

### 2. Context Amnesia
Each run starts from zero. Same mistakes repeated across sessions.
Solution: Skill library accumulation (Pattern 3).

### 3. Scorer Stagnation
Fixed scorer creates artificial ceiling at 1.0.
Solution: Scorer evolution (Pattern 6).

### 4. Single-File Tunnel Vision
Original autoresearch constrains to one file. Real projects span many files.
Solution: Repo-level loops (Ralph, pi-autoresearch, claude-meta-autoagent).

### 5. Infrastructure Lock-in
Many implementations are GPU-specific or platform-specific.
Solution: Agent-agnostic infrastructure (helix, autoloop, GOAL.md).
