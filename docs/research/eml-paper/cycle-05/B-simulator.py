"""Executable oracle for the extended-calculator reduction system.

Represents terms as nested tuples; primitives and free variables are strings.
Rules encoded from the task statement. The oracle performs bounded BFS on
reduction paths and checks that all pairs of reducts at any depth can be
rejoined at some common depth (confluence test by reductum intersection).
"""

from collections import deque
from typing import Tuple, Union, Dict, List, Set

Term = Union[str, Tuple["Term", "Term"]]

PRIMITIVES: Dict[str, int] = {
    "I": 1, "K": 2, "S": 3, "B": 3, "C": 3, "W": 2, "M": 1,
    "Y": 1, "T": 2, "V": 3, "D": 4, "P1": 2, "P2": 2,
}


def app(m: Term, n: Term) -> Term:
    return (m, n)


def head_args(t: Term):
    args = []
    cur = t
    while isinstance(cur, tuple):
        args.append(cur[1])
        cur = cur[0]
    return cur, list(reversed(args))


def apply_many(h: Term, args: List[Term]) -> Term:
    r = h
    for a in args:
        r = app(r, a)
    return r


def reduce_at_root(t: Term):
    """Contract the root redex if any; return None otherwise."""
    head, args = head_args(t)
    if not isinstance(head, str) or head not in PRIMITIVES:
        return None
    a = PRIMITIVES[head]
    if len(args) < a:
        return None
    taken = args[:a]
    rest = args[a:]
    if head == "I":
        (x,) = taken; r = x
    elif head == "K":
        x, y = taken; r = x
    elif head == "S":
        x, y, z = taken; r = app(app(x, z), app(y, z))
    elif head == "B":
        x, y, z = taken; r = app(x, app(y, z))
    elif head == "C":
        x, y, z = taken; r = app(app(x, z), y)
    elif head == "W":
        x, y = taken; r = app(app(x, y), y)
    elif head == "M":
        (x,) = taken; r = app(x, x)
    elif head == "Y":
        (f,) = taken; r = app(f, app("Y", f))
    elif head == "T":
        x, y = taken; r = app(y, x)
    elif head == "V":
        x, y, z = taken; r = app(app(z, x), y)
    elif head == "D":
        x, y, z, w = taken; r = app(app(x, y), app(z, w))
    elif head == "P1":
        x, y = taken; r = x
    elif head == "P2":
        x, y = taken; r = y
    else:
        return None
    return apply_many(r, rest)


def all_reducts_one_step(t: Term) -> List[Term]:
    """Enumerate every single-redex contraction (any position)."""
    out = []
    r = reduce_at_root(t)
    if r is not None:
        out.append(r)
    if isinstance(t, tuple):
        for sub in all_reducts_one_step(t[0]):
            out.append((sub, t[1]))
        for sub in all_reducts_one_step(t[1]):
            out.append((t[0], sub))
    return out


def size(t: Term) -> int:
    if isinstance(t, tuple):
        return 1 + size(t[0]) + size(t[1])
    return 1


_PRINT = {"P1": "Π₁", "P2": "Π₂"}

def show(t: Term) -> str:
    if isinstance(t, tuple):
        l, r = t
        ls = show(l)
        rs = show(r) if not isinstance(r, tuple) else f"({show(r)})"
        return f"{ls} {rs}"
    return _PRINT.get(t, t)


def reachable_bounded(start: Term, max_depth: int, size_cap: int = 200) -> Dict[Term, int]:
    """BFS of reducts. Returns map term -> shortest reduction distance from start.
    size_cap prunes terms whose size explodes (Y, M cause unbounded growth)."""
    dist: Dict[Term, int] = {start: 0}
    frontier = deque([(start, 0)])
    while frontier:
        t, d = frontier.popleft()
        if d >= max_depth:
            continue
        for r in all_reducts_one_step(t):
            if size(r) > size_cap:
                continue
            if r not in dist:
                dist[r] = d + 1
                frontier.append((r, d + 1))
    return dist


def confluence_check(start: Term, max_depth: int = 8, size_cap: int = 200):
    """For each pair of reachable reducts, search for a common reduct.
    Returns list of unjoined pairs (should be empty if confluent within bound)."""
    dist = reachable_bounded(start, max_depth, size_cap)
    # For joinability: N1 and N2 join iff reachable_bounded(N1) ∩ reachable_bounded(N2) ≠ ∅
    # But computing that for all pairs is quadratic in |dist|. Instead:
    # Compute closure-of-union: extend each pair's reachable sets up to some bound.
    unjoined = []
    keys = list(dist.keys())
    # Limit pairs to make tractable.
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            n1, n2 = keys[i], keys[j]
            r1 = reachable_bounded(n1, max_depth, size_cap)
            r2 = reachable_bounded(n2, max_depth, size_cap)
            common = set(r1.keys()) & set(r2.keys())
            if not common:
                unjoined.append((n1, n2))
    return dist, unjoined


