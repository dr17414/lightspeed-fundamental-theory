# Stage 5C Acceptance Specification — Independent Audit

Audit baseline: `c5313c4d1b7b21a82d8a63bb57ce830f2ef1f954` (`main`, 2026-08-26)

Audit target: the C0–C11 draft in `docs/handoff_v2.0.md`.

Scope: this document audits the acceptance rules only. It contains **no candidate kernel `K`**, no candidate weight, no interval/rank ansatz, and no recommendation among the candidate materials recorded in the handoff.

---

## 1. Verdict

**Revision required before the draft can be adopted as an acceptance specification.**

C0–C11 already contain the right research instincts: primitive accounting, quotient ambiguity, relabel/sector covariance, information-path analysis, causal support, finite-size control, an external massless benchmark, quantum positivity, delayed mass mixing, and a 4D firewall. However, the current text is still a methodological checklist rather than a pass/fail specification. A candidate could satisfy it by interpretation, by post-selection, or by choosing a convenient meaning of `K` after seeing the result.

Five issues are blocking:

1. **The mathematical type of `K` is undefined.** A kinetic/Dirac operator, evolution kernel, retarded Green function, Feynman propagator, and Wightman two-point function obey different support, adjoint, inverse, and positivity requirements. C5, C7, and C9 currently test different object types as though they were one object.
2. **Stage 5A supplies an orbit, not a canonical representative.** The intrinsic output is a realizer/sector-pair class modulo automorphisms and global sector swap. Treating a concrete labelled pair `(U,V)` or its ranks as freely available can silently add a choice that Stage 5A did not derive.
3. **The quantum two-component structure is under-ledgered.** A two-element set at each event is not yet a complex fermionic state space with an inner product or pairing, adjoint, conjugation, grading, CAR algebra, or basis-phase convention. These may be adopted as universal quantum kinematics, but they must be declared rather than counted as information extracted from the poset.
4. **The validation protocol permits circularity and has no numerical pass rule.** There is no locked calibration/holdout split, test statistic, tolerance, ensemble unit, sample size, or `fail` versus `inconclusive` rule. “Quantify” and “return to” are not executable acceptance conditions.
5. **C8 confuses physical sensitivity with arbitrary distinguishability.** Two independent sprinklings of the same continuum target should become equivalent in the continuum limit, not be rewarded for producing different answers. Conversely, different outputs are meaningful only when a predeclared external target says that they should differ.

Until these are repaired, Stage 5C remains **specification design**, not kernel construction and not a physical Go/No-Go result.

---

## 2. Hidden-primitive audit

The revised ledger must separate five categories. Calling all of them “allowed inputs” would erase the question Stage 5C is meant to test.

| Category | Examples | Required treatment |
|---|---|---|
| Layer-0 physical input | finite set, causal order, counting measure | May enter the construction directly. `P` and `prec` must not be double-counted as independent information. |
| Derived but non-canonical data | order-dimension-2 certificate, realizer orbits, unordered sector pair | Must descend to the relevant quotient. A chosen representative, ordering, tie-break, or orbit weight is not free. |
| Universal mathematical/quantum scaffolding | complex linear combinations, choice of pairing/adjoint, CAR or state-space rules | Must be stated explicitly and must not be reported as “emergent from order.” Any physical choice among inequivalent pairings is a new assumption. |
| Free/calibrated structure | coefficient functions, dimensionful scales, regulator, analytic prescription, boundary/initial state, measure over realizers | Must have a derivation or a declared external source. Fitting it on the same benchmark used for acceptance is circular. |
| Evaluation-only oracle | sprinkling coordinates, continuum metric, density/volume metadata, momentum, gamma/Clifford notation, target propagator, ensemble label | Must be sealed from the construction and used only by a predeclared evaluator. |

The phrase “quantum amplitude/phase is allowed” is presently too broad. An arbitrary phase table or arbitrary isomorphism-invariant phase functional could encode the desired answer, including the whole kernel. The specification must say **where amplitudes live, what assigns them, how they transform, and which parts are primitive versus derived**.

Other common leakage channels that must appear in the ledger are RNG seeds, optimization objectives, canonical-labeling routines, enumeration cutoffs, tolerance choices, and any decision made after inspecting continuum coordinates.

---

## 3. Circular-validation audit

The following paths must be explicitly forbidden:

1. Using sealed null coordinates to choose a realizer, orient `U/V`, resolve a tie, or select the `kappa=1` samples retained for analysis.
2. Tuning normalization, nonlocality range, coefficient functions, or density scaling on the same continuum cases later reported as the external benchmark.
3. Deriving an “independent” reference value with the same evaluator, asymptotic branch, interpolation, or inverse used by the candidate pipeline.
4. Choosing matched control statistics after inspecting which comparison makes the candidate look discriminating.
5. Inferring fermionic positivity by reusing a scalar identity or by defining the two-point function so that the desired positivity formula holds by construction.
6. Restricting to `kappa=1`, a preferred boundary window, or numerically well-behaved samples only after outcomes are known.
7. Changing an `N`-dependent range, cutoff, or tolerance separately at each density until a continuum curve appears.

