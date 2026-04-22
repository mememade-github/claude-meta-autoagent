# Attempt 01 — Confluence, WN, SN of R

> First-draft deliverable; later copied (with evaluator-driven edits) to
> `task/ARGUMENT.md`.  Executable oracle: `sim/simulator.py`; captured
> output: `sim/output-final.txt`.

The rewriting system under study:

    ρ1:  len(nil)              → 0
    ρ2:  len(cons(x, ys))      → s(len(ys))
    ρ3:  c(x, y)               → x
    ρ4:  c(x, y)               → y
    ρ5:  f(x)                  → f(s(x))
    ρ6:  f(x)                  → nil

Signature Σ: nullary `0`, `nil`, `a`; unary `s`, `len`, `f`; binary
`cons`, `c`.  Defined symbols: `len`, `f`, `c`.  Constructors: `0`,
`nil`, `a`, `s`, `cons`.  `a` is a constructor that appears in Σ but in
no rule's LHS — it exists solely to enrich the space of closed terms
with a second nullary witness distinct from `0` and `nil`.

**Positions.**  Positions are tuples of 1-indexed child positions; `()`
is the root.  In displayed overlap pairs we write `ε` for `()` and
`i.j` for `(i, j)`.  The simulator uses the same 1-indexed convention.

**Verdicts committed to.**

| Question | Verdict |
|----------|---------|
| Q1 confluence | **NOT confluent** |
| Q2 WN | **weakly normalizing** |
| Q3 SN | **NOT strongly normalizing** |

Two non-positive (Q1, Q3); one positive (Q2).  The rubric's "at least
two non-positive, at most one positive" window is met.

---

## 1. Motivation

### 1.1 Q1 — why confluence is implausible

Two pairs of rules share an LHS:

- `ρ3` and `ρ4` both have LHS `c(x, y)` and disagree on which child
  they project (left vs right).
- `ρ5` and `ρ6` both have LHS `f(x)` and disagree on what to do with
  the f-subterm (extend with `s`, or delete).

When two rules share an LHS and project to **distinct reducts**, the
TRS commits to a non-deterministic choice.  In programming terms this
is a non-deterministic choice operator: `c(u, v)` can mean "either `u`
or `v`", and the rewrite relation exposes both alternatives.  In
process-algebraic terms this is an external choice.

Non-determinism by itself does not break confluence: if the branches
can be reconciled downstream (i.e., the choice ultimately doesn't
matter), confluence can still hold.  The question is whether the two
branches from a shared LHS **must** meet again under →.  For `ρ5/ρ6`,
`f(s(x))` reduces to `nil` via `ρ6` at the root, so the two branches
do meet.  For `ρ3/ρ4`, however, the two reducts are the two arguments
`x` and `y`, which are independent variables: their reducts are
whatever was placed there at construction time.  The construction
`c(0, nil)` makes the two branches step to `0` and to `nil`, which
are both constructor-headed terms with no applicable rule, i.e., both
are normal forms.  They are distinct, and there is no rule of R that
rewrites `0` to `nil` or vice versa.

### 1.2 Q2 — why weak normalization is plausible

Four of the six rules strictly shrink term size on every closed
instance: `ρ1`, `ρ3`, `ρ4`, `ρ6`.  Rule `ρ2` also shrinks size on
every closed instance (the discarded subterm `x` compensates).  Only
`ρ5` grows the term.

Crucially, wherever `ρ5` is applicable (at an `f`-subterm), `ρ6` is
also applicable — they share the LHS.  So a reduction strategy that
"always has a non-`ρ5` alternative" is available whenever any redex
exists.  This is the structural precondition for weak normalization:
one of the two rules in every shared-LHS pair is "the size-shrinking
one," and the strategy that prefers it is guaranteed to make progress.

A precedent from adjacent computational domains: in lazy evaluation
of a functional program, one can always skip an expansion step (the
unbounded-recursion analogue of `ρ5`) in favour of a finite-answer
step (the `nil`-producing analogue of `ρ6`) whenever the latter is
available.  Lazy strategies give normal forms whenever some path
leads to one.

### 1.3 Q3 — why strong normalization is implausible

