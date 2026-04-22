"""
Executable oracle for the 6-rule TRS R on signature Sigma.

Sigma:
  nullary constructors:   0, nil, a
  unary  constructor :    s
  binary constructor :    cons
  unary  defined     :    len, f
  binary defined     :    c

Rules:
  rho1: len(nil)              -> 0
  rho2: len(cons(x, ys))      -> s(len(ys))
  rho3: c(x, y)               -> x
  rho4: c(x, y)               -> y
  rho5: f(x)                  -> f(s(x))
  rho6: f(x)                  -> nil

Terms are represented as tuples (head, args...) with atoms as ('0',), ('nil',), ('a',).
Variables in rule patterns are strings '?x', '?y', '?ys'.

The oracle performs:
  (A) critical-pair enumeration by first-order unification over every non-variable
      position of every LHS.
  (B) Q1 non-confluence witness: c(0, nil) has two distinct NF reducts.
  (C) Q3 infinite-reduction witness: f(0) -> f(s(0)) -> f(s(s(0))) -> ...
  (D) per-rule strict-decrease check for the Q2 measure mu over a grid of small
      ground instantiations, confirming rho1,rho2,rho3,rho4,rho6 strictly decrease
      mu and rho5 increases it.
  (E) WN strategy simulation: for each seed term, run strategy S (never-rho5,
      leftmost-outermost) and verify termination + strict mu-decrease on each step.

Run: python3 sim.py
"""

import itertools


# ---------- term machinery ----------

def is_var(t):
    return isinstance(t, str) and t.startswith("?")

def mk(head, *args):
    return (head,) + tuple(args)

def pretty(t):
    if is_var(t):
        return t
    h = t[0]
    args = t[1:]
    if not args:
        return h
    return h + "(" + ", ".join(pretty(a) for a in args) + ")"


RULES = [
    ("rho1", mk("len", mk("nil")), mk("0")),
    ("rho2", mk("len", mk("cons", "?x", "?ys")), mk("s", mk("len", "?ys"))),
    ("rho3", mk("c", "?x", "?y"), "?x"),
    ("rho4", mk("c", "?x", "?y"), "?y"),
    ("rho5", mk("f", "?x"), mk("f", mk("s", "?x"))),
    ("rho6", mk("f", "?x"), mk("nil")),
]

def rename_rule(rule, tag):
    name, lhs, rhs = rule
    def ren(t):
        if is_var(t):
            return t + tag
        return mk(t[0], *[ren(a) for a in t[1:]])
    return name, ren(lhs), ren(rhs)


# ---------- substitution / unification ----------

def subst(t, s):
    if is_var(t):
        return subst(s[t], s) if t in s else t
    return mk(t[0], *[subst(a, s) for a in t[1:]])

def occurs(v, t, s):
    t = subst(t, s)
    if is_var(t):
        return t == v
    return any(occurs(v, a, s) for a in t[1:])

def unify(t1, t2, s=None):
    if s is None:
        s = {}
    t1 = subst(t1, s); t2 = subst(t2, s)
    if is_var(t1):
        if t1 == t2:
            return s
        if occurs(t1, t2, s):
            return None
        s2 = dict(s); s2[t1] = t2
        return s2
    if is_var(t2):
        return unify(t2, t1, s)
    if t1[0] != t2[0] or len(t1) != len(t2):
        return None
    cur = s
    for a, b in zip(t1[1:], t2[1:]):
        cur = unify(a, b, cur)
        if cur is None:
            return None
    return cur


# ---------- rewriting ----------

def match(pattern, t, s=None):
    if s is None:
        s = {}
    if is_var(pattern):
        if pattern in s:
            return s if s[pattern] == t else None
        s2 = dict(s); s2[pattern] = t
        return s2
    if is_var(t):
        return None
    if pattern[0] != t[0] or len(pattern) != len(t):
        return None
    cur = s
    for a, b in zip(pattern[1:], t[1:]):
        cur = match(a, b, cur)
        if cur is None:
            return None
    return cur

def positions(t, prefix=()):
    yield prefix
    if is_var(t):
        return
    for i, a in enumerate(t[1:], 1):
        yield from positions(a, prefix + (i,))

