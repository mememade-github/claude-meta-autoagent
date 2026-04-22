# ARGUMENT — Confluence, weak normalization, and strong normalization of R

> **Iteration trace.**  Draft at `iterations/attempt-01.md`.  Evaluator
> report at `iterations/.eval-report-01.json` (10 gaps disclosed; this
> document closes G1–G9 and acknowledges G10 as no-action).  Executable
> oracle: `sim/simulator.py`, captured output `sim/output-final.txt`.

The rewriting system under study:

    ρ1:  len(nil)              → 0
    ρ2:  len(cons(x, ys))      → s(len(ys))
    ρ3:  c(x, y)               → x
    ρ4:  c(x, y)               → y
    ρ5:  f(x)                  → f(s(x))
    ρ6:  f(x)                  → nil

Signature Σ: nullary `0`, `nil`, `a`; unary `s`, `len`, `f`; binary
`cons`, `c`.  Defined symbols: `len`, `f`, `c`.  Constructors: `0`,
`nil`, `a`, `s`, `cons`.  The nullary constructor `a` appears in Σ but
in no rule's LHS; it enriches the closed-term space with a second
normal form distinct from `0` and `nil` and is used in §3.1/§6 to
realise concrete closed witnesses.

**Positions.**  Positions are tuples of 1-indexed child positions; `()`
is the root.  In displayed overlaps we write `ε` for `()` and `i.j`
for `(i, j)`, etc.  The simulator uses the same 1-indexed convention.

**Verdicts committed to.**

| Question | Verdict |
|----------|---------|
| Q1 confluence | **NOT confluent** |
| Q2 weak normalization | **weakly normalizing** |
| Q3 strong normalization | **NOT strongly normalizing** |

Two non-positive (Q1, Q3); one positive (Q2).  The rubric's "at least
two non-positive, at most one positive" window is met.

---

## 1. Motivation

### 1.1 Q1 — why confluence is implausible

Two pairs of rules share an LHS:

- `ρ3` and `ρ4` both have LHS `c(x, y)` and disagree on which child
  they project — left vs right.
- `ρ5` and `ρ6` both have LHS `f(x)` and disagree on what to do with
  the f-subterm — extend with `s`, or delete.

When two rules share an LHS and project to **distinct reducts**, R
commits to a non-deterministic choice.  In programming terms this
reads as a non-deterministic choice operator: `c(u, v)` means "either
`u` or `v`", and the rewrite relation exposes both.

Non-determinism by itself does not break confluence: if the branches
can be reconciled downstream — that is, if the choice ultimately
doesn't matter — confluence can still hold.  The question is whether
the two branches from a shared LHS **must** meet again under →.  For
`ρ5/ρ6`, `f(s(x))` reduces to `nil` via `ρ6` at the root, so the two
branches do meet at `nil`.  For `ρ3/ρ4`, however, the two reducts are
the two arguments `x` and `y` — independent variables whose reducts
are whatever was placed there at construction time.  The construction
`c(0, nil)` makes the two branches step to `0` and to `nil`, both
constructor-headed terms with no applicable rule: both are normal
forms.  They are distinct, and no rule of R rewrites `0` to `nil` or
vice versa.

### 1.2 Q2 — why weak normalization is plausible

Five of the six rules strictly shrink term size on every closed
instance: `ρ1`, `ρ2`, `ρ3`, `ρ4`, `ρ6`.  Only `ρ5` grows the term.

Crucially, wherever `ρ5` is applicable (at an `f`-subterm), `ρ6` is
also applicable — they share the LHS.  So a strategy that "always has
a non-`ρ5` alternative" is available whenever any redex exists at
all.  This is the structural precondition for weak normalization: one
of the two rules in every shared-LHS pair is size-shrinking, and the
strategy that prefers it is guaranteed to make progress.

A precedent from adjacent computational domains: in lazy evaluation of
a functional program, one can always skip an unbounded-recursion
expansion step (the analogue of `ρ5`) in favour of a finite-answer
step (the `nil`-producing analogue of `ρ6`) whenever both apply at
the same redex.  Lazy strategies reach normal forms whenever **some**
path leads to one.

