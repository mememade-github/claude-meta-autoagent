"""Executable oracle for the TRS R.

Signature: 0, nil, a (nullary); s, len, f (unary); cons, c (binary).

Rules:
  rho1: len(nil)          -> 0
  rho2: len(cons(x,ys))   -> s(len(ys))
  rho3: c(x,y)            -> x
  rho4: c(x,y)            -> y
  rho5: f(x)              -> f(s(x))
  rho6: f(x)              -> nil

Terms are tuples (head, *children). Variables are ('var', name).
Positions are tuples of 1-based child indices; () is the root.
"""

from __future__ import annotations


def mk(head, *children):
    return (head,) + children


def is_var(t):
    return isinstance(t, tuple) and len(t) == 2 and t[0] == "var"


def to_str(t):
    if is_var(t):
        return t[1]
    head = t[0]
    args = t[1:]
    if not args:
        return head
    return head + "(" + ", ".join(to_str(a) for a in args) + ")"


X = ("var", "x")
Y = ("var", "y")
YS = ("var", "ys")

RULES = {
    "rho1": (mk("len", mk("nil")), mk("0")),
    "rho2": (mk("len", mk("cons", X, YS)), mk("s", mk("len", YS))),
    "rho3": (mk("c", X, Y), X),
    "rho4": (mk("c", X, Y), Y),
    "rho5": (mk("f", X), mk("f", mk("s", X))),
    "rho6": (mk("f", X), mk("nil")),
}


def match(pattern, term, sub=None):
    if sub is None:
        sub = {}
    if is_var(pattern):
        name = pattern[1]
        if name in sub:
            return sub if sub[name] == term else None
        sub = dict(sub)
        sub[name] = term
        return sub
    if is_var(term):
        return None
    if pattern[0] != term[0] or len(pattern) != len(term):
        return None
    for p, t in zip(pattern[1:], term[1:]):
        sub = match(p, t, sub)
        if sub is None:
            return None
    return sub


def apply_sub(term, sub):
    if is_var(term):
        return sub.get(term[1], term)
    return (term[0],) + tuple(apply_sub(c, sub) for c in term[1:])


def try_rule_at_root(term, rule_name):
    lhs, rhs = RULES[rule_name]
    sub = match(lhs, term)
    if sub is None:
        return None
    return apply_sub(rhs, sub)


def redexes(term, path=()):
    out = []
    for rn in RULES:
        if try_rule_at_root(term, rn) is not None:
            out.append((path, rn))
    if not is_var(term):
        for i, c in enumerate(term[1:], start=1):
            out.extend(redexes(c, path + (i,)))
    return out


def reduce_at(term, path, rule_name):
    if not path:
        return try_rule_at_root(term, rule_name)
    i = path[0]
    new_child = reduce_at(term[i], path[1:], rule_name)
    if new_child is None:
        return None
    return term[:i] + (new_child,) + term[i + 1 :]


def is_nf(term):
    return len(redexes(term)) == 0


def size(term):
    if is_var(term):
        return 1
    return 1 + sum(size(c) for c in term[1:])


def non_variable_positions(term, path=()):
    if is_var(term):
        return []
    out = [path]
    for i, c in enumerate(term[1:], start=1):
        out.extend(non_variable_positions(c, path + (i,)))
    return out


def subterm_at(term, path):
    for i in path:
        term = term[i]
    return term


def replace_at(term, path, new):
    if not path:
        return new
    i = path[0]
    new_child = replace_at(term[i], path[1:], new)
    return term[:i] + (new_child,) + term[i + 1 :]


def occurs(name, term):
    if is_var(term):
        return term[1] == name
    return any(occurs(name, c) for c in term[1:])


def walk(t, sub):
    while is_var(t) and t[1] in sub:
        t = sub[t[1]]
    return t


def deep_walk(t, sub):
    t = walk(t, sub)
    if is_var(t):
        return t
    return (t[0],) + tuple(deep_walk(c, sub) for c in t[1:])


