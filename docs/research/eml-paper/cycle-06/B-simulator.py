"""
Executable oracle for the TRS

  rho1: len(nil)              -> 0
  rho2: len(cons(x, ys))      -> s(len(ys))
  rho3: app(nil, ys)          -> ys
  rho4: app(cons(x, xs), ys)  -> cons(x, app(xs, ys))
  rho5: app(app(xs, ys), zs)  -> app(xs, app(ys, zs))

Provides:
  - Term construction / pretty-print
  - One-step rewrite enumeration (all redex positions x all matching rules)
  - Normal-form reducer (leftmost-outermost and innermost strategies)
  - Joinability check via BFS on the one-step graph up to a bound
  - Polynomial interpretation phi and per-step strict-decrease check

Used to cross-check hand claims in ARGUMENT.md:
  * Every critical pair is joinable.
  * phi(t) strictly decreases at every rewrite step on the test suite.
  * Sample closed terms reduce to a unique normal form regardless of
    reduction order.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional, Set, Iterator


# ---------------------------- Terms ----------------------------

@dataclass(frozen=True)
class Term:
    head: str
    args: Tuple["Term", ...]

    def __repr__(self) -> str:
        if not self.args:
            return self.head
        return self.head + "(" + ",".join(repr(a) for a in self.args) + ")"


def v(name: str) -> Term:
    # Variables are encoded as nullary heads starting with '?'.
    return Term("?" + name, ())


def is_var(t: Term) -> bool:
    return t.head.startswith("?") and not t.args


def O() -> Term: return Term("0", ())
def NIL() -> Term: return Term("nil", ())
def S(x: Term) -> Term: return Term("s", (x,))
def CONS(x: Term, y: Term) -> Term: return Term("cons", (x, y))
def LEN(x: Term) -> Term: return Term("len", (x,))
def APP(x: Term, y: Term) -> Term: return Term("app", (x, y))


# ---------------------------- Matching ----------------------------

def match(pat: Term, term: Term, env: Optional[dict] = None) -> Optional[dict]:
    if env is None:
        env = {}
    if is_var(pat):
        name = pat.head
        if name in env:
            return env if env[name] == term else None
        env = dict(env)
        env[name] = term
        return env
    if pat.head != term.head or len(pat.args) != len(term.args):
        return None
    for p, t in zip(pat.args, term.args):
        env = match(p, t, env)
        if env is None:
            return None
    return env


def subst(t: Term, env: dict) -> Term:
    if is_var(t):
        return env.get(t.head, t)
    return Term(t.head, tuple(subst(a, env) for a in t.args))


# ---------------------------- Rules ----------------------------

X, Y, XS, YS, ZS = v("x"), v("y"), v("xs"), v("ys"), v("zs")

RULES = [
    ("rho1", LEN(NIL()), O()),
    ("rho2", LEN(CONS(X, YS)), S(LEN(YS))),
    ("rho3", APP(NIL(), YS), YS),
    ("rho4", APP(CONS(X, XS), YS), CONS(X, APP(XS, YS))),
    ("rho5", APP(APP(XS, YS), ZS), APP(XS, APP(YS, ZS))),
]


# ---------------------------- Rewriting ----------------------------

def positions(t: Term, pref: Tuple[int, ...] = ()) -> Iterator[Tuple[int, ...]]:
    yield pref
    for i, a in enumerate(t.args):
        yield from positions(a, pref + (i,))


def at(t: Term, p: Tuple[int, ...]) -> Term:
    for i in p:
        t = t.args[i]
    return t


def replace(t: Term, p: Tuple[int, ...], r: Term) -> Term:
    if not p:
        return r
    i, rest = p[0], p[1:]
    new_args = list(t.args)
    new_args[i] = replace(t.args[i], rest, r)
    return Term(t.head, tuple(new_args))


def one_step_rewrites(t: Term) -> List[Tuple[str, Tuple[int, ...], Term]]:
    out = []
    for p in positions(t):
        sub = at(t, p)
        for name, lhs, rhs in RULES:
            env = match(lhs, sub)
            if env is not None:
                new_sub = subst(rhs, env)
                out.append((name, p, replace(t, p, new_sub)))
    return out


# ---------------------------- Polynomial interpretation ----------------------------
# [0] = 0
# [nil] = 1
# [s](x)       = x + 1
# [cons](x, y) = x + y + 2
# [len](x)     = x
# [app](x, y)  = 2x + y + 1
# (Variables are not present in closed terms; simulator only uses closed terms.)

def phi(t: Term) -> int:
    if is_var(t):
        raise ValueError("phi defined only on closed terms")
    h = t.head
    if h == "0":   return 0
    if h == "nil": return 1
    if h == "s":   return phi(t.args[0]) + 1
    if h == "cons":return phi(t.args[0]) + phi(t.args[1]) + 2
    if h == "len": return phi(t.args[0])
    if h == "app": return 2 * phi(t.args[0]) + phi(t.args[1]) + 1
    raise ValueError("unknown head " + h)


# ---------------------------- Normalization and joinability ----------------------------

def reduce_to_nf(t: Term, strategy: str = "leftmost-outermost",
                 max_steps: int = 10_000) -> Tuple[Term, List[Tuple[str, Tuple[int, ...]]], List[int]]:
    trace = []
    measures = [phi(t)]
    for _ in range(max_steps):
        steps = one_step_rewrites(t)
        if not steps:
            return t, trace, measures
        if strategy == "leftmost-outermost":
            steps.sort(key=lambda s: s[1])
            name, p, t2 = steps[0]
        elif strategy == "rightmost-innermost":
            steps.sort(key=lambda s: s[1], reverse=True)
            name, p, t2 = steps[0]
        else:
            raise ValueError(strategy)
        if phi(t2) >= measures[-1]:
            raise RuntimeError(f"phi did not strictly decrease at {name} pos {p}: "
                               f"{measures[-1]} -> {phi(t2)} on {t} -> {t2}")
        trace.append((name, p))
        measures.append(phi(t2))
        t = t2
    raise RuntimeError("step bound exceeded")


def bfs_reachable(t: Term, bound: int = 1000) -> Set[Term]:
    seen = {t}
    frontier = [t]
    while frontier and len(seen) < bound:
        nxt = []
        for u in frontier:
            for _, _, v in one_step_rewrites(u):
                if v not in seen:
                    seen.add(v)
                    nxt.append(v)
        frontier = nxt
    return seen


def join(t1: Term, t2: Term, bound: int = 1000) -> Optional[Term]:
    r1 = bfs_reachable(t1, bound)
    r2 = bfs_reachable(t2, bound)
    common = r1 & r2
    if not common:
        return None
    return min(common, key=lambda x: phi(x))


# ---------------------------- Critical-pair test ----------------------------
# Instantiate the three non-trivial overlaps with closed witnesses and
# check joinability mechanically.

def critical_pair_witnesses():
    """Build the three non-trivial overlaps at a concrete ground instance
    and reduce each way to a common reduct."""
    out = []

    # CP1: (rho3, rho5) overlap at position 1 of rho5's LHS.
    # LHS instance: app(app(nil, YS), ZS). Put YS := cons(0, nil), ZS := cons(s(0), nil).
    ys_inst = CONS(O(), NIL())
    zs_inst = CONS(S(O()), NIL())
    t = APP(APP(NIL(), ys_inst), zs_inst)
    # Path a: rho3 at pos (0,) on subterm app(nil, YS) -> YS, giving app(YS, ZS).
    path_a = APP(ys_inst, zs_inst)
    # Path b: rho5 at root -> app(nil, app(YS, ZS)) -> (rho3) app(YS, ZS).
    path_b_one = APP(NIL(), APP(ys_inst, zs_inst))
    out.append(("CP1 (rho3, rho5) at pos 1", t, path_a, path_b_one))

    # CP2: (rho4, rho5) overlap at position 1 of rho5's LHS.
    # Instance: app(app(cons(X, XS), YS), ZS) with X := 0, XS := nil, YS := cons(s(0), nil), ZS := nil.
    x_inst = O()
    xs_inst = NIL()
    ys2 = CONS(S(O()), NIL())
    zs2 = NIL()
    t2 = APP(APP(CONS(x_inst, xs_inst), ys2), zs2)
    # Path a: rho4 at pos (0,) -> app(cons(0, app(nil, ys2)), nil).
    path_a2 = APP(CONS(x_inst, APP(xs_inst, ys2)), zs2)
    # Path b: rho5 at root -> app(cons(0, nil), app(ys2, nil)).
    path_b2 = APP(CONS(x_inst, xs_inst), APP(ys2, zs2))
    out.append(("CP2 (rho4, rho5) at pos 1", t2, path_a2, path_b2))

    # CP3: (rho5, rho5) self-overlap at position 1.
    # Instance: app(app(app(XS, YS), ZS), WS). Pick XS := nil, YS := cons(0, nil), ZS := nil, WS := cons(s(0), nil).
    xs3 = NIL()
    ys3 = CONS(O(), NIL())
    zs3 = NIL()
    ws3 = CONS(S(O()), NIL())
    t3 = APP(APP(APP(xs3, ys3), zs3), ws3)
    # Path a: rho5 at (0,) first: app(app(xs3, app(ys3, zs3)), ws3)
    path_a3 = APP(APP(xs3, APP(ys3, zs3)), ws3)
    # Path b: rho5 at root first: app(app(xs3, ys3), app(zs3, ws3))
    path_b3 = APP(APP(xs3, ys3), APP(zs3, ws3))
    out.append(("CP3 (rho5, rho5) at pos 1", t3, path_a3, path_b3))

    return out


# ---------------------------- Main ----------------------------

def main():
    print("=" * 60)
    print("Critical-pair joinability (ground instances)")
    print("=" * 60)
    for label, origin, a, b in critical_pair_witnesses():
        print(f"\n{label}")
        print(f"  origin:  {origin}   phi={phi(origin)}")
        print(f"  path a:  {a}   phi={phi(a)}")
        print(f"  path b:  {b}   phi={phi(b)}")
        w = join(a, b)
        if w is None:
            print("  FAIL: no common reduct within bound")
        else:
            print(f"  common reduct: {w}   phi={phi(w)}")

    print()
    print("=" * 60)
    print("Reduction-order independence on sample terms")
    print("=" * 60)
    samples = [
        APP(APP(APP(NIL(), NIL()), NIL()), NIL()),
        APP(APP(CONS(O(), NIL()), CONS(S(O()), NIL())), CONS(O(), NIL())),
        LEN(APP(CONS(O(), NIL()), CONS(S(O()), NIL()))),
        LEN(APP(APP(CONS(O(), CONS(S(O()), NIL())),
                    CONS(O(), NIL())),
                CONS(S(S(O())), NIL()))),
        APP(APP(CONS(O(), NIL()), NIL()), CONS(S(O()), NIL())),
    ]
    for t in samples:
        nf_lo, tr_lo, m_lo = reduce_to_nf(t, "leftmost-outermost")
        nf_ri, tr_ri, m_ri = reduce_to_nf(t, "rightmost-innermost")
        print(f"\n  t = {t}   phi={phi(t)}")
        print(f"    leftmost-outermost: {len(tr_lo):3d} steps,  nf = {nf_lo}  phi={phi(nf_lo)}")
        print(f"    rightmost-innermost:{len(tr_ri):3d} steps,  nf = {nf_ri}  phi={phi(nf_ri)}")
        assert nf_lo == nf_ri, "normal forms disagree!"
        print(f"    phi strictly decreases along both traces: OK")

    print()
    print("=" * 60)
    print("All rule applications on sample pool cross-checked for phi-decrease")
    print("=" * 60)
    pool = []
    for t in samples:
        pool.extend(bfs_reachable(t, bound=200))
    checks = 0
    for t in pool:
        for name, p, t2 in one_step_rewrites(t):
            if phi(t) <= phi(t2):
                print(f"  FAIL at {name} pos {p}: {t} -> {t2}   phi {phi(t)} -> {phi(t2)}")
                return
            checks += 1
    print(f"  {checks} rewrite steps across reachable pool: phi strictly decreases on every step.")


if __name__ == "__main__":
    main()
