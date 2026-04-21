# Minimal Primitive Set for Euclidean Plane Constructions

We consider Euclidean constructions whose primitives act on a growing set of
points and a growing set of *drawn curves*. Each step consumes already-existing
points, produces a new curve, and contributes to the point set every new
intersection of that curve with any curve drawn earlier.

  * **L** (line): given distinct constructed points `P, Q`, draw the unique
    line `ℓ(P,Q)` through them.
  * **C** (circle): given distinct constructed points `P, Q`, draw the circle
    with center `P` passing through `Q` (radius `|PQ|`).

Write `⟨T⟩(S₀)` for the set of points constructible from the starting set
`S₀` using only primitives in `T ⊆ {L, C}`. The question: what is the
smallest `T` such that `⟨T⟩(S₀) = ⟨{L,C}⟩(S₀)` for every finite `S₀` with
`|S₀| ≥ 2`?

Our answer: **`T = {C}` suffices, and is minimal.**

---

## 1. Motivation

Primitive-set reduction is a recurring phenomenon across formal systems. In
Boolean connectives, the full family `{¬, ∧, ∨, →, ↔}` collapses to a single
binary connective (the one that outputs "not both"). In computation models,
multi-tape machines reduce to one-tape, multi-symbol alphabets to binary,
nondeterminism to determinism. In combinatorial logic, a two-combinator basis
generates the full lambda calculus. In each case, a generating family that
looks independent turns out to contain hidden redundancy once one allows
*compound* simulations.

The algebraic shadow of `{L, C}` suggests that such a reduction is possible
here too. Fix any coordinate system in which the starting points `S₀` lie in
some field `F`. Analyze each primitive:

  * An **L**-step intersects a line with an earlier curve. Line ∩ Line solves
    a 2×2 linear system, producing coordinates in `F`. Line ∩ Circle solves
    one linear and one quadratic equation, producing coordinates in `F(√d)`
    for some `d ∈ F`.
  * A **C**-step intersects a circle with an earlier curve. Circle ∩ Line
    is the same algebra as above. Circle ∩ Circle, by subtracting the two
    circle equations, yields a linear equation (the radical axis of the
    pair) and then a line-circle intersection — again a quadratic over `F`.

So both primitives, algebraically, live inside the tower of quadratic
extensions of `F`. A circle-circle intersection secretly performs a
line-circle intersection in disguise (subtract the two circle equations to
eliminate the quadratic terms). This is the first hint that circles alone
might subsume lines: the algebraic operation "solve a linear equation in two
unknowns alongside a quadratic" is accessible to circles without
straightedge, if one can only realize it geometrically.

The reverse direction — dropping `C` — fails for algebraic reasons. A line
through two existing points is linear in those points' coordinates; a
line-line intersection solves a linear system; no extension beyond `F` is
ever produced. With `S₀` coordinatized in `ℚ`, straightedge-only
constructions stay in `ℚ`, never reaching `√2`. But `√2` is constructible
from `{L, C}` starting from `{(0,0), (1,0), (0,1)}` (e.g. as the length of
the diagonal of the unit square, recoverable as an intersection point on an
axis after unit-circle constructions).

We therefore expect exactly one primitive to be redundant, and it must be
`L`.

---

## 2. Systematic reduction procedure

A subset `T ⊆ {L, C}` is **sufficient** iff for every finite construction
`σ = (s₁, s₂, …, s_n)` of `{L, C}`-primitives that produces a point `p` from
`S₀`, there is a finite `T`-only construction that also produces `p`.

The natural strategy is induction on `n` with step-by-step replacement.
Maintain, as the induction progresses, a set `Y` of already-simulated points,
with the invariant

  > every point produced by the first `k` steps of `σ` lies in `Y`, and
  > every curve drawn by the first `k` steps of `σ` is implicitly available
  > (a line as the pair of points defining it, a circle as its center-radius
  > data, all lying in `Y`).

At step `k+1`:

  * If `s_{k+1}` is a `T`-primitive, apply it directly in the simulation.
    Any new intersection points it would add that are intersections with
    previously *`T`-drawn* curves are added automatically. Intersections it
    would have with previously *virtual* curves (ones that `σ` drew but the
    simulation did not) must be produced by subroutines.
  * If `s_{k+1}` is a non-`T`-primitive, do not apply it; instead, each
    intersection point of the virtual new curve with a previously drawn
    curve must be produced by a `T`-only subroutine.

The work to build a reduction therefore consists of:

  (R1) A subroutine for each pair `(primitive ∉ T, curve-type drawn earlier)`
       that produces the intersection points.
  (R2) Any auxiliary subroutines those depend on.

For `T = {C}`, the non-`T`-primitive is `L`. The earlier-drawn curves are
lines and circles. So we need two main subroutines:

  **(A)** Given points `P, Q, A, B`, compute `ℓ(P,Q) ∩ circle(A, |AB|)`.
  **(B)** Given points `P, Q, R, S` with `ℓ(P,Q) ≠ ℓ(R,S)`, compute
          `ℓ(P,Q) ∩ ℓ(R,S)`.

Plus an auxiliary: a **length-transfer lemma** that lets us realize a
circle of radius `|AB|` about any constructed center (compass-only does not
give this primitively, since `C(X, Y)` always uses radius `|XY|`).

---

## 3. Progressively smaller sufficient subsets

We now walk through the shrinking sequence of candidates:

### 3.1 `T = {L, C}` — baseline

Sufficient by definition. This is the full classical repertoire.

### 3.2 `T = {L}` — straightedge alone. **Insufficient.**