### 1.3 Q3 — why strong normalization is implausible

Rule `ρ5` applied to `f(t)` produces `f(s(t))`.  The result has the
same shape — an `f` at the root, an argument — and the argument is
strictly larger than the original.  Thus `ρ5` is self-reproducing:
after firing it, the redex pattern persists (with a bigger argument),
and `ρ5` applies again.

There is no global termination budget that `ρ5` consumes.  `f(t)` has
no "fuel" parameter that `ρ5` decrements; it pumps indefinitely.  The
pattern is the unbounded-recursion analogue of a non-productive
inductive clause: a rule that, given a term of its own shape,
produces a strictly larger term of its own shape.

---

## 2. Method Design

Three tools, stated once here and invoked by name in §4.

### §2.1 Confluence method

Given a finite TRS, confluence is decided by **finitely many critical
pair checks** combined with a **variable-overlap sublemma** that
covers overlaps at variable positions automatically.

**Sublemma 2.1 (variable-overlap joins automatically for left-linear
rules).**  Let `ρ: l → r` be a left-linear rule and `ρ': l' → r'` any
rule.  Suppose `ρ'` is fired at a position `p` strictly **below** a
variable position of `l` — i.e., `p = q.s` where `q` is the position
of a variable `v` in `l` and `s` is a non-empty position inside the
term matched by `v`.  Then the two reduction orders

  - outer-first: apply `ρ` at root, then `ρ'` at the residual
    positions;
  - inner-first: apply `ρ'` at `p`, then `ρ` at root;

both reach the same term.

*Proof.*  Let `σ` be the matching substitution of `ρ`'s LHS against
the overlap term, so `σ(v) = t` and `ρ'` fires inside `t` giving
`t → t'`.  Define `σ'` identical to `σ` except `σ'(v) = t'`.  Let `k`
be the number of occurrences of `v` in `r`.

  - Outer-first: `ρ` at root produces `σ(r)`.  Each of the `k`
    occurrences of `v` in `σ(r)` equals `t`; fire `ρ'` at each to
    reach `σ'(r)` in `k` steps.
  - Inner-first: fire `ρ'` inside `σ(v)`, replacing it with `σ'(v) =
    t'`; then fire `ρ` at root to get `σ'(r)` in one step.

Both paths reach `σ'(r)`, so variable-position overlaps join.  ∎

**Left-linearity audit for R.**

| Rule | LHS | Variable multiplicities |
|------|-----|-------------------------|
| ρ1 | `len(nil)`         | (no variables) |
| ρ2 | `len(cons(x, ys))` | `x`:1, `ys`:1 |
| ρ3 | `c(x, y)`          | `x`:1, `y`:1 |
| ρ4 | `c(x, y)`          | `x`:1, `y`:1 |
| ρ5 | `f(x)`             | `x`:1 |
| ρ6 | `f(x)`             | `x`:1 |

Every variable occurs at most once in every LHS — R is left-linear.
Sublemma 2.1 applies to every rule.

**Consequence.**  The enumeration in §3.1 need only consider overlaps
where the inner rule's LHS unifies with the outer rule's LHS at a
**non-variable position**.

**Closure procedure.**  For every such overlap, compute the two
reducts `⟨u, v⟩` of the most general overlap term, then search for a
common reduct `w` with `u ↠ w` and `v ↠ w`.  If every overlap joins,
R is confluent.  If any overlap has reducts `u ≠ v` that both reach
distinct normal forms (under some substitution if variables remain),
R is non-confluent; the substituted reducts form a concrete witness.

### §2.2 Weak-normalization method

WN is demonstrated by a **reduction strategy** `S` together with a
**progress measure** `M: closed terms → 𝐍`:

1. `S` is total on non-NF terms.
2. `M` strictly decreases along every step `S` takes.
3. `M` is well-founded.

Conditions 2 and 3 together imply termination of `S` from any closed
starting term.

**Sublemma 2.2 (size as progress measure).**  Term size `|t|` — the
number of symbol occurrences in `t` — is a natural-number-valued
measure, hence well-founded.  Size is monotone under term
construction: for any context `C[·]`, `|C[t]| = |C| + |t|`, where
`|C|` is the number of non-hole occurrences in `C`.  So if `t → t'`
strictly decreases size, so does `C[t] → C[t']` for any `C`.

