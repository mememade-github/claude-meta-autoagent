# projects/a — Level-3a baseline sub-project

The **A** sub-project is the static baseline arm of the A/B comparative evolution cycle described in the repository root `CLAUDE.md §6`. It exists to measure whether the evolvable architecture (`projects/b/`) out-reasons a minimal one-shot sub-agent on the same reasoning task.

## Role in the cycle

- Receives the same `<GOAL>` as B from ROOT on every cycle.
- Produces one artifact: `task/ARGUMENT.md`, written from first principles.
- Does not re-run, self-reflect, or accumulate memory across cycles.

A's purpose is to sit still so B's evolutionary pressure has something to be measured against.

## Configuration

`.claude/` is intentionally minimal. It ships only what is needed to enforce sandbox discipline:

- **CLAUDE.md** — the four-rule karpathy-skills behavioral anchor (Think Before Coding / Simplicity First / Surgical Changes / Goal-Driven Execution), verbatim. A's `CLAUDE.md` does not merely cite the anchor — it **is** the anchor. Nothing more.
- **`.claude/hooks/web-block.sh`** — PreToolUse hook that rejects `WebFetch` and `WebSearch`.
- **`.claude/hooks/paper-leak-guard.sh`** — PreToolUse hook that rejects tool payloads matching restricted identifiers. The guard reconstructs the identifier list from reversed forms at runtime; the hook source itself does not contain the forward-form strings it blocks.

What A does **not** have:

- No `/refine` skill and no `evaluator` / `wip-manager` agents.
- No cross-run learning (no `strategies.jsonl`, no `anti-patterns.jsonl`, no `scorer-evolution.jsonl`, no `agent-memory/`).
- No Meta-Evolution section. A never delegates, never judges, never modifies its own `.claude/`.

This asymmetry is the controlled variable of the cycle — do not add features to A to make it "more competitive".

## Frozen during a cycle

`projects/a/.frozen` is present throughout normal operation. ROOT's `sub-project-edit-guard.sh` hook refuses `Edit`/`Write` on any file under a frozen sub-project, so ROOT cannot accidentally modify A mid-cycle.

`.frozen` is lifted only by ROOT, only during pre-cycle prep (step 0 of the cycle sequence), and only to apply a defense-in-depth hardening of `paper-leak-guard.sh`. The lift-edit-restore sequence is executed via `Bash` in the working tree, and the net `git diff` for `.frozen` must be zero at commit time.

A itself never removes `.frozen`; A operates inside its own container without access to ROOT's hooks.

## Container

A runs in its own devcontainer:

- Compose file: `.devcontainer/docker-compose.yml`
- Container name: `claude-meta-autoagent-a`
- Mount: `projects/a/` → `/workspaces` (A has no filesystem visibility into the ROOT workspace, `docs/research/`, or `scripts/meta/`)

## Launch (ROOT-initiated, headless)

A is never launched interactively. ROOT starts it via the delegation wrapper, which enforces the paper-keyword pre-filter and the GOAL-not-METHOD rule:

```bash
# From the ROOT container, with A's container already up and credentials injected:
scripts/meta/delegate-sub.sh a "<GOAL describing the reasoning end-state, no paper keywords>"
```

The wrapper forwards to `scripts/meta/delegate-goal.sh`, which resolves the container name, injects the role-declaration header, honours `EFFORT` (default `medium`), records the launch under `.claude/.delegate-log/`, and runs `claude -p` inside the container. Direct `docker exec … claude -p` is blocked by `.claude/hooks/meta-evolution-guard.sh`.

A's deliverable is written to `projects/a/task/ARGUMENT.md` inside its container, which is the same path on the ROOT host via the bind mount. ROOT then runs `scripts/meta/paper-leak-audit.sh projects/a/task/ARGUMENT.md` before judging.