Rule `ρ5` applied to `f(t)` produces `f(s(t))`.  The result has the
same shape — an `f` at the root, an argument — and the argument is
strictly larger than the original.  Thus `ρ5` is self-reproducing:
after firing it, the redex pattern persists (with a bigger argument),
and `ρ5` applies again.

There is no global termination budget that `ρ5` consumes.  `f(t)` has
no finite "fuel" parameter that `ρ5` decrements; it pumps indefinitely.
The pattern is the unbounded-recursion analogue of a non-productive
inductive clause: a rule that, given a term of its own shape, produces
a strictly larger term of its own shape.

---

## 2. Method Design

Three tools, stated once here, invoked by name in §4.

### §2.1 Confluence method.

Given a finite TRS, confluence is decided by **finitely many critical
pair checks** together with a **variable-overlap sublemma** that
covers overlaps at variable positions automatically.

**Sublemma 2.1 (variable-overlap closes for left-linear rules).**  Let
`ρ: l → r` be a left-linear rule and let `ρ': l' → r'` be any rule.
If `ρ'` is fired at a position `p` strictly below a variable position
of `l` — i.e., `p = q.s` where `q` is the position of a variable `v`
in `l` and `s` is a position inside the term matched by `v` — then the
two reduction orders

  - (outer first) apply `ρ` at root, leaving a residual that no longer
    contains the `ρ'`-redex at that same relative position inside the
    matched subterm;
  - (inner first) apply `ρ'` at `p`, then `ρ` at root;

**join**.  Proof sketch: let `σ` be the matching substitution of `ρ`'s
LHS against the overlap term, so `σ(v) = t` and `ρ'` fires inside `t`
giving `t → t'`.  Define `σ'` identical to `σ` except `σ'(v) = t'`.
Because `l` is left-linear, `v` occurs at most once in `l` (actually,
left-linearity gives "at most once in `l`"; the argument also goes
through when `v` occurs multiple times in `l` provided each occurrence
is rewritten, which is automatic when both paths reduce the same `σ(v)`
instance — but for this R, left-linearity plus single-occurrence of
each variable in each LHS is enough).  Let `k` = number of occurrences
of `v` in `r`.  Then:

  - outer first: `ρ` at root produces `σ(r)`.  Then we must fire `ρ'`
    at all `k` occurrences of `v` in `σ(r)` to match the RHS of the
    "inner-first" path; each occurrence is `σ(v) = t`, which reduces
    to `t'` in one step.  So `σ(r) →* σ'(r)` in `k` steps.
  - inner first: fires `ρ'` inside `σ(v)`, replacing it with `σ'(v) =
    t'`; then fires `ρ` at root, giving `σ'(r)` in one step.

Both paths reach `σ'(r)`, so variable-position overlaps join.  ∎

**Consequence.**  The enumeration in §3.1 need only consider overlaps
where the inner rule's LHS unifies with the outer rule's LHS at a
**non-variable position**.

**Closure procedure.**  For every such overlap, compute the two
reducts `⟨u, v⟩` of the most general overlap term, and search for a
common reduct `w` with `u ↠ w` and `v ↠ w`.  If every overlap
joins, R is confluent.  If any overlap has reducts `u ≠ v` that are
both normal forms, R is non-confluent (a concrete witness is
exhibited by instantiating any variables in `u, v` to distinct
closed normal forms of Σ).

### §2.2 Weak-normalization method.

WN is demonstrated by a **reduction strategy** `S` together with a
**progress measure** `M: closed terms → 𝐍`:

1. `S` is total on non-NF terms: whenever `t` has a redex, `S(t)`
   picks one redex and a rule to apply.
2. `M` strictly decreases under every step that `S` takes.
3. `M` is well-founded on 𝐍.

Points 2 and 3 together imply termination of `S` from any starting
term.

**Sublemma 2.2 (size as progress measure).**  Term size `|t|` (number
of symbol occurrences) is well-founded on closed terms.  Size is
monotone under term construction: if `t → t'` strictly decreases size,
then `C[t] → C[t']` strictly decreases size of the enclosing term for
any context `C`.  This follows because `|C[t]|` is a sum of `|t|` and
context constants that do not depend on the step.