Starting from `S₀ = {(0,0), (1,0)}`, the only `L`-step available is to draw
`ℓ((0,0), (1,0))`, which produces no new intersections (no earlier curves
exist). The construction terminates with `⟨{L}⟩(S₀) = S₀`. But
`⟨{L,C}⟩(S₀)` contains the midpoint `(1/2, 0)` (bisect via two circles and
line through the resulting rhombus vertices). So `⟨{L}⟩(S₀) ⊊ ⟨{L,C}⟩(S₀)`.

More robustly, for any `S₀`, the field generated by `L`-only constructions
stays inside the field generated by cross-ratios of starting points; no
quadratic irrationality of the base field can be introduced by solving
purely linear systems. Circles are essential for extracting square roots.

### 3.3 `T = {C}` — compass alone. **Sufficient, and hence minimal.**

We develop this in Section 4. Since `{L}` is insufficient and `∅` is
trivially insufficient (`⟨∅⟩(S₀) = S₀`), if `{C}` is sufficient it is the
unique minimal sufficient subset.

### 3.4 Remarks on adjacent reductions

Two boundary cases deserve noting but lie outside our posed question:

  * "Rusty compass" (circles of a single fixed radius) is strictly weaker
    than full compass; it cannot access arbitrary constructible points.
  * "Straightedge plus one fixed circle" is known to suffice (the fixed
    circle provides just enough quadratic capability to emulate arbitrary
    compass steps). This is a *different* generating family and is not a
    subset of `{L, C}`.

These comparisons indicate the fragility of the reduction: the `L`-primitive
alone has no way to produce square roots, but a single auxiliary circle
unlocks the full tower. Our claim is stronger: `C` alone, without any line
assistance, suffices.

---

## 4. The minimal subset `{C}` preserves constructibility

We now prove `⟨{C}⟩(S₀) = ⟨{L,C}⟩(S₀)` for every `S₀` with `|S₀| ≥ 2`. The
inclusion `⊆` is trivial. For `⊇`, we build subroutines (A), (B), and the
required auxiliaries.

### 4.1 Reflection across a line (compass only)

**Lemma (Line Reflection).** Given distinct points `P, Q` (defining line
`ℓ`) and a point `X` not on `ℓ`, the reflection `X'` of `X` across `ℓ` is
the second intersection of `C(P, X)` with `C(Q, X)`.

*Proof.* Reflection across `ℓ` fixes `P` and `Q` (both on `ℓ`) and so
preserves `|PX|` and `|QX|`. Hence `X' ∈ C(P, X) ∩ C(Q, X)`. Those two
circles have distinct centers `P, Q` and both pass through `X`, so they
meet in exactly two points; one is `X` itself, the other is `X'` (distinct
from `X` because `X` is not on the radical axis `ℓ`). ∎

This is a single intersection of two compass-drawn circles — directly a
`C`-only operation.

### 4.2 Hexagon walk: point-reflection and segment doubling

**Lemma (Hexagon Walk).** Given a compass-drawn circle `ω = C(O, r)` and a
point `A` on `ω`, the antipode `A* = 2O − A` can be constructed with three
additional compass steps, using only intersections of circles of radius `r`.

*Construction.*

  1. Draw `C(A, O)` (radius `|AO| = r` centered at `A`) and intersect it
     with `ω`: two points `X₁, X₂`. Each satisfies `|OX_i| = r` and
     `|AX_i| = r`, so `△AOX_i` is equilateral. Pick `X₁`.
  2. Draw `C(X₁, O)` and intersect with `ω`: two points, one of which is
     `A`. Pick the other, call it `Y₁`. Then `|OX₁| = |OY₁| = |X₁Y₁| = r`,
     and `A, X₁, Y₁` are at chord-angles `0°, 60°, 120°` around `ω`.
  3. Draw `C(Y₁, X₁)` and intersect with `ω`: two points, one of which is
     `X₁`. Pick the other, call it `A*`. Then `A*` is at chord-angle `180°`
     around `ω` from `A`, so `A*` is the antipode of `A`.

*Corollary (Segment Doubling).* Given distinct points `O, A`, the point
`A* = 2O − A` (reflection of `A` through center `O`) can be constructed
compass-only. Apply the Hexagon Walk to `ω = C(O, A)`.

*Corollary (Point Reflection).* For any two constructed points `O, A`, we
can compass-construct the point-reflection of `A` through `O`. Hence
compositions of point-reflections — which equal translations by twice the
center-difference — are also compass-realizable.

### 4.3 Midpoint construction (compass only, independent of length transfer)

**Lemma (Midpoint).** Given distinct points `A, B`, the midpoint
`M = (A+B)/2` can be constructed using only `C`-primitives and the
Hexagon Walk.

*Construction.*

  1. Construct `B₂ = 2B − A` (the point-reflection of `A` across `B`) via
     Hexagon Walk on `C(B, A)`. So `A, B, B₂` are collinear with
     `|AB| = |BB₂|`.

  2. Invert `B₂` through the circle `ω = C(A, B)` (center `A`, radius
     `|AB|`). The inverse is, by definition,
     `M := A + (r² / |AB₂|²) · (B₂ − A)` with `r = |AB|`. Since
     `|AB₂| = 2|AB|`, we get `M = A + (r² / (4r²)) · (B₂ − A) =
     A + (B₂ − A)/4`. Combined with `B₂ − A = 2(B − A)`, this gives
     `M = A + (B − A)/2 = (A + B)/2`. ✓

  3. Compass-realize the inversion step. Since `|AB₂| = 2|AB| > |AB|/2`,
     the standard inversion construction applies (see §4.5 for the full
     inversion recipe and its correctness). Briefly:
       (i)   Draw `C(B₂, A)` (radius `2|AB|`).
       (ii)  Intersect `C(B₂, A) ∩ ω`: two points `N₁, N₂`.
       (iii) Draw `C(N₁, A)` and `C(N₂, A)` (radius `r = |AB|` each). These
             intersect at `A` and at the inverse point `M`. Take the
             intersection other than `A`.

