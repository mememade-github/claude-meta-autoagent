# B cross-cycle seed (committed, tracked)

This directory is B's cross-cycle learning seed.  Unlike
`.claude/agent-memory/`, which is gitignored and wiped between
containers, this path is tracked in the ROOT repository.  The B
container mounts it at `/workspaces/agent-memory-seed/`.

**Lifecycle.**

1. **Before each cycle launch**, ROOT may read, augment, or retain
   entries in `strategies.jsonl` based on the prior cycle's KEEP-class
   /refine outcomes.  Additions must survive a de-duplication pass
   (see Cycle #4 TASK.md §9 "Ingress path for next cycle").
2. **During a cycle**, B's `/refine` skill treats this directory as a
   read-only advisory input alongside `.claude/agent-memory/skills/`.
   B is free to load or ignore individual entries; entries are
   advisory, not mandatory.
3. **After each cycle**, ROOT harvests B's runtime `.claude/agent-memory/
   skills/strategies.jsonl` (which IS gitignored and lives only in the
   container volume), deduplicates, and promotes novel KEEP-class
   entries into this tracked seed.  The ROOT harvest mechanism is a
   `docker exec claude-meta-autoagent-b cat` of the runtime path,
   ROOT-side filter and merge, and a commit to this directory.

**Why this exists.**  Cycle #4 GOAL clause 5 requires that Cycle #4's
B-side artifact for cross-cycle learning be committed to a location
readable by Cycle #5's B container startup.  The gitignored
`.claude/agent-memory/` path does not satisfy that requirement (data
lost between cycles).  This tracked path is the compensating control.

**Policy on contents.**  Entries are first-principles reasoning
patterns observed to work across cycles, *not* domain answers.  If an
entry names a specific canonical result (e.g., a banned identifier
from a cycle), it is stripped before commit.  The seed is meta-level
(how to derive), not object-level (what the answer is).
