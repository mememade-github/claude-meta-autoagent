# Moltbook — Sample Project

A Moltbook AI social network integration demo. This sample demonstrates the `/refine` autonomous improvement loop.

## Try it

```bash
# Check agent status
python moltbook.py status

# Run the tests
python test_moltbook.py
```

## Run the scorer

```bash
bash .refine/score.sh
```

## Run /refine

From the ROOT workspace, with Claude Code:

```
/refine "improve the sample app" --project ./projects/sample-app
```

The agent will autonomously discover gaps via the scorer, fix them, and iterate until the score reaches the threshold.

## Validated Results

### Engagement Scorer Evolution (Phase 1–2)

The scorer was expanded with 8 new engagement-quality checks across three categories:

| Category | Checks | What they verify |
|----------|--------|-----------------|
| **P** (Pacing) | P1–P3 | Per-action-type cooldown between API calls; burst detection in activity log |
| **A** (API utilization) | A1–A2 | Breadth of Moltbook API usage; no dead-letter endpoints |
| **Q** (Quality/Diversity) | Q1–Q3 | Content diversity; interaction variety; non-repetitive engagement patterns |

**Scorer growth**: 50 → 57 → 72 checks (now 72 total across 17 categories: A, C, D, DR, E, F, G, K, L, M, N, P, Q, S, T, U, V; P/A/Q skip without activity.jsonl, M skips without MOLTBOOK_API_KEY).

### /refine Autonomous Recovery

After scorer expansion, the score dropped from **1.00 → 0.97** due to new P1 and P3 failures (burst patterns in activity timestamps).

`/refine` resolved this in **1 iteration**:
- **Root cause**: `log_activity()` wrote timestamps without inter-action spacing
- **Fix**: Added per-action-type cooldown pacing in `moltbook.py`
- **Score delta**: 0.97 → **1.00**
- **Strategy captured**: `S-1 (pacing)` — burst detection + per-action-type cooldown

## .claude/ Portable Artifacts

**Agents** (`.claude/agents/`): `evaluator.md`, `wip-manager.md`

**Hooks** (`.claude/hooks/`): `meta-evolution-guard.sh`, `pre-commit-gate.sh`, `pre-push-gate.sh`, `refinement-gate.sh`, `session-start.sh`, `sub-project-edit-guard.sh`

**Skills** (`.claude/skills/`): `refine/`, `status/`, `verify/`, `wiki/`

### Cumulative Stats

| Metric | Value |
|--------|-------|
| Total scorer checks | 72 |
| Refine runs (all time) | 4 |
| Cumulative iterations | 6 |
| Strategies in `strategies.jsonl` | 6 |
| Current score | **1.00** |
