# Minimal Instruction Set for a Universal Register Machine

## Preliminaries and counting convention

Fix the baseline 11-instruction set B = {LOAD, COPY, ADD, SUB, ZERO,
INC, DEC, JMP, JZ, JNZ, HALT} defined by the problem. Registers R0,
R1, R2, … hold non-negative integers of unbounded precision. A
program is a finite sequence of labelled instructions; every label
in the program names a position inside the sequence.

Before anything else, I commit to an explicit **counting
convention**, because the final "number" of primitives depends on
what we count:

* An **instruction** is an operation type. CJDECINC with four
  operand slots is one instruction, just as JZ with two operand
  slots (a register and a label) is one instruction in B.
* **Labels** are syntactic position markers in the program text,
  not primitives. Writing `L:` before an instruction is
  punctuation, not an executed operation.
* **Jump targets** are operands, not primitives. A target is a
  label name appearing in an instruction.
* **Registers** are an unbounded resource, not a primitive. Any
  program mentions finitely many of them.
* **Halting** can be modelled in two ways. Convention H1: running
  off the end of the program halts the machine, so an explicit HALT
  instruction is syntactic sugar for "jump to a label just past the
  last instruction". Convention H2: HALT is an irreducible
  primitive.

Under H1, the minimum I reach is a single-instruction set T with
|T| = 1. Under H2, the minimum is |T| = 2. I argue both below and
mark the relevant passages; unless otherwise stated, the default
convention is H1.

I also rely on the following structural fact, which is part of the
ordinary definition of a register machine and not a separate
theorem: non-input registers begin at 0, and any register that is
never syntactically written by the program retains its initial
value throughout execution. This lets me reserve a register `R_0`
as a syntactically-invariant zero. `R_0` is not a primitive; it is
a register, and registers are free.

---

## 1. Motivation

### 1.1 Why expect a large reduction at all?

Across unrelated algebraic and computational systems, we repeatedly
see a gap between the set of operations users find *convenient* and
the set required to *generate* the same behaviour. The 11-baseline
is a convenience set, curated for programmer comfort; universality
only demands a generating set. Four concrete precedents I can
reason about from scratch:

**Propositional logic.** There are 16 binary Boolean connectives,
plus NOT. A common complete basis is {AND, OR, NOT}. One can check
directly that {AND, NOT} is already complete: OR(x, y) =
NOT(AND(NOT x, NOT y)). Going further, the binary connective
f(x, y) = NOT(AND(x, y)) is by itself complete: NOT(x) = f(x, x),
AND(x, y) = f(f(x, y), f(x, y)), and OR follows from De Morgan.
So a 17-symbol algebra collapses to one binary symbol. The
compression factor is not small — it is maximal.

**Combinatory logic.** The untyped λ-calculus has β-reduction as
its sole rewriting rule but infinitely many terms. There are
fixed closed terms, call them s and k, satisfying
s x y z = x z (y z) and k x y = x, such that every λ-term is
extensionally equal to a combination of s and k. Two constants
suffice for a notation that can encode any computable function.
With a touch more work a single combinator (defined so that
repeated self-application produces both s and k) suffices.

**Elementary local rules.** For 1D two-state cellular automata
with three-cell neighbourhoods there are 2^8 = 256 rules. The
overwhelming majority are trivial (constant, shift, or
eventually-periodic). But at least one rule is rich enough that
patterns evolving under it can simulate logic gates and unbounded
memory. Universality from a *single* local update rule.

**Algebraic generators.** A group of finite or infinite order is
often written with many named operations (product, inverse,
commutator, conjugation). All of these are derivable from a small
generating set; a presentation `<gens | relations>` usually has far
fewer generators than the group has "natural" operations.

The common pattern: operational richness hides algebraic
redundancy. Once we distinguish "primitive" from "syntactic sugar"
by an explicit synthesis test, the primitive set is much smaller
than the convenience set.

### 1.2 What structure of B specifically invites reduction?

Sort the 11 baseline instructions by their obvious role:

| Role | Instructions |
|---|---|
| Constant injection | LOAD |
| Data movement | COPY |
| Compound arithmetic | ADD, SUB |
| Bulk reset | ZERO |
| Primitive arithmetic | INC, DEC |
| Control flow | JMP, JZ, JNZ |
| Termination | HALT |