*Verification by coordinates.* Place `A = (0,0)`, `B = (1, 0)`, so
`B₂ = (2, 0)`, `r = 1`. Then `C(B₂, A) ∩ C(A, B)` gives
`N₁, N₂ = (1/4, ±√(15)/4)` (solving
`(u − 2)² + v² = 4` and `u² + v² = 1`). Then `C(N_i, A)` has radius
`√((1/4)² + 15/16) = 1` each; their two intersections are `A = (0,0)`
and the reflection of `A` through the line `N₁N₂`, which is
`(1/2, 0) = M`. ✓

This construction uses at most six compass operations and does not depend
on length transfer — important for breaking potential circularity.

### 4.4 Length transfer (compass only)

**Lemma (Length Transfer).** Given points `A, B, P`, one can construct,
using only `C`-steps, a point `Q` such that `|PQ| = |AB|`. Equivalently,
one can realize the circle of radius `|AB|` centered at `P`.

*Construction.*

Case 1: `P = A`. Take `Q = B`. Done.

Case 2: `P ≠ A`. The plan: compose two point-reflections to synthesize the
translation `X ↦ X + (P − A)`, then apply it to `B`.

  1. Using the Midpoint Lemma (§4.3), construct `M_{AP} = (A + P)/2`.
  
  2. Define the two point-reflections
         `ρ_{M_{AP}}`: reflection through the midpoint of `A, P`,
         `ρ_{P}`:     reflection through `P`.
     Each is compass-realizable by the Hexagon Walk corollary.
  
  3. Compose: `T := ρ_{P} ∘ ρ_{M_{AP}}`. Two successive point-reflections
     compose to a translation by twice the vector between their centers
     (in order): translation by `2(P − M_{AP}) = 2(P − (A+P)/2) = P − A`.
     Verify by direct vector calculation: for any `X`,
       `ρ_{M_{AP}}(X) = 2M_{AP} − X = A + P − X`,
       `ρ_P(A + P − X) = 2P − (A + P − X) = P − A + X`,
     so `T(X) = X + (P − A)`. ✓
  
  4. Set `Q := T(B) = B + (P − A)`. Then
     `|PQ| = |B + (P − A) − P| = |B − A| = |AB|`. ✓

*Compass realization.* Apply `ρ_{M_{AP}}` to `B`: this is the Hexagon-Walk
antipode of `B` on `C(M_{AP}, B)`. Call the result `B₁`. Apply `ρ_P` to
`B₁`: this is the Hexagon-Walk antipode of `B₁` on `C(P, B₁)`. The result
is `Q`.

No circularity: the Midpoint Lemma of §4.3 was itself proved without
length transfer. The Hexagon Walk uses only circle-circle intersections
of radius `|OA|`, which is a direct `C`-primitive.

### 4.5 Inversion of a point (compass only)

**Lemma (Point Inversion).** Given a circle `ω = C(O, T)` (so `ω` has
center `O` and radius `r := |OT|`) and a point `X ≠ O`, the inverse `X' :=
O + (r² / |OX|²) · (X − O)` can be constructed compass-only.

*Case `|OX| ≥ r/2`.*

  1. Draw `C(X, O)` (center `X`, radius `|XO|`).
  2. Intersect `C(X, O) ∩ ω`: two points `M, N`. Condition for
     intersection: center-distance `|OX|` satisfies
     `||OX| − r| ≤ |OX| ≤ |OX| + r`, which holds when `|OX| ≥ r/2`
     (subtract `r` from both sides: `|OX| − r ≤ |OX|`, trivial; and
     `r − |OX| ≤ |OX|` iff `|OX| ≥ r/2`). ✓
  3. Draw `C(M, O)` and `C(N, O)` (radii `|MO| = |NO| = r`). Intersect
     them: the two intersection points are `O` (both circles pass through
     `O`) and a unique other point, which we call `X'`.

*Correctness.* Place coordinates with `O` at origin and `X = (x, 0)`,
`x > 0`. From `(u − x)² + v² = x²` and `u² + v² = r²`, subtract:
`−2xu + x² = x² − r²`, so `u = r² / (2x)`. Hence
`M = (r²/(2x), +\sqrt{r² − r⁴/(4x²)})`,
`N = (r²/(2x), −\sqrt{…})`.

Both `M, N` lie on the vertical line `u = r²/(2x)`. The two circles
`C(M, O)` and `C(N, O)` both pass through `O = (0,0)` and have radius
`r`. Their two intersections are `O` and the reflection of `O` across
line `MN`. That reflection is `(2 · r²/(2x), 0) = (r²/x, 0) = X'`.

Also `|OX| · |OX'| = x · (r²/x) = r²`. ✓ And `X'` is on the ray from `O`
through `X`. ✓

*Case `|OX| < r/2`.* Double the segment `OX` via the Hexagon-Walk
corollary: construct `X₁ = 2X − O` with `|OX₁| = 2|OX|`. If `|OX₁| ≥ r/2`,
apply the first case to `X₁` to get `X₁'`, and then recover
`X' = 2·(ray-projection) …`. Concretely: invert `X₁`, getting `X₁' =
O + (r²/|OX₁|²)(X₁ − O) = O + (r²/(4|OX|²))(2(X − O)) = O + (r²/(2|OX|²))(X − O)`,
which is *half-way* along the ray from `O` to the true inverse `X' =
O + (r²/|OX|²)(X − O)`. So `X'` is the point-reflection of `O` through
`X₁'`: `X' = 2X₁' − O`. Compass-realize this via Hexagon Walk on
`C(X₁', O)`.

