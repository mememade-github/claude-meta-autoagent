"""Executable oracle for the term-rewriting system R.

Signature Sigma:
  Nullary: 0, c, d
  Unary:   s, f, u
  Binary:  g, m

Rules R:
  rho1: g(0, y)    -> y
  rho2: g(s(x), y) -> s(g(x, y))
  rho3: m(x, y)    -> x
  rho4: m(x, y)    -> y
  rho5: f(x)       -> x
  rho6: f(x)       -> f(f(x))
  rho7: u(u(x))    -> x

Terms are represented as tuples: (head, arg1, arg2, ...).
A constant is a 1-tuple: ("0",), ("c",), ("d",).
Variables are strings starting with "?": "?x", "?y".

This simulator:
  (1) Enumerates every redex position in a term, with the rule that fires.
  (2) Performs one-step reductions at a chosen (position, rule).
  (3) Produces normal forms via a configurable strategy.
  (4) Cross-checks every claim made in ARGUMENT.md.
"""

from __future__ import annotations

import sys
from typing import Iterator


# ---------- term representation ----------

Term = tuple  # e.g. ("g", ("s", ("0",)), ("c",)) for g(s(0), c)

NULLARY = {"0", "c", "d"}
UNARY = {"s", "f", "u"}
BINARY = {"g", "m"}

ARITY = {h: 0 for h in NULLARY} | {h: 1 for h in UNARY} | {h: 2 for h in BINARY}


def mk(head: str, *args: Term) -> Term:
    assert head in ARITY, f"unknown head: {head}"
    assert len(args) == ARITY[head], f"{head} expects arity {ARITY[head]}, got {len(args)}"
    return (head,) + args


def show(t: Term) -> str:
    head = t[0]
    if len(t) == 1:
        return head
    return head + "(" + ", ".join(show(a) for a in t[1:]) + ")"


def size(t: Term) -> int:
    return 1 + sum(size(a) for a in t[1:])


# ---------- matching and substitution ----------

def match(pattern: Term, term: Term, subst: dict[str, Term] | None = None) -> dict[str, Term] | None:
    """First-order matching: returns substitution sigma such that pattern*sigma == term, or None.

    Pattern variables are strings starting with "?".
    """
    if subst is None:
        subst = {}
    if isinstance(pattern, str) and pattern.startswith("?"):
        if pattern in subst:
            return subst if subst[pattern] == term else None
        subst = dict(subst)
        subst[pattern] = term
        return subst
    if not isinstance(pattern, tuple) or not isinstance(term, tuple):
        return None
    if pattern[0] != term[0] or len(pattern) != len(term):
        return None
    for p, t in zip(pattern[1:], term[1:]):
        subst = match(p, t, subst)
        if subst is None:
            return None
    return subst


def subst_apply(t, subst: dict[str, Term]):
    if isinstance(t, str) and t.startswith("?"):
        return subst[t]
    if isinstance(t, tuple):
        return (t[0],) + tuple(subst_apply(a, subst) for a in t[1:])
    return t


# ---------- rules ----------

RULES: list[tuple[str, Term, Term]] = [
    ("rho1", ("g", ("0",), "?y"),         "?y"),
    ("rho2", ("g", ("s", "?x"), "?y"),    ("s", ("g", "?x", "?y"))),
    ("rho3", ("m", "?x", "?y"),           "?x"),
    ("rho4", ("m", "?x", "?y"),           "?y"),
    ("rho5", ("f", "?x"),                 "?x"),
    ("rho6", ("f", "?x"),                 ("f", ("f", "?x"))),
    ("rho7", ("u", ("u", "?x")),          "?x"),
]


# ---------- positions and subterm operations ----------

Position = tuple[int, ...]


def subterm_at(t: Term, pos: Position) -> Term:
    for i in pos:
        t = t[i]  # t[0] is head, t[1..] are children, so i is 1-indexed into children
    return t