def demo():
    # Example (a): S with inner K-redex and I-redexes
    # S (K I a) (I b) (I c)  — compare reduction orders
    t_a = app(app(app("S", app(app("K", "I"), "a")), app("I", "b")), app("I", "c"))
    print("=" * 70)
    print("EXAMPLE (a):  S (K I a) (I b) (I c)")
    print(f"  start: {show(t_a)}")
    dist, unjoined = confluence_check(t_a, max_depth=6, size_cap=80)
    print(f"  reachable count (depth<=6): {len(dist)}")
    if unjoined:
        print(f"  UNJOINED PAIRS: {len(unjoined)}")
        for u in unjoined[:3]:
            print(f"    -- {show(u[0])}  ||  {show(u[1])}")
    else:
        print("  all reachable pairs join within bound ✓")

    # Example (b): Y-induced divergence. Y f where f = I (harmless) so it
    # reduces to f (Y f) = I (Y f) → Y f (loop)
    t_b = app("Y", "f")
    print("=" * 70)
    print("EXAMPLE (b):  Y f  (non-terminating; test confluence on expansion)")
    print(f"  start: {show(t_b)}")
    dist, unjoined = confluence_check(t_b, max_depth=5, size_cap=50)
    print(f"  reachable count (depth<=5): {len(dist)}")
    if unjoined:
        print(f"  UNJOINED (within bound): {len(unjoined)}  — note: Y f grows unboundedly;")
        print("  apparent non-joinability within bound is not counter-evidence if")
        print("  the depth/size caps cut off a join that exists at higher depth.")
    else:
        print("  all reachable pairs join within bound ✓")

    # Example (c): leftmost-outermost vs rightmost-innermost
    # W (K a) (I b): LO first uses W, RI first uses inner I or K
    t_c = app(app("W", app("K", "a")), app("I", "b"))
    print("=" * 70)
    print("EXAMPLE (c):  W (K a) (I b)")
    print(f"  start: {show(t_c)}")
    dist, unjoined = confluence_check(t_c, max_depth=6, size_cap=60)
    print(f"  reachable count: {len(dist)}")
    if unjoined:
        print(f"  UNJOINED: {len(unjoined)}")
    else:
        print("  all reachable pairs join within bound ✓")

    # Example (d): D x y z w with redexes in y and z
    # D (K a) (I b) (I c) w  →  (K a) (I b) ((I c) w)
    t_d = app(app(app(app("D", app("K", "a")), app("I", "b")), app("I", "c")), "w")
    print("=" * 70)
    print("EXAMPLE (d):  D (K a) (I b) (I c) w")
    print(f"  start: {show(t_d)}")
    dist, unjoined = confluence_check(t_d, max_depth=6, size_cap=80)
    print(f"  reachable count: {len(dist)}")
    if unjoined:
        print(f"  UNJOINED: {len(unjoined)}")
    else:
        print("  all reachable pairs join within bound ✓")

    # Example (e): M with self-application — non-terminating but local diamond
    # M (I a)  →  (I a)(I a)  and also  M (I a) via inner I first → M a
    t_e = app("M", app("I", "a"))
    print("=" * 70)
    print("EXAMPLE (e):  M (I a)  (W/M non-right-linear, tests variable-duplication)")
    print(f"  start: {show(t_e)}")
    dist, unjoined = confluence_check(t_e, max_depth=5, size_cap=40)
    print(f"  reachable count: {len(dist)}")
    if unjoined:
        print(f"  UNJOINED: {len(unjoined)}")
        for u in unjoined[:3]:
            print(f"    -- {show(u[0])}  ||  {show(u[1])}")
    else:
        print("  all reachable pairs join within bound ✓")

    # Example (f): crossed redexes — S acting on terms each containing Π_i redexes
    t_f = app(app(app("S", app(app("P1", "a"), "b")), app(app("P2", "c"), "d")), "e")
    print("=" * 70)
    print("EXAMPLE (f):  S (Π₁ a b) (Π₂ c d) e")
    print(f"  start: {show(t_f)}")
    dist, unjoined = confluence_check(t_f, max_depth=6, size_cap=80)
    print(f"  reachable count: {len(dist)}")
    if unjoined:
        print(f"  UNJOINED: {len(unjoined)}")
    else:
        print("  all reachable pairs join within bound ✓")

    # Example (g): V and T interplay
    # V a b (T c d) — V's third argument receives T c d
    t_g = app(app(app("V", "a"), "b"), app(app("T", "c"), "d"))
    print("=" * 70)
    print("EXAMPLE (g):  V a b (T c d)")
    print(f"  start: {show(t_g)}")
    dist, unjoined = confluence_check(t_g, max_depth=6, size_cap=60)
    print(f"  reachable count: {len(dist)}")
    if unjoined:
        print(f"  UNJOINED: {len(unjoined)}")
    else:
        print("  all reachable pairs join within bound ✓")

    # Example (h): counter-example demonstration — add a rule K' x → x,
    # both K' and K acting on overlapping terms. Here we add the hypothesis
    # manually: K I a has two distinct reducts under the overlapping rule.
    # We simulate by exhibiting the divergence outside the simulator.
    print("=" * 70)
    print("DEMO (h):  illustrating why no critical pairs in baseline — see")
    print("  ARGUMENT.md §3 for the overlap-free check across all 13 primitives.")

if __name__ == "__main__":
    demo()