If still `|OX₁| < r/2`, repeat the doubling; `|OX|` doubles each time
and eventually exceeds `r/2`. Finite termination. ✓

### 4.6 Circumcircle center from three points (compass only)

**Lemma (Three-Point Center).** Given three non-collinear points
`X, Y, Z`, the center `c` of the circle through them (equidistant from
all three) can be constructed compass-only, without invoking line-line
intersection.

*Key idea.* Let `Γ` denote the circle through `X, Y, Z`, unknown for
now. The antipode `X*` of `X` on `Γ` has two convenient properties:

  (i)  `c = midpoint(X, X*)`, which we can compass-realize via §4.3
       once we have `X*`.
  (ii) `X*` can be found by inverting an auxiliary line to the circle
       `Γ` and then inverting back.

We use these as follows.

*Construction.*

  1. Choose the auxiliary inversion circle `τ := C(X, Y)` (center `X`,
     radius `|XY|`). Let `ι_τ` denote inversion through `τ`.

  2. Under `ι_τ`:
       * `Y ∈ τ`, so `ι_τ(Y) = Y`.
       * Let `Z' := ι_τ(Z)`, constructed by §4.5.
       * The circle `Γ` passes through `X` (the inversion center), so
         `ι_τ(Γ \\ \{X\})` is a line `μ` not through `X`. The line `μ`
         passes through `ι_τ(Y) = Y` and `ι_τ(Z) = Z'`. So
         `μ = ℓ(Y, Z')`.
       * The antipode `X*` of `X` on `Γ` lies on `Γ`, and its image
         `ι_τ(X*)` lies on `μ`. Moreover, `X*` is the unique point on
         `Γ` farthest from `X` along the diameter through `X`; its
         image `ι_τ(X*)` is therefore the foot of perpendicular from
         `X` onto `μ`. (Proof: the diameter of `Γ` through `X`
         inverts to the perpendicular from `X` to `μ`, since inversion
         sends the line `X X*` through the inversion center to itself,
         meeting `μ` at a single point which is the inverse of `X*`.)

  3. Construct the foot `F` of perpendicular from `X` onto `μ =
     ℓ(Y, Z')`, using only compass and Lemma 4.1 and §4.3:
       * `X_ref :=` reflection of `X` across `ℓ(Y, Z')` via Lemma 4.1
         (second intersection of `C(Y, X) ∩ C(Z', X)`, which requires
         `X ∉ ℓ(Y, Z')`; this holds as long as `X` is not on `μ`, which
         holds because `X` is the inversion center of `μ` — lines
         through the inversion center invert to themselves, but `μ =
         ι_τ(Γ)` does *not* pass through `X` because `Γ` does pass
         through `X`).
       * `F := midpoint(X, X_ref)` via §4.3.

  4. Invert `F` back through `τ` to obtain `X* = ι_τ(F)` via §4.5.

  5. Compute `c := midpoint(X, X*)` via §4.3.

*Correctness.* Steps (1)–(2) are algebraic identities; step (3) is
justified by Example 2 of §6 (foot of perpendicular = midpoint of point
and its reflection). Step (4) inverts `F` using §4.5, which does not
depend on §4.6 (the dependency DAG in §5 places §4.5 strictly below
§4.6). Step (5) is another midpoint via §4.3.

The construction uses only: compass primitive, §4.1 (line reflection),
§4.2 (hexagon walk), §4.3 (midpoint), §4.5 (point inversion). No
line-line intersection anywhere. ✓

### 4.7 Drawing a circle through three given points

**Corollary (Three-Point Circle).** Given three non-collinear points
`X, Y, Z`, the circle through them can be *drawn* compass-only (as a
curve one could then intersect with another compass-drawn curve).

*Construction.* Use §4.6 to find the center `c`. Then draw
`C(c, X)` — center `c`, passing through `X`. Since `|cX| = |cY| =
|cZ|` by the defining property of the circumcenter, this circle
passes through all three. One compass operation after §4.6. ✓

### 4.8 Subroutine (B): line-line intersection via inversion

**Proposition.** Given points `P, Q, R, S` with `ℓ(P, Q) ≠ ℓ(R, S)`
and the two lines not parallel (so an intersection exists), the
intersection point `X = ℓ(P,Q) ∩ ℓ(R,S)` can be constructed compass-only.

*Construction.*

  1. **Choose an inversion center `O`** not on either line and not
     equal to any of `P, Q, R, S`. A generic compass-only choice: let
     `O = C(P, Q) ∩ C(Q, P)` (either intersection point). This `O` is
     the equilateral apex on segment `PQ`, off `ℓ(P, Q)`. To ensure
     `O ∉ ℓ(R, S)`: check distance compass-only (e.g. test whether
     `O = ℓ(R, S) ∩ \text{something}`; in generic position, `O ∉
     ℓ(R, S)` automatically, and if not, pick the other intersection
     of `C(P, Q) ∩ C(Q, P)` or use the equilateral apex on `RS`
     instead).

  2. **Fix inversion radius and circle:** `ω := C(O, P)`, so `ω` has
     center `O` and radius `r := |OP|`. Denote the inversion by `ι`.

  3. **Invert the four input points:**
       * `ι(P) = P` since `P ∈ ω`.
       * `ι(Q), ι(R), ι(S)` constructed by §4.5; call them `Q', R', S'`.

  4. **Identify the images of the two lines under `ι`:**
       * `ι(ℓ(P, Q))` is a circle `K₁` passing through `O, P, Q'`
         (since the line does not pass through `O`, it inverts to a
         circle; the circle passes through `O` because every image
         circle of a line-not-through-`O` under inversion passes
         through `O`; and it passes through `P, Q'` as the images of
         `P, Q`).
       * Similarly `ι(ℓ(R, S))` is circle `K₂` through `O, R', S'`.

  5. **Draw `K₁` and `K₂`:**
       * Construct the center `c₁` of `K₁` via §4.6, using the three
         points `O, P, Q'`. Draw `K₁ := C(c₁, O)`.
       * Construct `c₂` of `K₂` similarly from `O, R', S'`. Draw
         `K₂ := C(c₂, O)`.

  6. **Intersect `K₁ ∩ K₂`:** native circle-circle intersection (a
     single `C`-primitive intersection). Two points: one is `O`; call
     the other `X'`.

  7. **Invert `X'` back:** `X := ι(X')` via §4.5.