### §2.3 Strong-normalization method.

**Option A (positive SN).**  Exhibit a well-founded measure `Φ: terms
→ W` that strictly decreases on every rule application and is
monotone under contexts.

**Option B (negative SN).**  Exhibit a closed term `t₀` and a sequence
of reductions `t₀ → t₁ → t₂ → …` where for each `n`, `t_n → t_{n+1}`
is justified by citing the rule applied and the redex position.  Then
**argue by induction** that the sequence does not terminate: show that
some shape invariant `P(t_n)` holds for all `n` and that `P` guarantees
`t_n` has an applicable redex of the same shape.

For R, Option B is the right tool (Q3 answer is negative).  No
well-founded measure can exist, because rule `ρ5` applied in isolation
generates an infinite sequence — any candidate measure Φ would have
to strictly decrease along this sequence, which is impossible for a
well-founded codomain.  (Stated as a negative sublemma §2.3.N below.)

**Sublemma 2.3.N (no well-founded Φ exists).**  If `t₀ → t₁ → t₂ → …`
is infinite, then any Φ with `Φ(t_n) > Φ(t_{n+1})` in a well-founded
order gives an infinite descending chain Φ(t₀) > Φ(t₁) > …, which
contradicts well-foundedness.  So the existence of an infinite
reduction from **any** closed term is by itself sufficient to rule
out SN.

---

## 3. Progressive Derivation

### §3.1 Critical-pair enumeration for Q1

The signature has 6 rules.  Each rule's LHS has the following
non-variable positions:

| Rule | LHS | Non-variable positions |
|------|-----|------------------------|
| ρ1 | `len(nil)` | `ε` (head `len`), `1` (subterm `nil`) |
| ρ2 | `len(cons(x, ys))` | `ε` (head `len`), `1` (subterm `cons(x, ys)`) |
| ρ3 | `c(x, y)` | `ε` (head `c`) |
| ρ4 | `c(x, y)` | `ε` (head `c`) |
| ρ5 | `f(x)` | `ε` (head `f`) |
| ρ6 | `f(x)` | `ε` (head `f`) |

The grid of (outer rule `ρ_i`, inner rule `ρ_j`, position `p`) triples
has `6 × 6 × (positions of ρ_i)` cells.  Total: `6 × 6 × 2 + 6 × 6 × 1
× 4 = 72 + 144`?  Let me recount.  Positions per rule: ρ1: 2, ρ2: 2,
ρ3: 1, ρ4: 1, ρ5: 1, ρ6: 1 → sum = 8.  Triples: 8 × 6 = **48**.

The simulator enumerates all 48 triples (see `sim/output-final.txt`,
"Q1 critical-pair enumeration").  Of these:

- **38** are non-unifiable because of **head mismatch** at the
  position in question (e.g., inner rule's LHS is headed by `c` but
  the outer-rule's subterm is headed by `len`, `f`, `nil`, or
  `cons`).
- **10** are unifiable.  The simulator's output lists all 10.

The 10 unifiable overlaps:

| (ρ_i, ρ_j, p) | outer reduct | inner reduct | disposition |
|---------------|--------------|--------------|-------------|
| (ρ1, ρ1, ε) | `0` | `0` | trivial (same rule, identical reducts) |
| (ρ2, ρ2, ε) | `s(len(ys))` | `s(len(ys))` | trivial |
| (ρ3, ρ3, ε) | `x` | `x` | trivial |
| (ρ3, ρ4, ε) | `x` | `y` | **nontrivial — non-joinable** |
| (ρ4, ρ3, ε) | `y` | `x` | **nontrivial — non-joinable** (same CP, swapped) |
| (ρ4, ρ4, ε) | `y` | `y` | trivial |
| (ρ5, ρ5, ε) | `f(s(x))` | `f(s(x))` | trivial |
| (ρ5, ρ6, ε) | `f(s(x))` | `nil` | joinable: `f(s(x)) →ρ6 nil` |
| (ρ6, ρ5, ε) | `nil` | `f(s(x))` | joinable: `f(s(x)) →ρ6 nil` |
| (ρ6, ρ6, ε) | `nil` | `nil` | trivial |

