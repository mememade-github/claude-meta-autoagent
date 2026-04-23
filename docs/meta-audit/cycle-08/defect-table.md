# Cycle 08 — Defect Table

Per CLAUDE.md §6.7 step 8a verification recipe: every row's Status
column is terminal at cycle close.  No "Partial", "pending",
"deferred", "follow-up", or "TODO" entries appear without an
accompanying "Carry-over to Cycle 9" mark.

| # | Defect / carry-over | Cycle of origin | Status |
|---|---------------------|-----------------|--------|
| 1 | M2.1-hook-write — `.claude/hooks/sub-project-edit-guard.sh` Bash-token guard | Cycle #2 | **Closed (env-constraint)** per `cycle-03/M21-RESOLUTION.md`. |
| 2 | M3.1-refine-architectural-blockage — B's `/refine` on `pre-commit-gate.sh` chain | Cycle #3 | **Closed (reframed Cycle #4; re-confirmed Cycles #5–#8)**.  B's manual-iteration substitute reaches R10 ≥ 2 every cycle since #4. |
| 3 | M5.1 / M6.1-task-ceiling-overshoot — A and B both at R1-R9 = 27/27 | Cycle #5 / #6 | **Closed at Cycle #8**.  A's R1-R9 = 20 under clean-prompt + tightened-rubric; ceiling is no longer the limiting factor. |
| 4 | M6.2-R10-band-0-1-second-edge-case — single-shot + post-hoc audit naming pre-disclosed gaps | Cycle #6 | **Closed** by Cycle #7 pre-cycle rubric port. |
| 5 | M6.3-R10-band-2-3-evaluator-report-substitution — second eval report missing | Cycle #6 | **Closed** by Cycle #7 pre-cycle rubric port + Cycle #8 pre-cycle schema sharpening; Cycle #8 B-R10 = 3 demonstrates the (c) substitute path operational. |
| 6 | M7.1-prompt-hint-leakage — Cycle #7 TASK invited band-3 patterns | Cycle #7 | **Closed at Cycle #8**.  Forward guardrail `task-prompt-discipline.md` ported; Cycle #8 TASK rubric-blind verified at commit; Cycle #8 in-cycle Δ = +6 matches Cycle #6 retrospective +6 baseline. |
| 7 | M7.2-R10-band-3-closure-artefact-tooling — M6.3 had no ROOT tooling | Cycle #7 | **Closed at Cycle #8**.  Schema `gap-closure-check.schema.json` ported; rubric R10 M6.3 sharpened to cite schema fields; B-gap-closure-check.json authored by ROOT with verifier_identity=ROOT for the first time. |
| 8 | Cross-cycle persistence validation — agent-memory-seed/strategies.jsonl path availability in B container | Cycle #4 forward-check | **Operational** — 16 entries consumed at Cycle #8 launch; post-cycle harvest will add seed-17 + seed-18 (see JUDGMENT §5b). |
| 9 | Proof-auditor wiring — CLAUDE.md §6.7 step 5c | Cycle #5 pre-cycle | **Operational** — Cycle #8 audit completed (`rubric-audit.json`); arbitration_triggered = false. |
| 10 | Cleanup forensic on L2→L3 boundary — `scripts/meta/cleanup-sub.sh` | Cycle #6 establish, Cycles #6/#7/#8 validate | **Operational — third consecutive cycle**.  Forensic credential count for both A and B = 0 post-cleanup (will be recorded in cycle-log.md after the cycle-9 close `cleanup-sub.sh --stop` invocation). |

## Verification of clause-3 closure

Per CLAUDE.md §6.7 step 8a, every row of this table must be
terminal at cycle close.  The verification recipe:

```
grep -nE '^\|' docs/meta-audit/cycle-08/defect-table.md \
  | grep -iE '(partial|pending|deferred|follow-up|todo)'
```

Expected output: only rows that also contain "Carry-over to Cycle"
on the same row.  In this defect-table, no rows contain those
status keywords (no carry-overs to Cycle 9 from this cycle's
defect-resolution table).  All M-IDs from Cycle #2 through Cycle
#7 are closed at Cycle #8.