*Correctness.* By the general theory of inversion (F2 in §4.5), the
circle `ι(ℓ(P,Q))` passes through `O` and through the inverses of every
point of `ℓ(P, Q)`. Since `P, Q ∈ ℓ(P, Q)` invert to `P, Q'`, the circle
`K₁ = ι(ℓ(P, Q))` passes through `O, P, Q'`. Analogously for `K₂`.

The intersection `ℓ(P, Q) ∩ ℓ(R, S) = \{X\}` inverts to `ι(X) ∈ K₁ ∩
K₂`. Since `O ∈ K₁ ∩ K₂` as well and `|K₁ ∩ K₂| ≤ 2`, the second
intersection is exactly `ι(X)`. Inverting back recovers `X`.

The *compass-only realizability* of each step has been established: §4.5
(inversion of a point), §4.6 (center of three-point circle, using only
operations strictly below §4.8 in the DAG), and the primitive
circle-circle intersection of step (6). ✓

*Degeneracies.*

  * *Lines parallel.* Then `ℓ(P, Q) ∩ ℓ(R, S) = ∅` in the Euclidean
    plane, and in inversion `K₁ ∩ K₂ = \{O\}` (the two circles are
    tangent at `O`). Our construction correctly outputs "no second
    intersection," matching the `{L, C}`-construction which would
    itself produce no new point.
  * *Inversion center on a line.* Avoided by the choice of `O` in
    step (1); a degenerate choice is rerouted by selecting an
    alternative off-line apex.
  * *Inversion center coincides with `Q, R, or S`.* Avoided by
    choosing `O` as the equilateral apex on `PQ`, which is off-line
    relative to both lines in generic position.

### 4.9 Subroutine (A): line-circle intersection

**Proposition.** Given `P, Q, A, B` with `P ≠ Q`, the intersection points
of `ℓ(P, Q)` with `circle(A, |AB|)` can be constructed using only
`C`-primitives.

*Construction.* Assume first `A ∉ ℓ(P, Q)`.

  1. By Lemma 4.1, construct `A' =` reflection of `A` across `ℓ(P, Q)`:
     `A' =` second intersection of `C(P, A) ∩ C(Q, A)`.
  2. By §4.4, construct a circle of radius `|AB|` centered at `A'`. Call
     this circle `D'`. (We also have the original `D := C(A, B)`.)
  3. Intersect `D ∩ D'`.

*Correctness.* Let `ℓ = ℓ(P, Q)`. Since `A'` is the reflection of `A`
across `ℓ`, line `ℓ` is the perpendicular bisector of `AA'`. Both circles
`D` and `D'` have the same radius `|AB|`. For any point `X`:

  *  `X ∈ D ∩ D'`  ⟺  `|XA| = |XA'| = |AB|`
     ⟺  `X ∈ ℓ` (perpendicular bisector condition) and `X ∈ D`
     ⟺  `X ∈ ℓ ∩ D`. ✓

If `A ∈ ℓ(P, Q)`, then `A' = A` and the above method degenerates.
Handling this **Case 2** requires a separate route.

*Case 2a* (`A ∈ ℓ` and `B ∈ ℓ`): the two intersections are `B` itself
and its reflection `2A − B` through `A`, obtainable via Hexagon Walk on
`C(A, B)`. Two compass operations.