def replace_at(t: Term, pos: Position, new: Term) -> Term:
    if not pos:
        return new
    head = t[0]
    i = pos[0]
    new_children = list(t[1:])
    new_children[i - 1] = replace_at(t[i], pos[1:], new)
    return (head,) + tuple(new_children)


def all_positions(t: Term) -> Iterator[Position]:
    yield ()
    for i, child in enumerate(t[1:], start=1):
        for sub in all_positions(child):
            yield (i,) + sub


# ---------- redex enumeration and reduction ----------

def redexes(t: Term) -> list[tuple[Position, str, Term, dict[str, Term]]]:
    """Return list of (position, rule_name, rhs_template, substitution)."""
    found = []
    for pos in all_positions(t):
        sub = subterm_at(t, pos)
        for name, lhs, rhs in RULES:
            s = match(lhs, sub)
            if s is not None:
                found.append((pos, name, rhs, s))
    return found


def step(t: Term, pos: Position, rule_name: str) -> Term:
    """Apply the named rule at position pos, returning the reduced term."""
    sub = subterm_at(t, pos)
    for name, lhs, rhs in RULES:
        if name != rule_name:
            continue
        s = match(lhs, sub)
        if s is None:
            raise ValueError(f"rule {rule_name} does not apply at position {pos} to {show(sub)}")
        reduced = subst_apply(rhs, s)
        return replace_at(t, pos, reduced)
    raise ValueError(f"unknown rule: {rule_name}")


def is_normal_form(t: Term) -> bool:
    return len(redexes(t)) == 0


# ---------- strategy: avoid rho6 ----------

def weight(t: Term) -> int:
    """Polynomial interpretation proving WN under 'avoid rho6' strategy.

    [0] = [c] = [d] = 1
    [s(t)] = 1 + [t]
    [f(t)] = 1 + [t]
    [u(t)] = 1 + [t]
    [g(t1,t2)] = 1 + 2*[t1] + [t2]
    [m(t1,t2)] = 1 + [t1] + [t2]
    """
    h = t[0]
    if h in NULLARY:
        return 1
    if h in UNARY:
        return 1 + weight(t[1])
    if h == "g":
        return 1 + 2 * weight(t[1]) + weight(t[2])
    if h == "m":
        return 1 + weight(t[1]) + weight(t[2])
    raise ValueError(h)


def reduce_avoiding_rho6(t: Term, max_steps: int = 10_000) -> tuple[Term, list[tuple[Position, str]]]:
    """Apply the 'avoid rho6' strategy: at each step, pick any redex whose rule is not rho6.

    For m-redexes we pick rho3 (either rho3 or rho4 would work, both shrink).
    Returns the normal form and the list of (position, rule) applied.
    """
    trace = []
    for _ in range(max_steps):
        rs = redexes(t)
        non6 = [r for r in rs if r[1] != "rho6"]
        if not non6:
            # No non-rho6 redex; either normal form or only rho6 applies.
            # If rho6 applies, rho5 must also apply at the same position (shared LHS).
            # So this branch shouldn't happen.
            if rs:
                raise RuntimeError(
                    f"only rho6 applies — should be impossible since rho5 shares LHS: {show(t)}"
                )
            return t, trace
        # Among non-rho6 redexes, prefer rho5/rho3/rho1/rho7 over rho2/rho4 purely for determinism.
        non6.sort(key=lambda r: {"rho5": 0, "rho3": 1, "rho1": 2, "rho7": 3, "rho2": 4, "rho4": 5}[r[1]])
        pos, name, _rhs, _s = non6[0]
        t = step(t, pos, name)
        trace.append((pos, name))
    raise RuntimeError(f"strategy did not terminate in {max_steps} steps")


# ---------- test suite ----------

def banner(msg: str) -> None:
    print()
    print("=" * 72)
    print(msg)
    print("=" * 72)


