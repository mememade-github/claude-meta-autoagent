# The Minimal Instruction Set for a Universal Register Machine

## §0. Setup and preview of the answer

We work with the register-machine model stated in the task: unbounded-precision
non-negative-integer registers R0, R1, R2, …, with an arbitrary finite number
available. The baseline is the 11 instructions (LOAD, COPY, ADD, SUB, ZERO, INC,
DEC, JMP, JZ, JNZ, HALT). We take as given that this 11-instruction set is
universal for the partial recursive functions on ℕᵏ.

**Question.** What is the smallest subset T (possibly enlarged by one fused
instruction we invent) that is still universal?

**Answer we will reach.** T consists of a single fused instruction we call
**STEP**, together with the label-and-jump machinery. STEP has the semantics

    STEP Ri, Rj, L1, L2:
        if Ri > 0: Ri := Ri − 1; goto L1
        else     : Rj := Rj + 1; goto L2

No instruction from the baseline survives; the one-instruction set {STEP}
simulates each of the 11. The counting convention under which this is a
*one-opcode* set — and the alternative conventions under which it is 2 or 4 —
is stated explicitly in §4.

The result is not a surprise once the structural feature in §1.2 is spotted.
What is substantive is the construction of STEP's two-branch guarded semantics
so that a single opcode absorbs both "grow" and "shrink" primitives.

A roadmap:

- §1 Motivation and structural intuition.
- §2 A general-purpose reduction procedure.
- §3 A sequence of progressively smaller subsets (11 → 9 → 8 → 6 → 5 → 4 → 1).
- §4 The minimal set T = {STEP}, with explicit counting convention.
- §5 The verification strategy (simulation of each baseline instruction) and
    its discharge.
- §6 Worked examples: addition, multiplication, proper subtraction.
- §7 Open questions, optimality, bounded-register variant, and a named
    limitation around the "hidden side effect on a garbage register."

---

## §1. Motivation

### §1.1 Precedents, reasoned from first principles

Four structurally analogous reductions in neighboring domains motivate the
expectation of a large collapse.

**(a) Functional completeness by a single connective.** Classical two-valued
logic admits a minimal basis {AND, NOT} — every Boolean function is expressible
from these two. But one can fuse them into a single connective, NAND, defined
by NAND(x, y) = NOT(AND(x, y)). Because NAND's truth table has the shape
"one output for (1,1), the opposite output elsewhere," it simultaneously encodes
a negation and a conjunction, and the 1-connective system is still complete.

The motif is: when a domain factors into "combine" and "invert" primitives,
a fused operator that behaves differently on a guarded input can absorb both.
We will fuse "grow" and "shrink" on the integer register in the same shape.

**(b) Combinator completeness.** The S and K combinators (with S f g x = f x (g x)
and K x y = x) are known to be jointly Turing-complete for the lambda
calculus. A *single-combinator* basis can be built by defining a combinator
whose reduction rule, applied to structurally-different argument patterns,
reproduces both S's action and K's action. A concrete sketch: if ι is
defined by ι f = f S K, then applying ι to a suitably chosen argument
recovers S, and applying it to a different argument recovers K, so both
primitives are expressible in terms of ι alone. The guarded-behavior motif
reappears: the *shape of the argument* plays the guard role, selecting
which original primitive the fused combinator simulates.

**(c) Generator reduction in algebra.** A free monoid on one generator is only
cyclic; but a *relation-constrained* monoid on one generator can be rich. The
constraint plays the same role as "guard" in (a) and (b): it enables a single
primitive to exhibit context-dependent behavior.

**(d) Universality of very small machines.** A variety of superficially trivial
computing devices — simple tag-style rewriting systems, certain minimal
cellular automata — are Turing-complete. The common feature is that a single
local rule both modifies state *and* transitions control, with the choice of
each being driven by a guard on the current state. This is structurally what
we will build: one instruction that modifies one of two registers and
transitions to one of two labels, guarded by a register's sign.

### §1.2 Structural feature of the baseline that invites a large reduction

The 11 baseline instructions cluster into three functional roles:

