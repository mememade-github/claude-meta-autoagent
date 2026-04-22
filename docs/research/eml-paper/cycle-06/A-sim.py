"""
Executable oracle for the 5-rule list TRS:

  rho1:  len(nil)              -> 0
  rho2:  len(cons(x, ys))      -> s(len(ys))
  rho3:  app(nil, ys)          -> ys
  rho4:  app(cons(x, xs), ys)  -> cons(x, app(xs, ys))
  rho5:  app(app(xs, ys), zs)  -> app(xs, app(ys, zs))

Term encoding: nested tuples headed by a string constructor name.
  ('0',)             zero
  ('nil',)           empty list
  ('s', t)           successor
  ('cons', h, t)     list cons
  ('len', t)         length operator
  ('app', t, u)      list append
  ('X', name)        free variable (used only in CP analysis)

The oracle does four independent things:
  1. Enumerate every one-step reduction of a term.
  2. Compute a polynomial interpretation [[.]] and verify it is
     strictly decreased by every rule firing observed.
  3. Mechanically enumerate all critical pairs by position-unification
     and exhibit joinability for each.
  4. For a test suite of closed terms, exhaustively enumerate the
     reduction graph until no new reducts appear, then check that all
     normal forms are identical (confluence witness) and that the
     interpretation strictly decreases along every edge (termination
     witness with an explicit step bound).
"""

from itertools import product


# ------------------------------------------------------------------
# Term plumbing
# ------------------------------------------------------------------

def pp(t):
    op = t[0]
    if op in ('0', 'nil'):
        return op
    if op == 'X':
        return t[1]
    if len(t) == 2:
        return op + '(' + pp(t[1]) + ')'
    return op + '(' + ', '.join(pp(a) for a in t[1:]) + ')'


def positions(t):
    """Yield (position_tuple, subterm) for every position in t."""
    yield (), t
    for i, arg in enumerate(t[1:], start=1):
        for p, s in positions(arg):
            yield (i,) + p, s


def replace_at(t, pos, new_sub):
    if not pos:
        return new_sub
    i = pos[0]
    args = list(t[1:])
    args[i - 1] = replace_at(args[i - 1], pos[1:], new_sub)
    return (t[0],) + tuple(args)


def subst(t, theta):
    if t[0] == 'X':
        return theta.get(t[1], t)
    return (t[0],) + tuple(subst(a, theta) for a in t[1:])


# ------------------------------------------------------------------
# Rule firing and reduction enumeration
# ------------------------------------------------------------------

def root_reducts(t):
    out = []
    op = t[0]
    if op == 'len' and len(t) == 2:
        a = t[1]
        if a == ('nil',):
            out.append(('rho1', ('0',)))
        elif a[0] == 'cons':
            _x, ys = a[1], a[2]
            out.append(('rho2', ('s', ('len', ys))))
    elif op == 'app' and len(t) == 3:
        a, b = t[1], t[2]
        if a == ('nil',):
            out.append(('rho3', b))
        elif a[0] == 'cons':
            x, xs = a[1], a[2]
            out.append(('rho4', ('cons', x, ('app', xs, b))))
        elif a[0] == 'app':
            xs, ys = a[1], a[2]
            out.append(('rho5', ('app', xs, ('app', ys, b))))
    return out


def one_step(t):
    result = []
    for pos, sub in positions(t):
        for rule, red in root_reducts(sub):
            result.append((rule, pos, replace_at(t, pos, red)))
    return result


# ------------------------------------------------------------------
# Polynomial interpretation (termination witness)
#
#   [0]         = 1
#   [nil]       = 1
#   [s(x)]      = x + 1
#   [cons(x,y)] = x + y + 1
#   [len(x)]    = 2*x
#   [app(x,y)]  = 2*x + y
#
# All atoms >= 1; every constructor strictly monotone in each arg.
# ------------------------------------------------------------------

def interp(t):
    op = t[0]
    if op == '0':     return 1
    if op == 'nil':   return 1
    if op == 's':     return interp(t[1]) + 1
    if op == 'cons':  return interp(t[1]) + interp(t[2]) + 1
    if op == 'len':   return 2 * interp(t[1])
    if op == 'app':   return 2 * interp(t[1]) + interp(t[2])
    if op == 'X':     raise ValueError("interp undefined on open variables")
    raise ValueError("unknown head: " + op)


# ------------------------------------------------------------------
# Critical pair enumeration
# ------------------------------------------------------------------

RULES = {
    'rho1': (('len', ('nil',)), ('0',)),
    'rho2': (('len', ('cons', ('X', 'x'), ('X', 'ys'))),
             ('s', ('len', ('X', 'ys')))),
    'rho3': (('app', ('nil',), ('X', 'ys')), ('X', 'ys')),
    'rho4': (('app', ('cons', ('X', 'x'), ('X', 'xs')), ('X', 'ys')),
             ('cons', ('X', 'x'), ('app', ('X', 'xs'), ('X', 'ys')))),
    'rho5': (('app', ('app', ('X', 'xs'), ('X', 'ys')), ('X', 'zs')),
             ('app', ('X', 'xs'), ('app', ('X', 'ys'), ('X', 'zs')))),
}


