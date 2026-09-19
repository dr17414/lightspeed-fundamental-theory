"""Check the proposed E5 family against the frozen region evaluators."""

from fractions import Fraction

import pytest

from analysis.stage5c_e5_budget import (
    FAMILY_SIZE,
    LINEAGE_ALPHA,
    RegionClaim,
    Split,
    local_alpha,
    local_alpha_exact,
)
from analysis.stage5c_statistical_regions import (
    E2Target,
    E3Claim,
    MAX_LOCAL_ALPHA,
)


def test_complete_claim_family_matches_region_gate_identifiers():
    assert {claim.value for claim in RegionClaim} == {
        "E1:T-plus-minus-T-minus",
        *(f"E2:{target.value}-null-equivalence" for target in E2Target),
        *(f"E3:{claim.value}" for claim in E3Claim),
    }
    assert len(RegionClaim) == 7


def test_successor_reserve_cannot_recycle_unreached_positions_or_splits():
    all_cells = [
        (member, split, claim)
        for member in range(1, FAMILY_SIZE + 1)
        for split in Split
        for claim in RegionClaim
    ]
    assert len(all_cells) == 154
    for generation in range(8):
        spent_if_all_reached = sum(
            (local_alpha_exact(*cell, generation) for cell in all_cells), Fraction()
        )
        assert spent_if_all_reached == LINEAGE_ALPHA / 2 ** (generation + 1)
    total_first_eight = sum(
        (local_alpha_exact(*cell, generation) for generation in range(8)
         for cell in all_cells), Fraction()
    )
    assert total_first_eight + LINEAGE_ALPHA / 2**8 == LINEAGE_ALPHA
    assert local_alpha_exact(1, Split.SELECTION, RegionClaim.E1, 1) == (
        local_alpha_exact(1, Split.SELECTION, RegionClaim.E1, 0) / 2
    )


def test_float_conversion_never_increases_the_exact_scientific_allocation():
    for generation in (0, 1, 17, 700):
        exact = local_alpha_exact(11, Split.CONFIRMATION, RegionClaim.E3_WRONG_SUPPORT, generation)
        submitted = local_alpha(11, Split.CONFIRMATION, RegionClaim.E3_WRONG_SUPPORT, generation)
        assert 0 < Fraction.from_float(submitted) <= exact
        assert submitted <= MAX_LOCAL_ALPHA
    with pytest.raises(ValueError, match="underflows"):
        local_alpha(1, Split.SELECTION, RegionClaim.E1, 2000)


@pytest.mark.parametrize(
    "member,split,claim,generation",
    [
        (0, Split.SELECTION, RegionClaim.E1, 0),
        (12, Split.SELECTION, RegionClaim.E1, 0),
        (True, Split.SELECTION, RegionClaim.E1, 0),
        (1, "confirmation", RegionClaim.E1, 0),
        (1, Split.SELECTION, "E1:T-plus-minus-T-minus", 0),
        (1, Split.SELECTION, RegionClaim.E1, -1),
        (1, Split.SELECTION, RegionClaim.E1, True),
    ],
)
def test_unregistered_cells_fail_closed(member, split, claim, generation):
    with pytest.raises(ValueError):
        local_alpha_exact(member, split, claim, generation)
