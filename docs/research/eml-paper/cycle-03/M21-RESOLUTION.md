# Cycle #3 — M2.1-hook-write carry-over: terminal resolution

**Handle.** `M2.1-hook-write` (tracked in `cycle-log.md` Cycle #2 entry).
**Cycle #3 role.** `cycle-03/TASK.md` §1 names step 0 pre-cycle prep as
the "explicit landing target" for this carry-over. This file discharges
that landing as a **structural close-out under path (b)** of the
Cycle #3 GOAL: the carry-over is closed not by applying the specified
hook + settings edits, but by documenting an environment constraint
that is outside the agent's autonomous modification authority, and
recording the compensating controls that keep the defect contained.

Second carry-over (option (c) in the Cycle #3 GOAL) is prohibited:
once a defect has been carried once and the underlying blocker has not
moved, carrying it again is a §4.2 no-partial-ship violation and a
§1.4 end-state-verifiable violation.

---

## 1. What M2.1 is

Stated in `cycle-02/JUDGMENT.md` §8 row 1: the
`.claude/hooks/sub-project-edit-guard.sh` hook matches only the `Edit`
and `Write` tool families. A ROOT agent could, in principle, bypass
frozen-sub-project protection by issuing a `Bash` call whose
`tool_input.command` contains a write-implying token (`>`, `>>`,
`sed -i`, `rm`, `mv`, `cp`, `tee`, `truncate`, `install`, `touch`,
`chmod`, `chown`, `ln`, `rsync`, `dd`, or `git checkout|restore|reset|
rm|mv|clean|apply|stash|add`) paired with a path under
`projects/<frozen>/`. The `.claude/settings.json` matcher list
currently registers the hook only for `Edit|Write`, not `Bash`.

The planned fix, fully specified at Cycle #2 scoring time and preserved
in `cycle-02/JUDGMENT.md` §8:

1. Extend `sub-project-edit-guard.sh` to inspect `tool_input.command`
   when the tool is `Bash`, applying a write-token regex scan against
   every discovered frozen sub-project path, with a whitelist for the
   `.frozen` marker itself so §6.7 step 0's marker remove/restore
   remains operable.
2. Add a `Bash` matcher entry in `.claude/settings.json`'s
   `hooks.PreToolUse` block that routes `Bash` tool calls into the
   same hook.

Both edits are surgical (≤ 80 lines in the hook, 3 lines in settings)
and fully scoped.

## 2. Why the fix did not land

The fix attempt at the start of Cycle #3 was blocked by the environment's
sensitive-file permission policy, which denies non-interactive writes to
any path under `.claude/hooks/**` and to `.claude/settings.json`. The
denial is mechanical: the tool call returns a permission-request block
rather than the edit itself, and no interactive escalation channel is
available in this autonomous-delegation session.

**Evidence.** The same policy was observed during Cycle #2 PM (see
`cycle-02/JUDGMENT.md` §8 row 1 "the environment's sensitive-file
policy currently denies non-interactively"; and the post-cycle ROOT
note "The G5 integrity axis for B's evaluator was attempted as a
direct edit to `projects/b/.claude/agents/evaluator.md` … The edit was
blocked by the environment's sensitive-file policy, which extends to
any `.claude/**` path including sub-project `.claude/` trees").
Cycle #3 attempted the same `.claude/hooks/sub-project-edit-guard.sh`
edit and received the same mechanical denial.

**Why this is not an agent-side defect.** The agent role the
Cycle #3 Human GOAL names (Level 2 ROOT) can produce the patch content
and the exact edit operations; what it cannot produce is the harness
consent to apply those operations. Consent lives with the user's
Claude Code configuration (`~/.claude/settings.json` permission mode
or project-level `.claude/settings.local.json` permission overrides),
which is a Level-0 / Level-1 artefact in the four-layer role table at
CLAUDE.md §6.1, not a Level-2 one.

**Why this counts as structural, not procedural.** A procedural
obstacle is one that another cycle could plausibly clear: new
information, a retry with different tooling, a fix to a bug in the
agent's plan. None of that applies here. The hook + settings edits
have been specified at the same level of detail since Cycle #2
JUDGMENT; further cycles of the same agent at the same permission
level will hit the same denial. The obstacle is the permission
configuration itself, which the agent cannot modify from inside the
role it occupies.

## 3. Compensating controls that keep M2.1 contained

The defect is contained to the extent that the following mitigations
are operative.

1. **Behavioural discipline (§1.3 Surgical Changes + §6.3).**  ROOT
   is instructed to not edit A during a cycle and to confine itself to
   documented edit paths on B (between JUDGMENT and the B-improvement
   commit, via unfreeze/edit/refreeze). The hook's Edit/Write coverage
   catches direct tool-level violations. Bash-level violations would
   have to be written by an agent that had already decided to
   circumvent the marker, which is a different (higher-severity)
   failure than a missed hook rule.

2. **Post-hoc diff audit (§6.7 step 8).**  Every cycle closes with
   `git diff cycle-NN-pre -- projects/a/` and the same on `projects/b/`
   restricted to ROOT-improvement scope. Any unexplained write to
   frozen sub-project paths — regardless of whether it came via
   Edit/Write or Bash — is caught by this diff and triggers rollback.
   The diff audit is a deterministic, after-the-fact check that does
   not depend on the hook's coverage.

3. **Forward-coverage tests (tests/cases/hook-sub-project-edit-guard.sh).**
   Cycle #2 added three Bash test cases that pass against both the
   current permissive hook and the planned post-fix hook (`.frozen`
   toggle allowed, read-only allowed, outside-frozen write allowed).
   These tests remain green; they do not themselves close the hole,
   but they prevent regression of the non-write cases when the hook
   is eventually extended.

4. **Partial-defect audit (CLAUDE.md §6.7 step 8a).** The same audit
   that caught the initial Cycle #2 partial-ship will catch any
   future "hook still unchanged" status claim, keeping the defect
   visible until it is either fixed or closed — and this file is
   the close-out.

## 4. Resolution decision

**M2.1-hook-write is closed as environment-constraint.** Status in
`cycle-log.md` flips from "Carry-over to Cycle #3" to
"Closed — env-constraint (sensitive-file policy); compensating
controls §3 of `cycle-03/M21-RESOLUTION.md`".

**Re-opening trigger.** If at any future point the sensitive-file
permission policy is lifted — either by a session run under a more
permissive permission mode, or by a Level-1 user action that adds the
relevant paths to the session allowlist — the hook rewrite and the
settings matcher addition, as specified in `cycle-02/JUDGMENT.md` §8
and retained here by reference, are to be applied in a single commit
bundled with the three complementary blocking Bash test cases
(`sed -i` / `rm` / redirection into frozen must exit 2). Re-opening is
not a Cycle #N carry-over; it is a one-shot policy-driven commit
that can be applied in any cycle's step-0 prep or between cycles.

**Second carry-over prohibited.** Per the Cycle #3 GOAL clause 2 and
CLAUDE.md §4.2, this defect cannot be carried to Cycle #4 or beyond
under the same environment constraint. Any future status claim of
"M2.1-hook-write: Carry-over to Cycle N" is, by this file's
publication, a protocol violation — the defect has to be either in
"Closed — env-constraint" (this file's disposition), or "Resolved"
(with the hook + settings commit landed).

## 5. Companion document for G5 axis

The evaluator.md direct edit that was also blocked by the same
policy during Cycle #2 PM (see `cycle-02/cycle-log.md` Post-cycle
ROOT note, second bullet) is tracked separately as a Cycle #3 G5
axis delivery note. It rides the TASK.md §7 channel for this cycle
(refinement-contract instruction delivered to B through the normal
delegation prompt) and is not subject to this file's close-out.

---

**Signed off in Cycle #3 pre-cycle prep commit (tagged `cycle-03-pre`).**
