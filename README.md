# claude-meta-autoagent

> A meta-agent system that runs an **A/B comparative evolution cycle** on a shared reasoning task. One sub-agent (A) is a frozen baseline; the other (B) is evolvable. A Meta-Agent (ROOT) judges both outputs, improves its own governance, and improves B between cycles. A human delegate oversees the Meta-Agent; the end user sets the GOAL.

## Four-layer architecture

This repository is organised as four role layers. Each layer has a strict subset of the authority of the one above it.

```
Level 0  End User (Human)
         │  sets ROOT GOAL, approves rollbacks
         ▼
Level 1  Human delegate
         │  delivers GOAL to ROOT, restarts ROOT, can roll back
         ▼
Level 2  ROOT — Meta-Agent  (this repo's top-level .claude/ + CLAUDE.md)
         │  judges A and B, improves self, improves B; never touches A
         ▼  docker exec via scripts/meta/delegate-sub.sh
┌────────┴────────┐
Level 3a            Level 3b
A Sub-Agent         B Sub-Agent
projects/a/         projects/b/
baseline            evolvable
one-shot            /refine + cross-run learning
frozen during       frozen during cycle,
cycle               edited by ROOT between cycles
```

### Role table (allowed / prohibited)

| Level | Role | Allowed | Prohibited |
|---|---|---|---|
| 0 | End User | Set ROOT GOAL; approve rollbacks | — |
| 1 | Human delegate | Deliver GOAL to ROOT; restart ROOT; roll back | Edit A/B/ROOT files directly |
| 2 | ROOT (Meta-Agent) | Judge A and B; improve self; improve B | Modify A's files; leak paper knowledge to A or B; drop or weaken §6 |
| 3a | A Sub-Agent | Produce `task/ARGUMENT.md` from first principles | Edit own `.claude/`; `WebFetch`; `WebSearch` |
| 3b | B Sub-Agent | Produce `task/ARGUMENT.md` via `/refine` | Edit own `.claude/`; `WebFetch`; `WebSearch` |

ROOT provides GOAL only. Sub-agents select METHOD autonomously. Slash commands, file paths, and imperative instructions must not appear in a delegation prompt — the prompt describes the desired end-state and lets the sub-agent plan execution.

## Paper-knowledge isolation

The A/B cycle measures whether the evolvable architecture out-reasons the baseline on a shared reasoning task. The task is derived from a paper, but **only ROOT holds the paper**. A and B must reason from first principles.

Isolation is enforced on three layers:

1. **Filesystem** — paper material lives under `docs/research/` at the ROOT workspace root. The A and B containers bind-mount `projects/a/` and `projects/b/` (respectively) as their `/workspaces`, so neither can see ROOT's paper directory, `scripts/meta/`, or the outer workspace.
2. **Tool hooks (PreToolUse, inside A and B)** —
   - `.claude/hooks/web-block.sh` rejects `WebFetch` and `WebSearch`.
   - `.claude/hooks/paper-leak-guard.sh` rejects tool payloads containing restricted identifiers. The hook source stores these identifiers only in reversed form, so it does not itself leak the forward-form strings it is meant to block.
3. **Prompt pre-filter (ROOT side)** — `scripts/meta/delegate-sub.sh` scans every GOAL text against the restricted-identifier list and refuses to launch a sub-agent when any match appears. `scripts/meta/paper-leak-audit.sh` runs the same scan post-hoc on each sub-agent's `task/ARGUMENT.md`; a hit voids the cycle.

## Cycle execution sequence

Every cycle is ROOT-owned and follows the same ten-step sequence (full detail in `CLAUDE.md §6`).

0. **Pre-cycle prep** — harden the paper-leak-guard reversed-form patterns in both sub-projects if new paths or identifiers should be blocked; ensure `projects/b/.frozen` exists; commit; `git tag cycle-NN-pre HEAD`. This is the **only** step during which ROOT may edit `projects/a/`, and it must be symmetric across A and B. A's `.frozen` is temporarily removed via `Bash` (working-tree only), the edit applied, then `.frozen` restored bitwise-identically — net `git diff` for `.frozen` is zero.
1. **Prepare task** — write `docs/research/cycle-NN/TASK.md`; do not mention restricted identifiers. Record any structural hints deliberately withheld from the prompt, so task-framing drift between cycles is visible.
2. **Launch** — `scripts/meta/delegate-sub.sh a "<GOAL>"` and `scripts/meta/delegate-sub.sh b "<GOAL>"` in parallel. Fresh sub-containers start with an empty `~/.claude/`, so `~/.claude/.credentials.json` must be copied from ROOT into each sub-container (`chmod 600`) before launch.
3. **Observe** — `docker exec` for process survival, `/tmp/agent.log`, git state, artifact presence, and `.refinement-active` / attempts JSONL / `.refine-output` on B.
4. **Paper-leak audit** — `scripts/meta/paper-leak-audit.sh` against each `projects/<a|b>/task/ARGUMENT.md`. Any hit disqualifies.
5. **Judge** — score each ARGUMENT.md against `docs/research/…/judgment-rubric.md`; write a per-criterion `JUDGMENT.md` for the cycle.
6. **Improve ROOT** — commit any `.claude/` or `CLAUDE.md` change that addresses a weakness surfaced by the comparison.
7. **Improve B** — commit any `projects/b/.claude/` or `projects/b/CLAUDE.md` change that addresses B-specific weakness (unfreeze via `Bash`, edit, refreeze bitwise-identically).
8. **Verify A untouched** — `git diff --quiet cycle-NN-pre -- projects/a/` must hold.
9. **Log** — append a cycle summary to the cycle log.
10. **Push** — `git push origin main`.