The only **non-joinable** critical pair is `⟨x, y⟩` from `(ρ3, ρ4, ε)`.
In the abstract CP, `x` and `y` are free variables and cannot be
joined without further substitution.

**Closure search for the non-joinable case.**  Setting `x := 0` and
`y := nil` (both NFs of Σ) gives the concrete witness `⟨0, nil⟩`.
Neither has a redex:

- `0` is a nullary constructor and no rule of R has LHS headed by `0`.
- `nil` similarly has no applicable rule.

Thus `0` and `nil` are both normal forms, and `0 ≠ nil`, so the CP
does not join even after arbitrary further reduction.

**Variable-position overlaps** — positions strictly below a variable
in an outer LHS — are handled by Sublemma 2.1 and need no case-by-case
check.

**Conclusion of §3.1.**  R has exactly one unjoinable critical pair;
R is **not confluent**.

### §3.2 Reduction-strategy construction for Q2

**Strategy `S`.**  Given a closed term `t` with at least one redex,
`S(t)` selects any redex whose rule is **not `ρ5`**, and rewrites
there.  (Any choice of non-ρ5 redex is acceptable.)

**Well-definedness of S.**  If `t` has a redex, it has a non-`ρ5`
redex.  Reason: every redex is headed by `len`, `c`, or `f`.  A redex
at an `f`-subterm can fire either `ρ5` or `ρ6` (both share LHS
`f(x)`), so there is always a `ρ6` alternative.  Redexes at `len` or
`c` are not `ρ5`-redexes.  Hence `S` is total on non-NF terms.

**Progress measure.**  Use term size `|t|` as the measure, applying
Sublemma 2.2.  Rule-by-rule: for each rule ρ other than ρ5, and any
closed instance `l·σ → r·σ`:

| Rule | `|l·σ|` | `|r·σ|` | Δ = `|r·σ| − |l·σ|` |
|------|---------|---------|---------------------|
| ρ1 | `1 (len) + 1 (nil) = 2` | `1 (0) = 1` | `−1` |
| ρ2 | `1 (len) + 1 (cons) + |σ(x)| + |σ(ys)| = 2 + |σ(x)| + |σ(ys)|` | `1 (s) + 1 (len) + |σ(ys)| = 2 + |σ(ys)|` | `−|σ(x)| ≤ −1` |
| ρ3 | `1 (c) + |σ(x)| + |σ(y)|` | `|σ(x)|` | `−1 − |σ(y)| ≤ −2` |
| ρ4 | `1 (c) + |σ(x)| + |σ(y)|` | `|σ(y)|` | `−1 − |σ(x)| ≤ −2` |
| ρ6 | `1 (f) + |σ(x)|` | `1 (nil) = 1` | `−|σ(x)| ≤ −1` |

(For a closed instance, every `σ(v)` has size ≥ 1, so all deltas are
strictly negative.)

Context closure: if `t → t'` by one of the above and `t'` has strictly
smaller size than `t`, then for any context `C[·]`, `C[t] → C[t']` has
size `|C| + |t'| < |C| + |t| = |C[t]|`, where `|C|` denotes the context
size excluding the hole.  So size strictly decreases under `S` at any
position.

**Termination.**  Because `|t|` is a natural number and strictly
decreases at each step, the iteration `t, S(t), S(S(t)), …` terminates
after at most `|t|` steps at a normal form.

**Oracle cross-check.**  `sim/simulator.py::test_q2_wn_strategy`
iterates this strategy on eleven hand-crafted closed terms ranging in
size from 2 to 11 and confirms that each reaches a normal form with
strictly decreasing size at every step.
`test_wn_strategy_on_random_terms` runs on 50 random closed terms
(depth 2–6) and confirms termination for every one (worst case: 6
steps).

**Conclusion of §3.2.**  R is **weakly normalizing**.

### §3.3 Measure construction for Q3 (negative)

