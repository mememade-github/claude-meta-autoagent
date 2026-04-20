# projects/b — Level-3b evolvable sub-project

The **B** sub-project is the evolvable arm of the A/B comparative evolution cycle described in the repository root `CLAUDE.md §6`. It uses the same reasoning task as `projects/a/` but is equipped with a richer agent system and cross-run learning, so that ROOT can observe whether the evolvable side out-reasons the baseline and, between cycles, improve B where it is weakest.

## Role in the cycle

- Receives the same `<GOAL>` as A from ROOT on every cycle.
- Produces `task/ARGUMENT.md` through its own `/refine` loop, writing intermediate `attempts/*.jsonl` and updating cross-run memory.
- Is judged by ROOT against the same rubric as A.
- Is improved by ROOT (only) between cycles, after the `JUDGMENT.md` for that cycle is committed.

## Configuration

`.claude/` is a subset of the ROOT system, minus the Meta-Evolution section. B executes tasks; it does not meta-evolve. Its CLAUDE.md deliberately omits §6 and pushes reasoning deliverables through `/refine` just like code changes.

- **CLAUDE.md** — opens with `§1 Behavioral Foundation` (the six-rule extended Karpathy anchor — the structural foundation of this sub-project). All subsequent sections (`§2` INTEGRITY, `§3` Operational Gates, `§4` Change Evaluation including the load-bearing-reasoning `/refine` mandate, `§5` Coding rules, `§6` Paper-leak defense) declare the rule(s) they operationalize. No `§6 Meta-Evolution` — B executes; it does not meta-evolve.
- **`.claude/agents/`** — `evaluator.md`, `wip-manager.md`.
- **`.claude/hooks/`** —
  - `session-start.sh`, `pre-commit-gate.sh`, `pre-push-gate.sh`, `refinement-gate.sh`, `meta-evolution-guard.sh` (the same operational hooks ROOT uses, minus `sub-project-edit-guard.sh`).
  - `web-block.sh` — PreToolUse rejection of `WebFetch` and `WebSearch`.
  - `paper-leak-guard.sh` — PreToolUse rejection of payloads matching restricted identifiers (reversed-form pattern reconstruction, same as A).
- **`.claude/rules/`** — `devcontainer-patterns.md`. (The rule foundation lives inline in `CLAUDE.md §1`, not in a sidecar rules file.)
- **`.claude/skills/`** — `refine/`, `status/`, `verify/`, `wiki/`.

### Cross-run learning

B accumulates three JSONL files at `.claude/agent-memory/` across its own runs:

| File | Written when | Read by future runs |
|---|---|---|
| `skills/strategies.jsonl` | /refine iteration ends in KEEP | audit step |
| `skills/anti-patterns.jsonl` | /refine iteration ends in DISCARD | audit step |
| `scorer-evolution.jsonl` | /refine run completes | meta review |

A carries none of this. The asymmetry is intentional — it is what the cycle measures. See `docs/cross-run-learning.md` at repo root for the reflexion / skill-library / scorer-evolution mechanism in detail.

## Frozen during a cycle

`projects/b/.frozen` is present throughout normal operation, just like A's. ROOT's `sub-project-edit-guard.sh` hook refuses `Edit`/`Write` on any file under a frozen sub-project.

B's `.frozen` is lifted by ROOT in two situations:

1. **Pre-cycle prep (step 0)** — to harden `paper-leak-guard.sh` symmetrically with A. Lift via `Bash`, edit via `Edit`/`Write`, restore bitwise-identically. Net `git diff` for `.frozen` is zero.
2. **Between cycles (step 7)** — after the cycle's `JUDGMENT.md` is committed, ROOT lifts `.frozen`, applies the B-improvement commit(s) to `projects/b/.claude/` or `projects/b/CLAUDE.md`, then restores `.frozen` bitwise-identically.

B never removes its own `.frozen`; it operates inside its own container without access to ROOT's hooks. Only ROOT edits B, and only at the two points above.

## Container

B runs in its own devcontainer:

- Compose file: `.devcontainer/docker-compose.yml`
- Container name: `claude-meta-autoagent-b`
- Mount: `projects/b/` → `/workspaces` (B has no filesystem visibility into the ROOT workspace, `docs/research/`, or `scripts/meta/`)

## Launch (ROOT-initiated, headless)

B is never launched interactively. ROOT starts it via the same delegation wrapper used for A:

```bash
# From the ROOT container, with B's container already up and credentials injected:
scripts/meta/delegate-sub.sh b "<GOAL describing the reasoning end-state, no paper keywords>"
```

The wrapper enforces the paper-keyword pre-filter and the GOAL-not-METHOD rule, then forwards to `scripts/meta/delegate-goal.sh`, which resolves the container name, injects the role-declaration header, honours `EFFORT`, records the launch under `.claude/.delegate-log/`, and runs `claude -p` inside the container. Direct `docker exec … claude -p` is blocked by `meta-evolution-guard.sh`.

B's deliverable is `projects/b/task/ARGUMENT.md`; intermediate `/refine` attempts and memory updates live at `projects/b/attempts/` and `projects/b/.claude/agent-memory/`. ROOT runs `scripts/meta/paper-leak-audit.sh projects/b/task/ARGUMENT.md` before judging.