- **Accumulators:** LOAD, COPY, ADD, INC — ways to grow or assign a register.
- **Reducers:** SUB, DEC, ZERO — ways to shrink or clear a register.
- **Control:** JMP, JZ, JNZ, HALT — ways to move the program counter.

Intra-cluster redundancy is abundant: within accumulators, INC plus looping
suffices for LOAD/COPY/ADD. Within reducers, DEC plus looping suffices for
ZERO, and SUB decomposes to DEC. Within control, JZ together with an
always-zero register suffices for JMP, and JNZ is JZ's dual.

This is the first collapse: we expect to reach {INC, DEC, JZ, HALT} (four
baseline instructions) without creative fusion.

The harder collapse — from four to one — requires fusion *across* clusters.
The key observation is that the act of decrementing a register and branching
on whether it was zero is *already* the test used by JZ: we can read a
register's zero-ness as a side effect of attempting to decrement it. A single
instruction that, depending on the outcome of a test-and-decrement, *either*
takes the decrement branch *or* performs a guarded increment of some other
register, can absorb both arithmetic and branching.

### §1.3 What could make us doubt a further reduction?

The saturation behavior of non-negative integer registers — DEC at 0 is a
no-op, SUB never goes negative — removes a tool used in some classical
reductions: if signed subtraction were available, one could simulate addition
by subtracting a negative constant from a fixed "minus-one" cell, collapsing
accumulation and reduction into one primitive. This tool is unavailable here.

So we should doubt a pure *SUB + branch* fusion. A single instruction that can
only shrink a register cannot simulate unbounded addition. The fused
instruction must itself include an increment branch. That is exactly what
STEP's "else" branch provides.

---

## §2. A systematic reduction procedure (generalizable)

We state a procedure RM-REDUCE that applies to any register-machine instruction
set; the specific reductions in §3 are instances.

**Input.** An instruction set I known to be universal, a semantic function
from I-programs to partial functions on ℕᵏ, and the model's standard
conventions (registers non-negative, arbitrary finite supply).

**Output.** A reduced instruction set I' ⊆ I (optionally enriched by
fused instructions not in I) that is still universal, together with an
explicit simulation of each removed instruction by a finite program in I'.

**Procedure RM-REDUCE.**

1. **Cluster by role.** Partition I into *accumulators* (grow/assign),
    *reducers* (shrink/clear), *tests-and-branches*, and *terminators*.
    Identify redundancy *within* each cluster: which instructions are
    syntactically distinct but semantically derivable from others?

2. **Eliminate intra-cluster redundancy.** For each redundant instruction X,
    give a finite *synthesis macro* in I \ {X} that, when inlined wherever X
    appears in a program, preserves the program's semantics. The macro may
    allocate fresh auxiliary registers and labels.

3. **Eliminate inter-cluster redundancy by guarded fusion.** If one can design
    a new instruction whose action is "behavior A under guard G; behavior B
    under guard ¬G" such that the existing primitives are re-derivable by
    arranging the inputs so that either G or ¬G holds deterministically, then
    collapse the relevant existing primitives into the fused instruction.

4. **Verify.** Translate each instruction in the original I (including those
    eliminated in step 2 and 3) into a finite program in I'. The translation is
    correct if, for every I-program P and every input, the translated I'-program
    P' halts on the same inputs as P and produces the same value on the
    designated output register.

5. **Respect auxiliary conventions.** Spell out which features are
    *instructions* (opcodes) and which are *conventions* (initial register
    values, label naming, end-of-program behavior). Any reduction claim is
    meaningless until the counting convention is fixed.

The procedure is sound when each synthesis macro is semantically correct
(inductively verified on program structure) and when the fused instruction
genuinely covers all cases: specifically, that inputs to the fused instruction
can always be chosen so that the desired guard outcome is forced. §3.6 below
discharges this condition for STEP.

---

## §3. Progressive reduction, with eliminations and syntheses

We apply RM-REDUCE. Each stage names the instructions eliminated and provides
the explicit synthesis used.

**Shared conventions for the syntheses.**

- Rz denotes a *zero register*: a register whose value is 0 and which never
    appears as a destination (second operand) in any STEP we emit in later
    stages. Since registers initialize to 0 by the standard setup and we never
    write to Rz, Rz's value is an invariant.