Inspection already suggests a lot of mutual definability:

* LOAD k ≈ "ZERO then k increments".
* COPY ≈ "ZERO then ADD".
* ADD and SUB ≈ loops whose bodies use INC, DEC, and a jump-on-zero
  test.
* ZERO ≈ "loop DEC until zero".
* JMP ≈ "JZ on a register known to be zero".
* JNZ ≈ "JZ, then JMP, with the landings swapped".
* HALT ≈ "jump past the last instruction" (under H1).

Only three instruction *roles* look genuinely irreducible:

1. Some way to **increase** register values (otherwise the program
   cannot produce a value larger than the largest input, ruling out
   almost every recursive function).
2. Some way to **decrease** register values (otherwise loops
   cannot measure progress against a counter and cannot terminate
   on arbitrary input data).
3. Some way to **branch on a register's value** (otherwise the
   function is total and its runtime depends only on program
   length, so partial recursive functions with genuinely
   non-halting behaviour are unreachable).

The natural question is whether those three roles can be fused
into one instruction. They can; §4 gives the fusion. I do not
expect to drop below one instruction: zero instructions is no
computation at all.

### 1.3 What might block reduction below one?

The feature that makes register-machine reduction harder than a
pure algebra is **asymmetry of ℕ**: registers cannot go negative,
so decrement alone cannot construct new values. A one-instruction
reduction must preserve an "increase" capability even at the
all-zero initial state. This rules out "subtract two registers
and branch" as a sole primitive over ℕ — it can never raise any
register's value. Our fused primitive must contain, somewhere in
its body, a path that increments a register.

---

## 2. The reduction procedure

### 2.1 Statement

Let B be a baseline instruction set presumed universal. I want to
show a subset (or fused variant) T ⊆ B* is also universal. The
method I apply throughout:

**Procedure SYNTHESIZE(I, T)**. For each instruction I ∈ B \ T,
exhibit a finite program M_I over T that, starting from any
register state σ and ending at a designated exit label, yields
the same effect on σ as I, up to a declared set of scratch
registers (whose final contents are don't-care).

M_I is allowed to:

* use labels that are fresh (distinct from all other labels in the
  eventual composed program);
* use a finite number of scratch registers disjoint from the
  caller's live registers;
* assume the existence of a syntactically-invariant register
  `R_0` that is never written by any instruction anywhere in the
  program.

M_I must:

* preserve every caller-visible register except those that I
  itself modifies;
* behave correctly on every value of the input registers,
  including the corner cases 0 and large inputs;
* terminate in finite time whenever I would (and loop forever
  whenever I's composite behaviour in a surrounding program
  requires it — this is automatic because M_I is a macro
  expansion, not a decision procedure).

### 2.2 Why this works modularly

A baseline program P compiles to a T-program T(P) by replacing each
baseline instruction with its macro, α-renaming scratches and
labels to avoid clashes across macro instances. The resulting
program:

* has size O(|P|) times the largest macro;
* uses O(|P|) extra labels and O(|P|) extra scratches (since
  macros may be statically distinguished per textual occurrence
  of the instruction, not per dynamic execution);
* executes the same trace as P, observed on the non-scratch
  registers.

That gives the slogan **"T simulates B instruction-by-instruction,
hence T is as universal as B"**. I discharge it in §5 after the
concrete reductions.

### 2.3 Generality

The procedure is not specific to register machines. It is just the
"macro-expansion" reduction used in any programming formalism where
we can substitute a phrase for a symbol without affecting the
semantics of surrounding phrases. It applies equally to stack
machines, Turing-style rewriting systems, and string-rewriting
calculi, given a suitable notion of "scratch" resource.

---

## 3. Progressive reduction

I chain macro expansions through a sequence of intermediate
stopping points T_0 ⊇ T_1 ⊇ … ⊇ T_10. At each stage I name the
instruction eliminated and its synthesis. I write pseudo-assembly
using labels `A:`, `B:`, and so on; `next` means the instruction
textually following the macro's final line.

### Stage 0. Baseline
T_0 = {LOAD, COPY, ADD, SUB, ZERO, INC, DEC, JMP, JZ, JNZ, HALT}.

### Stage 1. Eliminate LOAD.
**Synthesis of `LOAD k into Ri`:**
```
    ZERO Ri
    INC Ri          ; repeated k times
    ...
```
The constant `k` is a syntactic parameter of the baseline
instruction, so "unrolling it" is a compile-time transformation;
the resulting program has length 1 + k.

T_1 = {COPY, ADD, SUB, ZERO, INC, DEC, JMP, JZ, JNZ, HALT}.

### Stage 2. Eliminate COPY.
**Synthesis of `COPY Rj into Ri`:**
```
    ZERO Ri
    ADD Rj into Ri
```
`ADD` preserves Rj, so this preserves Rj as required by the
COPY specification.

T_2 = {ADD, SUB, ZERO, INC, DEC, JMP, JZ, JNZ, HALT}.

### Stage 3. Eliminate ZERO.
**Synthesis of `ZERO Ri`:**
```
A:  JZ Ri, B
    DEC Ri
    JMP A
B:  ; next
```
If Ri = 0 we jump straight to B. Otherwise DEC drops Ri by 1 and
JMP loops. Termination: Ri strictly decreases each iteration, so
it hits 0 in at most Ri_initial iterations.

T_3 = {ADD, SUB, INC, DEC, JMP, JZ, JNZ, HALT}.

### Stage 4. Eliminate ADD.
**Synthesis of `ADD Rj into Ri` using scratch Rt:**
```
    ZERO Rt            ; synthesised as Stage 3
A1: JZ Rj, A2
    DEC Rj
    INC Ri
    INC Rt
    JMP A1
A2: JZ Rt, A3
    DEC Rt
    INC Rj
    JMP A2
A3: ; next
```
Phase A1 simultaneously moves Rj into Ri and copies it into Rt.
When Rj hits 0, Rt holds the original value of Rj and Ri holds
the original Ri plus the original Rj. Phase A2 moves Rt back into
Rj, zeroing Rt and restoring Rj. Net effect: Ri ← Ri + Rj, Rj
unchanged, Rt ends at 0.

T_4 = {SUB, INC, DEC, JMP, JZ, JNZ, HALT}.

### Stage 5. Eliminate SUB.
**Synthesis of `SUB Rj from Ri` using scratch Rt:**
```
    ZERO Rt
S1: JZ Rj, S2
    DEC Rj
    DEC Ri             ; floor at 0 by DEC's definition
    INC Rt
    JMP S1
S2: JZ Rt, S3
    DEC Rt
    INC Rj
    JMP S2
S3: ; next
```
Same two-phase pattern. Ri is decremented once per unit of Rj,
capped at 0 by DEC's saturation semantics. Rj is then restored
from Rt. Net effect: Ri ← max(0, Ri − Rj), Rj unchanged.

T_5 = {INC, DEC, JMP, JZ, JNZ, HALT}.

### Stage 6. Eliminate JNZ.
**Synthesis of `JNZ Ri, L`:**
```
    JZ Ri, B
    JMP L
B:  ; next
```
If Ri = 0, we jump to B (which is "fall through"). Otherwise JZ
falls through and JMP takes us to L. Net: jump to L iff Ri ≠ 0.

T_6 = {INC, DEC, JMP, JZ, HALT}.

### Stage 7. Eliminate JMP.
Reserve a specific register name, `R_0`, and impose the syntactic
restriction that no instruction anywhere in the program writes
`R_0`. In particular, INC and DEC are never applied to `R_0`, and
no ADD/SUB/etc. targets it (these have been eliminated, but the
restriction would cover them too). Because non-input registers
start at 0 and `R_0` is never written, `R_0` is identically 0
throughout execution.

**Synthesis of `JMP L`:**
```
    JZ R_0, L
```
JZ fires unconditionally, so this is an unconditional jump.

T_7 = {INC, DEC, JZ, HALT}.

### Stage 8. Fuse DEC and JZ into DJZ.
Introduce a single instruction:

> **DJZ Ri, L**: if Ri = 0, jump to L and leave Ri untouched; else
> set Ri := Ri − 1 and fall through to the next instruction.

**Synthesis of `DEC Ri`** from DJZ alone:
```
    DJZ Ri, B
B:  ; next
```
If Ri = 0, DJZ jumps straight to B, leaving Ri at 0 — which
matches `DEC`'s floor behaviour. If Ri > 0, DJZ decrements Ri by
1 and falls through to B.

**Synthesis of `JZ Ri, L`** from DJZ plus INC (already present):
```
    DJZ Ri, L
    INC Ri              ; reached only when Ri was > 0
    ; next
```
If Ri = 0, DJZ jumps to L without side effect. Otherwise Ri is
decremented, INC restores it, and control falls through. Net:
jump to L iff Ri = 0, with Ri unchanged either way.

T_8 = {INC, DJZ, HALT}.

### Stage 9. Eliminate HALT (under convention H1).
H1 says: running off the final instruction halts. Then HALT is
syntactic sugar for "jump to a label placed one slot past the
program's last instruction". Since we have JMP in T_5 and its
synthesis via a zero-test is already in T_8 (via DJZ on `R_0`),
HALT translates to `DJZ R_0, L_end` where `L_end` is the
end-of-program marker.

T_9 = {INC, DJZ}.

Under convention H2, skip this stage: HALT stays as a second
primitive, and the final T is one stage richer everywhere below.

### Stage 10. Fuse INC and DJZ into CJDECINC.
Introduce a single instruction:

> **CJDECINC Ri, Rj, L_zero, L_nonzero**:
> * if Ri = 0: set Rj := Rj + 1, then jump to L_zero;
> * if Ri > 0: set Ri := Ri − 1, then jump to L_nonzero.

This fuses the two remaining primitives: the "Ri = 0" arm
replicates INC on a second register, and the "Ri > 0" arm
replicates DJZ on the first.

**Synthesis of `INC Rj`** from CJDECINC, using `R_0`:
```
    CJDECINC R_0, Rj, B, B
B:  ; next
```
`R_0` is identically 0, so the "zero" arm always fires: Rj is
incremented and we jump to B. Setting both labels to the same
target makes the fall-through behaviour crisp, and the
"nonzero" arm is unreachable by the invariant on `R_0`.

**Synthesis of `DJZ Ri, L`** from CJDECINC, using a scratch Rg:
```
    CJDECINC Ri, Rg, L, B
B:  ; next
```
If Ri = 0: Rg is incremented (garbage) and we jump to L. This
matches DJZ's "jump to L, Ri unchanged" arm.
If Ri > 0: Ri is decremented and we jump to B. This matches
DJZ's "decrement and fall through" arm.

The side effect on Rg is benign: Rg is a fresh scratch per
textual DJZ occurrence, and the program never reads it. A
program with k different DJZ occurrences uses k different Rg
scratches; k is finite because the program is finite.

**Single-instruction target reached.**

T_10 = {CJDECINC}.

---

## 4. The minimal set T

### 4.1 Definition

Under convention H1 (§0), the minimal instruction set I reach is

> **T = {CJDECINC}** with |T| = 1.

**CJDECINC Ri, Rj, L_zero, L_nonzero**. Operands: two register
names `Ri`, `Rj`; two labels `L_zero`, `L_nonzero`. Semantics:

```
  if [[Ri]] == 0:
      [[Rj]] := [[Rj]] + 1
      PC    := position of L_zero
  else:
      [[Ri]] := [[Ri]] − 1
      PC    := position of L_nonzero
```

The semantics is total: every state dispatches to exactly one arm.

Under convention H2, the minimum is **T = {CJDECINC, HALT}** with
|T| = 2; the HALT instruction simply stops the machine when
executed.

### 4.2 What counts and what does not

Per §0:

* **Register names** are operands, not primitives. `R_0` is a
  register with a syntactic "no-write" invariant.
* **Scratch registers** (the `Rg` family) are fresh operands per
  static textual occurrence of DJZ; their count is bounded by
  program length.
* **Labels and jump targets** are syntactic; the "jump-by-label
  machinery" is the framework within which the instruction is
  phrased, not a separate operation. CJDECINC's two label
  operands slot into this framework exactly the way JZ's one
  label operand slots into it in the baseline.
* **Halting by falling off the end** is a convention about the
  meaning of a finite program, not an instruction.

I acknowledge the alternative (stricter) counting — where HALT is
mandatory as a distinct primitive — and report |T| = 2 in that
regime.

### 4.3 Why I will not claim any fewer

Zero instructions cannot change register state. So |T| = 0 is not
possible. The only way to go strictly below |T| = 1 while
retaining something computational is to move "part of the
instruction" into the framework — for example, to make the
"increment scratch on zero-arm" side effect implicit. I decline to
do that: I fixed the counting convention in §0 specifically so
that the instruction is the operation, and the framework is only
labels and registers.

---

## 5. Verification

### 5.1 Chosen strategy

I verify T's universality by **instruction-wise simulation of the
baseline**. Because the baseline B is presumed universal for
partial recursive functions on ℕ^k, it is sufficient to exhibit,
for each baseline instruction I ∈ B, a finite macro M_I in T that
implements I's semantics on arbitrary register states. Then any
baseline program P compiles, modularly, to a T-program T(P) with
the same observable I/O behaviour.

### 5.2 Discharging the strategy

The macros were constructed in §3, stage by stage. Composing them
gives, for each baseline instruction, an explicit synthesis in T:

| Baseline instruction | Where synthesised in T |
|---|---|
| LOAD k into Ri | Stage 1 (`ZERO; INC^k`), further expanded through stages 3, 7, 8, 10 |
| COPY Rj into Ri | Stage 2, then ZERO (3) and ADD (4), expanded as below |
| ADD Rj into Ri | Stage 4, then ZERO (3), JMP (7), JZ (8), DEC (8), INC (10) |
| SUB Rj from Ri | Stage 5, similarly |
| ZERO Ri | Stage 3, then JMP (7), JZ (8), DEC (8) |
| INC Ri | Stage 10 |
| DEC Ri | Stage 8 via DJZ, then Stage 10 |
| JMP L | Stage 7 via `JZ R_0, L`, then Stage 8 via DJZ, Stage 10 via CJDECINC |
| JZ Ri, L | Stage 8 via DJZ + INC, then Stage 10 |
| JNZ Ri, L | Stage 6, then JMP and JZ as above |
| HALT | Stage 9 under H1; baseline primitive under H2 |

Three correctness obligations of the macro-expansion strategy
(stated in §2.1) hold:

1. **Per-instruction correctness.** Each stage came with a trace
   argument on the arms of the corresponding case split. Because
   later stages expand primitives introduced in earlier stages,
   the composition remains correct by induction on stage index.
2. **Scratch disjointness.** Each textual occurrence of a macro
   uses freshly named scratches. There are finitely many macro
   occurrences in a compiled program, so finitely many scratches
   suffice.
3. **Label disjointness.** Each macro's internal labels are
   α-renamed per occurrence.

Given these three, T(P) simulates P on the original registers.
Hence T computes every partial recursive function that P does;
hence T is universal.

### 5.3 Why I did not use an alternative verification route

A diagonal argument would let me refute universality but not
establish it. A reduction from a known-universal model via
outside-sourced results would violate the "no external citations"
rule. Direct construction of partial recursive functions inside T
— primitive recursion, unbounded μ-search — is feasible but
reduplicates §6's worked examples without adding confidence. The
simulation argument is the most compact discharge.

---

## 6. Worked examples

All three examples are written in the readable intermediate set
**{INC, DJZ}** (stage T_9) with `JMP L` as syntactic sugar for
`DJZ R_0, L`. The full expansion into T = {CJDECINC} is mechanical
via §3.10; I carry it out explicitly for addition at the end of
this section.

The convention in each example: input registers are listed;
output is R0; registers not listed as output are permitted to be
clobbered.

### 6.1 Addition: f(x, y) = x + y

Input R1 = x, R2 = y. Output R0 = x + y. R1 and R2 are destroyed.

```
; move R1 into R0
A1: DJZ R1, A2
    INC R0
    JMP A1
A2: ; move R2 into R0
    DJZ R2, A3
    INC R0
    JMP A2
A3: ; halt
```

**Trace.** Phase A1 runs x iterations, each moving one unit from R1
into R0; afterwards R1 = 0 and R0 has grown by x. Phase A2 is
identical on R2, adding y to R0. Final R0 = x + y. If x = 0, A1's
first DJZ jumps immediately to A2; the phase correctly contributes
0. Similarly for y = 0.

### 6.2 Multiplication: f(x, y) = x · y

Input R1 = x, R2 = y. Output R0 = x·y. R1 is destroyed; R2 is
preserved. Scratch R3.

```
; outer loop: x times, add R2 into R0 preserving R2 via R3
Out: DJZ R1, End
; add R2 into R0, splitting copies into R0 and R3
I1:  DJZ R2, I2
     INC R0
     INC R3
     JMP I1
I2:  ; restore R2 from R3
     DJZ R3, I3
     INC R2
     JMP I2
I3:  JMP Out
End: ; halt
```

**Trace.** At the top of each outer iteration, R2 = y and R3 = 0
(invariant: I3 is only reached with R3 = 0 because I2 drains it).
Phase I1 zeroes R2 while adding y to both R0 and R3. Phase I2
drains R3 into R2, restoring R2 = y and R3 = 0. After the restore,
R1 has been decremented once (by Out's own DJZ at the start of this
iteration). So each outer iteration adds y to R0 and drops R1 by 1.
The outer loop runs x times. Final R0 = x·y. Corner cases: x = 0
exits immediately at Out with R0 unchanged (still 0). y = 0 makes
I1 trivial, so each outer iteration adds 0, and the final R0 = 0.

### 6.3 Proper subtraction (monus): f(x, y) = max(0, x − y)

Input R1 = x, R2 = y. Output R0. R1 and R2 are destroyed.

```
; copy R1 to R0
C1: DJZ R1, C2
    INC R0
    JMP C1
C2: ; decrement R0 and R2 in parallel; exit when either hits 0
Lp: DJZ R2, Dn            ; if R2 = 0, done
    DJZ R0, Dn            ; else if R0 = 0, done
    JMP Lp
Dn: ; halt
```

**Trace.** Phase C1 moves R1 into R0 exactly, so after it R0 = x,
R1 = 0. The loop Lp executes the following per iteration:
first DJZ tests R2; if 0, jumps to Dn (answer is whatever R0
currently holds). Otherwise R2 is decremented and we test R0; if
0, jumps to Dn with answer 0. Otherwise R0 is decremented and we
loop. Let s = min(x, y). After s iterations of mutual decrement,
either R2 has reached 0 first (case x ≥ y, leaving R0 = x − y) or
R0 has reached 0 first (case x < y, leaving R0 = 0). In both
cases R0 holds max(0, x − y) at Dn. Edge cases x = 0 (R0 = 0 from
the start, exits via second DJZ) and y = 0 (exits via first DJZ on
first iteration) are covered.

### 6.4 Full expansion of addition into T = {CJDECINC}

To exhibit an honest program in T, I expand §6.1 mechanically using
§3.10. I use scratches `Rg1, …, Rg5`. Label `end` denotes the slot
past the final instruction (halting under H1).

```
A1:  CJDECINC R1, Rg1, A2,  A1a    ; DJZ R1, A2
A1a: CJDECINC R_0, R0, A1b, A1b    ; INC R0
A1b: CJDECINC R_0, Rg2, A1,  A1    ; JMP A1

A2:  CJDECINC R2, Rg3, A3,  A2a    ; DJZ R2, A3
A2a: CJDECINC R_0, R0, A2b, A2b    ; INC R0
A2b: CJDECINC R_0, Rg4, A2,  A2    ; JMP A2

A3:  CJDECINC R_0, Rg5, end, end   ; HALT ≡ JMP end
```

The program has seven CJDECINC instructions, uses one
invariant-zero register R_0, and five scratches. Every step
matches the instruction-synthesis rules of §3.10, so correctness
of §6.1 transfers.

---

## 7. Open questions and limitations

### 7.1 Is |T| = 1 optimal?

**In instruction count, yes.** Zero instructions perform no state
change. One is the floor under both conventions H1 and H2 (modulo
the halting primitive).

**In other complexity measures, no.** The single instruction
CJDECINC has four operand slots (two registers, two labels). If
the figure of merit is "total operand slots" or "semantic width",
the two-instruction set {INC, DJZ} — with 1 and 2 operand slots
respectively — is strictly leaner by that measure. There is a
genuine Pareto frontier:

| Design | Instructions | Max operands | Semantic arms per instruction |
|---|---|---|---|
| {INC, DEC, JZ} | 3 | 2 | 1 |
| {INC, DJZ} | 2 | 2 | 2 |
| {CJDECINC} | 1 | 4 | 2 |

Declaring any one of these "the" minimal set presumes a figure of
merit. My deliverable is |T| = 1 under the "count instruction
types" figure, which is what the task's phrasing ("smallest subset
T") appears to intend.

### 7.2 What if we remove one more instruction from T?

T has only one instruction; removing it empties T and kills
computation. A more interesting question is whether we can
*weaken* CJDECINC and keep universality.

* **Drop the increment arm.** Replace CJDECINC with a
  "decrement-or-halt" primitive. Then no instruction increases
  any register. From an initial state {inputs ∪ zeros}, register
  values are weakly decreasing over time. The machine cannot
  compute any function whose output on some input exceeds the
  maximum input value — which rules out, say, n ↦ n + 1. Not
  universal.
* **Drop the decrement arm.** No instruction decreases any
  register. Register values are weakly increasing. The program's
  termination depends only on control flow, not on register
  contents, since no zero test can ever flip from "nonzero" to
  "zero" during execution. Control flow over a finite instruction
  set with no state-contingent branching is trivial. Not
  universal.
* **Drop the conditional.** Force both arms to execute
  unconditionally (e.g., always decrement Ri *and* always
  increment Rj *and* fall through to the next instruction). Then
  every program is a straight-line sequence of fixed effects;
  runtime is fixed per input, and partial recursive functions
  with genuinely non-total behaviour cannot be implemented.

So each of the three features (inc, dec, branch) is individually
necessary. CJDECINC is "tight" in that sense.

### 7.3 Bounded registers

If each register is capped at a fixed integer bound B, the
machine's total state space is finite (|S| = B^{#registers} ×
#program-counters). Any finite-state machine computes only
regular behaviours on its input stream; in particular, functions
with unbounded range (factorial, exponentials, lookup tables for
non-regular sets) are excluded. T is therefore **not** universal
under a fixed register bound.

If the bound scales with input length, we recover a more
generous class (like polynomial or linear space). Full
universality for partial recursive functions on ℕ^k requires
unbounded precision.

A different axis: if the *number* of registers is bounded but
their contents are not, the machine stays universal with a
sufficiently generous bound (two unbounded registers suffice,
with some encoding overhead). This is a model-strength
orthogonality that I do not pursue here.

### 7.4 Sensitivity to counting convention

The single-instruction result depends on three choices made in §0:

* HALT absorbed into end-of-program (convention H1).
* Labels and jump targets treated as syntactic.
* Registers treated as a free resource with a syntactic "never
  written" invariant available for R_0.

Each is defensible but each is a choice. Under stricter
accounting (H2, or labels counted as a primitive), the minimum
rises to 2 or 3 primitives. I am explicit about this because the
question "what is the smallest T?" has no absolute answer without
a counting convention; the work is to state one and show what
follows.

### 7.5 Things I did not prove

* **Simulation overhead.** The compiled T-program has size
  linear in the baseline program in principle, but the constant
  is not small — each baseline instruction expands to a few T
  instructions, and those expand further through the stages.
  I did not bound the constant tightly.
* **Time and space blowup** of compiled programs over the
  baseline's time and space. For the worked examples, the blowup
  is modest, but I did not analyse it in general.
* **Smallest alternative one-instruction fusions.** CJDECINC is
  one design; "INCDECJZ Ri, Rj, L" (always increment Rj, always
  decrement Ri with floor, jump to L iff Ri was zero before
  decrement) is another. I believe it is also universal by a
  very similar argument, but I did not work it out.
* **Whether T without R_0 is universal.** If we forbid the
  syntactic-zero register, the `JMP L` synthesis in §3 stage 7
  breaks, and I would need a different bootstrap. I expect it to
  work (one can INC a fresh register once at the program start
  and use "jump on nonzero with restore" techniques), but I did
  not carry it through.

---

## Summary

Under the counting convention "instructions are operation types,
labels and jump targets are syntactic, halting is end-of-program"
(convention H1 of §0), the 11-baseline register-machine
instruction set collapses to a single fused primitive:

> **CJDECINC Ri, Rj, L_zero, L_nonzero** — if Ri = 0 then
> increment Rj and jump to L_zero; else decrement Ri and jump to
> L_nonzero.

The reduction is a 10-stage sequence of macro expansions, each
trace-verified on the two arms of a register-is-zero test. The
three roles that any universal register-machine instruction set
must fill (increase, decrease, conditional branch) are exactly the
three arms of CJDECINC; weakening any one of them breaks
universality. Under the stricter convention that HALT is itself
a primitive, the minimum is two instructions: {CJDECINC, HALT}.
