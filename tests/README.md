# tests/ — reproducible-execution behaviour suite

Every Agent-operational behaviour in this repo (hooks, delegation scripts,
cross-file invariants) is exercised here. Running `bash tests/run.sh` from
any commit produces a deterministic pass/fail verdict tied to that commit's
tree.

## Running

```bash
bash tests/run.sh
```

Exit code 0 ⇔ all assertions pass. Full per-test stdout/stderr is written to
`tests/results/last-run.log` (gitignored). The summary on stdout lists each
test as `pass` or `FAIL <name>`.

No external dependencies beyond `bash`, `jq`, `git`. The harness is a plain
shell runner (`tests/run.sh`) plus tiny assertion helpers in
`tests/lib/assert.sh`; there is no bats/pytest/node requirement.

## Layout

```
tests/
├── run.sh                       # discovery + runner
├── lib/assert.sh                # assert_eq / assert_contains / assert_file_*
├── cases/
│   ├── invariants.sh            # whole-repo properties (orphans, symmetry)
│   ├── hook-session-start.sh
│   ├── hook-pre-commit-gate.sh
│   ├── hook-pre-push-gate.sh
│   ├── hook-meta-evolution-guard.sh
│   ├── hook-sub-project-edit-guard.sh
│   ├── hook-refinement-gate.sh
│   ├── hook-paper-leak-guard.sh
│   ├── hook-web-block.sh
│   ├── script-delegate-goal.sh
│   ├── script-delegate-sub.sh
│   └── script-paper-leak-audit.sh
└── results/                     # gitignored; last-run.log lives here
```

## Coverage

Each row below names one Agent behaviour and the case file that verifies it.

| Agent behaviour | Source | Case |
|---|---|---|
| Session-start context injection (branch, WIP auto-resume, env issues, stale-marker cleanup) | `.claude/hooks/session-start.sh` | `hook-session-start.sh` |
| Pre-commit verification gate (marker freshness, auto-invoked checker) | `.claude/hooks/pre-commit-gate.sh` | `hook-pre-commit-gate.sh` |
| Pre-push credential / URL-drift / declaration gates | `.claude/hooks/pre-push-gate.sh` | `hook-pre-push-gate.sh` |
| Direct `docker exec ... claude -p` block (wrapper enforcement) | `.claude/hooks/meta-evolution-guard.sh` | `hook-meta-evolution-guard.sh` |
| Frozen sub-project edit block (`.frozen` discovery) | `.claude/hooks/sub-project-edit-guard.sh` | `hook-sub-project-edit-guard.sh` |
| /refine Stop-hook loop gate (marker + score + max-iter) | `.claude/hooks/refinement-gate.sh` | `hook-refinement-gate.sh` |
| A/B in-container paper-leak guard (reversed-pattern reconstruction) | `projects/a,b/.claude/hooks/paper-leak-guard.sh` | `hook-paper-leak-guard.sh` |
| A/B WebFetch/WebSearch block | `projects/a,b/.claude/hooks/web-block.sh` | `hook-web-block.sh` |
| Delegation pre-action gates (project-key, slash-command, imperative-steps, length, EFFORT) | `scripts/meta/delegate-goal.sh` | `script-delegate-goal.sh` |
| A/B launcher paper-keyword pre-filter | `scripts/meta/delegate-sub.sh` | `script-delegate-sub.sh` |
| Post-cycle ARGUMENT.md leak scan | `scripts/meta/paper-leak-audit.sh` | `script-paper-leak-audit.sh` |
| No orphan duplicate of CLAUDE.md §1 Behavioral Foundation under `.claude/rules/` | `.claude/rules/`, `projects/b/.claude/rules/` | `invariants.sh` |
| Every `@path` in CLAUDE.md resolves to a file | `CLAUDE.md` | `invariants.sh` |
| Every hook referenced in `settings.json` exists | `.claude/settings.json` | `invariants.sh` |
| A and B ship identical `paper-leak-guard.sh` / `web-block.sh` | both sub-projects | `invariants.sh` |
| `.frozen` markers present on both sub-projects between cycles | `projects/a/.frozen`, `projects/b/.frozen` | `invariants.sh` |
| Every hook script has a shebang | all hooks | `invariants.sh` |

Out of scope for mechanical tests (scored instead by `judgment-rubric.md`):

- Agent prompts (`.claude/agents/*.md`) — markdown only.
- Skill prompts (`.claude/skills/*/SKILL.md`) — markdown only.
- Live A/B cycle artefacts (`ARGUMENT.md`, `JUDGMENT.md`) — per-cycle.

## Writing a new case

Create `tests/cases/<name>.sh`. Each function named `test_*` is auto-
discovered after the file is sourced. Use the assertion helpers; any
failing assertion increments a counter that the runner reads.

```bash
test_my_new_scenario() {
  local out ec
  out=$(bash path/to/script.sh --flag 2>&1)
  ec=$?
  assert_eq 0 "$ec" "exit code"
  assert_contains "$out" "expected phrase" "stdout message"
}
```

## Verification-artefact location

- Live run log: `tests/results/last-run.log` (gitignored, overwritten each run).
- Per-test failures: printed to stdout as `FAIL [<case>::<test>] ...` with the
  offending value.
- No persistent verdict DB — the test suite is a pure function of the tree at
  HEAD. Rerun on any commit to reproduce.
