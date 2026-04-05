# Cross-run Learning — 3-loop Knowledge Accumulation

Cross-run learning adds persistent memory to the `/refine` loop. Without it, each `/refine` run starts from zero — the agent has no memory of what worked or failed before. These three learning loops accumulate knowledge across sessions.

## The Three Loops

### Loop 1: Reflexion (within iteration)

**When**: A `/refine` iteration is DISCARDED (score didn't improve).

**What**: The agent generates a structured reflection:
```json
{
  "reflection": "Why this specific code change failed",
  "principle": "General rule to prevent this class of failure"
}
```

**How it helps**: The reflection is appended to the attempts JSONL. The next iteration's Audit agent reads it and avoids repeating the same mistake.

**Academic basis**: [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) (Shinn et al., NeurIPS 2023)

---

### Loop 2: Skill Library (across runs)

**When**: Any `/refine` iteration completes (KEEP or DISCARD).

**What**:
- On **KEEP** — successful strategy is recorded to `strategies.jsonl`:
  ```json
  {
    "id": "S-3",
    "domain": "error-handling",
    "pattern": "uncaught exception on invalid input",
    "approach": "added input validation with specific error messages",
    "files": ["src/parser.py"],
    "score_delta": "0.75→0.83"
  }
  ```
- On **DISCARD** — failed approach is recorded to `anti-patterns.jsonl`:
  ```json
  {
    "id": "A-2",
    "domain": "performance",
    "pattern": "tried caching all results",
    "cause": "memory usage exceeded limits",
    "prevention": "profile memory before adding caches"
  }
  ```

**How it helps**: Future `/refine` runs read these files during the Audit step. The agent knows which approaches worked and which to avoid — even across completely separate runs.

**Inspired by**: [Voyager: An Open-Ended Embodied Agent](https://arxiv.org/abs/2305.16291) (Wang et al., 2023)

---

### Loop 3: Scorer Evolution (meta)

**When**: A `/refine` run completes (score meets threshold).

**What**: Records the run's outcome to `scorer-evolution.jsonl`:
```json
{
  "date": "2026-04-05",
  "task_id": "refine-20260405-143022",
  "final_score": 1.00,
  "iterations": 5,
  "threshold": 0.85
}
```

If the score reaches 1.00 (perfect), the agent flags potential scorer gaps — areas the scorer doesn't cover yet. This prevents a false sense of completeness.

**How it helps**: Over time, this log reveals whether the scorer is growing with the project or stagnating. A scorer that always gives 1.00 on the first try isn't challenging enough.

---

## Data Locations

```
.claude/agent-memory/
├── refinement/
│   └── attempts/          # Per-run JSONL (includes reflexions)
├── skills/
│   ├── strategies.jsonl   # Successful approaches (Loop 2)
│   └── anti-patterns.jsonl # Failed approaches (Loop 2)
└── scorer-evolution.jsonl  # Meta-learning log (Loop 3)
```

All files are `.gitignore`d — they're runtime artifacts, not source code.

## Without vs With Cross-run Learning

| | Without | With Learning |
|---|---|---|
| Run 1 fails approach X | Lost knowledge | Recorded in anti-patterns |
| Run 2 starts | Zero context | Reads anti-patterns, avoids X |
| Run 3 succeeds with Y | Forgotten next time | Recorded in strategies |
| Run 4 faces similar gap | Rediscovers Y from scratch | Retrieves Y, applies directly |
| Scorer reaches 1.00 | "Done" | Flags uncovered areas |