def rename_vars(t, suffix):
    if t[0] == 'X':
        return ('X', t[1] + suffix)
    return (t[0],) + tuple(rename_vars(a, suffix) for a in t[1:])


def unify(a, b):
    theta = {}

    def walk(x):
        while x[0] == 'X' and x[1] in theta:
            x = theta[x[1]]
        return x

    def occurs(v, x):
        x = walk(x)
        if x[0] == 'X':
            return x[1] == v
        return any(occurs(v, s) for s in x[1:])

    def uni(x, y):
        x, y = walk(x), walk(y)
        if x[0] == 'X' and y[0] == 'X' and x[1] == y[1]:
            return True
        if x[0] == 'X':
            if occurs(x[1], y): return False
            theta[x[1]] = y
            return True
        if y[0] == 'X':
            if occurs(y[1], x): return False
            theta[y[1]] = x
            return True
        if x[0] != y[0] or len(x) != len(y):
            return False
        return all(uni(xa, ya) for xa, ya in zip(x[1:], y[1:]))

    if not uni(a, b):
        return None

    def resolve(x):
        x = walk(x)
        if x[0] == 'X':
            return x
        return (x[0],) + tuple(resolve(s) for s in x[1:])
    return {k: resolve(v) for k, v in theta.items()}


def critical_pairs():
    """Overlap (ri, rj, position p): ri's LHS at non-variable position p
    unifies with rj's LHS.  (ri == rj, p == root) excluded."""
    cps = []
    for ni, (li, _) in RULES.items():
        li_o = rename_vars(li, '_o')
        _, ri_rhs = RULES[ni]
        ri_rhs_o = rename_vars(ri_rhs, '_o')
        for nj, (lj, rj) in RULES.items():
            lj_i = rename_vars(lj, '_i')
            rj_i = rename_vars(rj, '_i')
            for pos, sub in positions(li_o):
                if sub[0] == 'X':
                    continue
                if ni == nj and pos == ():
                    continue
                theta = unify(sub, lj_i)
                if theta is None:
                    continue
                source = subst(li_o, theta)
                u = subst(ri_rhs_o, theta)  # outer rule fires
                v = replace_at(source, pos, subst(rj_i, theta))  # inner fires
                cps.append((ni, nj, pos, source, u, v))
    return cps


# ------------------------------------------------------------------
# Reachability / confluence oracle
# ------------------------------------------------------------------

def reach_all(t, limit=5000):
    seen = {t}
    frontier = [t]
    while frontier:
        s = frontier.pop(0)
        for _rule, _pos, r in one_step(s):
            if r not in seen:
                seen.add(r)
                frontier.append(r)
                if len(seen) > limit:
                    raise RuntimeError("reach_all overflow on " + pp(t))
    return seen


def normal_forms_in(S):
    return {t for t in S if not one_step(t)}


def nf_leftmost(t):
    while True:
        reds = one_step(t)
        if not reds:
            return t
        t = reds[0][2]


def verify_confluence_and_termination(t, max_reach=5000):
    reach = reach_all(t, limit=max_reach)
    for s in reach:
        ms = interp(s)
        for _r, _p, r in one_step(s):
            if interp(r) >= ms:
                raise AssertionError(
                    "measure not strictly decreasing: "
                    + pp(s) + "(" + str(ms) + ") -> "
                    + pp(r) + "(" + str(interp(r)) + ")")
    nfs = normal_forms_in(reach)
    if len(nfs) != 1:
        raise AssertionError("multiple normal forms: "
                             + ", ".join(pp(x) for x in nfs))
    return {
        'reachable': len(reach),
        'normal_form': next(iter(nfs)),
        'initial_measure': interp(t),
        'max_chain_bound': interp(t) - 1,
    }


# ------------------------------------------------------------------
# Driver
# ------------------------------------------------------------------

def banner(s):
    return "\n" + "=" * 68 + "\n" + s + "\n" + "=" * 68


def section_critical_pairs():
    print(banner("SECTION 1 -- critical-pair enumeration"))
    cps = critical_pairs()
    print("total CPs found:", len(cps))
    for idx, (ni, nj, pos, src, u, v) in enumerate(cps, 1):
        print()
        print("CP#%d  (outer %s overlaps inner %s at pos %s)"
              % (idx, ni, nj, pos))
        print("  source : " + pp(src))
        print("  reduct1: " + pp(u))
        print("  reduct2: " + pp(v))
        # Ground witness: replace remaining variables with a small list
        witness_val = ('cons', ('0',), ('nil',))
        seen_vars = set()

        def collect(x):
            if x[0] == 'X':
                seen_vars.add(x[1])
            else:
                for s in x[1:]:
                    collect(s)
        collect(src); collect(u); collect(v)
        theta = {v_: witness_val for v_ in seen_vars}
        gsrc, gu, gv = subst(src, theta), subst(u, theta), subst(v, theta)
        nf_u, nf_v = nf_leftmost(gu), nf_leftmost(gv)
        print("  ground source -> " + pp(gsrc))
        print("  nf(reduct1) = " + pp(nf_u))
        print("  nf(reduct2) = " + pp(nf_v))
        print("  joinable    = " + str(nf_u == nf_v))


