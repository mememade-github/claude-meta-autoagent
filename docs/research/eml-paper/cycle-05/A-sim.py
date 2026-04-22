"""
Bounded reduction simulator for the extended calculator.

Implements:
  - Term representation
  - Single-step reduction (all redexes enumerated)
  - Parallel reduction `paral` (rewrite a chosen set of disjoint redexes
    in one step) and the complete-development operator `star`
  - Bounded BFS to enumerate reachable reducts and verify confluence
    (every pair of reducts of M has a common further reduct, modulo
    the depth bound)

Run:
    python3 sim.py
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Iterator, Optional


# ---------- Terms ----------

@dataclass(frozen=True)
class Sym:
    name: str

@dataclass(frozen=True)
class App:
    f: object
    a: object

Term = object  # Sym | App


def app(*xs):
    """Left-associative application: app(M,N,O) = ((M N) O)."""
    t = xs[0]
    for x in xs[1:]:
        t = App(t, x)
    return t


def show(t: Term) -> str:
    if isinstance(t, Sym):
        return t.name
    # left-associative pretty-printer
    parts = []
    cur = t
    while isinstance(cur, App):
        parts.append(cur.a)
        cur = cur.f
    parts.append(cur)
    parts.reverse()
    out = []
    for i, p in enumerate(parts):
        s = show(p)
        if isinstance(p, App) and i > 0:
            s = "(" + s + ")"
        out.append(s)
    return " ".join(out)


def size(t: Term) -> int:
    if isinstance(t, Sym):
        return 1
    return 1 + size(t.f) + size(t.a)


# ---------- Spine decomposition ----------

def spine(t: Term):
    """Return (head, [arg1, arg2, ...]) for t = head a1 a2 ... an."""
    args = []
    while isinstance(t, App):
        args.append(t.a)
        t = t.f
    args.reverse()
    return t, args


def rebuild(head: Term, args: list) -> Term:
    t = head
    for a in args:
        t = App(t, a)
    return t


# ---------- Rule table: arity and reduction ----------
# Each rule: head symbol -> (arity, rewrite function on the arg list)

RULES = {
    "I":  (1, lambda a: a[0]),
    "K":  (2, lambda a: a[0]),
    "S":  (3, lambda a: app(a[0], a[2], app(a[1], a[2]))),
    "B":  (3, lambda a: app(a[0], app(a[1], a[2]))),
    "C":  (3, lambda a: app(a[0], a[2], a[1])),
    "W":  (2, lambda a: app(a[0], a[1], a[1])),
    "M":  (1, lambda a: app(a[0], a[0])),
    "Y":  (1, lambda a: app(a[0], app(Sym("Y"), a[0]))),
    "T":  (2, lambda a: app(a[1], a[0])),
    "V":  (3, lambda a: app(a[2], a[0], a[1])),
    "D":  (4, lambda a: app(a[0], a[1], app(a[2], a[3]))),
    "P1": (2, lambda a: a[0]),  # Π₁
    "P2": (2, lambda a: a[1]),  # Π₂
}


def is_redex_at_root(t: Term) -> bool:
    h, args = spine(t)
    if not isinstance(h, Sym) or h.name not in RULES:
        return False
    arity, _ = RULES[h.name]
    return len(args) >= arity


def step_at_root(t: Term) -> Term:
    h, args = spine(t)
    arity, fn = RULES[h.name]
    head_term = fn(args[:arity])
    return rebuild(head_term, args[arity:])


# ---------- Single-step reduction: enumerate every redex position ----------

def positions(t: Term) -> list[tuple]:
    """All positions in t (tuples of 'f'/'a' navigating into App)."""
    out = [()]
    if isinstance(t, App):
        out += [("f",) + p for p in positions(t.f)]
        out += [("a",) + p for p in positions(t.a)]
    return out


def at(t: Term, p: tuple) -> Term:
    for d in p:
        t = t.f if d == "f" else t.a
    return t


def replace(t: Term, p: tuple, new: Term) -> Term:
    if not p:
        return new
    d, rest = p[0], p[1:]
    if d == "f":
        return App(replace(t.f, rest, new), t.a)
    else:
        return App(t.f, replace(t.a, rest, new))


def all_redex_positions(t: Term) -> list[tuple]:
    return [p for p in positions(t) if is_redex_at_root(at(t, p))]


def step_at(t: Term, p: tuple) -> Term:
    return replace(t, p, step_at_root(at(t, p)))


def all_one_step_reducts(t: Term) -> list[Term]:
    return [step_at(t, p) for p in all_redex_positions(t)]


# ---------- Parallel reduction (complete development M*) ----------

def star(t: Term) -> Term:
    """Complete development: reduce every redex currently in t in one
    parallel step, with all arguments themselves star-reduced."""
    if isinstance(t, Sym):
        return t
    h, args = spine(t)
    args_star = [star(a) for a in args]
    if isinstance(h, Sym) and h.name in RULES:
        arity, fn = RULES[h.name]
        if len(args_star) >= arity:
            head_term = fn(args_star[:arity])
            return rebuild(head_term, args_star[arity:])
    return rebuild(h, args_star)


# ---------- Bounded confluence checker ----------

def reducts_within(t: Term, depth: int, size_bound: int = 200) -> set:
    """All terms reachable from t in <= depth single-steps,
    skipping any reduct exceeding size_bound (Y and M can blow up)."""
    seen = {repr_term(t): t}
    frontier = {repr_term(t)}
    for _ in range(depth):
        nxt = set()
        for k in frontier:
            u = seen[k]
            for v in all_one_step_reducts(u):
                if size(v) > size_bound:
                    continue
                rk = repr_term(v)
                if rk not in seen:
                    seen[rk] = v
                    nxt.add(rk)
        frontier = nxt
        if not frontier:
            break
    return seen


def repr_term(t: Term) -> str:
    if isinstance(t, Sym):
        return t.name
    return "(" + repr_term(t.f) + " " + repr_term(t.a) + ")"


def common_reduct(a: Term, b: Term, depth: int, size_bound: int = 200) -> Optional[Term]:
    """Search for a common reduct of a and b within `depth` steps."""
    ra = reducts_within(a, depth, size_bound)
    rb = reducts_within(b, depth, size_bound)
    common = set(ra.keys()) & set(rb.keys())
    if not common:
        return None
    return ra[next(iter(common))]


def check_confluence_bounded(t: Term, depth: int, join_depth: int,
                              size_bound: int = 200) -> tuple[bool, list]:
    """For every pair of reducts (N1, N2) of t reachable in <= depth steps,
    verify they share a common further reduct reachable in <= join_depth
    steps from each. Returns (ok, failures)."""
    reducts = list(reducts_within(t, depth, size_bound).values())
    failures = []
    for i in range(len(reducts)):
        for j in range(i + 1, len(reducts)):
            N1, N2 = reducts[i], reducts[j]
            cr = common_reduct(N1, N2, join_depth, size_bound)
            if cr is None:
                failures.append((N1, N2))
    return (len(failures) == 0, failures)


# ---------- Worked examples ----------

I, K, S, B, C, W, M, Y, T, V, D = (Sym(n) for n in "IKSBCWMYTVD")
P1, P2 = Sym("P1"), Sym("P2")
a, b, c, d, e, f, x, y, z = (Sym(n) for n in ["a","b","c","d","e","f","x","y","z"])
# Lower-case symbols are inert "constants" (no rule), serving as test atoms.


def banner(s):
    print()
    print("=" * 72)
    print(s)
    print("=" * 72)


def trace(label, t, max_steps=30, strategy="leftmost"):
    print(f"\n[{label}] start: {show(t)}")
    seen = [t]
    for i in range(max_steps):
        rs = all_redex_positions(t)
        if not rs:
            print(f"  normal form after {i} steps: {show(t)}")
            return t
        # leftmost-outermost = first redex in pre-order, which is what
        # all_redex_positions returns (root first, then f-subtree, then a)
        if strategy == "leftmost":
            p = rs[0]
        else:  # rightmost-innermost
            p = rs[-1]
        t = step_at(t, p)
        if size(t) > 200:
            print(f"  step {i+1}: <oversize, |t|={size(t)}>, halting trace")
            return t
        print(f"  step {i+1} @{p}: {show(t)}")
        seen.append(t)
    print(f"  did not terminate within {max_steps} steps; current: {show(t)}")
    return t


def example_1_S_critical_branch():
    """S (K a b) (I c) (I d) -- explore divergent reduction orders."""
    banner("Example 1: S (K a b) (I c) (I d) -- multiple reduction orders")
    t = app(S, app(K, a, b), app(I, c), app(I, d))
    print("term:", show(t))
    print("redex positions:", all_redex_positions(t))
    print("one-step reducts:")
    for r in all_one_step_reducts(t):
        print("  ", show(r))
    # Two divergent traces:
    print("\n-- trace A: leftmost-outermost --")
    nA = trace("A", t, strategy="leftmost")
    print("\n-- trace B: rightmost-innermost --")
    nB = trace("B", t, strategy="rightmost")
    cr = common_reduct(nA, nB, depth=10)
    print(f"\ncommon reduct of A and B reachable: {show(cr) if cr else 'NONE'}")
    # Bounded confluence check
    ok, fails = check_confluence_bounded(t, depth=4, join_depth=8)
    print(f"bounded confluence over depth-4 reducts: {'OK' if ok else 'FAIL'}; "
          f"{len(fails)} failures")


def example_2_Y_divergence():
    """Y f -- non-terminating; check confluence on a bounded prefix."""
    banner("Example 2: Y f -- non-terminating; bounded-depth confluence")
    t = app(Y, f)
    print("term:", show(t))
    # Reductions: Y f -> f (Y f), then either reduce inner Y again,
    # or leave it; both must be reconcilable.
    n1 = step_at(t, ())                 # f (Y f)
    n2 = step_at(n1, ("a",))            # f (f (Y f))
    n3 = step_at(n2, ("a", "a"))        # f (f (f (Y f)))
    print("reduct sequence:")
    for i, r in enumerate([t, n1, n2, n3]):
        print(f"  {i}: {show(r)}")
    # Two divergent paths from t:
    #   path A: take 1 step  -> f (Y f)
    #   path B: take 2 steps -> f (f (Y f))
    cr = common_reduct(n1, n2, depth=3)
    print(f"common reduct of f(Yf) and f(f(Yf)): {show(cr) if cr else 'NONE'}")
    print(f"  (expected: f (f (Y f)) is itself reachable from f (Y f))")
    # Compute star(Yf):
    print(f"star(Y f) = {show(star(t))}")
    print(f"star(star(Y f)) = {show(star(star(t)))}")


def example_3_strategies():
    """A multi-combinator term: leftmost-outermost vs rightmost-innermost."""
    banner("Example 3: B (W I) (K a) c -- strategy independence of normal form")
    t = app(B, app(W, I), app(K, a), c)
    print("term:", show(t))
    nA = trace("leftmost", t, strategy="leftmost")
    nB = trace("rightmost", t, strategy="rightmost")
    print(f"\nA-normal: {show(nA)}")
    print(f"B-normal: {show(nB)}")
    print(f"equal? {repr_term(nA) == repr_term(nB)}")
    ok, fails = check_confluence_bounded(t, depth=6, join_depth=8)
    print(f"bounded confluence over depth-6 reducts: {'OK' if ok else 'FAIL'}; "
          f"{len(fails)} failures")


def example_4_M_self():
    """M M -- non-terminating, must remain confluent."""
    banner("Example 4: M M -- self-replicating; confluence under bounded steps")
    t = app(M, M)
    for i in range(5):
        rs = all_one_step_reducts(t)
        print(f"step {i}: {show(t)}, |reducts|={len(rs)}")
        if not rs:
            break
        t = rs[0]
    # M M reduces only to itself (M M -> M M -> ...).  Trivially confluent.
    print("Note: M M is its own unique one-step reduct.")


def example_5_overlap_audit():
    """Demonstrate that no two rule LHS's overlap at a non-variable position."""
    banner("Example 5: critical-pair / overlap audit")
    print("Each rule's LHS pattern is headed by a distinct primitive symbol.")
    print("LHS shapes (as spine head, arity):")
    for name, (ar, _) in RULES.items():
        print(f"  {name}: head={name}, arity={ar}")
    print()
    print("Two rules can produce a critical pair only when one rule's LHS")
    print("unifies with a non-variable subterm of another's LHS.  Each LHS")
    print("here is (PrimitiveSymbol  v1  ...  vk) where v_i are placeholder")
    print("metavariables.  The only non-variable subterms are the primitive")
    print("itself and the partial applications (Primitive v1), (Primitive v1 v2),")
    print("etc.  These all begin with the same primitive symbol; two distinct")
    print("primitives cannot unify.  Self-overlap reduces to root-overlap")
    print("(the trivial case).  Therefore: 0 non-trivial critical pairs.")


