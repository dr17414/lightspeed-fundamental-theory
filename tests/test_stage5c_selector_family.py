"""Pure structural regressions for the Stage 5C C8 selector family."""

from dataclasses import dataclass
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analysis.stage5a_kappa import sprinkle_2d  # noqa: E402
from analysis.stage5c_hard_controls import BlindedCase  # noqa: E402
from analysis.stage5c_selector_family import (  # noqa: E402
    CAPACITY_LIMIT,
    DEPTH_ENDPOINTS,
    FROZEN_FAMILY,
    SelectorDomainError,
    SelectorProtocolError,
    SelectorSelectionError,
    admissible_pairs,
    apply_selector,
    capacity_ledger,
    evaluation_order,
    family_capacity,
    past_depth,
    relabel,
    selection_coverage,
)


def _case(n=60, seed=101):
    order = sprinkle_2d(n, np.random.default_rng(seed))
    return BlindedCase(case_id=f"case-{seed}", order=order)


def _as_set(selection):
    return {(int(x), int(y)) for x, y in selection}


def test_pair_domain_is_exactly_the_causal_relations():
    case = _case()
    domain = admissible_pairs(case)
    assert domain.shape[1] == 2
    assert len(_as_set(domain)) == int(case.order.sum())
    assert all(case.order[x, y] for x, y in domain)
    assert not any(x == y for x, y in domain)


def test_api_rejects_raw_arrays_and_payloads_with_extra_metadata():
    case = _case()
    with pytest.raises(SelectorProtocolError):
        admissible_pairs(case.order)  # type: ignore[arg-type]

    @dataclass(frozen=True)
    class LeakyCase:
        case_id: str
        order: np.ndarray
        theta: float

    with pytest.raises(SelectorProtocolError):
        admissible_pairs(LeakyCase("leak", case.order, 0.4))  # type: ignore[arg-type]


def test_api_rejects_non_poset_relation_matrices():
    bad = []
    reflexive = np.eye(3, dtype=bool)
    bad.append(reflexive)
    symmetric = np.zeros((3, 3), dtype=bool)
    symmetric[0, 1] = symmetric[1, 0] = True
    bad.append(symmetric)
    nontransitive = np.zeros((3, 3), dtype=bool)
    nontransitive[0, 1] = nontransitive[1, 2] = True
    bad.append(nontransitive)
    bad.append(np.zeros((2, 3), dtype=bool))
    bad.append(np.zeros((3, 3), dtype=np.int64))
    for index, order in enumerate(bad):
        with pytest.raises(SelectorProtocolError):
            admissible_pairs(BlindedCase(f"bad-{index}", order))


def test_past_depth_gives_minimal_elements_zero():
    case = _case()
    depth = past_depth(case.order)
    minimal = np.flatnonzero(case.order.sum(axis=0) == 0)
    assert minimal.size > 0
    assert np.all(depth[minimal] == 0)
    assert depth.max() > 0


def test_relabel_covariance_uses_permutation_not_its_inverse():
    case = _case()
    permutation = np.roll(np.arange(case.order.shape[0]), 7)
    moved_case = relabel(case, permutation)
    base = apply_selector("links", (), case)
    moved = apply_selector("links", (), moved_case)
    recovered = {(int(permutation[x]), int(permutation[y])) for x, y in moved}
    assert recovered == _as_set(base)
    inverse = np.argsort(permutation)
    wrongly_recovered = {(int(inverse[x]), int(inverse[y])) for x, y in moved}
    assert wrongly_recovered != _as_set(base)


def test_all_registered_selectors_are_deterministic_domain_subsets():
    case = _case()
    domain = _as_set(admissible_pairs(case))
    for name, parameters in evaluation_order():
        try:
            first = apply_selector(name, parameters, case)
        except SelectorSelectionError:
            continue
        second = apply_selector(name, parameters, case)
        assert np.array_equal(first, second)
        assert _as_set(first) <= domain
        assert 0.0 < selection_coverage(first, case) <= 1.0


def test_all_relations_is_the_first_and_has_coverage_one():
    case = _case()
    assert evaluation_order()[0] == ("all_relations", ())
    selection = apply_selector("all_relations", (), case)
    assert _as_set(selection) == _as_set(admissible_pairs(case))
    assert selection_coverage(selection, case) == 1.0


def test_depth_bands_are_half_open_and_partition_related_pairs():
    order = np.triu(np.ones((6, 6), dtype=bool), k=1)
    case = BlindedCase("chain", order)
    selections = [
        _as_set(apply_selector("source_depth_band", (low, high), case))
        for low, high in zip(DEPTH_ENDPOINTS[:-1], DEPTH_ENDPOINTS[1:])
    ]
    assert set().union(*selections) == _as_set(admissible_pairs(case))
    assert sum(len(selection) for selection in selections) == len(set().union(*selections))


def test_empty_selection_is_not_mislabelled_as_out_of_domain():
    order = np.array([[False, True], [False, False]], dtype=bool)
    case = BlindedCase("two-chain", order)
    assert admissible_pairs(case).shape == (1, 2)
    with pytest.raises(SelectorSelectionError):
        apply_selector("interval_exact", (4,), case)


def test_empty_causal_pair_domain_is_reported_separately():
    case = BlindedCase("antichain", np.zeros((8, 8), dtype=bool))
    with pytest.raises(SelectorDomainError):
        admissible_pairs(case)
    with pytest.raises(SelectorDomainError):
        apply_selector("all_relations", (), case)


def test_capacity_counts_parameter_points_and_has_no_unused_headroom():
    assert len(FROZEN_FAMILY) == 4
    assert family_capacity() == 11
    assert family_capacity() == CAPACITY_LIMIT
    assert family_capacity() == sum(member.capacity for member in FROZEN_FAMILY)


def test_capacity_ledger_has_every_required_field_and_no_search_engine():
    required = {
        "name",
        "parameter_points",
        "description_length",
        "source_dependencies",
        "branch_count",
        "free_parameter_count",
        "lookup_entries",
        "optimizer",
        "rng",
    }
    rows = capacity_ledger()
    assert len(rows) == len(FROZEN_FAMILY)
    for row in rows:
        assert set(row) == required
        assert row["description_length"] > 0
        assert row["source_dependencies"]
        assert row["free_parameter_count"] == 0
        assert row["lookup_entries"] == 0
        assert row["optimizer"] == "none"
        assert row["rng"] == "none"


def test_unregistered_members_parameters_and_permutations_are_rejected():
    case = _case()
    with pytest.raises(SelectorProtocolError):
        apply_selector("sector_rank_band", (), case)
    with pytest.raises(SelectorProtocolError):
        apply_selector("interval_exact", (99,), case)
    with pytest.raises(SelectorProtocolError):
        relabel(case, np.zeros(case.order.shape[0], dtype=int))
