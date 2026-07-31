# Audit Discipline

> Source: a prior template audit cycle whose internal pass missed what an
> external re-audit caught — failures clustered in success-criteria scope and
> entry-path coverage.

## 1. Negative-space declaration

Before any audit, state in one sentence per axis what you are *not* checking —
otherwise "all clear" silently means "all clear within my chosen lens". Axes
templates commonly miss: cross-document consistency (counts/ports that disagree
across docs), multi-entry-point parity (DevContainer vs plain `docker compose
up`), rolling-version supply-chain drift, and marketing-vs-technical claims
("isolated"/"sandbox" framing that overstates the trust model). If an excluded
axis later turns out to matter, record it as a *scope error*, not a new finding.

## 2. Counter-test = two axes

Every fix's counter-test verifies both: (a) **positive** — an injected synthetic
violation is detected; (b) **regression** — adjacent paths the audit did not
exercise still hold. For any file edit, explicitly re-check what *other* claims
in the same or co-mounted files must still be true (e.g. a README number fix that
desyncs a co-mounted reference doc).

## 3. Mirror commits: re-verify locally

"Verified upstream" assumes a byte-identical mirror in an identical environment —
rarely fully true (different remote, cache, `.gitignore`, post-commit CI). Re-run
the counter-tests on the mirror; if genuinely redundant, state the basis in the
commit body rather than by silence.

## 4. External cross-check (AUD-2026-008)

Self-audits cannot catch their own scoping errors. Binary test: if the audit
output is reachable by any non-auditor reader (PR review, public docs, governance
commit body, Codex handoff), an external cross-check is **REQUIRED** — a different
vendor agent, an evaluator in a separate context window, or a static analyzer the
primary agent did not pick. Internal-only conclusions: recommended, not required.

## 5. Suspect the measurement, not just the result

A verdict is only as good as the command that produced it. **Never read an exit
code through a pipe** — in `cmd | tail; rc=$?` the `rc` belongs to `tail`, so a
failing gate reports success (fail-open). Redirect to a file and capture `rc`
directly; where a pipe is unavoidable, read `${PIPESTATUS[0]}` (bash-only — POSIX
shells have no equivalent, so the redirect form is the portable one). The same
applies to counters: under `set -e`, `v=$(grep -c ...)` dies on a legitimate zero,
and `$(cmd || echo fallback)` appends the fallback to partial output instead of
replacing it — assign the fallback outside the substitution.

An audit that passed because its measurement was broken is indistinguishable from
an audit that passed. When output looks strange, doubt the command before
reporting the finding.

---
*External anchor: independent-review / separation-of-duties audit practice.*
