"""Dump step-by-step phi values for the examples used in ARGUMENT.md §6."""

from simulator import (APP, NIL, O, S, CONS, LEN, phi,
                        reduce_to_nf, one_step_rewrites)


def dump(label, t):
    print(f"\n--- {label} ---")
    print(f"t = {t}   phi = {phi(t)}")
    nf_lo, tr_lo, m_lo = reduce_to_nf(t, "leftmost-outermost")
    print(f"  LMO trace ({len(tr_lo)} steps):")
    print(f"    phi: {m_lo}")
    for step, m in zip(tr_lo, m_lo[1:]):
        print(f"    {step}  -> phi={m}")
    nf_ri, tr_ri, m_ri = reduce_to_nf(t, "rightmost-innermost")
    print(f"  RMI trace ({len(tr_ri)} steps):")
    print(f"    phi: {m_ri}")
    for step, m in zip(tr_ri, m_ri[1:]):
        print(f"    {step}  -> phi={m}")
    assert nf_lo == nf_ri


dump("Ex 6.1: app(app(app(nil,nil),nil),nil)",
     APP(APP(APP(NIL(), NIL()), NIL()), NIL()))

dump("Ex 6.2: len(app(cons(0,nil), cons(s(0),nil)))",
     LEN(APP(CONS(O(), NIL()), CONS(S(O()), NIL()))))

dump("Ex 6.3: app(cons(0,nil), cons(s(0),nil))",
     APP(CONS(O(), NIL()), CONS(S(O()), NIL())))

dump("Ex 6.4: app(app(app(nil, cons(0,nil)), nil), cons(s(0),nil))",
     APP(APP(APP(NIL(), CONS(O(), NIL())), NIL()), CONS(S(O()), NIL())))