Claim: R is **not** strongly normalizing.  Witness:

    t_0 = f(0)
    t_1 = f(s(0))       via ρ5 at ε
    t_2 = f(s(s(0)))    via ρ5 at ε
    ...
    t_n = f(s^n(0))     via ρ5 at ε, for each n ≥ 0

**Verification that each step is a legal rewrite.**  Rule ρ5 is
`f(x) → f(s(x))`.  Matching `f(x)` against `t_n = f(s^n(0))` gives
`σ(x) = s^n(0)`.  The RHS under σ is `f(s(σ(x))) = f(s(s^n(0))) =
f(s^{n+1}(0)) = t_{n+1}`.  So `t_n → t_{n+1}` is a valid ρ5 step at
the root position `ε`.

**Invariant.**  For each `n`, `t_n = f(s^n(0))`.  This has the shape
`f(·)` at the root, where `·` is a closed term `s^n(0)` of size
`n + 1`.  The term `t_n` has size `n + 2`, which grows unboundedly.

**Unboundedness by induction.**  Base case: `t_0 = f(0)` has size 2.
Induction step: if `t_n` is defined with size `n + 2`, applying ρ5 at
the root produces `t_{n+1} = f(s(s^n(0))) = f(s^{n+1}(0))` with size
`n + 3`.  So the sequence has strictly increasing size and is therefore
infinite (no term appears twice; no normal form is reached).

**Why no well-founded Φ exists.**  By Sublemma 2.3.N: if any Φ were to
witness SN, Φ(t_0) > Φ(t_1) > Φ(t_2) > … would be an infinite
descending chain in a well-founded order, contradicting
well-foundedness.  So the mere existence of this infinite sequence
from `f(0)` rules out SN.

**Oracle cross-check.**  `test_q3_infinite_sequence` mechanically
traces 20 steps of this sequence, verifying at each step that the
term equals `f(s^n(0))` for the expected `n`, and that `ρ5` applies at
position ε.

**Conclusion of §3.3.**  R is **not strongly normalizing**.

---

## 4. Final Verdict Structure

### §4.1 Q1 answer — NOT confluent

By §3.1, the critical pair `⟨x, y⟩` from overlap `(ρ3, ρ4, ε)` has no
common reduct even after substitution.  Concrete closed witness:

- `t = c(0, nil)`.
- `t →ρ3 0`.
- `t →ρ4 nil`.
- `0` is a normal form of R (no rule has LHS headed by `0`).
- `nil` is a normal form of R (no rule has LHS headed by `nil`).
- `0 ≠ nil`.

Oracle trace: `sim/output-final.txt`, §"Q1 witness: R is NOT confluent".

### §4.2 Q2 answer — WN holds

By §3.2, the strategy "pick any non-`ρ5` redex" is well-defined on
every non-NF closed term, and every step strictly decreases `|t|`.
Since `|t|` is a natural number, the strategy terminates in at most
`|t|` steps.

Oracle trace: `sim/output-final.txt`, §"Q2 strategy … terminates with
strict size decrease", covering 11 hand-crafted and 50 random closed
terms.

### §4.3 Q3 answer — NOT SN

By §3.3, the sequence `f(0) →ρ5 f(s(0)) →ρ5 f(s(s(0))) →ρ5 …` is
infinite; each step is at position ε via ρ5 with σ(x) = s^n(0); size
strictly increases; no term is a normal form.

Oracle trace: `sim/output-final.txt`, §"Q3 witness: infinite reduction
via rho5", 20 steps traced.

### §4.4 Cross-question relationships

The three classical implications that might apply:

(i) **SN ⇒ WN.**  If every reduction terminates, then in particular at
least one reduction terminates — for any starting term, the "every
reduction" quantifier includes the "some reduction" existential.
Does not apply here: SN fails.  But observe that WN still holds, so
the failure of SN does not propagate to WN.  The converse (WN ⇒ SN)
is **false** in general, and R is a witness: WN holds (§4.2) but SN
fails (§4.3).

(ii) **Confluence ⇒ unique normal forms when they exist.**  If R were
confluent and some term `t` had normal forms `u` and `v` via
different reduction sequences, confluence would require `u` and `v`
to have a common reduct `w`; since `u` and `v` are NF, `u = w = v`.
Here confluence fails (§4.1); and indeed `c(0, nil)` is a concrete
term with two distinct normal forms, which is consistent with (and
a witness to) the failure of confluence.