Direct `docker exec ... claude -p` is prohibited; the `.claude/hooks/meta-evolution-guard.sh` hook blocks it and all delegation must route through `scripts/meta/delegate-goal.sh` or `scripts/meta/delegate-sub.sh`.

## Launching a cycle from scratch

Prerequisites: Docker (with `docker.sock` mounted if running from inside a devcontainer), Claude Code CLI v2.1+, and the ROOT container already authenticated (credentials at `~/.claude/.credentials.json`).

```bash
# 1. Start the ROOT container
cd .devcontainer && docker compose up -d && cd ..

# 2. Start both sub-containers
cd projects/a/.devcontainer && docker compose up -d && cd ../../..
cd projects/b/.devcontainer && docker compose up -d && cd ../../..

# 3. Bootstrap Claude credentials into each sub-container
for c in claude-meta-autoagent-a claude-meta-autoagent-b; do
  docker cp ~/.claude/.credentials.json "$c":/home/vscode/.claude/.credentials.json
  docker exec "$c" chmod 600 /home/vscode/.claude/.credentials.json
done

# 4. From the ROOT container: pre-cycle prep, tag, then delegate
#    (the GOAL text is ROOT's responsibility; it must describe a reasoning
#    end-state without naming the source paper)
git tag cycle-NN-pre HEAD
scripts/meta/delegate-sub.sh a "<GOAL>" &
scripts/meta/delegate-sub.sh b "<GOAL>" &
wait

# 5. Observe, audit, judge, improve, push — see CLAUDE.md §6
```

The Meta-Agent (the Claude session running inside the ROOT container) then follows the ten-step sequence above. Everything it does is recorded: each delegation appends to `.claude/.delegate-log/`, each cycle appends to the top-level `cycle-log.md`, each JUDGMENT.md under `docs/research/.../cycle-NN/` is an immutable cycle artifact.

## Cross-run learning (B only)

B carries `/refine` and three JSONL memory files at `.claude/agent-memory/`:

| File | Written when | Read by future runs |
|---|---|---|
| `skills/strategies.jsonl` | /refine iteration ends in KEEP | audit step |
| `skills/anti-patterns.jsonl` | /refine iteration ends in DISCARD | audit step |
| `scorer-evolution.jsonl` | /refine run completes | meta review |

A does not have `/refine` and does not accumulate agent-memory. This is the controlled asymmetry the cycle measures. See `docs/cross-run-learning.md` for the reflexion / skill-library / scorer-evolution mechanism in detail.

## Repository layout

```
claude-meta-autoagent/
├── CLAUDE.md                           # ROOT governance (§6 Meta-Evolution — A/B cycle)
├── .claude/                            # ROOT agent system (hooks, skills, agents, rules)
├── .devcontainer/                      # ROOT container
├── docs/
│   └── research/                       # ROOT-only paper material and per-cycle JUDGMENTs
├── projects/
│   ├── a/                              # Level-3a baseline sub-project (karpathy-skills only)
│   └── b/                              # Level-3b evolvable sub-project (ROOT-subset, no §6)
├── scripts/
│   └── meta/
│       ├── delegate-goal.sh            # generic GOAL-not-METHOD delegation wrapper
│       ├── delegate-sub.sh             # A/B wrapper with paper-keyword pre-filter
│       ├── paper-leak-audit.sh         # post-hoc ARGUMENT.md scanner
│       ├── completion-checker.sh
│       └── portability-check.sh
├── wip/                                # multi-session task state
└── cycle-log.md                        # per-cycle summary log
```

See `projects/a/README.md` and `projects/b/README.md` for each sub-project's detailed role and launch command.

## Requirements

- Claude Code CLI v2.1+
- Docker (with `docker.sock` mounted when running from inside a devcontainer)

No GPU required.

## License

MIT

---

[한국어 README](README.ko.md)