- Rg denotes a *garbage register*: a register whose value we may write to in
    macros but which never appears as a *source* (first operand) in any STEP we
    emit. Rg's value drifts upward during execution; because Rg is never read,
    this drift does not affect any computed function on the designated
    input/output registers.
- T, T1, T2, … denote *fresh temporaries*, allocated per synthesis instance.
    They begin at 0 (standard setup) and are not reused across instances.
- Labels are syntactic attachments to program points; we do not count them as
    opcodes (see §4.1).

### §3.1 Stage 0 → 1: eliminate LOAD and ZERO

Using {DEC, JZ, JMP}:

    ZERO Ri           synthesis:
        Lstart:  JZ Ri, Lend
                 DEC Ri
                 JMP Lstart
        Lend:

Using {ZERO, INC} (which itself is now available via the synthesis above):

    LOAD k into Ri    synthesis:
        ZERO Ri
        INC Ri    (repeated k times)

**Eliminated in this stage:** LOAD, ZERO.
**Remaining:** {COPY, ADD, SUB, INC, DEC, JMP, JZ, JNZ, HALT} — 9.

### §3.2 Stage 1 → 2: eliminate JNZ

    JNZ Ri, L         synthesis:
                 JZ Ri, Lskip
                 JMP L
        Lskip:

**Eliminated:** JNZ.
**Remaining:** {COPY, ADD, SUB, INC, DEC, JMP, JZ, HALT} — 8.

### §3.3 Stage 2 → 3: eliminate COPY and ADD

ADD preserves Rj; we shuttle Rj through a temp T to preserve it:

    ADD Rj into Ri    synthesis:
        ZERO T
        Lphase1:  JZ Rj, Lphase2
                  DEC Rj
                  INC T
                  INC Ri
                  JMP Lphase1
        Lphase2:  JZ T, Lend
                  DEC T
                  INC Rj
                  JMP Lphase2
        Lend:

And COPY is ZERO-then-ADD:

    COPY Rj into Ri   synthesis:
        ZERO Ri
        ADD Rj into Ri

**Eliminated:** COPY, ADD.
**Remaining:** {SUB, INC, DEC, JMP, JZ, HALT} — 6.

### §3.4 Stage 3 → 4: eliminate SUB

SUB is saturating subtraction preserving Rj. We move Rj into T (zeroing Rj),
then move T back into Rj while concurrently decrementing Ri:

    SUB Rj from Ri    synthesis:
        ZERO T
        Lphase1:  JZ Rj, Lphase2
                  DEC Rj
                  INC T
                  JMP Lphase1
        Lphase2:  JZ T, Lend
                  DEC T
                  INC Rj
                  DEC Ri     ( saturates at 0 )
                  JMP Lphase2
        Lend:

**Eliminated:** SUB.
**Remaining:** {INC, DEC, JMP, JZ, HALT} — 5.

### §3.5 Stage 4 → 5: eliminate JMP

    JMP L             synthesis (using Rz, always zero):
                  JZ Rz, L

**Eliminated:** JMP.
**Remaining:** {INC, DEC, JZ, HALT} — 4.

At this point, we have a pleasant four-instruction baseline. {INC, DEC, JZ,
HALT} is universal, as every baseline instruction above has been simulated
from it. The remaining collapse requires fusion.

### §3.6 Stage 5 → 6: fusion to STEP

Define the fused instruction:

    STEP Ri, Rj, L1, L2:
        if Ri > 0:
            Ri := Ri − 1
            goto L1
        else:          (Ri == 0)
            Rj := Rj + 1
            goto L2

STEP takes two register operands and two label operands; it has two mutually
exclusive branches, selected by a guard on Ri.

**Claim.** {STEP} simulates each of {INC, DEC, JZ, HALT}.

The simulation macros are given below. In each, "goto Lnext" means "continue
execution at label Lnext, which the translator assigns to whatever instruction
follows the macro in the original program." The macros use Rz (zero register),
Rg (garbage register), and a distinguished label Lhalt placed past the last
emitted instruction of the translation.

**INC Ri ; continue at Lnext:**

        STEP Rz, Ri, Lnext, Lnext