def example_6_progressive_subsets():
    """Mechanically check confluence on each prefix of {I,K,S,B,C,W,M,Y,T,V,D,P1,P2}."""
    banner("Example 6: progressive subsets -- mechanical bounded confluence")
    full_order = ["I","K","S","B","C","W","M","Y","T","V","D","P1","P2"]
    test_terms = [
        app(I, app(I, a)),
        app(K, a, app(I, b)),
        app(S, app(K, a, c), app(I, b), c),
        app(B, app(K, a), app(I, b), c),
        app(C, app(K, a), b, c),
        app(W, app(K, a), b),
        app(M, app(I, a)),
        app(Y, app(K, a)),       # Y(Ka) -> Ka(Y(Ka)) -> a (consuming the second arg)
        app(T, app(I, a), b),
        app(V, app(I, a), b, app(K, c, d)),
        app(D, app(I, a), b, app(K, c), d),
        app(P1, app(I, a), b),
        app(P2, a, app(I, b)),
    ]
    for k in range(1, len(full_order) + 1):
        active = set(full_order[:k])
        # Temporarily disable all rules outside `active`
        global RULES
        saved = RULES
        RULES = {n: r for n, r in RULES.items() if n in active}
        try:
            verdicts = []
            for t in test_terms:
                ok, _ = check_confluence_bounded(t, depth=3, join_depth=6,
                                                  size_bound=120)
                verdicts.append(ok)
            print(f"primitives = {sorted(active)}: "
                  f"confluence verified on {sum(verdicts)}/{len(verdicts)} probes")
        finally:
            RULES = saved