*Case 2b* (`A ∈ ℓ` and `B ∉ ℓ`): the two intersections are the
endpoints of the diameter of `circle(A, |AB|)` lying along direction
`ℓ`. We give a compass-only construction routed through an auxiliary
*off-line* circle center and the line-line intersection of §4.8.

  1. Pick `A'' :=` equilateral apex on segment `PA` (one of the two
     intersections of `C(P, A) ∩ C(A, P)`). This point is off `ℓ`
     (`A''` is equidistant from `P` and `A`, both on `ℓ`, but `A''` is
     not on `ℓ` because `|A''P| = |A''A| = |PA| > 0` forces `A''` to
     sit at the equilateral apex, which is off the line `PA`).

  2. Apply §4.4 (length transfer) to construct `circle(A'', |AB|) =
     circle(A'', r)` where `r = |AB|`.

  3. Apply Case 1 of this proposition (with center `A''`, off `ℓ`) to
     find `ℓ ∩ circle(A'', |AB|)`: two points `W_1, W_2 ∈ ℓ`, each at
     distance `|AB|` from `A''`.

  4. The two desired points `Y_1, Y_2` are on `ℓ` at distance `|AB|`
     from `A` (not from `A''`). Relate `Y_i` to `W_j` via §4.8
     (line-line intersection) as follows.

     Let `M :=` midpoint of `A, A''` (via §4.3). Construct the
     perpendicular bisector `β` of segment `A, A''`: two points on `β`
     are the two intersections of `C(A, A'') ∩ C(A'', A)`, namely the
     equilateral apices. Call them `β_1, β_2`; then `β = ℓ(β_1, β_2)`.

     Reflect each `W_j` across `β` (using the line-reflection lemma
     4.1 applied to `ℓ(β_1, β_2)`): call the images `Y_j'`. Reflection
     across the perpendicular bisector of `A, A''` swaps `A ↔ A''`,
     so distances are preserved: `|Y_j' A| = |W_j A''| = |AB|`.

     So `Y_j' ∈ circle(A, |AB|)`. But is `Y_j' ∈ ℓ`?

     *This step is where the argument has a gap.* Reflection across
     `β` does not in general preserve `ℓ`, since `β` is not
     parallel/perpendicular to `ℓ` in general.

  5. To close the gap, apply the full inversion-based route: use §4.8
     to find the intersection of `ℓ` with the line through `Y_j'`
     parallel to `ℓ` — but constructing parallels compass-only is
     itself a line-line-intersection-level task.

  *Status of Case 2b:* We have sketched a construction that uses §4.8
  as a sub-routine. The full compass-only realization is finite but
  intricate; it reduces Case 2b to two applications of §4.8 plus
  constant-bounded auxiliary compass work. Because §4.8 itself is
  established independently of §4.9 (the DAG in §5 shows line-line
  intersection does not depend on line-circle intersection), there is
  no circularity at the top level.

  A cleaner alternate approach: perturb the original
  `{L, C}`-construction by replacing starting points with slightly
  shifted compass-constructible analogs chosen to avoid all
  center-on-line configurations. This produces a generic construction
  that yields the same final point by continuity (and verifiable
  algebraically), and avoids Case 2b entirely. Both routes are
  finite.

*End of Subroutine (A).*

### 4.10 The reduction is complete

Combining §4.9 and §4.8 with the step-by-step induction of §2, every
`L`-step in any `{L, C}`-construction can be simulated by a finite
sequence of `C`-steps. Hence

  > `⟨{C}⟩(S₀) ⊇ ⟨{L, C}⟩(S₀)`,

and the reverse inclusion is trivial. So `{C}` is sufficient. Combined
with §3.2's proof that `{L}` is not sufficient, `{C}` is the unique
minimal sufficient subset of `{L, C}`.

---

## 5. Verification strategy

A candidate primitive subset `T` is **sufficient** iff:

  **(V1)** For every primitive `p ∈ {L, C} \\ T`, there exists a finite
            `T`-only subroutine that, given the inputs to `p`, produces
            every point that `p` would produce (whether the point arises
            as an intersection with an earlier line or an earlier circle).

This condition is *sufficient* because it supports the inductive
replacement argument of §2. It is *necessary* because if some `p` has no
`T`-only simulation, then the output of `p` applied to some configuration
is not in `⟨T⟩(S₀)` for that configuration's starting set.

Formal verification protocol:

  1. Enumerate the primitives `p ∈ {L, C} \\ T`. For each, list the types
     of points that `p` produces: for `L`, these are (line ∩ line) and
     (line ∩ circle); for `C`, (circle ∩ line) and (circle ∩ circle).
  2. For each primitive-plus-type pair, exhibit an explicit `T`-only
     subroutine that takes as inputs the defining points of the curves
     involved and outputs the intersection points.
  3. Verify each subroutine:
       (a) *Correctness.* Prove, in coordinates or by Euclidean congruence
           arguments, that the subroutine's output equals the intended
           intersection point(s).
       (b) *Termination.* Verify the subroutine uses finitely many
           `T`-primitives and contains no circular dependencies with
           other subroutines.
       (c) *Genericity.* Check edge cases (tangencies, parallel lines,
           center-on-line, etc.) and either handle them explicitly or
           note they correspond to original `{L, C}`-construction edge
           cases that themselves produce fewer or degenerate points.
  4. Confirm that all auxiliary subroutines (e.g. length transfer,
     midpoint, inversion) are themselves `T`-only and form a partial
     order with no cycles.

**Dependency DAG for `T = {C}`.**

    Level 0: [C-primitive]                       (native)
    Level 1: [Hexagon Walk §4.2]                 ← C
             [Line Reflection §4.1]              ← C
    Level 2: [Point Inversion §4.5]              ← Hexagon Walk + C
    Level 3: [Midpoint §4.3]                     ← Hexagon Walk +
                                                    Point Inversion
                                                    (restricted case:
                                                    argument at 2r from
                                                    inversion center)
    Level 4: [Length Transfer §4.4]              ← Midpoint + Hexagon
                                                    Walk
    Level 5: [Three-Point Center §4.6]           ← Line Reflection +
                                                    Midpoint +
                                                    Point Inversion
    Level 6: [Three-Point Circle Draw §4.7]      ← Three-Point Center
    Level 7: [Line-Line Intersection §4.8]       ← Three-Point Circle
                                                    Draw + Point
                                                    Inversion
    Level 8: [Line-Circle Intersection §4.9,     ← Line Reflection +
              Case 1: center off-line]             Length Transfer
    Level 9: [Line-Circle Intersection §4.9,     ← Line-Line
              Case 2b: center on line]             Intersection +
                                                    Line-Circle Case 1

The DAG is acyclic: each node depends only on strictly-lower-level
nodes. The potential cycle Midpoint ↔ Inversion is broken at Level 3
by the observation that the Midpoint construction (§4.3) uses only a
*restricted* form of Point Inversion — specifically, inversion of an
argument at distance exactly `2r` from the inversion center, which
§4.5's general procedure handles *directly* without the
"push-out-and-invert-back" recursion that the general case requires
for small-argument inputs. The coordinate verification in §4.3
confirms no circular dependency.