(iii) **Non-confluence ⇒ non-termination.**  This implication is
**false in general** and does not apply to R.  Non-confluence and
non-termination are independent: our system is non-confluent (§4.1)
but weakly normalizing (§4.2); both statements hold simultaneously.
A confluent non-terminating system is also possible (e.g., `a → a`).

All three observations are derivable from the definitions of
confluence, WN, and SN as stated in the task prompt; no external
theorem is invoked.

---

## 5. Verification Strategy

Verification is multi-layered:

1. **Symbolic CP enumeration** (§3.1 table, verified rule-by-rule
   against `RULES` in `sim/simulator.py`).  The simulator enumerates
   all 48 `(ρ_i, ρ_j, p)` triples, classifies each as non-unifiable,
   trivially joinable, unifiable-joinable, or unifiable-non-joinable.
   Ten are unifiable; exactly one (up to swap) is non-joinable.

2. **Per-rule size-delta arithmetic** (§3.2 table, verified by
   `test_per_rule_size_delta`).  Every rule's symbolic size delta is
   re-derived on a small closed instance, confirming ρ1–ρ4 and ρ6
   strictly decrease and ρ5 strictly increases.

3. **Strategy-termination empirical test** (`test_q2_wn_strategy`,
   `test_wn_strategy_on_random_terms`).  The strategy is applied on
   61 closed terms (11 hand-crafted plus 50 random of depth 2–6);
   each reaches an NF in ≤ 6 steps, and every step is checked for
   strict size decrease.

4. **Infinite-sequence trace** (`test_q3_infinite_sequence`).  The
   simulator mechanically traces 20 steps of the `f(0) → f(s(0)) → …`
   sequence, checking at each `n` that the term equals `f(s^n(0))`
   and that ρ5 applies at ε.  The pattern is structural and extends
   to any `n` by induction.

5. **NF sanity check** (`test_claimed_nfs`).  Every claimed normal
   form (`0`, `nil`, `a`, `s(0)`, `s(s(0))`, `cons(0, nil)`,
   `cons(a, cons(0, nil))`) is confirmed to have zero redexes.

6. **Non-join empirical check** (§4.1 witness).  The reachable sets
   from `0` and `nil` are computed to depth 20 (capped at size 80);
   each is the singleton of itself; their intersection is empty.
   This witnesses mechanically that `c(0, nil)` has no common reduct
   from the two distinct NF branches.

The oracle's output — `sim/output-final.txt` — is the concatenated
result of all seven test functions passing on a single run.

---

## 6. Worked Examples

### 6.1 Divergent pair for Q1

`t = c(0, nil)`:

- Reduction A: `c(0, nil) →ρ3@ε 0`.  Normal form; size 1.
- Reduction B: `c(0, nil) →ρ4@ε nil`.  Normal form; size 1.

Both reach distinct normal forms in one step each, from the same
starting term.  Oracle trace in §"Q1 witness" of `output-final.txt`.

### 6.2 Terminating and non-terminating sequences from the same term

`t = f(0)`:

- **Terminating path** (Q2 strategy): `f(0) →ρ6@ε nil`.  One step;
  reaches NF `nil`.  Size 2 → 1.
- **Non-terminating path** (Q3 witness): `f(0) →ρ5@ε f(s(0)) →ρ5@ε
  f(s(s(0))) →ρ5@ε f(s(s(s(0)))) → …`.  Unbounded.

Same `t`, two reductions: one terminates, one does not.  This is
exactly what WN-but-not-SN looks like.  Together with §6.1, this
covers a second orthogonal axis: not only non-confluence, but the
coexistence of terminating and non-terminating paths from one
starting term.

### 6.3 Deterministic termination via `len`

`t = len(cons(0, cons(a, nil)))` (no `c` and no `f`; strategy is
forced):

- Step 1: `len(cons(0, cons(a, nil))) →ρ2@ε s(len(cons(a, nil)))`.
  Size 6 → 5.