The entire causet—not an event, link, child, eigenvalue, or momentum sample—is the independent statistical unit unless an explicit dependence model proves otherwise.

---

## 4. C0–C11 line-by-line findings

| ID | Verdict | Gap | Required repair before acceptance |
|---|---|---|---|
| **C0** | Major revision | It mixes primitive, derived, mathematical, calibrated, and oracle data. Concrete `{U,V}` and unrestricted “phase” can smuggle in information. | Use the five-part ledger above. Record every function, constant, scale, prescription, boundary condition, ensemble label, and choice algorithm. Require a provenance path and a transformation law for each. |
| **C1** | Major revision | It covers `kappa>1` but omits order-dimension greater than 2, enumeration failure/caps, and the fact that `kappa=1` still gives an orbit rather than a representative. Restricting to `kappa=1` can also create selection bias and a domain that is unstable under restriction/extension. | Define the mathematical domain before results are seen; distinguish `dim>2`, `kappa>1`, and computationally unresolved cases; require descent to the realizer-orbit quotient; quantify the retained-domain frequency separately at every `N`; define `fail` versus `out of scope` versus `inconclusive`. |
| **C2** | Strengthen | `K approximately equivalent to K'` is undefined and a spectrum-only test can hide label-dependent construction. | Require kernel-level equivariance under each poset isomorphism, including automorphisms; state the induced action on event and sector indices. Stochastic procedures must be equivariant in distribution. Fix exact arithmetic or predeclared numerical tolerances. |
| **C3** | Major revision | Global sector swap is necessary but not the whole basis convention. The use of a two-component complex matrix already assumes linearization, pairing/adjoint, and phase conventions. | Declare the fiber/state-space scaffolding and the allowed global basis-gauge group. Test the complete output and all observables, not only a determinant or spectrum. Do not impose local sector rotations unless a connection rule has independently been supplied. |
| **C4** | Keep core, expand | The information-path idea is sound, but it does not type the objects or lock the final observables. Desired relabel similarity is also mixed together with unwanted algebraic blindness. | Add a second, typed derivation path from kinetic object to Green function/two-point function/observable. Predeclare observables and algebraic failure modes. Use symbolic analysis where possible and a genuinely independent numerical counterexample otherwise. Separate required gauge quotienting from accidental loss of causal information. |
| **C5** | Blocking ambiguity | “If retarded” lets a proposal choose whichever object avoids the test. Support alone does not specify normalization, contact terms, inverse/composition law, or initial/boundary data. | First declare what `K` is. Apply retarded support only to objects for which it is physically appropriate, then state the corresponding composition/inverse and boundary conditions. A non-retarded two-point object needs its own causal/anticommutator condition instead. |
| **C6** | Major revision | Density, total event count, physical volume, and nonlocality scale are conflated. A fixed finite diamond can hide whole-box and boundary dependence. Ensemble-mean convergence can coexist with growing single-sprinkling fluctuations. | Predeclare nested-region and density sequences; hold physical quantities and dimensionless ratios fixed; test bulk stability under domain extension; report ensemble mean **and** fluctuations/concentration; use independent RNG streams and causet-level uncertainty; give numeric thresholds and extrapolation/failure rules. |
| **C7** | Blocking ambiguity | “Set off-diagonal blocks to zero” is representation- and object-type dependent. The same massless Dirac physics can occupy different blocks depending on whether `K` denotes a chiral evolution object, a covariant kinetic operator, or a propagator. “Return to propagation” has no norm or holdout protocol. | State the representation-independent target: two decoupled massless chiral sectors with the correct causal propagation and normalization. Only after the object/basis contract is fixed may this be translated into block conditions. Use sealed coordinates solely for evaluation, compare modulo global sector swap, test distributional/observable convergence on locked holdouts, and report both bias and fluctuations. |
| **C8** | Replace | Requiring two manifoldlike/sprinkling-like causets to give different results may reward noise and contradict continuum universality. If the full poset is an input, mere non-equality is also trivial. | Split the test into (a) a **universality/null control**: independent discretizations of the same target converge to the same physical output distribution, and (b) a **sensitivity/positive control**: targets known independently to differ remain distinguishable after nuisance statistics are matched. Fix targets, matching variables, statistic, and effect threshold before running the candidate. |
| **C9** | Major revision | Momentum-space `slash-p` notation already assumes translation/Lorentz/Clifford structure and is unavailable on a generic finite causet. Fermionic positivity is not pointwise positivity of a matrix and cannot inherit the scalar Stage-3 formula. Pole scans alone do not establish a positive fermionic state or correct normalization. | Separate finite-causet position-space/state positivity from any later continuum spectral test. Derive the fermionic spectral components, inequalities, residues, equal-time/CAR normalization, analytic prescription, and pole/branch criteria from the declared object chain. Calibrate zero counters with planted failures and cross-check positivity through an independent representation. Continuum momentum/gamma data remain evaluation-only. |
| **C10** | Major revision | Passing C9 in the massless theory does not make the mixed theory viable. The location of a “mixing block” is representation dependent, and inserting a free coefficient is not mass emergence. | Distinguish three claims: explicit mass parameter, order-derived effective mass, and dynamical/spontaneous mass. Require an invariant massive benchmark, a continuous massless limit, scaling/units, and a complete rerun of C2–C9 after mixing. No emergence claim is allowed if the mass scale or mixing rule is inserted. |
| **C11** | Strengthen | Marking 1+1-dependent steps is necessary but does not control conclusions and project-status wording. | Define every Stage-5C success as a 1+1D toy feasibility result only. Forbid promotion to a 3+1D spinor/Dirac precursor or evidence for the core emergence hypothesis. A 4D continuation requires a new acceptance specification with independently supplied or derived local Lorentz/Clifford structure. |