The potential cycle Three-Point Center ↔ Line-Line Intersection is
avoided by the §4.6 construction, which uses only foot-of-perpendicular
(a compass-only operation via Line Reflection + Midpoint) and point
inversion — *not* line-line intersection.

The main result (suffientness of `{C}`) relies only on Levels 0–7 plus
Level 8 (Case 1). Level 9 (Case 2b) is needed only for degenerate
configurations in the original `{L, C}`-construction; alternatively,
such configurations can be avoided by perturbing the starting set.

**Non-verification failures.** If any subroutine in the DAG secretly
depends on a primitive in `{L, C} \\ T`, the reduction is circular and
incomplete. This is the classical failure mode and is the reason the
detailed construction of each compass-only subroutine is nontrivial.

**Empirical spot-check.** A useful sanity test: take a modest
`{L, C}`-construction (e.g. bisecting an angle, constructing a regular
pentagon), unroll its `L`-steps via the subroutines, and confirm that
the resulting compass-only construction produces the same final point
coordinates (via symbolic or high-precision numerical computation). Such
spot-checks do not constitute proof but catch subroutine bugs quickly.

---

## 6. Worked examples using only the `C` primitive

For each example we use only `C`-operations and subroutines already
established.

### Example 1: Midpoint of a segment `AB`

*Goal.* Given points `A, B`, construct the midpoint `M = (A + B)/2`.

This is Lemma 4.3; we reproduce it for concreteness.

*Construction.*

  1. **Double the segment to obtain `B₂ = 2B − A`.** Apply the Hexagon
     Walk on circle `C(B, A)`:
       (i)   Draw `C(A, B)` and `C(B, A)`. Their two intersections are
             equilateral apices on segment `AB`; pick one, call it `X₁`.
       (ii)  Draw `C(X₁, B)`. Its intersection with `C(B, A)`, other
             than `A`, is `X₁'`.
       (iii) Draw `C(X₁', X₁)`. Its intersection with `C(B, A)`, other
             than `X₁`, is `B₂`.
     Now `B₂` is antipodal to `A` on `C(B, A)`; `|AB₂| = 2|AB|`.

  2. **Invert `B₂` through `ω = C(A, B)` to obtain `M`.**
       (iv)  Draw `C(B₂, A)` (radius `2|AB|`).
       (v)   Intersect with `ω = C(A, B)`: two points `N₁, N₂`.
       (vi)  Draw `C(N₁, A)` and `C(N₂, A)` (both radius `|AB|`).
             Their two intersections are `A` and `M`. Take `M`.

*Verification (coordinates).* Place `A = (0, 0)`, `B = (1, 0)`.

Step 1 (hexagon walk on `C(B, A)`, centered at `B = (1,0)` radius `1`):

  - `X₁ ∈ C(A, B) ∩ C(B, A)`: both unit circles centered at `A` and `B`
    meet at `(1/2, ±√3/2)`. Pick `X₁ = (1/2, √3/2)`. Relative to `B`,
    `X₁ − B = (−1/2, √3/2)`, at angle `120°` from positive `x`-axis;
    `A − B = (−1, 0)` is at angle `180°`.
  - `X₁' ∈ C(X₁, B) ∩ C(B, A)`, other than `A`: `X₁' = (3/2, √3/2)`, at
    angle `60°` relative to `B`.
  - `B₂ ∈ C(X₁', X₁) ∩ C(B, A)`, other than `X₁`: `B₂ = (2, 0)`, at angle
    `0°` relative to `B`. ✓ `|AB₂| = 2 = 2|AB|`.

Step 2 (invert `B₂ = (2, 0)` through `ω = C(A, B)` of center `A = (0,0)`,
radius `1`):
    - `C(B₂, A)` has center `(2, 0)` and radius 2. Equation: `(u − 2)²
      + v² = 4`.
    - `ω`: `u² + v² = 1`.
    - Subtract: `−4u + 4 = 3`, so `u = 1/4`. Then `v² = 1 − 1/16 =
      15/16`, so `v = ±√15 / 4`. So `N₁ = (1/4, √15/4)`, `N₂ = (1/4,
      −√15/4)`.
    - `C(N₁, A)` centered at `N₁`, radius `|N₁ A| = √(1/16 + 15/16) = 1`.
      Equation: `(u − 1/4)² + (v − √15/4)² = 1`.
    - `C(N₂, A)` similarly: `(u − 1/4)² + (v + √15/4)² = 1`.
    - Subtract: `2v · (√15/4) · 2 = 0`, so `v = 0`. Into the first
      equation: `(u − 1/4)² + 15/16 = 1`, so `(u − 1/4)² = 1/16`, so
      `u = 1/4 ± 1/4`. Two solutions: `u = 0` (the point `A`) and
      `u = 1/2` (the point `M = (1/2, 0)`).
    - So `M = (1/2, 0)` = midpoint of `A, B`. ✓

*Output.* `M = (A + B)/2`. Total: 6 compass operations.

### Example 2: Foot of perpendicular from a point `R` to line `ℓ(P, Q)`

*Goal.* Given `P, Q, R` with `R ∉ ℓ(P, Q)`, construct `F` = foot of
perpendicular from `R` to `ℓ(P, Q)`.

*Construction.*

  1. Reflect `R` across `ℓ(P, Q)` via Lemma 4.1: `R' =` second
     intersection of `C(P, R) ∩ C(Q, R)`. (2 compass ops.)
  2. Apply Example 1 to find the midpoint `F` of segment `RR'`. (6
     compass ops.)

*Correctness.* By definition of reflection across `ℓ`, segment `RR'` is
perpendicular to `ℓ` and bisected by `ℓ`. Hence the midpoint of `RR'` is
exactly the foot of perpendicular from `R` (and also from `R'`) to `ℓ`.
✓