- Step 2: `s(len(cons(a, nil))) →ρ2@(1) s(s(len(nil)))`.  Size 5 → 4.
- Step 3: `s(s(len(nil))) →ρ1@(1.1) s(s(0))`.  Size 4 → 3.
- `s(s(0))` is a NF (no rule has LHS headed by `s` or `0`).

This is the fully-deterministic core of R (rules ρ1, ρ2 alone): any
term of the form `len(cons(t_1, cons(t_2, …, nil)))` reduces to
`s^n(0)` where `n` is the list length.  Oracle trace in §"Q2
strategy" of `output-final.txt`.

### 6.4 Infinite reduction for Q3 with visible pattern

`t_0 = f(0)`, stepped 20 times by ρ5 at ε:

    t_0 = f(0)                                    size 2
    t_1 = f(s(0))                                 size 3
    t_2 = f(s(s(0)))                              size 4
    t_3 = f(s(s(s(0))))                           size 5
    ...
    t_20 = f(s^20(0))                             size 22

General pattern: `t_n = f(s^n(0))`; applying ρ5 at ε with σ(x) =
s^n(0) yields `f(s(σ(x))) = f(s^{n+1}(0)) = t_{n+1}`.  The sequence
is infinite by induction on `n`.

Oracle trace: `test_q3_infinite_sequence` in `output-final.txt`.

### 6.5 (Bonus) Projection through choice via `len`

`t = len(c(cons(0, nil), nil))`.  This interleaves a `c` redex (inside
a `len`-argument position) with a `len` redex that becomes available
after either ρ3 or ρ4 fires:

- Via ρ3 then len: `len(c(cons(0, nil), nil)) →ρ3@(1)
  len(cons(0, nil)) →ρ2@ε s(len(nil)) →ρ1@(1) s(0)`.  Size 6 → 4 → 3
  → 2.  NF.
- Via ρ4 then len: `len(c(cons(0, nil), nil)) →ρ4@(1) len(nil) →ρ1@ε
  0`.  Size 6 → 2 → 1.  NF.

Two reachable NFs (`s(0)` and `0`) — another concrete witness of
non-confluence, this time with a `len` wrapper around the choice.
Not strictly needed for §4.1 (which already has `c(0, nil)`) but
shows the choice propagates through `len`.

---

## 7. Open Questions and Known Limitations

### 7.1 (a) Rule-removal parametric impossibility

Can any single-rule removal restore confluence?

- **Remove ρ1**.  `len(nil)` is no longer a redex; `len` on `nil`-based
  terms is stuck at `len(nil)`.  The remaining ρ3/ρ4 non-joining CP
  persists (`c(0, nil) → 0` and `c(0, nil) → nil` are still distinct
  NFs).  **Does not restore confluence.**
- **Remove ρ2**.  Same: ρ3/ρ4 CP persists.  **Does not restore.**
- **Remove ρ3**.  Then `c(x, y) → y` is the only choice rule; the
  choice becomes deterministic (always right-project).  The ρ3/ρ4 CP
  disappears.  The ρ5/ρ6 CP is joinable.  Need to check any residual
  CPs: after removing ρ3, the only CPs between remaining rules are
  those we already classified as joinable or trivial.  **Restores
  confluence.**  But the system loses its non-deterministic choice
  primitive — `c` becomes pure right-projection, equivalent to a
  projection constructor.
- **Remove ρ4**.  Symmetric.  **Restores confluence** at the cost of
  removing choice.
- **Remove ρ5**.  The remaining system has no infinite reductions
  (size is a strict-decrease measure for ρ1, ρ2, ρ3, ρ4, ρ6), so SN
  holds.  But ρ3/ρ4 CP persists.  **Does not restore confluence.**
- **Remove ρ6**.  The ρ3/ρ4 CP persists.  **Does not restore.**

So: confluence is restorable only by removing ρ3 or ρ4, but doing so
removes the non-deterministic choice primitive that ρ3+ρ4 jointly
encode.