---

## 5. Minimum structure of the revised specification

The revised document can retain the names C0–C11, but it must add the following executable contracts before any candidate is admitted:

1. **Claim contract** — exact claim being tested and claims explicitly not licensed.
2. **Object contract** — typed chain among kinetic operator, evolution/retarded inverse, quantum two-point object, and reported observables; no object may silently change meaning between criteria.
3. **Provenance contract** — five-part input ledger plus a no-oracle-leakage dataflow graph.
4. **Domain/quotient contract** — treatment of `dim>2`, all realizer orbits, automorphisms, sector swap, computational caps, and domain stability.
5. **Symmetry contract** — exact kernel-level and observable-level equivariance, including stochastic cases and basis phases.
6. **Continuum/statistical contract** — locked calibration and holdout ensembles, density/region sequences, independent units, uncertainty, tolerances, and stop rules.
7. **Two-axis control contract** — universality and sensitivity tested separately.
8. **Massless physics contract** — representation-independent chiral decoupling, propagation, normalization, and single-sprinkling fluctuation control.
9. **Quantum contract** — fermionic state/spectral positivity, residues/CAR normalization, full analytic stability, and independent cross-check.
10. **Mixing contract** — claim taxonomy, massive benchmark, massless limit, and full post-mixing revalidation.
11. **4D/output firewall** — limits not only the construction but every abstract, README, STATUS entry, and conclusion derived from it.

Each criterion must end with four machine-readable fields: **test**, **pass threshold**, **failure meaning**, and **evidence artifact**. A computational cap or missing evaluator is **inconclusive**, never a pass and never a physical No-Go.

---

## 6. Audit conclusion

The C0–C11 draft should **not** yet be used to accept or reject a candidate. Its conceptual direction is good, but it currently allows hidden representative choices, hidden quantum structure, object-type switching, adaptive validation, and a false discriminability success.

The next legitimate deliverable is a revised, executable acceptance specification incorporating the repairs above. Only after that document is frozen and committed may candidate construction begin.

The “candidate materials” paragraph at the end of handoff §2.3 remains a historical direction record and is intentionally absent from this audit’s acceptance architecture.

---

## 7. Primary references used only to delimit the tests

- Bombelli, Henson & Sorkin, *Discreteness without symmetry breaking: a theorem*, [arXiv:gr-qc/0605006](https://arxiv.org/abs/gr-qc/0605006) — scope of the intrinsic finite-direction/finite-valency obstruction.
- Aslanbeigi, Saravani & Sorkin, *Generalized Causal Set d'Alembertians*, [arXiv:1403.1622](https://arxiv.org/abs/1403.1622) — distinction between a causet operator, its sprinkling average, its retarded continuum operator, nonlocality scale, and single-sprinkling fluctuations.
- X, Dowker & Surya, *Scalar Field Green Functions on Causal Sets*, [arXiv:1701.07212](https://arxiv.org/abs/1701.07212) — Green-function construction is a separately typed problem, not interchangeable with defining a kinetic operator.
- Potting, *The Källén-Lehmann representation for Lorentz-violating field theory*, [arXiv:1112.5739](https://arxiv.org/abs/1112.5739) — fermionic propagators require multiple spectral structures and normalization/sum-rule information.
- Noldus, *Free Fermions on causal sets*, [arXiv:1305.0443](https://arxiv.org/abs/1305.0443) — an existing causal-set fermion construction explicitly encounters mixed-norm/ghost issues, supporting a separate fermionic viability gate.