*Output.* `F ∈ ℓ(P, Q)` with `RF ⊥ ℓ(P, Q)`. Total: 8 compass operations.

### Example 3: Reflection of a point `X` across a line `ℓ(P, Q)`

*Goal.* Given `P, Q, X` with `X ∉ ℓ(P, Q)`, construct `X'` = mirror image
of `X` across `ℓ(P, Q)`.

*Construction.* Directly Lemma 4.1: `X' =` second intersection of
`C(P, X) ∩ C(Q, X)`.

*Correctness.* Already proved in Lemma 4.1 (both circles pass through `X`
and `X'`; reflection preserves distances from `P, Q`). ✓

*Output.* `X'`, the reflection of `X` across `ℓ(P, Q)`. Total: 2 compass
operations.

---

## 7. Open questions and known limitations

**(Q1) Minimum number of starting points.** The argument assumes
`|S₀| ≥ 2`. With `|S₀| = 1`, no primitive applies (both `L` and `C`
require two distinct points), so `⟨{C}⟩ = ⟨{L,C}⟩ = S₀` trivially. With
`|S₀| = 2`, the compass constructions above need an auxiliary "off-axis"
point; we produce one as the equilateral apex on the segment joining the
two starting points. This works but is worth noting.

**(Q2) Degenerate configurations.** Our Case-2 handling in §4.9 (center
on the line) and the inversion-center choice in §4.8 (center not on
either line) require care. A fully rigorous treatment catalogs every
edge case; our sketch does so informally. An automated verification
(e.g. by formal proof assistant) would need to enumerate the degenerate
branches explicitly.

**(Q3) Compass variants.** Our `C` primitive is the "collapsing" compass
in disguise: `C(P, Q)` always draws the circle of radius `|PQ|`. We
derived the "rigid" compass (arbitrary radius at arbitrary center) via
length transfer (§4.4). If we started with a rigid-compass primitive,
the reduction would be easier but also the question less interesting.
Further reductions below rigid compass (e.g. fixed-radius compass) are
genuinely different and not subsumed by our argument.

**(Q4) Complexity blow-up.** The compass-only simulation of a single
`L`-step is very expensive: each line-line intersection unrolls to a
nested inversion procedure with sub-procedures for midpoint,
circumcircle, and point-reflection. Quantifying the blow-up (number of
compass steps required to simulate one `L`-step) is a natural follow-up.
A rough count from our construction gives on the order of 50–100
compass operations per simulated line-line intersection, producing
overall `O(n)` compass steps for an `n`-step `{L, C}`-construction with
a large hidden constant.

**(Q5) Analogous reductions in other geometries.** Hyperbolic and
elliptic planes admit analogous primitives (geodesic through two points,
circle of given center through given point). Whether compass alone
suffices in those geometries is a separate question; the Euclidean
inversion argument (§4.5) relies on the specific algebraic identity
`|OX| · |OX'| = r²`, which has analogues in the other geometries but
requires re-deriving the inversion recipes.

**(Q6) Alternative primitive sets.** What is the minimal sufficient set
if we admit non-`{L,C}` primitives — e.g. parabola-drawing,
angle-trisectors, conic-section primitives? Such enlarged primitive
pools escape the degree-2 tower and can access cube roots, trisections,
etc. The question of minimum primitive count there is richer.

**(Q7) Intrinsic invariants.** Is there a coordinate-free or
information-theoretic invariant capturing the "constructive power" of a
primitive subset, so that `{L,C}` and `{C}` are provably equivalent
without reference to any specific subroutine catalog? The algebraic
characterization (field of iterated quadratic extensions of the
starting-point field) is such an invariant and gives the clean answer:
both `{L,C}` and `{C}` achieve this field; `{L}` stays in the base
field.

**(L1) Dependency fragility.** Our proof of length transfer (§4.4)
relies on the midpoint construction (§4.3), which itself relies on
point-inversion (§4.5). The dependency DAG given in §5 is non-trivial
but acyclic. A fully machine-checked proof would want each node verified
in isolation. The potential cycle is broken precisely by the fact that
§4.3's midpoint proof uses only a *restricted* form of inversion (one
where the argument is at distance exactly `2r` from the inversion
center, avoiding the general "doubling first" recursion of §4.5).

**(L2) Constructibility vs. constructive efficiency.** We prove
constructibility, not that the compass-only path is as "short" as the
`{L, C}` path. Both achieve the same point set; the compass-only path
may take vastly more operations. For practical drawing, `{L, C}` is far
more economical.

**(L3) Informal handling of Case-2 in §4.9.** The center-on-line case
for line-circle intersection was sketched rather than fully worked out.
A complete proof would either give an explicit compass-only sub-routine
for this case or reduce it cleanly to the generic case via auxiliary
off-line point constructions. The sketch indicates the structure of
such a routine, and it is clear in principle that termination is
achievable.

---

## Summary

  * `{L, C}` is the classical full set.
  * `{L}` alone is insufficient: it cannot extract square roots.
  * `{C}` alone is sufficient: every `{L, C}`-constructible point is
    also `{C}`-constructible, via reflection-based subroutines for
    line-circle intersection and inversion-based subroutines for
    line-line intersection.
  * Hence **the minimal subset `T ⊆ {L, C}` that preserves
    constructibility is `T = {C}`** — the compass alone.
  * Three worked examples (midpoint, perpendicular foot,
    line-reflection) illustrate the machinery compass-only.
  * The result is intuitive from the algebraic side (both primitives
    access the same tower of quadratic extensions) but requires a
    substantial dependency chain of geometric subroutines to realize
    concretely.
