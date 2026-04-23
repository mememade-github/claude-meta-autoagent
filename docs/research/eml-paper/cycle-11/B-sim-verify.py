"""Numeric oracle for ARGUMENT.md §5.

Expresses every primitive in the §5 table using ONLY the basis operations
{+, exp, ln, -1} via the derived-toolkit macros, and compares against
numpy reference implementations at pseudo-random complex sample points.
"""

import numpy as np
import sys

SEED = 42
N_SAMPLES = 20
REL_TOL = 1e-8
ABS_TOL = 1e-10

# -----------------------------------------------------------------------
# Basis (the only four elements).
# -----------------------------------------------------------------------

def BASIS_ADD(a, b):
    return a + b

def BASIS_EXP(z):
    return np.exp(z)

def BASIS_LN(z):
    # numpy's log is principal branch: Im(log z) in (-pi, pi].
    return np.log(z)

BASIS_NEG1 = -1 + 0j

# -----------------------------------------------------------------------
# Derived toolkit -- each macro uses ONLY the basis operations above.
# -----------------------------------------------------------------------

def NEG(a):
    # -a = exp(ln(-1) + ln(a))
    return BASIS_EXP(BASIS_ADD(BASIS_LN(BASIS_NEG1), BASIS_LN(a)))

def MUL(a, b):
    # a*b = exp(ln a + ln b)
    return BASIS_EXP(BASIS_ADD(BASIS_LN(a), BASIS_LN(b)))

def RECIP(a):
    # 1/a = exp(-ln a)
    return BASIS_EXP(NEG(BASIS_LN(a)))

def DIV(a, b):
    # a/b = a * (1/b)
    return MUL(a, RECIP(b))

def SUB(a, b):
    # a - b = a + (-b)
    return BASIS_ADD(a, NEG(b))

# Constants in the basis.
C_ONE = MUL(BASIS_NEG1, BASIS_NEG1)          # 1 = (-1)(-1)
C_TWO = BASIS_ADD(C_ONE, C_ONE)              # 2 = 1+1
C_HALF = RECIP(C_TWO)                        # 1/2 = exp(-ln 2)
C_I = BASIS_EXP(MUL(C_HALF, BASIS_LN(BASIS_NEG1)))  # i = exp((1/2) ln(-1))
C_PI = MUL(NEG(C_I), BASIS_LN(BASIS_NEG1))   # pi = (-i)*ln(-1)
C_E = BASIS_EXP(C_ONE)                       # e = exp(1)

# -----------------------------------------------------------------------
# Primitive implementations in the basis (left column of §5 table).
# Each takes complex argument(s) and returns a complex value.
# -----------------------------------------------------------------------

# Constants -- expressed as zero-arg callables for uniform testing.
def prim_pi():  return C_PI
def prim_e():   return C_E
def prim_i():   return C_I
def prim_neg1():return BASIS_NEG1
def prim_one(): return C_ONE
def prim_two(): return C_TWO
def prim_half():return C_HALF

# Unary transcendental.
def prim_exp(x):    return BASIS_EXP(x)
def prim_ln(x):     return BASIS_LN(x)
def prim_sigmoid(x):
    # sigma(x) = 1/(1+exp(-x))
    return RECIP(BASIS_ADD(C_ONE, BASIS_EXP(NEG(x))))

# Unary algebraic.
def prim_recip(x):  return RECIP(x)
def prim_sqrt(x):   return BASIS_EXP(MUL(C_HALF, BASIS_LN(x)))
def prim_sq(x):     return BASIS_EXP(MUL(C_TWO, BASIS_LN(x)))
def prim_neg(x):    return MUL(BASIS_NEG1, x)
def prim_halve(x):  return BASIS_EXP(SUB(BASIS_LN(x), BASIS_LN(C_TWO)))

# Trig via Euler.
def prim_sin(x):
    # (e^{ix} - e^{-ix}) / (2i)
    ix = MUL(C_I, x)
    num = SUB(BASIS_EXP(ix), BASIS_EXP(NEG(ix)))
    return DIV(num, MUL(C_TWO, C_I))

def prim_cos(x):
    ix = MUL(C_I, x)
    num = BASIS_ADD(BASIS_EXP(ix), BASIS_EXP(NEG(ix)))
    return MUL(C_HALF, num)

def prim_tan(x):
    return DIV(prim_sin(x), prim_cos(x))