def subterm(t, p):
    for i in p:
        t = t[i]
    return t

def replace(t, p, new):
    if not p:
        return new
    i = p[0]
    return mk(t[0], *[(replace(a, p[1:], new) if j == i else a)
                      for j, a in enumerate(t[1:], 1)])

def all_redexes(t):
    for p in positions(t):
        st = subterm(t, p)
        if is_var(st):
            continue
        for name, lhs, _rhs in RULES:
            if match(lhs, st) is not None:
                yield p, name

def reduce_at(t, p, rule_name):
    for name, lhs, rhs in RULES:
        if name != rule_name:
            continue
        st = subterm(t, p)
        s = match(lhs, st)
        if s is None:
            raise ValueError(f"rule {rule_name} does not match at {p} of {pretty(t)}")
        return replace(t, p, subst(rhs, s))
    raise ValueError(f"unknown rule {rule_name}")

def is_normal_form(t):
    return not any(True for _ in all_redexes(t))


# ---------- (A) critical-pair enumeration ----------

def nonvar_positions(t, prefix=()):
    if is_var(t):
        return
    yield prefix
    for i, a in enumerate(t[1:], 1):
        yield from nonvar_positions(a, prefix + (i,))

def critical_pairs():
    pairs = []
    for i, rule_i in enumerate(RULES):
        ri_name, li, ri = rename_rule(rule_i, "_out")
        for j, rule_j in enumerate(RULES):
            rj_name, lj, rj = rename_rule(rule_j, "_in")
            for p in nonvar_positions(li):
                if i == j and p == ():
                    continue
                subi = subterm(li, p)
                s = unify(subi, lj)
                if s is None:
                    continue
                source = subst(li, s)
                outer_reduct = subst(ri, s)
                inner_reduct = replace(subst(li, s), p, subst(rj, s))
                pairs.append({
                    "ri": ri_name, "rj": rj_name, "pos": p,
                    "source": source,
                    "outer_reduct": outer_reduct,
                    "inner_reduct": inner_reduct,
                })
    return pairs


# ---------- (D) Q2 measure ----------

def mu(t):
    if is_var(t):
        return 1
    h = t[0]
    if h in ("0", "nil", "a"):
        return 1
    if h == "s":
        return mu(t[1]) + 1
    if h == "cons":
        return mu(t[1]) + mu(t[2]) + 1
    if h == "len":
        return 2 * mu(t[1]) + 1
    if h == "c":
        return mu(t[1]) + mu(t[2]) + 2
    if h == "f":
        return 2 * mu(t[1]) + 1
    raise ValueError(f"unknown head {h}")


# ---------- (E) strategy S ----------

def strategy_S_step(t):
    candidates = sorted(all_redexes(t), key=lambda pr: (len(pr[0]), pr[0]))
    for p, r in candidates:
        if r != "rho5":
            return p, r
    return None

def run_S(t, max_steps=200):
    trace = [(None, None, t, mu(t))]
    for _ in range(max_steps):
        step = strategy_S_step(t)
        if step is None:
            return trace, True
        p, r = step
        t = reduce_at(t, p, r)
        trace.append((r, p, t, mu(t)))
    return trace, False


# ---------- main ----------