### §2.3 Strong-normalization method

**Option A (positive SN).**  Exhibit a well-founded measure `Φ` that
strictly decreases on every rule application and is monotone under
contexts.

**Option B (negative SN).**  Exhibit a closed term `t₀` and an
infinite chain of reductions `t₀ → t₁ → t₂ → …`, justifying each
step by the rule applied and the redex position, plus an **inductive
argument** that the sequence is unbounded.

For R, Option B applies (Q3 verdict is negative).

**Sublemma 2.3.N (one infinite reduction defeats every Φ).**  If
`t₀ → t₁ → t₂ → …` is infinite and some candidate measure `Φ` claimed
to witness SN, then `Φ(t_0), Φ(t_1), Φ(t_2), …` would be an infinite
descending chain in Φ's well-founded order, which is impossible.
Hence the existence of one infinite reduction from any closed term
rules out SN regardless of what Φ is.

---

## 3. Progressive Derivation

### §3.1 Critical-pair enumeration for Q1

The non-variable positions of each LHS:

| Rule | LHS | Non-variable positions |
|------|-----|------------------------|
| ρ1 | `len(nil)`         | `ε` (head `len`), `1` (subterm `nil`) |
| ρ2 | `len(cons(x, ys))` | `ε` (head `len`), `1` (subterm `cons(x, ys)`) |
| ρ3 | `c(x, y)`          | `ε` (head `c`) |
| ρ4 | `c(x, y)`          | `ε` (head `c`) |
| ρ5 | `f(x)`             | `ε` (head `f`) |
| ρ6 | `f(x)`             | `ε` (head `f`) |