# Inverse trig via log forms.
def prim_arcsin(x):
    # -i * ln(ix + sqrt(1 - x^2))
    one_minus_x2 = SUB(C_ONE, prim_sq(x))
    inside = BASIS_ADD(MUL(C_I, x), prim_sqrt(one_minus_x2))
    return MUL(NEG(C_I), BASIS_LN(inside))

def prim_arccos(x):
    # pi/2 - arcsin x
    return SUB(MUL(C_HALF, C_PI), prim_arcsin(x))

def prim_arctan(x):
    # (1/(2i)) * ln((1+ix)/(1-ix))
    ix = MUL(C_I, x)
    top = BASIS_ADD(C_ONE, ix)
    bot = SUB(C_ONE, ix)
    return MUL(RECIP(MUL(C_TWO, C_I)), BASIS_LN(DIV(top, bot)))

# Hyperbolic.
def prim_sinh(x):
    return MUL(C_HALF, SUB(BASIS_EXP(x), BASIS_EXP(NEG(x))))

def prim_cosh(x):
    return MUL(C_HALF, BASIS_ADD(BASIS_EXP(x), BASIS_EXP(NEG(x))))

def prim_tanh(x):
    return DIV(prim_sinh(x), prim_cosh(x))

# Inverse hyperbolic.
def prim_arsinh(x):
    # ln(x + sqrt(x^2 + 1))
    return BASIS_LN(BASIS_ADD(x, prim_sqrt(BASIS_ADD(prim_sq(x), C_ONE))))

def prim_arcosh(x):
    # ln(x + sqrt(x^2 - 1))
    return BASIS_LN(BASIS_ADD(x, prim_sqrt(SUB(prim_sq(x), C_ONE))))

def prim_artanh(x):
    # (1/2) ln((1+x)/(1-x))
    return MUL(C_HALF, BASIS_LN(DIV(BASIS_ADD(C_ONE, x), SUB(C_ONE, x))))

# Binary.
def prim_add(x, y): return BASIS_ADD(x, y)
def prim_sub(x, y): return SUB(x, y)
def prim_mul(x, y): return MUL(x, y)
def prim_div(x, y): return DIV(x, y)

def prim_logx(x, y):
    # log_x(y) = ln y / ln x
    return DIV(BASIS_LN(y), BASIS_LN(x))

def prim_pow(x, y):
    # x^y = exp(y * ln x)
    return BASIS_EXP(MUL(y, BASIS_LN(x)))

def prim_mean(x, y):
    # (x+y)/2 = (x+y) * exp(-ln 2)
    return MUL(BASIS_ADD(x, y), BASIS_EXP(NEG(BASIS_LN(C_TWO))))

def prim_hypot(x, y):
    # sqrt(x^2 + y^2) = exp((1/2) ln(exp(2 ln x) + exp(2 ln y)))
    return BASIS_EXP(MUL(C_HALF,
        BASIS_LN(BASIS_ADD(prim_sq(x), prim_sq(y)))))

# -----------------------------------------------------------------------
# Sample-domain generators.  Return arrays of complex sample points.
# -----------------------------------------------------------------------

def annulus(rng, n, r_lo=0.5, r_hi=2.0):
    r = rng.uniform(r_lo, r_hi, n)
    theta = rng.uniform(-np.pi + 0.1, np.pi - 0.1, n)  # avoid the cut edge
    return r * np.exp(1j * theta)

def small_disk(rng, n, r_max=0.9):
    r = rng.uniform(0.05, r_max, n)
    theta = rng.uniform(-np.pi, np.pi, n)
    return r * np.exp(1j * theta)

def real_pos_ge_one(rng, n, lo=1.1, hi=3.0):
    return rng.uniform(lo, hi, n).astype(complex)

def real_pos(rng, n, lo=0.5, hi=2.5):
    return rng.uniform(lo, hi, n).astype(complex)

def general_complex(rng, n, r_lo=0.5, r_hi=2.0):
    return annulus(rng, n, r_lo, r_hi)

# -----------------------------------------------------------------------
# Test driver.
# -----------------------------------------------------------------------

def compare(name, got, ref):
    got = np.asarray(got, dtype=complex)
    ref = np.asarray(ref, dtype=complex)
    abs_err = np.abs(got - ref)
    # relative error guarded against |ref| ~ 0
    denom = np.maximum(np.abs(ref), 1.0)
    rel_err = abs_err / denom
    max_abs = float(np.max(abs_err))
    max_rel = float(np.max(rel_err))
    ok = (max_rel < REL_TOL) or (max_abs < ABS_TOL)
    return ok, max_abs, max_rel