def section_interpretation():
    print(banner("SECTION 2 -- polynomial interpretation, per-rule check"))
    witnesses = [
        ('0',),
        ('nil',),
        ('s', ('0',)),
        ('cons', ('0',), ('nil',)),
        ('cons', ('0',), ('cons', ('s', ('0',)), ('nil',))),
    ]
    for name, (lhs, rhs) in RULES.items():
        vs = set()

        def collect(x):
            if x[0] == 'X':
                vs.add(x[1])
            else:
                for s in x[1:]:
                    collect(s)
        collect(lhs)
        varlist = sorted(vs)
        mn, mx = None, None
        for combo in product(witnesses, repeat=len(varlist)):
            theta = dict(zip(varlist, combo))
            d = interp(subst(lhs, theta)) - interp(subst(rhs, theta))
            mn = d if mn is None else min(mn, d)
            mx = d if mx is None else max(mx, d)
        print("%-6s  [LHS]-[RHS] over witnesses: min=%d max=%d  (must be > 0)"
              % (name, mn, mx))


def section_reduction_graphs():
    print(banner("SECTION 3 -- exhaustive reduction graphs (closed terms)"))
    n0, s0 = ('0',), ('s', ('0',))
    nil_ = ('nil',)
    L1 = ('cons', n0, nil_)
    L2 = ('cons', s0, nil_)
    L3 = ('cons', n0, ('cons', s0, nil_))

    def leftapp(*args):
        t = args[0]
        for a in args[1:]:
            t = ('app', t, a)
        return t

    def rightapp(*args):
        t = args[-1]
        for a in reversed(args[:-1]):
            t = ('app', a, t)
        return t

    tests = [
        ('len(nil)',                      ('len', nil_)),
        ('len(cons(0,cons(s0,nil)))',     ('len', L3)),
        ('app(nil, L2)',                  ('app', nil_, L2)),
        ('app(L1, L2)',                   ('app', L1, L2)),
        ('app(app(nil, L1), L2)',         ('app', ('app', nil_, L1), L2)),
        ('left((L1,L2,L3))',              leftapp(L1, L2, L3)),
        ('left((nil,nil,nil,nil))',       leftapp(nil_, nil_, nil_, nil_)),
        ('len(app(L1,L3))',               ('len', ('app', L1, L3))),
        ('len(left(L1,L2,L3))',           ('len', leftapp(L1, L2, L3))),
        ('right(L1,L2,L3)',               rightapp(L1, L2, L3)),
        ('left(L1,L2,L3,L2,L1)',          leftapp(L1, L2, L3, L2, L1)),
    ]
    for label, t in tests:
        info = verify_confluence_and_termination(t)
        print("  %-30s |reach|=%3d  nf=%-38s  [t0]=%3d  stepsLE=%d"
              % (label, info['reachable'], pp(info['normal_form']),
                 info['initial_measure'], info['max_chain_bound']))


def section_worked_trace():
    print(banner("SECTION 4 -- worked traces with measure per step"))
    L1 = ('cons', ('0',), ('nil',))
    L2 = ('cons', ('s', ('0',)), ('nil',))
    L3 = ('cons', ('0',), ('nil',))
    t = ('app', ('app', L1, L2), L3)

    def trace(label, start, pick):
        print("\n[%s]  start=%s  [t0]=%d" %
              (label, pp(start), interp(start)))
        s = start
        step = 0
        while True:
            reds = one_step(s)
            if not reds:
                print("  (NF at step %d: %s)" % (step, pp(s)))
                return s
            rule, pos, r = pick(reds)
            step += 1
            print("  %2d  %-5s @%-10s -> %s  [.]=%d"
                  % (step, rule, str(pos), pp(r), interp(r)))
            s = r
            if step > 40:
                return s

    nf_a = trace("leftmost-outermost, ((L1@L2)@L3)",
                 t, pick=lambda R: R[0])
    nf_b = trace("rightmost-innermost, ((L1@L2)@L3)",
                 t, pick=lambda R: R[-1])
    print("  converge? %s to %s" % (nf_a == nf_b, pp(nf_a)))

    t2 = ('len', ('app', L1, L2))
    nf_a = trace("len/app interleave A", t2, pick=lambda R: R[0])
    nf_b = trace("len/app interleave B", t2, pick=lambda R: R[-1])
    print("  converge? %s to %s" % (nf_a == nf_b, pp(nf_a)))

    tc = ('app', ('app', ('app', ('nil',), ('nil',)), ('nil',)), ('nil',))
    nf_a = trace("rho5-first on (((nil@nil)@nil)@nil)",
                 tc, pick=lambda R: R[0])
    nf_b = trace("rho3-first on (((nil@nil)@nil)@nil)",
                 tc, pick=lambda R: R[-1])
    print("  converge? %s to %s" % (nf_a == nf_b, pp(nf_a)))


def main():
    section_critical_pairs()
    section_interpretation()
    section_reduction_graphs()
    section_worked_trace()
    print(banner("DONE"))


if __name__ == '__main__':
    main()