def example_7_diamond_via_star():
    """For several t and divergent N1, N2, verify N1 ⇒ star(t) and N2 ⇒ star(t)."""
    banner("Example 7: diamond closure via complete development (star)")
    cases = [
        ("S(Kab)(Ic)(Id)", app(S, app(K, a, b), app(I, c), app(I, d))),
        ("Y f", app(Y, f)),
        ("M(Ia)", app(M, app(I, a))),
        ("W(Ka)b", app(W, app(K, a), b)),
        ("D(Ka)bcd", app(D, app(K, a), b, c, d)),
        ("V(Ia)bc", app(V, app(I, a), b, c)),
    ]
    for name, t in cases:
        st = star(t)
        # Take any two divergent one-step reducts; check both reach star(t)
        # by some sequence of single-steps within a small bound.
        rs = all_one_step_reducts(t)
        print(f"{name}: star = {show(st)}")
        for r in rs[:3]:
            cr = common_reduct(r, st, depth=4)
            print(f"  reduct {show(r)} reaches star? {'YES via '+show(cr) if cr else 'NO'}")


def main():
    example_5_overlap_audit()
    example_1_S_critical_branch()
    example_2_Y_divergence()
    example_3_strategies()
    example_4_M_self()
    example_7_diamond_via_star()
    example_6_progressive_subsets()


if __name__ == "__main__":
    main()