def run_unary(name, basis_fn, ref_fn, samples):
    got = np.array([basis_fn(x) for x in samples], dtype=complex)
    ref = ref_fn(samples)
    return compare(name, got, ref)

def run_binary(name, basis_fn, ref_fn, xs, ys):
    got = np.array([basis_fn(x, y) for x, y in zip(xs, ys)], dtype=complex)
    ref = ref_fn(xs, ys)
    return compare(name, got, ref)

def run_const(name, basis_val, ref_val):
    got = complex(basis_val)
    ref = complex(ref_val)
    abs_err = abs(got - ref)
    denom = max(abs(ref), 1.0)
    rel_err = abs_err / denom
    ok = (rel_err < REL_TOL) or (abs_err < ABS_TOL)
    return ok, abs_err, rel_err


def main():
    rng = np.random.default_rng(SEED)
    results = []  # (name, ok, max_abs, max_rel)

    # --- constants ---
    results.append(("pi",   *run_const("pi",   prim_pi(),   np.pi + 0j)))
    results.append(("e",    *run_const("e",    prim_e(),    np.e + 0j)))
    results.append(("i",    *run_const("i",    prim_i(),    1j)))
    results.append(("-1",   *run_const("-1",   prim_neg1(), -1 + 0j)))
    results.append(("1",    *run_const("1",    prim_one(),  1 + 0j)))
    results.append(("2",    *run_const("2",    prim_two(),  2 + 0j)))
    results.append(("1/2",  *run_const("1/2",  prim_half(), 0.5 + 0j)))

    # --- unary transcendental ---
    s = annulus(rng, N_SAMPLES)
    results.append(("exp(x)",     *run_unary("exp(x)",     prim_exp,     np.exp, s)))
    results.append(("ln(x)",      *run_unary("ln(x)",      prim_ln,      np.log, s)))
    # sigmoid: avoid x where 1+exp(-x) ~ 0 (needs exp(-x) ~ -1, i.e. x ~ i*pi);
    # stay in a moderate-magnitude box.
    s_sig = annulus(rng, N_SAMPLES, 0.5, 2.0)
    results.append(("sigmoid(x)", *run_unary("sigmoid(x)", prim_sigmoid,
                                             lambda z: 1.0/(1.0 + np.exp(-z)), s_sig)))

    # --- unary algebraic ---
    s_nz = annulus(rng, N_SAMPLES)                          # avoid 0 for reciprocal/ln
    results.append(("1/x",    *run_unary("1/x",    prim_recip, lambda z: 1.0/z, s_nz)))
    results.append(("sqrt(x)",*run_unary("sqrt(x)",prim_sqrt,  np.sqrt, s_nz)))
    results.append(("x^2",    *run_unary("x^2",    prim_sq,    lambda z: z*z, s_nz)))
    results.append(("-x",     *run_unary("-x",     prim_neg,   lambda z: -z, s_nz)))
    results.append(("x/2",    *run_unary("x/2",    prim_halve, lambda z: z/2.0, s_nz)))

    # --- trig ---
    s_trig = annulus(rng, N_SAMPLES, 0.3, 1.5)
    results.append(("sin(x)", *run_unary("sin(x)", prim_sin, np.sin, s_trig)))
    results.append(("cos(x)", *run_unary("cos(x)", prim_cos, np.cos, s_trig)))
    # tan: avoid zeros of cos; stay away from pi/2.  Our domain |x|<=1.5 is safe.
    results.append(("tan(x)", *run_unary("tan(x)", prim_tan, np.tan, s_trig)))

    # --- inverse trig: keep on principal branch ---
    # arcsin / arccos: |x| <= 0.9 (complex points inside disk of radius 0.9).
    s_as = small_disk(rng, N_SAMPLES, r_max=0.9)
    results.append(("arcsin(x)", *run_unary("arcsin(x)", prim_arcsin, np.arcsin, s_as)))
    results.append(("arccos(x)", *run_unary("arccos(x)", prim_arccos, np.arccos, s_as)))
    # arctan: avoid |x|=1 on the imaginary axis; small disk is safe.
    s_at = small_disk(rng, N_SAMPLES, r_max=0.9)
    results.append(("arctan(x)", *run_unary("arctan(x)", prim_arctan, np.arctan, s_at)))

    # --- hyperbolic ---
    s_h = annulus(rng, N_SAMPLES, 0.3, 1.5)
    results.append(("sinh(x)", *run_unary("sinh(x)", prim_sinh, np.sinh, s_h)))
    results.append(("cosh(x)", *run_unary("cosh(x)", prim_cosh, np.cosh, s_h)))
    results.append(("tanh(x)", *run_unary("tanh(x)", prim_tanh, np.tanh, s_h)))

    # --- inverse hyperbolic ---
    # arsinh: branch cuts on imaginary axis |Im z| > 1.  Disk r<=0.9 is safe.
    s_arsinh = small_disk(rng, N_SAMPLES, r_max=0.9)
    results.append(("arsinh(x)", *run_unary("arsinh(x)", prim_arsinh, np.arcsinh, s_arsinh)))
    # arcosh: principal domain x >= 1 on real line.
    s_arcosh = real_pos_ge_one(rng, N_SAMPLES, 1.1, 3.0)
    results.append(("arcosh(x)", *run_unary("arcosh(x)", prim_arcosh, np.arccosh, s_arcosh)))
    # artanh: |x| < 1.  Small disk r<=0.9.
    s_artanh = small_disk(rng, N_SAMPLES, r_max=0.9)
    results.append(("artanh(x)", *run_unary("artanh(x)", prim_artanh, np.arctanh, s_artanh)))

    # --- binary ---
    xs = annulus(rng, N_SAMPLES)
    ys = annulus(rng, N_SAMPLES)
    results.append(("x+y", *run_binary("x+y", prim_add, lambda a,b: a+b, xs, ys)))
    results.append(("x-y", *run_binary("x-y", prim_sub, lambda a,b: a-b, xs, ys)))
    results.append(("x*y", *run_binary("x*y", prim_mul, lambda a,b: a*b, xs, ys)))
    results.append(("x/y", *run_binary("x/y", prim_div, lambda a,b: a/b, xs, ys)))

    # log_x(y): need ln x and ln y, both nonzero, and x != 1.  Use positive-real
    # bases away from 1 and positive-real args to avoid branch ambiguity vs numpy.
    xs_lb = real_pos(rng, N_SAMPLES, 1.5, 3.0)   # base > 1
    ys_lb = real_pos(rng, N_SAMPLES, 0.5, 3.0)
    results.append(("log_x(y)", *run_binary("log_x(y)", prim_logx,
        lambda a, b: np.log(b) / np.log(a), xs_lb, ys_lb)))

    # pow(x,y) = exp(y ln x).  For arbitrary complex x,y use positive-real base
    # so principal branch matches numpy's np.power on that domain unambiguously.
    xs_pw = real_pos(rng, N_SAMPLES, 0.5, 2.5)
    ys_pw = annulus(rng, N_SAMPLES, 0.3, 1.5)
    results.append(("pow(x,y)", *run_binary("pow(x,y)", prim_pow,
        lambda a, b: np.power(a, b), xs_pw, ys_pw)))

    # mean, hypot
    xs_m = annulus(rng, N_SAMPLES)
    ys_m = annulus(rng, N_SAMPLES)
    results.append(("(x+y)/2", *run_binary("(x+y)/2", prim_mean,
        lambda a, b: (a + b) / 2.0, xs_m, ys_m)))

    # hypot via §5 formula uses ln on x^2+y^2 and on x,y, so x,y != 0 and x^2+y^2 != 0.
    # Annulus samples avoid 0; random pairs almost surely avoid x^2+y^2 = 0.
    # Use positive real x,y to keep principal branch clean against np.sqrt(x^2+y^2).
    xs_h = real_pos(rng, N_SAMPLES, 0.5, 2.5)
    ys_h = real_pos(rng, N_SAMPLES, 0.5, 2.5)
    results.append(("sqrt(x^2+y^2)", *run_binary("sqrt(x^2+y^2)", prim_hypot,
        lambda a, b: np.sqrt(a*a + b*b), xs_h, ys_h)))

    # --- Report ---
    name_w = max(len(r[0]) for r in results)
    n_pass = 0
    for name, ok, mabs, mrel in results:
        status = "PASS" if ok else "FAIL"
        if ok:
            n_pass += 1
        print(f"{name.ljust(name_w)}  {status}   max_abs_err={mabs:.3e}   max_rel_err={mrel:.3e}")

    print()
    print(f"SUMMARY: {n_pass} / {len(results)} primitives PASS")

    return 0 if n_pass == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