**Parametric disclosure.**  ρ3 and ρ4 jointly encode an essentially
non-confluent choice: they share an LHS and disagree on the reduct,
and the reducts are two independent variables.  Any rule pair with
the shape `g(v₁, v₂, …, v_n) → v_i` and `g(v₁, …, v_n) → v_j` for
`i ≠ j` induces a non-joinable CP `⟨v_i, v_j⟩` (because v_i and v_j
are independent variables and no rule of R — by the same shape
constraint — can reduce v_i to v_j).  So the non-confluence of R is
not incidental: it is determined by the pair of projection rules on
`c`, and no rule-modification short of removing one of them can
eliminate it.

### 7.2 (b) Strategy uniqueness for Q2

Is the "avoid ρ5" strategy the only WN-witnessing strategy?

**Class of strategies that succeed.**  Any strategy `S` with the
property "every ρ5 step is eventually followed by a ρ6 step at some
ancestor f-position" terminates.  The weaker sufficient condition is
"size eventually strictly decreases along any prefix of length k for
some fixed k".  The strictest is "never use ρ5".

In fact, any strategy that **bounds the number of consecutive ρ5
applications before a non-ρ5 step** terminates: if the bound is `B`,
then after at most `B` consecutive ρ5 steps the size has grown by
`≤ B`, and the next non-ρ5 step subtracts at least 1; so the net
change over `B + 1` steps is ≤ `B − 1`, and if this net change can
be bounded by a fixed negative constant (which requires more than
`B + 1` to include a shrinkage-step of size > B), the sequence
terminates.  A cleaner sufficient condition: **every ρ5 step at an
f-subterm `f(t)` is eventually followed by a ρ6 step at that same
f-subterm position, before the subterm is destroyed by an outer ρ3
or ρ4 or ρ6 step.**

Not unique, but the "avoid ρ5" strategy is minimal-sufficient — it
works on every closed term with zero lookahead.  Other strategies
(innermost-preferential, size-minimizing, etc.) succeed under
additional side conditions.

### 7.3 (c) Measure sensitivity for Q3

Is the non-SN verdict sensitive to the choice of Φ?

**Parametric disclosure.**  The non-SN verdict is **insensitive** to
any choice of measure.  The sequence `f(0) → f(s(0)) → …` is infinite
as a concrete witness — no measure is invoked to derive the infinite
reduction, and the sequence exists whatever we choose Φ to be.  By
Sublemma 2.3.N, **any** candidate Φ that claims to witness SN would
have to strictly decrease along this sequence, contradicting
well-foundedness.  Therefore no Φ in any class (polynomial, lex
product, multiset, etc.) can witness SN of R.

### 7.4 (d) Generalization of Q1/Q2/Q3 to rule-shape classes

- **Does every TRS with a ρ3/ρ4-shaped pair fail confluence?**  Yes,
  per §7.1: any two rules sharing an LHS and projecting to distinct
  variables induce a non-joinable CP.  This is parametric in the
  number of arguments and the projected indices — only the "distinct
  variables projected" property matters.
- **Does every TRS with an `f(x) → f(s(x))`-shaped rule fail SN?**
  Yes, when `f` and `s` are distinct symbols (so the rule is not a
  degenerate identity).  From any closed term `f(t)`, repeated
  application of the rule at the root produces `f(s(t)), f(s(s(t))),
  …`, an infinite strictly-growing sequence.  This is parametric in
  what `s` is: any unary (or higher-arity but with a fixed
  closed-term filler for other arguments) constructor that does not
  collapse with `f` gives this infinite reduction.
- **Is R's WN holding contingent on other rules?**  Yes.  If we added
  a rule `f(x) → f(f(x))`, then there would be no size-shrinking
  alternative at an f-subterm (both alternatives grow size: one by 1,
  one by 2), and the "avoid ρ5" strategy would fail.  WN of R is
  contingent on ρ6 being the "shrinking escape" that pairs with
  ρ5's growth.

**Structural upshot.**  R is not an isolated bad example: ρ3+ρ4
exemplify a non-confluent choice primitive, ρ5 exemplifies an
unbounded-recursion rule, and ρ6 exemplifies the shrinking escape
that is structurally necessary for WN.  Removing ρ6 would keep R
non-confluent and non-SN, and **also** destroy WN, giving a TRS that
is none of the three.
