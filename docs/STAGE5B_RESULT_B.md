# Stage 5B-2 — Limited Result B: global sectors do not supply a microscopic nearest-neighbour channel

## Status

This note freezes the negative result reached after Stage 5A. It deliberately stops **before** any fermionic kernel `K` is proposed.

Stage 5A established a candidate global precursor

\[
(C,\prec)\longrightarrow \{U,V\}/S_2,
\]

where `U` and `V` are two global total orders on the same event set. They are **not** a local spinor fiber and must not be called chirality.

Stage 5B-2 asks a narrower question: can those global sectors be turned into a microscopic link-by-link nearest-neighbour propagation rule using only intrinsic causal-set data?

## 1. Three-valued rank diagnostic

For a causal link `x <. y`, let `r_U,r_V` be ranks in the two Stage-5A total orders and define

\[
\Delta r_U=r_U(y)-r_U(x),\qquad
\Delta r_V=r_V(y)-r_V(x).
\]

The only `U<->V`-covariant comparison of these two numbers is

\[
\chi(x\lessdot y)=
\begin{cases}
U,&\Delta r_U>\Delta r_V,\\
V,&\Delta r_V>\Delta r_U,\\
\bot,&\Delta r_U=\Delta r_V.
\end{cases}
\]

A tie cannot be silently assigned to `U` or `V`: under the global sector swap a tie remains a tie, so any forced two-valued tie-break would introduce extra structure.

In the fixed source-of-record run in `analysis/stage5b_link_channel.py` (`N=300`, seed `55002`), there are 1328 links, 16 rank ties (1.20%), and the non-tie rank diagnostic agrees with the sealed continuum comparison `sign(Delta u-Delta v)` on about 97.4% of links. This shows that `chi` is a useful **global diagnostic**. It does not show that `chi` is local chirality.

## 2. What the conformal argument does and does not prove

In 1+1D,

\[
u\mapsto f(u),\qquad v\mapsto g(v)
\]

with strictly increasing `f,g` preserves every causal-order relation. Therefore a metric target such as whether `|Delta u|>|Delta v|` is not pure-order data.

This must **not** be over-read as saying the channel concept is meaningless or that order+number cannot recover metric information. A conformally distorted coordinate image of a uniform sprinkling is generally not a uniform sprinkling for the transformed volume form. The correct reading is the standard causal-set one: order supplies conformal structure; number supplies volume information needed to select metric scale/representative.

The fixed numerical witness applies `u -> u^3`, `v -> v^(1/4)`. The causal matrix and all ranks remain bitwise unchanged while the sealed coordinate metric comparison flips on 150 of 1328 links. This is a sanity witness for the scope statement above, not the proof that order+number fails.

## 3. The actual project-level obstruction: the rank diagnostic is not microscopic link-local

For a link, the open Alexandrov interval `I(x,y)` is empty by definition. The rank gaps nevertheless count elements in null-coordinate strips extending outside that empty interval. Hence the estimator gets volume information by looking beyond the link itself.

The source-of-record intervention makes this dependence constructive. For a link classified `U`, add elements with

\[
u_w<u_x,\qquad v_x<v_w<v_y.
\]

They leave all pre-existing order relations unchanged, preserve `x<.y` as a link, leave `Delta r_U` unchanged, and increase only `Delta r_V`. The `V` case is obtained by exchanging `U` and `V`. Merely saying that the new points are outside `I(x,y)` is **not** an independent remoteness test: if an added point entered the open interval, the target pair would cease to be a link. The benchmark therefore measures a separate, purely order-theoretic quantity for every added point `w`,

\[
|I(w,y)\cap C_{\rm old}|,
\]

counting only pre-existing events between `w` and `y`. The 60 intervention targets are selected only when **every** added point has this count at least 5. In the fixed run, 60/60 selected links flip channel; 320 points are added in total, the median is 5.5 added points per link, and the order-depth counts over all added points have min/median/max `5 / 8 / 21`. Thus the evidence is accurately described as an **order-separated link-external intervention**, not merely as "outside the empty link interval" and not as an unquantified claim of macroscopic remoteness. This is a constructive witness that this rank-based `chi` is **not** a microscopic link-local rule.

This does **not** prove that every possible local two-state internal space is impossible.

## 4. Independent literature constraint: BHS

Bombelli, Henson & Sorkin, *Discreteness without symmetry breaking: a theorem* (arXiv:gr-qc/0605006), prove for Poisson sprinklings of full Minkowski spacetime that there is no measurable Lorentz-equivariant map from a sprinkling to a spacetime direction (Theorem 1). They further state that no finite set of timelike/spacelike directions at a point can be associated consistently with Lorentz invariance, and infer that a finite-valency graph cannot be assigned to the sprinkling in a Lorentz-invariant way.

This is stronger and cleaner than trying to rescue a checkerboard nearest-neighbour construction by a better local tie-break. It removes the following mainline target:

> intrinsically select one finite `U` neighbour and one finite `V` neighbour at each event and use them as a Lorentz-equivariant nearest-neighbour walk.

Scope: BHS applies strictly to **full Minkowski sprinklings**. Finite causal diamonds contain boundary information and may admit boundary-induced preferred directions; such constructions are not evidence for an intrinsic full-spacetime local rule.

## 5. Result B — accepted scope

**【Stage 5B Result B / limited No-Go】**

1. Stage 5A can provide a highly canonical pair of **global** null-order sectors at tested finite `N`.
2. A metric link-direction target is not pure-order data; number/volume information is needed.
3. The tested rank-based three-valued `chi` obtains that information from population outside the empty link interval and is therefore not a microscopic link-local rule; order-separated link-external interventions can flip it without breaking the link or altering any old-old relation.
4. Independently, BHS rules out an intrinsic Lorentz-equivariant finite-direction / finite-valency nearest-neighbour construction on a full Minkowski sprinkling.

**The No-Go does not claim that any local two-state internal space is impossible.**

The next allowed question is therefore not another nearest-neighbour classifier. It is whether the globally derived pair `U,V` can be used merely as a two-component bookkeeping fiber while all nontrivial dynamics resides in an intrinsically **nonlocal** two-sector kernel. That question belongs to Stage 5C and is outside this commit.

## 6. Explicit retractions retained

The following stronger statements were considered and are **not** part of the result:

- "number is a volume quantity, therefore every order+number construction is necessarily nonlocal" — **retracted**. Counting can be performed on finite regions. The precise obstruction here is that a link's own Alexandrov interval is empty, so this estimator must reach outside it.
- "therefore no local two-state internal fiber can exist" — **not established**.
- "a successful 1+1D two-sector construction can be extrapolated to 3+1D" — **not established**. In 3+1D the relevant Weyl/Dirac structure is a local Lorentz/Clifford representation structure, not a pair of global null total orders.