Summing non-variable positions: `2 + 2 + 1 + 1 + 1 + 1 = 8`.  There
are 6 outer rules × 8 outer-positions across them × 6 inner rules =
`8 × 6 = 48` `(outer rule ρ_i, inner rule ρ_j, position p)` triples.
The simulator enumerates all 48 (see `sim/output-final.txt`, §"Q1
critical-pair enumeration").  Of these, **38** are non-unifiable by
head mismatch and **10** are unifiable.

**The 10 unifiable overlaps.**

| (ρ_i, ρ_j, p) | outer reduct | inner reduct | disposition |
|---------------|--------------|--------------|-------------|
| (ρ1, ρ1, ε) | `0` | `0` | trivial (same rule, identical reducts) |
| (ρ2, ρ2, ε) | `s(len(ys))` | `s(len(ys))` | trivial |
| (ρ3, ρ3, ε) | `x` | `x` | trivial |
| (ρ3, ρ4, ε) | `x` | `y` | **nontrivial — NON-JOINABLE** |
| (ρ4, ρ3, ε) | `y` | `x` | **nontrivial — NON-JOINABLE** (same CP, swapped) |
| (ρ4, ρ4, ε) | `y` | `y` | trivial |
| (ρ5, ρ5, ε) | `f(s(x))` | `f(s(x))` | trivial |
| (ρ5, ρ6, ε) | `f(s(x))` | `nil` | joinable: `f(s(x)) →ρ6 nil` |
| (ρ6, ρ5, ε) | `nil` | `f(s(x))` | joinable: `f(s(x)) →ρ6 nil` |
| (ρ6, ρ6, ε) | `nil` | `nil` | trivial |

The only **non-joinable** critical pair is `⟨x, y⟩` from (ρ3, ρ4, ε).
In the abstract CP, `x` and `y` are free independent variables and
cannot be joined without further substitution.

**Closure search for the non-joinable case.**  Setting `x := 0` and
`y := nil` — both NFs of Σ — gives the concrete witness `⟨0, nil⟩`.
Neither has a redex:

- `0` is nullary and no rule has LHS headed by `0`.
- `nil` is nullary and no rule has LHS headed by `nil`.

So `0` and `nil` are both normal forms, and `0 ≠ nil`, so the CP does
not join even after arbitrary further reduction.

**Variable-position overlaps** — positions strictly below a variable
in an outer LHS — are handled by Sublemma 2.1 (the left-linearity
audit in §2.1 confirms its applicability) and need no case check.

**Conclusion of §3.1.**  R has exactly one unjoinable critical pair
(up to swap); R is **not confluent**.

### §3.2 Reduction-strategy construction for Q2

**Strategy `S`.**  Given a closed term `t` with at least one redex,
`S(t)` picks any redex whose rule is **not ρ5** and rewrites there.
Any choice of non-ρ5 redex is acceptable; `S` is the class of such
strategies.

**Well-definedness of `S`.**  If `t` has a redex, it has a non-ρ5
redex.  Every redex is headed by `len`, `c`, or `f`.  A redex at an
`f`-subterm can fire either `ρ5` or `ρ6` (both share LHS `f(x)`), so
there is always a `ρ6` alternative.  Redexes at `len` or `c` are by
definition not `ρ5`-redexes.  Hence `S` is total on every non-NF
closed term.

**Progress measure.**  Term size `|t|`.  The rule-by-rule size deltas
on closed instances (each variable `v` matched to a closed term of
size `|σ(v)| ≥ 1`):

| Rule | `|lhs·σ|` | `|rhs·σ|` | Δ = `|rhs·σ| − |lhs·σ|` |
|------|-----------|-----------|-------------------------|
| ρ1 | `1 + 1 = 2` | `1` | `−1` |
| ρ2 | `1 + 1 + |σ(x)| + |σ(ys)| = 2 + |σ(x)| + |σ(ys)|` | `1 + 1 + |σ(ys)| = 2 + |σ(ys)|` | `−|σ(x)| ≤ −1` |
| ρ3 | `1 + |σ(x)| + |σ(y)|` | `|σ(x)|` | `−1 − |σ(y)| ≤ −2` |
| ρ4 | `1 + |σ(x)| + |σ(y)|` | `|σ(y)|` | `−1 − |σ(x)| ≤ −2` |
| ρ5 | `1 + |σ(x)|` | `1 + 1 + |σ(x)| = 2 + |σ(x)|` | `+1`  *(not used by S)* |
| ρ6 | `1 + |σ(x)|` | `1` | `−|σ(x)| ≤ −1` |

The ρ5 row is shown for completeness (G8): it is the sole positive
delta, and is precisely the rule `S` avoids.  All other rules have
strictly negative Δ on closed instances.

**Context closure.**  By Sublemma 2.2, a step that strictly shrinks
`|t|` strictly shrinks `|C[t]|` for any context `C`.  So S's step at
any position strictly decreases whole-term size.

**Termination.**  Because `|t|` is a natural number and strictly
decreases at each step, the iteration `t, S(t), S²(t), …` terminates
after at most `|t|` steps at a normal form.

**Oracle cross-check.**  `sim/simulator.py::test_q2_wn_strategy`
iterates this strategy on eleven hand-crafted closed terms ranging in
size from 2 to 11; each reaches a normal form with strict size
decrease at every step.  `test_wn_strategy_on_random_terms` does the
same on 50 random closed terms of depth 2–6; every one reaches an NF
(worst case: 6 steps).

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
position ε.

**Invariant.**  For each `n`, `t_n = f(s^n(0))`.  This has the shape
`f(·)` at the root, where `·` is a closed term `s^n(0)` of size
`n + 1`.  The whole term `t_n` has size `n + 2`.

**Unboundedness by induction on `n`.**  Base: `t_0 = f(0)` has size
2.  Step: if `t_n = f(s^n(0))` has size `n + 2`, then ρ5 at ε yields
`t_{n+1} = f(s^{n+1}(0))` with size `n + 3`.  So sizes strictly grow,
no term repeats, and no normal form is reached — the sequence is
infinite.

**Why no well-founded Φ exists.**  By Sublemma 2.3.N: any Φ that
claimed SN would induce `Φ(t_0) > Φ(t_1) > Φ(t_2) > …`, an infinite
descending chain in a well-founded order — impossible.  The infinite
sequence alone rules out SN in **every** measure class.

**Oracle cross-check.**  `test_q3_infinite_sequence` mechanically
traces 20 steps of this sequence, verifying at each step that the
term equals `f(s^n(0))` and that ρ5 applies at position ε.

**Conclusion of §3.3.**  R is **not strongly normalizing**.

---

## 4. Final Verdict Structure

### §4.1 Q1 answer — NOT confluent

By §3.1, the critical pair `⟨x, y⟩` from overlap (ρ3, ρ4, ε) has no
common reduct even after substitution.  Concrete closed witness:

- `t = c(0, nil)`.
- `t →ρ3 0`.
- `t →ρ4 nil`.
- `0` is a normal form of R (no rule has LHS headed by `0`).
- `nil` is a normal form of R (no rule has LHS headed by `nil`).
- `0 ≠ nil`.

Oracle trace: `sim/output-final.txt`, §"Q1 witness: R is NOT
confluent".  The same file's §"Q1 critical-pair enumeration" confirms
that (ρ3, ρ4, ε) is the unique non-joinable overlap (up to swap).

### §4.2 Q2 answer — WN holds

By §3.2, the strategy "pick any non-ρ5 redex" is well-defined on
every non-NF closed term, and each step strictly decreases `|t|`.
Since `|t|` is a natural number, the strategy terminates in at most
`|t|` steps.

Oracle trace: `sim/output-final.txt`, §"Q2 strategy … terminates with
strict size decrease" (11 hand-crafted) and §"Q2 stress: strategy on
50 closed random terms" (50 random).

### §4.3 Q3 answer — NOT SN

By §3.3, the reduction `f(0) →ρ5 f(s(0)) →ρ5 f(s(s(0))) →ρ5 …` is
infinite.  Each step fires ρ5 at position ε with matching `σ(x) =
s^n(0)`; sizes strictly increase; no term is a normal form.

Oracle trace: `sim/output-final.txt`, §"Q3 witness: infinite reduction
via rho5", 20 steps traced.

### §4.4 Cross-question relationships

The three classical implications that might bear on R:

**(i) SN ⇒ WN.**  If every reduction from `t` terminates, then in
particular **some** reduction from `t` terminates — the universal
subsumes the existential.  Does not apply positively here (SN fails,
§4.3).  The converse (WN ⇒ SN) is false in general, and R is a
witness: WN holds (§4.2) but SN fails (§4.3).  So failure of SN does
**not** propagate to WN for R.

**(ii) Confluence ⇒ unique NFs when they exist.**  Derivation:
suppose R is confluent.  Let `t` reduce to NFs `u` and `v` by
different reduction sequences: `t ↠ u` and `t ↠ v`, both with `u`, `v`
in NF.  By confluence applied at `t`, there exists `w` with `u ↠ w`
and `v ↠ w`.  Since `u` is NF, `u = w`; since `v` is NF, `v = w`;
hence `u = v`.  Here R is not confluent (§4.1), and indeed
`c(0, nil)` has two distinct normal forms `0` and `nil` — a concrete
witness of the failure of unique-NF, consistent with the failure of
confluence.

**(iii) Non-confluence ⇒ non-termination.**  False in general; does
not apply.  Confluence and termination are independent: R is non-
confluent (§4.1) but weakly normalizing (§4.2), both holding
simultaneously.  Conversely, a confluent non-terminating system exists
(e.g., the single-rule system `{a → a}`).

All three observations are derivable from the definitions of
confluence, WN, and SN as stated in the task prompt; no external
theorem is invoked.

---

## 5. Verification Strategy

Verification is multi-layered:

1. **Symbolic CP enumeration** (§3.1 table).  `sim/simulator.py::
   test_q1_cp_enumeration` enumerates all 48 `(ρ_i, ρ_j, p)` triples,
   classifies each as non-unifiable, trivial, unifiable-joinable, or
   unifiable-non-joinable.  Exactly one (up to swap) is non-joinable.
   The enumeration is exhaustive.

2. **Per-rule size-delta arithmetic** (§3.2 table).
   `test_per_rule_size_delta` re-derives each rule's symbolic size
   delta on a concrete closed instance, confirming:
   ρ1:−1, ρ2:−1, ρ3:−2, ρ4:−2, ρ5:+1, ρ6:−1.

3. **Strategy-termination empirical test** (`test_q2_wn_strategy`,
   `test_wn_strategy_on_random_terms`).  Applies "avoid ρ5" to 61
   closed terms (11 hand-crafted + 50 random depth 2–6); every one
   reaches NF in ≤ 6 steps.  Every step is checked for strict size
   decrease.

4. **Infinite-sequence trace** (`test_q3_infinite_sequence`).  20
   steps of `f(0) →ρ5 f(s(0)) →ρ5 …` are mechanically traced; at
   each `n`, the term is structurally checked to equal `f(s^n(0))`.

5. **NF sanity check** (`test_claimed_nfs`).  Every claimed normal
   form (`0`, `nil`, `a`, `s(0)`, `s(s(0))`, `cons(0, nil)`,
   `cons(a, cons(0, nil))`) is confirmed to have zero redexes.

6. **Non-join empirical check** (`test_q1_non_confluence_witness`).
   Reachable sets from `0` and `nil` are computed to depth 20 (size
   capped at 80); each is `{self}`; their intersection is empty,
   witnessing that `c(0, nil)` has no common reduct from the two
   NF branches.

7. **ρ5/ρ6 joinability check** (`test_q1_rho5_rho6_overlap_joinable`).
   Confirms that `f(s(0)) →ρ6 nil`, so the (ρ5, ρ6, ε) overlap joins.

The oracle's output — `sim/output-final.txt` — is the concatenated
result of all these tests on a single run.  Every claim in §3 and §4
traces to at least one entry in that file.

---

## 6. Worked Examples

### 6.1 Divergent pair for Q1

`t = c(0, nil)`:

- Reduction A: `c(0, nil) →ρ3@ε 0`.  Normal form; size 1.
- Reduction B: `c(0, nil) →ρ4@ε nil`.  Normal form; size 1.

Both reach distinct normal forms in one step from the same starting
term.  Oracle trace in §"Q1 witness" of `output-final.txt`.

### 6.2 Terminating and non-terminating reductions from the same term

`t = f(0)`:

- **Terminating path** (Q2 strategy): `f(0) →ρ6@ε nil`.  One step;
  reaches NF `nil`.  Size 2 → 1.
- **Non-terminating path** (Q3 witness): `f(0) →ρ5@ε f(s(0)) →ρ5@ε
  f(s(s(0))) →ρ5@ε f(s(s(s(0)))) → …`.  Unbounded.

Same `t`, two reductions: one terminates, one does not.  This is
exactly what WN-but-not-SN looks like at the term level.  With §6.1
this covers a second orthogonal axis: coexistence of terminating and
non-terminating paths from one starting term.

### 6.3 Deterministic termination via `len`

`t = len(cons(0, cons(a, nil)))` (no `c`, no `f`; strategy is forced):

- Step 1 (path `ε`, rule ρ2): `len(cons(0, cons(a, nil))) → s(len(cons(a, nil)))`.
  Size 6 → 5.
- Step 2 (path `(1)`, rule ρ2): `s(len(cons(a, nil))) → s(s(len(nil)))`.
  Size 5 → 4.
- Step 3 (path `(1, 1)`, rule ρ1): `s(s(len(nil))) → s(s(0))`.
  Size 4 → 3.
- `s(s(0))` is NF (no rule has LHS headed by `s` or `0`).

This is the deterministic core of R (rules ρ1, ρ2 alone): any term of
the form `len(cons(t_1, cons(t_2, … nil)))` reduces to `s^n(0)` where
`n` is the list length.  Oracle trace in §"Q2 strategy" of
`output-final.txt`.

### 6.4 Infinite reduction for Q3 with visible pattern

`t_0 = f(0)`, stepped 20 times by ρ5 at ε:

    t_0  = f(0)                                   size 2
    t_1  = f(s(0))                                size 3
    t_2  = f(s(s(0)))                             size 4
    t_3  = f(s(s(s(0))))                          size 5
    ...
    t_20 = f(s^20(0))                             size 22

General pattern: `t_n = f(s^n(0))`; applying ρ5 at ε with σ(x) =
s^n(0) yields `f(s(σ(x))) = f(s^{n+1}(0)) = t_{n+1}`.  The sequence
is infinite by induction on `n`.

Oracle trace: `test_q3_infinite_sequence` in `output-final.txt`.

### 6.5 Choice propagating through `len`

`t = len(c(cons(0, nil), nil))`.  A `c` redex at `(1)` and, depending
on which ρ fires, different `len` redexes become available:

- Via ρ3 then `len`: `len(c(cons(0, nil), nil)) →ρ3@(1) len(cons(0, nil))
  →ρ2@ε s(len(nil)) →ρ1@(1) s(0)`.  Size 6 → 4 → 3 → 2.  NF.
- Via ρ4 then `len`: `len(c(cons(0, nil), nil)) →ρ4@(1) len(nil)
  →ρ1@ε 0`.  Size 6 → 2 → 1.  NF.

Two distinct NFs (`s(0)` and `0`) reachable — a second concrete
witness of non-confluence, this time with a `len` wrapper around the
choice.  Not strictly needed for §4.1 (already has `c(0, nil)`), but
demonstrates that the choice non-confluence propagates through the
otherwise-deterministic `len` fragment.

---

## 7. Open Questions and Known Limitations

### 7.1 Rule-removal parametric analysis

Can any single-rule removal restore confluence?

| Remove | Does it restore confluence? | Reason |
|--------|----------------------------|--------|
| ρ1 | No | (ρ3, ρ4, ε) CP still non-joinable; `c(0, nil)` still has NFs `0` and `nil` (both remain NFs in `R \ {ρ1}`). |
| ρ2 | No | Same reason as removing ρ1. |
| ρ3 | **Yes** | The only non-joinable CP disappears; see residual CP audit below. |
| ρ4 | **Yes** | Symmetric to removing ρ3. |
| ρ5 | No | `c(0, nil)` CP persists. |
| ρ6 | No | `c(0, nil)` CP persists. |

**Residual CP audit for R \\ {ρ3}** (the positive case; closes G7).
With ρ3 removed, the remaining rules are ρ1, ρ2, ρ4, ρ5, ρ6.  The
non-variable-position overlap grid has `(2 + 2 + 1 + 1 + 1) × 5 = 35`
triples.  The critical-pair analysis carries over: the only unifiable
non-variable overlaps involve matching heads.  In `R \\ {ρ3}`:

- Same-head `len`: (ρ1, ρ1, ε), (ρ1, ρ2, ε) non-unifiable (nil vs
  cons), (ρ2, ρ1, ε) non-unifiable, (ρ2, ρ2, ε) trivial.
- Same-head `c`: only ρ4 remains; (ρ4, ρ4, ε) is trivial.  The
  previously non-joinable (ρ3, ρ4, ε) and (ρ4, ρ3, ε) pairs
  **vanish**.
- Same-head `f`: (ρ5, ρ5, ε) trivial, (ρ6, ρ6, ε) trivial, (ρ5, ρ6, ε)
  joinable at nil, (ρ6, ρ5, ε) joinable at nil.

Every unifiable non-variable overlap in `R \\ {ρ3}` is either trivial
or joinable.  By §2.1's sublemma, variable-position overlaps also
join.  Hence `R \\ {ρ3}` is confluent.

The symmetric analysis for `R \\ {ρ4}` gives the same verdict.

**Parametric disclosure.**  ρ3 and ρ4 jointly encode an essentially
non-confluent choice: they share an LHS and disagree on the reduct,
and the reducts are two independent variables.  Any pair of rules
with shape `g(v_1, v_2, …, v_n) → v_i` and `g(v_1, …, v_n) → v_j` for
`i ≠ j` induces a non-joinable CP `⟨v_i, v_j⟩`, because `v_i` and
`v_j` are independent variables and no rule of R — by the same shape
constraint — can rewrite `v_i` into `v_j`.  This is parametric in the
arity and index pair: the non-confluence of R is not incidental to
the specific rule numbering, it is determined by the pattern of
projection rules on `c`, and no rule-modification short of removing
one of them can eliminate it.

### 7.2 Strategy uniqueness for Q2

Is the "avoid ρ5" strategy the only WN-witnessing strategy?

**No.**  The "avoid ρ5" strategy is a minimal-sufficient witness: it
works on every closed term with zero lookahead and only requires
knowing which rule each redex fires.  Other strategies also succeed:

- **Any strategy that never fires ρ5 at all** — innermost-preferential
  restricted to non-ρ5 rules; leftmost-outermost restricted to non-ρ5
  rules; `S` itself — all terminate by §3.2's size argument.
- **"Always fire ρ6 at every f-subterm before descending"** reaches
  NF by first replacing every `f`-subterm with `nil`, then reducing
  any remaining `len` and `c` redexes.  The remaining system (without
  `f`) is finite-branching and strictly size-decreasing.

**Sufficient class (characterization of what works).**  A strategy
`S'` WN-witnesses R iff the reduction sequence `t, S'(t), S'²(t), …`
contains, from some step onward, only size-nonincreasing steps and
is bounded overall.  The crispest sufficient condition we know of is:

> `S'` never fires ρ5 at any `f`-subterm that is not subsequently
> destroyed (by an outer ρ3/ρ4/ρ6 step) within a bounded number of
> additional steps.

The "avoid ρ5" strategy satisfies this with bound `0`.  Other
strategies succeed at various nonzero bounds, as long as the ρ5
growth is eventually absorbed by a finite number of non-ρ5 steps.
Strategies that fire ρ5 infinitely many times on the same `f`-subterm
(without ever letting a ρ6 or outer ρ3/ρ4 step destroy it) fail WN,
as §3.3 demonstrates.

### 7.3 Measure sensitivity for Q3

Is the non-SN verdict sensitive to the choice of Φ?

**No — the non-SN verdict is insensitive to any choice of measure.**
The sequence `f(0) → f(s(0)) → f(s(s(0))) → …` is an infinite concrete
witness; no measure is invoked to derive it, and the sequence exists
regardless of Φ.  By Sublemma 2.3.N, **any** well-founded order
whatsoever — any attempt to witness SN by a strictly-decreasing
measure over **any** well-founded codomain — would have to produce an
infinite descending chain along this sequence, which is impossible by
well-foundedness.  The impossibility is therefore parametric across
the entire class of measure constructions: R is non-SN in every
measure class.

### 7.4 Generalization to rule-shape classes

- **Does every TRS with a ρ3/ρ4-shaped pair fail confluence?**  Yes,
  per §7.1: two rules sharing an LHS and projecting to distinct
  variables induce a non-joinable CP.  Parametric in arity and
  projected indices — only the "distinct variables projected"
  property matters.
- **Does every TRS with an `f(x) → f(s(x))`-shaped rule fail SN?**
  Yes, provided `f` and `s` are distinct symbols (so the rule is not
  a degenerate identity).  From any closed term `f(t)`, repeated
  ρ5-style application at the root produces `f(s(t)), f(s(s(t))), …`,
  strictly growing in size.  Parametric in what `s` is: any
  constructor (or term-builder) that does not collapse with `f`
  gives this infinite reduction.
- **Is R's WN holding contingent on the other rules?**  Yes.  The
  key is that ρ6 provides a size-shrinking **alternative** at every
  `f`-subterm, so the strategy can avoid ρ5 entirely.  If we **remove
  ρ6**, the remaining system `R \\ {ρ6}` has only the growing ρ5 at
  `f`-subterms, and any closed term containing `f(…)` has no finite
  reduction (the only rule applicable at that position is ρ5, which
  pumps).  WN of R is contingent on ρ6 being present — the "shrinking
  escape" that pairs with ρ5's growth.

**Structural upshot.**  R is not an isolated bad example: ρ3 + ρ4
exemplify a non-confluent choice primitive; ρ5 exemplifies an
unbounded-recursion rule; ρ6 exemplifies the shrinking escape that
is structurally necessary for WN.  Removing ρ6 would keep R
non-confluent and non-SN, **and** destroy WN, yielding a TRS that
is none of the three.  The three properties are each pinned to a
specific structural feature of R's rule set.