def unify(s, t, sub=None):
    if sub is None:
        sub = {}
    s = walk(s, sub)
    t = walk(t, sub)
    if is_var(s):
        if is_var(t) and s[1] == t[1]:
            return sub
        if occurs(s[1], t):
            return None
        sub = dict(sub)
        sub[s[1]] = t
        return sub
    if is_var(t):
        if occurs(t[1], s):
            return None
        sub = dict(sub)
        sub[t[1]] = s
        return sub
    if s[0] != t[0] or len(s) != len(t):
        return None
    for a, b in zip(s[1:], t[1:]):
        sub = unify(a, b, sub)
        if sub is None:
            return None
    return sub


def rename_vars(term, suffix):
    if is_var(term):
        return ("var", term[1] + suffix)
    return (term[0],) + tuple(rename_vars(c, suffix) for c in term[1:])


def critical_pairs():
    """Enumerate every (ni, nj, position) overlap, unified where possible."""
    out = []
    for ni, (lhs_i, rhs_i) in RULES.items():
        lhs_i_r = rename_vars(lhs_i, "#i")
        rhs_i_r = rename_vars(rhs_i, "#i")
        for nj, (lhs_j, rhs_j) in RULES.items():
            lhs_j_r = rename_vars(lhs_j, "#j")
            rhs_j_r = rename_vars(rhs_j, "#j")
            for p in non_variable_positions(lhs_i_r):
                sub_at_p = subterm_at(lhs_i_r, p)
                u = unify(sub_at_p, lhs_j_r)
                if u is None:
                    out.append((ni, nj, p, None, None, "non-unifiable"))
                    continue
                overlap = deep_walk(lhs_i_r, u)
                outer_reduct = deep_walk(rhs_i_r, u)
                inner_replacement = deep_walk(rhs_j_r, u)
                inner_reduct_full = replace_at(overlap, p, inner_replacement)
                if p == () and ni == nj:
                    disposition = "same-rule-at-root (trivial)"
                elif outer_reduct == inner_reduct_full:
                    disposition = "identical reducts (trivial)"
                else:
                    disposition = "nontrivial"
                out.append((ni, nj, p, outer_reduct, inner_reduct_full, disposition))
    return out


def reachable(term, max_steps=20, max_size=80):
    seen = {term}
    frontier = [term]
    for _ in range(max_steps):
        new_frontier = []
        for t in frontier:
            for path, rn in redexes(t):
                r = reduce_at(t, path, rn)
                if r is not None and size(r) <= max_size and r not in seen:
                    seen.add(r)
                    new_frontier.append(r)
        if not new_frontier:
            break
        frontier = new_frontier
    return seen


def common_reduct(u, v, max_steps=10, max_size=40):
    ru = reachable(u, max_steps, max_size)
    rv = reachable(v, max_steps, max_size)
    common = ru & rv
    return next(iter(common)) if common else None


def test_per_rule_size_delta():
    print("\n=== Per-rule size deltas on closed instances ===")
    instances = {
        "rho1": (mk("len", mk("nil")), "(no vars)"),
        "rho2": (mk("len", mk("cons", mk("0"), mk("nil"))), "x=0, ys=nil"),
        "rho3": (mk("c", mk("0"), mk("a")), "x=0, y=a"),
        "rho4": (mk("c", mk("0"), mk("a")), "x=0, y=a"),
        "rho5": (mk("f", mk("0")), "x=0"),
        "rho6": (mk("f", mk("0")), "x=0"),
    }
    for rn, (t, desc) in instances.items():
        r = try_rule_at_root(t, rn)
        delta = size(r) - size(t)
        sign = "+" if delta > 0 else ""
        print(f"  {rn}: {to_str(t):32s} -> {to_str(r):20s}  size {size(t)} -> {size(r)}  (delta {sign}{delta})  [{desc}]")


