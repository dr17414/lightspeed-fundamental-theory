"""Stage 5C C8 selector-family structural source of record.

Candidate-independent and contrast-free.  The public API accepts only the
existing ``BlindedCase`` boundary and returns an unweighted subset of causal
pairs.  It never receives a candidate kernel, endpoint, target label, seed,
coordinates, reference-probe features, or sector realizer.

This module freezes the selector *form*.  It does not run or adjudicate full
6a-S: induced-measure stability, effective sample size, and numerical floors
still require the separately frozen smearing and normalisation contracts.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from analysis.stage5c_hard_controls import BlindedCase


CAPACITY_LIMIT = 11
DEPTH_ENDPOINTS = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)
INTERVAL_ORDERS = (1, 2, 3, 4)


class SelectorProtocolError(ValueError):
    """The caller or registered schema violates the frozen protocol."""


class SelectorDomainError(RuntimeError):
    """The input causet has no admissible causal-pair domain."""


class SelectorSelectionError(RuntimeError):
    """A registered selector has no selected pair on this valid input."""


@dataclass(frozen=True)
class SelectorMember:
    """One finite, auditable member of the frozen selector family."""

    name: str
    parameter_points: tuple[tuple, ...]
    form: str
    provenance: str
    source_dependencies: tuple[str, ...]
    branch_count: int = 0
    free_parameter_count: int = 0
    lookup_entries: int = 0
    optimizer: str = "none"
    rng: str = "none"

    @property
    def capacity(self) -> int:
        return len(self.parameter_points)

    @property
    def description_length(self) -> int:
        return len(self.form.encode("utf-8"))


FROZEN_FAMILY: tuple[SelectorMember, ...] = (
    SelectorMember(
        name="all_relations",
        parameter_points=((),),
        form="select every ordered pair x<y",
        provenance="minimal nonlocal selector: the admissible domain itself",
        source_dependencies=("docs/STAGE5C_ACCEPTANCE.md#1.3",),
    ),
    SelectorMember(
        name="links",
        parameter_points=((),),
        form="select every x<y with open-interval cardinality zero",
        provenance="C8.1 frozen link-density diagnostic; all links, not one neighbour",
        source_dependencies=("docs/STAGE5C_C8_4_HARD_CONTROLS.md#4",),
    ),
    SelectorMember(
        name="interval_exact",
        parameter_points=tuple((order,) for order in INTERVAL_ORDERS),
        form="select x<y with open-interval cardinality exactly m, m in {1,2,3,4}",
        provenance="C8.1 frozen interval-abundance orders 1..4, evaluation-only",
        source_dependencies=("docs/STAGE5C_C8_4_HARD_CONTROLS.md#4",),
    ),
    SelectorMember(
        name="endpoint_depth_mass_band",
        parameter_points=tuple(
            (DEPTH_ENDPOINTS[i], DEPTH_ENDPOINTS[i + 1])
            for i in range(len(DEPTH_ENDPOINTS) - 1)
        ),
        form=(
            "select x<y by pair-mass midquantile of "
            "past_depth(x)+future_depth(y) in [lo,hi), final band [lo,1]"
        ),
        provenance=(
            "order-dual endpoint-depth score on causal pairs; C8.1 frozen "
            "height-CDF grid 0.2,0.4,0.6,0.8 supplies the closed quantile grid"
        ),
        source_dependencies=("docs/STAGE5C_C8_4_HARD_CONTROLS.md#4",),
        branch_count=1,
    ),
)


def family_capacity(members: tuple[SelectorMember, ...] = FROZEN_FAMILY) -> int:
    """Count finite parameter points, never just top-level member names."""
    return sum(member.capacity for member in members)


def evaluation_order(
    members: tuple[SelectorMember, ...] = FROZEN_FAMILY,
) -> tuple[tuple[str, tuple], ...]:
    return tuple(
        (member.name, parameters)
        for member in members
        for parameters in member.parameter_points
    )


def capacity_ledger() -> tuple[dict[str, object], ...]:
    """Complete schema fields required by the selector capacity audit."""
    return tuple(
        {
            "name": member.name,
            "parameter_points": member.capacity,
            "description_length": member.description_length,
            "source_dependencies": member.source_dependencies,
            "branch_count": member.branch_count,
            "free_parameter_count": member.free_parameter_count,
            "lookup_entries": member.lookup_entries,
            "optimizer": member.optimizer,
            "rng": member.rng,
        }
        for member in FROZEN_FAMILY
    )


def _validated_case(case: BlindedCase) -> np.ndarray:
    if not isinstance(case, BlindedCase):
        raise SelectorProtocolError("selector accepts BlindedCase only")
    if set(vars(case)) != {"case_id", "order"}:
        raise SelectorProtocolError("selector payload contains forbidden metadata")
    if not isinstance(case.case_id, str):
        raise SelectorProtocolError("case_id must be an opaque string")
    order = np.asarray(case.order)
    if order.dtype != np.bool_ or order.ndim != 2 or order.shape[0] != order.shape[1]:
        raise SelectorProtocolError("order must be a square boolean matrix")
    if np.any(np.diag(order)):
        raise SelectorProtocolError("order must be irreflexive")
    if np.any(order & order.T):
        raise SelectorProtocolError("order must be asymmetric")
    composed = (order.astype(np.int32) @ order.astype(np.int32)) > 0
    if np.any(composed & ~order):
        raise SelectorProtocolError("order must be transitively closed")
    return order


def _admissible_pairs(order: np.ndarray) -> np.ndarray:
    return np.argwhere(order)


def admissible_pairs(case: BlindedCase) -> np.ndarray:
    """Frozen domain D: every ordered causally related pair."""
    order = _validated_case(case)
    pairs = _admissible_pairs(order)
    if pairs.shape[0] == 0:
        raise SelectorDomainError("empty causal-pair domain")
    return pairs


def interval_cardinalities(order: np.ndarray) -> np.ndarray:
    relation = order.astype(np.int32)
    return relation @ relation


def past_depth(order: np.ndarray) -> np.ndarray:
    """Longest-chain past depth; minimal elements have depth zero."""
    depth = np.zeros(order.shape[0], dtype=np.int64)
    for element in np.argsort(order.sum(axis=0), kind="stable"):
        predecessors = np.flatnonzero(order[:, element])
        if predecessors.size:
            depth[element] = 1 + int(depth[predecessors].max())
    return depth


def _rule_all_relations(order: np.ndarray, _parameters: tuple) -> np.ndarray:
    return _admissible_pairs(order)


def _rule_links(order: np.ndarray, _parameters: tuple) -> np.ndarray:
    return np.argwhere(order & (interval_cardinalities(order) == 0))


def _rule_interval_exact(order: np.ndarray, parameters: tuple) -> np.ndarray:
    (wanted,) = parameters
    return np.argwhere(order & (interval_cardinalities(order) == wanted))


def _rule_endpoint_depth_mass_band(order: np.ndarray, parameters: tuple) -> np.ndarray:
    low, high = parameters
    pairs = _admissible_pairs(order)
    if pairs.shape[0] == 0:
        return pairs
    past = past_depth(order)
    future = past_depth(order.T)
    score = past[pairs[:, 0]] + future[pairs[:, 1]]
    pair_mass_midquantile = np.empty(len(pairs), dtype=float)
    cumulative = 0
    for value in np.unique(score):
        mask = score == value
        mass = int(mask.sum())
        pair_mass_midquantile[mask] = (cumulative + 0.5 * mass) / len(pairs)
        cumulative += mass
    if high == 1.0:
        inside = (pair_mass_midquantile >= low) & (pair_mass_midquantile <= high)
    else:
        inside = (pair_mass_midquantile >= low) & (pair_mass_midquantile < high)
    return pairs[inside]


_RULES = {
    "all_relations": _rule_all_relations,
    "links": _rule_links,
    "interval_exact": _rule_interval_exact,
    "endpoint_depth_mass_band": _rule_endpoint_depth_mass_band,
}


def _registered_member(name: str) -> SelectorMember:
    matches = [member for member in FROZEN_FAMILY if member.name == name]
    if len(matches) != 1:
        raise SelectorProtocolError(f"unregistered selector member: {name}")
    return matches[0]


def apply_selector(
    name: str, parameters: tuple, case: BlindedCase
) -> np.ndarray:
    """Apply one exactly registered parameter point to one blinded case."""
    order = _validated_case(case)
    domain = _admissible_pairs(order)
    if domain.shape[0] == 0:
        raise SelectorDomainError("empty causal-pair domain")
    member = _registered_member(name)
    if parameters not in member.parameter_points:
        raise SelectorProtocolError(
            f"unregistered parameter point for {name}: {parameters}"
        )
    selection = np.asarray(_RULES[name](order, parameters), dtype=np.int64)
    if selection.ndim != 2 or selection.shape[1:] != (2,):
        raise SelectorProtocolError("selector rule returned an invalid pair array")
    if selection.shape[0] == 0:
        raise SelectorSelectionError("registered selector returned no pair")
    if np.unique(selection, axis=0).shape[0] != selection.shape[0]:
        raise SelectorProtocolError("selector rule returned duplicate pairs")
    if not np.all(order[selection[:, 0], selection[:, 1]]):
        raise SelectorProtocolError("selector output is not a subset of D")
    return selection


def selection_coverage(selection: np.ndarray, case: BlindedCase) -> float:
    """Report raw coverage; no numerical pass/fail band is frozen here."""
    return float(np.asarray(selection).shape[0] / admissible_pairs(case).shape[0])


def relabel(case: BlindedCase, permutation: np.ndarray) -> BlindedCase:
    """Return O'[i,j]=O[permutation[i],permutation[j]]."""
    order = _validated_case(case)
    permutation = np.asarray(permutation)
    n = order.shape[0]
    if (
        permutation.shape != (n,)
        or not np.issubdtype(permutation.dtype, np.integer)
        or not np.array_equal(np.sort(permutation), np.arange(n))
    ):
        raise SelectorProtocolError("permutation must be a bijection of case labels")
    return BlindedCase(case_id=case.case_id, order=order[np.ix_(permutation, permutation)])


def _source_of_record() -> None:
    print("member               points  desc-bytes  branches  free  lookup  optimizer  rng")
    for row in capacity_ledger():
        print(
            f"{row['name']:20s} {row['parameter_points']:6d} "
            f"{row['description_length']:11d} {row['branch_count']:9d} "
            f"{row['free_parameter_count']:5d} {row['lookup_entries']:7d} "
            f"{row['optimizer']:9s} {row['rng']}"
        )
    print(f"capacity: {family_capacity()} (closed limit {CAPACITY_LIMIT})")
    print("evaluation order:", evaluation_order())


if __name__ == "__main__":
    _source_of_record()
