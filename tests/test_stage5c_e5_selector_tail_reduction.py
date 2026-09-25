"""Deterministic reductions for the remaining Gate-A selector tail.

These tests use no generator, RNG, seed, arm identity, or candidate kernel.
They exercise the frozen selector on finite permutation orders and lock only
structural reductions; they do not estimate a registered failure probability.
"""

from itertools import permutations

import numpy as np
import pytest

from analysis.stage5c_hard_controls import BlindedCase
from analysis.stage5c_selector_family import (
    SelectorDomainError,
    SelectorSelectionError,
    apply_selector,
    past_depth,
)


def _permutation_order(permutation: tuple[int, ...]) -> np.ndarray:
    """Order the u-sorted points by their v-rank permutation."""

    rank = np.asarray(permutation)
    index = np.arange(len(permutation))
    return (index[:, None] < index[None, :]) & (rank[:, None] < rank[None, :])


def _rectangle_occupancy(
    permutation: tuple[int, ...], left: int, right: int
) -> int:
    return sum(
        left < middle < right
        and permutation[left] < permutation[middle] < permutation[right]
        for middle in range(len(permutation))
    )


def _score_block_masses(order: np.ndarray) -> tuple[int, ...]:
    pairs = np.argwhere(order)
    past = past_depth(order)
    future = past_depth(order.T)
    score = past[pairs[:, 0]] + future[pairs[:, 1]]
    return tuple(int(np.sum(score == value)) for value in np.unique(score))


def test_interval_exact_empty_event_is_a_many_chamber_permutation_problem():
    """At n=6 the four empty events already contain many order chambers."""

    n = 6
    empty_counts = {wanted: 0 for wanted in (1, 2, 3, 4)}
    for permutation in permutations(range(n)):
        order = _permutation_order(permutation)
        case = BlindedCase(f"permutation-{permutation}", order)
        for wanted in empty_counts:
            expected = {
                (left, right)
                for left in range(n)
                for right in range(left + 1, n)
                if permutation[left] < permutation[right]
                and _rectangle_occupancy(permutation, left, right) == wanted
            }
            try:
                observed = {
                    tuple(pair)
                    for pair in apply_selector("interval_exact", (wanted,), case)
                }
            except (SelectorDomainError, SelectorSelectionError):
                observed = set()
            assert observed == expected
            empty_counts[wanted] += not observed

    # Exact exhaustive chamber counts, including the one antichain chamber.
    # They rule out treating any interval-exact failure as merely antichain.
    assert empty_counts == {1: 194, 2: 439, 3: 614, 4: 696}


def test_empty_depth_band_requires_a_large_adjacent_score_block():
    """Exhaustively lock the 0.4M concentration certificate at n=6."""

    endpoints = tuple(value / 5 for value in range(6))
    checked_empty_bands = 0
    for permutation in permutations(range(6)):
        order = _permutation_order(permutation)
        if not np.any(order):
            continue
        case = BlindedCase(f"depth-{permutation}", order)
        masses = _score_block_masses(order)
        total = sum(masses)
        padded = (0, *masses, 0)
        adjacent_max = max(
            padded[index] + padded[index + 1]
            for index in range(len(padded) - 1)
        )
        for low, high in zip(endpoints[:-1], endpoints[1:]):
            try:
                apply_selector("endpoint_depth_mass_band", (low, high), case)
            except SelectorSelectionError:
                checked_empty_bands += 1
                # Midpoints of consecutive mass blocks differ by half their
                # combined mass.  Skipping a width-1/5 band therefore needs
                # an adjacent (boundary zero included) mass of at least 2/5.
                assert 5 * adjacent_max >= 2 * total

    assert checked_empty_bands > 0


def test_depth_band_partition_does_not_make_each_band_nonempty():
    """A height-two complete bipartite order puts every pair at one midpoint."""

    order = np.zeros((6, 6), dtype=bool)
    order[:3, 3:] = True
    case = BlindedCase("height-two-tie-block", order)
    endpoints = tuple(value / 5 for value in range(6))
    selected = []
    for low, high in zip(endpoints[:-1], endpoints[1:]):
        try:
            selected.append(
                len(apply_selector("endpoint_depth_mass_band", (low, high), case))
            )
        except SelectorSelectionError:
            selected.append(0)

    assert selected == [0, 0, 9, 0, 0]

