"""Executable oracle for the TRS R over signature Sigma.

Signature:
  Nullary: 0, e
  Unary:   s, neg, t
  Binary:  add, mul, q

Rules:
  alpha1: add(0, y)      -> y
  alpha2: add(s(x), y)   -> s(add(x, y))
  alpha3: mul(0, y)      -> 0
  alpha4: mul(s(x), y)   -> add(y, mul(x, y))
  alpha5: q(x, y)        -> x
  alpha6: q(x, y)        -> y
  alpha7: t(x)           -> t(s(x))
  alpha8: neg(neg(x))    -> x

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

RULES = {
    "alpha1": (mk("add", mk("0"), Y), Y),
    "alpha2": (mk("add", mk("s", X), Y), mk("s", mk("add", X, Y))),
    "alpha3": (mk("mul", mk("0"), Y), mk("0")),
    "alpha4": (mk("mul", mk("s", X), Y), mk("add", Y, mk("mul", X, Y))),
    "alpha5": (mk("q", X, Y), X),
    "alpha6": (mk("q", X, Y), Y),
    "alpha7": (mk("t", X), mk("t", mk("s", X))),
    "alpha8": (mk("neg", mk("neg", X)), X),
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
    return term[:i] + (new_child,) + term[i + 1:]


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
    return term[:i] + (new_child,) + term[i + 1:]


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
    """Enumerate every (outer, inner, position) overlap, unified where possible."""
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
        for cur in frontier:
            for path, rn in redexes(cur):
                r = reduce_at(cur, path, rn)
                if r is not None and size(r) <= max_size and r not in seen:
                    seen.add(r)
                    new_frontier.append(r)
        if not new_frontier:
            break
        frontier = new_frontier
    return seen


def test_q1_non_confluence_witness():
    print("\n=== Q1 witness: R is NOT confluent ===")
    t = mk("q", mk("0"), mk("e"))
    u = reduce_at(t, (), "alpha5")
    v = reduce_at(t, (), "alpha6")
    print(f"  t   = {to_str(t)}")
    print(f"  t --alpha5@eps--> {to_str(u)}")
    print(f"  t --alpha6@eps--> {to_str(v)}")
    assert u == mk("0") and v == mk("e")
    assert is_nf(u), f"{to_str(u)} not NF"
    assert is_nf(v), f"{to_str(v)} not NF"
    assert u != v
    print(f"  is_nf({to_str(u)}) = True;  is_nf({to_str(v)}) = True;  0 != e.")
    print(f"  reachable({to_str(u)}) = {{{', '.join(to_str(x) for x in reachable(u))}}}")
    print(f"  reachable({to_str(v)}) = {{{', '.join(to_str(x) for x in reachable(v))}}}")
    assert not (reachable(u) & reachable(v))
    print("  reachable sets are disjoint ==> no common reduct.")


def test_q1_cp_enumeration():
    print("\n=== Q1 critical-pair enumeration (every (outer, inner, pos)) ===")
    rows = critical_pairs()
    unifiable = [r for r in rows if r[5] != "non-unifiable"]
    nonunif = len(rows) - len(unifiable)
    print(f"  total (outer, inner, pos) triples: {len(rows)}")
    print(f"  non-unifiable (head mismatch): {nonunif}")
    print(f"  unifiable:                     {len(unifiable)}")
    print("\n  Unifiable overlaps (details):")
    for (ni, nj, p, o, i, disp) in unifiable:
        pstr = "eps" if p == () else ".".join(str(x) for x in p)
        if disp == "same-rule-at-root (trivial)":
            mark = "[trivial (same rule)]"
        elif disp == "identical reducts (trivial)":
            mark = "[identical reducts]"
        else:
            ru = reachable(o, max_steps=8, max_size=30)
            rv = reachable(i, max_steps=8, max_size=30)
            common = ru & rv
            if common:
                mark = f"[joinable -> e.g. {to_str(next(iter(common)))}]"
            else:
                mark = "[NON-JOINABLE by bounded search]"
        print(f"    ({ni}, {nj}, pos={pstr}): <{to_str(o)}, {to_str(i)}>   {mark}")


def test_q2_not_wn_witness():
    print("\n=== Q2 witness: R is NOT weakly normalizing ===")
    print("  Claim: from t_0 = t(0), the *only* reduction sequence is infinite.")
    print("  Step-by-step unique redex at each stage:")
    cur = mk("t", mk("0"))
    for n in range(0, 10):
        rds = redexes(cur)
        if n <= 3 or n == 9:
            print(f"    t_{n} = {to_str(cur)}   "
                  f"redexes: {[(p or 'eps', rn) for (p, rn) in rds]}")
        elif n == 4:
            print("    ... (pattern persists: only redex is alpha7 at root) ...")
        assert len(rds) == 1, f"expected 1 redex at t_{n}, got {rds}"
        assert rds[0] == ((), "alpha7"), f"unexpected redex {rds[0]}"
        cur = reduce_at(cur, (), "alpha7")
    print(f"    t_9 confirmed at size {size(cur)}")
    print("  Every closed term reachable from t(0) has shape t(s^n(0)), "
          "with unique redex alpha7@eps, so NO normal form is reachable.")


def test_t_subterm_has_only_alpha7_redex():
    """For many terms of shape t(s^n(0)), verify the unique-redex property."""
    print("\n=== Q2 support: uniqueness of the alpha7@eps redex on t(s^n(0)) ===")
    cur = mk("0")
    expected = 1
    for n in range(0, 12):
        term = mk("t", cur)
        rds = redexes(term)
        assert rds == [((), "alpha7")], (
            f"on t(s^{n}(0)): expected only alpha7@eps, got {rds}"
        )
        expected += 1
        cur = mk("s", cur)
    print("  Verified: for n in 0..11, t(s^n(0)) has exactly one redex, at root via alpha7.")


def test_q3_infinite_sequence():
    print("\n=== Q3 witness: infinite reduction via alpha7 ===")
    t = mk("t", mk("0"))
    print(f"  t_0 = {to_str(t)}   size={size(t)}")
    for n in range(1, 21):
        nxt = reduce_at(t, (), "alpha7")
        assert nxt is not None
        # Verify structural form: t(s^n(0)).
        inner = nxt[1]
        layers = 0
        while isinstance(inner, tuple) and inner[0] == "s":
            layers += 1
            inner = inner[1]
        assert inner == mk("0") and layers == n
        t = nxt
        if n <= 3 or n == 20:
            print(f"  t_{n} = {to_str(t)}   size={size(t)}   via alpha7@eps")
        elif n == 4:
            print("  ... (structure: t(s^n(0)); each step appends one s-layer) ...")
    print(f"  t_20 confirmed at size {size(t)}; sequence is unbounded.")


def test_claimed_nfs():
    print("\n=== Sanity: claimed NFs are irreducible ===")
    nfs = [
        mk("0"),
        mk("e"),
        mk("s", mk("0")),
        mk("s", mk("s", mk("e"))),
        mk("neg", mk("0")),
        mk("neg", mk("s", mk("e"))),
    ]
    for n in nfs:
        assert is_nf(n), f"{to_str(n)} has redex {redexes(n)}"
        print(f"  {to_str(n)}   [NF confirmed]")


def test_per_rule_size_delta():
    print("\n=== Per-rule size deltas on representative closed instances ===")
    instances = {
        "alpha1": (mk("add", mk("0"), mk("e")),                    "y=e"),
        "alpha2": (mk("add", mk("s", mk("0")), mk("e")),           "x=0, y=e"),
        "alpha3": (mk("mul", mk("0"), mk("e")),                    "y=e"),
        "alpha4": (mk("mul", mk("s", mk("0")), mk("e")),           "x=0, y=e"),
        "alpha5": (mk("q", mk("0"), mk("e")),                      "x=0, y=e"),
        "alpha6": (mk("q", mk("0"), mk("e")),                      "x=0, y=e"),
        "alpha7": (mk("t", mk("0")),                               "x=0"),
        "alpha8": (mk("neg", mk("neg", mk("e"))),                  "x=e"),
    }
    for rn, (t, desc) in instances.items():
        r = try_rule_at_root(t, rn)
        delta = size(r) - size(t)
        sign = "+" if delta > 0 else ""
        print(f"  {rn}: {to_str(t):28s} -> {to_str(r):20s}  size {size(t)} -> {size(r)}  (delta {sign}{delta})  [{desc}]")


def test_no_lhs_headed_by():
    """Verify that no rule's LHS is headed by 0, e, or s."""
    print("\n=== Sanity: no LHS is headed by 0, e, or s ===")
    for rn, (lhs, _rhs) in RULES.items():
        head = lhs[0]
        assert head not in ("0", "e", "s"), f"rule {rn} has LHS head {head}"
        print(f"  {rn}: LHS head = {head}")
    print("  Conclusion: terms headed by 0, e, or s have no root redex.")
    print("  (Subterm redexes are independent of this.)")


if __name__ == "__main__":
    test_no_lhs_headed_by()
    test_claimed_nfs()
    test_per_rule_size_delta()
    test_q1_non_confluence_witness()
    test_q1_cp_enumeration()
    test_q2_not_wn_witness()
    test_t_subterm_has_only_alpha7_redex()
    test_q3_infinite_sequence()
    print("\n=== All oracle checks passed. ===")
