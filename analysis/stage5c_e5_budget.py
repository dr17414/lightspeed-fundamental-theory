"""Candidate-independent proposed 6a-E E5 claim-family spending schedule.

This module only allocates nominal local error budgets.  It neither runs a
scientific comparison nor reads a seed, a ledger, an endpoint, or arm data.
Item 8 remains OPEN until the separately required power audit is complete.
"""

from __future__ import annotations

from enum import Enum
from fractions import Fraction
from math import nextafter

from analysis.stage5c_statistical_regions import E2Target, E3Claim


E5_BUDGET_ID = "stage5c-6a-e-e5-lineage-spending-proposal-v0.1"
FAMILY_SIZE = 11
LINEAGE_ALPHA = Fraction(1, 20)


class Split(str, Enum):
    SELECTION = "selection"
    CONFIRMATION = "confirmation"


class RegionClaim(str, Enum):
    E1 = "E1:T-plus-minus-T-minus"
    E2_PLUS = f"E2:{E2Target.PLUS.value}-null-equivalence"
    E2_MINUS = f"E2:{E2Target.MINUS.value}-null-equivalence"
    E3_CHIRAL = f"E3:{E3Claim.CHIRAL_VS_BLIND.value}"
    E3_DIFFUSION = f"E3:{E3Claim.DIFFUSION_VS_BLIND.value}"
    E3_WRONG_SUPPORT = f"E3:{E3Claim.CORRECT_VS_WRONG_SUPPORT.value}"
    E3_BLIND_NULL = f"E3:{E3Claim.SECTOR_BLIND_NULL.value}"


def local_alpha_exact(
    member: int, split: Split, claim: RegionClaim, successor_generation: int = 0
) -> Fraction:
    """Allocate one fixed cell, including a disjoint geometric retry reserve.

    Generation zero is the genesis attempt; generation r>0 is the r-th new
    reviewed protocol in this lineage.  Every generation reserves its own
    cells, even when preceding members or splits were never reached.
    """

    if type(member) is not int or not 1 <= member <= FAMILY_SIZE:
        raise ValueError("member must be an original family position 1..11")
    if not isinstance(split, Split):
        raise ValueError("split must be a registered selection or confirmation")
    if not isinstance(claim, RegionClaim):
        raise ValueError("claim must be one of the seven registered regions")
    if type(successor_generation) is not int or successor_generation < 0:
        raise ValueError("successor generation must be a nonnegative integer")
    return LINEAGE_ALPHA / (
        FAMILY_SIZE * len(Split) * len(RegionClaim) * 2 ** (successor_generation + 1)
    )


def local_alpha(
    member: int, split: Split, claim: RegionClaim, successor_generation: int = 0
) -> float:
    """Convert an exact allocation downward for the existing region builder.

    A binary64 round-to-nearest value can exceed the rational allocation.
    Refuse generations whose positive allocation underflows binary64.
    """

    exact = local_alpha_exact(member, split, claim, successor_generation)
    rounded = float(exact)
    if not rounded:
        raise ValueError("allocation underflows binary64; no scientific test authorized")
    if Fraction.from_float(rounded) > exact:
        rounded = nextafter(rounded, 0.0)
    if not rounded:
        raise ValueError("allocation underflows binary64; no scientific test authorized")
    return rounded
