"""Exact likelihood-moment targets for the Gate-A selector bucket.

These tests use rational arithmetic only.  They do not call the generator,
RNG, selector, producer, arm data, or any candidate kernel.
"""

from fractions import Fraction
from math import comb


Q_COEFFICIENTS = (Fraction(1), Fraction(-6), Fraction(6))
BETA_STAR = Fraction(48035549, 96000000000000)


def _multiply(
    left: tuple[Fraction, ...], right: tuple[Fraction, ...]
) -> tuple[Fraction, ...]:
    product = [Fraction(0)] * (len(left) + len(right) - 1)
    for left_degree, left_value in enumerate(left):
        for right_degree, right_value in enumerate(right):
            product[left_degree + right_degree] += left_value * right_value
    return tuple(product)


def _q_moments(maximum_power: int) -> tuple[Fraction, ...]:
    polynomial = (Fraction(1),)
    moments = []
    for _ in range(maximum_power + 1):
        moments.append(
            sum(
                coefficient / (degree + 1)
                for degree, coefficient in enumerate(polynomial)
            )
        )
        polynomial = _multiply(polynomial, Q_COEFFICIENTS)
    return tuple(moments)


def _likelihood_moment(theta: Fraction, power: int) -> Fraction:
    moments = _q_moments(power)
    return sum(
        Fraction(comb(power, index))
        * theta**index
        * moments[index] ** 2
        for index in range(power + 1)
    )


def test_q_moments_are_exact_for_the_frozen_density_polynomial():
    assert _q_moments(10) == (
        Fraction(1),
        Fraction(0),
        Fraction(1, 5),
        Fraction(2, 35),
        Fraction(3, 35),
        Fraction(4, 77),
        Fraction(53, 1001),
        Fraction(6, 143),
        Fraction(95, 2431),
        Fraction(1576, 46189),
        Fraction(1449, 46189),
    )


def test_frozen_holder_targets_fit_the_selector_bucket_exactly():
    # Each tuple is (theta, N, integer Holder power, uniform-event target).
    # The decimal-looking targets are exact terminating rationals and are
    # deliberately rounded down from the corresponding algebraic root.
    targets = (
        (Fraction(-2, 5), 64, 10, Fraction(156, 10**10)),
        (Fraction(-2, 5), 96, 8, Fraction(655, 10**11)),
        (Fraction(-2, 5), 128, 7, Fraction(309, 10**11)),
        (Fraction(2, 5), 64, 9, Fraction(115, 10**10)),
        (Fraction(2, 5), 96, 7, Fraction(483, 10**11)),
        (Fraction(2, 5), 128, 7, Fraction(230, 10**11)),
    )

    for theta, sample_size, power, uniform_target in targets:
        moment = _likelihood_moment(theta, power)
        assert moment**sample_size * uniform_target ** (power - 1) <= (
            BETA_STAR**power
        )

        # The Holder envelope is strictly less demanding than the earlier
        # pointwise-density envelope beta_star / p_max**N.
        p_max = Fraction(6, 5) if theta < 0 else Fraction(7, 5)
        assert uniform_target > BETA_STAR / p_max**sample_size