def main():
    print("=" * 70)
    print("SECTION A. Critical-pair enumeration")
    print("=" * 70)
    cps = critical_pairs()
    non_joinable_candidates = []
    for cp in cps:
        equal = cp["outer_reduct"] == cp["inner_reduct"]
        mark = "EQUAL" if equal else "distinct"
        print(f"  ({cp['ri']} outer, {cp['rj']} inner, pos={cp['pos']}): "
              f"src={pretty(cp['source'])}  -> "
              f"{pretty(cp['outer_reduct'])}  ||  {pretty(cp['inner_reduct'])}  [{mark}]")
        if not equal:
            non_joinable_candidates.append(cp)
    print()
    print(f"  Non-trivially-equal CP instances: {len(non_joinable_candidates)}")

    print()
    print("=" * 70)
    print("SECTION B. Q1 non-confluence witness: c(0, nil)")
    print("=" * 70)
    t = mk("c", mk("0"), mk("nil"))
    u = reduce_at(t, (), "rho3")
    v = reduce_at(t, (), "rho4")
    print(f"  t = {pretty(t)}    mu(t) = {mu(t)}")
    print(f"  t ->rho3 {pretty(u)}   (normal form? {is_normal_form(u)})")
    print(f"  t ->rho4 {pretty(v)}   (normal form? {is_normal_form(v)})")
    print(f"  u != v: {u != v}")
    assert is_normal_form(u) and is_normal_form(v) and u != v
    print("  VERIFIED: R is NOT confluent.")

    # Also check f(x) critical pair: f(s(x)) must be joinable with nil via rho6.
    print()
    print("  Aside: the f-critical-pair (rho5, rho6) IS joinable:")
    fs = mk("f", mk("s", mk("0")))
    print(f"    f(s(0)) ->rho6 {pretty(reduce_at(fs, (), 'rho6'))}   == nil")

    print()
    print("=" * 70)
    print("SECTION C. Q3 non-termination witness: f(0)")
    print("=" * 70)
    t = mk("f", mk("0"))
    seq = [t]
    for _ in range(10):
        t = reduce_at(t, (), "rho5")
        seq.append(t)
    for i, ti in enumerate(seq):
        print(f"  step {i}:  {pretty(ti)}    [s-stack depth = {i}]")
    # Quick proof-of-unboundedness: the height of the term is strictly
    # increasing, so the sequence cannot cycle.
    print("  Pattern: after n rho5 steps the term is f(s^n(0)); height strictly")
    print("  grows, so the sequence has no cycle and is unbounded.")

    print()
    print("=" * 70)
    print("SECTION D. Per-rule measure behaviour (mu)")
    print("=" * 70)
    samples = [mk("0"), mk("nil"), mk("a"),
               mk("s", mk("0")), mk("s", mk("s", mk("0"))),
               mk("cons", mk("0"), mk("nil")),
               mk("cons", mk("a"), mk("cons", mk("0"), mk("nil")))]
    for name, lhs, rhs in RULES:
        V = set()
        def fvs(t):
            if is_var(t):
                V.add(t)
            else:
                for a in t[1:]:
                    fvs(a)
        fvs(lhs)
        V = sorted(V)
        deltas = []
        for combo in itertools.product(samples, repeat=len(V)):
            s = dict(zip(V, combo))
            L = subst(lhs, s); R = subst(rhs, s)
            deltas.append(mu(L) - mu(R))
        sign = "decreases" if min(deltas) > 0 else ("increases" if max(deltas) < 0 else "mixed/zero")
        print(f"  {name}: mu(LHS)-mu(RHS) over {len(deltas)} samples: "
              f"min={min(deltas)}, max={max(deltas)}  [{sign}]")

    print()
    print("=" * 70)
    print("SECTION E. Strategy S terminates on seed terms")
    print("=" * 70)
    L1 = mk("cons", mk("0"), mk("nil"))
    L2 = mk("cons", mk("s", mk("0")), mk("cons", mk("a"), mk("nil")))
    seeds = [
        mk("c", mk("0"), mk("nil")),
        mk("f", mk("0")),
        mk("c", mk("f", mk("0")), mk("len", L2)),
        mk("len", mk("cons", mk("a"), mk("cons", mk("0"), mk("nil")))),
        mk("f", mk("c", mk("0"), mk("a"))),
        mk("c", mk("f", mk("a")), mk("len", L1)),
    ]
    for seed in seeds:
        trace, done = run_S(seed, max_steps=200)
        print(f"\n  seed: {pretty(seed)}  mu={mu(seed)}")
        for (r, p, ti, m) in trace:
            tag = f"{r} @ {p}" if r else "init"
            print(f"    {tag:22s} -> {pretty(ti):60s} mu={m}")
        ms = [step[3] for step in trace]
        assert all(ms[i] > ms[i+1] for i in range(len(ms)-1))
        assert done
        nf = trace[-1][2]
        assert is_normal_form(nf)
        print(f"    FINAL normal form: {pretty(nf)}  (mu decreased {ms[0]} -> {ms[-1]})")

    print()
    print("All oracle checks passed.")


if __name__ == "__main__":
    main()