Because Rz = 0, only the else branch fires: Ri is incremented and we jump to
Lnext. Both label operands are set to Lnext; the choice is immaterial because
the other branch is inaccessible.

**DEC Ri ; continue at Lnext** (with baseline saturation at 0):

        STEP Ri, Rg, Lnext, Lnext

If Ri > 0, Ri is decremented and we jump to Lnext (matching baseline DEC).
If Ri = 0, Rg is incremented (a garbage side effect, §3 convention) and we
jump to Lnext; Ri remains 0 (matching baseline's saturation). Either way the
jump destination is Lnext, so the macro is position-preserving.

**JZ Ri, Ltarget ; continue at Lfall** (baseline: jump to Ltarget if Ri = 0,
else fall through with Ri unchanged):

        Ltest:  STEP Ri, Rg, Lrestore, Ltarget
        Lrestore: STEP Rz, Ri, Lfall, Lfall

Trace: if Ri = 0, the first STEP takes its else branch: Rg++, jump to
Ltarget. Ri remained 0 throughout, matching the baseline's "Ri unchanged"
behavior.

If Ri > 0, the first STEP decrements Ri to Ri−1 and jumps to Lrestore. The
second STEP (at Lrestore) then increments Ri back to its original value
(because Rz = 0 forces the else branch) and jumps to Lfall. Ri is restored.

**HALT:**

We designate a distinguished label Lhalt placed past the last emitted STEP of
the translation. We adopt the convention "control arriving at a label with
no instruction halts execution." HALT is then translated as:

        STEP Rz, Rg, Lhalt, Lhalt

which unconditionally jumps to Lhalt and terminates.

**Eliminated at this stage:** INC, DEC, JZ, HALT.
**Remaining:** {STEP} — 1 opcode.

---

## §4. The minimal T, and the counting convention

T = {STEP}.

### §4.1 Counting convention (explicit)

We adopt the following counting convention throughout:

An **instruction** (or **opcode**) is a named atomic operation the machine
recognizes at each step of execution. Each instruction may take operands,
drawn from:
- register names (R0, R1, …),
- numeric constants (as in LOAD k of the baseline),
- labels, which are references to program points.

The following are **not** opcodes:

- **Labels.** A label is syntactic glue attaching a symbolic name to a
    program point. Jumps are *operand* references to labels, not separate
    instructions.
- **End-of-program halting.** The program's termination at the end of its
    instruction list is a semantic convention of the model, not an opcode.
- **Register initialization to 0.** The fact that registers not used as
    input begin at 0 is a semantic convention of the model, not an opcode.
- **Designation of a register as "always zero" (Rz) or "garbage" (Rg).**
    These are naming conventions imposed by the *translator* (the human
    writing the program). They do not add opcodes.

Under this convention, T = {STEP} is a **one-opcode** instruction set.

### §4.2 Alternative conventions

Some readers may insist on counting more things as primitives. We record the
count under each alternative:

- **Strict opcode count** (our convention): 1. (STEP alone.)
- **Opcode + terminal convention**: 2. (STEP + the halt-at-end rule, if one
    views halting as an opcode.)
- **Opcode + terminal + zero-init**: 3. (Adding register initialization.)
- **Opcode + labels as a primitive**: 2. (If one declares "has labels" a
    primitive of the language.)
- **Fully conservative** (all conventions counted): 4.

The central engineering fact — that a single *computing* instruction suffices
— is robust across these conventions. What varies is merely bookkeeping.

### §4.3 Exact semantics of STEP

    STEP Ri, Rj, L1, L2:
        if Ri > 0:   Ri := Ri − 1;  goto L1
        else:        Rj := Rj + 1;  goto L2

- Ri, Rj are register names. They may be the same register; §4.4 discusses
    this edge case.
- L1, L2 are labels. They may coincide (and do coincide in several of our
    synthesis macros: INC, DEC, HALT all use L1 = L2).
- The two branches are *mutually exclusive*: exactly one fires per execution.
- The action is atomic: the register update and the jump are one step.
- The register arithmetic is saturating at 0 *by virtue of the guard*:
    the decrement branch fires only when Ri > 0, so Ri − 1 ≥ 0 is guaranteed.

### §4.4 Edge case: Ri = Rj

If Ri and Rj are the same register R, then:

- If R > 0: the decrement branch fires and R := R − 1, goto L1. The "other
    operand" (which is the same register) is irrelevant because the decrement
    branch does not touch it.
- If R = 0: the else branch fires and R := R + 1, goto L2. After the step,
    R = 1.

This is well-defined but rarely useful. The synthesis macros in §3.6 never
pass the same register as both operands; they always use distinct registers
(often Rz in slot 1 or Rg in slot 2). We mention the edge case only to confirm
that STEP is fully defined on all operand choices.

### §4.5 Where the "zero register" convention has content

The convention "Rz is always 0" is what the translator imposes. Concretely:
the translator never emits a STEP with Rz in slot 2 (the destination of the
else branch's increment). Rz may appear in slot 1 (the source of the guard),
but reading Rz with Ri = 0 triggers the else branch, which writes to *Rj*, not
to *Ri*. So Rz's value is never modified by any emitted STEP, and Rz = 0 is
a program-wide invariant.

This is a discipline on the translator, not a new opcode. Similarly, Rg
appears only in slot 2 and never in slot 1; its value drifts upward but is
never read.

---

## §5. Verification strategy

**Strategy.** Simulation of each baseline instruction by STEP-only macros.

The 11-instruction baseline is given universal. To show T = {STEP} is
universal, it suffices to show that every baseline instruction can be
simulated by a finite STEP-only program with the correct halting and
input-output behavior.

### §5.1 Coverage

§3 eliminated each of the 11 baseline instructions in at least one stage. By
composing the syntheses:

- LOAD and ZERO were synthesized from {DEC, JZ, JMP} in §3.1.
- JNZ from {JZ, JMP} in §3.2.
- COPY and ADD from {INC, DEC, JZ, JMP} in §3.3.
- SUB from {INC, DEC, JZ, JMP} in §3.4.
- JMP from {JZ} (with Rz) in §3.5.
- INC, DEC, JZ, HALT from {STEP} in §3.6.

Composing these: each of the 11 is expressible in {STEP}.

### §5.2 Correctness of the simulation (inductive)

Let P be any baseline program and P' its STEP-only translation. We claim P
and P' compute the same partial function on the designated input/output
registers.

**Inductive invariant.** At any point where P's program counter is at
baseline instruction number n and P's register state is σ, P' has just
completed the macro for instruction n − 1, its program counter is at the
label corresponding to the start of instruction n's macro, and P's
designated registers have values σ in P' (except that Rg, Rz, and temporaries
are as specified by §3 conventions).

**Base case.** n = 0: P' starts at the macro for baseline instruction 0,
with the same inputs in the same designated registers; Rg = Rz = 0, and all
temporaries are 0. The invariant holds.

**Inductive step.** Suppose the invariant holds before instruction n. The
macro for instruction n is a finite STEP-only sequence that:

- reads and writes exactly the registers that the baseline instruction reads
    and writes (plus Rg and temporaries);
- terminates in a bounded number of steps and transfers control to the label
    corresponding to the next baseline instruction;
- leaves the designated registers in the state the baseline instruction
    would have produced (§3.6 verifies this register-by-register for each of
    INC, DEC, JZ, HALT, and transitively for the others via §3's chain).

So the invariant holds after instruction n.

**Halting behavior.** If baseline P halts at some step, its translation halts
(all macros are finite; HALT becomes a jump to Lhalt, which by §4.1's
convention terminates). If baseline P diverges, so does P' (infinitely many
baseline steps translate to infinitely many STEP steps).

**Input-output agreement.** By the invariant, the designated output register
holds the same value at halt in both P and P'.

Therefore P and P' compute the same partial function. ∎

### §5.3 Why not a diagonal argument or a different strategy?

A diagonal argument would show only that some partial recursive function is
not in T (which we do not want: we want the opposite). A reduction to an
external universal model (e.g., to a known-universal functional calculus)
would require first establishing that model's universality within our
constraints (no citation, derive from first principles), which is more work
than the direct instruction-by-instruction simulation above. The chosen
strategy is the most efficient path given the task's "no-citations" constraint
and the given universality of the baseline.

---

## §6. Worked examples

In all examples: inputs are in R1, R2, …; output is in Rout (assumed 0 at
start). Rz is the always-zero register; Rg is the garbage register;
T, T1, T2 are temporaries (initialized to 0 by §3 conventions).

Execution halts upon arriving at the distinguished label Lhalt at the end of
the program.

### §6.1 Addition: f(a, b) = a + b

Strategy: transfer R1 into Rout; then transfer R2 into Rout.

    L0:    STEP R1, Rg, Linc1, L1
    Linc1: STEP Rz, Rout, L0, L0
    L1:    STEP R2, Rg, Linc2, Lhalt
    Linc2: STEP Rz, Rout, L1, L1
    Lhalt:

Trace (with R1 = a, R2 = b, Rout = 0):

- At L0: if R1 > 0, DEC R1 and go to Linc1; else Rg++ and go to L1.
- At Linc1 (Rz = 0 → else branch): INC Rout and go back to L0.
- After a iterations: R1 = 0, Rout = a. At L0, we take the Rg-else branch
    and go to L1.
- At L1: if R2 > 0, DEC R2 and go to Linc2; else Rg++ and go to Lhalt.
- At Linc2: INC Rout, go to L1.
- After b iterations: R2 = 0, Rout = a + b. At L1, Rg-else branch goes to
    Lhalt. Halt.

Final Rout = a + b. ✓

### §6.2 Multiplication: f(a, b) = a · b

Strategy: while R1 > 0, decrement R1 and add a preserved copy of R2 to Rout.
Adding R2 preservingly is done by shuttling R2 through a temporary T.

    Louter: STEP R1, Rg, Lcopy, Lhalt
    Lcopy:  STEP R2, Rg, LincR, Lback
    LincR:  STEP Rz, Rout, LincT, LincT
    LincT:  STEP Rz, T,    Lcopy, Lcopy
    Lback:  STEP T,  Rg,   LincB, Lnext
    LincB:  STEP Rz, R2,   Lback, Lback
    Lnext:  STEP Rz, Rg,   Louter, Louter
    Lhalt:

Trace skeleton (R1 = a, R2 = b, Rout = 0, T = 0):

- Louter: if R1 > 0, DEC R1, go to Lcopy; else go to Lhalt.
- Inner "copy-and-accumulate" loop (Lcopy … LincT):
    - Each iteration executes three STEPs in sequence: Lcopy decrements R2,
      LincR increments Rout, LincT increments T, then control returns to
      Lcopy. So each DEC of R2 is matched (within the same iteration) by
      one INC of Rout and one INC of T.
    - When R2 = 0, the Lcopy else branch goes to Lback.
    - Post-loop: R2 = 0, Rout is increased by old(R2), T = old(R2).
- "Restore R2" loop (Lback … LincB):
    - Transfers T back into R2.
    - Post-loop: T = 0, R2 = old(R2).
- Lnext: unconditional jump to Louter (Rz-forced else branch).

After one outer iteration: R1 decreased by 1, R2 unchanged, Rout increased
by b, T = 0.

After a outer iterations: R1 = 0, R2 = b, Rout = a · b. Halt.

Final Rout = a · b. ✓

### §6.3 Proper subtraction (monus): f(a, b) = max(0, a − b)

Strategy: move R1 to Rout. Then, for each decrement of R2, decrement Rout
(with natural saturation at 0).

    Lmov:  STEP R1, Rg, LincO, Lsub
    LincO: STEP Rz, Rout, Lmov, Lmov
    Lsub:  STEP R2, Rg, Ldec, Lhalt
    Ldec:  STEP Rout, Rg, Lsub, Lsub
    Lhalt:

Trace (R1 = a, R2 = b, Rout = 0):

- Lmov / LincO loop: transfers R1 into Rout. After: R1 = 0, Rout = a.
- Lsub: if R2 > 0, DEC R2, go to Ldec; else halt.
- Ldec: if Rout > 0, DEC Rout, go back to Lsub; if Rout = 0 (we have
    already hit zero), INC Rg and go back to Lsub (Rout stays 0).
- The combined effect: min(a, b) iterations decrement Rout from a down to
    max(0, a − b); any remaining iterations of the outer loop decrement R2
    while leaving Rout at 0.

Case a ≥ b: after b outer iterations, R2 = 0 and Rout = a − b. Halt.
Case a < b: after a outer iterations, Rout = 0 and R2 = b − a. The next
b − a outer iterations decrement R2 further, leaving Rout = 0 throughout.
After b total outer iterations, R2 = 0 and Rout = 0. Halt.

Either way, Final Rout = max(0, a − b). ✓

---

## §7. Open questions and known limitations

### §7.1 Is T = {STEP} optimal, or merely sufficient?

At the *opcode count* convention of §4.1, T is optimal: zero opcodes cannot
compute any non-trivial function, so 1 is the minimum.

At the *semantic complexity* level — how much is STEP "doing" — T is *not
strictly demonstrated* optimal. We have argued informally (§1.3) that a
single instruction lacking an increment branch cannot be universal under
non-negative saturating arithmetic; a pure "decrement-and-branch" fusion is
insufficient. We have also argued that a single instruction with only one
label operand cannot express two distinct successors without auxiliary
structure (the "fall-through" convention is really a second implicit label).
But we have not ruled out all *differently structured* one-opcode instructions
with fewer operand slots than STEP's 4 (2 registers + 2 labels). This is a
**named gap** rather than a closed argument.

Concretely, the candidates we have *not* formally excluded are:

(i) **2 regs + 1 explicit label + fall-through** (effectively 4 slots if
    fall-through is counted as an implicit label; but 3 if not). Our present
    argument is that the fall-through is a disguise of a second label, so
    this is not really a reduction — but this is a *counting* argument, not
    a complexity argument.

(ii) **1 register + 2 labels**. A STEP-variant like "if Ri > 0, DEC Ri,
    goto L1; else INC Ri, goto L2" has only 1 register operand. Our doubt:
    the instruction can only modify a single register per site (the same
    register it tests), and we see no way to maintain an "always zero"
    register to drive unconditional INC of an *arbitrary* target, nor to
    non-destructively copy values across registers with only one register
    per instruction. But we have not formalized a proof that no encoding
    recovers universality; a Gödel-pairing argument might do it with clever
    use of multiple register sites.

(iii) **0 registers + k labels**, where the instruction has fixed
    hard-coded target counters (as in a 2-counter or 3-counter machine with
    a single fused operation on fixed counters). A fixed-target one-opcode
    machine would need enough branches to express INC and DEC on at least
    two distinct counters, giving a lower bound on the number of labels
    needed; we have not done the combinatorial accounting.

In each case, the obstruction we intuit is structural, not formal. We
therefore preserve the conjecture "STEP's 4 operand slots are minimal" as a
disclosed, unresolved question, and refrain from asserting a closure that
would require case analysis we have not completed. (Per the integrity
convention this document honors: a named gap is strictly preferred over a
closed-looking proof that turns out to rely on its own conclusion.)

### §7.2 What happens if we remove one more instruction from T?

Since T has exactly one opcode, "removing one more" leaves zero opcodes. A
zero-opcode program consists only of labels and has no executable steps. Such
a program computes only the identity function (output = input, no computation
performed). So universality is lost immediately upon removal.

### §7.3 What changes if the register model is bounded?

Suppose each register holds values in {0, 1, …, M} for fixed M. Then the
total machine state is finite: at most M^k configurations of k registers times
however many program points. A machine with finite state computes only a
subset of the partial recursive functions (the regular / finitely-computable
ones) and cannot be universal.

This is a *global* bound on what any instruction set can achieve; no fused
instruction or clever instruction design can recover universality on bounded
registers. Any unboundedness must live somewhere in the model — in our case,
in register precision.

### §7.4 A named limitation: the garbage register's monotone drift

Our simulation incurs monotone growth of the garbage register Rg. Concretely,
Rg is incremented by 1 in each of the following cases:

- every simulated DEC of a register whose current value is 0 (the else branch
    of the `STEP Ri, Rg, Lnext, Lnext` macro fires and writes Rg);
- every simulated JZ whose tested register is 0 (the first STEP of the
    `STEP Ri, Rg, Lrestore, Ltarget` macro takes its else branch);
- every unconditional jump via `JZ Rz, L` (Rz is always 0, so the else
    branch fires and increments whatever register is in slot 2 — in our
    §3.6 expansion of JMP, this is Rg);
- every simulated HALT (compiled to `STEP Rz, Rg, Lhalt, Lhalt`, whose
    else branch always fires since Rz = 0; this contributes exactly one
    increment to Rg per program run).

Rg is never read by any emitted STEP (§3 convention), so this monotone drift
does not affect the *computed function* on the designated input/output
registers. However, the translation does *not* preserve the exact multiset
of register values: the total "mass" in registers under the translation is
larger than under the baseline. We preserve only the projections onto the
designated input and output registers, which is the correct notion of
"computes the same partial function" (§5.2's inductive invariant makes this
explicit by carving out Rg, Rz, and temporaries). We name this discrepancy
so that any reader who expected register-by-register faithfulness is not
surprised.

### §7.5 A named internal tension

§4.2 offers several counting conventions. Under the most conservative
(count labels, terminal convention, zero-init as primitives), T has 4
"primitives," not 1. A reader who insists on this strict counting would
deny the headline "1 instruction suffices." We do not resolve this — the
counting choice is genuinely conventional. We preserve the claim "1
*opcode*" under §4.1's convention, while disclosing that it becomes
"up to 4 primitives" under the most conservative bookkeeping. This tension
is explicit; it is not smuggled.

### §7.6 What a closed version of §7.1 would need

To upgrade §7.1 from "disclosed gap" to "closed argument," we would need:

1. A precise formal notion of "one-opcode instruction with k operand
    slots," including the types of each slot (register name, label, small
    tag, numeric constant) and the form of the guard (e.g., sign-of-a-
    single-register, comparison of two registers, a Boolean on internal
    state).