def test_q1_non_confluence_witness():
    print("\n=== Q1 witness: R is NOT confluent ===")
    t = mk("c", mk("0"), mk("nil"))
    u = reduce_at(t, (), "rho3")
    v = reduce_at(t, (), "rho4")
    print(f"  t   = {to_str(t)}")
    print(f"  t --rho3@eps--> {to_str(u)}")
    print(f"  t --rho4@eps--> {to_str(v)}")
    assert u == mk("0") and v == mk("nil")
    assert is_nf(u), f"{to_str(u)} not NF"
    assert is_nf(v), f"{to_str(v)} not NF"
    print(f"  is_nf({to_str(u)}) = {is_nf(u)};  is_nf({to_str(v)}) = {is_nf(v)}")
    print(f"  reachable({to_str(u)}) = {{{', '.join(to_str(x) for x in reachable(u))}}}")
    print(f"  reachable({to_str(v)}) = {{{', '.join(to_str(x) for x in reachable(v))}}}")
    assert not (reachable(u) & reachable(v))
    print(f"  reachable({to_str(u)}) cap reachable({to_str(v)}) = empty  ==> no common reduct")


def test_q1_cp_enumeration():
    print("\n=== Q1 critical-pair enumeration (every (rho_i, rho_j, pos)) ===")
    rows = critical_pairs()
    unifiable = [r for r in rows if r[5] != "non-unifiable"]
    nonunif = len(rows) - len(unifiable)
    print(f"  total (rho_i, rho_j, pos) triples: {len(rows)}")
    print(f"  non-unifiable (head mismatch or variable position):  {nonunif}")
    print(f"  unifiable:                                            {len(unifiable)}")
    print(f"\n  Unifiable overlaps (details):")
    for (ni, nj, p, o, i, disp) in unifiable:
        pstr = "eps" if p == () else ".".join(str(x) for x in p)
        joinmark = ""
        if disp == "same-rule-at-root (trivial)":
            joinmark = "[trivial]"
        elif disp == "identical reducts (trivial)":
            joinmark = "[identical reducts]"
        else:
            cr = common_reduct(o, i)
            if cr is not None:
                joinmark = f"[joinable -> {to_str(cr)}]"
            else:
                joinmark = "[NON-JOINABLE]"
        print(f"    ({ni}, {nj}, pos={pstr}): <{to_str(o)}, {to_str(i)}>   {joinmark}")


def test_q2_wn_strategy():
    print("\n=== Q2 strategy 'any redex except rho5' terminates with strict size decrease ===")

    def step(t):
        for path, rn in redexes(t):
            if rn != "rho5":
                return reduce_at(t, path, rn), rn, path
        return None, None, None

    terms = [
        mk("c", mk("0"), mk("nil")),
        mk("f", mk("0")),
        mk("f", mk("a")),
        mk("len", mk("cons", mk("0"), mk("cons", mk("a"), mk("nil")))),
        mk("f", mk("c", mk("0"), mk("a"))),
        mk("len", mk("c", mk("cons", mk("0"), mk("nil")), mk("nil"))),
        mk("c", mk("f", mk("0")), mk("len", mk("cons", mk("a"), mk("nil")))),
        mk("f", mk("f", mk("0"))),
        mk("f", mk("f", mk("f", mk("f", mk("0"))))),
        mk("c",
           mk("f", mk("f", mk("0"))),
           mk("len", mk("cons", mk("f", mk("a")), mk("cons", mk("0"), mk("nil"))))),
        mk("len", mk("cons",
                     mk("f", mk("c", mk("0"), mk("a"))),
                     mk("cons", mk("f", mk("a")), mk("nil")))),
    ]
    for t in terms:
        orig = to_str(t)
        cur = t
        sizes = [size(cur)]
        steps = 0
        rule_hist = []
        while not is_nf(cur) and steps < 2000:
            nxt, rn, p = step(cur)
            assert nxt is not None, f"strategy stuck on {to_str(cur)}"
            assert size(nxt) < size(cur), (
                f"non-decrease under {rn}: {to_str(cur)} -> {to_str(nxt)}  "
                f"sizes {size(cur)} -> {size(nxt)}"
            )
            rule_hist.append(rn)
            cur = nxt
            sizes.append(size(cur))
            steps += 1
        assert is_nf(cur)
        from collections import Counter
        rc = dict(Counter(rule_hist))
        print(f"  {orig}  =>  {to_str(cur)}  ({steps} steps, size {sizes[0]}->{sizes[-1]}, rules: {rc})")