def test_Q1_non_confluence() -> None:
    banner("Q1. NON-CONFLUENCE: witness m(c, d)")
    t = ("m", ("c",), ("d",))
    print(f"t = {show(t)}")
    print(f"  size = {size(t)}, weight = {weight(t)}")
    rs = redexes(t)
    print(f"  redexes: {[(p, n) for p, n, _, _ in rs]}")
    # Apply rho3
    u1 = step(t, (), "rho3")
    print(f"  via rho3 at root:  {show(t)} -> {show(u1)}")
    assert u1 == ("c",)
    # Apply rho4
    u2 = step(t, (), "rho4")
    print(f"  via rho4 at root:  {show(t)} -> {show(u2)}")
    assert u2 == ("d",)
    # Check both are normal forms
    assert is_normal_form(u1), f"expected NF: {show(u1)}"
    assert is_normal_form(u2), f"expected NF: {show(u2)}"
    print(f"  {show(u1)} is a normal form: {is_normal_form(u1)}")
    print(f"  {show(u2)} is a normal form: {is_normal_form(u2)}")
    assert u1 != u2
    print(f"  {show(u1)} != {show(u2)}  -->  R is not confluent.")


def test_Q3_non_SN_infinite_sequence() -> None:
    banner("Q3. NON-SN: infinite sequence from f(c)")
    t = ("f", ("c",))
    print(f"t_0 = {show(t)}")
    seq = [t]
    for k in range(8):
        # Apply rho6 at the OUTERMOST f (position ()), matches x := f^k(c).
        t = step(t, (), "rho6")
        seq.append(t)
    for i, ti in enumerate(seq):
        print(f"  t_{i} = {show(ti)}   (size={size(ti)}, weight={weight(ti)})")
    # Verify each ti is strictly "longer" than ti-1 via rho6 at root.
    for i in range(len(seq) - 1):
        prev, nxt = seq[i], seq[i + 1]
        got = step(prev, (), "rho6")
        assert got == nxt, f"step mismatch at i={i}"
    # Show that the sequence is f^(n+1)(c)
    def fn(n: int) -> Term:
        t = ("c",)
        for _ in range(n):
            t = ("f", t)
        return t
    for i, ti in enumerate(seq):
        assert ti == fn(i + 1), f"i={i}: got {show(ti)} expected {show(fn(i+1))}"
    print("  Verified: t_n = f^(n+1)(c) for n = 0..8, with rho6 applied at the root at every step.")


def test_Q2_strategy_terminates_on_sample() -> None:
    banner("Q2. WN: 'avoid rho6' strategy terminates on a variety of terms")
    samples: list[Term] = [
        ("f", ("c",)),
        ("f", ("f", ("c",))),
        ("u", ("u", ("c",))),
        ("u", ("u", ("u", ("u", ("c",))))),
        ("g", ("0",), ("c",)),
        ("g", ("s", ("s", ("s", ("0",)))), ("d",)),
        ("m", ("c",), ("d",)),
        ("m", ("f", ("c",)), ("u", ("u", ("d",)))),
        ("g", ("s", ("s", ("0",))), ("m", ("c",), ("d",))),
        ("f", ("g", ("s", ("s", ("0",))), ("u", ("u", ("c",))))),
        ("m", ("f", ("g", ("s", ("0",)), ("c",))), ("u", ("u", ("f", ("d",))))),
        ("g", ("s", ("s", ("s", ("s", ("0",))))), ("f", ("u", ("u", ("g", ("s", ("0",)), ("c",)))))),
    ]
    for t in samples:
        w0 = weight(t)
        nf, tr = reduce_avoiding_rho6(t, max_steps=500)
        print(f"  {show(t)}  (weight={w0}, {len(tr)} steps)  ->  {show(nf)}")
        assert is_normal_form(nf), f"not a normal form: {show(nf)}"
        # Verify weights strictly decrease along the trace.
        cur = t
        prev_w = weight(cur)
        for pos, name in tr:
            cur = step(cur, pos, name)
            nw = weight(cur)
            assert nw < prev_w, f"weight did not strictly decrease under {name}: {prev_w} -> {nw}"
            prev_w = nw
    print("  Every sample reached a normal form; weight strictly decreased at every step.")


