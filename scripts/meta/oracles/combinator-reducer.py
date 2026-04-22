#!/usr/bin/env python3
"""Combinator β-reducer (weak-head, leftmost-outermost).

Term grammar
    term := ATOM | ( term term+ )
    ATOM := uppercase-run | lowercase-run | digit | (utf-8 greek/subscript OK)

Application is written with explicit parens and is left-associative inside a
single parenthesized group:  (S K K x)  ==  (((S K) K) x).

Rules
    A rule is "NAME v1 v2 .. vk -> <body>" where v_i are lowercase
    variables and NAME is an uppercase atom.  The body is a term over
    {v_i, NAME (self-ref allowed), other atoms}.
    Built-in rules loaded by default: I, K, S, B, C, W, M, T, V, D, P1, P2, Y.
    Primitives with non-ASCII names (Π₁, Π₂) are aliased to P1, P2 for
    CLI convenience.

Reduction strategy
    Leftmost-outermost weak-head: reduce the spine's head combinator when
    it has enough arguments.  Do not reduce inside an unapplied combinator.
    This matches the standard combinatory-calculus semantics and is what
    A-ARGUMENT.md and B-ARGUMENT.md both rely on.

CLI
    --selftest                 Run the built-in test battery.
    --trace "<term>"           Print each reduction step of <term>.
    --reduce "<term>"          Print only the normal form.
    --max-depth N              Reduction-step cap (default 1000).
    --rule "<NAME v1 v2 -> body>"   Add/override a rule (repeatable).
    --no-builtins              Do not load built-in rules.

Exit codes
    0  normal form reached
    1  input / parse error
    2  stuck (no rule applies at head, not normal-form-clean)
    3  depth exceeded (likely divergent)
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from typing import Optional


# ---------- Term model ----------------------------------------------------


@dataclass(frozen=True)
class Atom:
    name: str

    def __repr__(self) -> str:  # pragma: no cover
        return self.name


@dataclass(frozen=True)
class App:
    f: "Term"
    x: "Term"

    def __repr__(self) -> str:  # pragma: no cover
        return f"({self.f} {self.x})"


Term = object  # Atom | App


def is_var(a: Atom) -> bool:
    return a.name and a.name[0].islower()


def fmt(t: Term) -> str:
    """Pretty-print a term (minimal-paren, left-assoc)."""
    if isinstance(t, Atom):
        return t.name
    # spine
    head, args = spine(t)
    inner = " ".join([fmt(head)] + [fmt_arg(a) for a in args])
    return f"({inner})"


def fmt_arg(t: Term) -> str:
    if isinstance(t, Atom):
        return t.name
    return fmt(t)


def spine(t: Term) -> tuple[Term, list[Term]]:
    """Left-associative spine: (h, [a1, a2, ...]) for t = h a1 a2 ..."""
    args: list[Term] = []
    cur = t
    while isinstance(cur, App):
        args.append(cur.x)
        cur = cur.f
    args.reverse()
    return cur, args


def rebuild(head: Term, args: list[Term]) -> Term:
    out: Term = head
    for a in args:
        out = App(out, a)
    return out


# ---------- Parser --------------------------------------------------------


def tokenize(s: str) -> list[str]:
    out: list[str] = []
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c.isspace():
            i += 1
            continue
        if c in "()":
            out.append(c)
            i += 1
            continue
        # gather an atom: run of non-whitespace non-paren non-arrow
        j = i
        while j < n and not s[j].isspace() and s[j] not in "()":
            # "->" and "→" are delimiters
            if s[j : j + 2] == "->" or s[j] == "→":
                break
            j += 1
        if j == i:
            raise ValueError(f"unexpected char at {i}: {c!r}")
        out.append(s[i:j])
        i = j
    return out


def parse_term(tokens: list[str], pos: int) -> tuple[Term, int]:
    if pos >= len(tokens):
        raise ValueError("unexpected end of input")
    tok = tokens[pos]
    if tok == "(":
        pos += 1
        items: list[Term] = []
        while pos < len(tokens) and tokens[pos] != ")":
            sub, pos = parse_term(tokens, pos)
            items.append(sub)
        if pos >= len(tokens):
            raise ValueError("unclosed paren")
        if not items:
            raise ValueError("empty parens")
        pos += 1  # consume ")"
        # left-associative fold
        out: Term = items[0]
        for it in items[1:]:
            out = App(out, it)
        return out, pos
    if tok == ")":
        raise ValueError("unexpected )")
    return Atom(tok), pos + 1


def parse(src: str) -> Term:
    toks = tokenize(src)
    if not toks:
        raise ValueError("empty term")
    t, pos = parse_term(toks, 0)
    if pos != len(toks):
        raise ValueError(f"trailing tokens at {pos}: {toks[pos:]}")
    return t


# ---------- Rules ---------------------------------------------------------


@dataclass(frozen=True)
class Rule:
    name: str
    params: tuple[str, ...]  # lowercase variable names
    body: Term

    @property
    def arity(self) -> int:
        return len(self.params)


def parse_rule(src: str) -> Rule:
    # "NAME v1 v2 .. -> body"  or  "NAME v1 .. → body"
    if "->" in src:
        lhs, rhs = src.split("->", 1)
    elif "→" in src:
        lhs, rhs = src.split("→", 1)
    else:
        raise ValueError(f"rule missing '->': {src!r}")
    lhs_toks = lhs.split()
    if not lhs_toks:
        raise ValueError("rule LHS empty")
    name = lhs_toks[0]
    if not name[0].isupper():
        raise ValueError(f"rule name must be uppercase atom: {name}")
    params = tuple(lhs_toks[1:])
    for p in params:
        if not (p and p[0].islower()):
            raise ValueError(f"rule parameter must be lowercase: {p}")
    body = parse(rhs.strip())
    return Rule(name=name, params=params, body=body)


BUILTINS = [
    "I x -> x",
    "K x y -> x",
    "S x y z -> (x z (y z))",
    "B x y z -> (x (y z))",
    "C x y z -> (x z y)",
    "W x y -> (x y y)",
    "M x -> (x x)",
    "T x y -> (y x)",
    "V x y z -> (z x y)",
    "D x y z w -> (x y (z w))",
    "P1 x y -> x",
    "P2 x y -> y",
    "Y f -> (f (Y f))",
]


def builtin_rules() -> dict[str, Rule]:
    out: dict[str, Rule] = {}
    for src in BUILTINS:
        r = parse_rule(src)
        out[r.name] = r
    return out


# ---------- Substitution ---------------------------------------------------


def subst(body: Term, env: dict[str, Term]) -> Term:
    if isinstance(body, Atom):
        return env.get(body.name, body)
    return App(subst(body.f, env), subst(body.x, env))


# ---------- Reduction -----------------------------------------------------


def try_reduce_head(t: Term, rules: dict[str, Rule]) -> Optional[Term]:
    """If the head of t is a redex, return the one-step reduct; else None."""
    head, args = spine(t)
    if not isinstance(head, Atom):
        return None
    rule = rules.get(head.name)
    if rule is None:
        return None
    if len(args) < rule.arity:
        return None
    consumed = args[: rule.arity]
    remaining = args[rule.arity :]
    env = {p: consumed[i] for i, p in enumerate(rule.params)}
    reduced = subst(rule.body, env)
    return rebuild(reduced, remaining)


def one_step(t: Term, rules: dict[str, Rule]) -> Optional[Term]:
    """Leftmost-outermost one-step reduction; None if t is in normal form.

    Order: (i) try reducing the head-redex of t if any; (ii) else recurse
    into t.f then t.x (the function side is "more outer" in left-assoc).
    """
    r = try_reduce_head(t, rules)
    if r is not None:
        return r
    if not isinstance(t, App):
        return None
    r_f = one_step(t.f, rules)
    if r_f is not None:
        return App(r_f, t.x)
    r_x = one_step(t.x, rules)
    if r_x is not None:
        return App(t.f, r_x)
    return None


def reduce_trace(t: Term, rules: dict[str, Rule], max_depth: int) -> tuple[str, list[Term]]:
    """Return (status, trace). status in {"normal","divergent"}."""
    trace: list[Term] = [t]
    cur = t
    for _ in range(max_depth):
        nxt = one_step(cur, rules)
        if nxt is None:
            return "normal", trace
        cur = nxt
        trace.append(cur)
    return "divergent", trace


# ---------- CLI ------------------------------------------------------------


def cmd_trace(args, rules: dict[str, Rule]) -> int:
    try:
        t = parse(args.trace)
    except ValueError as e:
        print(f"parse error: {e}", file=sys.stderr)
        return 1
    status, tr = reduce_trace(t, rules, args.max_depth)
    for i, s in enumerate(tr):
        print(f"[{i}] {fmt(s)}")
    print(f"status: {status}  steps: {len(tr) - 1}")
    return {"normal": 0, "stuck": 2, "divergent": 3}[status]


def cmd_reduce(args, rules: dict[str, Rule]) -> int:
    try:
        t = parse(args.reduce)
    except ValueError as e:
        print(f"parse error: {e}", file=sys.stderr)
        return 1
    status, tr = reduce_trace(t, rules, args.max_depth)
    print(fmt(tr[-1]))
    print(f"# status: {status}  steps: {len(tr) - 1}", file=sys.stderr)
    return {"normal": 0, "stuck": 2, "divergent": 3}[status]


# ---------- Self-test -----------------------------------------------------


SELFTESTS = [
    # (description, term, expected-normal-form, status)
    ("I x reduces to x", "(I a)", "a", "normal"),
    ("K x y reduces to x", "(K a b)", "a", "normal"),
    ("S x y z reduces to x z (y z)", "(S a b c)", "(a c (b c))", "normal"),
    ("I via SKK: (S K K) x = x", "(S K K x)", "x", "normal"),
    ("M via SII: (S I I) x = x x", "(S I I x)", "(x x)", "normal"),
    ("W via SS(SK): (S S (S K)) x y = x y y", "(S S (S K) x y)", "(x y y)", "normal"),
    ("W via SS(KI): (S S (K I)) x y = x y y", "(S S (K I) x y)", "(x y y)", "normal"),
    ("B via S(KS)K: (S (K S) K) x y z = x (y z)", "(S (K S) K x y z)", "(x (y z))", "normal"),
    ("C via S(BBS)(KK): (S (B B S) (K K)) x y z = x z y", "(S (B B S) (K K) x y z)", "(x z y)", "normal"),
    ("D via BB: (B B) x y z w = x y (z w)", "(B B x y z w)", "(x y (z w))", "normal"),
    ("T via CI: (C I) x y = y x", "(C I x y)", "(y x)", "normal"),
    ("V via BC(CI): (B C (C I)) x y z = z x y", "(B C (C I) x y z)", "(z x y)", "normal"),
    ("Pi1 = K directly", "(P1 a b)", "a", "normal"),
    ("Pi2 = K I directly", "(P2 a b)", "b", "normal"),
    # divergence test: omega-omega using I=SKK, M = SII
    ("omega-omega: (SII)(SII) diverges", "(S I I (S I I))", None, "divergent"),
]


def cmd_selftest(args, rules: dict[str, Rule]) -> int:
    passed = 0
    failed = 0
    for desc, src, expected, expected_status in SELFTESTS:
        try:
            t = parse(src)
        except ValueError as e:
            print(f"FAIL parse {desc!r}: {e}")
            failed += 1
            continue
        status, tr = reduce_trace(t, rules, args.max_depth)
        got = fmt(tr[-1])
        if status != expected_status:
            print(f"FAIL [{desc}] status={status}  got={got}  expected_status={expected_status}")
            failed += 1
            continue
        if expected is not None:
            exp_t = parse(expected)
            if fmt(exp_t) != got:
                print(f"FAIL [{desc}]  got={got}  expected={fmt(exp_t)}")
                failed += 1
                continue
        print(f"pass [{desc}]  -> {got} ({status}, {len(tr)-1} steps)")
        passed += 1
    total = passed + failed
    print(f"\nSelf-test: {passed}/{total} passed")
    return 0 if failed == 0 else 2


# ---------- Main -----------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description="Combinator β-reducer (weak-head, leftmost-outermost).")
    ap.add_argument("--selftest", action="store_true", help="Run built-in tests.")
    ap.add_argument("--trace", metavar="TERM", help="Trace reduction of TERM.")
    ap.add_argument("--reduce", metavar="TERM", help="Reduce TERM; print normal form only.")
    ap.add_argument("--max-depth", type=int, default=1000, help="Step cap (default 1000).")
    ap.add_argument("--rule", action="append", default=[], help="Add/override rule: 'NAME v1 v2 -> body'")
    ap.add_argument("--no-builtins", action="store_true", help="Do not load built-in rules.")
    args = ap.parse_args()

    rules: dict[str, Rule] = {} if args.no_builtins else builtin_rules()
    for r_src in args.rule:
        try:
            r = parse_rule(r_src)
        except ValueError as e:
            print(f"rule parse error: {e}", file=sys.stderr)
            return 1
        rules[r.name] = r

    actions = [args.selftest, bool(args.trace), bool(args.reduce)]
    if sum(actions) != 1:
        ap.error("exactly one of --selftest / --trace / --reduce required")

    if args.selftest:
        return cmd_selftest(args, rules)
    if args.trace:
        return cmd_trace(args, rules)
    return cmd_reduce(args, rules)


if __name__ == "__main__":
    raise SystemExit(main())