def test_q3_infinite_sequence():
    print("\n=== Q3 witness: infinite reduction via rho5 ===")
    t = mk("f", mk("0"))
    print(f"  t_0 = {to_str(t)}   size={size(t)}")
    for n in range(1, 21):
        nxt = reduce_at(t, (), "rho5")
        assert nxt is not None
        peeled = nxt[1]
        layers = 0
        while isinstance(peeled, tuple) and peeled[0] == "s":
            layers += 1
            peeled = peeled[1]
        assert peeled == mk("0") and layers == n
        t = nxt
        if n <= 3 or n == 20:
            print(f"  t_{n} = {to_str(t)}   size={size(t)}   via rho5@eps")
        elif n == 4:
            print(f"  ... (structure: f(s^n(0)); each step appends one s-layer) ...")
    print(f"  t_20 confirmed at size {size(t)}; sequence is unbounded.")


def test_q1_rho5_rho6_overlap_joinable():
    print("\n=== Q1 sanity: (rho5, rho6) at eps is joinable ===")
    # CP (with x unified): outer reduct is f(s(x)), inner reduct is nil.
    # As a CP over variables, we must test joinability using the
    # variable-as-constant pattern (rewriting is closed under context
    # of substitution, so joinability at some closed instance suffices).
    u = mk("f", mk("s", mk("0")))  # f(s(x)) with x := 0
    v = mk("nil")                  # nil
    ru = reachable(u)
    rv = reachable(v)
    common = ru & rv
    print(f"  f(s(0)) -->* nil via rho6;  rho6 at eps closes the CP.")
    assert common, f"no common reduct"


def test_claimed_nfs():
    print("\n=== Sanity: claimed NFs are irreducible ===")
    nfs = [
        mk("0"), mk("nil"), mk("a"),
        mk("s", mk("0")), mk("s", mk("s", mk("0"))),
        mk("cons", mk("0"), mk("nil")),
        mk("cons", mk("a"), mk("cons", mk("0"), mk("nil"))),
    ]
    for t in nfs:
        assert is_nf(t), f"{to_str(t)} has redex {redexes(t)}"
        print(f"  {to_str(t)}   [NF confirmed]")


def test_wn_strategy_on_random_terms():
    print("\n=== Q2 stress: strategy on 50 closed random terms ===")
    import random
    random.seed(0)
    nullary = ["0", "nil", "a"]
    unary = ["s", "len", "f"]
    binary = ["cons", "c"]

    def gen(depth):
        if depth == 0:
            return mk(random.choice(nullary))
        r = random.random()
        if r < 0.3:
            return mk(random.choice(nullary))
        elif r < 0.65:
            return mk(random.choice(unary), gen(depth - 1))
        else:
            return mk(random.choice(binary), gen(depth - 1), gen(depth - 1))

    def step(t):
        for path, rn in redexes(t):
            if rn != "rho5":
                return reduce_at(t, path, rn), rn, path
        return None, None, None

    worst = 0
    for _ in range(50):
        d = random.randint(2, 6)
        t = gen(d)
        cur = t
        sz0 = size(cur)
        steps = 0
        while not is_nf(cur) and steps < 5000:
            nxt, rn, p = step(cur)
            assert nxt is not None
            assert size(nxt) < size(cur)
            cur = nxt
            steps += 1
        assert is_nf(cur)
        worst = max(worst, steps)
    print(f"  50/50 reached NF; max steps observed: {worst}")


if __name__ == "__main__":
    test_per_rule_size_delta()
    test_q1_non_confluence_witness()
    test_q1_cp_enumeration()
    test_q1_rho5_rho6_overlap_joinable()
    test_q2_wn_strategy()
    test_q3_infinite_sequence()
    test_claimed_nfs()
    test_wn_strategy_on_random_terms()
    print("\n=== All oracle checks passed. ===")