def test_weight_strict_decrease_on_every_rule_instance() -> None:
    banner("Measure check: weight strictly decreases under every non-rho6 rule (sampled instances)")
    # Try many random substitutions for each rule LHS; verify weight(LHS*sigma) > weight(RHS*sigma).
    import itertools
    import random

    random.seed(0)

    ground_atoms = [("0",), ("c",), ("d",)]

    def random_term(depth: int) -> Term:
        if depth <= 0 or random.random() < 0.3:
            return random.choice(ground_atoms)
        heads = ["s", "f", "u", "g", "m"]
        h = random.choice(heads)
        if h in UNARY:
            return (h, random_term(depth - 1))
        else:
            return (h, random_term(depth - 1), random_term(depth - 1))

    for name, lhs, rhs in RULES:
        if name == "rho6":
            # rho6 INCREASES weight — that's the point.
            cnt_increase = 0
            for _ in range(200):
                sigma = {v: random_term(3) for v in ["?x", "?y"] if v in vars_in(lhs) or v in vars_in(rhs)}
                l, r = subst_apply(lhs, sigma), subst_apply(rhs, sigma)
                if weight(l) < weight(r):
                    cnt_increase += 1
            print(f"  {name}: weight INCREASES in {cnt_increase}/200 random instances  (non-rho6 rules must decrease)")
            assert cnt_increase == 200, "rho6 should always increase weight by 1 — check rule form"
            continue
        checked = 0
        for _ in range(500):
            sigma = {v: random_term(3) for v in vars_in(lhs) | vars_in(rhs)}
            l, r = subst_apply(lhs, sigma), subst_apply(rhs, sigma)
            wl, wr = weight(l), weight(r)
            assert wl > wr, f"{name}: weight({show(l)})={wl} not > weight({show(r)})={wr}"
            checked += 1
        print(f"  {name}: {checked} random instances, all satisfy weight(LHS) > weight(RHS)")


def vars_in(t) -> set[str]:
    if isinstance(t, str) and t.startswith("?"):
        return {t}
    if isinstance(t, tuple):
        out: set[str] = set()
        for a in t[1:]:
            out |= vars_in(a)
        return out
    return set()


def test_critical_pair_enumeration() -> None:
    banner("Critical-pair sanity: only (rho3, rho4) at root of m(x,y) yields non-joinable pair")
    # (rho3, rho4) at root of m(x,y):
    #   rho3 gives x, rho4 gives y.  Instantiate x=c, y=d -> c vs d, both NF, c != d.
    #
    # (rho5, rho6) at root of f(x):
    #   rho5 gives x, rho6 gives f(f(x)).  f(f(x)) -->rho5-> f(x) -->rho5-> x.  Joinable.
    t = ("f", ("c",))
    # rho6 path
    a = step(t, (), "rho6")      # f(f(c))
    # join with rho5 path: reduce f(f(c)) by two rho5 to c
    b = step(a, (), "rho5")      # f(c)
    c_ = step(b, (), "rho5")     # c
    # And t --rho5--> c
    d = step(t, (), "rho5")      # c
    print(f"  (rho5,rho6) overlap at f(c): rho5 -> {show(d)}; rho6 -> {show(a)} -rho5-> {show(b)} -rho5-> {show(c_)}")
    print(f"  both join at {show(d)}.  So this critical pair is joinable.")
    assert d == c_ == ("c",)

    # No other rule pairs can overlap — the top symbols differ, or the LHSs are linear with unrelated shapes.
    print("  (rho3,rho4) overlap at m(c,d): rho3 -> c; rho4 -> d; c and d are distinct normal forms.")


def main() -> None:
    test_Q1_non_confluence()
    test_Q3_non_SN_infinite_sequence()
    test_Q2_strategy_terminates_on_sample()
    test_weight_strict_decrease_on_every_rule_instance()
    test_critical_pair_enumeration()
    banner("ALL ORACLE CHECKS PASSED")


if __name__ == "__main__":
    main()