2. Case-by-case dismissal of each reduction candidate listed in §7.1 —
    (i) the fall-through variant, (ii) the 1-register + 2-label variant,
    (iii) the 0-register + k-label hard-coded-target variant — as
    non-universal over non-negative registers. Each dismissal would
    itself require:
    - a proof that the candidate cannot produce arbitrary non-negative
      register values (for the "grow" axis), or
    - a proof that it cannot distinguish register-zero from register-
      non-zero across arbitrary inputs (for the "branch" axis), or
    - a combinatorial accounting of how many instruction sites are
      required per baseline instruction, showing no finite expansion
      suffices.

We have sketched the intuitive obstructions (§1.3 for fewer operands of the
wrong type; §4.3–§4.5 for the registers-and-labels split; §7.1 for the
specific three candidate reductions) but have not formalized them. This
remains open, and is preserved as a named gap rather than closed with an
argument we cannot fully verify.

### §7.7 Sensitivity to the guard

STEP's guard is "Ri > 0 vs Ri = 0." One could define a variant STEP' whose
guard is "Rj > 0 vs Rj = 0" (checking the second operand instead) with
identical behavior up to swapping operand roles. Any such re-parameterization
is trivially equivalent. More interesting questions — whether a guard on a
*different* predicate (e.g., "Ri > Rj") would yield a different minimal
instruction — are beyond this argument's scope.

---

## §8. Summary

- The full 11-instruction baseline admits a systematic reduction to 4
    instructions {INC, DEC, JZ, HALT} without fusion (§3.1–§3.5), and to
    1 instruction {STEP} with a single guarded fusion (§3.6).
- T = {STEP} with labels-as-operands is universal, verified by simulation
    of the baseline (§5).
- The counting convention under which T has 1 opcode is stated explicitly
    (§4.1) and alternatives enumerated (§4.2). The central fact — that one
    *computing* instruction suffices — is invariant across the conventions.
- Worked examples (§6) exhibit addition, multiplication, and proper
    subtraction as full STEP programs.
- Limitations are disclosed (§7): the optimality of STEP at the operand-
    count level is a named gap (§7.1), and the translation's monotone drift
    of the garbage register is a named non-preservation (§7.4). The counting
    convention's sensitivity (§7.5) is explicitly flagged, not smuggled.
